# WP2 Gate 2B — Formal Partial Historical Pilot Status

**Date:** 2026-09-01  
**Status:** IN_PROGRESS  
**Counts toward Gate 2B:** YES, for GitHub + VDP source/schema validation only

## 1. Formal partial batch

The third automated batch completed successfully end-to-end and is the first batch counted as a formal historical Pilot subcorpus.

Research cutoff: `2026-06-30`.

Actual screened records:

- GitHub/Open Source: 140
- Vulnerability Demand / VDP: 140
- Total: 280

The workflow completed collection, point-in-time VDP materialization, screening, summarization, review-queue generation, rebase and persistence to the repository.

## 2. GitHub formal rules

Repositories must satisfy:

`created_at <= 2026-06-30`

Current stars/forks and similar popularity values remain stored only as current-as-observed metadata and are prohibited from historical backtest features unless a valid historical reconstruction is created in WP3.

### Current artifact distribution

- production_platform: 64
- tool_framework: 43
- paper_code: 15
- offensive_tool hard negatives: 18

This is substantially cleaner than the previous current-sanity batch, where catalog and dataset repositories were overrepresented.

### Current orientation distribution

- DEFENSIVE: 91
- DUAL_USE_DEFENSE_PRIMARY: 15
- OFFENSIVE: 8
- UNKNOWN: 26

The OFFENSIVE and selected UNKNOWN cases are retained as hard negatives / review cases rather than positive engineering-supply evidence.

## 3. VDP formal rules

NVD sampling now uses deterministic publication-date windows of at most 120 days across the historical research period instead of unbounded current CWE search results.

At research cutoff, each sampled CVE is materialized with:

- KEV status subject to `dateAdded <= cutoff`;
- EPSS using the explicit historical observation date `2026-06-30`;
- CVSS/CWE/CPE and affected vendor/product data;
- the original NVD publication-window identifier.

Spot checks confirm that the point-in-time materializer writes `materialized_cutoff`, `kev_status_at_cutoff`, `epss_score_at_cutoff`, `epss_percentile_at_cutoff`, and `epss_observation_date` rather than reusing current enrichment fields.

### Current weakness distribution

- W01 memory safety: 59
- W02 injection / traversal / unsafe interpretation: 47
- W03 authentication / authorization: 13
- W04 crypto / credentials: 4
- W05 configuration / dependency / supply chain: 2
- W06 availability / resource exhaustion: 8
- W07 concurrency / state / logic: 7

Interpretation: W01/W02 are currently overrepresented and W04/W05 are underrepresented. The 500-record VDP Pilot must use quota balancing rather than simple proportional continuation.

## 4. Automatic screening distribution

Across 280 formal partial records:

- auto in-scope: 246
- auto out-of-scope: 34
- HIGH confidence: 67
- MEDIUM confidence: 179
- LOW confidence: 24
- REJECT: 10

GitHub auto-family counts currently cover most Txx families but are sparse for T12/T14/T15 and absent/sparse for some families. This batch is not sufficient to judge taxonomy macro-F1.

## 5. Review queue correction

The first review queue retained full text and became unnecessarily large. `build_review_queue.py` has been revised to generate compact annotation-ready JSONL/CSV with:

- source id and date;
- title/name;
- max 1200-character evidence excerpt;
- automatic in-scope/family/orientation/artifact labels;
- gold-label fields for human review.

The final Gate 2B gold set remains targeted at >=300 reviewed records after all four sources are present.

## 6. Remaining external acquisition dependencies

### Science / OpenAlex

OpenAlex REST API currently requires a free API key. The complete public snapshot is free and quarterly, but is roughly hundreds of GB compressed, so downloading the entire snapshot inside GitHub Actions is not an efficient Pilot strategy.

Implementation status:

- collector code: READY;
- retrieval semantics corrected to multi-query recall + deduplication;
- API execution: WAITING_FOR_OPENALEX_API_KEY or a separately provisioned local snapshot/subset.

### Technology / Patents

PatentsView/USPTO bulk data remains the preferred formal source. Current USPTO Open Data Portal access requires account authentication, and PatentSearch API requires a key.

Implementation status:

- bulk/API normalizer: READY;
- formal 500-record patent Pilot: WAITING_FOR_BULK_INPUT_OR_EXISTING_KEY.

Google Patents pages remain valid for sanity checking only and will not be substituted for the formal 500-record dataset.

## 7. Gate 2B current decision

`Gate 2B = IN_PROGRESS`.

Passed components:

- source-role schema;
- formal GitHub historical-existence cutoff;
- reproducible time-windowed NVD sampling;
- point-in-time KEV/EPSS materialization architecture;
- formal partial data persistence;
- compact human-review workflow design.

Not yet passed:

- ~1000 OpenAlex paper records;
- ~500 formal patent records;
- GitHub expansion toward ~500 engineering/boundary records;
- VDP expansion/rebalancing toward ~500;
- >=300 completed gold reviews;
- in-scope Precision >=0.90;
- primary-family macro-F1 >=0.80;
- high-frequency family F1 >=0.85.

WP3 must not start before these requirements are either met or explicitly revised with documented justification.
