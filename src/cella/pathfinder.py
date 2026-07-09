"""Cella pathfinder route planning and conservative rewrite support."""

from __future__ import annotations

import ast
from fractions import Fraction

from .cleanliness import cleanliness_rank
from .residual_profile import residual_profile


def route_plan(
    expression: str,
    sweep: dict,
    constants: dict | None = None,
    include_profile: bool = False,
    include_samples: bool = False,
    domain: str | None = None,
    geometry: dict | None = None,
) -> dict:
    geometry_overlay = _geometry_overlay(domain, geometry)
    try:
        profile = residual_profile(
            str(expression),
            sweep,
            constants=constants or {},
            include_samples=include_samples,
        )
    except Exception as exc:
        fingerprint = _residual_fingerprint(
            expression=str(expression),
            operation_shape=None,
            dominant=None,
            sites=[],
            burden={},
            exact_account_coverage="none",
            rewrite_coverage={
                "catastrophic_site_count": 0,
                "rewriteable_catastrophic_site_count": 0,
                "unresolved_catastrophic_site_count": 0,
            },
            missing=[],
            decision="unsupported_shape",
            geometry_overlay=geometry_overlay,
            unsupported=str(exc),
        )
        out = {
            "expression": str(expression),
            "decision": "unsupported_shape",
            "why": f"Residual profile could not parse or probe the expression: {exc}",
            "operation_shape": None,
            "dominant_pattern": None,
            "residual_fingerprint": fingerprint,
            "exact_account_available": False,
            "blocking_inputs": {"unsupported": str(exc), "missing_constants": []},
            "next_tools": ["cella_help"],
            "route_confidence": "low",
            "profile_summary": {
                "catastrophic_site_count": 0,
                "rewriteable_catastrophic_site_count": 0,
                "unresolved_catastrophic_site_count": 0,
                "exact_account_coverage": "none",
            },
        }
        if geometry_overlay is not None:
            out["geometry_overlay"] = geometry_overlay
            out["next_tools"] = _merge_next_tools(out["next_tools"], geometry_overlay.get("next_tools", []))
        return out

    sites = list(profile.get("danger_sites", []))
    burden = dict(profile.get("predicted_burden_vector", {}))
    operation_shape = str(profile.get("operation_shape"))
    dominant = burden.get("dominant_pattern")
    missing = _missing_constants(sites)
    exact_account_coverage = _exact_account_coverage(sites, operation_shape)
    exact_account = exact_account_coverage in ("some", "all", "structural")
    rewrite_coverage = _catastrophic_rewrite_coverage(str(expression), sites)
    catastrophic_count = rewrite_coverage["catastrophic_site_count"]
    rewriteable_count = rewrite_coverage["rewriteable_catastrophic_site_count"]
    unresolved_count = rewrite_coverage["unresolved_catastrophic_site_count"]
    known_rewrite = catastrophic_count > 0 and unresolved_count == 0

    if missing:
        decision = "needs_declared_constants"
        why = "At least one subtraction site contains an unknown symbolic parameter."
        next_tools = ["cella_route_plan"]
        confidence = "high"
    elif operation_shape == "no_subtraction":
        decision = "direct_ok"
        why = "No subtraction site was detected."
        next_tools = ["cella_symbolic_rational", "cella_arith_precision_budget"]
        confidence = "high"
    elif operation_shape == "self_cancellation":
        decision = "collapse_symbolically"
        why = "A structural x-x site can be collapsed before arithmetic."
        next_tools = ["cella_symbolic_rational", "cella_symbolic_equal"]
        confidence = "high"
    elif operation_shape == "catastrophic_cancellation" and known_rewrite:
        decision = "rewrite_candidate_needed"
        why = "Every catastrophic same-leading-constant cancellation site has a conservative rewrite family."
        next_tools = ["cella_rewrite_candidates", "cella_pathfinder_compare"]
        confidence = "high" if exact_account_coverage in ("all", "structural") else "medium"
    elif operation_shape == "catastrophic_cancellation":
        decision = "precision_budget_needed"
        if rewriteable_count:
            why = "Some catastrophic sites have conservative rewrite families, but at least one catastrophic site remains unresolved."
            next_tools = [
                "cella_rewrite_candidates",
                "cella_arith_precision_budget",
                "cella_operand_residue_trace",
            ]
        else:
            why = "Catastrophic cancellation was detected but no conservative rewrite family was found."
            next_tools = ["cella_arith_precision_budget", "cella_operand_residue_trace"]
        confidence = "medium"
    elif operation_shape == "benign_cancellation":
        decision = "direct_ok"
        why = "Cancellation opens with a benign fractional signal; monitor BACL/account burden."
        next_tools = ["cella_bacl_pair", "cella_operand_residue_trace"]
        confidence = "medium"
    elif operation_shape == "partly_unrecognised":
        decision = "unsupported_shape"
        why = "At least one subtraction site could not be classified."
        next_tools = ["cella_operand_residue_trace", "cella_help"]
        confidence = "low"
    else:
        decision = "direct_ok"
        why = "No high-risk cancellation route was detected."
        next_tools = ["cella_arith_precision_budget"]
        confidence = "medium"

    fingerprint = _residual_fingerprint(
        expression=str(expression),
        operation_shape=operation_shape,
        dominant=dominant,
        sites=sites,
        burden=burden,
        exact_account_coverage=exact_account_coverage,
        rewrite_coverage=rewrite_coverage,
        missing=missing,
        decision=decision,
        geometry_overlay=geometry_overlay,
    )
    out = {
        "expression": str(expression),
        "decision": decision,
        "why": why,
        "operation_shape": operation_shape,
        "dominant_pattern": dominant,
        "residual_fingerprint": fingerprint,
        "exact_account_available": exact_account,
        "blocking_inputs": {"missing_constants": missing},
        "next_tools": next_tools,
        "route_confidence": confidence,
        "profile_summary": {
            "site_count": len(sites),
            "danger_sites": [
                {
                    "path": site.get("path"),
                    "pattern": site.get("pattern"),
                    "severity": site.get("severity"),
                    "signal_exponent": site.get("signal_exponent"),
                    "account_probe_status": site.get("account_probe_status"),
                    "unknown_parameters": site.get("unknown_parameters", []),
                }
                for site in sites
            ],
            "predicted_burden_vector": burden,
            "catastrophic_site_count": catastrophic_count,
            "rewriteable_catastrophic_site_count": rewriteable_count,
            "unresolved_catastrophic_site_count": unresolved_count,
            "exact_account_coverage": exact_account_coverage,
        },
    }
    if geometry_overlay is not None:
        out["geometry_overlay"] = geometry_overlay
        out["next_tools"] = _merge_next_tools(out["next_tools"], geometry_overlay.get("next_tools", []))
    if include_profile:
        out["profile"] = profile
    return out


def _residual_fingerprint(
    *,
    expression: str,
    operation_shape,
    dominant,
    sites: list[dict],
    burden: dict,
    exact_account_coverage: str,
    rewrite_coverage: dict,
    missing: list[str],
    decision: str,
    geometry_overlay: dict | None,
    unsupported: str | None = None,
) -> dict:
    local_shape = _local_shape_class(operation_shape, rewrite_coverage, missing)
    residual_order = _residual_order(sites)
    residual_order_evidence = _residual_order_evidence(sites, residual_order)
    scale_class = _residual_scale_class(sites, operation_shape, missing)
    account_status = _account_closure_status(exact_account_coverage)
    domain_stratum = _domain_refusal_stratum(missing, decision, geometry_overlay, unsupported)
    canonical_cross_form = _canonical_cross_form(
        operation_shape=operation_shape,
        residual_order=residual_order,
        scale_class=scale_class,
        account_status=account_status,
        missing=missing,
        unsupported=unsupported,
    )
    fingerprint_id = (
        f"rfp:v1:{local_shape}:order={residual_order}:"
        f"account={account_status}:route={decision}"
    )
    root = _parse_expression_ast(expression)
    return {
        "fingerprint_id": fingerprint_id,
        "local_shape_class": local_shape,
        "residual_order": residual_order,
        "residual_order_evidence": residual_order_evidence,
        "residual_scale_class": scale_class,
        "account_closure_status": account_status,
        "burden_vector": dict(burden),
        "domain_refusal_stratum": domain_stratum,
        "required_route": decision,
        "canonical_cross_form": canonical_cross_form,
        "dominant_residual_pattern": dominant,
        "source_expression_role": "debug_metadata",
        "source_expression": expression,
        "engine_stack": _engine_stack_record(sites),
        "site_count": len(sites),
        "site_fingerprints": [_site_fingerprint(site, root) for site in sites],
        "route_contract": (
            "Residual fingerprint is the primary routing record; expression text is retained "
            "only as debug/source metadata until a route explicitly requests symbolic verification."
        ),
    }


def _engine_stack_record(sites: list[dict]) -> dict:
    order_sources = sorted({
        str((site.get("residual_order_evidence") or {}).get("order_source"))
        for site in sites
        if isinstance(site.get("residual_order_evidence"), dict)
        and (site.get("residual_order_evidence") or {}).get("order_source")
    })
    source_methods = [
        "typed_finite_difference",
        "sweep_signature_probe",
        "slope_flow_segment_model_matching",
        "executable_expression_graph_probe",
        "exact_q_float_account_probe",
        "bacl_refinery_cleanliness_ranking",
    ]
    return {
        "visibility": "internal_background_engine",
        "primary_record": "residual_fingerprint",
        "source_methods": source_methods,
        "order_sources": order_sources,
        "symbolic_verification_role": "secondary_only_when_required_route_demands_it",
        "public_mcp_policy": "not_exposed_as_a_tool_profile",
    }


def _canonical_cross_form(
    *,
    operation_shape,
    residual_order: str,
    scale_class: str,
    account_status: str,
    missing: list[str],
    unsupported: str | None,
) -> dict:
    shape = _canonical_shape_class(operation_shape, scale_class, missing, unsupported)
    canonical_id = f"rfp-canon:v1:{shape}:order={residual_order}:scale={scale_class}:account={account_status}"
    return {
        "canonical_fingerprint_id": canonical_id,
        "canonical_shape_class": shape,
        "canonicalization_level": "residual_texture_not_algebraic_identity",
        "canonicalized_fields": [
            "local_shape_class_family",
            "residual_order",
            "residual_scale_class",
            "account_closure_status",
        ],
        "noncanonical_axes": [
            "signal_coefficient",
            "route_assembly",
            "natural_ulp_scale",
            "common_mode_roundoff",
        ],
        "excluded_fields": [
            "source_expression",
            "source_ast_shape",
            "rewrite_visibility",
            "route_specific_candidate_coverage",
            "route_assembly",
            "signal_coefficient",
            "natural_ulp_scale",
            "common_mode_roundoff",
        ],
        "contract": (
            "Cross-form canonicalization groups residual texture only. It must not be read as "
            "algebraic identity, route-equivalence, shared ULP scale, or common-mode roundoff erasure."
        ),
    }


def _canonical_shape_class(operation_shape, scale_class: str, missing: list[str], unsupported: str | None) -> str:
    if missing:
        return "parameter_blocked_residual_texture"
    if unsupported or operation_shape is None:
        return "unsupported_residual_texture"
    if operation_shape == "catastrophic_cancellation" and scale_class == "same_leading_constant":
        return "same_leading_constant_catastrophic"
    if operation_shape == "benign_cancellation" and scale_class == "same_leading_constant":
        return "same_leading_constant_benign"
    if operation_shape == "self_cancellation":
        return "structural_zero_self_cancellation"
    if operation_shape == "no_subtraction":
        return "no_subtraction_direct_texture"
    if operation_shape == "partly_unrecognised":
        return "unrecognised_residual_texture"
    return "ordinary_subtraction_texture"


def _local_shape_class(operation_shape, rewrite_coverage: dict, missing: list[str]) -> str:
    if missing:
        return "parameter_blocked_residual_texture"
    if operation_shape is None:
        return "unsupported_residual_texture"
    if operation_shape == "no_subtraction":
        return "no_subtraction_direct_texture"
    if operation_shape == "self_cancellation":
        return "structural_zero_self_cancellation"
    if operation_shape == "catastrophic_cancellation":
        catastrophic = int(rewrite_coverage.get("catastrophic_site_count", 0))
        rewriteable = int(rewrite_coverage.get("rewriteable_catastrophic_site_count", 0))
        unresolved = int(rewrite_coverage.get("unresolved_catastrophic_site_count", 0))
        if catastrophic and unresolved == 0:
            return "same_leading_constant_catastrophic_rewriteable"
        if rewriteable:
            return "same_leading_constant_catastrophic_partly_rewriteable"
        return "same_leading_constant_catastrophic_unresolved"
    if operation_shape == "benign_cancellation":
        return "same_leading_constant_benign_fractional"
    if operation_shape == "partly_unrecognised":
        return "unrecognised_residual_texture"
    return "ordinary_subtraction_texture"


def _residual_order(sites: list[dict]) -> str:
    if not sites:
        return "none"
    orders = sorted({
        str(site.get("signal_exponent"))
        for site in sites
        if site.get("signal_exponent") is not None
    })
    if not orders:
        return "unknown"
    if len(orders) == 1:
        return orders[0]
    return "mixed:" + ",".join(orders)


def _residual_order_evidence(sites: list[dict], residual_order: str) -> dict:
    evidences = [
        site.get("residual_order_evidence")
        for site in sites
        if isinstance(site.get("residual_order_evidence"), dict)
    ]
    if not evidences:
        return {
            "status": "SLOPE_FLOW_NOT_APPLICABLE",
            "selected_model_name": None,
            "selected_order": residual_order,
            "reported_order": residual_order,
            "order_stability": "none" if residual_order == "none" else "indeterminate",
            "segment_evidence": [],
            "site_count": len(sites),
            "comparison_kind": "residual_order",
        }
    if len(evidences) == 1:
        out = dict(evidences[0])
        out["site_count"] = len(sites)
        out.setdefault("reported_order", residual_order)
        return out
    selected_orders = sorted({
        str(evidence.get("selected_order") or evidence.get("reported_order"))
        for evidence in evidences
        if evidence.get("selected_order") is not None or evidence.get("reported_order") is not None
    })
    stable = len(selected_orders) == 1 and all(
        evidence.get("order_stability") == "stable_model_match" for evidence in evidences
    )
    return {
        "status": "SLOPE_FLOW_MULTI_SITE_STABLE" if stable else "SLOPE_FLOW_MULTI_SITE_MIXED",
        "selected_model_name": evidences[0].get("selected_model_name") if stable else None,
        "selected_order": selected_orders[0] if stable else residual_order,
        "reported_order": residual_order,
        "order_stability": "stable_model_match" if stable else "mixed_site_orders",
        "segment_evidence": [],
        "site_evidence": evidences,
        "site_count": len(sites),
        "comparison_kind": "residual_order",
    }


def _residual_scale_class(sites: list[dict], operation_shape, missing: list[str]) -> str:
    if missing:
        return "parameter_blocked"
    if operation_shape is None:
        return "unsupported"
    if not sites:
        return "no_subtraction"
    patterns = {str(site.get("pattern")) for site in sites}
    if patterns == {"self_cancellation"}:
        return "structural_zero"
    if "unrecognised" in patterns:
        return "probe_unavailable"
    if "zero_base_cancellation" in patterns:
        return "zero_base"
    if patterns & {"sterbenz_safe_catastrophic", "sterbenz_safe_benign"}:
        return "same_leading_constant"
    return "scale_separated"


def _account_closure_status(exact_account_coverage: str) -> str:
    return {
        "structural": "structural_exact",
        "all": "all_exact_q_account",
        "some": "partial_exact_q_account",
        "none": "no_exact_account",
    }.get(str(exact_account_coverage), "unknown_account_status")


def _domain_refusal_stratum(
    missing: list[str],
    decision: str,
    geometry_overlay: dict | None,
    unsupported: str | None,
) -> str:
    if missing:
        return "unknown_parameters:" + ",".join(missing)
    if unsupported:
        return "unsupported_shape"
    if decision == "unsupported_shape":
        return "unrecognised_residual_texture"
    if geometry_overlay and geometry_overlay.get("regularity_status") == "q_zero_singular":
        return "q_zero_singular"
    return "none"


def _site_fingerprint(site: dict, root: ast.AST | None = None) -> dict:
    return {
        "path": site.get("path"),
        "local_shape_class": site.get("pattern"),
        "residual_order": site.get("signal_exponent"),
        "residual_order_evidence": site.get("residual_order_evidence"),
        "severity": site.get("severity"),
        "signal_coefficient": site.get("signal_coefficient"),
        "signal_signed_coefficient": site.get("signal_signed_coefficient"),
        "predicted_precision_crossing_epsilon": site.get("predicted_precision_crossing_epsilon"),
        "operand_perturbation": site.get("operand_perturbation"),
        "route_assembly_class": _route_assembly_class(site, root),
        "scale_evidence": {
            "chart_local": True,
            "anchor": site.get("chart_local_debug", {}).get("anchor", "x=0"),
            "left_leading_constant": site.get("chart_local_debug", {}).get("left_leading_constant"),
            "right_leading_constant": site.get("chart_local_debug", {}).get("right_leading_constant"),
            "leading_constant_gap": site.get("chart_local_debug", {}).get("leading_constant_gap"),
        },
        "account_probe_status": site.get("account_probe_status"),
        "unknown_parameters": site.get("unknown_parameters", []),
        "probe_used": bool(site.get("probe_used")),
    }


def _parse_expression_ast(expression: str) -> ast.AST | None:
    try:
        return ast.parse(str(expression), mode="eval").body
    except SyntaxError:
        return None


def _route_assembly_class(site: dict, root: ast.AST | None) -> str:
    if site.get("pattern") == "self_cancellation":
        return "structural_self_cancellation"
    residual_class = _route_assembly_class_from_residual(site)
    if residual_class is not None:
        return residual_class
    if root is None:
        return "unknown"
    node = _node_at_profile_path(root, site.get("path"))
    if node is None or not _is_subtraction(node):
        return "unknown"
    if _constant_offset_collapse_candidate(node) is not None:
        return "constant_offset_collapse"
    if _scaled_constant_offset_collapse_candidate(node) is not None:
        return "scaled_constant_offset_collapse"
    if _difference_of_squares_candidate(node) is not None:
        return "difference_of_squares"
    if _sqrt_conjugate_candidate(node) is not None:
        return "sqrt_conjugate"
    if _common_factor_candidate(node) is not None:
        return "common_factor_extraction"
    pattern = str(site.get("pattern") or "")
    if pattern == "non_cancelling_subtraction":
        return "ordinary_subtraction"
    if pattern in {"sterbenz_safe_catastrophic", "sterbenz_safe_benign"}:
        return "unclassified_same_leading_constant_subtraction"
    if pattern == "unrecognised":
        return "unrecognised_subtraction"
    return "unclassified_subtraction"


def _route_assembly_class_from_residual(site: dict) -> str | None:
    perturb = site.get("operand_perturbation")
    if not isinstance(perturb, dict):
        return None
    left = perturb.get("left") or {}
    right = perturb.get("right") or {}
    diff = perturb.get("difference") or {}
    if not left or not right or not diff:
        return None

    left_stationary = _is_stationary_perturbation(left)
    right_stationary = _is_stationary_perturbation(right)
    if left_stationary and right_stationary:
        return "stationary_operands"

    same_constant = site.get("chart_local_debug", {}).get("leading_constant_gap") == 0.0
    if not same_constant:
        return None

    if left_stationary != right_stationary:
        active = right if left_stationary else left
        active_order = str(active.get("exponent"))
        diff_order = str(diff.get("exponent"))
        if active_order != diff_order:
            return "one_sided_mixed_order_subtraction"
        coeff = abs(float(active.get("signed_coefficient") or active.get("coefficient") or 0.0))
        if _near(coeff, 1.0, rel=1.0e-6, abs_tol=1.0e-9):
            return "constant_offset_collapse"
        return "scaled_constant_offset_collapse"

    left_order = str(left.get("exponent"))
    right_order = str(right.get("exponent"))
    if left_order != right_order:
        return "mixed_order_operand_subtraction"

    left_coeff = abs(float(left.get("signed_coefficient") or left.get("coefficient") or 0.0))
    right_coeff = abs(float(right.get("signed_coefficient") or right.get("coefficient") or 0.0))
    diff_coeff = abs(float(diff.get("signed_coefficient") or diff.get("coefficient") or 0.0))
    if max(left_coeff, right_coeff) > 0.0 and diff_coeff <= 0.1 * max(left_coeff, right_coeff):
        return "matched_perturbation_cancellation"
    return "two_sided_same_order_subtraction"


def _is_stationary_perturbation(profile: dict) -> bool:
    exponent = profile.get("exponent")
    coefficient = abs(float(profile.get("coefficient") or 0.0))
    return exponent in (None, "zero", "0") or coefficient <= 1.0e-15


def _near(a: float, b: float, *, rel: float, abs_tol: float) -> bool:
    return abs(a - b) <= max(abs_tol, rel * max(abs(a), abs(b), 1.0))


def _merge_next_tools(primary: list[str], extra: list[str]) -> list[str]:
    out = []
    for item in list(primary) + list(extra):
        if item and item not in out:
            out.append(item)
    return out


def _geometry_overlay(domain: str | None, geometry: dict | None) -> dict | None:
    if domain is None and not geometry:
        return None

    context = dict(geometry or {})
    domain_key = _norm_key(domain or context.get("domain") or "generic_pathfinder")
    case = _norm_key(context.get("case") or context.get("metric_case") or context.get("divisor") or "")

    out = {
        "domain": domain_key,
        "authority": "generic_pathfinder",
        "route_status": "open_successor",
        "channel_predicate": _string_or_none(context.get("channel_predicate")),
        "regularity_status": "unknown",
        "local_germ_kind": "unknown",
        "shape_resolution": "not_applicable",
        "next_tools": [],
        "warnings": [],
        "notes": [],
    }

    if _is_inverse_metric_domain(domain_key):
        out["authority"] = "lead7_kn"
        out["route_status"] = "paper_local_form"
        _apply_inverse_metric_overlay(out, context, case)
    elif _is_dbp_domain(domain_key):
        out["authority"] = "dbp_standing_results"
        out["route_status"] = "standing_canonical"
        if case in ("stage_c_pin_move", "three_channel_kg", "c001"):
            out["authority"] = "c001_eval"
            out["route_status"] = "eval_tier"
        _apply_dbp_overlay(out, context, case)
    else:
        out["notes"].append("No specialized domain overlay matched; arithmetic Pathfinder rules still apply.")

    return out


def _norm_key(value) -> str:
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def _string_or_none(value) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text else None


def _is_dbp_domain(domain_key: str) -> bool:
    return domain_key in {
        "dbp",
        "three_channel_kg",
        "c001",
        "dbp_standing",
        "role_pair_carrier",
        "rolechspec",
    }


def _is_inverse_metric_domain(domain_key: str) -> bool:
    return domain_key in {
        "inverse_channel_metric",
        "kn",
        "kerr_newman",
        "lead7",
        "pfc",
        "thermodynamic_metric",
    }


def _apply_dbp_overlay(out: dict, context: dict, case: str) -> None:
    _apply_stage_c_channel_rule(out, context, case)
    _apply_regularity_rule(out, context)
    _apply_quantity_rule(out, context)
    _apply_shape_rule(out, context)
    if out["next_tools"]:
        return
    if out["channel_predicate"] == "delta_kappa_c":
        out["next_tools"].extend(["cella_gauge_channel_transport", "cella_three_channel_referee"])


def _apply_stage_c_channel_rule(out: dict, context: dict, case: str) -> None:
    declared = _norm_key(context.get("pin_move_predicate") or context.get("channel_predicate") or "")
    if case == "stage_c_pin_move":
        out["channel_predicate"] = "delta_kappa_c"
        out["notes"].append("Stage C pin/move predicates are keyed to the coupling channel, not the whole channel tuple.")
        out["next_tools"].extend(["cella_gauge_channel_transport", "cella_three_channel_referee"])
        if declared in {"whole_vector", "whole_vector_equality", "full_channel_tuple", "channel_tuple"}:
            out["warnings"].append("whole_vector_predicate_superseded")


def _apply_regularity_rule(out: dict, context: dict) -> None:
    if "regularity_g" not in context:
        return
    try:
        g = tuple(_q(v) for v in context["regularity_g"])
    except (TypeError, ValueError):
        out["regularity_status"] = "unknown"
        out["warnings"].append("regularity_g_not_exact_rational")
        return
    q = sum(v * v for v in g)
    out["regularity"] = {
        "g": [_fraction_text(v) for v in g],
        "q": _fraction_text(q),
        "rule": "refuse only when q=g^Tg is zero",
    }
    if q == 0:
        out["regularity_status"] = "q_zero_singular"
        out["warnings"].append("true_singular_locus_q_zero")
        return
    out["regularity_status"] = "regular"
    if any(v == 0 for v in g):
        out["notes"].append("single_g_i_zero_is_not_singular_when_q_nonzero")


def _apply_quantity_rule(out: dict, context: dict) -> None:
    if "quantity" not in context and not _is_dbp_domain(out["domain"]):
        return
    out["quantity_definitions"] = {
        "squared_total_KG": "K_G^2",
        "channel_norm_sq": "kappa_c^2 + kappa_s^2 + kappa_int^2",
    }
    quantity = _norm_key(context.get("quantity") or "")
    if quantity in {"kappa_squared", "kappa^2", "kappa2", "kappa_sq"}:
        out["warnings"].append("ambiguous_kappa_squared")
        out["notes"].append("Name squared-total and channel-norm quantities separately before ranking or comparing.")


def _apply_shape_rule(out: dict, context: dict) -> None:
    if "n" not in context:
        return
    try:
        n = _integer(context["n"])
    except (TypeError, ValueError):
        out["shape_resolution"] = "unknown"
        out["warnings"].append("n_not_integral")
        return
    out["n"] = str(n)
    out["carrier"] = "M^(n-2,2) = C[C(n,2)]"
    out["loss_shape"] = "S^(n-2,2)"
    if n <= 4:
        out["shape_resolution"] = "scalar_spectrum_sufficient"
    else:
        out["shape_resolution"] = "carrier_required"
        out["next_tools"].extend(["cella_role_pair_loss_diagnostic", "cella_rolechspec_n3"])


def _apply_inverse_metric_overlay(out: dict, context: dict, case: str) -> None:
    out["metric_assembly"] = "mass_role_inverse_sum_u0"
    out["role_role_policy"] = "omit_as_channel_isotropy_diagnostic"
    out["graph_normalization_required"] = True
    out["next_tools"].extend(["cella_metric_candidate_selector", "cella_kn_metric_builder"])
    out["notes"].append("Route by local valuation data before assembling a global scalar-curvature expression.")

    if case in {"reflection_face", "spin_reflection", "charge_reflection", "omega_0", "phi_e_0", "omega", "phi_e"}:
        m = _safe_integer(context.get("m", 2), default=2)
        B = str(context.get("B", "B"))
        out["authority"] = "pfc_normal_forms"
        out["local_germ_kind"] = "parity_fixed"
        out["local_law"] = {
            "kind": "parity_fixed",
            "order": "4",
            "coefficient_text": f"-{m * (m + 5)}/({B})",
            "law": "R = -m(m+5)/B * x^-4 + O(x^-2)",
        }
        out["next_tools"].extend(["cella_diag_germ_classifier", "cella_local_pole_law"])
    elif case in {"extremal_face", "extremal", "t_0", "t"}:
        out["authority"] = "pfc_normal_forms"
        out["local_germ_kind"] = "generic_quadratic"
        out["local_law"] = {
            "kind": "generic_quadratic",
            "order": "3",
            "coefficient_text": "A^-1 * sum_alpha d_x log(P_alpha)|_0",
            "law": "R = (1/A) * sum(P_alpha1/P_alpha0) * x^-3 + O(x^-2)",
        }
        out["next_tools"].extend(["cella_diag_germ_classifier", "cella_role_divisor_retrodict"])
    elif case in {"double_reflection_corner", "schwarzschild_corner", "corner"}:
        out["authority"] = "pfc_normal_forms"
        out["local_germ_kind"] = "corner_newton_wedge"
        out["corner_law"] = {
            "kind": "codimension_2_newton_wedge",
            "support": "support function of nonzero polar vertices",
            "warning": "not a superposition of the two single-face laws",
        }
        out["next_tools"].extend(["cella_corner_frontface", "cella_corner_newton"])


def _q(value) -> Fraction:
    if isinstance(value, bool):
        raise TypeError("booleans are not exact rationals")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        return Fraction(value.strip())
    raise TypeError(f"expected exact rational string/integer, got {type(value).__name__}")


def _integer(value) -> int:
    q = _q(value)
    if q.denominator != 1:
        raise ValueError(f"expected integer, got {q}")
    return q.numerator


def _safe_integer(value, default: int) -> int:
    try:
        return _integer(value)
    except (TypeError, ValueError):
        return default


def _fraction_text(value: Fraction) -> str:
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _exact_account_coverage(sites: list[dict], operation_shape: str) -> str:
    if operation_shape == "self_cancellation":
        return "structural"
    if not sites:
        return "none"

    statuses = [site.get("account_probe_status") for site in sites]
    if all(status == "structural_exact" for status in statuses):
        return "structural"
    if all(status in ("exact_q_account", "structural_exact") for status in statuses):
        return "all"
    if any(status in ("exact_q_account", "structural_exact") for status in statuses):
        return "some"
    return "none"


def _missing_constants(sites: list[dict]) -> list[str]:
    missing = set()
    for site in sites:
        if _site_needs_declared_constants(site):
            for name in site.get("unknown_parameters", []) or []:
                if name:
                    missing.add(str(name))
        text = str(site.get("probe_error", ""))
        marker = "unknown parameter "
        if marker in text:
            name = text.split(marker, 1)[1].split(";", 1)[0].strip().strip("'\"")
            if name:
                missing.add(name)
    return sorted(missing)


def _site_needs_declared_constants(site: dict) -> bool:
    return (
        site.get("account_probe_status") == "unavailable"
        or site.get("pattern") == "unrecognised"
        or site.get("severity") == "needs_empirical_refinery"
    )


def _catastrophic_rewrite_coverage(expression: str, sites: list[dict]) -> dict:
    catastrophic_sites = [site for site in sites if _is_catastrophic_site(site)]
    catastrophic_count = len(catastrophic_sites)
    rewriteable_count = 0

    try:
        root = ast.parse(str(expression), mode="eval").body
    except SyntaxError:
        return {
            "catastrophic_site_count": catastrophic_count,
            "rewriteable_catastrophic_site_count": 0,
            "unresolved_catastrophic_site_count": catastrophic_count,
        }

    for site in catastrophic_sites:
        node = _node_at_profile_path(root, site.get("path"))
        if node is not None and _has_known_rewrite_family(node):
            rewriteable_count += 1

    return {
        "catastrophic_site_count": catastrophic_count,
        "rewriteable_catastrophic_site_count": rewriteable_count,
        "unresolved_catastrophic_site_count": catastrophic_count - rewriteable_count,
    }


def _has_known_rewrite_family(node: ast.AST) -> bool:
    if not _is_subtraction(node):
        return False
    return (
        _constant_offset_collapse_candidate(node) is not None
        or _scaled_constant_offset_collapse_candidate(node) is not None
        or _difference_of_squares_candidate(node) is not None
        or _sqrt_conjugate_candidate(node) is not None
        or _common_factor_candidate(node) is not None
    )


def _is_catastrophic_site(site: dict) -> bool:
    return (
        site.get("severity") == "catastrophic"
        or site.get("pattern") == "sterbenz_safe_catastrophic"
    )


def _is_subtraction(node: ast.AST) -> bool:
    return isinstance(node, ast.BinOp) and isinstance(node.op, ast.Sub)


def _node_at_profile_path(root: ast.AST, path: object) -> ast.AST | None:
    if not isinstance(path, str) or not path.startswith("root"):
        return None
    node = root
    for part in path.split(".")[1:]:
        if part == "left" and isinstance(node, ast.BinOp):
            node = node.left
        elif part == "right" and isinstance(node, ast.BinOp):
            node = node.right
        elif part == "arg":
            if isinstance(node, ast.UnaryOp):
                node = node.operand
            elif isinstance(node, ast.Call) and node.args:
                node = node.args[0]
            else:
                return None
        else:
            return None
    return node


def _constant_value(node: ast.AST) -> int | float | None:
    if (
        isinstance(node, ast.Constant)
        and isinstance(node.value, (int, float))
        and not isinstance(node.value, bool)
    ):
        return node.value
    return None


def rewrite_candidates(
    expression: str,
    route_plan_record: dict | None = None,
    sweep: dict | None = None,
    constants: dict | None = None,
) -> dict:
    original = str(expression)
    candidates: list[dict] = []
    not_generated: list[dict] = []
    try:
        tree = ast.parse(original, mode="eval").body
    except SyntaxError as exc:
        return {
            "original": original,
            "route_decision": None if route_plan_record is None else route_plan_record.get("decision"),
            "candidates": [],
            "requires_ranking": False,
            "not_generated": [{"family": "parse", "reason": str(exc)}],
        }

    _add_unique(candidates, _self_collapse_candidate(tree))
    _add_unique(candidates, _constant_offset_collapse_candidate(tree))
    _add_unique(candidates, _scaled_constant_offset_collapse_candidate(tree))
    _add_unique(candidates, _difference_of_squares_candidate(tree))
    _add_unique(candidates, _sqrt_conjugate_candidate(tree))
    _add_unique(candidates, _common_factor_candidate(tree))
    for candidate in _three_term_regroup_candidates(tree):
        _add_unique(candidates, candidate)

    for family in (
        "self_collapse",
        "constant_offset_collapse",
        "scaled_constant_offset_collapse",
        "difference_of_squares",
        "sqrt_conjugate",
        "common_factor_extraction",
        "three_term_regroup",
    ):
        if not any(c["family"] == family for c in candidates):
            not_generated.append({"family": family, "reason": "pattern_not_visible"})

    return {
        "original": original,
        "route_decision": None if route_plan_record is None else route_plan_record.get("decision"),
        "candidates": candidates,
        "requires_ranking": any(c["family"] != "self_collapse" for c in candidates),
        "not_generated": not_generated,
    }


def _add_unique(candidates: list[dict], candidate: dict | None) -> None:
    if candidate is None:
        return
    if any(c["family"] == candidate["family"] and c["expression"] == candidate["expression"] for c in candidates):
        return
    candidates.append(candidate)


def _source(node: ast.AST) -> str:
    return ast.unparse(node)


def _same_ast(a: ast.AST, b: ast.AST) -> bool:
    return ast.dump(a, include_attributes=False) == ast.dump(b, include_attributes=False)


def _self_collapse_candidate(node: ast.AST) -> dict | None:
    if _is_subtraction(node) and _same_ast(node.left, node.right):
        return {
            "name": "self_collapse_zero",
            "expression": "0",
            "family": "self_collapse",
            "reason": "The subtraction operands are structurally identical.",
            "risk": "low",
        }
    return None


def _constant_offset_collapse_candidate(node: ast.AST) -> dict | None:
    if not _is_subtraction(node):
        return None
    if not isinstance(node.left, ast.BinOp) or not isinstance(node.left.op, ast.Add):
        return None
    if _same_ast(node.left.left, node.right):
        residual = _source(node.left.right)
    elif _same_ast(node.left.right, node.right):
        residual = _source(node.left.left)
    else:
        return None
    return {
        "name": "constant_offset_collapse",
        "expression": residual,
        "family": "constant_offset_collapse",
        "reason": "Visible (c+x)-c structure; expose the residual carrier directly.",
        "risk": "low",
    }


def _constant_ast_fraction(node: ast.AST) -> Fraction | None:
    value = _constant_value(node)
    if value is not None:
        return Fraction(str(value))
    if isinstance(node, ast.UnaryOp):
        child = _constant_ast_fraction(node.operand)
        if child is None:
            return None
        if isinstance(node.op, ast.USub):
            return -child
        if isinstance(node.op, ast.UAdd):
            return child
        return None
    if isinstance(node, ast.BinOp):
        left = _constant_ast_fraction(node.left)
        right = _constant_ast_fraction(node.right)
        if left is None or right is None:
            return None
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            if right == 0:
                return None
            return left / right
    return None


def _constant_factor_split(node: ast.AST) -> tuple[Fraction, ast.AST, ast.AST] | None:
    if not isinstance(node, ast.BinOp) or not isinstance(node.op, ast.Mult):
        return None
    left = _constant_ast_fraction(node.left)
    if left is not None:
        return left, node.left, node.right
    right = _constant_ast_fraction(node.right)
    if right is not None:
        return right, node.right, node.left
    return None


def _add_constant_residual(node: ast.AST, target_constant: Fraction) -> ast.AST | None:
    if not isinstance(node, ast.BinOp) or not isinstance(node.op, ast.Add):
        return None
    left = _constant_ast_fraction(node.left)
    if left == target_constant:
        return node.right
    right = _constant_ast_fraction(node.right)
    if right == target_constant:
        return node.left
    return None


def _scaled_constant_offset_collapse_candidate(node: ast.AST) -> dict | None:
    if not _is_subtraction(node):
        return None
    split = _constant_factor_split(node.left)
    if split is None:
        return None
    factor_value, factor_node, inner = split
    right_value = _constant_ast_fraction(node.right)
    if right_value is None or factor_value == 0:
        return None
    residual = _add_constant_residual(inner, right_value / factor_value)
    if residual is None:
        return None
    factor = _source(factor_node)
    carrier = _source(residual)
    return {
        "name": "scaled_constant_offset_collapse",
        "expression": f"({factor}) * ({carrier})",
        "family": "scaled_constant_offset_collapse",
        "reason": "Residual fingerprint exposes k*(c+x)-k*c; route directly to the scaled residual carrier.",
        "risk": "low",
    }


def _is_square_product(node: ast.AST) -> ast.AST | None:
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult) and _same_ast(node.left, node.right):
        return node.left
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
        if isinstance(node.right, ast.Constant) and node.right.value == 2:
            return node.left
    return None


def _sqrt_int_constant(node: ast.AST) -> int | None:
    value = _constant_value(node)
    if value is None or value < 0:
        return None
    root = int(round(float(value) ** 0.5))
    if root * root == value:
        return root
    return None


def _difference_of_squares_candidate(node: ast.AST) -> dict | None:
    if not _is_subtraction(node):
        return None
    left_base = _is_square_product(node.left)
    if left_base is None:
        return None

    right_base = _is_square_product(node.right)
    right_root = _sqrt_int_constant(node.right)
    if right_base is not None:
        other = _source(right_base)
    elif right_root is not None:
        other = str(right_root)
    else:
        return None

    base = _source(left_base)
    return {
        "name": "difference_of_squares",
        "expression": f"(({base}) - ({other})) * (({base}) + ({other}))",
        "family": "difference_of_squares",
        "reason": "Visible a^2-b^2 structure.",
        "risk": "medium",
    }


def _sqrt_call_arg(node: ast.AST) -> ast.AST | None:
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "sqrt"
        and len(node.args) == 1
    ):
        return node.args[0]
    return None


def _split_one_plus_x(node: ast.AST) -> ast.AST | None:
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        if isinstance(node.left, ast.Constant) and node.left.value == 1:
            return node.right
        if isinstance(node.right, ast.Constant) and node.right.value == 1:
            return node.left
    return None


def _sqrt_conjugate_candidate(node: ast.AST) -> dict | None:
    if not _is_subtraction(node):
        return None
    left_arg = _sqrt_call_arg(node.left)
    if left_arg is not None and isinstance(node.right, ast.Constant) and node.right.value == 1:
        residual = _split_one_plus_x(left_arg)
        numerator = _source(residual) if residual is not None else f"({_source(left_arg)}) - 1"
        inner = _source(left_arg)
        return {
            "name": "sqrt_conjugate",
            "expression": f"({numerator}) / (sqrt({inner}) + 1)",
            "family": "sqrt_conjugate",
            "reason": "Conjugate removes same-leading-constant subtraction.",
            "risk": "medium",
        }

    right_arg = _sqrt_call_arg(node.right)
    if right_arg is not None and isinstance(node.left, ast.Constant) and node.left.value == 1:
        residual = _split_one_minus_x(right_arg)
        numerator = _source(residual) if residual is not None else f"1 - ({_source(right_arg)})"
        inner = _source(right_arg)
        return {
            "name": "sqrt_conjugate",
            "expression": f"({numerator}) / (1 + sqrt({inner}))",
            "family": "sqrt_conjugate",
            "reason": "Conjugate removes same-leading-constant subtraction.",
            "risk": "medium",
        }
    return None


def _split_one_minus_x(node: ast.AST) -> ast.AST | None:
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Sub):
        if isinstance(node.left, ast.Constant) and node.left.value == 1:
            return node.right
    return None


def _product_factors(node: ast.AST) -> tuple[ast.AST, ast.AST] | None:
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
        return node.left, node.right
    return None


def _common_factor_candidate(node: ast.AST) -> dict | None:
    if not _is_subtraction(node):
        return None
    left = _product_factors(node.left)
    right = _product_factors(node.right)
    if left is None or right is None:
        return None

    pairs = (
        (left[0], left[1], right[0], right[1]),
        (left[0], left[1], right[1], right[0]),
        (left[1], left[0], right[0], right[1]),
        (left[1], left[0], right[1], right[0]),
    )
    for factor, left_other, right_factor, right_other in pairs:
        if _same_ast(factor, right_factor):
            f = _source(factor)
            a = _source(left_other)
            b = _source(right_other)
            return {
                "name": "common_factor_extraction",
                "expression": f"({f}) * (({a}) - ({b}))",
                "family": "common_factor_extraction",
                "reason": "Visible u*c-v*c structure; factor the shared operand before subtracting.",
                "risk": "medium",
            }
    return None


def _flatten_add(node: ast.AST) -> list[ast.AST]:
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _flatten_add(node.left) + _flatten_add(node.right)
    return [node]


def _three_term_regroup_candidates(node: ast.AST) -> list[dict]:
    terms = _flatten_add(node)
    if len(terms) != 3:
        return []
    a, b, c = [_source(t) for t in terms]
    return [
        {
            "name": "pair_0_1_then_2",
            "expression": f"(({a}) + ({b})) + ({c})",
            "family": "three_term_regroup",
            "reason": "Pair-first additive regrouping for BACL ranking.",
            "risk": "low",
        },
        {
            "name": "pair_0_2_then_1",
            "expression": f"(({a}) + ({c})) + ({b})",
            "family": "three_term_regroup",
            "reason": "Pair-first additive regrouping for BACL ranking.",
            "risk": "low",
        },
        {
            "name": "pair_1_2_then_0",
            "expression": f"(({b}) + ({c})) + ({a})",
            "family": "three_term_regroup",
            "reason": "Pair-first additive regrouping for BACL ranking.",
            "risk": "low",
        },
    ]


def pathfinder_compare(
    variables: list,
    forms: list[dict],
    grid: dict,
    dimensions: list[str] | None = None,
) -> dict:
    ranking = cleanliness_rank(
        [str(v) for v in variables],
        forms,
        grid,
        dimensions=None if dimensions is None else [str(d) for d in dimensions],
    )
    winner = ranking["dial_origin"]
    return {
        "winner": winner,
        "ranking": {
            "pareto_frontier": ranking["pareto_frontier"],
            "dominated": ranking["dominated"],
            "dominated_by": ranking["dominated_by"],
            "pairwise_comparisons": ranking["pairwise_comparisons"],
        },
        "burden_vectors": ranking["burden_vectors"],
        "equivalence_status": ranking["sample_equivalence"],
        "trace_examples": ranking["trace_examples"],
        "decision_reason": (
            "Winner selected by declared-grid exact equivalence, BACL lattice burden, "
            "rounding residual ulps, final residual ulps, operation depth, and stable tie-break."
        ),
        "winner_burden": ranking["burden_vectors"][winner],
        "next_tools": ["cella_operand_residue_trace", "cella_refinery_compare"],
        "scope": "declared_grid_only",
    }
