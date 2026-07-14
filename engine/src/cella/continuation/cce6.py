"""Thin production import of the completed CCE-6 native-surface package.

The mathematical replay remains owned by the supplied standalone package.
This adapter only source-locks that package and exposes its released two-route
scope through the continuation engine.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from .canonical import canonical_digest
from .model import Refusal


SCHEMA_ID = "cella.continuation.cce6_surface_package_import_certificate"
SCHEMA_VERSION = "1.0"
VERIFIER_VERSION = "cella.continuation.cce6.import.verifier.v1"
PACKAGE_CERT_DIGEST = "5326bb2fe928c107264cd45f693fd7e0102551ab8aa60f61e339fa4eeabd6397"
PACKAGE_THEOREM_DIGEST = "8f59e6641a9d7d588d284c3570695b43ebf7f77abd395beef6af2c1c6e0a3ef7"
PACKAGE_VERIFIER_DIGEST = "d196955cc9d5eec7261c7b7ca1edbbd27bf93a98c53409141ffd3a0fc8e0fd00"
CCE2_STAGE_DIGEST = "f4db1c6252015bff0fb905ad3831d9d05c210b9e6dbb0ecc471c858394a49ee9"
CCE2_CLEARANCE_DIGEST = "160c8efbf8e781ae8ca8336bd754ad170208fdccfe8dc8f0d30cae97f9463a50"
ROUTES = ("dbp_corridor_upper_qi_v1", "dbp_corridor_lower_qi_v1")
REFUSALS = ("OutsideNativeSurfaceImage", "WholeSurfaceScopeUnproved", "SurfaceRouteAdmissibilityMissing")


def _sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _package_paths() -> tuple[tuple[str, Path, str], ...]:
    root = Path(__file__).parents[4]
    package = root / "research/campaigns/CELLA_CONTINUATION_ENGINE/07_cce6_surface/CCE_6_COMPLETE_PACKAGE_v1.0"
    return (
        ("completed_certificate", package / "DBP_NATIVE_SURFACE_SWEEP_CLEARANCE_CERTIFICATE_v1.0.json", PACKAGE_CERT_DIGEST),
        ("completed_theorem", package / "DBP_NATIVE_SURFACE_SWEEP_CLEARANCE_THEOREM_v1.0.md", PACKAGE_THEOREM_DIGEST),
        ("standalone_verifier", package / "verify_dbp_native_surface_sweep_clearance.py", PACKAGE_VERIFIER_DIGEST),
        ("live_cce2_stage", root / "research/campaigns/CELLA_CONTINUATION_ENGINE/03_cce2_corridors/CCE_2_STAGE_REPORT_v1.0.json", CCE2_STAGE_DIGEST),
        ("live_cce2_clearance", root / "research/campaigns/CELLA_CONTINUATION_ENGINE/03_cce2_corridors/DBP_EXACT_CORRIDOR_CLEARANCE_CERTIFICATES_v1.0.json", CCE2_CLEARANCE_DIGEST),
    )


def _load_package() -> tuple[dict, tuple[tuple[str, str], ...]]:
    ledger = []
    paths = _package_paths()
    for name, path, expected in paths:
        if not path.is_file() or _sha256(path) != expected:
            raise CCE6ImportError("StageDependencyUnavailable", "cce6_package_source_lock", f"{name} does not match its imported digest")
        ledger.append((name, expected))
    package = json.loads(paths[0][1].read_text(encoding="utf-8"))
    if package.get("verdict") != "PROVED" or package.get("claim_scope") != "two_exact_dbp_corridors_on_native_surface_image":
        raise CCE6ImportError("SurfacePackageMismatch", "released_claim_scope", "completed package has an unexpected verdict or scope")
    if tuple(package.get("retained_refusals", ())) != REFUSALS:
        raise CCE6ImportError("SurfacePackageMismatch", "retained_refusals", "completed package refusal ceiling changed")
    route_ids = tuple(package["nested_corridor_certificates"][arm]["route_id"] for arm in ("upper", "lower"))
    if route_ids != ROUTES:
        raise CCE6ImportError("SurfacePackageMismatch", "nested_corridors", "completed package route bindings changed")
    return package, tuple(ledger)


@dataclass(frozen=True, slots=True)
class CCE6Request:
    request_id: str
    route_id: str
    requested_scope: str = "native_surface_image"

    @property
    def digest(self) -> str:
        return canonical_digest(self)


@dataclass(frozen=True, slots=True)
class CCE6ImportCertificate:
    schema_id: str
    schema_version: str
    request: CCE6Request
    package_source_ledger: tuple[tuple[str, str], ...]
    package_schema_id: str
    package_verdict: str
    claim_scope: str
    scope_ceiling: str
    route_binding: tuple[tuple[str, str], ...]
    quantitative_witnesses: tuple[tuple[str, str], ...]
    retained_refusals: tuple[str, ...]
    import_note: str
    verifier_version: str
    canonical_certificate_digest: str


@dataclass(frozen=True, slots=True)
class CertifiedSurfaceSweep:
    request: CCE6Request
    certificate: CCE6ImportCertificate


class CCE6ImportError(ValueError):
    def __init__(self, code: str, obligation: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.obligation = obligation
        self.detail = detail


def _assemble(request: CCE6Request) -> CCE6ImportCertificate:
    if request.requested_scope == "whole_surface":
        raise CCE6ImportError("WholeSurfaceScopeUnproved", "native_surface_scope_ceiling", "CCE-6 proves only image(L_Z)")
    if request.requested_scope != "native_surface_image":
        raise CCE6ImportError("OutsideNativeSurfaceImage", "native_surface_scope", "requested carrier is outside the native swept image")
    if request.route_id not in ROUTES:
        raise CCE6ImportError("SurfaceRouteAdmissibilityMissing", "released_corridor_binding", "route is not one of the two completed CCE-6 corridors")
    package, source_ledger = _load_package()
    arm = "upper" if request.route_id == ROUTES[0] else "lower"
    nested = package["nested_corridor_certificates"][arm]
    transfer = package["quantitative_transfer"]
    unsigned = {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "request": request,
        "package_source_ledger": source_ledger,
        "package_schema_id": package["schema_id"],
        "package_verdict": package["verdict"],
        "claim_scope": package["claim_scope"],
        "scope_ceiling": package["scope_ceiling"],
        "route_binding": (
            ("route_id", nested["route_id"]),
            ("route_manifest_digest", nested["route_manifest_digest"]),
            ("clearance_certificate_digest", nested["clearance_certificate_digest"]),
            ("selected_terminal_class", nested["selected_terminal_class"]),
        ),
        "quantitative_witnesses": (
            ("epsilon_infinity", transfer["released_route_epsilon_infinity"]),
            ("epsilon_1", transfer["released_route_epsilon_1"]),
            ("epsilon_2", transfer["released_route_epsilon_2"]),
        ),
        "retained_refusals": tuple(package["retained_refusals"]),
        "import_note": "mathematics replayed by the source-locked standalone CCE-6 verifier; this is the production import binding",
        "verifier_version": VERIFIER_VERSION,
    }
    return CCE6ImportCertificate(**unsigned, canonical_certificate_digest=canonical_digest(unsigned))


def continue_surface_sweep_certified(request: CCE6Request) -> CertifiedSurfaceSweep | Refusal:
    try:
        certificate = _assemble(request)
        return CertifiedSurfaceSweep(request, certificate)
    except CCE6ImportError as exc:
        return Refusal(exc.code, exc.obligation, "cella.continuation.cce6", False, True, exc.detail)


def verify_cce6_import_certificate(certificate: CCE6ImportCertificate) -> bool | Refusal:
    try:
        expected = _assemble(certificate.request)
    except CCE6ImportError as exc:
        return Refusal(exc.code, exc.obligation, "cella.continuation.cce6.verify", False, True, exc.detail)
    if certificate != expected:
        return Refusal("SurfacePackageMismatch", "canonical_import_reconstruction", "cella.continuation.cce6.verify", False, False, "CCE-6 import certificate differs from reconstruction")
    return True


def released_cce6_request(arm: str = "upper") -> CCE6Request:
    if arm not in ("upper", "lower"):
        raise ValueError("arm must be upper or lower")
    return CCE6Request(f"cce6-native-surface-{arm}-v1", ROUTES[0 if arm == "upper" else 1])
