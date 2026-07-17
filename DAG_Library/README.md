# DAG Library

The canonical, renderer-neutral research graph lives at
`canonical/theorem-dag.json`. It is compiled from registered source graphs and
artifact sidecars; it is not hand-edited.

## Authority boundary

This graph indexes declared relationships and provenance. A node saying
`claim_status: proved` remains a documentary claim unless Cella's authoritative
STATE and certificate chain admit it. The DAG does not upgrade evidence.

## Interfaces

```bash
PYTHONPATH=engine/src python3 -m cella.dag_mcp_server --list-tools
PYTHONPATH=engine/src python3 -m cella.dag_mcp_server --transport stdio
python3 engine/tools/dag_cli.py status
python3 engine/tools/dag_cli.py validate --verify-files
python3 engine/tools/dag_cli.py export dot --write
python3 engine/tools/dag_cli.py view-capabilities
python3 engine/tools/dag_cli.py view-compute layered --write
python3 engine/tools/start_campaign.py scaffold --help
```

For a Cloudflare Tunnel, keep the server bound locally and allow the tunnel's
public hostname explicitly:

```bash
PYTHONPATH=engine/src python3 -m cella.dag_mcp_server \
  --transport streamable-http \
  --allowed-host cella-mcp.example.com \
  --allowed-origin https://cella-mcp.example.com
```

The default HTTP endpoint is `http://127.0.0.1:8000/mcp`. The allowlist is
required because FastMCP rejects unrecognised `Host` headers with HTTP 421.

MCP mutations are deliberately transactional:

1. `cella_dag_submit(..., dry_run=true)` previews validation and impact.
2. `cella_dag_submit(..., dry_run=false)` stages an accepted submission.
3. `cella_dag_apply(submission_id, confirm=true)` applies it only if the base
   revision still matches, emits a receipt, and attempts a local Git commit
   containing only the artifact-declared source files, canonical graph, applied
   submission and receipt.

Apply never pushes and never absorbs unrelated worktree changes. A Git failure
does not roll back the valid DAG transaction: the result reports
`git_commit.status = git_publication_pending` with the intended paths and error,
so publication cannot disappear behind a successful mathematical receipt.

Nodes are retired or superseded, never destructively deleted. Edge removal must
name an exact stable edge id.

## Campaign openings

Campaigns use a stricter two-command path:

1. `start_campaign.py scaffold` resolves the next `CMP-NNNN` and `CMA-NNNNNN`,
   family folder, `DBP:campaign:<acronym>` node, explicit artifact binding, live
   base revision, sidecar, and graph delta. It writes only under
   `Campaign_Library/_staging/`.
2. `start_campaign.py commit <staging-dir>` revalidates and previews, then
   refuses the write without `--confirm`.
3. A confirmed commit writes a registered source overlay, rebuilds the complete
   DAG from `SOURCE_REGISTRY.json`, passes both intended and rebuilt graphs
   through the deterministic canonicalizer, and requires an empty
   `git diff --no-index` before application.
4. Any rebuild difference, submission failure, or post-apply validation failure
   rolls back the sidecar, overlay, registry, canonical graph, bundle, and
   receipt.

The MCP equivalents are `cella_campaign_scaffold` and
`cella_campaign_commit`. The acceptance gate is:

```bash
python3 engine/tests/gate_campaign_start.py
```

The rebuild-and-diff check is intentionally a semantic survival proof: source
ordering, generation timestamps, and revision metadata cannot create noise,
while any changed node or edge remains a hard failure.

## Visualization independence

The export adapter currently emits canonical JSON, plain node/edge JSON,
Graphviz DOT, GraphML and Cytoscape JSON. Those files are disposable derived
views; adding a future renderer does not alter the graph schema.

Layout geometry is likewise stored separately under `derived_views/`. Each
record binds its canonical graph revision, filter selection, algorithm,
parameters, resolved CPU/CUDA backend and content digest. Stale views remain
auditable but are never silently treated as current.

## Native workbench

The Qt Quick desktop navigator lives under `apps/cella_graph_workbench/`:

```bash
python -m pip install -e 'engine[workbench]'
python apps/cella_graph_workbench/main.py --check
python apps/cella_graph_workbench/main.py
```

It provides search/status filters, layered and spring layouts, explicit
CPU/CUDA selection, provenance inspection, impact-closure highlighting and
content-addressed view saving. See `WORKBENCH_ARCHITECTURE.md` for the
CUDA/Vulkan renderer seam and transport rules.
