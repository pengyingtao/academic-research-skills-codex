from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import pandas as pd

from common import OUT_DIR, base_record, load_queries, write_jsonl

ALIASES = {
    "patent_id": ["patent_id", "publication_number", "patent_number"],
    "title": ["patent_title", "title", "invention_title"],
    "abstract": ["patent_abstract", "abstract"],
    "date": ["patent_date", "publication_date", "date"],
    "application_id": ["application_id", "application_number"],
    "assignee": ["assignee_organization", "assignee", "assignee_name"],
}


def col(df: pd.DataFrame, key: str) -> str | None:
    for name in ALIASES[key]:
        if name in df.columns:
            return name
    return None


def compile_family_patterns(q: dict[str, Any]) -> dict[str, re.Pattern[str]]:
    """Compile ONLY family capability terms.

    AI anchors are evaluated separately. Mixing generic AI terms into every
    family pattern makes one AI hit falsely mark all Txx families as candidates.
    """
    out: dict[str, re.Pattern[str]] = {}
    for family, cfg in q["families"].items():
        terms = sorted(set(cfg["terms"]), key=len, reverse=True)
        out[family] = re.compile("|".join(re.escape(t) for t in terms), re.I)
    return out


def normalize_date(value: object) -> str | None:
    if value is None or pd.isna(value):
        return None
    s = str(value).strip()
    if not s:
        return None
    # Supports YYYY-MM-DD and common compact YYYYMMDD bulk formats.
    if re.fullmatch(r"\d{8}", s):
        return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
    return s[:10]


def main() -> None:
    ap = argparse.ArgumentParser(description="Filter PatentsView/USPTO bulk TSV into WP2 patent Pilot candidates.")
    ap.add_argument("--patent-tsv", required=True)
    ap.add_argument("--max-total", type=int, default=500)
    ap.add_argument("--chunksize", type=int, default=100000)
    ap.add_argument("--cutoff", default=None, help="Publication/event cutoff YYYY-MM-DD; defaults to query-pack window end")
    args = ap.parse_args()

    q = load_queries()
    cutoff = args.cutoff or q["window"]["to"]
    patterns = compile_family_patterns(q)
    ai_terms = [t.lower() for t in q["ai_terms"]]
    rows: list[dict[str, Any]] = []
    path = Path(args.patent_tsv)

    for chunk in pd.read_csv(path, sep="\t", dtype=str, chunksize=args.chunksize, on_bad_lines="skip"):
        idc, tc, ac, dc = col(chunk, "patent_id"), col(chunk, "title"), col(chunk, "abstract"), col(chunk, "date")
        appc, assigneec = col(chunk, "application_id"), col(chunk, "assignee")
        if not idc or not tc:
            raise RuntimeError(f"Could not resolve required patent columns from: {list(chunk.columns)[:30]}")

        for _, r in chunk.iterrows():
            if len(rows) >= args.max_total:
                break

            title = str(r.get(tc) or "")
            abstract = str(r.get(ac) or "") if ac else ""
            text = f"{title}\n{abstract}"
            lower = text.lower()

            ai_hit_terms = sorted({t for t in ai_terms if t in lower})
            if not ai_hit_terms:
                continue

            matched = [fam for fam, pat in patterns.items() if pat.search(text)]
            if not matched:
                continue

            event_date = normalize_date(r.get(dc)) if dc else None
            if event_date and event_date > cutoff:
                continue

            native_id = str(r.get(idc))
            rec = base_record("patent", native_id, title=title, text=abstract, query_id="PV-BULK-PILOT")
            rec.update({
                "event_date": event_date,
                "patent_id": native_id,
                "application_id": str(r.get(appc)) if appc and not pd.isna(r.get(appc)) else None,
                "filing_date": None,
                "publication_date": event_date,
                "assignee": str(r.get(assigneec)) if assigneec and not pd.isna(r.get(assigneec)) else None,
                "inventors": [],
                "cpc_codes": [],
                "ipc_codes": [],
                "claims_evidence": None,
                "cited_patents": [],
                "cited_non_patent_literature": [],
                "candidate_families": matched,
                "retrieved_by_ai_terms": ai_hit_terms,
                "formal_event_cutoff": cutoff,
            })
            rows.append(rec)

        if len(rows) >= args.max_total:
            break

    # Deduplicate within patent source before cross-source resolution.
    dedup = {r["patent_id"]: r for r in rows}
    n = write_jsonl(OUT_DIR / "patent_candidates.jsonl", list(dedup.values())[:args.max_total])
    print(f"wrote {n} patent candidates with event_date <= {cutoff}")


if __name__ == "__main__":
    main()
