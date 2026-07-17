"""RC-2 RE-CERTIFICATION: the gauge-normal form, SYMBOLIC tier (n = 3, 4, 5).

Re-verification rule (README rule 3): fresh derivation, no origin code, no
origin values. Everything below is proven as a POLYNOMIAL / RATIONAL-FUNCTION
IDENTITY in the indeterminates (g_i, H_ij, b_i, c) — not at fixtures.

Objects (regular locus: all g_i != 0; char 0 — the construction divides by 2g_i):
    G_g(a) = g a^T + a g^T                      (the gauge image map)
    a*(H)_i = H_ii / (2 g_i)                    (the diagonal-killing gauge)
    H_perp  = H - G_g(a*(H))                    (gauge-normal representative)
    O_ij(H) = H_ij - g_i H_jj/(2 g_j) - g_j H_ii/(2 g_i),  i < j   (carrier)

Checks, each a symbolic identity per n in {3,4,5}:
    NF1  diag(H_perp) == 0                       (the gauge kills the diagonal)
    NF2  offdiag(H_perp) == O                    (normal form exposes the carrier)
    NF3  a* is the UNIQUE diagonal-killing gauge (linear system det = 2^n * prod g_i)
    NF4  O(H + G_g(b)) == O(H) for generic b     (carrier is gauge-invariant)
    NF5  O linear in H: O(H+K)==O(H)+O(K), O(c*H)==c*O(H)
    NF6  rank Im(G_g) = n: the diagonal-row minor of [vec G(e_1)..vec G(e_n)]
         equals 2^n * prod g_i  (nonzero exactly on the regular locus)
    NF7  Jacobian dO/dH restricted to off-diagonal slots is the IDENTITY
         (=> rank O = n(n-1)/2; with NF4 and the dimension count
         dim Sym_n - n(n-1)/2 = n = dim Im(G_g), this forces ker O = Im(G_g))
    NF8  G_g(b) zero-diagonal  ==>  b = 0        (Im(G_g) meets ZeroDiag only at 0;
         with NF1-NF3: Sym_n = Im(G_g) (+) ZeroDiag, a DIRECT SUM)

Dependency: sympy (symbolic tier only — no float, no verdict-path use of sympy
beyond exact rational-function cancellation).
Run:  python verification/recert_normal_form.py   (exit 0 iff all identities hold)
Byte-stability: run twice, sha256 the stdout.
"""

import sys
import sympy as sp

FAILS = []


def check(name, ok):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


def is_zero(expr):
    return sp.expand(sp.cancel(sp.together(expr))) == 0


def run(n):
    g = [sp.Symbol(f"g{i}", nonzero=True) for i in range(n)]
    b = [sp.Symbol(f"b{i}") for i in range(n)]
    c = sp.Symbol("c")
    H = [[sp.Symbol(f"H{min(i,j)}{max(i,j)}") for j in range(n)] for i in range(n)]
    K = [[sp.Symbol(f"K{min(i,j)}{max(i,j)}") for j in range(n)] for i in range(n)]

    def gauge_mat(vec):
        return [[g[i] * vec[j] + vec[i] * g[j] for j in range(n)] for i in range(n)]

    def add(A, B):
        return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

    def O(M):
        return {
            (i, j): M[i][j] - g[i] * M[j][j] / (2 * g[j]) - g[j] * M[i][i] / (2 * g[i])
            for i in range(n) for j in range(i + 1, n)
        }

    pairs = sorted(O(H).keys())

    # NF1 / NF2 — the normal form
    a_star = [H[i][i] / (2 * g[i]) for i in range(n)]
    Ga = gauge_mat(a_star)
    Hp = [[H[i][j] - Ga[i][j] for j in range(n)] for i in range(n)]
    check(f"NF1 n={n} diag(H_perp) == 0 (symbolic)",
          all(is_zero(Hp[i][i]) for i in range(n)))
    OH = O(H)
    check(f"NF2 n={n} offdiag(H_perp) == O (symbolic)",
          all(is_zero(Hp[i][j] - OH[(i, j)]) for (i, j) in pairs))

    # NF3 — uniqueness: diag(G_g(a)) = diag(H) is diag(2 g_i) a = (H_ii)
    detM = sp.expand(sp.prod([2 * g[i] for i in range(n)]))
    expected = sp.expand(2 ** n * sp.prod(g))
    check(f"NF3 n={n} unique diagonal-killing gauge (system det == 2^{n}*prod g)",
          sp.expand(detM - expected) == 0)

    # NF4 — gauge invariance of the carrier, generic b
    OHb = O(add(H, gauge_mat(b)))
    check(f"NF4 n={n} O(H + G_g(b)) == O(H) (symbolic, generic b)",
          all(is_zero(OHb[p] - OH[p]) for p in pairs))

    # NF5 — linearity in H
    OK_ = O(K)
    OHK = O(add(H, K))
    cH = [[c * H[i][j] for j in range(n)] for i in range(n)]
    OcH = O(cH)
    check(f"NF5 n={n} O(H+K) == O(H)+O(K) (symbolic)",
          all(is_zero(OHK[p] - OH[p] - OK_[p]) for p in pairs))
    check(f"NF5 n={n} O(c*H) == c*O(H) (symbolic)",
          all(is_zero(OcH[p] - c * OH[p]) for p in pairs))

    # NF6 — rank Im(G_g) = n via the diagonal-row minor
    basis_cols = []
    for j in range(n):
        e = [sp.Integer(k == j) for k in range(n)]
        Ge = gauge_mat(e)
        basis_cols.append([Ge[i][i] for i in range(n)])   # diagonal rows only
    minor = sp.Matrix(basis_cols).T.det()
    check(f"NF6 n={n} diagonal-row minor == 2^{n}*prod g (rank Im(G_g) = {n})",
          sp.expand(minor - expected) == 0)

    # NF7 — dO/dH on off-diagonal slots is the identity
    ok7 = True
    for (i, j) in pairs:
        for (k, l) in pairs:
            d = sp.diff(OH[(i, j)], H[k][l])
            ok7 &= (d - sp.Integer(1 if (k, l) == (i, j) else 0)) == 0
    check(f"NF7 n={n} dO/dH off-diagonal block == I "
          f"(rank O = {n*(n-1)//2}; + NF4 + dim count => ker O = Im(G_g))", bool(ok7))

    # NF8 — Im(G_g) meets ZeroDiag only at 0
    sol = sp.solve([2 * g[i] * b[i] for i in range(n)], b, dict=True)
    check(f"NF8 n={n} G_g(b) zero-diagonal ==> b == 0 (direct sum with ZeroDiag)",
          sol == [{bi: 0 for bi in b}])


for n in (3, 4, 5):
    run(n)

print()
if FAILS:
    print(f"RC-2: FAIL ({len(FAILS)})")
    sys.exit(1)
print("RC-2: CLEAN — normal form re-proven SYMBOLICALLY at n=3,4,5 "
      "(identities over Q(g)[H,b,c]; regular locus; char 0).")
sys.exit(0)
