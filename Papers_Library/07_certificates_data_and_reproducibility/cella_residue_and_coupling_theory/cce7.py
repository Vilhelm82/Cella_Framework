"""CCE-7 exact labelled-root continuation on rational static-chamber routes."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import comb, gcd, lcm
from pathlib import Path

from cella.pathfinder.scout.sturm import sturm_root_count

from .canonical import canonical_digest, canonical_json_bytes
from .model import Refusal


SCHEMA_ID = "cella.continuation.cce7_static_cover_certificate"
SCHEMA_VERSION = "1.0"
VERIFIER_VERSION = "cella.continuation.cce7.verifier.v1"
ADAPTER_ID = "cella.continuation.static_horizon_cover_v1"
ROUTE_ID = "r5_static_m4_segment_12_to_13_v1"
PAPER_IV_DIGEST = "777daf7b60d337709587606f0974f8d4c8ff9c79473b609aadd54827223613ce"
R5_DIGEST = "945a58cfacabb911d8864c94bb2457bf2bf414cc7c972d4588421e8e45afd5dd"
R5_AUDIT_DIGEST = "dbeabfe02f2d4bccb2803c345ec50716ca7c26f54ce3eee624bf4639ad3f7b97"
STURM_DIGEST = "8f189602515bc38afe71165fce7d22859446a8e21dc13c86461382ba9f715b63"
REAL_PROVIDER_DIGEST = "d1d849e07f84c3ddd46def707d2c5312e4dcb51035f4ec7f287e87ce086a8e69"
COVER_PROVIDER_DIGEST = "9c7b0808ed1ba29a67cc39d6c95957cda3bb207918850fb04334108e75d4993d"
WREATH_PROVIDER_DIGEST = "71179b53e772938375abbb077c587acf86ead6e506d9aea25a3fe39776168fce"
ROOT_LABELS = ("physical", "shadow_N1", "shadow_N2", "shadow_N3", "shadow_N4")
CHARGES = (1, 2, 3, 4)
M4_NODES = tuple(Fraction(96 + index, 8) for index in range(9))


def _sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sources() -> tuple[tuple[str, Path, str], ...]:
    root = Path(__file__).parents[4]
    return (
        ("paper_iv", root / "research/paper/Theorems/DBP/galois_horizon_cover_v1_0.tex", PAPER_IV_DIGEST),
        ("r5_selection", root / "docs/files/LOG_ENTRY_R5_total_reality_v2.md", R5_DIGEST),
        ("r5_audit", root / "docs/files/AUDIT_REPORT_R5_TOTAL_REALITY_AND_LEDGER_v0_2.md", R5_AUDIT_DIGEST),
        ("sturm", root / "engine/src/cella/pathfinder/scout/sturm.py", STURM_DIGEST),
        ("real_provider", root / "engine/src/cella/pathfinder/recognize/real.py", REAL_PROVIDER_DIGEST),
        ("cover_provider", root / "engine/src/cella/pathfinder/recognize/cover.py", COVER_PROVIDER_DIGEST),
        ("wreath_provider", root / "engine/src/cella/pathfinder/recognize/wreath.py", WREATH_PROVIDER_DIGEST),
    )


def _source_ledger() -> tuple[tuple[str, str], ...]:
    ledger = []
    for name, path, expected in _sources():
        if not path.is_file() or _sha256(path) != expected:
            raise CoverError("AlgebraicCoverUnsupported", "source_lock", f"{name} source does not match its frozen digest")
        ledger.append((name, expected))
    return tuple(ledger)


def _trim(poly: list[Fraction]) -> list[Fraction]:
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def _add(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0)] * max(len(left), len(right))
    for index, value in enumerate(left):
        out[index] += value
    for index, value in enumerate(right):
        out[index] += value
    return _trim(out)


def _sub(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0)] * max(len(left), len(right))
    for index, value in enumerate(left):
        out[index] += value
    for index, value in enumerate(right):
        out[index] -= value
    return _trim(out)


def _mul(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    if not left or not right:
        return []
    out = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return _trim(out)


def _scale(poly: list[Fraction], scalar: Fraction) -> list[Fraction]:
    return _trim([scalar * value for value in poly])


def _binary_trim(poly: list[list[Fraction]]) -> list[list[Fraction]]:
    while poly and not poly[-1]:
        poly.pop()
    return poly


def _binary_mul(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    if not left or not right:
        return []
    out = [[] for _ in range(len(left) + len(right) - 1)]
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            if a and b:
                out[i + j] = _add(out[i + j], _mul(a, b))
    return _binary_trim(out)


def _binary_sub(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    length = max(len(left), len(right))
    return _binary_trim([_sub(left[i] if i < len(left) else [], right[i] if i < len(right) else []) for i in range(length)])


def _binary_mul_upoly(poly: list[list[Fraction]], factor: list[Fraction]) -> list[list[Fraction]]:
    return _binary_trim([_mul(coefficient, factor) if coefficient else [] for coefficient in poly])


def _norm_step(poly: list[list[Fraction]], charge_squared: Fraction) -> list[list[Fraction]]:
    wsq = [Fraction(charge_squared), Fraction(1)]
    degree = len(poly) - 1
    powers = [[Fraction(1)]]
    for _ in range(degree // 2 + 1):
        powers.append(_mul(powers[-1], wsq))
    even = [[] for _ in range(degree + 1)]
    odd = [[] for _ in range(degree + 1)]
    for j, coefficient in enumerate(poly):
        if not coefficient:
            continue
        for exponent in range(j + 1):
            term = _scale(coefficient, Fraction(comb(j, exponent)))
            half, parity = divmod(exponent, 2)
            if half:
                term = _mul(term, powers[half])
            target = even if parity == 0 else odd
            target[j - exponent] = _add(target[j - exponent], term)
    return _binary_sub(
        _binary_mul(_binary_trim(even), _binary_trim(even)),
        _binary_mul_upoly(_binary_mul(_binary_trim(odd), _binary_trim(odd)), wsq),
    )


def _primitive_integer(poly: list[Fraction]) -> tuple[Fraction, ...]:
    denominator = 1
    for value in poly:
        denominator = lcm(denominator, value.denominator)
    integers = [int(value * denominator) for value in poly]
    content = 0
    for value in integers:
        content = gcd(content, abs(value))
    integers = [value // content for value in integers]
    if integers[-1] < 0:
        integers = [-value for value in integers]
    return tuple(Fraction(value) for value in integers)


def norm_quintic(m4: Fraction, charges: tuple[Fraction, Fraction, Fraction, Fraction] = CHARGES) -> tuple[Fraction, ...]:
    """Exact N4(u) by four successive quadratic conjugate norms."""
    poly: list[list[Fraction]] = [[], [Fraction(1)]]
    for charge in charges:
        poly = _norm_step(poly, charge * charge)
    out: list[Fraction] = []
    power_m4 = Fraction(1)
    for coefficient in poly:
        if coefficient:
            out = _add(out, _scale(coefficient, power_m4))
        power_m4 *= m4
    result = _primitive_integer(out)
    if len(result) != 6:
        raise CoverError("AlgebraicCoverUnsupported", "degree_five_norm", "the released specialization did not produce a quintic")
    return result


def _evaluate(poly: tuple[Fraction, ...], point: Fraction) -> Fraction:
    value = Fraction(0)
    for coefficient in reversed(poly):
        value = value * point + coefficient
    return value


def _split_nonroot(poly: tuple[Fraction, ...], lower: Fraction, upper: Fraction) -> Fraction:
    for denominator in range(2, 18):
        split = lower + (upper - lower) / denominator
        if _evaluate(poly, split) != 0:
            return split
    raise CoverError("RootIsolationAmbiguous", "rational_split", "could not choose a non-root rational split")


def _positive_isolators(poly: tuple[Fraction, ...]) -> tuple[tuple[Fraction, Fraction], ...]:
    """Exact adaptive Sturm isolators with a Cauchy positive-root bound."""
    leading = abs(poly[-1])
    bound = 1 + max(abs(value) / leading for value in poly[:-1])
    upper = Fraction(bound.numerator // bound.denominator + (bound.denominator != 1) + 1)
    if sturm_root_count(poly, Fraction(0), upper) != 5 or sturm_root_count(poly, Fraction(0), None) != 5:
        raise CoverError("RootIsolationAmbiguous", "five_positive_simple_roots", "the exact quintic did not have five positive roots")
    queue = [(Fraction(0), upper, 5, 0)]
    isolators = []
    while queue:
        lower, high, count, depth = queue.pop()
        if depth > 256:
            raise CoverError("RootIsolationAmbiguous", "adaptive_sturm_depth", "adaptive isolation did not terminate")
        if count == 1:
            # Narrow singleton intervals so adjacent-node overlap matching is
            # effective even on long strict-chamber routes.
            for _ in range(12):
                split = _split_nonroot(poly, lower, high)
                left_count = sturm_root_count(poly, lower, split)
                if left_count == 1:
                    high = split
                else:
                    lower = split
            isolators.append((lower, high))
            continue
        split = _split_nonroot(poly, lower, high)
        left_count = sturm_root_count(poly, lower, split)
        right_count = sturm_root_count(poly, split, high)
        if left_count + right_count != count:
            raise CoverError("RootIsolationAmbiguous", "sturm_partition", "root count failed to partition")
        if right_count:
            queue.append((split, high, right_count, depth + 1))
        if left_count:
            queue.append((lower, split, left_count, depth + 1))
    isolators.sort()
    if len(isolators) != 5:
        raise CoverError("RootIsolationAmbiguous", "five_singleton_isolators", "adaptive isolation did not return five intervals")
    return tuple(isolators)


def _root_labels(charges: tuple[Fraction, Fraction, Fraction, Fraction]) -> tuple[str, ...]:
    """R5d orders shadows by increasing charge magnitude."""
    ordered = sorted(range(4), key=lambda index: charges[index] * charges[index])
    return ("physical", *(f"shadow_N{index + 1}" for index in ordered))


@dataclass(frozen=True, slots=True)
class CCE7Request:
    request_id: str
    route_id: str = ROUTE_ID
    charges: tuple[int, int, int, int] = CHARGES
    m4_nodes: tuple[Fraction, ...] = M4_NODES
    requested_scope: str = "static_strict_chamber_labelled_roots"
    physical_selection: str = "R5c_unique_least_root"

    def __post_init__(self) -> None:
        object.__setattr__(self, "charges", tuple(self.charges))
        object.__setattr__(self, "m4_nodes", tuple(Fraction(value) for value in self.m4_nodes))

    @property
    def digest(self) -> str:
        return canonical_digest(self)


@dataclass(frozen=True, slots=True)
class CoverNode:
    m4: Fraction
    strict_chamber_margin: Fraction
    polynomial: tuple[Fraction, ...]
    isolators: tuple[tuple[Fraction, Fraction], ...]
    node_digest: str


@dataclass(frozen=True, slots=True)
class CCE7Certificate:
    schema_id: str
    schema_version: str
    request: CCE7Request
    source_ledger: tuple[tuple[str, str], ...]
    theorem_ledger: tuple[str, ...]
    nodes: tuple[CoverNode, ...]
    overlap_ledger: tuple[tuple[int, int, str, Fraction, Fraction], ...]
    root_labels: tuple[str, ...]
    terminal_permutation: tuple[int, ...]
    inertia_ledger: tuple[tuple[str, str], ...]
    kummer_sign_ledger: tuple[tuple[str, str], ...]
    physical_selection_ledger: tuple[tuple[str, str], ...]
    pathfinder_ledger: tuple[tuple[str, str], ...]
    previous_checkpoint_digest: str | None
    verifier_version: str
    canonical_certificate_digest: str


@dataclass(frozen=True, slots=True)
class CertifiedCoverResult:
    request: CCE7Request
    certificate: CCE7Certificate


@dataclass(frozen=True, slots=True)
class CCE7Checkpoint:
    schema_id: str
    request_digest: str
    certificate_digest: str
    certified_node_count: int
    remaining_nodes_digest: str
    previous_checkpoint_digest: str | None
    checkpoint_digest: str


class CoverError(ValueError):
    def __init__(self, code: str, obligation: str, detail: str) -> None:
        super().__init__(detail)
        self.code, self.obligation, self.detail = code, obligation, detail


@dataclass(frozen=True, slots=True)
class StaticChamberPoint:
    """One exact point (4M,N1,N2,N3,N4) of the static chamber."""

    m4: Fraction
    charges: tuple[Fraction, Fraction, Fraction, Fraction]

    def __post_init__(self) -> None:
        values = (self.m4, *self.charges)
        if any(isinstance(value, bool) or not isinstance(value, (int, Fraction)) for value in values):
            raise TypeError("static chamber points require exact int/Fraction coordinates")
        object.__setattr__(self, "m4", Fraction(self.m4))
        object.__setattr__(self, "charges", tuple(Fraction(value) for value in self.charges))

    @property
    def margin(self) -> Fraction:
        return self.m4 - sum(abs(charge) for charge in self.charges)


@dataclass(frozen=True, slots=True)
class CCE7ChamberRequest:
    request_id: str
    route_id: str
    points: tuple[StaticChamberPoint, ...]
    requested_scope: str = "full_static_strict_chamber_polygonal_route"
    physical_selection: str = "R5c_unique_least_root"

    def __post_init__(self) -> None:
        if not self.request_id or not self.route_id or len(self.points) < 2:
            raise ValueError("full chamber request needs ids and at least two points")
        object.__setattr__(self, "points", tuple(self.points))

    @property
    def digest(self) -> str:
        return canonical_digest(self)


@dataclass(frozen=True, slots=True)
class ChamberCoverNode:
    point: StaticChamberPoint
    polynomial: tuple[Fraction, ...]
    isolators: tuple[tuple[Fraction, Fraction], ...]
    node_digest: str


@dataclass(frozen=True, slots=True)
class CCE7ChamberCertificate:
    schema_id: str
    schema_version: str
    request: CCE7ChamberRequest
    source_ledger: tuple[tuple[str, str], ...]
    theorem_ledger: tuple[str, ...]
    nodes: tuple[ChamberCoverNode, ...]
    segment_ledger: tuple[tuple[int, Fraction, str], ...]
    charge_zero_crossings: tuple[tuple[int, int, Fraction], ...]
    root_labels: tuple[str, ...]
    terminal_permutation: tuple[int, ...]
    verifier_version: str
    canonical_certificate_digest: str


@dataclass(frozen=True, slots=True)
class CertifiedChamberCoverResult:
    request: CCE7ChamberRequest
    certificate: CCE7ChamberCertificate


@dataclass(frozen=True, slots=True)
class StaticWallEvent:
    point: StaticChamberPoint
    event_kind: str
    zero_root_multiplicity: int
    colliding_labels: tuple[str, ...]
    positive_root_count: int
    polynomial: tuple[Fraction, ...]
    event_digest: str


def classify_static_wall(point: StaticChamberPoint) -> StaticWallEvent | Refusal:
    """Classify the exact chamber boundary m4=sum|Ni| under H2."""
    try:
        if point.margin != 0:
            raise CoverError("UnprovedWallCrossing", "static_boundary_equality", "point is not on the static chamber boundary")
        if len({charge * charge for charge in point.charges}) != 4:
            raise CoverError("RootIsolationAmbiguous", "R5d_boundary_H2", "boundary point violates distinct squared charges")
        polynomial = norm_quintic(point.m4, point.charges)
        multiplicity = 0
        for coefficient in polynomial:
            if coefficient:
                break
            multiplicity += 1
        zero_indices = tuple(index for index, charge in enumerate(point.charges) if charge == 0)
        # H2 keeps the degree-five norm root simple even when a zero-charge
        # sign flip makes two signed sheets represent the same contact.
        expected = 1
        if multiplicity != expected:
            raise CoverError("RootIsolationAmbiguous", "boundary_zero_multiplicity", "exact norm polynomial disagrees with the R5 boundary collision type")
        positive_count = sturm_root_count(polynomial[multiplicity:], Fraction(0), None)
        if positive_count != 5 - multiplicity:
            raise CoverError("RootIsolationAmbiguous", "boundary_positive_roots", "remaining boundary roots were not positive and simple")
        event_kind = "physical_zero_charge_sheet_coincidence" if zero_indices else "physical_simple_contact"
        labels = ("physical", *(f"shadow_N{index + 1}" for index in zero_indices))
        unsigned = {
            "point": point,
            "event_kind": event_kind,
            "zero_root_multiplicity": multiplicity,
            "colliding_labels": labels,
            "positive_root_count": positive_count,
            "polynomial": polynomial,
        }
        return StaticWallEvent(**unsigned, event_digest=canonical_digest(unsigned))
    except CoverError as error:
        return Refusal(error.code, error.obligation, "cella.continuation.cce7.static_wall", False, True, error.detail)


def _admit_chamber_segment(left: StaticChamberPoint, right: StaticChamberPoint, index: int) -> tuple[int, Fraction, str]:
    # m4(t)-sum|Ni(t)| is concave, so its minimum on an interval is at an endpoint.
    minimum_margin = min(left.margin, right.margin)
    if minimum_margin <= 0:
        raise CoverError("UnprovedWallCrossing", "strict_chamber_polygon", f"segment {index} leaves the strict chamber")
    witnesses = []
    for i in range(4):
        for j in range(i + 1, 4):
            for sign in (-1, 1):
                left_factor = left.charges[i] + sign * left.charges[j]
                right_factor = right.charges[i] + sign * right.charges[j]
                if left_factor * right_factor <= 0:
                    raise CoverError("RootIsolationAmbiguous", "R5d_segment_H2", f"segment {index} meets N{i + 1}^2=N{j + 1}^2")
                witnesses.append((i, j, sign, left_factor, right_factor))
    return index, minimum_margin, canonical_digest(tuple(witnesses))


def _assemble_chamber(request: CCE7ChamberRequest) -> CCE7ChamberCertificate:
    if request.requested_scope != "full_static_strict_chamber_polygonal_route" or request.physical_selection != "R5c_unique_least_root":
        raise CoverError("PhysicalSelectionUnproved", "full_static_chamber_scope", "request exceeds the R5c/R5d static chamber")
    segments = tuple(_admit_chamber_segment(left, right, index) for index, (left, right) in enumerate(zip(request.points, request.points[1:])))
    initial_order = tuple(sorted(range(4), key=lambda index: request.points[0].charges[index] ** 2))
    for point in request.points:
        if point.margin <= 0 or len({charge * charge for charge in point.charges}) != 4:
            raise CoverError("RootIsolationAmbiguous", "strict_chamber_H2_nodes", "route node violates the strict chamber or H2")
        if tuple(sorted(range(4), key=lambda index: point.charges[index] ** 2)) != initial_order:
            raise CoverError("RootPermutationMismatch", "R5d_shadow_order", "shadow magnitude order changed without a certified wall")
    nodes = []
    for point in request.points:
        polynomial = norm_quintic(point.m4, point.charges)
        isolators = _positive_isolators(polynomial)
        unsigned_node = {"point": point, "polynomial": polynomial, "isolators": isolators}
        nodes.append(ChamberCoverNode(**unsigned_node, node_digest=canonical_digest(unsigned_node)))
    zero_crossings = []
    for edge, (left, right) in enumerate(zip(request.points, request.points[1:])):
        for charge_index, (a, b) in enumerate(zip(left.charges, right.charges)):
            if a == 0:
                zero_crossings.append((edge, charge_index, Fraction(0)))
            elif b == 0:
                zero_crossings.append((edge, charge_index, Fraction(1)))
            elif a * b < 0:
                zero_crossings.append((edge, charge_index, -a / (b - a)))
    root_labels = ("physical", *(f"shadow_N{index + 1}" for index in initial_order))
    unsigned = {
        "schema_id": "cella.continuation.cce7_full_static_chamber_certificate",
        "schema_version": "1.0",
        "request": request,
        "source_ledger": _source_ledger(),
        "theorem_ledger": (
            "R5b:five-positive-roots-throughout-strict-chamber",
            "R5c-1:physical-root-unique-least",
            "R5d:H2-global-simplicity-and-charge-magnitude-ordering",
            "exact-concavity:polygonal-strict-chamber-admission",
        ),
        "nodes": tuple(nodes),
        "segment_ledger": segments,
        "charge_zero_crossings": tuple(zero_crossings),
        "root_labels": root_labels,
        "terminal_permutation": (0, 1, 2, 3, 4),
        "verifier_version": "cella.continuation.cce7.full_chamber.verifier.v1",
    }
    return CCE7ChamberCertificate(**unsigned, canonical_certificate_digest=canonical_digest(unsigned))


def continue_static_chamber_certified(request: CCE7ChamberRequest) -> CertifiedChamberCoverResult | Refusal:
    try:
        return CertifiedChamberCoverResult(request, _assemble_chamber(request))
    except CoverError as error:
        return Refusal(error.code, error.obligation, "cella.continuation.cce7.full_chamber", False, True, error.detail)


def verify_cce7_chamber_certificate(certificate: CCE7ChamberCertificate) -> bool | Refusal:
    try:
        expected = _assemble_chamber(certificate.request)
    except CoverError as error:
        return Refusal(error.code, error.obligation, "cella.continuation.cce7.full_chamber.verify", False, True, error.detail)
    if canonical_json_bytes(expected) != canonical_json_bytes(certificate):
        return Refusal("RootPermutationMismatch", "exact_full_chamber_replay", "cella.continuation.cce7.full_chamber.verify", False, False, "full chamber certificate bytes do not replay")
    return True


def _node(m4: Fraction, charges: tuple[int, int, int, int]) -> CoverNode:
    margin = m4 - sum(abs(charge) for charge in charges)
    if margin <= 0:
        raise CoverError("UnprovedWallCrossing", "strict_chamber_margin", "route leaves 4M>sum|N_i|")
    polynomial = norm_quintic(m4, charges)
    isolators = _positive_isolators(polynomial)
    unsigned = {"m4": m4, "strict_chamber_margin": margin, "polynomial": polynomial, "isolators": isolators}
    return CoverNode(**unsigned, node_digest=canonical_digest(unsigned))


def _assemble(request: CCE7Request, previous_checkpoint_digest: str | None = None) -> CCE7Certificate:
    if not request.route_id or len(request.m4_nodes) < 2:
        raise CoverError("AlgebraicCoverUnsupported", "exact_static_route", "an exact route id and at least two rational nodes are required")
    if request.requested_scope != "static_strict_chamber_labelled_roots" or request.physical_selection != "R5c_unique_least_root":
        raise CoverError("PhysicalSelectionUnproved", "static_selection_scope", "request exceeds R5c/R5d static strict-chamber scope")
    if len(request.charges) != 4 or any(isinstance(charge, bool) or not isinstance(charge, int) for charge in request.charges):
        raise CoverError("AlgebraicCoverUnsupported", "four_integral_charges", "exactly four integral charges are required")
    if len({charge * charge for charge in request.charges}) != 4:
        raise CoverError("RootIsolationAmbiguous", "R5d_distinct_squared_charges", "R5d simplicity requires distinct squared charges")
    root_labels = _root_labels(request.charges)
    sources = _source_ledger()
    cache: dict[Fraction, CoverNode] = {}
    def node(m4: Fraction) -> CoverNode:
        if m4 not in cache:
            cache[m4] = _node(m4, request.charges)
        return cache[m4]

    def shared(left: CoverNode, right: CoverNode) -> tuple[tuple[str, Fraction, Fraction], ...] | None:
        out = []
        for label_index, label in enumerate(root_labels):
            lower = min(left.isolators[label_index][0], right.isolators[label_index][0])
            upper = max(left.isolators[label_index][1], right.isolators[label_index][1])
            if sturm_root_count(left.polynomial, lower, upper) != 1 or sturm_root_count(right.polynomial, lower, upper) != 1:
                return None
            out.append((label, lower, upper))
        return tuple(out)

    def refine(left_m4: Fraction, right_m4: Fraction, depth: int = 0) -> list[CoverNode]:
        left, right = node(left_m4), node(right_m4)
        if shared(left, right) is not None:
            return [left, right]
        if depth >= 32:
            raise CoverError("RootIsolationAmbiguous", "adaptive_route_overlap", "exact route subdivision did not obtain singleton overlaps")
        middle = (left_m4 + right_m4) / 2
        return refine(left_m4, middle, depth + 1)[:-1] + refine(middle, right_m4, depth + 1)

    expanded: list[CoverNode] = []
    for left_m4, right_m4 in zip(request.m4_nodes, request.m4_nodes[1:]):
        segment = refine(left_m4, right_m4)
        expanded.extend(segment if not expanded else segment[1:])
    nodes = tuple(expanded)
    overlaps = []
    for index, (left, right) in enumerate(zip(nodes, nodes[1:])):
        witnesses = shared(left, right)
        if witnesses is None:
            raise CoverError("RootIsolationAmbiguous", "adjacent_overlap", "adaptively refined nodes lack exact overlaps")
        for label, lower, upper in witnesses:
            overlaps.append((index, index + 1, label, lower, upper))
    unsigned = {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "request": request,
        "source_ledger": sources,
        "theorem_ledger": (
            "PaperIV:exact-four-charge-norm-quintic",
            "R5b:five-positive-mass-square-roots",
            "R5c-1:physical-root-unique-least",
            "R5d:global-simplicity-and-shadow-ordering-under-H2",
        ),
        "nodes": nodes,
        "overlap_ledger": tuple(overlaps),
        "root_labels": root_labels,
        "terminal_permutation": (0, 1, 2, 3, 4),
        "inertia_ledger": (("discriminant_crossings", "0"), ("oriented_inertia", "identity"), ("reason", "R5d global simplicity on every exact segment inside the strict chamber")),
        "kummer_sign_ledger": (("charge_signs", ",".join("+" if charge > 0 else "-" if charge < 0 else "0" for charge in request.charges)), ("deck_parity", "unchanged"), ("wall_crossing", "none")),
        "physical_selection_ledger": (("rule", "unique least root"), ("initial_label", "physical"), ("terminal_label", "physical"), ("nearest_float_used", "false")),
        "pathfinder_ledger": (("route_digest", canonical_digest((request.route_id, request.charges, request.m4_nodes))), ("sturm_source_digest", STURM_DIGEST), ("real_provider_digest", REAL_PROVIDER_DIGEST), ("cover_provider_digest", COVER_PROVIDER_DIGEST), ("wreath_provider_digest", WREATH_PROVIDER_DIGEST)),
        "previous_checkpoint_digest": previous_checkpoint_digest,
        "verifier_version": VERIFIER_VERSION,
    }
    return CCE7Certificate(**unsigned, canonical_certificate_digest=canonical_digest(unsigned))


def continue_static_cover_certified(request: CCE7Request) -> CertifiedCoverResult | Refusal:
    try:
        return CertifiedCoverResult(request, _assemble(request))
    except CoverError as error:
        return Refusal(error.code, error.obligation, "cella.continuation.cce7", False, True, error.detail)


def verify_cce7_certificate(certificate: CCE7Certificate) -> bool | Refusal:
    try:
        expected = _assemble(certificate.request, certificate.previous_checkpoint_digest)
    except CoverError as error:
        return Refusal(error.code, error.obligation, "cella.continuation.cce7.verify", False, True, error.detail)
    if canonical_json_bytes(expected) != canonical_json_bytes(certificate):
        return Refusal("RootPermutationMismatch", "exact_certificate_replay", "cella.continuation.cce7.verify", False, False, "certificate bytes do not replay")
    return True


def released_cce7_request() -> CCE7Request:
    return CCE7Request("cce7-r5-static-m4-12-to-13")


def released_cce7_chamber_request() -> CCE7ChamberRequest:
    return CCE7ChamberRequest(
        "cce7-full-static-polygon-v1",
        "rational-polygon-with-charge-zero-crossing",
        (
            StaticChamberPoint(Fraction(12), (Fraction(1), Fraction(2), Fraction(3), Fraction(4))),
            StaticChamberPoint(Fraction(13), (Fraction(-1), Fraction(2), Fraction(3), Fraction(4))),
            StaticChamberPoint(Fraction(15), (Fraction(-2), Fraction(3), Fraction(4), Fraction(5))),
        ),
    )


def make_cce7_checkpoint(result: CertifiedCoverResult, certified_node_count: int = 5, previous: CCE7Checkpoint | None = None) -> CCE7Checkpoint:
    nodes = result.certificate.nodes
    if not 1 <= certified_node_count <= len(nodes):
        raise ValueError("checkpoint node count outside route")
    unsigned = {
        "schema_id": "cella.continuation.cce7_checkpoint.v1",
        "request_digest": result.request.digest,
        "certificate_digest": result.certificate.canonical_certificate_digest,
        "certified_node_count": certified_node_count,
        "remaining_nodes_digest": canonical_digest(nodes[certified_node_count:]),
        "previous_checkpoint_digest": previous.checkpoint_digest if previous else None,
    }
    return CCE7Checkpoint(**unsigned, checkpoint_digest=canonical_digest(unsigned))


def verify_cce7_checkpoint(checkpoint: CCE7Checkpoint, result: CertifiedCoverResult, previous: CCE7Checkpoint | None = None) -> bool:
    unsigned = {name: getattr(checkpoint, name) for name in ("schema_id", "request_digest", "certificate_digest", "certified_node_count", "remaining_nodes_digest", "previous_checkpoint_digest")}
    return (
        checkpoint.checkpoint_digest == canonical_digest(unsigned)
        and checkpoint.request_digest == result.request.digest
        and checkpoint.certificate_digest == result.certificate.canonical_certificate_digest
        and checkpoint.remaining_nodes_digest == canonical_digest(result.certificate.nodes[checkpoint.certified_node_count:])
        and checkpoint.previous_checkpoint_digest == (previous.checkpoint_digest if previous else None)
    )


def resume_cce7(checkpoint: CCE7Checkpoint, request: CCE7Request) -> CertifiedCoverResult | Refusal:
    fresh = continue_static_cover_certified(request)
    if isinstance(fresh, Refusal) or not verify_cce7_checkpoint(checkpoint, fresh):
        return Refusal("RootPermutationMismatch", "checkpoint_chain", "cella.continuation.cce7.resume", False, False, "checkpoint does not replay")
    try:
        return CertifiedCoverResult(request, _assemble(request, checkpoint.checkpoint_digest))
    except CoverError as error:
        return Refusal(error.code, error.obligation, "cella.continuation.cce7.resume", False, True, error.detail)


__all__ = [
    "CCE7Certificate", "CCE7ChamberCertificate", "CCE7ChamberRequest",
    "CCE7Checkpoint", "CCE7Request", "CertifiedChamberCoverResult",
    "CertifiedCoverResult", "ChamberCoverNode", "CoverNode",
    "StaticChamberPoint", "StaticWallEvent", "classify_static_wall",
    "continue_static_chamber_certified",
    "continue_static_cover_certified", "make_cce7_checkpoint", "norm_quintic",
    "released_cce7_chamber_request", "released_cce7_request", "resume_cce7",
    "verify_cce7_certificate",
    "verify_cce7_chamber_certificate", "verify_cce7_checkpoint",
]
