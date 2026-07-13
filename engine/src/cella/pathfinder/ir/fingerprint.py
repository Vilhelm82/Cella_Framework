"""Structural fingerprint engine.

One typed record per request covering every analysis axis the recognizers
consult: algebraic shape, cancellation, scale class, factor/dependency
structure, elimination shape, complete-intersection indicators, strata,
symmetry, role/channel/carrier, cover/Kummer/wreath, local-germ and
realization-poset structure, plus a canonical content hash and provenance.

The fingerprint is derived data: it asserts nothing about the host's
deliverable and is never a verdict.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from ..serialize.canonical import canonical_json_bytes
from .evidence import ScoutEvidence
from .problem import NormalizedProblem
from .values import FrozenValue


@dataclass(frozen=True, slots=True)
class StructuralFingerprint:
    fingerprint_id: str
    problem_hash: str
    local_algebraic_shape: str
    cancellation_class: str
    residual_order: str
    scale_precision_class: str
    factor_dependency_structure: tuple[tuple[str, FrozenValue], ...]
    elimination_saturation_shape: str
    complete_intersection_indicators: tuple[tuple[str, FrozenValue], ...]
    domain_stratum_classification: tuple[str, ...]
    symmetry_orbit_structure: tuple[tuple[str, FrozenValue], ...]
    role_channel_carrier: tuple[tuple[str, FrozenValue], ...]
    cover_branch_inertia_kummer_wreath: tuple[tuple[str, FrozenValue], ...]
    local_germ_divisor_structure: tuple[tuple[str, FrozenValue], ...]
    realization_poset_structure: tuple[tuple[str, FrozenValue], ...]
    canonical_cross_form: str
    provenance: tuple[str, ...] = field(default=())


def _evidence_fingerprint(
    evidence: tuple[ScoutEvidence, ...], family: str
) -> dict[str, FrozenValue]:
    for item in evidence:
        if item.scout_family == family:
            return dict(item.structural_fingerprint)
    return {}


def _pairs(mapping: dict[str, FrozenValue]) -> tuple[tuple[str, FrozenValue], ...]:
    return tuple(sorted(mapping.items()))


def fingerprint_problem(
    problem: NormalizedProblem,
    evidence: tuple[ScoutEvidence, ...] = (),
) -> StructuralFingerprint:
    from .problem import stable_problem_hash

    expression_shape = _evidence_fingerprint(evidence, "expression_shape")
    fresh = _evidence_fingerprint(evidence, "fresh_variable_monic")
    triangular = _evidence_fingerprint(evidence, "triangular_tower")
    degrees = _evidence_fingerprint(evidence, "degree_balance")
    parity = _evidence_fingerprint(evidence, "kummer_parity_matrix")
    orbit = _evidence_fingerprint(evidence, "sign_orbit")
    glue = _evidence_fingerprint(evidence, "self_glue_trinomial")
    inertia = _evidence_fingerprint(evidence, "exact_rational_inertia")
    regularity = _evidence_fingerprint(evidence, "dbp_regularity")
    germ_corner = _evidence_fingerprint(evidence, "newton_corner")

    # Local algebraic shape: expression texture when present, else ideal shape.
    if problem.expression is not None:
        local_shape = str(expression_shape.get("shape", "expression_unprofiled"))
    elif problem.ideals:
        local_shape = f"ideal_presentation:{len(problem.ideals)}"
    else:
        local_shape = problem.problem_shape or "undeclared"

    cancellation = str(expression_shape.get("shape", "not_applicable"))
    residual_order = (
        "structural_zero"
        if cancellation == "self_cancellation"
        else "unknown"
        if problem.expression is not None
        else "not_applicable"
    )
    scale_class = (
        "same_leading_constant"
        if cancellation.startswith("cancellation")
        else "no_subtraction"
        if cancellation == "no_subtraction"
        else "not_applicable"
    )

    factor_dependency: dict[str, FrozenValue] = {}
    if glue:
        factor_dependency["self_glue_trinomial"] = _pairs(glue)
    if problem.ideals:
        factor_dependency["ideal_names"] = tuple(ideal.name for ideal in problem.ideals)
        factor_dependency["generator_counts"] = tuple(
            len(ideal.generators) for ideal in problem.ideals
        )

    elimination_shape = problem.operation or (
        "projection" if "projection" in problem.problem_shape else "undeclared"
    )

    ci_indicators: dict[str, FrozenValue] = {}
    if fresh:
        ci_indicators["regular_sequence_certified"] = fresh.get("regular_sequence_certified", False)
        ci_indicators["ring_safe_monic"] = fresh.get("ring_safe_monic", False)
        ci_indicators["fresh_variables"] = fresh.get("fresh_variables", ())
    if triangular:
        ci_indicators["triangular_tower"] = triangular.get("triangular", False)
    if degrees:
        ci_indicators["weighted_degrees"] = degrees.get("weighted_degrees", ())
        ci_indicators["complete_intersection_degree"] = degrees.get(
            "complete_intersection_degree", 0
        )
    if problem.ring is not None and problem.ideals:
        target = problem.ideal("target")
        if target is not None:
            ci_indicators["generators_equal_expected_codim"] = len(target.generators)

    strata = tuple(
        f"{stratum.status}:{stratum.name}:{stratum.condition}" for stratum in problem.strata
    )

    symmetry: dict[str, FrozenValue] = {}
    if problem.symmetry is not None:
        symmetry["kind"] = problem.symmetry.kind
        symmetry["group_name"] = problem.symmetry.group_name
        symmetry["orbit_size"] = problem.symmetry.orbit_size
    if orbit:
        symmetry["complete_sign_orbit"] = orbit.get("complete_orbit", False)
        symmetry["sign_dimension"] = orbit.get("dimension", 0)

    role_channel: dict[str, FrozenValue] = {}
    if problem.role_channels:
        role_channel["channels"] = problem.role_channels
    if regularity:
        role_channel["dbp_q"] = regularity.get("q")
        role_channel["dbp_regular"] = regularity.get("regular", False)
    if inertia:
        role_channel["inertia_signature"] = inertia.get("signature")

    cover_structure: dict[str, FrozenValue] = {}
    if problem.cover is not None:
        cover_structure["degree"] = problem.cover.degree
        cover_structure["channel_count"] = len(problem.cover.channels)
        cover_structure["base_group"] = problem.cover.base_group
        cover_structure["parity_row_count"] = len(problem.cover.parity_rows)
    if parity:
        cover_structure["f2_rank"] = parity.get("f2_rank", 0)
        cover_structure["full_column_rank"] = parity.get("full_column_rank", False)
        cover_structure["kernel_dimension"] = parity.get("kernel_dimension", 0)
        cover_structure["kronecker_structured_shape"] = parity.get(
            "kronecker_structured_shape", False
        )
    if glue:
        cover_structure["self_glue_layer"] = glue.get("layer_candidate", "")

    local_germ: dict[str, FrozenValue] = {}
    if germ_corner:
        local_germ["newton_polar_vertices"] = germ_corner.get("polar_vertices", ())
        local_germ["vertex_cancellation"] = germ_corner.get("vertex_cancellation", False)
    germ_value = problem.context_value("local_germ")
    if isinstance(germ_value, tuple):
        local_germ["declared_germ"] = germ_value

    poset: dict[str, FrozenValue] = {}
    poset_value = problem.context_value("realization_poset")
    if isinstance(poset_value, tuple):
        poset["declared_nodes"] = poset_value

    cross_form = (
        f"{local_shape}|{elimination_shape}|"
        f"ci={bool(ci_indicators.get('regular_sequence_certified'))}"
        f"|cover={cover_structure.get('degree', 0)}x{cover_structure.get('channel_count', 0)}"
        f"|rank={cover_structure.get('f2_rank', 0)}"
    )

    problem_hash = stable_problem_hash(problem)
    body = {
        "problem_hash": problem_hash,
        "cross_form": cross_form,
        "cancellation": cancellation,
        "ci": _pairs(ci_indicators),
        "cover": _pairs(cover_structure),
    }
    digest = hashlib.sha256(canonical_json_bytes(tuple(sorted(body.items())))).hexdigest()[:24]

    return StructuralFingerprint(
        fingerprint_id=f"sfp:v1:{digest}",
        problem_hash=problem_hash,
        local_algebraic_shape=local_shape,
        cancellation_class=cancellation,
        residual_order=residual_order,
        scale_precision_class=scale_class,
        factor_dependency_structure=_pairs(factor_dependency),
        elimination_saturation_shape=elimination_shape,
        complete_intersection_indicators=_pairs(ci_indicators),
        domain_stratum_classification=strata,
        symmetry_orbit_structure=_pairs(symmetry),
        role_channel_carrier=_pairs(role_channel),
        cover_branch_inertia_kummer_wreath=_pairs(cover_structure),
        local_germ_divisor_structure=_pairs(local_germ),
        realization_poset_structure=_pairs(poset),
        canonical_cross_form=cross_form,
        provenance=tuple(sorted({item.scout_family for item in evidence})),
    )
