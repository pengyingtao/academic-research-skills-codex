# WP2 Gate 2B — Blockers and Recovery Conditions

**Updated:** 2026-09-01

## 1. OpenAlex Science layer

### Current status

`BLOCKED_CREDENTIAL`

The repository workflow has already verified that `OPENALEX_API_KEY` is not configured.

### Recovery condition

Configure a valid OpenAlex free API key as repository secret:

`OPENALEX_API_KEY`

Then re-run:

`.github/workflows/wp2-openalex-pilot.yml`

Expected output:

- `My_work/03_data/pilot/output/openalex_candidates.jsonl`
- target: approximately 1000 Science-layer candidates
- event cutoff: 2026-06-30

### Alternative

A local OpenAlex snapshot can be processed with `collect_openalex_snapshot.py`, but a complete snapshot is too large for a normal GitHub Actions Pilot. This route is appropriate only if snapshot data are already available on suitable local/cloud storage.

---

## 2. Patent Technology layer

### Current status

`BLOCKED_AUTHENTICATED_ODP_ACCESS`

A legacy PatentsView S3 URL was tested in GitHub Actions and returned HTTP 403. The failed run is retained as execution evidence.

USPTO moved PatentsView downloads to the Open Data Portal Bulk Data Directory. Current ODP dataset access/download requires a USPTO.gov account login.

### Recovery condition A — official bulk file

Download the relevant official PatentsView bulk tables from the authenticated ODP session and make the TSV/CSV input available to the research runtime.

Then run:

```bash
cd My_work/03_data/pilot
python collect_patents_bulk.py \
  --patent-tsv <OFFICIAL_PATENT_BULK_FILE> \
  --max-total 500 \
  --cutoff 2026-06-30
```

### Recovery condition B — authenticated export/API

If an authenticated ODP/PatentsView export or API becomes available, normalize its output to the fields expected by `collect_patents_bulk.py` or the Pilot schema.

### Provenance rule

Third-party mirrors must not silently replace official USPTO/PatentsView data in WP3. If used at all in WP2, they must be explicitly labeled `PILOT_ONLY_MIRROR` and excluded from final production-data claims unless provenance is separately validated.

---

## 3. GitHub and VDP layers

No external credential blocker currently prevents formal Pilot execution.

Current expanded targets:

- GitHub main candidates: 450
- VDP: 500
- compact review queue: 300

The expansion workflow is currently executing. Its outputs only count after successful persistence to the repository.

---

## 4. Gate 2B release rule

WP2 cannot move to DONE until all of the following are satisfied or formally revised in the research protocol:

1. Science Pilot present;
2. Patent Pilot present;
3. GitHub Pilot near target and source-role audited;
4. VDP Pilot near target and group balance audited;
5. >=300 gold reviews completed;
6. in-scope Precision >=0.90;
7. primary-family macro-F1 >=0.80;
8. high-frequency family F1 >=0.85;
9. temporal/provenance leakage checks pass.
