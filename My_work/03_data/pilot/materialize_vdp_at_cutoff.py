from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

import requests

from common import OUT_DIR, write_jsonl

CISA_KEV = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
EPSS_API = "https://api.first.org/data/v1/epss"
EPSS_START = date(2021, 4, 14)


def load_jsonl(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def fetch_kev() -> dict[str, dict[str, Any]]:
    r = requests.get(CISA_KEV, timeout=45)
    r.raise_for_status()
    return {x["cveID"]: x for x in r.json().get("vulnerabilities", []) if x.get("cveID")}


def fetch_epss_at(cves: list[str], cutoff: str) -> dict[str, dict[str, Any]]:
    cutoff_date = date.fromisoformat(cutoff)
    if cutoff_date < EPSS_START:
        return {}
    out: dict[str, dict[str, Any]] = {}
    # FIRST supports comma-separated CVEs, with a 2000-character parameter cap.
    batch: list[str] = []
    chars = 0
    batches: list[list[str]] = []
    for cve in cves:
        extra = len(cve) + (1 if batch else 0)
        if batch and chars + extra > 1900:
            batches.append(batch); batch = []; chars = 0
        batch.append(cve); chars += extra
    if batch:
        batches.append(batch)
    for b in batches:
        r = requests.get(EPSS_API, params={"cve": ",".join(b), "date": cutoff, "limit": 10000}, timeout=45)
        r.raise_for_status()
        for x in r.json().get("data", []):
            if x.get("cve"):
                out[x["cve"]] = x
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Materialize VDP exploitation features as knowable at a historical cutoff.")
    ap.add_argument("--input", default=str(OUT_DIR / "nvd_candidates.jsonl"))
    ap.add_argument("--cutoff", required=True, help="YYYY-MM-DD")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    cutoff_date = date.fromisoformat(args.cutoff)
    rows = load_jsonl(Path(args.input))
    kev = fetch_kev()
    epss = fetch_epss_at([r["cve_id"] for r in rows if r.get("cve_id")], args.cutoff)

    for row in rows:
        cve = row.get("cve_id")
        k = kev.get(cve)
        kev_date = date.fromisoformat(k["dateAdded"]) if k and k.get("dateAdded") else None
        e = epss.get(cve)
        row["materialized_cutoff"] = args.cutoff
        row["kev_status_at_cutoff"] = bool(kev_date and kev_date <= cutoff_date)
        row["kev_added_date"] = k.get("dateAdded") if k else None
        if cutoff_date >= EPSS_START:
            row["epss_structurally_available_at_cutoff"] = True
            row["epss_score_at_cutoff"] = float(e["epss"]) if e and e.get("epss") else None
            row["epss_percentile_at_cutoff"] = float(e["percentile"]) if e and e.get("percentile") else None
            row["epss_observation_date"] = e.get("date") if e else None
        else:
            row["epss_structurally_available_at_cutoff"] = False
            row["epss_score_at_cutoff"] = None
            row["epss_percentile_at_cutoff"] = None
            row["epss_observation_date"] = None

    output = Path(args.out) if args.out else OUT_DIR / f"vdp_at_{args.cutoff}.jsonl"
    n = write_jsonl(output, rows)
    print(f"wrote {n} point-in-time VDP records for cutoff {args.cutoff}")


if __name__ == "__main__":
    main()
