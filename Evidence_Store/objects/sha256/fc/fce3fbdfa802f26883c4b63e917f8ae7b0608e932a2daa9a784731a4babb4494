#!/usr/bin/env python3
"""Standalone exact replay of the CCE-3 relative-class mathematics.

The historical filename is retained as a retrieval handle.  This verifier no
longer constructs or compares cryptographic release certificates.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "engine/src").is_dir())
sys.path.insert(0, str(ROOT / "engine/src"))

from cella.continuation import continue_relative_class_certified, released_cce3_request  # noqa: E402
from cella.continuation.canonical import to_canonical_data  # noqa: E402
from cella.continuation.model import CoefficientRing as C, Refusal  # noqa: E402
from cella.continuation.relative_classes import (  # noqa: E402
    HALF_DG, I_DG, ONE_DG, ZERO_DG, construct_basis_manifest,
)

HERE = Path(__file__).parent
passed = 0


def check(label: str, condition: bool) -> None:
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


operations = (
    ("lateral_pair", C.Z),
    ("cpv", C.Z_HALF),
    ("phase_upper", C.Z_I),
    ("phase_lower", C.Z_I),
    ("phase_cpv", C.Z_HALF_I),
    ("prove_phase_obstruction", C.Z),
)
results = {op: continue_relative_class_certified(released_cce3_request(op, ring)) for op, ring in operations}
check("all released operations construct", all(not isinstance(result, Refusal) for result in results.values()))

basis = construct_basis_manifest("1fc835086c30fbae414853f186a9cab9ac8c39e6cff1ed79b7364ebb5db6d5ae")
stored_basis = json.loads((HERE / "DBP_RELATIVE_CLASS_BASIS_MANIFEST_v1.0.json").read_text())
check("basis artifact exact", stored_basis["manifest"] == to_canonical_data(basis))

pair = results["lateral_pair"].certificate.lateral_pair
cpv = results["cpv"].certificate.cpv_record
check("upper vector exact", pair.upper_selected_class.coordinates == (ZERO_DG, ZERO_DG, ZERO_DG, ONE_DG))
check("lower vector exact", pair.lower_selected_class.coordinates == (ZERO_DG, ZERO_DG, ONE_DG, ONE_DG))
check("upper quotient exact", pair.upper_transport.known_quotient_class.quotient_coordinates == (ZERO_DG, ONE_DG))
check("lower quotient exact", pair.lower_transport.known_quotient_class.quotient_coordinates == (ONE_DG, ONE_DG))
check("independent corrections retained", {pair.upper_transport.uncertainty_terms[0].correction.symbol_id, pair.lower_transport.uncertainty_terms[0].correction.symbol_id} == {"lambda_up", "lambda_down"})
check("CPV exact midpoint", cpv is not None and cpv.selected_endpoint_half_sum.coordinates == (ZERO_DG, ZERO_DG, HALF_DG, ONE_DG))
check("CPV affine ambiguity exact", cpv is not None and [(term.correction.symbol_id, term.coefficient) for term in cpv.compact_ambiguity_terms] == [("lambda_down", HALF_DG), ("lambda_up", HALF_DG)])
check("i-lateral boundary exact", results["phase_upper"].certificate.phased_class.boundary_coefficient == I_DG)
check("obstruction exact", results["prove_phase_obstruction"].certificate.obstruction_witness.phased_boundary == I_DG)

matrix = json.loads((HERE / "CCE_3_TEST_REFUSAL_MATRIX_v1.0.json").read_text())
check("refusal matrix nonempty", len(matrix["cases"]) >= 10)
for row in matrix["cases"]:
    ring = next(ring for ring in C if ring.value == row["ring"])
    outcome = continue_relative_class_certified(released_cce3_request(row["operation"], ring))
    check(f"refusal {row['case_id']}", isinstance(outcome, Refusal) and outcome.code == row["expected_code"] == row["observed_code"])

print(f"CCE-3 direct relative-class proof replay: {passed} assertions passed")
