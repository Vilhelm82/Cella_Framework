#!/usr/bin/env python3
"""Small CLI over the standalone Cella DAG service."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "engine" / "src"))

from cella.dag_service import (  # noqa: E402
    DagError,
    apply_bundle,
    dag_status,
    export_graph,
    impact_analysis,
    query_nodes,
    schema_record,
    submit_bundle,
    validate_graph,
)
from cella.dag_views import compute_view, get_view, list_views, view_capabilities  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    schema = sub.add_parser("schema"); schema.add_argument("name", nargs="?", default="registry")
    validate = sub.add_parser("validate"); validate.add_argument("--verify-files", action="store_true")
    query = sub.add_parser("query"); query.add_argument("--filters", default="{}"); query.add_argument("--limit", type=int, default=100); query.add_argument("--cursor", type=int, default=0)
    impact = sub.add_parser("impact"); impact.add_argument("node_ids", nargs="+"); impact.add_argument("--max-depth", type=int, default=8)
    submit = sub.add_parser("submit"); submit.add_argument("path", type=Path); submit.add_argument("--stage", action="store_true")
    apply = sub.add_parser("apply"); apply.add_argument("submission_id"); apply.add_argument("--confirm", action="store_true")
    export = sub.add_parser("export"); export.add_argument("format"); export.add_argument("--filters", default="{}"); export.add_argument("--write", action="store_true"); export.add_argument("--include-data", action="store_true")
    views = sub.add_parser("views"); views.add_argument("--current-only", action="store_true")
    view_get = sub.add_parser("view-get"); view_get.add_argument("identifier")
    view_compute = sub.add_parser("view-compute"); view_compute.add_argument("algorithm", choices=("layered", "spring")); view_compute.add_argument("--backend", choices=("auto", "cpu", "cuda"), default="auto"); view_compute.add_argument("--filters", default="{}"); view_compute.add_argument("--parameters", default="{}"); view_compute.add_argument("--write", action="store_true")
    sub.add_parser("view-capabilities")
    args = parser.parse_args()
    try:
        if args.command == "status": result = dag_status()
        elif args.command == "schema": result = schema_record(args.name)
        elif args.command == "validate": result = validate_graph(verify_files=args.verify_files)
        elif args.command == "query": result = query_nodes(json.loads(args.filters), limit=args.limit, cursor=args.cursor)
        elif args.command == "impact": result = impact_analysis(args.node_ids, max_depth=args.max_depth)
        elif args.command == "submit": result = submit_bundle(json.loads(args.path.read_text()), dry_run=not args.stage)
        elif args.command == "apply": result = apply_bundle(args.submission_id, confirm=args.confirm)
        elif args.command == "export": result = export_graph(args.format, json.loads(args.filters), write=args.write, include_data=args.include_data)
        elif args.command == "views": result = list_views(include_stale=not args.current_only)
        elif args.command == "view-get": result = get_view(args.identifier)
        elif args.command == "view-compute": result = compute_view(args.algorithm, args.backend, json.loads(args.filters), json.loads(args.parameters), write=args.write)
        else: result = view_capabilities()
    except DagError as exc:
        result = exc.record()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
