"""Independent deterministic replay for CCE-1 certificate envelopes."""

from __future__ import annotations

import json

from cella.native_periods import verify_dbp_certificate
from cella.native_periods.records import decode_bracket_record

from .canonical import canonical_digest, canonical_json_bytes
from .certificate import (
    CCE_CERTIFICATE_SCHEMA_VERSION,
    EVALUATION_SCHEMA_ID,
    PF0_CONFIRMATION_REPORT_DIGEST,
    ROUTE_SCHEMA_ID,
)
from .model import EvaluationCertificate, UnsupportedRequest, VerificationReport
from .pathfinder import FAMILY_MANIFEST_DIGEST, construct_plan


def verify_continuation_certificate(
    certificate: EvaluationCertificate,
) -> VerificationReport:
    checked: list[str] = []
    if (
        certificate.schema_id != EVALUATION_SCHEMA_ID
        or certificate.schema_version != CCE_CERTIFICATE_SCHEMA_VERSION
        or certificate.route_certificate.schema_id != ROUTE_SCHEMA_ID
        or certificate.route_certificate.schema_version != CCE_CERTIFICATE_SCHEMA_VERSION
    ):
        return VerificationReport(False, "unsupported_certificate_schema", tuple(checked))
    checked.append("schema")

    route = certificate.route_certificate
    reconstructed = construct_plan(route.request)
    if isinstance(reconstructed, UnsupportedRequest):
        return VerificationReport(False, reconstructed.refusal.code, tuple(checked))
    if canonical_json_bytes(reconstructed) != canonical_json_bytes(route.pathfinder_plan):
        return VerificationReport(False, "certificate_digest_mismatch", tuple(checked + ["pathfinder_plan"]))
    checked.extend(("pathfinder_request_scope", "pathfinder_plan"))

    if route.pf0_confirmation_digest != PF0_CONFIRMATION_REPORT_DIGEST:
        return VerificationReport(False, "certificate_digest_mismatch", tuple(checked + ["pf0_confirmation_digest"]))
    if route.adapter_manifest_digest != FAMILY_MANIFEST_DIGEST:
        return VerificationReport(False, "route_identity_failed", tuple(checked + ["adapter_manifest_digest"]))
    checked.extend(("pf0_confirmation_digest", "adapter_manifest_digest"))

    route_unsigned = {
        "schema_id": route.schema_id,
        "schema_version": route.schema_version,
        "request": route.request,
        "pathfinder_plan": route.pathfinder_plan,
        "pf0_confirmation_digest": route.pf0_confirmation_digest,
        "adapter_manifest_digest": route.adapter_manifest_digest,
        "legacy_certificate_digest": route.legacy_certificate_digest,
    }
    if canonical_digest(route_unsigned) != route.route_digest:
        return VerificationReport(False, "certificate_digest_mismatch", tuple(checked + ["route_digest"]))
    checked.append("route_digest")

    try:
        legacy_record = json.loads(certificate.legacy_certificate_json)
    except (TypeError, json.JSONDecodeError):
        return VerificationReport(False, "certificate_digest_mismatch", tuple(checked + ["legacy_json"]))
    legacy_verdict = verify_dbp_certificate(legacy_record)
    if legacy_verdict is not True:
        code = getattr(legacy_verdict, "token", "certificate_digest_mismatch")
        return VerificationReport(False, code, tuple(checked + ["legacy_certificate_replay"]))
    if legacy_record.get("certificate_digest") != route.legacy_certificate_digest:
        return VerificationReport(False, "certificate_digest_mismatch", tuple(checked + ["legacy_digest_link"]))
    if legacy_record.get("target") != route.request.target:
        return VerificationReport(False, "route_identity_failed", tuple(checked + ["legacy_target_link"]))
    bracket = decode_bracket_record(legacy_record["dyadic_bracket"])
    if (
        bracket.width_bits != certificate.achieved_width_bits
        or bracket.width_bits < route.request.requested_bits
    ):
        return VerificationReport(False, "analytic_account_not_closed", tuple(checked + ["achieved_width"]))
    checked.extend(("legacy_certificate_replay", "legacy_digest_link", "legacy_target_link", "achieved_width"))

    evaluation_unsigned = {
        "schema_id": certificate.schema_id,
        "schema_version": certificate.schema_version,
        "route_certificate": route,
        "legacy_certificate_json": certificate.legacy_certificate_json,
        "achieved_width_bits": certificate.achieved_width_bits,
    }
    if canonical_digest(evaluation_unsigned) != certificate.evaluation_digest:
        return VerificationReport(False, "certificate_digest_mismatch", tuple(checked + ["evaluation_digest"]))
    checked.append("evaluation_digest")
    return VerificationReport(
        True,
        "verified",
        tuple(checked),
        certificate.evaluation_digest,
    )
