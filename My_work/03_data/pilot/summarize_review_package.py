from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from common import OUT_DIR


def load(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def main() -> None:
    rows = load(OUT_DIR / "manual_review_queue_compact.jsonl")
    supply = [r for r in rows if r.get("source_type") != "vulnerability"]
    vdp = [r for r in rows if r.get("source_type") == "vulnerability"]

    candidate_family = Counter(str(r.get("candidate_family") or "NONE") for r in supply)
    auto_primary = Counter(str(r.get("auto_primary_technology_id") or "NONE") for r in supply)
    confidence = Counter(str(r.get("auto_confidence") or "NONE") for r in supply)
    source = Counter(str(r.get("source_type") or "NONE") for r in rows)
    reasons = Counter()
    for r in rows:
        for reason in r.get("review_sampling_reason") or []:
            reasons[str(reason)] += 1

    expected = [f"T{i:02d}" for i in range(1, 16)]
    candidate_support = {f: candidate_family.get(f, 0) for f in expected}
    auto_primary_support = {f: auto_primary.get(f, 0) for f in expected}

    report = {
        "n": len(rows),
        "source_counts": dict(source),
        "supply_n": len(supply),
        "vdp_n": len(vdp),
        "candidate_family_support": candidate_support,
        "auto_primary_family_support": auto_primary_support,
        "auto_primary_none": auto_primary.get("NONE", 0),
        "confidence_counts": dict(confidence),
        "sampling_reason_counts": dict(reasons),
        "candidate_families_below_10": [f for f, n in candidate_support.items() if n < 10],
        "candidate_families_below_5": [f for f, n in candidate_support.items() if n < 5],
        "interpretation_guardrail": "These are sampling supports based on candidate/automatic labels, not gold family supports. Final gold support may differ after human review.",
    }
    (OUT_DIR / "human_review_sampling_summary.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
