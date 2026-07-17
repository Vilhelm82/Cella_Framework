# Cella Papers Library

This is a non-destructive, digest-addressed library assembled from the active Cella
repository and the retired Lloyd Engine V4 tree. Originals remain in place.

The library contains **508 unique artifacts** representing
**547 original paths**. Exact mirrors are stored once and every
origin is retained in `_catalogue/LEDGER.json`.

## Categories

| Directory | Meaning |
|---|---|
| `01_completed_papers/` | Paper sources and rendered papers without draft markers |
| `02_theorems_and_lemmas/` | Theorem, lemma, law, correspondence, and derived-result statements |
| `03_proofs_derivations_and_audits/` | Proofs, derivations, closeoffs, and claim-level audits |
| `04_drafts_and_incomplete_papers/` | Drafts, staged manuscripts, briefs, plans, and unfinished publication work |
| `05_expository_companions_and_research_maps/` | Companions, maps, ledgers, logs, and explanatory notes |
| `06_hypotheses_conjectures_and_research_programs/` | Explicit hypotheses, conjectures, and open research programmes |
| `07_certificates_data_and_reproducibility/` | Verifiers, scripts, outputs, digests, packages, and certificate data |
| `08_patents_and_invention_disclosures/` | Patent filings, provisional drafts, and invention material |
| `09_historical_and_superseded_versions/` | Backups and explicitly older program-source versions |

Within every category, artifacts are grouped by subject family. Placement describes
the artifact's documentary role, not Cella canonical status or mathematical validity.

## Ledgers

- `_catalogue/LEDGER.json` — complete machine-readable record.
- `_catalogue/LEDGER.csv` — one row per origin path.
- `_catalogue/ORIGIN_AND_BINDING_LEDGER.md` — human index and digest/certificate bindings.
- `_catalogue/RETIREMENT_DELETION_RECEIPT.json` — machine-readable record of safely retired originals.
- `_catalogue/RETIREMENT_DELETION_RECEIPT.md` — human-readable deletion receipt and exclusions.
- `_catalogue/build_library.py` — reproducible builder.
