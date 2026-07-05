"""The exact number tower: ℚ and ℚ(√q).

Admission: A-003 (PROPOSED).

Contract
--------
- Rung 0: ``fractions.Fraction`` (stdlib) — exact rational arithmetic.
- Rung 1: ``QSqrt(a, b, q)`` representing a + b·√q with a, b ∈ ℚ and q a
  positive non-square rational. Add/sub/mul/div exact; equality is exact
  structural equality after normal form.
- Why exactly two rungs: the parity law — even-order invariants are rational,
  odd-order invariants carry exactly one √q. Two rungs cover the whole tower.
- No float constructor is reachable from any verdict path. Conversion to
  float exists ONLY on the display path and is marked lossy at type level.
"""

from __future__ import annotations


class QSqrt:
    """a + b·√q, exact. Not yet implemented (Gate G0.3)."""

    def __init__(self, a, b, q):
        raise NotImplementedError("Gate G0.3 open: lands with A-003")
