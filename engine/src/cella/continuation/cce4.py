"""CCE-4 finite-grammar envelopes for the two released DBP observables.

This module deliberately does not parse expressions.  It admits two immutable
KernelSpec programs assembled from the six recurrence operations already used
by :mod:`cella.native_periods.algebraic_series`, then delegates the numerical
proof to the legacy schema-1.1 evaluator without changing that evaluator.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
from pathlib import Path

from cella.native_periods import (
    CertifiedPeriodResult,
    evaluate_dbp_relative_period,
    verify_dbp_certificate,
)
from cella.native_periods.dbp_theta_route import canonical_source, compile_dbp_theta
from cella.native_periods.records import DUAL_PATH, PRIMARY_PATH
from cella.native_periods.schedule import admitted_m1_schedule

from .canonical import canonical_digest, canonical_json_bytes
from .cce3 import (
    CCE3RelativeClassCertificate,
    continue_relative_class_certified,
    released_cce3_request,
    verify_cce3_certificate,
)
from .model import CoefficientRing, Refusal


CCE4_SCHEMA_ID = "cella.continuation.cce4_bounded_evaluation_certificate"
CCE4_SCHEMA_VERSION = "1.0"
CCE4_VERIFIER_VERSION = "cella.continuation.cce4.verifier.v1"
KERNEL_SPEC_VERSION = "cella.continuation.kernel_spec.dbp_smooth.v1"
RECERTIFIED_BITS = (192, 256, 384)
MIN_CERTIFIED_BITS = 16
RELEASE_TARGETS = ("primary", "dual_cpv")


@dataclass(frozen=True, slots=True)
class OpcodeSpec:
    opcode: str
    version: str
    arity: int
    operand_types: tuple[str, ...]
    result_type: str
    coefficient_domain: str
    precondition: str
    exact_rule: str
    analytic_rule: str
    serialization: str
    source_digest: str


@dataclass(frozen=True, slots=True)
class KernelNode:
    node_id: str
    opcode: str
    operands: tuple[str, ...] = ()
    exact_parameter: str | None = None


@dataclass(frozen=True, slots=True)
class KernelSpec:
    spec_id: str
    spec_version: str
    target: str
    kernel_id: str
    nodes: tuple[KernelNode, ...]
    output_node: str
    domain_witnesses: tuple[str, ...]
    opcode_ledger: tuple[OpcodeSpec, ...]
    compiler_source_digest: str
    recurrence_source_digest: str
    canonical_spec_digest: str


@dataclass(frozen=True, slots=True)
class CCE4Request:
    request_id: str
    target: str
    target_bits: int
    requested_kernel_spec_version: str = KERNEL_SPEC_VERSION
    evaluation_mode: str = "exact_reduction_plus_smooth_kernel"
    requested_class_scope: str = "theorem_selected_relative_class"

    @property
    def digest(self) -> str:
        return canonical_digest(self)


@dataclass(frozen=True, slots=True)
class CCE4Certificate:
    schema_id: str
    schema_version: str
    request: CCE4Request
    kernel_spec: KernelSpec
    target_normalization: tuple[str, ...]
    nested_cce3_certificate: CCE3RelativeClassCertificate
    nested_cce2_certificate_digests: tuple[str, str]
    pathfinder_identity: tuple[str, str]
    schedule_ledger: tuple[tuple[int, int, int, int], ...]
    analytic_account: tuple[tuple[str, str], ...]
    dual_polar_reduction: tuple[tuple[str, str], ...]
    legacy_certificate: dict
    exact_dyadic_bracket: dict
    achieved_width_bits: int
    previous_checkpoint_digest: str | None
    verifier_version: str
    canonical_certificate_digest: str


@dataclass(frozen=True, slots=True)
class CertifiedBoundedEvaluation:
    request: CCE4Request
    certificate: CCE4Certificate


@dataclass(frozen=True, slots=True)
class CCE4Checkpoint:
    schema_id: str
    request_digest: str
    certificate_digest: str
    certified_prefix: tuple[str, ...]
    remaining_operations_digest: str
    previous_checkpoint_digest: str | None
    checkpoint_digest: str


class KernelSpecError(ValueError):
    def __init__(self, code: str, obligation: str, detail: str):
        super().__init__(detail)
        self.code, self.obligation, self.detail = code, obligation, detail


def released_cce4_request(target: str, target_bits: int) -> CCE4Request:
    return CCE4Request(f"cce4-{target}-{target_bits}", target, target_bits)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _native_paths() -> tuple[Path, Path]:
    native = Path(__file__).parents[1] / "native_periods"
    return native / "dbp_theta_route.py", native / "algebraic_series.py"


def _opcode_ledger(source_digest: str) -> tuple[OpcodeSpec, ...]:
    common = ("1.0", "exact dyadic interval Taylor series", "canonical JSON node tuple", source_digest)
    return (
        OpcodeSpec("INPUT_AFFINE", common[0], 0, (), common[1], "Q", "center, slope in Q", "a_0=center, a_1=slope, a_k=0", "entire affine series", common[2], common[3]),
        OpcodeSpec("ADD", common[0], 2, (common[1], common[1]), common[1], "Q", "same truncation order", "coefficientwise exact interval addition", "sum of analytic series", common[2], common[3]),
        OpcodeSpec("SCALE_Q", common[0], 1, (common[1],), common[1], "Q", "canonical rational coefficient", "coefficientwise rational scaling", "rational multiple preserves radius", common[2], common[3]),
        OpcodeSpec("MUL", common[0], 2, (common[1], common[1]), common[1], "Q", "finite admitted truncation order", "Cauchy product with outward dyadic rounding", "product majorized on admitted disk", common[2], common[3]),
        OpcodeSpec("SQRT", common[0], 1, (common[1],), common[1], "Q with certified dyadic intervals", "constant term positive and disk avoids branch divisor", "principal-root coefficient recurrence", "positive-real branch and Cauchy disk separation", common[2], common[3]),
        OpcodeSpec("DIV", common[0], 2, (common[1], common[1]), common[1], "Q with certified dyadic intervals", "denominator constant interval excludes zero", "formal quotient coefficient recurrence", "denominator separated on admitted disk", common[2], common[3]),
    )


def _program(target: str) -> tuple[str, tuple[KernelNode, ...], str]:
    common = (
        KernelNode("t", "INPUT_AFFINE", exact_parameter="center,+1"),
        KernelNode("w", "INPUT_AFFINE", exact_parameter="1-center,-1"),
        KernelNode("t2", "MUL", ("t", "t")),
        KernelNode("w2", "MUL", ("w", "w")),
    )
    if target == "primary":
        nodes = common + (
            KernelNode("t4", "MUL", ("t2", "t2")),
            KernelNode("t2w2", "MUL", ("t2", "w2")),
            KernelNode("w4", "MUL", ("w2", "w2")),
            KernelNode("two_t2w2", "SCALE_Q", ("t2w2",), "2/1"),
            KernelNode("two_w4", "SCALE_Q", ("w4",), "2/1"),
            KernelNode("p0", "ADD", ("t4", "two_t2w2")),
            KernelNode("p", "ADD", ("p0", "two_w4")),
            KernelNode("root", "SQRT", ("p",)),
            KernelNode("minus_two_w2", "SCALE_Q", ("w2",), "-2/1"),
            KernelNode("num0", "ADD", ("t2", "minus_two_w2")),
            KernelNode("num", "SCALE_Q", ("num0",), "16/1"),
            KernelNode("eight_w2", "SCALE_Q", ("w2",), "8/1"),
            KernelNode("den0", "ADD", ("t2", "eight_w2")),
            KernelNode("den", "MUL", ("den0", "root")),
            KernelNode("out", "DIV", ("num", "den")),
        )
        return "g_plus_v1", nodes, "out"
    if target == "dual_cpv":
        nodes = common + (
            KernelNode("minus_w2", "SCALE_Q", ("w2",), "-1/1"),
            KernelNode("delta", "ADD", ("t2", "minus_w2")),
            KernelNode("delta2", "MUL", ("delta", "delta")),
            KernelNode("w4", "MUL", ("w2", "w2")),
            KernelNode("p", "ADD", ("delta2", "w4")),
            KernelNode("root", "SQRT", ("p",)),
            KernelNode("sqrt2_input", "INPUT_AFFINE", exact_parameter="2,0"),
            KernelNode("sqrt2", "SQRT", ("sqrt2_input",)),
            KernelNode("sqrt2root", "MUL", ("sqrt2", "root")),
            KernelNode("two_w2", "SCALE_Q", ("w2",), "2/1"),
            KernelNode("inner0", "ADD", ("t2", "two_w2")),
            KernelNode("inner", "ADD", ("inner0", "sqrt2root")),
            KernelNode("num", "SCALE_Q", ("t2",), "-16/1"),
            KernelNode("den", "MUL", ("root", "inner")),
            KernelNode("out", "DIV", ("num", "den")),
        )
        return "g_minus_v1", nodes, "out"
    raise KernelSpecError("KernelSpecMismatch", "released_target", f"no released KernelSpec for {target!r}")


def compile_kernel_spec(target: str) -> KernelSpec:
    if target not in RELEASE_TARGETS:
        raise KernelSpecError("KernelSpecMismatch", "released_target", f"unsupported target {target!r}")
    compiler_path, recurrence_path = _native_paths()
    path = PRIMARY_PATH if target == "primary" else DUAL_PATH
    compiled = compile_dbp_theta(canonical_source(path))
    if not hasattr(compiled, "kernel_id"):
        raise KernelSpecError("KernelSpecMismatch", "native_compiler", "native theorem-directed compiler refused")
    kernel_id, nodes, output = _program(target)
    if compiled.kernel_id != kernel_id:
        raise KernelSpecError("KernelSpecMismatch", "native_kernel_identity", "sealed grammar disagrees with native compiler")
    unsigned = {
        "spec_id": f"cella.dbp.{kernel_id}.kernel_spec.v1",
        "spec_version": KERNEL_SPEC_VERSION,
        "target": target,
        "kernel_id": kernel_id,
        "nodes": nodes,
        "output_node": output,
        "domain_witnesses": tuple(compiled.domain_witnesses),
        "opcode_ledger": _opcode_ledger(_sha(recurrence_path)),
        "compiler_source_digest": _sha(compiler_path),
        "recurrence_source_digest": _sha(recurrence_path),
    }
    return KernelSpec(**unsigned, canonical_spec_digest=canonical_digest(unsigned))


def _validate_spec(spec: KernelSpec, target: str) -> None:
    known = {item.opcode for item in _opcode_ledger(spec.recurrence_source_digest)}
    unknown = tuple(node.opcode for node in spec.nodes if node.opcode not in known)
    if unknown:
        raise KernelSpecError("UnsupportedOpcode", "finite_opcode_grammar", f"unknown opcode {unknown[0]!r}")
    expected = compile_kernel_spec(target)
    if canonical_json_bytes(spec) != canonical_json_bytes(expected):
        raise KernelSpecError("KernelSpecMismatch", "canonical_kernel_spec", "KernelSpec is not the released canonical program")


def _refusal(error: KernelSpecError) -> Refusal:
    return Refusal(error.code, error.obligation, "cella.continuation.cce4", False, error.code != "RequestedWidthNotProved", error.detail)


def _assemble(request: CCE4Request, spec: KernelSpec | None = None, previous_checkpoint_digest: str | None = None) -> CCE4Certificate:
    if request.target not in RELEASE_TARGETS:
        raise KernelSpecError("KernelSpecMismatch", "released_target", "target is outside the two-kernel release")
    if isinstance(request.target_bits, bool) or not isinstance(request.target_bits, int) or request.target_bits < MIN_CERTIFIED_BITS:
        raise KernelSpecError("RequestedWidthNotProved", "positive_precision_domain", f"certified Taylor evaluation requires target_bits >= {MIN_CERTIFIED_BITS}")
    if request.requested_kernel_spec_version != KERNEL_SPEC_VERSION:
        raise KernelSpecError("KernelSpecMismatch", "kernel_spec_version", "requested KernelSpec version is not admitted")
    if request.evaluation_mode != "exact_reduction_plus_smooth_kernel":
        raise KernelSpecError("EvaluationCertificateMismatch", "evaluation_mode", "numerical CPV or alternate evaluation modes are not admitted")
    if request.requested_class_scope != "theorem_selected_relative_class":
        raise KernelSpecError("EvaluationCertificateMismatch", "relative_class_scope", "quotient-only or absolute representative escalation is not admitted")
    spec = spec or compile_kernel_spec(request.target)
    _validate_spec(spec, request.target)

    operation, ring = (("lateral_pair", CoefficientRing.Z) if request.target == "primary" else ("cpv", CoefficientRing.Z_HALF))
    class_result = continue_relative_class_certified(released_cce3_request(operation, ring))
    if not hasattr(class_result, "certificate"):
        raise KernelSpecError("EvaluationCertificateMismatch", "nested_cce3_certificate", "CCE-3 class construction did not certify")
    legacy = evaluate_dbp_relative_period(request.target, request.target_bits, certificate=True)
    if not isinstance(legacy, CertifiedPeriodResult) or legacy.certificate_record is None:
        raise KernelSpecError("EvaluationCertificateMismatch", "legacy_schema_1_1_evaluation", "native evaluator did not certify")
    if verify_dbp_certificate(legacy.certificate_record) is not True:
        raise KernelSpecError("EvaluationCertificateMismatch", "legacy_schema_1_1_replay", "native certificate replay failed")
    if legacy.dyadic_bracket.width_bits < request.target_bits:
        raise KernelSpecError("RequestedWidthNotProved", "dyadic_bracket_width", "legacy enclosure missed requested width")

    schedule = admitted_m1_schedule(spec.kernel_id)
    log2_lower = {2: Fraction(1), 3: Fraction(3, 2), 4: Fraction(2), 6: Fraction(5, 2), 8: Fraction(3)}
    def admitted_order(item: dict) -> int:
        required = Fraction(request.target_bits + 32, 1) / log2_lower[item["radius_multiplier"]]
        return max(item["order"], (required.numerator + required.denominator - 1) // required.denominator)
    schedule_ledger = tuple((x["panel"], admitted_order(x), request.target_bits + 8 + x["guard_bits"], x["radius_multiplier"]) for x in schedule["panel_schedules"])
    nested = class_result.certificate
    polar = (
        ("runtime_cpv", "false"),
        ("polar_kernel_cpv", "0"),
        ("rationalizing_identity", "A^2 - 2*P_minus = -t^2*D"),
    ) if request.target == "dual_cpv" else (("runtime_cpv", "not_applicable"),)
    normalization = (
        ("native integral scale", "1/2"),
        ("post-normalization", "subtract exactly enclosed 2*pi" if request.target == "primary" else "none"),
        ("terminal", "transport-safe exact dyadic bracket; decimal is explanatory only"),
    )
    unsigned = {
        "schema_id": CCE4_SCHEMA_ID,
        "schema_version": CCE4_SCHEMA_VERSION,
        "request": request,
        "kernel_spec": spec,
        "target_normalization": normalization,
        "nested_cce3_certificate": nested,
        "nested_cce2_certificate_digests": (nested.upper_route_certificate.certificate_digest, nested.lower_route_certificate.certificate_digest),
        "pathfinder_identity": (nested.source_ledger.pathfinder_closure_digest, nested.source_ledger.pf0_confirmation_digest),
        "schedule_ledger": schedule_ledger,
        "analytic_account": (
            ("rule", legacy.remainder_ledger["rule"]),
            ("quadrature_remainder", str(legacy.remainder_ledger["quadrature_remainder"])),
            ("operation_defect_digest", legacy.account_ledger["operation_defect_digest"]),
            ("account_closed", "true"),
        ),
        "dual_polar_reduction": polar,
        "legacy_certificate": legacy.certificate_record,
        "exact_dyadic_bracket": legacy.dyadic_bracket.to_record(),
        "achieved_width_bits": legacy.dyadic_bracket.width_bits,
        "previous_checkpoint_digest": previous_checkpoint_digest,
        "verifier_version": CCE4_VERIFIER_VERSION,
    }
    return CCE4Certificate(**unsigned, canonical_certificate_digest=canonical_digest(unsigned))


def evaluate_bounded_observable(request: CCE4Request, kernel_spec: KernelSpec | None = None) -> CertifiedBoundedEvaluation | Refusal:
    try:
        certificate = _assemble(request, kernel_spec)
    except KernelSpecError as error:
        return _refusal(error)
    return CertifiedBoundedEvaluation(request, certificate)


def verify_cce4_certificate(certificate: CCE4Certificate) -> bool | Refusal:
    if verify_cce3_certificate(certificate.nested_cce3_certificate) is not True:
        return Refusal("EvaluationCertificateMismatch", "nested_cce3_replay", "cella.continuation.cce4.verify", False, False, "nested CCE-3 certificate failed")
    if verify_dbp_certificate(certificate.legacy_certificate) is not True:
        return Refusal("EvaluationCertificateMismatch", "legacy_replay", "cella.continuation.cce4.verify", False, False, "nested native certificate failed")
    try:
        expected = _assemble(certificate.request, previous_checkpoint_digest=certificate.previous_checkpoint_digest)
    except KernelSpecError as error:
        return _refusal(error)
    if canonical_json_bytes(expected) != canonical_json_bytes(certificate):
        return Refusal("EvaluationCertificateMismatch", "exact_certificate_replay", "cella.continuation.cce4.verify", False, False, "certificate bytes do not replay")
    return True


def _operations(result: CertifiedBoundedEvaluation) -> tuple[str, ...]:
    return (
        "bind_canonical_kernel_spec", "replay_nested_cce2_routes", "replay_nested_cce3_class",
        "admit_panel_disk_schedule", "execute_exact_recurrence", "close_analytic_tail_account",
        "apply_target_normalization", "materialize_exact_dyadic_bracket",
    )


def make_cce4_checkpoint(result: CertifiedBoundedEvaluation, certified_prefix: tuple[str, ...] | None = None, previous_checkpoint: CCE4Checkpoint | None = None) -> CCE4Checkpoint:
    operations = _operations(result)
    prefix = certified_prefix or operations[:4]
    if prefix != operations[:len(prefix)]:
        raise ValueError("checkpoint prefix must be an ordered execution prefix")
    unsigned = {
        "schema_id": "cella.continuation.cce4_checkpoint.v1",
        "request_digest": result.request.digest,
        "certificate_digest": result.certificate.canonical_certificate_digest,
        "certified_prefix": prefix,
        "remaining_operations_digest": canonical_digest(operations[len(prefix):]),
        "previous_checkpoint_digest": previous_checkpoint.checkpoint_digest if previous_checkpoint else None,
    }
    return CCE4Checkpoint(**unsigned, checkpoint_digest=canonical_digest(unsigned))


def _checkpoint_valid(checkpoint: CCE4Checkpoint) -> bool:
    unsigned = {name: getattr(checkpoint, name) for name in (
        "schema_id", "request_digest", "certificate_digest", "certified_prefix",
        "remaining_operations_digest", "previous_checkpoint_digest",
    )}
    return checkpoint.checkpoint_digest == canonical_digest(unsigned)


def verify_cce4_checkpoint_chain(chain: tuple[CCE4Checkpoint, ...]) -> bool:
    previous = None
    for checkpoint in chain:
        if not _checkpoint_valid(checkpoint) or checkpoint.previous_checkpoint_digest != previous:
            return False
        previous = checkpoint.checkpoint_digest
    return True


def verify_cce4_checkpoint(checkpoint: CCE4Checkpoint, result: CertifiedBoundedEvaluation, previous_chain: tuple[CCE4Checkpoint, ...] = ()) -> bool:
    operations = _operations(result)
    prefix = checkpoint.certified_prefix
    return (
        verify_cce4_checkpoint_chain(previous_chain)
        and checkpoint.previous_checkpoint_digest == (previous_chain[-1].checkpoint_digest if previous_chain else None)
        and prefix == operations[:len(prefix)]
        and checkpoint.request_digest == result.request.digest
        and checkpoint.certificate_digest == result.certificate.canonical_certificate_digest
        and checkpoint.remaining_operations_digest == canonical_digest(operations[len(prefix):])
        and _checkpoint_valid(checkpoint)
    )


def resume_cce4(checkpoint: CCE4Checkpoint, request: CCE4Request, previous_chain: tuple[CCE4Checkpoint, ...] = ()) -> CertifiedBoundedEvaluation | Refusal:
    fresh = evaluate_bounded_observable(request)
    if isinstance(fresh, Refusal) or not verify_cce4_checkpoint(checkpoint, fresh, previous_chain):
        return Refusal("EvaluationCertificateMismatch", "checkpoint_chain", "cella.continuation.cce4.resume", False, False, "checkpoint does not match replayed request")
    try:
        certificate = _assemble(request, previous_checkpoint_digest=checkpoint.checkpoint_digest)
    except KernelSpecError as error:
        return _refusal(error)
    return CertifiedBoundedEvaluation(request, certificate)


__all__ = [
    "CCE4Certificate", "CCE4Checkpoint", "CCE4Request", "CertifiedBoundedEvaluation",
    "KernelNode", "KernelSpec", "OpcodeSpec", "compile_kernel_spec",
    "evaluate_bounded_observable", "make_cce4_checkpoint", "released_cce4_request",
    "resume_cce4", "verify_cce4_certificate", "verify_cce4_checkpoint",
    "verify_cce4_checkpoint_chain",
]
