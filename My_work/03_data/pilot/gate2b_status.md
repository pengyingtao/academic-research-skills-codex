# Gate 2B Status

Updated: 2026-09-01

## Current status

**Gate 2B: IN_PROGRESS**

## Completed engineering assets

- Query pack frozen: `query_pack_v1.yaml`
- Unified JSONL helpers: `common.py`
- OpenAlex collector: `collect_openalex.py`
- GitHub collector: `collect_github.py`
- NVD collector: `collect_nvd.py`
- PatentsView/USPTO bulk filter: `collect_patents_bulk.py`
- Conservative supply/VDP screen: `screen_candidates.py`
- Manual review queue builder: `build_review_queue.py`
- Gate metrics evaluator: `validate_taxonomy.py`
- Current KEV/EPSS sanity enrichment: `enrich_vdp_current.py`
- Historical VDP protocol: `historical_vdp_protocol.md`
- Manual cross-source sanity examples: `manual_sanity_samples_v0_1.jsonl`
- Partial GitHub+NVD GitHub Actions workflow: `.github/workflows/wp2-pilot-partial.yml`

## Actual acquisition state

### GitHub

- Automated partial batch launched through GitHub Actions.
- Target for first automated run: 120 repositories.
- Full Pilot target remains ~500.
- Authenticated search is used because repository search has a separate restrictive rate-limit bucket.

### NVD

- Automated partial batch is queued after GitHub collection.
- Target for first automated run: 120 CVE demand records sampled across CWE strata.
- Full Pilot target remains ~500.
- NVD API key is optional; no-key mode is intentionally throttled.

### OpenAlex

- Collector is implemented.
- Formal API collection is not executed because the repository does not currently provide `OPENALEX_API_KEY`.
- Current OpenAlex API requires a free API key. For WP3 scale, quarterly snapshot remains the preferred bulk route.

### Patents

- Bulk filtering pipeline is implemented.
- Formal 500-record Patent Pilot is not executed because a PatentsView/USPTO bulk file has not yet been materialized in the repository/runtime.
- PatentsView PatentSearch API requires a key, and new key grants are currently suspended; therefore bulk data is the primary planned route.

## No-synthetic-data rule

Missing OpenAlex key or patent bulk input must not be replaced with invented/synthetic records merely to reach 2,500. Gate 2B counts only real retrieved records.

## Gate 2B remaining conditions

1. Complete first GitHub+NVD automated batch and inspect failure/coverage statistics.
2. Materialize OpenAlex Science candidates with API key or snapshot-based route.
3. Materialize Patent candidates from PatentsView/USPTO bulk data or an existing valid key.
4. Merge/deduplicate toward the ~2,500 Pilot target.
5. Generate at least 300-record manual review queue.
6. Fill gold labels and compute:
   - in-scope Precision
   - Primary-family macro-F1
   - per-family F1/confusion
   - GitHub orientation/artifact accuracy
   - VDP point-in-time missingness/coverage
7. Freeze taxonomy version for WP3 only if Gate thresholds pass.
