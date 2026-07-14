"""CCE-5 exact connection, absolute PL calibration, and corridor-groupoid gate."""

from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.continuation.cce5 import (
    CCE5GroupoidRequest, CCE5Request, CertifiedCorridorGroupoidTransport,
    CertifiedDBPConnection, compact_correction_coordinates,
    compact_picard_lefschetz_matrix, continue_corridor_groupoid_certified,
    continue_dbp_connection_certified, corridor_transport_matrix,
    corridor_word_endpoints, dbp_characteristic, dbp_connection_matrix,
    make_cce5_checkpoint, relative_picard_lefschetz_matrix,
    released_cce5_request, resume_cce5, trace_comparison_coordinates,
    verify_braid_calibration, verify_cce5_certificate,
    verify_cce5_checkpoint, verify_cce5_groupoid_certificate,
    verify_dbp_connection_identity, verify_dbp_family_identity,
)
from cella.continuation.model import Refusal


passed = 0


def check(label, condition):
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


results = {}
for arm in ("upper", "lower"):
    request = released_cce5_request(arm)
    first = continue_dbp_connection_certified(request)
    second = continue_dbp_connection_certified(request)
    check(f"{arm} certifies", isinstance(first, CertifiedDBPConnection))
    check(f"{arm} deterministic", first == second)
    check(f"{arm} verifies", isinstance(first, CertifiedDBPConnection) and verify_cce5_certificate(first.certificate) is True)
    if isinstance(first, CertifiedDBPConnection):
        results[arm] = first
        check(f"{arm} route bound", first.certificate.route_id.endswith(f"{arm}_qi_v1"))
        check(f"{arm} boundary preserved", first.certificate.relative_matrix[-1] == (0, 0, 0, 1))
        checkpoint = make_cce5_checkpoint(first)
        check(f"{arm} checkpoint", verify_cce5_checkpoint(checkpoint, first))
        resumed = resume_cce5(checkpoint, request)
        check(f"{arm} resume", isinstance(resumed, CertifiedDBPConnection) and resumed.certificate.previous_checkpoint_digest == checkpoint.checkpoint_digest)

check("family characteristic", dbp_characteristic(Fraction(1, 4)) == Fraction(-1, 8))
check("family elimination", verify_dbp_family_identity())
check("connection identity", verify_dbp_connection_identity())
check("braid calibration", verify_braid_calibration())
matrix = dbp_connection_matrix(Fraction(1, 4))
check("rank three", len(matrix) == 3 and all(len(row) == 3 for row in matrix))
check("exact entries", all(isinstance(value, Fraction) for row in matrix for value in row))
check("upper compact matrix", compact_picard_lefschetz_matrix("upper") == ((1, 0), (2, 1)))
check("lower compact inverse", compact_picard_lefschetz_matrix("lower") == ((1, 0), (-2, 1)))
check("upper correction", compact_correction_coordinates("upper") == (0, 1))
check("lower correction", compact_correction_coordinates("lower") == (0, -1))
check("compact corrections cancel", tuple(a + b for a, b in zip(compact_correction_coordinates("upper"), compact_correction_coordinates("lower"))) == (0, 0))
check("upper abc", trace_comparison_coordinates("upper") == (1, 0, 0))
check("lower abc", trace_comparison_coordinates("lower") == (1, 0, 1))
check("lateral difference refines quotient", relative_picard_lefschetz_matrix("upper")[1][3] - relative_picard_lefschetz_matrix("lower")[1][3] == 2)

for word, endpoints in (("U", ("plus", "minus")), ("l", ("minus", "plus")), ("Ul", ("plus", "plus")), ("lU", ("minus", "minus")), ("UlUl", ("plus", "plus"))):
    check(f"{word} endpoints", corridor_word_endpoints(word) == endpoints)
    groupoid = continue_corridor_groupoid_certified(CCE5GroupoidRequest(f"groupoid-{word}", word))
    check(f"{word} groupoid certifies", isinstance(groupoid, CertifiedCorridorGroupoidTransport))
    if isinstance(groupoid, CertifiedCorridorGroupoidTransport):
        check(f"{word} groupoid verifies", verify_cce5_groupoid_certificate(groupoid.certificate) is True)

identity4 = tuple(tuple(int(i == j) for j in range(4)) for i in range(4))
check("upper inverse cancels", corridor_transport_matrix("Uu") == identity4 and corridor_transport_matrix("uU") == identity4)
check("lower inverse cancels", corridor_transport_matrix("Ll") == identity4 and corridor_transport_matrix("lL") == identity4)
check("upper-lower loop is nontrivial", corridor_transport_matrix("Ul") != identity4)
check("word composition order", corridor_transport_matrix("UlUl") == tuple(tuple(sum(corridor_transport_matrix("Ul")[i][k] * corridor_transport_matrix("Ul")[k][j] for k in range(4)) for j in range(4)) for i in range(4)))

try:
    CCE5GroupoidRequest("noncomposable", "UL")
except ValueError as exc:
    check("noncomposable corridor word refuses", getattr(exc, "code", None) == "RouteMismatch")
else:
    raise AssertionError("noncomposable corridor word accepted")

for singular in (Fraction(0), Fraction(1, 2), Fraction(1)):
    try:
        dbp_connection_matrix(singular)
    except ValueError as exc:
        check(f"singularity {singular} refuses", getattr(exc, "code", None) == "ConnectionSingularity")
    else:
        raise AssertionError(f"singularity {singular} accepted")

wrong_scope = continue_dbp_connection_certified(replace(released_cce5_request(), requested_scope="whole_parameter_plane"))
check("unreleased scope refuses", isinstance(wrong_scope, Refusal) and wrong_scope.code == "StageDependencyUnavailable")
wrong_route = continue_dbp_connection_certified(CCE5Request("bad-route", "generic"))
check("route mismatch refuses", isinstance(wrong_route, Refusal) and wrong_route.code == "RouteMismatch")
wrong_basis = continue_dbp_connection_certified(replace(released_cce5_request(), basis=("K", "E", "Kprime")))
check("basis mismatch refuses", isinstance(wrong_basis, Refusal) and wrong_basis.code == "BasisMismatch")

cert = results["upper"].certificate
check("matrix tamper rejects", isinstance(verify_cce5_certificate(replace(cert, compact_matrix=((1, 0), (0, 1)))), Refusal))
check("correction tamper rejects", isinstance(verify_cce5_certificate(replace(cert, compact_correction=(0, 0))), Refusal))
check("abc tamper rejects", isinstance(verify_cce5_certificate(replace(cert, trace_comparison_abc=(0, 0, 0))), Refusal))

checkpoint = make_cce5_checkpoint(results["upper"])
check("checkpoint mutation rejects", not verify_cce5_checkpoint(replace(checkpoint, checkpoint_digest="0" * 64), results["upper"]))
check("checkpoint splice refuses", isinstance(resume_cce5(checkpoint, released_cce5_request("lower")), Refusal))

source = Path(__file__).resolve().parents[1].joinpath("src/cella/continuation/cce5.py").read_text()
check("campaign-local scout is separate from production", "pathfinder_m1_scout.py" not in source)
check("no external CAS", all(token not in source for token in ("import sympy", "import sage", "subprocess")))

print(f"CCE-5 exact corridor and generated-groupoid gate: {passed} assertions passed")
