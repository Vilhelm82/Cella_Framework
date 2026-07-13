"""Gate MCP residual profiler.

The residual profiler is the Cella preflight layer: it inspects an expression
shape before expensive arithmetic and routes the work toward the cleaner
formulation when cancellation texture is visible.

Run:  python tests/gate_mcp_residual_profile.py
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
        CellaRouter,
        TOOL_GROUPS,
        TOOL_NAMES,
        call_cella_help,
        call_residual_profile,
    )
except Exception as exc:  # expected RED before implementation
    print(f"GATE MCP RESIDUAL PROFILE: OPEN - import failed: {exc}")
    sys.exit(1)


def profile(expression, low="1e-12", high="1e-4"):
    return call_residual_profile(
        expression=expression,
        sweep={"variable": "eps", "low": low, "high": high},
        n_samples=9,
    )


direct = profile("sqrt(eps)")
check("R1 no-subtraction expressions stay on the direct sparse route",
      direct["ok"]
      and direct["value"]["operation_shape"] == "no_subtraction"
      and direct["value"]["predicted_burden_vector"]["subtraction_sites"] == 0
      and direct["value"]["recommended_process"]["primary"] == "direct_or_symbolic_sparse")

self_cancel = profile("eps - eps")
check("R2 structural self-cancellation is detected without a probe burden",
      self_cancel["ok"]
      and self_cancel["value"]["operation_shape"] == "self_cancellation"
      and self_cancel["value"]["danger_sites"][0]["pattern"] == "self_cancellation"
      and self_cancel["value"]["danger_sites"][0]["probe_used"] is False)

linear = profile("(1 + eps) - 1")
check("R3 linear same-leading-constant subtraction is routed as catastrophic",
      linear["ok"]
      and linear["value"]["operation_shape"] == "catastrophic_cancellation"
      and linear["value"]["danger_sites"][0]["pattern"] == "sterbenz_safe_catastrophic"
      and linear["value"]["danger_sites"][0]["signal_exponent"] == "1"
      and linear["value"]["recommended_process"]["primary"] == "rewrite_before_evaluation")

sqrt_gap = profile("(1 + sqrt(eps)) - 1")
check("R4 square-root gap with same leading constant is benign and keeps exponent telemetry",
      sqrt_gap["ok"]
      and sqrt_gap["value"]["operation_shape"] == "benign_cancellation"
      and sqrt_gap["value"]["danger_sites"][0]["pattern"] == "sterbenz_safe_benign"
      and sqrt_gap["value"]["danger_sites"][0]["signal_exponent"] == "1/2"
      and sqrt_gap["value"]["predicted_burden_vector"]["benign_sites"] == 1)

buried_constant = profile("((12 + eps) * (12 + eps)) - 144")
check("R5 buried constants are exposed by the cheap expression-graph micro-probe",
      buried_constant["ok"]
      and buried_constant["value"]["operation_shape"] == "catastrophic_cancellation"
      and buried_constant["value"]["danger_sites"][0]["pattern"] == "sterbenz_safe_catastrophic"
      and buried_constant["value"]["danger_sites"][0]["probe_used"] is True
      and buried_constant["value"]["danger_sites"][0]["chart_local_debug"]["left_leading_constant"] == 144.0
      and buried_constant["value"]["danger_sites"][0]["chart_local_debug"]["right_leading_constant"] == 144.0)

linear_perturb = linear["value"]["danger_sites"][0].get("operand_perturbation", {})
buried_perturb = buried_constant["value"]["danger_sites"][0].get("operand_perturbation", {})
check("R5b operand perturbation profiles expose route assembly without AST matching",
      linear_perturb.get("left", {}).get("exponent") == "1"
      and abs(linear_perturb.get("left", {}).get("signed_coefficient", 0.0) - 1.0) < 1e-6
      and linear_perturb.get("right", {}).get("exponent") == "zero"
      and buried_perturb.get("left", {}).get("exponent") == "1"
      and abs(buried_perturb.get("left", {}).get("signed_coefficient", 0.0) - 24.0) < 1e-4
      and buried_perturb.get("right", {}).get("exponent") == "zero")

linear_fit = linear_perturb.get("left", {}).get("fit_quality", {})
check("R5c residual profiler uses the Cella-native copied V4 slope diagnostic core",
      linear_fit.get("n_used") == 9
      and linear_fit.get("standard_error") is not None
      and linear_fit.get("log_f_min") is not None
      and linear_fit.get("log_f_max") is not None
      and linear_fit.get("expression_path") == "cella_signed_power_law_fit")

linear_sweep = linear_perturb.get("left", {}).get("sweep_signature", {})
linear_order = linear_perturb.get("left", {}).get("residual_order_evidence", {})
linear_derivative = linear_order.get("sweep_signature_derivative_flow", {})
check("R5d V4 sweep telemetry carries residual stats and preserves derivative-flow provenance",
      "residual_rms" in linear_fit
      and "residual_max_abs" in linear_fit
      and "residual_relative_rms" in linear_fit
      and "residual_rms" in linear_sweep
      and "residual_max_abs" in linear_sweep
      and "residual_relative_rms" in linear_sweep
      and linear_order.get("order_source") == "direct_residual_slope_flow_fallback"
      and linear_derivative.get("comparison_kind") == "sweep_signature_residual_order")

registered = call_cella_help("cella_residual_profile")
check("R6 residual profiler is documented but not exposed as a public chat profile tool",
      "cella_residual_profile" not in TOOL_NAMES
      and "pathfinder" not in TOOL_GROUPS
      and registered["ok"]
      and registered["value"]["tool"]["purpose"].startswith("Preflight an expression"))

router = CellaRouter(default_profile="clean")
blocked = router.call(
    "residual_profile",
    {"expression": "eps - eps", "sweep": {"variable": "eps", "low": "1e-12", "high": "1e-8"}},
)
sampled = call_residual_profile(
    expression="((12 + eps) * (12 + eps)) - 144",
    sweep={"variable": "eps", "low": "1e-12", "high": "1e-8"},
    n_samples=5,
    include_samples=True,
)
sample_site = sampled["value"]["danger_sites"][0] if sampled["ok"] else {}
check("R7 internal residual profiler exposes measured residual noise as first-class telemetry",
      not blocked["ok"]
      and blocked["error"]["token"] == "UNKNOWN_TOOL"
      and sampled["ok"]
      and sampled["number_type"] == "telemetry-record"
      and sampled["value"]["measured_artifact_contract"]["samples_included"] is True
      and isinstance(sample_site["probe_samples"][0]["difference"], float)
      and sample_site["signal_coefficient"] > 20.0)

first_account = sample_site["probe_samples"][0].get("exact_account", {})
check("R8 arithmetic probe samples carry the Cella exact float-account ledger when available",
      first_account.get("status") == "exact_q_account"
      and first_account.get("value_plus_account_equals_true_q") is True
      and first_account.get("difference_exact") != first_account.get("rounded_difference")
      and "rounding_residue" in first_account
      and "rounding_residue_ulps" in first_account)

print()
if FAILS:
    print(f"GATE MCP RESIDUAL PROFILE: OPEN ({len(FAILS)} failing)")
    sys.exit(1)
print("GATE MCP RESIDUAL PROFILE: CLOSED - residual profiler routes operation shape before expensive arithmetic.")
sys.exit(0)
