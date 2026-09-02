from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from common import OUT_DIR, load_queries

CANDIDATES = OUT_DIR / "openalex_boolean_candidates.jsonl"
SCREENED = OUT_DIR / "openalex_boolean_screened.jsonl"


def load(path: Path) -> list[dict[str, Any]]:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def hits(text: str, terms: list[str]) -> list[str]:
    t = text.lower()
    return [x for x in terms if x.lower() in t]


def main() -> None:
    q = load_queries()
    candidates = load(CANDIDATES)
    screened = {r.get("source_native_id"): r for r in load(SCREENED)}

    family_topic_only = Counter()
    family_body_only = Counter()
    family_both = Counter()
    ai_channel = Counter()
    empty_abstract = 0
    auto_in_scope_with_topic_only_primary_signal = 0
    auto_in_scope_with_no_body_family_signal = 0
    examples: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for c in candidates:
        title = c.get("title_or_name") or ""
        abstract = c.get("text_evidence") or ""
        topics = " ".join(c.get("topics") or [])
        body = f"{title}\n{abstract}"

        if not abstract.strip():
            empty_abstract += 1

        body_ai = hits(body, q["ai_terms"])
        topic_ai = hits(topics, q["ai_terms"])
        if body_ai and topic_ai:
            ai_channel["BODY_AND_TOPICS"] += 1
        elif body_ai:
            ai_channel["BODY_ONLY"] += 1
        elif topic_ai:
            ai_channel["TOPICS_ONLY"] += 1
        else:
            ai_channel["NONE"] += 1

        body_family_hits: dict[str, list[str]] = {}
        topic_family_hits: dict[str, list[str]] = {}
        for fam, cfg in q["families"].items():
            bh = hits(body, cfg["terms"])
            th = hits(topics, cfg["terms"])
            if bh:
                body_family_hits[fam] = bh
            if th:
                topic_family_hits[fam] = th

            if bh and th:
                family_both[fam] += 1
            elif bh:
                family_body_only[fam] += 1
            elif th:
                family_topic_only[fam] += 1

        s = screened.get(c.get("source_native_id"), {})
        auto_primary = s.get("primary_technology_id")
        if s.get("in_scope") and auto_primary:
            if auto_primary not in body_family_hits:
                auto_in_scope_with_no_body_family_signal += 1
                if auto_primary in topic_family_hits:
                    auto_in_scope_with_topic_only_primary_signal += 1
                    if len(examples[auto_primary]) < 8:
                        examples[auto_primary].append({
                            "source_native_id": c.get("source_native_id"),
                            "title": title,
                            "candidate_family": c.get("candidate_family"),
                            "auto_primary": auto_primary,
                            "topic_hits": topic_family_hits.get(auto_primary),
                            "topics": c.get("topics") or [],
                            "abstract_present": bool(abstract.strip()),
                        })

    report = {
        "status": "DIAGNOSTIC_ONLY_NOT_GOLD",
        "n": len(candidates),
        "screening_version": "1.3.2",
        "empty_abstract_n": empty_abstract,
        "empty_abstract_rate": empty_abstract / len(candidates) if candidates else 0,
        "ai_signal_channel": dict(ai_channel),
        "family_signal_topic_only_counts": dict(family_topic_only),
        "family_signal_body_only_counts": dict(family_body_only),
        "family_signal_body_and_topics_counts": dict(family_both),
        "auto_in_scope_with_no_title_abstract_primary_family_signal": auto_in_scope_with_no_body_family_signal,
        "auto_in_scope_with_topic_only_primary_family_signal": auto_in_scope_with_topic_only_primary_signal,
        "topic_only_primary_examples": dict(examples),
        "interpretation": [
            "OpenAlex topics are platform-generated metadata and should not silently substitute for title/abstract evidence in semantic family classification.",
            "A topic-only primary-family signal is a source-specific leakage risk, not automatically a wrong label; independent review is still required.",
            "OpenAlex search may match fulltext that is not stored in the Pilot abstract, so retrieval and stored semantic evidence can legitimately disagree.",
        ],
    }
    (OUT_DIR / "openalex_evidence_channel_diagnostics.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
