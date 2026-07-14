"""CCE-4 finite grammar, bounded evaluation, hostile replay and checkpoints."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.continuation.canonical import canonical_json_bytes
from cella.continuation.cce4 import (
    CertifiedBoundedEvaluation, compile_kernel_spec, evaluate_bounded_observable,
    make_cce4_checkpoint, released_cce4_request, resume_cce4,
    verify_cce4_certificate, verify_cce4_checkpoint, verify_cce4_checkpoint_chain,
)
from cella.continuation.model import Refusal
from cella.native_periods import evaluate_dbp_relative_period, verify_dbp_certificate
from cella.native_periods.algebraic_series import integrate_recurrence_panel
from cella.native_periods.exact_scalar import Interval
from cella.native_periods.quadrature import integrate_certified
from cella.native_periods.schedule import admitted_m1_schedule


passed = 0


def check(label: str, condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


def interval(bracket) -> tuple[Fraction, Fraction]:
    denominator = 1 << bracket.denominator_exponent
    return Fraction(bracket.lower_numerator, denominator), Fraction(bracket.upper_numerator, denominator)


def contains(outer, inner) -> bool:
    a, b = interval(outer)
    c, d = interval(inner)
    return a <= c <= d <= b


primary_spec = compile_kernel_spec("primary")
dual_spec = compile_kernel_spec("dual_cpv")
check("six-opcode grammar", tuple(x.opcode for x in primary_spec.opcode_ledger) == ("INPUT_AFFINE", "ADD", "SCALE_Q", "MUL", "SQRT", "DIV"))
check("primary sealed program", primary_spec.kernel_id == "g_plus_v1" and len(primary_spec.nodes) == 19)
check("dual sealed program", dual_spec.kernel_id == "g_minus_v1" and len(dual_spec.nodes) == 19)
check("grammar deterministic", canonical_json_bytes(primary_spec) == canonical_json_bytes(compile_kernel_spec("primary")))

results = {}
for target in ("primary", "dual_cpv"):
    previous = None
    for bits in (192, 256, 384):
        request = released_cce4_request(target, bits)
        first = evaluate_bounded_observable(request)
        second = evaluate_bounded_observable(request)
        check(f"{target}/{bits} certifies", isinstance(first, CertifiedBoundedEvaluation))
        check(f"{target}/{bits} deterministic", canonical_json_bytes(first) == canonical_json_bytes(second))
        check(f"{target}/{bits} verifies", isinstance(first, CertifiedBoundedEvaluation) and verify_cce4_certificate(first.certificate) is True)
        if not isinstance(first, CertifiedBoundedEvaluation):
            continue
        legacy = evaluate_dbp_relative_period(target, bits, certificate=True)
        check(f"{target}/{bits} legacy verifies", verify_dbp_certificate(legacy.certificate_record) is True)
        check(f"{target}/{bits} byte-compatible bracket", first.certificate.exact_dyadic_bracket == legacy.dyadic_bracket.to_record())
        check(f"{target}/{bits} width", first.certificate.achieved_width_bits >= bits)
        if previous is not None:
            check(f"{target}/{bits} precision nesting", contains(previous.certificate.nested_cce3_certificate and previous.certificate.legacy_certificate and evaluate_dbp_relative_period(target, previous.request.target_bits).dyadic_bracket, legacy.dyadic_bracket))
        previous = first
        results[(target, bits)] = first

# The historical 192/256/384 matrix is a recertification matrix, not a hard
# precision ceiling.  Exercise an exact non-matrix precision.
expanded = evaluate_bounded_observable(released_cce4_request("primary", 64))
check("arbitrary precision certifies", isinstance(expanded, CertifiedBoundedEvaluation))
check("arbitrary precision verifies", isinstance(expanded, CertifiedBoundedEvaluation) and verify_cce4_certificate(expanded.certificate) is True)
check("arbitrary precision width", isinstance(expanded, CertifiedBoundedEvaluation) and expanded.certificate.achieved_width_bits >= 64)

# The dual proof is reduction plus a smooth kernel, never runtime contour cancellation.
dual = results[("dual_cpv", 192)].certificate
check("dual runtime CPV disabled", dict(dual.dual_polar_reduction)["runtime_cpv"] == "false")
check("dual polar CPV exact zero", dict(dual.dual_polar_reduction)["polar_kernel_cpv"] == "0")
check("primary normalization records pi", "2*pi" in dict(results[("primary", 192)].certificate.target_normalization)["post-normalization"])
check("native certificate remains schema 1.1", dual.legacy_certificate["schema_version"] == "1.1")

# One independent 2x subdivision replay per kernel.  It need only overlap the
# admitted enclosure; it is a diagnostic theorem replay, not a replacement schedule.
for target, kernel in (("primary", "g_plus_v1"), ("dual_cpv", "g_minus_v1")):
    bits = 200
    base = integrate_certified(kernel, bits)
    schedule = admitted_m1_schedule(kernel)
    total = Interval.point(0)
    for item in schedule["panel_schedules"]:
        a, b = Fraction(item["panel"], schedule["panels"]), Fraction(item["panel"] + 1, schedule["panels"])
        m = (a + b) / 2
        for lo, hi in ((a, m), (m, b)):
            panel, _ = integrate_recurrence_panel(kernel, lo, hi, max(item["order"], 96), bits + item["guard_bits"], item["radius_multiplier"])
            total += panel
    check(f"{target} subdivision overlap", total.lo <= base.enclosure.hi and base.enclosure.lo <= total.hi)

# Hostile grammar and request mutations.
bad_node = replace(primary_spec.nodes[-1], opcode="EVAL_PYTHON")
bad_spec = replace(primary_spec, nodes=primary_spec.nodes[:-1] + (bad_node,))
refusal = evaluate_bounded_observable(released_cce4_request("primary", 192), bad_spec)
check("unknown opcode refuses", isinstance(refusal, Refusal) and refusal.code == "UnsupportedOpcode")
mutated_parameter = replace(primary_spec.nodes[13], exact_parameter="-3/1")
bad_spec = replace(primary_spec, nodes=primary_spec.nodes[:13] + (mutated_parameter,) + primary_spec.nodes[14:])
refusal = evaluate_bounded_observable(released_cce4_request("primary", 192), bad_spec)
check("spec mutation refuses", isinstance(refusal, Refusal) and refusal.code == "KernelSpecMismatch")
for request, code in (
    (released_cce4_request("unknown", 192), "KernelSpecMismatch"),
    (released_cce4_request("primary", 0), "RequestedWidthNotProved"),
    (replace(released_cce4_request("dual_cpv", 192), evaluation_mode="numerical_lateral_cancellation"), "EvaluationCertificateMismatch"),
    (replace(released_cce4_request("primary", 192), requested_class_scope="absolute_representative"), "EvaluationCertificateMismatch"),
    (replace(released_cce4_request("primary", 192), requested_class_scope="quotient_only"), "EvaluationCertificateMismatch"),
):
    outcome = evaluate_bounded_observable(request)
    check(f"stable refusal {code}/{request.request_id}", isinstance(outcome, Refusal) and outcome.code == code)

# Certificate mutation, decimal-only evidence, and nested class mismatch.
cert = results[("primary", 192)].certificate
check("tail mutation rejected", isinstance(verify_cce4_certificate(replace(cert, analytic_account=(("account_closed", "false"),))), Refusal))
check("false width rejected", isinstance(verify_cce4_certificate(replace(cert, achieved_width_bits=10_000)), Refusal))
check("normalization mutation rejected", isinstance(verify_cce4_certificate(replace(cert, target_normalization=(("post-normalization", "none"),))), Refusal))
check("decimal-only evidence rejected", isinstance(verify_cce4_certificate(replace(cert, exact_dyadic_bracket={"decimal": "0.0"})), Refusal))
other_class = results[("dual_cpv", 192)].certificate.nested_cce3_certificate
check("wrong class rejected", isinstance(verify_cce4_certificate(replace(cert, nested_cce3_certificate=other_class)), Refusal))

# Authenticated checkpoint/resume and splice rejection.
result = results[("dual_cpv", 256)]
checkpoint = make_cce4_checkpoint(result)
check("checkpoint verifies", verify_cce4_checkpoint(checkpoint, result))
resumed = resume_cce4(checkpoint, result.request)
check("resume certifies", isinstance(resumed, CertifiedBoundedEvaluation) and resumed.certificate.previous_checkpoint_digest == checkpoint.checkpoint_digest)
second = make_cce4_checkpoint(resumed, previous_checkpoint=checkpoint)
check("checkpoint chain verifies", verify_cce4_checkpoint_chain((checkpoint, second)))
check("checkpoint splice rejects", not verify_cce4_checkpoint(second, resumed) and not verify_cce4_checkpoint_chain((second, checkpoint)))
check("checkpoint mutation rejects", not verify_cce4_checkpoint(replace(checkpoint, checkpoint_digest="0" * 64), result))
wrong_resume = resume_cce4(checkpoint, released_cce4_request("dual_cpv", 384))
check("wrong-request resume refuses", isinstance(wrong_resume, Refusal))

source = "\n".join(path.read_text() for path in (Path(__file__).resolve().parents[1] / "src").rglob("*.py"))
check("campaign-local scout is separate from production", "pathfinder_m1_scout.py" not in source)
check("CCE-4 has no external referee", all(token not in Path(__file__).resolve().parents[1].joinpath("src/cella/continuation/cce4.py").read_text() for token in ("import sympy", "import sage", "subprocess")))

print(f"CCE-4 finite grammar and bounded evaluation: {passed} assertions passed")
