# Standalone DAG MCP tools

Server module: `cella.dag_mcp_server`  
Response schema: `cella-dag-service-v1`

| Tool | Mode | Purpose |
|---|---|---|
| `cella_dag_status` | read | Current graph id, revision, counts and validation state. |
| `cella_dag_schema` | read | Retrieve registry, relation, artifact, DAG or submission schema. |
| `cella_dag_get` | read | One node plus a bounded incoming/outgoing neighborhood. |
| `cella_dag_source` | read | Return the full text of the source file behind a pointer or a node's `source_ref` (sha-verified; binary payloads declined; path-traversal guarded). `include_connections=true` also returns every node backed by the same file, their incident edges, and the units it contains. |
| `cella_dag_query` | read | Paginated filters over ids, types, statuses, layers, reachability, text, external ids, and `source_ids` / `edge_relations` / `cross_source`. |
| `cella_dag_validate` | read | Validate the canonical graph or a supplied graph/artifact record. |
| `cella_dag_impact` | read | Relation-aware reevaluation closure for changed nodes or source digests. |
| `cella_dag_submit` | staged write | Preview by default; optionally stage a revision-bound mutation bundle. |
| `cella_dag_apply` | confirmed write | Apply a staged bundle only with `confirm=true`; emit an audit receipt. |
| `cella_dag_export` | derived write/read | Produce canonical JSON, node/edge JSON, DOT, GraphML or Cytoscape JSON. |
| `cella_dag_view_capabilities` | read | Report layout algorithms and live CPU/CUDA availability. |
| `cella_dag_view_compute` | derived write/read | Compute a revision-bound layout and optionally persist it by content digest. |
| `cella_dag_view_list` | read | List stored views and flag stale graph revisions. |
| `cella_dag_view_get` | read | Retrieve a stored view by stable id or digest. |
| `cella_campaign_scaffold` | staged write | Resolve campaign/artifact ids, family mapping, canonical paths, explicit artifact binding, live revision and graph delta; write only a repeatable staging bundle. |
| `cella_campaign_commit` | confirmed write | Revalidate, preview, rebuild registered sources, require an empty canonical git diff, then apply only with `confirm=true`; roll back every touched file on failure. |

## Mutation semantics

- Create and update nodes/edges with `graph_delta.upsert_nodes` and
  `graph_delta.upsert_edges`.
- Remove an edge only by its exact stable id.
- Retire nodes with `graph_delta.retire_nodes`; there is intentionally no
  destructive node-delete operation.
- Every submission names the graph revision it was built against. A stale
  revision is rejected rather than silently rebased.
- `cella_dag_submit` defaults to `dry_run=true`. Staging is not application.
- Application revalidates under a cross-process write lock and records both
  before/after revisions.
- New DAG nodes must bind a submitted sidecar through
  `node.external_ids.artifacts`; matching a node id to an artifact id is not a
  binding.

## Campaign mutation semantics

- `cella_campaign_scaffold` is repeatable and writes only to
  `Campaign_Library/_staging/`. Relations use `relation`, `target_id`, `basis`,
  and optional `from_id`; `promote_tracked` names existing frontier nodes.
- `cella_campaign_commit(..., confirm=false)` is an impact preview and always
  refuses application.
- A confirmed commit materializes the intended graph and independently rebuilds
  the registered-source graph. Both pass through the deterministic semantic
  canonicalizer and `git diff --no-index --exit-code` must return zero.
- The sidecar, source overlay, source registry, canonical graph, pending/applied
  submissions, and receipt are snapshotted and restored on any failure.
- Replaying an already admitted staging bundle still reruns the rebuild proof,
  then returns `idempotent_replay=true` without duplicating graph records.

## LLM usage sequence

1. `cella_dag_status`
2. `cella_dag_schema(name="submission")`
3. `cella_dag_query(...)` or `cella_dag_get(...)`
4. `cella_dag_impact(...)`
5. `cella_dag_submit(submission, dry_run=true)`
6. Review `changes`, `impact`, errors and warnings.
7. `cella_dag_submit(submission, dry_run=false)`
8. Only after explicit maintainer approval:
   `cella_dag_apply(submission_id, confirm=true)`

Large graph reads are paginated and capped at 500 nodes per call. Exports return
digests and paths by default; `include_data=true` is available for clients that
actually need the serialized payload.
