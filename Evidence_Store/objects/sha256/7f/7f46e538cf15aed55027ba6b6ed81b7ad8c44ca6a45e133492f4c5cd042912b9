"""The sensor set — gate G1.2.

Four invariant sensors, each shipping its invariance group + blindness set +
completeness scope (A-007). Mathematics recertified in-repo at Stage 0 of the
G1.2 campaign (campaigns/G12_sensor_set/), values retrodicted never trusted:

  numerator tower   kappa_r = e_r(P Hc P) / q^(r/2)   (RC-6; Hc = offdiag H)
                    the F->tF invariant coupling tower; r=2 rung == certified
                    channel kc; self-fault blind (factor-through-Hc); parity-
                    typed (even Q, odd Q(sqrt q)) exactly like the sigma tower.
  shape moment      S_n-isotypic norms of the carrier O in the pair module
                    (RC-7). The (n-2,2) "shape" component is new at n>=4 and
                    is what scalar invariants miss at n>=5 (dimension threshold).
  localization      triangle channels Delta_S (RC-8, SHADOW_LAW Lemma 3) and the
                    support map {S : d/dt Delta_S != 0} == {S : e* subset S}.
  fingerprint       n=3 role layer (A-008): Lambda triple, A_c, faithfulness
                    det = 8*L_P*L_D*L_S/q0^6. Refuses CHANNEL_ISOTROPIC (A-010)
                    when a Lambda vanishes, ROLE_CHART_UNAVAILABLE off the chart.

Design freeze: every input is a ConstraintBlock (len>1 -> CODIM_UNSUPPORTED);
generic-n except the fingerprint, which is n=3-fenced by A-008 scope (n!=3 is an
API-contract ValueError, not a data condition). No float on any verdict path.
"""

from __future__ import annotations

import math
from fractions import Fraction
from itertools import combinations, permutations

from .carrier import carrier
from .cell import Cell
from .jet import ConstraintBlock
from .qsqrt import QSqrt
from .refusal import Refusal

TIER_SENSORS = "tier: local; codim-1; order 2; sensor set (G1.2)"


# ===================== shared exact linear algebra =====================

def _det(M):
    n = len(M)
    if n == 0:
        return Fraction(1)
    if n == 1:
        return M[0][0]
    total = Fraction(0)
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in M[1:]]
        total += (-1) ** j * M[0][j] * _det(minor)
    return total


def _e_r(A, r):
    n = len(A)
    return sum(_det([[A[i][j] for j in S] for i in S])
               for S in combinations(range(n), r))


def _is_square_rational(r: Fraction) -> bool:
    p, q = r.numerator, r.denominator
    sp, sq = math.isqrt(p), math.isqrt(q)
    return sp * sp == p and sq * sq == q


def _P_matrix(g, n, q):
    return tuple(tuple((Fraction(1) if i == j else Fraction(0))
                       - Fraction(g[i] * g[j]) / q for j in range(n))
                 for i in range(n))


def _PXP(P, X, n):
    PX = tuple(tuple(sum(P[i][k] * X[k][l] for k in range(n)) for l in range(n))
               for i in range(n))
    return tuple(tuple(sum(PX[i][k] * P[k][j] for k in range(n))
                       for j in range(n)) for i in range(n))


def _offdiag(H, n):
    return tuple(tuple(H[i][j] if i != j else Fraction(0) for j in range(n))
                 for i in range(n))


def _codim_refusal(block):
    if len(block) > 1:
        return Refusal("CODIM_UNSUPPORTED",
                       f"constraint system of {len(block)} constraints "
                       "(codimension >= 2)")
    return None


def _zeros_like(x):
    if isinstance(x, tuple):
        return tuple(_zeros_like(i) for i in x)
    return Fraction(0)


# ============================ 1. numerator tower ============================

def numerator_tower(block: ConstraintBlock) -> Cell:
    """kappa_r = (-1)^r e_r(P Hc P) / q^(r/2), r = 2..n-1, parity-typed.

    Hc = offdiag(H): the tower is a function of the coupling part alone, so a
    self-fault (a diagonal perturbation) leaves it identically fixed — exact
    blindness (RC-6). P is scale-invariant, so the tower is F->tF-invariant.
    Refuses CODIM_UNSUPPORTED and SINGULAR_GRADIENT only; like the sigma tower
    it COMPUTES on component-zero gradients (P-route needs only q != 0)."""
    if not isinstance(block, ConstraintBlock):
        raise TypeError("numerator_tower takes a ConstraintBlock")
    ref = _codim_refusal(block)
    if ref is not None:
        return Cell(None, ref)
    jet = block.jets[0]
    g, H, n = jet.g, jet.h, jet.n
    q = sum(x * x for x in g)
    if q == 0:
        return Cell(None, Refusal("SINGULAR_GRADIENT",
                    "vanishing gradient: no surface direction at the base point"))
    q = Fraction(q)
    A = _PXP(_P_matrix(g, n, q), _offdiag(H, n), n)
    out = []
    for r in range(2, n):
        c = _e_r(A, r)
        if r % 2 == 0:
            out.append(c / q ** (r // 2))
        else:
            b = -c / q ** ((r + 1) // 2)
            if b == 0:
                out.append(Fraction(0))
            elif _is_square_rational(q):
                sp = Fraction(math.isqrt(q.numerator), math.isqrt(q.denominator))
                out.append(b * sp)
            else:
                out.append(QSqrt(0, b, q))
    value = tuple(out)
    return Cell(value, _zeros_like(value))


# ============================ 2. shape moment ============================
# S_n characters via Murnaghan-Nakayama on beta-sets (fresh, exact, no import).

def _partitions(n):
    out = []

    def rec(rem, mx, acc):
        if rem == 0:
            out.append(tuple(acc)); return
        for k in range(min(rem, mx), 0, -1):
            acc.append(k); rec(rem - k, k, acc); acc.pop()
    rec(n, n, [])
    return out


def _cycle_type(p):
    n = len(p); seen = [False] * n; t = []
    for i in range(n):
        if not seen[i]:
            L = 0; j = i
            while not seen[j]:
                seen[j] = True; j = p[j]; L += 1
            t.append(L)
    return tuple(sorted(t, reverse=True))


def _mn(beta, mu):
    if not mu:
        return 1
    k, rest = mu[0], mu[1:]
    tot = 0
    for b in beta:
        if b >= k and (b - k) not in beta:
            legs = sum(1 for c in beta if (b - k) < c < b)
            tot += (-1) ** legs * _mn(frozenset((beta - {b}) | {b - k}), rest)
    return tot


def _chi(lam, mu):
    s = len(lam)
    beta = frozenset(lam[i] + (s - 1 - i) for i in range(s))
    return _mn(beta, tuple(sorted(mu, reverse=True)))


def _pairs(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def _isotypic_norm(vec, n, lam, pair_index):
    """||P_lam vec||^2 for the S_n pair-module vector `vec` (exact)."""
    d = _chi(lam, tuple([1] * n))          # dim of the irrep
    N = len(vec)
    # P_lam = (d/n!) sum_g chi(g) rho(g);  ||P vec||^2 = vec^T P vec (P proj)
    total = Fraction(0)
    nfac = math.factorial(n)
    for p in permutations(range(n)):
        c = _chi(lam, _cycle_type(p))
        if c == 0:
            continue
        # rho(p) acts on pairs: pair (i,j) -> (p[i],p[j])
        s = Fraction(0)
        for e_idx, (i, j) in enumerate(_pairs(n)):
            pi, pj = p[i], p[j]
            key = (min(pi, pj), max(pi, pj))
            s += vec[e_idx] * vec[pair_index[key]]
        total += c * s
    return Fraction(d, nfac) * total


def shape_moment(block: ConstraintBlock) -> Cell:
    """Isotypic norms (triv, std, shape) of the carrier O in the pair module.

    `shape` is the S^(n-2,2) component — dimension n(n-3)/2, absent at n=3
    (returned as 0), the content scalar invariants miss at n>=5 (RC-7). Being a
    function of O, it inherits O's chart refusals (ROLE_CHART_UNAVAILABLE off a
    component-zero gradient)."""
    if not isinstance(block, ConstraintBlock):
        raise TypeError("shape_moment takes a ConstraintBlock")
    c = carrier(block)                      # handles CODIM / SINGULAR / chart
    if c.is_refusal():
        return c
    n = block.n
    O = c.value
    pidx = {e: k for k, e in enumerate(_pairs(n))}
    triv = _isotypic_norm(O, n, (n,), pidx)
    std = _isotypic_norm(O, n, (n - 1, 1), pidx)
    shape = (_isotypic_norm(O, n, (n - 2, 2), pidx)
             if n >= 4 else Fraction(0))
    value = (triv, std, shape)
    return Cell(value, _zeros_like(value))


# ============================ 3. localization ============================

def _W(g, n):
    out = []
    for (i, j) in _pairs(n):
        w = Fraction(1)
        for k in range(n):
            if k not in (i, j):
                w *= Fraction(g[k])
        out.append(w)
    return out


def _T(g, n, S):
    d = Fraction(1)
    for m in range(n):
        if m not in S:
            d *= Fraction(g[m]) * Fraction(g[m])
    return Fraction(1) / d


def _delta_S(g, offd, n, S, pidx, W):
    nu = [Fraction(offd[e]) * W[e] for e in range(len(W))]
    es = [pidx[p] for p in combinations(S, 2)]
    loc = (sum(nu[a] * nu[a] for a in es)
           - sum(nu[a] * nu[b] for a in es for b in es if a != b))
    return _T(g, n, S) * loc


def _loc_refusal(block):
    ref = _codim_refusal(block)
    if ref is not None:
        return ref
    g = block.jets[0].g
    zero = [i for i, x in enumerate(g) if x == 0]
    if len(zero) == len(g):
        return Refusal("SINGULAR_GRADIENT",
                       "vanishing gradient: no surface direction at the base point")
    if zero:
        return Refusal("ROLE_CHART_UNAVAILABLE",
                       "zero gradient component(s) at index set "
                       f"{{{', '.join(map(str, zero))}}}: the W-product "
                       "normalization has no triangle chart there")
    return None


def localization(block: ConstraintBlock) -> Cell:
    """Triangle channels (Delta_S) over all 3-subsets S, in combinatorial order
    (SHADOW_LAW Lemma 3). At n=3 there is one triangle. Needs all g != 0 (the
    W-product normalization); component-zero refuses ROLE_CHART_UNAVAILABLE."""
    if not isinstance(block, ConstraintBlock):
        raise TypeError("localization takes a ConstraintBlock")
    ref = _loc_refusal(block)
    if ref is not None:
        return Cell(None, ref)
    jet = block.jets[0]
    g, H, n = jet.g, jet.h, jet.n
    if n < 3:
        return Cell(None, Refusal("ROLE_CHART_UNAVAILABLE",
                    "localization needs at least three roles (a triangle)"))
    offd = [H[i][j] for (i, j) in _pairs(n)]
    W = _W(g, n)
    pidx = {e: k for k, e in enumerate(_pairs(n))}
    value = tuple(_delta_S(g, offd, n, S, pidx, W)
                  for S in combinations(range(n), 3))
    return Cell(value, _zeros_like(value))


def localization_support(block: ConstraintBlock, e_star):
    """{ S : d/dt Delta_S != 0 at t=0 } for a coupling fault on edge e_star.
    Support theorem (RC-8): equals { S : e_star subset S } on the covered class.
    Returns a set of 3-subsets (tuples). Raises on a refusing block."""
    ref = _loc_refusal(block)
    if ref is not None:
        raise ValueError(f"localization_support on a refusing block: {ref.token}")
    jet = block.jets[0]
    g, H, n = jet.g, jet.h, jet.n
    e_star = (min(e_star), max(e_star))
    pidx = {e: k for k, e in enumerate(_pairs(n))}
    e0 = pidx[e_star]
    W = _W(g, n)
    base = [Fraction(H[i][j]) for (i, j) in _pairs(n)]
    moved = set()
    for S in combinations(range(n), 3):
        es = [pidx[p] for p in combinations(S, 2)]
        if e0 not in es:
            continue                         # structural: Delta_S free of nu_e*
        nu = [base[e] * W[e] for e in range(len(W))]
        d = 2 * _T(g, n, S) * W[e0] * (nu[e0] - sum(nu[a] for a in es if a != e0))
        if d != 0:
            moved.add(S)
    return moved


# ============================ 4. fingerprint (n=3-fenced) ============================

def _graph_chart(g, H):
    """Ambient (g,H) at n=3 -> graph-chart role jet (a,b,A,B,C), dependent = the
    P role (index 2). a=-g0/g2, b=-g1/g2; A,B,C the graph Hessian (implicit
    function 2nd derivatives). Raises ZeroDivisionError if g2 = 0."""
    g0, g1, g2 = (Fraction(x) for x in g)
    a = -g0 / g2
    b = -g1 / g2
    H00, H01, H02 = Fraction(H[0][0]), Fraction(H[0][1]), Fraction(H[0][2])
    H11, H12, H22 = Fraction(H[1][1]), Fraction(H[1][2]), Fraction(H[2][2])
    A = -(H00 + 2 * H02 * a + H22 * a * a) / g2
    B = -(H01 + H02 * b + H12 * a + H22 * a * b) / g2
    C = -(H11 + 2 * H12 * b + H22 * b * b) / g2
    return a, b, A, B, C


def fingerprint(block: ConstraintBlock) -> Cell:
    """The role fingerprint (n=3-fenced, A-008): Lambda triple, kappa triple,
    A_c, and the faithfulness determinant 8*L_P*L_D*L_S/q0^6.

    Refusals: CODIM_UNSUPPORTED (len>1); ROLE_CHART_UNAVAILABLE off the role
    chart (a component-zero gradient — a=0/b=0 role-singular, or g2=0 no P-chart);
    CHANNEL_ISOTROPIC (A-010) when a Lambda vanishes (faithfulness rank drop),
    naming the isotropic channel. n != 3 is an API-contract ValueError (the
    fingerprint's certified scope is n=3, A-008)."""
    if not isinstance(block, ConstraintBlock):
        raise TypeError("fingerprint takes a ConstraintBlock")
    if block.n != 3:
        raise ValueError("the fingerprint is n=3-fenced (A-008 certified scope) "
                         "— the general-n sensors are the tower/shape/localization")
    ref = _codim_refusal(block)
    if ref is not None:
        return Cell(None, ref)
    jet = block.jets[0]
    g, H = jet.g, jet.h
    zero = [i for i, x in enumerate(g) if x == 0]
    if len(zero) == 3:
        return Cell(None, Refusal("SINGULAR_GRADIENT",
                    "vanishing gradient: no surface direction at the base point"))
    if zero:
        return Cell(None, Refusal("ROLE_CHART_UNAVAILABLE",
                    "zero gradient component(s) at index set "
                    f"{{{', '.join(map(str, zero))}}}: the role chart does not "
                    "exist in those directions"))
    a, b, A, B, C = _graph_chart(g, H)
    q0 = 1 + a * a + b * b
    LamP, LamD, LamS = B, (A * b - a * B) / a, (C * a - b * B) / b
    zero_ch = [name for name, L in (("P", LamP), ("D", LamD), ("S", LamS))
               if L == 0]
    if zero_ch:
        return Cell(None, Refusal(
            "CHANNEL_ISOTROPIC",
            f"role channel(s) {{{', '.join(zero_ch)}}} isotropic (Lambda = 0): "
            "the faithfulness determinant vanishes, so states differing only in "
            f"the {'/'.join(zero_ch)} channel are fingerprint-indistinguishable"))
    kP, kD, kS = (-(LamP ** 2) / q0 ** 2, -(LamD ** 2) / q0 ** 2,
                  -(LamS ** 2) / q0 ** 2)
    A_c = (kP - kD) ** 2 + (kD - kS) ** 2 + (kS - kP) ** 2
    det = 8 * LamP * LamD * LamS / q0 ** 6
    value = (A_c, det, (LamP, LamD, LamS), (kP, kD, kS))
    return Cell(value, _zeros_like(value))
