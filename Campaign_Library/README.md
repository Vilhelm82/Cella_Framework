# Cella Campaign Library

Non-destructive campaign library assembled from Cella and Lloyd Engine V4 campaign
trees. The library contains **39 campaigns**, **952
campaign artifacts**, and **952 source paths**.

Every campaign-only clone is byte-identical to its recorded origin. Exact overlaps with
`Papers_Library` are relative symlinks, preserving separate campaign and paper trees while
storing the bytes once. Folder names, campaign IDs, role folders, phase labels, and
filenames are normalized under `_catalogue/TERMINOLOGY.md`. Source files and source
references were not renamed or edited.

## Catalogue

- `_catalogue/CAMPAIGN_REGISTRY.md` — campaign IDs, aliases, families, and counts.
- `_catalogue/CAMPAIGN_PAPER_LINEAGE.md` — campaign-to-paper/theorem identity edges.
- `_catalogue/CAMPAIGN_PAPER_LINEAGE.json` — machine-readable lineage and symlink map.
- `_catalogue/DEDUPLICATION_SWEEP.md` — exact-identity deduplication result and exclusions.
- `_catalogue/DEDUPLICATION_SWEEP.json` — machine-readable zero-deletion receipt.
- `_catalogue/TERMINOLOGY.md` — controlled folder and filename vocabulary.
- `_catalogue/LEDGER.json` — authoritative artifact, origin, digest, and mirror ledger.
- `_catalogue/LEDGER.csv` — one row per origin path.
- `_catalogue/PATH_RENAME_MAP.csv` — original-to-normalized mapping; rewrite status remains scope-only.
- `_catalogue/REFERENCE_UPDATE_SCOPE.md` — human scope assessment for a later rewrite stage.
- `_catalogue/REFERENCE_IMPACT.json` — occurrence-level reference impact data.
- `_catalogue/build_campaign_library.py` — reproducible builder and verifier.

## Authority boundary

This is a documentary library. Cella `STATE/` remains canon. Campaign names such as
`PROVEN`, `CERTIFIED`, `FINAL`, or `CLOSE` are origin claims and are not promoted by
their placement here.
