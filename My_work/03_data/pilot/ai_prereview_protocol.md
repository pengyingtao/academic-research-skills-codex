# WP2 Gate 2B — AI Pre-review Protocol

**Version:** 1.0  
**Date:** 2026-09-02  
**Status:** ACTIVE

## 1. Purpose

AI-assisted pre-review is used only to reduce the manual annotation burden for the 300-record Gate 2B review set. It must not be represented as human gold labeling.

## 2. Status separation

Allowed pre-review status values:

- `AI_PREREVIEW_AGREE_AUTO`
- `AI_PREREVIEW_DISAGREE_AUTO`
- `AI_PREREVIEW_AMBIGUOUS`
- `AI_PREREVIEW_NEEDS_SOURCE_READ`

Only a later human/independent adjudication step may set:

- `gold_status=AGREED`
- `gold_status=ADJUDICATED`

`evaluate_gold.py` therefore remains unchanged and ignores AI pre-review-only records.

## 3. Review priority

Priority order:

1. records whose labels changed between keyword/screening v1.1 and v1.2;
2. LOW/MEDIUM-confidence supply records;
3. personal-profile / aggregator / education exclusions;
4. offensive / dual-use boundary cases;
5. family-boundary cases with multiple plausible Txx labels;
6. VDP mapping records;
7. random HIGH-confidence controls.

## 4. Pre-review fields

Each AI pre-review record should preserve the automatic prediction and add:

- `ai_prereview_status`
- `ai_suggested_in_scope`
- `ai_suggested_primary_technology_id`
- `ai_suggested_secondary_technology_ids`
- `ai_suggested_use_orientation`
- `ai_suggested_false_positive_type`
- `ai_suggested_artifact_type`
- `ai_suggested_vdp_group`
- `ai_review_confidence`
- `ai_review_note`

No `gold_*` field may be populated by the AI pre-review process.

## 5. Decision rules

### Supply records

A record is in scope only if the evidence supports both:

1. an identifiable AI/ML method or AI-enabled autonomous capability; and
2. a primary cybersecurity defensive capability mapped to T01–T15.

Exclude or separately classify:

- personal profile/resume repositories;
- generic AI repositories;
- generic software engineering without a security objective;
- training/certification-only artifacts;
- catalogs/awesome lists/resource aggregators;
- Security-of-AI rather than AI-for-Cybersecurity;
- offensive-only pentesting/exploit automation.

### VDP records

Vulnerability records remain demand-pressure evidence only. They must not receive a T01–T15 gold family. AI pre-review checks CWE-group consistency and temporal/provenance semantics only.

## 6. Human finalization

The compact CSV is the handoff surface for human review. Human reviewers may accept or override AI suggestions. Final Gate metrics are computed only after at least 300 records receive valid human/independent `gold_status` values.

## 7. Reporting rule

Before final gold completion, any calculated agreement or accuracy statistic must be labeled `PROVISIONAL` and must not be used as the paper's taxonomy validation result.
