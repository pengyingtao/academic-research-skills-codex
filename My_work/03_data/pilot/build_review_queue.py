from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from common import OUT_DIR, write_jsonl


def load(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def key(row):
    return (row.get("source_type"), row.get("source_native_id"))


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
    selected = {}
    reason_map = {}
    for reason, pool, target in plan:
        pool = list(pool)
        rng.shuffle(pool)
        for r in pool[:target]:
            selected[key(r)] = dict(r)
            reason_map.setdefault(key(r), []).append(reason)

    if len(selected) < min(args.n, len(rows)):
        remaining = [r for r in rows if key(r) not in selected]
        rng.shuffle(remaining)
        for r in remaining:
            if len(selected) >= min(args.n, len(rows)):
                break
            selected[key(r)] = dict(r)
            reason_map.setdefault(key(r), []).append("top_up")

    out = []
    for k, r in selected.items():
        r["review_sampling_reason"] = reason_map[k]
        r["gold_in_scope"] = None
        r["gold_primary_technology_id"] = None
        r["gold_secondary_technology_ids"] = []
        r["gold_use_orientation"] = None
        r["gold_false_positive_type"] = None
        r["reviewer_note"] = None
        out.append(r)

    n = write_jsonl(OUT_DIR / "manual_review_queue.jsonl", out)
    print(f"wrote {n} review records")


if __name__ == "__main__":
    main()
