from __future__ import annotations

import json
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import requests

KEV_REPO = "https://github.com/cisagov/kev-data.git"
KEV_BRANCH = "develop"
KEV_FILE = "known_exploited_vulnerabilities.json"
CURRENT_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"


@dataclass
class KevSnapshot:
    entries: dict[str, dict[str, Any]]
    method: str
    cutoff: str
    source_commit: str | None
    source_commit_date: str | None
    earliest_git_commit_date: str | None
    caveat: str | None


def _git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def _parse_entries(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {x["cveID"]: x for x in data.get("vulnerabilities", []) if x.get("cveID")}


def _current_dateadded_approx(cutoff: str, earliest: str | None) -> KevSnapshot:
    r = requests.get(CURRENT_KEV_URL, timeout=45)
    r.raise_for_status()
    data = r.json()
    cutoff_date = date.fromisoformat(cutoff)
    entries: dict[str, dict[str, Any]] = {}
    for item in data.get("vulnerabilities", []):
        cve = item.get("cveID")
        added = item.get("dateAdded")
        if not cve or not added:
            continue
        try:
            if date.fromisoformat(added) <= cutoff_date:
                entries[cve] = item
        except ValueError:
            continue
    return KevSnapshot(
        entries=entries,
        method="CURRENT_CATALOG_DATEADDED_APPROX",
        cutoff=cutoff,
        source_commit=None,
        source_commit_date=None,
        earliest_git_commit_date=earliest,
        caveat=(
            "CISA kev-data Git history does not extend to this cutoff. Historical KEV status is approximated "
            "by filtering the current catalog on dateAdded; entries later removed or retroactively changed may be missed."
        ),
    )


def resolve_kev_snapshot(cutoff: str) -> KevSnapshot:
    """Resolve KEV as knowable at cutoff.

    Preferred method: latest CISA kev-data Git commit at or before cutoff.
    Fallback for cutoffs predating the public mirror's history: current catalog
    filtered by dateAdded, explicitly flagged as an approximation.
    """
    cutoff_date = date.fromisoformat(cutoff)
    with tempfile.TemporaryDirectory(prefix="kev-data-") as td:
        repo = Path(td) / "kev-data"
        subprocess.check_call(
            [
                "git",
                "clone",
                "--quiet",
                "--filter=blob:none",
                "--no-checkout",
                "--branch",
                KEV_BRANCH,
                KEV_REPO,
                str(repo),
            ]
        )
        root = _git(repo, "rev-list", "--max-parents=0", f"origin/{KEV_BRANCH}").splitlines()[0]
        earliest_iso = _git(repo, "show", "-s", "--format=%cI", root)
        earliest_date = earliest_iso[:10]

        if cutoff_date < date.fromisoformat(earliest_date):
            return _current_dateadded_approx(cutoff, earliest_date)

        sha = _git(repo, "rev-list", "-1", f"--before={cutoff}T23:59:59Z", f"origin/{KEV_BRANCH}")
        if not sha:
            return _current_dateadded_approx(cutoff, earliest_date)

        commit_iso = _git(repo, "show", "-s", "--format=%cI", sha)
        raw = _git(repo, "show", f"{sha}:{KEV_FILE}")
        data = json.loads(raw)
        return KevSnapshot(
            entries=_parse_entries(data),
            method="CISA_KEV_GIT_SNAPSHOT",
            cutoff=cutoff,
            source_commit=sha,
            source_commit_date=commit_iso,
            earliest_git_commit_date=earliest_date,
            caveat=None,
        )
