"""PF-0 gate for the finite recertified DBP Pathfinder domain."""

from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.continuation.canonical import canonical_json_bytes
from cella.continuation.model import CoefficientRing, ProofBudget, UnsupportedRequest
from cella.continuation.pathfinder import (
    ADMITTED_REQUESTS,
    construct_plan,
    plan_fits_budget,
    released_request,
)


EXPECTED_DIGESTS = {
    ("primary", 192): "a6d8e2cca14f78f94367f5c42cace779fa4139780d1160f5ac8ad37999f299a9",
    ("dual_cpv", 192): "4cb53a0b4820d152186e3df388ed21d4262b1870e3115b39e862de774470fac8",
    ("primary", 256): "9e4b4fe6b81e94f611ee88c63b0366290d94f1c444d2c118981d7886af20cd84",
    ("dual_cpv", 256): "ada6e19757b07a2e06b06dc5dcb71cf8cd35bfd6cd52e3f82dfb64bfe1c7669a",
    ("primary", 384): "5e7ae86cc389c908ae69bd0df70fc987a8c1ac35b1d8e0f0f325afa4fb30f45a",
    ("dual_cpv", 384): "8b662b4e984102e61c4e971ec456d851f469ca3296b0090a64a2cb5bf0f3da35",
}

passed = 0


def check(label: str, condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


for pair in ADMITTED_REQUESTS:
    request = released_request(*pair)
    first = construct_plan(request)
    second = construct_plan(request)
    check(f"{pair}: constructor returns a valid plan", not isinstance(first, UnsupportedRequest))
    assert not isinstance(first, UnsupportedRequest)
    check(f"{pair}: canonical digest is locked", first.plan_digest == EXPECTED_DIGESTS[pair])
    check(f"{pair}: repeated construction is byte deterministic", canonical_json_bytes(first) == canonical_json_bytes(second))
    check(f"{pair}: live typed Pathfinder provider is recorded", '"route_family":"dbp_native_released_evaluation"' in first.canonical_route_json)
    check(f"{pair}: Pathfinder route contains no final result", "final_result" not in first.canonical_route_json)
    check(f"{pair}: panel schedule is an exact partition", tuple(item[0] for item in first.panel_schedule) == tuple(range(32)))
    check(f"{pair}: default proof budget is adequate", plan_fits_budget(request, first))


base = released_request("primary", 192)
mutations = (
    (replace(base, adapter_id="wrong"), "unsupported_adapter"),
    (replace(base, adapter_version="0"), "unsupported_adapter"),
    (replace(base, target="unknown"), "unsupported_path"),
    (replace(base, requested_bits=191), "unsupported_path"),
    (replace(base, requested_bits=193), "unsupported_path"),
    (replace(base, requested_bits=255), "unsupported_path"),
    (replace(base, requested_bits=257), "unsupported_path"),
    (replace(base, requested_bits=383), "unsupported_path"),
    (replace(base, requested_bits=385), "unsupported_path"),
    (replace(base, family_manifest_digest="0" * 64), "route_identity_failed"),
    (replace(base, exact_path_digest="0" * 64), "route_identity_failed"),
    (replace(base, selected_state_digest="0" * 64), "route_identity_failed"),
    (replace(base, coefficient_ring=CoefficientRing.Z_HALF), "route_identity_failed"),
)
for request, code in mutations:
    outcome = construct_plan(request)
    check(
        f"hostile request refuses as {code}",
        isinstance(outcome, UnsupportedRequest) and outcome.refusal.code == code,
    )


small_budget = replace(
    base,
    proof_budget=ProofBudget(max_steps=31, max_recurrence_order=87, max_work_bits=281),
)
small_plan = construct_plan(small_budget)
check("inadequate budget does not invalidate the plan", not isinstance(small_plan, UnsupportedRequest))
assert not isinstance(small_plan, UnsupportedRequest)
check("adequacy is reported separately", not plan_fits_budget(small_budget, small_plan))

source = (Path(__file__).resolve().parent.parent / "src/cella/continuation/pathfinder.py").read_text()
check("constructor contains no random or external numerical dependency", not any(
    token in source for token in ("random", "mpmath", "sympy", "scipy", "flint", "sage")
))

print(f"CCE PF-0 finite-domain confirmation: {passed} assertions passed")
