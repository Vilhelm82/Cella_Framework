"""The two-ledger residue algebra — implemented from the certified design.

Design authority (all in-repo, all re-proven, none imported):
    Stage A close — canonical account, order-independence, purity      [T-A]
    Stage B close — attribution theorem: rho_M* = Sum E + G_e(Sum a)   [F1/F3]
    Stage C close — asymmetry law (d stays R, e generates M), no
                    multiplicative escape, owned holonomy, the
                    false-alarm/miss discriminating pair
Admission A-002. Gates G0.1 / G0.2 certify this implementation
(tests/gate_01.py, tests/gate_02.py).

Species
-------
M — measurement defect: an element of a free Q-module (Fraction scalar,
    tuple vector, or tuple-of-tuples matrix). Composes by exact addition.
    Membership criterion: it affects reconstruction.
R — representation defect: a GROUP PARAMETER `a` acting through a declared
    base `g` (at order 2: translation by G_g(a)). Composes by parameter
    addition AT THE SAME BASE ONLY; a base change is an epoch boundary
    (two-epoch law, TC-P2) and is never silently merged.

Account discipline (theorems, not conventions)
----------------------------------------------
- The two ledgers never mix in composition (design freeze rule 1).
- Cross-terms — execution at a defective base — are computed at the
  geometry layer (closed forms F1/F3) and folded into M EXPLICITLY via
  `Account.fold_into_m`: membership by criterion, never by pedigree.
- Holonomy between two accounts of the same truth is OWNED, not denied:
  it equals the M-ledger gap exactly (RC-3, TC-P5) — `Account.holonomy_gap`.
- No float touches any payload: a float is a TypeError, not a warning.
"""

from __future__ import annotations

from fractions import Fraction

SPECIES_M = "M"
SPECIES_R = "R"

_SCALARS = (Fraction, int)


def _validate_exact(x, ctx="payload"):
    if isinstance(x, (float, complex)):
        raise TypeError(f"{ctx} contains {type(x).__name__}: floats are forbidden "
                        "on verdict paths (exact tower only)")
    if isinstance(x, _SCALARS):
        return
    if isinstance(x, tuple):
        for item in x:
            _validate_exact(item, ctx)
        return
    raise TypeError(f"{ctx} must be Fraction/int or (nested) tuple thereof, "
                    f"got {type(x).__name__}")


def madd(x, y):
    """Exact addition on the free Q-module (scalars and nested tuples)."""
    if isinstance(x, _SCALARS) and isinstance(y, _SCALARS):
        return Fraction(x) + Fraction(y)
    if isinstance(x, tuple) and isinstance(y, tuple) and len(x) == len(y):
        return tuple(madd(a, b) for a, b in zip(x, y))
    raise TypeError("module addition requires operands of identical shape")


def msub(x, y):
    if isinstance(x, _SCALARS) and isinstance(y, _SCALARS):
        return Fraction(x) - Fraction(y)
    if isinstance(x, tuple) and isinstance(y, tuple) and len(x) == len(y):
        return tuple(msub(a, b) for a, b in zip(x, y))
    raise TypeError("module subtraction requires operands of identical shape")


def is_zero(x) -> bool:
    if isinstance(x, _SCALARS):
        return x == 0
    return all(is_zero(i) for i in x)


class Residue:
    """A typed defect: species M (module element) or R (base, parameter)."""

    __slots__ = ("_species", "_payload", "_base")

    def __init__(self, species: str, payload, base=None):
        if species not in (SPECIES_M, SPECIES_R):
            raise ValueError(f"unknown species {species!r}")
        _validate_exact(payload)
        if species == SPECIES_M:
            if base is not None:
                raise ValueError("species M carries no base")
        else:
            if base is None:
                raise ValueError("species R requires its acting base")
            _validate_exact(base, "base")
            if not isinstance(base, tuple):
                raise TypeError("base must be a tuple (the gradient g)")
        object.__setattr__(self, "_species", species)
        object.__setattr__(self, "_payload", payload)
        object.__setattr__(self, "_base", base)

    def __setattr__(self, *_):
        raise AttributeError("Residue is immutable")

    @property
    def species(self):
        return self._species

    @property
    def payload(self):
        return self._payload

    @property
    def base(self):
        return self._base

    def compose(self, other: "Residue") -> "Residue":
        """Same-species composition. M: module addition. R: parameter addition
        at the SAME base only — a differing base is an epoch boundary, which is
        an Account operation, never a Residue operation."""
        if not isinstance(other, Residue) or other._species != self._species:
            raise TypeError("compose requires a Residue of the same species")
        if self._species == SPECIES_M:
            return Residue(SPECIES_M, madd(self._payload, other._payload))
        if self._base != other._base:
            raise ValueError("R-composition across bases: epoch boundary — "
                             "absorb into an Account instead (two-epoch law)")
        return Residue(SPECIES_R, madd(self._payload, other._payload), self._base)

    def __eq__(self, other):
        if not isinstance(other, Residue):
            return NotImplemented
        return (self._species, self._payload, self._base) == \
               (other._species, other._payload, other._base)

    def __repr__(self):
        b = f", base={self._base!r}" if self._base is not None else ""
        return f"Residue({self._species}, {self._payload!r}{b})"


class Account:
    """The two-ledger account: an M-ledger (module element) and an R-ledger
    (ordered epochs of (base, parameter)). Never mixed by composition."""

    __slots__ = ("_m", "_epochs")

    def __init__(self, m=None, epochs=()):
        if m is not None:
            _validate_exact(m, "m-ledger")
        for base, param in epochs:
            _validate_exact(base, "epoch base")
            _validate_exact(param, "epoch parameter")
        object.__setattr__(self, "_m", m)
        object.__setattr__(self, "_epochs", tuple((b, p) for b, p in epochs))

    def __setattr__(self, *_):
        raise AttributeError("Account is immutable")

    @property
    def m_total(self):
        """The M-ledger: what must be subtracted to reconstruct truth."""
        return self._m

    @property
    def r_epochs(self):
        """The R-ledger: ordered (base, parameter) epochs — pure representation
        motion; provably without effect on any declared invariant (T-A purity)."""
        return self._epochs

    def absorb(self, res: Residue) -> "Account":
        """Compose one more observed defect into the account (order-safe on the
        certified class: Stage A / TC-P2)."""
        if res.species == SPECIES_M:
            m = res.payload if self._m is None else madd(self._m, res.payload)
            return Account(m, self._epochs)
        if self._epochs and self._epochs[-1][0] == res.base:
            merged = self._epochs[:-1] + \
                ((res.base, madd(self._epochs[-1][1], res.payload)),)
            return Account(self._m, merged)
        return Account(self._m, self._epochs + ((res.base, res.payload),))

    def fold_into_m(self, cross_term) -> "Account":
        """Fold a computed cross-term into the M-ledger — the Stage-B
        attribution move (rho_M* = Sum E + G_e(Sum a)). The caller computes the
        term at the geometry layer (closed forms F1/F3); membership is decided
        by the reconstruction criterion, never by pedigree."""
        _validate_exact(cross_term, "cross-term")
        m = cross_term if self._m is None else madd(self._m, cross_term)
        return Account(m, self._epochs)

    def holonomy_gap(self, other: "Account"):
        """The owned holonomy against another account of the same truth:
        exactly the M-ledger gap (RC-3 / TC-P5). Zero defines the commuting
        class — account equality, not operation exactness."""
        if (self._m is None) != (other._m is None):
            raise TypeError("holonomy gap requires comparable M-ledgers")
        if self._m is None:
            return Fraction(0)
        return msub(other._m, self._m)

    def __eq__(self, other):
        if not isinstance(other, Account):
            return NotImplemented
        return self._m == other._m and self._epochs == other._epochs

    def __repr__(self):
        return f"Account(m={self._m!r}, epochs={self._epochs!r})"
