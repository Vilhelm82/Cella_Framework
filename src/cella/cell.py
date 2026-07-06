"""The cell: a computed result that carries its own account.

Admission: A-001 (ESTABLISHED — the dominance case is in ADMISSIONS.md; the
criterion forces this object: exact reconstruction where possible, typed
non-recovery where not, composable defects).

Contract
--------
A Cell is (value, residue). The defining identity, checked not assumed:

    value ⊕ residue == TRUE OBJECT

- ``value`` and ``residue`` live on the exact tower (Fraction / int now;
  QSqrt joins at Gate G0.3).
- ``reconstruct()`` returns the true object exactly. Never a guess.
- Cells are immutable.
- No float enters a Cell on any verdict path — a float argument is a
  TypeError, not a warning (tolerance-leak is a type error here).

Current scope (grows by gate, never silently):
- G0 (closed): exact residues on the rational-op class.
- G0.1: residues become Residue objects with species and composition.
- G0.3: QSqrt values join the tower.
- G0.4: refusal cells — until then ``is_refusal()`` is honestly False,
  because no Refusal can yet be constructed.
"""

from __future__ import annotations

from fractions import Fraction

_EXACT_TYPES = (Fraction, int)


class Cell:
    """(value, residue) on the exact tower. Gate G0: closed."""

    __slots__ = ("_value", "_residue")

    def __init__(self, value, residue):
        for name, x in (("value", value), ("residue", residue)):
            if isinstance(x, (float, complex)):
                raise TypeError(
                    f"{name} is {type(x).__name__}: floats are forbidden on "
                    "verdict paths (exact tower only)"
                )
            if not isinstance(x, _EXACT_TYPES):
                raise TypeError(
                    f"{name} must be exact (Fraction or int), got {type(x).__name__}"
                )
        object.__setattr__(self, "_value", Fraction(value))
        object.__setattr__(self, "_residue", Fraction(residue))

    def __setattr__(self, name, val):  # immutability
        raise AttributeError("Cell is immutable")

    @property
    def value(self) -> Fraction:
        """The representable value — what a lossy observation reported."""
        return self._value

    @property
    def residue(self) -> Fraction:
        """The typed defect — what the observation discarded, kept exactly."""
        return self._residue

    def reconstruct(self) -> Fraction:
        """The true object, exactly: value ⊕ residue."""
        return self._value + self._residue

    def is_refusal(self) -> bool:
        """Refusal cells land at Gate G0.4; no Refusal is constructible yet."""
        return False

    def __eq__(self, other) -> bool:
        if not isinstance(other, Cell):
            return NotImplemented
        return self._value == other._value and self._residue == other._residue

    def __hash__(self) -> int:
        return hash((self._value, self._residue))

    def __repr__(self) -> str:
        return f"Cell(value={self._value!r}, residue={self._residue!r})"
