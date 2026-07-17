"""Standalone MCP server for the Cella research DAG.

This server is intentionally independent of ``cella.mcp_server`` while that
surface is under reconstruction.
"""
from __future__ import annotations

import argparse

from mcp.server.transport_security import TransportSecuritySettings

from .campaign_start import commit_campaign, scaffold_campaign
from .dag_service import (
    DagError,
    apply_bundle,
    dag_status,
    export_graph,
    fetch_source,
    get_node,
    impact_analysis,
    query_nodes,
    schema_record,
    submit_bundle,
    validate_artifact,
    validate_graph,
)
from .dag_views import compute_view, get_view, list_views, view_capabilities


DAG_TOOL_NAMES = (
    "cella_dag_status",
    "cella_dag_schema",
    "cella_dag_get",
    "cella_dag_source",
    "cella_dag_query",
    "cella_dag_validate",
    "cella_dag_impact",
    "cella_dag_submit",
    "cella_dag_apply",
    "cella_dag_export",
    "cella_dag_view_capabilities",
    "cella_dag_view_compute",
    "cella_dag_view_list",
    "cella_dag_view_get",
    "cella_campaign_scaffold",
    "cella_campaign_commit",
)


def _safe(callable_, *args, **kwargs):
    try:
        return callable_(*args, **kwargs)
    except DagError as exc:
        return exc.record()
    except Exception as exc:  # transport boundary: return structured failure
        return {
            "schema": "cella-dag-service-v1",
            "ok": False,
            "error": {"token": "UNEXPECTED_DAG_ERROR", "message": str(exc), "exception_type": type(exc).__name__},
        }


def call_dag_status() -> dict:
    """Orientation call -- run this FIRST in a session. Reports the graph id, the content revision
    (a sha256 you must pass as base_revision when mutating), node and edge counts, the histogram of
    node types and layers, whether the graph currently validates, and the on-disk paths. Use it to
    learn how big the graph is and which layers/types exist before you query anything. Read-only."""
    return _safe(dag_status)


def call_dag_schema(name: str = "registry") -> dict:
    """Read one registered schema so you build valid documents. name is one of: 'registry' (the
    allowed node types, claim_statuses, lifecycle_statuses and reachability values), 'relation' (the
    allowed edge relations), 'artifact', 'dag', 'derived_view', or 'submission' (the exact shape a
    mutation must take). Call schema('registry') and schema('submission') before ever building a
    cella_dag_submit, so you use only allowed values. Read-only."""
    return _safe(schema_record, name)


def call_dag_get(node_id: str, direction: str = "both", depth: int = 1) -> dict:
    """Read ONE node by its exact id, plus everything directly connected to it: the node's full
    record and every incident edge (what supersedes / supplements / depends_on / opens_gap /
    same_content_as / proves it) together with the neighbor nodes on the other end. Use this after a
    query to answer 'what does this specific unit connect to'. direction is 'in', 'out', or 'both';
    depth is the neighborhood hop count (keep it 1-2). Read-only."""
    return _safe(get_node, node_id, direction=direction, depth=depth)


def call_dag_source(pointer: str | None = None, node_id: str | None = None, max_bytes: int = 1_000_000, include_connections: bool = False) -> dict:
    """Open the actual source FILE behind a node or pointer, to read the full proof / derivation /
    paper text that a node only summarises. Pass EITHER node_id (uses that node's first source_ref)
    OR an explicit pointer like 'cella:Papers_Library/.../file.tex'. Returns the file's full text plus
    its live sha256 and whether it matches the node's recorded digest. Binary files (pdf/zip/png) are
    declined with a note; long text is capped at max_bytes (the 'truncated' flag is set if hit).
    Set include_connections=true to ALSO get, in the SAME call, every node backed by that same file,
    all edges touching that set, and the ids of the units the file contains -- i.e. 'this file plus
    everything connected to it'. Read-only. Typical use: cella_dag_query to find a node, then this."""
    return _safe(fetch_source, pointer=pointer, node_id=node_id, max_bytes=max_bytes, include_connections=include_connections)


def call_dag_query(filters: dict | None = None, edge_mode: str = "induced", limit: int = 100, cursor: int = 0) -> dict:
    """The main discovery/search tool -- find nodes by criteria and get the edges among them.
    filters is an object; any of: ids, types (theorem/definition/formula/paper/proof/gap/report/...),
    claim_statuses (proved/machine-verified/conjectured/refuted/open/...), lifecycle_statuses,
    layers (frontier/substrate/succession), reachability (EASY/MODERATE/WALL/INVARIANT), tracked
    (bool), text (case-insensitive substring over label+summary+facets), external_ids, and the
    source-composition filters: source_ids (view one registered source's tree in isolation, or
    several), edge_relations (keep only these relation types), cross_source (true = only edges whose
    endpoints come from DIFFERENT sources, e.g. the frontier<->encyclopedia bridges). Paginated:
    limit (<=500) and cursor; edge_mode is 'induced' (edges within the page), 'incident' (any edge
    touching the page) or 'none'. Read-only. Typical R&D use: query for a topic or a reusable move,
    then cella_dag_get or cella_dag_source on the hits."""
    return _safe(query_nodes, filters, edge_mode=edge_mode, limit=limit, cursor=cursor)


def call_dag_validate(document_type: str = "graph", document: dict | None = None, verify_files: bool = False) -> dict:
    """Check that a graph or artifact record is well-formed BEFORE you try to submit it. Pass
    document_type 'graph' or 'artifact' and the document to check (omit document to validate the live
    canonical graph). verify_files=true additionally confirms each cella: source file exists and its
    sha matches. Returns ok plus a list of errors (blocking) and warnings (advisory). Read-only."""
    kind = str(document_type).strip().lower()
    if kind == "graph":
        return _safe(validate_graph, document, verify_files=verify_files)
    if kind == "artifact":
        if document is None:
            return {"schema": "cella-dag-service-v1", "ok": False, "error": {"token": "DOCUMENT_REQUIRED", "message": "artifact validation requires document"}}
        return _safe(validate_artifact, document, verify_files=verify_files)
    return {"schema": "cella-dag-service-v1", "ok": False, "error": {"token": "UNKNOWN_DOCUMENT_TYPE", "message": "document_type must be graph or artifact"}}


def call_dag_impact(changed_node_ids: list[str] | None = None, changed_source_sha256s: list[str] | None = None, max_depth: int = 8) -> dict:
    """Preview the blast radius of a change before you make it. Give changed_node_ids (or
    changed_source_sha256s) and it returns every node that would need re-evaluation because it
    depends_on / is proved by / is evidenced by what you changed, out to max_depth hops. Use it
    between building a submission and applying it, so you know exactly what a mutation touches.
    Read-only."""
    return _safe(impact_analysis, changed_node_ids, changed_source_sha256s, max_depth=max_depth)


def call_dag_submit(submission: dict, dry_run: bool = True) -> dict:
    """Step 1 of a mutation (creating/updating/retiring nodes or edges). Build a submission per
    schema('submission'): it needs base_revision (the current revision from cella_dag_status -- a
    stale one is rejected, never silently rebased), an idempotency_key, a summary, matching artifact
    sidecars, and a graph_delta with upsert_nodes / upsert_edges / retire_nodes / remove_edges.
    dry_run defaults to TRUE: that validates and previews impact WITHOUT changing anything -- always
    do this first and read the errors/impact. Call again with dry_run=false to STAGE an accepted
    submission (still not applied). Then call cella_dag_apply. Nodes are retired/superseded, never
    deleted; remove an edge only by its exact id."""
    return _safe(submit_bundle, submission, dry_run=dry_run)


def call_dag_apply(submission_id: str, confirm: bool = False) -> dict:
    """Step 2 of a mutation -- actually write a previously staged submission into the canonical graph.
    Requires the submission_id from a successful dry_run=false submit AND confirm=true (without
    confirm it is a deliberate no-op safeguard). It re-checks base_revision under a lock, applies the
    delta, records before/after revisions, and writes an audit receipt. This is the ONLY call that
    mutates the canonical graph."""
    return _safe(apply_bundle, submission_id, confirm=confirm)


def call_dag_export(format: str = "node_edge_json", filters: dict | None = None, write: bool = False, include_data: bool = False) -> dict:
    """Write the graph out in a renderer/tool-friendly format for use OUTSIDE this MCP: 'canonical_json',
    'node_edge_json', 'dot' (Graphviz), 'graphml', or 'cytoscape_json'. Pass filters (same shape as
    cella_dag_query) to export only a slice. write=true saves a file and returns its path+digest;
    include_data=true returns the serialized payload inline. Use for visualization pipelines and
    external graph tools -- not for reading content (use query/get/source for that)."""
    return _safe(export_graph, format, filters, write=write, include_data=include_data)


def call_dag_view_capabilities() -> dict:
    """Report which layout algorithms exist (layered, spring) and whether the CPU and CUDA backends
    are available right now, plus the renderer boundary. Call before cella_dag_view_compute to pick a
    backend. Read-only."""
    return _safe(view_capabilities)


def call_dag_view_compute(algorithm: str = "layered", backend: str = "auto", filters: dict | None = None, parameters: dict | None = None, write: bool = False) -> dict:
    """Compute node POSITIONS (a graph layout) for rendering -- this is geometry, not content.
    algorithm is 'layered' or 'spring'; backend is 'auto'/'cpu'/'cuda'. Pass filters to lay out a
    slice (recommended -- the full graph is large). write=true stores the view keyed by content
    digest and graph revision. The heavy visualization itself happens in the native workbench, not
    here; use this only when you need coordinates."""
    return _safe(compute_view, algorithm, backend, filters, parameters, write=write)


def call_dag_view_list(include_stale: bool = True) -> dict:
    """List stored derived-view layouts. include_stale=true also shows views bound to an older graph
    revision (each flagged stale). Read-only."""
    return _safe(list_views, include_stale=include_stale)


def call_dag_view_get(identifier: str) -> dict:
    """Read one stored derived-view layout by its view id, content digest, or exact filename.
    Read-only."""
    return _safe(get_view, identifier)


def call_campaign_scaffold(title: str, subject_family: str, summary: str,
                           relations: list[dict] | None = None,
                           promote_tracked: list[str] | None = None,
                           existing_sidecar: str | None = None) -> dict:
    """Prepare a complete campaign-opening bundle without mutating the Campaign Library or DAG.
    Resolves the next CMP and CMA identifiers, the explicit subject-family folder mapping, the
    DBP:campaign:<acronym> node id, live base revision, canonical paths, sidecar, relations, and the
    mandatory node.external_ids.artifacts binding. relations entries use relation, target_id, basis,
    and optional from_id; promote_tracked lists existing node ids to move to the tracked frontier.
    Writes only to Campaign_Library/_staging and is safe to repeat."""
    return _safe(
        scaffold_campaign,
        title=title,
        subject_family=subject_family,
        summary=summary,
        relations=relations,
        promote_tracked=promote_tracked,
        existing_sidecar=existing_sidecar,
    )


def call_campaign_commit(staging_dir: str, confirm: bool = False) -> dict:
    """Gate and commit one cella_campaign_scaffold bundle. Re-fetches the live revision, validates
    the sidecar with file verification, previews the graph delta and impact, and refuses all writes
    unless confirm=true. A confirmed call writes the campaign sidecar, stages and applies the DAG
    submission transactionally, validates the complete graph, and emits a receipt. Before applying,
    it registers a persistent campaign source, rebuilds the DAG, canonicalizes both results, and
    requires an empty git diff; any failure rolls every write back. This is the only campaign-opening write."""
    return _safe(commit_campaign, staging_dir, confirm=confirm)


def tool_callable_map() -> dict:
    return {
        "cella_dag_status": call_dag_status,
        "cella_dag_schema": call_dag_schema,
        "cella_dag_get": call_dag_get,
        "cella_dag_source": call_dag_source,
        "cella_dag_query": call_dag_query,
        "cella_dag_validate": call_dag_validate,
        "cella_dag_impact": call_dag_impact,
        "cella_dag_submit": call_dag_submit,
        "cella_dag_apply": call_dag_apply,
        "cella_dag_export": call_dag_export,
        "cella_dag_view_capabilities": call_dag_view_capabilities,
        "cella_dag_view_compute": call_dag_view_compute,
        "cella_dag_view_list": call_dag_view_list,
        "cella_dag_view_get": call_dag_view_get,
        "cella_campaign_scaffold": call_campaign_scaffold,
        "cella_campaign_commit": call_campaign_commit,
    }


def build_dag_mcp_server(*, host: str = "127.0.0.1", port: int = 8000,
                         allowed_hosts: list[str] | None = None,
                         allowed_origins: list[str] | None = None):
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("the Python 'mcp' package is required to run the DAG MCP server") from exc

    transport_security = TransportSecuritySettings(
        allowed_hosts=["127.0.0.1:*", "localhost:*", "[::1]:*"] + list(allowed_hosts or []),
        allowed_origins=["http://127.0.0.1:*", "http://localhost:*", "http://[::1]:*"] + list(allowed_origins or []),
    )
    mcp = FastMCP(
        "cella-dag",
        instructions=(
            "Renderer-neutral research DAG of mathematical units (theorems, definitions, formulas, "
            "proofs, papers, gaps) and their relations. It is an INDEX of declared claims and "
            "provenance; it does not make mathematics true.\n"
            "READING (start here, all read-only): 1) cella_dag_status to orient (size, layers, the "
            "current revision). 2) cella_dag_query to FIND nodes by type/subject/status/reachability/"
            "text, or by source_ids/cross_source to view one source or the links between sources. "
            "3) cella_dag_get to see ONE node and everything it connects to. 4) cella_dag_source to "
            "open a node's full underlying FILE (proof/derivation text); add include_connections=true "
            "to get the file plus every node and edge attached to it in one call.\n"
            "WRITING (only if asked to change the graph): cella_dag_validate -> cella_dag_impact "
            "(preview blast radius) -> cella_dag_submit (dry_run=true to preview, then dry_run=false "
            "to stage) -> cella_dag_apply (confirm=true). base_revision must match the live revision "
            "or the write is rejected. Nodes are retired/superseded, never deleted.\n"
            "TWO STATUS FIELDS, never conflate them: claim_status is mathematical truth "
            "(proved/refuted/open/...); lifecycle_status is document state (released/superseded/...). "
            "Layouts (cella_dag_view_*) are geometry for rendering, not content."
            " CAMPAIGNS: cella_campaign_scaffold resolves every mechanical identifier and binding; "
            "cella_campaign_commit revalidates and requires confirm=true before the single write."
        ),
        host=host,
        port=port,
        transport_security=transport_security,
    )

    for name, callable_ in tool_callable_map().items():
        mcp.tool(name=name)(callable_)

    return mcp


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run the standalone Cella DAG MCP server.")
    parser.add_argument("--transport", choices=("stdio", "sse", "streamable-http"), default="stdio")
    parser.add_argument("--host", default="127.0.0.1", help="bind address for HTTP transports")
    parser.add_argument("--port", type=int, default=8000, help="bind port for HTTP transports")
    parser.add_argument("--allowed-host", action="append", default=[], help="additional Host header pattern, repeatable")
    parser.add_argument("--allowed-origin", action="append", default=[], help="additional Origin pattern, repeatable")
    parser.add_argument("--list-tools", action="store_true")
    args = parser.parse_args(argv)
    if args.list_tools:
        print("\n".join(DAG_TOOL_NAMES)); return 0
    build_dag_mcp_server(
        host=args.host,
        port=args.port,
        allowed_hosts=args.allowed_host,
        allowed_origins=args.allowed_origin,
    ).run(args.transport)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
