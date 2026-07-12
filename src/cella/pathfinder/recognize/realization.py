"""Lazy realization-poset route provider (v1.3 section 18, handoff 8.5).

The realization poset is a first-class proof object, not a postprocessed
table: nodes carry defining schemes, codimension, typed degree and
multiplicity records; edges carry inclusion/specialization witnesses.
Construction is lazy and demand-driven — intersections and saturations are
computed once, content-addressed and reused.  Doubled nodes such as
Ceven+IZ = Ceven+(J^2) retain multiplicity and are never silently reduced.
Pathfinder returns the dependency-aware node/edge route only; realization
execution and certificates remain external.
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
    family_enabled,
    lookup,
    refuse,
    require_odd_characteristic,
    require_shape,
)
from ..plan.assemble import assemble_candidate
from ..plan.registry import RouteProvider


REALIZATION_POSET_CERTIFICATES = (
    Obligation(
        "node-invariants-after-declared-saturation",
        "Each realized node carries codimension, typed degree and nonemptiness certified after the declared saturation, never before it.",
        "exact-scheme-invariants",
    ),
    Obligation(
        "edge-witnesses",
        "Every poset edge carries an explicit inclusion or specialization witness.",
        "exact-ideal-containment",
    ),
    Obligation(
        "multiplicity-retention-on-doubled-nodes",
        "Doubled nodes (for example the (J^2)-shaped structure of Ceven+IZ) retain their scheme multiplicity and are never replaced by the reduced support.",
        "scheme-structure",
    ),
    Obligation(
        "boundary-task-retention",
        "Boundary strata excluded from the generic open locus are retained as explicit boundary tasks, never silently dropped.",
        "task-ledger",
    ),
)

REALIZATION_POSET_CONTRACT = RouteContract(
    route_family="lazy_realization_poset",
    accepted_problem_shape="realization_poset",
    required_hypotheses=(
        "the incidence model is declared as explicit ideals",
        "characteristic 0 or odd characteristic (char 2 collapses the signed structure)",
        "the requested nodes are named explicitly; realization is lazy and demand-driven",
        "intersections and saturations are computed once and content-addressed",
        "the generic saturation applies only away from the divisor under study",
    ),
    required_evidence=("declared requested nodes", "declared incidence ideal presentation"),
    produced_obligations=(
        Obligation(
            "execute-lazy-poset-realization",
            "Realize the requested poset nodes and edges lazily and emit them with their certificates in host bindings.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "boundary strata require boundary-specific saturation; the generic saturation is invalid on the very divisor under study",
        "higher-codimension nonemptiness may depend on a compactified discriminant scheme and is refused as poset_node_outside_declared_open",
    ),
    execution_module="external.realization_poset_executor",
    certificate_obligations=REALIZATION_POSET_CERTIFICATES,
    source_references=(
        "CELLA_ARCHITECTURE_v1.3.md#18",
        "docs/m2_out_2026-07-10/REALIZATION_POSET_RUN_REPORT_2026-07-10.md",
        "campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md#8.5",
    ),
)


def _as_pairs(value: FrozenValue | None) -> dict[str, FrozenValue]:
    if isinstance(value, tuple) and all(
        isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], str)
        for item in value
    ):
        return dict(value)  # type: ignore[arg-type]
    return {}


def recognize_lazy_realization_poset(request: PathfinderRequest) -> RecognitionOutcome:
    """Admit lazy node/edge realization over a declared incidence model."""

    family = REALIZATION_POSET_CONTRACT.route_family
    outcome = (
        family_enabled(request, family)
        or require_shape(request, family, REALIZATION_POSET_CONTRACT.accepted_problem_shape)
        or require_odd_characteristic(request, family)
    )
    if outcome is not None:
        return outcome

    poset_declaration = _as_pairs(lookup(request.mathematical_context, "realization_poset"))
    requested_nodes = poset_declaration.get("requested_nodes")
    if (
        not isinstance(requested_nodes, tuple)
        or not requested_nodes
        or not all(isinstance(node, str) and node.strip() for node in requested_nodes)
    ):
        return refuse(
            family,
            "no_requested_nodes",
            "The realization-poset declaration names no requested nodes; lazy realization has no demand to serve.",
            "realization_poset.requested_nodes as a nonempty tuple of node names",
        )

    problem = lower_request(request)
    if not problem.ideals:
        return refuse(
            family,
            "missing_incidence_presentation",
            "No incidence-model ideals were declared; poset nodes have no defining schemes.",
            "ideals with explicit generator strings",
        )

    excluded_strata = tuple(
        stratum.name for stratum in problem.strata if stratum.status == "excluded"
    )
    outside_open = tuple(node for node in requested_nodes if node in excluded_strata)
    if outside_open:
        return refuse(
            family,
            "poset_node_outside_declared_open",
            "Requested nodes lie on excluded strata; their nonemptiness may depend on a compactified discriminant scheme beyond the declared open locus.",
            *outside_open,
        )

    steps = (
        RouteStep(
            "order-nodes",
            "order_requested_nodes_by_dependency",
            ("realization_poset_declaration", "incidence_ideals"),
            ("ordered_node_requests",),
            freeze_mapping({"requested_nodes": requested_nodes}),
        ),
        RouteStep(
            "derive-presentations",
            "derive_node_presentations",
            ("ordered_node_requests", "incidence_ideals"),
            ("node_presentations",),
            freeze_mapping(
                {
                    "intersection_policy": "computed_once_content_addressed",
                    "saturation_policy": "computed_once_content_addressed",
                    "evaluation": "lazy",
                }
            ),
        ),
        RouteStep(
            "attach-records",
            "attach_boundary_and_multiplicity_records",
            ("node_presentations",),
            ("annotated_nodes",),
            freeze_mapping(
                {
                    "doubled_node_policy": "record_multiplicity_never_reduce",
                    "doubled_node_shape": "(J^2)",
                    "boundary_policy": "retain_excluded_boundary_tasks",
                }
            ),
        ),
        RouteStep(
            "emit-poset",
            "emit_poset_node_and_edge_route",
            ("annotated_nodes",),
            ("host_poset_nodes", "host_poset_edges"),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=REALIZATION_POSET_CONTRACT,
        steps=steps,
        data_dependencies=("realization_poset_declaration", "incidence_ideals"),
        required_intermediate_objects=(
            "ordered_node_requests",
            "node_presentations",
            "annotated_nodes",
        ),
        completion_condition="The external executor emits the requested poset nodes and edges with their certificates in host bindings.",
        burden_vector=BurdenVector(
            invariant_level=2,
            global_expansion_rank=0,
            elimination_rank=1,
            exact_operation_count=4,
            scout_operation_count=0,
            expression_depth=2,
        ),
        structural_preference_rank=2,
    )


PROVIDERS: tuple[RouteProvider, ...] = (
    RouteProvider(
        route_family="lazy_realization_poset",
        contract=REALIZATION_POSET_CONTRACT,
        recognizer=recognize_lazy_realization_poset,
        native_scouts=(),
        wrapper_capabilities=(
            "content_addressed_ideal_cache",
            "saturation_and_intersection",
            "scheme_multiplicity_records",
        ),
    ),
)
