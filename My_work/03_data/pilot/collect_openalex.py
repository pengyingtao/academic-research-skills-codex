from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import OUT_DIR, base_record, env, load_queries, request_json, write_jsonl

API = "https://api.openalex.org/works"
AI_ANCHORS = ["machine learning", "artificial intelligence", "large language model", "deep learning"]


class OpenAlexAccessStop(RuntimeError):
    """Stop the current Pilot run when access/budget is unavailable."""


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


def api_request(params: dict[str, Any], key: str | None) -> dict[str, Any]:
    if key:
        params["api_key"] = key
    # Keyless access is intentionally fast-fail. Repeating five exponential
    # backoffs for every family/query can turn a simple access failure into a
    # 45-minute workflow. Credentialed mode keeps a small retry allowance.
    retries = 2 if key else 1
    try:
        return request_json(
            "GET",
            API,
            params=params,
            min_interval=0.20 if key else 0.35,
            max_retries=retries,
        )
    except RuntimeError as exc:
        raise OpenAlexAccessStop(str(exc)) from exc


def probe_access(start: str, end: str, key: str | None) -> bool:
    params: dict[str, Any] = {
        "search": "machine learning cybersecurity",
        "filter": f"from_publication_date:{start},to_publication_date:{end}",
        "per_page": 1,
        "select": "id,title,publication_date",
    }
    try:
        data = api_request(params, key)
        ok = bool(data.get("results"))
        print(f"OpenAlex access probe: {'PASS' if ok else 'EMPTY'}")
        return ok
    except OpenAlexAccessStop as exc:
        print(f"OpenAlex access probe: FAIL_FAST ({exc})")
        return False


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
        data = api_request(params, key)
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


def load_existing(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-family", type=int, default=70)
    ap.add_argument("--max-total", type=int, default=1000)
    ap.add_argument("--no-resume", action="store_true", help="Ignore any persisted partial OpenAlex corpus")
    args = ap.parse_args()
    q = load_queries()
    start, end = q["window"]["from"], q["window"]["to"]
    key = env("OPENALEX_API_KEY")
    mode = "API_KEY" if key else "KEYLESS_BUDGETED"
    print(f"OpenAlex access mode: {mode}")

    out_path = OUT_DIR / "openalex_candidates.jsonl"
    existing = [] if args.no_resume else load_existing(out_path)
    all_rows: list[dict[str, Any]] = existing[: args.max_total]
    seen: set[str] = {r.get("source_native_id") for r in all_rows if r.get("source_native_id")}
    if existing:
        print(f"Resuming from {len(existing)} persisted OpenAlex candidates")

    if len(all_rows) >= args.max_total:
        print(f"OpenAlex target already satisfied with {len(all_rows)} records")
        return

    if not probe_access(start, end, key):
        write_jsonl(out_path, all_rows)
        print(f"wrote {len(all_rows)} OpenAlex candidates; access probe unavailable")
        return

    try:
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
            # Persist after each family so a later budget stop can resume from
            # verified partial output on the next run.
            write_jsonl(out_path, all_rows)
            print(f"OpenAlex progress: {len(all_rows)}/{args.max_total} after {family}")
    except OpenAlexAccessStop as exc:
        print(f"OpenAlex collection stopped early: {exc}")

    n = write_jsonl(out_path, all_rows)
    print(f"wrote {n} OpenAlex candidates using {mode}")


if __name__ == "__main__":
    main()
