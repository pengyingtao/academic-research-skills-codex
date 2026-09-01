from __future__ import annotations

import argparse
from typing import Any

from common import OUT_DIR, base_record, env, load_queries, request_json, write_jsonl

SEARCH_API = "https://api.github.com/search/repositories"
REPO_API = "https://api.github.com/repos/{full_name}"
README_API = "https://api.github.com/repos/{full_name}/readme"


def headers() -> dict[str, str]:
    token = env("GITHUB_TOKEN")
    h = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2026-03-10"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def fetch_readme(full_name: str) -> str:
    try:
        data = request_json("GET", README_API.format(full_name=full_name), headers=headers(), min_interval=0.35)
        download_url = data.get("download_url")
        if not download_url:
            return ""
        import requests
        r = requests.get(download_url, timeout=30)
        r.raise_for_status()
        return r.text[:20000]
    except Exception:
        return ""


def artifact_type(repo: dict[str, Any], readme: str) -> str:
    text = " ".join([repo.get("name") or "", repo.get("description") or "", " ".join(repo.get("topics") or []), readme[:4000]]).lower()
    if "awesome" in text and "list" in text:
        return "awesome_list_catalog"
    if any(x in text for x in ["ctf", "capture the flag", "training lab", "tutorial"]):
        return "ctf_demo" if "ctf" in text or "capture the flag" in text else "tutorial_course"
    if any(x in text for x in ["autonomous pentest", "penetration testing", "exploit orchestration", "red team", "bug bounty"]):
        return "offensive_tool"
    if any(x in text for x in ["dataset", "benchmark"]):
        return "dataset_benchmark"
    if any(x in text for x in ["paper", "arxiv", "research code"]):
        return "paper_code"
    if any(x in text for x in ["platform", "production", "siem", "soar"]):
        return "production_platform"
    return "tool_framework"


def fetch_family(family: str, terms: list[str], limit: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for term in terms:
        if len(rows) >= limit:
            break
        q = f'"{term}" cybersecurity in:name,description,readme archived:false fork:false'
        data = request_json("GET", SEARCH_API, headers=headers(), params={"q": q, "sort": "updated", "order": "desc", "per_page": min(30, limit - len(rows))}, min_interval=2.1)
        for item in data.get("items", []):
            full_name = item.get("full_name")
            if not full_name or full_name in seen:
                continue
            seen.add(full_name)
            repo = request_json("GET", REPO_API.format(full_name=full_name), headers=headers(), min_interval=0.35)
            readme = fetch_readme(full_name)
            rec = base_record("open_source", full_name, title=full_name, text=(repo.get("description") or "") + "\n" + readme, query_id=f"GH-{family}")
            rec.update({
                "event_date": repo.get("created_at"),
                "source_modified_at": repo.get("updated_at"),
                "repository_full_name": full_name,
                "created_at": repo.get("created_at"),
                "pushed_at": repo.get("pushed_at"),
                "language": repo.get("language"),
                "topics": repo.get("topics") or [],
                "artifact_type": artifact_type(repo, readme),
                "fork": repo.get("fork", False),
                "archived": repo.get("archived", False),
                "stars_as_observed": repo.get("stargazers_count"),
                "forks_as_observed": repo.get("forks_count"),
                "release_count_as_observed": None,
                "contributor_count_as_observed": None,
                "commit_activity_as_observed": None,
                "candidate_family": family,
                "candidate_term": term,
            })
            rows.append(rec)
            if len(rows) >= limit:
                break
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-family", type=int, default=40)
    ap.add_argument("--max-total", type=int, default=500)
    args = ap.parse_args()
    q = load_queries()
    rows: list[dict[str, Any]] = []
    for family, cfg in q["families"].items():
        remaining = args.max_total - len(rows)
        if remaining <= 0:
            break
        rows.extend(fetch_family(family, cfg["terms"], min(args.per_family, remaining)))
    dedup = {r["repository_full_name"]: r for r in rows}
    n = write_jsonl(OUT_DIR / "github_candidates.jsonl", dedup.values())
    print(f"wrote {n} GitHub candidates")


if __name__ == "__main__":
    main()
