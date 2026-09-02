# Gate 2B Human Gold Review Protocol V1

> Scope: WP2 Pilot Corpus taxonomy validation only.
>
> Status: ACTIVE PROTOCOL. This protocol defines what may be counted as `gold` for Gate 2B. AI-assisted prereview is explicitly excluded from final gold status.

## 1. Objective

Construct at least 300 independently reviewed records for estimating:

- supply in-scope precision/recall/F1;
- T01–T15 primary-family confusion and macro-F1;
- GitHub artifact-type / use-orientation quality;
- VDP weakness-group mapping quality.

The review must not expose the model prediction during first-pass annotation.

## 2. Blinded package

First-pass reviewers use only:

`output/human_review_blind_300.csv`

They must not open:

`output/human_review_prediction_map_300.jsonl`

until all first-pass labels for their assigned records are locked.

`review_id` is a stable SHA1-derived identifier based on `source_type + source_native_id`; it is not row-order dependent.

## 3. Reviewer structure

### Reviewer A

Independently labels all 300 records.

### Reviewer B

Independently labels the same 300 records using a separate copy of the blinded file. Reviewer B must not see Reviewer A's labels or model predictions before submission.

### Adjudication

After both independent passes are frozen:

- exact substantive agreement -> `gold_status=AGREED`;
- any disagreement in `gold_in_scope`, primary family, source role, or VDP group -> adjudication;
- adjudicated final decision -> `gold_status=ADJUDICATED`;
- unresolved cases -> `gold_status=UNRESOLVED` and are excluded from Gate metrics until resolved.

## 4. Required fields

For supply records (`science`, `patent`, `open_source`):

- `gold_in_scope`
- `gold_primary_technology_id` when in-scope
- `gold_secondary_technology_ids` when justified
- `gold_use_orientation` when applicable
- `gold_artifact_type` for GitHub
- `reviewer_confidence`
- `reviewer_note` for ambiguous/boundary cases

For vulnerability-demand records:

- no T01–T15 positive label
- `gold_vdp_group`
- `reviewer_confidence`
- `reviewer_note` when mapping is ambiguous

## 5. Decision hierarchy

Reviewers must apply labels in this order:

1. **Source role** — technology supply vs vulnerability demand vs auxiliary/reference artifact.
2. **In-scope** — is the record evidence of AI used for cybersecurity defense/operations?
3. **Orientation** — defensive, dual-use defense-primary, dual-use offense-primary, offensive.
4. **Primary family** — final defensive objective, not merely a keyword hit.
5. **Secondary family** — only for a real second capability, not contextual mention.
6. **Artifact type / VDP group** — source-specific fields.

## 6. High-risk boundary rules

### GitHub containers are not automatically engineering implementations

Examples requiring exclusion or auxiliary treatment unless the repository itself implements the capability:

- personal/profile repository;
- blog/portfolio;
- paper/reference feed;
- awesome/curated list;
- vendor/tool catalog;
- third-party API/company profile;
- broad learning roadmap/training repository;
- multi-project hub where the actual technology exists only in linked child repositories.

### Student/hackathon projects

A student, dissertation, portfolio-oriented, or hackathon repository is **not excluded solely because of its origin**. It can count as engineering-supply evidence when the repository itself contains a functioning implementation of an in-scope AI-for-cybersecurity capability. A profile/container that only describes linked projects does not count as the implementation.

### T02 automated vulnerability repair

T02 requires code-level vulnerability repair / patch generation / secure refactoring / generated patch validation. Risk scoring, patch recommendation, remediation advice, or vulnerability prioritization without generated code-level repair should not receive T02 solely because the word `patch` appears.

### T09 AI SOC / Security Agent

Use T09 as primary when the central capability is an AI copilot/agent/autonomous workflow for SOC investigation, triage, correlation, analyst assistance, or security operations. Narrow detectors remain the primary family when the system is fundamentally a detector with only incidental chatbot/agent features.

## 7. Gold status semantics

Only the following are counted by `evaluate_gold.py`:

- `AGREED`
- `ADJUDICATED`

The following do not count as final gold:

- blank
- `SINGLE_REVIEWED`
- `AI_PREREVIEW`
- `UNRESOLVED`

AI assistance may create separate `AI_PREREVIEW_*` fields for triage, but it must never set or infer `AGREED`/`ADJUDICATED`.

## 8. Model merge and evaluation

After human decisions are frozen, evaluate using:

```bash
python evaluate_gold.py \
  --blind-csv output/human_review_blind_300.csv \
  --prediction-map output/human_review_prediction_map_300.jsonl \
  --out output/gate2b_gold_metrics.json
```

The evaluator verifies stable `review_id` matching before merging predictions with gold labels.

## 9. Reporting guardrail

Before 300 records have `AGREED` or `ADJUDICATED` status:

- any metric is diagnostic/provisional only;
- do not report it as Gate 2B precision/F1;
- do not freeze the taxonomy based on AI prereview agreement;
- do not enter WP3 on the basis of automatic screening statistics alone.

## 10. Gate decision

Gate 2B can be considered only after:

1. >=300 finalized independent/human gold records;
2. supply precision and primary-family macro-F1 are calculated from the blinded merge;
3. per-family confusion is inspected for high-frequency families;
4. GitHub artifact/orientation errors are audited;
5. VDP records have zero direct T01–T15-label violations;
6. Science, Patent, Open Source and Vulnerability source behavior has been reviewed across the intended multi-source design.
