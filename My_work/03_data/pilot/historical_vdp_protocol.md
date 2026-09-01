# Historical VDP Reconstruction Protocol

## Purpose

VDP must be reconstructable at each historical forecast cutoff. Current CVSS/KEV/EPSS values must not be backfilled into older folds unless the value is demonstrably knowable at that time.

## Components

### CVE/CWE/CVSS

Use NVD/CVE records with publication and modification timestamps. For a cutoff `t`, materialize the latest record state available on or before `t`. Current enriched values are not assumed to have existed at publication time.

### KEV

CISA KEV is an exploitation-evidence signal. The usable historical feature is:

`KEV(cve,t) = 1 if dateAdded <= t else 0`

A vulnerability added to KEV after the cutoff must be treated as non-KEV for that historical fold.

### EPSS

Use FIRST's historical daily score archive or API date parameter. EPSS historical data are available from 2021-04-14 onward. The feature for a cutoff must be the score published on or before the cutoff date.

Important: EPSS model versions change over time, so score discontinuities across model-version boundaries are partly methodological. Preserve `epss_model_version` where available and test robustness using within-version normalization or version indicators.

Known historical model periods from FIRST documentation at protocol creation:

- EPSS v1: from 2021-04-14
- EPSS v2: publishing from 2022-02-04
- EPSS v3: publishing from 2023-03-07
- EPSS v4: publishing from 2025-03-17
- EPSS v5: publishing from 2026-06-15

## VDP materialization

For technology/pressure group `k` and quarter `t`, candidate features include:

- CVE count published by `t`
- new CVE count in quarter
- median/max CVSS base score known at `t`
- exploitability-score distribution known at `t`
- KEV count with `dateAdded <= t`
- EPSS mean/max/top-decile share using the score snapshot at `t`
- affected vendor/product diversity
- remediation-gap proxy where patch/advisory timing is auditable

The final VDP formula is not frozen in WP2. WP2 only establishes that historical components are obtainable without future leakage. Formula selection and ablation occur in WP4/WP6.

## Gate 2B checks

Before closing WP2, report:

1. percentage of sampled CVEs with usable CWE;
2. percentage with CVSS known at the relevant observation point;
3. percentage with CPE/vendor/product mapping;
4. historical KEV reconstructability from `dateAdded`;
5. historical EPSS coverage by year (2021 onward only);
6. explicit missing-value strategy for 2012–2020, when EPSS does not exist.

For 2012–2020, EPSS must be marked structurally unavailable rather than imputed as if it had existed. Alternative exploitation proxies may be tested later but must remain distinguishable from EPSS.
