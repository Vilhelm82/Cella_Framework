#!/usr/bin/env python3
"""Normalized-incidence/inertia import and tamper gate."""

from dataclasses import replace
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.continuation.cce7_inertia import (
    normalized_incidence_inertia_certificate,
    verify_normalized_incidence_inertia_certificate,
)
from cella.continuation.model import Refusal


passed = 0


def check(label, condition):
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


cert = normalized_incidence_inertia_certificate()
check("source closure has six locks", len(cert.source_ledger) == 6)
check("relative Jacobian is exact", cert.relative_jacobian == "8*e3(w1,w2,w3,w4)")
check("difference divisor degree imported", ("rotating_difference", 1, 64) in cert.realized_strata)
check("mass/difference intersection degree imported", ("mass_ramification+rotating_difference", 2, 192) in cert.realized_strata)
check("equal-charge crossing stays unramified", dict(cert.generic_inertia)["equal_squared_charges"].startswith("unramified"))
check("reciprocal sub-balance has C4 inertia", dict(cert.generic_inertia)["reciprocal_sub_balance"].startswith("C4"))
check("certificate independently replays", verify_normalized_incidence_inertia_certificate(cert) is True)
check("Jacobian mutation rejects", isinstance(verify_normalized_incidence_inertia_certificate(replace(cert, relative_jacobian="projected_discriminant")), Refusal))
check("inertia mutation rejects", isinstance(verify_normalized_incidence_inertia_certificate(replace(cert, generic_inertia=(("equal_squared_charges", "C2"),))), Refusal))
check("complex route work remains named", "complex loop" in cert.active_obligation)

print(f"CCE-7 normalized-incidence inertia import: {passed} assertions passed")
