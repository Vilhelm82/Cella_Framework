#!/usr/bin/env python3
"""Scaffold and explicitly commit a Cella campaign opening."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "engine" / "src"))

from cella.campaign_start import commit_campaign, scaffold_campaign  # noqa: E402
from cella.dag_service import DagError  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(prog="start_campaign")
    commands = parser.add_subparsers(dest="command", required=True)
    scaffold = commands.add_parser("scaffold", help="reserve identifiers and write a non-canonical staging bundle")
    scaffold.add_argument("--title", default="")
    scaffold.add_argument("--subject-family", required=True)
    scaffold.add_argument("--summary", default="")
    scaffold.add_argument("--relation", nargs=3, action="append", metavar=("RELATION", "TARGET", "BASIS"), default=[])
    scaffold.add_argument("--edge", nargs=4, action="append", metavar=("FROM", "RELATION", "TARGET", "BASIS"), default=[])
    scaffold.add_argument("--promote-tracked", action="append", default=[])
    scaffold.add_argument("--from-existing", type=Path)
    commit = commands.add_parser("commit", help="run all gates and explicitly apply one scaffold")
    commit.add_argument("staging_dir", type=Path)
    commit.add_argument("--confirm", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "scaffold":
            relations = [
                {"relation": relation, "target_id": target, "basis": basis}
                for relation, target, basis in args.relation
            ] + [
                {"from_id": source, "relation": relation, "target_id": target, "basis": basis}
                for source, relation, target, basis in args.edge
            ]
            result = scaffold_campaign(
                title=args.title,
                subject_family=args.subject_family,
                summary=args.summary,
                relations=relations,
                promote_tracked=args.promote_tracked,
                existing_sidecar=str(args.from_existing) if args.from_existing else None,
            )
        else:
            result = commit_campaign(str(args.staging_dir), confirm=args.confirm)
    except DagError as exc:
        result = exc.record()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
