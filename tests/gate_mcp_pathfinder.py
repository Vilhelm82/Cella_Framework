"""Gate MCP pathfinder route planning.

Run:  python tests/gate_mcp_pathfinder.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

FAILS = []


def check(name, ok):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


try:
    from cella.mcp_server import (
        TOOL_GROUPS,
        TOOL_NAMES,
        call_route_plan,
    )
except Exception as exc:
    print(f"GATE MCP PATHFINDER: OPEN - import failed: {exc}")
    sys.exit(1)


def route(expression, constants=None):
    return call_route_plan(
        expression=expression,
        sweep={"variable": "eps", "low": "1e-12", "high": "1e-4"},
        constants=constants,
    )


linear = route("(1 + eps) - 1")
check("PTH1 catastrophic same-leading-constant expression requests rewrite candidates",
      linear["ok"]
      and linear["value"]["decision"] == "rewrite_candidate_needed"
      and linear["value"]["operation_shape"] == "catastrophic_cancellation"
      and linear["value"]["exact_account_available"] is True
      and "cella_rewrite_candidates" in linear["value"]["next_tools"])

self_cancel = route("eps - eps")
check("PTH2 structural self-cancellation routes to symbolic collapse",
      self_cancel["ok"]
      and self_cancel["value"]["decision"] == "collapse_symbolically"
      and self_cancel["value"]["route_confidence"] == "high"
      and "cella_symbolic_rational" in self_cancel["value"]["next_tools"])

unknown = route("(A + eps) - A")
check("PTH3 missing constants are surfaced as blocking inputs",
      unknown["ok"]
      and unknown["value"]["decision"] == "needs_declared_constants"
      and "A" in unknown["value"]["blocking_inputs"]["missing_constants"])

benign = route("(1 + sqrt(eps)) - 1")
check("PTH4 benign cancellation remains direct but asks for BACL monitoring",
      benign["ok"]
      and benign["value"]["decision"] == "direct_ok"
      and benign["value"]["dominant_pattern"] == "sterbenz_safe_benign"
      and "cella_bacl_pair" in benign["value"]["next_tools"])

print()
if FAILS:
    print(f"GATE MCP PATHFINDER: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE MCP PATHFINDER: CLOSED - route planner, candidates, and comparison are MCP-callable.")
sys.exit(0)
