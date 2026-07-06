"""Observation maps — where every M-residue is born.

Admission A-001 (ESTABLISHED). Gate G0.4 certifies this implementation.

Design note (settled by the G0.2 campaign, not a stub compromise): an
ObservationMap models LOSSY OBSERVATION — species M and refusals. It does
NOT model representation changes: the campaign proved R is a *declared
parameter action* (a Residue R absorbed into an Account), not an
observation of data — conflating the two is precisely the false-alarm
mutant the Stage-C battery kills. The earlier stub's `species` parameter
is therefore gone, by theorem rather than taste.

Contract
--------
- ``fn(T)`` returns either ``("ok", value, residue_payload)`` — value and
  residue on the exact tower, value ⊕ residue == T — or a ``Refusal``.
- ``apply(T)`` always returns a Cell: a value cell or a refusal cell.
  It never raises for a data condition and never emits NaN.
- ``then(other)`` composes: residues add on the module (G0.1); a refusal
  at any step short-circuits to a refusal cell (refuse-not-lie).
"""

from __future__ import annotations

from .cell import Cell
from .refusal import Refusal
from .residue import madd


class ObservationMap:
    """A lossy map with a typed, composable defect."""

    __slots__ = ("_name", "_fn")

    def __init__(self, name: str, fn):
        if not isinstance(name, str) or not name:
            raise ValueError("an observation map must be named")
        object.__setattr__(self, "_name", name)
        object.__setattr__(self, "_fn", fn)

    def __setattr__(self, *_):
        raise AttributeError("ObservationMap is immutable")

    @property
    def name(self) -> str:
        return self._name

    def apply(self, true_object) -> Cell:
        out = self._fn(true_object)
        if isinstance(out, Refusal):
            return Cell(None, out)
        tag, value, residue = out
        if tag != "ok":
            raise ValueError(f"observation fn returned unknown tag {tag!r}")
        return Cell(value, residue)

    def then(self, other: "ObservationMap") -> "ObservationMap":
        """self, then other — one map whose defect is the composed account."""

        def composed(true_object):
            first = self._fn(true_object)
            if isinstance(first, Refusal):
                return first
            _, v1, r1 = first
            second = other._fn(v1)
            if isinstance(second, Refusal):
                return second
            _, v2, r2 = second
            return ("ok", v2, madd(r1, r2))

        return ObservationMap(f"{self._name}>>{other._name}", composed)

    def __repr__(self):
        return f"ObservationMap({self._name!r})"
