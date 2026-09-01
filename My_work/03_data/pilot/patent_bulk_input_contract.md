# WP2 Patent Bulk Input Contract

**Status:** READY_FOR_INPUT  
**Formal target:** ~500 patent candidates  
**Research cutoff:** 2026-06-30

## 1. Formal source policy

The formal WP2 patent Pilot must use PatentsView/USPTO bulk data or an existing authenticated PatentSearch/USPTO API export. Google Patents pages are retained only for sanity checking and individual boundary examples; they are not the formal 500-record corpus.

## 2. Preferred ingestion path

Place a PatentsView/USPTO tab-delimited bulk file in a local/CI-accessible path and run:

```bash
cd My_work/03_data/pilot
python collect_patents_bulk.py \
  --patent-tsv <PATH_TO_BULK_TSV> \
  --max-total 500 \
  --cutoff 2026-06-30
python screen_candidates.py output/patent_candidates.jsonl
```

The collector reads in chunks and therefore does not require loading the entire bulk dataset into memory.

## 3. Minimum accepted fields

The normalizer resolves common aliases for:

- patent/publication id (required)
- title (required)
- abstract (strongly recommended)
- publication/patent date (required for temporal freeze)
- application id (optional)
- assignee (optional)

Accepted alias examples are encoded in `collect_patents_bulk.py`.

## 4. Formal candidate logic

A patent is only a candidate when:

1. title/abstract contains at least one AI-method signal from `query_pack_v1.yaml`;
2. title/abstract contains at least one T01–T15 cybersecurity capability signal;
3. event/publication date is on or before `2026-06-30`.

The candidate family is not the final gold label. Abstract/claims evidence must still pass semantic screening.

## 5. Required enrichment after candidate extraction

For final Gate 2B validation, candidate patents should be enriched where available with:

- CPC / IPC classifications;
- claims evidence or at least independent-claim text for boundary cases;
- assignee and inventor metadata;
- patent citations;
- non-patent literature citations;
- application/priority/family identifiers for later deduplication.

The 500-record taxonomy Pilot may proceed with title+abstract first, but WP3 production data must add structural metadata needed for graph construction.

## 6. Quality checks

Before patent records count toward Gate 2B:

- unique patent ids after source-level deduplication;
- no event date after research cutoff;
- no `nan`/missing-title candidates;
- AI signal and cybersecurity family signal both recorded;
- hard boundary sample for T01 vs T04 vs T12;
- hard boundary sample for security program repair T02 vs generic program repair;
- at least a subset reviewed using claims/CPC where title/abstract is ambiguous.

## 7. Current external dependency

Current USPTO Open Data Portal access is account-gated and programmatic APIs require authentication. Therefore this repository does not fabricate or scrape a replacement dataset.

Formal patent status remains:

`WAITING_FOR_BULK_INPUT_OR_EXISTING_AUTHENTICATED_EXPORT`.

Once a bulk file/export is available, the normalizer is ready to execute without changing the taxonomy protocol.
