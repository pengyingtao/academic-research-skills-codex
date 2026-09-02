# WP2 Gate 2B — Blockers and Recovery Conditions

**Updated:** 2026-09-02

## 1. OpenAlex Science layer

### Current status

`RUNNING_KEYLESS_BUDGETED / API_KEY_RECOMMENDED`

The earlier `BLOCKED_CREDENTIAL` classification has been retired.

Current OpenAlex documentation (rechecked 2026-09-02) allows basic API queries without an API key, with a smaller daily budget. A free API key remains strongly recommended for larger-scale/repeated collection because it raises the available daily budget.

The repository has been updated so that:

- `OPENALEX_API_KEY` is optional rather than required;
- when a key exists, the collector uses `API_KEY` mode;
- without a key, the collector uses `KEYLESS_BUDGETED` mode;
- Science screening writes to `openalex_screened.jsonl` and no longer overwrites the formal O/V `pilot_screened.jsonl`;
- the next collector version uses a one-shot access probe, fast circuit breaking, and persisted partial-output resume to avoid repeated long backoffs.

Current workflow:

`.github/workflows/wp2-openalex-pilot.yml`

Target output:

- `My_work/03_data/pilot/output/openalex_candidates.jsonl`
- `My_work/03_data/pilot/output/openalex_screened.jsonl`
- `My_work/03_data/pilot/output/openalex_pilot_status.json`
- target: approximately 1000 Science-layer candidates
- event cutoff: 2026-06-30

### Recovery/escalation condition

If keyless mode returns only a partial corpus or repeatedly hits access/budget limits, configure a free OpenAlex API key as repository secret:

`OPENALEX_API_KEY`

Then re-run the same workflow. A full OpenAlex snapshot remains an alternative only when suitable local/cloud storage is available; it is unnecessarily large for an ordinary GitHub Actions Pilot.

---

## 2. Patent Technology layer

### Current status

`BLOCKED_AUTHENTICATED_ODP_ACCESS`

This blocker was rechecked against current USPTO Open Data Portal documentation on 2026-09-02 and remains valid.

Relevant current access facts:

- ODP access requires a valid USPTO.gov account/login;
- Bulk Data API access requires authentication/API credentials;
- the legacy public PatentsView S3 route previously tested in GitHub Actions returned HTTP 403;
- the former Developer Hub route is no longer a valid production path.

### Recovery condition A — official bulk file

Download the relevant official PatentsView/USPTO bulk tables from an authenticated ODP session and make the TSV/CSV input available to the research runtime.

Then run:

```bash
cd My_work/03_data/pilot
python collect_patents_bulk.py \
  --patent-tsv <OFFICIAL_PATENT_BULK_FILE> \
  --max-total 500 \
  --cutoff 2026-06-30
```

### Recovery condition B — authenticated export/API

If an authenticated ODP export/API becomes available, normalize its output to the fields expected by `collect_patents_bulk.py` or the Pilot schema.

### Provenance rule

Third-party mirrors must not silently replace official USPTO/PatentsView data in WP3. If used at all in WP2, they must be explicitly labeled `PILOT_ONLY_MIRROR` and excluded from final production-data claims unless provenance is separately validated.

---

## 3. GitHub and VDP layers

No external credential blocker currently prevents formal Pilot execution.

Formal historical corpus already persisted under the 2026-06-30 cutoff:

- GitHub/Open Source: 450
- Vulnerability Demand / VDP: 500
- O/V total: 950

VDP group balance is substantially improved relative to the first 140-record batch, although W05 remains the smallest stratum and should be monitored in final modeling.

---

## 4. Human gold validation

### Current status

`READY_FOR_INDEPENDENT_HUMAN_REVIEW / 0 FINALIZED GOLD`

The 300-record package is now:

- blinded to model predictions;
- keyed by stable SHA1-derived `review_id` rather than row order;
- synchronized to screening version `1.3.2`;
- paired with a hidden prediction map for post-review evaluation only.

Files:

- `output/human_review_blind_300.csv`
- `output/human_review_prediction_map_300.jsonl`
- `output/human_review_manifest.json`
- `human_gold_review_protocol_v1.md`

The merge/evaluation dry run has passed with all 300 review IDs matched and `n_finalized_gold=0`. AI prereview/diagnostic output must not populate `AGREED` or `ADJUDICATED`.

---

## 5. Screening candidate status

Current candidate screening version:

`v1.3.2 — CANDIDATE / NOT FROZEN`

Relative to v1.3.1, only 9/950 O/V records changed, including one in-scope → out-of-scope change. The changes are narrowly targeted at reference/paper feeds and the T02 automated-repair versus T12 vulnerability-intelligence boundary.

Two 60-record audit samples are available:

- centrality false-negative audit: 60/123 pool;
- in-scope false-positive audit: 60/167 pool.

A reproducible diagnostic report flags recurring lexical and container/reference patterns but is explicitly not a gold error-rate estimate.

---

## 6. Gate 2B release rule

WP2 cannot move to DONE until all of the following are satisfied or formally revised in the research protocol:

1. Science Pilot present and source behavior audited;
2. Patent Pilot present and provenance verified;
3. GitHub Pilot near target and source-role audited;
4. VDP Pilot near target and group balance audited;
5. >=300 independent/human gold reviews finalized as `AGREED` or `ADJUDICATED`;
6. in-scope Precision >=0.90;
7. primary-family macro-F1 >=0.80;
8. high-frequency family F1 >=0.85;
9. temporal/provenance leakage checks pass.

Until these conditions are met:

**WP2 = IN_PROGRESS; Gate 2B = IN_PROGRESS; WP3 must not start.**
