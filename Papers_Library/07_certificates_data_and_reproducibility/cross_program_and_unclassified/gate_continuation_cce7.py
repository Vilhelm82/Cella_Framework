"""CCE-7 exact static strict-chamber labelled-root continuation gate."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.continuation.canonical import canonical_json_bytes
from cella.continuation.cce7 import (
    CCE7ChamberRequest, CCE7Request, CertifiedChamberCoverResult,
    CertifiedCoverResult, StaticChamberPoint, StaticWallEvent,
    classify_static_wall, continue_static_chamber_certified,
    continue_static_cover_certified, make_cce7_checkpoint, norm_quintic,
    released_cce7_request, resume_cce7, verify_cce7_certificate,
    verify_cce7_chamber_certificate, verify_cce7_checkpoint,
)
from cella.continuation.model import Refusal
from cella.pathfinder.scout.sturm import sturm_root_count


passed = 0


def check(label: str, condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


request = released_cce7_request()
first = continue_static_cover_certified(request)
second = continue_static_cover_certified(request)
check("route certifies", isinstance(first, CertifiedCoverResult))
check("clean deterministic replay", canonical_json_bytes(first) == canonical_json_bytes(second))
if not isinstance(first, CertifiedCoverResult):
    raise SystemExit(1)
certificate = first.certificate
check("certificate verifies", verify_cce7_certificate(certificate) is True)
check("nine exact rational nodes", len(certificate.nodes) == 9 and certificate.nodes[0].m4 == 12 and certificate.nodes[-1].m4 == 13)
check("strict chamber margin positive", all(node.strict_chamber_margin >= 2 for node in certificate.nodes))
check("five labelled roots per node", all(len(node.isolators) == 5 for node in certificate.nodes))
check("five exact positive roots per node", all(sturm_root_count(node.polynomial, Fraction(0), None) == 5 for node in certificate.nodes))
check("40 adjacent overlap witnesses", len(certificate.overlap_ledger) == 8 * 5)
check("identity terminal permutation", certificate.terminal_permutation == tuple(range(5)))
check("physical unique-least label", certificate.root_labels[0] == "physical" and dict(certificate.physical_selection_ledger)["nearest_float_used"] == "false")
check("no discriminant crossing", dict(certificate.inertia_ledger)["discriminant_crossings"] == "0")
check("Kummer signs unchanged", dict(certificate.kummer_sign_ledger)["deck_parity"] == "unchanged")

known = norm_quintic(Fraction(12))
check("M4=12 exact quintic pin", known == tuple(Fraction(x) for x in (-268240896000, 153410745600, -18763949785, 948667896, -21722256, 186624)))

for mutated, code in (
    (replace(request, m4_nodes=(Fraction(10),)), "AlgebraicCoverUnsupported"),
    (replace(request, m4_nodes=(Fraction(12), Fraction(10))), "UnprovedWallCrossing"),
    (replace(request, requested_scope="rotating_off_chamber"), "PhysicalSelectionUnproved"),
    (replace(request, physical_selection="nearest_float"), "PhysicalSelectionUnproved"),
    (replace(request, charges=(1, 1, 3, 4)), "RootIsolationAmbiguous"),
):
    outcome = continue_static_cover_certified(mutated)
    check(f"hostile request refuses {code}", isinstance(outcome, Refusal) and outcome.code == code)

custom = CCE7Request(
    "cce7-custom-forward",
    "custom-rational-route",
    (4, -1, 3, -2),
    (Fraction(11), Fraction(23, 2), Fraction(14)),
)
custom_result = continue_static_cover_certified(custom)
check("arbitrary exact fixed-charge route certifies", isinstance(custom_result, CertifiedCoverResult))
if isinstance(custom_result, CertifiedCoverResult):
    check("custom route preserves requested endpoints", custom_result.certificate.nodes[0].m4 == 11 and custom_result.certificate.nodes[-1].m4 == 14)
    check("shadow labels follow squared-charge order", custom_result.certificate.root_labels == ("physical", "shadow_N2", "shadow_N4", "shadow_N3", "shadow_N1"))
    check("charge signs are recorded", dict(custom_result.certificate.kummer_sign_ledger)["charge_signs"] == "+,-,+,-")
    check("custom certificate verifies", verify_cce7_certificate(custom_result.certificate) is True)

reverse = replace(custom, request_id="cce7-custom-reverse", route_id="custom-rational-route-reverse", m4_nodes=tuple(reversed(custom.m4_nodes)))
reverse_result = continue_static_cover_certified(reverse)
check("reverse exact route certifies", isinstance(reverse_result, CertifiedCoverResult))

chamber_request = CCE7ChamberRequest(
    "full-static-polygon",
    "rational-polygon-with-charge-zero-crossing",
    (
        StaticChamberPoint(Fraction(12), (Fraction(1), Fraction(2), Fraction(3), Fraction(4))),
        StaticChamberPoint(Fraction(13), (Fraction(-1), Fraction(2), Fraction(3), Fraction(4))),
        StaticChamberPoint(Fraction(15), (Fraction(-2), Fraction(3), Fraction(4), Fraction(5))),
    ),
)
chamber_result = continue_static_chamber_certified(chamber_request)
check("full multivariable static route certifies", isinstance(chamber_result, CertifiedChamberCoverResult))
if isinstance(chamber_result, CertifiedChamberCoverResult):
    check("full chamber certificate verifies", verify_cce7_chamber_certificate(chamber_result.certificate) is True)
    check("full chamber exact nodes", len(chamber_result.certificate.nodes) == 3)
    check("charge zero crossing retained", chamber_result.certificate.charge_zero_crossings == ((0, 0, Fraction(1, 2)),))
    check("full chamber identity permutation", chamber_result.certificate.terminal_permutation == tuple(range(5)))
    check("full chamber five exact roots", all(sturm_root_count(node.polynomial, Fraction(0), None) == 5 for node in chamber_result.certificate.nodes))

wall_request = replace(chamber_request, request_id="full-static-wall", points=(chamber_request.points[0], StaticChamberPoint(Fraction(10), (Fraction(1), Fraction(2), Fraction(3), Fraction(4)))))
wall_result = continue_static_chamber_certified(wall_request)
check("full chamber boundary crossing refuses", isinstance(wall_result, Refusal) and wall_result.code == "UnprovedWallCrossing")

h2_request = replace(chamber_request, request_id="full-static-h2-wall", points=(
    chamber_request.points[0],
    StaticChamberPoint(Fraction(13), (Fraction(2), Fraction(1), Fraction(3), Fraction(4))),
))
h2_result = continue_static_chamber_certified(h2_request)
check("full chamber H2 crossing refuses", isinstance(h2_result, Refusal) and h2_result.code == "RootIsolationAmbiguous")

simple_wall = classify_static_wall(StaticChamberPoint(Fraction(10), (Fraction(1), Fraction(2), Fraction(3), Fraction(4))))
check("nonzero-charge wall classifies", isinstance(simple_wall, StaticWallEvent))
if isinstance(simple_wall, StaticWallEvent):
    check("physical boundary contact is simple", simple_wall.event_kind == "physical_simple_contact" and simple_wall.zero_root_multiplicity == 1)
    check("four positive shadow roots remain", simple_wall.positive_root_count == 4)

zero_wall = classify_static_wall(StaticChamberPoint(Fraction(6), (Fraction(0), Fraction(1), Fraction(2), Fraction(3))))
check("zero-charge wall classifies", isinstance(zero_wall, StaticWallEvent))
if isinstance(zero_wall, StaticWallEvent):
    check("zero charge creates typed signed-sheet coincidence", zero_wall.event_kind == "physical_zero_charge_sheet_coincidence" and zero_wall.colliding_labels == ("physical", "shadow_N1"))
    check("H2 norm root remains simple", zero_wall.zero_root_multiplicity == 1 and zero_wall.positive_root_count == 4)

check("permutation tamper rejects", isinstance(verify_cce7_certificate(replace(certificate, terminal_permutation=(1, 0, 2, 3, 4))), Refusal))
check("isolator tamper rejects", isinstance(verify_cce7_certificate(replace(certificate, nodes=certificate.nodes[:-1])), Refusal))
check("selection tamper rejects", isinstance(verify_cce7_certificate(replace(certificate, physical_selection_ledger=(("rule", "nearest"),))), Refusal))

checkpoint = make_cce7_checkpoint(first)
check("checkpoint verifies", verify_cce7_checkpoint(checkpoint, first))
resumed = resume_cce7(checkpoint, request)
check("resume certifies", isinstance(resumed, CertifiedCoverResult) and resumed.certificate.previous_checkpoint_digest == checkpoint.checkpoint_digest)
check("checkpoint mutation rejects", not verify_cce7_checkpoint(replace(checkpoint, checkpoint_digest="0" * 64), first))

source = Path(__file__).resolve().parents[1].joinpath("src/cella/continuation/cce7.py").read_text()
check("campaign-local scout is separate from production", "pathfinder_m1_scout.py" not in source)
check("no floating root tracking", all(token not in source for token in ("float(", "numpy", "mpmath", "findroot", "nroots")))
check("no external CAS", all(token not in source for token in ("import sympy", "import sage", "subprocess")))

print(f"CCE-7 exact static labelled-root gate: {passed} assertions passed")
