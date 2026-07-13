"""Gate MCP arithmetic arm.

The arithmetic arm certifies high-precision numerical work by combining exact
symbolic gates, admissible special-function routes, independent numerical
referees, and honest precision/refusal records.

Run:  python tests/gate_mcp_arithmetic.py
"""

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

FAILS = []


def check(name, ok):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


try:
    from cella.typed_elementary import (
        RefineStatus,
        exp_eval,
        log_eval,
        pi_eval,
        typed_acos,
        typed_atan,
        typed_cos,
        typed_exp,
        typed_log,
        typed_log2,
        typed_pow,
        typed_refine,
        typed_sin,
        typed_tan,
    )
    from cella.probe_observers import (
        DeclaredAlphaModel,
        directional_alpha_probe,
        scalar_alpha_jet_bundle,
        singular_alpha_jet_bundle,
        sweep_signature_probe,
        typed_finite_difference,
    )
    from cella.mcp_server import (
        TOOL_GROUPS,
        TOOL_NAMES,
        call_arith_constant_pin,
        call_arith_precision_budget,
        call_arith_refine,
        call_carlson_period_referee,
        call_elliptic_legendre_reduce,
        call_period_curve_invariants,
        call_pslq_field_referee,
        call_residue_branch_gate,
        call_third_kind_cpv,
        call_two_route_compare,
    )
except Exception as exc:  # expected RED before implementation
    print(f"GATE MCP ARITHMETIC: OPEN — import failed: {exc}")
    sys.exit(1)


constructive_refine = typed_refine(log_eval, "2", 12)
check("A0 constructive typed_refine/log_eval resolves without libm",
      constructive_refine["status"] == RefineStatus.REFINED_CORRECTLY_ROUNDED
      and constructive_refine["value"] is not None
      and int(constructive_refine["working_bits"]) >= 14)

elementary = {
    "exp0": typed_exp("0", 12),
    "log1": typed_log("1", 12),
    "log2": typed_log2("2", 10),
    "sin0": typed_sin("0", 12),
    "cos0": typed_cos("0", 12),
    "atan1": typed_atan("1", 10),
    "acos1": typed_acos("1", 12),
    "pow": typed_pow("4", "1/2", 10),
    "tan0": typed_tan("0", 12),
}
check("A0b constructive typed elementary family exposes rounded dyadic values/refusals",
      elementary["exp0"]["value"] == "1"
      and elementary["log1"]["value"] == "0"
      and elementary["sin0"]["value"] == "0"
      and elementary["cos0"]["value"] == "1"
      and elementary["acos1"]["value"] == "0"
      and elementary["pow"]["value"] == "2"
      and elementary["tan0"]["value"] == "0"
      and elementary["log2"]["status"] == RefineStatus.REFINED_CORRECTLY_ROUNDED
      and elementary["atan1"]["status"] == RefineStatus.REFINED_CORRECTLY_ROUNDED)

domain_refusal = typed_log("-1", 12)
pi_enclosure = pi_eval(20)
exp_enclosure = exp_eval("0", 20)
check("A0c constructive evaluators preserve domain refusal and rational enclosures",
      domain_refusal["status"] == RefineStatus.REFINED_DOMAIN_REFUSED
      and Fraction(pi_enclosure["lo"]) < Fraction(pi_enclosure["hi"])
      and exp_enclosure["lo"] == "1"
      and exp_enclosure["hi"] == "1")

fd = typed_finite_difference(lambda x: x * x, 1.0e-3, 1.0e-9, function_label="square")
sweep_sig = sweep_signature_probe(
    lambda x: x * x,
    [1.0e-6, 1.0e-5, 1.0e-4, 1.0e-3],
    eta=1.0e-3,
    function_label="square",
    probe_id="square_sweep",
)
alpha_model = DeclaredAlphaModel("quadratic", 2.0, 0.10)
alpha = directional_alpha_probe(
    lambda h: h * h,
    [1.0e-6, 1.0e-5, 1.0e-4, 1.0e-3],
    probe_id="quadratic_alpha",
    function_label="quadratic",
    eta=1.0e-3,
    declared_alpha_models=[alpha_model],
)
scalar_jet = scalar_alpha_jet_bundle(
    lambda x: (x - 1.0) * (x - 1.0),
    1.0,
    [1.0e-6, 1.0e-5, 1.0e-4, 1.0e-3],
    probe_id="scalar_quad",
    function_label="scalar_quad",
    eta=1.0e-3,
    declared_alpha_models=[alpha_model],
)
singular_jet = singular_alpha_jet_bundle(
    lambda x: 1.0 / (x - 1.0),
    1.0,
    [1.0e-4, 1.0e-3, 1.0e-2, 1.0e-1],
    probe_id="simple_pole",
    function_label="simple_pole",
    eta=1.0e-3,
    declared_alpha_models=[DeclaredAlphaModel("pole", -1.0, 0.15)],
)
check("A0d copied V4 probe observers classify sweep, alpha, and local jet shape",
      fd["status"] == "transfer_observed"
      and sweep_sig["status"] == "sweep_signature_clean"
      and abs(sweep_sig["slope_observation"]["slope"] - 1.0) < 0.05
      and alpha["status"] == "alpha_regular_integer"
      and alpha["selected_alpha_model"] == "quadratic"
      and scalar_jet["status"] == "scalar_jet_regular_integer_alpha"
      and scalar_jet["selected_alpha_model"] == "quadratic"
      and singular_jet["status"] == "singular_jet_negative_alpha_singularity"
      and singular_jet["selected_alpha_model"] == "pole")


SQRT2 = "sqrt(2)"
M_DUAL = "(2 + sqrt(2))/4"
N_DUAL = "(4 + 3*sqrt(2))/8"
P_DUAL = "-2**(7/4)*(3 - 2*sqrt(2))"


refine = call_arith_refine(
    required_bits=5,
    enclosures=[
        {"working_bits": 5, "lo": "1", "hi": "9/8"},
        {"working_bits": 8, "lo": "17/16", "hi": "17/16"},
    ],
)
check("A1 Ziv refinement resolves only when endpoint rounding agrees",
      refine["ok"]
      and refine["value"]["status"] == "refined_correctly_rounded"
      and refine["value"]["value"] == "17/16"
      and refine["value"]["working_bits"] == "8"
      and refine["value"]["iterations"] == "2")

budget = call_arith_precision_budget(
    output_bits=80,
    path_losses=[7, 13],
    format_bits=128,
    atoms=[
        {"name": "elliptic_route", "kind": "construct_to_tolerance", "budget_bits": 220},
        {"name": "float64_leaf", "kind": "finite_exact_algebraic", "format_bits": 53},
    ],
)
check("A2 precision budget separates global floor from per-atom meetability",
      budget["ok"]
      and budget["value"]["composition_floor"] == "100"
      and budget["value"]["overall_verdict"] == "unmeetable"
      and budget["value"]["atoms"][0]["verdict"] == "proven"
      and budget["value"]["atoms"][1]["verdict"] == "unmeetable")

reduction = call_elliptic_legendre_reduce(m=M_DUAL, n=N_DUAL)
check("A3 Legendre reducer refuses naive singular ellippi and gives regular CPV route",
      reduction["ok"]
      and reduction["value"]["singular_third_kind"] is True
      and reduction["value"]["naive_ellippi_allowed"] is False
      and reduction["value"]["regular_parameter_q"] == "-2 + 2*sqrt(2)"
      and "K(m) - Pi(q; m)" in reduction["value"]["identity"])

residue = call_residue_branch_gate(m=M_DUAL, n=N_DUAL, prefactor=P_DUAL)
check("A4 residue gate proves signed weighted residue and branch offsets",
      residue["ok"]
      and residue["value"]["weighted_residue"] == "4"
      and residue["value"]["weighted_residue_minpoly"] == "x - 4"
      and residue["value"]["one_sided_offset"] == "+/-4*pi*i"
      and residue["value"]["two_sided_jump"] == "8*pi*i")

cpv = call_third_kind_cpv(
    m=M_DUAL,
    n=N_DUAL,
    scale="-2**(7/4)",
    weight_pi="3 - 2*sqrt(2)",
    weight_k="2 - 2*sqrt(2)",
    dps=90,
    tolerance="1e-35",
    contour_height="0.25",
)
check("A5 third-kind CPV uses two admissible routes and records achieved floor",
      cpv["ok"]
      and cpv["value"]["routes_agree"] is True
      and cpv["value"]["naive_ellippi_used"] is False
      and int(cpv["value"]["achieved_decimal_digits"]) >= 35
      and abs(float(cpv["value"]["branch_offset_weighted_over_pi_abs"]) - 4.0) < 1e-12)

carlson = call_carlson_period_referee(
    m_primary="(2 - sqrt(2))/4",
    m_dual=M_DUAL,
    dps=90,
)
check("A6 Carlson period referee independently gates omega identities",
      carlson["ok"]
      and carlson["value"]["all_gates_passed"] is True
      and int(carlson["value"]["omega1_digits"]) >= 50
      and int(carlson["value"]["im_omega2_digits"]) >= 50
      and int(carlson["value"]["rhombic_digits"]) >= 50)

compare = call_two_route_compare(
    route_a="1.234567890123456789",
    route_b="1.234567890123456780",
    requested_digits=17,
)
check("A7 two-route comparator reports an achieved agreement floor",
      compare["ok"]
      and compare["value"]["certified_to_requested"] is True
      and int(compare["value"]["achieved_decimal_digits"]) >= 17)

curve = call_period_curve_invariants(lambda_value="(2 - sqrt(2))/4", partner_j="128")
check("A8 curve invariant tool proves lambda product, j, and Phi2 isogeny",
      curve["ok"]
      and curve["value"]["lambda_product"] == "1/8"
      and curve["value"]["j"] == "10976"
      and curve["value"]["phi2_partner_zero"] is True)

pslq = call_pslq_field_referee(value="3 + 2*sqrt(2)", basis=["1", "sqrt(2)"], max_coeff=5)
check("A9 field-aware PSLQ referee returns bounded relations without overclaiming",
      pslq["ok"]
      and pslq["value"]["relation_found"] is True
      and pslq["value"]["coefficients"] == ["3", "2"]
      and pslq["value"]["scope"] == "bounded-search")

pin = call_arith_constant_pin(
    name="dual_cpv_demo",
    value="-3.98800108597455809771976225753908737969",
    certified_digits=40,
    route_agreement_digits=45,
    branch_convention="CPV",
    exact_gates=["weighted_residue=4", "Phi2(128,10976)=0"],
)
check("A10 constant pin records branch convention, digit floor, and stable digest",
      pin["ok"]
      and pin["value"]["status"] == "certified"
      and pin["value"]["digest"] == call_arith_constant_pin(
          name="dual_cpv_demo",
          value="-3.98800108597455809771976225753908737969",
          certified_digits=40,
          route_agreement_digits=45,
          branch_convention="CPV",
          exact_gates=["weighted_residue=4", "Phi2(128,10976)=0"],
      )["value"]["digest"])

check("A11 arithmetic tools are exposed as an independent MCP profile",
      "arithmetic" in TOOL_GROUPS
      and set(TOOL_GROUPS["arithmetic"]) == {
          "cella_help",
          "cella_arith_refine",
          "cella_arith_precision_budget",
          "cella_elliptic_legendre_reduce",
          "cella_third_kind_cpv",
          "cella_residue_branch_gate",
          "cella_carlson_period_referee",
          "cella_two_route_compare",
          "cella_period_curve_invariants",
          "cella_period_quartic",
          "cella_period_third_kind_residue",
          "cella_period_normal_form",
          "cella_period_route_compare",
          "cella_period_gap_report",
          "cella_dbp_relative_period",
          "cella_dbp_certificate_verify",
          "cella_legendre_ke_enclose",
          "cella_legendre_pinning",
          "cella_dbp_landen_trace_verify",
          "cella_dbp_release_receipt",
          "cella_pslq_field_referee",
          "cella_arith_constant_pin",
      }
      and all(name in TOOL_NAMES for name in TOOL_GROUPS["arithmetic"]))

print()
if FAILS:
    print(f"GATE MCP ARITHMETIC: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE MCP ARITHMETIC: CLOSED — arithmetic certification arm is MCP-callable.")
sys.exit(0)
