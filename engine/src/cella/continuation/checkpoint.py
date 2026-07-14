"""Content-addressed checkpoint construction and chain verification."""

from __future__ import annotations

from .canonical import canonical_digest
from .model import (
    ContinuationCheckpoint,
    ContinuationRequest,
    PathfinderPlan,
    VerificationReport,
)


def make_checkpoint(
    request: ContinuationRequest,
    plan: PathfinderPlan,
    certified_prefix_digest: str,
    *,
    next_segment_index: int = 0,
    previous_checkpoint_digest: str | None = None,
) -> ContinuationCheckpoint:
    if next_segment_index < 0:
        raise ValueError("next segment index must be non-negative")
    unsigned = {
        "schema_id": "cella.continuation.checkpoint.v1",
        "adapter_id": request.adapter_id,
        "family_manifest_digest": request.family_manifest_digest,
        "exact_path_digest": request.exact_path_digest,
        "selected_state_digest": request.selected_state_digest,
        "coefficient_ring": request.coefficient_ring,
        "pathfinder_plan_digest": plan.plan_digest,
        "certified_prefix_digest": certified_prefix_digest,
        "next_segment_index": next_segment_index,
        "previous_checkpoint_digest": previous_checkpoint_digest,
    }
    return ContinuationCheckpoint(
        **unsigned,
        checkpoint_digest=canonical_digest(unsigned),
    )


def verify_checkpoint(
    checkpoint: ContinuationCheckpoint,
    request: ContinuationRequest,
    plan: PathfinderPlan,
) -> VerificationReport:
    unsigned = {
        "schema_id": checkpoint.schema_id,
        "adapter_id": checkpoint.adapter_id,
        "family_manifest_digest": checkpoint.family_manifest_digest,
        "exact_path_digest": checkpoint.exact_path_digest,
        "selected_state_digest": checkpoint.selected_state_digest,
        "coefficient_ring": checkpoint.coefficient_ring,
        "pathfinder_plan_digest": checkpoint.pathfinder_plan_digest,
        "certified_prefix_digest": checkpoint.certified_prefix_digest,
        "next_segment_index": checkpoint.next_segment_index,
        "previous_checkpoint_digest": checkpoint.previous_checkpoint_digest,
    }
    if canonical_digest(unsigned) != checkpoint.checkpoint_digest:
        return VerificationReport(False, "checkpoint_chain_invalid", ("checkpoint_digest",))
    matches = (
        checkpoint.adapter_id == request.adapter_id
        and checkpoint.family_manifest_digest == request.family_manifest_digest
        and checkpoint.exact_path_digest == request.exact_path_digest
        and checkpoint.selected_state_digest == request.selected_state_digest
        and checkpoint.coefficient_ring == request.coefficient_ring
        and checkpoint.pathfinder_plan_digest == plan.plan_digest
    )
    if not matches:
        return VerificationReport(False, "checkpoint_chain_invalid", ("source_path_state_ring_plan_identity",))
    return VerificationReport(
        True,
        "verified",
        ("checkpoint_digest", "source_path_state_ring_plan_identity"),
        checkpoint.checkpoint_digest,
    )
