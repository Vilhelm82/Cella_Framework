"""Gate MCP proof tools — certified local geometry and polynomial proof.

This gate tests the callable surface that the MCP server exposes for the
first proof-kernel layer. These tools are exact and certificate-shaped; they
replace recurring SymPy/mpmath proof moves from verification scripts with
Cella-owned records.

Run:  python tests/gate_mcp_proof.py
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
        TOOL_NAMES,
        call_corner_newton,
        call_local_pole_law,
        call_poly_certificate,
        call_sturm_positive,
        call_surface_jet,
    )
except Exception as exc:  # expected RED before implementation
    print(f"GATE MCP PROOF: OPEN — import failed: {exc}")
    sys.exit(1)


pf = call_local_pole_law(kind="parity_fixed", m=2, B="7")
check("P1 parity-fixed law returns exact order and coefficient",
      pf["ok"]
      and pf["value"]["order"] == "4"
      and pf["value"]["coefficient"] == "-2"
      and pf["value"]["intrinsic_distance"]["power"] == "2"
      and pf["value"]["intrinsic_distance"]["coefficient"] == "-7/2")

gen = call_local_pole_law(
    kind="generic_quadratic",
    A="5",
    transverse_P0=["2", "3"],
    transverse_P1=["7", "11"],
)
check("P2 generic quadratic collapse returns exact order-3 drift coefficient",
      gen["ok"]
      and gen["value"]["order"] == "3"
      and gen["value"]["coefficient"] == "43/30"
      and gen["value"]["drift"] == "43/6")

master = call_local_pole_law(kind="master_quadric", exponents=["2", "-2", "-2"], B="7")
check("P2b master quadric exponent vector returns C(p) and the exact pole coefficient",
      master["ok"]
      and master["value"]["order"] == "4"
      and master["value"]["C_p"] == "-14"
      and master["value"]["coefficient"] == "-2"
      and master["value"]["transverse_exponents"] == ["-2", "-2"])

flat_master = call_local_pole_law(kind="master_quadric", exponents=["2", "0", "0"])
check("P2c master quadric finite transverse exponents produce zero monomial pole",
      flat_master["ok"]
      and flat_master["value"]["C_p"] == "0"
      and flat_master["value"]["coefficient"] == "0")

corner = call_corner_newton(
    weights={"p0": "-6", "q0": "0", "p1": "2", "q1": "-2", "p2": "-2", "q2": "2"},
    path={"ax": "1", "ay": "1"},
)
check("P3 corner Newton rule recovers KN active vertices and balanced order 2",
      corner["ok"]
      and corner["value"]["vertices"]["V1"]["exponent"] == ["-4", "2"]
      and corner["value"]["vertices"]["V2"]["exponent"] == ["2", "-4"]
      and corner["value"]["vertices"]["V0"]["polar"] is False
      and corner["value"]["support_order"] == "2")

poly = call_poly_certificate(
    variables=["t"],
    terms=[["1", [2]], ["-2", [1]], ["4", [0]]],
    shifts={"t": {"new": "r", "offset": "1"}},
)
check("P4 coefficient certificate proves shifted polynomial positive",
      poly["ok"]
      and poly["value"]["positive"] is True
      and poly["value"]["variables"] == ["r"]
      and poly["value"]["terms"] == [["3", ["0"]], ["1", ["2"]]])

sturm = call_sturm_positive(
    variable="t",
    terms=[["1", [2]], ["-2", [1]], ["2", [0]]],
    lower="1",
)
check("P5 Sturm certificate proves no roots and positive sign on (1, infinity)",
      sturm["ok"]
      and sturm["value"]["positive"] is True
      and sturm["value"]["root_count"] == "0"
      and sturm["value"]["sample_value"] == "2")

jet = call_surface_jet(
    expression="D**2 + D*S + P**2 - 3",
    variables=["D", "S", "P"],
    point=["1", "1", "1"],
)
check("P5b symbolic surface bridge returns exact value, gradient, and Hessian",
      jet["ok"]
      and jet["value"]["surface_value"] == "0"
      and jet["value"]["on_surface"] is True
      and jet["value"]["gradient"] == ["3", "1", "2"]
      and jet["value"]["hessian"] == [["2", "1", "0"], ["1", "0", "0"], ["0", "0", "2"]]
      and jet["value"]["jet"] == {
          "point": ["1", "1", "1"],
          "g": ["3", "1", "2"],
          "H": [["2", "1", "0"], ["1", "0", "0"], ["0", "0", "2"]],
      })

try:
    call_surface_jet(
        expression="x + 0.1",
        variables=["x"],
        point=["0"],
        require_on_surface=False,
    )
    decimal_rejected = False
except ValueError:
    decimal_rejected = True
check("P5c symbolic surface bridge rejects decimal literals instead of rationalizing them",
      decimal_rejected)

check("P6 MCP tool names include proof-kernel tools",
      {
          "cella_corner_newton",
          "cella_local_pole_law",
          "cella_poly_certificate",
          "cella_surface_jet",
          "cella_sturm_positive",
      } <= set(TOOL_NAMES))

print()
if FAILS:
    print(f"GATE MCP PROOF: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE MCP PROOF: CLOSED — certified proof-kernel surface is MCP-callable.")
sys.exit(0)
