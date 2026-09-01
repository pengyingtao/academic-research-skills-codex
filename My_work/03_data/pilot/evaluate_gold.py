from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def safe_div(a: float, b: float) -> float:
    return a / b if b else 0.0


def prf(tp: int, fp: int, fn: int) -> dict[str, float]:
    p = safe_div(tp, tp + fp)
    r = safe_div(tp, tp + fn)
    f1 = safe_div(2 * p * r, p + r)
    return {"precision": p, "recall": r, "f1": f1, "support_tp": tp, "fp": fp, "fn": fn}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True, help="Gold-review JSONL with prediction + gold fields")
    ap.add_argument("--out", default="output/gate2b_gold_metrics.json")
    args = ap.parse_args()

    rows = [r for r in read_jsonl(Path(args.gold)) if r.get("gold_status") in {"AGREED", "ADJUDICATED"}]
    supply = [r for r in rows if r.get("source_type") in {"science", "patent", "open_source"}]
    vuln = [r for r in rows if r.get("source_type") == "vulnerability"]

    # Binary in-scope metrics for supply.
    tp = sum(bool(r.get("in_scope")) and bool(r.get("gold_in_scope")) for r in supply)
    fp = sum(bool(r.get("in_scope")) and not bool(r.get("gold_in_scope")) for r in supply)
    fn = sum(not bool(r.get("in_scope")) and bool(r.get("gold_in_scope")) for r in supply)
    tn = sum(not bool(r.get("in_scope")) and not bool(r.get("gold_in_scope")) for r in supply)

    # Primary-family metrics only for gold in-scope supply records.
    families = [f"T{i:02d}" for i in range(1, 16)]
    per_family: dict[str, Any] = {}
    confusion: dict[str, Counter[str]] = defaultdict(Counter)
    f1_values: list[float] = []

    for r in supply:
        if not bool(r.get("gold_in_scope")):
            continue
        gold = r.get("gold_primary_technology_id") or "NONE"
        pred = r.get("primary_technology_id") if bool(r.get("in_scope")) else "NONE"
        pred = pred or "NONE"
        confusion[str(gold)][str(pred)] += 1

    for fam in families:
        fam_tp = sum(confusion[fam][pred] for pred in confusion[fam] if pred == fam)
        fam_fn = sum(confusion[fam][pred] for pred in confusion[fam] if pred != fam)
        fam_fp = sum(counter[fam] for gold, counter in confusion.items() if gold != fam)
        m = prf(fam_tp, fam_fp, fam_fn)
        support = sum(confusion[fam].values())
        m["gold_support"] = support
        per_family[fam] = m
        if support > 0:
            f1_values.append(m["f1"])

    macro_f1 = sum(f1_values) / len(f1_values) if f1_values else 0.0

    github = [r for r in supply if r.get("source_type") == "open_source"]
    gh_artifact = [r for r in github if r.get("gold_artifact_type")]
    gh_orientation = [r for r in github if r.get("gold_use_orientation")]
    artifact_acc = safe_div(sum(r.get("artifact_type") == r.get("gold_artifact_type") for r in gh_artifact), len(gh_artifact))
    orient_acc = safe_div(sum(r.get("use_orientation") == r.get("gold_use_orientation") for r in gh_orientation), len(gh_orientation))

    # VDP quality: Txx labels are explicitly prohibited.
    vdp_direct_txx_violations = sum(bool(r.get("primary_technology_id")) for r in vuln)
    vdp_group_eval = [r for r in vuln if r.get("gold_vdp_group")]
    vdp_group_acc = safe_div(sum(r.get("cwe_group") == r.get("gold_vdp_group") for r in vdp_group_eval), len(vdp_group_eval))

    report = {
        "n_finalized_gold": len(rows),
        "n_supply_gold": len(supply),
        "n_vulnerability_gold": len(vuln),
        "supply_in_scope": {**prf(tp, fp, fn), "tn": tn},
        "primary_family_macro_f1": macro_f1,
        "per_family": per_family,
        "confusion_matrix": {gold: dict(counter) for gold, counter in confusion.items()},
        "github": {
            "artifact_type_accuracy": artifact_acc,
            "artifact_type_n": len(gh_artifact),
            "orientation_accuracy": orient_acc,
            "orientation_n": len(gh_orientation),
        },
        "vulnerability": {
            "vdp_group_accuracy": vdp_group_acc,
            "vdp_group_n": len(vdp_group_eval),
            "direct_txx_label_violations": vdp_direct_txx_violations,
        },
        "gate_thresholds": {
            "min_finalized_gold": 300,
            "min_supply_precision": 0.90,
            "min_primary_family_macro_f1": 0.80,
        },
    }
    report["gate_partial_pass"] = bool(
        len(rows) >= 300
        and report["supply_in_scope"]["precision"] >= 0.90
        and macro_f1 >= 0.80
        and vdp_direct_txx_violations == 0
    )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
