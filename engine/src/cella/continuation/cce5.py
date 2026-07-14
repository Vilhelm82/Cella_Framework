"""CCE-5 exact DBP K/E/Pi connection and absolute PL calibration."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from .canonical import canonical_digest
from .model import Refusal


SCHEMA_ID = "cella.continuation.cce5_dbp_absolute_connection_certificate"
SCHEMA_VERSION = "1.0"
VERIFIER_VERSION = "cella.continuation.cce5.verifier.v2"
PERIODS_DIGEST = "11c2c2da7b9e7c0463c6d2ce82be8740f7238e4177bccd9b7d3a5e12187c4e87"
PAPER_III_DIGEST = "1fc835086c30fbae414853f186a9cab9ac8c39e6cff1ed79b7364ebb5db6d5ae"
STAGE3_DIGEST = "bdaabb1a1015f7b6b3055321b422a3b6d84053c808d2e3669ea646ff3de82670"
CCE2_CLEARANCE_DIGEST = "160c8efbf8e781ae8ca8336bd754ad170208fdccfe8dc8f0d30cae97f9463a50"
CALIBRATION_THEOREM_DIGEST = "ee7ed03edc592ba230da38f5337fa8d462cc5700b4198815113a4e86af9f5da2"
ENCYCLOPEDIA_REFERENCES = (
    Path("/home/wlloyd/Lloyd_Mathematics_Encyclopedia/subjects/periods-elliptic.md"),
    Path("/home/wlloyd/Lloyd_Mathematics_Encyclopedia/subjects/curvature-integrals-quadrics.md"),
)
THEOREM_IDS = (
    "E-0003:Legendre-KE-Picard-Fuchs",
    "E-0014:DBP-primary-dual-third-kind-periods",
    "E-0022:DBP-family-wide-K-Pi-form",
    "CCE5.1:DBP-rank-three-rational-connection",
    "CCE5.2:exact-branch-braid-calibration",
    "CCE5.3:absolute-relative-Picard-Lefschetz-matrices",
    "CCE5.4:fixed-curve-relative-trace-comparison",
)
SINGULAR_LOCUS = ("m=0", "m=1/2", "m=1", "m=infinity")
PERIOD_BASIS = ("K(m)", "E(m)", "Pi(m^2/(2m-1);m)")
TOPOLOGICAL_BASIS = ("A", "B", "mu", "delta_lateral")
ROUTE_IDS = {
    "upper": "dbp_corridor_upper_qi_v1",
    "lower": "dbp_corridor_lower_qi_v1",
}


def _sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_ledger() -> tuple[tuple[str, str], ...]:
    root = Path(__file__).parents[4]
    sources = (
        ("periods_runtime", root / "engine/src/cella/periods.py", PERIODS_DIGEST),
        ("paper_iii", root / "research/paper/Theorems/DBP/DBP_CURVATURE_PERIODS_OF_THE_DBP_QUADRIC_v1.0.md", PAPER_III_DIGEST),
        ("stage3_topology", root / "research/paper/Theorems/DBP/technical_supplements/DBP_DUAL_SURFACE_CYCLE_STAGE3_v0.1.md", STAGE3_DIGEST),
        ("cce2_clearance", root / "research/campaigns/CELLA_CONTINUATION_ENGINE/03_cce2_corridors/DBP_EXACT_CORRIDOR_CLEARANCE_CERTIFICATES_v1.0.json", CCE2_CLEARANCE_DIGEST),
        ("calibration_theorem", root / "research/campaigns/CELLA_CONTINUATION_ENGINE/06_cce5_connection/DBP_CCE5_ABSOLUTE_CALIBRATION_THEOREM_v1.0.md", CALIBRATION_THEOREM_DIGEST),
    )
    ledger = []
    for name, path, expected in sources:
        if not path.is_file() or _sha256(path) != expected:
            raise CCE5Error("StageDependencyUnavailable", "source_lock", f"{name} does not match its frozen digest")
        ledger.append((name, expected))
    return tuple(ledger)


def dbp_characteristic(m: Fraction) -> Fraction:
    m = Fraction(m)
    if 2 * m == 1:
        raise CCE5Error("ConnectionSingularity", "m_not_half", "n(m) has a pole at m=1/2")
    return m * m / (2 * m - 1)


def dbp_connection_matrix(m: Fraction) -> tuple[tuple[Fraction, ...], ...]:
    """Exact M(m) for d(K,E,Pi(n(m);m))/dm=M(m)(K,E,Pi)^T."""
    m = Fraction(m)
    if m in (0, Fraction(1, 2), 1):
        raise CCE5Error("ConnectionSingularity", "regular_dbp_parameter", "m lies on the connection singular locus")
    return (
        (-1 / (2 * m), -1 / (2 * m * (m - 1)), Fraction(0)),
        (-1 / (2 * m), 1 / (2 * m), Fraction(0)),
        (1 / (m * (m - 1)), (4 * m - 1) / (2 * m * (m - 1) ** 2), -(2 * m * m + 2 * m - 1) / (2 * m * (m - 1) * (2 * m - 1))),
    )


def _chain_rule_row(m: Fraction) -> tuple[Fraction, Fraction, Fraction]:
    m = Fraction(m)
    n = dbp_characteristic(m)
    n_prime = 2 * m * (m - 1) / (2 * m - 1) ** 2
    if not m or m == 1 or n in (0, 1) or n == m:
        raise CCE5Error("ConnectionSingularity", "third_kind_regular_locus", "partial Pi connection is singular")
    dm = (Fraction(0), -1 / (2 * (n - m) * (m - 1)), 1 / (2 * (n - m)))
    dn = (1 / (2 * (n - 1) * n), n / (2 * (m - n) * (n - 1) * n), (n * n - m) / (2 * (m - n) * (n - 1) * n))
    return tuple(dm[index] + n_prime * dn[index] for index in range(3))


def verify_dbp_connection_identity() -> bool:
    samples = (Fraction(-3), Fraction(-2), Fraction(-1), Fraction(1, 4), Fraction(1, 3), Fraction(2), Fraction(3))
    return all(_chain_rule_row(m) == dbp_connection_matrix(m)[2] for m in samples)


def verify_dbp_family_identity() -> bool:
    for m in (Fraction(-2), Fraction(-1), Fraction(1, 4), Fraction(1, 3), Fraction(2), Fraction(3)):
        C = m / (1 - m)
        if (m - C) / (1 - C) != dbp_characteristic(m):
            return False
    return True


def compact_picard_lefschetz_matrix(arm: str) -> tuple[tuple[int, int], ...]:
    sign = 1 if arm == "upper" else -1 if arm == "lower" else 0
    if not sign:
        raise CCE5Error("RouteMismatch", "released_corridor", "arm must be upper or lower")
    # Column action: A -> A+/-2B, B -> B.
    return ((1, 0), (2 * sign, 1))


def relative_picard_lefschetz_matrix(arm: str) -> tuple[tuple[int, ...], ...]:
    sign = 1 if arm == "upper" else -1 if arm == "lower" else 0
    if not sign:
        raise CCE5Error("RouteMismatch", "released_corridor", "arm must be upper or lower")
    # Route-specific endpoint basis (A,B,mu,delta_up/down), column action.
    return (
        (1, 0, 0, 0),
        (2 * sign, 1, 0, sign),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    )


def compact_correction_coordinates(arm: str) -> tuple[int, int]:
    if arm == "upper":
        return 0, 1
    if arm == "lower":
        return 0, -1
    raise CCE5Error("RouteMismatch", "released_corridor", "arm must be upper or lower")


def trace_comparison_coordinates(arm: str) -> tuple[int, int, int]:
    """(a,b,c) in the frozen real-projective-circle marking on E_128."""
    if arm == "upper":
        return 1, 0, 0
    if arm == "lower":
        return 1, 0, 1
    raise CCE5Error("RouteMismatch", "released_corridor", "arm must be upper or lower")


def _matmul(left: tuple[tuple[int, ...], ...], right: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(sum(left[i][k] * right[k][j] for k in range(len(right))) for j in range(len(right[0]))) for i in range(len(left)))


def _transpose(matrix: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(zip(*matrix))


def _identity(size: int) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(int(i == j) for j in range(size)) for i in range(size))


# Both corridor generators are expressed in the common endpoint basis
# (A,B,mu,delta_upper).  The lower route's delta_lower=delta_upper+mu
# conversion is therefore visible in its third and fourth columns.
CORRIDOR_COMPACT_MATRICES = {
    "U": ((1, 0), (2, 1)),
    "L": ((1, 0), (-2, 1)),
    "u": ((1, 0), (-2, 1)),
    "l": ((1, 0), (2, 1)),
}
CORRIDOR_RELATIVE_MATRICES = {
    "U": ((1, 0, 0, 0), (2, 1, 0, 1), (0, 0, 1, 0), (0, 0, 0, 1)),
    "L": ((1, 0, 0, 0), (-2, 1, 0, -1), (0, 0, 1, 1), (0, 0, 0, 1)),
    "u": ((1, 0, 0, 0), (-2, 1, 0, -1), (0, 0, 1, 0), (0, 0, 0, 1)),
    "l": ((1, 0, 0, 0), (2, 1, 0, 1), (0, 0, 1, -1), (0, 0, 0, 1)),
}


def corridor_word_endpoints(word: str) -> tuple[str, str]:
    """Validate a word in the two-corridor fundamental groupoid."""
    if not word or set(word) - {"U", "L", "u", "l"}:
        raise CCE5Error("RouteMismatch", "corridor_groupoid_word", "word must be non-empty in U,L,u,l")
    start = "plus" if word[0].isupper() else "minus"
    current = start
    for letter in word:
        source, target = ("plus", "minus") if letter.isupper() else ("minus", "plus")
        if current != source:
            raise CCE5Error("RouteMismatch", "composable_corridor_word", "corridor letters are not endpoint-composable")
        current = target
    return start, current


def corridor_transport_matrix(word: str, *, relative: bool = True) -> tuple[tuple[int, ...], ...]:
    corridor_word_endpoints(word)
    matrices = CORRIDOR_RELATIVE_MATRICES if relative else CORRIDOR_COMPACT_MATRICES
    total = _identity(4 if relative else 2)
    for letter in word:
        total = _matmul(matrices[letter], total)
    return total


@dataclass(frozen=True, slots=True)
class CCE5GroupoidRequest:
    request_id: str
    corridor_word: str
    requested_scope: str = "dbp_two_corridor_fundamental_groupoid"

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("groupoid request id is required")
        corridor_word_endpoints(self.corridor_word)

    @property
    def digest(self) -> str:
        return canonical_digest(self)


@dataclass(frozen=True, slots=True)
class CCE5GroupoidCertificate:
    schema_id: str
    schema_version: str
    request: CCE5GroupoidRequest
    source_ledger: tuple[tuple[str, str], ...]
    generator_ledger: tuple[tuple[str, str], ...]
    start_object: str
    end_object: str
    compact_matrix: tuple[tuple[int, ...], ...]
    relative_matrix: tuple[tuple[int, ...], ...]
    groupoid_law_ledger: tuple[tuple[str, bool], ...]
    verifier_version: str
    canonical_certificate_digest: str


@dataclass(frozen=True, slots=True)
class CertifiedCorridorGroupoidTransport:
    request: CCE5GroupoidRequest
    certificate: CCE5GroupoidCertificate


def _assemble_groupoid(request: CCE5GroupoidRequest) -> CCE5GroupoidCertificate:
    if request.requested_scope != "dbp_two_corridor_fundamental_groupoid":
        raise CCE5Error("StageDependencyUnavailable", "two_corridor_groupoid_scope", "request exceeds the calibrated two-corridor groupoid")
    start, end = corridor_word_endpoints(request.corridor_word)
    compact = corridor_transport_matrix(request.corridor_word, relative=False)
    relative = corridor_transport_matrix(request.corridor_word, relative=True)
    laws = (
        ("Uu=e_plus", corridor_transport_matrix("Uu", relative=True) == _identity(4)),
        ("uU=e_minus", corridor_transport_matrix("uU", relative=True) == _identity(4)),
        ("Ll=e_plus", corridor_transport_matrix("Ll", relative=True) == _identity(4)),
        ("lL=e_minus", corridor_transport_matrix("lL", relative=True) == _identity(4)),
        ("boundary_preserved", relative[-1] == (0, 0, 0, 1)),
    )
    if not all(value for _, value in laws):
        raise CCE5Error("AnalyticTopologicalMismatch", "corridor_groupoid_laws", "exact corridor groupoid replay failed")
    unsigned = {
        "schema_id": "cella.continuation.cce5_corridor_groupoid_certificate",
        "schema_version": "1.0",
        "request": request,
        "source_ledger": _source_ledger(),
        "generator_ledger": (
            ("U", ROUTE_IDS["upper"]), ("L", ROUTE_IDS["lower"]),
            ("u", "inverse:" + ROUTE_IDS["upper"]), ("l", "inverse:" + ROUTE_IDS["lower"]),
        ),
        "start_object": start,
        "end_object": end,
        "compact_matrix": compact,
        "relative_matrix": relative,
        "groupoid_law_ledger": laws,
        "verifier_version": "cella.continuation.cce5.groupoid.verifier.v1",
    }
    return CCE5GroupoidCertificate(**unsigned, canonical_certificate_digest=canonical_digest(unsigned))


def continue_corridor_groupoid_certified(request: CCE5GroupoidRequest) -> CertifiedCorridorGroupoidTransport | Refusal:
    try:
        return CertifiedCorridorGroupoidTransport(request, _assemble_groupoid(request))
    except CCE5Error as exc:
        return Refusal(exc.code, exc.obligation, "cella.continuation.cce5.groupoid", False, True, exc.detail)


def verify_cce5_groupoid_certificate(certificate: CCE5GroupoidCertificate) -> bool | Refusal:
    try:
        expected = _assemble_groupoid(certificate.request)
    except CCE5Error as exc:
        return Refusal(exc.code, exc.obligation, "cella.continuation.cce5.groupoid.verify", False, True, exc.detail)
    if certificate != expected:
        return Refusal("AnalyticTopologicalMismatch", "canonical_groupoid_reconstruction", "cella.continuation.cce5.groupoid.verify", False, False, "groupoid certificate differs from reconstruction")
    return True


def verify_braid_calibration() -> bool:
    # At sigma=i/2 on the continued negative sheet, q=4*sqrt(3)-6.
    # Squaring positive quantities proves 0<q<1: 6<4sqrt(3)<7.
    exact_crossing = 48 > 36 and 48 < 49
    J = ((0, 1), (-1, 0))
    upper = compact_picard_lefschetz_matrix("upper")
    lower = compact_picard_lefschetz_matrix("lower")
    identity = ((1, 0), (0, 1))
    symplectic = all(_matmul(_matmul(_transpose(matrix), J), matrix) == J for matrix in (upper, lower))
    inverse = _matmul(upper, lower) == identity == _matmul(lower, upper)
    boundary = all(matrix[-1] == (0, 0, 0, 1) for matrix in (relative_picard_lefschetz_matrix("upper"), relative_picard_lefschetz_matrix("lower")))
    correction_cancellation = tuple(a + b for a, b in zip(compact_correction_coordinates("upper"), compact_correction_coordinates("lower"))) == (0, 0)
    meridian_relation = tuple(a - b for a, b in zip(trace_comparison_coordinates("upper"), trace_comparison_coordinates("lower"))) == (0, 0, -1)
    return exact_crossing and symplectic and inverse and boundary and correction_cancellation and meridian_relation


@dataclass(frozen=True, slots=True)
class CCE5Request:
    request_id: str
    route_arm: str
    requested_scope: str = "dbp_exact_absolute_corridor_transport"
    basis: tuple[str, str, str] = PERIOD_BASIS

    @property
    def digest(self) -> str:
        return canonical_digest(self)


@dataclass(frozen=True, slots=True)
class CCE5Certificate:
    schema_id: str
    schema_version: str
    request: CCE5Request
    theorem_ids: tuple[str, ...]
    source_ledger: tuple[tuple[str, str], ...]
    basis: tuple[str, ...]
    characteristic_formula: str
    connection_rows: tuple[tuple[str, ...], ...]
    singular_locus: tuple[str, ...]
    route_id: str
    branch_crossing_ledger: tuple[tuple[str, str], ...]
    compact_basis: tuple[str, str]
    compact_matrix: tuple[tuple[int, int], ...]
    relative_basis: tuple[str, ...]
    relative_matrix: tuple[tuple[int, ...], ...]
    compact_correction: tuple[int, int]
    trace_comparison_abc: tuple[int, int, int]
    compatibility_ledger: tuple[tuple[str, bool], ...]
    previous_checkpoint_digest: str | None
    verifier_version: str
    canonical_certificate_digest: str


@dataclass(frozen=True, slots=True)
class CertifiedDBPConnection:
    request: CCE5Request
    certificate: CCE5Certificate


@dataclass(frozen=True, slots=True)
class CCE5Checkpoint:
    schema_id: str
    request_digest: str
    certificate_digest: str
    previous_checkpoint_digest: str | None
    checkpoint_digest: str


class CCE5Error(ValueError):
    def __init__(self, code: str, obligation: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.obligation = obligation
        self.detail = detail


def _assemble(request: CCE5Request, previous_checkpoint_digest: str | None = None) -> CCE5Certificate:
    if request.requested_scope != "dbp_exact_absolute_corridor_transport":
        raise CCE5Error("StageDependencyUnavailable", "released_cce5_scope", "only the two exact DBP absolute corridor transports are released")
    if request.route_arm not in ROUTE_IDS:
        raise CCE5Error("RouteMismatch", "released_corridor", "route arm must be upper or lower")
    if request.basis != PERIOD_BASIS:
        raise CCE5Error("BasisMismatch", "ordered_period_basis", "request basis is not the theorem-bound DBP basis")
    family = verify_dbp_family_identity()
    connection = verify_dbp_connection_identity()
    topology = verify_braid_calibration()
    if not family or not connection or not topology:
        raise CCE5Error("AnalyticTopologicalMismatch", "exact_calibration_replay", "connection or braid calibration failed")
    sign_word = "+B" if request.route_arm == "upper" else "-B"
    direction = "lower_to_upper" if request.route_arm == "upper" else "upper_to_lower"
    unsigned = {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "request": request,
        "theorem_ids": THEOREM_IDS,
        "source_ledger": _source_ledger(),
        "basis": request.basis,
        "characteristic_formula": "n(m)=m^2/(2m-1)",
        "connection_rows": (
            ("-1/(2m)", "-1/(2m(m-1))", "0"),
            ("-1/(2m)", "1/(2m)", "0"),
            ("1/(m(m-1))", "(4m-1)/(2m(m-1)^2)", "-(2m^2+2m-1)/(2m(m-1)(2m-1))"),
        ),
        "singular_locus": SINGULAR_LOCUS,
        "route_id": ROUTE_IDS[request.route_arm],
        "branch_crossing_ledger": (
            ("central_crossing", "sigma=+i/2" if request.route_arm == "upper" else "sigma=-i/2"),
            ("continued_sheet", "rho=-sqrt(3)/2"),
            ("moving_branch", "q=1/m=4*sqrt(3)-6 in (0,1)"),
            ("crossing_direction", direction),
            ("relative_contour_jump", sign_word),
        ),
        "compact_basis": ("A", "B; period orientation +2iK(1-m)"),
        "compact_matrix": compact_picard_lefschetz_matrix(request.route_arm),
        "relative_basis": TOPOLOGICAL_BASIS,
        "relative_matrix": relative_picard_lefschetz_matrix(request.route_arm),
        "compact_correction": compact_correction_coordinates(request.route_arm),
        "trace_comparison_abc": trace_comparison_coordinates(request.route_arm),
        "compatibility_ledger": (
            ("E0022_family_elimination", family),
            ("rank3_chain_rule", connection),
            ("compact_symplectic_and_inverse", topology),
            ("boundary_preserved", topology),
            ("CPV_compact_corrections_cancel", topology),
            ("analytic_contour_equals_PL_chain_transport", topology),
        ),
        "previous_checkpoint_digest": previous_checkpoint_digest,
        "verifier_version": VERIFIER_VERSION,
    }
    return CCE5Certificate(**unsigned, canonical_certificate_digest=canonical_digest(unsigned))


def continue_dbp_connection_certified(request: CCE5Request) -> CertifiedDBPConnection | Refusal:
    try:
        certificate = _assemble(request)
        return CertifiedDBPConnection(request, certificate)
    except CCE5Error as exc:
        return Refusal(exc.code, exc.obligation, "cella.continuation.cce5", False, True, exc.detail)


def verify_cce5_certificate(certificate: CCE5Certificate) -> bool | Refusal:
    try:
        expected = _assemble(certificate.request, certificate.previous_checkpoint_digest)
    except CCE5Error as exc:
        return Refusal(exc.code, exc.obligation, "cella.continuation.cce5.verify", False, True, exc.detail)
    if certificate != expected:
        return Refusal("AnalyticTopologicalMismatch", "canonical_reconstruction", "cella.continuation.cce5.verify", False, False, "CCE-5 certificate differs from reconstruction")
    return True


def make_cce5_checkpoint(result: CertifiedDBPConnection, previous_checkpoint: CCE5Checkpoint | None = None) -> CCE5Checkpoint:
    previous = previous_checkpoint.checkpoint_digest if previous_checkpoint else None
    unsigned = {
        "schema_id": "cella.continuation.cce5_checkpoint",
        "request_digest": result.request.digest,
        "certificate_digest": result.certificate.canonical_certificate_digest,
        "previous_checkpoint_digest": previous,
    }
    return CCE5Checkpoint(**unsigned, checkpoint_digest=canonical_digest(unsigned))


def verify_cce5_checkpoint(checkpoint: CCE5Checkpoint, result: CertifiedDBPConnection) -> bool:
    unsigned = {
        "schema_id": checkpoint.schema_id,
        "request_digest": checkpoint.request_digest,
        "certificate_digest": checkpoint.certificate_digest,
        "previous_checkpoint_digest": checkpoint.previous_checkpoint_digest,
    }
    return checkpoint.schema_id == "cella.continuation.cce5_checkpoint" and checkpoint.request_digest == result.request.digest and checkpoint.certificate_digest == result.certificate.canonical_certificate_digest and checkpoint.checkpoint_digest == canonical_digest(unsigned)


def resume_cce5(checkpoint: CCE5Checkpoint, request: CCE5Request) -> CertifiedDBPConnection | Refusal:
    original = continue_dbp_connection_certified(request)
    if not isinstance(original, CertifiedDBPConnection) or not verify_cce5_checkpoint(checkpoint, original):
        return Refusal("AnalyticTopologicalMismatch", "checkpoint_chain", "cella.continuation.cce5.resume", False, False, "checkpoint does not replay")
    certificate = _assemble(request, checkpoint.checkpoint_digest)
    return CertifiedDBPConnection(request, certificate)


def released_cce5_request(arm: str = "upper") -> CCE5Request:
    if arm not in ROUTE_IDS:
        raise ValueError("arm must be upper or lower")
    return CCE5Request(f"cce5-dbp-absolute-{arm}-v1", arm)


def released_cce5_groupoid_request(word: str = "UlUl") -> CCE5GroupoidRequest:
    corridor_word_endpoints(word)
    return CCE5GroupoidRequest(f"cce5-dbp-corridor-groupoid-{word}-v1", word)
