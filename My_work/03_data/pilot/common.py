from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import requests
import yaml

ROOT = Path(__file__).resolve().parent
QUERY_PACK = ROOT / "query_pack_v1.yaml"
OUT_DIR = ROOT / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_queries() -> dict[str, Any]:
    with QUERY_PACK.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def stable_id(source_type: str, native_id: str) -> str:
    raw = f"{source_type}:{native_id}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    n = 0
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    return n


def request_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    timeout: int = 45,
    max_retries: int = 5,
    min_interval: float = 0.25,
) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(max_retries):
        try:
            r = requests.request(method, url, headers=headers, params=params, timeout=timeout)
            if r.status_code in (403, 429):
                retry_after = r.headers.get("retry-after")
                wait = float(retry_after) if retry_after else min(60.0, 2 ** attempt)
                time.sleep(wait)
                continue
            r.raise_for_status()
            time.sleep(min_interval)
            return r.json()
        except Exception as exc:  # pragma: no cover - operational path
            last_error = exc
            time.sleep(min(30.0, 2 ** attempt))
    raise RuntimeError(f"request failed after {max_retries} attempts: {url}") from last_error


def env(name: str, required: bool = False) -> str | None:
    value = os.getenv(name)
    if required and not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def base_record(source_type: str, native_id: str, *, title: str = "", text: str = "", query_id: str = "") -> dict[str, Any]:
    observed = now_iso()
    return {
        "record_id": stable_id(source_type, native_id),
        "source_type": source_type,
        "source_native_id": native_id,
        "observed_at": observed,
        "event_date": None,
        "source_modified_at": None,
        "title_or_name": title,
        "text_evidence": text,
        "retrieval_query_id": query_id,
        "retrieved_by_terms": [],
        "taxonomy_version": "1.1",
        "keyword_version": "1.3.2",
        "in_scope": None,
        "confidence": None,
        "screening_reason": None,
        "false_positive_type": None,
    }
