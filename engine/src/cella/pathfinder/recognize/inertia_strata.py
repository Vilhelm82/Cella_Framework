"""Branch/collision inertia stratification route-family providers.

Two route families from WREATH_COVER_INERTIA_BRANCH_STRATIFICATION v1.1:

- ``branch_inertia_stratification`` — Thms 3.1/4.1/13.1 and the colored cycle
  rule: for a tame henselized transverse stratum, the local Kummer inertia is
  (C_2)^r with r the F2 rank of the incident parity rows; a nonzero parity
  vector alone gives a cyclic order-2 generator.  Cyclic orders of collision
  loops follow the colored cycle rule: a cycle of length l contributes l when
  its channel sum vanishes and 2l otherwise; the order is the lcm.
- ``collision_partition_inertia`` — the controlling theorem (10.2):
  I_local is contained in U semidirect P, where U is the P-stable F2 span of
  the incident parity vectors and P is the Young subgroup
  S_{m_1} x ... x S_{m_t} of the declared collision partition; equality is an
  external realization obligation.

Both recognizers perform bounded native route analysis (F2 rank of declared
rows, lcm/factorial arithmetic).  Route instructions and certificate
obligations only; no Galois computation, no execution.
"""

from __future__ import annotations

from math import factorial, lcm

from ..api.contract import RecognitionOutcome, RouteContract
from ..api.request import PathfinderRequest
from ..api.route import RouteStep
from ..ir.burden import BurdenVector
from ..ir.obligation import Obligation
from ..ir.problem import lower_request
from ..ir.values import FrozenValue, freeze_mapping
from ..plan.admissibility import (
    family_enabled,
    lookup,
    refuse,
    require_odd_characteristic,
    require_shape,
)
from ..plan.assemble import assemble_candidate
from ..plan.registry import RouteProvider
from ..scout.f2 import f2_rank
from ..scout.kummer import parity_matrix_scout


def _is_exact_int(value: FrozenValue | None) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _declared_true(request: PathfinderRequest, key: str) -> bool:
    return lookup(request.mathematical_context, key) is True


# ---------------------------------------------------------------------------
# branch_inertia_stratification  (Thms 3.1 / 4.1 / 13.1 + colored cycle rule)
# ---------------------------------------------------------------------------

BRANCH_INERTIA_CERTIFICATES = (
    Obligation(
        "transversality-realized",
        "The declared transversality (normal crossing) of the stratum is realized in the "
        "normalized incidence model, not only in the projected shadow.",
        "exact-stratification",
    ),
    Obligation(
        "henselization-hypotheses",
        "The local rings are henselized and the extension is tame (residue "
        "characteristic != 2) so the parity reading of inertia applies.",
        "exact-local-hypotheses",
    ),
    Obligation(
        "loop-realization-for-equality",
        "Equality of the local inertia group with the F2 span requires independently "
        "realized loops; until they are realized the classification is a containment only.",
        "exact-loop-realization",
    ),
)

BRANCH_INERTIA_CONTRACT = RouteContract(
    route_family="branch_inertia_stratification",
    accepted_problem_shape="inertia_classification",
    required_hypotheses=(
        "characteristic != 2",
        "tame: residue characteristic != 2 (declared certificate)",
        "normal crossing / transversality for multi-row strata (a single height-one "
        "Kummer divisor is exempt)",
        "the generic open locus 2*P*prod(N_a^2 - N_b^2) is inverted",
        "henselized local rings",
    ),
    required_evidence=(
        "the incident valuation-parity rows of the stratum",
        "declared residue-characteristic and transversality certificates",
    ),
    produced_obligations=(
        Obligation(
            "certify-local-inertia",
            "Certify transversality and henselization; the local inertia is then (C_2)^r "
            "with r the F2 rank of the incident parity rows (Prop 4.1, Thm 13.1(2)), and "
            "cyclic orders of declared collision cycles follow the colored cycle rule.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "non-transverse sub-balance contact yields colored C_4 — an order-4 generator "
        "after adjoining sqrt(u) — not (C_2)^r",
        "apparent intersections must be resolved on the incidence normalization before "
        "parity rows are read",
    ),
    execution_module="external.branch_inertia_executor",
    certificate_obligations=BRANCH_INERTIA_CERTIFICATES,
    source_references=(
        "docs/files/WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md#3",
        "docs/files/WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md#4",
        "docs/files/WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md#5.2",
        "docs/files/WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md#13",
    ),
)


def _colored_cycle_order(
    declared: FrozenValue,
) -> int | None:
    """lcm over declared cycles of (l if channel_sum even else 2l); None if malformed."""

    if not isinstance(declared, tuple) or not declared:
        return None
    contributions: list[int] = []
    for entry in declared:
        if not isinstance(entry, tuple) or len(entry) != 2:
            return None
        length, channel_sum = entry
        if not _is_exact_int(length) or not _is_exact_int(channel_sum) or length < 1:
            return None
        contributions.append(length if channel_sum % 2 == 0 else 2 * length)
    return lcm(*contributions)


def recognize_branch_inertia_stratification(request: PathfinderRequest) -> RecognitionOutcome:
    family = BRANCH_INERTIA_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        require_shape(request, family, "inertia_classification"),
        require_odd_characteristic(request, family),
    ):
        if gate is not None:
            return gate

    if not _declared_true(request, "residue_characteristic_not_two"):
        return refuse(
            family,
            "wild_or_residue_characteristic_two",
            "The parity reading of inertia is tame-only: residue characteristic 2 (or an "
            "undeclared residue characteristic) makes the order-2 sign generators and the "
            "colored cycle rule inapplicable.",
            "residue_characteristic_not_two",
        )

    problem = lower_request(request)
    cover = problem.cover
    if cover is None or not cover.parity_rows:
        return refuse(
            family,
            "missing_parity_rows",
            "The stratum's incident valuation-parity rows were not declared.",
            "cover.parity_rows",
        )
    rows = cover.parity_rows
    try:
        rank = f2_rank(rows)
    except ValueError:
        return refuse(
            family,
            "malformed_parity_rows",
            "The declared incident parity rows do not share one width over F2.",
            "rectangular parity rows",
        )
    if len(rows) > 1 and not _declared_true(request, "transverse_intersection"):
        return refuse(
            family,
            "missing_transversality",
            "A multi-row stratum needs the normal-crossing/transversality declaration "
            "before its inertia can be read as the F2 span (Prop 4.1); a single "
            "height-one Kummer divisor is exempt (Thm 3.1). The non-transverse "
            "sub-balance contact yields colored C_4 instead.",
            "transverse_intersection",
        )

    classify_parameters: dict[str, object] = {
        "f2_rank": rank,
        "group_description": f"(C_2)^{rank}",
    }
    declared_cycles = lookup(request.mathematical_context, "collision_cycles")
    if declared_cycles is not None:
        cyclic_order = _colored_cycle_order(declared_cycles)
        if cyclic_order is None:
            return refuse(
                family,
                "invalid_collision_cycles",
                "The declared collision cycles must be a nonempty tuple of "
                "(cycle length >= 1, integer channel sum) pairs.",
                "collision_cycles as ((length, channel_sum), ...)",
            )
        classify_parameters["colored_cyclic_order"] = cyclic_order
        classify_parameters["colored_cycle_rule"] = (
            "a cycle of length l contributes l if its channel sum is 0 and 2l otherwise; "
            "the cyclic order is the lcm of the contributions"
        )

    steps = (
        RouteStep(
            "span-rows",
            "span_incident_parity_rows",
            ("incident_parity_rows",),
            ("incident_span",),
            freeze_mapping({"row_count": len(rows)}),
        ),
        RouteStep(
            "classify",
            "classify_local_inertia",
            ("incident_span",),
            ("local_inertia_classification",),
            freeze_mapping(classify_parameters),
        ),
        RouteStep(
            "emit-obligations",
            "emit_inertia_certificate_obligations",
            ("local_inertia_classification",),
            ("inertia_stratification_route",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=BRANCH_INERTIA_CONTRACT,
        steps=steps,
        data_dependencies=("incident_parity_rows", "transversality_declaration"),
        required_intermediate_objects=("incident_span", "local_inertia_classification"),
        completion_condition=(
            "The external certifier realizes transversality on the normalized model and "
            "the independent loops; the classification (C_2)^r (with any colored cyclic "
            "orders) is then an equality rather than a containment."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            exact_operation_count=3,
            scout_operation_count=1,
            expression_depth=1,
        ),
        structural_preference_rank=1,
    )


# ---------------------------------------------------------------------------
# collision_partition_inertia  (Thm 10.2 U semidirect P; sections 12.2/12.3)
# ---------------------------------------------------------------------------

COLLISION_INERTIA_CERTIFICATES = (
    Obligation(
        "collision-type-transversality",
        "Transversality/realization of the declared collision types: the controlling "
        "theorem classifies the possible inertia, it does not assert the collision "
        "stratum's existence.",
        "exact-stratification",
    ),
    Obligation(
        "loop-realization-equality",
        "Equality I_local = U semidirect P requires the loops to be realized "
        "independently; until then only the containment I_local inside U semidirect P "
        "is certified.",
        "exact-loop-realization",
    ),
    Obligation(
        "sub-balance-colored-table",
        "On the non-transverse sub-balance stratum the colored table (section 12.3) "
        "governs: S_1 = 0, S_3 != 0, B_1 != 0 give an order-4 colored generator after "
        "adjoining sqrt(u).",
        "exact-local-hypotheses",
    ),
)

COLLISION_INERTIA_CONTRACT = RouteContract(
    route_family="collision_partition_inertia",
    accepted_problem_shape="collision_inertia",
    required_hypotheses=(
        "characteristic != 2",
        "separable cover of the declared degree (the corpus instance is degree 5)",
        "tame: residue characteristic != 2",
        "the collision partition sums to the cover degree",
        "on the sub-balance stratum: S_3 != 0 and B_1 != 0, else higher contact",
    ),
    required_evidence=(
        "a declared collision partition of the cover degree",
        "the P-stable incident valuation-parity rows",
    ),
    produced_obligations=(
        Obligation(
            "certify-collision-inertia",
            "Certify the realization of the collision types; the local inertia then "
            "embeds in U semidirect P with U the P-stable F2 span of the incident parity "
            "vectors and P the Young subgroup of the partition, with equality when the "
            "loops are realized independently (Thm 10.2, Thm 13.1(3)).",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "equal squared charges N_a^2 = N_b^2 is a CROSSING of normalized sheets, not "
        "ramification: u_pm(t) = u_0 +- c*t + O(t^2) with c != 0 (unramified), and the "
        "eliminant discriminant's crossing multiplicity is even",
        "the sub-balance stratum carries colored C_4 inertia, not a Young-subgroup form",
    ),
    execution_module="external.collision_inertia_executor",
    certificate_obligations=COLLISION_INERTIA_CERTIFICATES,
    source_references=(
        "docs/files/WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md#10.2",
        "docs/files/WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md#12.2",
        "docs/files/WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md#12.3",
    ),
)


def recognize_collision_partition_inertia(request: PathfinderRequest) -> RecognitionOutcome:
    family = COLLISION_INERTIA_CONTRACT.route_family
    for gate in (
        family_enabled(request, family),
        require_shape(request, family, "collision_inertia"),
        require_odd_characteristic(request, family),
    ):
        if gate is not None:
            return gate

    problem = lower_request(request)
    cover = problem.cover
    if cover is None or not cover.parity_rows:
        return refuse(
            family,
            "missing_parity_rows",
            "The collision stratum's incident valuation-parity rows were not declared.",
            "cover.parity_rows",
        )
    declared_partition = lookup(request.mathematical_context, "collision_partition")
    if declared_partition is None:
        return refuse(
            family,
            "missing_collision_partition",
            "No collision partition was declared; the Young subgroup P is undefined.",
            "collision_partition",
        )
    if (
        not isinstance(declared_partition, tuple)
        or not declared_partition
        or any(not _is_exact_int(part) or part < 1 for part in declared_partition)
    ):
        return refuse(
            family,
            "invalid_collision_partition",
            "The collision partition must be a nonempty tuple of positive integers.",
            "collision_partition as a tuple of positive integers",
        )
    partition = tuple(int(part) for part in declared_partition)
    if cover.degree < 1 or sum(partition) != cover.degree:
        return refuse(
            family,
            "invalid_collision_partition",
            f"The declared collision partition {partition} does not sum to the declared "
            f"cover degree {cover.degree if cover.degree >= 1 else '(undeclared)'}; "
            "the Young subgroup S_{m_1} x ... x S_{m_t} must partition the sheet set.",
            "sum(collision_partition) = cover.degree >= 1",
        )
    try:
        parity_rank = f2_rank(cover.parity_rows)
    except ValueError:
        return refuse(
            family,
            "malformed_parity_rows",
            "The declared incident parity rows do not share one width over F2.",
            "rectangular parity rows",
        )

    young_order = 1
    for part in partition:
        young_order *= factorial(part)
    young_description = " x ".join(f"S_{part}" for part in partition)

    steps = (
        RouteStep(
            "young",
            "partition_to_young_subgroup",
            ("collision_partition",),
            ("young_subgroup",),
            freeze_mapping(
                {
                    "partition": partition,
                    "young_subgroup": young_description,
                    "young_order": young_order,
                }
            ),
        ),
        RouteStep(
            "span",
            "span_stable_parity_rows",
            ("incident_parity_rows",),
            ("stable_parity_span",),
            freeze_mapping({"parity_rank": parity_rank}),
        ),
        RouteStep(
            "emit-obligations",
            "emit_semidirect_inertia_obligations",
            ("young_subgroup", "stable_parity_span"),
            ("collision_inertia_route",),
            freeze_mapping(
                {
                    "partition": partition,
                    "young_order": young_order,
                    "parity_rank": parity_rank,
                    "containment": "I_local is contained in U semidirect P; equality is "
                    "an external realization obligation",
                }
            ),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=COLLISION_INERTIA_CONTRACT,
        steps=steps,
        data_dependencies=("collision_partition", "incident_parity_rows"),
        required_intermediate_objects=("young_subgroup", "stable_parity_span"),
        completion_condition=(
            "The external certifier realizes the collision types and their independent "
            "loops; the semidirect containment then sharpens to equality."
        ),
        burden_vector=BurdenVector(
            invariant_level=1,
            exact_operation_count=3,
            scout_operation_count=1,
            expression_depth=1,
        ),
        structural_preference_rank=1,
    )


PROVIDERS: tuple[RouteProvider, ...] = (
    RouteProvider(
        route_family="branch_inertia_stratification",
        contract=BRANCH_INERTIA_CONTRACT,
        recognizer=recognize_branch_inertia_stratification,
        native_scouts=(parity_matrix_scout,),
        wrapper_capabilities=("parity_span_classification",),
    ),
    RouteProvider(
        route_family="collision_partition_inertia",
        contract=COLLISION_INERTIA_CONTRACT,
        recognizer=recognize_collision_partition_inertia,
        native_scouts=(parity_matrix_scout,),
        wrapper_capabilities=("young_subgroup_assembly", "parity_span_classification"),
    ),
)
