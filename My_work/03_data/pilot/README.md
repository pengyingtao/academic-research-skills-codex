# WP2 Pilot Corpus Collection Pipeline

## Purpose

This directory operationalizes Gate 2B for the AI-for-Cybersecurity taxonomy. The target Pilot corpus is approximately 2,500 records:

- OpenAlex / Science: ~1,000
- Patents / Technology: ~500
- GitHub / Open Source: ~500
- NVD/CVE/CWE / Vulnerability Demand: ~500

The Pilot is for taxonomy validation and source-role validation. It is not the final WP3 full dataset.

## Frozen methodological rules

1. Science/Patent/GitHub are **technology-supply evidence** and may be classified into T01–T15.
2. CVE/CWE/KEV/EPSS are **vulnerability-demand evidence** and MUST NOT be assigned T01–T15 as ground truth.
3. Every mutable observation must carry `observed_at` semantics.
4. Historical backtesting must materialize data that were knowable before each fold cutoff.
5. Offensive-only tools, Security-of-AI work and generic software-engineering repair are retained as hard negatives where useful but excluded from positive AI-for-Cybersecurity supply.

## Files

- `query_pack_v1.yaml` — versioned family queries and VDP weakness strata.
- `common.py` — shared HTTP, ID and JSONL helpers.
- `collect_openalex.py` — OpenAlex candidate collector.
- `collect_github.py` — GitHub repository candidate collector.
- `collect_nvd.py` — NVD vulnerability-demand collector.
- `collect_patents_bulk.py` — PatentsView/USPTO bulk TSV candidate filter.
- `screen_candidates.py` — conservative rule-based first-pass screening; NOT a replacement for manual validation.
- `manual_sanity_samples_v0_1.jsonl` — manually inspected cross-source boundary examples.
- `output/` — generated data; large generated files should normally be excluded from long-term Git history once WP3 begins.

## Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### OpenAlex

Current OpenAlex API access requires a free API key. Set:

```bash
export OPENALEX_API_KEY="..."
python collect_openalex.py --max-total 1000
```

For WP3 scale, prefer the quarterly OpenAlex snapshot rather than spending API budget on bulk retrieval.

### GitHub

Authenticated requests are strongly preferred because repository search has a separate restrictive rate limit.

```bash
export GITHUB_TOKEN="..."
python collect_github.py --max-total 500
```

The collector intentionally retrieves README/metadata because repository names alone are not sufficient for classification.

### NVD

An NVD API key is optional but strongly recommended. Without a key, the collector throttles heavily.

```bash
export NVD_API_KEY="..."   # optional
python collect_nvd.py --max-total 500
```

NVD output is VDP demand evidence only. KEV and historical EPSS enrichment are separate follow-up steps because historical point-in-time states must not be reconstructed from current values.

### Patents

PatentsView currently requires an API key and has temporarily suspended new key grants. For this study, the preferred path is PatentsView/USPTO bulk data.

```bash
python collect_patents_bulk.py --patent-tsv /path/to/patent_bulk.tsv --max-total 500
```

Google Patents is used only for query/sanity verification, not as the formal bulk acquisition channel.

## First-pass screening

After candidate collection:

```bash
python screen_candidates.py \
  output/openalex_candidates.jsonl \
  output/patent_candidates.jsonl \
  output/github_candidates.jsonl \
  output/nvd_candidates.jsonl
```

This creates `output/pilot_screened.jsonl`.

The rule pass is intentionally conservative. `MEDIUM`, `LOW`, dual-use and family-confusion records must enter manual review.

## Gate 2B validation plan

Minimum manual review target: 300 records.

Metrics:

- in-scope Precision target >= 0.90
- Primary-family macro-F1 target >= 0.80
- high-frequency family F1 target >= 0.85
- GitHub artifact/orientation accuracy
- VDP CWE-group coverage and point-in-time field missingness

Gate 2B remains open until the actual corpus and validation report exist. Missing external keys/bulk files are logged as acquisition dependencies, not silently replaced by synthetic records.
