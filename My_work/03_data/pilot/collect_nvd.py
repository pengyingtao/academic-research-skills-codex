from __future__ import annotations

import argparse
from typing import Any

from common import OUT_DIR, base_record, env, load_queries, request_json, write_jsonl

API = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# Each NVD date query is <=120 consecutive days. These deterministic slices span
# the frozen research window for Gate 2B source/schema validation; WP3 will use
# bulk/complete materialization rather than treating these slices as population estimates.
FORMAL_WINDOWS = [
    ("2012-01-01T00:00:00.000Z", "2012-04-29T23:59:59.999Z"),
    ("2014-07-01T00:00:00.000Z", "2014-10-28T23:59:59.999Z"),
    ("2016-01-01T00:00:00.000Z", "2016-04-29T23:59:59.999Z"),
    ("2018-07-01T00:00:00.000Z", "2018-10-28T23:59:59.999Z"),
    ("2020-01-01T00:00:00.000Z", "2020-04-29T23:59:59.999Z"),
    ("2022-07-01T00:00:00.000Z", "2022-10-28T23:59:59.999Z"),
    ("2024-01-01T00:00:00.000Z", "2024-04-29T23:59:59.999Z"),
    ("2026-03-01T00:00:00.000Z", "2026-06-28T23:59:59.999Z"),
]


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
            return d.get("baseScore"), vals[0].get("exploitabilityScore")
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


def fetch_cwe(cwe: str, max_items: int, window: tuple[str, str] | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    start = 0
    while len(rows) < max_items:
        params: dict[str, Any] = {
            "cweId": cwe,
            "resultsPerPage": min(200, max_items - len(rows)),
            "startIndex": start,
            "noRejected": "",
        }
        if window:
            params["pubStartDate"], params["pubEndDate"] = window
        data = request_json("GET", API, headers=headers(), params=params, min_interval=0.7 if headers() else 6.1)
        vulns = data.get("vulnerabilities") or []
        if not vulns:
            break
        rows.extend(vulns)
        start += len(vulns)
        if start >= data.get("totalResults", 0):
            break
    return rows[:max_items]


def to_record(cve: dict[str, Any], groups: dict[str, list[str]], query_id: str, sampling_window: tuple[str, str] | None) -> dict[str, Any]:
    cve_id = cve.get("id") or ""
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
    rec = base_record("vulnerability", cve_id, title=cve_id, text=text, query_id=query_id)
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
        "kev_status_as_observed": None,
        "kev_added_date": None,
        "epss_score_as_observed": None,
        "epss_percentile_as_observed": None,
        "pressure_group": weakness_group(cwes, groups),
        "hypothesized_pressure_targets": [],
        "pilot_sampling_window": sampling_window,
    })
    return rec


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-total", type=int, default=500)
    ap.add_argument("--per-cwe", type=int, default=20)
    ap.add_argument("--formal-windowed", action="store_true", help="Sample across deterministic <=120-day windows spanning 2012Q1-2026Q2")
    args = ap.parse_args()
    q = load_queries()
    groups = q["vulnerability_strata"]
    raw: dict[str, tuple[dict[str, Any], tuple[str, str] | None]] = {}

    windows = FORMAL_WINDOWS if args.formal_windowed else [None]
    # Round-robin across windows and CWE groups so early/high-volume weaknesses do
    # not consume the whole Pilot quota.
    active_groups = [(g, cwes) for g, cwes in groups.items() if g != "W99"]
    per_query = max(1, min(args.per_cwe, 5 if args.formal_windowed else args.per_cwe))
    for window in windows:
        for _, cwes in active_groups:
            for cwe in cwes:
                if len(raw) >= args.max_total:
                    break
                for item in fetch_cwe(cwe, min(per_query, args.max_total - len(raw)), window):
                    cve = item.get("cve") or {}
                    if cve.get("id"):
                        raw.setdefault(cve["id"], (cve, window))
            if len(raw) >= args.max_total:
                break
        if len(raw) >= args.max_total:
            break

    rows = [to_record(cve, groups, "NVD-CWE-WINDOWED" if args.formal_windowed else "NVD-CWE-STRATA", window) for cve, window in raw.values()]
    n = write_jsonl(OUT_DIR / "nvd_candidates.jsonl", rows[:args.max_total])
    mode = "formal-windowed" if args.formal_windowed else "sanity"
    print(f"wrote {n} NVD vulnerability-demand candidates ({mode})")


if __name__ == "__main__":
    main()
