from __future__ import annotations

import argparse
from collections import defaultdict
from typing import Any

from common import OUT_DIR, base_record, env, load_queries, request_json, write_jsonl

API = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def headers() -> dict[str, str]:
    key = env("NVD_API_KEY")
    return {"apiKey": key} if key else {}


def weakness_group(cwes: list[str], groups: dict[str, list[str]]) -> str:
    for group, ids in groups.items():
        if any(c in ids for c in cwes):
            return group
    return "W99"


def extract_metrics(cve: dict[str, Any]) -> tuple[float | None, float | None]:
    metrics = cve.get("metrics") or {}
    for key in ("cvssMetricV31", "cvssMetricV30"):
        vals = metrics.get(key) or []
        if vals:
            d = vals[0].get("cvssData") or {}
            return d.get("baseScore"), d.get("exploitabilityScore") or vals[0].get("exploitabilityScore")
    vals = metrics.get("cvssMetricV2") or []
    if vals:
        d = vals[0].get("cvssData") or {}
        return d.get("baseScore"), vals[0].get("exploitabilityScore")
    return None, None


def extract_cpes(configurations: list[dict[str, Any]]) -> list[str]:
    out: set[str] = set()
    stack = list(configurations or [])
    while stack:
        obj = stack.pop()
        for m in obj.get("cpeMatch") or []:
            if m.get("criteria"):
                out.add(m["criteria"])
        stack.extend(obj.get("nodes") or [])
    return sorted(out)


def fetch_cwe(cwe: str, max_items: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    start = 0
    while len(rows) < max_items:
        params = {"cweId": cwe, "resultsPerPage": min(200, max_items - len(rows)), "startIndex": start}
        data = request_json("GET", API, headers=headers(), params=params, min_interval=0.7 if headers() else 6.1)
        vulns = data.get("vulnerabilities") or []
        if not vulns:
            break
        rows.extend(vulns)
        start += len(vulns)
        if start >= data.get("totalResults", 0):
            break
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-total", type=int, default=500)
    ap.add_argument("--per-cwe", type=int, default=20)
    args = ap.parse_args()
    q = load_queries()
    groups = q["vulnerability_strata"]
    raw: dict[str, dict[str, Any]] = {}
    for group, cwes in groups.items():
        if group == "W99":
            continue
        for cwe in cwes:
            if len(raw) >= args.max_total:
                break
            for item in fetch_cwe(cwe, min(args.per_cwe, args.max_total - len(raw))):
                cve = item.get("cve") or {}
                if cve.get("id"):
                    raw[cve["id"]] = cve
        if len(raw) >= args.max_total:
            break

    rows: list[dict[str, Any]] = []
    for cve_id, cve in raw.items():
        descriptions = cve.get("descriptions") or []
        text = next((d.get("value", "") for d in descriptions if d.get("lang") == "en"), descriptions[0].get("value", "") if descriptions else "")
        cwes = sorted({d.get("value") for w in (cve.get("weaknesses") or []) for d in (w.get("description") or []) if d.get("value", "").startswith("CWE-")})
        base, exploitability = extract_metrics(cve)
        cpes = extract_cpes(cve.get("configurations") or [])
        vendors = set(); products = set()
        for cpe in cpes:
            parts = cpe.split(":")
            if len(parts) > 4:
                vendors.add(parts[3]); products.add(parts[4])
        rec = base_record("vulnerability", cve_id, title=cve_id, text=text, query_id="NVD-CWE-STRATA")
        rec.update({
            "event_date": cve.get("published"),
            "source_modified_at": cve.get("lastModified"),
            "cve_id": cve_id,
            "cwe_ids": cwes,
            "cwe_group": weakness_group(cwes, groups),
            "cvss_base_as_observed": base,
            "cvss_exploitability_as_observed": exploitability,
            "cpe_as_observed": cpes,
            "affected_vendor_count": len(vendors),
            "affected_product_count": len(products),
            "kev_status_as_observed": False,
            "kev_added_date": None,
            "epss_score_as_observed": None,
            "epss_percentile_as_observed": None,
            "pressure_group": weakness_group(cwes, groups),
            "hypothesized_pressure_targets": [],
        })
        rows.append(rec)
    n = write_jsonl(OUT_DIR / "nvd_candidates.jsonl", rows[:args.max_total])
    print(f"wrote {n} NVD vulnerability-demand candidates")


if __name__ == "__main__":
    main()
