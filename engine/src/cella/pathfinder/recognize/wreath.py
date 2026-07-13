"""Wreath-lift and wreath-closure route-family providers.

Three route families from the horizon wreath corpus:

- ``conjugate_module_wreath_lift`` — KUMMER_MODULE_WREATH_LIFT Thms 3.1/5.1/6.1
  and R9 Prop 9.1: full parity rank (directly, or via sheet-level B
  invertibility with the Kronecker structure B (x) I_d) plus the faithful
  signed-permutation action and the order equality 2^(s*d)*|G| force the FULL
  wreath product C_2^s wr_I G.
- ``rotating_three_channel_wreath_closure`` — the rotating 15-column closure
  (C_2^3 wr S_5, order 3932160) and its ordered-horizon 10-column subcase
  (C_2^2 wr S_5, order 122880).
- ``self_glue_exponent_gcd`` — the trinomial gcd law (Lemma C): x^m + s*x^k - c
  has layer monodromy C_d wr S_(m/d) with d = gcd(m, k), order d^(m/d)*(m/d)!.

Route instructions and certificate obligations only; no execution.
"""

from __future__ import annotations

from math import factorial

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
from ..scout.algebra import self_glue_trinomial_scout
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
# conjugate_module_wreath_lift  (Thms 3.1 / 5.1 / 6.1, Prop 9.1)
# ---------------------------------------------------------------------------

CONJUGATE_WREATH_LIFT_CERTIFICATES = (
    Obligation(
        "normal-closure-equality",
        "Both inclusions of the normal-closure equality: L (E with all sd conjugate "
        "square roots adjoined) equals the normal closure of the radical extension over F.",
        "exact-field-equality",
    ),
    Obligation(
        "base-group-identity",
        "The imported identification of the base group G = Gal(E/F) remains valid.",
        "imported-certificate",
    ),
    Obligation(
        "faithful-signed-permutation-action",
        "Gal(L/F) acts faithfully by signed permutations on the sd square-root generators.",
        "exact-galois-action",
    ),
    Obligation(
        "order-equality",
        "The order equality |Gal(L/F)| = 2^(s*d) * |G| holds; together with the faithful "
        "embedding this forces the FULL wreath product.",
        "exact-order-count",
    ),
    Obligation(
        "regularity-unramifiedness-checklist",
        "The section-12 checklist of the wreath-lift source: radicands regular, base "
        "divisors survive the normal model, ramification preserves odd valuations, "
        "off-sheet valuations even, and B invertible over F2.",
        "exact-valuation",
    ),
)

CONJUGATE_WREATH_LIFT_CONTRACT = RouteContract(
    route_family="conjugate_module_wreath_lift",
    accepted_problem_shape="wreath_closure",
    required_hypotheses=(
        "characteristic != 2",
        "K/F finite separable of degree d with normal closure E",
        "G = Gal(E/F) acts transitively and faithfully on the sheet set",
        "every conjugate radicand is nonzero",
        "maximality of the Kummer module is equivalent to full parity rank (R = 0, rho = sd)",
        "the sheet-level matrix B is invertible over F2 when the Kronecker route is used "
        "(full matrix = B (x) I_d, Thm 5.1)",
    ),
    required_evidence=(
        "kummer_parity_matrix evidence with full_column_rank true",
        "declared base group with integer order",
    ),
    produced_obligations=(
        Obligation(
            "certify-wreath-lift",
            "Certify the normal-closure equality, faithful action, and order equality; "
            "Gal(L/F) is then the full wreath product (C_2^s)^d semidirect G = C_2^s wr_I G "
            "of order 2^(s*d)*|G| (Thm 6.1).",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "R != 0 yields the subgroup cut out by (V/R)-dual, not the full wreath product",
        "the closure group is C_2^s wreath G — an s-dimensional block (V_4 for s = 2) per "
        "sheet — NOT C_2 wreath G",
        "rank < sd is SILENT: it does not disprove maximality",
    ),
    execution_module="external.wreath_lift_executor",
    certificate_obligations=CONJUGATE_WREATH_LIFT_CERTIFICATES,
    source_references=(
        "docs/files/KUMMER_MODULE_WREATH_LIFT_THEOREM_2026-07-10.md#3",
        "docs/files/KUMMER_MODULE_WREATH_LIFT_THEOREM_2026-07-10.md#5",
        "docs/files/KUMMER_MODULE_WREATH_LIFT_THEOREM_2026-07-10.md#6",
        "docs/files/R9_STATIC_CLOSURE_OPENING_DERIVATION_2026-07-10.md#9",
    ),
)


def recognize_conjugate_module_wreath_lift(request: PathfinderRequest) -> RecognitionOutcome:
    family = CONJUGATE_WREATH_LIFT_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        _accept_shape(request, family, ("wreath_closure",)),
        require_odd_characteristic(request, family),
    ):
        if gate is not None:
            return gate

    problem = lower_request(request)
    cover = problem.cover
    if cover is None:
        return refuse(
            family,
            "missing_cover_declaration",
            "No cover structure (degree, channels, base group, parity rows) was declared.",
            "cover declaration",
        )
    if not cover.base_group:
        return refuse(
            family,
            "missing_base_group",
            "The wreath lift imports the base group G = Gal(E/F); none was declared.",
            "cover.base_group",
        )
    if cover.degree < 1:
        return refuse(
            family,
            "missing_cover_degree",
            "The cover degree d must be declared as a positive integer.",
            "cover.degree >= 1",
        )
    if not cover.channels:
        return refuse(
            family,
            "missing_channels",
            "The radicand channels (the s conjugate families) must be declared.",
            "cover.channels",
        )
    if not cover.parity_rows:
        return refuse(
            family,
            "missing_parity_rows",
            "No valuation-parity rows were declared for the conjugate module.",
            "cover.parity_rows",
        )
    base_group_order = lookup(request.mathematical_context, "base_group_order")
    if not _is_exact_int(base_group_order) or base_group_order < 1:
        return refuse(
            family,
            "missing_base_group_order",
            "The order-equality obligation |Gal(L/F)| = 2^(s*d)*|G| needs the exact "
            "integer order of the imported base group.",
            "base_group_order",
        )

    fingerprint = _parity_fingerprint(request)
    if fingerprint is None:
        return refuse(
            family,
            "missing_parity_rows",
            "The declared parity rows do not assemble into a well-formed F2 matrix.",
            "cover.parity_rows",
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
            f"The parity matrix has F2 rank {rank} over {columns} columns; neither the "
            "sheet-level B route nor the direct route reaches full rank. The criterion "
            "is SILENT here — a deficient rank does NOT disprove the wreath closure; the "
            "failure mode is a nonzero G-stable relation submodule R, in which case "
            "Gal(L/F) is the subgroup cut out by (V/R)-dual rather than the full wreath.",
            "full F2 column rank (directly or via B (x) I_d)",
        )

    channel_count = len(cover.channels)
    degree = cover.degree
    order = 2 ** (channel_count * degree) * base_group_order
    order_parameters = freeze_mapping(
        {
            "order": order,
            "order_identity": "2^(s*d) * |G|",
            "channel_count": channel_count,
            "degree": degree,
            "base_group": cover.base_group,
            "base_group_order": base_group_order,
        }
    )

    if fingerprint.get("kronecker_structured_shape") is True:
        steps = (
            RouteStep(
                "assemble-sheet-matrix",
                "assemble_sheet_matrix",
                ("cover_declaration",),
                ("sheet_matrix_B",),
                freeze_mapping({"sheet_matrix_size": channel_count}),
            ),
            RouteStep(
                "verify-invertibility",
                "verify_f2_invertibility",
                ("sheet_matrix_B",),
                ("sheet_invertibility_certificate",),
            ),
            RouteStep(
                "expand-kronecker",
                "expand_kronecker_structure",
                ("sheet_matrix_B", "sheet_invertibility_certificate"),
                ("full_parity_matrix",),
                freeze_mapping({"structure": "B (x) I_d", "degree": degree}),
            ),
            RouteStep(
                "emit-obligations",
                "emit_wreath_lift_obligations",
                ("full_parity_matrix",),
                ("wreath_lift_route",),
                order_parameters,
            ),
        )
        intermediates = (
            "sheet_matrix_B",
            "sheet_invertibility_certificate",
            "full_parity_matrix",
        )
    else:
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
                "emit_wreath_lift_obligations",
                ("parity_rank_certificate",),
                ("wreath_lift_route",),
                order_parameters,
            ),
        )
        intermediates = ("valuation_parity_matrix", "parity_rank_certificate")

    return assemble_candidate(
        request=request,
        contract=CONJUGATE_WREATH_LIFT_CONTRACT,
        steps=steps,
        data_dependencies=("cover_declaration", "base_group_order"),
        required_intermediate_objects=intermediates,
        completion_condition=(
            "The external certifier discharges the normal-closure equality (both "
            "inclusions), the faithful signed-permutation action, the order equality "
            "2^(s*d)*|G|, and the regularity/unramifiedness checklist."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            exact_operation_count=len(steps),
            scout_operation_count=1,
            expression_depth=1,
        ),
        structural_preference_rank=0,
    )


# ---------------------------------------------------------------------------
# rotating_three_channel_wreath_closure
# ---------------------------------------------------------------------------

_CLOSURE_SCOPES: dict[str, tuple[int, int, str]] = {
    # scope -> (expected F2 rank, expected order, closure group description)
    "augmented": (15, 3932160, "C_2^3 wr S_5"),
    "ordered_horizon": (10, 122880, "C_2^2 wr S_5"),
}

ROTATING_CLOSURE_CERTIFICATES = (
    Obligation(
        "banked-base-group",
        "The banked certificate [K:F] = 5, Gal(E/F) = S_5, K = F(gamma) remains valid "
        "over the purely transcendental base F_J = F(J).",
        "imported-certificate",
    ),
    Obligation(
        "gauss-valuation-parity",
        "The Gauss valuation vhat(sum a_n J^n) = min_n v(a_n) reads vhat(delta_j) = 0 "
        "because the coefficient of J^2 in delta_j is the unit -16.",
        "exact-valuation",
    ),
    Obligation(
        "private-prime-realization",
        "Each private prime q_i realizes the row (0|0|e_i): v_{q_i}(delta_i) = 1 and "
        "v_{q_i}(delta_j) = v_{q_i}(u_j) = v_{q_i}(gamma_j) = 0 for j != i.",
        "exact-valuation",
    ),
    Obligation(
        "closure-order-equality",
        "The closure order equality holds for the declared scope: 2^15 * 120 = 3932160 "
        "(augmented) or 2^10 * 120 = 122880 (ordered horizon).",
        "exact-order-count",
    ),
)

ROTATING_CLOSURE_CONTRACT = RouteContract(
    route_family="rotating_three_channel_wreath_closure",
    accepted_problem_shape="rotating_wreath_closure",
    required_hypotheses=(
        "characteristic != 2",
        "banked: [K:F] = 5, Gal(E/F) = S_5, K = F(gamma)",
        "standing nonvanishing: u_i, gamma_i, beta_i, gamma_i - 4P all nonzero",
        "purely transcendental base F_J = F(J)",
        "columns are u_1..u_5 | gamma_1..gamma_5 | delta_1..delta_5 (three channels, "
        "five sheets) with block form [[I5,0,0],[I5,I5,0],[0,0,I5]] in the augmented scope",
    ),
    required_evidence=(
        "kummer_parity_matrix evidence at the scope's expected rank (15 augmented, "
        "10 ordered-horizon)",
        "declared banked base group S_5 (or base group with order 120)",
    ),
    produced_obligations=(
        Obligation(
            "certify-rotating-closure",
            "Certify the banked, Gauss-valuation, and private-prime obligations; the "
            "closure group is then C_2^3 wr S_5 of order 3932160 (augmented) or "
            "C_2^2 wr S_5 of order 122880 (ordered horizon).",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "J = 0 is a rank-drop fiber ([delta_0] = [u][gamma])",
        "the generic closure does not specialize as a constant group along fibers",
    ),
    execution_module="external.rotating_wreath_closure_executor",
    certificate_obligations=ROTATING_CLOSURE_CERTIFICATES,
    source_references=(
        "docs/files/ROTATING_THREE_CHANNEL_WREATH_CLOSURE_2026-07-10.md#5",
        "docs/files/ROTATING_THREE_CHANNEL_WREATH_CLOSURE_2026-07-10.md#4",
    ),
)


def recognize_rotating_three_channel_wreath_closure(
    request: PathfinderRequest,
) -> RecognitionOutcome:
    family = ROTATING_CLOSURE_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        _accept_shape(request, family, ("rotating_wreath_closure",)),
        require_odd_characteristic(request, family),
    ):
        if gate is not None:
            return gate

    problem = lower_request(request)
    banked = lookup(request.mathematical_context, "banked_base_group")
    base_group_order = lookup(request.mathematical_context, "base_group_order")
    banked_ok = banked == "S5" or (
        problem.cover is not None
        and bool(problem.cover.base_group)
        and _is_exact_int(base_group_order)
        and base_group_order == 120
    )
    if not banked_ok:
        return refuse(
            family,
            "missing_banked_base_group",
            "The standing banked certificate Gal(E/F) = S_5 (order 120) is not declared; "
            "the closure route consumes it and does not re-derive the base group.",
            "banked_base_group = S5 (or declared base group with base_group_order 120)",
        )
    missing = tuple(
        key
        for key in ("primitivity_certificate", "standing_nonvanishing")
        if not _declared_true(request, key)
    )
    if missing:
        return refuse(
            family,
            "missing_imported_certificate",
            "The following standing certificates are not declared true: "
            + ", ".join(missing)
            + " (primitivity K = F(gamma); nonvanishing of u_i, gamma_i, beta_i, gamma_i - 4P).",
            *missing,
        )

    scope_value = lookup(request.mathematical_context, "closure_scope")
    scope = "augmented" if scope_value is None else scope_value
    if scope not in _CLOSURE_SCOPES:
        return refuse(
            family,
            "invalid_closure_scope",
            "The declared closure scope is neither 'augmented' (15 columns, order 3932160) "
            "nor 'ordered_horizon' (10 columns, order 122880).",
            "closure_scope in {augmented, ordered_horizon}",
        )
    expected_rank, expected_order, group_description = _CLOSURE_SCOPES[scope]

    fingerprint = _parity_fingerprint(request)
    if fingerprint is None:
        return refuse(
            family,
            "missing_parity_rows",
            "No valuation-parity rows were declared for the rotating closure matrix.",
            "cover.parity_rows",
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
    if rank != expected_rank:
        return refuse(
            family,
            "parity_rank_inconclusive",
            f"The declared rows have F2 rank {rank}; the {scope} closure needs rank "
            f"{expected_rank}. The criterion is SILENT here — a deficient rank does NOT "
            "disprove the closure; it only means the declared rows fail to witness it.",
            f"F2 rank {expected_rank} for the {scope} scope",
        )

    steps = (
        RouteStep(
            "extend-gauss-rows",
            "extend_static_rows_by_gauss_valuation",
            ("cover_declaration",),
            ("gauss_extended_rows",),
            freeze_mapping(
                {
                    "unit_coefficient": -16,
                    "identity": "coefficient of J^2 in delta_j is the unit -16",
                    "gauss_valuation": "vhat(sum a_n J^n) = min_n v(a_n)",
                }
            ),
        ),
        RouteStep(
            "adjoin-private-primes",
            "adjoin_private_prime_rows",
            ("gauss_extended_rows",),
            ("closure_parity_matrix",),
            freeze_mapping({"row_pattern": "(0|0|e_i)"}),
        ),
        RouteStep(
            "block-reduce",
            "f2_block_reduce",
            ("closure_parity_matrix",),
            ("closure_rank_certificate",),
            freeze_mapping(
                {"f2_rank": rank, "expected_rank": expected_rank, "closure_scope": scope}
            ),
        ),
        RouteStep(
            "emit-obligations",
            "emit_wreath_closure_obligations",
            ("closure_rank_certificate",),
            ("wreath_closure_route",),
            freeze_mapping(
                {"expected_order": expected_order, "closure_group": group_description}
            ),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=ROTATING_CLOSURE_CONTRACT,
        steps=steps,
        data_dependencies=("cover_declaration", "banked_base_group"),
        required_intermediate_objects=(
            "gauss_extended_rows",
            "closure_parity_matrix",
            "closure_rank_certificate",
        ),
        completion_condition=(
            "The external certifier discharges the banked-base-group, Gauss-valuation, "
            "private-prime, and order-equality obligations for the declared scope."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            exact_operation_count=4,
            scout_operation_count=1,
            expression_depth=1,
        ),
        structural_preference_rank=0,
    )


# ---------------------------------------------------------------------------
# self_glue_exponent_gcd  (Lemmas A / B / B' / C and the wreath law)
# ---------------------------------------------------------------------------

_SELF_GLUE_SHAPES = ("cover_monodromy", "self_glue_monodromy")

SELF_GLUE_CERTIFICATES = (
    Obligation(
        "separability",
        "The trinomial layer x^m + s*x^k - c is separable over the base.",
        "exact-separability",
    ),
    Obligation(
        "distinct-critical-values",
        "The layer has distinct critical values (Morse conditions) off the declared "
        "degeneracy loci.",
        "exact-critical-values",
    ),
    Obligation(
        "block-collapse-discriminant",
        "The block-collapse discriminant is nonzero: discA != 0.",
        "exact-nonvanishing",
    ),
    Obligation(
        "lemma-c-base-field",
        "The base-field hypotheses of the gcd law (Lemma C) hold for the declared base.",
        "exact-field-hypotheses",
    ),
)

SELF_GLUE_CONTRACT = RouteContract(
    route_family="self_glue_exponent_gcd",
    accepted_problem_shape="cover_monodromy",
    required_hypotheses=(
        "the layer polynomial x^m + s*x^k - c is separable (genuine hypothesis)",
        "s != 0 for 0 < k < m (k = 0 is the pure-power endpoint, monodromy C_m, "
        "with the convention gcd(m, 0) = m)",
        "off the degeneracy loci: A = 3, B = 0, and discA = 0 (block collapse) are excluded",
        "base-field hypotheses of Lemma C",
    ),
    required_evidence=(
        "self_glue_trinomial evidence with exact exponents (m, k) and d = gcd(m, k)",
        "declared separability certificate",
    ),
    produced_obligations=(
        Obligation(
            "certify-gcd-layer-monodromy",
            "Certify separability, Morse conditions, and discA != 0; the layer monodromy "
            "is then C_d wr S_(m/d) with d = gcd(m, k), order d^(m/d) * (m/d)! (Lemma C, "
            "by the substitution y = x^d).",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "m_P = 2 degeneracy: C_2 = S_2 are indistinguishable at that layer "
        "(recorded explicitly; the product cover reads D_4)",
        "k = 0 pure-power endpoint: monodromy C_m (Lemma A)",
        "gcd(m, k) = 1 endpoint: monodromy S_m (Lemmas B / B')",
        "A = 3 and B = 0 are excluded fibers",
    ),
    execution_module="external.self_glue_monodromy_executor",
    certificate_obligations=SELF_GLUE_CERTIFICATES,
    source_references=(
        "Reference_Material/papers/current/self_glue_monodromy.txt#4",
        "Reference_Material/papers/current/self_glue_monodromy.txt#7",
        "Reference_Material/papers/current/self_glue_monodromy.txt#12",
    ),
)


def recognize_self_glue_exponent_gcd(request: PathfinderRequest) -> RecognitionOutcome:
    family = SELF_GLUE_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        _accept_shape(request, family, _SELF_GLUE_SHAPES),
    ):
        if gate is not None:
            return gate

    if not _declared_true(request, "separability_certificate"):
        return refuse(
            family,
            "missing_separability",
            "Separability of the trinomial layer is a genuine hypothesis of the gcd law "
            "(Lemma C) and is not declared true.",
            "separability_certificate",
        )

    fingerprint = evidence_by_family(request, "self_glue_trinomial")
    if fingerprint is None:
        evidence = self_glue_trinomial_scout(lower_request(request), request.analysis_budget)
        if evidence is not None:
            fingerprint = dict(evidence.structural_fingerprint)
    if fingerprint is None:
        return refuse(
            family,
            "not_a_trinomial_layer",
            "No self-glue trinomial layer x^m + s*x^k - c was recognized in the declared "
            "target and no self_glue_trinomial evidence was supplied; the gcd law does "
            "not apply to non-trinomial layers.",
            "self_glue_trinomial evidence",
        )
    m = fingerprint.get("m")
    k = fingerprint.get("k")
    d = fingerprint.get("gcd")
    if (
        not _is_exact_int(m)
        or not _is_exact_int(k)
        or not _is_exact_int(d)
        or m < 1
        or k < 0
        or d < 1
        or m % d != 0
    ):
        return refuse(
            family,
            "malformed_trinomial_evidence",
            "The trinomial evidence does not carry exact exponents m > 0, k >= 0 and "
            "a valid divisor d = gcd(m, k).",
            "exact exponent fingerprint (m, k, gcd)",
        )
    blocks = m // d
    order = d**blocks * factorial(blocks)

    steps = (
        RouteStep(
            "read-exponents",
            "read_trinomial_exponents",
            ("trinomial_layer",),
            ("exponent_pair",),
            freeze_mapping({"m": m, "k": k}),
        ),
        RouteStep(
            "gcd-layer",
            "compute_gcd_layer_type",
            ("exponent_pair",),
            ("layer_group_type",),
            freeze_mapping(
                {
                    "d": d,
                    "layer_candidate": f"C_{d} wr S_{blocks}",
                    "order": order,
                    "gcd_convention": "gcd(m, 0) = m",
                    "substitution": "y = x^d",
                }
            ),
        ),
        RouteStep(
            "emit-obligations",
            "emit_wreath_monodromy_obligations",
            ("layer_group_type",),
            ("self_glue_monodromy_route",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=SELF_GLUE_CONTRACT,
        steps=steps,
        data_dependencies=("trinomial_layer", "separability_certificate"),
        required_intermediate_objects=("exponent_pair", "layer_group_type"),
        completion_condition=(
            "The external certifier discharges separability, distinct-critical-value, and "
            "block-collapse obligations; the layer group C_d wr S_(m/d) is then certified."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            exact_operation_count=3,
            scout_operation_count=1,
            expression_depth=1,
        ),
        structural_preference_rank=0,
    )


PROVIDERS: tuple[RouteProvider, ...] = (
    RouteProvider(
        route_family="conjugate_module_wreath_lift",
        contract=CONJUGATE_WREATH_LIFT_CONTRACT,
        recognizer=recognize_conjugate_module_wreath_lift,
        native_scouts=(parity_matrix_scout,),
        wrapper_capabilities=("valuation_parity_assembly", "f2_row_reduction"),
    ),
    RouteProvider(
        route_family="rotating_three_channel_wreath_closure",
        contract=ROTATING_CLOSURE_CONTRACT,
        recognizer=recognize_rotating_three_channel_wreath_closure,
        native_scouts=(parity_matrix_scout,),
        wrapper_capabilities=("gauss_valuation_rows", "f2_row_reduction"),
    ),
    RouteProvider(
        route_family="self_glue_exponent_gcd",
        contract=SELF_GLUE_CONTRACT,
        recognizer=recognize_self_glue_exponent_gcd,
        native_scouts=(self_glue_trinomial_scout,),
        wrapper_capabilities=("trinomial_layer_reading",),
    ),
)
