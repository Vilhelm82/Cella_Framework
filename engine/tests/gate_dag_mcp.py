"""Smoke gate for standalone DAG FastMCP registration and wrappers."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.dag_mcp_server import (
    DAG_TOOL_NAMES,
    build_dag_mcp_server,
    call_dag_apply,
    call_dag_query,
    call_dag_schema,
    call_dag_status,
)
from cella.dag_service import load_graph

FAILS = []


def check(name, condition):
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")
    if not condition:
        FAILS.append(name)


server = build_dag_mcp_server()
registered = set(getattr(server._tool_manager, "_tools", {}))
check("FastMCP registers exactly the standalone DAG tool surface", registered == set(DAG_TOOL_NAMES))

status = call_dag_status()
check("MCP status wrapper reads a valid canonical graph", status["ok"] and status["counts"]["nodes"] == len(load_graph()["nodes"]))

schema = call_dag_schema("submission")
check("MCP schema wrapper exposes the submission contract", schema["ok"] and schema["document"]["title"] == "Cella DAG mutation submission")

query = call_dag_query({"layers": ["frontier"], "tracked": True}, limit=10)
check("MCP query wrapper is bounded and filterable", query["ok"] and query["counts"]["returned_nodes"] <= 10 and all(node["layer"] == "frontier" and node["tracked"] for node in query["nodes"]))

refusal = call_dag_apply("not-staged", confirm=False)
check("MCP apply refuses mutation without explicit confirmation", not refusal["ok"] and refusal["error"]["token"] == "CONFIRMATION_REQUIRED")

if FAILS:
    print(f"DAG MCP GATE: OPEN — {len(FAILS)} failure(s): {FAILS}")
    raise SystemExit(1)
print("DAG MCP GATE: CLOSED")
