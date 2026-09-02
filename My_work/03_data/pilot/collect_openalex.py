from __future__ import annotations

import argparse
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
            pairs.append((pos, word))
    return " ".join(word for _, word in sorted(pairs))


def convert_work(w: dict[str, Any], family: str, term: str, anchor: str) -> dict[str, Any]:
    native_id = w.get("id", "")
    abstract = reconstruct_abstract(w.get("abstract_inverted_index"))
    rec = base_record("science", native_id, title=w.get("title") or "", text=abstract, query_id=f"OA-{family}")
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
        "candidate_term": term,
        "ai_anchor": anchor,
    })
    return rec


def fetch_query(family: str, term: str, anchor: str, start: str, end: str, limit: int, key: str | None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    cursor = "*"
    search = f"{term} {anchor}"
    while len(rows) < limit:
        params: dict[str, Any] = {
            "search": search,
            "filter": f"from_publication_date:{start},to_publication_date:{end}",
            "per_page": min(100, limit - len(rows)),
            "cursor": cursor,
            "select": "id,doi,title,publication_date,primary_location,topics,authorships,cited_by_count,referenced_works,abstract_inverted_index",
        }
        if key:
            params["api_key"] = key
        try:
            data = request_json("GET", API, params=params, min_interval=0.20 if key else 0.35)
        except RuntimeError as exc:
            # Keyless OpenAlex access has a smaller daily budget. Preserve any
            # records already collected and let the workflow mark a partial run
            # rather than losing the entire Science Pilot attempt.
            print(f"OpenAlex query stopped after budget/network error for {family}/{term}/{anchor}: {exc}")
            break
        results = data.get("results", [])
        if not results:
            break
        rows.extend(convert_work(w, family, term, anchor) for w in results)
        cursor = (data.get("meta") or {}).get("next_cursor")
        if not cursor:
            break
    return rows[:limit]


def fetch_family(family: str, terms: list[str], start: str, end: str, limit: int, key: str | None) -> list[dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    per_query = max(5, min(20, limit))
    for term in terms:
        for anchor in AI_ANCHORS:
            if len(rows) >= limit:
                break
            for rec in fetch_query(family, term, anchor, start, end, min(per_query, limit - len(rows)), key):
                rows.setdefault(rec["source_native_id"], rec)
        if len(rows) >= limit:
            break
    return list(rows.values())[:limit]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-family", type=int, default=70)
    ap.add_argument("--max-total", type=int, default=1000)
    args = ap.parse_args()
    q = load_queries()
    start, end = q["window"]["from"], q["window"]["to"]
    key = env("OPENALEX_API_KEY")
    mode = "API_KEY" if key else "KEYLESS_BUDGETED"
    print(f"OpenAlex access mode: {mode}")

    all_rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for family, cfg in q["families"].items():
        remaining = args.max_total - len(all_rows)
        if remaining <= 0:
            break
        family_rows = fetch_family(family, cfg["terms"], start, end, min(args.per_family, remaining), key)
        for rec in family_rows:
            native_id = rec["source_native_id"]
            if native_id not in seen:
                seen.add(native_id)
                all_rows.append(rec)
                if len(all_rows) >= args.max_total:
                    break
    n = write_jsonl(OUT_DIR / "openalex_candidates.jsonl", all_rows)
    print(f"wrote {n} OpenAlex candidates using {mode}")


if __name__ == "__main__":
    main()
