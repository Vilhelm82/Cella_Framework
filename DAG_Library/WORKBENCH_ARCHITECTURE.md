# Cella Graph Workbench architecture

## Boundary

```text
SOURCE_REGISTRY.json  (frontier, encyclopedia-units, bridges, object-layer, ...)
        |
        +-- build_dag_library.py --source A --source B ...  (tagged union; stamps facets.source_id; dedups by id)
        |
canonical/theorem-dag.json
        |
        +-- dag_service / standalone DAG MCP (semantic read, query, impact, write)
        |
        +-- dag_views (selection + reproducible CPU/CUDA computation)
                  |
                  +-- derived_views/<revision>/<digest>.view.json
                                  |
                                  +-- Qt Quick native workbench
                                  +-- CUDA/Vulkan QSGRenderNode
                                  +-- future 3D/timeline/export renderers
```

Canonical JSON owns graph identity and declared relationships. Derived-view JSON
owns only reproducible selection, geometry, scalar and grouping output. A
renderer owns transient camera, hover and selection state. None may silently
write back into the layer above it.

## Source composition and filtered views

The canonical graph is a **tagged union** of registered source graphs, not a single
hand-authored file. `SOURCE_REGISTRY.json` lists each source — the DBP frontier overlay, the
Encyclopedia unit substrate, cross-source bridges, and later the object and affordance layers.
`build_dag_library.py` compiles them with `--source <id>=<path>` (repeatable), unions nodes and
edges (dedup by stable id, collisions reported in `extensions.source_composition`), and stamps
every element with `facets.source_id`. A single `--source` reproduces the previous single-graph
behaviour; `--out <path>` compiles to an alternate location without touching the live store or
`SOURCE_REGISTRY.json`.

Because provenance is per-element, a *source* is a filter, not a fork:

- **View one tree** — filter `source_ids: ["dbp-frontier-v1"]` returns just that source's
  one-way tree, in isolation. `["encyclopedia-units-v1"]` returns the other.
- **Compose several** — admit multiple `source_ids` to overlay trees in one view.
- **Cross-source relationships** live in dedicated **bridge sources**: edge-only graphs whose
  endpoints are ids from two other sources (e.g. `frontier-encyclopedia-bridge-v1`, whose edges
  link frontier anchors to Encyclopedia `U-` units). They compile in like any source and toggle
  as a unit. `cross_source: true` keeps only edges whose endpoints carry *different*
  `source_id`; `edge_relations: [...]` restricts to chosen relation types.

These three filter dimensions (`source_ids`, `edge_relations`, `cross_source`) extend the existing
node filters (type, subject, layer, reachability, status, text, external ids) in `cella_dag_query`,
and route through the same `query_nodes` choke point that `export` and `dag_views` selection use —
so they apply uniformly to queries, exports and saved views. A filter selection persisted as a
`derived_views/` record is a reproducible, revision-bound view. "The frontier tree", "the
Encyclopedia tree", and "gauge ↔ Galois relationships across both" are therefore filter presets over
one canonical graph — no separate reader, no destructive merge. Onboarding a new body of knowledge is:
register a source, add its bridge, recompile; every prior view still resolves against the new revision.

## Compute adapter contract

A compute adapter receives:

- canonical graph revision;
- selected node and edge records;
- algorithm id and versioned parameters;
- requested backend (`auto`, `cpu`, or `cuda`).

It returns a derived-view record with stable node ids, normalised positions,
resolved backend, implementation, device and content digest. The first release
provides deterministic layered CPU layout, NetworkX spring layout and a PyTorch
CUDA force layout. RAPIDS cuGraph can later implement the same contract without
changing the UI or canonical schema.

`auto` deliberately uses CPU below a configurable node threshold. GPU launch
and transfer overhead is pointless for the current 88-node corpus; explicitly
requesting `cuda` remains available for verification and future workloads.

## Renderer adapter seam

The Qt Quick workbench now uses a native Vulkan `QSGRenderNode` that consumes
flat node/edge geometry. The renderer implements these capabilities behind the
same model:

1. upload or import node-position, scalar and edge-route buffers;
2. draw, zoom, pan, pick and highlight stable node ids;
3. report supported dimensions, primitives and export targets;
4. keep camera and frame state transient;
5. refuse a view whose graph revision is stale unless the user explicitly opens
   it as historical material.

Vulkan allocates exportable device-local memory and a semaphore, passes their
Linux opaque FDs to CUDA, and draws directly from the CUDA-mapped allocation.
The APIs therefore share the render buffer without a CUDA-to-Vulkan round trip.
Current layout adapters still return positions through host memory; later
adapters may write directly into the published CUDA allocation.

## Transport rule

Standalone DAG MCP remains the LLM-friendly semantic interface for status,
schemas, queries, neighborhoods, impact, transactional submissions and derived
view requests. MCP JSON is not the frame transport. Large geometry should move
through memory-mapped arrays, shared memory, Arrow-compatible batches or direct
CUDA/graphics external memory.

## Extension sequence

1. Add cuGraph ForceAtlas2 and centrality/community adapters.
2. Add direct compute-adapter writes into the renderer's CUDA mapping, avoiding
   the remaining host materialization between layout completion and view upload.
3. Add renderer plugins for 3D, temporal succession, reachability heatmaps and
   publication exports.
4. Add live graph-revision notifications so an open view is marked stale as
   soon as a canonical submission is applied.

The implementation boundary follows the Qt Quick scene graph and NVIDIA CUDA
graphics-interoperability models:

- <https://doc.qt.io/qt-6/qtquick-visualcanvas-scenegraph.html>
- <https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/graphics-interop.html>
- <https://docs.rapids.ai/api/cugraph/stable/api_docs/cugraph/layout/>
