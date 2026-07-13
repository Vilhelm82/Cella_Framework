"""The cell: a computed result that carries its own account.

Admission A-001 (ESTABLISHED). Gates: G0 (closed — first round-trip),
G0.4 (refusal cells; tower values).

Contract
--------
A Cell is (value, residue):

    value ⊕ residue == TRUE OBJECT          (residue on the exact tower), or
    residue is a Refusal                    (value is None; the cell names
                                             exactly why no truth is
                                             recoverable — never NaN, never
                                             an exception)

- values/residues live on the exact tower: Fraction, int, QSqrt, or nested
  tuples thereof. Floats are TypeErrors, not warnings.
- ``reconstruct()`` returns the true object exactly, or the Refusal.
- Cells are immutable.
"""

from __future__ import annotations

from .refusal import Refusal
from .residue import _validate_exact, madd


class Cell:
    """(value, residue) on the exact tower, or a refusal cell."""

    __slots__ = ("_value", "_residue")

    def __init__(self, value, residue):
        if isinstance(residue, Refusal):
            if value is not None:
                raise ValueError("a refusal cell carries no value — the "
                                 "refusal stands where the value would be")
        else:
            _validate_exact(value, "value")
            _validate_exact(residue, "residue")
        object.__setattr__(self, "_value", value)
        object.__setattr__(self, "_residue", residue)

    def __setattr__(self, *_):
        raise AttributeError("Cell is immutable")

    @property
    def value(self):
        """The representable value; None iff this is a refusal cell."""
        return self._value

    @property
    def residue(self):
        """The typed defect — exact leftover, or the Refusal."""
        return self._residue

    def is_refusal(self) -> bool:
        return isinstance(self._residue, Refusal)

    def reconstruct(self):
        """The true object exactly — or the Refusal. Never a guess."""
        if self.is_refusal():
            return self._residue
        return madd(self._value, self._residue)

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return NotImplemented
        return self._value == other._value and self._residue == other._residue

    def __hash__(self):
        return hash((self._value, self._residue))

    def __repr__(self):
        return f"Cell(value={self._value!r}, residue={self._residue!r})"
