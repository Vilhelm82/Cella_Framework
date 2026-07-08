"""
rep_utils.py -- Independent, exact representation theory of the symmetric group.

This module is the REFEREE for the DBP 2-Primary Involution Campaign.  It is
built ONLY from textbook definitions (Murnaghan-Nakayama on beta-sets, the
character inner product, explicit integer matrices) and shares no code with the
DBP / RoleChSpec engine under test.  That independence is deliberate: the
campaign rule forbids tautological verification ("a claimed decomposition is not
checked by character/rank/projector evidence" is a campaign-fail condition), so
the truth side must not be the same code that produces the claim.

EVERYTHING here is exact.  Integers and sympy.Rational only -- no float ever.

Conventions
-----------
* A permutation of {0,...,n-1} is a one-line tuple ``p`` with ``p[i]`` = image of i.
* A partition is a weakly-decreasing tuple of positive ints (its sum is the n).
* A conjugacy class of S_n is indexed by its cycle type (a partition of n).
* Irreducible reps of S_n (Specht modules) are indexed by partitions of n.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations
import sympy as sp
from sympy import Integer, Rational, Matrix, factorial


# --------------------------------------------------------------------------- #
#  Partitions, conjugacy classes, permutations                                #
# --------------------------------------------------------------------------- #

@lru_cache(maxsize=None)
def partitions(n: int) -> tuple:
    """All partitions of n as weakly-decreasing tuples, in reverse-lex order."""
    if n == 0:
        return ((),)
    out = []
    # generate with parts bounded above by `mx`
    def rec(rem, mx, acc):
        if rem == 0:
            out.append(tuple(acc))
            return
        for k in range(min(rem, mx), 0, -1):
            acc.append(k)
            rec(rem - k, k, acc)
            acc.pop()
    rec(n, n, [])
    return tuple(out)


def cycle_type(p: tuple) -> tuple:
    """Cycle type of a one-line permutation, as a weakly-decreasing tuple."""
    n = len(p)
    seen = [False] * n
    lengths = []
    for i in range(n):
        if not seen[i]:
            L = 0
            j = i
            while not seen[j]:
                seen[j] = True
                j = p[j]
                L += 1
            lengths.append(L)
    return tuple(sorted(lengths, reverse=True))


def class_rep(mu: tuple, n: int) -> tuple:
    """A representative one-line permutation of S_n with cycle type mu."""
    assert sum(mu) == n, (mu, n)
    p = [0] * n
    pos = 0
    for L in mu:
        # cycle on positions pos, pos+1, ..., pos+L-1
        for k in range(L):
            p[pos + k] = pos + (k + 1) % L
        pos += L
    return tuple(p)


def class_size(mu: tuple, n: int) -> int:
    """Size of the conjugacy class of cycle type mu in S_n: n!/prod(k^{m_k} m_k!)."""
    from collections import Counter
    c = Counter(mu)
    denom = 1
    for k, m in c.items():
        denom *= (k ** m) * int(factorial(m))
    return int(factorial(n)) // denom


@lru_cache(maxsize=None)
def conjugacy_classes(n: int) -> tuple:
    """Tuple of (cycle_type, class_size) over all partitions of n."""
    return tuple((mu, class_size(mu, n)) for mu in partitions(n))


def compose(p: tuple, q: tuple) -> tuple:
    """(p o q)(i) = p[q[i]]  (apply q first, then p)."""
    return tuple(p[q[i]] for i in range(len(q)))


def perm_power(p: tuple, k: int) -> tuple:
    """p**k as a one-line permutation."""
    n = len(p)
    out = tuple(range(n))
    base = p
    e = k
    while e > 0:
        if e & 1:
            out = compose(out, base)
        base = compose(base, base)
        e >>= 1
    return out


def fix(p: tuple) -> int:
    """Number of fixed points."""
    return sum(1 for i in range(len(p)) if p[i] == i)


def perm_sign(p: tuple) -> int:
    """Sign of a permutation, +1 / -1."""
    n = len(p)
    seen = [False] * n
    s = 1
    for i in range(n):
        if not seen[i]:
            L = 0
            j = i
            while not seen[j]:
                seen[j] = True
                j = p[j]
                L += 1
            if L % 2 == 0:
                s = -s
    return s


# --------------------------------------------------------------------------- #
#  Murnaghan-Nakayama character of a Specht module S^lambda                    #
# --------------------------------------------------------------------------- #

def _beta_set(lam: tuple) -> frozenset:
    """First-column beta-set (abacus) of a partition with s = len(lam) beads."""
    s = len(lam)
    return frozenset(lam[i] + (s - 1 - i) for i in range(s))


@lru_cache(maxsize=None)
def _mn_beta(beta: frozenset, mu: tuple) -> int:
    """Murnaghan-Nakayama on the abacus: chi for the partition encoded by `beta`
    evaluated on the cycle type `mu` (a tuple of parts, processed front to back).

    Removing a rim hook of length k == moving one bead down by k into an empty
    slot; the sign is (-1)^(legs), legs = #beads strictly between the new and old
    positions.  This is exact integer arithmetic.
    """
    if not mu:
        return 1
    k = mu[0]
    rest = mu[1:]
    total = 0
    for b in beta:
        if b >= k and (b - k) not in beta:
            legs = sum(1 for c in beta if (b - k) < c < b)
            new_beta = frozenset((beta - {b}) | {b - k})
            total += (-1) ** legs * _mn_beta(new_beta, rest)
    return total


@lru_cache(maxsize=None)
def specht_char(lam: tuple, mu: tuple) -> int:
    """Character value chi^lambda(mu) of the Specht module S^lambda on class mu."""
    lam = tuple(lam)
    mu = tuple(sorted(mu, reverse=True))
    assert sum(lam) == sum(mu), (lam, mu)
    if not lam:
        return 1
    return _mn_beta(_beta_set(lam), mu)


def specht_dim(lam: tuple) -> int:
    """Dimension of S^lambda = chi^lambda(identity class 1^n) via hook lengths."""
    n = sum(lam)
    return specht_char(lam, tuple([1] * n))


# --------------------------------------------------------------------------- #
#  Class functions and decomposition into irreducibles                        #
# --------------------------------------------------------------------------- #

def inner_product(chi: dict, psi: dict, n: int) -> Rational:
    """<chi, psi> = (1/n!) sum_classes |class| chi(mu) psi(mu).
    chi, psi are dicts keyed by cycle type.  S_n characters are real-integer,
    so no complex conjugation is needed."""
    order = factorial(n)
    s = Integer(0)
    for mu, sz in conjugacy_classes(n):
        s += sz * Integer(chi[mu]) * Integer(psi[mu])
    return Rational(s, order)


def specht_char_dict(lam: tuple) -> dict:
    """Character of S^lambda as {cycle_type: value} over all classes of S_n."""
    n = sum(lam)
    return {mu: specht_char(lam, mu) for mu, _ in conjugacy_classes(n)}


def decompose(chi: dict, n: int) -> dict:
    """Decompose a class function chi (dict keyed by cycle type) into Specht
    multiplicities {partition: multiplicity}.  Asserts integer multiplicities
    and that the multiplicities reproduce chi exactly (a genuine check, not a
    tautology)."""
    out = {}
    for lam in partitions(n):
        m = inner_product(chi, specht_char_dict(lam), n)
        assert m.is_integer, f"non-integer multiplicity {m} for {lam}"
        m = int(m)
        if m != 0:
            out[lam] = m
    # exact reconstruction check
    for mu, _ in conjugacy_classes(n):
        recon = sum(mult * specht_char(lam, mu) for lam, mult in out.items())
        assert recon == chi[mu], f"decomposition does not reproduce chi at {mu}"
    return out


def char_of_perm_rep(value_on_class, n: int) -> dict:
    """Build a character dict from a function class-rep-> integer."""
    return {mu: value_on_class(class_rep(mu, n)) for mu, _ in conjugacy_classes(n)}


# --------------------------------------------------------------------------- #
#  Standard reference characters                                               #
# --------------------------------------------------------------------------- #

def chi_triv(n: int) -> dict:
    return {mu: 1 for mu, _ in conjugacy_classes(n)}


def chi_sign(n: int) -> dict:
    return {mu: perm_sign(class_rep(mu, n)) for mu, _ in conjugacy_classes(n)}


def chi_perm(n: int) -> dict:
    """Character of the permutation rep Q^n: chi(sigma) = fix(sigma)."""
    return {mu: fix(class_rep(mu, n)) for mu, _ in conjugacy_classes(n)}


def chi_std(n: int) -> dict:
    """Character of the standard rep std_n: chi(sigma) = fix(sigma) - 1."""
    return {mu: fix(class_rep(mu, n)) - 1 for mu, _ in conjugacy_classes(n)}


def chi_sym2_of(base: dict, n: int) -> dict:
    """Sym^2 character: 1/2 (chi(g)^2 + chi(g^2))."""
    out = {}
    for mu, _ in conjugacy_classes(n):
        g = class_rep(mu, n)
        g2 = cycle_type(perm_power(g, 2))
        val = Rational(base[mu] ** 2 + base[g2], 2)
        assert val.is_integer
        out[mu] = int(val)
    return out


def chi_wedge2_of(base: dict, n: int) -> dict:
    """Wedge^2 (alternating) character: 1/2 (chi(g)^2 - chi(g^2))."""
    out = {}
    for mu, _ in conjugacy_classes(n):
        g = class_rep(mu, n)
        g2 = cycle_type(perm_power(g, 2))
        val = Rational(base[mu] ** 2 - base[g2], 2)
        assert val.is_integer
        out[mu] = int(val)
    return out


# --------------------------------------------------------------------------- #
#  Explicit INTEGER matrices for the standard representation                   #
# --------------------------------------------------------------------------- #
#  Integral basis of std_n = {x in Z^n : sum x_i = 0}:  f_i = e_i - e_{n-1},
#  i = 0..n-2.  The S_n action e_j -> e_{p(j)} gives, with f_{n-1} := 0,
#       p . f_i = f_{p(i)} - f_{p(n-1)}.
#  All matrices are integer (so the same std serves the SNF lattice work).

def std_matrix(p: tuple, n: int) -> Matrix:
    """(n-1) x (n-1) INTEGER matrix of p acting on std_n in the f-basis."""
    last = n - 1
    cols = []
    for i in range(n - 1):
        col = [0] * (n - 1)
        pi = p[i]
        if pi != last:
            col[pi] += 1
        pl = p[last]
        if pl != last:
            col[pl] -= 1
        cols.append(col)
    return Matrix(n - 1, n - 1, lambda r, c: cols[c][r])


def perm_matrix(p: tuple, n: int) -> Matrix:
    """n x n permutation matrix, P e_i = e_{p(i)}  (so P[p(i), i] = 1)."""
    return Matrix(n, n, lambda r, c: 1 if r == p[c] else 0)


# --------------------------------------------------------------------------- #
#  Self-test                                                                   #
# --------------------------------------------------------------------------- #

def _self_test():
    import sys
    ok = True

    def check(cond, msg):
        nonlocal ok
        mark = "ok  " if cond else "FAIL"
        if not cond:
            ok = False
        print(f"  [{mark}] {msg}")

    # 1. Known small Specht dimensions (hook-length cross-check by hand)
    check(specht_dim((3,)) == 1, "dim S^(3) = 1 (triv)")
    check(specht_dim((2, 1)) == 2, "dim S^(2,1) = 2 (std_3)")
    check(specht_dim((1, 1, 1)) == 1, "dim S^(1,1,1) = 1 (sign)")
    check(specht_dim((2, 2)) == 2, "dim S^(2,2) = 2")
    check(specht_dim((3, 1)) == 3, "dim S^(3,1) = 3 (std_4)")
    check(specht_dim((2, 1, 1)) == 3, "dim S^(2,1,1) = 3")
    check(specht_dim((3, 2)) == 5, "dim S^(3,2) = 5")
    check(specht_dim((4, 2)) == 9, "dim S^(4,2) = 9")

    # 2. Known S_3 character table (classes 1^3, 21, 3)
    c111, c21, c3 = (1, 1, 1), (2, 1), (3,)
    check([specht_char((2, 1), m) for m in (c111, c21, c3)] == [2, 0, -1], "std_3 char = (2,0,-1)")
    check([specht_char((1, 1, 1), m) for m in (c111, c21, c3)] == [1, -1, 1], "sign_3 char = (1,-1,1)")

    # 3. Known S_4 character table (classes 1^4,21^2,2^2,31,4)
    cls4 = [(1, 1, 1, 1), (2, 1, 1), (2, 2), (3, 1), (4,)]
    check([specht_char((3, 1), m) for m in cls4] == [3, 1, -1, 0, -1], "std_4 char")
    check([specht_char((2, 2), m) for m in cls4] == [2, 0, 2, -1, 0], "S^(2,2) char")
    check([specht_char((2, 1, 1), m) for m in cls4] == [3, -1, -1, 0, 1], "S^(2,1,1) char")

    # 4. Orthonormality of irreducible characters for n=3..7
    for n in range(3, 8):
        parts = partitions(n)
        orth = True
        for a in parts:
            for b in parts:
                ip = inner_product(specht_char_dict(a), specht_char_dict(b), n)
                if ip != (1 if a == b else 0):
                    orth = False
        check(orth, f"irreducible characters orthonormal, S_{n}  ({len(parts)} irreps)")

    # 5. std char = fix - 1, and std == S^(n-1,1)
    for n in range(3, 9):
        std = chi_std(n)
        sp_std = specht_char_dict((n - 1, 1))
        check(all(std[mu] == sp_std[mu] for mu, _ in conjugacy_classes(n)),
              f"chi_std == S^(n-1,1) at n={n}")

    # 6. std_matrix is an integer rep with trace = fix - 1, and a homomorphism
    for n in range(3, 8):
        good_tr = True
        for mu, _ in conjugacy_classes(n):
            g = class_rep(mu, n)
            M = std_matrix(g, n)
            if M.trace() != fix(g) - 1:
                good_tr = False
            if any(not x.is_integer for x in M):
                good_tr = False
        check(good_tr, f"std_matrix integer, trace=fix-1 at n={n}")
        # homomorphism on a couple of elements
        import itertools
        elts = [class_rep(mu, n) for mu, _ in conjugacy_classes(n)]
        hom = all(std_matrix(compose(a, b), n) == std_matrix(a, n) * std_matrix(b, n)
                  for a, b in itertools.islice(itertools.product(elts, elts), 25))
        check(hom, f"std_matrix homomorphism at n={n}")

    # 7. Sym2(std) and Wedge2(std) characters + decomposition (the campaign's A2)
    for n in range(3, 9):
        std = chi_std(n)
        sym2 = chi_sym2_of(std, n)
        wed2 = chi_wedge2_of(std, n)
        d_sym = decompose(sym2, n)
        d_wed = decompose(wed2, n)
        # dims
        dim_sym = sym2[tuple([1] * n)]
        dim_wed = wed2[tuple([1] * n)]
        check(dim_sym == n * (n - 1) // 2, f"dim Sym2(std_{n}) = n(n-1)/2 = {n*(n-1)//2}")
        check(dim_wed == (n - 1) * (n - 2) // 2, f"dim Wedge2(std_{n}) = (n-1)(n-2)/2")
        # Sym2(std) = triv + std + S^(n-2,2)  (S^(n-2,2) absent for n=3)
        exp_sym = {(n,): 1, (n - 1, 1): 1}
        if n >= 4:
            exp_sym[(n - 2, 2)] = 1
        check(d_sym == exp_sym, f"Sym2(std_{n}) = triv+std+S^(n-2,2): {d_sym}")
        # Wedge2(std) = S^(n-2,1,1)
        exp_wed = {(n - 2, 1, 1): 1}
        check(d_wed == exp_wed, f"Wedge2(std_{n}) = S^(n-2,1,1): {d_wed}")

    # 8. n=4 special: Wedge2(std_4) = S^(2,1,1) = std (x) sign
    std4 = chi_std(4)
    sgn4 = chi_sign(4)
    std_x_sign = {mu: std4[mu] * sgn4[mu] for mu, _ in conjugacy_classes(4)}
    check(decompose(std_x_sign, 4) == {(2, 1, 1): 1}, "std4 (x) sign = S^(2,1,1)")
    wed4 = chi_wedge2_of(std4, 4)
    check(all(wed4[mu] == std_x_sign[mu] for mu, _ in conjugacy_classes(4)),
          "Wedge2(std_4) == std4 (x) sign  (char level)")

    print("\nrep_utils self-test:", "ALL PASS" if ok else "FAILURES PRESENT")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if _self_test() else 1)
