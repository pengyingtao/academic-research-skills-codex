# External Acquisition Dependency Manifest

Updated: 2026-09-01

## OpenAlex / Science

### Status

Collector implemented, formal 1000-record Pilot not yet executed.

### Dependency

Current OpenAlex API access requires an API key. A free key is sufficient for the Pilot, but no key is stored in this repository.

### Preferred routes

- WP2 Pilot: `OPENALEX_API_KEY` + `collect_openalex.py`
- WP3 scale: quarterly OpenAlex snapshot preferred for reproducibility and bulk efficiency

### Security rule

Do not commit API keys to the repository. Provide them through GitHub Actions secrets or runtime environment variables.

## Patent / Technology

### Status

Bulk filtering pipeline implemented; formal 500-record Patent Pilot not yet executed.

### Dependency

PatentsView/USPTO patent access has changed during 2026. PatentsView bulk data remains the preferred research format where available; the USPTO Open Data Portal now requires a USPTO.gov sign-in for portal access and its APIs require an API key.

### Preferred routes

1. Materialized PatentsView/USPTO bulk TSV/CSV/XML file + `collect_patents_bulk.py`;
2. Existing valid PatentsView/USPTO API key, if available;
3. Google Patents only for retrieval-rule sanity checks, not as the formal bulk acquisition route.

### Security rule

Do not commit USPTO/PatentsView credentials or API keys.

## GitHub / Open Source

### Status

Authenticated GitHub Actions collection works. Repository search has a separate rate-limit bucket, so queries are deliberately throttled.

### Historical caveat

`created_at` can be used to enforce the 2026-06-30 corpus cutoff. Current stars/forks/activity cannot be interpreted as historical values and require later point-in-time reconstruction or event-based features.

## NVD / Vulnerability Demand

### Status

NVD collection works without a key under conservative throttling; a key is optional but materially faster.

### Historical caveat

NVD date filters have a maximum range of 120 consecutive days. Formal Pilot sampling therefore uses deterministic <=120-day windows across the research period. WP3 should use complete bulk/local materialization for population-level estimates.

## CISA KEV

Current KEV catalog can be used for sanity enrichment. Historical state is reconstructed via `dateAdded <= cutoff`.

## FIRST EPSS

Current and historical scores are accessible via the public FIRST EPSS API. Historical queries are available from 2021-04-14 onward using the `date` parameter. Pre-2021 periods are structurally missing, not zero.

## Gate 2B consequence

Gate 2B may progress with GitHub + NVD engineering validation, but it cannot be closed until real Science and Patent Pilot records are materialized and the 300-record validation sample covers the supply sources adequately.
