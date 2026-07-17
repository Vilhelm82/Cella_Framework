# Prospective reference-update scope

No source references were rewritten in this stage.

- Detected reference records: **1619**
- Source files potentially affected: **405**
- Scope counts: `cross_campaign`=61, `outside_campaign_tree`=968, `same_campaign`=590
- Resolution counts: `campaign_relative`=371, `repository_relative`=757, `unique_basename`=491
- Source repositories: `Cella Framework`=138, `Lloyd_Engine_V4`=267
- Risk flags by unique source file: `archive_or_historical_reference`=67, `cella_canon_or_governance_adjacent`=11, `digest_or_manifest_bound`=33, `executable_source`=93, `machine_readable_contract_or_record`=38, `ordinary_prose`=188

## Interpretation

A later rewrite stage must decide whether references should target normalized library paths,
whether source campaign trees will themselves be renamed, and how executable imports and
digest-bound manifests will be regenerated. This report scopes that work; it authorizes none of it.

## Recommended execution split

1. Rewrite same-campaign ordinary prose and validate local links.
2. Review cross-campaign references campaign-by-campaign against the lineage ledger.
3. Handle executable and machine-readable references with import/schema checks.
4. Regenerate and re-verify every digest-, pin-, certificate-, or manifest-bound artifact.
5. Review Cella canon/governance-adjacent references manually; never bulk-promote campaign status.

The complete occurrence-level record is `REFERENCE_IMPACT.json` and the one-row-per-origin
mapping is `PATH_RENAME_MAP.csv`.
