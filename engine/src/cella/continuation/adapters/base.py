"""Protocol implemented by continuation family adapters."""

from __future__ import annotations

from typing import Protocol

from ..model import ContinuationRequest, PathfinderPlan


class ContinuationAdapter(Protocol):
    adapter_id: str
    adapter_version: str
    family_manifest_digest: str

    def execute(self, request: ContinuationRequest, plan: PathfinderPlan) -> object:
        """Execute an already constructed valid plan."""
