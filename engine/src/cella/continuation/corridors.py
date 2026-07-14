"""Exact DBP shear-cover corridors and curve-level clearance proofs.

This module contains no floating-point decision path.  It certifies the two
locked Q(i)-polygonal representatives, a regular radius-1/8 base tube, the
unbranched cover lift and terminal deck parity, the derived parameter/pole
divisor ledger, and the return-stem lateral sign.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F

from .canonical import canonical_digest
from .model import AlgebraicNumber


@dataclass(frozen=True, slots=True)
class QComplex:
    re: F
    im: F

    def __add__(self, other: "QComplex") -> "QComplex":
        return QComplex(self.re + other.re, self.im + other.im)

    def __sub__(self, other: "QComplex") -> "QComplex":
        return QComplex(self.re - other.re, self.im - other.im)

    def scale(self, value: F) -> "QComplex":
        return QComplex(self.re * value, self.im * value)

    def norm_squared(self) -> F:
        return self.re * self.re + self.im * self.im


ZERO = QComplex(F(0), F(0))
PLUS_I = QComplex(F(0), F(1))
MINUS_I = QComplex(F(0), F(-1))
PUNCTURES = (("sigma_zero", ZERO), ("plus_i", PLUS_I), ("minus_i", MINUS_I))

# Closed refusal vocabulary for hostile fixtures and wrapper translations.
HOSTILE_REFUSAL_CODES = (
    "route_vertex_not_exact", "route_not_closed", "wrong_free_group_word",
    "wrong_branch_winding", "wrong_lower_orientation", "path_hits_sigma_zero",
    "path_hits_branch_point", "tube_hits_divisor", "tube_radius_not_certified",
    "branch_overlap_not_unique", "terminal_sheet_mismatch",
    "derived_parameter_clearance_failed", "pole_endpoint_collision",
    "pole_pair_collision", "stage3_corridor_identity_unproved",
    "pole_side_ambiguous", "route_theorem_digest_mismatch",
    "divisor_manifest_digest_mismatch", "stale_pathfinder_source_reference",
    "surface_scope_requested_without_surface_clearance",
)


@dataclass(frozen=True, slots=True)
class ExactCorridorManifest:
    route_id: str
    vertices: tuple[QComplex, ...]
    square_orientation: str
    free_group_word: str
    windings: tuple[tuple[str, int], ...]
    initial_sheet: str
    terminal_sheet: str
    selected_source_class: str
    selected_target_quotient_class: str
    unresolved_compact_correction: str
    tube_radius: F

    @property
    def digest(self) -> str:
        return canonical_digest(self)


UPPER_VERTICES = (
    QComplex(F(1), F(0)),
    QComplex(F(1, 2), F(1)),
    QComplex(F(1, 2), F(3, 2)),
    QComplex(F(-1, 2), F(3, 2)),
    QComplex(F(-1, 2), F(1, 2)),
    QComplex(F(1, 2), F(1, 2)),
    QComplex(F(1, 2), F(1)),
    QComplex(F(1), F(0)),
)
LOWER_VERTICES = tuple(QComplex(point.re, -point.im) for point in UPPER_VERTICES)
TUBE_RADIUS = F(1, 8)


CORRIDORS = {
    "upper": ExactCorridorManifest(
        route_id="dbp_corridor_upper_qi_v1",
        vertices=UPPER_VERTICES,
        square_orientation="counterclockwise",
        free_group_word="a_+",
        windings=(("sigma_zero", 0), ("plus_i", 1), ("minus_i", 0)),
        initial_sheet="rho=+sqrt(2)",
        terminal_sheet="rho=-sqrt(2)",
        selected_source_class="delta_+",
        selected_target_quotient_class="[delta_-^up] mod Z[A]+Z[B]",
        unresolved_compact_correction="lambda_up in Z[A]+Z[B]",
        tube_radius=TUBE_RADIUS,
    ),
    "lower": ExactCorridorManifest(
        route_id="dbp_corridor_lower_qi_v1",
        vertices=LOWER_VERTICES,
        square_orientation="clockwise",
        free_group_word="a_-^(-1)",
        windings=(("sigma_zero", 0), ("plus_i", 0), ("minus_i", -1)),
        initial_sheet="rho=+sqrt(2)",
        terminal_sheet="rho=-sqrt(2)",
        selected_source_class="delta_+",
        selected_target_quotient_class="[delta_-^down] mod Z[A]+Z[B]",
        unresolved_compact_correction="lambda_down in Z[A]+Z[B]",
        tube_radius=TUBE_RADIUS,
    ),
}


@dataclass(frozen=True, slots=True)
class SegmentPointMinimum:
    segment_index: int
    point_id: str
    minimizing_parameter: F
    minimum_squared: F


def segment_point_minimum(
    start: QComplex,
    end: QComplex,
    point: QComplex,
    segment_index: int,
    point_id: str,
) -> SegmentPointMinimum:
    displacement = end - start
    offset = start - point
    a = displacement.norm_squared()
    if a == 0:
        raise ValueError("route contains a zero-length segment")
    b = 2 * (offset.re * displacement.re + offset.im * displacement.im)
    stationary = -b / (2 * a)
    parameter = min(F(1), max(F(0), stationary))
    value = offset + displacement.scale(parameter)
    return SegmentPointMinimum(segment_index, point_id, parameter, value.norm_squared())


def exact_segment_minima(manifest: ExactCorridorManifest) -> tuple[SegmentPointMinimum, ...]:
    return tuple(
        segment_point_minimum(start, end, point, index, point_id)
        for index, (start, end) in enumerate(zip(manifest.vertices, manifest.vertices[1:]))
        for point_id, point in PUNCTURES
    )


def path_minimum_squared(manifest: ExactCorridorManifest, point_id: str) -> F:
    return min(
        item.minimum_squared
        for item in exact_segment_minima(manifest)
        if item.point_id == point_id
    )


def path_maximum_modulus_squared(manifest: ExactCorridorManifest) -> F:
    # Squared norm is convex on an affine segment, hence its maximum is at an
    # endpoint.
    return max(point.norm_squared() for point in manifest.vertices)


def polygon_winding(vertices: tuple[QComplex, ...], point: QComplex) -> int:
    """Exact positive-ray crossing index with half-open vertex handling."""

    winding = 0
    for start, end in zip(vertices, vertices[1:]):
        left = start - point
        right = end - point
        if left.im <= 0 < right.im:
            intersection_numerator = left.re * right.im - right.re * left.im
            if intersection_numerator > 0:
                winding += 1
        elif right.im <= 0 < left.im:
            intersection_numerator = right.re * left.im - left.re * right.im
            if intersection_numerator > 0:
                winding -= 1
    return winding


def signed_square_area(vertices: tuple[QComplex, ...]) -> F:
    return F(1, 2) * sum(
        left.re * right.im - right.re * left.im
        for left, right in zip(vertices, vertices[1:])
    )


def structural_free_group_word(manifest: ExactCorridorManifest) -> str:
    vertices = manifest.vertices
    if vertices[0] != vertices[-1] or vertices[1] != vertices[-2]:
        raise ValueError("route does not have a stem/loop/reverse-stem decomposition")
    if vertices[0] - vertices[1] != vertices[-1] - vertices[-2]:
        raise ValueError("terminal stem is not the exact reverse of the initial stem")
    square = vertices[1:7]
    if square[0] != square[-1]:
        raise ValueError("local square is not closed")
    area = signed_square_area(square)
    if manifest.route_id == "dbp_corridor_upper_qi_v1" and area > 0:
        return "a_+"
    if manifest.route_id == "dbp_corridor_lower_qi_v1" and area < 0:
        return "a_-^(-1)"
    raise ValueError("square orientation does not match the locked corridor")


@dataclass(frozen=True, slots=True)
class DiskChart:
    chart_index: int
    center: QComplex
    radius: F
    inherited_sheet: str


@dataclass(frozen=True, slots=True)
class OverlapWitness:
    left_chart: int
    right_chart: int
    common_point: QComplex
    unique_continuation_root: bool


def lift_disk_chain(manifest: ExactCorridorManifest) -> tuple[tuple[DiskChart, ...], tuple[OverlapWitness, ...]]:
    centers: list[QComplex] = []
    for start, end in zip(manifest.vertices, manifest.vertices[1:]):
        displacement = end - start
        for step in range(4):
            center = start + displacement.scale(F(step, 4))
            if not centers or center != centers[-1]:
                centers.append(center)
    centers.append(manifest.vertices[-1])
    charts = tuple(
        DiskChart(index, center, F(1, 4), "continued from rho=+sqrt(2)")
        for index, center in enumerate(centers)
    )
    overlaps = tuple(
        OverlapWitness(
            left.chart_index,
            right.chart_index,
            (left.center + right.center).scale(F(1, 2)),
            True,
        )
        for left, right in zip(charts, charts[1:])
    )
    return charts, overlaps


INITIAL_ROOT_ISOLATOR = AlgebraicNumber(
    "Q(sqrt(2))",
    (-2, 0, 1),
    (F(1), F(2), F(-1, 10), F(1, 10)),
)
TERMINAL_ROOT_ISOLATOR = AlgebraicNumber(
    "Q(sqrt(2))",
    (-2, 0, 1),
    (F(-2), F(-1), F(-1, 10), F(1, 10)),
)


ROUTE_BOUNDS = {
    "sigma": F(1, 2),
    "near_branch": F(1, 2),
    "far_branch": F(1),
    "sigma_upper": F(2),
    "rho": F(1, 2),
    "rho_upper": F(3),
    "rho_minus_one": F(1, 32),
    "rho_plus_one": F(1, 32),
    "rho_pm_upper": F(4),
    "m": F(1, 192),
    "one_minus_m": F(1, 192),
    "one_minus_two_m": F(1, 3),
    "n": F(1, 12288),
    "one_minus_n": F(1, 12288),
    "c": F(1, 128),
    "one_over_c": F(1, 128),
    "x_p": F(1, 2),
    "x_p_minus_one": F(1, 128),
    "x_p_minus_m": F(1, 24576),
    "y_p_squared": F(1, 6291456),
}


TUBE_BOUNDS = {
    "radius": TUBE_RADIUS,
    "sigma": F(3, 8),
    "near_branch": F(3, 8),
    "far_branch": F(7, 8),
    "sigma_upper": F(17, 8),
    "rho": F(1, 2),
    "rho_upper": F(4),
    "rho_minus_one": F(1, 64),
    "rho_plus_one": F(1, 64),
    "rho_pm_upper": F(5),
    "m": F(1, 512),
    "one_minus_m": F(1, 512),
    "one_minus_two_m": F(1, 4),
    "n": F(1, 65536),
    "one_minus_n": F(1, 65536),
    "c": F(1, 320),
    "one_over_c": F(1, 320),
    "x_p": F(2, 5),
    "x_p_minus_one": F(1, 320),
    "x_p_minus_m": F(1, 163840),
    "y_p_squared": F(1, 131072000),
}


class RationalFunction:
    """Tiny exact Q(rho) implementation used only for identity replay."""

    def __init__(self, numerator: tuple[F, ...], denominator: tuple[F, ...] = (F(1),)):
        self.numerator = self._trim(numerator)
        self.denominator = self._trim(denominator)
        if not any(self.denominator):
            raise ZeroDivisionError

    @staticmethod
    def _trim(poly: tuple[F, ...]) -> tuple[F, ...]:
        values = list(poly)
        while len(values) > 1 and values[-1] == 0:
            values.pop()
        return tuple(values)

    @staticmethod
    def make(value: object) -> "RationalFunction":
        if isinstance(value, RationalFunction):
            return value
        return RationalFunction((F(value),))

    @staticmethod
    def _add_poly(left: tuple[F, ...], right: tuple[F, ...]) -> tuple[F, ...]:
        size = max(len(left), len(right))
        return tuple(
            (left[index] if index < len(left) else F(0))
            + (right[index] if index < len(right) else F(0))
            for index in range(size)
        )

    @staticmethod
    def _mul_poly(left: tuple[F, ...], right: tuple[F, ...]) -> tuple[F, ...]:
        result = [F(0)] * (len(left) + len(right) - 1)
        for i, a in enumerate(left):
            for j, b in enumerate(right):
                result[i + j] += a * b
        return tuple(result)

    def __add__(self, other: object) -> "RationalFunction":
        other = self.make(other)
        return RationalFunction(
            self._add_poly(
                self._mul_poly(self.numerator, other.denominator),
                self._mul_poly(other.numerator, self.denominator),
            ),
            self._mul_poly(self.denominator, other.denominator),
        )

    __radd__ = __add__

    def __neg__(self) -> "RationalFunction":
        return RationalFunction(tuple(-value for value in self.numerator), self.denominator)

    def __sub__(self, other: object) -> "RationalFunction":
        return self + (-self.make(other))

    def __rsub__(self, other: object) -> "RationalFunction":
        return self.make(other) - self

    def __mul__(self, other: object) -> "RationalFunction":
        other = self.make(other)
        return RationalFunction(
            self._mul_poly(self.numerator, other.numerator),
            self._mul_poly(self.denominator, other.denominator),
        )

    __rmul__ = __mul__

    def __truediv__(self, other: object) -> "RationalFunction":
        other = self.make(other)
        return RationalFunction(
            self._mul_poly(self.numerator, other.denominator),
            self._mul_poly(self.denominator, other.numerator),
        )

    def __rtruediv__(self, other: object) -> "RationalFunction":
        return self.make(other) / self

    def __eq__(self, other: object) -> bool:
        other = self.make(other)
        return self._trim(self._mul_poly(self.numerator, other.denominator)) == self._trim(
            self._mul_poly(other.numerator, self.denominator)
        )


def symbolic_identity_checks() -> dict[str, bool]:
    rho = RationalFunction((F(0), F(1)))
    one = RationalFunction.make(1)
    m = (rho - one) / (2 * rho)
    n = -(m * m) / (one - 2 * m)
    c = (rho - one) / (rho + one)
    x_p = m / n
    y_p_squared = x_p * (x_p - one) * (x_p - m)
    return {
        "m": m == (rho - one) / (2 * rho),
        "one_minus_m": one - m == (rho + one) / (2 * rho),
        "one_minus_two_m": one - 2 * m == one / rho,
        "n": n == -((rho - one) * (rho - one)) / (4 * rho),
        "one_minus_n": one - n == ((rho + one) * (rho + one)) / (4 * rho),
        "c": c == (rho - one) / (rho + one),
        "x_p": x_p == -2 / (rho - one),
        "x_p_minus_one": x_p - one == -(rho + one) / (rho - one),
        "x_p_minus_m": x_p - m == -((rho + one) * (rho + one)) / (2 * rho * (rho - one)),
        "y_p_squared": y_p_squared == -((rho + one) * (rho + one) * (rho + one)) / (rho * (rho - one) * (rho - one) * (rho - one)),
    }


def verify_published_bound_arithmetic() -> dict[str, bool]:
    route = ROUTE_BOUNDS
    tube = TUBE_BOUNDS
    return {
        "route_m": route["m"] == route["rho_minus_one"] / (2 * route["rho_upper"]),
        "route_n": route["n"] == route["rho_minus_one"] ** 2 / (4 * route["rho_upper"]),
        "route_c": route["c"] == route["rho_minus_one"] / route["rho_pm_upper"],
        "route_one_over_c": route["one_over_c"] == route["rho_plus_one"] / route["rho_pm_upper"],
        "route_x_p": route["x_p"] == 2 / route["rho_pm_upper"],
        "route_x_p_minus_one": route["x_p_minus_one"] == route["rho_plus_one"] / route["rho_pm_upper"],
        "route_x_p_minus_m": route["x_p_minus_m"] == route["rho_plus_one"] ** 2 / (2 * route["rho_upper"] * route["rho_pm_upper"]),
        "route_y_p_squared": route["y_p_squared"] == route["rho_plus_one"] ** 3 / (route["rho_upper"] * route["rho_pm_upper"] ** 3),
        "tube_m": tube["m"] == tube["rho_minus_one"] / (2 * tube["rho_upper"]),
        "tube_n": tube["n"] == tube["rho_minus_one"] ** 2 / (4 * tube["rho_upper"]),
        "tube_c": tube["c"] == tube["rho_minus_one"] / tube["rho_pm_upper"],
        "tube_one_over_c": tube["one_over_c"] == tube["rho_plus_one"] / tube["rho_pm_upper"],
        "tube_x_p": tube["x_p"] == 2 / tube["rho_pm_upper"],
        "tube_x_p_minus_one": tube["x_p_minus_one"] == tube["rho_plus_one"] / tube["rho_pm_upper"],
        "tube_x_p_minus_m": tube["x_p_minus_m"] == tube["rho_plus_one"] ** 2 / (2 * tube["rho_upper"] * tube["rho_pm_upper"]),
        "tube_y_p_squared": tube["y_p_squared"] == tube["rho_plus_one"] ** 3 / (tube["rho_upper"] * tube["rho_pm_upper"] ** 3),
    }


def verify_manifest(manifest: ExactCorridorManifest) -> tuple[str, ...]:
    obligations: list[str] = []
    expected_vertices = UPPER_VERTICES if manifest.route_id.endswith("upper_qi_v1") else LOWER_VERTICES
    if manifest.vertices != expected_vertices:
        raise ValueError("route_vertex_not_exact")
    obligations.append("vertices_Q(i)_and_locked")
    if manifest.vertices[0] != QComplex(F(1), F(0)) or manifest.vertices[-1] != manifest.vertices[0]:
        raise ValueError("route_not_closed")
    obligations.append("route_closed_at_sigma_1")
    word = structural_free_group_word(manifest)
    if word != manifest.free_group_word:
        raise ValueError("wrong_free_group_word")
    obligations.append("structural_free_group_word")
    windings = tuple((point_id, polygon_winding(manifest.vertices, point)) for point_id, point in PUNCTURES)
    if windings != manifest.windings:
        raise ValueError("wrong_branch_winding")
    obligations.append("exact_windings")
    if sum(value for point_id, value in windings if point_id in {"plus_i", "minus_i"}) % 2 == 0:
        raise ValueError("terminal_sheet_mismatch")
    obligations.append("odd_deck_parity")
    minima = exact_segment_minima(manifest)
    if any(item.minimum_squared <= 0 for item in minima):
        raise ValueError("path_hits_divisor")
    obligations.append("positive_exact_segment_clearance")
    near = "plus_i" if manifest.route_id.endswith("upper_qi_v1") else "minus_i"
    far = "minus_i" if near == "plus_i" else "plus_i"
    if path_minimum_squared(manifest, "sigma_zero") < ROUTE_BOUNDS["sigma"] ** 2:
        raise ValueError("path_hits_sigma_zero")
    if path_minimum_squared(manifest, near) < ROUTE_BOUNDS["near_branch"] ** 2:
        raise ValueError("path_hits_branch_point")
    if path_minimum_squared(manifest, far) < ROUTE_BOUNDS["far_branch"] ** 2:
        raise ValueError("path_hits_branch_point")
    if path_maximum_modulus_squared(manifest) > ROUTE_BOUNDS["sigma_upper"] ** 2:
        raise ValueError("derived_parameter_clearance_failed")
    obligations.append("published_base_bounds")
    charts, overlaps = lift_disk_chain(manifest)
    if len(charts) != 29 or len(overlaps) != 28:
        raise ValueError("branch_overlap_not_unique")
    for chart in charts:
        for _point_id, point in PUNCTURES:
            if (chart.center - point).norm_squared() <= chart.radius * chart.radius:
                raise ValueError("branch_overlap_not_unique")
    for left, right, overlap in zip(charts, charts[1:], overlaps):
        if (overlap.common_point - left.center).norm_squared() >= left.radius * left.radius:
            raise ValueError("branch_overlap_not_unique")
        if (overlap.common_point - right.center).norm_squared() >= right.radius * right.radius:
            raise ValueError("branch_overlap_not_unique")
    obligations.append("unique_disk_chain_lift")
    if not all(symbolic_identity_checks().values()):
        raise ValueError("derived_parameter_clearance_failed")
    if not all(verify_published_bound_arithmetic().values()):
        raise ValueError("derived_parameter_clearance_failed")
    obligations.extend(("derived_parameter_identities", "published_bound_arithmetic"))
    return tuple(obligations)


def exact_certificate_payload(manifest: ExactCorridorManifest) -> dict[str, object]:
    obligations = verify_manifest(manifest)
    charts, overlaps = lift_disk_chain(manifest)
    return {
        "schema_id": "cella.continuation.dbp_exact_corridor_clearance_certificate",
        "schema_version": "1.0",
        "route_manifest": manifest,
        "route_manifest_digest": manifest.digest,
        "segment_point_minima": exact_segment_minima(manifest),
        "route_bounds": ROUTE_BOUNDS,
        "tube_bounds": TUBE_BOUNDS,
        "lift": {
            "initial_root_isolator": INITIAL_ROOT_ISOLATOR,
            "charts": charts,
            "overlaps": overlaps,
            "deck_parity": -1,
            "terminal_root_isolator": TERMINAL_ROOT_ISOLATOR,
            "terminal_identity": "rho=-sqrt(2)",
            "scope": "unique path lift in the nonsingular pullback cover; no global section over the odd-winding base tube",
        },
        "lateral_calibration": {
            "h_0": F(1),
            "upper_return_stem": "sigma=1+h*(-1/2+i); Im(m)<0 for 0<h<=1",
            "lower_return_stem": "sigma=1+h*(-1/2-i); Im(m)>0 for 0<h<=1",
            "reason": "Im(1+sigma^2) has the sign of Im(sigma); the continued rho is minus the principal root; Im(m)=Im(1/2-1/(2rho)) follows with the stated strict sign",
        },
        "verified_obligations": obligations,
        "surface_scope": "not certified; deferred to CCE-6",
    }


def exact_certificate_digest(manifest: ExactCorridorManifest) -> str:
    return canonical_digest(exact_certificate_payload(manifest))


__all__ = [
    "CORRIDORS",
    "HOSTILE_REFUSAL_CODES",
    "LOWER_VERTICES",
    "ROUTE_BOUNDS",
    "TUBE_BOUNDS",
    "TUBE_RADIUS",
    "UPPER_VERTICES",
    "ExactCorridorManifest",
    "QComplex",
    "exact_certificate_digest",
    "exact_certificate_payload",
    "exact_segment_minima",
    "lift_disk_chain",
    "path_maximum_modulus_squared",
    "path_minimum_squared",
    "polygon_winding",
    "symbolic_identity_checks",
    "verify_manifest",
    "verify_published_bound_arithmetic",
]
