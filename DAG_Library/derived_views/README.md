# Derived views

This directory holds content-addressed, renderer-neutral graph geometry. Each
view is bound to one canonical graph revision and records its selection,
algorithm, backend, parameters, node positions and provenance.

Views are non-authoritative and disposable. A view becomes stale when its
`graph_revision` differs from the canonical DAG revision; it must never be used
to overwrite canonical nodes or edges.

Generated records are stored under the first sixteen hexadecimal characters of
their graph revision:

```text
derived_views/<graph-revision-prefix>/<view-sha256>.view.json
```

MCP and the desktop workbench use JSON for semantic operations. Future
high-volume render buffers belong on shared memory or CUDA/graphics
interoperability rather than being pushed through MCP JSON.
