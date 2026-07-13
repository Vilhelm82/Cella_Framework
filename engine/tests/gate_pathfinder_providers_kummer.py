"""Gate the Galois/Kummer/wreath/cover/inertia route-family providers.

Fixtures follow the corpus extract exactly:
- static 10x10 parity matrix [[I5,0],[I5,I5]] of F2 rank 10 (R9 instance);
- rotating 15x15 matrix [[I5,0,0],[I5,I5,0],[0,0,I5]] of rank 15;
- sheet matrix B = [[1,0],[1,1]];
- gcd law m=6, k=4 -> d=2 -> C_2 wr S_3 of order 48;
- collision partition (2,1,1,1) of 5.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.pathfinder.api.request import PathfinderRequest
from cella.pathfinder.ir.obligation import Obligation
from cella.pathfinder.recognize import cover as cover_module
from cella.pathfinder.recognize import inertia_strata as inertia_module
from cella.pathfinder.recognize import kummer as kummer_module
from cella.pathfinder.recognize import wreath as wreath_module
from cella.pathfinder.serialize import canonical_json_bytes


FAILS: list[str] = []


def check(name: str, condition: bool) -> None:
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")
    if not condition:
        FAILS.append(name)


ALL_FAMILIES = tuple(
    provider.route_family
    for module in (kummer_module, wreath_module, cover_module, inertia_module)
    for provider in module.PROVIDERS
)


def e(i: int, width: int = 5) -> tuple[int, ...]:
    return tuple(1 if j == i else 0 for j in range(width))


def zeros(width: int = 5) -> tuple[int, ...]:
    return tuple(0 for _ in range(width))


# Static [[I5,0],[I5,I5]]: 10x10, rank 10.
STATIC_ROWS = tuple(e(i) + zeros() for i in range(5)) + tuple(e(i) + e(i) for i in range(5))
# Rank-deficient mutation: the second block loses its last row.
STATIC_ROWS_DEFICIENT = STATIC_ROWS[:9]
# Rotating [[I5,0,0],[I5,I5,0],[0,0,I5]]: 15x15, rank 15.
ROTATING_ROWS = (
    tuple(e(i) + zeros() + zeros() for i in range(5))
    + tuple(e(i) + e(i) + zeros() for i in range(5))
    + tuple(zeros() + zeros() + e(i) for i in range(5))
)
# Ordered-horizon [[I5,0],[0,I5]]: 10x10, rank 10.
HORIZON_ROWS = tuple(e(i) + zeros() for i in range(5)) + tuple(zeros() + e(i) for i in range(5))


def make_request(context: dict[str, object], request_id: str = "gate-kummer-fixture") -> PathfinderRequest:
    return PathfinderRequest.create(
        request_id=request_id,
        target_obligation=Obligation(
            "route-discovery",
            "Return a computational route for the declared structural task.",
            "exact-route",
        ),
        external_binding={"host_model": "external:model"},
        mathematical_context=context,
        available_route_families=ALL_FAMILIES,
    )


def static_cover(rows: tuple[tuple[int, ...], ...] = STATIC_ROWS) -> dict[str, object]:
    return {
        "degree": 5,
        "channels": ("u", "gamma"),
        "base_group": "S5",
        "parity_rows": rows,
    }


def rotating_cover(rows: tuple[tuple[int, ...], ...] = ROTATING_ROWS) -> dict[str, object]:
    return {
        "degree": 5,
        "channels": ("u", "gamma", "delta"),
        "base_group": "S5",
        "parity_rows": rows,
    }


def step_params(route, index: int) -> dict[str, object]:
    return dict(route.ordered_steps[index].parameters)


def check_refusal(name: str, outcome, code: str) -> None:
    check(name, outcome.refusal is not None and outcome.refusal.code == code)


def check_silent_reason(name: str, outcome) -> None:
    """The silent-criterion refusal must not read as a disproof."""

    reason = outcome.refusal.reason if outcome.refusal is not None else ""
    check(name, "does NOT disprove" in reason and "SILENT" in reason)


# ===========================================================================
# kummer_square_class_independence
# ===========================================================================

print("--- kummer_square_class_independence ---")

sci_context = {
    "problem_shape": "square_class_rank",
    "characteristic": 0,
    "cover": static_cover(),
}
outcome = kummer_module.recognize_kummer_square_class_independence(make_request(sci_context))
check("static 10x10 full-rank fixture is admitted", outcome.candidate is not None)
if outcome.candidate is not None:
    route = outcome.candidate.route
    check(
        "route steps are assemble -> f2_row_reduce -> emit obligations",
        tuple(step.operation for step in route.ordered_steps)
        == (
            "assemble_valuation_parity_rows",
            "f2_row_reduce",
            "emit_square_class_independence_obligations",
        ),
    )
    check(
        "f2_row_reduce carries exact rank 10 of 10 columns",
        step_params(route, 1) == {"column_count": 10, "f2_rank": 10},
    )
    check(
        "certificate obligations include the four external checks",
        tuple(item.obligation_id for item in route.certificate_obligations)
        == (
            "radicand-regularity",
            "base-divisor-unramifiedness",
            "odd-valuation-preservation",
            "off-sheet-evenness",
        ),
    )
    serialized = canonical_json_bytes(route)
    check("route serialization is byte deterministic", serialized == canonical_json_bytes(route))
    check("route has no wall-clock prediction", b"predicted_duration" not in serialized)

alt = kummer_module.recognize_kummer_square_class_independence(
    make_request({**sci_context, "problem_shape": "kummer_module_rank"})
)
check("alternate shape kummer_module_rank is accepted", alt.candidate is not None)

deficient = kummer_module.recognize_kummer_square_class_independence(
    make_request({**sci_context, "cover": static_cover(STATIC_ROWS_DEFICIENT)})
)
check_refusal(
    "rank-deficient matrix refuses parity_rank_inconclusive (never admits)",
    deficient,
    "parity_rank_inconclusive",
)
check_silent_reason("deficient-rank refusal does not claim disproof", deficient)
if deficient.refusal is not None:
    check(
        "deficient-rank refusal names the G-stable relation submodule falsifier",
        "G-stable relation submodule" in deficient.refusal.reason,
    )

check_refusal(
    "wrong shape is refused",
    kummer_module.recognize_kummer_square_class_independence(
        make_request({**sci_context, "problem_shape": "boundary_stratification"})
    ),
    "shape_mismatch",
)
check_refusal(
    "characteristic two is refused",
    kummer_module.recognize_kummer_square_class_independence(
        make_request({**sci_context, "characteristic": 2})
    ),
    "characteristic_two",
)
check_refusal(
    "undeclared characteristic is refused",
    kummer_module.recognize_kummer_square_class_independence(
        make_request({key: value for key, value in sci_context.items() if key != "characteristic"})
    ),
    "missing_characteristic",
)
check_refusal(
    "missing parity rows are refused",
    kummer_module.recognize_kummer_square_class_independence(
        make_request({"problem_shape": "square_class_rank", "characteristic": 0})
    ),
    "missing_parity_rows",
)

# ===========================================================================
# valuation_parity_lower_bound
# ===========================================================================

print("--- valuation_parity_lower_bound ---")

single_row_cover = {
    "degree": 5,
    "channels": ("u", "gamma"),
    "base_group": "S5",
    "parity_rows": (e(0) + zeros(),),
}
lb_context = {
    "problem_shape": "square_class_lower_bound",
    "characteristic": 0,
    "cover": single_row_cover,
}
outcome = kummer_module.recognize_valuation_parity_lower_bound(make_request(lb_context))
check("a single odd-valuation row is admitted as a lower bound", outcome.candidate is not None)
if outcome.candidate is not None:
    route = outcome.candidate.route
    params = step_params(route, 2)
    check("the certified lower bound is exactly the F2 rank 1", params.get("certified_lower_bound") == 1)
    check(
        "the exact law rank(parity) <= rank(square-class module) is a route parameter",
        params.get("law") == "rank_F2(parity matrix) <= dim_F2(square-class module W)",
    )
    check(
        "the lower-bound law is in the contract hypotheses",
        any("LOWER BOUND" in item for item in route.required_hypotheses),
    )
    check(
        "wall transversality and height-one realization are certificate obligations",
        tuple(item.obligation_id for item in route.certificate_obligations)
        == ("odd-valuation-height-one-prime", "wall-transversality"),
    )
    check(
        "the sub-balance exceptional branch is recorded",
        any("sub-balance" in branch for branch in route.exceptional_branches),
    )

full_bound = kummer_module.recognize_valuation_parity_lower_bound(
    make_request({**lb_context, "cover": static_cover()})
)
check(
    "the full static matrix certifies lower bound 10",
    full_bound.candidate is not None
    and step_params(full_bound.candidate.route, 2).get("certified_lower_bound") == 10,
)
check_refusal(
    "all-zero parity rows are refused (bound zero carries no route)",
    kummer_module.recognize_valuation_parity_lower_bound(
        make_request({**lb_context, "cover": {**single_row_cover, "parity_rows": (zeros(10),)}})
    ),
    "zero_parity_rank",
)
check_refusal(
    "characteristic two is refused",
    kummer_module.recognize_valuation_parity_lower_bound(
        make_request({**lb_context, "characteristic": 2})
    ),
    "characteristic_two",
)
check_refusal(
    "wrong shape is refused",
    kummer_module.recognize_valuation_parity_lower_bound(
        make_request({**lb_context, "problem_shape": "collision_inertia"})
    ),
    "shape_mismatch",
)

# ===========================================================================
# rotating_kummer_rank_jump
# ===========================================================================

print("--- rotating_kummer_rank_jump ---")

rj_context = {
    "problem_shape": "rotating_rank_jump",
    "characteristic": 0,
    "charges_nonzero_distinct": True,
    "beta_nonzero": True,
    "crown_certificate": True,
    "primitivity_certificate": True,
}
outcome = kummer_module.recognize_rotating_kummer_rank_jump(make_request(rj_context))
check("rank-jump fixture with H1-H4 declared is admitted", outcome.candidate is not None)
if outcome.candidate is not None:
    route = outcome.candidate.route
    params = step_params(route, 1)
    check(
        "the private prime is delta_0 - 16*J^2 with derivative -32*J",
        params.get("private_prime") == "delta_0 - 16*J^2" and params.get("derivative") == "-32*J",
    )
    check(
        "the squarefree witness gcd(delta_J, d/dJ delta_J) = 1 is a route parameter",
        params.get("squarefree_check") == "gcd(delta_J, d/dJ delta_J) = 1",
    )
    check(
        "the J = 0 rank-drop fiber is an exceptional branch",
        any("J = 0" in branch and "rank-drop" in branch for branch in route.exceptional_branches),
    )
    check(
        "closure monodromy over F(J) is explicitly not promoted",
        any("NOT promoted" in branch for branch in route.exceptional_branches),
    )
    check("certificate obligations are present", len(route.certificate_obligations) == 4)

missing_crown = kummer_module.recognize_rotating_kummer_rank_jump(
    make_request({key: value for key, value in rj_context.items() if key != "crown_certificate"})
)
check_refusal("missing crown certificate is refused", missing_crown, "missing_imported_certificate")
if missing_crown.refusal is not None:
    check(
        "the refusal names the missing H3 crown hypothesis",
        "H3" in missing_crown.refusal.reason
        and "crown_certificate" in missing_crown.refusal.unmet_requirements,
    )
check_refusal(
    "characteristic two is refused",
    kummer_module.recognize_rotating_kummer_rank_jump(
        make_request({**rj_context, "characteristic": 2})
    ),
    "characteristic_two",
)
check_refusal(
    "wrong shape is refused",
    kummer_module.recognize_rotating_kummer_rank_jump(
        make_request({**rj_context, "problem_shape": "square_class_rank"})
    ),
    "shape_mismatch",
)

# ===========================================================================
# kummer_finite_extension_primeness
# ===========================================================================

print("--- kummer_finite_extension_primeness ---")

pp_context = {
    "problem_shape": "prime_certificate",
    "characteristic": 0,
    "primitivity_certificate": True,
    "constant_terms_nonzero": True,
}
outcome = kummer_module.recognize_kummer_finite_extension_primeness(make_request(pp_context))
check("primeness fixture is admitted", outcome.candidate is not None)
if outcome.candidate is not None:
    route = outcome.candidate.route
    check(
        "route is derivative-gcd -> constant-difference -> emit primeness",
        tuple(step.operation for step in route.ordered_steps)
        == (
            "certify_squarefree_by_derivative_gcd",
            "certify_pairwise_coprime_by_constant_difference",
            "emit_private_prime_rows_and_primeness_obligations",
        ),
    )
    check(
        "irreducibility over the splitting field is stated as NOT required",
        any("NOT required" in item for item in route.required_hypotheses),
    )
    check(
        "the Kummer quadratic (v1.3 section 12.3) is the primeness certificate",
        any(
            "B[J]/(J^2 - (gamma - 4P)/16)" in item.statement
            for item in route.certificate_obligations
        ),
    )
    check(
        "the gcd(delta_i, -32*J) = 1 witness is a certificate obligation",
        any("gcd(delta_i, -32*J) = 1" in item.statement for item in route.certificate_obligations),
    )

check_refusal(
    "shape difference_ideal_primeness is also accepted",
    kummer_module.recognize_kummer_finite_extension_primeness(
        make_request({**pp_context, "problem_shape": "wrong_shape"})
    ),
    "shape_mismatch",
)
check(
    "difference_ideal_primeness shape admits",
    kummer_module.recognize_kummer_finite_extension_primeness(
        make_request({**pp_context, "problem_shape": "difference_ideal_primeness"})
    ).candidate
    is not None,
)
check_refusal(
    "positive characteristic is refused as characteristic_not_zero",
    kummer_module.recognize_kummer_finite_extension_primeness(
        make_request({**pp_context, "characteristic": 3})
    ),
    "characteristic_not_zero",
)
check_refusal(
    "characteristic two is refused before the zero test",
    kummer_module.recognize_kummer_finite_extension_primeness(
        make_request({**pp_context, "characteristic": 2})
    ),
    "characteristic_two",
)
check_refusal(
    "missing constant-term nonvanishing is refused",
    kummer_module.recognize_kummer_finite_extension_primeness(
        make_request(
            {key: value for key, value in pp_context.items() if key != "constant_terms_nonzero"}
        )
    ),
    "missing_imported_certificate",
)

# ===========================================================================
# conjugate_module_wreath_lift
# ===========================================================================

print("--- conjugate_module_wreath_lift ---")

wl_context = {
    "problem_shape": "wreath_closure",
    "characteristic": 0,
    "cover": static_cover(),
    "base_group_order": 120,
}
outcome = wreath_module.recognize_conjugate_module_wreath_lift(make_request(wl_context))
check("static structured fixture is admitted", outcome.candidate is not None)
if outcome.candidate is not None:
    route = outcome.candidate.route
    check(
        "structured shape selects the sheet-level B route (Thm 5.1)",
        tuple(step.operation for step in route.ordered_steps)
        == (
            "assemble_sheet_matrix",
            "verify_f2_invertibility",
            "expand_kronecker_structure",
            "emit_wreath_lift_obligations",
        ),
    )
    check(
        "the order equality is 2^(2*5) * 120 = 122880",
        step_params(route, 3).get("order") == 122880,
    )
    check(
        "the R != 0 subgroup and C_2^s-not-C_2 branches are recorded",
        any("(V/R)-dual" in branch for branch in route.exceptional_branches)
        and any("NOT C_2 wreath" in branch for branch in route.exceptional_branches),
    )
    check(
        "order equality and faithful action are certificate obligations",
        {"order-equality", "faithful-signed-permutation-action", "normal-closure-equality"}
        <= {item.obligation_id for item in route.certificate_obligations},
    )

# Sheet matrix B = [[1,0],[1,1]] alone (degree 1): structured 2 = 2*1.
b_fixture = wreath_module.recognize_conjugate_module_wreath_lift(
    make_request(
        {
            **wl_context,
            "cover": {
                "degree": 1,
                "channels": ("u", "gamma"),
                "base_group": "S5",
                "parity_rows": ((1, 0), (1, 1)),
            },
        }
    )
)
check(
    "sheet matrix B = [[1,0],[1,1]] is admitted with order 2^2 * 120",
    b_fixture.candidate is not None
    and step_params(b_fixture.candidate.route, 3).get("order") == 480,
)

deficient_lift = wreath_module.recognize_conjugate_module_wreath_lift(
    make_request({**wl_context, "cover": static_cover(STATIC_ROWS_DEFICIENT)})
)
check_refusal(
    "rank-deficient parity matrix refuses parity_rank_inconclusive",
    deficient_lift,
    "parity_rank_inconclusive",
)
check_silent_reason("wreath-lift deficient-rank refusal does not claim disproof", deficient_lift)

check_refusal(
    "missing base group order is refused",
    wreath_module.recognize_conjugate_module_wreath_lift(
        make_request({key: value for key, value in wl_context.items() if key != "base_group_order"})
    ),
    "missing_base_group_order",
)
check_refusal(
    "missing base group is refused",
    wreath_module.recognize_conjugate_module_wreath_lift(
        make_request({**wl_context, "cover": {**static_cover(), "base_group": ""}})
    ),
    "missing_base_group",
)
check_refusal(
    "characteristic two is refused",
    wreath_module.recognize_conjugate_module_wreath_lift(
        make_request({**wl_context, "characteristic": 2})
    ),
    "characteristic_two",
)
check_refusal(
    "wrong shape is refused",
    wreath_module.recognize_conjugate_module_wreath_lift(
        make_request({**wl_context, "problem_shape": "square_class_rank"})
    ),
    "shape_mismatch",
)

# ===========================================================================
# rotating_three_channel_wreath_closure
# ===========================================================================

print("--- rotating_three_channel_wreath_closure ---")

rc_context = {
    "problem_shape": "rotating_wreath_closure",
    "characteristic": 0,
    "cover": rotating_cover(),
    "banked_base_group": "S5",
    "primitivity_certificate": True,
    "standing_nonvanishing": True,
}
outcome = wreath_module.recognize_rotating_three_channel_wreath_closure(make_request(rc_context))
check("rotating 15x15 rank-15 fixture is admitted", outcome.candidate is not None)
if outcome.candidate is not None:
    route = outcome.candidate.route
    check(
        "route extends by Gauss valuation with the unit -16 identity",
        step_params(route, 0).get("unit_coefficient") == -16
        and step_params(route, 0).get("identity")
        == "coefficient of J^2 in delta_j is the unit -16",
    )
    check(
        "the augmented expected order is 3932160",
        step_params(route, 3).get("expected_order") == 3932160,
    )
    check(
        "the closure group is C_2^3 wr S_5",
        step_params(route, 3).get("closure_group") == "C_2^3 wr S_5",
    )

horizon = wreath_module.recognize_rotating_three_channel_wreath_closure(
    make_request(
        {
            **rc_context,
            "closure_scope": "ordered_horizon",
            "cover": {
                "degree": 5,
                "channels": ("u", "gamma"),
                "base_group": "S5",
                "parity_rows": HORIZON_ROWS,
            },
        }
    )
)
check(
    "ordered-horizon scope expects rank 10 and order 122880",
    horizon.candidate is not None
    and step_params(horizon.candidate.route, 3).get("expected_order") == 122880,
)

deficient_closure = wreath_module.recognize_rotating_three_channel_wreath_closure(
    make_request({**rc_context, "cover": rotating_cover(ROTATING_ROWS[:14])})
)
check_refusal(
    "rank-14 rotating matrix refuses parity_rank_inconclusive",
    deficient_closure,
    "parity_rank_inconclusive",
)
check_silent_reason("rotating deficient-rank refusal does not claim disproof", deficient_closure)

check_refusal(
    "missing standing nonvanishing is refused",
    wreath_module.recognize_rotating_three_channel_wreath_closure(
        make_request(
            {key: value for key, value in rc_context.items() if key != "standing_nonvanishing"}
        )
    ),
    "missing_imported_certificate",
)
check_refusal(
    "missing banked base group is refused",
    wreath_module.recognize_rotating_three_channel_wreath_closure(
        make_request({key: value for key, value in rc_context.items() if key != "banked_base_group"})
    ),
    "missing_banked_base_group",
)
check_refusal(
    "an unknown closure scope is refused",
    wreath_module.recognize_rotating_three_channel_wreath_closure(
        make_request({**rc_context, "closure_scope": "everything"})
    ),
    "invalid_closure_scope",
)
check_refusal(
    "characteristic two is refused",
    wreath_module.recognize_rotating_three_channel_wreath_closure(
        make_request({**rc_context, "characteristic": 2})
    ),
    "characteristic_two",
)

# ===========================================================================
# self_glue_exponent_gcd
# ===========================================================================

print("--- self_glue_exponent_gcd ---")

sg_context = {
    "problem_shape": "self_glue_monodromy",
    "characteristic": 0,
    "separability_certificate": True,
    "ring": {"variables": ("x",)},
    "ideals": {"target": ("x**6 + 3*x**4 - 5",)},
}
outcome = wreath_module.recognize_self_glue_exponent_gcd(make_request(sg_context))
check("trinomial m=6, k=4 is admitted", outcome.candidate is not None)
if outcome.candidate is not None:
    route = outcome.candidate.route
    check(
        "the gcd law reads d = 2 and layer C_2 wr S_3",
        step_params(route, 1).get("d") == 2
        and step_params(route, 1).get("layer_candidate") == "C_2 wr S_3",
    )
    check("the layer order is 2^3 * 3! = 48", step_params(route, 1).get("order") == 48)
    check(
        "the m_P = 2 (C_2 = S_2) degeneracy and the two endpoints are recorded",
        any("C_2 = S_2" in branch for branch in route.exceptional_branches)
        and any("pure-power endpoint" in branch for branch in route.exceptional_branches)
        and any("S_m" in branch for branch in route.exceptional_branches),
    )
    check(
        "separability, Morse, and block-collapse certificates are present",
        {"separability", "distinct-critical-values", "block-collapse-discriminant"}
        <= {item.obligation_id for item in route.certificate_obligations},
    )

check_refusal(
    "missing separability certificate is refused",
    wreath_module.recognize_self_glue_exponent_gcd(
        make_request(
            {key: value for key, value in sg_context.items() if key != "separability_certificate"}
        )
    ),
    "missing_separability",
)
check_refusal(
    "a non-trinomial layer is refused",
    wreath_module.recognize_self_glue_exponent_gcd(
        make_request({**sg_context, "ideals": {"target": ("x**6 + 3*x**4 + x - 5",)}})
    ),
    "not_a_trinomial_layer",
)
check_refusal(
    "wrong shape is refused",
    wreath_module.recognize_self_glue_exponent_gcd(
        make_request({**sg_context, "problem_shape": "wreath_closure"})
    ),
    "shape_mismatch",
)

# ===========================================================================
# normalization_aware_cover
# ===========================================================================

print("--- normalization_aware_cover ---")

nc_context = {
    "problem_shape": "cover_ramification",
    "characteristic": 0,
    "ring": {"variables": ("w1", "w2", "w3", "w4", "u", "M", "N1", "N2", "N3", "N4")},
    "ideals": {
        "incidence": (
            "w1**2 - u - N1**2",
            "w2**2 - u - N2**2",
            "w3**2 - u - N3**2",
            "w4**2 - u - N4**2",
            "w1 + w2 + w3 + w4 - 4*M",
        )
    },
}
outcome = cover_module.recognize_normalization_aware_cover(make_request(nc_context))
check("incidence-presented cover is admitted", outcome.candidate is not None)
if outcome.candidate is not None:
    route = outcome.candidate.route
    check(
        "route builds the incidence model before any projection",
        tuple(step.operation for step in route.ordered_steps)
        == (
            "build_incidence_model",
            "derive_relative_ramification_from_jacobian",
            "decompose_upstairs_before_projection",
            "emit_branch_image_route",
        ),
    )
    check(
        "the discriminant prohibition is a contract hypothesis",
        any(
            "eliminant discriminant must not be used to decide ramification" in item
            for item in route.required_hypotheses
        ),
    )
    check(
        "the Jacobian step uses the generic relative determinant with the fixture identity",
        step_params(route, 1).get("determinant") == "relative_jacobian_determinant"
        and step_params(route, 1).get("horizon_fixture_identity") == "ramDet = 8*e3(w) mod IX",
    )
    check(
        "the certified overcount instance backs the IR-only certificate",
        any("(8,8,12,20)" in item.statement for item in route.certificate_obligations),
    )
    check(
        "boundary-specific saturation branches are recorded for M=0 / P=0 / crossings",
        len(route.exceptional_branches) == 3,
    )

check_refusal(
    "a missing incidence presentation is refused",
    cover_module.recognize_normalization_aware_cover(
        make_request({key: value for key, value in nc_context.items() if key != "ideals"})
    ),
    "missing_incidence_presentation",
)
check_refusal(
    "a missing ring declaration is refused",
    cover_module.recognize_normalization_aware_cover(
        make_request({key: value for key, value in nc_context.items() if key != "ring"})
    ),
    "missing_ring_declaration",
)
check_refusal(
    "an undeclared characteristic is refused",
    cover_module.recognize_normalization_aware_cover(
        make_request({key: value for key, value in nc_context.items() if key != "characteristic"})
    ),
    "missing_characteristic",
)
check(
    "the branch_image shape is also accepted",
    cover_module.recognize_normalization_aware_cover(
        make_request({**nc_context, "problem_shape": "branch_image"})
    ).candidate
    is not None,
)

# ===========================================================================
# structured_incidence_projection
# ===========================================================================

print("--- structured_incidence_projection ---")

sp_context = {
    "problem_shape": "structured_projection",
    "characteristic": 0,
    "cover": static_cover(),
    "base_group_transitive": True,
}
outcome = cover_module.recognize_structured_incidence_projection(make_request(sp_context))
check("structured static fixture is admitted", outcome.candidate is not None)
if outcome.candidate is not None:
    route = outcome.candidate.route
    checklist = step_params(route, 1).get("checklist")
    check("the geometric package has exactly five points", isinstance(checklist, tuple) and len(checklist) == 5)
    check(
        "the five-point package is mirrored by five certificate obligations",
        tuple(item.obligation_id for item in route.certificate_obligations)
        == (
            "not-discriminant-component",
            "generic-point-unramified",
            "single-odd-sheet",
            "off-sheet-even",
            "radicand-regularity",
        ),
    )
    check(
        "orbit transport supplies the d = 5 rows",
        step_params(route, 2).get("degree") == 5,
    )

check_refusal(
    "missing transitivity is refused",
    cover_module.recognize_structured_incidence_projection(
        make_request({key: value for key, value in sp_context.items() if key != "base_group_transitive"})
    ),
    "missing_transitivity",
)
check_refusal(
    "a non-structured shape (10 columns vs channels*degree = 6) is refused",
    cover_module.recognize_structured_incidence_projection(
        make_request({**sp_context, "cover": {**static_cover(), "degree": 3}})
    ),
    "not_structured_shape",
)
deficient_structured = cover_module.recognize_structured_incidence_projection(
    make_request({**sp_context, "cover": static_cover(STATIC_ROWS_DEFICIENT)})
)
check_refusal(
    "rank-deficient structured rows refuse parity_rank_inconclusive",
    deficient_structured,
    "parity_rank_inconclusive",
)
check_silent_reason("structured deficient-rank refusal does not claim disproof", deficient_structured)
check_refusal(
    "characteristic two is refused",
    cover_module.recognize_structured_incidence_projection(
        make_request({**sp_context, "characteristic": 2})
    ),
    "characteristic_two",
)

# ===========================================================================
# generic_open_boundary_split
# ===========================================================================

print("--- generic_open_boundary_split ---")

bs_context = {
    "problem_shape": "boundary_stratification",
    "characteristic": 0,
    "cover": static_cover(),
}
outcome = cover_module.recognize_generic_open_boundary_split(make_request(bs_context))
check("boundary split over cover parity data is admitted", outcome.candidate is not None)
if outcome.candidate is not None:
    route = outcome.candidate.route
    table = step_params(route, 0).get("disposition_table")
    check("the disposition table lists all seven boundaries", isinstance(table, tuple) and len(table) == 7)
    if isinstance(table, tuple):
        names = tuple(entry[0] for entry in table)
        check(
            "the table covers J=0, J=inf, N_a=0, crossings, sub-balance, M=0, weighted infinity",
            names
            == (
                "J = 0",
                "J = infinity",
                "N_a = 0",
                "N_a^2 = N_b^2",
                "sub-balance Sigma eps_i/N_i = 0",
                "M = 0",
                "weighted infinity",
            ),
        )
        check(
            "J = 0 is classified as an unramified RELATION divisor, not ramification",
            "relation divisor" in dict(table)["J = 0"],
        )
    check(
        "one retained task per boundary is the split policy",
        step_params(route, 1).get("policy") == "one retained task per declared boundary",
    )
    check(
        "the sub-balance stratum is the unique genuine-inertia exceptional branch",
        len(route.exceptional_branches) == 1
        and "sub-balance" in route.exceptional_branches[0],
    )

strata_only = cover_module.recognize_generic_open_boundary_split(
    make_request(
        {
            "problem_shape": "boundary_stratification",
            "characteristic": 0,
            "strata": (
                {"name": "J0", "condition": "J = 0", "status": "boundary"},
                {"name": "subbalance", "condition": "Sigma eps_i/N_i = 0", "status": "boundary"},
            ),
        }
    )
)
check("declared strata without cover parity data also admit", strata_only.candidate is not None)
check_refusal(
    "no boundary declarations at all are refused",
    cover_module.recognize_generic_open_boundary_split(
        make_request({"problem_shape": "boundary_stratification", "characteristic": 0})
    ),
    "missing_boundary_declarations",
)
check_refusal(
    "characteristic two is refused",
    cover_module.recognize_generic_open_boundary_split(
        make_request({**bs_context, "characteristic": 2})
    ),
    "characteristic_two",
)

# ===========================================================================
# branch_inertia_stratification
# ===========================================================================

print("--- branch_inertia_stratification ---")

single_row_context = {
    "problem_shape": "inertia_classification",
    "characteristic": 0,
    "residue_characteristic_not_two": True,
    "cover": {
        "degree": 5,
        "channels": ("u", "gamma"),
        "base_group": "S5",
        "parity_rows": (e(0) + zeros(),),
    },
}
outcome = inertia_module.recognize_branch_inertia_stratification(make_request(single_row_context))
check("a single height-one Kummer row admits without transversality", outcome.candidate is not None)
if outcome.candidate is not None:
    check(
        "single row classifies as (C_2)^1",
        step_params(outcome.candidate.route, 1).get("group_description") == "(C_2)^1",
    )

two_row_context = {
    **single_row_context,
    "transverse_intersection": True,
    "cover": {
        "degree": 5,
        "channels": ("u", "gamma"),
        "base_group": "S5",
        "parity_rows": (e(0) + zeros(), e(1) + e(1)),
    },
}
outcome = inertia_module.recognize_branch_inertia_stratification(make_request(two_row_context))
check("a transverse two-row stratum is admitted", outcome.candidate is not None)
if outcome.candidate is not None:
    route = outcome.candidate.route
    check(
        "the transverse span classifies as (C_2)^2",
        step_params(route, 1).get("f2_rank") == 2
        and step_params(route, 1).get("group_description") == "(C_2)^2",
    )
    check(
        "loop realization for equality is a certificate obligation",
        any(
            item.obligation_id == "loop-realization-for-equality"
            for item in route.certificate_obligations
        ),
    )
    check(
        "the colored C_4 sub-balance branch is recorded",
        any("colored C_4" in branch for branch in route.exceptional_branches),
    )

colored = inertia_module.recognize_branch_inertia_stratification(
    make_request({**two_row_context, "collision_cycles": ((3, 1), (2, 0))})
)
check(
    "colored cycle rule: cycles (3, sum 1) and (2, sum 0) give lcm(6, 2) = 6",
    colored.candidate is not None
    and step_params(colored.candidate.route, 1).get("colored_cyclic_order") == 6,
)
check_refusal(
    "malformed collision cycles are refused",
    inertia_module.recognize_branch_inertia_stratification(
        make_request({**two_row_context, "collision_cycles": ((0, 1),)})
    ),
    "invalid_collision_cycles",
)
check_refusal(
    "a multi-row stratum without declared transversality is refused",
    inertia_module.recognize_branch_inertia_stratification(
        make_request(
            {key: value for key, value in two_row_context.items() if key != "transverse_intersection"}
        )
    ),
    "missing_transversality",
)
check_refusal(
    "residue characteristic two (wild) is refused",
    inertia_module.recognize_branch_inertia_stratification(
        make_request(
            {
                key: value
                for key, value in single_row_context.items()
                if key != "residue_characteristic_not_two"
            }
        )
    ),
    "wild_or_residue_characteristic_two",
)
check_refusal(
    "characteristic two is refused",
    inertia_module.recognize_branch_inertia_stratification(
        make_request({**single_row_context, "characteristic": 2})
    ),
    "characteristic_two",
)
check_refusal(
    "wrong shape is refused",
    inertia_module.recognize_branch_inertia_stratification(
        make_request({**single_row_context, "problem_shape": "collision_inertia"})
    ),
    "shape_mismatch",
)

# ===========================================================================
# collision_partition_inertia
# ===========================================================================

print("--- collision_partition_inertia ---")

cp_context = {
    "problem_shape": "collision_inertia",
    "characteristic": 0,
    "collision_partition": (2, 1, 1, 1),
    "cover": {
        "degree": 5,
        "channels": ("u", "gamma"),
        "base_group": "S5",
        "parity_rows": ((1, 1, 0, 0, 0, 1, 1, 0, 0, 0),),
    },
}
outcome = inertia_module.recognize_collision_partition_inertia(make_request(cp_context))
check("collision partition (2,1,1,1) of 5 is admitted", outcome.candidate is not None)
if outcome.candidate is not None:
    route = outcome.candidate.route
    check(
        "the Young subgroup is S_2 x S_1 x S_1 x S_1 of order 2",
        step_params(route, 0).get("young_subgroup") == "S_2 x S_1 x S_1 x S_1"
        and step_params(route, 0).get("young_order") == 2,
    )
    check(
        "the emitted conclusion is the containment I_local in U semidirect P",
        "I_local is contained in U semidirect P"
        in str(step_params(route, 2).get("containment")),
    )
    check(
        "equal squared charges are recorded as a CROSSING, not ramification",
        any(
            "CROSSING" in branch and "u_pm(t) = u_0 +- c*t" in branch
            for branch in route.exceptional_branches
        ),
    )
    check(
        "collision-type realization and loop equality are certificate obligations",
        {"collision-type-transversality", "loop-realization-equality", "sub-balance-colored-table"}
        == {item.obligation_id for item in route.certificate_obligations},
    )
    check(
        "collision burden is invariant level 1 with preference rank 1",
        outcome.candidate.burden_vector.invariant_level == 1
        and outcome.candidate.structural_preference_rank == 1,
    )

check_refusal(
    "partition (3,3) does not sum to degree 5 and is refused",
    inertia_module.recognize_collision_partition_inertia(
        make_request({**cp_context, "collision_partition": (3, 3)})
    ),
    "invalid_collision_partition",
)
check_refusal(
    "an undeclared cover degree is refused",
    inertia_module.recognize_collision_partition_inertia(
        make_request(
            {
                **cp_context,
                "cover": {
                    "channels": ("u", "gamma"),
                    "base_group": "S5",
                    "parity_rows": ((1, 1, 0, 0, 0),),
                },
            }
        )
    ),
    "invalid_collision_partition",
)
check_refusal(
    "a missing partition is refused",
    inertia_module.recognize_collision_partition_inertia(
        make_request({key: value for key, value in cp_context.items() if key != "collision_partition"})
    ),
    "missing_collision_partition",
)
check_refusal(
    "characteristic two is refused",
    inertia_module.recognize_collision_partition_inertia(
        make_request({**cp_context, "characteristic": 2})
    ),
    "characteristic_two",
)

# ===========================================================================
# cross-cutting provider checks
# ===========================================================================

print("--- cross-cutting provider checks ---")

for module in (kummer_module, wreath_module, cover_module, inertia_module):
    for provider in module.PROVIDERS:
        check(
            f"{provider.route_family}: contract cites its corpus sources",
            len(provider.contract.source_references) >= 1,
        )
        check(
            f"{provider.route_family}: contract declares certificate obligations",
            len(provider.contract.certificate_obligations) >= 1,
        )

check(
    "the twelve corpus families are all provided exactly once",
    len(set(ALL_FAMILIES)) == 12,
)


print()
if FAILS:
    print(f"GATE PATHFINDER PROVIDERS KUMMER: OPEN ({len(FAILS)} failing)")
    raise SystemExit(1)
print("GATE PATHFINDER PROVIDERS KUMMER: CLOSED")
