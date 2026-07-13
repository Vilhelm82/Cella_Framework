"""Canonical wrapper-neutral problem IR for route analysis.

Lowering normalizes the request's mathematical context into typed structure
recognizers can query uniformly.  Host object identities in external bindings
remain opaque; this IR carries only declared structure and never becomes a
public mathematical object model.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from ..api.request import PathfinderRequest
from ..serialize.canonical import canonical_json_bytes
from .values import FrozenValue


@dataclass(frozen=True, slots=True)
class RingDeclaration:
    """A declared ambient ring; identities belong to the wrapper."""

    variables: tuple[str, ...]
    weights: tuple[int, ...] = ()
    coefficient_domain: str = "QQ"
    characteristic: int | None = 0
    monomial_order: str = "GRevLex"

    def __post_init__(self) -> None:
        if not self.variables:
            raise ValueError("a ring declaration requires at least one variable")
        if len(set(self.variables)) != len(self.variables):
            raise ValueError("ring variables must be unique")
        if self.weights and len(self.weights) != len(self.variables):
            raise ValueError("weight vector length must match the variable list")

    def weight_vector(self) -> tuple[int, ...]:
        return self.weights if self.weights else tuple(1 for _ in self.variables)


@dataclass(frozen=True, slots=True)
class IdealDeclaration:
    """A named ideal presentation given by generator strings."""

    name: str
    generators: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.generators:
            raise ValueError("an ideal declaration requires a name and generators")


@dataclass(frozen=True, slots=True)
class DomainStratum:
    """One declared assumption stratum (open condition, excluded locus, ...)."""

    name: str
    condition: str
    status: str = "assumed"  # assumed | excluded | boundary

    def __post_init__(self) -> None:
        if self.status not in {"assumed", "excluded", "boundary"}:
            raise ValueError(f"unknown stratum status: {self.status}")


@dataclass(frozen=True, slots=True)
class SymmetryDeclaration:
    """Declared symmetry/orbit structure; admission stays with the recognizer."""

    kind: str  # sign_orbit | permutation | group_action
    group_name: str = ""
    orbit_size: int = 0
    detail: tuple[tuple[str, FrozenValue], ...] = ()


@dataclass(frozen=True, slots=True)
class CoverDeclaration:
    """Declared cover/channel structure for Kummer/wreath route analysis."""

    degree: int = 0
    channels: tuple[str, ...] = ()
    base_group: str = ""
    parity_rows: tuple[tuple[int, ...], ...] = ()
    sheet_variables: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class NormalizedProblem:
    """The lowered, wrapper-neutral route-analysis view of one request."""

    request_id: str
    problem_shape: str
    operation: str
    characteristic: int | None
    ring: RingDeclaration | None
    ideals: tuple[IdealDeclaration, ...]
    expression: str | None
    strata: tuple[DomainStratum, ...]
    symmetry: SymmetryDeclaration | None
    cover: CoverDeclaration | None
    required_invariants: tuple[str, ...]
    role_channels: tuple[str, ...] = ()
    context: tuple[tuple[str, FrozenValue], ...] = field(default=())

    def ideal(self, name: str) -> IdealDeclaration | None:
        return next((item for item in self.ideals if item.name == name), None)

    def context_value(self, key: str) -> FrozenValue | None:
        return next((value for item_key, value in self.context if item_key == key), None)


def stable_problem_hash(problem: NormalizedProblem) -> str:
    return hashlib.sha256(canonical_json_bytes(problem)).hexdigest()


def _get(context: dict[str, FrozenValue], key: str) -> FrozenValue | None:
    return context.get(key)


def _as_pairs(value: FrozenValue | None) -> dict[str, FrozenValue]:
    if isinstance(value, tuple) and all(
        isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], str) for item in value
    ):
        return dict(value)  # type: ignore[arg-type]
    return {}


def _string_tuple(value: FrozenValue | None) -> tuple[str, ...]:
    if isinstance(value, tuple) and all(isinstance(item, str) for item in value):
        return tuple(value)  # type: ignore[arg-type]
    return ()


def lower_request(request: PathfinderRequest) -> NormalizedProblem:
    """Normalize the declared mathematical context; unknown keys stay opaque."""

    context = dict(request.mathematical_context)

    ring: RingDeclaration | None = None
    ring_pairs = _as_pairs(_get(context, "ring"))
    variables = _string_tuple(ring_pairs.get("variables"))
    if variables:
        raw_weights = ring_pairs.get("weights")
        weights = (
            tuple(int(w) for w in raw_weights)  # type: ignore[union-attr]
            if isinstance(raw_weights, tuple) and all(isinstance(w, int) for w in raw_weights)
            else ()
        )
        characteristic_value = ring_pairs.get("characteristic", _get(context, "characteristic"))
        ring = RingDeclaration(
            variables=variables,
            weights=weights,
            coefficient_domain=str(ring_pairs.get("coefficients", "QQ")),
            characteristic=characteristic_value if isinstance(characteristic_value, int) else None,
            monomial_order=str(ring_pairs.get("order", "GRevLex")),
        )

    ideals: list[IdealDeclaration] = []
    ideal_pairs = _as_pairs(_get(context, "ideals"))
    for name in sorted(ideal_pairs):
        generators = _string_tuple(ideal_pairs[name])
        if generators:
            ideals.append(IdealDeclaration(name=name, generators=generators))

    strata: list[DomainStratum] = []
    for entry in _get(context, "strata") or ():
        pairs = _as_pairs(entry)
        if "name" in pairs and "condition" in pairs:
            strata.append(
                DomainStratum(
                    name=str(pairs["name"]),
                    condition=str(pairs["condition"]),
                    status=str(pairs.get("status", "assumed")),
                )
            )

    symmetry: SymmetryDeclaration | None = None
    symmetry_pairs = _as_pairs(_get(context, "symmetry"))
    if symmetry_pairs:
        orbit_size = symmetry_pairs.get("orbit_size", 0)
        symmetry = SymmetryDeclaration(
            kind=str(symmetry_pairs.get("kind", "group_action")),
            group_name=str(symmetry_pairs.get("group_name", "")),
            orbit_size=int(orbit_size) if isinstance(orbit_size, int) else 0,
            detail=tuple(sorted(symmetry_pairs.items())),
        )

    cover: CoverDeclaration | None = None
    cover_pairs = _as_pairs(_get(context, "cover"))
    if cover_pairs:
        degree = cover_pairs.get("degree", 0)
        raw_rows = cover_pairs.get("parity_rows")
        parity_rows: tuple[tuple[int, ...], ...] = ()
        if isinstance(raw_rows, tuple):
            collected = []
            for row in raw_rows:
                if isinstance(row, tuple) and all(isinstance(bit, int) for bit in row):
                    collected.append(tuple(int(bit) for bit in row))
            parity_rows = tuple(collected)
        cover = CoverDeclaration(
            degree=int(degree) if isinstance(degree, int) else 0,
            channels=_string_tuple(cover_pairs.get("channels")),
            base_group=str(cover_pairs.get("base_group", "")),
            parity_rows=parity_rows,
            sheet_variables=_string_tuple(cover_pairs.get("sheet_variables")),
        )

    expression_value = _get(context, "expression")
    characteristic = _get(context, "characteristic")

    return NormalizedProblem(
        request_id=request.request_id,
        problem_shape=str(_get(context, "problem_shape") or ""),
        operation=str(_get(context, "operation") or ""),
        characteristic=characteristic if isinstance(characteristic, int) else None,
        ring=ring,
        ideals=tuple(ideals),
        expression=str(expression_value) if isinstance(expression_value, str) else None,
        strata=tuple(strata),
        symmetry=symmetry,
        cover=cover,
        required_invariants=_string_tuple(_get(context, "required_invariants")),
        role_channels=_string_tuple(_get(context, "role_channels")),
        context=request.mathematical_context,
    )
