from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def load(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def safe_div(a, b):
    return a / b if b else 0.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reviewed", required=True, help="Reviewed JSONL with gold_* fields filled")
    ap.add_argument("--out", default="output/taxonomy_validation_metrics.json")
    args = ap.parse_args()
    rows = load(Path(args.reviewed))
    supply = [r for r in rows if r.get("source_type") != "vulnerability" and r.get("gold_in_scope") is not None]

    tp = sum(1 for r in supply if r.get("in_scope") is True and r.get("gold_in_scope") is True)
    fp = sum(1 for r in supply if r.get("in_scope") is True and r.get("gold_in_scope") is False)
    fn = sum(1 for r in supply if r.get("in_scope") is False and r.get("gold_in_scope") is True)
    screening_precision = safe_div(tp, tp + fp)
    screening_recall = safe_div(tp, tp + fn)
    screening_f1 = safe_div(2 * screening_precision * screening_recall, screening_precision + screening_recall)

    labels = sorted({r.get("gold_primary_technology_id") for r in supply if r.get("gold_in_scope") and r.get("gold_primary_technology_id")})
    per_family = {}
    confusion = defaultdict(Counter)
    for fam in labels:
        ftp = ffp = ffn = 0
        for r in supply:
            if not r.get("gold_in_scope"):
                continue
            gold = r.get("gold_primary_technology_id")
            pred = r.get("primary_technology_id") if r.get("in_scope") else None
            confusion[gold][pred or "NONE"] += 1
            if pred == fam and gold == fam:
                ftp += 1
            elif pred == fam and gold != fam:
                ffp += 1
            elif pred != fam and gold == fam:
                ffn += 1
        p = safe_div(ftp, ftp + ffp)
        rec = safe_div(ftp, ftp + ffn)
        f1 = safe_div(2 * p * rec, p + rec)
        per_family[fam] = {"precision": p, "recall": rec, "f1": f1, "support": sum(1 for r in supply if r.get("gold_primary_technology_id") == fam)}

    macro_f1 = safe_div(sum(v["f1"] for v in per_family.values()), len(per_family))
    orientation_rows = [r for r in supply if r.get("gold_use_orientation")]
    orientation_accuracy = safe_div(sum(1 for r in orientation_rows if r.get("use_orientation") == r.get("gold_use_orientation")), len(orientation_rows))

    vuln = [r for r in rows if r.get("source_type") == "vulnerability"]
    cwe_coverage = safe_div(sum(1 for r in vuln if r.get("cwe_ids")), len(vuln))
    cvss_missing = safe_div(sum(1 for r in vuln if r.get("cvss_base_as_observed") is None), len(vuln))
    kev_missing = safe_div(sum(1 for r in vuln if r.get("kev_status_as_observed") is None), len(vuln))
    epss_missing = safe_div(sum(1 for r in vuln if r.get("epss_score_as_observed") is None), len(vuln))

    result = {
        "reviewed_supply_n": len(supply),
        "reviewed_vulnerability_n": len(vuln),
        "screening": {"precision": screening_precision, "recall": screening_recall, "f1": screening_f1},
        "primary_family_macro_f1": macro_f1,
        "per_family": per_family,
        "orientation_accuracy": orientation_accuracy,
        "vdp_missingness": {"cwe_missing_rate": 1 - cwe_coverage, "cvss_missing_rate": cvss_missing, "kev_missing_rate": kev_missing, "epss_missing_rate": epss_missing},
        "confusion": {k: dict(v) for k, v in confusion.items()},
        "gate_targets": {"screening_precision": 0.90, "primary_family_macro_f1": 0.80, "high_frequency_family_f1": 0.85},
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
