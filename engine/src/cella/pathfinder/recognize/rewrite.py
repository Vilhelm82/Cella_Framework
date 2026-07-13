"""Symbolic-collapse rewrite recognizer for scalar cancellation expressions.

Route family ``symbolic_collapse_rewrite`` covers the prototype arithmetic
rewrite routes (self-collapse, constant-offset collapse, scaled-offset
collapse, difference-of-squares, sqrt-conjugate, common-factor extraction).
The route instructs the host to apply the conservative rewrite families
recorded per subtraction site; it never evaluates the expression and never
emits the rewritten result itself.  Cancellation shapes the conservative
rewrite terrain does not cover are refused mathematically — precision
escalation belongs to the host, not to this route.

Sources: campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md#8.1 and the behavioral
reference src/cella/_legacy_pathfinder.py.
"""

from __future__ import annotations

from ..api.contract import RecognitionOutcome, RouteContract
from ..api.request import PathfinderRequest
from ..api.route import RouteStep
from ..ir.burden import BurdenVector
from ..ir.obligation import Obligation
from ..ir.problem import lower_request
from ..ir.values import freeze_mapping
from ..plan.admissibility import evidence_by_family, family_enabled, refuse, require_shape
from ..plan.assemble import assemble_candidate
from ..plan.registry import RouteProvider
from ..scout import expression_shape_scout


ADMITTED_CANCELLATION_SHAPES = ("self_cancellation", "cancellation_fully_rewriteable")

SYMBOLIC_COLLAPSE_CERTIFICATES = (
    Obligation(
        "rewrite-exact-identity",
        "The rewritten expression equals the original expression exactly as a rational/symbolic identity.",
        "exact-symbolic-identity",
    ),
    Obligation(
        "rewrite-conservative-domain",
        "Every applied rewrite is conservative: the definition domain is not enlarged.",
        "domain-preservation",
    ),
)

SYMBOLIC_COLLAPSE_REWRITE_CONTRACT = RouteContract(
    route_family="symbolic_collapse_rewrite",
    accepted_problem_shape="scalar_expression",
    required_hypotheses=(
        "every subtraction site admits a recorded conservative rewrite family",
        "the expression is shadowable within the declared analysis budget",
    ),
    required_evidence=("expression_shape scout evidence with full rewrite coverage",),
    produced_obligations=(
        Obligation(
            "execute-symbolic-collapse",
            "Apply the recorded per-site conservative rewrites and emit the rewritten expression.",
            "host-exact",
        ),
    ),
    discharged_obligations=(),
    exceptional_branches=(
        "cancellation_unresolved sites are outside the conservative rewrite terrain; precision escalation belongs to the host",
        "expressions without subtraction have nothing to collapse; direct evaluation is the host default",
        "partly rewriteable expressions require a route that mixes rewriting with host evaluation",
    ),
    execution_module="external.symbolic_rewrite_executor",
    certificate_obligations=SYMBOLIC_COLLAPSE_CERTIFICATES,
    source_references=(
        "campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md#8.1",
        "src/cella/_legacy_pathfinder.py",
    ),
)


def recognize_symbolic_collapse_rewrite(request: PathfinderRequest) -> RecognitionOutcome:
    """Admit expressions whose every subtraction site has a conservative rewrite."""

    family = SYMBOLIC_COLLAPSE_REWRITE_CONTRACT.route_family
    gate = family_enabled(request, family)
    if gate is not None:
        return gate
    gate = require_shape(request, family, SYMBOLIC_COLLAPSE_REWRITE_CONTRACT.accepted_problem_shape)
    if gate is not None:
        return gate

    fingerprint = evidence_by_family(request, "expression_shape")
    if fingerprint is None:
        evidence = expression_shape_scout(lower_request(request), request.analysis_budget)
        if evidence is None:
            return refuse(
                family,
                "no_expression",
                "The request declares no scalar expression to rewrite.",
                "mathematical_context.expression",
            )
        fingerprint = dict(evidence.structural_fingerprint)

    shape = fingerprint.get("shape")
    if shape == "no_subtraction":
        return refuse(
            family,
            "no_cancellation_to_collapse",
            "The expression contains no subtraction site; there is nothing to rewrite and direct evaluation is the host default.",
            "at least one subtraction site",
        )
    if shape not in ADMITTED_CANCELLATION_SHAPES:
        return refuse(
            family,
            "unsupported_expression_shape",
            "The conservative rewrite terrain does not cover this cancellation shape; precision escalation belongs to the host.",
            *ADMITTED_CANCELLATION_SHAPES,
        )

    site_count = fingerprint.get("subtraction_site_count")
    site_families = fingerprint.get("site_rewrite_families")
    if not isinstance(site_count, int) or isinstance(site_count, bool) or not isinstance(site_families, tuple):
        return refuse(
            family,
            "evidence_unavailable",
            "The expression_shape evidence does not carry usable per-site rewrite records.",
            "subtraction_site_count",
            "site_rewrite_families",
        )
    depth = fingerprint.get("expression_depth")
    expression_depth = depth if isinstance(depth, int) and not isinstance(depth, bool) else 0

    steps = (
        RouteStep(
            "classify-sites",
            "classify_cancellation_sites",
            ("scalar_expression",),
            ("classified_cancellation_sites",),
            freeze_mapping({"shape": shape, "site_count": site_count}),
        ),
        RouteStep(
            "apply-rewrites",
            "apply_conservative_rewrites",
            ("scalar_expression", "classified_cancellation_sites"),
            ("rewritten_expression",),
            freeze_mapping({"site_rewrite_families": site_families}),
        ),
        RouteStep(
            "emit-rewritten",
            "emit_rewritten_expression_in_external_bindings",
            ("rewritten_expression",),
            ("host_rewritten_expression",),
        ),
    )
    return assemble_candidate(
        request=request,
        contract=SYMBOLIC_COLLAPSE_REWRITE_CONTRACT,
        steps=steps,
        data_dependencies=("scalar_expression",),
        required_intermediate_objects=("classified_cancellation_sites", "rewritten_expression"),
        completion_condition="The external executor emits the conservatively rewritten expression in host bindings.",
        burden_vector=BurdenVector(
            invariant_level=1,
            global_expansion_rank=0,
            elimination_rank=0,
            exact_operation_count=site_count,
            scout_operation_count=1,
            expression_depth=expression_depth,
        ),
        structural_preference_rank=0,
    )


PROVIDERS: tuple[RouteProvider, ...] = (
    RouteProvider(
        route_family="symbolic_collapse_rewrite",
        contract=SYMBOLIC_COLLAPSE_REWRITE_CONTRACT,
        recognizer=recognize_symbolic_collapse_rewrite,
        native_scouts=(expression_shape_scout,),
        wrapper_capabilities=("conservative_expression_rewrite",),
    ),
)
