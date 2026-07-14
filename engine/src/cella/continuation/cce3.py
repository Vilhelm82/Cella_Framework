"""CCE-3 theorem-bound typed relative-class certificates and API."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path

from .canonical import canonical_digest, canonical_json_bytes
from .model import CoefficientRing, CorridorRouteCertificate, Refusal
from .relative_classes import (
    BoundaryObstructionWitness,
    CPVClassRecord,
    CertifiedLateralPair,
    ClaimScope,
    RelativeBasisManifest,
    RelativeClassError,
    RelativeClassVector,
    construct_basis_manifest,
    construct_lateral_pair,
    form_cpv,
    multiply_by_i,
    prove_integral_phase_obstruction,
)


CCE3_SCHEMA_ID = "cella.continuation.cce3_relative_class_certificate"
CCE3_SCHEMA_VERSION = "1.0"
CCE3_CANONICALIZATION_VERSION = "cella.canonical.json.v1"
CCE3_VERIFIER_VERSION = "cella.continuation.cce3.verifier.v1"
BASE_COMMIT = "50683b971399236abe413cafcf2c56c5b1b9228c"
PF0_CONFIRMATION_DIGEST = "304fccce5ed1206f23969952634d10b250d8d4d7a7a955971afa8018c2372008"
CCE2_BUNDLE_DIGEST = "b2fc82f6705cfe25070a641f4678f2caf94c35e36a11bc1023a9fd9a4f56605c"
PAPER_III_POST_INSERTION_DIGEST = "1fc835086c30fbae414853f186a9cab9ac8c39e6cff1ed79b7364ebb5db6d5ae"
CCE2_THEOREM_DIGEST = "bfb0dc4c4678803cc46e791cbe60e87736ea41ce14db157e8fb1726e28b671fe"
CCE2_DIVISOR_DIGEST = "cf893db1c6c2718a614dfdf519e220cbb3b7312aff62130c608ddd7598c1c93a"
CCE2_LATERAL_DIGEST = "f94cb784d7218e3fa2f03c024a4921457b1d517ddfa022c81a90865c4dec5143"


@dataclass(frozen=True, slots=True)
class CCE3Request:
    request_id: str
    operation: str
    requested_ring: CoefficientRing
    input_class: str = "delta_plus"
    requested_claim_scope: ClaimScope = ClaimScope.EXACT_COMPACT_QUOTIENT_CLASS

    @property
    def digest(self) -> str:
        return canonical_digest(self)


@dataclass(frozen=True, slots=True)
class CCE3SourceLedger:
    repository_identity: str
    paper_iii_digest: str
    theorem_ids_and_digests: tuple[tuple[str, str], ...]
    basis_source_digests: tuple[str, ...]
    selected_quotient_groupoid_digest: str
    pf0_confirmation_digest: str
    pathfinder_closure_digest: str
    dbp_provider_digest: str
    cce3_source_digest: str
    cce2_bundle_digest: str

    @property
    def digest(self) -> str:
        return canonical_digest(self)


@dataclass(frozen=True, slots=True)
class CCE3OperationPlan:
    plan_id: str
    request_digest: str
    nested_cce2_plan_digests: tuple[str, str]
    ordered_steps: tuple[str, ...]
    canonical_plan_json: str
    plan_digest: str


@dataclass(frozen=True, slots=True)
class CCE3RelativeClassCertificate:
    schema_id: str
    schema_version: str
    canonicalization_version: str
    source_ledger: CCE3SourceLedger
    request: CCE3Request
    operation_plan: CCE3OperationPlan
    upper_route_certificate: CorridorRouteCertificate
    lower_route_certificate: CorridorRouteCertificate
    basis_manifest: RelativeBasisManifest
    lateral_pair: CertifiedLateralPair
    cpv_record: CPVClassRecord | None
    phased_class: RelativeClassVector | None
    obstruction_witness: BoundaryObstructionWitness | None
    output_digest: str
    previous_checkpoint_digest: str | None
    verifier_version: str
    canonical_certificate_digest: str


@dataclass(frozen=True, slots=True)
class CertifiedRelativeClassResult:
    request: CCE3Request
    certificate: CCE3RelativeClassCertificate


@dataclass(frozen=True, slots=True)
class CCE3Checkpoint:
    schema_id: str
    request_digest: str
    certificate_digest: str
    certified_prefix: tuple[str, ...]
    remaining_operations_digest: str
    previous_checkpoint_digest: str | None
    checkpoint_digest: str


def released_cce3_request(operation: str, requested_ring: CoefficientRing) -> CCE3Request:
    scopes = {
        "lateral_pair": ClaimScope.AFFINE_OVER_COMPACT_SUBMODULE,
        "cpv": ClaimScope.SCALAR_EXTENDED_AFFINE_CLASS,
        "phase_upper": ClaimScope.EXACT_ABSOLUTE_CLASS,
        "phase_lower": ClaimScope.EXACT_ABSOLUTE_CLASS,
        "phase_cpv": ClaimScope.EXACT_ABSOLUTE_CLASS,
        "prove_phase_obstruction": ClaimScope.EXACT_ABSOLUTE_CLASS,
    }
    return CCE3Request(
        f"cce3-{operation}-{requested_ring.name.lower()}",
        operation,
        requested_ring,
        "delta_plus",
        scopes.get(operation, ClaimScope.EXACT_COMPACT_QUOTIENT_CLASS),
    )


def _pathfinder_identity() -> tuple[str, str]:
    package_root = Path(__file__).parents[1] / "pathfinder"
    source_digest = canonical_digest(tuple(
        (str(path.relative_to(Path(__file__).parents[2])), hashlib.sha256(path.read_bytes()).hexdigest())
        for path in sorted(package_root.rglob("*.py"))
    ))
    provider = package_root / "recognize/dbp_native.py"
    return source_digest, hashlib.sha256(provider.read_bytes()).hexdigest()


def _source_ledger() -> CCE3SourceLedger:
    closure, provider = _pathfinder_identity()
    repository_root = Path(__file__).parents[4]
    paper_path = repository_root / "research/paper/Theorems/DBP/DBP_CURVATURE_PERIODS_OF_THE_DBP_QUADRIC_v1.0.md"
    live_paper_digest = hashlib.sha256(paper_path.read_bytes()).hexdigest()
    if live_paper_digest != PAPER_III_POST_INSERTION_DIGEST:
        raise RelativeClassError("SourceDigestMismatch", "paper_iii_digest", "Paper III bytes changed after the authorized CCE-2 insertion")
    cce3_source_digest = canonical_digest(tuple(
        (path.name, hashlib.sha256(path.read_bytes()).hexdigest())
        for path in (Path(__file__).with_name("relative_classes.py"), Path(__file__))
    ))
    return CCE3SourceLedger(
        BASE_COMMIT,
        PAPER_III_POST_INSERTION_DIGEST,
        (
            ("PaperIII.Theorem7F.1", PAPER_III_POST_INSERTION_DIGEST),
            ("CCE2.ExactCorridorTheorem", CCE2_THEOREM_DIGEST),
            ("CCE2.DivisorReduction", CCE2_DIVISOR_DIGEST),
            ("CCE2.LateralCalibration", CCE2_LATERAL_DIGEST),
        ),
        (PAPER_III_POST_INSERTION_DIGEST, CCE2_THEOREM_DIGEST, CCE2_LATERAL_DIGEST),
        "40461c1fbb177e0d173f0b11a5d12224dc7ce894bb7fd43c944c8fa75cdaf0d9",
        PF0_CONFIRMATION_DIGEST,
        closure,
        provider,
        cce3_source_digest,
        CCE2_BUNDLE_DIGEST,
    )


def _route_certificates() -> tuple[CorridorRouteCertificate, CorridorRouteCertificate]:
    from .api import continue_corridor_certified
    from .pathfinder import released_corridor_request

    upper = continue_corridor_certified(released_corridor_request("upper"))
    lower = continue_corridor_certified(released_corridor_request("lower"))
    if not hasattr(upper, "route_certificate") or not hasattr(lower, "route_certificate"):
        raise RelativeClassError("RouteCertificateRequired", "nested_cce2_certificates", "both CCE-2 routes must certify")
    if canonical_digest((upper.route_certificate, lower.route_certificate)) != CCE2_BUNDLE_DIGEST:
        raise RelativeClassError("SourceDigestMismatch", "cce2_bundle_digest", "nested CCE-2 certificate bundle changed")
    return upper.route_certificate, lower.route_certificate


def _operation_plan(
    request: CCE3Request,
    upper: CorridorRouteCertificate,
    lower: CorridorRouteCertificate,
) -> CCE3OperationPlan:
    common = (
        "replay_upper_cce2_route_certificate",
        "replay_lower_cce2_route_certificate",
        "bind_relative_basis_boundary_and_compact_quotient",
        "construct_integral_lateral_pair_with_independent_affine_corrections",
    )
    tails = {
        "lateral_pair": (),
        "cpv": ("extend_scalars_and_form_endpoint_quotient_affine_cpv",),
        "phase_upper": ("extend_to_gaussian_ring_and_multiply_upper_by_i",),
        "phase_lower": ("extend_to_gaussian_ring_and_multiply_lower_by_i",),
        "phase_cpv": ("form_cpv_then_extend_to_dyadic_gaussian_ring_and_multiply_by_i",),
        "prove_phase_obstruction": ("replay_boundary_i_beta_outside_integral_boundary_lattice",),
    }
    if request.operation not in tails:
        raise RelativeClassError("UnsupportedOperation", "cce3_operation_domain", f"unsupported operation {request.operation!r}")
    steps = common + tails[request.operation]
    plan_data = {
        "plan_id": "cella.cce3.exact_relative_operation_plan.v1",
        "request_digest": request.digest,
        "nested_cce2_plan_digests": (
            upper.pathfinder_plan.plan_digest,
            lower.pathfinder_plan.plan_digest,
        ),
        "ordered_steps": steps,
        "numeric_semantics": "exact integers and dyadic Gaussian scalars; no binary floating point",
        "pathfinder_policy": "reuse nested CCE-2 canonical route plans; do not create a redundant route finder",
    }
    encoded = canonical_json_bytes(plan_data).decode("utf-8")
    return CCE3OperationPlan(
        "cella.cce3.exact_relative_operation_plan.v1",
        request.digest,
        (upper.pathfinder_plan.plan_digest, lower.pathfinder_plan.plan_digest),
        steps,
        encoded,
        canonical_digest(plan_data),
    )


def _refusal(request: CCE3Request, error: RelativeClassError) -> Refusal:
    return Refusal(
        error.code,
        error.obligation,
        "cella.continuation.cce3.continue_relative_class_certified",
        False,
        error.code not in {"RingTooSmall", "BoundaryObstruction", "EvaluationStageRequired"},
        error.detail,
    )


def _assemble(request: CCE3Request, previous_checkpoint_digest: str | None = None) -> CCE3RelativeClassCertificate:
    if request.input_class != "delta_plus":
        raise RelativeClassError("UnsupportedInputClass", "selected_delta_plus", "CCE-3 only accepts delta_plus")
    if request.operation in {"absolute_scalar", "absolute_from_affine"}:
        raise RelativeClassError("AbsoluteRepresentativeUnknown", "compact_correction_coordinates", "absolute representative is not fixed")
    if request.operation == "full_transport_matrix":
        raise RelativeClassError("FullTransportMatrixUnavailable", "compact_monodromy_coordinates", "full A/B matrix is not proved")
    if request.operation in {"evaluate", "numeric_cpv"}:
        raise RelativeClassError("EvaluationStageRequired", "cce4_observable_stage", "CCE-3 returns classes, not numeric values")
    if request.operation in {"surface_lift", "whole_surface", "compose_routes", "reverse_route"}:
        raise RelativeClassError("UnsupportedOperation", "cce3_scope", "operation lies outside CCE-3")
    if request.operation == "integral_phase_replacement":
        raise RelativeClassError("BoundaryObstruction", "i_beta_not_integral", "phased boundary i*beta cannot lie in Z*beta modulo closed cycles")

    expected_scopes = {
        "lateral_pair": ClaimScope.AFFINE_OVER_COMPACT_SUBMODULE,
        "cpv": ClaimScope.SCALAR_EXTENDED_AFFINE_CLASS,
        "phase_upper": ClaimScope.EXACT_ABSOLUTE_CLASS,
        "phase_lower": ClaimScope.EXACT_ABSOLUTE_CLASS,
        "phase_cpv": ClaimScope.EXACT_ABSOLUTE_CLASS,
        "prove_phase_obstruction": ClaimScope.EXACT_ABSOLUTE_CLASS,
    }
    if request.operation in expected_scopes and request.requested_claim_scope != expected_scopes[request.operation]:
        raise RelativeClassError("QuotientScopeMismatch", "requested_claim_scope", "request attempts to escalate or alter the proved claim scope")

    source = _source_ledger()
    upper, lower = _route_certificates()
    basis = construct_basis_manifest(source.paper_iii_digest)
    pair = construct_lateral_pair(upper, lower, basis)
    plan = _operation_plan(request, upper, lower)
    cpv: CPVClassRecord | None = None
    phased: RelativeClassVector | None = None
    obstruction: BoundaryObstructionWitness | None = None
    output: object = pair

    if request.operation == "lateral_pair":
        if request.requested_ring != CoefficientRing.Z:
            raise RelativeClassError("IllegalImplicitScalarExtension", "lateral_pair_ring", "integral lateral-pair constructor is declared over Z")
    elif request.operation == "cpv":
        cpv = form_cpv(pair, basis, request.requested_ring)
        output = cpv
    elif request.operation in {"phase_upper", "phase_lower"}:
        selected = pair.upper_selected_class if request.operation == "phase_upper" else pair.lower_selected_class
        phased = multiply_by_i(selected, request.requested_ring)
        output = phased
    elif request.operation == "phase_cpv":
        if request.requested_ring != CoefficientRing.Z_HALF_I:
            raise RelativeClassError("RingTooSmall", "dyadic_gaussian_phase", "i*CPV requires Z[1/2,i]")
        cpv = form_cpv(pair, basis, CoefficientRing.Z_HALF_I)
        phased = multiply_by_i(cpv.selected_endpoint_half_sum, CoefficientRing.Z_HALF_I)
        output = phased
    elif request.operation == "prove_phase_obstruction":
        obstruction = prove_integral_phase_obstruction(pair.upper_selected_class)
        output = obstruction

    unsigned = {
        "schema_id": CCE3_SCHEMA_ID,
        "schema_version": CCE3_SCHEMA_VERSION,
        "canonicalization_version": CCE3_CANONICALIZATION_VERSION,
        "source_ledger": source,
        "request": request,
        "operation_plan": plan,
        "upper_route_certificate": upper,
        "lower_route_certificate": lower,
        "basis_manifest": basis,
        "lateral_pair": pair,
        "cpv_record": cpv,
        "phased_class": phased,
        "obstruction_witness": obstruction,
        "output_digest": canonical_digest(output),
        "previous_checkpoint_digest": previous_checkpoint_digest,
        "verifier_version": CCE3_VERIFIER_VERSION,
    }
    return CCE3RelativeClassCertificate(**unsigned, canonical_certificate_digest=canonical_digest(unsigned))


def continue_relative_class_certified(request: CCE3Request) -> CertifiedRelativeClassResult | Refusal:
    try:
        certificate = _assemble(request)
    except RelativeClassError as error:
        return _refusal(request, error)
    return CertifiedRelativeClassResult(request, certificate)


def verify_cce3_certificate(certificate: CCE3RelativeClassCertificate) -> bool | Refusal:
    from .api import verify_corridor_certificate

    if verify_corridor_certificate(certificate.upper_route_certificate) is not True or verify_corridor_certificate(certificate.lower_route_certificate) is not True:
        return Refusal("RouteCertificateMismatch", "nested_cce2_replay", "cella.continuation.cce3.verify_cce3_certificate", False, False, "nested route certificate failed")
    try:
        expected = _assemble(certificate.request, certificate.previous_checkpoint_digest)
    except RelativeClassError as error:
        return _refusal(certificate.request, error)
    if canonical_json_bytes(expected) != canonical_json_bytes(certificate):
        return Refusal("CertificateTampered", "exact_certificate_replay", "cella.continuation.cce3.verify_cce3_certificate", False, False, "certificate bytes do not replay")
    return True


def make_cce3_checkpoint(
    result: CertifiedRelativeClassResult,
    certified_prefix: tuple[str, ...] | None = None,
    previous_checkpoint: CCE3Checkpoint | None = None,
) -> CCE3Checkpoint:
    prefix = certified_prefix or result.certificate.operation_plan.ordered_steps[:4]
    remaining = tuple(step for step in result.certificate.operation_plan.ordered_steps if step not in prefix)
    unsigned = {
        "schema_id": "cella.continuation.cce3_checkpoint.v1",
        "request_digest": result.request.digest,
        "certificate_digest": result.certificate.canonical_certificate_digest,
        "certified_prefix": prefix,
        "remaining_operations_digest": canonical_digest(remaining),
        "previous_checkpoint_digest": previous_checkpoint.checkpoint_digest if previous_checkpoint else None,
    }
    return CCE3Checkpoint(**unsigned, checkpoint_digest=canonical_digest(unsigned))


def _checkpoint_self_digest_valid(checkpoint: CCE3Checkpoint) -> bool:
    unsigned = {
        "schema_id": checkpoint.schema_id,
        "request_digest": checkpoint.request_digest,
        "certificate_digest": checkpoint.certificate_digest,
        "certified_prefix": checkpoint.certified_prefix,
        "remaining_operations_digest": checkpoint.remaining_operations_digest,
        "previous_checkpoint_digest": checkpoint.previous_checkpoint_digest,
    }
    return checkpoint.checkpoint_digest == canonical_digest(unsigned)


def verify_cce3_checkpoint_chain(chain: tuple[CCE3Checkpoint, ...]) -> bool:
    previous_digest: str | None = None
    for checkpoint in chain:
        if not _checkpoint_self_digest_valid(checkpoint) or checkpoint.previous_checkpoint_digest != previous_digest:
            return False
        previous_digest = checkpoint.checkpoint_digest
    return True


def verify_cce3_checkpoint(
    checkpoint: CCE3Checkpoint,
    result: CertifiedRelativeClassResult,
    previous_chain: tuple[CCE3Checkpoint, ...] = (),
) -> bool:
    remaining = tuple(step for step in result.certificate.operation_plan.ordered_steps if step not in checkpoint.certified_prefix)
    return (
        verify_cce3_checkpoint_chain(previous_chain)
        and checkpoint.previous_checkpoint_digest == (previous_chain[-1].checkpoint_digest if previous_chain else None)
        and checkpoint.request_digest == result.request.digest
        and checkpoint.certificate_digest == result.certificate.canonical_certificate_digest
        and checkpoint.remaining_operations_digest == canonical_digest(remaining)
        and _checkpoint_self_digest_valid(checkpoint)
    )


def resume_cce3(
    checkpoint: CCE3Checkpoint,
    request: CCE3Request,
    previous_chain: tuple[CCE3Checkpoint, ...] = (),
) -> CertifiedRelativeClassResult | Refusal:
    fresh = continue_relative_class_certified(request)
    if isinstance(fresh, Refusal) or not verify_cce3_checkpoint(checkpoint, fresh, previous_chain):
        return Refusal("CheckpointMismatch", "checkpoint_chain", "cella.continuation.cce3.resume_cce3", False, False, "checkpoint does not match request and replayed certificate")
    try:
        certificate = _assemble(request, checkpoint.checkpoint_digest)
    except RelativeClassError as error:
        return _refusal(request, error)
    return CertifiedRelativeClassResult(request, certificate)


__all__ = [
    "CCE3Checkpoint", "CCE3OperationPlan", "CCE3RelativeClassCertificate",
    "CCE3Request", "CCE3SourceLedger", "CertifiedRelativeClassResult",
    "continue_relative_class_certified", "make_cce3_checkpoint",
    "released_cce3_request", "resume_cce3", "verify_cce3_certificate",
    "verify_cce3_checkpoint",
    "verify_cce3_checkpoint_chain",
]
