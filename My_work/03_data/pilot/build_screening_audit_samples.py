from __future__ import annotations

import argparse
import csv
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any

from common import OUT_DIR


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def round_robin_stratified(rows: list[dict[str, Any]], key: str, n: int, seed: int) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        buckets[str(r.get(key) or "NONE")].append(r)
    for vals in buckets.values():
        rng.shuffle(vals)
    labels = sorted(buckets, key=lambda x: (len(buckets[x]), x))
    out: list[dict[str, Any]] = []
    while len(out) < n and labels:
        next_labels: list[str] = []
        for label in labels:
            if len(out) >= n:
                break
            if buckets[label]:
                out.append(buckets[label].pop())
            if buckets[label]:
                next_labels.append(label)
        labels = next_labels
    return out


def compact(row: dict[str, Any], audit_type: str) -> dict[str, Any]:
    return {
        "audit_type": audit_type,
        "source_native_id": row.get("source_native_id"),
        "event_date": row.get("event_date"),
        "title_or_name": row.get("title_or_name"),
        "candidate_family": row.get("candidate_family"),
        "auto_in_scope": row.get("in_scope"),
        "auto_primary_technology_id": row.get("primary_technology_id"),
        "auto_secondary_technology_ids": row.get("secondary_technology_ids") or [],
        "auto_confidence": row.get("confidence"),
        "auto_false_positive_type": row.get("false_positive_type"),
        "auto_orientation": row.get("use_orientation"),
        "artifact_type": row.get("artifact_type"),
        "analysis_role": row.get("analysis_role"),
        "screening_reason": row.get("screening_reason"),
        "evidence_excerpt": (row.get("text_evidence") or "").replace("\n", " ")[:1800],
        "ai_prereview_status": None,
        "ai_suggested_in_scope": None,
        "ai_suggested_primary_technology_id": None,
        "ai_review_note": None,
        "gold_status": None,
        "gold_in_scope": None,
        "gold_primary_technology_id": None,
        "reviewer_note": None,
    }


def write_pair(stem: str, rows: list[dict[str, Any]]) -> None:
    jpath = OUT_DIR / f"{stem}.jsonl"
    cpath = OUT_DIR / f"{stem}.csv"
    with jpath.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    if rows:
        with cpath.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(OUT_DIR / "pilot_screened.jsonl"))
    ap.add_argument("--false-negative-n", type=int, default=60)
    ap.add_argument("--false-positive-n", type=int, default=60)
    ap.add_argument("--seed", type=int, default=20260902)
    args = ap.parse_args()

    rows = load_jsonl(Path(args.input))
    github = [r for r in rows if r.get("source_type") == "open_source"]

    fn_pool = [
        r for r in github
        if not r.get("in_scope") and r.get("false_positive_type") == "NO_AI_SIGNAL"
    ]
    fp_pool = [
        r for r in github
        if r.get("in_scope") is True and (r.get("analysis_role") in (None, "ENGINEERING_SUPPLY"))
    ]

    fn = [compact(r, "CENTRALITY_FALSE_NEGATIVE") for r in round_robin_stratified(fn_pool, "candidate_family", min(args.false_negative_n, len(fn_pool)), args.seed)]
    fp = [compact(r, "IN_SCOPE_FALSE_POSITIVE") for r in round_robin_stratified(fp_pool, "primary_technology_id", min(args.false_positive_n, len(fp_pool)), args.seed + 1)]

    write_pair("centrality_false_negative_audit", fn)
    write_pair("in_scope_false_positive_audit", fp)

    summary = {
        "screening_version": "1.3.1",
        "github_total": len(github),
        "centrality_false_negative_pool": len(fn_pool),
        "centrality_false_negative_sample": len(fn),
        "in_scope_false_positive_pool": len(fp_pool),
        "in_scope_false_positive_sample": len(fp),
        "sampling": "round-robin stratified by candidate_family / primary_technology_id",
        "seed": args.seed,
        "guardrail": "Audit samples are not gold until independently reviewed."
    }
    (OUT_DIR / "screening_audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
