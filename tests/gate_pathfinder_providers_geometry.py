"""Gate the DBP curvature / local-germ / exact-real route-family providers."""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.pathfinder import Obligation, PathfinderRequest
from cella.pathfinder.recognize.curvature import (
    PROVIDERS as CURVATURE_PROVIDERS,
    recognize_canonical_invariant_reduction,
    recognize_curvature_role_orbit,
    recognize_dbp_role_orbit_reduction,
    recognize_gauge_channel_transport,
)
from cella.pathfinder.recognize.local_germ import (
    PROVIDERS as LOCAL_GERM_PROVIDERS,
    recognize_extremal_face,
    recognize_local_metric_germ,
    recognize_newton_wedge_corner,
    recognize_parity_fixed_face,
)
from cella.pathfinder.recognize.real import (
    PROVIDERS as REAL_PROVIDERS,
    recognize_exact_rational_inertia,
    recognize_invariant_floor_real,
    recognize_matrix_pencil_selection,
    recognize_sturm_escalation,
)
from cella.pathfinder.serialize import canonical_json_bytes


FAILS: list[str] = []

ALL_FAMILIES = tuple(
    provider.route_family
    for provider in CURVATURE_PROVIDERS + LOCAL_GERM_PROVIDERS + REAL_PROVIDERS
)


def check(name: str, condition: bool) -> None:
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")
    if not condition:
        FAILS.append(name)


def request(shape: str, **context_extra: object) -> PathfinderRequest:
    context: dict[str, object] = {"problem_shape": shape}
    context.update(context_extra)
    return PathfinderRequest.create(
        request_id="geometry-provider-fixture-v1",
        target_obligation=Obligation(
            "geometry-route",
            "Emit a certified geometric/exact-real computational route.",
            "route-only",
        ),
        external_binding={"host_surface": "external:dbp_surface"},
        mathematical_context=context,
        available_route_families=ALL_FAMILIES,
    )


def check_refusal(name: str, outcome: object, code: str) -> None:
    check(
        name,
        outcome.refusal is not None and outcome.refusal.code == code,
    )


# Keystone fixture F = x1^2 + x1*x2 + x3^2 - 3 at (1, 1, 1).
KEYSTONE_GRADIENT = (3, 1, 2)
KEYSTONE_HESSIAN = ((2, 1, 0), (1, 0, 0), (0, 0, 2))


# ---------------------------------------------------------------------------
# canonical_invariant_reduction
# ---------------------------------------------------------------------------

print("== canonical_invariant_reduction ==")
canonical = recognize_canonical_invariant_reduction(
    request(
        "curvature_invariant",
        gradient=KEYSTONE_GRADIENT,
        hessian=KEYSTONE_HESSIAN,
        invariant_order=2,
    )
)
check("keystone curvature fixture is recognized", canonical.candidate is not None)
assert canonical.candidate is not None
route = canonical.candidate.route
check(
    "route sums channels rather than computing sigma_r",
    tuple(step.operation for step in route.ordered_steps)
    == (
        "form_bordered_channel_minors",
        "vandermonde_channel_split",
        "sum_channels_to_invariant",
        "emit_invariant_and_channel_account",
    ),
)
check(
    "vandermonde nodes are 0..r",
    dict(route.ordered_steps[1].parameters)["nodes"] == (0, 1, 2),
)
sum_params = dict(route.ordered_steps[2].parameters)
check("r = 2 parity law lands in QQ", sum_params["parity"] == "even" and sum_params["value_field"] == "QQ")
check(
    "certificates include bordered-det cross-check and KC laws",
    {"kc1-gauge-invariance", "kc2-zero-sum-residue", "kc5-rational-numerator", "bordered-det-cross-check"}
    <= {ob.obligation_id for ob in route.certificate_obligations},
)
check(
    "canonical route serialization is byte deterministic",
    canonical_json_bytes(route) == canonical_json_bytes(route),
)
check_refusal(
    "q = 0 gradient refuses singular stratum",
    recognize_canonical_invariant_reduction(
        request(
            "curvature_invariant",
            gradient=(0, 0, 0),
            hessian=KEYSTONE_HESSIAN,
            invariant_order=2,
        )
    ),
    "singular_stratum_q_zero",
)
check_refusal(
    "missing hessian refuses non-rational input",
    recognize_canonical_invariant_reduction(
        request("curvature_invariant", gradient=KEYSTONE_GRADIENT, invariant_order=2)
    ),
    "non_rational_input",
)
check_refusal(
    "asymmetric hessian refuses non-rational input",
    recognize_canonical_invariant_reduction(
        request(
            "curvature_invariant",
            gradient=KEYSTONE_GRADIENT,
            hessian=((2, 1, 0), (0, 0, 0), (0, 0, 2)),
            invariant_order=2,
        )
    ),
    "non_rational_input",
)
check_refusal(
    "invariant order r = n is out of range",
    recognize_canonical_invariant_reduction(
        request(
            "curvature_invariant",
            gradient=KEYSTONE_GRADIENT,
            hessian=KEYSTONE_HESSIAN,
            invariant_order=3,
        )
    ),
    "invariant_order_out_of_range",
)
check_refusal(
    "wrong shape is refused",
    recognize_canonical_invariant_reduction(
        request("gauge_transport", gradient=KEYSTONE_GRADIENT, hessian=KEYSTONE_HESSIAN, invariant_order=2)
    ),
    "shape_mismatch",
)

# ---------------------------------------------------------------------------
# dbp_role_orbit_reduction
# ---------------------------------------------------------------------------

print("== dbp_role_orbit_reduction ==")
RETRODICTION_JET = (5, 7, 2, 3, 4)
orbit = recognize_dbp_role_orbit_reduction(
    request("role_orbit_invariance", jet=RETRODICTION_JET)
)
check("retrodiction jet is recognized", orbit.candidate is not None)
assert orbit.candidate is not None
restrict_params = dict(orbit.candidate.route.ordered_steps[0].parameters)
check(
    "coupling numerators are exact: Lambda = (3, -1/5, -1/7), q0 = 75",
    restrict_params["lambda_p"] == 3
    and restrict_params["lambda_d"] == Fraction(-1, 5)
    and restrict_params["lambda_s"] == Fraction(-1, 7)
    and restrict_params["q0"] == 75,
)
transport_params = dict(orbit.candidate.route.ordered_steps[1].parameters)
check(
    "S3 birational maps are declared exactly",
    transport_params["s_action"] == "s(a,b) = (b,a)"
    and transport_params["t_action"] == "t(a,b) = (1/a, -b/a)"
    and "(A*b - a*B)/a^3" in transport_params["t_second_order"],
)
check(
    "orbit-separation Jacobian is the exact nonzero rational 8*prod(Lambda)/q0^6",
    dict(orbit.candidate.route.ordered_steps[2].parameters)["jacobian_determinant"]
    == Fraction(8 * 3, 1) * Fraction(-1, 5) * Fraction(-1, 7) / Fraction(75) ** 6,
)
check(
    "orbit certificates include the S3 relations",
    "s3-group-relations" in {ob.obligation_id for ob in orbit.candidate.route.certificate_obligations},
)
check_refusal(
    "jet with a = 0 refuses absent output chart",
    recognize_dbp_role_orbit_reduction(request("role_orbit_invariance", jet=(0, 7, 2, 3, 4))),
    "output_chart_absent",
)
check_refusal(
    "channel isotropy Lambda_P = 0 is refused",
    recognize_dbp_role_orbit_reduction(request("role_orbit_invariance", jet=(5, 7, 2, 0, 4))),
    "channel_isotropy_locus",
)
check_refusal(
    "missing jet refuses non-rational input",
    recognize_dbp_role_orbit_reduction(request("role_orbit_invariance")),
    "non_rational_input",
)
check_refusal(
    "wrong shape is refused",
    recognize_dbp_role_orbit_reduction(request("curvature_invariant", jet=RETRODICTION_JET)),
    "shape_mismatch",
)

# ---------------------------------------------------------------------------
# curvature_role_orbit
# ---------------------------------------------------------------------------

print("== curvature_role_orbit ==")
spectrum = recognize_curvature_role_orbit(
    request(
        "role_curvature_spectrum",
        jet=RETRODICTION_JET,
        declared_shared_K=Fraction(-1, 5625),
    )
)
check("retrodiction anchor jet is recognized", spectrum.candidate is not None)
assert spectrum.candidate is not None
spectra_params = dict(spectrum.candidate.route.ordered_steps[2].parameters)
check(
    "shared K and q0 replay the anchor: q0 = 75, K = -1/5625",
    spectra_params["q0"] == 75 and spectra_params["shared_K"] == Fraction(-1, 5625),
)
check(
    "the three closed-form spectra are route parameters",
    all(key in spectra_params for key in ("C_P", "C_D", "C_S"))
    and "retrodiction_anchor" in spectra_params,
)
check(
    "role-spectrum certificates include shared-K identities",
    "shared-k-identities"
    in {ob.obligation_id for ob in spectrum.candidate.route.certificate_obligations},
)
check_refusal(
    "declared shared K violating the identity refuses inconsistent jet data",
    recognize_curvature_role_orbit(
        request(
            "role_curvature_spectrum",
            jet=RETRODICTION_JET,
            declared_shared_K=Fraction(1, 5625),
        )
    ),
    "inconsistent_jet_data",
)
check_refusal(
    "jet with b = 0 refuses absent output chart",
    recognize_curvature_role_orbit(request("role_curvature_spectrum", jet=(5, 0, 2, 3, 4))),
    "output_chart_absent",
)
check_refusal(
    "malformed jet refuses non-rational input",
    recognize_curvature_role_orbit(request("role_curvature_spectrum", jet=(5, 7, 2, 3))),
    "non_rational_input",
)
check_refusal(
    "wrong shape is refused",
    recognize_curvature_role_orbit(request("role_orbit_invariance", jet=RETRODICTION_JET)),
    "shape_mismatch",
)

# ---------------------------------------------------------------------------
# gauge_channel_transport
# ---------------------------------------------------------------------------

print("== gauge_channel_transport ==")
gauge = recognize_gauge_channel_transport(
    request(
        "gauge_transport",
        gradient=KEYSTONE_GRADIENT,
        hessian=KEYSTONE_HESSIAN,
        gauge_vector=(1, 2, 3),
    )
)
check("keystone gauge fixture is recognized", gauge.candidate is not None)
assert gauge.candidate is not None
check(
    "rank-two update identity is declared",
    dict(gauge.candidate.route.ordered_steps[0].parameters)["identity"] == "H~ = H + g a^T + a g^T",
)
check(
    "Lorentzian classification carries the signature (2,1) form",
    "signature (2,1)"
    in dict(gauge.candidate.route.ordered_steps[2].parameters)["lorentzian_form"],
)
check(
    "gauge certificates include the KC6 single-edge law",
    "kc6-single-edge-law"
    in {ob.obligation_id for ob in gauge.candidate.route.certificate_obligations},
)
check(
    "gauge-rigid null directions stay in the exceptional branches",
    any("gauge-rigid" in branch for branch in gauge.candidate.route.exceptional_branches),
)
check_refusal(
    "missing gauge vector is refused",
    recognize_gauge_channel_transport(
        request("gauge_transport", gradient=KEYSTONE_GRADIENT, hessian=KEYSTONE_HESSIAN)
    ),
    "missing_gauge_vector",
)
check_refusal(
    "q = 0 gradient refuses singular stratum",
    recognize_gauge_channel_transport(
        request(
            "gauge_transport",
            gradient=(0, 0, 0),
            hessian=KEYSTONE_HESSIAN,
            gauge_vector=(1, 2, 3),
        )
    ),
    "singular_stratum_q_zero",
)
check_refusal(
    "non-rational gauge entry is refused",
    recognize_gauge_channel_transport(
        request(
            "gauge_transport",
            gradient=KEYSTONE_GRADIENT,
            hessian=KEYSTONE_HESSIAN,
            gauge_vector=(1, "two", 3),
        )
    ),
    "non_rational_input",
)
check_refusal(
    "wrong shape is refused",
    recognize_gauge_channel_transport(
        request(
            "curvature_invariant",
            gradient=KEYSTONE_GRADIENT,
            hessian=KEYSTONE_HESSIAN,
            gauge_vector=(1, 2, 3),
        )
    ),
    "shape_mismatch",
)

# ---------------------------------------------------------------------------
# local_metric_germ
# ---------------------------------------------------------------------------

print("== local_metric_germ ==")
germ = recognize_local_metric_germ(
    request(
        "local_pole_order",
        collapse_coefficients=(2, 5),
        transverse_channels=((3, 1), (4, 2)),
    )
)
check("generic collapse germ is recognized", germ.candidate is not None)
assert germ.candidate is not None
pole_params = dict(germ.candidate.route.ordered_steps[1].parameters)
check(
    "order-3 pole with exact coefficient (1/2)*(1/3 + 2/4) = 5/12",
    pole_params["pole_order"] == 3 and pole_params["leading_coefficient"] == Fraction(5, 12),
)
check(
    "germ certificates include the A2 Taylor identity",
    "a2-taylor-identity" in {ob.obligation_id for ob in germ.candidate.route.certificate_obligations},
)
check_refusal(
    "A2 = 0 refuses degenerate collapse",
    recognize_local_metric_germ(
        request(
            "local_pole_order",
            collapse_coefficients=(0, 5),
            transverse_channels=((3, 1),),
        )
    ),
    "degenerate_collapse",
)
check_refusal(
    "vanishing transverse channel is refused",
    recognize_local_metric_germ(
        request(
            "local_pole_order",
            collapse_coefficients=(2, 5),
            transverse_channels=((0, 1), (4, 2)),
        )
    ),
    "transverse_channel_vanishes",
)
check_refusal(
    "even germ (all P1 = 0) escalates to parity_fixed_face",
    recognize_local_metric_germ(
        request(
            "local_pole_order",
            collapse_coefficients=(2, 5),
            transverse_channels=((3, 0), (4, 0)),
        )
    ),
    "parity_fixed_escalation",
)
check_refusal(
    "missing germ data refuses non-rational input",
    recognize_local_metric_germ(request("local_pole_order")),
    "non_rational_input",
)
check_refusal(
    "wrong shape is refused",
    recognize_local_metric_germ(
        request(
            "corner_pole_order",
            collapse_coefficients=(2, 5),
            transverse_channels=((3, 1),),
        )
    ),
    "shape_mismatch",
)

# ---------------------------------------------------------------------------
# parity_fixed_face
# ---------------------------------------------------------------------------

print("== parity_fixed_face ==")
face = recognize_parity_fixed_face(
    request(
        "local_pole_order",
        germ_parity="even",
        fibre_dimension=2,
        radial_coefficient=1,
    )
)
check("even m = 2 face is recognized", face.candidate is not None)
assert face.candidate is not None
face_params = dict(face.candidate.route.ordered_steps[1].parameters)
check(
    "m = 2, B = 1 gives order-4 pole with coefficient -14",
    face_params["pole_order"] == 4 and face_params["leading_coefficient"] == Fraction(-14),
)
check(
    "decomposition m(m+5) = 6m + m(m-1) is recorded (12 + 2)",
    face_params["decomposition_terms"] == (12, 2),
)
check(
    "face certificates include first-principles Ricci replays",
    "first-principles-ricci-low-m"
    in {ob.obligation_id for ob in face.candidate.route.certificate_obligations},
)
check_refusal(
    "m = 0 refuses as flat (no pole)",
    recognize_parity_fixed_face(
        request("local_pole_order", germ_parity="even", fibre_dimension=0, radial_coefficient=1)
    ),
    "flat_no_pole",
)
check_refusal(
    "missing fibre dimension is refused",
    recognize_parity_fixed_face(
        request("local_pole_order", germ_parity="even", radial_coefficient=1)
    ),
    "missing_fibre_dimension",
)
check_refusal(
    "B = 0 refuses degenerate radial coefficient",
    recognize_parity_fixed_face(
        request("local_pole_order", germ_parity="even", fibre_dimension=2, radial_coefficient=0)
    ),
    "degenerate_radial_coefficient",
)
check_refusal(
    "odd germ parity is refused",
    recognize_parity_fixed_face(
        request("local_pole_order", germ_parity="odd", fibre_dimension=2, radial_coefficient=1)
    ),
    "germ_parity_not_even",
)
check_refusal(
    "wrong shape is refused",
    recognize_parity_fixed_face(
        request("real_decision", germ_parity="even", fibre_dimension=2, radial_coefficient=1)
    ),
    "shape_mismatch",
)

# ---------------------------------------------------------------------------
# extremal_face
# ---------------------------------------------------------------------------

print("== extremal_face ==")
extremal = recognize_extremal_face(
    request(
        "extremal_edge_pole",
        wedge_membership=True,
        collapse_coefficient_A2=Fraction(9, 4),
        transverse_log_derivative=Fraction(-3, 2),
    )
)
check("outer-wedge extremal edge is recognized", extremal.candidate is not None)
assert extremal.candidate is not None
edge_params = dict(extremal.candidate.route.ordered_steps[1].parameters)
check(
    "order-3 pole with R_ext = (-3/2)/(9/4) = -2/3 and negative sign recorded",
    edge_params["pole_order"] == 3
    and edge_params["leading_coefficient"] == Fraction(-2, 3)
    and edge_params["transverse_log_derivative_sign"] == "negative",
)
sturm_gate_params = dict(extremal.candidate.route.ordered_steps[2].parameters)
check(
    "sign gate cites the lead7_test8 Sturm certificates",
    sturm_gate_params["certificate_id"] == "lead7_test8"
    and any("2t^5 + 5t^4 - 15t^3" in item for item in sturm_gate_params["sturm_certificates"]),
)
check_refusal(
    "outside the physical wedge is refused",
    recognize_extremal_face(
        request(
            "extremal_edge_pole",
            wedge_membership=False,
            collapse_coefficient_A2=Fraction(9, 4),
            transverse_log_derivative=Fraction(-3, 2),
        )
    ),
    "outside_physical_wedge",
)
check_refusal(
    "A2 <= 0 is refused",
    recognize_extremal_face(
        request(
            "extremal_edge_pole",
            wedge_membership=True,
            collapse_coefficient_A2=-1,
            transverse_log_derivative=Fraction(-3, 2),
        )
    ),
    "nonpositive_A2",
)
check_refusal(
    "zero transverse derivative refuses toward the corner stratum",
    recognize_extremal_face(
        request(
            "extremal_edge_pole",
            wedge_membership=True,
            collapse_coefficient_A2=Fraction(9, 4),
            transverse_log_derivative=0,
        )
    ),
    "degenerate_transverse_derivative",
)
check_refusal(
    "wrong shape is refused",
    recognize_extremal_face(
        request(
            "local_pole_order",
            wedge_membership=True,
            collapse_coefficient_A2=Fraction(9, 4),
            transverse_log_derivative=Fraction(-3, 2),
        )
    ),
    "shape_mismatch",
)

# ---------------------------------------------------------------------------
# newton_wedge_corner
# ---------------------------------------------------------------------------

print("== newton_wedge_corner ==")
corner = recognize_newton_wedge_corner(
    request("corner_pole_order", corner_exponents=((1, 1), (2, 1), (1, 2)))
)
check("integer corner exponents are recognized", corner.candidate is not None)
assert corner.candidate is not None
vertex_params = dict(corner.candidate.route.ordered_steps[0].parameters)
check(
    "vertex coefficients A = B = 5 with all three polar vertices",
    vertex_params["vertex_coefficient_a"] == 5
    and vertex_params["vertex_coefficient_b"] == 5
    and vertex_params["polar_vertices"] == ((-4, -1), (-1, -4), (-1, -1)),
)
support_params = dict(corner.candidate.route.ordered_steps[1].parameters)
check(
    "support function values: balanced 5, axes 4 and 4",
    support_params["support_balanced_diagonal"] == 5
    and support_params["support_axis_x"] == 4
    and support_params["support_axis_y"] == 4,
)
check(
    "mixed-excess warning is a contract hypothesis",
    any("NOT the superposition" in item for item in corner.candidate.route.required_hypotheses),
)
check(
    "corner certificates include the vertex-coefficient closed form",
    "vertex-coefficient-closed-form"
    in {ob.obligation_id for ob in corner.candidate.route.certificate_obligations},
)
check_refusal(
    "missing corner exponents are refused",
    recognize_newton_wedge_corner(request("corner_pole_order")),
    "missing_corner_exponents",
)
check_refusal(
    "malformed exponent pairs are refused",
    recognize_newton_wedge_corner(
        request("corner_pole_order", corner_exponents=((1, 1, 1), (2, 1), (1, 2)))
    ),
    "missing_corner_exponents",
)
check_refusal(
    "wrong shape is refused",
    recognize_newton_wedge_corner(
        request("local_pole_order", corner_exponents=((1, 1), (2, 1), (1, 2)))
    ),
    "shape_mismatch",
)

# ---------------------------------------------------------------------------
# invariant_floor_real
# ---------------------------------------------------------------------------

print("== invariant_floor_real ==")
floor = recognize_invariant_floor_real(request("real_decision", claim_level="coefficient"))
check("coefficient-level claim stays on the coefficient floor", floor.candidate is not None)
assert floor.candidate is not None
check(
    "coefficient floor route never opens the spectrum",
    tuple(step.operation for step in floor.candidate.route.ordered_steps)
    == ("check_coefficient_invariants", "emit_coefficient_floor_route")
    and "precede root isolation"
    in dict(floor.candidate.route.ordered_steps[0].parameters)["invariant_floor"],
)
escalation = recognize_invariant_floor_real(request("real_decision", claim_level="root_order"))
check("root-order claim produces the escalation route", escalation.candidate is not None)
assert escalation.candidate is not None
check(
    "escalation declares sturm_escalation as the next route family",
    dict(escalation.candidate.route.ordered_steps[1].parameters)["next_route_family"]
    == "sturm_escalation",
)
check(
    "floor certificates include the Law 15 adequacy obligation",
    "observation-family-adequacy"
    in {ob.obligation_id for ob in floor.candidate.route.certificate_obligations},
)
check_refusal(
    "unknown claim level is refused",
    recognize_invariant_floor_real(request("real_decision", claim_level="spectral_intuition")),
    "unknown_claim_level",
)
check_refusal(
    "missing claim level is refused",
    recognize_invariant_floor_real(request("real_decision")),
    "unknown_claim_level",
)
check_refusal(
    "wrong shape is refused",
    recognize_invariant_floor_real(request("real_root_count", claim_level="coefficient")),
    "shape_mismatch",
)

# ---------------------------------------------------------------------------
# sturm_escalation
# ---------------------------------------------------------------------------

print("== sturm_escalation ==")
# H~(t) = 2t^5 + 5t^4 - 15t^3 - 7t^2 + 15t + 8, ascending coefficients, on (1, +infinity).
H_TILDE = (8, 15, -7, -15, 5, 2)
sturm = recognize_sturm_escalation(
    request("real_root_count", univariate_coefficients=H_TILDE, interval=(1, "+infinity"))
)
check("H~ root-count fixture is recognized", sturm.candidate is not None)
assert sturm.candidate is not None
count_params = dict(sturm.candidate.route.ordered_steps[1].parameters)
check(
    "H~ has zero distinct roots on (1, +infinity) (lead7_test8 positivity)",
    count_params["degree"] == 5 and count_params["distinct_real_roots_in_interval"] == 0,
)
check(
    "half-open counting convention is recorded",
    count_params["count_convention"] == "distinct roots in the half-open interval (a, b]",
)
decision_sturm = recognize_sturm_escalation(
    request(
        "real_decision",
        claim_level="root_order",
        univariate_coefficients=H_TILDE,
        interval=(1, "+infinity"),
    )
)
check(
    "real_decision at claim level root_order is also accepted",
    decision_sturm.candidate is not None,
)
check(
    "sturm certificates include exact chain replay",
    "sturm-chain-replay"
    in {ob.obligation_id for ob in sturm.candidate.route.certificate_obligations},
)
check_refusal(
    "missing polynomial is refused",
    recognize_sturm_escalation(request("real_root_count", interval=(1, "+infinity"))),
    "missing_polynomial",
)
check_refusal(
    "constant polynomial is refused",
    recognize_sturm_escalation(request("real_root_count", univariate_coefficients=(8,))),
    "missing_polynomial",
)
check_refusal(
    "wrong shape is refused",
    recognize_sturm_escalation(
        request("pencil_selection", univariate_coefficients=H_TILDE)
    ),
    "shape_mismatch",
)

# ---------------------------------------------------------------------------
# matrix_pencil_selection
# ---------------------------------------------------------------------------

print("== matrix_pencil_selection ==")
pencil = recognize_matrix_pencil_selection(
    request(
        "pencil_selection",
        pencil_members=("u=-1", "u=0", "u=1"),
        member_interior_regular=(True, True, False),
        member_positive_definite=(False, True, True),
        symmetric_matrix=((2, 0), (0, 3)),
    )
)
check("unique admissible member u=0 is recognized", pencil.candidate is not None)
assert pencil.candidate is not None
check(
    "the selected member is u=0",
    dict(pencil.candidate.route.ordered_steps[2].parameters)["selected_member"] == "u=0",
)
check(
    "pencil certificates include the complementarity law",
    "complementarity-law"
    in {ob.obligation_id for ob in pencil.candidate.route.certificate_obligations},
)
check_refusal(
    "two admissible members refuse: selection not unique",
    recognize_matrix_pencil_selection(
        request(
            "pencil_selection",
            pencil_members=("u=-1", "u=0", "u=1"),
            member_interior_regular=(True, True, False),
            member_positive_definite=(True, True, False),
            symmetric_matrix=((2, 0), (0, 3)),
        )
    ),
    "selection_not_unique",
)
check_refusal(
    "zero admissible members refuse: selection not unique",
    recognize_matrix_pencil_selection(
        request(
            "pencil_selection",
            pencil_members=("u=-1", "u=0", "u=1"),
            member_interior_regular=(False, False, False),
            member_positive_definite=(True, True, True),
            symmetric_matrix=((2, 0), (0, 3)),
        )
    ),
    "selection_not_unique",
)
check_refusal(
    "mismatched member declarations are malformed",
    recognize_matrix_pencil_selection(
        request(
            "pencil_selection",
            pencil_members=("u=-1", "u=0", "u=1"),
            member_interior_regular=(True, True),
            member_positive_definite=(False, True, True),
            symmetric_matrix=((2, 0), (0, 3)),
        )
    ),
    "malformed_pencil_declaration",
)
check_refusal(
    "missing definiteness evidence is refused",
    recognize_matrix_pencil_selection(
        request(
            "pencil_selection",
            pencil_members=("u=-1", "u=0", "u=1"),
            member_interior_regular=(True, True, False),
            member_positive_definite=(False, True, True),
        )
    ),
    "missing_definiteness_evidence",
)
check_refusal(
    "wrong shape is refused",
    recognize_matrix_pencil_selection(
        request(
            "symmetric_inertia",
            pencil_members=("u=0",),
            member_interior_regular=(True,),
            member_positive_definite=(True,),
            symmetric_matrix=((2, 0), (0, 3)),
        )
    ),
    "shape_mismatch",
)

# ---------------------------------------------------------------------------
# exact_rational_inertia
# ---------------------------------------------------------------------------

print("== exact_rational_inertia ==")
# The coupling metric 2I - J for n = 3: signature (2, 1), zero nullity.
TWO_I_MINUS_J = ((1, -1, -1), (-1, 1, -1), (-1, -1, 1))
inertia = recognize_exact_rational_inertia(
    request("symmetric_inertia", symmetric_matrix=TWO_I_MINUS_J)
)
check("2I - J inertia fixture is recognized", inertia.candidate is not None)
assert inertia.candidate is not None
pivot_params = dict(inertia.candidate.route.ordered_steps[0].parameters)
check(
    "2I - J has congruence inertia (2, 1, 0)",
    pivot_params["positive"] == 2 and pivot_params["negative"] == 1 and pivot_params["nullity"] == 0,
)
check(
    "no floating eigendecomposition is admitted",
    "no floating eigendecomposition" in pivot_params["pivot_rule"],
)
check(
    "classification is INERTIA_CERTIFIED_WITH_NULLITY(rank=3, signature=1, nullity=0)",
    dict(inertia.candidate.route.ordered_steps[1].parameters)["classification"]
    == "INERTIA_CERTIFIED_WITH_NULLITY(rank=3, signature=1, nullity=0)",
)
check(
    "kappa_s trap is recorded in the contract hypotheses",
    any("naive mirror formula" in item for item in inertia.candidate.route.required_hypotheses),
)
check(
    "HIGHER_JET_REQUIRED_FOR_CLASSIFICATION stays in the exceptional branches",
    any(
        "HIGHER_JET_REQUIRED_FOR_CLASSIFICATION" in branch
        for branch in inertia.candidate.route.exceptional_branches
    ),
)
check(
    "inertia certificates include Sylvester replay and the monomial partition",
    {"sylvester-law-replay", "monomial-partition-cross-check"}
    <= {ob.obligation_id for ob in inertia.candidate.route.certificate_obligations},
)
check_refusal(
    "missing symmetric matrix is refused",
    recognize_exact_rational_inertia(request("symmetric_inertia")),
    "missing_symmetric_matrix",
)
check_refusal(
    "asymmetric matrix is refused",
    recognize_exact_rational_inertia(
        request("symmetric_inertia", symmetric_matrix=((1, 2), (3, 4)))
    ),
    "missing_symmetric_matrix",
)
check_refusal(
    "declared q = 0 gradient refuses (never returns 0)",
    recognize_exact_rational_inertia(
        request("symmetric_inertia", symmetric_matrix=TWO_I_MINUS_J, gradient=(0, 0, 0))
    ),
    "singular_stratum_q_zero",
)
check_refusal(
    "wrong shape is refused",
    recognize_exact_rational_inertia(
        request("pencil_selection", symmetric_matrix=TWO_I_MINUS_J)
    ),
    "shape_mismatch",
)

# ---------------------------------------------------------------------------
# Provider tuples: contracts, scouts, and route-only discipline.
# ---------------------------------------------------------------------------

print("== provider tuples ==")
check(
    "twelve providers are declared across the three modules",
    len(ALL_FAMILIES) == 12 and len(set(ALL_FAMILIES)) == 12,
)
for provider in CURVATURE_PROVIDERS + LOCAL_GERM_PROVIDERS + REAL_PROVIDERS:
    contract = provider.contract
    check(
        f"{provider.route_family}: contract cites sources and certificate obligations",
        bool(contract.source_references) and bool(contract.certificate_obligations),
    )
check(
    "curvature providers attach the regularity scout",
    all(len(provider.native_scouts) >= 1 for provider in CURVATURE_PROVIDERS),
)


print()
if FAILS:
    print(f"GATE PATHFINDER PROVIDERS GEOMETRY: OPEN ({len(FAILS)} failing)")
    raise SystemExit(1)
print("GATE PATHFINDER PROVIDERS GEOMETRY: CLOSED")
