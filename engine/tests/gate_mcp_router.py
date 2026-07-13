"""Gate MCP router.

The router is the Claude-facing Cella MCP surface: a tiny stable tool set that
lets chat sessions switch Cella profiles without loading every Cella tool schema.

Run:  python tests/gate_mcp_router.py
"""

import sys
import json
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

FAILS = []


def check(name, ok):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


try:
    from cella.mcp_server import (
        ROUTER_TOOL_NAMES,
        CellaRouter,
        build_router_mcp_server,
    )
except Exception as exc:  # expected RED before implementation
    print(f"GATE MCP ROUTER: OPEN — import failed: {exc}")
    sys.exit(1)


router = CellaRouter(default_profile="core")

profiles = router.profiles()
check("Q1 router exposes five tiny public tools",
      ROUTER_TOOL_NAMES == (
          "cella_profiles",
          "cella_use_profile",
          "cella_tools",
          "cella_json_export",
          "cella_call",
      )
      and profiles["schema"] == "cella-router-v1"
      and profiles["active_profile"] == "core"
      and profiles["router_tools"] == list(ROUTER_TOOL_NAMES))

core_tools = router.tools()
check("Q2 router lists active profile summaries without dumping all tool help",
      core_tools["ok"]
      and core_tools["profile"] == "core"
      and core_tools["tool_count"] == "8"
      and [t["name"] for t in core_tools["tools"]][:2] == ["cella_help", "cella_surface_jet"]
      and all(set(t) <= {"name", "purpose", "inputs", "proper_use"} for t in core_tools["tools"]))

switch = router.use_profile("symbolic")
check("Q3 profile switch is an in-chat state change",
      switch["ok"]
      and switch["previous_profile"] == "core"
      and switch["active_profile"] == "symbolic"
      and switch["tool_count"] == "7")

symbolic_call = router.call(
    "symbolic_equal",
    {"left": "x+x", "right": "2*x", "variables": ["x"]},
)
check("Q4 router dispatches short tool aliases through the active profile",
      symbolic_call["ok"]
      and symbolic_call["active_profile"] == "symbolic"
      and symbolic_call["tool"] == "cella_symbolic_equal"
      and symbolic_call["result"]["ok"]
      and symbolic_call["result"]["value"]["equal"] is True)

blocked = router.call(
    "role_jet_orbit",
    {"order": 1, "jet": ["1", "2"]},
)
check("Q5 router refuses tools outside the active profile without invoking them",
      not blocked["ok"]
      and blocked["error"]["token"] == "TOOL_NOT_IN_PROFILE"
      and blocked["active_profile"] == "symbolic"
      and "cella_role_jet_orbit" in blocked["available_profiles"]["reference"])

explicit = router.call(
    "role_jet_orbit",
    {"order": 1, "jet": ["1", "2"]},
    profile="reference",
)
check("Q6 one-shot profile override dispatches without changing active profile",
      explicit["ok"]
      and explicit["active_profile"] == "symbolic"
      and explicit["effective_profile"] == "reference"
      and explicit["tool"] == "cella_role_jet_orbit"
      and router.active_profile == "symbolic")

bad_args = router.call("symbolic_equal", ["not", "a", "dict"])
check("Q7 malformed router calls return structured errors",
      not bad_args["ok"]
      and bad_args["error"]["token"] == "BAD_ARGS")

with tempfile.TemporaryDirectory() as folder:
    export_on = router.json_export(enabled=True, folder=folder)
    exported_call = router.call(
        "symbolic_equal",
        {"left": "x*x", "right": "x**2", "variables": ["x"]},
    )
    exported_path = Path(exported_call["json_export"]["path"])
    exported_exists = exported_path.exists()
    exported_payload = json.loads(exported_path.read_text())
    before_count = len(list(Path(folder).glob("*.json")))
    export_off = router.json_export(enabled=False)
    unexported_call = router.call(
        "symbolic_equal",
        {"left": "x+1", "right": "1+x", "variables": ["x"]},
    )
    after_count = len(list(Path(folder).glob("*.json")))
check("Q8 JSON export toggle writes full tool results to the nominated folder and stops cleanly",
      export_on["ok"]
      and export_on["enabled"] is True
      and exported_exists
      and exported_payload["tool"] == "cella_symbolic_equal"
      and exported_payload["result"]["value"]["equal"] is True
      and before_count == 1
      and export_off["ok"]
      and export_off["enabled"] is False
      and "json_export" not in unexported_call
      and after_count == before_count)

with tempfile.TemporaryDirectory() as folder:
    compact_on = router.json_export(enabled=True, folder=folder, inline_result=False)
    compact_call = router.call(
        "symbolic_equal",
        {"left": "(x+1)**2", "right": "x**2+2*x+1", "variables": ["x"]},
    )
    compact_payload = json.loads(Path(compact_call["json_export"]["path"]).read_text())
    router.json_export(enabled=False)
check("Q9 JSON export can suppress the full inline result while preserving the file readout",
      compact_on["ok"]
      and compact_on["inline_result"] is False
      and compact_call["ok"]
      and "result" not in compact_call
      and compact_call["result_summary"]["tool"] == "cella_symbolic_equal"
      and compact_call["result_summary"]["ok"] is True
      and compact_payload["result"]["value"]["equal"] is True)

try:
    build_router_mcp_server(default_profile="core")
    router_server_builds = True
except Exception as exc:
    print(f"Router server build failed: {exc}")
    router_server_builds = False
check("Q10 router MCP server instantiates", router_server_builds)

print()
if FAILS:
    print(f"GATE MCP ROUTER: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE MCP ROUTER: CLOSED — Cella router enables chat-native profile switching.")
sys.exit(0)
