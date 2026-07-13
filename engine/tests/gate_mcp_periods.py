"""Gate MCP native period/residue spike.

This gate is deliberately structural: it checks exact quartic data, third-kind
residue ledgers, CPV period normal forms, route comparison, and explicit gap
records. It does not accept numerical route agreement as a substitute.

Run:  python tests/gate_mcp_periods.py
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
        call_period_gap_report,
        call_period_normal_form,
        call_period_quartic,
        call_period_route_compare,
        call_period_third_kind_residue,
    )
except Exception as exc:  # expected RED before implementation
    print(f"GATE MCP PERIODS: OPEN — import failed: {exc}")
    sys.exit(1)


quartic = call_period_quartic(kind="legendre_even", m="1/2")
check("P1 native quartic records exact Legendre curve structure",
      quartic["ok"]
      and quartic["value"]["curve_id"] == "legendre_even:m=1/2"
      and quartic["value"]["equation"] == "y^2 = (1 - x^2)*(1 - (1/2)*x^2)"
      and quartic["value"]["branch_squares"] == ["1", "2"]
      and quartic["value"]["j_invariant"] == "1728"
      and quartic["value"]["method"] == "cella_native_exact_quartic_record")

residue = call_period_third_kind_residue(
    curve={"kind": "legendre_even", "m": "1/2"},
    n="2",
    prefactor="8",
)
check("P2 third-kind pole residue is exact in Q(sqrt 3) with branch jumps",
      residue["ok"]
      and residue["value"]["x0_squared"] == "1/2"
      and residue["value"]["y0_squared"] == "3/8"
      and residue["value"]["residue_square"] == "64/3"
      and residue["value"]["positive_x_residue"] == {
          "type": "QSqrt", "a": "0", "b": "-8/3", "r": "3"}
      and residue["value"]["negative_x_residue"] == {
          "type": "QSqrt", "a": "0", "b": "8/3", "r": "3"}
      and residue["value"]["residue_antisymmetry"] is True
      and residue["value"]["one_sided_offset_over_pi_i"] == {
          "type": "QSqrt", "a": "0", "b": "-8/3", "r": "3"}
      and residue["value"]["two_sided_jump_over_pi_i"] == {
          "type": "QSqrt", "a": "0", "b": "-16/3", "r": "3"})

cpv_form = call_period_normal_form(
    kind="third_kind_cpv",
    curve={"kind": "legendre_even", "m": "1/2"},
    n="2",
    scale="3",
    weight_pi="5",
    weight_k="7",
)
check("P3 CPV normal form reduces to exact K/Pi basis coefficients",
      cpv_form["ok"]
      and cpv_form["value"]["basis_terms"] == {
          "K(1/2)": "-6",
          "Pi(1/4;1/2)": "-15",
      }
      and cpv_form["value"]["regular_parameter_q"] == "1/4"
      and cpv_form["value"]["numeric_evaluation"] is None
      and cpv_form["value"]["gaps"][0]["gap"] == "certified_numeric_evaluation")

declared_same = call_period_normal_form(
    kind="declared_basis",
    curve={"kind": "legendre_even", "m": "1/2"},
    basis_terms=[
        {"atom": "Pi(1/4;1/2)", "coefficient": "-15"},
        {"atom": "K(1/2)", "coefficient": "-6"},
    ],
)
route_same = call_period_route_compare(cpv_form["value"], declared_same["value"])
check("P4 route comparison proves structural equality independent of term order",
      route_same["ok"]
      and route_same["value"]["equivalent"] is True
      and route_same["value"]["difference_terms"] == {}
      and route_same["value"]["method"] == "exact_period_normal_form_difference")

declared_wrong = call_period_normal_form(
    kind="declared_basis",
    curve={"kind": "legendre_even", "m": "1/2"},
    basis_terms=[
        {"atom": "K(1/2)", "coefficient": "-5"},
        {"atom": "Pi(1/4;1/2)", "coefficient": "-15"},
    ],
)
route_wrong = call_period_route_compare(cpv_form["value"], declared_wrong["value"])
check("P5 route comparison exposes exact period-basis mismatch",
      route_wrong["ok"]
      and route_wrong["value"]["equivalent"] is False
      and route_wrong["value"]["difference_terms"] == {"K(1/2)": "-1"}
      and route_wrong["value"]["first_gap"]["gap"] == "period_basis_mismatch")

gaps = call_period_gap_report(scope="elliptic_quartic_spike")
gap_names = [item["gap"] for item in gaps["value"]["gaps"]]
check("P6 gap report names the next spike targets explicitly",
      gaps["ok"]
      and gap_names == [
          "certified_numeric_evaluation",
          "general_algebraic_number_field",
          "general_rational_differential_reduction",
          "raw_bordered_hessian_surface_route",
      ]
      and all(item["status"] == "open" for item in gaps["value"]["gaps"]))

check("P7 native period tools are exposed through the arithmetic profile",
      all(name in TOOL_NAMES for name in {
          "cella_period_quartic",
          "cella_period_third_kind_residue",
          "cella_period_normal_form",
          "cella_period_route_compare",
          "cella_period_gap_report",
      })
      and all(name in TOOL_GROUPS["arithmetic"] for name in {
          "cella_period_quartic",
          "cella_period_third_kind_residue",
          "cella_period_normal_form",
          "cella_period_route_compare",
          "cella_period_gap_report",
      }))

print()
if FAILS:
    print(f"GATE MCP PERIODS: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE MCP PERIODS: CLOSED — native period/residue spike is MCP-callable.")
sys.exit(0)
