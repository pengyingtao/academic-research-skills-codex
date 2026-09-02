from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from common import OUT_DIR

FN = OUT_DIR / "centrality_false_negative_audit.jsonl"
FP = OUT_DIR / "in_scope_false_positive_audit.jsonl"

AI_METHOD_VARIANTS = {
    "ai_assisted": [r"\bai[- ]assisted\b"],
    "hyphenated_ml": [r"\bmachine[- ]learning\b"],
    "cnn_lstm": [r"\bcnn\b", r"\blstm\b", r"\brnn\b"],
    "tree_ensemble": [r"\brandom forest\b", r"\bxgboost\b", r"\blightgbm\b", r"\bisolation forest\b"],
    "agent_language": [r"\bautonomous (?:security )?agent\b", r"\bai security copilot\b"],
}

FALSE_POSITIVE_DIAGNOSTICS = {
    "profile_or_portfolio": [
        r"\bpersonal (?:academic )?portfolio\b", r"\bportfolio website\b", r"\babout me\b",
        r"\boperator profile\b", r"\bresume[- ]focused\b",
    ],
    "reference_or_paper_feed": [
        r"\barxiv[- ]daily\b", r"\bweekly[- ]arxiv\b", r"\brecent papers\b",
        r"\bpaper(s)? collection\b", r"\bdaily updated papers\b", r"\btracks .* papers\b",
    ],
    "catalog_or_hub": [
        r"\bcurated repos\b", r"\bcurated selection\b", r"\btool descriptions\b",
        r"\bcommunity hub\b", r"\bjunk drawer\b", r"\bmarketplace\b",
    ],
    "third_party_profile": [
        r"\bindependent third-party profile\b", r"\bthis is not our api\b", r"\bapi evangelist\b",
    ],
    "blog_or_reference_content": [
        r"\bblog portfolio\b", r"\bpublished articles\b", r"\bguide\b", r"\broadmap\b",
    ],
    "training_or_learning": [
        r"\blearning path\b", r"\bcertification roadmap\b", r"\btraining\b",
        r"\b30-day .* challenge\b", r"\bfor learning\b", r"\binterview preparation\b",
    ],
}


def load(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def matches(text: str, patterns: list[str]) -> bool:
    t = text.lower()
    return any(re.search(p, t, flags=re.I) for p in patterns)


def main() -> None:
    fn_rows = load(FN)
    fp_rows = load(FP)

    fn_counter: Counter[str] = Counter()
    fn_examples: dict[str, list[str]] = {}
    for r in fn_rows:
        text = f"{r.get('title_or_name','')} {r.get('evidence_excerpt','')}"
        for label, patterns in AI_METHOD_VARIANTS.items():
            if matches(text, patterns):
                fn_counter[label] += 1
                fn_examples.setdefault(label, []).append(r.get("source_native_id"))

    fp_counter: Counter[str] = Counter()
    fp_examples: dict[str, list[str]] = {}
    for r in fp_rows:
        text = f"{r.get('title_or_name','')} {r.get('evidence_excerpt','')}"
        native = (r.get("source_native_id") or "").lower()
        parts = native.split("/", 1)
        if len(parts) == 2 and parts[0] == parts[1]:
            fp_counter["owner_repo_profile"] += 1
            fp_examples.setdefault("owner_repo_profile", []).append(r.get("source_native_id"))
        for label, patterns in FALSE_POSITIVE_DIAGNOSTICS.items():
            if matches(text, patterns):
                fp_counter[label] += 1
                fp_examples.setdefault(label, []).append(r.get("source_native_id"))

    report = {
        "status": "DIAGNOSTIC_ONLY_NOT_GOLD",
        "screening_version": "1.3.2",
        "centrality_false_negative_sample_n": len(fn_rows),
        "in_scope_false_positive_sample_n": len(fp_rows),
        "centrality_missed_ai_method_variant_flags": dict(fn_counter),
        "centrality_examples": {k: v[:8] for k, v in fn_examples.items()},
        "in_scope_non_tool_or_container_flags": dict(fp_counter),
        "in_scope_examples": {k: v[:8] for k, v in fp_examples.items()},
        "interpretation": [
            "Counts are overlapping diagnostic flags, not error rates and not gold labels.",
            "A false-negative audit record may contain an AI method token but still be out of scope for other reasons.",
            "A false-positive audit record may look like a profile/feed/container but still require independent review before exclusion.",
            "Use this report to prioritize targeted human review and narrow rule changes only.",
        ],
    }
    (OUT_DIR / "screening_audit_diagnostics_v1_3_2.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
