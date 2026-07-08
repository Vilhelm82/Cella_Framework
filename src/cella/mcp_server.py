"""MCP adapter for the Cella exact geometry core.

This module is deliberately thin: it parses exact JSON-ish inputs, calls the
existing Cella primitives, and returns certificate-shaped JSON records. The
mathematics stays in ``carrier.py``, ``tower.py``, and ``sensors.py``.

Run as an MCP stdio server:

    PYTHONPATH=src python3 -m cella.mcp_server
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

from .arithmetic import (
    arith_constant_pin,
    arith_precision_budget,
    arith_refine,
    carlson_period_referee,
    elliptic_legendre_reduce,
    period_curve_invariants,
    pslq_field_referee,
    residue_branch_gate,
    third_kind_cpv,
    two_route_compare,
)
from .carrier import as_labeled, carrier, channels_n3_crosscheck
from .campaign import (
    corner_frontface,
    diag_germ_classifier,
    implicit_gaussian_curvature,
    kn_metric_builder,
    metric_candidate_selector,
    positive_factor_certificate,
    role_divisor_retrodict,
)
from .cell import Cell
from .certificate import emit
from .cleanliness import (
    bacl_dial,
    bacl_pair,
    cleanliness_rank,
    operand_residue_trace,
    refinery_compare,
)
from .jet import ConstraintBlock, Jet2
from .periods import (
    period_gap_report,
    period_normal_form,
    period_quartic,
    period_route_compare,
    third_kind_residue,
)
from .pathfinder import pathfinder_compare, rewrite_candidates, route_plan
from .proofs import (
    corner_newton,
    local_pole_law,
    shifted_polynomial_certificate,
    sturm_positive_on_open_ray,
    surface_jet,
)
from .qsqrt import QSqrt
from .reference_lift import (
    curvature_orbit_spectrum,
    gauge_channel_transport,
    role_jet_orbit,
    role_pair_loss_diagnostic,
    rolechspec_n3,
    shadow_law,
    three_channel_referee,
    wreath_law,
)
from .refusal import Refusal
from .residual_profile import residual_profile
from .sensors import (
    fingerprint,
    localization,
    numerator_tower,
    shape_moment,
)
from .symbolic import (
    symbolic_channel_sum,
    symbolic_equal,
    symbolic_gauge_carrier,
    symbolic_pole_law,
    symbolic_rational,
    symbolic_valuation,
)
from .tower import sigma_tower

SCHEMA = "cella-mcp-v1"

TOOL_NAMES = (
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
    "cella_corner_newton",
    "cella_corner_frontface",
    "cella_curvature_orbit_spectrum",
    "cella_diag_germ_classifier",
    "cella_fingerprint",
    "cella_gauge_channel_transport",
    "cella_implicit_gaussian_curvature",
    "cella_kn_metric_builder",
    "cella_elliptic_legendre_reduce",
    "cella_local_pole_law",
    "cella_metric_candidate_selector",
    "cella_operand_residue_trace",
    "cella_period_curve_invariants",
    "cella_period_gap_report",
    "cella_period_normal_form",
    "cella_period_quartic",
    "cella_period_route_compare",
    "cella_period_third_kind_residue",
    "cella_poly_certificate",
    "cella_positive_factor_certificate",
    "cella_pslq_field_referee",
    "cella_refinery_compare",
    "cella_residue_branch_gate",
    "cella_role_jet_orbit",
    "cella_role_pair_loss_diagnostic",
    "cella_role_divisor_retrodict",
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
)

ROUTER_TOOL_NAMES = (
    "cella_profiles",
    "cella_use_profile",
    "cella_tools",
    "cella_json_export",
    "cella_call",
)

TOOL_GROUPS = {
    "all": TOOL_NAMES,
    "core": (
        "cella_help",
        "cella_surface_jet",
        "cella_carrier",
        "cella_sigma_tower",
        "cella_channels_n3",
        "cella_sensor",
        "cella_fingerprint",
        "cella_implicit_gaussian_curvature",
    ),
    "proof": (
        "cella_help",
        "cella_local_pole_law",
        "cella_corner_newton",
        "cella_poly_certificate",
        "cella_sturm_positive",
        "cella_positive_factor_certificate",
    ),
    "symbolic": (
        "cella_help",
        "cella_symbolic_rational",
        "cella_symbolic_equal",
        "cella_symbolic_pole_law",
        "cella_symbolic_gauge_carrier",
        "cella_symbolic_channel_sum",
        "cella_symbolic_valuation",
    ),
    "clean": (
        "cella_help",
        "cella_bacl_pair",
        "cella_operand_residue_trace",
        "cella_refinery_compare",
        "cella_cleanliness_rank",
        "cella_bacl_dial",
    ),
    "campaign": (
        "cella_help",
        "cella_diag_germ_classifier",
        "cella_role_divisor_retrodict",
        "cella_corner_frontface",
        "cella_positive_factor_certificate",
        "cella_metric_candidate_selector",
        "cella_kn_metric_builder",
        "cella_implicit_gaussian_curvature",
    ),
    "reference": (
        "cella_help",
        "cella_role_jet_orbit",
        "cella_curvature_orbit_spectrum",
        "cella_three_channel_referee",
        "cella_gauge_channel_transport",
        "cella_rolechspec_n3",
        "cella_role_pair_loss_diagnostic",
        "cella_shadow_law",
        "cella_wreath_law",
    ),
    "arithmetic": (
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
        "cella_pslq_field_referee",
        "cella_arith_constant_pin",
    ),
}

_PROFILE_ALIASES = {
    "geometry": "core",
    "local": "core",
    "arith": "arithmetic",
    "numeric": "arithmetic",
    "numerical": "arithmetic",
    "bacl": "clean",
    "cleanliness": "clean",
    "refinery": "clean",
    "residual": "clean",
    "profiler": "clean",
    "path": "clean",
    "pathfinding": "clean",
    "ref": "reference",
    "reference-lift": "reference",
    "reference_lift": "reference",
}


def normalize_profile(profile: str | None) -> str:
    key = "all" if profile is None else str(profile).strip().lower().replace("_", "-")
    key = _PROFILE_ALIASES.get(key, key)
    if key not in TOOL_GROUPS:
        raise ValueError(f"unknown Cella MCP profile {profile!r}; choose one of {sorted(TOOL_GROUPS)}")
    return key


def tool_names_for_profile(profile: str | None) -> tuple[str, ...]:
    return TOOL_GROUPS[normalize_profile(profile)]


def available_profiles_for_tool(tool_name: str) -> dict:
    canonical = normalize_tool_name(tool_name)
    return {
        name: list(names)
        for name, names in TOOL_GROUPS.items()
        if canonical in names
    }


def normalize_tool_name(tool_name: str) -> str:
    key = str(tool_name).strip()
    if key in TOOL_NAMES:
        return key
    if not key.startswith("cella_"):
        prefixed = f"cella_{key}"
        if prefixed in TOOL_NAMES:
            return prefixed
    return key

_SENSORS = {
    "fingerprint": fingerprint,
    "localization": localization,
    "numerator_tower": numerator_tower,
    "shape_moment": shape_moment,
}

_RESULT_CONTRACT = {
    "ok": "True means value is usable. False means read refusal/refusals; do not treat value as a number.",
    "value": "The certified payload. Exact numbers are serialized as integer or rational strings.",
    "number_type": "Q, Q(sqrt q), mixed, none, or proof-record.",
    "account": "Cella accounting residue metadata for certificate-shaped outputs.",
    "refusal": "Primary typed refusal when a geometric stratum is unsupported or singular.",
    "refusals": "All refusals emitted by the tool.",
    "rerun_digest": "Double-run certificate digest. Equal reruns should produce the same digest.",
    "plain": "Human-readable certificate summary.",
}

_SPARSE_RECORD_GUIDE = {
    "variables": "Ordered symbol basis. Exponent vectors follow this order.",
    "numerator": "Sparse numerator terms as [coefficient_string, exponent_vector].",
    "denominator": "Sparse denominator terms as [coefficient_string, exponent_vector].",
    "terms": "Sparse polynomial terms as [coefficient_string, exponent_vector].",
    "text": "Display form only. Use term tables and equality certificates for verdicts.",
    "is_zero": "Exact zero verdict over the sparse polynomial/rational record.",
}

_HELP_TOOLS = {
    "cella_help": {
        "purpose": "Explain the Cella MCP tools, expected inputs, and result fields.",
        "proper_use": "Call with no topic for the whole guide, or topic='tool_name' for one tool.",
        "read_result": "The value contains result_contract, sparse_record_guide, and tool entries.",
    },
    "cella_arith_refine": {
        "purpose": "Resolve a sequence of rational enclosures by exact endpoint rounding, Ziv-style.",
        "inputs": "required_bits, enclosures [{working_bits, lo, hi}], optional ceiling.",
        "proper_use": "Use when a numerical evaluator can provide rational enclosures at increasing working precision.",
        "read_result": "status is refined_correctly_rounded or refined_budget_exceeded; value is an exact dyadic rational when resolved.",
    },
    "cella_arith_precision_budget": {
        "purpose": "Compute a composition-floor precision budget and per-atom meetability verdicts.",
        "inputs": "output_bits, path_losses, format_bits, optional atoms with kind/budget_bits/format_bits.",
        "proper_use": "Use before high-precision comparisons to declare the required working floor instead of inventing tolerances.",
        "read_result": "composition_floor is output_bits plus losses; overall_verdict is proven/eval/unmeetable.",
    },
    "cella_elliptic_legendre_reduce": {
        "purpose": "Normalize Legendre elliptic third-kind inputs and block singular direct ellippi routes.",
        "inputs": "m and n as exact SymPy-compatible algebraic expressions.",
        "proper_use": "Use before any Pi(n;m) evaluation; if n>1, certify via a regular CPV transform, not direct ellippi.",
        "read_result": "singular_third_kind flags real-path poles; regular_parameter_q and identity name the admissible route.",
    },
    "cella_third_kind_cpv": {
        "purpose": "Certify a third-kind Cauchy-principal-value constant by independent contour and regular-transform routes.",
        "inputs": "m, n, scale, weight_pi, weight_k, dps, tolerance, contour_height.",
        "proper_use": "Use for dual/third-kind constants where singular-path special-function evaluation is unsafe.",
        "read_result": "routes_agree and achieved_decimal_digits name the certified floor; constant is scoped to that floor.",
    },
    "cella_residue_branch_gate": {
        "purpose": "Prove exact pole residue, weighted residue, antisymmetry, and branch-offset metadata.",
        "inputs": "m, n, prefactor for dx/((1-n*x^2)*y) on y^2=(1-x^2)(1-m*x^2).",
        "proper_use": "Use before trusting CPV branch conventions or continuation offsets.",
        "read_result": "weighted_residue_minpoly and offsets are exact symbolic gates.",
    },
    "cella_carlson_period_referee": {
        "purpose": "Independently gate elliptic period identities using Carlson RF formulas.",
        "inputs": "m_primary, m_dual, dps.",
        "proper_use": "Use as a route-independent period referee beside Legendre K/Pi identities.",
        "read_result": "digit fields report agreement floors for omega1, Im omega2, and rhombic Re omega2=omega1/2.",
    },
    "cella_two_route_compare": {
        "purpose": "Compare two independent high-precision route outputs and report the achieved decimal agreement floor.",
        "inputs": "route_a, route_b, requested_digits.",
        "proper_use": "Use to state how many digits are actually certified by route agreement.",
        "read_result": "certified_to_requested is true only when achieved_decimal_digits meets the declared request.",
    },
    "cella_period_curve_invariants": {
        "purpose": "Compute exact Legendre lambda, j-invariant, dual lambda, and Phi2 isogeny checks.",
        "inputs": "lambda_value and optional partner_j.",
        "proper_use": "Use to separate curve/isogeny structure from numerical period evaluation.",
        "read_result": "phi2_partner_zero certifies the degree-2 modular polynomial relation when partner_j is supplied.",
    },
    "cella_period_quartic": {
        "purpose": "Create a Cella-native exact elliptic quartic record without numeric evaluation.",
        "inputs": "kind='legendre_even', m as an exact rational.",
        "proper_use": "Use before reducing period routes so curve identity, branch squares, and j are explicit.",
        "read_result": "curve_id, branch_squares, coefficients, and j_invariant are exact; gaps name unsupported layers.",
    },
    "cella_period_third_kind_residue": {
        "purpose": "Compute exact third-kind pole residues and branch-jump coefficients on a native Legendre quartic.",
        "inputs": "curve {kind:'legendre_even', m}, n, prefactor as exact rationals.",
        "proper_use": "Use before any CPV route to make pole signs and indentation jumps explicit.",
        "read_result": "positive_x_residue and jump coefficients may live in Q(sqrt q); residue_antisymmetry should be true.",
    },
    "cella_period_normal_form": {
        "purpose": "Reduce supported period routes into exact K/Pi basis terms plus residue-jump metadata.",
        "inputs": "kind='third_kind_cpv' with curve,n,scale,weight_pi,weight_k; or kind='declared_basis' with basis_terms.",
        "proper_use": "Use to compare routes structurally before asking for decimal evaluation.",
        "read_result": "basis_terms is the verdict payload; numeric_evaluation is intentionally None in this native spike.",
    },
    "cella_period_route_compare": {
        "purpose": "Compare two Cella period normal forms by exact basis-term subtraction.",
        "inputs": "route_a and route_b as period-normal-form records.",
        "proper_use": "Use to prove two routes agree structurally or expose the exact period-basis mismatch.",
        "read_result": "equivalent True means the structural normal forms cancel; first_gap explains mismatches.",
    },
    "cella_period_gap_report": {
        "purpose": "Report the explicit open gaps for the native period/residue spike.",
        "inputs": "optional scope string.",
        "proper_use": "Use after a spike result to decide the next implementation target.",
        "read_result": "gaps are ordered by ROI: native evaluation, algebraic fields, differential reduction, raw K_G route.",
    },
    "cella_pslq_field_referee": {
        "purpose": "Search for bounded linear relations over a declared algebraic basis without overclaiming independence.",
        "inputs": "value, basis list, max_coeff.",
        "proper_use": "Use for paper-side relation hunting over fields such as Q(2^(1/4)); negative results are bounded only.",
        "read_result": "relation_found and coefficients give an exact bounded relation, or a scoped no-relation warning.",
    },
    "cella_arith_constant_pin": {
        "purpose": "Record a certified arithmetic constant with branch convention, digit floor, exact gates, and stable digest.",
        "inputs": "name, value, certified_digits, route_agreement_digits, branch_convention, exact_gates.",
        "proper_use": "Use when a chat session needs a reusable constant receipt rather than a loose decimal string.",
        "read_result": "status is certified only when route_agreement_digits covers certified_digits; digest is stable for the record.",
    },
    "cella_bacl_pair": {
        "purpose": "Expose the BACL integer-lattice law for one binary64 additive/subtractive pair.",
        "inputs": "a and b as binary64 declarations: hex floats are best; decimal, integer, rational strings, and JSON floats are accepted as operational binary64 inputs.",
        "proper_use": "Use when asking whether a-b lies on the clean integer lattice measured in ulp(b).",
        "read_result": "theorem_protected means ulp(a) >= ulp(b) and the lattice index is integer; integer_residual gives the off-lattice distance to the nearest integer cell.",
        "pitfalls": "This is an IEEE operational diagnostic, not an exact symbolic identity proof.",
    },
    "cella_operand_residue_trace": {
        "purpose": "Trace a restricted arithmetic expression over binary64 while carrying exact rational residues for every operation.",
        "inputs": "expression, variables, values. Supported operations: +, -, *, /, and integer powers.",
        "proper_use": "Use to see where an operand chain introduces roundoff and where additive BACL cleanliness is lost.",
        "read_result": "entries list per-operation exact_result, rounded_result, rounding_residual_ulps, and bacl_pair for additive/subtractive ops; diagnostics aggregates lattice and roundoff burden.",
    },
    "cella_refinery_compare": {
        "purpose": "Compare two same-geometry burden vectors by the refinery componentwise Pareto law.",
        "inputs": "reference and candidate records with name, geometry, and burden dictionaries; optional dimensions.",
        "proper_use": "Use after producing or declaring burden vectors for equivalent algebraic forms.",
        "read_result": "accepted means same geometry, no worse dimensions, and at least one candidate_better dimension.",
    },
    "cella_cleanliness_rank": {
        "purpose": "Rank algebraically equivalent binary64 forms by BACL lattice burden and refinery Pareto comparison.",
        "inputs": "variables, forms [{name, expression}], grid {variable: [binary64 declarations]}, optional dimensions.",
        "proper_use": "Use for the mature 'which algebraic configuration is operationally cleanest?' workflow.",
        "read_result": "dial_origin is the lexicographic BACL-clean choice; pareto_frontier is the componentwise Pareto frontier; dominated maps each form to forms it strictly improves.",
        "pitfalls": "It ranks the declared forms over the declared grid. It does not invent arbitrary algebraic identities.",
    },
    "cella_bacl_dial": {
        "purpose": "Generate the three pair-first configurations of a 3-term constraint and rank them by BACL cleanliness.",
        "inputs": "variables, exactly three terms [{label, expression}], and a grid.",
        "proper_use": "Use when the forms should emerge from absorption order rather than a hand-picked catalogue.",
        "read_result": "generated_forms shows the three pair-first forms; dial_origin_pair names the first pair that gives the cleanest lattice burden.",
    },
    "cella_residual_profile": {
        "purpose": "Preflight an expression graph to identify cancellation shape and route the computation before expensive arithmetic.",
        "inputs": "expression string; sweep {variable, low, high} or explicit positive points; optional n_samples, constants, and include_samples.",
        "proper_use": "Use before mpmath/SymPy-style expansion or high-precision evaluation to detect no-subtraction, self-cancellation, benign fractional gaps, catastrophic same-leading-constant subtraction, and buried constants.",
        "read_result": "operation_shape is the route label; danger_sites names each subtraction texture; predicted_burden_vector aggregates counts; measured floats are first-class residual/noise telemetry, not exact verdicts.",
        "pitfalls": "This is a fast pathfinder over a restricted one-variable expression graph. Unknown symbolic parameters need constants or a later symbolic/asymptotic arm.",
    },
    "cella_route_plan": {
        "purpose": "Emit the primary residual fingerprint for one expression and choose the next Cella process before expansion, high precision, or manual algebra.",
        "inputs": "expression string; sweep {variable, low, high} or explicit positive points; optional constants, include_profile, include_samples, domain, and geometry.",
        "proper_use": "Use this as the primary Pathfinder call. Read residual_fingerprint first; call symbolic tools only when required_route asks for symbolic verification or rewrite proof.",
        "read_result": "residual_fingerprint is the primary record: fingerprint_id, local_shape_class, residual_order, residual_scale_class, account_closure_status, burden_vector, domain_refusal_stratum, required_route, and canonical_cross_form. next_tools lists follow-up tools for that route. decision/operation_shape/profile_summary remain compatibility and evidence fields; expression text is debug metadata.",
        "pitfalls": "This is a residual-shape router, not a CAS simplifier. rewrite_candidate_needed means ask for candidates; precision_budget_needed means at least one catastrophic fingerprint has no conservative rewrite yet. geometry_overlay is process routing metadata; use the named campaign/proof tools for exact records.",
    },
    "cella_rewrite_candidates": {
        "purpose": "Emit conservative algebraic rewrite candidates for cancellation-shaped expressions.",
        "inputs": "expression string; optional route_plan, sweep, and constants.",
        "proper_use": "Call when cella_route_plan returns rewrite_candidate_needed, or when inspecting a known local cancellation form.",
        "read_result": "candidates lists small rewrite records with family, expression, reason, and risk; requires_ranking says to compare original and candidates before using one.",
        "pitfalls": "Candidates are syntactic and conservative. They are not global simplification proofs; rank or prove the selected form before paper use.",
    },
    "cella_pathfinder_compare": {
        "purpose": "Rank declared equivalent forms by exact-account, BACL, and refinery burden over a declared binary64 grid.",
        "inputs": "variables, forms [{name, expression}], grid {variable: [binary64 declarations]}, optional dimensions.",
        "proper_use": "Use after rewrite candidates are emitted to decide which algebraic configuration is operationally cleaner.",
        "read_result": "winner is the selected form; equivalence_status scopes the comparison; burden_vectors and trace_examples show why.",
        "pitfalls": "The verdict is declared-grid scoped. It does not prove global symbolic equivalence.",
    },
    "cella_diag_germ_classifier": {
        "purpose": "Classify a local diagonal metric germ into PFC/LEAD7 normal forms.",
        "inputs": "coordinate, native leading/power/parity, and transverse channel leading powers or finite P0/P1 drift data.",
        "proper_use": "Use before any global scalar-curvature expansion to read parity_fixed, generic_quadratic, or flat collapsing-only structure.",
        "read_result": "kind gives parity_fixed/generic_quadratic/etc.; order and coefficient_text give the local Laurent law; proof_obligations list what must be checked.",
    },
    "cella_role_divisor_retrodict": {
        "purpose": "Build a complementarity retrodiction table from classified role divisors.",
        "inputs": "divisors with names and classifier records, plus optional expected_orders.",
        "proper_use": "Use to assemble a paper-native 3/4/4 or similar campaign table without expanding the global curvature.",
        "read_result": "table lists divisor, local_type, order, and coefficient; orders_match_expected checks the declared signature.",
    },
    "cella_corner_frontface": {
        "purpose": "Compute a richer codim-2 corner/front-face support certificate.",
        "inputs": "Either face_data p_x,p_y,r_x,r_y or raw weights p0,q0,p1,q1,p2,q2; optional path ax,ay.",
        "proper_use": "Use for Schwarzschild-style double corners, mixed front-face terms, and cancellation checks.",
        "read_result": "vertices, active_vertices, balanced_direction, support_order, active_frontface, and cancellation A/B describe the corner law.",
    },
    "cella_positive_factor_certificate": {
        "purpose": "Compose factorwise positivity proofs from coefficient-shift and Sturm certificates.",
        "inputs": "variables plus factors with terms and method coefficient_shift or sturm_open_ray.",
        "proper_use": "Use for extremal-gate sign proofs where some factors are coefficient-positive and others need Sturm.",
        "read_result": "positive True means every factor certificate is positive; inspect factors for method-specific proof records.",
    },
    "cella_metric_candidate_selector": {
        "purpose": "Select DBP metric candidates by campaign gates: n=2 reduction, positivity, boundary sensitivity, and interior cleanliness.",
        "inputs": "candidate records with booleans for n2_reduction, positive_definite, role_boundary_sensitive, interior_pole_free, optional graph_norm.",
        "proper_use": "Use to replace ad-hoc candidate comparison scripts for LEAD7-style metric selection.",
        "read_result": "selected is the unique candidate passing all gates; rejected candidates include precise reasons.",
    },
    "cella_kn_metric_builder": {
        "purpose": "Return the paper-native graph-normalized Kerr-Newman mass-role inverse-channel metric construction.",
        "inputs": "roles, assembly, graph_norm, u.",
        "proper_use": "Use to seed LEAD7 retrodiction workflows and avoid dropping the graph-normalization 1+ term.",
        "read_result": "components.G_i gives the formula, role_divisors gives support, warnings flag non-selected candidate choices.",
    },
    "cella_implicit_gaussian_curvature": {
        "purpose": "Exact bordered-Hessian Gaussian curvature referee for implicit surfaces in R^3.",
        "inputs": "gradient and symmetric Hessian as exact rationals.",
        "proper_use": "Use as the independent K_G total-curvature referee for exact surface jets.",
        "read_result": "K_G is -det([[H,g],[g^T,0]])/|g|^4 exactly; bordered_hessian_det exposes the numerator.",
    },
    "cella_role_jet_orbit": {
        "purpose": "Compute the exact active S3 role-transposition orbit for order-1, order-2, or order-3 graph jets.",
        "inputs": "order=1|2|3, jet=(a,b[,A,B,C[,E,F,G,H]]), optional exponents=(m,n).",
        "proper_use": "Use before claiming a local expression is role-invariant; active recharting is birational, not passive relabelling.",
        "read_result": "orbit lists exact transformed jets; group_laws pins s^2=t^2=(st)^3=e; first_projective_invariants and degree_spectrum are role-quotient diagnostics.",
    },
    "cella_curvature_orbit_spectrum": {
        "purpose": "Compute the six active graph-role curvature charts and their three output-role spectra.",
        "inputs": "graph_jet=(a,b,A,B,C) for P=f(D,S).",
        "proper_use": "Use to distinguish passive curvature covariance from active role recharting.",
        "read_result": "charts has six ordered readings; output_spectra has P/D/S; total_curvature_values should be a singleton.",
    },
    "cella_three_channel_referee": {
        "purpose": "Return the n=3 determinant partition Delta_c/Delta_s/Delta_m and labeled K_G channels.",
        "inputs": "gradient and symmetric Hessian for a regular implicit R^3 point.",
        "proper_use": "Use when you need deltas, bordered determinant, or mutation-trap metadata beyond cella_channels_n3.",
        "read_result": "channels are labeled; deltas sum to bordered_det; mutation_traps identify classic false simplifications.",
    },
    "cella_gauge_channel_transport": {
        "purpose": "Apply H -> H + g a^T + a g^T and report exact movement of the channel allocation.",
        "inputs": "gradient, hessian, and gauge vector a for n=3.",
        "proper_use": "Use to explain gauge motion, zero-sum channel residue, and single-edge pin/move behavior.",
        "read_result": "K_invariant and zero_sum_channel_shift should be true; single_edge names endpoint axes and opposite-axis kappa_c motion when applicable.",
    },
    "cella_rolechspec_n3": {
        "purpose": "Compute graph-chart RoleChSpec density records and recover the n=3 carrier O from r=1 coupling rows.",
        "inputs": "gradient plus hessian, or gradient plus carrier=[O12,O13,O23].",
        "proper_use": "Use instead of Groebner/equality-ideal work when checking RoleChSpec faithfulness in n=3.",
        "read_result": "recovery.recovered_O matching carrier_O is the linear injectivity certificate; charts expose r=1 and r=2 density pieces.",
    },
    "cella_role_pair_loss_diagnostic": {
        "purpose": "Report role-pair carrier dimensions, magnitude-summary loss, and the n=4 quotient / n>=5 faithful transition.",
        "inputs": "n>=3.",
        "proper_use": "Use to block the mistake that per-role magnitudes equal the full coupling carrier.",
        "read_result": "shape_dim is the discarded S^(n-2,2) content; shape_status tells absent, quotient, or faithful.",
    },
    "cella_shadow_law": {
        "purpose": "Compute the Johnson-shadow scalar and direction for the all-n triangle decomposition of the coupling form.",
        "inputs": "n and nonzero gradient vector.",
        "proper_use": "Use for the exact shadow law s(g)*((n-2)I-A1) without rebuilding projector scripts.",
        "read_result": "scalar_s is the average triangle weight; direction_eigenvalues are on triv/std/shape.",
    },
    "cella_wreath_law": {
        "purpose": "Return the closed gcd/wreath monodromy law for trinomial layers and self-glue product/directive covers.",
        "inputs": "kind='trinomial_layer' with m,k; or kind='self_glue_product'/'self_glue_directive' with m.",
        "proper_use": "Use for group-type/degree predictions before any numerical continuation run.",
        "read_result": "group and order expose cyclic-vs-symmetric wreath asymmetry; gcd types mixed trinomial layers.",
    },
    "cella_carrier": {
        "purpose": "Compute the gauge-normal carrier O for one exact codim-1 2-jet.",
        "inputs": "point, g, H as exact integer or rational strings. H is an n by n Hessian matrix.",
        "proper_use": "Use after you already have an exact jet. Gradient components must be nonzero.",
        "read_result": "value is the lexicographic upper-triangle O_ij list: O12, O13, ...",
        "pitfalls": "It is a point evaluator. For symbolic O_ij, use cella_symbolic_gauge_carrier.",
    },
    "cella_sigma_tower": {
        "purpose": "Compute the invariant sigma tower for one exact local jet.",
        "inputs": "point, g, H exact rationals.",
        "proper_use": "Use for parity-typed local invariants over Q or Q(sqrt q).",
        "read_result": "Even entries are rational strings; odd radical entries are QSqrt records.",
    },
    "cella_channels_n3": {
        "purpose": "Compute labeled n=3 channel cross-checks kc, kint, ks and K_G.",
        "inputs": "point, g, H exact rationals with exactly 3 variables.",
        "proper_use": "Use as the n=3 channel-account cross-check, not as the general carrier path.",
        "read_result": "value has labels kc, kint, ks, K_G. Do not read channel slots positionally.",
    },
    "cella_sensor": {
        "purpose": "Dispatch one named Cella sensor: fingerprint, localization, numerator_tower, shape_moment.",
        "inputs": "sensor name plus point, g, H exact rationals.",
        "proper_use": "Use when you need one sensor without calling the convenience wrapper.",
        "read_result": "value shape depends on the sensor; refusals name unsupported or singular strata.",
    },
    "cella_fingerprint": {
        "purpose": "Convenience wrapper for the n=3 role fingerprint sensor.",
        "inputs": "point, g, H exact rationals.",
        "proper_use": "Use for role fingerprinting and typed CHANNEL_ISOTROPIC refusals.",
        "read_result": "ok False with CHANNEL_ISOTROPIC is a meaningful stratum, not a crash.",
    },
    "cella_local_pole_law": {
        "purpose": "Exact numeric local pole laws for master_quadric, parity_fixed, and generic_quadratic germs.",
        "inputs": "Exact rational parameters: exponents/B, m/B, or A/transverse_P0/transverse_P1.",
        "proper_use": "Use when all units are exact rationals.",
        "read_result": "value gives order, coefficient, and the law formula as exact rationals.",
    },
    "cella_corner_newton": {
        "purpose": "Exact codim-2 corner Newton/support certificate from monomial weights.",
        "inputs": "weights p0,q0,p1,q1,p2,q2 and optional path weights ax,ay.",
        "proper_use": "Use for fixed numeric monomial-weight corners.",
        "read_result": "active_vertices and support_order identify polar leading support.",
    },
    "cella_poly_certificate": {
        "purpose": "Prove sparse polynomial positivity by exact coefficient nonnegativity after shifts.",
        "inputs": "variables, terms [coeff, powers], optional affine shifts.",
        "proper_use": "Use when coefficient nonnegativity on a positive orthant is the intended proof.",
        "read_result": "positive True is a certificate from the shifted sparse coefficients.",
    },
    "cella_sturm_positive": {
        "purpose": "Prove univariate polynomial positivity on an open ray by Sturm sequence.",
        "inputs": "variable, polynomial terms, lower endpoint.",
        "proper_use": "Use for one-variable positivity when coefficient tests are insufficient.",
        "read_result": "root_count 0 plus positive sample_value gives positive True.",
    },
    "cella_surface_jet": {
        "purpose": "Bridge a symbolic implicit surface and rational point into an exact gradient/Hessian jet.",
        "inputs": "expression, variables, point, require_on_surface.",
        "proper_use": "Use to avoid hand-transcribing Hessians before calling exact point tools.",
        "read_result": "value.jet contains point, g, H ready for carrier/sigma/channel tools.",
        "pitfalls": "Decimals and transcendental residuals are rejected. This is a jet bridge, not a CAS proof.",
    },
    "cella_symbolic_rational": {
        "purpose": "Parse an exact rational function into Cella sparse Q[variables] records.",
        "inputs": "expression string and ordered variables.",
        "proper_use": "Use to inspect support, denominators, and exact symbolic payloads.",
        "read_result": "value.expression has numerator/denominator sparse term tables and display text.",
    },
    "cella_symbolic_equal": {
        "purpose": "Decide rational-function equality by exact sparse cross-multiplication.",
        "inputs": "left, right, variables.",
        "proper_use": "Use for identities such as alternate forms of -14/B(S,Q,pi).",
        "read_result": "equal True iff cross_difference.is_zero is True. Inspect cross_difference when False.",
    },
    "cella_symbolic_pole_law": {
        "purpose": "Compute local pole-law coefficients over symbolic rational-function units.",
        "inputs": "kind, variables, plus exponents/B, m/B, or A/transverse_P0/transverse_P1.",
        "proper_use": "Use for symbolic coefficients like -14/B or C(p)/B(S,Q,pi).",
        "read_result": "coefficient is the sparse rational record; coefficient_text is display only.",
    },
    "cella_symbolic_gauge_carrier": {
        "purpose": "Compute O_ij over Q[variables] for symbolic g and H.",
        "inputs": "variables, g list, H matrix as rational-function strings.",
        "proper_use": "Use to keep gauge-normal algebra exact without hand-simplifying Hessians.",
        "read_result": "value.O contains labeled O12/O13/... sparse records and normal_form has zero diagonal.",
    },
    "cella_symbolic_channel_sum": {
        "purpose": "Sum symbolic channel expressions and optionally certify a target total.",
        "inputs": "variables, channels dict, optional expected_total.",
        "proper_use": "Use for channel-account identities and affine transport planes.",
        "read_result": "sum is a sparse rational record; sum_equals_expected is certified by cross_difference.",
    },
    "cella_symbolic_valuation": {
        "purpose": "Compute symbolic Newton/support valuations with unit coefficients and deletion walls.",
        "inputs": "coordinates, terms with labels/coefficient/powers, optional path, optional parameters.",
        "proper_use": "Use before curvature expansion to identify active polar support and coefficient walls.",
        "read_result": "active_terms, support_order, leading_terms, deletion_walls, and domain_walls describe the support proof obligations.",
    },
}


def exact_from_json(x):
    """Parse an exact scalar from JSON input.

    Accepted scalar forms are integers and strings accepted by Fraction, e.g.
    ``"3"``, ``"-1/49"``. Floats are rejected: a JSON float has already lost
    the exact declaration Cella needs.
    """
    if isinstance(x, bool):
        raise TypeError("booleans are not exact scalars")
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, str):
        return Fraction(x.strip())
    if isinstance(x, list):
        return tuple(exact_from_json(i) for i in x)
    if isinstance(x, tuple):
        return tuple(exact_from_json(i) for i in x)
    raise TypeError(f"expected exact integer or rational string, got {type(x).__name__}")


def exact_to_json(x):
    """Serialize Cella exact values without decimal loss."""
    if isinstance(x, bool):
        raise TypeError("boolean is not an exact Cella value")
    if isinstance(x, int):
        return str(x)
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, QSqrt):
        return {
            "type": "QSqrt",
            "a": exact_to_json(x.a),
            "b": exact_to_json(x.b),
            "r": exact_to_json(x.r),
        }
    if isinstance(x, Refusal):
        return refusal_to_json(x)
    if isinstance(x, tuple):
        return [exact_to_json(i) for i in x]
    if isinstance(x, list):
        return [exact_to_json(i) for i in x]
    if isinstance(x, dict):
        return {str(k): exact_to_json(v) for k, v in x.items()}
    if isinstance(x, (float, complex)):
        raise TypeError("float reached MCP serialization: forbidden on verdict paths")
    if x is None or isinstance(x, str):
        return x
    raise TypeError(f"cannot serialize {type(x).__name__}")


def proof_to_json(x):
    """Serialize proof records, including boolean metadata."""
    if isinstance(x, bool):
        return x
    if isinstance(x, dict):
        return {str(k): proof_to_json(v) for k, v in x.items()}
    if isinstance(x, tuple):
        return [proof_to_json(i) for i in x]
    if isinstance(x, list):
        return [proof_to_json(i) for i in x]
    return exact_to_json(x)


def refusal_to_json(ref: Refusal) -> dict:
    return {
        "token": ref.token,
        "stratum": ref.stratum,
        "plain": ref.plain(),
    }


def _block(point, g, H) -> ConstraintBlock:
    return ConstraintBlock([Jet2(exact_from_json(point), exact_from_json(g),
                                 exact_from_json(H))])


def _number_type(value) -> str:
    if value is None:
        return "none"
    if isinstance(value, QSqrt):
        return "Q(sqrt q)"
    if isinstance(value, Fraction):
        return "Q"
    if isinstance(value, tuple):
        parts = {_number_type(i) for i in value}
        if parts == {"Q"}:
            return "Q"
        if parts <= {"Q", "Q(sqrt q)"}:
            return "Q + Q(sqrt q)"
        return "mixed"
    if isinstance(value, dict):
        parts = {_number_type(i) for i in value.values()}
        if parts == {"Q"}:
            return "Q"
        if parts <= {"Q", "Q(sqrt q)"}:
            return "Q + Q(sqrt q)"
        return "mixed"
    return type(value).__name__


def _wrap_cell(tool: str, what: str, compute_cell, depends=()) -> dict:
    """Run a Cell computation under Cella's double-run certificate law."""

    def compute_record():
        cell = compute_cell()
        if cell.is_refusal():
            return {
                "value": None,
                "number_type": "none",
                "account": {"m": None, "r_epochs": ()},
                "refusals": [cell.residue],
            }
        return {
            "value": cell.value,
            "number_type": _number_type(cell.value),
            "account": {"m": cell.residue, "r_epochs": ()},
            "refusals": [],
        }

    cert = emit(what, compute_record, depends=depends)
    machine = cert.machine()
    raw = compute_record()
    refusals = raw["refusals"]
    refusal_json = [refusal_to_json(r) for r in refusals]
    return {
        "schema": SCHEMA,
        "tool": tool,
        "ok": not refusal_json,
        "what": machine["what"],
        "value": exact_to_json(raw["value"]),
        "number_type": raw["number_type"],
        "account": exact_to_json(raw["account"]),
        "refusal": refusal_json[0] if refusal_json else None,
        "refusals": refusal_json,
        "rerun_digest": machine["rerun_digest"],
        "plain": cert.plain(),
    }


def _wrap_proof(tool: str, what: str, compute_value, depends=()) -> dict:
    """Run an exact proof-record computation under the certificate law."""

    def compute_record():
        return {
            "value": compute_value(),
            "number_type": "proof-record",
            "account": {"m": Fraction(0), "r_epochs": ()},
            "refusals": [],
        }

    cert = emit(what, compute_record, depends=depends)
    machine = cert.machine()
    raw = compute_record()
    return {
        "schema": SCHEMA,
        "tool": tool,
        "ok": True,
        "what": machine["what"],
        "value": proof_to_json(raw["value"]),
        "number_type": raw["number_type"],
        "account": exact_to_json(raw["account"]),
        "refusal": None,
        "refusals": [],
        "rerun_digest": machine["rerun_digest"],
        "plain": cert.plain(),
    }


def telemetry_to_json(x):
    """Serialize operational telemetry; measured finite floats are allowed."""
    if isinstance(x, bool):
        return x
    if isinstance(x, int):
        return x
    if isinstance(x, float):
        if not (x == x and abs(x) != float("inf")):
            raise TypeError("non-finite float reached MCP telemetry serialization")
        return x
    if isinstance(x, Fraction):
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, QSqrt):
        return {
            "type": "QSqrt",
            "a": telemetry_to_json(x.a),
            "b": telemetry_to_json(x.b),
            "r": telemetry_to_json(x.r),
        }
    if isinstance(x, Refusal):
        return refusal_to_json(x)
    if isinstance(x, tuple):
        return [telemetry_to_json(i) for i in x]
    if isinstance(x, list):
        return [telemetry_to_json(i) for i in x]
    if isinstance(x, dict):
        return {str(k): telemetry_to_json(v) for k, v in x.items()}
    if x is None or isinstance(x, str):
        return x
    raise TypeError(f"cannot serialize telemetry {type(x).__name__}")


def _telemetry_digest(record: dict) -> str:
    blob = json.dumps(telemetry_to_json(record), sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def _wrap_telemetry(tool: str, what: str, compute_value, depends=()) -> dict:
    """Run a deterministic operational telemetry computation twice."""

    def compute_record():
        return {
            "value": compute_value(),
            "number_type": "telemetry-record",
            "account": {"m": "measured_artifact", "r_epochs": ()},
            "refusals": [],
        }

    raw1, raw2 = compute_record(), compute_record()
    d1, d2 = _telemetry_digest(raw1), _telemetry_digest(raw2)
    if d1 != d2:
        raise RuntimeError("double-run mismatch in operational telemetry")
    return {
        "schema": SCHEMA,
        "tool": tool,
        "ok": True,
        "what": what,
        "value": telemetry_to_json(raw1["value"]),
        "number_type": raw1["number_type"],
        "account": telemetry_to_json(raw1["account"]),
        "refusal": None,
        "refusals": [],
        "rerun_digest": d1,
        "plain": "\n".join([
            "WHAT WAS COMPUTED",
            f"  {what}",
            "",
            "HOW TO READ IT",
            "  This is operational telemetry: route labels are structural predictions; finite floats are measured probe artifacts.",
            "",
            "WHAT WOULD CHANGE THIS RESULT",
            *[f"  - {d}" for d in depends],
        ]),
    }


def call_carrier(point, g, H) -> dict:
    """Compute the gauge-normal carrier O from an exact order-2 jet."""
    return _wrap_cell(
        "cella_carrier",
        "Gauge-normal carrier O for one codim-1 exact jet.",
        lambda: carrier(_block(point, g, H)),
        depends=("Input point, gradient, and Hessian are exact rationals.",),
    )


def call_sigma_tower(point, g, H) -> dict:
    """Compute sigma_1..sigma_{n-1}, parity-typed over Q or Q(sqrt q)."""
    return _wrap_cell(
        "cella_sigma_tower",
        "Invariant sigma tower for one codim-1 exact jet.",
        lambda: sigma_tower(_block(point, g, H)),
        depends=("Input point, gradient, and Hessian are exact rationals.",),
    )


def call_channels_n3(point, g, H) -> dict:
    """Compute labeled n=3 channels kc, kint, ks and their exact total K_G."""
    out = _wrap_cell(
        "cella_channels_n3",
        "Labeled n=3 channel cross-check kc, kint, ks, and K_G.",
        lambda: channels_n3_crosscheck(_block(point, g, H)),
        depends=("Only n=3 is supported by this channel cross-check.",),
    )
    if out["ok"]:
        kc, kint, ks = out["value"]
        out["value"] = {"kc": kc, "kint": kint, "ks": ks, "K_G": exact_to_json(
            sum(channels_n3_crosscheck(_block(point, g, H)).value))}
    return out


def call_sensor(sensor: str, point, g, H) -> dict:
    """Compute one G1.2 Cella sensor by name."""
    if sensor not in _SENSORS:
        raise ValueError(f"unknown sensor {sensor!r}; choose one of {sorted(_SENSORS)}")
    return _wrap_cell(
        "cella_sensor",
        f"Cella sensor {sensor} for one codim-1 exact jet.",
        lambda: _SENSORS[sensor](_block(point, g, H)),
        depends=(f"Sensor selected: {sensor}.",),
    )


def call_fingerprint(point, g, H) -> dict:
    """Convenience wrapper for the n=3 role fingerprint sensor."""
    return call_sensor("fingerprint", point, g, H)


def call_local_pole_law(
    kind: str,
    m=None,
    B=None,
    A=None,
    transverse_P0=None,
    transverse_P1=None,
    exponents=None,
) -> dict:
    """Compute an exact local curvature pole law for a supported germ class."""
    if kind == "master_quadric":
        kwargs = {
            "exponents": exact_from_json(exponents),
            "B": Fraction(1) if B is None else exact_from_json(B),
        }
    elif kind == "parity_fixed":
        kwargs = {"m": exact_from_json(m), "B": exact_from_json(B)}
    elif kind == "generic_quadratic":
        kwargs = {
            "A": exact_from_json(A),
            "transverse_P0": exact_from_json(transverse_P0),
            "transverse_P1": exact_from_json(transverse_P1),
        }
    else:
        kwargs = {}
    return _wrap_proof(
        "cella_local_pole_law",
        f"Local curvature pole law for {kind}.",
        lambda: local_pole_law(kind, **kwargs),
        depends=("Supported germ classes: master_quadric, parity_fixed, generic_quadratic.",),
    )


def call_corner_newton(weights: dict, path: dict | None = None) -> dict:
    """Compute exact codim-2 corner Newton vertices and path support order."""
    weights_q = {str(k): exact_from_json(v) for k, v in weights.items()}
    path_q = None if path is None else {str(k): exact_from_json(v) for k, v in path.items()}
    return _wrap_proof(
        "cella_corner_newton",
        "Corner Newton/support certificate from inverse-channel monomial weights.",
        lambda: corner_newton(weights_q, path_q),
        depends=("Single-weight codimension-2 corner germ with spectator coordinate.",),
    )


def call_poly_certificate(variables: list, terms: list, shifts: dict | None = None) -> dict:
    """Prove sparse polynomial positivity by exact coefficient nonnegativity."""
    terms_q = [(exact_from_json(c), tuple(int(e) for e in p)) for c, p in terms]
    shifts_q = None
    if shifts is not None:
        shifts_q = {
            str(k): {"new": str(v["new"]), "offset": exact_from_json(v["offset"])}
            for k, v in shifts.items()
        }
    return _wrap_proof(
        "cella_poly_certificate",
        "Sparse polynomial coefficient-positivity certificate after exact shifts.",
        lambda: shifted_polynomial_certificate(tuple(str(v) for v in variables), terms_q, shifts_q),
        depends=("Strict positive orthant for the resulting variables.",),
    )


def call_sturm_positive(variable: str, terms: list, lower) -> dict:
    """Prove univariate polynomial positivity on (lower, infinity) by Sturm."""
    terms_q = [(exact_from_json(c), tuple(int(e) for e in p)) for c, p in terms]
    return _wrap_proof(
        "cella_sturm_positive",
        f"Univariate Sturm positivity certificate for {variable} on an open ray.",
        lambda: sturm_positive_on_open_ray(str(variable), terms_q, exact_from_json(lower)),
        depends=("Positive sign is certified on the open ray after the lower endpoint.",),
    )


def call_surface_jet(
    expression: str,
    variables: list,
    point: list,
    require_on_surface: bool = True,
) -> dict:
    """Build an exact rational gradient/Hessian jet from a symbolic implicit surface."""
    return _wrap_proof(
        "cella_surface_jet",
        "Exact symbolic surface-to-jet bridge at a rational point.",
        lambda: surface_jet(
            str(expression),
            [str(v) for v in variables],
            exact_from_json(point),
            bool(require_on_surface),
        ),
        depends=("SymPy differentiates the expression; Cella accepts only exact rational jet entries.",),
    )


def call_symbolic_rational(expression: str, variables: list) -> dict:
    """Parse an exact rational function into Cella sparse Q[variables] records."""
    return _wrap_proof(
        "cella_symbolic_rational",
        "Exact rational-function parse into Cella sparse symbolic records.",
        lambda: symbolic_rational(str(expression), [str(v) for v in variables]),
        depends=("Cella's native restricted AST front-end compiles directly into sparse Q[variables] records.",),
    )


def call_symbolic_equal(left: str, right: str, variables: list) -> dict:
    """Decide equality in Q[variables] by exact cross-multiplication."""
    return _wrap_proof(
        "cella_symbolic_equal",
        "Exact rational-function identity check by sparse cross-multiplication.",
        lambda: symbolic_equal(str(left), str(right), [str(v) for v in variables]),
        depends=("No numeric sampling; equality is the zero cross-difference polynomial.",),
    )


def call_symbolic_pole_law(
    kind: str,
    variables: list,
    m=None,
    B=None,
    A=None,
    transverse_P0=None,
    transverse_P1=None,
    exponents=None,
) -> dict:
    """Compute a supported local pole law over symbolic rational-function units."""
    return _wrap_proof(
        "cella_symbolic_pole_law",
        f"Symbolic rational-function local curvature pole law for {kind}.",
        lambda: symbolic_pole_law(
            str(kind),
            [str(v) for v in variables],
            m=m,
            B=B,
            A=A,
            transverse_P0=transverse_P0,
            transverse_P1=transverse_P1,
            exponents=exponents,
        ),
        depends=("Supported symbolic germ classes: master_quadric, parity_fixed, generic_quadratic.",),
    )


def call_symbolic_gauge_carrier(variables: list, g: list, H: list) -> dict:
    """Compute the gauge-normal carrier O over Q[variables]."""
    return _wrap_proof(
        "cella_symbolic_gauge_carrier",
        "Symbolic gauge-normal carrier O over an exact rational-function field.",
        lambda: symbolic_gauge_carrier([str(v) for v in variables], g, H),
        depends=("Gradient components are treated as nonzero chart units.",),
    )


def call_symbolic_channel_sum(variables: list, channels: dict, expected_total=None) -> dict:
    """Sum symbolic channel expressions and optionally certify a target total."""
    return _wrap_proof(
        "cella_symbolic_channel_sum",
        "Symbolic channel-account sum in exact rational-function form.",
        lambda: symbolic_channel_sum([str(v) for v in variables], channels, expected_total),
        depends=("This is the channel-account identity layer, not a geometric recomputation.",),
    )


def call_symbolic_valuation(
    coordinates: list,
    terms: list,
    path: dict | None = None,
    parameters: list | None = None,
) -> dict:
    """Compute symbolic Newton/support valuations with coefficient walls."""
    return _wrap_proof(
        "cella_symbolic_valuation",
        "Symbolic Newton/support valuation with exact unit-coefficient walls.",
        lambda: symbolic_valuation(
            [str(v) for v in coordinates],
            terms,
            path,
            None if parameters is None else [str(v) for v in parameters],
        ),
        depends=("Coefficient numerators define deletion walls; denominators define chart domain walls.",),
    )


def call_bacl_pair(a, b, precision: str = "binary64") -> dict:
    """Expose the binary64 BACL integer-lattice pair diagnostic."""
    return _wrap_proof(
        "cella_bacl_pair",
        "BACL binary64 integer-lattice diagnostic for a-b measured in ulp(b).",
        lambda: bacl_pair(a, b, str(precision)),
        depends=("Operational binary64 inputs are reported by exact hex and Fraction records.",),
    )


def call_operand_residue_trace(
    expression: str,
    variables: list,
    values,
    precision: str = "binary64",
) -> dict:
    """Trace exact rational roundoff residue through a binary64 operand chain."""
    return _wrap_proof(
        "cella_operand_residue_trace",
        "Exact residue and BACL cleanliness trace for one binary64 operand chain.",
        lambda: operand_residue_trace(str(expression), [str(v) for v in variables], values, str(precision)),
        depends=("Supported operations: +, -, *, /, and integer powers over binary64 inputs.",),
    )


def call_refinery_compare(reference: dict, candidate: dict, dimensions: list | None = None) -> dict:
    """Compare two burden vectors under the componentwise refinery decision law."""
    return _wrap_proof(
        "cella_refinery_compare",
        "Same-geometry componentwise refinery comparison of burden vectors.",
        lambda: refinery_compare(reference, candidate, dimensions=None if dimensions is None else [str(d) for d in dimensions]),
        depends=("Geometry dictionaries must match before burden reduction can be accepted.",),
    )


def call_cleanliness_rank(
    variables: list,
    forms: list,
    grid: dict,
    dimensions: list | None = None,
) -> dict:
    """Rank declared algebraic forms by BACL/refinery cleanliness burden."""
    return _wrap_proof(
        "cella_cleanliness_rank",
        "BACL/refinery cleanliness ranking for declared binary64 algebraic forms.",
        lambda: cleanliness_rank(
            [str(v) for v in variables],
            forms,
            grid,
            dimensions=None if dimensions is None else [str(d) for d in dimensions],
        ),
        depends=("Forms are ranked over the declared grid; no numeric sampling outside the grid is implied.",),
    )


def call_bacl_dial(
    variables: list,
    terms: list,
    grid: dict,
    dimensions: list | None = None,
) -> dict:
    """Generate pair-first forms for a three-term constraint and rank them."""
    return _wrap_proof(
        "cella_bacl_dial",
        "Three-term pair-first BACL absorption dial.",
        lambda: bacl_dial(
            [str(v) for v in variables],
            terms,
            grid,
            dimensions=None if dimensions is None else [str(d) for d in dimensions],
        ),
        depends=("Exactly three declared terms are combined by all pair-first absorption orders.",),
    )


def call_residual_profile(
    expression: str,
    sweep: dict,
    n_samples: int = 9,
    constants: dict | None = None,
    include_samples: bool = False,
) -> dict:
    """Preflight operation shape and route the expression before heavy arithmetic."""
    return _wrap_telemetry(
        "cella_residual_profile",
        "Residual-shape preflight over an expression graph before expensive arithmetic.",
        lambda: residual_profile(str(expression), sweep, int(n_samples), constants or {}, bool(include_samples)),
        depends=(
            "The profiler supports one sweep variable and a restricted arithmetic/function grammar.",
            "Measured floats are reference telemetry; route labels are predictions for the next Cella process.",
        ),
    )


def call_route_plan(
    expression: str,
    sweep: dict,
    constants: dict | None = None,
    include_profile: bool = False,
    include_samples: bool = False,
    domain: str | None = None,
    geometry: dict | None = None,
) -> dict:
    """Plan the next Cella route for one expression."""
    return _wrap_telemetry(
        "cella_route_plan",
        "Single-expression route plan from residual telemetry and conservative rewrite detection.",
        lambda: route_plan(
            str(expression),
            sweep,
            constants=constants or {},
            include_profile=bool(include_profile),
            include_samples=bool(include_samples),
            domain=domain,
            geometry=geometry or {},
        ),
        depends=(
            "The route plan inherits the residual profiler's one-variable expression grammar.",
            "next_tools is process guidance; it is not a proof that no better algebraic form exists.",
            "Declared DBP/inverse-channel domains add a geometry overlay that routes to existing campaign/proof tools.",
        ),
    )


def call_rewrite_candidates(
    expression: str,
    route_plan: dict | None = None,
    sweep: dict | None = None,
    constants: dict | None = None,
) -> dict:
    """Generate conservative rewrite candidates for one expression."""
    return _wrap_telemetry(
        "cella_rewrite_candidates",
        "Conservative syntactic rewrite candidates for cancellation-shaped expressions.",
        lambda: rewrite_candidates(
            str(expression),
            route_plan_record=route_plan,
            sweep=sweep,
            constants=constants or {},
        ),
        depends=(
            "Candidate generation is syntactic and intentionally conservative.",
            "Use cella_pathfinder_compare or cleanliness tools before adopting a candidate operationally.",
        ),
    )


def call_pathfinder_compare(
    variables: list,
    forms: list,
    grid: dict,
    dimensions: list | None = None,
) -> dict:
    """Rank declared forms by exact-account/BACL pathfinder burden."""
    what = "Pathfinder ranking for declared algebraic forms over a binary64 grid."
    try:
        return _wrap_proof(
            "cella_pathfinder_compare",
            what,
            lambda: pathfinder_compare(
                [str(v) for v in variables],
                forms,
                grid,
                dimensions=None if dimensions is None else [str(d) for d in dimensions],
            ),
            depends=("The comparison scope is the declared grid; it is not a global identity proof.",),
        )
    except ValueError as exc:
        refusal = Refusal("INDETERMINATE", "non_equivalent_declared_grid", str(exc))
        refusal_json = refusal_to_json(refusal)
        digest = _telemetry_digest({
            "tool": "cella_pathfinder_compare",
            "refusal": refusal_json,
            "variables": [str(v) for v in variables],
            "forms": forms,
            "grid": grid,
            "dimensions": dimensions,
        })
        return {
            "schema": SCHEMA,
            "tool": "cella_pathfinder_compare",
            "ok": False,
            "what": what,
            "value": None,
            "number_type": "proof-record",
            "account": {"m": "refusal", "r_epochs": []},
            "refusal": refusal_json,
            "refusals": [refusal_json],
            "rerun_digest": digest,
            "plain": refusal.plain(),
        }


def call_diag_germ_classifier(coordinate: str, native: dict, transverse: list) -> dict:
    """Classify a local diagonal metric germ by PFC/LEAD7 normal forms."""
    return _wrap_proof(
        "cella_diag_germ_classifier",
        "Paper-native local diagonal metric germ classifier.",
        lambda: diag_germ_classifier(str(coordinate), native, transverse),
        depends=("Supported campaign germs: parity-fixed inverse-channel, generic quadratic, and flat collapsing-only.",),
    )


def call_role_divisor_retrodict(divisors: list, expected_orders: dict | None = None) -> dict:
    """Build a role-divisor retrodiction table from local germ classifiers."""
    return _wrap_proof(
        "cella_role_divisor_retrodict",
        "Complementarity retrodiction table from local role-divisor germs.",
        lambda: role_divisor_retrodict(divisors, expected_orders),
        depends=("This is a local-normal-form table, not a global scalar-curvature expansion.",),
    )


def call_corner_frontface(
    face_data: dict | None = None,
    weights: dict | None = None,
    path: dict | None = None,
) -> dict:
    """Compute a codim-2 corner/front-face support certificate."""
    return _wrap_proof(
        "cella_corner_frontface",
        "Codimension-2 corner support, balanced direction, and front-face certificate.",
        lambda: corner_frontface(face_data=face_data, weights=weights, path=path),
        depends=("Provide exactly one of face_data or raw monomial weights.",),
    )


def call_positive_factor_certificate(variables: list, factors: list) -> dict:
    """Compose factorwise positivity certificates."""
    return _wrap_proof(
        "cella_positive_factor_certificate",
        "Factorwise positivity proof composer.",
        lambda: positive_factor_certificate([str(v) for v in variables], factors),
        depends=("Methods: coefficient_shift and sturm_open_ray.",),
    )


def call_metric_candidate_selector(candidates: list) -> dict:
    """Select metric candidates by DBP campaign canonicity gates."""
    return _wrap_proof(
        "cella_metric_candidate_selector",
        "DBP metric candidate selection by role-boundary and interior-cleanliness gates.",
        lambda: metric_candidate_selector(candidates),
        depends=("Candidate booleans are declared proof outcomes; this tool applies the selection law.",),
    )


def call_kn_metric_builder(
    roles: list | None = None,
    assembly: str = "mass_role_inverse_sum",
    graph_norm: bool = True,
    u="0",
) -> dict:
    """Return the Kerr-Newman graph-normalized mass-role inverse-channel metric record."""
    return _wrap_proof(
        "cella_kn_metric_builder",
        "LEAD7 Kerr-Newman metric construction record.",
        lambda: kn_metric_builder(
            None if roles is None else [str(v) for v in roles],
            str(assembly),
            bool(graph_norm),
            u,
        ),
        depends=("KN specialization for the current LEAD7 campaign surface.",),
    )


def call_implicit_gaussian_curvature(gradient: list, hessian: list) -> dict:
    """Compute the exact bordered-Hessian implicit Gaussian curvature scalar."""
    return _wrap_proof(
        "cella_implicit_gaussian_curvature",
        "Exact bordered-Hessian Gaussian curvature referee for an implicit R^3 surface.",
        lambda: implicit_gaussian_curvature(gradient, hessian),
        depends=("Gradient and Hessian must be exact rationals at a regular implicit surface point.",),
    )


def call_role_jet_orbit(order: int, jet: list, exponents: list | None = None) -> dict:
    """Compute exact active S3 role-jet orbits through order 3."""
    return _wrap_proof(
        "cella_role_jet_orbit",
        f"Exact active S3 role-jet orbit at order {order}.",
        lambda: role_jet_orbit(int(order), jet, exponents),
        depends=("Generators are the input swap s and output-role swap t; group laws are checked exactly.",),
    )


def call_curvature_orbit_spectrum(graph_jet: list) -> dict:
    """Compute active graph-role curvature spectra from (a,b,A,B,C)."""
    return _wrap_proof(
        "cella_curvature_orbit_spectrum",
        "Active graph-role curvature spectrum: six ordered charts, three output spectra.",
        lambda: curvature_orbit_spectrum(graph_jet),
        depends=("Graph-normalized charts have kappa_int=0; total K_G is checked across roles.",),
    )


def call_three_channel_referee(gradient: list, hessian: list) -> dict:
    """Return determinant partition and labeled n=3 channel record."""
    return _wrap_proof(
        "cella_three_channel_referee",
        "Exact n=3 three-channel determinant-partition referee.",
        lambda: three_channel_referee(gradient, hessian),
        depends=("Channels are labeled; do not read tuples positionally.",),
    )


def call_gauge_channel_transport(gradient: list, hessian: list, gauge: list) -> dict:
    """Apply exact gauge transport and report channel movement."""
    return _wrap_proof(
        "cella_gauge_channel_transport",
        "Exact gauge-channel transport under H -> H + g a^T + a g^T.",
        lambda: gauge_channel_transport(gradient, hessian, gauge),
        depends=("K_G must remain fixed; the channel shift should live in the zero-sum fiber.",),
    )


def call_rolechspec_n3(
    gradient: list,
    hessian: list | None = None,
    carrier: list | None = None,
) -> dict:
    """Compute n=3 RoleChSpec densities and recover carrier O linearly."""
    return _wrap_proof(
        "cella_rolechspec_n3",
        "n=3 RoleChSpec density fingerprint with linear carrier recovery.",
        lambda: rolechspec_n3(gradient, hessian=hessian, carrier=carrier),
        depends=("The recovery uses r=1 coupling-density rows; no Groebner basis is involved.",),
    )


def call_role_pair_loss_diagnostic(n: int) -> dict:
    """Report role-pair carrier/magnitude loss dimensions."""
    return _wrap_proof(
        "cella_role_pair_loss_diagnostic",
        f"Role-pair carrier loss diagnostic for n={n}.",
        lambda: role_pair_loss_diagnostic(int(n)),
        depends=("Magnitude summaries keep triv+std and discard S^(n-2,2).",),
    )


def call_shadow_law(n: int, gradient: list) -> dict:
    """Compute the Johnson shadow-law scalar and direction."""
    return _wrap_proof(
        "cella_shadow_law",
        f"Johnson shadow-law scalar and direction for n={n}.",
        lambda: shadow_law(int(n), gradient),
        depends=("The scalar is the average of triangle weights T_S.",),
    )


def call_wreath_law(kind: str, m: int, k: int | None = None) -> dict:
    """Return exact gcd/wreath monodromy law records."""
    return _wrap_proof(
        "cella_wreath_law",
        f"Closed wreath-law monodromy record for {kind}.",
        lambda: wreath_law(str(kind), m, k),
        depends=("This is the closed law; it does not perform numerical continuation.",),
    )


def call_arith_refine(required_bits: int, enclosures: list, ceiling: int | None = None) -> dict:
    """Resolve rational enclosures by exact endpoint rounding."""
    return _wrap_proof(
        "cella_arith_refine",
        "Ziv-style rational enclosure refinement certificate.",
        lambda: arith_refine(int(required_bits), enclosures, ceiling=ceiling),
        depends=("Every enclosure endpoint is rounded exactly; unresolved cases refuse by budget.",),
    )


def call_arith_precision_budget(
    output_bits: int,
    path_losses: list | None = None,
    format_bits: int = 53,
    atoms: list | None = None,
) -> dict:
    """Compute a composition-floor precision budget."""
    return _wrap_proof(
        "cella_arith_precision_budget",
        "Composition-floor precision budget and atom meetability verdict.",
        lambda: arith_precision_budget(
            int(output_bits),
            path_losses=path_losses,
            format_bits=int(format_bits),
            atoms=atoms,
        ),
        depends=("The floor is declared-output bits plus declared path losses.",),
    )


def call_elliptic_legendre_reduce(m, n) -> dict:
    """Normalize Legendre third-kind data and block singular direct routes."""
    return _wrap_proof(
        "cella_elliptic_legendre_reduce",
        "Legendre third-kind route admissibility and regularization record.",
        lambda: elliptic_legendre_reduce(m, n),
        depends=("If n>1, direct singular-path ellippi is not a certified route.",),
    )


def call_third_kind_cpv(
    m,
    n,
    scale,
    weight_pi,
    weight_k,
    dps: int = 90,
    tolerance="1e-35",
    contour_height="0.25",
) -> dict:
    """Certify a third-kind CPV value by two admissible numerical routes."""
    return _wrap_proof(
        "cella_third_kind_cpv",
        "Third-kind CPV certificate by regular transform and complex contour routes.",
        lambda: third_kind_cpv(
            m,
            n,
            scale,
            weight_pi,
            weight_k,
            dps=int(dps),
            tolerance=tolerance,
            contour_height=contour_height,
        ),
        depends=("No naive ellippi(n>1,m) call is used on certified singular paths.",),
    )


def call_residue_branch_gate(m, n, prefactor) -> dict:
    """Prove exact residue and branch-offset metadata for a third-kind pole."""
    return _wrap_proof(
        "cella_residue_branch_gate",
        "Exact third-kind residue and branch-offset gate.",
        lambda: residue_branch_gate(m, n, prefactor),
        depends=("Residues are symbolic gates; branch offsets derive from the weighted residue.",),
    )


def call_carlson_period_referee(m_primary, m_dual, dps: int = 90) -> dict:
    """Gate period identities by independent Carlson RF evaluations."""
    return _wrap_proof(
        "cella_carlson_period_referee",
        "Carlson RF period referee for omega identities.",
        lambda: carlson_period_referee(m_primary, m_dual, dps=int(dps)),
        depends=("Carlson RF is the independent numerical period route.",),
    )


def call_two_route_compare(route_a, route_b, requested_digits: int) -> dict:
    """Compare two route values and report achieved decimal agreement."""
    return _wrap_proof(
        "cella_two_route_compare",
        "Independent-route agreement floor certificate.",
        lambda: two_route_compare(route_a, route_b, int(requested_digits)),
        depends=("Route agreement certifies only to the achieved floor and assumes route independence.",),
    )


def call_period_curve_invariants(lambda_value, partner_j=None) -> dict:
    """Compute exact Legendre curve invariants and optional Phi2 check."""
    return _wrap_proof(
        "cella_period_curve_invariants",
        "Exact Legendre lambda, j-invariant, and modular-polynomial check.",
        lambda: period_curve_invariants(lambda_value, partner_j=partner_j),
        depends=("This is the curve-structure layer, separate from numerical period evaluation.",),
    )


def call_period_quartic(kind: str, m) -> dict:
    """Create a Cella-native elliptic quartic structural record."""
    return _wrap_proof(
        "cella_period_quartic",
        f"Cella-native exact period quartic record for {kind}.",
        lambda: period_quartic(str(kind), m),
        depends=("This is a structural period record; no numerical period evaluation is performed.",),
    )


def call_period_third_kind_residue(curve: dict, n, prefactor) -> dict:
    """Compute exact third-kind pole residues and branch jumps."""
    return _wrap_proof(
        "cella_period_third_kind_residue",
        "Cella-native third-kind residue and branch-jump ledger.",
        lambda: third_kind_residue(curve, n, prefactor),
        depends=("Residues are exact structural data for the declared curve and differential.",),
    )


def call_period_normal_form(
    kind: str,
    curve: dict,
    n=None,
    scale=1,
    weight_pi=1,
    weight_k=0,
    basis_terms: list | None = None,
    residue_jumps: list | None = None,
) -> dict:
    """Reduce a supported route into exact period-basis normal form."""
    return _wrap_proof(
        "cella_period_normal_form",
        f"Cella-native period normal form for {kind}.",
        lambda: period_normal_form(
            str(kind),
            curve,
            n=n,
            scale=scale,
            weight_pi=weight_pi,
            weight_k=weight_k,
            basis_terms=basis_terms,
            residue_jumps=residue_jumps,
        ),
        depends=("Normal-form equality is structural; numeric_evaluation remains intentionally absent.",),
    )


def call_period_route_compare(route_a: dict, route_b: dict) -> dict:
    """Compare exact period normal forms structurally."""
    return _wrap_proof(
        "cella_period_route_compare",
        "Exact Cella period normal-form route comparison.",
        lambda: period_route_compare(route_a, route_b),
        depends=("Comparison subtracts basis coefficients and residue-jump records exactly.",),
    )


def call_period_gap_report(scope: str = "elliptic_quartic_spike") -> dict:
    """Return explicit gaps for the native period/residue spike."""
    return _wrap_proof(
        "cella_period_gap_report",
        f"Cella-native period spike gap report for {scope}.",
        lambda: period_gap_report(str(scope)),
        depends=("Gap records are implementation targets, not mathematical verdicts.",),
    )


def call_pslq_field_referee(value, basis: list, max_coeff: int = 10) -> dict:
    """Search for bounded exact linear relations over a declared basis."""
    return _wrap_proof(
        "cella_pslq_field_referee",
        "Bounded algebraic-basis relation referee.",
        lambda: pslq_field_referee(value, basis, max_coeff=int(max_coeff)),
        depends=("Negative results are bounded-search findings, not independence proofs.",),
    )


def call_arith_constant_pin(
    name: str,
    value: str,
    certified_digits: int,
    route_agreement_digits: int,
    branch_convention: str,
    exact_gates: list | None = None,
) -> dict:
    """Record a certified arithmetic constant pin."""
    return _wrap_proof(
        "cella_arith_constant_pin",
        f"Arithmetic constant pin for {name}.",
        lambda: arith_constant_pin(
            name,
            value,
            int(certified_digits),
            int(route_agreement_digits),
            branch_convention,
            exact_gates=exact_gates,
        ),
        depends=("The digest is a receipt over value, branch convention, digit floor, and exact gates.",),
    )


def call_cella_help(topic: str | None = None) -> dict:
    """Explain Cella MCP tools and how to read certificate-shaped results."""

    def compute_help():
        if topic is None or str(topic).strip() in ("", "all", "*"):
            return {
                "topic": "all",
                "overview": (
                    "Cella is an exact local-geometry and symbolic rational-function MCP. "
                    "Use point tools for evaluated jets, symbolic tools for Q[variables] certificates, "
                    "proof tools for pole laws, support, and positivity, and cleanliness tools for "
                    "BACL/refinery algebra-selection over binary64 operand chains."
                ),
                "exact_input_rule": (
                    "Use integers or rational strings. Decimal JSON floats are forbidden on verdict paths."
                ),
                "result_contract": _RESULT_CONTRACT,
                "sparse_record_guide": _SPARSE_RECORD_GUIDE,
                "profiles": {
                    name: {
                        "tool_count": str(len(names)),
                        "tools": list(names),
                    }
                    for name, names in TOOL_GROUPS.items()
                },
                "tools": _HELP_TOOLS,
                "recommended_workflows": {
                    "surface_to_exact_point": [
                        "cella_surface_jet",
                        "cella_carrier or cella_sigma_tower",
                        "cella_channels_n3 when n=3 channel labels are needed",
                    ],
                    "symbolic_coefficient": [
                        "cella_symbolic_pole_law",
                        "cella_symbolic_equal",
                    ],
                    "support_before_expansion": [
                        "cella_symbolic_valuation",
                        "cella_poly_certificate or cella_sturm_positive when positivity remains",
                    ],
                    "cleanliness_refinery": [
                        "cella_bacl_pair",
                        "cella_operand_residue_trace",
                        "cella_cleanliness_rank or cella_bacl_dial",
                        "cella_refinery_compare for hand-declared burden vectors",
                    ],
                    "pathfinder_preflight": [
                        "Pathfinder is an internal engine layer, not a public chat profile.",
                        "Use cella_operand_residue_trace for exact operand telemetry when needed.",
                        "Use cella_cleanliness_rank or cella_bacl_dial for declared candidate ranking.",
                        "Use cella_refinery_compare for hand-declared burden vectors.",
                        "Use cella_arith_precision_budget when no cleaner rewrite is available.",
                    ],
                    "campaign_retrodiction": [
                        "cella_kn_metric_builder when working the KN metric",
                        "cella_diag_germ_classifier for each role divisor",
                        "cella_role_divisor_retrodict for the complementarity table",
                        "cella_corner_frontface for codimension-2 corners",
                        "cella_positive_factor_certificate for sign/positivity gates",
                        "cella_implicit_gaussian_curvature as the exact total-curvature referee",
                    ],
                    "reference_lift": [
                        "cella_role_jet_orbit for active role-transposition sanity",
                        "cella_curvature_orbit_spectrum for graph-role curvature charts",
                        "cella_three_channel_referee then cella_gauge_channel_transport for channel provenance",
                        "cella_rolechspec_n3 for RoleChSpec faithfulness without Groebner swell",
                        "cella_role_pair_loss_diagnostic and cella_shadow_law for carrier/loss campaigns",
                        "cella_wreath_law before any numerical monodromy continuation",
                    ],
                    "arithmetic_certification": [
                        "cella_arith_precision_budget before declaring a comparison tolerance",
                        "cella_period_quartic and cella_period_third_kind_residue to create native structural records",
                        "cella_period_normal_form and cella_period_route_compare before decimal evaluation",
                        "cella_elliptic_legendre_reduce before any third-kind Pi evaluation",
                        "cella_residue_branch_gate for branch offsets and residue signs",
                        "cella_third_kind_cpv for two-route CPV certification",
                        "cella_carlson_period_referee for independent period controls",
                        "cella_period_gap_report to pick the next native-kernel spike",
                        "cella_two_route_compare and cella_arith_constant_pin to bank the achieved floor",
                    ],
                },
            }
        key = str(topic).strip()
        if key in ("profiles", "profile", "tool_groups", "tool-groups"):
            return {
                "topic": "profiles",
                "profiles": {
                    name: {
                        "tool_count": str(len(names)),
                        "tools": list(names),
                    }
                    for name, names in TOOL_GROUPS.items()
                },
                "usage": "Launch with python -m cella.mcp_server --profile PROFILE.",
            }
        if key not in _HELP_TOOLS:
            raise ValueError(f"unknown Cella help topic {key!r}; choose one of {sorted(_HELP_TOOLS)}")
        return {
            "topic": key,
            "tool": _HELP_TOOLS[key],
            "result_contract": _RESULT_CONTRACT,
            "sparse_record_guide": _SPARSE_RECORD_GUIDE,
        }

    return _wrap_proof(
        "cella_help",
        "Cella MCP tool guide and result-reading contract.",
        compute_help,
        depends=("Help is descriptive; it does not perform a mathematical verdict.",),
    )


def tool_callable_map() -> dict:
    return {
        "cella_help": call_cella_help,
        "cella_bacl_pair": call_bacl_pair,
        "cella_operand_residue_trace": call_operand_residue_trace,
        "cella_refinery_compare": call_refinery_compare,
        "cella_cleanliness_rank": call_cleanliness_rank,
        "cella_bacl_dial": call_bacl_dial,
        "cella_residual_profile": call_residual_profile,
        "cella_route_plan": call_route_plan,
        "cella_rewrite_candidates": call_rewrite_candidates,
        "cella_pathfinder_compare": call_pathfinder_compare,
        "cella_diag_germ_classifier": call_diag_germ_classifier,
        "cella_role_divisor_retrodict": call_role_divisor_retrodict,
        "cella_corner_frontface": call_corner_frontface,
        "cella_positive_factor_certificate": call_positive_factor_certificate,
        "cella_metric_candidate_selector": call_metric_candidate_selector,
        "cella_kn_metric_builder": call_kn_metric_builder,
        "cella_implicit_gaussian_curvature": call_implicit_gaussian_curvature,
        "cella_role_jet_orbit": call_role_jet_orbit,
        "cella_curvature_orbit_spectrum": call_curvature_orbit_spectrum,
        "cella_three_channel_referee": call_three_channel_referee,
        "cella_gauge_channel_transport": call_gauge_channel_transport,
        "cella_rolechspec_n3": call_rolechspec_n3,
        "cella_role_pair_loss_diagnostic": call_role_pair_loss_diagnostic,
        "cella_shadow_law": call_shadow_law,
        "cella_wreath_law": call_wreath_law,
        "cella_arith_refine": call_arith_refine,
        "cella_arith_precision_budget": call_arith_precision_budget,
        "cella_elliptic_legendre_reduce": call_elliptic_legendre_reduce,
        "cella_third_kind_cpv": call_third_kind_cpv,
        "cella_residue_branch_gate": call_residue_branch_gate,
        "cella_carlson_period_referee": call_carlson_period_referee,
        "cella_two_route_compare": call_two_route_compare,
        "cella_period_curve_invariants": call_period_curve_invariants,
        "cella_period_quartic": call_period_quartic,
        "cella_period_third_kind_residue": call_period_third_kind_residue,
        "cella_period_normal_form": call_period_normal_form,
        "cella_period_route_compare": call_period_route_compare,
        "cella_period_gap_report": call_period_gap_report,
        "cella_pslq_field_referee": call_pslq_field_referee,
        "cella_arith_constant_pin": call_arith_constant_pin,
        "cella_carrier": call_carrier,
        "cella_sigma_tower": call_sigma_tower,
        "cella_channels_n3": call_channels_n3,
        "cella_sensor": call_sensor,
        "cella_fingerprint": call_fingerprint,
        "cella_local_pole_law": call_local_pole_law,
        "cella_corner_newton": call_corner_newton,
        "cella_poly_certificate": call_poly_certificate,
        "cella_surface_jet": call_surface_jet,
        "cella_sturm_positive": call_sturm_positive,
        "cella_symbolic_rational": call_symbolic_rational,
        "cella_symbolic_equal": call_symbolic_equal,
        "cella_symbolic_pole_law": call_symbolic_pole_law,
        "cella_symbolic_gauge_carrier": call_symbolic_gauge_carrier,
        "cella_symbolic_channel_sum": call_symbolic_channel_sum,
        "cella_symbolic_valuation": call_symbolic_valuation,
    }


def _router_error(token: str, message: str, **extra) -> dict:
    return {
        "schema": "cella-router-v1",
        "ok": False,
        "error": {
            "token": token,
            "message": message,
        },
        **extra,
    }


def _profile_record(profile: str) -> dict:
    names = tool_names_for_profile(profile)
    return {
        "tool_count": str(len(names)),
        "tools": list(names),
    }


def _tool_summary(tool_name: str) -> dict:
    info = _HELP_TOOLS.get(tool_name, {})
    out = {
        "name": tool_name,
        "purpose": info.get("purpose", ""),
    }
    for key in ("inputs", "proper_use"):
        if key in info:
            out[key] = info[key]
    return out


def _optional_bool(value) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        key = value.strip().lower()
        if key in ("1", "true", "yes", "on", "enable", "enabled"):
            return True
        if key in ("0", "false", "no", "off", "disable", "disabled"):
            return False
    raise ValueError("enabled must be a boolean or one of on/off/true/false")


def _slug(value: str) -> str:
    out = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in value)
    return out[:80] or "cella_result"


class JsonExportState:
    def __init__(self):
        self.enabled = False
        self.folder: Path | None = None
        self.sequence = 0
        self.inline_result = True

    def status(self) -> dict:
        return {
            "enabled": self.enabled,
            "folder": None if self.folder is None else str(self.folder),
            "sequence": str(self.sequence),
            "inline_result": self.inline_result,
        }

    def configure(self, enabled=None, folder: str | None = None, inline_result=None) -> dict:
        requested = _optional_bool(enabled)
        inline = _optional_bool(inline_result)
        if folder is not None:
            folder_path = Path(str(folder)).expanduser()
            folder_path.mkdir(parents=True, exist_ok=True)
            if not folder_path.is_dir():
                raise NotADirectoryError(str(folder_path))
            self.folder = folder_path
        if inline is not None:
            self.inline_result = inline
        if requested is True and self.folder is None:
            raise ValueError("folder is required the first time JSON export is enabled")
        if requested is not None:
            self.enabled = requested
        return self.status()

    def write(self, tool_name: str, payload: dict) -> dict | None:
        if not self.enabled or self.folder is None:
            return None
        self.folder.mkdir(parents=True, exist_ok=True)
        self.sequence += 1
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        path = self.folder / f"{timestamp}-{self.sequence:04d}-{_slug(tool_name)}.json"
        with path.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
            fh.write("\n")
        return {
            "enabled": True,
            "folder": str(self.folder),
            "path": str(path),
            "sequence": str(self.sequence),
        }


def _preview_json(value, limit: int = 600) -> str:
    text = json.dumps(value, sort_keys=True)
    if len(text) <= limit:
        return text
    return text[:limit] + "...[truncated]"


def _result_summary(result) -> dict:
    if not isinstance(result, dict):
        return {
            "ok": True,
            "value_preview": _preview_json(result),
        }
    summary = {
        "ok": result.get("ok"),
        "tool": result.get("tool"),
        "schema": result.get("schema"),
        "what": result.get("what"),
        "number_type": result.get("number_type"),
        "refusal": result.get("refusal"),
        "plain": result.get("plain"),
    }
    if "value" in result:
        summary["value_preview"] = _preview_json(result["value"])
    return {k: v for k, v in summary.items() if v is not None}


class CellaRouter:
    """Stateful chat-facing router over the full Cella MCP callable map."""

    def __init__(self, default_profile: str | None = "core"):
        self.active_profile = normalize_profile(default_profile or "core")
        self.export_state = JsonExportState()

    def profiles(self) -> dict:
        return {
            "schema": "cella-router-v1",
            "ok": True,
            "active_profile": self.active_profile,
            "router_tools": list(ROUTER_TOOL_NAMES),
            "json_export": self.export_state.status(),
            "profiles": {
                name: _profile_record(name)
                for name in TOOL_GROUPS
            },
            "usage": {
                "switch": "Call cella_use_profile(profile) to change the active Cella profile in this MCP process.",
                "inspect": "Call cella_tools(profile) to see the compressed tool list for one profile.",
                "export": "Call cella_json_export(enabled, folder) to toggle full JSON result files for cella_call.",
                "dispatch": "Call cella_call(tool, args, profile) to run one Cella tool without loading its schema.",
            },
        }

    def use_profile(self, profile: str) -> dict:
        previous = self.active_profile
        active = normalize_profile(profile)
        self.active_profile = active
        names = tool_names_for_profile(active)
        return {
            "schema": "cella-router-v1",
            "ok": True,
            "previous_profile": previous,
            "active_profile": active,
            "tool_count": str(len(names)),
            "tools": list(names),
        }

    def tools(self, profile: str | None = None) -> dict:
        selected = normalize_profile(profile) if profile is not None else self.active_profile
        names = tool_names_for_profile(selected)
        return {
            "schema": "cella-router-v1",
            "ok": True,
            "active_profile": self.active_profile,
            "profile": selected,
            "tool_count": str(len(names)),
            "tools": [_tool_summary(name) for name in names],
        }

    def json_export(self, enabled=None, folder: str | None = None, inline_result=None) -> dict:
        """Configure full JSON result export for subsequent cella_call invocations."""
        try:
            status = self.export_state.configure(
                enabled=enabled,
                folder=folder,
                inline_result=inline_result,
            )
        except Exception as exc:
            return _router_error(
                "EXPORT_CONFIG_FAILED",
                str(exc),
                active_profile=self.active_profile,
                exception_type=type(exc).__name__,
                json_export=self.export_state.status(),
            )
        return {
            "schema": "cella-router-v1",
            "ok": True,
            **status,
            "usage": (
                "When enabled, every cella_call writes its full router result as one JSON file. "
                "Set inline_result=false to return only a compact summary plus the JSON path."
            ),
        }

    def _finish_call(self, tool_name: str, response: dict) -> dict:
        export_enabled = self.export_state.enabled
        try:
            export = self.export_state.write(tool_name, response)
        except Exception as exc:
            response = dict(response)
            response["json_export"] = {
                "enabled": True,
                "error": {
                    "token": "EXPORT_WRITE_FAILED",
                    "message": str(exc),
                    "exception_type": type(exc).__name__,
                },
            }
            return response
        if export is None:
            return response
        if export_enabled and not self.export_state.inline_result:
            compact = {
                "schema": response.get("schema", "cella-router-v1"),
                "ok": response.get("ok", False),
                "active_profile": response.get("active_profile"),
                "effective_profile": response.get("effective_profile"),
                "tool": response.get("tool", tool_name),
                "result_summary": _result_summary(response.get("result")),
                "json_export": export,
            }
            if "error" in response:
                compact["error"] = response["error"]
            return compact
        response = dict(response)
        response["json_export"] = export
        return response

    def call(self, tool: str, args: dict | None = None, profile: str | None = None) -> dict:
        effective_profile = normalize_profile(profile) if profile is not None else self.active_profile
        tool_name = normalize_tool_name(tool)
        if tool_name not in TOOL_NAMES:
            return self._finish_call(
                tool_name,
                _router_error(
                    "UNKNOWN_TOOL",
                    f"unknown Cella tool {tool!r}",
                    active_profile=self.active_profile,
                    effective_profile=effective_profile,
                    tool=tool_name,
                ),
            )
        if tool_name not in tool_names_for_profile(effective_profile):
            return self._finish_call(
                tool_name,
                _router_error(
                    "TOOL_NOT_IN_PROFILE",
                    f"{tool_name} is not exposed by profile {effective_profile!r}",
                    active_profile=self.active_profile,
                    effective_profile=effective_profile,
                    tool=tool_name,
                    available_profiles=available_profiles_for_tool(tool_name),
                ),
            )
        if args is None:
            args = {}
        if not isinstance(args, dict):
            return self._finish_call(
                tool_name,
                _router_error(
                    "BAD_ARGS",
                    "cella_call args must be a JSON object keyed by the target tool argument names",
                    active_profile=self.active_profile,
                    effective_profile=effective_profile,
                    tool=tool_name,
                ),
            )
        callables = tool_callable_map()
        try:
            result = callables[tool_name](**args)
        except Exception as exc:
            return self._finish_call(
                tool_name,
                _router_error(
                    "CALL_FAILED",
                    str(exc),
                    active_profile=self.active_profile,
                    effective_profile=effective_profile,
                    tool=tool_name,
                    exception_type=type(exc).__name__,
                ),
            )
        return self._finish_call(tool_name, {
            "schema": "cella-router-v1",
            "ok": bool(result.get("ok", True)) if isinstance(result, dict) else True,
            "active_profile": self.active_profile,
            "effective_profile": effective_profile,
            "tool": tool_name,
            "result": result,
        })


def build_mcp_server(profile: str | None = None):
    """Create a FastMCP server exposing one practical Cella tool profile."""
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("the Python 'mcp' package is required to run the MCP server") from exc

    profile = normalize_profile(profile)
    tool_names = tool_names_for_profile(profile)
    server_name = "cella" if profile == "all" else f"cella-{profile}"
    mcp = FastMCP(
        server_name,
        instructions=(
            f"Cella MCP profile '{profile}'. Inputs must be exact integers or "
            "rational strings. Results are certificate-shaped records with exact "
            "values or typed refusals. Start with cella_help if you need tool usage "
            "or result-field guidance."
        ),
    )

    callables = tool_callable_map()
    missing = [name for name in tool_names if name not in callables]
    if missing:
        raise RuntimeError(f"profile {profile!r} references unregistered tools: {missing}")
    for name in tool_names:
        mcp.tool(name=name)(callables[name])
    return mcp


def build_router_mcp_server(default_profile: str | None = "core"):
    """Create the slim Claude-facing Cella router MCP server."""
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("the Python 'mcp' package is required to run the MCP server") from exc

    router = CellaRouter(default_profile=default_profile or "core")
    mcp = FastMCP(
        "cella-router",
        instructions=(
            "Cella router exposes five stable tools: cella_profiles, "
            "cella_use_profile, cella_tools, cella_json_export, and cella_call. "
            "Switch profiles in chat, inspect one compressed profile at a time, "
            "toggle full JSON result export when needed, and dispatch exact Cella "
            "tools through cella_call without loading every tool schema."
        ),
    )
    mcp.tool(name="cella_profiles")(router.profiles)
    mcp.tool(name="cella_use_profile")(router.use_profile)
    mcp.tool(name="cella_tools")(router.tools)
    mcp.tool(name="cella_json_export")(router.json_export)
    mcp.tool(name="cella_call")(router.call)
    return mcp


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run the Cella MCP server.")
    parser.add_argument(
        "--transport",
        choices=("stdio", "sse", "streamable-http"),
        default="stdio",
        help="MCP transport to use.",
    )
    parser.add_argument(
        "--profile",
        default=None,
        metavar="PROFILE",
        help="Tool profile to expose, or router default profile when --router is set.",
    )
    parser.add_argument(
        "--router",
        action="store_true",
        help="Expose the slim chat-switchable Cella router instead of a direct profile.",
    )
    parser.add_argument(
        "--list-profiles",
        action="store_true",
        help="List available tool profiles and exit.",
    )
    args = parser.parse_args(argv)
    if args.list_profiles:
        print(f"router: {len(ROUTER_TOOL_NAMES)} tools")
        for name in ROUTER_TOOL_NAMES:
            print(f"  {name}")
        for profile_name, names in TOOL_GROUPS.items():
            print(f"{profile_name}: {len(names)} tools")
            for name in names:
                print(f"  {name}")
        return 0
    if args.router:
        build_router_mcp_server(default_profile=args.profile or "core").run(args.transport)
    else:
        build_mcp_server(args.profile or "all").run(args.transport)
    return 0


if __name__ == "__main__":  # pragma: no cover - exercised by MCP clients
    raise SystemExit(main())
