from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import OUT_DIR, load_queries, write_jsonl


def hits(text: str, terms: list[str]) -> list[str]:
    t = text.lower()
    return [x for x in terms if x.lower() in t]


def screen_supply(row: dict[str, Any], q: dict[str, Any]) -> dict[str, Any]:
    text = f"{row.get('title_or_name','')}\n{row.get('text_evidence','')}\n{' '.join(row.get('topics') or [])}".lower()
    offensive = hits(text, q["negative_context"]["offensive_only"])
    security_ai = hits(text, q["negative_context"]["security_of_ai"])

    family_scores: list[tuple[str, int, list[str]]] = []
    for family, cfg in q["families"].items():
        term_hits = hits(text, cfg["terms"])
        required = cfg.get("required_context") or []
        required_hits = hits(text, required) if required else ["NO_REQUIRED_CONTEXT"]
        score = len(term_hits) * 2 + min(2, len(required_hits))
        if term_hits and required_hits:
            family_scores.append((family, score, term_hits + required_hits[:2]))
    family_scores.sort(key=lambda x: x[1], reverse=True)

    if security_ai:
        row.update({"in_scope": False, "confidence": "REJECT", "false_positive_type": "SECURITY_OF_AI", "screening_reason": f"security-of-AI terms: {security_ai[:3]}"})
        return row

    if offensive and not any(x in text for x in ["remediation", "defensive", "blue team", "soc", "patch", "secure code"]):
        row.update({"in_scope": False, "confidence": "REJECT", "false_positive_type": "OFFENSIVE_ONLY", "use_orientation": "OFFENSIVE", "screening_reason": f"offensive-primary terms: {offensive[:3]}"})
        return row

    if not family_scores:
        row.update({"in_scope": False, "confidence": "LOW", "false_positive_type": "GENERIC_AI", "screening_reason": "no family passed term/context rules"})
        return row

    best = family_scores[0]
    secondaries = [x[0] for x in family_scores[1:3] if x[1] >= best[1] - 1]
    orientation = "DUAL_USE_DEFENSE_PRIMARY" if offensive else "DEFENSIVE"
    row.update({
        "in_scope": True,
        "confidence": "MEDIUM" if secondaries or offensive else "HIGH",
        "primary_technology_id": best[0],
        "secondary_technology_ids": secondaries,
        "use_orientation": orientation,
        "screening_reason": f"matched {best[2][:5]}",
        "false_positive_type": None,
        "needs_review": bool(secondaries or offensive),
    })
    return row


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+", help="JSONL candidate files")
    args = ap.parse_args()
    q = load_queries()
    out: list[dict[str, Any]] = []
    for p in args.inputs:
        for line in Path(p).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("source_type") == "vulnerability":
                row["in_scope"] = True
                row["confidence"] = "MEDIUM"
                row["screening_reason"] = "VDP demand record; not T01-T15 labeled"
                row["primary_technology_id"] = None
                row["secondary_technology_ids"] = []
                row["needs_review"] = False
            else:
                row = screen_supply(row, q)
            out.append(row)
    n = write_jsonl(OUT_DIR / "pilot_screened.jsonl", out)
    print(f"wrote {n} screened records")


if __name__ == "__main__":
    main()
