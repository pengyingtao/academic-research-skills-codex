# Gate 2B Gold Review Protocol V1

## 1. Purpose

This protocol defines the human-reviewed gold set used to decide whether WP2 may pass Gate 2B. Automatic screening labels must never be treated as gold labels.

## 2. Minimum evidence volume

Target: at least 300 finalized review records.

Strata:

- 120 randomly sampled S/T/O supply records;
- 80 LOW/MEDIUM confidence or `needs_review=true` records;
- 50 family-boundary/confusion records;
- 25 offensive/dual-use GitHub records;
- 25 VDP mapping records.

If a Txx family has fewer than 20 candidates, all available records from that family enter the review candidate pool.

## 3. Gold fields

Each reviewed record must retain the original prediction and add:

- `gold_in_scope`: true/false;
- `gold_primary_technology_id`: T01–T15 or null;
- `gold_secondary_technology_ids`: list;
- `gold_use_orientation`: DEFENSIVE / DUAL_USE_DEFENSE_PRIMARY / DUAL_USE_OFFENSE_PRIMARY / OFFENSIVE / UNCLEAR;
- `gold_artifact_type`: GitHub only;
- `gold_vdp_group`: vulnerability only;
- `gold_false_positive_type`: optional;
- `reviewer_1`;
- `reviewer_1_reason`;
- `reviewer_2`;
- `reviewer_2_reason`;
- `adjudicated`: true/false;
- `adjudicator`;
- `adjudication_reason`;
- `gold_status`: PENDING / AGREED / ADJUDICATED / EXCLUDED;

## 4. Review rule

### Supply records (Science / Patent / Open Source)

Review in this order:

1. Is AI/ML actually used as part of the cybersecurity capability?
2. Is the primary orientation AI for Cybersecurity rather than Security of AI or offense-only?
3. What is the principal defended object/action?
4. Which Txx family best represents that principal capability?
5. Are secondary families materially present, or merely mentioned?

### Vulnerability records

Do not assign T01–T15.

Review only:

- CWE extraction correctness;
- W01–W07/W99 group mapping;
- CVSS/exploitability field correctness;
- KEV/EPSS point-in-time semantics;
- affected product/vendor extraction quality.

## 5. Blinding

Where feasible, reviewers should decide gold labels without being shown the model confidence. The predicted family may be hidden in the first-pass review interface and revealed only during adjudication.

## 6. Agreement and adjudication

- Exact agreement on `gold_in_scope` is required.
- For in-scope supply records, exact agreement on primary Txx is required.
- Disagreements go to adjudication.
- A record is counted in final metrics only when `gold_status` is AGREED or ADJUDICATED.

Recommended inter-rater statistics before adjudication:

- Cohen's kappa for in-scope;
- Cohen's kappa for primary-family labels on mutually in-scope records.

## 7. Gate 2B metrics

### Supply screening

- In-scope Precision target ≥ 0.90;
- In-scope Recall reported (no hard gate unless expanded-negative sampling supports it);
- Primary-family macro-F1 target ≥ 0.80;
- High-frequency-family F1 target ≥ 0.85;
- family confusion matrix required.

### GitHub

Report separately:

- artifact-type accuracy;
- offensive/defensive orientation accuracy;
- ENGINEERING_SUPPLY / AUXILIARY_EVIDENCE / DISCOVERY_ONLY composition.

### Vulnerability demand

Do not compute Txx F1. Report:

- CWE/W-group agreement;
- CVSS completeness;
- KEV point-in-time completeness;
- EPSS point-in-time completeness (only dates supported by EPSS history);
- affected product/vendor completeness.

## 8. Leakage rule

Gold review may improve taxonomy/keywords during WP2, but any taxonomy changes made using post-cutoff knowledge must be versioned. Historical WP7 folds must use a taxonomy/materialization policy frozen consistently for the fold, rather than silently using future labels.

## 9. Gate decision

WP2 passes Gate 2B only after:

1. all four source roles have real Pilot data;
2. ≥300 gold records are finalized;
3. supply Precision and macro-F1 thresholds are met;
4. VDP point-in-time fields are operationally available;
5. the production taxonomy version for WP3 is frozen.
