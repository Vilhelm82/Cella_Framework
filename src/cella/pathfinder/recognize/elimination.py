"""Elimination-terrain recognizers: generic elimination, boundary split, host default.

``generic_elimination`` (ticket PF-PLAN-002; handoff #8.2 elimination-order
route): the admissible comparison candidate.  Its burden vector is dominated
by every structural route, so an admitted structural route always wins the
ordered comparison; when no structural route is admitted, this route is
selected rather than refusing.  The external M2 wrapper may still refuse
lifting; that decision belongs to the wrapper, never to this recognizer.

``localization_boundary_split`` (v1.3 Law 5, §11.8): saturate to a declared
open set while every excluded boundary stratum becomes an explicit retained
task; the open condition f != 0 stays recorded in scope.

``ordinary_host_computation``: the host's own default route as an explicit
admissible candidate — present because it is genuinely fastest for some
requests, not as an excuse for an unimplemented provider.  It always carries
the highest burden and the last preference rank.

Sources: CELLA_ARCHITECTURE_v1.3.md#11.2, #11.8 and
campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md#8.2.
"""

from __future__ import annotations

from ..api.contract import RecognitionOutcome, RouteContract
from ..api.request import PathfinderRequest
from ..api.route import RouteStep
from ..ir.burden import BurdenVector
from ..ir.obligation import Obligation
from ..ir.problem import lower_request
from ..ir.values import freeze_mapping
from ..plan.admissibility import family_enabled, lookup, refuse, require_shape
from ..plan.assemble import assemble_candidate
from ..plan.registry import RouteProvider


# ---------------------------------------------------------------------------
# generic_elimination — the admissible comparison candidate (PF-PLAN-002)


GENERIC_ELIMINATION_SHAPES = (
    "signed_contact_projection",
    "complete_signed_contact_projection",
    "ideal_projection",
    "ideal_elimination",
)
_GENERIC_SHAPE_LABEL = "|".join(GENERIC_ELIMINATION_SHAPES)

GENERIC_ELIMINATION_CERTIFICATES = (
    Obligation(
        "elimination-projection-closure",
        "The eliminated ideal equals the closure of the projection image of the saturated ideal.",
        "exact-ideal-equality",
    ),
    Obligation(
        "saturation-scope-record",
        "The saturation scope is recorded and the excluded locus is retained as explicit boundary tasks.",
        "scope-record",
    ),
)

GENERIC_ELIMINATION_CONTRACT = RouteContract(
    route_family="generic_elimination",
    accepted_problem_shape=_GENERIC_SHAPE_LABEL,
    required_hypotheses=(
        "the coefficient characteristic is declared exactly",
        "the sheet/eliminable variables are declared in context or in the external binding",
    ),
    required_evidence=("declared sheet variables",),
    produced_obligations=(
        Obligation(
            "execute-generic-elimination",
            "Saturate by the declared denominator, eliminate the sheet variables, and emit the eliminated ideal.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "any admitted structural route dominates this comparison candidate in the ordered comparison",
        "the external wrapper may refuse lifting when it cannot represent the eliminated image",
    ),
    execution_module="external.generic_elimination_executor",
    certificate_obligations=GENERIC_ELIMINATION_CERTIFICATES,
    source_references=(
        "campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md#8.2",
        "CELLA_ARCHITECTURE_v1.3.md#11.2",
        "docs/pathfinder/BUILD_SPEC.md",
    ),
)


def recognize_generic_elimination(request: PathfinderRequest) -> RecognitionOutcome:
    """Admit whenever shape, characteristic, and sheet variables are declared."""

    family = GENERIC_ELIMINATION_CONTRACT.route_family
    gate = family_enabled(request, family)
    if gate is not None:
        return gate
    shape = lookup(request.mathematical_context, "problem_shape")
    if shape not in GENERIC_ELIMINATION_SHAPES:
        return refuse(
            family,
            "shape_mismatch",
            "The task does not declare a projection/elimination problem shape.",
            *GENERIC_ELIMINATION_SHAPES,
        )
    characteristic = lookup(request.mathematical_context, "characteristic")
    if not isinstance(characteristic, int) or isinstance(characteristic, bool):
        return refuse(
            family,
            "missing_characteristic",
            "The coefficient characteristic must be declared exactly.",
            "integer characteristic",
        )

    sheet_variables = lookup(request.mathematical_context, "sheet_variables")
    sheet_source = "mathematical_context"
    if sheet_variables is not None:
        if (
            not isinstance(sheet_variables, tuple)
            or not sheet_variables
            or not all(isinstance(v, str) and v for v in sheet_variables)
        ):
            return refuse(
                family,
                "missing_sheet_variables",
                "The declared sheet variables must be a non-empty tuple of variable names.",
                "sheet_variables as a tuple of variable names",
            )
    else:
        sheet_variables = dict(request.external_binding).get("sheet_variables")
        sheet_source = "external_binding"
        if sheet_variables is None:
            return refuse(
                family,
                "missing_sheet_variables",
                "Neither the mathematical context nor the external binding declares the sheet/eliminable variables.",
                "mathematical_context.sheet_variables",
                "external_binding.sheet_variables",
            )

    denominator = lookup(request.mathematical_context, "generic_denominator")
    declared_denominator = (
        denominator if isinstance(denominator, str) and denominator.strip() else "identity"
    )

    steps = (
        RouteStep(
            "saturate-denominator",
            "saturate_by_declared_denominator",
            ("target_ideal",),
            ("saturated_ideal",),
            freeze_mapping(
                {"denominator": declared_denominator, "excluded_locus_retained": True}
            ),
        ),
        RouteStep(
            "eliminate-sheets",
            "eliminate_sheet_variables",
            ("saturated_ideal",),
            ("eliminated_ideal",),
            freeze_mapping(
                {"sheet_variables": sheet_variables, "sheet_variable_source": sheet_source}
            ),
        ),
        RouteStep(
            "emit-eliminated",
            "emit_eliminated_ideal_in_external_bindings",
            ("eliminated_ideal",),
            ("host_eliminated_ideal",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=GENERIC_ELIMINATION_CONTRACT,
        steps=steps,
        data_dependencies=("target_ideal", "sheet_variables"),
        required_intermediate_objects=("saturated_ideal", "eliminated_ideal"),
        completion_condition="The external executor emits the eliminated ideal in host bindings.",
        burden_vector=BurdenVector(
            invariant_level=2,
            global_expansion_rank=2,
            elimination_rank=3,
            exact_operation_count=2,
            scout_operation_count=0,
            expression_depth=0,
        ),
        structural_preference_rank=3,
    )


# ---------------------------------------------------------------------------
# localization_boundary_split — v1.3 Law 5, §11.8


LOCALIZATION_BOUNDARY_SPLIT_CERTIFICATES = (
    Obligation(
        "saturation-witness",
        "The open restriction equals the exact saturation I : d^infinity with an explicit witness.",
        "exact-saturation-witness",
    ),
    Obligation(
        "boundary-tasks-retained",
        "Every excluded boundary stratum is retained as an explicit task in the ledger.",
        "task-ledger",
    ),
    Obligation(
        "open-condition-retained",
        "The defining open condition f != 0 remains recorded in the route scope.",
        "scope-record",
    ),
)

LOCALIZATION_BOUNDARY_SPLIT_CONTRACT = RouteContract(
    route_family="localization_boundary_split",
    accepted_problem_shape="generic_open_restriction",
    required_hypotheses=(
        "the open restriction is declared by strata or by a generic denominator",
        "removed components stay retained as explicit boundary tasks",
    ),
    required_evidence=("declared strata or generic_denominator",),
    produced_obligations=(
        Obligation(
            "execute-localization-boundary-split",
            "Saturate to the declared open set, record the boundary tasks, and emit the open restriction.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "saturation may destroy a displayed complete-intersection presentation; re-certify after localization (v1.3 §11.8)",
        "the reported degree is the degree of the saturated closure, never of the discarded boundary",
    ),
    execution_module="external.localization_boundary_split_executor",
    certificate_obligations=LOCALIZATION_BOUNDARY_SPLIT_CERTIFICATES,
    source_references=(
        "CELLA_ARCHITECTURE_v1.3.md#11.8",
        "campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md#8.2",
    ),
)


def recognize_localization_boundary_split(request: PathfinderRequest) -> RecognitionOutcome:
    """Law 5: nothing is silently discarded; every excluded boundary is a task."""

    family = LOCALIZATION_BOUNDARY_SPLIT_CONTRACT.route_family
    gate = family_enabled(request, family)
    if gate is not None:
        return gate
    gate = require_shape(
        request, family, LOCALIZATION_BOUNDARY_SPLIT_CONTRACT.accepted_problem_shape
    )
    if gate is not None:
        return gate

    problem = lower_request(request)
    denominator = lookup(request.mathematical_context, "generic_denominator")
    declared_denominator = (
        denominator if isinstance(denominator, str) and denominator.strip() else None
    )
    if not problem.strata and declared_denominator is None:
        return refuse(
            family,
            "missing_open_stratum_declaration",
            "The request declares neither domain strata nor a generic denominator, so there is no open set to restrict to.",
            "mathematical_context.strata",
            "mathematical_context.generic_denominator",
        )

    boundary_tasks: list[tuple[str, str, str]] = []
    assumed_conditions: list[str] = []
    for stratum in problem.strata:
        if stratum.status == "assumed":
            assumed_conditions.append(stratum.condition)
            boundary_tasks.append(("complement", stratum.name, stratum.condition))
        else:
            boundary_tasks.append((stratum.status, stratum.name, stratum.condition))
    if declared_denominator is not None:
        boundary_tasks.append(
            ("denominator_locus", "generic_denominator", f"{declared_denominator} = 0")
        )

    steps = (
        RouteStep(
            "saturate-open",
            "saturate_to_open",
            ("target_ideal",),
            ("open_restricted_ideal",),
            freeze_mapping(
                {
                    "denominator": declared_denominator or "declared_strata",
                    "assumed_conditions": tuple(assumed_conditions),
                }
            ),
        ),
        RouteStep(
            "record-boundaries",
            "record_excluded_boundary_tasks",
            ("open_restricted_ideal",),
            ("boundary_task_ledger",),
            freeze_mapping(
                {"boundary_tasks": tuple(boundary_tasks), "task_count": len(boundary_tasks)}
            ),
        ),
        RouteStep(
            "emit-open-restriction",
            "emit_open_restriction",
            ("open_restricted_ideal", "boundary_task_ledger"),
            ("host_open_restriction",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=LOCALIZATION_BOUNDARY_SPLIT_CONTRACT,
        steps=steps,
        data_dependencies=("target_ideal", "strata"),
        required_intermediate_objects=("open_restricted_ideal", "boundary_task_ledger"),
        completion_condition="The external executor emits the open restriction and the retained boundary-task ledger.",
        burden_vector=BurdenVector(
            invariant_level=1,
            global_expansion_rank=0,
            elimination_rank=1,
            exact_operation_count=1 + len(boundary_tasks),
            scout_operation_count=0,
            expression_depth=0,
        ),
        structural_preference_rank=2,
    )


# ---------------------------------------------------------------------------
# ordinary_host_computation — the host default as an explicit candidate


ORDINARY_HOST_COMPUTATION_CERTIFICATES = (
    Obligation(
        "host-default-result-identity",
        "The emitted result is exactly the host default route's result.",
        "host-exact",
    ),
    Obligation(
        "host-default-exactness",
        "Exactness is inherited from the host's declared semantics for the default operation.",
        "host-semantics",
    ),
)

ORDINARY_HOST_COMPUTATION_CONTRACT = RouteContract(
    route_family="ordinary_host_computation",
    accepted_problem_shape="any",
    required_hypotheses=(
        "the wrapper declares the host's default operation for this task",
    ),
    required_evidence=("context key host_default_route naming the host default operation",),
    produced_obligations=(
        Obligation(
            "execute-host-default",
            "Execute the host's declared default route and emit its result.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "an admitted structural route always precedes this candidate in the ordered comparison",
    ),
    execution_module="external.host_default_executor",
    certificate_obligations=ORDINARY_HOST_COMPUTATION_CERTIFICATES,
    source_references=(
        "campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md#8.1",
        "campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md#9",
    ),
)


def recognize_ordinary_host_computation(request: PathfinderRequest) -> RecognitionOutcome:
    """The host default route as an explicit candidate; any declared shape."""

    family = ORDINARY_HOST_COMPUTATION_CONTRACT.route_family
    gate = family_enabled(request, family)
    if gate is not None:
        return gate

    host_default = lookup(request.mathematical_context, "host_default_route")
    if not isinstance(host_default, str) or not host_default.strip():
        return refuse(
            family,
            "missing_host_default_declaration",
            "The wrapper did not declare the host's default operation for this task.",
            "mathematical_context.host_default_route",
        )

    steps = (
        RouteStep(
            "execute-host-default",
            "execute_host_default_route",
            ("host_task",),
            ("host_default_result",),
            freeze_mapping({"operation": host_default}),
        ),
        RouteStep(
            "emit-host-result",
            "emit_host_result_in_external_bindings",
            ("host_default_result",),
            ("host_result",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=ORDINARY_HOST_COMPUTATION_CONTRACT,
        steps=steps,
        data_dependencies=("host_task",),
        required_intermediate_objects=("host_default_result",),
        completion_condition="The external executor emits the host default route's result in host bindings.",
        burden_vector=BurdenVector(
            invariant_level=3,
            global_expansion_rank=3,
            elimination_rank=3,
            exact_operation_count=1,
            scout_operation_count=0,
            expression_depth=0,
        ),
        structural_preference_rank=4,
    )


PROVIDERS: tuple[RouteProvider, ...] = (
    RouteProvider(
        route_family="generic_elimination",
        contract=GENERIC_ELIMINATION_CONTRACT,
        recognizer=recognize_generic_elimination,
        native_scouts=(),
        wrapper_capabilities=("saturation", "elimination_order"),
    ),
    RouteProvider(
        route_family="localization_boundary_split",
        contract=LOCALIZATION_BOUNDARY_SPLIT_CONTRACT,
        recognizer=recognize_localization_boundary_split,
        native_scouts=(),
        wrapper_capabilities=("saturation", "boundary_task_ledger"),
    ),
    RouteProvider(
        route_family="ordinary_host_computation",
        contract=ORDINARY_HOST_COMPUTATION_CONTRACT,
        recognizer=recognize_ordinary_host_computation,
        native_scouts=(),
        wrapper_capabilities=("host_default_dispatch",),
    ),
)
