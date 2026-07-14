"""Thin CCE-6 completed-package import gate; no mathematical re-proof."""

from dataclasses import replace
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cella.continuation.cce6 import (
    CCE6Request, CertifiedSurfaceSweep, continue_surface_sweep_certified,
    released_cce6_request, verify_cce6_import_certificate,
)
from cella.continuation.model import Refusal


passed = 0


def check(label, condition):
    global passed
    if not condition:
        raise AssertionError(label)
    passed += 1


for arm in ("upper", "lower"):
    request = released_cce6_request(arm)
    first = continue_surface_sweep_certified(request)
    second = continue_surface_sweep_certified(request)
    check(f"{arm} imports", isinstance(first, CertifiedSurfaceSweep))
    check(f"{arm} deterministic", first == second)
    check(f"{arm} verifies", isinstance(first, CertifiedSurfaceSweep) and verify_cce6_import_certificate(first.certificate) is True)
    if isinstance(first, CertifiedSurfaceSweep):
        check(f"{arm} package proved", first.certificate.package_verdict == "PROVED")
        check(f"{arm} has positive exact witnesses", all(value == "1/105186307200" for _, value in first.certificate.quantitative_witnesses))

outside = continue_surface_sweep_certified(replace(released_cce6_request(), requested_scope="other_surface_carrier"))
check("outside native refuses", isinstance(outside, Refusal) and outside.code == "OutsideNativeSurfaceImage")
whole = continue_surface_sweep_certified(replace(released_cce6_request(), requested_scope="whole_surface"))
check("whole surface refuses", isinstance(whole, Refusal) and whole.code == "WholeSurfaceScopeUnproved")
route = continue_surface_sweep_certified(CCE6Request("unknown", "unreleased_route"))
check("unknown route refuses", isinstance(route, Refusal) and route.code == "SurfaceRouteAdmissibilityMissing")

cert = continue_surface_sweep_certified(released_cce6_request())
if isinstance(cert, CertifiedSurfaceSweep):
    check("tamper rejects", isinstance(verify_cce6_import_certificate(replace(cert.certificate, package_verdict="UNKNOWN")), Refusal))

source = Path(__file__).resolve().parents[1].joinpath("src/cella/continuation/cce6.py").read_text()
check("campaign-local scout is separate from production", "pathfinder_m1_scout.py" not in source)
check("no proof duplication", "def reduce_cover" not in source and "def equal_cover" not in source)

print(f"CCE-6 completed-package import gate: {passed} assertions passed")
