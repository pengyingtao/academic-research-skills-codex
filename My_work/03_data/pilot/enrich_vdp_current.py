from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import requests

from common import OUT_DIR, now_iso, write_jsonl

CISA_KEV = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
EPSS_API = "https://api.first.org/data/v1/epss"


def load_jsonl(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def fetch_kev() -> dict[str, dict[str, Any]]:
    r = requests.get(CISA_KEV, timeout=45)
    r.raise_for_status()
    data = r.json()
    return {x["cveID"]: x for x in data.get("vulnerabilities", []) if x.get("cveID")}


def fetch_epss(cves: list[str]) -> dict[str, dict[str, Any]]:
    out = {}
    for i in range(0, len(cves), 50):
        batch = cves[i:i+50]
        r = requests.get(EPSS_API, params={"cve": ",".join(batch)}, timeout=45)
        r.raise_for_status()
        for x in r.json().get("data", []):
            out[x.get("cve")] = x
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Current-state enrichment for Pilot sanity only; do not use current values in historical backtests.")
    ap.add_argument("--input", default=str(OUT_DIR / "nvd_candidates.jsonl"))
    args = ap.parse_args()
    rows = load_jsonl(Path(args.input))
    kev = fetch_kev()
    epss = fetch_epss([r["cve_id"] for r in rows if r.get("cve_id")])
    observed = now_iso()
    for row in rows:
        cve = row.get("cve_id")
        k = kev.get(cve)
        e = epss.get(cve)
        row["kev_status_as_observed"] = bool(k)
        row["kev_added_date"] = k.get("dateAdded") if k else None
        row["epss_score_as_observed"] = float(e["epss"]) if e and e.get("epss") else None
        row["epss_percentile_as_observed"] = float(e["percentile"]) if e and e.get("percentile") else None
        row["vdp_enriched_at"] = observed
        row["vdp_enrichment_semantics"] = "CURRENT_SANITY_ONLY"
    n = write_jsonl(OUT_DIR / "nvd_candidates_current_enriched.jsonl", rows)
    print(f"wrote {n} current-enriched VDP records")


if __name__ == "__main__":
    main()
