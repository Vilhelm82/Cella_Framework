"""CCE-8 exact finite-order active role-cover continuation.

The released certificate retains the order-2 channel account, while the finite
adapter implements Paper I's rational S3 action at every requested jet order.
Cross-carrier identifications are separate mathematical questions.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from .canonical import canonical_digest, canonical_json_bytes
from .model import Refusal


SCHEMA_ID = "cella.continuation.cce8_role_cover_certificate"
SCHEMA_VERSION = "1.0"
VERIFIER_VERSION = "cella.continuation.cce8.verifier.v1"
ADAPTER_ID = "cella.continuation.role_cover_order2_v1"
PAPER_I_DIGEST = "f045a92762f68cd1ddfc83e243e76eb4739d720f8097bc6736e29195c88d2d01"
RECERT_DIGEST = "4afe63564fcc06b7ae5a2517baa5f08acca652e9f207ec50d969930a249247fe"
REFERENCE_LIFT_DIGEST = "caca79c7f903b9e9ea4018da650e09737b0f53947a91482a46d1a2432752f15f"
PATHFINDER_PROVIDER_DIGEST = "69de4e1a54432c696fe69abadf6b68f80f342a486589d285108ae031e68b64a4"
THEOREM_IDS = (
    "RC-I.1:regular-active-role-locus",
    "RC-I.2:order-2-rational-rechart-generators",
    "RC-I.3:s2-t2-st3-relations",
    "RC-I.4:active-role-jet-orbit",
    "RC-I.5:named-channel-permutation",
    "RC-I.6:faithfulness-jacobian",
    "RC-I.7:typed-role-boundaries",
)
FINITE_THEOREM_IDS = (
    "RC-I.1:regular-active-role-locus",
    "RC-I.2:rational-rechart-generators-at-every-finite-order",
    "RC-I.3:s2-t2-st3-relations",
    "RC-I.4:active-role-jet-orbit",
    "RC-I.5:named-channel-permutation",
)
ROLES = ("P", "D", "S")


def _q(value: int | Fraction) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError("role jets require exact int/Fraction entries")
    return Fraction(value)


def _sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_paths() -> tuple[tuple[str, Path, str], ...]:
    root = Path(__file__).parents[4]
    return (
        ("paper_i", root / "archive/Reference_Material/papers/current/dbp_orbit_calculus.tex", PAPER_I_DIGEST),
        ("recert", root / "research/verification/recert_role_channels.py", RECERT_DIGEST),
        ("runtime", root / "engine/src/cella/reference_lift.py", REFERENCE_LIFT_DIGEST),
        ("pathfinder", root / "engine/src/cella/pathfinder/recognize/curvature.py", PATHFINDER_PROVIDER_DIGEST),
    )


def _source_ledger() -> tuple[tuple[str, str], ...]:
    ledger = []
    for name, path, expected in _source_paths():
        if not path.is_file() or _sha256(path) != expected:
            raise RoleCoverError("StageDependencyUnavailable", "source_lock", f"{name} source does not match its frozen digest")
        ledger.append((name, expected))
    return tuple(ledger)


@dataclass(frozen=True, slots=True)
class CCE8Request:
    request_id: str
    jet: tuple[Fraction, Fraction, Fraction, Fraction, Fraction]
    operation_word: str
    selected_role: str
    requested_scope: str = "paper_i_order2_role_cover"
    source_lock_digest: str = PAPER_I_DIGEST

    def __post_init__(self) -> None:
        object.__setattr__(self, "jet", tuple(_q(x) for x in self.jet))
        if not self.request_id or self.selected_role not in ROLES:
            raise ValueError("request id and selected P/D/S role are required")
        if self.operation_word != "e" and (not self.operation_word or set(self.operation_word) - {"s", "t"}):
            raise ValueError("operation word must be e or a non-empty word in s,t")

    @property
    def digest(self) -> str:
        return canonical_digest(self)


@dataclass(frozen=True, slots=True)
class RoleCoverState:
    active_chart: str
    jet: tuple[Fraction, ...]
    role_labels: tuple[str, str, str]
    selected_role: str
    selected_chart_label: str
    lambda_channels: tuple[Fraction, Fraction, Fraction]
    kappa_channels: tuple[Fraction, Fraction, Fraction]
    divisor_ledger: tuple[tuple[str, Fraction], ...]
    state_digest: str


@dataclass(frozen=True, slots=True)
class CCE8Certificate:
    schema_id: str
    schema_version: str
    request: CCE8Request
    theorem_ids: tuple[str, ...]
    source_ledger: tuple[tuple[str, str], ...]
    initial_state: RoleCoverState
    terminal_state: RoleCoverState
    operation_trace: tuple[tuple[str, str], ...]
    role_permutation: tuple[tuple[str, str], ...]
    group_law_ledger: tuple[tuple[str, bool], ...]
    channel_account_ledger: tuple[tuple[str, str], ...]
    selection_ledger: tuple[tuple[str, str], ...]
    previous_checkpoint_digest: str | None
    verifier_version: str
    canonical_certificate_digest: str


@dataclass(frozen=True, slots=True)
class CertifiedRoleCoverResult:
    request: CCE8Request
    certificate: CCE8Certificate


@dataclass(frozen=True, slots=True)
class CCE8Checkpoint:
    schema_id: str
    request_digest: str
    certificate_digest: str
    certified_prefix: tuple[str, ...]
    remaining_operations_digest: str
    previous_checkpoint_digest: str | None
    checkpoint_digest: str


class RoleCoverError(ValueError):
    def __init__(self, code: str, obligation: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.obligation = obligation
        self.detail = detail


@dataclass(frozen=True, slots=True)
class RoleBoundaryEvent:
    jet: tuple[Fraction, Fraction, Fraction, Fraction, Fraction]
    stratum_types: tuple[str, ...]
    unavailable_output_roles: tuple[str, ...]
    vanishing_channel_numerators: tuple[str, ...]
    regular_active_role_locus: bool
    event_digest: str


def classify_role_boundary(jet: tuple[Fraction, Fraction, Fraction, Fraction, Fraction]) -> RoleBoundaryEvent:
    """Paper-I typed specialization at chart and channel-isotropy divisors."""
    a, b, A, B, C = tuple(_q(value) for value in jet)
    unavailable = []
    strata = []
    if a == 0:
        unavailable.append("D")
        strata.append("active_chart_failure:a=0")
    if b == 0:
        unavailable.append("S")
        strata.append("active_chart_failure:b=0")
    numerators = {
        "Lambda_P": B,
        "a*Lambda_D": A * b - a * B,
        "b*Lambda_S": C * a - b * B,
    }
    vanishing = tuple(name for name, value in numerators.items() if value == 0)
    strata.extend(f"channel_isotropy:{name}=0" for name in vanishing)
    if not strata:
        strata.append("regular_active_role_locus")
    unsigned = {
        "jet": (a, b, A, B, C),
        "stratum_types": tuple(strata),
        "unavailable_output_roles": tuple(unavailable),
        "vanishing_channel_numerators": vanishing,
        "regular_active_role_locus": not unavailable and not vanishing,
    }
    return RoleBoundaryEvent(**unsigned, event_digest=canonical_digest(unsigned))


@dataclass(frozen=True, slots=True)
class FiniteRoleJet:
    """A normalized bivariate Taylor polynomial P=f(D,S), without constant."""

    order: int
    coefficients: tuple[tuple[int, int, Fraction], ...]

    def __post_init__(self) -> None:
        if isinstance(self.order, bool) or not isinstance(self.order, int) or self.order < 2:
            raise ValueError("finite role-jet order must be an integer at least two")
        merged: dict[tuple[int, int], Fraction] = {}
        for i, j, value in self.coefficients:
            if isinstance(i, bool) or isinstance(j, bool) or not isinstance(i, int) or not isinstance(j, int):
                raise TypeError("jet exponents must be integers")
            if i < 0 or j < 0 or not 1 <= i + j <= self.order:
                raise ValueError("jet monomial lies outside the finite positive-degree truncation")
            key = (i, j)
            if key in merged:
                raise ValueError("duplicate finite-jet monomial")
            merged[key] = _q(value)
        canonical = tuple((i, j, value) for (i, j), value in sorted(merged.items()) if value)
        object.__setattr__(self, "coefficients", canonical)

    @property
    def digest(self) -> str:
        return canonical_digest(self)

    def coefficient(self, i: int, j: int) -> Fraction:
        return dict(((p, q), value) for p, q, value in self.coefficients).get((i, j), Fraction(0))

    def order2_jet(self) -> tuple[Fraction, Fraction, Fraction, Fraction, Fraction]:
        return (
            self.coefficient(1, 0),
            self.coefficient(0, 1),
            2 * self.coefficient(2, 0),
            self.coefficient(1, 1),
            2 * self.coefficient(0, 2),
        )


def truncate_finite_role_jet(jet: FiniteRoleJet, target_order: int) -> FiniteRoleJet:
    """Canonical quotient by the ideal of monomials of degree > target_order."""
    if isinstance(target_order, bool) or not isinstance(target_order, int):
        raise TypeError("finite tower order must be an integer")
    if not 2 <= target_order <= jet.order:
        raise ValueError("finite tower target must lie between two and the source order")
    return FiniteRoleJet(
        target_order,
        tuple((i, j, value) for i, j, value in jet.coefficients if i + j <= target_order),
    )


@dataclass(frozen=True, slots=True)
class FiniteTowerNaturalityWitness:
    """Exact commuting-square witness for one finite truncation and S3 word."""

    source_jet_digest: str
    source_order: int
    target_order: int
    operation_word: str
    implementation_ledger: tuple[tuple[str, str], ...]
    act_then_truncate_digest: str
    truncate_then_act_digest: str
    recurrence_ledger: tuple[tuple[str, str], ...]
    theorem_id: str
    witness_digest: str


def finite_jet_from_order2(jet: tuple[Fraction, Fraction, Fraction, Fraction, Fraction], order: int = 2) -> FiniteRoleJet:
    a, b, A, B, C = tuple(_q(value) for value in jet)
    return FiniteRoleJet(order, ((1, 0, a), (0, 1, b), (2, 0, A / 2), (1, 1, B), (0, 2, C / 2)))


def _poly_add(left: dict[tuple[int, int], Fraction], right: dict[tuple[int, int], Fraction], order: int) -> dict[tuple[int, int], Fraction]:
    out = dict(left)
    for monomial, value in right.items():
        if sum(monomial) <= order:
            out[monomial] = out.get(monomial, Fraction(0)) + value
            if not out[monomial]:
                del out[monomial]
    return out


def _poly_mul(left: dict[tuple[int, int], Fraction], right: dict[tuple[int, int], Fraction], order: int) -> dict[tuple[int, int], Fraction]:
    out: dict[tuple[int, int], Fraction] = {}
    for (i, j), a in left.items():
        for (k, ell), b in right.items():
            monomial = (i + k, j + ell)
            if sum(monomial) <= order:
                out[monomial] = out.get(monomial, Fraction(0)) + a * b
    return {monomial: value for monomial, value in out.items() if value}


def _poly_pow(poly: dict[tuple[int, int], Fraction], exponent: int, order: int) -> dict[tuple[int, int], Fraction]:
    out = {(0, 0): Fraction(1)}
    for _ in range(exponent):
        out = _poly_mul(out, poly, order)
    return out


def _compose_graph(coefficients: dict[tuple[int, int], Fraction], inner_d: dict[tuple[int, int], Fraction], order: int) -> dict[tuple[int, int], Fraction]:
    s = {(0, 1): Fraction(1)}
    out: dict[tuple[int, int], Fraction] = {}
    for (i, j), value in coefficients.items():
        term = _poly_mul(_poly_pow(inner_d, i, order), _poly_pow(s, j, order), order)
        out = _poly_add(out, {monomial: value * coefficient for monomial, coefficient in term.items()}, order)
    return out


def _finite_act_s(jet: FiniteRoleJet) -> FiniteRoleJet:
    return FiniteRoleJet(jet.order, tuple((j, i, value) for i, j, value in jet.coefficients))


def _finite_act_t(jet: FiniteRoleJet) -> FiniteRoleJet:
    """Exact formal inverse D=g(P,S), recursively by homogeneous degree."""
    coefficients = {(i, j): value for i, j, value in jet.coefficients}
    a = coefficients.get((1, 0), Fraction(0))
    if a == 0:
        raise RoleCoverError("RechartDomainViolation", "a_nonzero", "the D-output chart is absent at a=0")
    inverse: dict[tuple[int, int], Fraction] = {}
    for degree in range(1, jet.order + 1):
        composed = _compose_graph(coefficients, inverse, jet.order)
        for i in range(degree + 1):
            j = degree - i
            target = Fraction(1) if (i, j) == (1, 0) else Fraction(0)
            value = (target - composed.get((i, j), Fraction(0))) / a
            if value:
                inverse[(i, j)] = value
    return FiniteRoleJet(jet.order, tuple((i, j, value) for (i, j), value in inverse.items()))


def act_finite_role_jet(jet: FiniteRoleJet, operation_word: str) -> FiniteRoleJet:
    if operation_word != "e" and (not operation_word or set(operation_word) - {"s", "t"}):
        raise ValueError("operation word must be e or a non-empty word in s,t")
    if operation_word == "e":
        return jet
    for generator in operation_word:
        jet = _finite_act_s(jet) if generator == "s" else _finite_act_t(jet)
    return jet


def finite_role_group_laws(jet: FiniteRoleJet) -> tuple[tuple[str, bool], ...]:
    return (
        ("s^2=e", act_finite_role_jet(jet, "ss") == jet),
        ("t^2=e", act_finite_role_jet(jet, "tt") == jet),
        ("(st)^3=e", act_finite_role_jet(jet, "ststst") == jet),
    )


def finite_tower_naturality(
    jet: FiniteRoleJet,
    target_order: int,
    operation_word: str,
) -> FiniteTowerNaturalityWitness:
    """Prove that the exact role action commutes with finite truncation.

    The ``s`` generator only permutes bidegrees.  The ``t`` generator is the
    recursively unique formal inverse; its coefficient of total degree d
    depends only on input and inverse coefficients of degrees at most d.
    Therefore quotienting by terms above ``target_order`` commutes with each
    generator, and hence with every finite word by induction on word length.
    The equality is also replayed here coefficient-by-coefficient.
    """
    truncated = truncate_finite_role_jet(jet, target_order)
    left = truncate_finite_role_jet(act_finite_role_jet(jet, operation_word), target_order)
    right = act_finite_role_jet(truncated, operation_word)
    if left != right:
        raise RoleCoverError(
            "FiniteTowerNaturalityMismatch",
            "truncation_rechart_commuting_square",
            "finite role action failed to commute with truncation",
        )
    recurrence = (
        ("s", "bidegree permutation preserves the total-degree filtration"),
        ("t", "degree-d inverse coefficient depends only on coefficients through degree d"),
        ("word", "generator naturality composes by induction on finite word length"),
    )
    unsigned = {
        "source_jet_digest": jet.digest,
        "source_order": jet.order,
        "target_order": target_order,
        "operation_word": operation_word,
        "implementation_ledger": (("cce8_runtime", _sha256(Path(__file__))),),
        "act_then_truncate_digest": left.digest,
        "truncate_then_act_digest": right.digest,
        "recurrence_ledger": recurrence,
        "theorem_id": "RC-I.8:finite-tower-truncation-naturality",
    }
    return FiniteTowerNaturalityWitness(**unsigned, witness_digest=canonical_digest(unsigned))


def verify_finite_tower_naturality(
    jet: FiniteRoleJet,
    witness: FiniteTowerNaturalityWitness,
) -> bool | Refusal:
    try:
        expected = finite_tower_naturality(jet, witness.target_order, witness.operation_word)
    except (RoleCoverError, TypeError, ValueError, ZeroDivisionError) as error:
        return Refusal(
            "FiniteTowerNaturalityMismatch",
            "finite_tower_witness_replay",
            "cella.continuation.cce8.finite_tower.verify",
            False,
            False,
            str(error),
        )
    if canonical_json_bytes(expected) != canonical_json_bytes(witness):
        return Refusal(
            "FiniteTowerNaturalityMismatch",
            "finite_tower_witness_replay",
            "cella.continuation.cce8.finite_tower.verify",
            False,
            False,
            "finite-tower witness bytes do not replay",
        )
    return True


@dataclass(frozen=True, slots=True)
class CCE8FiniteRequest:
    request_id: str
    jet: FiniteRoleJet
    operation_word: str
    selected_role: str
    requested_scope: str = "paper_i_arbitrary_finite_role_cover"
    source_lock_digest: str = PAPER_I_DIGEST

    def __post_init__(self) -> None:
        if not self.request_id or self.selected_role not in ROLES:
            raise ValueError("request id and selected P/D/S role are required")
        if self.operation_word != "e" and (not self.operation_word or set(self.operation_word) - {"s", "t"}):
            raise ValueError("operation word must be e or a non-empty word in s,t")

    @property
    def digest(self) -> str:
        return canonical_digest(self)


@dataclass(frozen=True, slots=True)
class FiniteRoleCoverState:
    jet: FiniteRoleJet
    role_labels: tuple[str, str, str]
    selected_role: str
    selected_chart_label: str
    order2_channel_state: RoleCoverState
    state_digest: str


@dataclass(frozen=True, slots=True)
class CCE8FiniteCertificate:
    schema_id: str
    schema_version: str
    request: CCE8FiniteRequest
    theorem_ids: tuple[str, ...]
    source_ledger: tuple[tuple[str, str], ...]
    initial_state: FiniteRoleCoverState
    terminal_state: FiniteRoleCoverState
    operation_trace: tuple[tuple[str, str], ...]
    group_law_ledger: tuple[tuple[str, bool], ...]
    previous_checkpoint_digest: str | None
    verifier_version: str
    canonical_certificate_digest: str


@dataclass(frozen=True, slots=True)
class CertifiedFiniteRoleCoverResult:
    request: CCE8FiniteRequest
    certificate: CCE8FiniteCertificate


def _finite_state(jet: FiniteRoleJet, labels: tuple[str, str, str], selected_role: str) -> FiniteRoleCoverState:
    channel_state = _state(jet.order2_jet(), labels, selected_role)
    unsigned = {
        "jet": jet,
        "role_labels": labels,
        "selected_role": selected_role,
        "selected_chart_label": channel_state.selected_chart_label,
        "order2_channel_state": channel_state,
    }
    return FiniteRoleCoverState(**unsigned, state_digest=canonical_digest(unsigned))


def _assemble_finite(request: CCE8FiniteRequest, previous_checkpoint_digest: str | None = None) -> CCE8FiniteCertificate:
    if request.requested_scope != "paper_i_arbitrary_finite_role_cover" or request.source_lock_digest != PAPER_I_DIGEST:
        raise RoleCoverError("StageDependencyUnavailable", "canonical_paper_i_scope", "request does not bind the frozen Paper-I finite-order source")
    source_ledger = _source_ledger()
    initial = _finite_state(request.jet, ROLES, request.selected_role)
    jet, labels = request.jet, ROLES
    trace = []
    if request.operation_word == "e":
        trace.append(("e", jet.digest))
    else:
        for generator in request.operation_word:
            jet = _finite_act_s(jet) if generator == "s" else _finite_act_t(jet)
            labels = _permute_labels(labels, generator)
            trace.append((generator, canonical_digest((jet, labels))))
    terminal = _finite_state(jet, labels, request.selected_role)
    laws = finite_role_group_laws(request.jet)
    if not all(value for _, value in laws):
        raise RoleCoverError("RechartInverseMismatch", "finite_s3_group_laws", "the exact finite-order S3 laws failed")
    expected_kappa = tuple(initial.order2_channel_state.kappa_channels[ROLES.index(label)] for label in labels)
    if terminal.order2_channel_state.kappa_channels != expected_kappa:
        raise RoleCoverError("RolePermutationMismatch", "finite_channel_account_transform", "order-2 channel projection did not follow the role permutation")
    unsigned = {
        "schema_id": "cella.continuation.cce8_finite_role_cover_certificate",
        "schema_version": "1.0",
        "request": request,
        "theorem_ids": FINITE_THEOREM_IDS,
        "source_ledger": source_ledger,
        "initial_state": initial,
        "terminal_state": terminal,
        "operation_trace": tuple(trace),
        "group_law_ledger": laws,
        "previous_checkpoint_digest": previous_checkpoint_digest,
        "verifier_version": "cella.continuation.cce8.finite.verifier.v1",
    }
    return CCE8FiniteCertificate(**unsigned, canonical_certificate_digest=canonical_digest(unsigned))


def continue_finite_role_cover_certified(request: CCE8FiniteRequest) -> CertifiedFiniteRoleCoverResult | Refusal:
    try:
        return CertifiedFiniteRoleCoverResult(request, _assemble_finite(request))
    except (RoleCoverError, TypeError, ZeroDivisionError) as error:
        if isinstance(error, RoleCoverError):
            return Refusal(error.code, error.obligation, "cella.continuation.cce8.finite", False, True, error.detail)
        return Refusal("RechartDomainViolation", "exact_finite_role_arithmetic", "cella.continuation.cce8.finite", False, True, str(error))


def verify_cce8_finite_certificate(certificate: CCE8FiniteCertificate) -> bool | Refusal:
    try:
        expected = _assemble_finite(certificate.request, certificate.previous_checkpoint_digest)
    except RoleCoverError as error:
        return Refusal(error.code, error.obligation, "cella.continuation.cce8.finite.verify", False, True, error.detail)
    if canonical_json_bytes(expected) != canonical_json_bytes(certificate):
        return Refusal("RolePermutationMismatch", "exact_finite_certificate_replay", "cella.continuation.cce8.finite.verify", False, False, "certificate bytes do not replay")
    return True


def _act_s(jet: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    a, b, A, B, C = jet
    return b, a, C, B, A


def _act_t(jet: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    a, b, A, B, C = jet
    if a == 0:
        raise RoleCoverError("RechartDomainViolation", "a_nonzero", "the D-output chart is absent at a=0")
    return (
        1 / a,
        -b / a,
        -A / a**3,
        (A * b - a * B) / a**3,
        (-A * b**2 + 2 * a * b * B - a**2 * C) / a**3,
    )


def _permute_labels(labels: tuple[str, str, str], generator: str) -> tuple[str, str, str]:
    P, D, S = labels
    return (P, S, D) if generator == "s" else (D, P, S)


def _channels(jet: tuple[Fraction, ...]) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    a, b, A, B, C = jet
    if a == 0 or b == 0:
        raise RoleCoverError("RechartDomainViolation", "regular_role_chart", "a and b must be nonzero")
    lambdas = (B, (A * b - a * B) / a, (C * a - b * B) / b)
    q0 = 1 + a * a + b * b
    kappas = tuple(-(x * x) / (q0 * q0) for x in lambdas)
    return lambdas, kappas


def _state(jet: tuple[Fraction, ...], labels: tuple[str, str, str], selected_role: str) -> RoleCoverState:
    lambdas, kappas = _channels(jet)
    if any(value == 0 for value in lambdas):
        raise RoleCoverError("RoleDivisorCrossing", "channel_isotropy_clearance", "a named coupling channel vanishes")
    a, b = jet[:2]
    selected_chart_label = labels.index(selected_role)
    unsigned = {
        "active_chart": f"{labels[0]}|{labels[1]},{labels[2]}",
        "jet": jet,
        "role_labels": labels,
        "selected_role": selected_role,
        "selected_chart_label": ROLES[selected_chart_label],
        "lambda_channels": lambdas,
        "kappa_channels": kappas,
        "divisor_ledger": (("a", a), ("b", b), ("Lambda_P", lambdas[0]), ("Lambda_D", lambdas[1]), ("Lambda_S", lambdas[2])),
    }
    return RoleCoverState(**unsigned, state_digest=canonical_digest(unsigned))


def _apply_word(jet: tuple[Fraction, ...], word: str) -> tuple[tuple[Fraction, ...], tuple[str, str, str], tuple[tuple[str, str], ...]]:
    labels = ROLES
    trace = []
    if word == "e":
        return jet, labels, (("e", canonical_digest(jet)),)
    for generator in word:
        jet = _act_s(jet) if generator == "s" else _act_t(jet)
        labels = _permute_labels(labels, generator)
        trace.append((generator, canonical_digest((jet, labels))))
    return jet, labels, tuple(trace)


def _group_laws(jet: tuple[Fraction, ...]) -> tuple[tuple[str, bool], ...]:
    s2 = _act_s(_act_s(jet)) == jet
    t2 = _act_t(_act_t(jet)) == jet
    value = jet
    for _ in range(3):
        value = _act_s(_act_t(value))
    return (("s^2=e", s2), ("t^2=e", t2), ("(st)^3=e", value == jet))


def _assemble(request: CCE8Request, previous_checkpoint_digest: str | None = None) -> CCE8Certificate:
    if request.requested_scope != "paper_i_order2_role_cover" or request.source_lock_digest != PAPER_I_DIGEST:
        raise RoleCoverError("StageDependencyUnavailable", "canonical_paper_i_scope", "request does not bind the frozen Paper-I order-2 source")
    source_ledger = _source_ledger()
    initial = _state(request.jet, ROLES, request.selected_role)
    terminal_jet, terminal_labels, trace = _apply_word(request.jet, request.operation_word)
    terminal = _state(terminal_jet, terminal_labels, request.selected_role)
    laws = _group_laws(request.jet)
    if not all(value for _, value in laws):
        raise RoleCoverError("RechartInverseMismatch", "s3_group_laws", "the exact S3 laws failed")
    expected_kappa = tuple(initial.kappa_channels[ROLES.index(label)] for label in terminal_labels)
    if terminal.kappa_channels != expected_kappa:
        raise RoleCoverError("RolePermutationMismatch", "channel_account_transform", "channel account did not follow the role permutation")
    role_permutation = tuple((role, ROLES[terminal_labels.index(role)]) for role in ROLES)
    unsigned = {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "request": request,
        "theorem_ids": THEOREM_IDS,
        "source_ledger": source_ledger,
        "initial_state": initial,
        "terminal_state": terminal,
        "operation_trace": trace,
        "role_permutation": role_permutation,
        "group_law_ledger": laws,
        "channel_account_ledger": (
            ("initial_kappa_digest", canonical_digest(initial.kappa_channels)),
            ("terminal_kappa_digest", canonical_digest(terminal.kappa_channels)),
            ("permuted_initial_kappa_digest", canonical_digest(expected_kappa)),
        ),
        "selection_ledger": (
            ("selected_geometric_role", request.selected_role),
            ("initial_chart_slot", initial.selected_chart_label),
            ("terminal_chart_slot", terminal.selected_chart_label),
            ("policy", "transport role identity through exact S3 permutation"),
        ),
        "previous_checkpoint_digest": previous_checkpoint_digest,
        "verifier_version": VERIFIER_VERSION,
    }
    return CCE8Certificate(**unsigned, canonical_certificate_digest=canonical_digest(unsigned))


def continue_role_cover_certified(request: CCE8Request) -> CertifiedRoleCoverResult | Refusal:
    try:
        return CertifiedRoleCoverResult(request, _assemble(request))
    except (RoleCoverError, TypeError, ZeroDivisionError) as error:
        if isinstance(error, RoleCoverError):
            return Refusal(error.code, error.obligation, "cella.continuation.cce8", False, True, error.detail)
        return Refusal("RechartDomainViolation", "exact_role_arithmetic", "cella.continuation.cce8", False, True, str(error))


def verify_cce8_certificate(certificate: CCE8Certificate) -> bool | Refusal:
    try:
        expected = _assemble(certificate.request, certificate.previous_checkpoint_digest)
    except RoleCoverError as error:
        return Refusal(error.code, error.obligation, "cella.continuation.cce8.verify", False, True, error.detail)
    if canonical_json_bytes(expected) != canonical_json_bytes(certificate):
        return Refusal("RolePermutationMismatch", "exact_certificate_replay", "cella.continuation.cce8.verify", False, False, "certificate bytes do not replay")
    return True


def released_cce8_request(word: str = "st", selected_role: str = "P") -> CCE8Request:
    return CCE8Request(
        request_id=f"cce8-paper-i-order2-{word}-{selected_role.lower()}",
        jet=(Fraction(-3, 2), Fraction(-1, 2), Fraction(-13, 4), Fraction(-5, 4), Fraction(-1, 4)),
        operation_word=word,
        selected_role=selected_role,
    )


def released_cce8_finite_request(word: str = "st", selected_role: str = "P") -> CCE8FiniteRequest:
    jet = FiniteRoleJet(
        4,
        (
            (1, 0, Fraction(-3, 2)), (0, 1, Fraction(-1, 2)),
            (2, 0, Fraction(-13, 8)), (1, 1, Fraction(-5, 4)), (0, 2, Fraction(-1, 8)),
            (3, 0, Fraction(2, 7)), (2, 1, Fraction(-3, 11)),
            (1, 2, Fraction(5, 13)), (0, 3, Fraction(7, 17)),
            (4, 0, Fraction(1, 19)), (2, 2, Fraction(-2, 23)), (0, 4, Fraction(3, 29)),
        ),
    )
    return CCE8FiniteRequest(f"cce8-paper-i-order4-{word}-{selected_role.lower()}", jet, word, selected_role)


def _operations(result: CertifiedRoleCoverResult) -> tuple[str, ...]:
    return ("bind_paper_i", "admit_regular_role_locus", "apply_exact_rechart_word", "transport_role_labels", "replay_channel_account", "seal_certificate")


def make_cce8_checkpoint(result: CertifiedRoleCoverResult, prefix_length: int = 3, previous: CCE8Checkpoint | None = None) -> CCE8Checkpoint:
    operations = _operations(result)
    if not 0 <= prefix_length <= len(operations):
        raise ValueError("invalid checkpoint prefix length")
    unsigned = {
        "schema_id": "cella.continuation.cce8_checkpoint.v1",
        "request_digest": result.request.digest,
        "certificate_digest": result.certificate.canonical_certificate_digest,
        "certified_prefix": operations[:prefix_length],
        "remaining_operations_digest": canonical_digest(operations[prefix_length:]),
        "previous_checkpoint_digest": previous.checkpoint_digest if previous else None,
    }
    return CCE8Checkpoint(**unsigned, checkpoint_digest=canonical_digest(unsigned))


def verify_cce8_checkpoint(checkpoint: CCE8Checkpoint, result: CertifiedRoleCoverResult, previous: CCE8Checkpoint | None = None) -> bool:
    operations = _operations(result)
    unsigned = {name: getattr(checkpoint, name) for name in ("schema_id", "request_digest", "certificate_digest", "certified_prefix", "remaining_operations_digest", "previous_checkpoint_digest")}
    return (
        checkpoint.checkpoint_digest == canonical_digest(unsigned)
        and checkpoint.request_digest == result.request.digest
        and checkpoint.certificate_digest == result.certificate.canonical_certificate_digest
        and checkpoint.certified_prefix == operations[:len(checkpoint.certified_prefix)]
        and checkpoint.remaining_operations_digest == canonical_digest(operations[len(checkpoint.certified_prefix):])
        and checkpoint.previous_checkpoint_digest == (previous.checkpoint_digest if previous else None)
    )


def resume_cce8(checkpoint: CCE8Checkpoint, request: CCE8Request) -> CertifiedRoleCoverResult | Refusal:
    fresh = continue_role_cover_certified(request)
    if isinstance(fresh, Refusal) or not verify_cce8_checkpoint(checkpoint, fresh):
        return Refusal("RechartInverseMismatch", "checkpoint_chain", "cella.continuation.cce8.resume", False, False, "checkpoint does not replay")
    try:
        return CertifiedRoleCoverResult(request, _assemble(request, checkpoint.checkpoint_digest))
    except RoleCoverError as error:
        return Refusal(error.code, error.obligation, "cella.continuation.cce8.resume", False, True, error.detail)


__all__ = [
    "CCE8Certificate", "CCE8Checkpoint", "CCE8FiniteCertificate",
    "CCE8FiniteRequest", "CCE8Request", "CertifiedFiniteRoleCoverResult",
    "CertifiedRoleCoverResult", "FiniteRoleCoverState", "FiniteRoleJet",
    "FiniteTowerNaturalityWitness",
    "RoleBoundaryEvent", "RoleCoverState", "act_finite_role_jet",
    "classify_role_boundary", "continue_finite_role_cover_certified",
    "continue_role_cover_certified", "finite_jet_from_order2",
    "finite_role_group_laws", "finite_tower_naturality", "make_cce8_checkpoint", "released_cce8_finite_request",
    "released_cce8_request", "resume_cce8", "verify_cce8_certificate", "verify_cce8_checkpoint",
    "truncate_finite_role_jet", "verify_cce8_finite_certificate",
    "verify_finite_tower_naturality",
]
