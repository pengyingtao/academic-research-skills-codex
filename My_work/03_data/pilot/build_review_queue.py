from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path

from common import OUT_DIR, write_jsonl


def load(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def key(row):
    return (row.get("source_type"), row.get("source_native_id"))


def compact(row: dict, reasons: list[str]) -> dict:
    evidence = (row.get("text_evidence") or "").replace("\n", " ").strip()
    return {
        "source_type": row.get("source_type"),
        "source_native_id": row.get("source_native_id"),
        "event_date": row.get("event_date"),
        "title_or_name": row.get("title_or_name"),
        "evidence_excerpt": evidence[:1200],
        "candidate_family": row.get("candidate_family"),
        "auto_in_scope": row.get("in_scope"),
        "auto_primary_technology_id": row.get("primary_technology_id"),
        "auto_secondary_technology_ids": row.get("secondary_technology_ids") or [],
        "auto_use_orientation": row.get("use_orientation"),
        "auto_false_positive_type": row.get("false_positive_type"),
        "auto_confidence": row.get("confidence"),
        "artifact_type": row.get("artifact_type"),
        "analysis_role": row.get("analysis_role"),
        "cwe_group": row.get("cwe_group"),
        "review_sampling_reason": reasons,
        "gold_in_scope": None,
        "gold_primary_technology_id": None,
        "gold_secondary_technology_ids": [],
        "gold_use_orientation": None,
        "gold_false_positive_type": None,
        "gold_artifact_type": None,
        "gold_vdp_group": None,
        "reviewer_note": None,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(OUT_DIR / "pilot_screened.jsonl"))
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    rows = load(Path(args.input))
    supply = [r for r in rows if r.get("source_type") != "vulnerability"]
    vuln = [r for r in rows if r.get("source_type") == "vulnerability"]
    lowmed = [r for r in supply if r.get("confidence") in {"LOW", "MEDIUM"}]
    boundary = [r for r in supply if r.get("needs_review") or r.get("secondary_technology_ids")]
    offensive = [r for r in supply if r.get("use_orientation") in {"OFFENSIVE", "DUAL_USE_OFFENSE_PRIMARY", "DUAL_USE_DEFENSE_PRIMARY"} or r.get("false_positive_type") == "OFFENSIVE_ONLY"]

    plan = [
        ("random_supply", supply, 120),
        ("low_medium", lowmed, 80),
        ("family_boundary", boundary, 50),
        ("dual_use_offensive", offensive, 25),
        ("vdp_mapping", vuln, 25),
    ]
    selected: dict[tuple, dict] = {}
    reason_map: dict[tuple, list[str]] = {}
    for reason, pool, target in plan:
        pool = list(pool)
        rng.shuffle(pool)
        for r in pool[:target]:
            selected[key(r)] = r
            reason_map.setdefault(key(r), []).append(reason)

    target_n = min(args.n, len(rows))
    if len(selected) < target_n:
        remaining = [r for r in rows if key(r) not in selected]
        rng.shuffle(remaining)
        for r in remaining:
            if len(selected) >= target_n:
                break
            selected[key(r)] = r
            reason_map.setdefault(key(r), []).append("top_up")

    out = [compact(r, reason_map[k]) for k, r in selected.items()]
    n = write_jsonl(OUT_DIR / "manual_review_queue_compact.jsonl", out)

    csv_path = OUT_DIR / "manual_review_queue_compact.csv"
    if out:
        fields = list(out[0].keys())
        with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for row in out:
                csv_row = dict(row)
                for field in ["auto_secondary_technology_ids", "review_sampling_reason", "gold_secondary_technology_ids"]:
                    csv_row[field] = json.dumps(csv_row[field], ensure_ascii=False)
                w.writerow(csv_row)
    print(f"wrote {n} compact review records")


if __name__ == "__main__":
    main()
