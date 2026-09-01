from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def load(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="output/pilot_screened.jsonl")
    ap.add_argument("--out", default="output/pilot_summary.json")
    args = ap.parse_args()
    rows = load(Path(args.input))
    result = {
        "n": len(rows),
        "by_source": Counter(r.get("source_type") for r in rows),
        "by_scope": Counter(str(r.get("in_scope")) for r in rows),
        "by_confidence": Counter(r.get("confidence") for r in rows),
        "by_primary_family": Counter(r.get("primary_technology_id") or "NONE" for r in rows if r.get("source_type") != "vulnerability"),
        "by_false_positive": Counter(r.get("false_positive_type") or "NONE" for r in rows if r.get("source_type") != "vulnerability"),
        "github_artifact_type": Counter(r.get("artifact_type") or "UNKNOWN" for r in rows if r.get("source_type") == "open_source"),
        "github_orientation": Counter(r.get("use_orientation") or "UNKNOWN" for r in rows if r.get("source_type") == "open_source"),
        "vdp_group": Counter(r.get("cwe_group") or "W99" for r in rows if r.get("source_type") == "vulnerability"),
    }
    serializable = {k: dict(v) if isinstance(v, Counter) else v for k, v in result.items()}
    Path(args.out).write_text(json.dumps(serializable, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(serializable, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
