from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from common import load_queries
from screen_candidates import screen_supply


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="output/github_candidates.jsonl")
    ap.add_argument("--out", default="analysis/current_sanity_rescreen_v1.json")
    args = ap.parse_args()

    q = load_queries()
    rows = []
    for line in Path(args.input).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        rows.append(screen_supply(row, q))

    summary = {
        "n": len(rows),
        "in_scope": dict(Counter(str(bool(r.get("in_scope"))) for r in rows)),
        "confidence": dict(Counter(r.get("confidence") or "NONE" for r in rows)),
        "false_positive_type": dict(Counter(r.get("false_positive_type") or "NONE" for r in rows)),
        "primary_family": dict(Counter(r.get("primary_technology_id") or "NONE" for r in rows)),
        "note": "Re-screen of the persisted current-sanity GitHub batch using the post-2026-09-01 hard AI-anchor rule. This is diagnostic only, not Gate 2B formal-history data.",
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
