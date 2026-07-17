"""Exact independent R3 realization: the lossless two-bus AC fold cover."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
from pathlib import Path

from .canonical import canonical_digest, canonical_json_bytes
from .model import Refusal
from .selected_skeleton import SelectedSkeletonMorphism, SelectedSkeletonObject


SCHEMA_ID = "cella.continuation.r3_ac_fold_certificate"
SCHEMA_VERSION = "1.0"
VERIFIER_VERSION = "cella.continuation.r3_ac_fold.verifier.v1"
THEOREM_IDS = (
    "R3-AC.1:lossless-two-bus-quadratic-cover",
    "R3-AC.2:positive-discriminant-two-sheet-chamber",
    "R3-AC.3:no-load-high-voltage-selection",
    "R3-AC.4:discriminant-loop-c2-monodromy",
    "R3-AC.5:selected-skeleton-reduction",
)
SHEETS = ("high", "low")


def _q(value: int | Fraction) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError("AC-fold parameters require exact int/Fraction entries")
    return Fraction(value)


def _source_ledger() -> tuple[tuple[str, str], ...]:
    import hashlib

    root = Path(__file__).parents[4]
    paths = (
        ("r3_runtime", Path(__file__)),
        ("selected_skeleton_runtime", Path(__file__).with_name("selected_skeleton.py")),
        ("ensemble_architecture", root / "research/paper/Theorems/DBP/DBP_PAPER_ENSEMBLE_ARCHITECTURE_v1.0.md"),
        ("hostile_precommit", root / "research/campaigns/CELLA_CONTINUATION_ENGINE/10_post8_universalization/R3_AC_FOLD_PRECOMMITTED_HOSTILE_FIXTURE_v1.0.md"),
    )
    return tuple((name, hashlib.sha256(path.read_bytes()).hexdigest()) for name, path in paths)


@dataclass(frozen=True, slots=True)
class ACFoldParameters:
    P: Fraction
    Q: Fraction
    X: Fraction
    E: Fraction

    def __post_init__(self) -> None:
        for name in ("P", "Q", "X", "E"):
            object.__setattr__(self, name, _q(getattr(self, name)))
        if self.X <= 0 or self.E <= 0:
            raise ValueError("the physical AC-fold chart requires X>0 and E>0")

    @property
    def linear_coefficient(self) -> Fraction:
        return 2 * self.Q * self.X - self.E * self.E

    @property
    def constant_coefficient(self) -> Fraction:
        return self.X * self.X * (self.P * self.P + self.Q * self.Q)

    @property
    def discriminant(self) -> Fraction:
        return self.E**4 - 4 * self.E * self.E * self.Q * self.X - 4 * self.P * self.P * self.X * self.X

    @property
    def digest(self) -> str:
        return canonical_digest(self)


@dataclass(frozen=True, slots=True)
class ACFoldObject:
    parameters: ACFoldParameters
    sheet: str
    object_digest: str

    @classmethod
    def build(cls, parameters: ACFoldParameters, sheet: str) -> "ACFoldObject":
        if sheet not in SHEETS:
            raise ValueError("AC-fold sheet must be high or low")
        unsigned = {"parameters": parameters, "sheet": sheet}
        return cls(**unsigned, object_digest=canonical_digest(unsigned))


@dataclass(frozen=True, slots=True)
class ACFoldMorphism:
    source: ACFoldObject
    target: ACFoldObject
    winding: int
    route_digest: str


def ac_fold_route(source: ACFoldObject, winding: int) -> ACFoldMorphism:
    if isinstance(winding, bool) or not isinstance(winding, int):
        raise TypeError("AC-fold winding must be an integer")
    target_sheet = source.sheet if winding % 2 == 0 else ("low" if source.sheet == "high" else "high")
    target = ACFoldObject.build(source.parameters, target_sheet)
    unsigned = {"source": source, "target": target, "winding": winding}
    return ACFoldMorphism(**unsigned, route_digest=canonical_digest(unsigned))


def reverse_ac_fold_route(route: ACFoldMorphism) -> ACFoldMorphism:
    return ac_fold_route(route.target, -route.winding)


def compose_ac_fold_routes(first: ACFoldMorphism, second: ACFoldMorphism) -> ACFoldMorphism:
    """Return second after first."""
    if first.target != second.source:
        raise ValueError("AC-fold routes are not composable")
    return ac_fold_route(first.source, first.winding + second.winding)


def _sqrt_interval(value: Fraction, bits: int = 80) -> tuple[Fraction, Fraction]:
    if value <= 0:
        raise ValueError("square-root isolation requires a positive rational")
    sn, sd = isqrt(value.numerator), isqrt(value.denominator)
    if sn * sn == value.numerator and sd * sd == value.denominator:
        exact = Fraction(sn, sd)
        epsilon = Fraction(1, 1 << bits)
        return exact - epsilon, exact + epsilon
    scale = 1 << bits
    floor_scaled = isqrt((value.numerator * scale * scale) // value.denominator)
    lower = Fraction(floor_scaled, scale)
    upper = Fraction(floor_scaled + 1, scale)
    if not lower * lower < value < upper * upper:
        raise ArithmeticError("failed to isolate rational square root")
    return lower, upper


def ac_fold_root_interval(parameters: ACFoldParameters, sheet: str) -> tuple[Fraction, Fraction]:
    if parameters.discriminant <= 0:
        raise ValueError("two-sheet root isolation requires Delta>0")
    lower_sqrt, upper_sqrt = _sqrt_interval(parameters.discriminant)
    centre = (parameters.E * parameters.E - 2 * parameters.Q * parameters.X) / 2
    if sheet == "high":
        return centre + lower_sqrt / 2, centre + upper_sqrt / 2
    if sheet == "low":
        return centre - upper_sqrt / 2, centre - lower_sqrt / 2
    raise ValueError("AC-fold sheet must be high or low")


def reduce_ac_fold_object(obj: ACFoldObject) -> SelectedSkeletonObject:
    return SelectedSkeletonObject.build(
        realization_id="r3.lossless_two_bus_ac_fold.v1",
        base_digest=obj.parameters.digest,
        selected_divisor="Delta=0",
        incidence_stratum="Delta>0:regular_two_sheet_chamber",
        selected_branch=obj.sheet,
        local_symmetry="C2:sheet_exchange",
        coefficient_domain="Q[sqrt(Delta)] with selected real embedding",
        orientation=1,
    )


def reduce_ac_fold_morphism(route: ACFoldMorphism) -> SelectedSkeletonMorphism:
    return SelectedSkeletonMorphism.build(
        reduce_ac_fold_object(route.source),
        reduce_ac_fold_object(route.target),
        route.winding % 2,
        f"discriminant_loop_winding:{route.winding}",
    )


@dataclass(frozen=True, slots=True)
class ACFoldCertificate:
    schema_id: str
    schema_version: str
    theorem_ids: tuple[str, ...]
    source_ledger: tuple[tuple[str, str], ...]
    route: ACFoldMorphism
    equation_coefficients: tuple[Fraction, Fraction, Fraction]
    discriminant: Fraction
    high_root_interval: tuple[Fraction, Fraction]
    low_root_interval: tuple[Fraction, Fraction]
    selection_ledger: tuple[tuple[str, str], ...]
    skeleton_source: SelectedSkeletonObject
    skeleton_target: SelectedSkeletonObject
    skeleton_morphism: SelectedSkeletonMorphism
    dependency_ledger: tuple[tuple[str, str], ...]
    verifier_version: str
    certificate_digest: str


@dataclass(frozen=True, slots=True)
class CertifiedACFoldResult:
    certificate: ACFoldCertificate


class ACFoldError(ValueError):
    def __init__(self, code: str, obligation: str, detail: str) -> None:
        super().__init__(detail)
        self.code, self.obligation, self.detail = code, obligation, detail


def _assemble_ac_fold(route: ACFoldMorphism) -> ACFoldCertificate:
    params = route.source.parameters
    if route.target.parameters != params or route != ac_fold_route(route.source, route.winding):
        raise ACFoldError("RouteCompositionMismatch", "native_ac_fold_route", "route target or digest does not match winding parity")
    if params.discriminant <= 0:
        raise ACFoldError("OutsideStrictChamber", "positive_discriminant", "the regular two-sheet realization requires Delta>0")
    high = ac_fold_root_interval(params, "high")
    low = ac_fold_root_interval(params, "low")
    if not low[1] < high[0] or high[1] <= 0:
        raise ACFoldError("RootIsolationFailure", "positive_high_voltage_sheet", "root brackets are not ordered or the high sheet is nonpositive")
    skeleton = reduce_ac_fold_morphism(route)
    unsigned = {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "theorem_ids": THEOREM_IDS,
        "source_ledger": _source_ledger(),
        "route": route,
        "equation_coefficients": (Fraction(1), params.linear_coefficient, params.constant_coefficient),
        "discriminant": params.discriminant,
        "high_root_interval": high,
        "low_root_interval": low,
        "selection_ledger": (
            ("physical_section", "high-voltage sheet continued from v=E^2 at P=Q=0"),
            ("wall", "Delta=0 square-root saddle-node fold"),
            ("route_action", "sheet exchange iff discriminant winding is odd"),
        ),
        "skeleton_source": skeleton.source,
        "skeleton_target": skeleton.target,
        "skeleton_morphism": skeleton,
        "dependency_ledger": (
            ("native_equation", "lossless two-bus AC power-flow quadratic"),
            ("arithmetic", "fractions.Fraction and integer square-root isolation"),
            ("existing_arm_oracle", "none"),
        ),
        "verifier_version": VERIFIER_VERSION,
    }
    return ACFoldCertificate(**unsigned, certificate_digest=canonical_digest(unsigned))


def continue_ac_fold_certified(route: ACFoldMorphism) -> CertifiedACFoldResult | Refusal:
    try:
        return CertifiedACFoldResult(_assemble_ac_fold(route))
    except (ACFoldError, TypeError, ValueError, ArithmeticError) as error:
        if isinstance(error, ACFoldError):
            return Refusal(error.code, error.obligation, "cella.continuation.r3_ac_fold", False, True, error.detail)
        return Refusal("RootIsolationFailure", "exact_ac_fold_arithmetic", "cella.continuation.r3_ac_fold", False, True, str(error))


def verify_ac_fold_certificate(certificate: ACFoldCertificate) -> bool | Refusal:
    try:
        expected = _assemble_ac_fold(certificate.route)
    except ACFoldError as error:
        return Refusal(error.code, error.obligation, "cella.continuation.r3_ac_fold.verify", False, False, error.detail)
    if canonical_json_bytes(expected) != canonical_json_bytes(certificate):
        return Refusal("CertificateReplayMismatch", "exact_ac_fold_replay", "cella.continuation.r3_ac_fold.verify", False, False, "certificate bytes do not replay")
    return True


def hostile_ac_fold_parameters() -> ACFoldParameters:
    return ACFoldParameters(Fraction(1), Fraction(0), Fraction(1), Fraction(2))


__all__ = [
    "ACFoldCertificate", "ACFoldMorphism", "ACFoldObject", "ACFoldParameters",
    "CertifiedACFoldResult", "ac_fold_root_interval", "ac_fold_route",
    "compose_ac_fold_routes", "continue_ac_fold_certified", "hostile_ac_fold_parameters",
    "reduce_ac_fold_morphism", "reduce_ac_fold_object", "reverse_ac_fold_route",
    "verify_ac_fold_certificate",
]
