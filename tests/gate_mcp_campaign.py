"""Gate MCP campaign arm — paper-native R&D proof tools.

This gate pins the tools lifted from the LEAD7 and PFC papers:

- local germ classification from metric leading data;
- role-divisor retrodiction tables;
- richer corner/front-face support certificates;
- positivity proof composition;
- metric-candidate selection records;
- KN metric construction summaries;
- exact implicit Gaussian-curvature referee.

Run:  python tests/gate_mcp_campaign.py
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
        call_cella_help,
        call_corner_frontface,
        call_diag_germ_classifier,
        call_implicit_gaussian_curvature,
        call_kn_metric_builder,
        call_metric_candidate_selector,
        call_positive_factor_certificate,
        call_role_divisor_retrodict,
    )
except Exception as exc:  # expected RED before implementation
    print(f"GATE MCP CAMPAIGN: OPEN — import failed: {exc}")
    sys.exit(1)


parity = call_diag_germ_classifier(
    coordinate="x",
    native={"leading": "B", "power": "2", "parity": "even"},
    transverse=[
        {"leading": "A1", "power": "-2", "parity": "even"},
        {"leading": "A2", "power": "-2", "parity": "even"},
    ],
)
generic = call_diag_germ_classifier(
    coordinate="delta",
    native={"leading": "A2", "power": "2"},
    transverse=[
        {"P0": "P0", "P1": "P1", "power": "0"},
        {"P0": "R0", "P1": "R1", "power": "0"},
    ],
)
check("R1 germ classifier recognizes parity-fixed and generic local laws",
      parity["ok"]
      and parity["value"]["kind"] == "parity_fixed"
      and parity["value"]["order"] == "4"
      and parity["value"]["coefficient_text"] == "-14/(B)"
      and generic["ok"]
      and generic["value"]["kind"] == "generic_quadratic"
      and generic["value"]["coefficient_text"] == "(P1/P0 + R1/R0)/(A2)")

retro = call_role_divisor_retrodict(
    divisors=[
        {"name": "T=0", "classifier": generic["value"]},
        {"name": "Omega=0", "classifier": parity["value"], "coefficient": "C_Omega"},
        {"name": "Phi_e=0", "classifier": parity["value"], "coefficient": "C_Phi"},
    ],
    expected_orders={"T=0": "3", "Omega=0": "4", "Phi_e=0": "4"},
)
check("R2 role-divisor retrodict emits the 3/4/4 complementarity table",
      retro["ok"]
      and retro["value"]["orders_match_expected"] is True
      and retro["value"]["order_signature"] == ["3", "4", "4"]
      and retro["value"]["table"][1]["coefficient"] == "C_Omega")

corner = call_corner_frontface(
    face_data={"p_x": "4", "p_y": "4", "r_x": "2", "r_y": "2"},
    path={"ax": "1", "ay": "1"},
)
weights_corner = call_corner_frontface(
    weights={"p0": "-6", "q0": "0", "p1": "2", "q1": "-2", "p2": "-2", "q2": "2"},
    path={"ax": "1", "ay": "1"},
)
check("R3 corner frontface supports face-data and weight-data inputs",
      corner["ok"]
      and corner["value"]["active_vertices"] == ["Vx", "Vy"]
      and corner["value"]["support_order"] == "2"
      and corner["value"]["balanced_direction"]["ax_over_ay"] == "1"
      and weights_corner["ok"]
      and weights_corner["value"]["vertices"]["V1"]["exponent"] == ["-4", "2"]
      and weights_corner["value"]["cancellation"]["A"] == "-84")

pos = call_positive_factor_certificate(
    variables=["t"],
    factors=[
        {
            "name": "h",
            "terms": [["1", [3]], ["5", [2]], ["3", [1]], ["-9", [0]]],
            "method": "sturm_open_ray",
            "lower": "1",
            "sample": "2",
        },
        {
            "name": "shifted_square_plus",
            "terms": [["1", [2]], ["-2", [1]], ["2", [0]]],
            "method": "coefficient_shift",
            "shifts": {"t": {"new": "r", "offset": "1"}},
        },
    ],
)
check("R4 positivity composer combines Sturm and shifted coefficient certificates",
      pos["ok"]
      and pos["value"]["positive"] is True
      and pos["value"]["factors"]["h"]["positive"] is True
      and pos["value"]["factors"]["shifted_square_plus"]["method"] == "coefficient_nonnegative_on_positive_orthant")

selection = call_metric_candidate_selector(
    candidates=[
        {
            "name": "sum_then_invert",
            "n2_reduction": True,
            "positive_definite": True,
            "role_boundary_sensitive": False,
            "interior_pole_free": True,
        },
        {
            "name": "invert_then_sum_u1",
            "n2_reduction": True,
            "positive_definite": True,
            "role_boundary_sensitive": True,
            "interior_pole_free": False,
        },
        {
            "name": "mass_role_u0",
            "n2_reduction": True,
            "positive_definite": True,
            "role_boundary_sensitive": True,
            "interior_pole_free": True,
            "graph_norm": True,
        },
    ],
)
check("R5 metric candidate selector chooses mass-role u=0 and explains failures",
      selection["ok"]
      and selection["value"]["selected"] == "mass_role_u0"
      and selection["value"]["candidate_results"]["sum_then_invert"]["decision"] == "rejected"
      and "hides_role_boundary_poles" in selection["value"]["candidate_results"]["sum_then_invert"]["reasons"]
      and "interior_channel_isotropy_pole" in selection["value"]["candidate_results"]["invert_then_sum_u1"]["reasons"])

kn = call_kn_metric_builder(
    roles=["S", "J", "Q"],
    assembly="mass_role_inverse_sum",
    graph_norm=True,
    u="0",
)
check("R6 KN metric builder returns the graph-normalized mass-role inverse-channel formulae",
      kn["ok"]
      and kn["value"]["selected_metric"] == "g_F(u=0)"
      and kn["value"]["role_divisors"] == {"T": "U_S=0", "Omega": "J=0", "Phi_e": "Q=0"}
      and kn["value"]["components"]["G_i"]["formula"].startswith("(U_i^2 + 4U"))

kg = call_implicit_gaussian_curvature(
    gradient=["3", "1", "2"],
    hessian=[["2", "1", "0"], ["1", "0", "0"], ["0", "0", "2"]],
)
check("R7 implicit Gaussian-curvature referee returns exact bordered-Hessian K_G",
      kg["ok"]
      and kg["value"]["K_G"] == "-3/49"
      and kg["value"]["method"] == "bordered_hessian_implicit_surface")

help_all = call_cella_help()
help_germ = call_cella_help("cella_diag_germ_classifier")
check("R8 help includes the campaign R&D workflow",
      help_all["ok"]
      and "campaign_retrodiction" in help_all["value"]["recommended_workflows"]
      and help_germ["ok"]
      and "parity_fixed" in help_germ["value"]["tool"]["read_result"])

check("R9 MCP tool names include the campaign arm",
      {
          "cella_corner_frontface",
          "cella_diag_germ_classifier",
          "cella_implicit_gaussian_curvature",
          "cella_kn_metric_builder",
          "cella_metric_candidate_selector",
          "cella_positive_factor_certificate",
          "cella_role_divisor_retrodict",
      } <= set(TOOL_NAMES))

print()
if FAILS:
    print(f"GATE MCP CAMPAIGN: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE MCP CAMPAIGN: CLOSED — paper-native R&D campaign tools are MCP-callable.")
sys.exit(0)
