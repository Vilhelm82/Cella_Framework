"""Exact coefficient-typed DBP relative classes for CCE-3.

The implementation is deliberately finite and theorem-bound.  It models the
marked endpoint lattice (A,B,mu,delta), its compact A/B quotient, independent
affine compact corrections, the selected lateral pair, and CPV scalar
extension.  It never invents compact coordinates or a full transport matrix.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from fractions import Fraction
from typing import ClassVar

from .canonical import canonical_digest
from .model import CoefficientRing, CorridorRouteCertificate


class RelativeClassError(ValueError):
    def __init__(self, code: str, obligation: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.obligation = obligation
        self.detail = detail


class ClaimScope(str, Enum):
    EXACT_ABSOLUTE_CLASS = "EXACT_ABSOLUTE_CLASS"
    EXACT_COMPACT_QUOTIENT_CLASS = "EXACT_COMPACT_QUOTIENT_CLASS"
    AFFINE_OVER_COMPACT_SUBMODULE = "AFFINE_OVER_COMPACT_SUBMODULE"
    SCALAR_EXTENDED_AFFINE_CLASS = "SCALAR_EXTENDED_AFFINE_CLASS"


@dataclass(frozen=True, slots=True)
class DyadicGaussian:
    real_numerator: int
    imag_numerator: int = 0
    denominator_exponent: int = 0

    def __post_init__(self) -> None:
        if isinstance(self.real_numerator, bool) or isinstance(self.imag_numerator, bool):
            raise RelativeClassError("MalformedScalar", "integer_numerators", "boolean numerators are forbidden")
        if not all(isinstance(value, int) for value in (self.real_numerator, self.imag_numerator, self.denominator_exponent)):
            raise RelativeClassError("MalformedScalar", "integer_encoding", "dyadic Gaussian fields must be integers")
        if self.denominator_exponent < 0:
            raise RelativeClassError("MalformedScalar", "nonnegative_exponent", "denominator exponent is negative")
        real, imag, exponent = self.real_numerator, self.imag_numerator, self.denominator_exponent
        if real == 0 and imag == 0:
            exponent = 0
        else:
            while exponent > 0 and real % 2 == 0 and imag % 2 == 0:
                real //= 2
                imag //= 2
                exponent -= 1
        object.__setattr__(self, "real_numerator", real)
        object.__setattr__(self, "imag_numerator", imag)
        object.__setattr__(self, "denominator_exponent", exponent)

    @classmethod
    def parse_canonical(cls, real: int, imag: int, exponent: int) -> "DyadicGaussian":
        value = cls(real, imag, exponent)
        if (value.real_numerator, value.imag_numerator, value.denominator_exponent) != (real, imag, exponent):
            raise RelativeClassError("MalformedScalar", "canonical_encoding", "scalar encoding is reducible or has noncanonical zero")
        return value

    @classmethod
    def from_fraction(cls, value: Fraction) -> "DyadicGaussian":
        denominator = value.denominator
        if denominator & (denominator - 1):
            raise RelativeClassError("RingTooSmall", "dyadic_denominator", "fraction denominator is not a power of two")
        return cls(value.numerator, 0, denominator.bit_length() - 1)

    def __add__(self, other: "DyadicGaussian") -> "DyadicGaussian":
        exponent = max(self.denominator_exponent, other.denominator_exponent)
        left = 1 << (exponent - self.denominator_exponent)
        right = 1 << (exponent - other.denominator_exponent)
        return DyadicGaussian(
            self.real_numerator * left + other.real_numerator * right,
            self.imag_numerator * left + other.imag_numerator * right,
            exponent,
        )

    def __neg__(self) -> "DyadicGaussian":
        return DyadicGaussian(-self.real_numerator, -self.imag_numerator, self.denominator_exponent)

    def __sub__(self, other: "DyadicGaussian") -> "DyadicGaussian":
        return self + (-other)

    def __mul__(self, other: "DyadicGaussian") -> "DyadicGaussian":
        return DyadicGaussian(
            self.real_numerator * other.real_numerator - self.imag_numerator * other.imag_numerator,
            self.real_numerator * other.imag_numerator + self.imag_numerator * other.real_numerator,
            self.denominator_exponent + other.denominator_exponent,
        )

    @property
    def digest(self) -> str:
        return canonical_digest(self)


ZERO_DG = DyadicGaussian(0)
ONE_DG = DyadicGaussian(1)
HALF_DG = DyadicGaussian(1, 0, 1)
I_DG = DyadicGaussian(0, 1)


RING_INCLUSIONS: dict[CoefficientRing, frozenset[CoefficientRing]] = {
    CoefficientRing.Z: frozenset({CoefficientRing.Z, CoefficientRing.Z_HALF, CoefficientRing.Z_I, CoefficientRing.Z_HALF_I}),
    CoefficientRing.Z_HALF: frozenset({CoefficientRing.Z_HALF, CoefficientRing.Z_HALF_I}),
    CoefficientRing.Z_I: frozenset({CoefficientRing.Z_I, CoefficientRing.Z_HALF_I}),
    CoefficientRing.Z_HALF_I: frozenset({CoefficientRing.Z_HALF_I}),
}


def scalar_is_member(value: DyadicGaussian, ring: CoefficientRing) -> bool:
    if ring == CoefficientRing.Z:
        return value.denominator_exponent == 0 and value.imag_numerator == 0
    if ring == CoefficientRing.Z_HALF:
        return value.imag_numerator == 0
    if ring == CoefficientRing.Z_I:
        return value.denominator_exponent == 0
    return True


def minimal_ring(value: DyadicGaussian) -> CoefficientRing:
    if value.imag_numerator == 0:
        return CoefficientRing.Z if value.denominator_exponent == 0 else CoefficientRing.Z_HALF
    return CoefficientRing.Z_I if value.denominator_exponent == 0 else CoefficientRing.Z_HALF_I


def ring_join(left: CoefficientRing, right: CoefficientRing) -> CoefficientRing:
    if right in RING_INCLUSIONS[left]:
        return right
    if left in RING_INCLUSIONS[right]:
        return left
    return CoefficientRing.Z_HALF_I


PAPER_III_PRE_INSERTION_DIGEST = "c5d790829434f848057529ef77ff855e3bc4d9f582e1d766dc2f273b4c76aeb6"
STAGE3_DIGEST = "bdaabb1a1015f7b6b3055321b422a3b6d84053c808d2e3669ea646ff3de82670"
SQG_FOUNDATION_DIGEST = "40461c1fbb177e0d173f0b11a5d12224dc7ce894bb7fd43c944c8fa75cdaf0d9"


@dataclass(frozen=True, slots=True)
class RelativeBasisManifest:
    family_id: str
    endpoint_id: str
    selected_pole_id: str
    basis_id: str
    ordered_generators: tuple[str, ...]
    generator_orientations: tuple[str, ...]
    boundary_vector: tuple[int, ...]
    compact_submodule_basis: tuple[str, ...]
    quotient_basis: tuple[str, ...]
    compact_intersection: tuple[tuple[int, int], ...]
    unclaimed_intersection_entries: tuple[str, ...]
    primitive_meridian_witness: str
    theorem_ids_and_digests: tuple[tuple[str, str], ...]

    @property
    def digest(self) -> str:
        return canonical_digest(self)


def construct_basis_manifest(paper_iii_digest: str) -> RelativeBasisManifest:
    return RelativeBasisManifest(
        family_id="dbp_legendre_third_kind_relative_family_v1",
        endpoint_id="u_minus=(sigma=1,rho=-sqrt(2))",
        selected_pole_id="P_minus_plus_selected_dual_pole",
        basis_id="dbp_u_minus_A_B_mu_delta_up_v1",
        ordered_generators=("A_minus", "B_minus", "mu_minus", "delta_minus_up"),
        generator_orientations=("A.B=+1", "B.A=-1", "positive selected-pole meridian", "Q_0 to Q_m; upper indentation"),
        boundary_vector=(0, 0, 0, 1),
        compact_submodule_basis=("A_minus", "B_minus"),
        quotient_basis=("mu_minus", "delta_minus_up"),
        compact_intersection=((0, 1), (-1, 0)),
        unclaimed_intersection_entries=("A.mu", "A.delta", "B.mu", "B.delta", "mu.mu", "mu.delta", "delta.delta"),
        primitive_meridian_witness="Stage3 (3.2)-(3.6): positive loop about one puncture is primitive; residue detects it; endpoint exact-sequence quotient is free",
        theorem_ids_and_digests=(
            ("PaperIII.Theorem7F.1", paper_iii_digest),
            ("DBP_DUAL_SURFACE_CYCLE_STAGE3.Section3", STAGE3_DIGEST),
            ("SelectedQuotientGroupoids.Proposition4.2", SQG_FOUNDATION_DIGEST),
        ),
    )


@dataclass(frozen=True, slots=True)
class RelativeClassVector:
    basis_digest: str
    ring_id: CoefficientRing
    coordinates: tuple[DyadicGaussian, DyadicGaussian, DyadicGaussian, DyadicGaussian]
    label: str

    def __post_init__(self) -> None:
        if len(self.coordinates) != 4:
            raise RelativeClassError("BasisManifestMismatch", "rank_four_coordinates", "relative vector must have four coordinates")
        if not all(scalar_is_member(value, self.ring_id) for value in self.coordinates):
            raise RelativeClassError("RingTooSmall", "coordinate_membership", "coordinate is outside declared ring")

    @property
    def boundary_coefficient(self) -> DyadicGaussian:
        return self.coordinates[3]

    @property
    def digest(self) -> str:
        return canonical_digest(self)


@dataclass(frozen=True, slots=True)
class CompactQuotientClass:
    basis_digest: str
    ring_id: CoefficientRing
    null_submodule_digest: str
    quotient_coordinates: tuple[DyadicGaussian, DyadicGaussian]
    derived_boundary_coefficient: DyadicGaussian
    representative_digest: str | None
    label: str

    @property
    def digest(self) -> str:
        return canonical_digest(self)


@dataclass(frozen=True, slots=True)
class UnknownCompactCorrection:
    symbol_id: str
    route_certificate_digest: str
    submodule_digest: str
    coefficient_ring: CoefficientRing
    status: str = "unresolved"

    def __post_init__(self) -> None:
        if self.status != "unresolved":
            raise RelativeClassError("UnknownCompactCorrection", "unresolved_status", "compact correction may not be asserted resolved")

    @property
    def digest(self) -> str:
        return canonical_digest(self)


@dataclass(frozen=True, slots=True)
class WeightedCompactUncertainty:
    correction: UnknownCompactCorrection
    coefficient: DyadicGaussian


@dataclass(frozen=True, slots=True)
class AffineRelativeClass:
    known_representative: RelativeClassVector | None
    known_quotient_class: CompactQuotientClass
    uncertainty_terms: tuple[WeightedCompactUncertainty, ...]
    ambient_basis_digest: str
    coefficient_ring: CoefficientRing
    boundary_coefficient: DyadicGaussian
    claim_scope: ClaimScope
    label: str

    def __post_init__(self) -> None:
        if self.claim_scope not in {ClaimScope.AFFINE_OVER_COMPACT_SUBMODULE, ClaimScope.SCALAR_EXTENDED_AFFINE_CLASS}:
            raise RelativeClassError("UnknownCompactCorrection", "affine_claim_scope", "affine class cannot claim an exact absolute representative")
        if not self.uncertainty_terms:
            raise RelativeClassError("UnknownCompactCorrection", "uncertainty_retention", "affine transport must retain compact uncertainty")
        if not scalar_is_member(self.boundary_coefficient, self.coefficient_ring):
            raise RelativeClassError("RingTooSmall", "boundary_membership", "boundary is outside affine ring")

    @property
    def digest(self) -> str:
        return canonical_digest(self)


def compact_submodule_digest(basis: RelativeBasisManifest) -> str:
    return canonical_digest({"basis_digest": basis.digest, "generators": basis.compact_submodule_basis})


def take_compact_quotient(value: RelativeClassVector, basis: RelativeBasisManifest) -> CompactQuotientClass:
    if value.basis_digest != basis.digest:
        raise RelativeClassError("BasisManifestMismatch", "basis_digest", "class and basis differ")
    return CompactQuotientClass(
        basis.digest,
        value.ring_id,
        compact_submodule_digest(basis),
        (value.coordinates[2], value.coordinates[3]),
        value.boundary_coefficient,
        value.digest,
        f"q({value.label})",
    )


def compute_boundary(value: RelativeClassVector | CompactQuotientClass | AffineRelativeClass) -> DyadicGaussian:
    if isinstance(value, RelativeClassVector):
        return value.boundary_coefficient
    if isinstance(value, CompactQuotientClass):
        return value.derived_boundary_coefficient
    return value.boundary_coefficient


def _same_basis(left: RelativeClassVector, right: RelativeClassVector) -> None:
    if left.basis_digest != right.basis_digest:
        raise RelativeClassError("BasisManifestMismatch", "basis_digest", "class operands use different bases")
    if left.ring_id != right.ring_id:
        raise RelativeClassError("IllegalImplicitScalarExtension", "explicit_ring_extension", "mixed-ring arithmetic requires explicit scalar extension")


def add_classes(left: RelativeClassVector, right: RelativeClassVector, label: str = "sum") -> RelativeClassVector:
    _same_basis(left, right)
    return RelativeClassVector(left.basis_digest, left.ring_id, tuple(a + b for a, b in zip(left.coordinates, right.coordinates)), label)  # type: ignore[arg-type]


def subtract_classes(left: RelativeClassVector, right: RelativeClassVector, label: str = "difference") -> RelativeClassVector:
    _same_basis(left, right)
    return RelativeClassVector(left.basis_digest, left.ring_id, tuple(a - b for a, b in zip(left.coordinates, right.coordinates)), label)  # type: ignore[arg-type]


def scale_class(scalar: DyadicGaussian, value: RelativeClassVector, label: str = "scaled") -> RelativeClassVector:
    if not scalar_is_member(scalar, value.ring_id):
        raise RelativeClassError("RingTooSmall", "scalar_membership", "scalar lies outside the class ring")
    return RelativeClassVector(value.basis_digest, value.ring_id, tuple(scalar * item for item in value.coordinates), label)  # type: ignore[arg-type]


def extend_scalars(value: RelativeClassVector, target_ring: CoefficientRing) -> RelativeClassVector:
    if target_ring not in RING_INCLUSIONS[value.ring_id]:
        raise RelativeClassError("IllegalImplicitScalarExtension", "ring_inclusion", f"no legal inclusion {value.ring_id.value} -> {target_ring.value}")
    return replace(value, ring_id=target_ring, label=f"Ext[{target_ring.value}]({value.label})")


def restrict_scalars_if_member(value: RelativeClassVector, target_ring: CoefficientRing) -> RelativeClassVector:
    if not all(scalar_is_member(item, target_ring) for item in value.coordinates):
        raise RelativeClassError("ScalarRestrictionFailed", "exact_ring_membership", "coordinates do not lie in requested subring")
    return replace(value, ring_id=target_ring, label=f"Res[{target_ring.value}]({value.label})")


def vector_minimal_ring(value: RelativeClassVector) -> CoefficientRing:
    result = CoefficientRing.Z
    for coordinate in value.coordinates:
        result = ring_join(result, minimal_ring(coordinate))
    return result


def _combine_uncertainties(terms: tuple[WeightedCompactUncertainty, ...], ring: CoefficientRing) -> tuple[WeightedCompactUncertainty, ...]:
    accumulated: dict[str, tuple[UnknownCompactCorrection, DyadicGaussian]] = {}
    for term in terms:
        if not scalar_is_member(term.coefficient, ring):
            raise RelativeClassError("RingTooSmall", "uncertainty_coefficient", "uncertainty coefficient lies outside class ring")
        current = accumulated.get(term.correction.symbol_id)
        if current is None:
            accumulated[term.correction.symbol_id] = (term.correction, term.coefficient)
        else:
            if current[0].digest != term.correction.digest:
                raise RelativeClassError("UnknownCompactCorrection", "symbol_identity", "same symbol id has inconsistent provenance")
            accumulated[term.correction.symbol_id] = (current[0], current[1] + term.coefficient)
    return tuple(
        WeightedCompactUncertainty(correction, coefficient)
        for _symbol, (correction, coefficient) in sorted(accumulated.items())
        if coefficient != ZERO_DG
    )


@dataclass(frozen=True, slots=True)
class CertifiedLateralPair:
    upper_route_certificate_digest: str
    lower_route_certificate_digest: str
    upper_selected_class: RelativeClassVector
    lower_selected_class: RelativeClassVector
    upper_transport: AffineRelativeClass
    lower_transport: AffineRelativeClass
    meridian_relation_digest: str
    common_boundary: DyadicGaussian
    quotient_witnesses: tuple[str, str]

    @property
    def digest(self) -> str:
        return canonical_digest(self)


@dataclass(frozen=True, slots=True)
class CPVClassRecord:
    lateral_pair_digest: str
    scalar_extension_witness: str
    selected_endpoint_half_sum: RelativeClassVector
    quotient_half_sum: CompactQuotientClass
    transported_affine_half_sum: AffineRelativeClass
    compact_ambiguity_terms: tuple[WeightedCompactUncertainty, ...]
    nonintegrality_witness: str
    minimal_ring: CoefficientRing

    @property
    def digest(self) -> str:
        return canonical_digest(self)


@dataclass(frozen=True, slots=True)
class BoundaryObstructionWitness:
    input_boundary: DyadicGaussian
    phased_boundary: DyadicGaussian
    integral_boundary_generator: str
    closed_cycle_boundary: DyadicGaussian
    contradiction: str

    @property
    def digest(self) -> str:
        return canonical_digest(self)


def construct_selected_lateral(
    route_certificate: CorridorRouteCertificate,
    basis: RelativeBasisManifest,
) -> tuple[RelativeClassVector, AffineRelativeClass]:
    from .api import verify_corridor_certificate

    replay = verify_corridor_certificate(route_certificate)
    if replay is not True:
        raise RelativeClassError("RouteCertificateMismatch", "nested_cce2_replay", "nested corridor certificate failed replay")
    route_id = route_certificate.request.route_id
    if route_id.endswith("upper_qi_v1"):
        coordinates = (ZERO_DG, ZERO_DG, ZERO_DG, ONE_DG)
        side, target_token, symbol = "upper", "delta_-^up", "lambda_up"
    elif route_id.endswith("lower_qi_v1"):
        coordinates = (ZERO_DG, ZERO_DG, ONE_DG, ONE_DG)
        side, target_token, symbol = "lower", "delta_-^down", "lambda_down"
    else:
        raise RelativeClassError("UnsupportedRoute", "theorem_bound_route", "route is outside the certified pair")
    if target_token not in route_certificate.selected_target_quotient_class:
        raise RelativeClassError("RouteCertificateMismatch", "lateral_side", "route and selected lateral side disagree")
    selected = RelativeClassVector(basis.digest, CoefficientRing.Z, coordinates, f"delta_minus_{side}")
    quotient = take_compact_quotient(selected, basis)
    correction = UnknownCompactCorrection(symbol, route_certificate.certificate_digest, compact_submodule_digest(basis), CoefficientRing.Z)
    transport = AffineRelativeClass(
        selected,
        quotient,
        (WeightedCompactUncertainty(correction, ONE_DG),),
        basis.digest,
        CoefficientRing.Z,
        ONE_DG,
        ClaimScope.AFFINE_OVER_COMPACT_SUBMODULE,
        f"G_{side}(delta_plus)",
    )
    return selected, transport


def construct_lateral_pair(
    upper_certificate: CorridorRouteCertificate,
    lower_certificate: CorridorRouteCertificate,
    basis: RelativeBasisManifest,
) -> CertifiedLateralPair:
    upper, upper_transport = construct_selected_lateral(upper_certificate, basis)
    lower, lower_transport = construct_selected_lateral(lower_certificate, basis)
    if not upper_certificate.request.route_id.endswith("upper_qi_v1") or not lower_certificate.request.route_id.endswith("lower_qi_v1"):
        raise RelativeClassError("RouteCertificateMismatch", "route_order", "lateral certificates are swapped")
    meridian = RelativeClassVector(basis.digest, CoefficientRing.Z, (ZERO_DG, ZERO_DG, -ONE_DG, ZERO_DG), "-mu_minus")
    relation = subtract_classes(upper, lower, "delta_up_minus_delta_down")
    if relation.coordinates != meridian.coordinates:
        raise RelativeClassError("MeridianRelationMismatch", "delta_up_minus_delta_down", "lateral difference is not -mu")
    if compute_boundary(upper) != ONE_DG or compute_boundary(lower) != ONE_DG:
        raise RelativeClassError("BoundaryMismatch", "common_beta", "lateral boundaries differ from beta")
    return CertifiedLateralPair(
        upper_certificate.certificate_digest,
        lower_certificate.certificate_digest,
        upper,
        lower,
        upper_transport,
        lower_transport,
        canonical_digest({"left": relation, "right": meridian}),
        ONE_DG,
        (upper_transport.known_quotient_class.digest, lower_transport.known_quotient_class.digest),
    )


def _extend_affine(value: AffineRelativeClass, target_ring: CoefficientRing) -> AffineRelativeClass:
    if target_ring not in RING_INCLUSIONS[value.coefficient_ring]:
        raise RelativeClassError("IllegalImplicitScalarExtension", "ring_inclusion", "illegal affine scalar extension")
    known = extend_scalars(value.known_representative, target_ring) if value.known_representative else None
    quotient = replace(
        value.known_quotient_class,
        ring_id=target_ring,
        label=f"Ext[{target_ring.value}]({value.known_quotient_class.label})",
    )
    terms = tuple(
        WeightedCompactUncertainty(replace(term.correction, coefficient_ring=target_ring), term.coefficient)
        for term in value.uncertainty_terms
    )
    return AffineRelativeClass(known, quotient, terms, value.ambient_basis_digest, target_ring, value.boundary_coefficient, ClaimScope.SCALAR_EXTENDED_AFFINE_CLASS, f"Ext[{target_ring.value}]({value.label})")


def extend_affine_scalars(value: AffineRelativeClass, target_ring: CoefficientRing) -> AffineRelativeClass:
    return _extend_affine(value, target_ring)


def scale_affine_class(
    scalar: DyadicGaussian,
    value: AffineRelativeClass,
    label: str = "scaled_affine",
) -> AffineRelativeClass | RelativeClassVector:
    if not scalar_is_member(scalar, value.coefficient_ring):
        raise RelativeClassError("RingTooSmall", "affine_scalar_membership", "scalar lies outside affine ring")
    known = scale_class(scalar, value.known_representative, f"known({label})") if value.known_representative else None
    terms = _combine_uncertainties(tuple(
        WeightedCompactUncertainty(term.correction, scalar * term.coefficient)
        for term in value.uncertainty_terms
    ), value.coefficient_ring)
    if not terms:
        if known is None:
            raise RelativeClassError("AbsoluteRepresentativeUnknown", "zero_affine_representative", "cancellation left no known representative")
        return known
    quotient = CompactQuotientClass(
        value.known_quotient_class.basis_digest,
        value.coefficient_ring,
        value.known_quotient_class.null_submodule_digest,
        tuple(scalar * coordinate for coordinate in value.known_quotient_class.quotient_coordinates),  # type: ignore[arg-type]
        scalar * value.known_quotient_class.derived_boundary_coefficient,
        known.digest if known else None,
        f"q({label})",
    )
    return AffineRelativeClass(
        known, quotient, terms, value.ambient_basis_digest, value.coefficient_ring,
        scalar * value.boundary_coefficient, value.claim_scope, label,
    )


def add_affine_classes(
    left: AffineRelativeClass,
    right: AffineRelativeClass,
    label: str = "affine_sum",
) -> AffineRelativeClass | RelativeClassVector:
    if left.ambient_basis_digest != right.ambient_basis_digest:
        raise RelativeClassError("BasisManifestMismatch", "affine_basis", "affine operands use different bases")
    if left.coefficient_ring != right.coefficient_ring:
        raise RelativeClassError("IllegalImplicitScalarExtension", "explicit_ring_extension", "mixed-ring affine arithmetic requires extension")
    if left.known_quotient_class.null_submodule_digest != right.known_quotient_class.null_submodule_digest:
        raise RelativeClassError("NullSubmoduleMismatch", "affine_null_submodule", "affine operands use different null submodules")
    known = None
    if left.known_representative is not None and right.known_representative is not None:
        known = add_classes(left.known_representative, right.known_representative, f"known({label})")
    terms = _combine_uncertainties(left.uncertainty_terms + right.uncertainty_terms, left.coefficient_ring)
    if not terms:
        if known is None:
            raise RelativeClassError("AbsoluteRepresentativeUnknown", "cancelled_affine_representative", "uncertainties cancelled without a known representative")
        return known
    quotient = CompactQuotientClass(
        left.ambient_basis_digest,
        left.coefficient_ring,
        left.known_quotient_class.null_submodule_digest,
        tuple(a + b for a, b in zip(left.known_quotient_class.quotient_coordinates, right.known_quotient_class.quotient_coordinates)),  # type: ignore[arg-type]
        left.boundary_coefficient + right.boundary_coefficient,
        known.digest if known else None,
        f"q({label})",
    )
    scope = ClaimScope.SCALAR_EXTENDED_AFFINE_CLASS if ClaimScope.SCALAR_EXTENDED_AFFINE_CLASS in {left.claim_scope, right.claim_scope} else ClaimScope.AFFINE_OVER_COMPACT_SUBMODULE
    return AffineRelativeClass(
        known, quotient, terms, left.ambient_basis_digest, left.coefficient_ring,
        left.boundary_coefficient + right.boundary_coefficient, scope, label,
    )


def subtract_affine_classes(
    left: AffineRelativeClass,
    right: AffineRelativeClass,
    label: str = "affine_difference",
) -> AffineRelativeClass | RelativeClassVector:
    negated = scale_affine_class(DyadicGaussian(-1), right, f"-{right.label}")
    if not isinstance(negated, AffineRelativeClass):
        raise RelativeClassError("UnknownCompactCorrection", "affine_subtraction", "unexpected exact negated affine class")
    return add_affine_classes(left, negated, label)


def form_cpv(
    pair: CertifiedLateralPair,
    basis: RelativeBasisManifest,
    requested_ring: CoefficientRing,
) -> CPVClassRecord:
    if requested_ring not in {CoefficientRing.Z_HALF, CoefficientRing.Z_HALF_I}:
        raise RelativeClassError("RingTooSmall", "cpv_half_meridian", "CPV requires inversion of 2")
    upper = extend_scalars(pair.upper_selected_class, requested_ring)
    lower = extend_scalars(pair.lower_selected_class, requested_ring)
    endpoint = scale_class(HALF_DG, add_classes(upper, lower, "lateral_sum"), "delta_minus_CPV")
    expected = (ZERO_DG, ZERO_DG, HALF_DG, ONE_DG)
    if endpoint.coordinates != expected:
        raise RelativeClassError("MeridianRelationMismatch", "cpv_coordinates", "CPV coordinates do not replay")
    quotient = take_compact_quotient(endpoint, basis)
    up_affine = _extend_affine(pair.upper_transport, requested_ring)
    down_affine = _extend_affine(pair.lower_transport, requested_ring)
    terms = _combine_uncertainties(tuple(
        WeightedCompactUncertainty(term.correction, HALF_DG)
        for term in (*up_affine.uncertainty_terms, *down_affine.uncertainty_terms)
    ), requested_ring)
    transported = AffineRelativeClass(
        endpoint,
        quotient,
        terms,
        basis.digest,
        requested_ring,
        ONE_DG,
        ClaimScope.SCALAR_EXTENDED_AFFINE_CLASS,
        "(G_up(delta_plus)+G_down(delta_plus))/2",
    )
    if tuple(term.correction.symbol_id for term in terms) != ("lambda_down", "lambda_up"):
        raise RelativeClassError("UnknownCompactCorrection", "independent_half_corrections", "CPV affine ambiguity was lost or merged")
    return CPVClassRecord(
        pair.digest,
        f"Z -> {requested_ring.value}; exact scalar 1/2",
        endpoint,
        quotient,
        transported,
        terms,
        "mu_minus is primitive; coordinate 1/2 cannot restrict to Z",
        CoefficientRing.Z_HALF,
    )


def multiply_by_i(value: RelativeClassVector, requested_ring: CoefficientRing) -> RelativeClassVector:
    if requested_ring not in {CoefficientRing.Z_I, CoefficientRing.Z_HALF_I}:
        raise RelativeClassError("RingTooSmall", "gaussian_phase", "multiplication by i requires a Gaussian coefficient ring")
    extended = extend_scalars(value, requested_ring)
    return scale_class(I_DG, extended, f"i*{value.label}")


def prove_integral_phase_obstruction(value: RelativeClassVector) -> BoundaryObstructionWitness:
    phased = multiply_by_i(value, CoefficientRing.Z_HALF_I if value.ring_id == CoefficientRing.Z_HALF else CoefficientRing.Z_I)
    if compute_boundary(value) != ONE_DG or compute_boundary(phased) != I_DG:
        raise RelativeClassError("BoundaryMismatch", "phase_boundary", "boundary computation does not yield beta and i*beta")
    return BoundaryObstructionWitness(
        ONE_DG,
        I_DG,
        "Z*beta",
        ZERO_DG,
        "i is not an integer; adding any closed cycle changes boundary by 0, so i*beta is outside Z*beta",
    )


REFUSAL_VOCABULARY = (
    "UnsupportedRoute", "RouteCertificateRequired", "RouteCertificateMismatch",
    "UnsupportedInputClass", "BasisManifestMismatch", "BoundaryMismatch",
    "IntersectionConventionMismatch", "NullSubmoduleMismatch", "QuotientScopeMismatch",
    "PrimitiveMeridianUnproved", "MeridianRelationMismatch", "RingTooSmall",
    "IllegalImplicitScalarExtension", "ScalarRestrictionFailed", "BoundaryObstruction",
    "UnknownCompactCorrection", "AbsoluteRepresentativeUnknown",
    "FullTransportMatrixUnavailable", "EvaluationStageRequired", "UnsupportedOperation",
    "SourceDigestMismatch", "CheckpointMismatch", "CertificateTampered", "MalformedScalar",
)


__all__ = [
    "AffineRelativeClass", "BoundaryObstructionWitness", "CPVClassRecord",
    "CertifiedLateralPair", "ClaimScope", "DyadicGaussian", "HALF_DG", "I_DG",
    "ONE_DG", "REFUSAL_VOCABULARY", "RING_INCLUSIONS", "RelativeBasisManifest",
    "RelativeClassError", "RelativeClassVector", "SQG_FOUNDATION_DIGEST",
    "STAGE3_DIGEST", "UnknownCompactCorrection", "WeightedCompactUncertainty",
    "ZERO_DG", "add_classes", "compact_submodule_digest", "compute_boundary",
    "add_affine_classes",
    "construct_basis_manifest", "construct_lateral_pair", "construct_selected_lateral",
    "extend_affine_scalars", "extend_scalars", "form_cpv", "minimal_ring", "multiply_by_i",
    "prove_integral_phase_obstruction", "restrict_scalars_if_member", "ring_join",
    "scalar_is_member", "scale_affine_class", "scale_class", "subtract_affine_classes", "subtract_classes", "take_compact_quotient",
    "vector_minimal_ring",
]
