"""Immutable compatibility facade for the recertified DBP native evaluator."""

from __future__ import annotations

from cella.native_periods import evaluate_dbp_relative_period

from ..model import ContinuationRequest, PathfinderPlan
from ..pathfinder import ADAPTER_ID, ADAPTER_VERSION, FAMILY_MANIFEST_DIGEST


class DBPNativeV1Adapter:
    adapter_id = ADAPTER_ID
    adapter_version = ADAPTER_VERSION
    family_manifest_digest = FAMILY_MANIFEST_DIGEST

    def execute(self, request: ContinuationRequest, plan: PathfinderPlan) -> object:
        if plan.target != request.target or plan.requested_bits != request.requested_bits:
            raise ValueError("plan/request identity mismatch")
        return evaluate_dbp_relative_period(
            request.target,
            request.requested_bits,
            certificate=True,
        )
