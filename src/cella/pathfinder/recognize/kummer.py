"""Kummer square-class route-family providers.

Four route families from the horizon wreath corpus:

- ``kummer_square_class_independence`` — valuation-separation theorem
  (KUMMER_MODULE_WREATH_LIFT Thm 4.1): full F2 column rank of the
  valuation-parity matrix forces R = 0 and rho = sd.
- ``valuation_parity_lower_bound`` — stacked odd-valuation rows certify a
  LOWER BOUND on the square-class module rank; never an upper bound.
- ``rotating_kummer_rank_jump`` — private-prime rank jump over F(J)
  (ROTATING_KUMMER_RANK_JUMP Thm 3.1) under imported certificates H1-H4.
- ``kummer_finite_extension_primeness`` — the P4/IZ primeness route
  (ROTATING_THREE_CHANNEL Lemma 4.1): derivative-gcd squarefreeness plus
  constant-difference coprimeness replace irreducibility testing.

This module emits route instructions and certificate obligations only; it
never executes the deliverable and never returns a final answer.
"""

from __future__ import annotations

from ..api.contract import RecognitionOutcome, RouteContract
from ..api.request import PathfinderRequest
from ..api.route import RouteStep
from ..ir.burden import BurdenVector
from ..ir.obligation import Obligation
from ..ir.problem import lower_request
from ..ir.values import FrozenValue, freeze_mapping
from ..plan.admissibility import (
    evidence_by_family,
    family_enabled,
    lookup,
    refuse,
    require_odd_characteristic,
)
from ..plan.assemble import assemble_candidate
from ..plan.registry import RouteProvider
from ..scout.algebra import sign_orbit_scout
from ..scout.kummer import parity_matrix_scout


def _accept_shape(
    request: PathfinderRequest,
    route_family: str,
    accepted_shapes: tuple[str, ...],
) -> RecognitionOutcome | None:
    shape = lookup(request.mathematical_context, "problem_shape")
    if shape not in accepted_shapes:
        return refuse(
            route_family,
            "shape_mismatch",
            "The task does not declare one of the accepted problem shapes: "
            + ", ".join(repr(item) for item in accepted_shapes)
            + ".",
            *accepted_shapes,
        )
    return None


def _is_exact_int(value: FrozenValue | None) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _parity_fingerprint(request: PathfinderRequest) -> dict[str, FrozenValue] | None:
    """Supplied kummer_parity_matrix evidence, else the native scout's."""

    supplied = evidence_by_family(request, "kummer_parity_matrix")
    if supplied is not None:
        return supplied
    evidence = parity_matrix_scout(lower_request(request), request.analysis_budget)
    if evidence is None:
        return None
    return dict(evidence.structural_fingerprint)


def _declared_true(request: PathfinderRequest, key: str) -> bool:
    return lookup(request.mathematical_context, key) is True


# ---------------------------------------------------------------------------
# kummer_square_class_independence  (Thm 4.1 valuation separation)
# ---------------------------------------------------------------------------

_SQUARE_CLASS_SHAPES = ("square_class_rank", "kummer_module_rank")

SQUARE_CLASS_INDEPENDENCE_CERTIFICATES = (
    Obligation(
        "radicand-regularity",
        "Every conjugate radicand r_alpha,i is regular at the chosen base divisors "
        "on the normalized model.",
        "exact-valuation",
    ),
    Obligation(
        "base-divisor-unramifiedness",
        "Each base divisor carrying a parity row is unramified in E/F.",
        "exact-ramification",
    ),
    Obligation(
        "odd-valuation-preservation",
        "Ramification indices over the chosen divisors preserve the declared odd valuations.",
        "exact-ramification",
    ),
    Obligation(
        "off-sheet-evenness",
        "Off-sheet valuations of every conjugate radicand at each chosen divisor are even.",
        "exact-valuation",
    ),
)

SQUARE_CLASS_INDEPENDENCE_CONTRACT = RouteContract(
    route_family="kummer_square_class_independence",
    accepted_problem_shape="square_class_rank",
    required_hypotheses=(
        "characteristic != 2",
        "K/F finite separable of degree d with normal closure E",
        "G = Gal(E/F) acts transitively and faithfully on the sheet set I",
        "every conjugate radicand is nonzero",
        "the declared valuations are discrete on E",
        "rank_F2 of the valuation-parity matrix equals its column count sd (Thm 4.1 condition 4.2)",
        "for any inertia reading the residue characteristic is not 2",
    ),
    required_evidence=("kummer_parity_matrix evidence with full_column_rank true",),
    produced_obligations=(
        Obligation(
            "certify-square-class-independence",
            "Certify the four external obligations; the full-rank parity matrix then forces "
            "R = 0, W isomorphic to V, rho = sd: all sd conjugate radicand square classes "
            "are independent in E*/E*^2.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "rank < sd is SILENT: the criterion neither proves nor disproves independence; "
        "the falsifier is a nonzero G-stable relation submodule R",
        "residue characteristic two blocks the inertia reading of parity rows",
    ),
    execution_module="external.kummer_square_class_executor",
    certificate_obligations=SQUARE_CLASS_INDEPENDENCE_CERTIFICATES,
    source_references=(
        "docs/files/KUMMER_MODULE_WREATH_LIFT_THEOREM_2026-07-10.md#4",
        "docs/files/R9_STATIC_CLOSURE_OPENING_DERIVATION_2026-07-10.md#6",
        "docs/files/DEGREE_20_CROWN_CERTIFICATE_REPORT_2026-07-10.md#2.4",
    ),
)


def recognize_kummer_square_class_independence(request: PathfinderRequest) -> RecognitionOutcome:
    family = SQUARE_CLASS_INDEPENDENCE_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        _accept_shape(request, family, _SQUARE_CLASS_SHAPES),
        require_odd_characteristic(request, family),
    ):
        if gate is not None:
            return gate

    fingerprint = _parity_fingerprint(request)
    if fingerprint is None:
        return refuse(
            family,
            "missing_parity_rows",
            "No cover declaration with valuation-parity rows was supplied and no "
            "kummer_parity_matrix evidence is available.",
            "cover declaration with parity_rows",
        )
    rank = fingerprint.get("f2_rank")
    columns = fingerprint.get("column_count")
    if not _is_exact_int(rank) or not _is_exact_int(columns):
        return refuse(
            family,
            "malformed_parity_evidence",
            "The parity-matrix evidence does not carry exact integer rank and column count.",
            "f2_rank",
            "column_count",
        )
    if fingerprint.get("full_column_rank") is not True:
        return refuse(
            family,
            "parity_rank_inconclusive",
            f"The valuation-parity matrix has F2 rank {rank} over {columns} columns; "
            "the full-column-rank criterion (Thm 4.1) is SILENT here. A deficient parity "
            "rank does NOT disprove square-class independence — the falsifier is a nonzero "
            "G-stable relation submodule R, which this route does not compute.",
            "rank_F2(parity matrix) = column count sd",
        )

    steps = (
        RouteStep(
            "assemble-rows",
            "assemble_valuation_parity_rows",
            ("cover_declaration",),
            ("valuation_parity_matrix",),
        ),
        RouteStep(
            "row-reduce",
            "f2_row_reduce",
            ("valuation_parity_matrix",),
            ("parity_rank_certificate",),
            freeze_mapping({"f2_rank": rank, "column_count": columns}),
        ),
        RouteStep(
            "emit-obligations",
            "emit_square_class_independence_obligations",
            ("parity_rank_certificate",),
            ("square_class_independence_route",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=SQUARE_CLASS_INDEPENDENCE_CONTRACT,
        steps=steps,
        data_dependencies=("cover_declaration",),
        required_intermediate_objects=("valuation_parity_matrix", "parity_rank_certificate"),
        completion_condition=(
            "The external certifier discharges the regularity, unramifiedness, "
            "odd-valuation-preservation, and off-sheet-evenness obligations attached "
            "to the full-rank parity matrix."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            exact_operation_count=3,
            scout_operation_count=1,
            expression_depth=1,
        ),
        structural_preference_rank=0,
    )


# ---------------------------------------------------------------------------
# valuation_parity_lower_bound
# ---------------------------------------------------------------------------

_LOWER_BOUND_SHAPES = (
    "square_class_rank",
    "kummer_module_rank",
    "square_class_lower_bound",
)

VALUATION_LOWER_BOUND_CERTIFICATES = (
    Obligation(
        "odd-valuation-height-one-prime",
        "Each declared odd valuation is realized by a height-one prime on the normalization.",
        "exact-valuation",
    ),
    Obligation(
        "wall-transversality",
        "Every contributing wall is transverse — away from the reciprocal sub-balance "
        "Sigma eps_i/N_i = 0 (record the sub-balance stratum as an exceptional branch).",
        "exact-stratification",
    ),
)

VALUATION_LOWER_BOUND_CONTRACT = RouteContract(
    route_family="valuation_parity_lower_bound",
    accepted_problem_shape="square_class_lower_bound",
    required_hypotheses=(
        "characteristic != 2",
        "rank(parity) <= rank(square-class module): the emitted rank is a certified "
        "LOWER BOUND only, never an upper bound or an independence verdict",
        "each charge N_i is nonzero and the squared charges N_i^2 are pairwise distinct",
        "P != 0",
        "away from the reciprocal sub-balance Sigma eps_i/N_i = 0",
        "beta is a unit at each contributing wall",
        "each wall is a height-one prime on the normalization",
    ),
    required_evidence=("kummer_parity_matrix evidence with f2_rank >= 1",),
    produced_obligations=(
        Obligation(
            "certify-square-class-lower-bound",
            "Certify the wall realizations; the F2 rank of the assembled parity rows is then a "
            "certified lower bound for dim_F2 of the square-class module W.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "reciprocal sub-balance Sigma eps_i/N_i = 0: non-transverse wall with order-4 "
        "colored inertia; excluded from this route and owned by the inertia family",
        "places at infinity are excluded",
        "the charge-zero boundary N_i = 0 is excluded",
    ),
    execution_module="external.valuation_parity_executor",
    certificate_obligations=VALUATION_LOWER_BOUND_CERTIFICATES,
    source_references=(
        "docs/files/DEGREE_20_CROWN_CERTIFICATE_REPORT_2026-07-10.md#3.1",
        "docs/files/DEGREE_20_CROWN_CERTIFICATE_REPORT_2026-07-10.md#3.2",
        "docs/files/KUMMER_MODULE_WREATH_LIFT_THEOREM_2026-07-10.md#7",
        "docs/files/R9_STATIC_CLOSURE_OPENING_DERIVATION_2026-07-10.md#3",
    ),
)


def recognize_valuation_parity_lower_bound(request: PathfinderRequest) -> RecognitionOutcome:
    family = VALUATION_LOWER_BOUND_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        _accept_shape(request, family, _LOWER_BOUND_SHAPES),
        require_odd_characteristic(request, family),
    ):
        if gate is not None:
            return gate

    fingerprint = _parity_fingerprint(request)
    if fingerprint is None:
        return refuse(
            family,
            "missing_parity_rows",
            "No valuation-parity rows were declared; without at least one odd-valuation "
            "row there is no lower-bound evidence.",
            "cover declaration with parity_rows",
        )
    rank = fingerprint.get("f2_rank")
    columns = fingerprint.get("column_count")
    if not _is_exact_int(rank) or not _is_exact_int(columns):
        return refuse(
            family,
            "malformed_parity_evidence",
            "The parity-matrix evidence does not carry exact integer rank and column count.",
            "f2_rank",
            "column_count",
        )
    if rank < 1:
        return refuse(
            family,
            "zero_parity_rank",
            "Every declared parity row is zero over F2; a lower bound of zero carries "
            "no route content (a single odd valuation is what forces a nonsquare).",
            "at least one F2-nonzero parity row",
        )

    steps = (
        RouteStep(
            "assemble-rows",
            "assemble_valuation_parity_rows",
            ("cover_declaration",),
            ("valuation_parity_matrix",),
        ),
        RouteStep(
            "row-reduce",
            "f2_row_reduce",
            ("valuation_parity_matrix",),
            ("parity_rank_certificate",),
            freeze_mapping({"f2_rank": rank, "column_count": columns}),
        ),
        RouteStep(
            "emit-lower-bound",
            "emit_certified_square_class_lower_bound",
            ("parity_rank_certificate",),
            ("square_class_lower_bound_route",),
            freeze_mapping(
                {
                    "certified_lower_bound": rank,
                    "law": "rank_F2(parity matrix) <= dim_F2(square-class module W)",
                    "bound_only": True,
                }
            ),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=VALUATION_LOWER_BOUND_CONTRACT,
        steps=steps,
        data_dependencies=("cover_declaration",),
        required_intermediate_objects=("valuation_parity_matrix", "parity_rank_certificate"),
        completion_condition=(
            "The external certifier realizes each odd valuation by a height-one prime and "
            "confirms wall transversality; the rank is then a certified lower bound only."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            exact_operation_count=3,
            scout_operation_count=1,
            expression_depth=1,
        ),
        structural_preference_rank=0,
    )


# ---------------------------------------------------------------------------
# rotating_kummer_rank_jump  (Thm 3.1 private-prime rank jump)
# ---------------------------------------------------------------------------

_RANK_JUMP_IMPORTED_CERTIFICATES = (
    (
        "charges_nonzero_distinct",
        "H1: every N_i is nonzero and the squared charges N_i^2 are pairwise distinct",
    ),
    ("beta_nonzero", "H2: beta != 0"),
    ("crown_certificate", "H3: [u] and [gamma] independent (the imported crown certificate)"),
    ("primitivity_certificate", "H4: K = F(gamma) (primitivity)"),
)

ROTATING_RANK_JUMP_CERTIFICATES = (
    Obligation(
        "private-prime-valuation",
        "At the private prime p = (delta_0 - 16*J^2): v_p(delta_J) = 1 and "
        "v_p(u) = v_p(gamma) = 0.",
        "exact-valuation",
    ),
    Obligation(
        "squarefree-witness",
        "gcd(delta_J, d/dJ delta_J) = gcd(delta_J, -32*J) = 1; a common factor would force "
        "gamma - 4P = 0, contradicting the hypotheses.",
        "exact-polynomial-gcd",
    ),
    Obligation(
        "transcendental-injection",
        "The square-class map K*/K*^2 -> K(J)*/K(J)*^2 is injective on [u] and [gamma] "
        "over the purely transcendental base F_J = F(J).",
        "exact-square-class",
    ),
    Obligation(
        "rank-three-conclusion",
        "Rank 3 of {[u],[gamma],[delta_J]} yields H_J = K_J(sqrt(gamma), sqrt(delta_J)) with "
        "Galois group V_4 and [H_J:F_J] = 20, and L_J of degree 8 with (Z/2)^3, [L_J:F_J] = 40.",
        "exact-galois",
    ),
)

ROTATING_RANK_JUMP_CONTRACT = RouteContract(
    route_family="rotating_kummer_rank_jump",
    accepted_problem_shape="rotating_rank_jump",
    required_hypotheses=(
        "characteristic != 2 (the rank-jump lemma is stated over a characteristic-zero base)",
        "H1: N_i != 0 and N_i^2 != N_j^2 for i != j (imported certificate)",
        "H2: beta != 0 (imported certificate)",
        "H3: [u] and [gamma] independent — the crown certificate (imported)",
        "H4: K = F(gamma) primitivity (imported certificate)",
        "F_J = F(J) is purely transcendental over F",
    ),
    required_evidence=(
        "declared imported certificates H1-H4 as context flags",
        "identity delta_J = delta_0 - 16*J^2 with delta_0 = 4*u*beta^2/gamma",
    ),
    produced_obligations=(
        Obligation(
            "certify-rank-three-jump",
            "Certify the private-prime valuation and the imported certificates; the "
            "square-class rank then jumps to 3 over F(J) with the stated degrees 8/40.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "J = 0 is a genuine rank-drop fiber: [delta_0] = [u][gamma], the rank drops to 2 "
        "and the algebra splits E x E",
        "other algebraic values of J require separate specialization checks",
        "closure monodromy over F(J) is explicitly NOT promoted by this route",
    ),
    execution_module="external.rotating_rank_jump_executor",
    certificate_obligations=ROTATING_RANK_JUMP_CERTIFICATES,
    source_references=(
        "docs/files/ROTATING_KUMMER_RANK_JUMP_LEMMA_REPORT_2026-07-10.md#3",
    ),
)


def recognize_rotating_kummer_rank_jump(request: PathfinderRequest) -> RecognitionOutcome:
    family = ROTATING_RANK_JUMP_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        _accept_shape(request, family, ("rotating_rank_jump",)),
        require_odd_characteristic(request, family),
    ):
        if gate is not None:
            return gate

    missing = tuple(
        (key, label)
        for key, label in _RANK_JUMP_IMPORTED_CERTIFICATES
        if not _declared_true(request, key)
    )
    if missing:
        named = "; ".join(label for _, label in missing)
        return refuse(
            family,
            "missing_imported_certificate",
            f"The following imported hypotheses of Thm 3.1 are not declared true: {named}. "
            "The rank-jump route consumes these certificates; it does not re-derive them.",
            *(key for key, _ in missing),
        )

    steps = (
        RouteStep(
            "inject-base",
            "inject_square_classes_through_transcendental_base",
            ("base_square_classes",),
            ("injected_square_classes",),
            freeze_mapping(
                {
                    "base_extension": "F_J = F(J) purely transcendental",
                    "imported_classes": ("[u]", "[gamma]"),
                }
            ),
        ),
        RouteStep(
            "adjoin-private-prime",
            "adjoin_private_prime_class",
            ("injected_square_classes",),
            ("rank_three_module",),
            freeze_mapping(
                {
                    "private_prime": "delta_0 - 16*J^2",
                    "derivative": "-32*J",
                    "squarefree_check": "gcd(delta_J, d/dJ delta_J) = 1",
                }
            ),
        ),
        RouteStep(
            "emit-obligations",
            "emit_rank_three_kummer_obligations",
            ("rank_three_module",),
            ("rank_jump_route",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=ROTATING_RANK_JUMP_CONTRACT,
        steps=steps,
        data_dependencies=("base_square_classes", "imported_certificates"),
        required_intermediate_objects=("injected_square_classes", "rank_three_module"),
        completion_condition=(
            "The external certifier verifies the private-prime valuation and the imported "
            "H1-H4 certificates; the rank-3 conclusion and its degree consequences are then "
            "certified outside Pathfinder."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            exact_operation_count=3,
            scout_operation_count=1,
            expression_depth=2,
        ),
        structural_preference_rank=0,
    )


# ---------------------------------------------------------------------------
# kummer_finite_extension_primeness  (Lemma 4.1 — the P4/IZ primeness route)
# ---------------------------------------------------------------------------

_PRIMENESS_SHAPES = ("prime_certificate", "difference_ideal_primeness")

_PRIMENESS_IMPORTED_CERTIFICATES = (
    (
        "primitivity_certificate",
        "K = F(gamma) primitivity, giving gamma_i pairwise distinct",
    ),
    (
        "constant_terms_nonzero",
        "gamma_i - 4P != 0 for every sheet (nonzero constant terms)",
    ),
)

FINITE_EXTENSION_PRIMENESS_CERTIFICATES = (
    Obligation(
        "derivative-gcd-witness",
        "For each sheet i: gcd(delta_i, d/dJ delta_i) = gcd(delta_i, -32*J) = 1 "
        "(delta_i squarefree; a common factor would force gamma_i - 4P = 0).",
        "exact-polynomial-gcd",
    ),
    Obligation(
        "constant-difference-witness",
        "For each pair i != j: delta_i - delta_j = gamma_i - gamma_j is a nonzero "
        "constant of E*, so delta_i and delta_j are coprime.",
        "exact-constant-nonvanishing",
    ),
    Obligation(
        "kummer-quadratic-primeness",
        "Once B is a domain and [gamma - 4P] is a nonsquare, "
        "IZ is prime via the Kummer quadratic IZ = B[J]/(J^2 - (gamma - 4P)/16) "
        "(CELLA_ARCHITECTURE_v1.3 section 12.3).",
        "exact-ideal-primeness",
    ),
)

FINITE_EXTENSION_PRIMENESS_CONTRACT = RouteContract(
    route_family="kummer_finite_extension_primeness",
    accepted_problem_shape="prime_certificate",
    required_hypotheses=(
        "characteristic 0",
        "gamma_i pairwise distinct (primitivity K = F(gamma), imported certificate)",
        "gamma_i - 4P != 0 for every sheet",
        "u_j and gamma_j are nonzero constants of E",
        "irreducibility of delta_i over the splitting field E is NOT required: "
        "squarefreeness plus pairwise coprimeness suffice (Lemma 4.1 strengthening)",
    ),
    required_evidence=(
        "declared primitivity and constant-term-nonvanishing certificates",
        "identity d/dJ delta_i = -32*J",
        "identity delta_i - delta_j = gamma_i - gamma_j in E*",
    ),
    produced_obligations=(
        Obligation(
            "certify-finite-extension-primeness",
            "Certify the derivative-gcd and constant-difference witnesses; the private "
            "primes q_i with parity rows (0|0|e_i) and the primeness of IZ then follow "
            "via the Kummer quadratic.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "gamma_i - 4P = 0 for some sheet collapses delta_i to -16*J^2, which is not squarefree",
        "[gamma - 4P] a square in B breaks the Kummer-quadratic primeness reading",
    ),
    execution_module="external.finite_extension_primeness_executor",
    certificate_obligations=FINITE_EXTENSION_PRIMENESS_CERTIFICATES,
    source_references=(
        "docs/files/ROTATING_THREE_CHANNEL_WREATH_CLOSURE_2026-07-10.md#4",
        "docs/files/ROTATING_KUMMER_RANK_JUMP_LEMMA_REPORT_2026-07-10.md#3",
        "CELLA_ARCHITECTURE_v1.3.md#12.3",
    ),
)


def recognize_kummer_finite_extension_primeness(request: PathfinderRequest) -> RecognitionOutcome:
    family = FINITE_EXTENSION_PRIMENESS_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        _accept_shape(request, family, _PRIMENESS_SHAPES),
        require_odd_characteristic(request, family),
    ):
        if gate is not None:
            return gate

    characteristic = lookup(request.mathematical_context, "characteristic")
    if characteristic != 0:
        return refuse(
            family,
            "characteristic_not_zero",
            "The private-prime primeness route (Lemma 4.1) is stated in characteristic zero: "
            "the derivative identity d/dJ delta_i = -32*J and the constant-difference "
            "coprimeness argument are read over a characteristic-zero base.",
            "characteristic 0",
        )

    missing = tuple(
        (key, label)
        for key, label in _PRIMENESS_IMPORTED_CERTIFICATES
        if not _declared_true(request, key)
    )
    if missing:
        named = "; ".join(label for _, label in missing)
        return refuse(
            family,
            "missing_imported_certificate",
            f"The following imported hypotheses of Lemma 4.1 are not declared true: {named}.",
            *(key for key, _ in missing),
        )

    steps = (
        RouteStep(
            "squarefree",
            "certify_squarefree_by_derivative_gcd",
            ("sheet_polynomials",),
            ("squarefree_certificates",),
            freeze_mapping(
                {
                    "derivative": "d/dJ delta_i = -32*J",
                    "witness": "gcd(delta_i, -32*J) = 1",
                    "failure_reading": "a common factor forces gamma_i - 4P = 0, "
                    "contradicting the declared nonvanishing",
                }
            ),
        ),
        RouteStep(
            "pairwise-coprime",
            "certify_pairwise_coprime_by_constant_difference",
            ("sheet_polynomials",),
            ("coprimality_certificates",),
            freeze_mapping(
                {"identity": "delta_i - delta_j = gamma_i - gamma_j, a nonzero constant of E*"}
            ),
        ),
        RouteStep(
            "emit-obligations",
            "emit_private_prime_rows_and_primeness_obligations",
            ("squarefree_certificates", "coprimality_certificates"),
            ("primeness_route",),
            freeze_mapping(
                {
                    "parity_row_pattern": "(0|0|e_i)",
                    "kummer_quadratic": "IZ = B[J]/(J^2 - (gamma - 4P)/16)",
                    "irreducibility_not_required": True,
                }
            ),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=FINITE_EXTENSION_PRIMENESS_CONTRACT,
        steps=steps,
        data_dependencies=("sheet_polynomials", "imported_certificates"),
        required_intermediate_objects=("squarefree_certificates", "coprimality_certificates"),
        completion_condition=(
            "The external certifier verifies the gcd and constant-difference witnesses; "
            "primeness of the finite-extension ideal then follows via the Kummer quadratic "
            "without any irreducibility test over the splitting field."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            exact_operation_count=3,
            scout_operation_count=0,
            expression_depth=2,
        ),
        structural_preference_rank=0,
    )


PROVIDERS: tuple[RouteProvider, ...] = (
    RouteProvider(
        route_family="kummer_square_class_independence",
        contract=SQUARE_CLASS_INDEPENDENCE_CONTRACT,
        recognizer=recognize_kummer_square_class_independence,
        native_scouts=(parity_matrix_scout,),
        wrapper_capabilities=("valuation_parity_assembly", "f2_row_reduction"),
    ),
    RouteProvider(
        route_family="valuation_parity_lower_bound",
        contract=VALUATION_LOWER_BOUND_CONTRACT,
        recognizer=recognize_valuation_parity_lower_bound,
        native_scouts=(parity_matrix_scout, sign_orbit_scout),
        wrapper_capabilities=("valuation_parity_assembly", "f2_row_reduction"),
    ),
    RouteProvider(
        route_family="rotating_kummer_rank_jump",
        contract=ROTATING_RANK_JUMP_CONTRACT,
        recognizer=recognize_rotating_kummer_rank_jump,
        native_scouts=(parity_matrix_scout,),
        wrapper_capabilities=("square_class_injection", "private_prime_adjunction"),
    ),
    RouteProvider(
        route_family="kummer_finite_extension_primeness",
        contract=FINITE_EXTENSION_PRIMENESS_CONTRACT,
        recognizer=recognize_kummer_finite_extension_primeness,
        native_scouts=(),
        wrapper_capabilities=("univariate_gcd_certification", "constant_difference_check"),
    ),
)
