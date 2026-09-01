# WP2 Persisted Current-Sanity Batch Analysis V0.1

Batch commit: `cb45d6677c98b5ce1365023ec34ae3d813485441`

## Batch size

- GitHub candidates: 109
- NVD vulnerability-demand candidates: 120
- Total screened: 229

This batch is **not** the formal historical Pilot because the GitHub collector used current retrieval without the later-added 2026-06-30 creation cutoff. It is retained as a current-sanity/regression batch.

## Automated screening distribution

- `in_scope=True`: 198
- `in_scope=False`: 31
- HIGH: 44
- MEDIUM: 154
- LOW: 27
- REJECT: 4

The large MEDIUM count is expected because all VDP demand records are deliberately not assigned T01–T15 and are treated separately.

## GitHub technology-family candidate distribution

Among 109 GitHub candidates:

- T01: 10
- T03: 13
- T04: 14
- T05: 9
- T06: 5
- T07: 6
- T08: 3
- T09: 3
- T10: 6
- T11: 2
- T12: 2
- T14: 1
- T15: 4
- NONE/excluded: 31

T02 and T13 were absent from this small current-sanity batch. This is not interpreted as domain absence; it indicates retrieval/query coverage must be assessed at the larger formal Pilot stage.

## GitHub false-positive / boundary signals

Automated flags:

- OFFENSIVE_ONLY: 3
- GENERIC_AI: 27
- SECURITY_OF_AI: 1

The main retrieval-quality issue is not only these explicit false-positive classes. Artifact-role analysis revealed substantial auxiliary content:

- awesome-list/catalog: 21
- dataset/benchmark: 20
- CTF/demo: 2
- tutorial/course: 1
- tool/framework: 26
- production platform: 26
- paper code: 6
- offensive tool: 7

Thus 44/109 repositories were catalogs, datasets/benchmarks, CTFs or tutorials rather than direct engineering implementations. Treating all of them as equivalent Open-Source technology-supply signals would substantially distort the O layer.

## Method change triggered by the batch

GitHub O-source is now role-separated:

1. `ENGINEERING_SUPPLY`
   - tool/framework
   - production platform
   - paper code, subject to deduplication with Science records
   - offensive tool is retained only for boundary analysis and normally excluded from defensive supply
2. `AUXILIARY_EVIDENCE`
   - dataset/benchmark
   - CTF/demo
   - tutorial/course
3. `DISCOVERY_ONLY`
   - awesome-list/catalog

Formal Pilot target counts prioritize `ENGINEERING_SUPPLY`; auxiliary/discovery records are stored separately and do not receive equal engineering-activity weight.

## VDP distribution in current-sanity batch

- W01 memory-safety / low-level weaknesses: 40
- W02 injection / code-data boundary: 35
- W03 auth/access-control: 25
- W04 crypto/credential/transport: 20

W05–W07 did not appear because the original sanity collector filled its quota before reaching later strata. This is a sampling artifact, not a substantive result.

## Method change triggered by VDP distribution

Formal NVD Pilot sampling now uses deterministic <=120-day publication windows across 2012Q1–2026Q2 and round-robin traversal across CWE groups. This prevents early/high-volume weakness classes from consuming the entire quota and respects the NVD API's maximum date-range rule.

## Temporal semantics

The current-sanity batch contains current-as-observed GitHub popularity data and current KEV/EPSS enrichment. Those fields are useful only for schema validation. They MUST NOT be used as if they were historical values.

The formal partial batch instead uses:

- GitHub repository creation cutoff: 2026-06-30;
- NVD publication windows within 2012Q1–2026Q2;
- `KEV = dateAdded <= cutoff`;
- historical EPSS queried with `date=2026-06-30`.

## Status

Current-sanity batch: **DONE / retained for regression testing**.

Gate 2B: **IN_PROGRESS**.

The next formal partial batch is the first GitHub+VDP batch eligible to count toward Gate 2B source/schema validation.
