"""Order-2 jets and constraint blocks — Layer 1's input objects.

Admissions: A-007 (carrier dominance, mathematical scope), A-009 (tokens).
Gate G1.0 certifies this implementation.

Design freeze (ROADMAP) binds this module:
- Constraint inputs are BLOCKS (a typed system of constraints). The API can
  always express what the theory cannot yet compute; implementations refuse
  by token, never by exception, on scope boundaries (freeze rule 3).
- Generic n throughout — nothing here knows n = 3.
- These are typed, validated, immutable carriers of exact jet data; no
  computation lives here.
"""

from __future__ import annotations

from .residue import _validate_exact


def _as_matrix(H, n):
    """Coerce a sequence-of-sequences to an n x n tuple-of-tuples."""
    rows = tuple(tuple(r) for r in H)
    if len(rows) != n or any(len(r) != n for r in rows):
        raise ValueError("H must be n x n, matching the gradient length")
    return rows


class Jet2:
    """The order-2 jet of one scalar constraint at a base point:
    (point, gradient g, symmetric Hessian H), all on the exact tower."""

    __slots__ = ("_point", "_g", "_h")

    def __init__(self, point, g, H):
        point, g = tuple(point), tuple(g)
        _validate_exact(point, "point")
        _validate_exact(g, "gradient")
        n = len(g)
        if n < 2:
            raise ValueError("a jet needs at least two variables")
        if len(point) != n:
            raise ValueError("point and gradient must have the same length")
        H = _as_matrix(H, n)
        _validate_exact(H, "hessian")
        for i in range(n):
            for j in range(i + 1, n):
                if H[i][j] != H[j][i]:
                    raise ValueError("H must be symmetric")
        object.__setattr__(self, "_point", point)
        object.__setattr__(self, "_g", g)
        object.__setattr__(self, "_h", H)

    def __setattr__(self, *_):
        raise AttributeError("Jet2 is immutable")

    @property
    def n(self) -> int:
        return len(self._g)

    @property
    def point(self):
        return self._point

    @property
    def g(self):
        return self._g

    @property
    def h(self):
        return self._h

    def __eq__(self, other):
        if not isinstance(other, Jet2):
            return NotImplemented
        return (self._point, self._g, self._h) == \
               (other._point, other._g, other._h)

    def __repr__(self):
        return f"Jet2(n={self.n}, point={self._point!r})"


class ConstraintBlock:
    """A typed system of constraints at one shared base point.

    The block is the ONLY constraint input type (freeze rule 3): codim-1
    implementations receive a block and refuse len > 1 with a typed token —
    the API expresses systems today, the theory earns them later.
    """

    __slots__ = ("_jets",)

    def __init__(self, jets):
        jets = tuple(jets)
        if not jets:
            raise ValueError("a block needs at least one constraint")
        for j in jets:
            if not isinstance(j, Jet2):
                raise TypeError("a block holds Jet2 constraints only")
        n0, p0 = jets[0].n, jets[0].point
        for j in jets[1:]:
            if j.n != n0 or j.point != p0:
                raise ValueError("all constraints in a block share the same "
                                 "point and dimension")
        object.__setattr__(self, "_jets", jets)

    def __setattr__(self, *_):
        raise AttributeError("ConstraintBlock is immutable")

    @property
    def jets(self):
        return self._jets

    @property
    def n(self) -> int:
        return self._jets[0].n

    @property
    def point(self):
        return self._jets[0].point

    def __len__(self):
        return len(self._jets)

    def __repr__(self):
        return f"ConstraintBlock(k={len(self._jets)}, n={self.n})"
