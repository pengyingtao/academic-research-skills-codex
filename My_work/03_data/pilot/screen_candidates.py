from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import OUT_DIR, load_queries, write_jsonl


def hits(text: str, terms: list[str]) -> list[str]:
    t = text.lower()
    return [x for x in terms if x.lower() in t]


def reject(row: dict[str, Any], fp_type: str, reason: str, *, confidence: str = "REJECT") -> dict[str, Any]:
    row.update({
        "in_scope": False,
        "confidence": confidence,
        "false_positive_type": fp_type,
        "screening_reason": reason,
        "primary_technology_id": None,
        "secondary_technology_ids": [],
        "needs_review": confidence != "REJECT",
    })
    return row


def screen_supply(row: dict[str, Any], q: dict[str, Any]) -> dict[str, Any]:
    title = row.get("title_or_name", "") or ""
    evidence = row.get("text_evidence", "") or ""
    text = f"{title}\n{evidence}\n{' '.join(row.get('topics') or [])}".lower()
    ai_hits = hits(text, q["ai_terms"])
    offensive = hits(text, q["negative_context"]["offensive_only"])
    security_ai = hits(text, q["negative_context"]["security_of_ai"])

    # GitHub-specific hygiene is applied before family scoring. These records may
    # be useful for discovery, training or ecosystem context but should not be
    # counted as engineering-supply evidence in the core O layer.
    if row.get("source_type") == "open_source":
        artifact = row.get("artifact_type")
        role = row.get("analysis_role")
        if role == "DISCOVERY_ONLY" or artifact == "awesome_list_catalog":
            return reject(row, "AGGREGATOR_NOT_TOOL", "discovery/catalog repository is not core engineering-supply evidence")

        catalog_hits = hits(text, q["negative_context"].get("catalog_only", []))
        if catalog_hits:
            return reject(row, "AGGREGATOR_NOT_TOOL", f"catalog/resource-list indicators: {catalog_hits[:3]}")

        native = (row.get("source_native_id") or "").lower()
        parts = native.split("/", 1)
        profile_hits = hits(text, q["negative_context"].get("personal_profile", []))
        is_profile_repo = len(parts) == 2 and parts[0] == parts[1]
        if is_profile_repo and profile_hits:
            return reject(row, "PERSONAL_PROFILE", f"profile repository indicators: {profile_hits[:3]}")

        education_hits = hits(text, q["negative_context"].get("education_only", []))
        operational_terms = [
            "malware detection", "intrusion detection", "phishing detection", "threat hunting",
            "incident response", "vulnerability detection", "vulnerability repair", "secure code",
            "digital forensics", "security orchestration", "threat intelligence", "soc agent",
        ]
        if education_hits and not hits(text, operational_terms):
            return reject(row, "EDUCATIONAL_ONLY", f"education/training artifact without a primary defensive capability: {education_hits[:3]}")

    # Supply-side records must satisfy the protocol's AI-anchor requirement.
    if not ai_hits:
        return reject(row, "NO_AI_SIGNAL", "cybersecurity capability found but no AI-method anchor")

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
        return reject(row, "SECURITY_OF_AI", f"security-of-AI terms: {security_ai[:3]}")

    if offensive and not any(x in text for x in ["remediation", "defensive", "blue team", "soc", "patch", "secure code"]):
        row["use_orientation"] = "OFFENSIVE"
        return reject(row, "OFFENSIVE_ONLY", f"offensive-primary terms: {offensive[:3]}")

    if not family_scores:
        return reject(
            row,
            "GENERIC_AI",
            f"AI signal {ai_hits[:3]} present but no AI-for-cybersecurity family passed term/context rules",
            confidence="LOW",
        )

    best = family_scores[0]
    secondaries = [x[0] for x in family_scores[1:3] if x[1] >= best[1] - 1]
    orientation = "DUAL_USE_DEFENSE_PRIMARY" if offensive else "DEFENSIVE"
    row.update({
        "in_scope": True,
        "confidence": "MEDIUM" if secondaries or offensive else "HIGH",
        "primary_technology_id": best[0],
        "secondary_technology_ids": secondaries,
        "use_orientation": orientation,
        "ai_method_tags": ai_hits,
        "screening_reason": f"AI={ai_hits[:3]}; family={best[2][:5]}",
        "false_positive_type": None,
        "needs_review": bool(secondaries or offensive),
        "keyword_version": "1.2",
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
            row["keyword_version"] = "1.2"
            if row.get("source_type") == "vulnerability":
                # V is demand pressure only; never assign T01-T15 ground truth.
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
