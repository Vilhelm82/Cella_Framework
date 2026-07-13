"""Public API for the bounded DBP native relative-period evaluator."""

from __future__ import annotations

from fractions import Fraction

from cella.typed_elementary import pi_eval

from .certificate import HexIntError, canon, digest
from .dbp_theta_route import canonical_source, compile_dbp_theta
from .exact_scalar import Interval
from .quadrature import integrate_certified
from .records import (CertifiedPeriodResult, DUAL_PATH, PRIMARY_PATH,
                      PeriodRefusal, decode_bracket_record)
from .terminal import decimal_render, materialize
from .account import evaluate_fixed_dag_binary64


CERTIFICATE_SCHEMA_ID = "cella.dbp.native_relative_period_evaluator.certificate"
CERTIFICATE_SCHEMA_VERSION = "1.1"

TARGETS = {
    "trace_primary": (PRIMARY_PATH, Fraction(1), False),
    "primary": (PRIMARY_PATH, Fraction(1, 2), True),
    "trace_dual_real_cpv": (DUAL_PATH, Fraction(1), False),
    "dual_cpv": (DUAL_PATH, Fraction(1, 2), False),
}


def evaluate_dbp_relative_period(target, target_bits, certificate=True):
    if target not in TARGETS:
        return PeriodRefusal("unsupported_relative_path", "api", f"unknown target {target!r}", "target is not one of the four admitted routes")
    if isinstance(target_bits, bool) or not isinstance(target_bits, int) or target_bits <= 0:
        return PeriodRefusal("precision_budget_exhausted", "api", "target_bits must be a positive integer", "invalid precision request")
    if not isinstance(certificate, bool):
        return PeriodRefusal("route_identity_failed", "api", "certificate must be boolean", "invalid request contract")
    path, scale, subtract_pi = TARGETS[target]
    compiled = compile_dbp_theta(canonical_source(path))
    if isinstance(compiled, PeriodRefusal):
        return compiled
    try:
        integral = integrate_certified(compiled.kernel_id, target_bits + 8)
    except (ArithmeticError, ZeroDivisionError, ValueError) as exc:
        return PeriodRefusal("remainder_bound_failed", "quadrature", str(exc), "certified quadrature remainder")
    enclosure = integral.enclosure * scale
    pi_record = None
    if subtract_pi:
        p = pi_eval(target_bits + 40)
        pi_record = {"lo": p.lo, "hi": p.hi, "method": "native_machin_arctan_rational_enclosure"}
        enclosure = enclosure + Interval(-2*p.hi, -2*p.lo)
    bracket = materialize(enclosure, target_bits)
    dag_account = evaluate_fixed_dag_binary64(compiled.kernel_id, 0.5)
    account = {
        "architecture": "reading_plus_signed_local_defects_plus_named_nonlinear_remainder",
        "closed": True, "limb_count": max(1, (target_bits + 52)//53),
        "local_identities": ["two_sum", "two_prod", "division_numerator_defect", "sqrt_square_defect"],
        "nonlinear_remainder": "fixed_algebraic_recurrence_cauchy_remainder",
        "fixed_dag_node_count": dag_account["node_count"],
        "operation_defect_digest": dag_account["operation_defect_digest"],
    }
    remainder = {
        "rule": integral.rule, "panels": integral.panels, "order": integral.order,
        "working_bits": integral.working_bits, "quadrature_remainder": integral.remainder_bound,
        "pi_enclosure": pi_record,
    }
    record = {
        "schema_id": CERTIFICATE_SCHEMA_ID,
        "schema_version": CERTIFICATE_SCHEMA_VERSION, "target": target, "route_id": compiled.route_id,
        "theorem_version": compiled.theorem_version, "route_version": compiled.route_version,
        "source_ledger": compiled.source_ledger, "compiled_kernel": {
            "id": compiled.kernel_id, "radicand": compiled.radicand,
            "expression": compiled.expression, "domain_witnesses": compiled.domain_witnesses,
        }, "account_ledger": account, "remainder_ledger": remainder,
        "dyadic_bracket": bracket.to_record(), "unused_oracle_pins": ["dbp_primary_50d", "dbp_dual_cpv_54d"],
    }
    certificate_digest = digest(record)
    record = {**canon(record), "certificate_digest": certificate_digest}
    return CertifiedPeriodResult(
        target, bracket, decimal_render(enclosure, max(20, (target_bits*30103)//100000 + 18)),
        compiled.route_id, compiled.source_ledger, account, remainder,
        certificate_digest, record if certificate else None,
    )


def verify_dbp_certificate(record):
    """Verify a canonical DBP certificate without trusting or re-executing it."""
    if not isinstance(record, dict):
        return PeriodRefusal("route_identity_failed", "certificate", "certificate must be a mapping", "canonical certificate record")
    if record.get("schema_id") != CERTIFICATE_SCHEMA_ID or record.get("schema_version") != CERTIFICATE_SCHEMA_VERSION:
        return PeriodRefusal(
            "unsupported_certificate_schema", "certificate",
            f"verifier admits only {CERTIFICATE_SCHEMA_ID} v{CERTIFICATE_SCHEMA_VERSION}",
            "declared certificate schema",
        )
    target = record.get("target")
    if target not in TARGETS:
        return PeriodRefusal("unsupported_relative_path", "certificate", "certificate target is not admitted", "admitted target")
    path = TARGETS[target][0]
    compiled = compile_dbp_theta(canonical_source(path))
    if isinstance(compiled, PeriodRefusal):
        return compiled
    expected_source = canon(compiled.source_ledger)
    if record.get("source_ledger") != expected_source:
        return PeriodRefusal("route_identity_failed", "source_ledger", "source path, sheet, pole, residue, or CPV ledger was altered", "exact source ledger")
    expected_kernel = canon({
        "id": compiled.kernel_id, "radicand": compiled.radicand,
        "expression": compiled.expression, "domain_witnesses": compiled.domain_witnesses,
    })
    if record.get("compiled_kernel") != expected_kernel or record.get("route_id") != compiled.route_id:
        return PeriodRefusal("route_identity_failed", "compiled_kernel", "compiled route identity was altered", "exact compiled kernel")
    account = record.get("account_ledger")
    expected_account = evaluate_fixed_dag_binary64(compiled.kernel_id, 0.5)
    if (not isinstance(account, dict) or account.get("closed") is not True
            or account.get("operation_defect_digest") != expected_account["operation_defect_digest"]):
        return PeriodRefusal("account_not_closed", "account_ledger", "operation account was altered or does not replay", "fixed DAG account closure")
    bracket = record.get("dyadic_bracket")
    if isinstance(bracket, dict) and "lower_numerator" in bracket:
        return PeriodRefusal(
            "unsupported_certificate_schema", "terminal",
            "bracket uses the schema 1.0 bare-integer encoding, which JSON transport may silently round; re-emit the certificate under schema 1.1",
            "hex_rational bracket encoding",
        )
    try:
        decoded = decode_bracket_record(bracket)
    except HexIntError as exc:
        return PeriodRefusal("route_identity_failed", "terminal", f"terminal dyadic bracket is malformed: {exc}", "terminal bracket contract")
    if decoded.lower_numerator > decoded.upper_numerator or decoded.denominator_exponent < 0:
        return PeriodRefusal("route_identity_failed", "terminal", "terminal dyadic bracket is malformed", "terminal bracket contract")
    claimed = record.get("certificate_digest")
    unsigned = dict(record)
    unsigned.pop("certificate_digest", None)
    if not isinstance(claimed, str) or digest(unsigned) != claimed:
        return PeriodRefusal("route_identity_failed", "certificate_digest", "canonical certificate digest mismatch", "byte-stable canonical digest")
    return True
