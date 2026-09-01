from __future__ import annotations

import argparse
from typing import Any

from common import OUT_DIR, base_record, env, load_queries, request_json, write_jsonl

API = "https://api.openalex.org/works"


def reconstruct_abstract(inv: dict[str, list[int]] | None) -> str:
    if not inv:
        return ""
    pairs: list[tuple[int, str]] = []
    for word, positions in inv.items():
        for pos in positions:
            pairs.append((pos, word))
    return " ".join(word for _, word in sorted(pairs))


def fetch_family(family: str, terms: list[str], ai_terms: list[str], start: str, end: str, limit: int) -> list[dict[str, Any]]:
    key = env("OPENALEX_API_KEY", required=True)
    rows: list[dict[str, Any]] = []
    cursor = "*"
    query = " OR ".join(f'"{t}"' for t in terms)
    # Candidate retrieval intentionally favors recall; classification occurs later.
    search = f"({query}) ({' OR '.join(ai_terms[:8])})"
    while len(rows) < limit:
        params = {
            "api_key": key,
            "search": search,
            "filter": f"from_publication_date:{start},to_publication_date:{end}",
            "per-page": min(100, limit - len(rows)),
            "cursor": cursor,
            "select": "id,doi,title,publication_date,primary_location,topics,authorships,cited_by_count,referenced_works,abstract_inverted_index",
        }
        data = request_json("GET", API, params=params, min_interval=0.15)
        results = data.get("results", [])
        if not results:
            break
        for w in results:
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
            })
            rows.append(rec)
            if len(rows) >= limit:
                break
        cursor = (data.get("meta") or {}).get("next_cursor")
        if not cursor:
            break
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-family", type=int, default=70)
    ap.add_argument("--max-total", type=int, default=1000)
    args = ap.parse_args()
    q = load_queries()
    start, end = q["window"]["from"], q["window"]["to"]
    all_rows: list[dict[str, Any]] = []
    families = list(q["families"].items())
    for family, cfg in families:
        remaining = args.max_total - len(all_rows)
        if remaining <= 0:
            break
        all_rows.extend(fetch_family(family, cfg["terms"], q["ai_terms"], start, end, min(args.per_family, remaining)))
    # Deduplicate works retrieved by multiple family queries.
    dedup = {r["source_native_id"]: r for r in all_rows}
    n = write_jsonl(OUT_DIR / "openalex_candidates.jsonl", dedup.values())
    print(f"wrote {n} OpenAlex candidates")


if __name__ == "__main__":
    main()
