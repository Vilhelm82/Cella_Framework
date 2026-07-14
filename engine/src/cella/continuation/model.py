"""Immutable typed records for the staged Cella Continuation Engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from fractions import Fraction


class CoefficientRing(str, Enum):
    Z = "Z"
    Z_HALF = "Z[1/2]"
    Z_I = "Z[i]"
    Z_HALF_I = "Z[1/2,i]"


@dataclass(frozen=True, slots=True)
class AlgebraicFieldSpec:
    field_id: str
    generators: tuple[str, ...]
    defining_relations: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AlgebraicNumber:
    field_id: str
    minimal_polynomial: tuple[int, ...]
    isolating_rectangle: tuple[Fraction, Fraction, Fraction, Fraction]


@dataclass(frozen=True, slots=True)
class ExactPathSegment:
    segment_kind: str
    exact_data: tuple[tuple[str, str], ...]
    orientation: int

    def __post_init__(self) -> None:
        if self.orientation not in {-1, 1}:
            raise ValueError("path orientation must be +1 or -1")


@dataclass(frozen=True, slots=True)
class ExactPath:
    path_id: str
    start_id: str
    end_id: str
    segments: tuple[ExactPathSegment, ...]
    winding_data: tuple[tuple[str, int], ...] = ()


@dataclass(frozen=True, slots=True)
class FamilyManifest:
    manifest_id: str
    adapter_id: str
    coefficient_field: AlgebraicFieldSpec
    equations: tuple[str, ...]
    digest: str


@dataclass(frozen=True, slots=True)
class SingularDivisorManifest:
    manifest_id: str
    divisors: tuple[str, ...]
    digest: str


@dataclass(frozen=True, slots=True)
class RelativeModuleSpec:
    basis: tuple[str, ...]
    boundary_map: tuple[tuple[str, str], ...]
    intersection_data: tuple[tuple[str, str], ...]
    quotient_submodule: tuple[str, ...]
    basis_digest: str


@dataclass(frozen=True, slots=True)
class SelectedState:
    state_id: str
    coefficient_ring: CoefficientRing
    vector: tuple[str, ...]
    sheet_label: str
    branch_label: str
    pole_label: str
    unresolved_compact_corrections: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ObservableManifest:
    observable_id: str
    normalization: str
    required_ring: CoefficientRing
    digest: str


@dataclass(frozen=True, slots=True)
class ProofBudget:
    max_steps: int = 10_000
    max_recurrence_order: int = 512
    max_work_bits: int = 1024

    def __post_init__(self) -> None:
        if min(self.max_steps, self.max_recurrence_order, self.max_work_bits) <= 0:
            raise ValueError("proof-budget limits must be positive")


@dataclass(frozen=True, slots=True)
class ContinuationRequest:
    request_id: str
    adapter_id: str
    adapter_version: str
    target: str
    requested_bits: int
    family_manifest_digest: str
    exact_path_digest: str
    selected_state_digest: str
    coefficient_ring: CoefficientRing
    proof_budget: ProofBudget = field(default_factory=ProofBudget)

    def __post_init__(self) -> None:
        if not self.request_id.strip() or not self.adapter_id.strip():
            raise ValueError("request and adapter identity must be explicit")
        if isinstance(self.requested_bits, bool) or self.requested_bits <= 0:
            raise ValueError("requested_bits must be a positive integer")


@dataclass(frozen=True, slots=True)
class PathfinderPlan:
    schema_id: str
    pathfinder_version: str
    pathfinder_source_digest: str
    admitted_domain_id: str
    request_digest: str
    target: str
    requested_bits: int
    kernel_id: str
    static_schedule_digest: str
    canonical_route_json: str
    computational_route_digest: str
    panel_schedule: tuple[tuple[int, int, int, int], ...]
    constructor_invariants: tuple[str, ...]
    numeric_representation: str
    plan_digest: str


@dataclass(frozen=True, slots=True)
class RoutePlan:
    pathfinder_plan: PathfinderPlan
    source_theorem_digests: tuple[str, ...]
    route_digest: str


@dataclass(frozen=True, slots=True)
class RouteCertificate:
    schema_id: str
    schema_version: str
    request: ContinuationRequest
    pathfinder_plan: PathfinderPlan
    pf0_confirmation_digest: str
    adapter_manifest_digest: str
    legacy_certificate_digest: str
    route_digest: str


@dataclass(frozen=True, slots=True)
class EvaluationCertificate:
    schema_id: str
    schema_version: str
    route_certificate: RouteCertificate
    legacy_certificate_json: str
    achieved_width_bits: int
    evaluation_digest: str


@dataclass(frozen=True, slots=True)
class ContinuationCheckpoint:
    schema_id: str
    adapter_id: str
    family_manifest_digest: str
    exact_path_digest: str
    selected_state_digest: str
    coefficient_ring: CoefficientRing
    pathfinder_plan_digest: str
    certified_prefix_digest: str
    next_segment_index: int
    previous_checkpoint_digest: str | None
    checkpoint_digest: str


@dataclass(frozen=True, slots=True)
class ContinuationResult:
    request: ContinuationRequest
    plan: PathfinderPlan


@dataclass(frozen=True, slots=True)
class VerificationReport:
    valid: bool
    code: str
    checked_obligations: tuple[str, ...]
    certificate_digest: str | None = None


@dataclass(frozen=True, slots=True)
class Refusal:
    code: str
    failed_obligation: str
    source_location: str
    larger_budget_may_help: bool
    new_theorem_or_adapter_required: bool
    detail: str


@dataclass(frozen=True, slots=True)
class CertifiedResult(ContinuationResult):
    route_certificate: RouteCertificate
    evaluation_certificate: EvaluationCertificate


@dataclass(frozen=True, slots=True)
class CertifiedPrefix(ContinuationResult):
    checkpoint: ContinuationCheckpoint
    remaining_path_digest: str


@dataclass(frozen=True, slots=True)
class InsufficientProofBudget:
    request: ContinuationRequest
    plan: PathfinderPlan
    refusal: Refusal


@dataclass(frozen=True, slots=True)
class UnsupportedRequest:
    request: ContinuationRequest
    refusal: Refusal


@dataclass(frozen=True, slots=True)
class CorridorContinuationRequest:
    request_id: str
    adapter_id: str
    adapter_version: str
    route_id: str
    family_manifest_digest: str
    divisor_manifest_digest: str
    route_manifest_digest: str
    theorem_digest: str
    selected_state_digest: str
    coefficient_ring: CoefficientRing
    surface_scope: str


@dataclass(frozen=True, slots=True)
class CorridorPathfinderPlan:
    schema_id: str
    pathfinder_version: str
    pathfinder_source_digest: str
    provider_source_digest: str
    pf0_confirmation_digest: str
    request_digest: str
    route_id: str
    canonical_route_json: str
    computational_route_digest: str
    constructor_invariants: tuple[str, ...]
    plan_digest: str


@dataclass(frozen=True, slots=True)
class CorridorRouteCertificate:
    schema_id: str
    schema_version: str
    request: CorridorContinuationRequest
    pathfinder_plan: CorridorPathfinderPlan
    clearance_certificate_digest: str
    initial_sheet: str
    terminal_sheet: str
    deck_parity: int
    selected_target_quotient_class: str
    unresolved_compact_correction: str
    certificate_digest: str


@dataclass(frozen=True, slots=True)
class CertifiedCorridorResult:
    request: CorridorContinuationRequest
    plan: CorridorPathfinderPlan
    route_certificate: CorridorRouteCertificate
