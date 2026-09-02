# WP2 Gate 2B — Human / Independent Gold Adjudication Protocol V1

**Date:** 2026-09-02  
**Status:** READY_FOR_REVIEW  
**Target:** >=300 records

## 1. Purpose

This protocol defines the independent gold-label procedure used to validate the AI-for-Cybersecurity screening and T01–T15 taxonomy before Gate 2B can pass.

The first-pass reviewer must be blinded to model/automatic predictions to reduce anchoring bias.

## 2. Files

### Reviewer-facing file

`output/human_review_blind_300.csv`

Contains only:

- review ID;
- source type / native ID;
- date;
- title/name;
- evidence excerpt;
- empty gold fields.

### Hidden prediction mapping

`output/human_review_prediction_map_300.jsonl`

Contains the automatic screening output for the same review IDs. This file must not be consulted during first-pass independent review.

### Manifest

`output/human_review_manifest.json`

Defines sample size, screening version and merge key.

## 3. First decision — source role

For `science`, `patent`, `open_source` supply records, answer:

> Is this record substantively about an AI-enabled cybersecurity defensive capability?

`gold_in_scope = true` requires BOTH:

1. an identifiable AI/ML/autonomous-intelligence mechanism; and
2. a primary cybersecurity defensive objective.

Reject or separately classify:

- generic AI without a cybersecurity defensive objective;
- Security-of-AI where the protected target is the AI model/system itself;
- offensive-only exploitation/pentesting automation;
- personal profiles/resumes;
- catalogs, awesome lists, paper feeds, vendor lists and resource aggregators;
- training/certification/tutorial-only artifacts;
- conventional cyber tools in which AI is only a peripheral/integration mention.

For `vulnerability` records, do NOT assign T01–T15. Review CWE/VDP grouping and temporal semantics only.

## 4. Primary family assignment

Assign exactly one primary Txx for in-scope supply records based on the principal capability implemented or studied.

Use secondary labels only for substantive additional capabilities.

Important boundaries:

- T01 Vulnerability Discovery: finding/localizing software or binary weaknesses;
- T02 Automated Program Repair: generating/validating code-level security fixes or patches. Vulnerability prioritization or remediation advice alone is NOT T02;
- T04 Intrusion/Anomaly Detection: network/endpoint anomalous or intrusion behavior;
- T06 Botnet/DDoS/Malicious Infrastructure: dedicated botnet, C2, DDoS or infrastructure detection;
- T07 Cyber Threat Intelligence: IOC/TTP extraction, CTI reasoning, threat knowledge;
- T08 Threat Hunting: active hunt/investigation hypotheses and attack-chain investigation;
- T09 AI SOC / Security Agent: system-level copilot/agent/autonomous SOC operations. Narrow sub-capabilities may be secondary;
- T10 Incident Response / Orchestration: response playbooks, containment and security orchestration;
- T11 Digital Forensics: forensic evidence and artifact analysis;
- T12 Attack Surface / Exposure / Vulnerability Prioritization: exposure/risk prioritization and attack-surface management;
- T15 Secure Software / Code Security Analysis: secure code review, SAST/DAST and software security analysis.

## 5. Orientation

Allowed values:

- `DEFENSIVE`
- `DUAL_USE_DEFENSE_PRIMARY`
- `DUAL_USE_OFFENSE_PRIMARY`
- `OFFENSIVE`
- `UNCLEAR`

Offensive-primary records are outside the main AI-for-Cybersecurity supply corpus even if technically sophisticated.

## 6. Gold status

Allowed final status values:

- `AGREED` — independent reviewer is confident in the final label;
- `ADJUDICATED` — disagreement/ambiguity was resolved by a second-pass adjudication.

Do not use `AGREED` merely because the reviewer agrees with an AI prereview; the first-pass review should be performed blind.

## 7. Reviewer confidence

Use:

- `HIGH` — evidence directly supports the decision;
- `MEDIUM` — evidence is sufficient but boundary-sensitive;
- `LOW` — full source reading or second reviewer is needed.

LOW-confidence records should enter adjudication rather than being forced into a final family.

## 8. Minimum validation metrics

After >=300 valid gold records:

- supply in-scope Precision >= 0.90;
- primary-family macro-F1 >= 0.80;
- high-frequency family F1 >= 0.85;
- GitHub artifact/orientation accuracy reported separately;
- VDP mapping consistency and missingness reported separately.

## 9. Additional bias-control checks

The 300-record main sample is supplemented by:

- 60-record centrality false-negative audit;
- 60-record in-scope false-positive audit.

These targeted audits are not substitutes for the main gold sample. They test failure modes that a random review set may underrepresent.

## 10. Freeze rule

Taxonomy/screening must not be frozen for WP3 until gold metrics are calculated and error analysis shows no unresolved structural failure mode.
