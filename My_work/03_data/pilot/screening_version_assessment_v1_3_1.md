# WP2 Gate 2B — Screening Version Assessment V1.3.1

**Date:** 2026-09-02  
**Status:** CANDIDATE — NOT FROZEN  
**Taxonomy:** 1.1  
**Current screening/keyword revision:** 1.3.1

## 1. Fixed evaluation corpus

All screening-version comparisons in this document use the same formal historical O/V Pilot corpus:

- Open Source / GitHub: 450 records
- Vulnerability Demand / VDP: 500 records
- Total: 950 records
- Research cutoff: 2026-06-30

No external data were added between the rescreen comparisons. Changes therefore reflect screening logic only.

## 2. Version history

### V1.1 baseline

Key weakness observed during compact review:

- narrow AI vocabulary missed XAI / agentic AI / AI-powered wording;
- personal profile repositories, catalogs and resource aggregators could be treated as engineering supply;
- AI signal anywhere in README could influence inclusion.

Frozen baseline summary:

- in-scope: 769 / 950
- out-of-scope: 181 / 950
- NO_AI_SIGNAL: 105
- HIGH: 144

These values include all 500 VDP records, which are always demand-layer in-scope. They are not supply precision estimates.

### V1.2 — recall and hygiene expansion

Changes:

- added XAI, explainable AI, agentic AI, AI-powered / AI-driven / AI-based variants;
- added profile, catalog and education-only exclusions;
- added GitHub artifact hygiene.

Regression against V1.1:

- in-scope: +19
- NO_AI_SIGNAL: -50
- PERSONAL_PROFILE: +29
- AGGREGATOR_NOT_TOOL: +11
- HIGH: +21

Interpretation:

V1.2 repaired obvious AI vocabulary misses and removed some artifact-type noise. However targeted review showed that deep/incidental AI mentions in long READMEs could still make conventional security tools pass the AI gate.

### V1.3 — central AI gate

Changes:

- GitHub AI signal must occur in title + first 2500 characters of project evidence + topics;
- expanded personal-profile/catalog terms;
- introduced system-level T09 priority for agentic/autonomous SOC projects.

Regression against V1.2:

- in-scope: 788 -> 673 (-115)
- out-of-scope: 162 -> 277 (+115)
- PERSONAL_PROFILE: 29 -> 113
- NO_AI_SIGNAL: 55 -> 123
- T09: 19 -> 41
- 201 records changed at least one key label;
- 124 records transitioned TRUE -> FALSE;
- 154 records required high-priority targeted review.

Interpretation:

The magnitude of the change is too large to accept V1.3 without targeted review. Review of changed records found many correct removals (profile repositories, aggregators, non-AI security tools), but also exposed a code bug in SOC detection.

### V1.3.1 — SOC substring bug fix

Bug:

V1.3 used substring matching for `soc`, allowing unrelated strings containing the character sequence `soc` (e.g. `associated`) to trigger system-level T09 priority.

Fix:

- use exact word-boundary `SOC` or explicit `security operations center/centre` phrases;
- use the same exact SOC context for offensive/defensive orientation;
- add regression tests ensuring `associated` is not interpreted as SOC.

Effect relative to V1.3:

- only 12 / 950 records changed;
- 6 remained in-scope but changed primary family;
- 6 moved TRUE -> FALSE;
- T09 decreased from 41 to 33.

Current V1.3.1 summary:

- total: 950
- auto in-scope: 667
- auto out-of-scope: 283
- HIGH: 107
- MEDIUM: 560
- LOW: 26
- REJECT: 257
- PERSONAL_PROFILE: 113
- NO_AI_SIGNAL: 123
- AGGREGATOR_NOT_TOOL: 8

Again, these are screening outputs, not accuracy metrics.

## 3. Targeted AI pre-review status

AI pre-review is explicitly separated from human gold review.

Completed pre-review files:

- `analysis/ai_prereview_changed_batch01.jsonl` — 20 records
- `analysis/ai_prereview_changed_batch02.jsonl` — 10 records
- `analysis/ai_prereview_changed_batch03.jsonl` — 6 records

Total AI-pre-reviewed changed records: **36**.

Consistent findings so far:

1. profile repositories are a major source of false engineering-supply signals;
2. resource/vendor/trending/star aggregators must not count as engineering implementations;
3. AI centrality is necessary because conventional security tools can mention AI incidentally deep in a README;
4. autonomous/agentic SOC should usually be modeled as system-level T09 with narrower capabilities as secondary labels;
5. centrality must not be treated as validated until human/independent adjudication measures false negatives.

## 4. Candidate decision

**V1.3.1 is retained as the current candidate screening version, but is NOT frozen for WP3.**

Rationale:

- it fixes known false-positive mechanisms identified by targeted review;
- its unit/regression tests pass;
- it fixes the V1.3 SOC substring bug;
- but the TRUE -> FALSE shift relative to V1.2 is large enough that human gold validation is still required.

## 5. Freeze conditions

Do not freeze the screening version until:

1. >=300 independent/human gold reviews are complete;
2. in-scope supply Precision >= 0.90;
3. primary-family macro-F1 >= 0.80;
4. high-frequency family F1 >= 0.85;
5. false-negative audit specifically covers V1.3/V1.3.1 centrality exclusions;
6. profile/catalog exclusions are checked for accidental removal of organization-owned real tools;
7. Science and Patent layers are added and cross-source behavior is tested.

## 6. Current blockers outside screening

- Science/OpenAlex: official API Pilot blocked on missing `OPENALEX_API_KEY`; snapshot path remains available outside ordinary Actions runtime.
- Patent/USPTO: official Pilot blocked on authenticated ODP/bulk access.
- Human gold: 300-record compact queue exists, but AI pre-review cannot be substituted for independent gold labels.

## 7. Next executable work

While Science/Patent credentials remain blocked:

1. continue targeted AI pre-review of V1.2 -> V1.3.1 high-priority changes;
2. prepare the 300-record human adjudication package and reviewer instructions;
3. run false-negative focused sampling among `NO_AI_SIGNAL` records;
4. run false-positive focused sampling among V1.3.1 in-scope GitHub records;
5. update rules only when an error mode is supported by reviewed examples and regression tests.
