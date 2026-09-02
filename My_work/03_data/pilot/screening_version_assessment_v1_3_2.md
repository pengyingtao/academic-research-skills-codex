# WP2 Gate 2B — Screening Version Assessment V1.3.2

**Date:** 2026-09-02  
**Status:** CANDIDATE — NOT FROZEN  
**Taxonomy:** 1.1  
**Screening/keyword revision:** 1.3.2

## 1. Fixed regression corpus

All V1.3.1 -> V1.3.2 comparisons use the same formal historical O/V corpus:

- GitHub/Open Source: 450
- Vulnerability Demand/VDP: 500
- Total: 950
- cutoff: 2026-06-30

No new records were added during this screening regression.

## 2. Changes from V1.3.1

V1.3.2 intentionally makes only two narrow boundary corrections:

1. **Reference/paper feeds are not engineering implementations.** Automated arXiv/paper lists and comparable reference feeds map to `AGGREGATOR_NOT_TOOL` unless the repository itself implements the in-scope capability.
2. **T02 is code-level automated vulnerability repair.** Patch recommendation, remediation advice, vulnerability intelligence or risk prioritization do not qualify as T02 without explicit generated code repair / patch synthesis / secure refactoring evidence. These records may map to T12 when the actual objective is prioritization/risk/remediation intelligence.

## 3. Regression effect

V1.3.1 -> V1.3.2 on 950 records:

- changed records: **9**
- TRUE -> TRUE: **7**
- TRUE -> FALSE: **1**
- FALSE -> FALSE: **1**

Primary-family transitions include:

- T02 -> T12: 1
- T04 -> T12: 1
- T01 -> T02: 3
- T14 -> NONE: 1

The single TRUE -> FALSE case is an automated arXiv/reference feed that had been incorrectly treated as a cyber-deception implementation.

Examples supporting the T02/T12 correction:

- `23CSBS041/Patch-vulnerability-checker`: vulnerability enrichment, risk scoring and patch recommendations -> T12 rather than T02;
- `OmarHassan-99/WebPatcher`: explicit LLM-generated security patches plus validation -> T02;
- attack-chain scanner projects that include actual code remediation evidence can map to T02; detection-only functionality remains T01/T04 as appropriate.

Conclusion: the delta is small and explainable, so V1.3.2 supersedes V1.3.1 as the **current candidate**.

## 4. Audit evidence

Two stratified 60-record audit sets are retained:

- `centrality_false_negative_audit.jsonl`: 60 sampled from 123 `NO_AI_SIGNAL` GitHub records;
- `in_scope_false_positive_audit.jsonl`: 60 sampled from 167 automatically in-scope GitHub records.

`screening_audit_diagnostics_v1_3_2.json` identifies recurring diagnostic flags.

### Centrality lexical misses

Observed flags include:

- `AI-assisted`: 3
- `machine-learning`: 2
- autonomous/agent language: 2
- CNN/LSTM/RNN: 1
- tree-ensemble wording: 1

These flags show that the centrality rule can miss AI methodology when wording differs from the current anchor list. They do **not** prove that each flagged record belongs in scope.

### In-scope container/reference risk

Observed overlapping flags include:

- reference/paper feeds: 5
- catalog/hub: 7
- blog/reference content: 6
- third-party profile: 3
- owner==repo profile: 5
- training/learning: 3

These are review-priority flags, not gold false-positive counts.

## 5. Why V1.3.3 is not yet created

Do not add every missed model term (CNN, LSTM, Random Forest, XGBoost, etc.) to the general AI gate yet.

Reason:

- broad algorithm names can appear in non-cyber/non-AI-central contexts;
- current audit flags overlap;
- Science and Patent source language differs from GitHub README language;
- a global vocabulary expansion before cross-source review risks repairing GitHub recall while degrading cross-source precision.

The next vocabulary revision should therefore be source-aware and supported by independent gold errors, not only AI prereview.

## 6. Human gold package

The formal 300-record review package is now synchronized to V1.3.2 and uses stable SHA1-derived `review_id` values.

- blind evidence: `output/human_review_blind_300.csv`
- hidden predictions: `output/human_review_prediction_map_300.jsonl`
- manifest: `output/human_review_manifest.json`
- protocol: `human_gold_review_protocol_v1.md`

A dry-run merge verified:

- blind rows: 300
- prediction rows: 300
- merged IDs: 300
- screening version: 1.3.2
- finalized human gold: 0
- Gate result: correctly blocked/incomplete

## 7. Source-access update

### OpenAlex

OpenAlex is no longer classified as a hard credential blocker. Current official documentation permits basic keyless API use with a smaller daily budget; an isolated GitHub Actions probe returned HTTP 200 without a key.

A low-budget Boolean retrieval design is being tested to minimize search calls and preserve family coverage.

### Patent

USPTO/PatentsView remains an authenticated ODP blocker. Official current access requires USPTO.gov login, and Bulk API use requires authenticated credentials/API access.

## 8. Freeze conditions

V1.3.2 remains **NOT FROZEN** until:

1. >=300 records reach human `AGREED` or `ADJUDICATED` gold status;
2. supply in-scope Precision >=0.90;
3. primary-family macro-F1 >=0.80;
4. high-frequency family F1 >=0.85;
5. centrality false-negative behavior is measured against independent human labels;
6. container/reference exclusions are checked for accidental removal of real implementations;
7. Science and Patent layers are present and cross-source behavior is validated;
8. temporal/provenance leakage audit passes.

**Current verdict: retain V1.3.2 as the active candidate, continue Gate 2B, do not enter WP3.**
