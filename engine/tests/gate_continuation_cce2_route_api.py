"""Public CCE-2 composition/reversal promotion gate."""

from dataclasses import replace
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.continuation import (
    CCE5GroupoidRequest,
    CertifiedCorridorGroupoidTransport,
    compose_routes,
    continue_corridor_groupoid_certified,
    reverse_route,
    verify_cce5_groupoid_certificate,
)
from cella.continuation.model import Refusal


passed = 0


def check(label, condition):
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


def certified(word: str) -> CertifiedCorridorGroupoidTransport:
    result = continue_corridor_groupoid_certified(CCE5GroupoidRequest(f"fixture-{word}", word))
    if not isinstance(result, CertifiedCorridorGroupoidTransport):
        raise AssertionError(f"fixture {word} did not certify")
    return result


upper = certified("U")
lower_inverse = certified("l")
upper_inverse = certified("u")

loop = compose_routes(upper, lower_inverse)
check("certified composition", isinstance(loop, CertifiedCorridorGroupoidTransport))
if isinstance(loop, CertifiedCorridorGroupoidTransport):
    check("composition word", loop.request.corridor_word == "Ul")
    check("composition replays", verify_cce5_groupoid_certificate(loop.certificate) is True)

reversed_loop = reverse_route(loop)
check("certified reversal", isinstance(reversed_loop, CertifiedCorridorGroupoidTransport))
if isinstance(reversed_loop, CertifiedCorridorGroupoidTransport):
    check("inverse word", reversed_loop.request.corridor_word == "Lu")
    check("inverse replays", verify_cce5_groupoid_certificate(reversed_loop.certificate) is True)
    round_trip = reverse_route(reversed_loop)
    check("double reversal certifies", isinstance(round_trip, CertifiedCorridorGroupoidTransport))
    if isinstance(round_trip, CertifiedCorridorGroupoidTransport) and isinstance(loop, CertifiedCorridorGroupoidTransport):
        check("double reversal canonical", round_trip.certificate == loop.certificate)

left_associated = compose_routes(compose_routes(upper, lower_inverse), upper)
right_associated = compose_routes(upper, compose_routes(lower_inverse, upper))
check("left association certifies", isinstance(left_associated, CertifiedCorridorGroupoidTransport))
check("right association certifies", isinstance(right_associated, CertifiedCorridorGroupoidTransport))
if isinstance(left_associated, CertifiedCorridorGroupoidTransport) and isinstance(right_associated, CertifiedCorridorGroupoidTransport):
    check("composition associative", left_associated.certificate == right_associated.certificate)

noncomposable = compose_routes(upper, certified("L"))
check("noncomposable refuses", isinstance(noncomposable, Refusal) and noncomposable.code == "RouteMismatch")

raw_route = compose_routes("U", lower_inverse)
check("uncertified input refuses", isinstance(raw_route, Refusal) and raw_route.code == "UnsupportedOperation")

tampered = replace(upper, certificate=replace(upper.certificate, canonical_certificate_digest="0" * 64))
tampered_result = compose_routes(tampered, upper_inverse)
check("tampered source refuses", isinstance(tampered_result, Refusal) and tampered_result.code == "CertificateReplayFailed")

print(f"CCE-2 public route composition/reversal gate: {passed} assertions passed")
