"""Single-pass public API for the PF-0-authorized CCE-1 scope."""

from __future__ import annotations

from cella.native_periods import PeriodRefusal

from .adapters.dbp_native_v1 import DBPNativeV1Adapter
from .certificate import assemble_certificates
from .checkpoint import verify_checkpoint
from .model import (
    CertifiedCorridorResult,
    CertifiedResult,
    CorridorContinuationRequest,
    CorridorRouteCertificate,
    ContinuationCheckpoint,
    ContinuationRequest,
    InsufficientProofBudget,
    Refusal,
    UnsupportedRequest,
)
from .pathfinder import construct_corridor_plan, construct_plan, plan_fits_budget, released_corridor_request, released_request
from .canonical import canonical_digest
from .corridors import CORRIDORS, exact_certificate_digest, verify_manifest
from .verifier import verify_continuation_certificate


def continue_certified(
    request: ContinuationRequest,
) -> CertifiedResult | InsufficientProofBudget | UnsupportedRequest:
    plan = construct_plan(request)
    if isinstance(plan, UnsupportedRequest):
        return plan
    if not plan_fits_budget(request, plan):
        return InsufficientProofBudget(
            request,
            plan,
            Refusal(
                "proof_budget_exhausted",
                "schedule_adequacy",
                "cella.continuation.api.continue_certified",
                True,
                False,
                "the valid canonical plan exceeds the declared proof budget",
            ),
        )

    legacy = DBPNativeV1Adapter().execute(request, plan)
    if isinstance(legacy, PeriodRefusal):
        if legacy.token in {"precision_budget_exhausted", "remainder_bound_failed"}:
            return InsufficientProofBudget(
                request,
                plan,
                Refusal(
                    "proof_budget_exhausted",
                    legacy.first_unclosed_obligation,
                    f"native_periods:{legacy.stage}",
                    True,
                    False,
                    legacy.detail,
                ),
            )
        return UnsupportedRequest(
            request,
            Refusal(
                legacy.token,
                legacy.first_unclosed_obligation,
                f"native_periods:{legacy.stage}",
                False,
                True,
                legacy.detail,
            ),
        )
    route, evaluation = assemble_certificates(request, plan, legacy)
    return CertifiedResult(request, plan, route, evaluation)


def resume_continuation(
    checkpoint: ContinuationCheckpoint,
    request: ContinuationRequest,
) -> CertifiedResult | InsufficientProofBudget | UnsupportedRequest:
    plan = construct_plan(request)
    if isinstance(plan, UnsupportedRequest):
        return plan
    replay = verify_checkpoint(checkpoint, request, plan)
    if not replay.valid:
        return UnsupportedRequest(
            request,
            Refusal(
                "checkpoint_chain_invalid",
                replay.code,
                "cella.continuation.api.resume_continuation",
                False,
                False,
                "checkpoint source, path, state, ring, plan or digest does not replay",
            ),
        )
    return continue_certified(request)


def evaluate_observable(target: str, requested_bits: int):
    return continue_certified(released_request(target, requested_bits))


def continue_corridor_certified(
    request: CorridorContinuationRequest,
) -> CertifiedCorridorResult | Refusal:
    plan = construct_corridor_plan(request)
    if isinstance(plan, Refusal):
        return plan
    manifest = next(item for item in CORRIDORS.values() if item.route_id == request.route_id)
    unsigned = {
        "schema_id": "cella.continuation.dbp_exact_corridor_route_certificate",
        "schema_version": "1.0",
        "request": request,
        "pathfinder_plan": plan,
        "clearance_certificate_digest": exact_certificate_digest(manifest),
        "initial_sheet": manifest.initial_sheet,
        "terminal_sheet": manifest.terminal_sheet,
        "deck_parity": -1,
        "selected_target_quotient_class": manifest.selected_target_quotient_class,
        "unresolved_compact_correction": manifest.unresolved_compact_correction,
    }
    certificate = CorridorRouteCertificate(**unsigned, certificate_digest=canonical_digest(unsigned))
    return CertifiedCorridorResult(request, plan, certificate)


def verify_corridor_certificate(certificate: CorridorRouteCertificate):
    request = certificate.request
    rebuilt_plan = construct_corridor_plan(request)
    if isinstance(rebuilt_plan, Refusal) or rebuilt_plan != certificate.pathfinder_plan:
        return Refusal("stale_pathfinder_source_reference", "pathfinder_plan_replay", "cella.continuation.api.verify_corridor_certificate", False, False, "Pathfinder source or canonical plan does not replay")
    manifest = next((item for item in CORRIDORS.values() if item.route_id == request.route_id), None)
    if manifest is None:
        return Refusal("unsupported_path", "route_identity", "cella.continuation.api.verify_corridor_certificate", False, True, "unknown route")
    try:
        verify_manifest(manifest)
    except ValueError as exc:
        return Refusal(str(exc), "exact_corridor_manifest", "cella.continuation.corridors.verify_manifest", False, True, "manifest replay failed")
    unsigned = {
        "schema_id": certificate.schema_id,
        "schema_version": certificate.schema_version,
        "request": request,
        "pathfinder_plan": certificate.pathfinder_plan,
        "clearance_certificate_digest": certificate.clearance_certificate_digest,
        "initial_sheet": certificate.initial_sheet,
        "terminal_sheet": certificate.terminal_sheet,
        "deck_parity": certificate.deck_parity,
        "selected_target_quotient_class": certificate.selected_target_quotient_class,
        "unresolved_compact_correction": certificate.unresolved_compact_correction,
    }
    expected = (
        certificate.clearance_certificate_digest == exact_certificate_digest(manifest)
        and certificate.initial_sheet == manifest.initial_sheet
        and certificate.terminal_sheet == manifest.terminal_sheet
        and certificate.deck_parity == -1
        and certificate.selected_target_quotient_class == manifest.selected_target_quotient_class
        and certificate.unresolved_compact_correction == manifest.unresolved_compact_correction
        and certificate.certificate_digest == canonical_digest(unsigned)
    )
    if not expected:
        return Refusal("terminal_sheet_mismatch", "corridor_certificate_replay", "cella.continuation.api.verify_corridor_certificate", False, False, "clearance, lift, lateral class or certificate digest changed")
    return True


def compose_routes(left, right):
    return Refusal(
        "unsupported_path",
        "route_composition_not_in_cce1",
        "cella.continuation.api.compose_routes",
        False,
        True,
        "CCE-1 wraps terminal fixed routes; exact continuation composition begins at CCE-2",
    )


def reverse_route(route):
    return Refusal(
        "unsupported_path",
        "route_reversal_not_in_cce1",
        "cella.continuation.api.reverse_route",
        False,
        True,
        "CCE-1 does not claim an inverse for a terminal evaluator route",
    )


def explain_outcome(outcome: object) -> str:
    if isinstance(outcome, CertifiedResult):
        return f"certified:{outcome.evaluation_certificate.evaluation_digest}"
    if isinstance(outcome, InsufficientProofBudget):
        return f"insufficient_proof_budget:{outcome.refusal.failed_obligation}"
    if isinstance(outcome, UnsupportedRequest):
        return f"unsupported:{outcome.refusal.code}:{outcome.refusal.failed_obligation}"
    return "unknown_outcome"


__all__ = [
    "compose_routes",
    "continue_certified",
    "continue_corridor_certified",
    "evaluate_observable",
    "explain_outcome",
    "resume_continuation",
    "reverse_route",
    "verify_continuation_certificate",
    "verify_corridor_certificate",
]
