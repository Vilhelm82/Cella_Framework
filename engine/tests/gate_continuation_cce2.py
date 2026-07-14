"""CCE-2 exact DBP corridor, Pathfinder and certificate gate."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.continuation import (
    CertifiedCorridorResult, continue_corridor_certified,
    released_corridor_request, verify_corridor_certificate,
)
from cella.continuation.canonical import canonical_json_bytes
from cella.continuation.corridors import CORRIDORS, HOSTILE_REFUSAL_CODES, exact_certificate_digest, verify_manifest
from cella.continuation.model import Refusal
from cella.continuation.pathfinder import (
    CORRIDOR_DIVISOR_MANIFEST_DIGEST, CORRIDOR_THEOREM_DIGEST,
    PF0_CONFIRMATION_DIGEST, construct_corridor_plan,
)

passed = 0


def check(label: str, condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


results = {}
for name in ("upper", "lower"):
    request = released_corridor_request(name)
    first = continue_corridor_certified(request)
    second = continue_corridor_certified(request)
    check(f"{name} returns certified corridor", isinstance(first, CertifiedCorridorResult))
    check(f"{name} deterministic bytes", canonical_json_bytes(first) == canonical_json_bytes(second))
    check(f"{name} plan is live-source-bound", len(first.plan.pathfinder_source_digest) == 64)
    check(f"{name} provider is source-bound", len(first.plan.provider_source_digest) == 64)
    check(f"{name} PF0 report is bound", first.plan.pf0_confirmation_digest == PF0_CONFIRMATION_DIGEST)
    check(f"{name} exact manifest replays", bool(verify_manifest(CORRIDORS[name])))
    check(f"{name} clearance digest bound", first.route_certificate.clearance_certificate_digest == exact_certificate_digest(CORRIDORS[name]))
    check(f"{name} terminal deck flip", first.route_certificate.deck_parity == -1 and first.route_certificate.terminal_sheet == "rho=-sqrt(2)")
    check(f"{name} certificate verifies", verify_corridor_certificate(first.route_certificate) is True)
    results[name] = first

check("upper class selected", "delta_-^up" in results["upper"].route_certificate.selected_target_quotient_class)
check("lower class selected", "delta_-^down" in results["lower"].route_certificate.selected_target_quotient_class)
check("compact ambiguity retained", all("Z[A]+Z[B]" in result.route_certificate.unresolved_compact_correction for result in results.values()))

request = released_corridor_request("upper")
wrong_theorem = construct_corridor_plan(replace(request, theorem_digest="0" * 64))
check("theorem digest mismatch refuses", isinstance(wrong_theorem, Refusal) and wrong_theorem.code == "route_theorem_digest_mismatch")
wrong_divisor = construct_corridor_plan(replace(request, divisor_manifest_digest="0" * 64))
check("divisor digest mismatch refuses", isinstance(wrong_divisor, Refusal) and wrong_divisor.code == "divisor_manifest_digest_mismatch")
surface = construct_corridor_plan(replace(request, surface_scope="curve_and_surface"))
check("surface scope refuses", isinstance(surface, Refusal) and surface.code == "surface_scope_requested_without_surface_clearance")
tampered_terminal = replace(results["upper"].route_certificate, terminal_sheet="rho=+sqrt(2)")
check("terminal sheet tampering refuses", isinstance(verify_corridor_certificate(tampered_terminal), Refusal))
tampered_plan = replace(results["upper"].plan, pathfinder_source_digest="0" * 64)
tampered_certificate = replace(results["upper"].route_certificate, pathfinder_plan=tampered_plan)
check("mismatched Pathfinder source refuses", isinstance(verify_corridor_certificate(tampered_certificate), Refusal))
check("production theorem digest locked", request.theorem_digest == CORRIDOR_THEOREM_DIGEST)
check("production divisor digest locked", request.divisor_manifest_digest == CORRIDOR_DIVISOR_MANIFEST_DIGEST)

root = Path(__file__).resolve().parents[1]
production = "\n".join(path.read_text() for path in (root / "src").rglob("*.py"))
check("campaign-local scout is separate from production", "pathfinder_m1_scout.py" not in production)
check("exact corridor core uses no external CAS", all(token not in (root / "src/cella/continuation/corridors.py").read_text() for token in ("sympy", "sage", "subprocess")))
check("hostile refusal vocabulary is closed and stable", len(HOSTILE_REFUSAL_CODES) == len(set(HOSTILE_REFUSAL_CODES)) == 20)

print(f"CCE-2 exact corridor integration: {passed} assertions passed")
