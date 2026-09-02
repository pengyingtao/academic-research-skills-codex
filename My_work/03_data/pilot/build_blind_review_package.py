from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from common import OUT_DIR, stable_id
from screen_candidates import VERSION


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def review_id_for(row: dict[str, Any]) -> str:
    source_type = str(row.get("source_type") or "unknown")
    native_id = str(row.get("source_native_id") or "")
    return f"G2B-{stable_id(source_type, native_id)[:12].upper()}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(OUT_DIR / "manual_review_queue_compact.jsonl"))
    args = ap.parse_args()

    rows = load_jsonl(Path(args.input))
    blind_rows: list[dict[str, Any]] = []
    prediction_map: list[dict[str, Any]] = []

    for r in rows:
        review_id = review_id_for(r)
        blind_rows.append({
            "review_id": review_id,
            "source_type": r.get("source_type"),
            "source_native_id": r.get("source_native_id"),
            "event_date": r.get("event_date"),
            "title_or_name": r.get("title_or_name"),
            "evidence_excerpt": r.get("evidence_excerpt"),
            "gold_status": "",
            "gold_in_scope": "",
            "gold_primary_technology_id": "",
            "gold_secondary_technology_ids": "",
            "gold_use_orientation": "",
            "gold_artifact_type": "",
            "gold_vdp_group": "",
            "reviewer_confidence": "",
            "reviewer_note": "",
        })
        prediction_map.append({
            "review_id": review_id,
            "source_type": r.get("source_type"),
            "source_native_id": r.get("source_native_id"),
            "auto_in_scope": r.get("auto_in_scope"),
            "auto_primary_technology_id": r.get("auto_primary_technology_id"),
            "auto_secondary_technology_ids": r.get("auto_secondary_technology_ids"),
            "auto_use_orientation": r.get("auto_use_orientation"),
            "auto_artifact_type": r.get("artifact_type"),
            "auto_vdp_group": r.get("cwe_group"),
            "auto_confidence": r.get("auto_confidence"),
            "auto_false_positive_type": r.get("auto_false_positive_type"),
            "screening_version": VERSION,
        })

    # Stable IDs make package regeneration safe across model versions. Sort by
    # review_id so presentation order is deterministic and independent of queue
    # dictionary insertion order.
    blind_rows.sort(key=lambda x: x["review_id"])
    prediction_map.sort(key=lambda x: x["review_id"])

    if len({r["review_id"] for r in blind_rows}) != len(blind_rows):
        raise RuntimeError("Duplicate stable review_id detected")

    blind_csv = OUT_DIR / "human_review_blind_300.csv"
    with blind_csv.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(blind_rows[0]))
        w.writeheader()
        w.writerows(blind_rows)

    pred_path = OUT_DIR / "human_review_prediction_map_300.jsonl"
    with pred_path.open("w", encoding="utf-8") as f:
        for r in prediction_map:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    manifest = {
        "n": len(blind_rows),
        "review_design": "BLINDED_TO_MODEL_PREDICTION",
        "screening_version": VERSION,
        "review_id_semantics": "stable SHA1-derived ID from source_type + source_native_id",
        "blind_file": blind_csv.name,
        "prediction_map": pred_path.name,
        "merge_key": "review_id",
        "rule": "Do not open prediction_map during first-pass independent review. Merge only after gold_status is completed.",
        "guardrail": "Regenerating the prediction map for a new screening version must not change review_id for the same source record.",
    }
    (OUT_DIR / "human_review_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
