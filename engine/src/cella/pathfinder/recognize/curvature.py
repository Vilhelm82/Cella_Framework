"""DBP curvature route-family providers.

Families: ``canonical_invariant_reduction``, ``dbp_role_orbit_reduction``,
``curvature_role_orbit``, ``gauge_channel_transport``.

Recognition is exact-rational only: context numbers arrive as ``int`` or
``fractions.Fraction`` (floats are outside the canonical value domain and
``bool`` is not a number).  Refusals are mathematical, never implementation
gaps.  No host deliverable is computed here: coupling numerators, q0, and the
orbit-separation Jacobian below are admissibility evidence and route
parameters, never the requested curvature account itself.

Corpus regularity rule: refuse ``singular_stratum_q_zero`` when q = g^T g = 0
(refuse, do not divide).  A single vanishing gradient component with q != 0 is
a normal-coordinate chart boundary, not a singular stratum; it stays in the
exceptional branches.
"""

from __future__ import annotations

from fractions import Fraction

from ..api.contract import RecognitionOutcome, RouteContract
from ..api.request import PathfinderRequest
from ..api.route import RouteStep
from ..ir.burden import BurdenVector
from ..ir.obligation import Obligation
from ..ir.problem import lower_request
from ..ir.values import FrozenValue, freeze_mapping
from ..plan.admissibility import evidence_by_family, family_enabled, lookup, refuse, require_shape
from ..plan.assemble import assemble_candidate
from ..plan.registry import RouteProvider
from ..scout.regularity import regularity_scout


# ---------------------------------------------------------------------------
# Exact-rational validation helpers (no floats anywhere).
# ---------------------------------------------------------------------------


def _rational(value: FrozenValue | None) -> Fraction | None:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        return None
    return Fraction(value)


def _rational_tuple(
    value: FrozenValue | None,
    expected_length: int | None = None,
) -> tuple[Fraction, ...] | None:
    if not isinstance(value, tuple) or not value:
        return None
    if expected_length is not None and len(value) != expected_length:
        return None
    entries: list[Fraction] = []
    for entry in value:
        rational = _rational(entry)
        if rational is None:
            return None
        entries.append(rational)
    return tuple(entries)


def _symmetric_matrix(
    value: FrozenValue | None,
    size: int,
) -> tuple[tuple[Fraction, ...], ...] | None:
    if not isinstance(value, tuple) or len(value) != size or size == 0:
        return None
    rows: list[tuple[Fraction, ...]] = []
    for raw_row in value:
        row = _rational_tuple(raw_row, size)
        if row is None:
            return None
        rows.append(row)
    for i in range(size):
        for j in range(i):
            if rows[i][j] != rows[j][i]:
                return None
    return tuple(rows)


def _regularity_fingerprint(request: PathfinderRequest) -> dict[str, FrozenValue] | None:
    """dbp_regularity evidence, or a fresh native regularity_scout run."""

    evidence = evidence_by_family(request, "dbp_regularity")
    if evidence is not None:
        return evidence
    result = regularity_scout(lower_request(request), request.analysis_budget)
    if result is None:
        return None
    return dict(result.structural_fingerprint)


# ---------------------------------------------------------------------------
# canonical_invariant_reduction
# ---------------------------------------------------------------------------

CANONICAL_INVARIANT_CERTIFICATES = (
    Obligation(
        "kc1-gauge-invariance",
        "KC1: sigma_r is invariant under defining-function gauge changes mu*F with mu(x) = 1.",
        "exact-identity-replay",
    ),
    Obligation(
        "kc2-zero-sum-residue",
        "KC2: the channel residue of the reduction sums to zero inside ker Sigma.",
        "exact-identity-replay",
    ),
    Obligation(
        "kc5-rational-numerator",
        "KC5: the normalized invariant numerator is exactly rational for the declared parity.",
        "exact-rational",
    ),
    Obligation(
        "channel-additivity",
        "sigma_r equals the exact sum of its channel-account entries.",
        "exact-identity-replay",
    ),
    Obligation(
        "bordered-det-cross-check",
        "det(H_b) = Delta_c + Delta_s + Delta_m as an exact disjoint monomial partition.",
        "exact-identity-replay",
    ),
)

CANONICAL_INVARIANT_CONTRACT = RouteContract(
    route_family="canonical_invariant_reduction",
    accepted_problem_shape="curvature_invariant",
    required_hypotheses=(
        "q = g^T g != 0 (regular DBP stratum)",
        "privileged DBP basis with H = H_s + H_c, H_s = diag(H)",
        "invariant order r satisfies 1 <= r <= n-1",
        "exact rational gradient and symmetric Hessian",
    ),
    required_evidence=("dbp_regularity scout evidence", "exact gradient and Hessian context"),
    produced_obligations=(
        Obligation(
            "execute-canonical-invariant-reduction",
            "Execute the bordered-minor/Vandermonde reduction and emit sigma_r with its channel account.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "g_i = 0 normal-coordinate boundary: a vanishing gradient component with q != 0 is a chart boundary, not a singular stratum",
        "umbilic locus: the channel account degenerates while sigma_r remains valid",
        "higher interaction orders for n > 3 must not be collapsed into a single interaction channel",
    ),
    execution_module="external.canonical_invariant_reduction_executor",
    certificate_obligations=CANONICAL_INVARIANT_CERTIFICATES,
    source_references=(
        "Reference_Material/papers/current/Canonical_Invariant_Reduction_Theorem.md",
        "CELLA_ARCHITECTURE_v1.3.md#17.1",
    ),
)


def recognize_canonical_invariant_reduction(request: PathfinderRequest) -> RecognitionOutcome:
    family = CANONICAL_INVARIANT_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        require_shape(request, family, CANONICAL_INVARIANT_CONTRACT.accepted_problem_shape),
    ):
        if gate is not None:
            return gate

    fingerprint = _regularity_fingerprint(request)
    if fingerprint is None:
        return refuse(
            family,
            "non_rational_input",
            "The gradient must be declared as a non-empty tuple of exact int/Fraction values.",
            "exact rational gradient",
        )
    q = _rational(fingerprint.get("q"))
    if q is None:
        return refuse(
            family,
            "non_rational_input",
            "The regularity evidence does not carry an exact rational q = g^T g.",
            "exact rational q",
        )
    if q == 0:
        return refuse(
            family,
            "singular_stratum_q_zero",
            "q = g^T g = 0 is the singular stratum: refuse, do not divide.",
            "q != 0",
        )
    dimension = fingerprint.get("dimension")
    if isinstance(dimension, bool) or not isinstance(dimension, int) or dimension < 1:
        return refuse(
            family,
            "non_rational_input",
            "The regularity evidence does not carry an exact gradient dimension.",
            "gradient dimension",
        )

    hessian = _symmetric_matrix(lookup(request.mathematical_context, "hessian"), dimension)
    if hessian is None:
        return refuse(
            family,
            "non_rational_input",
            "The Hessian must be an exactly symmetric n x n tuple-of-tuples of int/Fraction "
            f"with n = {dimension}.",
            "exact symmetric rational Hessian",
        )

    order = lookup(request.mathematical_context, "invariant_order")
    if isinstance(order, bool) or not isinstance(order, int) or not 1 <= order <= dimension - 1:
        return refuse(
            family,
            "invariant_order_out_of_range",
            f"The invariant order must be an integer r with 1 <= r <= n-1 = {dimension - 1}.",
            "1 <= invariant_order <= n-1",
        )

    parity_even = order % 2 == 0
    steps = (
        RouteStep(
            "form-bordered-minors",
            "form_bordered_channel_minors",
            ("gradient", "hessian"),
            ("bordered_minor_family",),
            freeze_mapping({"subset_size": order + 1, "dimension": dimension, "q": q}),
        ),
        RouteStep(
            "vandermonde-split",
            "vandermonde_channel_split",
            ("bordered_minor_family",),
            ("channel_vector",),
            freeze_mapping({"nodes": tuple(range(order + 1))}),
        ),
        RouteStep(
            "sum-channels",
            "sum_channels_to_invariant",
            ("channel_vector",),
            ("invariant_sigma_r",),
            freeze_mapping(
                {
                    "invariant_order": order,
                    "normalization": "q^((r+2)/2)",
                    "parity_law": "r even -> sigma_r rational; r odd -> sigma_r in QQ(sqrt(q))",
                    "parity": "even" if parity_even else "odd",
                    "value_field": "QQ" if parity_even else "QQ(sqrt(q))",
                }
            ),
        ),
        RouteStep(
            "emit-invariant-account",
            "emit_invariant_and_channel_account",
            ("invariant_sigma_r", "channel_vector"),
            ("host_invariant_and_channel_account",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=CANONICAL_INVARIANT_CONTRACT,
        steps=steps,
        data_dependencies=("gradient", "hessian", "invariant_order"),
        required_intermediate_objects=("bordered_minor_family", "channel_vector", "invariant_sigma_r"),
        completion_condition=(
            "The external executor emits sigma_r and its channel account in host bindings."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=order + 2,
            scout_operation_count=dimension,
            expression_depth=2,
        ),
        structural_preference_rank=0,
    )


# ---------------------------------------------------------------------------
# dbp_role_orbit_reduction
# ---------------------------------------------------------------------------

ROLE_ORBIT_CERTIFICATES = (
    Obligation(
        "s3-group-relations",
        "The birational actions satisfy s^2 = t^2 = (s*t)^3 = e exactly on the admitted locus.",
        "exact-identity-replay",
    ),
    Obligation(
        "orbit-separation-jacobian",
        "det dO/d(A,B,C) = 8*Lambda_P*Lambda_D*Lambda_S/q0^6 is nonzero (orbit separation).",
        "exact-rational",
    ),
    Obligation(
        "orbit-completeness",
        "The invariance test covers the complete six-element S3 orbit required by the application's claim.",
        "finite-exact-enumeration",
    ),
)

ROLE_ORBIT_CONTRACT = RouteContract(
    route_family="dbp_role_orbit_reduction",
    accepted_problem_shape="role_orbit_invariance",
    required_hypotheses=(
        "regular active-role locus Omega_1 = {F = 0, F_D*F_S*F_P != 0}",
        "graph form with a = f_D != 0 and b = f_S != 0",
        "exact rational order-2 jet (a, b, A, B, C)",
        "passive S_n recharting acts trivially; only active recharting is nontrivial",
    ),
    required_evidence=("exact rational jet context", "nonzero coupling numerators Lambda_P, Lambda_D, Lambda_S"),
    produced_obligations=(
        Obligation(
            "execute-role-orbit-reduction",
            "Transport the jet through the S3 action and emit the orbit-invariance obligations.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "coordinate not solvable as an output role requires a different chart",
        "normal coordinate vanishing leaves the graph-form hypotheses",
        "curvature denominator degeneration leaves the regular role locus",
    ),
    execution_module="external.dbp_role_orbit_executor",
    certificate_obligations=ROLE_ORBIT_CERTIFICATES,
    source_references=(
        "Reference_Material/papers/current/dbp_orbit_calculus.tex#thm:orbit",
        "CELLA_ARCHITECTURE_v1.3.md#17.1",
    ),
)

_S3_ACTION_PARAMETERS = {
    "s_action": "s(a,b) = (b,a)",
    "t_action": "t(a,b) = (1/a, -b/a)",
    "s_second_order": "(a,b,A,B,C) -> (b, a, C, B, A)",
    "t_second_order": (
        "(a,b,A,B,C) -> (1/a, -b/a, -A/a^3, (A*b - a*B)/a^3, (-A*b^2 + 2*a*b*B - a^2*C)/a^3)"
    ),
    "group_relations": "s^2 = t^2 = (s*t)^3 = e",
}


def _admit_jet(
    request: PathfinderRequest,
    family: str,
) -> tuple[Fraction, ...] | RecognitionOutcome:
    """Validate the order-2 jet (a, b, A, B, C) shared by the orbit families."""

    jet = _rational_tuple(lookup(request.mathematical_context, "jet"), 5)
    if jet is None:
        return refuse(
            family,
            "non_rational_input",
            "The jet must be declared as an exact 5-tuple (a, b, A, B, C) of int/Fraction values.",
            "exact rational jet (a, b, A, B, C)",
        )
    if jet[0] == 0 or jet[1] == 0:
        return refuse(
            family,
            "output_chart_absent",
            "a = 0 or b = 0: the output-role graph chart is absent on this locus.",
            "a != 0",
            "b != 0",
        )
    # Corpus regularity: honor declared gradient evidence when present.
    fingerprint = _regularity_fingerprint(request)
    if fingerprint is not None:
        q = _rational(fingerprint.get("q"))
        if q is not None and q == 0:
            return refuse(
                family,
                "singular_stratum_q_zero",
                "q = g^T g = 0 is the singular stratum: refuse, do not divide.",
                "q != 0",
            )
    return jet


def recognize_dbp_role_orbit_reduction(request: PathfinderRequest) -> RecognitionOutcome:
    family = ROLE_ORBIT_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        require_shape(request, family, ROLE_ORBIT_CONTRACT.accepted_problem_shape),
    ):
        if gate is not None:
            return gate

    admitted = _admit_jet(request, family)
    if isinstance(admitted, RecognitionOutcome):
        return admitted
    a, b, jet_a, jet_b, jet_c = admitted

    lambda_p = jet_b
    lambda_d = (jet_a * b - a * jet_b) / a
    lambda_s = (jet_c * a - b * jet_b) / b
    if lambda_p * lambda_d * lambda_s == 0:
        return refuse(
            family,
            "channel_isotropy_locus",
            "Lambda_P * Lambda_D * Lambda_S = 0: the channel-isotropy locus separates no orbit.",
            "Lambda_P != 0",
            "Lambda_D != 0",
            "Lambda_S != 0",
        )
    q0 = 1 + a * a + b * b
    jacobian = 8 * lambda_p * lambda_d * lambda_s / q0**6

    steps = (
        RouteStep(
            "restrict-regular-locus",
            "restrict_to_regular_role_locus",
            ("jet",),
            ("regular_role_jet",),
            freeze_mapping(
                {
                    "locus": "F = 0 and F_P*F_D*F_S != 0",
                    "lambda_p": lambda_p,
                    "lambda_d": lambda_d,
                    "lambda_s": lambda_s,
                    "q0": q0,
                }
            ),
        ),
        RouteStep(
            "transport-s3",
            "transport_jet_through_s3_action",
            ("regular_role_jet",),
            ("s3_jet_orbit",),
            freeze_mapping(_S3_ACTION_PARAMETERS),
        ),
        RouteStep(
            "test-orbit-constancy",
            "test_orbit_constancy",
            ("s3_jet_orbit",),
            ("orbit_constancy_report",),
            freeze_mapping({"jacobian_determinant": jacobian, "orbit_size": 6}),
        ),
        RouteStep(
            "emit-orbit-obligations",
            "emit_orbit_invariance_obligations",
            ("orbit_constancy_report",),
            ("host_orbit_invariance_obligations",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=ROLE_ORBIT_CONTRACT,
        steps=steps,
        data_dependencies=("jet",),
        required_intermediate_objects=("regular_role_jet", "s3_jet_orbit", "orbit_constancy_report"),
        completion_condition=(
            "The external executor certifies orbit constancy and emits the invariance obligations "
            "in host bindings."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=6,
            scout_operation_count=1,
            expression_depth=2,
        ),
        structural_preference_rank=0,
    )


# ---------------------------------------------------------------------------
# curvature_role_orbit
# ---------------------------------------------------------------------------

ROLE_SPECTRUM_CERTIFICATES = (
    Obligation(
        "shared-k-identities",
        "All three output-role spectra share K = (A*C - B^2)/q0^2 via the exact channel identities.",
        "exact-identity-replay",
    ),
    Obligation(
        "anisotropy-norm-identity",
        "The anisotropy satisfies the standard-irrep norm identity A_c = 3*||P2 O||^2.",
        "exact-identity-replay",
    ),
    Obligation(
        "retrodiction-anchor",
        "External replay of the anchor a=5, b=7, A=2, B=3, C=4 yields q0 = 75 and K = -1/5625.",
        "external-replay",
    ),
)

ROLE_SPECTRUM_CONTRACT = RouteContract(
    route_family="curvature_role_orbit",
    accepted_problem_shape="role_curvature_spectrum",
    required_hypotheses=(
        "a != 0 and b != 0 (all three output-role charts exist)",
        "exact rational order-2 jet (a, b, A, B, C)",
        "shared-K consistency identity A*(A*b^2 - 2*a*b*B + a^2*C) - (A*b - a*B)^2 = a^2*(A*C - B^2)",
    ),
    required_evidence=("exact rational jet context",),
    produced_obligations=(
        Obligation(
            "execute-role-curvature-spectrum",
            "Read the three fixed closed-form channel spectra and emit the role spectrum.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "channel isotropy Lambda_rho = 0 degenerates the corresponding role spectrum entry",
        "a = 0 or b = 0 removes an output chart and requires another route",
    ),
    execution_module="external.curvature_role_orbit_executor",
    certificate_obligations=ROLE_SPECTRUM_CERTIFICATES,
    source_references=(
        "Reference_Material/papers/current/dbp_orbit_calculus.tex#thm:orbit",
        "CELLA_ARCHITECTURE_v1.3.md#17.1",
    ),
)

_CHANNEL_SPECTRA_FORMULAS = {
    "C_P": "(K, -B^2/q0^2, A*C/q0^2, 0)",
    "C_D": "(K, -(A*b - a*B)^2/(a^2*q0^2), A*(A*b^2 - 2*a*b*B + a^2*C)/(a^2*q0^2), 0)",
    "C_S": "(K, -(C*a - b*B)^2/(b^2*q0^2), C*(C*a^2 - 2*a*b*B + b^2*A)/(b^2*q0^2), 0)",
}


def recognize_curvature_role_orbit(request: PathfinderRequest) -> RecognitionOutcome:
    family = ROLE_SPECTRUM_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        require_shape(request, family, ROLE_SPECTRUM_CONTRACT.accepted_problem_shape),
    ):
        if gate is not None:
            return gate

    admitted = _admit_jet(request, family)
    if isinstance(admitted, RecognitionOutcome):
        return admitted
    a, b, jet_a, jet_b, jet_c = admitted

    q0 = 1 + a * a + b * b
    shared_k = (jet_a * jet_c - jet_b * jet_b) / q0**2

    # Shared-K consistency identity (theorem guard, exact Fractions).
    lhs = jet_a * (jet_a * b * b - 2 * a * b * jet_b + a * a * jet_c) - (jet_a * b - a * jet_b) ** 2
    rhs = a * a * (jet_a * jet_c - jet_b * jet_b)
    if lhs != rhs:
        return refuse(
            family,
            "inconsistent_jet_data",
            "The shared-K identity A*(A*b^2 - 2*a*b*B + a^2*C) - (A*b - a*B)^2 = a^2*(A*C - B^2) fails.",
            "shared-K consistency identity",
        )
    # A wrapper-declared shared K must satisfy the same identity exactly.
    declared_k = lookup(request.mathematical_context, "declared_shared_K")
    if declared_k is not None:
        declared_rational = _rational(declared_k)
        if declared_rational is None:
            return refuse(
                family,
                "non_rational_input",
                "declared_shared_K must be an exact int/Fraction value.",
                "exact rational declared_shared_K",
            )
        if declared_rational * q0**2 != jet_a * jet_c - jet_b * jet_b:
            return refuse(
                family,
                "inconsistent_jet_data",
                "The declared shared K does not satisfy K*q0^2 = A*C - B^2 for the declared jet.",
                "declared_shared_K = (A*C - B^2)/q0^2",
            )

    steps = (
        RouteStep(
            "solve-output-roles",
            "solve_relation_in_each_output_role",
            ("jet",),
            ("role_relations",),
            freeze_mapping({"roles": ("P", "D", "S")}),
        ),
        RouteStep(
            "graph-normalize",
            "graph_normalize_charts",
            ("role_relations",),
            ("normalized_role_charts",),
        ),
        RouteStep(
            "read-channel-spectra",
            "read_channel_spectra",
            ("normalized_role_charts",),
            ("role_channel_spectra",),
            freeze_mapping(
                {
                    **_CHANNEL_SPECTRA_FORMULAS,
                    "q0": q0,
                    "shared_K": shared_k,
                    "retrodiction_anchor": "a=5, b=7, A=2, B=3, C=4 -> q0=75, K=-1/5625",
                }
            ),
        ),
        RouteStep(
            "emit-role-spectrum",
            "emit_role_spectrum_route",
            ("role_channel_spectra",),
            ("host_role_curvature_spectrum",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=ROLE_SPECTRUM_CONTRACT,
        steps=steps,
        data_dependencies=("jet",),
        required_intermediate_objects=("role_relations", "normalized_role_charts", "role_channel_spectra"),
        completion_condition=(
            "The external executor emits the three-role curvature spectrum in host bindings."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=5,
            scout_operation_count=1,
            expression_depth=2,
        ),
        structural_preference_rank=0,
    )


# ---------------------------------------------------------------------------
# gauge_channel_transport
# ---------------------------------------------------------------------------

GAUGE_TRANSPORT_CERTIFICATES = (
    Obligation(
        "kc1-invariant-preservation",
        "KC1: every sigma_r is preserved under H~ = H + g*a^T + a*g^T with mu(x) = 1.",
        "exact-identity-replay",
    ),
    Obligation(
        "kc2-channel-shift-kernel",
        "KC2: the channel shift lies strictly inside ker Sigma (n = 3: sum of delta kappa = 0).",
        "exact-identity-replay",
    ),
    Obligation(
        "kc6-single-edge-law",
        "KC6: with exactly one nonzero coupling edge H_ij = h, delta_kappa_c = 4*t*g1*g2*g3*h/q^2.",
        "exact-identity-replay",
    ),
    Obligation(
        "four-gauge-retrodiction",
        "The four-gauge retrodiction table replays exactly (keystone transport triple sums to -3/49).",
        "external-replay",
    ),
)

GAUGE_TRANSPORT_CONTRACT = RouteContract(
    route_family="gauge_channel_transport",
    accepted_problem_shape="gauge_transport",
    required_hypotheses=(
        "q = g^T g != 0",
        "gauge normalization mu(x) = 1, a = grad log mu at the base point",
        "exact rational gradient, Hessian, and gauge vector",
        "the single-edge law applies only with exactly one nonzero coupling edge",
    ),
    required_evidence=("dbp_regularity scout evidence", "exact gauge vector context"),
    produced_obligations=(
        Obligation(
            "execute-gauge-channel-transport",
            "Apply the rank-two Hessian update and emit the transported channel account.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "Lorentzian null (gauge-rigid) directions of 2I - J admit no channel reallocation",
        "prod(g) = 0 boundary degenerates the single-edge law",
    ),
    execution_module="external.gauge_channel_transport_executor",
    certificate_obligations=GAUGE_TRANSPORT_CERTIFICATES,
    source_references=(
        "Reference_Material/papers/current/Gauge_Channel_Transport_Law.md",
        "CELLA_ARCHITECTURE_v1.3.md#17.1",
    ),
)


def recognize_gauge_channel_transport(request: PathfinderRequest) -> RecognitionOutcome:
    family = GAUGE_TRANSPORT_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        require_shape(request, family, GAUGE_TRANSPORT_CONTRACT.accepted_problem_shape),
    ):
        if gate is not None:
            return gate

    fingerprint = _regularity_fingerprint(request)
    if fingerprint is None:
        return refuse(
            family,
            "non_rational_input",
            "The gradient must be declared as a non-empty tuple of exact int/Fraction values.",
            "exact rational gradient",
        )
    q = _rational(fingerprint.get("q"))
    if q is None:
        return refuse(
            family,
            "non_rational_input",
            "The regularity evidence does not carry an exact rational q = g^T g.",
            "exact rational q",
        )
    if q == 0:
        return refuse(
            family,
            "singular_stratum_q_zero",
            "q = g^T g = 0 is the singular stratum: refuse, do not divide.",
            "q != 0",
        )
    dimension = fingerprint.get("dimension")
    if isinstance(dimension, bool) or not isinstance(dimension, int) or dimension < 1:
        return refuse(
            family,
            "non_rational_input",
            "The regularity evidence does not carry an exact gradient dimension.",
            "gradient dimension",
        )

    hessian = _symmetric_matrix(lookup(request.mathematical_context, "hessian"), dimension)
    if hessian is None:
        return refuse(
            family,
            "non_rational_input",
            "The Hessian must be an exactly symmetric n x n tuple-of-tuples of int/Fraction "
            f"with n = {dimension}.",
            "exact symmetric rational Hessian",
        )

    raw_gauge = lookup(request.mathematical_context, "gauge_vector")
    if not isinstance(raw_gauge, tuple) or len(raw_gauge) != dimension:
        return refuse(
            family,
            "missing_gauge_vector",
            f"The gauge vector must be declared as a length-{dimension} tuple.",
            "gauge_vector of gradient length",
        )
    gauge = _rational_tuple(raw_gauge, dimension)
    if gauge is None:
        return refuse(
            family,
            "non_rational_input",
            "Every gauge-vector entry must be an exact int/Fraction value.",
            "exact rational gauge vector",
        )

    steps = (
        RouteStep(
            "rank-two-update",
            "apply_rank_two_hessian_update",
            ("gradient", "hessian", "gauge_vector"),
            ("transported_hessian",),
            freeze_mapping({"identity": "H~ = H + g a^T + a g^T", "q": q}),
        ),
        RouteStep(
            "verify-invariants",
            "verify_invariant_preservation",
            ("transported_hessian",),
            ("invariant_preservation_report",),
            freeze_mapping(
                {
                    "preserved": "every sigma_r, 1 <= r <= n-1",
                    "channel_shift": "strictly inside ker Sigma",
                }
            ),
        ),
        RouteStep(
            "classify-shift",
            "classify_channel_shift",
            ("invariant_preservation_report",),
            ("channel_shift_classification",),
            freeze_mapping(
                {
                    "lorentzian_form": "2*|nu|^2 - (1.nu)^2 signature (2,1)",
                    "nu": "(g1*H23, g2*H13, g3*H12)",
                    "gauge_null_direction_n3": "(1, 1, -2)",
                }
            ),
        ),
        RouteStep(
            "emit-gauge-transport",
            "emit_gauge_transport_route",
            ("channel_shift_classification",),
            ("host_gauge_transport_account",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=GAUGE_TRANSPORT_CONTRACT,
        steps=steps,
        data_dependencies=("gradient", "hessian", "gauge_vector"),
        required_intermediate_objects=(
            "transported_hessian",
            "invariant_preservation_report",
            "channel_shift_classification",
        ),
        completion_condition=(
            "The external executor emits the transported channel account in host bindings."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=4,
            scout_operation_count=dimension,
            expression_depth=2,
        ),
        structural_preference_rank=0,
    )


PROVIDERS = (
    RouteProvider(
        route_family="canonical_invariant_reduction",
        contract=CANONICAL_INVARIANT_CONTRACT,
        recognizer=recognize_canonical_invariant_reduction,
        native_scouts=(regularity_scout,),
        wrapper_capabilities=("bordered_minor_formation", "vandermonde_solve"),
    ),
    RouteProvider(
        route_family="dbp_role_orbit_reduction",
        contract=ROLE_ORBIT_CONTRACT,
        recognizer=recognize_dbp_role_orbit_reduction,
        native_scouts=(regularity_scout,),
        wrapper_capabilities=("birational_jet_transport", "orbit_constancy_test"),
    ),
    RouteProvider(
        route_family="curvature_role_orbit",
        contract=ROLE_SPECTRUM_CONTRACT,
        recognizer=recognize_curvature_role_orbit,
        native_scouts=(regularity_scout,),
        wrapper_capabilities=("graph_chart_normalization", "closed_form_spectrum_readout"),
    ),
    RouteProvider(
        route_family="gauge_channel_transport",
        contract=GAUGE_TRANSPORT_CONTRACT,
        recognizer=recognize_gauge_channel_transport,
        native_scouts=(regularity_scout,),
        wrapper_capabilities=("rank_two_symmetric_update", "lorentzian_sign_classification"),
    ),
)
