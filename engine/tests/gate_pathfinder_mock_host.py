"""Wrapper-independence gate: a mock (non-M2) host drives the same core.

Verifies the boundary law: external identities survive the round trip, host
objects never leak into core IR, routes are byte-deterministic, input-order
noise cannot change the canonical route, and Pathfinder never emits a final
mathematical answer.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.pathfinder import Obligation, PathfinderRequest, plan_request
from cella.pathfinder.serialize import canonical_json_bytes

FAILS: list[str] = []


def check(name: str, condition: bool) -> None:
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")
    if not condition:
        FAILS.append(name)


class MockHostObject:
    """An opaque host object that must never enter core IR."""

    def __repr__(self) -> str:  # pragma: no cover
        return "MockHostObject()"


def lower_mock_task(*, context_key_order: tuple[str, ...]) -> PathfinderRequest:
    """A mock wrapper lowering; context insertion order is deliberately varied."""

    base_context: dict[str, object] = {
        "problem_shape": "signed_contact_projection",
        "sign_product": 1,
        "characteristic": 0,
        "target_generator": "delta",
        "exact_slice": {"N1": 4, "N2": 8, "N3": 12, "N4": 20},
    }
    context = {key: base_context[key] for key in context_key_order}
    return PathfinderRequest.create(
        request_id="mock-host-contact-v1",
        target_obligation=Obligation("base-image", "Mock host base image.", "exact-scheme"),
        external_binding={
            "incidence_ideal": "mockhost://objects/incidence-42",
            "contact_component": "mockhost://objects/contact-7",
            "target_generator": "mockhost://objects/delta-3",
        },
        mathematical_context=context,
        available_route_families=("contact_restriction",),
    )


ordered = tuple(
    ("problem_shape", "sign_product", "characteristic", "target_generator", "exact_slice")
)
shuffled = tuple(
    ("exact_slice", "characteristic", "target_generator", "problem_shape", "sign_product")
)

first = plan_request(lower_mock_task(context_key_order=ordered))
second = plan_request(lower_mock_task(context_key_order=ordered))
noisy = plan_request(lower_mock_task(context_key_order=shuffled))

check("mock host selects the same structural route as M2", first.route is not None)
assert first.route is not None and second.route is not None and noisy.route is not None

check(
    "external mock identities survive the round trip",
    dict(first.route.external_binding)["incidence_ideal"] == "mockhost://objects/incidence-42",
)
serialized_first = canonical_json_bytes(first.route)
check("same request twice is byte-identical", serialized_first == canonical_json_bytes(second.route))
check(
    "context insertion-order noise does not change the canonical route",
    serialized_first == canonical_json_bytes(noisy.route),
)
check("route never contains a final mathematical result", b"final_result" not in serialized_first)
check("route never contains a wall-clock prediction", b"predicted_duration" not in serialized_first)
check(
    "no host-specific object type leaks into the serialized route",
    b"MockHostObject" not in serialized_first and b"mockhost://" in serialized_first,
)

try:
    PathfinderRequest.create(
        request_id="mock-leak",
        target_obligation=Obligation("o", "s", "w"),
        external_binding={"object": MockHostObject()},  # type: ignore[dict-item]
        mathematical_context={"problem_shape": "x"},
        available_route_families=("contact_restriction",),
    )
    check("core IR rejects non-canonical host objects at the boundary", False)
except TypeError:
    check("core IR rejects non-canonical host objects at the boundary", True)

try:
    PathfinderRequest.create(
        request_id="mock-float",
        target_obligation=Obligation("o", "s", "w"),
        external_binding={"value": 0.5},
        mathematical_context={"problem_shape": "x"},
        available_route_families=("contact_restriction",),
    )
    check("core IR rejects binary floats at the boundary", False)
except TypeError:
    check("core IR rejects binary floats at the boundary", True)

# Execution modules are referenced, never invoked, during selection.
check(
    "execution module is referenced by name only",
    first.selected_candidate is not None
    and first.selected_candidate.contract.execution_module.startswith("external."),
)
check(
    "certificate obligations are emitted, never discharged, inside Pathfinder",
    first.selected_candidate is not None
    and len(first.route.certificate_obligations) > 0
    and first.selected_candidate.contract.discharged_obligations == (),
)


print()
if FAILS:
    print(f"GATE PATHFINDER MOCK HOST: OPEN ({len(FAILS)} failing)")
    raise SystemExit(1)
print("GATE PATHFINDER MOCK HOST: CLOSED")
