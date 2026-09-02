from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def parse_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    s = str(value).strip().lower()
    if s in {"true", "1", "yes", "y"}:
        return True
    if s in {"false", "0", "no", "n"}:
        return False
    return None


def read_blind_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["gold_in_scope"] = parse_bool(r.get("gold_in_scope"))
        for key in ["gold_primary_technology_id", "gold_use_orientation", "gold_artifact_type", "gold_vdp_group"]:
            if not (r.get(key) or "").strip():
                r[key] = None
    return rows


def merge_blinded_gold(blind_csv: Path, prediction_map: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    gold_rows = read_blind_csv(blind_csv)
    preds = read_jsonl(prediction_map)

    gold_by_id = {str(r.get("review_id")): r for r in gold_rows if r.get("review_id")}
    pred_by_id = {str(r.get("review_id")): r for r in preds if r.get("review_id")}
    if len(gold_by_id) != len(gold_rows):
        raise RuntimeError("Duplicate or missing review_id in blind gold CSV")
    if len(pred_by_id) != len(preds):
        raise RuntimeError("Duplicate or missing review_id in prediction map")

    missing_predictions = sorted(set(gold_by_id) - set(pred_by_id))
    orphan_predictions = sorted(set(pred_by_id) - set(gold_by_id))
    if missing_predictions or orphan_predictions:
        raise RuntimeError(
            f"Blind/prediction review_id mismatch: missing_predictions={len(missing_predictions)}, "
            f"orphan_predictions={len(orphan_predictions)}"
        )

    versions = sorted({str(p.get("screening_version")) for p in preds if p.get("screening_version")})
    if len(versions) != 1:
        raise RuntimeError(f"Prediction map must contain exactly one screening version, found {versions}")

    merged: list[dict[str, Any]] = []
    for review_id, g in gold_by_id.items():
        p = pred_by_id[review_id]
        row = dict(g)
        row.update({
            "in_scope": parse_bool(p.get("auto_in_scope")),
            "primary_technology_id": p.get("auto_primary_technology_id"),
            "secondary_technology_ids": p.get("auto_secondary_technology_ids") or [],
            "use_orientation": p.get("auto_use_orientation"),
            "artifact_type": p.get("auto_artifact_type"),
            "cwe_group": p.get("auto_vdp_group"),
            "confidence": p.get("auto_confidence"),
            "false_positive_type": p.get("auto_false_positive_type"),
            "screening_version": p.get("screening_version"),
        })
        merged.append(row)

    diagnostics = {
        "review_design": "BLINDED_TO_MODEL_PREDICTION",
        "n_blind_rows": len(gold_rows),
        "n_prediction_rows": len(preds),
        "n_merged_rows": len(merged),
        "screening_version": versions[0],
        "review_id_match": True,
    }
    return merged, diagnostics


def safe_div(a: float, b: float) -> float:
    return a / b if b else 0.0


def prf(tp: int, fp: int, fn: int) -> dict[str, float]:
    p = safe_div(tp, tp + fp)
    r = safe_div(tp, tp + fn)
    f1 = safe_div(2 * p * r, p + r)
    return {"precision": p, "recall": r, "f1": f1, "support_tp": tp, "fp": fp, "fn": fn}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", help="Legacy merged gold-review JSONL with prediction + gold fields")
    ap.add_argument("--blind-csv", help="Blinded human-review CSV with gold fields")
    ap.add_argument("--prediction-map", help="Hidden model prediction JSONL keyed by stable review_id")
    ap.add_argument("--out", default="output/gate2b_gold_metrics.json")
    args = ap.parse_args()

    merge_diagnostics: dict[str, Any] | None = None
    if args.blind_csv or args.prediction_map:
        if not (args.blind_csv and args.prediction_map):
            raise SystemExit("--blind-csv and --prediction-map must be provided together")
        all_rows, merge_diagnostics = merge_blinded_gold(Path(args.blind_csv), Path(args.prediction_map))
    elif args.gold:
        all_rows = read_jsonl(Path(args.gold))
    else:
        raise SystemExit("Provide either --gold or both --blind-csv and --prediction-map")

    rows = [r for r in all_rows if r.get("gold_status") in {"AGREED", "ADJUDICATED"}]
    supply = [r for r in rows if r.get("source_type") in {"science", "patent", "open_source"}]
    vuln = [r for r in rows if r.get("source_type") == "vulnerability"]

    tp = sum(bool(r.get("in_scope")) and bool(r.get("gold_in_scope")) for r in supply)
    fp = sum(bool(r.get("in_scope")) and not bool(r.get("gold_in_scope")) for r in supply)
    fn = sum(not bool(r.get("in_scope")) and bool(r.get("gold_in_scope")) for r in supply)
    tn = sum(not bool(r.get("in_scope")) and not bool(r.get("gold_in_scope")) for r in supply)

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

    vdp_direct_txx_violations = sum(bool(r.get("primary_technology_id")) for r in vuln)
    vdp_group_eval = [r for r in vuln if r.get("gold_vdp_group")]
    vdp_group_acc = safe_div(sum(r.get("cwe_group") == r.get("gold_vdp_group") for r in vdp_group_eval), len(vdp_group_eval))

    report = {
        "evaluation_status": "FINAL_GOLD" if len(rows) >= 300 else "INCOMPLETE_GOLD_DO_NOT_USE_AS_GATE_RESULT",
        "merge_diagnostics": merge_diagnostics,
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
        "guardrail": "Metrics from fewer than 300 finalized independent/human gold records are diagnostic only and must not be reported as Gate 2B performance.",
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
