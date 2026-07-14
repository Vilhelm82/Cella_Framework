"""Deterministic CCE-1 route and evaluation certificate assembly."""

from __future__ import annotations

from cella.native_periods.certificate import canonical_bytes as legacy_canonical_bytes

from .canonical import canonical_digest
from .model import (
    ContinuationRequest,
    EvaluationCertificate,
    PathfinderPlan,
    RouteCertificate,
)
from .pathfinder import FAMILY_MANIFEST_DIGEST


ROUTE_SCHEMA_ID = "cella.continuation.route_certificate"
EVALUATION_SCHEMA_ID = "cella.continuation.evaluation_certificate"
CCE_CERTIFICATE_SCHEMA_VERSION = "2.0-cce1"
PF0_CONFIRMATION_REPORT_DIGEST = "304fccce5ed1206f23969952634d10b250d8d4d7a7a955971afa8018c2372008"


def assemble_certificates(
    request: ContinuationRequest,
    plan: PathfinderPlan,
    legacy_result: object,
) -> tuple[RouteCertificate, EvaluationCertificate]:
    legacy_record = getattr(legacy_result, "certificate_record")
    legacy_digest = getattr(legacy_result, "certificate_digest")
    bracket = getattr(legacy_result, "dyadic_bracket")

    route_unsigned = {
        "schema_id": ROUTE_SCHEMA_ID,
        "schema_version": CCE_CERTIFICATE_SCHEMA_VERSION,
        "request": request,
        "pathfinder_plan": plan,
        "pf0_confirmation_digest": PF0_CONFIRMATION_REPORT_DIGEST,
        "adapter_manifest_digest": FAMILY_MANIFEST_DIGEST,
        "legacy_certificate_digest": legacy_digest,
    }
    route = RouteCertificate(
        **route_unsigned,
        route_digest=canonical_digest(route_unsigned),
    )
    legacy_json = legacy_canonical_bytes(legacy_record).decode("utf-8")
    evaluation_unsigned = {
        "schema_id": EVALUATION_SCHEMA_ID,
        "schema_version": CCE_CERTIFICATE_SCHEMA_VERSION,
        "route_certificate": route,
        "legacy_certificate_json": legacy_json,
        "achieved_width_bits": bracket.width_bits,
    }
    evaluation = EvaluationCertificate(
        **evaluation_unsigned,
        evaluation_digest=canonical_digest(evaluation_unsigned),
    )
    return route, evaluation
