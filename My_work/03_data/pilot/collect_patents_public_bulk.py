from __future__ import annotations

import argparse
import hashlib
import heapq
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from common import OUT_DIR, base_record, load_queries, write_jsonl

DEFAULT_BASE = "https://s3.amazonaws.com/data.patentsview.org/download"


def stable_score(patent_id: str, family: str) -> int:
    h = hashlib.sha256(f"{family}|{patent_id}".encode("utf-8")).hexdigest()
    return int(h[:16], 16)


def download(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        print(f"reuse {dest} ({dest.stat().st_size} bytes)")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length") or 0)
        got = 0
        with dest.open("wb") as f:
            for chunk in r.iter_content(chunk_size=8 * 1024 * 1024):
                if not chunk:
                    continue
                f.write(chunk)
                got += len(chunk)
                if total:
                    print(f"download {dest.name}: {got}/{total}", flush=True)
                else:
                    print(f"download {dest.name}: {got}", flush=True)


def find_col(columns: list[str], aliases: list[str]) -> str | None:
    lower = {c.lower(): c for c in columns}
    for a in aliases:
        if a.lower() in lower:
            return lower[a.lower()]
    return None


def normalize_date(value: object) -> str | None:
    if value is None or pd.isna(value):
        return None
    s = str(value).strip()
    if not s:
        return None
    if len(s) == 8 and s.isdigit():
        return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
    return s[:10]


def scan_abstracts(zip_path: Path, per_family_pool: int, chunksize: int) -> dict[str, dict[str, Any]]:
    q = load_queries()
    ai_terms = [t.lower() for t in q["ai_terms"]]
    family_terms = {fam: [t.lower() for t in cfg["terms"]] for fam, cfg in q["families"].items()}
    heaps: dict[str, list[tuple[int, str, str, list[str]]]] = {fam: [] for fam in family_terms}
    scanned = 0

    for chunk in pd.read_csv(zip_path, sep="\t", dtype=str, chunksize=chunksize, on_bad_lines="skip"):
        cols = list(chunk.columns)
        idc = find_col(cols, ["patent_id", "id", "patent_number"])
        ac = find_col(cols, ["patent_abstract", "abstract"])
        if not idc or not ac:
            raise RuntimeError(f"Could not resolve id/abstract columns from {cols[:30]}")
        for _, r in chunk.iterrows():
            scanned += 1
            pid = str(r.get(idc) or "").strip()
            abstract = str(r.get(ac) or "")
            if not pid or not abstract or abstract == "nan":
                continue
            lower = abstract.lower()
            ai_hits = sorted({t for t in ai_terms if t in lower})
            if not ai_hits:
                continue
            for fam, terms in family_terms.items():
                if not any(t in lower for t in terms):
                    continue
                score = stable_score(pid, fam)
                item = (-score, pid, abstract, ai_hits)
                heap = heaps[fam]
                if len(heap) < per_family_pool:
                    heapq.heappush(heap, item)
                elif score < -heap[0][0]:
                    heapq.heapreplace(heap, item)
        if scanned % 1_000_000 < chunksize:
            print(f"scanned abstract rows: {scanned}; retained pools: {sum(len(x) for x in heaps.values())}", flush=True)

    merged: dict[str, dict[str, Any]] = {}
    for fam, heap in heaps.items():
        for _, pid, abstract, ai_hits in heap:
            rec = merged.setdefault(pid, {"patent_id": pid, "abstract": abstract, "candidate_families": set(), "ai_hits": set()})
            rec["candidate_families"].add(fam)
            rec["ai_hits"].update(ai_hits)
    print(f"abstract scan complete: scanned={scanned}, unique_candidates={len(merged)}")
    return merged


def join_patent_metadata(zip_path: Path, candidates: dict[str, dict[str, Any]], cutoff: str, chunksize: int) -> list[dict[str, Any]]:
    wanted = set(candidates)
    found: dict[str, dict[str, Any]] = {}
    for chunk in pd.read_csv(zip_path, sep="\t", dtype=str, chunksize=chunksize, on_bad_lines="skip"):
        cols = list(chunk.columns)
        idc = find_col(cols, ["patent_id", "id", "patent_number"])
        tc = find_col(cols, ["patent_title", "title"])
        dc = find_col(cols, ["patent_date", "date", "publication_date"])
        typec = find_col(cols, ["patent_type", "type"])
        if not idc:
            raise RuntimeError(f"Could not resolve patent id column from {cols[:30]}")
        sub = chunk[chunk[idc].astype(str).isin(wanted)]
        for _, r in sub.iterrows():
            pid = str(r.get(idc))
            event_date = normalize_date(r.get(dc)) if dc else None
            if event_date and event_date > cutoff:
                continue
            found[pid] = {
                "title": str(r.get(tc) or "") if tc else "",
                "date": event_date,
                "patent_type": str(r.get(typec) or "") if typec else None,
            }
        if len(found) >= len(wanted):
            break
    rows: list[dict[str, Any]] = []
    for pid, meta in found.items():
        c = candidates[pid]
        rec = base_record("patent", pid, title=meta["title"], text=c["abstract"], query_id="PV-PUBLIC-BULK-PILOT")
        rec.update({
            "event_date": meta["date"],
            "patent_id": pid,
            "application_id": None,
            "filing_date": None,
            "publication_date": meta["date"],
            "assignee": None,
            "inventors": [],
            "cpc_codes": [],
            "ipc_codes": [],
            "claims_evidence": None,
            "cited_patents": [],
            "cited_non_patent_literature": [],
            "candidate_families": sorted(c["candidate_families"]),
            "retrieved_by_ai_terms": sorted(c["ai_hits"]),
            "formal_event_cutoff": cutoff,
            "patentsview_patent_type": meta["patent_type"],
            "sampling_method": "public_bulk_abstract_scan_deterministic_family_pool",
        })
        rows.append(rec)
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-total", type=int, default=500)
    ap.add_argument("--per-family-pool", type=int, default=160)
    ap.add_argument("--chunksize", type=int, default=200000)
    ap.add_argument("--cutoff", default="2026-06-30")
    ap.add_argument("--cache-dir", default=".cache_patentsview")
    ap.add_argument("--base-url", default=DEFAULT_BASE)
    args = ap.parse_args()

    cache = Path(args.cache_dir)
    abstract_zip = cache / "g_patent_abstract.tsv.zip"
    patent_zip = cache / "g_patent.tsv.zip"
    download(f"{args.base_url}/g_patent_abstract.tsv.zip", abstract_zip)
    download(f"{args.base_url}/g_patent.tsv.zip", patent_zip)

    candidates = scan_abstracts(abstract_zip, args.per_family_pool, args.chunksize)
    rows = join_patent_metadata(patent_zip, candidates, args.cutoff, args.chunksize)
    rows.sort(key=lambda r: stable_score(r["patent_id"], "GLOBAL"))
    n = write_jsonl(OUT_DIR / "patent_candidates.jsonl", rows[: args.max_total])
    print(f"wrote {n} public PatentsView patent candidates with date <= {args.cutoff}")


if __name__ == "__main__":
    main()
