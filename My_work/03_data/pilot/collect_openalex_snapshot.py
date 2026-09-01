from __future__ import annotations

import argparse
import gzip
import hashlib
import heapq
import json
from pathlib import Path
from typing import Any

from common import OUT_DIR, base_record, load_queries, write_jsonl
from collect_openalex import reconstruct_abstract


def stable_score(work_id: str, family: str) -> int:
    h = hashlib.sha256(f"{family}|{work_id}".encode("utf-8")).hexdigest()
    return int(h[:16], 16)


def matches(text: str, terms: list[str]) -> list[str]:
    lower = text.lower()
    return [t for t in terms if t.lower() in lower]


def main() -> None:
    ap = argparse.ArgumentParser(description="Build a stratified OpenAlex Pilot sample from a local snapshot.")
    ap.add_argument("--snapshot-root", required=True, help="OpenAlex snapshot root containing data/works/**/*.gz")
    ap.add_argument("--per-family", type=int, default=70)
    ap.add_argument("--max-total", type=int, default=1000)
    ap.add_argument("--cutoff", default="2026-06-30")
    ap.add_argument("--progress-every", type=int, default=500000)
    args = ap.parse_args()

    q = load_queries()
    ai_terms = q["ai_terms"]
    family_terms = {fam: cfg["terms"] for fam, cfg in q["families"].items()}

    # For each family retain the deterministic lowest-hash candidates. This avoids
    # depending on snapshot shard/file order while keeping memory bounded.
    heaps: dict[str, list[tuple[int, dict[str, Any]]]] = {fam: [] for fam in family_terms}
    seen_ids: set[str] = set()
    scanned = 0

    files = sorted(Path(args.snapshot_root).glob("data/works/**/*.gz"))
    if not files:
        raise FileNotFoundError("No OpenAlex work .gz files found under data/works/**/*.gz")

    for gz_path in files:
        with gzip.open(gz_path, "rt", encoding="utf-8") as fh:
            for line in fh:
                scanned += 1
                if args.progress_every and scanned % args.progress_every == 0:
                    counts = {k: len(v) for k, v in heaps.items()}
                    print(f"scanned={scanned} retained={sum(counts.values())} by_family={counts}")

                try:
                    w = json.loads(line)
                except json.JSONDecodeError:
                    continue

                work_id = w.get("id") or ""
                if not work_id or work_id in seen_ids:
                    continue
                pub_date = w.get("publication_date") or ""
                if pub_date and pub_date[:10] > args.cutoff:
                    continue

                title = w.get("title") or w.get("display_name") or ""
                abstract = reconstruct_abstract(w.get("abstract_inverted_index"))
                text = f"{title}\n{abstract}"
                ai_hits = matches(text, ai_terms)
                if not ai_hits:
                    continue

                matched_families = [fam for fam, terms in family_terms.items() if matches(text, terms)]
                if not matched_families:
                    continue

                seen_ids.add(work_id)
                for fam in matched_families:
                    score = stable_score(work_id, fam)
                    rec = base_record("science", work_id, title=title, text=abstract, query_id=f"OA-SNAPSHOT-{fam}")
                    rec.update({
                        "event_date": pub_date or None,
                        "doi": w.get("doi"),
                        "openalex_id": work_id,
                        "publication_date": pub_date or None,
                        "venue": (((w.get("primary_location") or {}).get("source") or {}).get("display_name")),
                        "topics": [t.get("display_name") for t in (w.get("topics") or []) if t.get("display_name")],
                        "authors": [((a.get("author") or {}).get("display_name")) for a in (w.get("authorships") or []) if (a.get("author") or {}).get("display_name")],
                        "institutions": sorted({i.get("display_name") for a in (w.get("authorships") or []) for i in (a.get("institutions") or []) if i.get("display_name")}),
                        "cited_by_count_as_observed": w.get("cited_by_count"),
                        "referenced_works": w.get("referenced_works") or [],
                        "candidate_family": fam,
                        "candidate_families": matched_families,
                        "retrieved_by_ai_terms": ai_hits,
                        "formal_event_cutoff": args.cutoff,
                        "sampling_method": "deterministic_low_hash_within_family",
                    })
                    heap = heaps[fam]
                    item = (-score, rec)
                    if len(heap) < args.per_family:
                        heapq.heappush(heap, item)
                    elif score < -heap[0][0]:
                        heapq.heapreplace(heap, item)

    merged: dict[str, dict[str, Any]] = {}
    for fam, heap in heaps.items():
        for _, rec in heap:
            wid = rec["source_native_id"]
            if wid not in merged:
                merged[wid] = rec
            else:
                fams = set(merged[wid].get("candidate_families") or [])
                fams.update(rec.get("candidate_families") or [])
                merged[wid]["candidate_families"] = sorted(fams)

    rows = sorted(merged.values(), key=lambda r: stable_score(r["source_native_id"], "GLOBAL"))[: args.max_total]
    n = write_jsonl(OUT_DIR / "openalex_candidates.jsonl", rows)
    print(f"scanned {scanned} works; wrote {n} OpenAlex snapshot candidates with publication_date <= {args.cutoff}")


if __name__ == "__main__":
    main()
