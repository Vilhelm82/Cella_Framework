"""The cell: a computed result that carries its own account.

Admission: A-001 (PROPOSED — contract stub; implementation lands when the record
is ADMITTED).

Contract
--------
A Cell is (value, residue). The defining identity, checked not assumed:

    value ⊕ residue == TRUE OBJECT        (residue in the exact carrier), or
    residue is a Refusal token            (and the cell names why no true
                                           object is recoverable)

- ``value`` is always representable (exact tower: Fraction or QSqrt).
- ``reconstruct()`` returns the true object exactly, or raises never — a cell
  whose residue is a token reports the token.
- Cells are immutable. Operations on cells produce new cells whose residues
  are composed by the residue algebra (see residue.py), never dropped.
- No float enters or leaves a Cell on any verdict path.
"""

from __future__ import annotations


class Cell:
    """(value, residue) — see module contract. Not yet implemented (Gate G0)."""

    def __init__(self, value, residue):
        raise NotImplementedError("Gate G0 open: Cell lands with admission A-001")

    def reconstruct(self):
        """Return the true object exactly, or the refusal token. Never a guess."""
        raise NotImplementedError

    def is_refusal(self) -> bool:
        raise NotImplementedError
