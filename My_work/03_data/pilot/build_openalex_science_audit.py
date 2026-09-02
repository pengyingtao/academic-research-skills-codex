from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from common import OUT_DIR

CANDIDATES = OUT_DIR / "openalex_boolean_candidates.jsonl"
SCREENED = OUT_DIR / "openalex_boolean_screened.jsonl"


def load(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def main() -> None:
    candidates = load(CANDIDATES)
    screened = load(SCREENED)
    screen_by_id = {r.get("source_native_id"): r for r in screened}

    merged = []
    crosswalk: dict[str, Counter[str]] = defaultdict(Counter)
    for c in candidates:
        s = screen_by_id.get(c.get("source_native_id"), {})
        row = {
            "source_type": "science",
            "source_native_id": c.get("source_native_id"),
            "event_date": c.get("event_date"),
            "title_or_name": c.get("title_or_name"),
            "doi": c.get("doi"),
            "venue": c.get("venue"),
            "topics": c.get("topics") or [],
            "candidate_family": c.get("candidate_family"),
            "retrieved_candidate_families": c.get("retrieved_candidate_families") or [c.get("candidate_family")],
            "auto_in_scope": s.get("in_scope"),
            "auto_primary_technology_id": s.get("primary_technology_id"),
            "auto_secondary_technology_ids": s.get("secondary_technology_ids") or [],
            "auto_confidence": s.get("confidence"),
            "auto_false_positive_type": s.get("false_positive_type"),
            "screening_reason": s.get("screening_reason"),
            "evidence_excerpt": (c.get("text_evidence") or "")[:1600],
            "retrieval_evidence_scope": "OpenAlex search covers title/abstract/fulltext; stored Pilot evidence currently includes title metadata plus reconstructed abstract, not fulltext.",
            "ai_prereview_status": None,
            "ai_suggested_in_scope": None,
            "ai_suggested_primary_technology_id": None,
            "ai_review_note": None,
            "gold_status": None,
            "gold_in_scope": None,
            "gold_primary_technology_id": None,
            "reviewer_note": None,
        }
        merged.append(row)
        crosswalk[str(row["candidate_family"] or "NONE")][str(row["auto_primary_technology_id"] or "NONE")] += 1

    # 4 records per retrieval family. Within each family prioritize diversity of
    # automatic outcome/confidence rather than simply taking the first four.
    by_family: dict[str, list[dict]] = defaultdict(list)
    for r in merged:
        by_family[str(r.get("candidate_family") or "NONE")].append(r)

    audit = []
    for i in range(1, 16):
        fam = f"T{i:02d}"
        pool = by_family.get(fam, [])
        pool.sort(key=lambda r: (
            str(r.get("auto_in_scope")),
            str(r.get("auto_confidence")),
            str(r.get("auto_primary_technology_id") or "NONE"),
            str(r.get("source_native_id")),
        ))
        buckets: dict[tuple, list[dict]] = defaultdict(list)
        for r in pool:
            buckets[(r.get("auto_in_scope"), r.get("auto_confidence"), r.get("auto_primary_technology_id"))].append(r)
        keys = list(buckets)
        depth = 0
        chosen = []
        while len(chosen) < 4 and keys:
            added = False
            for k in keys:
                if depth < len(buckets[k]):
                    chosen.append(buckets[k][depth])
                    added = True
                    if len(chosen) == 4:
                        break
            if not added:
                break
            depth += 1
        audit.extend(chosen)

    out_jsonl = OUT_DIR / "openalex_science_audit_60.jsonl"
    with out_jsonl.open("w", encoding="utf-8") as f:
        for r in audit:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    out_csv = OUT_DIR / "openalex_science_audit_60.csv"
    if audit:
        fields = list(audit[0])
        with out_csv.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for r in audit:
                rr = dict(r)
                for field in ["topics", "retrieved_candidate_families", "auto_secondary_technology_ids"]:
                    rr[field] = json.dumps(rr[field], ensure_ascii=False)
                w.writerow(rr)

    crosswalk_payload = {
        "candidate_n": len(candidates),
        "screened_n": len(screened),
        "audit_n": len(audit),
        "audit_design": "4 records per T01-T15 retrieval family with automatic-outcome diversity",
        "retrieval_to_auto_primary": {fam: dict(counter) for fam, counter in crosswalk.items()},
        "guardrail": "Retrieval family is a sampling stratum, not ground truth. Auto primary is model output, not gold.",
        "evidence_note": "OpenAlex full-text search may retrieve a work because of fulltext matches even when the stored abstract lacks the matched AI/family term; this can produce NO_AI_SIGNAL during abstract-based screening and must be treated as a retrieval-evidence mismatch rather than automatically as a classifier error.",
    }
    (OUT_DIR / "openalex_science_crosswalk.json").write_text(
        json.dumps(crosswalk_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(crosswalk_payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
