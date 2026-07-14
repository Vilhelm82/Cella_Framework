"""CCE-3 exact rings, relative classes, CPV, certificates and refusals."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.continuation import (
    CertifiedRelativeClassResult, continue_relative_class_certified,
    make_cce3_checkpoint, released_cce3_request, resume_cce3,
    verify_cce3_certificate, verify_cce3_checkpoint,
    verify_cce3_checkpoint_chain,
)
from cella.continuation.canonical import canonical_json_bytes
from cella.continuation.model import CoefficientRing, Refusal
from cella.continuation.relative_classes import (
    AffineRelativeClass, ClaimScope, DyadicGaussian, HALF_DG, I_DG, ONE_DG,
    REFUSAL_VOCABULARY, RelativeClassError, RelativeClassVector, ZERO_DG,
    add_affine_classes, add_classes, compact_submodule_digest, compute_boundary,
    construct_basis_manifest, extend_scalars, minimal_ring, restrict_scalars_if_member,
    scalar_is_member, scale_affine_class, subtract_affine_classes,
    take_compact_quotient, vector_minimal_ring,
)

passed = 0


def check(label: str, condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


# Exact dyadic-Gaussian engine and coefficient diamond.
check("canonical zero", DyadicGaussian(0, 0, 9) == ZERO_DG)
check("canonical dyadic reduction", DyadicGaussian(6, 2, 3) == DyadicGaussian(3, 1, 2))
check("exact addition", DyadicGaussian(1, 0, 1) + DyadicGaussian(1, 0, 2) == DyadicGaussian(3, 0, 2))
check("exact Gaussian multiplication", I_DG * I_DG == DyadicGaussian(-1))
check("Z membership", scalar_is_member(ONE_DG, CoefficientRing.Z) and not scalar_is_member(HALF_DG, CoefficientRing.Z))
check("Z[1/2] membership", scalar_is_member(HALF_DG, CoefficientRing.Z_HALF) and not scalar_is_member(I_DG, CoefficientRing.Z_HALF))
check("Z[i] membership", scalar_is_member(I_DG, CoefficientRing.Z_I) and not scalar_is_member(DyadicGaussian(1, 1, 1), CoefficientRing.Z_I))
check("top-ring membership", scalar_is_member(DyadicGaussian(1, 1, 1), CoefficientRing.Z_HALF_I))
check("minimal integer ring", minimal_ring(ONE_DG) == CoefficientRing.Z)
check("minimal dyadic ring", minimal_ring(HALF_DG) == CoefficientRing.Z_HALF)
check("minimal Gaussian ring", minimal_ring(I_DG) == CoefficientRing.Z_I)
check("minimal dyadic Gaussian ring", minimal_ring(DyadicGaussian(1, 1, 1)) == CoefficientRing.Z_HALF_I)
try:
    DyadicGaussian.parse_canonical(2, 0, 1)
except RelativeClassError as exc:
    check("noncanonical scalar rejected", exc.code == "MalformedScalar")
else:
    check("noncanonical scalar rejected", False)

basis = construct_basis_manifest("1fc835086c30fbae414853f186a9cab9ac8c39e6cff1ed79b7364ebb5db6d5ae")
check("ordered rank-four basis", basis.ordered_generators == ("A_minus", "B_minus", "mu_minus", "delta_minus_up"))
check("boundary vector", basis.boundary_vector == (0, 0, 0, 1))
check("compact submodule exactly A/B", basis.compact_submodule_basis == ("A_minus", "B_minus"))
check("quotient retains meridian", basis.quotient_basis == ("mu_minus", "delta_minus_up"))
check("partial intersection only", basis.compact_intersection == ((0, 1), (-1, 0)) and bool(basis.unclaimed_intersection_entries))
check("primitive witness source-bound", "primitive" in basis.primitive_meridian_witness)

results = {}
for operation, ring in (
    ("lateral_pair", CoefficientRing.Z),
    ("cpv", CoefficientRing.Z_HALF),
    ("cpv", CoefficientRing.Z_HALF_I),
    ("phase_upper", CoefficientRing.Z_I),
    ("phase_lower", CoefficientRing.Z_I),
    ("phase_cpv", CoefficientRing.Z_HALF_I),
    ("prove_phase_obstruction", CoefficientRing.Z),
):
    first = continue_relative_class_certified(released_cce3_request(operation, ring))
    second = continue_relative_class_certified(released_cce3_request(operation, ring))
    check(f"{operation}/{ring.value} certifies", isinstance(first, CertifiedRelativeClassResult))
    check(f"{operation}/{ring.value} deterministic", canonical_json_bytes(first) == canonical_json_bytes(second))
    check(f"{operation}/{ring.value} verifies", isinstance(first, CertifiedRelativeClassResult) and verify_cce3_certificate(first.certificate) is True)
    results[(operation, ring)] = first

pair = results[("lateral_pair", CoefficientRing.Z)].certificate.lateral_pair
check("upper exact coordinates", pair.upper_selected_class.coordinates == (ZERO_DG, ZERO_DG, ZERO_DG, ONE_DG))
check("lower exact coordinates", pair.lower_selected_class.coordinates == (ZERO_DG, ZERO_DG, ONE_DG, ONE_DG))
check("common primitive boundary", compute_boundary(pair.upper_selected_class) == compute_boundary(pair.lower_selected_class) == ONE_DG)
check("upper quotient", take_compact_quotient(pair.upper_selected_class, basis).quotient_coordinates == (ZERO_DG, ONE_DG))
check("lower quotient", take_compact_quotient(pair.lower_selected_class, basis).quotient_coordinates == (ONE_DG, ONE_DG))
check("mu survives quotient", take_compact_quotient(pair.lower_selected_class, basis).quotient_coordinates[0] == ONE_DG)
check("independent compact symbols", {pair.upper_transport.uncertainty_terms[0].correction.symbol_id, pair.lower_transport.uncertainty_terms[0].correction.symbol_id} == {"lambda_up", "lambda_down"})
check("compact correction submodule", all(term.correction.submodule_digest == compact_submodule_digest(basis) for transport in (pair.upper_transport, pair.lower_transport) for term in transport.uncertainty_terms))

cpv = results[("cpv", CoefficientRing.Z_HALF)].certificate.cpv_record
check("CPV record present", cpv is not None)
check("CPV exact coordinates", cpv is not None and cpv.selected_endpoint_half_sum.coordinates == (ZERO_DG, ZERO_DG, HALF_DG, ONE_DG))
check("CPV quotient", cpv is not None and cpv.quotient_half_sum.quotient_coordinates == (HALF_DG, ONE_DG))
check("CPV minimal ring", cpv is not None and cpv.minimal_ring == CoefficientRing.Z_HALF)
check("CPV boundary beta", cpv is not None and compute_boundary(cpv.selected_endpoint_half_sum) == ONE_DG)
check("affine CPV keeps two halves", cpv is not None and [(term.correction.symbol_id, term.coefficient) for term in cpv.compact_ambiguity_terms] == [("lambda_down", HALF_DG), ("lambda_up", HALF_DG)])
check("endpoint and transported CPV distinct", cpv is not None and cpv.selected_endpoint_half_sum.digest != cpv.transported_affine_half_sum.digest)

phase_upper = results[("phase_upper", CoefficientRing.Z_I)].certificate.phased_class
phase_cpv = results[("phase_cpv", CoefficientRing.Z_HALF_I)].certificate.phased_class
check("i-lateral minimal ring", phase_upper is not None and vector_minimal_ring(phase_upper) == CoefficientRing.Z_I)
check("i-CPV minimal ring", phase_cpv is not None and vector_minimal_ring(phase_cpv) == CoefficientRing.Z_HALF_I)
check("phased boundary i beta", phase_upper is not None and compute_boundary(phase_upper) == I_DG)
obstruction = results[("prove_phase_obstruction", CoefficientRing.Z)].certificate.obstruction_witness
check("boundary obstruction replays", obstruction is not None and obstruction.phased_boundary == I_DG and obstruction.closed_cycle_boundary == ZERO_DG and "outside Z*beta" in obstruction.contradiction)

# Exact algebra and uncertainty behavior.
integral_sum = add_classes(pair.upper_selected_class, pair.lower_selected_class)
check("exact vector addition", integral_sum.coordinates == (ZERO_DG, ZERO_DG, ONE_DG, DyadicGaussian(2)))
extended = extend_scalars(pair.upper_selected_class, CoefficientRing.Z_HALF)
check("legal scalar extension", extended.ring_id == CoefficientRing.Z_HALF)
check("exact scalar restriction", restrict_scalars_if_member(extended, CoefficientRing.Z).ring_id == CoefficientRing.Z)
try:
    restrict_scalars_if_member(cpv.selected_endpoint_half_sum, CoefficientRing.Z)  # type: ignore[union-attr]
except RelativeClassError as exc:
    check("failed scalar restriction", exc.code == "ScalarRestrictionFailed")
else:
    check("failed scalar restriction", False)
cancelled = add_affine_classes(pair.upper_transport, scale_affine_class(DyadicGaussian(-1), pair.upper_transport))
check("same uncertainty symbol cancels exactly", isinstance(cancelled, RelativeClassVector) and cancelled.coordinates == (ZERO_DG,) * 4)
different = subtract_affine_classes(pair.upper_transport, pair.lower_transport)
check("different uncertainty symbols never cancel", isinstance(different, AffineRelativeClass) and {term.correction.symbol_id for term in different.uncertainty_terms} == {"lambda_up", "lambda_down"})

# Public refusal behavior.
for operation, ring, code in (
    ("cpv", CoefficientRing.Z, "RingTooSmall"),
    ("cpv", CoefficientRing.Z_I, "RingTooSmall"),
    ("phase_upper", CoefficientRing.Z, "RingTooSmall"),
    ("phase_cpv", CoefficientRing.Z_HALF, "RingTooSmall"),
    ("integral_phase_replacement", CoefficientRing.Z, "BoundaryObstruction"),
    ("absolute_scalar", CoefficientRing.Z, "AbsoluteRepresentativeUnknown"),
    ("full_transport_matrix", CoefficientRing.Z, "FullTransportMatrixUnavailable"),
    ("evaluate", CoefficientRing.Z_HALF, "EvaluationStageRequired"),
    ("surface_lift", CoefficientRing.Z, "UnsupportedOperation"),
    ("compose_routes", CoefficientRing.Z, "UnsupportedOperation"),
):
    refusal = continue_relative_class_certified(released_cce3_request(operation, ring))
    check(f"{operation} stable refusal", isinstance(refusal, Refusal) and refusal.code == code)
check("closed refusal vocabulary", len(REFUSAL_VOCABULARY) == len(set(REFUSAL_VOCABULARY)) == 24)

bad_input = continue_relative_class_certified(replace(released_cce3_request("cpv", CoefficientRing.Z_HALF), input_class="bare_route_label"))
check("route label without input class refuses", isinstance(bad_input, Refusal) and bad_input.code == "UnsupportedInputClass")
bad_scope = continue_relative_class_certified(replace(released_cce3_request("cpv", CoefficientRing.Z_HALF), requested_claim_scope=ClaimScope.EXACT_ABSOLUTE_CLASS))
check("claim escalation refuses", isinstance(bad_scope, Refusal) and bad_scope.code == "QuotientScopeMismatch")

# Certificate/checkpoint tampering.
cert = results[("cpv", CoefficientRing.Z_HALF)].certificate
check("nested CCE-2 bundle locked", cert.source_ledger.cce2_bundle_digest == "b2fc82f6705cfe25070a641f4678f2caf94c35e36a11bc1023a9fd9a4f56605c")
check("PF-0 bound", cert.source_ledger.pf0_confirmation_digest == "304fccce5ed1206f23969952634d10b250d8d4d7a7a955971afa8018c2372008")
check("52-file closure bound", len(cert.source_ledger.pathfinder_closure_digest) == 64)
check("CCE-3 implementation closure bound", len(cert.source_ledger.cce3_source_digest) == 64)
tampered = replace(cert, output_digest="0" * 64)
check("certificate tampering rejected", isinstance(verify_cce3_certificate(tampered), Refusal))
try:
    replace(cert.lateral_pair.upper_transport, uncertainty_terms=())
except RelativeClassError as exc:
    check("uncertainty deletion rejected", exc.code == "UnknownCompactCorrection")
else:
    check("uncertainty deletion rejected", False)

result = results[("cpv", CoefficientRing.Z_HALF)]
checkpoint = make_cce3_checkpoint(result)
check("checkpoint verifies", verify_cce3_checkpoint(checkpoint, result))
check("checkpoint tampering rejects", not verify_cce3_checkpoint(replace(checkpoint, checkpoint_digest="0" * 64), result))
resumed = resume_cce3(checkpoint, result.request)
check("checkpoint resume certifies", isinstance(resumed, CertifiedRelativeClassResult) and resumed.certificate.previous_checkpoint_digest == checkpoint.checkpoint_digest)
second = make_cce3_checkpoint(resumed, previous_checkpoint=checkpoint)
check("checkpoint chain verifies", verify_cce3_checkpoint_chain((checkpoint, second)))
check("second checkpoint requires predecessor", verify_cce3_checkpoint(second, resumed, (checkpoint,)) and not verify_cce3_checkpoint(second, resumed))
check("predecessor tampering rejects", not verify_cce3_checkpoint_chain((replace(checkpoint, checkpoint_digest="0" * 64), second)))
wrong_resume = resume_cce3(checkpoint, released_cce3_request("phase_upper", CoefficientRing.Z_I))
check("wrong-request resume refuses", isinstance(wrong_resume, Refusal) and wrong_resume.code == "CheckpointMismatch")

source = "\n".join(path.read_text() for path in (Path(__file__).resolve().parents[1] / "src").rglob("*.py"))
check("campaign-local scout is separate from production", "pathfinder_m1_scout.py" not in source)
cce3_source = (Path(__file__).resolve().parents[1] / "src/cella/continuation/cce3.py").read_text() + (Path(__file__).resolve().parents[1] / "src/cella/continuation/relative_classes.py").read_text()
check("no external CAS in CCE-3", all(token not in cce3_source for token in ("import sympy", "import sage", "subprocess")))

print(f"CCE-3 typed relative-class and CPV engine: {passed} assertions passed")
