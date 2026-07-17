# Artifact Schemas

This registry is the admission contract for new research material and the
renderer-neutral theorem DAG. Native files remain Markdown, TeX, PDF, code, or
data; every admitted file set receives one JSON sidecar conforming to
`schemas/artifact.schema.json`.

## Design laws

1. JSON is canonical. Renderers and MCP clients are adapters, never authorities.
2. Stable ids and explicit directed relations carry meaning; filenames do not.
3. Mathematical `claim_status` and documentary `lifecycle_status` are separate.
4. Digests bind content independently of paths. Moves with the same digest do not
   trigger mathematical reevaluation.
5. Unknown future metadata belongs under `extensions`; visualization preferences
   belong under `visual_hints` and never alter graph semantics.
6. Mutations enter as submission bundles with optimistic `base_revision`, an
   idempotency key, validation, impact preview, and an audit receipt.
7. LLM-facing summaries and retrieval hints are explicit fields, not inferred
   from filenames. DAG nodes carry a compact `retrieval` projection; artifact
   sidecars carry the fuller `llm` record.
8. Computed layouts conform to `schemas/derived-view.schema.json`, bind the
   canonical graph revision, and remain disposable non-authoritative records.
9. Every new DAG node binds its submitted artifact sidecar explicitly through
   `external_ids.artifacts`; identifier resemblance is never accepted as
   provenance.
10. Campaign admission must survive a full registered-source rebuild with an
    empty deterministic semantic diff before the canonical DAG may change.

## Required workflow

1. Copy the closest file from `templates/` beside the new artifact as
   `<stem>.artifact.json`.
2. Fill every `REPLACE_...` value, calculate file SHA-256 digests, and declare
   dependencies, evidence, supersessions, conflicts, and expected consequences.
3. Validate the sidecar or submission through the DAG CLI/MCP service.
4. Preview reverse-dependency impact.
5. Submit, then explicitly apply the accepted bundle.

The schemas are deliberately presentation-agnostic. The same canonical DAG may
later export to JSON node/edge lists, Graphviz DOT, GraphML, Cytoscape JSON, or
other visualization formats without changing research records.
