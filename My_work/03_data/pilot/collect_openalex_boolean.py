from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from common import OUT_DIR, base_record, env, load_queries, request_json, write_jsonl

API = "https://api.openalex.org/works"
AI_ANCHORS = ["machine learning", "artificial intelligence", "large language model", "deep learning"]


def reconstruct_abstract(inv: dict[str, list[int]] | None) -> str:
    if not inv:
        return ""
    pairs: list[tuple[int, str]] = []
    for word, positions in inv.items():
        for pos in positions:
            pairs.extend((pos, word) for pos in positions)
            break
    # The loop above intentionally adds all positions in one extend; normalize
    # through a clean rebuild to avoid accidental duplicate nesting.
    pairs = [(pos, word) for word, positions in inv.items() for pos in positions]
    return " ".join(word for _, word in sorted(pairs))


def qterm(term: str) -> str:
    term = term.strip()
    if " " in term or "-" in term:
        return f'"{term}"'
    return term


def build_family_query(terms: list[str]) -> str:
    # Keep URLs comfortably below the ~4 KB OpenAlex search limit.
    family_terms = terms[:6]
    family_expr = " OR ".join(qterm(t) for t in family_terms)
    ai_expr = " OR ".join(qterm(t) for t in AI_ANCHORS)
    return f"({family_expr}) AND ({ai_expr})"


def convert_work(w: dict[str, Any], family: str, query: str) -> dict[str, Any]:
    native_id = w.get("id", "")
    abstract = reconstruct_abstract(w.get("abstract_inverted_index"))
    rec = base_record("science", native_id, title=w.get("title") or "", text=abstract, query_id=f"OA-BOOL-{family}")
    rec.update({
        "event_date": w.get("publication_date"),
        "doi": w.get("doi"),
        "openalex_id": native_id,
        "publication_date": w.get("publication_date"),
        "venue": (((w.get("primary_location") or {}).get("source") or {}).get("display_name")),
        "topics": [t.get("display_name") for t in (w.get("topics") or []) if t.get("display_name")],
        "authors": [((a.get("author") or {}).get("display_name")) for a in (w.get("authorships") or []) if (a.get("author") or {}).get("display_name")],
        "institutions": sorted({i.get("display_name") for a in (w.get("authorships") or []) for i in (a.get("institutions") or []) if i.get("display_name")}),
        "cited_by_count_as_observed": w.get("cited_by_count"),
        "referenced_works": w.get("referenced_works") or [],
        "candidate_family": family,
        "retrieved_candidate_families": [family],
        "boolean_search_query": query,
        "openalex_collection_design": "ONE_BOOLEAN_SEARCH_PER_FAMILY",
    })
    return rec


def fetch_family(family: str, terms: list[str], start: str, end: str, key: str | None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    query = build_family_query(terms)
    params: dict[str, Any] = {
        "search": query,
        "filter": f"from_publication_date:{start},to_publication_date:{end}",
        "per_page": 100,
        "select": "id,doi,title,publication_date,primary_location,topics,authorships,cited_by_count,referenced_works,abstract_inverted_index",
    }
    if key:
        params["api_key"] = key
    try:
        data = request_json(
            "GET", API, params=params,
            max_retries=2 if key else 1,
            min_interval=0.2 if key else 0.35,
        )
        rows = [convert_work(w, family, query) for w in data.get("results", [])]
        meta = data.get("meta") or {}
        return rows, {
            "family": family,
            "status": "PASS",
            "returned": len(rows),
            "available_count": meta.get("count"),
            "cost_usd": meta.get("cost_usd"),
            "query": query,
        }
    except Exception as exc:
        return [], {
            "family": family,
            "status": "ERROR",
            "returned": 0,
            "error": repr(exc),
            "query": query,
        }


def stratified_dedup(pools: dict[str, list[dict[str, Any]]], max_total: int) -> list[dict[str, Any]]:
    merged_by_id: dict[str, dict[str, Any]] = {}
    family_ids: dict[str, list[str]] = {}

    for family, rows in pools.items():
        ids: list[str] = []
        for r in rows:
            native_id = r.get("source_native_id")
            if not native_id:
                continue
            ids.append(native_id)
            if native_id not in merged_by_id:
                merged_by_id[native_id] = r
            else:
                fams = merged_by_id[native_id].setdefault("retrieved_candidate_families", [])
                if family not in fams:
                    fams.append(family)
        family_ids[family] = ids

    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()
    families = list(pools)
    depth = 0
    while len(selected) < max_total:
        added = False
        for family in families:
            ids = family_ids.get(family, [])
            if depth >= len(ids):
                continue
            native_id = ids[depth]
            if native_id not in selected_ids:
                selected_ids.add(native_id)
                selected.append(merged_by_id[native_id])
                added = True
                if len(selected) >= max_total:
                    break
        if not added and all(depth + 1 >= len(family_ids.get(f, [])) for f in families):
            break
        depth += 1
    return selected


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-total", type=int, default=1000)
    args = ap.parse_args()

    q = load_queries()
    start, end = q["window"]["from"], q["window"]["to"]
    key = env("OPENALEX_API_KEY")
    mode = "API_KEY" if key else "KEYLESS_BUDGETED"

    pools: dict[str, list[dict[str, Any]]] = {}
    query_status: list[dict[str, Any]] = []
    for family, cfg in q["families"].items():
        rows, status = fetch_family(family, cfg["terms"], start, end, key)
        pools[family] = rows
        query_status.append(status)
        print(json.dumps(status, ensure_ascii=False))
        if status["status"] == "ERROR" and not key:
            # A shared keyless budget may be exhausted. Preserve all successful
            # earlier family calls instead of burning repeated requests.
            break

    selected = stratified_dedup(pools, args.max_total)
    n = write_jsonl(OUT_DIR / "openalex_boolean_candidates.jsonl", selected)

    raw_n = sum(len(v) for v in pools.values())
    unique_n = len({r.get("source_native_id") for rows in pools.values() for r in rows if r.get("source_native_id")})
    status_payload = {
        "source": "openalex",
        "collection_design": "ONE_BOOLEAN_SEARCH_PER_FAMILY",
        "access_mode": mode,
        "research_cutoff": end,
        "target": args.max_total,
        "families_attempted": len(query_status),
        "families_passed": sum(s.get("status") == "PASS" for s in query_status),
        "raw_rows_across_family_queries": raw_n,
        "unique_rows_before_cap": unique_n,
        "selected_rows": n,
        "query_status": query_status,
        "budget_note": "At most one billable full-text search call per attempted technology family; per_page=100.",
        "guardrail": "Pilot candidate retrieval only; taxonomy accuracy requires independent human gold review.",
    }
    (OUT_DIR / "openalex_boolean_status.json").write_text(
        json.dumps(status_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(status_payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
