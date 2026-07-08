"""Gate MCP profile split.

The Cella MCP server can expose narrow tool profiles so Claude Desktop does not
load the entire toolbox into every chat context.

Run:  python tests/gate_mcp_profiles.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.mcp_server import TOOL_GROUPS, TOOL_NAMES, normalize_profile, tool_names_for_profile

FAILS = []


def check(name, ok):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


non_all = {k: v for k, v in TOOL_GROUPS.items() if k != "all"}
union = set().union(*(set(v) for v in non_all.values()))

check("P1 all profile remains the full historical MCP surface",
      tool_names_for_profile("all") == TOOL_NAMES
      and set(TOOL_GROUPS["all"]) == set(TOOL_NAMES))

check("P2 every narrow profile is smaller than all and includes cella_help",
      all(1 < len(names) < len(TOOL_NAMES) and names[0] == "cella_help"
          for names in non_all.values()))

check("P3 narrow profiles cover the full surface when intentionally combined",
      union == set(TOOL_NAMES))

check("P4 profile aliases normalize to canonical groups",
      normalize_profile("geometry") == "core"
      and normalize_profile("reference_lift") == "reference"
      and normalize_profile("bacl") == "clean"
      and normalize_profile("profiler") == "clean")

check("P5 reference-heavy tools are quarantined outside the core profile",
      "cella_role_jet_orbit" in TOOL_GROUPS["reference"]
      and "cella_wreath_law" in TOOL_GROUPS["reference"]
      and "cella_role_jet_orbit" not in TOOL_GROUPS["core"]
      and "cella_wreath_law" not in TOOL_GROUPS["core"])

check("P6 symbolic and cleanliness arms are independently loadable",
      set(TOOL_GROUPS["symbolic"]) == {
          "cella_help",
          "cella_symbolic_rational",
          "cella_symbolic_equal",
          "cella_symbolic_pole_law",
          "cella_symbolic_gauge_carrier",
          "cella_symbolic_channel_sum",
          "cella_symbolic_valuation",
      }
      and set(TOOL_GROUPS["clean"]) == {
          "cella_help",
          "cella_bacl_pair",
          "cella_operand_residue_trace",
          "cella_refinery_compare",
          "cella_cleanliness_rank",
          "cella_bacl_dial",
      })

check("P7 pathfinder is internal engine state, not a public profile",
      "pathfinder" not in TOOL_GROUPS
      and "cella_route_plan" not in TOOL_GROUPS["all"]
      and "cella_residual_profile" not in TOOL_GROUPS["all"]
      and "cella_rewrite_candidates" not in TOOL_GROUPS["all"]
      and "cella_pathfinder_compare" not in TOOL_GROUPS["all"]
      and "cella_cleanliness_rank" in TOOL_GROUPS["clean"]
      and "cella_refinery_compare" in TOOL_GROUPS["clean"])

try:
    normalize_profile("does-not-exist")
    bad_profile_rejected = False
except ValueError:
    bad_profile_rejected = True
check("P8 unknown profile is rejected before server launch", bad_profile_rejected)

print()
if FAILS:
    print(f"GATE MCP PROFILES: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE MCP PROFILES: CLOSED — Cella tool profiles split the MCP surface.")
sys.exit(0)
