from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from common import OUT_DIR, load_queries, write_jsonl
from screen_candidates import screen_supply

PROFILE = "SCIENCE_TITLE_ABSTRACT_V1"
BASE_VERSION = "1.3.2"


def normalize_science_text(text: str) -> str:
    # Academic titles often use hyphenated model names, e.g. graph neural-network
    # or machine-learning. Normalize punctuation without adding external evidence.
    t = re.sub(r"[-‐‑–—_/]+", " ", text or "")
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def screen_science(row: dict[str, Any], q: dict[str, Any]) -> dict[str, Any]:
    work = dict(row)
    original_topics = list(work.get("topics") or [])
    work["title_or_name"] = normalize_science_text(work.get("title_or_name") or "")
    work["text_evidence"] = normalize_science_text(work.get("text_evidence") or "")

    # Critical source-aware separation: OpenAlex topics are platform-generated
    # metadata. Preserve them for later graph/features, but do not let them act as
    # direct semantic evidence for the T01-T15 family classifier.
    work["topics"] = []
    screened = screen_supply(work, q)
    screened["topics"] = original_topics
    screened["source_screening_profile"] = PROFILE
    screened["base_screening_version"] = BASE_VERSION
    screened["science_semantic_evidence"] = "TITLE_PLUS_ABSTRACT_ONLY"
    screened["openalex_topics_role"] = "AUXILIARY_METADATA_NOT_FAMILY_EVIDENCE"
    screened["abstract_present"] = bool((row.get("text_evidence") or "").strip())
    return screened


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="OpenAlex candidate JSONL")
    ap.add_argument("--output", default="openalex_science_screened_v1.jsonl")
    args = ap.parse_args()
    q = load_queries()

    rows: list[dict[str, Any]] = []
    for line in Path(args.input).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("source_type") != "science":
            raise RuntimeError(f"Science screener received non-science source: {row.get('source_type')}")
        rows.append(screen_science(row, q))

    n = write_jsonl(OUT_DIR / Path(args.output).name, rows)
    print(f"wrote {n} Science-profile screened records")


if __name__ == "__main__":
    main()
