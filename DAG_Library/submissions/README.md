# DAG submissions

`pending/` contains validated, unapplied mutation bundles. `applied/` preserves
the exact bundles that changed the canonical graph; `receipts/` at the DAG root
binds each bundle digest to its before/after revisions.

LLM clients should always:

1. call status and retain the current revision;
2. read the submission and artifact schemas;
3. validate new sidecars;
4. request an impact preview;
5. submit with `dry_run=true` first;
6. stage only after reviewing warnings;
7. apply only with the maintainer's explicit confirmation.

There is no raw filesystem-write or arbitrary-delete MCP tool. Mutations are
schema-bounded graph deltas, and node removal is represented as retirement or
supersession so provenance survives.
