from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from collect_patents_bulk import ALIASES, col, normalize_date


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate a PatentsView/USPTO bulk TSV before Pilot filtering.")
    ap.add_argument("--patent-tsv", required=True)
    ap.add_argument("--sample-rows", type=int, default=50000)
    ap.add_argument("--cutoff", default="2026-06-30")
    ap.add_argument("--out", default="output/patent_bulk_validation.json")
    args = ap.parse_args()

    path = Path(args.patent_tsv)
    if not path.exists():
        raise FileNotFoundError(path)

    df = pd.read_csv(path, sep="\t", dtype=str, nrows=args.sample_rows, on_bad_lines="skip")
    resolved = {k: col(df, k) for k in ALIASES}
    required_ok = bool(resolved["patent_id"] and resolved["title"])

    date_col = resolved["date"]
    dates = []
    if date_col:
        dates = [normalize_date(x) for x in df[date_col].tolist()]
        dates = [d for d in dates if d]

    abstract_col = resolved["abstract"]
    title_col = resolved["title"]
    report = {
        "file": str(path),
        "sample_rows_read": int(len(df)),
        "resolved_columns": resolved,
        "required_columns_ok": required_ok,
        "title_non_null_rate": float(df[title_col].notna().mean()) if title_col else 0.0,
        "abstract_non_null_rate": float(df[abstract_col].notna().mean()) if abstract_col else 0.0,
        "date_non_null_rate": float(df[date_col].notna().mean()) if date_col else 0.0,
        "sample_min_date": min(dates) if dates else None,
        "sample_max_date": max(dates) if dates else None,
        "rows_on_or_before_cutoff": int(sum(d <= args.cutoff for d in dates)),
        "cutoff": args.cutoff,
        "gate_ready": bool(required_ok and title_col and abstract_col and date_col),
        "notes": [
            "Claims/CPC/IPC/citations may require separate bulk tables and joins; this validator only checks the core candidate-retrieval table.",
            "Gate 2B Patent Pilot should not be counted if title, abstract, or event date is structurally unavailable.",
        ],
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
