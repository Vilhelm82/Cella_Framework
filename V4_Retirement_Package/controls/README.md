# Lloyd Engine V4 — retirement staging repository

This repository has been reorganized for evidence review and eventual ingestion by
`/home/wlloyd/Cella Framework`. It is no longer arranged as an active V4 development
workspace.

Start with [`STATE/CURRENT.md`](STATE/CURRENT.md), then use
[`STATE/MIGRATION.json`](STATE/MIGRATION.json) to resolve old paths and
[`STATE/ARTIFACTS.json`](STATE/ARTIFACTS.json) to search the current inventory.

## Repository regions

| Region | Contents | Authority during Cella ingestion |
|---|---|---|
| `STATE/` | Retirement status, migration ledger, and generated artifact registry | Staging metadata only; not Cella canon |
| `engine/` | Legacy V4 source, tests, package metadata, and demos | Historical implementation; functionality is not maintained by this reorganization |
| `research/` | Campaigns, verification scripts, reports, papers, and derivations | Candidate evidence requiring evaluation and fresh Cella-side verification |
| `docs/` | Architecture, governance, reference material, and agent-training context | Non-normative context |
| `archive/` | Prior canon, audits, superseded documents, packages, and attic material | Historical sediment; never automatically authoritative |

Old documents and scripts were intentionally not rewritten to repair internal path
references. Their original wording is provenance. Resolve moved roots through the
migration ledger instead of treating a stale path as a missing artifact.

No legacy claim, status label, test result, or implementation is promoted into Cella
by its placement here. Promotion belongs to Cella's admissions and re-verification
process.
