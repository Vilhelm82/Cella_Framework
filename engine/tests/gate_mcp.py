"""Gate MCP — Cella as an MCP-callable exact geometry tool.

This gate does not test the MCP transport itself. It tests the callable surface
that the MCP server exposes: exact JSON inputs in, certificate-shaped exact JSON
out, no floats, and Cella refusals instead of numeric garbage.

Run:  python tests/gate_mcp.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

FAILS = []


def check(name, ok):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


POINT = ["1", "1", "1"]
G = ["3", "1", "2"]
H = [["2", "1", "0"], ["1", "0", "0"], ["0", "0", "2"]]


try:
    from cella.mcp_server import (
        TOOL_NAMES,
        call_carrier,
        call_channels_n3,
        call_fingerprint,
        call_sensor,
        call_sigma_tower,
        exact_to_json,
    )
except Exception as exc:  # expected RED before implementation
    print(f"GATE MCP: OPEN — import failed: {exc}")
    sys.exit(1)


carrier = call_carrier(POINT, G, H)
check("M1 carrier returns exact keystone O, no refusal",
      carrier["ok"] and carrier["value"] == ["2/3", "-13/6", "-1/2"]
      and carrier["refusal"] is None)
check("M1 carrier emits certificate-shaped metadata",
      carrier["schema"] == "cella-mcp-v1"
      and carrier["number_type"] == "Q"
      and "rerun_digest" in carrier
      and len(carrier["rerun_digest"]) == 16)

tower = call_sigma_tower(POINT, G, H)
check("M2 sigma tower preserves odd QSqrt and even rational values",
      tower["ok"]
      and tower["value"] == [
          {"type": "QSqrt", "a": "0", "b": "-6/49", "r": "14"},
          "-3/49",
      ])

channels = call_channels_n3(POINT, G, H)
check("M3 n=3 channels are labeled and K_G is their exact sum",
      channels["ok"]
      and channels["value"] == {
          "kc": "-1/49",
          "kint": "-3/49",
          "ks": "1/49",
          "K_G": "-3/49",
      })

num = call_sensor("numerator_tower", POINT, G, H)
shape = call_sensor("shape_moment", POINT, G, H)
loc = call_sensor("localization", POINT, G, H)
check("M4 sensor dispatcher exposes numerator tower, shape moment, localization",
      num["ok"] and num["value"] == ["-1/49"]
      and shape["ok"] and shape["value"][2] == "0"
      and loc["ok"] and loc["value"] == ["4"])

iso = call_fingerprint(
    POINT,
    ["-2", "-2", "1"],
    [["-2", "0", "0"], ["0", "-2", "0"], ["0", "0", "0"]],
)
check("M5 fingerprint returns typed CHANNEL_ISOTROPIC refusal, not a value",
      not iso["ok"]
      and iso["value"] is None
      and iso["refusal"]["token"] == "CHANNEL_ISOTROPIC"
      and "P" in iso["refusal"]["stratum"])

try:
    exact_to_json(0.25)
    float_blocked = False
except TypeError:
    float_blocked = True
check("M6 JSON exact serializer blocks floats on verdict paths", float_blocked)

check("M7 MCP tool names cover the practical Cella surface",
      set(TOOL_NAMES) == {
          "cella_help",
          "cella_arith_constant_pin",
          "cella_arith_precision_budget",
          "cella_arith_refine",
          "cella_bacl_dial",
          "cella_bacl_pair",
          "cella_carlson_period_referee",
          "cella_carrier",
          "cella_channels_n3",
          "cella_cleanliness_rank",
          "cella_corner_frontface",
          "cella_corner_newton",
          "cella_curvature_orbit_spectrum",
          "cella_diag_germ_classifier",
          "cella_elliptic_legendre_reduce",
          "cella_fingerprint",
          "cella_gauge_channel_transport",
          "cella_implicit_gaussian_curvature",
          "cella_kn_metric_builder",
          "cella_local_pole_law",
          "cella_metric_candidate_selector",
          "cella_operand_residue_trace",
          "cella_period_curve_invariants",
          "cella_period_gap_report",
          "cella_period_normal_form",
          "cella_period_quartic",
          "cella_period_route_compare",
          "cella_period_third_kind_residue",
          "cella_dbp_relative_period",
          "cella_dbp_certificate_verify",
          "cella_legendre_ke_enclose",
          "cella_legendre_pinning",
          "cella_dbp_landen_trace_verify",
          "cella_dbp_release_receipt",
          "cella_poly_certificate",
          "cella_positive_factor_certificate",
          "cella_pslq_field_referee",
          "cella_refinery_compare",
          "cella_residue_branch_gate",
          "cella_role_divisor_retrodict",
          "cella_role_jet_orbit",
          "cella_role_pair_loss_diagnostic",
          "cella_rolechspec_n3",
          "cella_sensor",
          "cella_shadow_law",
          "cella_sigma_tower",
          "cella_surface_jet",
          "cella_sturm_positive",
          "cella_symbolic_channel_sum",
          "cella_symbolic_equal",
          "cella_symbolic_gauge_carrier",
          "cella_symbolic_pole_law",
          "cella_symbolic_rational",
          "cella_symbolic_valuation",
          "cella_third_kind_cpv",
          "cella_three_channel_referee",
          "cella_two_route_compare",
          "cella_wreath_law",
      })

print()
if FAILS:
    print(f"GATE MCP: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE MCP: CLOSED — exact Cella geometry surface is MCP-callable.")
sys.exit(0)
