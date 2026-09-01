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
    out = {}
    for family, cfg in q["families"].items():
        terms = sorted(set(q["ai_terms"] + cfg["terms"]), key=len, reverse=True)
        out[family] = re.compile("|".join(re.escape(t) for t in terms), re.I)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Filter PatentsView/USPTO bulk TSV into WP2 patent Pilot candidates.")
    ap.add_argument("--patent-tsv", required=True)
    ap.add_argument("--max-total", type=int, default=500)
    ap.add_argument("--chunksize", type=int, default=100000)
    args = ap.parse_args()

    q = load_queries()
    patterns = compile_family_patterns(q)
    rows: list[dict[str, Any]] = []
    path = Path(args.patent_tsv)
    for chunk in pd.read_csv(path, sep="\t", dtype=str, chunksize=args.chunksize, on_bad_lines="skip"):
        idc, tc, ac, dc = col(chunk, "patent_id"), col(chunk, "title"), col(chunk, "abstract"), col(chunk, "date")
        if not idc or not tc:
            raise RuntimeError(f"Could not resolve required patent columns from: {list(chunk.columns)[:30]}")
        for _, r in chunk.iterrows():
            if len(rows) >= args.max_total:
                break
            title = str(r.get(tc) or "")
            abstract = str(r.get(ac) or "") if ac else ""
            text = f"{title}\n{abstract}"
            matched = [fam for fam, pat in patterns.items() if pat.search(text)]
            if not matched:
                continue
            # Require at least one cyber capability term and one AI method term for candidate retrieval.
            lower = text.lower()
            ai_hit = any(t.lower() in lower for t in q["ai_terms"])
            cyber_hit = any(term.lower() in lower for fam in q["families"].values() for term in fam["terms"])
            if not (ai_hit and cyber_hit):
                continue
            native_id = str(r.get(idc))
            rec = base_record("patent", native_id, title=title, text=abstract, query_id="PV-BULK-PILOT")
            rec.update({
                "event_date": str(r.get(dc)) if dc else None,
                "patent_id": native_id,
                "application_id": str(r.get(col(chunk, "application_id"))) if col(chunk, "application_id") else None,
                "filing_date": None,
                "publication_date": str(r.get(dc)) if dc else None,
                "assignee": str(r.get(col(chunk, "assignee"))) if col(chunk, "assignee") else None,
                "inventors": [],
                "cpc_codes": [],
                "ipc_codes": [],
                "claims_evidence": None,
                "cited_patents": [],
                "cited_non_patent_literature": [],
                "candidate_families": matched,
            })
            rows.append(rec)
        if len(rows) >= args.max_total:
            break
    n = write_jsonl(OUT_DIR / "patent_candidates.jsonl", rows)
    print(f"wrote {n} patent candidates")


if __name__ == "__main__":
    main()
