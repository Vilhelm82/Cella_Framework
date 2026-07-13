"""Gate the typed Pathfinder core and first structural recognizer."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.pathfinder import Obligation, PathfinderRequest
from cella.pathfinder.recognize import recognize_contact_restriction
from cella.pathfinder.serialize import canonical_json_bytes


FAILS: list[str] = []


def check(name: str, condition: bool) -> None:
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")
    if not condition:
        FAILS.append(name)


def request(**overrides: object) -> PathfinderRequest:
    context = {
        "problem_shape": "signed_contact_projection",
        "sign_product": 1,
        "characteristic": 0,
        "target_generator": "delta",
        "exact_slice": {"N1": 4, "N2": 8, "N3": 12, "N4": 20},
    }
    context.update(overrides)
    return PathfinderRequest.create(
        request_id="m2-even-contact-delta-slice-a-v1",
        target_obligation=Obligation(
            "base-image",
            "Compute the exact sliced base-image ideal.",
            "exact-scheme",
        ),
        external_binding={
            "incidence_ideal": "m2:IX",
            "contact_component": "m2:Ceven",
            "target_generator": "m2:delta",
        },
        mathematical_context=context,
        available_route_families=("contact_restriction", "generic_elimination"),
    )


accepted = recognize_contact_restriction(request())
check("even contact fixture is recognized", accepted.candidate is not None)
assert accepted.candidate is not None
route = accepted.candidate.route
check("recognizer returns instructions rather than a final ideal", route.route_family == "contact_restriction")
check(
    "route bypasses generic saturation and elimination",
    not any("saturat" in step.operation or "eliminat" in step.operation for step in route.ordered_steps),
)
check(
    "route explicitly retains multiplicity two",
    dict(route.ordered_steps[1].parameters).get("retain_power") == 2,
)
check(
    "wrapper-owned external bindings survive unchanged",
    route.external_binding == request().external_binding,
)
serialized = canonical_json_bytes(route)
check("typed route serialization is byte deterministic", serialized == canonical_json_bytes(route))
check("public route has no wall-clock prediction", b"predicted_duration" not in serialized)
check("public route has no final mathematical result field", b"final_result" not in serialized)

for label, changed, code in (
    ("odd contact is refused", {"sign_product": -1}, "unsupported_sign_product"),
    ("characteristic two is refused", {"characteristic": 2}, "characteristic_two"),
    ("wrong generator is refused", {"target_generator": "gamma"}, "target_generator_mismatch"),
    (
        "incomplete slice is refused",
        {"exact_slice": {"N1": 4, "N2": 8, "N3": 12}},
        "incomplete_exact_slice",
    ),
):
    outcome = recognize_contact_restriction(request(**changed))
    check(label, outcome.refusal is not None and outcome.refusal.code == code)


print()
if FAILS:
    print(f"GATE PATHFINDER TYPED CORE: OPEN ({len(FAILS)} failing)")
    raise SystemExit(1)
print("GATE PATHFINDER TYPED CORE: CLOSED")
