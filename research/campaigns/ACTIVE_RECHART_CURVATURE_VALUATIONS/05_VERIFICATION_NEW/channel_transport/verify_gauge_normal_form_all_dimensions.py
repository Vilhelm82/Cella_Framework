#!/usr/bin/env python3
"""Stage 4 gate D: gauge-normal-form quotient in ALL dimensions (PO-16) and
the Lorentzian coupling edge (PO-15).

  D1  n = 3,4,5 symbolic: a_i = H_ii/(2 g_i) is the unique gauge killing the
      diagonal; the representative H_perp is zero-diagonal with off-diagonals
      O_ij = H_ij - g_i H_jj/(2 g_j) - g_j H_ii/(2 g_i)
  D2  O is gauge-invariant: O(H + G_g(v)) = O(H) for symbolic v
  D3  direct sum: Sym_n = Im(G_g) (+) {zero-diagonal}, hence
      Sym_n / Im(G_g) ~= Q^(n(n-1)/2)  — the all-dimensional replacement of
      the three-role quotient Sym_3/Im(G_g) ~= Q^3
  D4  PO-15: kappa_c = -Delta_c/q^2 with Delta_c = nu^T (2I - J) nu,
      nu = (g1 H23, g2 H13, g3 H12); signature of 2I-J is (2,1) (Lorentzian);
      verified against the bordered channel density on generic symbolic data
  D5  single-axis gauge law (general H, R9-corrected scope):
      delta kappa_c(t e_i) = 4 t g1 g2 g3 H_jk / q^2  identically, hence
      pinning iff H_jk = 0
"""
import sys
import itertools
import sympy as sp

failures = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)


def G_op(g, v, n):
    gm, vm = sp.Matrix(g), sp.Matrix(v)
    return gm * vm.T + vm * gm.T


# ---- D1-D3 for n = 3,4,5 ----------------------------------------------------
for n in (3, 4, 5):
    g = [sp.Symbol(f"g{i}", nonzero=True) for i in range(n)]
    H = sp.Matrix(n, n, lambda i, j: sp.Symbol(f"h{min(i,j)}{max(i,j)}"))
    avec = [H[i, i] / (2 * g[i]) for i in range(n)]
    Hperp = sp.expand(H - G_op(g, avec, n))
    okdiag = all(sp.simplify(Hperp[i, i]) == 0 for i in range(n))
    okoff = True
    for i, j in itertools.combinations(range(n), 2):
        Oij = H[i, j] - g[i] * H[j, j] / (2 * g[j]) - g[j] * H[i, i] / (2 * g[i])
        if sp.simplify(Hperp[i, j] - Oij) != 0:
            okoff = False
    check(f"D1 n={n}: normalizing gauge kills diagonal; off-diag = O_ij", okdiag and okoff)

    # D2 gauge invariance of O
    v = [sp.Symbol(f"v{i}") for i in range(n)]
    Hg = sp.expand(H + G_op(g, v, n))
    okinv = True
    for i, j in itertools.combinations(range(n), 2):
        Oij = lambda M: M[i, j] - g[i] * M[j, j] / (2 * g[j]) - g[j] * M[i, i] / (2 * g[i])
        if sp.simplify(Oij(Hg) - Oij(H)) != 0:
            okinv = False
    check(f"D2 n={n}: O(H + G_g(v)) = O(H) identically in v", okinv)

    # D3 direct sum: G_g(v) zero-diagonal => v = 0 (uniqueness/trivial intersection)
    sols = sp.solve([2 * g[i] * v[i] for i in range(n)], v, dict=True)
    triv = sols == [{vi: 0 for vi in v}] or sols == [dict()] or all(
        all(s[vi] == 0 for vi in s) for s in sols)
    check(f"D3 n={n}: Im(G_g) ∩ zero-diag = 0, so Sym_{n}/Im(G_g) ~= Q^{n*(n-1)//2}", triv)

# ---- D4: Lorentzian coupling edge (n = 3) -----------------------------------
g1, g2, g3 = sp.symbols("g1 g2 g3", nonzero=True)
hs = {(i, j): sp.Symbol(f"H{i+1}{j+1}") for i in range(3) for j in range(i, 3)}
H = sp.Matrix(3, 3, lambda i, j: hs[(min(i, j), max(i, j))])
gv = [g1, g2, g3]
q = g1**2 + g2**2 + g3**2

# bordered channel density, coupling coefficient (t^2)
t, u = sp.Dummy("t"), sp.Dummy("u")
Hc = H - sp.diag(H[0, 0], H[1, 1], H[2, 2])
Hs = sp.diag(H[0, 0], H[1, 1], H[2, 2])
Mtu = t * Hc + u * Hs
Bm = sp.zeros(4, 4)
for ii in range(3):
    Bm[0, ii + 1] = gv[ii]
    Bm[ii + 1, 0] = gv[ii]
    for jj in range(3):
        Bm[ii + 1, jj + 1] = Mtu[ii, jj]
dens = sp.expand(-Bm.det())
kc_hat = sp.Poly(dens, t, u).coeff_monomial(t**2)
kc = sp.cancel(kc_hat / q**2)

nu = sp.Matrix([g1 * H[1, 2], g2 * H[0, 2], g3 * H[0, 1]])
Jm = sp.ones(3, 3)
Delta_c = sp.expand((nu.T * (2 * sp.eye(3) - Jm) * nu)[0, 0])
check("D4 kappa_c = -nu^T(2I-J)nu / q^2 identically (generic symbolic)",
      sp.simplify(kc + Delta_c / q**2) == 0)
eigs = sorted((2 * sp.eye(3) - Jm).eigenvals().items(), key=lambda kv: kv[0])
check("D4 signature of 2I-J is (2,1): eigenvalues {-1, 2, 2}",
      dict((k, v) for k, v in eigs) == {-1: 1, 2: 2})

# ---- D5: single-axis gauge law, general H ------------------------------------
tsym = sp.Symbol("t_gauge")
ok = True
for i in range(3):
    e = [sp.Integer(0)] * 3
    e[i] = tsym
    Hgauge = sp.expand(H + G_op(gv, e, 3))
    Mtu2 = t * (Hgauge - sp.diag(*[Hgauge[k, k] for k in range(3)])) \
        + u * sp.diag(*[Hgauge[k, k] for k in range(3)])
    B2 = sp.zeros(4, 4)
    for ii in range(3):
        B2[0, ii + 1] = gv[ii]
        B2[ii + 1, 0] = gv[ii]
        for jj in range(3):
            B2[ii + 1, jj + 1] = Mtu2[ii, jj]
    kc2 = sp.cancel(sp.Poly(sp.expand(-B2.det()), t, u).coeff_monomial(t**2) / q**2)
    jk = [k for k in range(3) if k != i]
    Hjk = H[jk[0], jk[1]]
    delta = sp.simplify(kc2 - kc - 4 * tsym * g1 * g2 * g3 * Hjk / q**2)
    if delta != 0:
        ok = False
check("D5 delta kappa_c(t e_i) = 4 t g1 g2 g3 H_jk / q^2 for ARBITRARY H, all axes", ok)
check("D5 pinning biconditional: shift vanishes for all t iff H_jk = 0", ok)

print()
if failures:
    print("STAGE 4D GATE FAILED:", failures)
    sys.exit(1)
print("STAGE 4D GATE PASSED: gauge-normal quotient Sym_n/Im(G_g) ~= Q^(n(n-1)/2) "
      "for n=3,4,5; Lorentzian edge and single-axis law exact.")
