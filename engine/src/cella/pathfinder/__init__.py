"""Typed Pathfinder route-planning core with legacy API compatibility.

Pathfinder discovers and selects computational routes.  It does not execute the
host mathematical task or construct its final result/certificate.
"""

from .api.contract import RecognitionOutcome, RecognitionRefusal, RouteCandidate, RouteContract
from .api.request import PathfinderRequest
from .api.route import ComputationalRoute, RouteStep
from .compat import pathfinder_compare, rewrite_candidates, route_plan
from .ir.burden import BurdenVector
from .ir.evidence import ScoutEvidence
from .ir.fingerprint import StructuralFingerprint, fingerprint_problem
from .ir.obligation import Obligation
from .ir.problem import NormalizedProblem, lower_request, stable_problem_hash
from .ir.scope import AnalysisBudget, Scope
from .plan import PlanningOutcome, PlanningRefusal, plan_request
from .plan.compare import RouteRejection
from .plan.registry import PROVIDERS, RouteProvider

__all__ = [
    "AnalysisBudget",
    "BurdenVector",
    "ComputationalRoute",
    "NormalizedProblem",
    "Obligation",
    "PROVIDERS",
    "PathfinderRequest",
    "PlanningOutcome",
    "PlanningRefusal",
    "RecognitionOutcome",
    "RecognitionRefusal",
    "RouteCandidate",
    "RouteContract",
    "RouteProvider",
    "RouteRejection",
    "RouteStep",
    "Scope",
    "ScoutEvidence",
    "StructuralFingerprint",
    "fingerprint_problem",
    "lower_request",
    "pathfinder_compare",
    "plan_request",
    "rewrite_candidates",
    "route_plan",
    "stable_problem_hash",
]
