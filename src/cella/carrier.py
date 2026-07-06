"""Carrier extraction and the gauge-normal form — gate G1.0.

The mathematics is certified in-repo, never imported on documentary status:
    RC-2 (`verification/recert_normal_form.py`, b21992f3) — H_perp uniqueness,
         O the complete same-g invariant, general-n note.
    RC-1 (`verification/recert_transport_law.py`, 4ad5a6eb) — O gauge-
         invariance and linearity; the labeled channel triple.
    RC-4 (`verification/recert_role_channels.py`, 3d7ed1bf) — the n=3 role/
         channel layer, used here ONLY as a cross-check.

Design freeze (ROADMAP) binds this module:
- O is read from H DIRECTLY by the general-n formula; no channel pathway.
- Channel recovery is an n=3 CROSS-CHECK only; calling it at n != 3 is an
  API-contract error (ValueError), not a data condition.
- Every input is a ConstraintBlock; len > 1 refuses CODIM_UNSUPPORTED.
- Certificates state their tier (see TIER).

LABEL-CONVENTION CASE LAW (2026-07-06): channel triples are NEVER positional
without labels. The slot order here is pinned by CHANNEL_SLOTS, adjacent to
the function that emits it; use `as_labeled` for any display or comparison.
"""

from __future__ import annotations

from fractions import Fraction

from .cell import Cell
from .jet import ConstraintBlock
from .refusal import Refusal

TIER = "tier: local; codim-1; order 2; jets over Q certified"

CHANNEL_SLOTS = ("kc", "kint", "ks")   # coupling, INTERACTION (middle), self


def _zeros_like(x):
    if isinstance(x, tuple):
        return tuple(_zeros_like(i) for i in x)
    return Fraction(0)


def _block_refusal(block) -> Refusal | None:
    """Refusal precedence (PREREG P5): block shape first, then gradient strata."""
    if len(block) > 1:
        return Refusal("CODIM_UNSUPPORTED",
                       f"constraint system of {len(block)} constraints "
                       "(codimension >= 2)")
    g = block.jets[0].g
    zero = [i for i, x in enumerate(g) if x == 0]
    if len(zero) == len(g):
        return Refusal("SINGULAR_GRADIENT",
                       "vanishing gradient: no surface direction at the base "
                       "point")
    if zero:
        return Refusal("ROLE_CHART_UNAVAILABLE",
                       "zero gradient component(s) at index set "
                       f"{{{', '.join(map(str, zero))}}}: no output chart in "
                       "those directions")
    return None


def carrier(block: ConstraintBlock) -> Cell:
    """The gauge-invariant carrier O, upper triangle in lex pair order.

    O_ij = H_ij - g_i*H_jj/(2*g_j) - g_j*H_ii/(2*g_i)   (RC-2; generic n)
    """
    if not isinstance(block, ConstraintBlock):
        raise TypeError("carrier takes a ConstraintBlock")
    ref = _block_refusal(block)
    if ref is not None:
        return Cell(None, ref)
    jet = block.jets[0]
    g, H, n = jet.g, jet.h, jet.n
    O = tuple(H[i][j] - g[i] * H[j][j] / (2 * g[j]) - g[j] * H[i][i] / (2 * g[i])
              for i in range(n) for j in range(i + 1, n))
    return Cell(O, _zeros_like(O))


def normal_form(block: ConstraintBlock) -> Cell:
    """The gauge-normal representative H_perp: zero diagonal, off-diagonal O.

    Canonical: every gauge H + g a^T + a g^T has the same H_perp (RC-2
    uniqueness; certified operationally at this gate)."""
    c = carrier(block)
    if c.is_refusal():
        return c
    n, O = block.n, c.value
    pos = {}
    k = 0
    for i in range(n):
        for j in range(i + 1, n):
            pos[(i, j)] = k
            k += 1
    Hp = tuple(tuple(Fraction(0) if i == j
                     else O[pos[(min(i, j), max(i, j))]]
                     for j in range(n)) for i in range(n))
    return Cell(Hp, _zeros_like(Hp))


def _det(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    total = Fraction(0)
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in M[1:]]
        total += (-1) ** j * M[0][j] * _det(minor)
    return total


def channels_n3_crosscheck(block: ConstraintBlock) -> Cell:
    """The three-channel decomposition (kc, kint, ks) — n=3 CROSS-CHECK ONLY.

    Slot order is CHANNEL_SLOTS: (kc, kint, ks) — interaction in the MIDDLE.
    This is not the carrier pathway (freeze rule 3); it exists to cross-check
    the carrier path against RC-1/RC-4 pinned values at n = 3."""
    if not isinstance(block, ConstraintBlock):
        raise TypeError("channels_n3_crosscheck takes a ConstraintBlock")
    if block.n != 3:
        raise ValueError("channel recovery is an n=3 cross-check only — the "
                         "carrier path is the general-n route (design freeze)")
    ref = _block_refusal(block)
    if ref is not None:
        return Cell(None, ref)
    jet = block.jets[0]
    g, H = jet.g, jet.h

    def density(t, u):
        M = [[(t if i != j else u) * H[i][j] for j in range(3)]
             for i in range(3)]
        B = [[Fraction(0)] + list(g)] + [[g[i]] + M[i] for i in range(3)]
        return -_det(B)

    q = sum(x * x for x in g)
    f0 = density(Fraction(0), Fraction(1))
    f1 = density(Fraction(1), Fraction(1))
    f2 = density(Fraction(2), Fraction(1))
    c_t2 = (f2 - 2 * f1 + f0) / 2          # t^2  -> coupling
    c_tu = f1 - f0 - c_t2                  # t*u  -> interaction
    c_u2 = f0                              # u^2  -> self
    triple = (c_t2 / q ** 2, c_tu / q ** 2, c_u2 / q ** 2)
    return Cell(triple, _zeros_like(triple))


def as_labeled(channel_cell: Cell) -> dict:
    """Labeled view of a channel cell — the only sanctioned way to read one."""
    if channel_cell.is_refusal():
        raise ValueError("refusal cell has no channels to label")
    d = dict(zip(CHANNEL_SLOTS, channel_cell.value))
    d["K_G"] = sum(channel_cell.value)
    return d
