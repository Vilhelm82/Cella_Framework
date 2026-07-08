"""Gate MCP reference-lift arm.

This gate pins the highest-ROI practical tools lifted from Reference_Material:

- exact active role-jet S3 orbits;
- active graph curvature spectra;
- n=3 three-channel referee records and gauge-channel transport;
- n=3 RoleChSpec densities with linear carrier recovery;
- role-pair carrier/loss diagnostics;
- Johnson shadow-law scalar and universal direction;
- gcd/wreath monodromy law for self-glue style covers.

Run:  python tests/gate_mcp_reference.py
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
        call_curvature_orbit_spectrum,
        call_gauge_channel_transport,
        call_role_jet_orbit,
        call_role_pair_loss_diagnostic,
        call_rolechspec_n3,
        call_shadow_law,
        call_three_channel_referee,
        call_wreath_law,
    )
except Exception as exc:  # expected RED before implementation
    print(f"GATE MCP REFERENCE: OPEN — import failed: {exc}")
    sys.exit(1)


jet = call_role_jet_orbit(
    order=3,
    jet=["4", "3", "5/2", "-7/3", "11/5", "13/7", "-17/11", "19/13", "-23/17"],
    exponents=["2", "1"],
)
check("X1 role-jet orbit verifies S3 laws and projective invariants",
      jet["ok"]
      and jet["value"]["group_laws"] == {"s2": True, "t2": True, "st3": True}
      and jet["value"]["first_projective_invariants"]["I1"] == "-5/2"
      and jet["value"]["first_projective_invariants"]["I2"] == "-18"
      and jet["value"]["first_projective_invariants"]["Delta_n"] == "400"
      and jet["value"]["degree_spectrum"] == ["-1", "-1", "0", "0", "3", "3"])

orbit = call_curvature_orbit_spectrum(
    graph_jet=["5", "7", "2", "3", "4"],
)
check("X2 active graph curvature orbit collapses six ordered charts to three outputs",
      orbit["ok"]
      and orbit["value"]["unique_output_spectrum_count"] == "3"
      and orbit["value"]["total_curvature_values"] == ["-1/5625"]
      and orbit["value"]["charts"][0]["spectrum"]["kappa_int"] == "0"
      and orbit["value"]["output_spectra"]["P"]["kappa_c"] == "-1/625")

tc = call_three_channel_referee(
    gradient=["3", "1", "2"],
    hessian=[["2", "1", "0"], ["1", "0", "0"], ["0", "0", "2"]],
)
check("X3 three-channel referee returns deltas, bordered determinant, and labeled channels",
      tc["ok"]
      and tc["value"]["channels"] == {
          "K_G": "-3/49",
          "kappa_c": "-1/49",
          "kappa_s": "1/49",
          "kappa_int": "-3/49",
      }
      and tc["value"]["deltas"] == {"Delta_c": "4", "Delta_s": "-4", "Delta_m": "12"}
      and tc["value"]["bordered_det"] == "12"
      and tc["value"]["mutation_traps"]["mirror_self_formula_caught"] is True)

transport = call_gauge_channel_transport(
    gradient=["3", "1", "2"],
    hessian=[["2", "1", "0"], ["1", "0", "0"], ["0", "0", "2"]],
    gauge=["1", "0", "0"],
)
transport_e3 = call_gauge_channel_transport(
    gradient=["3", "1", "2"],
    hessian=[["2", "1", "0"], ["1", "0", "0"], ["0", "0", "2"]],
    gauge=["0", "0", "1"],
)
check("X4 gauge-channel transport preserves K and classifies single-edge pin/move axes",
      transport["ok"]
      and transport["value"]["moved"]["channels"]["kappa_c"] == "-1/49"
      and transport["value"]["delta"]["sum_channels"] == "0"
      and transport["value"]["single_edge"]["endpoint_axes"] == ["0", "1"]
      and transport_e3["ok"]
      and transport_e3["value"]["delta"]["kappa_c"] == "6/49"
      and transport_e3["value"]["single_edge"]["opposite_axis"] == "2")

rolech = call_rolechspec_n3(
    gradient=["3", "1", "2"],
    hessian=[["2", "1", "0"], ["1", "0", "0"], ["0", "0", "2"]],
)
check("X5 RoleChSpec densities recover the gauge-normal carrier without Groebner swell",
      rolech["ok"]
      and rolech["value"]["carrier_O"] == ["2/3", "-13/6", "-1/2"]
      and rolech["value"]["recovery"]["recovered_O"] == ["2/3", "-13/6", "-1/2"]
      and rolech["value"]["recovery"]["determinant"] != "0"
      and rolech["value"]["charts"]["P"]["r2"]["kappa_int_hat"] == "0")

loss = call_role_pair_loss_diagnostic(n=5)
loss4 = call_role_pair_loss_diagnostic(n=4)
check("X6 role-pair loss diagnostic exposes marginal loss and n=4 quotient accident",
      loss["ok"]
      and loss["value"]["carrier_dim"] == "10"
      and loss["value"]["magnitude_summary_dim"] == "5"
      and loss["value"]["shape_dim"] == "5"
      and loss["value"]["shape_status"] == "faithful"
      and loss["value"]["faithfulness_margin"] == "4"
      and loss4["ok"]
      and loss4["value"]["shape_status"] == "quotient_S4_over_V4")

shadow = call_shadow_law(n=4, gradient=["1", "2", "3", "5"])
check("X7 shadow law returns Johnson direction and exact scalar s(g)",
      shadow["ok"]
      and shadow["value"]["direction_eigenvalues"] == {
          "triv": "-2",
          "std": "2",
          "shape": "4",
      }
      and shadow["value"]["scalar_s"] == "1261/3600"
      and shadow["value"]["triangle_weights"]["0,1,2"] == "1/25")

wreath = call_wreath_law(kind="trinomial_layer", m=6, k=2)
product = call_wreath_law(kind="self_glue_product", m=3)
directive = call_wreath_law(kind="self_glue_directive", m=3)
check("X8 wreath law certifies gcd layer and product/directive asymmetry",
      wreath["ok"]
      and wreath["value"]["gcd"] == "2"
      and wreath["value"]["group"] == "C_2 wr S_3"
      and wreath["value"]["order"] == "48"
      and product["value"]["group"] == "C_3 wr C_3"
      and product["value"]["order"] == "81"
      and directive["value"]["group"] == "S_3 wr S_3"
      and directive["value"]["order"] == "1296")

help_all = call_cella_help()
check("X9 help and MCP tool names include the reference-lift arm",
      help_all["ok"]
      and "reference_lift" in help_all["value"]["recommended_workflows"]
      and {
          "cella_curvature_orbit_spectrum",
          "cella_gauge_channel_transport",
          "cella_role_jet_orbit",
          "cella_role_pair_loss_diagnostic",
          "cella_rolechspec_n3",
          "cella_shadow_law",
          "cella_three_channel_referee",
          "cella_wreath_law",
      } <= set(TOOL_NAMES))

print()
if FAILS:
    print(f"GATE MCP REFERENCE: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE MCP REFERENCE: CLOSED — Reference_Material lifts are MCP-callable.")
sys.exit(0)
