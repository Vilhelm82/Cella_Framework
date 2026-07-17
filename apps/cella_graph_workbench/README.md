# Cella Graph Workbench

A native Qt Quick navigator for the canonical Cella research DAG. The workbench
reads canonical nodes and edges through `cella.dag_service` and obtains geometry
through `cella.dag_views`; it never writes layout state into the canonical DAG.

## Launch

```bash
python -m pip install --user 'PySide6>=6.8'
./apps/cella_graph_workbench/run.sh
```

The launcher requests Qt's Vulkan RHI backend by default. It also builds and
loads the native CUDA/Vulkan `QSGRenderNode` plugin when necessary. Use
`--graphics-api auto` to allow Qt to select another native graphics API.

```bash
./apps/cella_graph_workbench/run.sh --check
./apps/cella_graph_workbench/run.sh --rebuild-native
timeout 6s ./apps/cella_graph_workbench/run.sh --verify-native
./apps/cella_graph_workbench/run.sh --graphics-api auto
```

`run.sh` resolves the repository location itself, so it can be invoked from any
working directory. Set `PYTHON=/path/to/python` to select a different Python
interpreter. Any additional arguments are forwarded unchanged to the launcher.

## Included workflow

- Search and filter by artifact type and lifecycle status.
- Toggle registered source layers from an edge-bounded, vertically scrollable
  source menu; long labels retain hover tooltips.
- Switch between deterministic layered and force-directed layouts.
- Select CPU, CUDA, or automatic compute backend.
- Inspect node status, summary, provenance pointers and external identifiers.
- Highlight the explicit relation-aware reevaluation closure for a node.
- Save the current layout as a content-addressed, revision-bound derived view.

The header separates Find, Layout, and Appearance controls. It uses two columns
on wide windows and stacks the primary groups below 1420 pixels; the window has
a 900-pixel supported minimum width. All Appearance popups clamp to the current
overlay rectangle, flip above their anchor when necessary, and reposition when
the window changes size.

```bash
python engine/tests/gate_graph_workbench_ui.py
python engine/tests/gate_graph_workbench_native.py
```

The primary canvas is a custom Vulkan `QSGRenderNode`. Vulkan exports its vertex
allocation and semaphore as Linux opaque FDs; CUDA imports both and writes the
same allocation before Vulkan draws it. Device UUIDs must match. A coherent
Vulkan upload buffer and Qt software renderer remain available as explicit,
reported fallbacks.

Semantic query calls remain capped at 500 records, while the internal workbench
pages across those calls. The canvas therefore consumes the full selected graph
and is prepared for the planned 1,915-unit encyclopedia corpus without weakening
the MCP query boundary.
