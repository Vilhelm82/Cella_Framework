#!/usr/bin/env python3
"""Stage 2 falsification gate: PO-5..PO-8 and Gate 2.

  C1  bordered-minor channel density (Paper I 5.2) reproduces sigma_2(S) of the
      true tangent shape operator: ambient n = 3 and n = 4, random exact data
  C2  R = 2*sigma_2 for Euclidean hypersurfaces: dim 2 (in R^3) and dim 3 (in R^4),
      intrinsic scalar curvature of the induced graph metric vs channel sum
  C3  Gate 2: graph gauge in dim 2 recovers kc = -M^2/Q^2, ks = L*N/Q^2,
      kint = 0, K_G = kc + ks  exactly, on the generic symbolic 2-jet
  C4  keystone replay: F = x1^2 + x1 x2 + x3^2 - 3 at (1,1,1):
      (kc, kint, ks) = (-1/49, -3/49, 1/49), K_G = -3/49
  C5  PO-8: point-normalized defining gauge shifts H by g a^T + a g^T;
      P (g a^T + a g^T) P = 0 (tangent shape operator invariant), channels move
      strictly inside ker(Sigma_channel); keystone pinning locus w(u+3v+1)+2uv=0
  C6  PO-5 (n=4 Gauss-Kronecker row): Newton-identity grid K_30+K_21+K_12+K_03
      equals sigma_3(S) exactly, random exact data
  C7  exact sequence sanity: Sigma_channel is onto, kernel is the zero-sum
      plane, and the gauge orbit lies in the affine fibre over K_G
"""
import random
import sys
import itertools
import sympy as sp

failures = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)


def channel_density(gvec, H, n, r=2):
    """Paper I 5.2: C_hat_r(t,u) = (-1)^{r+1} sum_{|I|=r+1} det bordered minor.

    The grading variables are Dummy symbols so they can never collide with
    symbols appearing in the metric/Hessian data (that collision was a real
    Stage-2 falsification event, caught by gate C5 and fixed here)."""
    t, u = sp.Dummy("t"), sp.Dummy("u")
    Hc = H - sp.diag(*[H[i, i] for i in range(n)])
    Hs = sp.diag(*[H[i, i] for i in range(n)])
    M = t * Hc + u * Hs
    total = 0
    for I in itertools.combinations(range(n), r + 1):
        B = sp.zeros(r + 2, r + 2)
        for ii, i in enumerate(I):
            B[0, ii + 1] = gvec[i]
            B[ii + 1, 0] = gvec[i]
            for jj, j in enumerate(I):
                B[ii + 1, jj + 1] = M[i, j]
        total += B.det()
    total = sp.expand((-1) ** (r + 1) * total)
    poly = sp.Poly(total, t, u)
    q = sum(x**2 for x in gvec)
    norm = q ** sp.Rational(r + 2, 2)
    chans = {}
    for p in range(r + 1):
        chans[(r - p, p)] = sp.cancel(poly.coeff_monomial(t ** (r - p) * u ** p) / norm)
    return chans  # keys (t-power, u-power) = (coupling degree, self degree)


def shape_operator(gvec, H, n):
    """Exact tangent shape operator matrix in an explicit tangent basis."""
    g = sp.Matrix(gvec)
    q = (g.T * g)[0, 0]
    # tangent basis: complete g to a basis, Gram-Schmidt not needed; use
    # projections of coordinate vectors with one dropped direction
    # pick k with g[k] != 0
    k = max(range(n), key=lambda i: abs(gvec[i]) if gvec[i] != 0 else -1)
    basis = []
    for i in range(n):
        if i == k:
            continue
        e = sp.zeros(n, 1)
        e[i] = 1
        v = e - (g[i] / q) * g
        basis.append(v)
    Tb = sp.Matrix.hstack(*basis)
    Ifund = (Tb.T * Tb)
    IIfund = (Tb.T * (H / sp.sqrt(q)) * Tb)
    return Ifund.inv() * IIfund


def sigma_r_of(Smat, r):
    lam = sp.symbols("lam")
    p = Smat.charpoly(lam)
    n = Smat.shape[0]
    # char poly = lam^n - e1 lam^{n-1} + e2 lam^{n-2} - ...
    return sp.expand((-1) ** r * p.coeff_monomial(lam ** (n - r)))


rng = random.Random(20260730)


def rand_sym(n):
    H = sp.zeros(n, n)
    for i in range(n):
        for j in range(i, n):
            v = sp.Rational(rng.randint(-6, 6), rng.randint(1, 5))
            H[i, j] = H[j, i] = v
    return H


def rand_g(n):
    while True:
        g = [sp.Rational(rng.randint(-6, 6), rng.randint(1, 4)) for _ in range(n)]
        if all(x != 0 for x in g):
            return g


# ---- C1: channel sum = sigma_2 of true shape operator, n=3 and n=4 ---------
ok = True
for n in (3, 4):
    for _ in range(3):
        gv, H = rand_g(n), rand_sym(n)
        ch = channel_density(gv, H, n, r=2)
        s2_direct = sigma_r_of(shape_operator(gv, H, n), 2)
        if sp.simplify(sum(ch.values()) - s2_direct) != 0:
            ok = False
check("C1 bordered channel sum equals sigma_2(shape operator), n=3,4 exact", ok)

# ---- C2: R = 2 sigma_2 for Euclidean hypersurface graphs -------------------
ok = True
for dim in (2, 3):
    nvars = dim
    xs = sp.symbols(f"y0:{nvars}")
    # random exact 2-jet graph h with zero linear part not required — keep general
    h = sum(sp.Rational(rng.randint(-4, 4), rng.randint(1, 3)) * xs[i] for i in range(nvars))
    for i in range(nvars):
        for j in range(i, nvars):
            h += sp.Rational(rng.randint(-4, 4), rng.randint(1, 3)) * xs[i] * xs[j]
    grad = [sp.diff(h, v) for v in xs]
    gmet = sp.eye(nvars) + sp.Matrix(grad) * sp.Matrix(grad).T
    # intrinsic scalar curvature at origin
    ginv = gmet.inv()
    Gam = [[[sum(ginv[l, m] * (sp.diff(gmet[m, i], xs[j]) + sp.diff(gmet[m, j], xs[i])
                               - sp.diff(gmet[i, j], xs[m])) for m in range(nvars)) / 2
             for j in range(nvars)] for i in range(nvars)] for l in range(nvars)]
    Ric = sp.zeros(nvars, nvars)
    for i in range(nvars):
        for j in range(nvars):
            expr = 0
            for l in range(nvars):
                expr += sp.diff(Gam[l][i][j], xs[l]) - sp.diff(Gam[l][i][l], xs[j])
                for m in range(nvars):
                    expr += Gam[l][l][m] * Gam[m][i][j] - Gam[l][j][m] * Gam[m][i][l]
            Ric[i, j] = expr
    Rscal = sum(ginv[i, j] * Ric[i, j] for i in range(nvars) for j in range(nvars))
    Rscal0 = sp.simplify(Rscal.subs({v: 0 for v in xs}))
    # channel side: F = z - h, ambient n = dim+1
    amb = nvars + 1
    gv = [-grad[i].subs({v: 0 for v in xs}) for i in range(nvars)] + [1]
    H = sp.zeros(amb, amb)
    for i in range(nvars):
        for j in range(nvars):
            H[i, j] = -sp.diff(h, xs[i], xs[j])
    ch = channel_density(gv, H, amb, r=2)
    if sp.simplify(Rscal0 - 2 * sum(ch.values())) != 0:
        ok = False
check("C2 R = 2*sigma_2 exactly for graph hypersurfaces, dim 2 and 3", ok)

# ---- C3: Gate 2 generic symbolic dim-2 recovery -----------------------------
al, be, L, M_, N = sp.symbols("alpha beta L M N")
gv = [-al, -be, 1]
H = sp.Matrix([[-L, -M_, 0], [-M_, -N, 0], [0, 0, 0]])
ch = channel_density(gv, H, 3, r=2)
Q = 1 + al**2 + be**2
kc, kint, ks = ch[(2, 0)], ch[(1, 1)], ch[(0, 2)]
check("C3 Gate2 kc = -M^2/Q^2", sp.simplify(kc + M_**2 / Q**2) == 0)
check("C3 Gate2 ks = L*N/Q^2", sp.simplify(ks - L * N / Q**2) == 0)
check("C3 Gate2 kint = 0 (graph gauge)", sp.simplify(kint) == 0)
check("C3 Gate2 K_G = kc + ks = (LN - M^2)/Q^2",
      sp.simplify(kc + kint + ks - (L * N - M_**2) / Q**2) == 0)

# ---- C4: keystone replay -----------------------------------------------------
gv = [3, 1, 2]
H = sp.Matrix([[2, 1, 0], [1, 0, 0], [0, 0, 2]])
ch = channel_density(gv, H, 3, r=2)
check("C4 keystone (kc,kint,ks) = (-1/49, -3/49, 1/49)",
      (ch[(2, 0)], ch[(1, 1)], ch[(0, 2)]) ==
      (sp.Rational(-1, 49), sp.Rational(-3, 49), sp.Rational(1, 49)))
check("C4 keystone K_G = -3/49", sum(ch.values()) == sp.Rational(-3, 49))

# ---- C5: gauge transport PO-8 ------------------------------------------------
u_, v_, w_ = sp.symbols("u v w")
avec = sp.Matrix([u_, v_, w_])
gmat = sp.Matrix(gv)
Hg = H + gmat * avec.T + avec * gmat.T
P = sp.eye(3) - gmat * gmat.T / 14
check("C5 tangent projection kills the gauge shift: P(ga^T+ag^T)P = 0",
      sp.simplify(P * (gmat * avec.T + avec * gmat.T) * P) == sp.zeros(3, 3))
chg = channel_density(gv, Hg, 3, r=2)
tot = sp.simplify(sum(chg.values()))
check("C5 gauge orbit stays in the affine fibre: sum = -3/49 for ALL (u,v,w)",
      tot == sp.Rational(-3, 49))
kc_g = sp.expand(chg[(2, 0)])
expected_kc = sp.Rational(1, 49) * (12 * u_ * v_ + 6 * u_ * w_ + 18 * v_ * w_ + 6 * w_ - 1)
check("C5 keystone kc gauge law matches Paper I appendix exactly",
      sp.simplify(kc_g - expected_kc) == 0)
pin = sp.factor(kc_g - sp.Rational(-1, 49))
check("C5 kc pinned exactly on w(u+3v+1) + 2uv = 0",
      sp.simplify(sp.expand(pin * 49 / 6) - sp.expand(w_ * (u_ + 3 * v_ + 1) + 2 * u_ * v_)) == 0)

# ---- C6: n=4 Gauss-Kronecker row (r=3) via Newton identities ------------------
ok = True
for _ in range(2):
    gv4, H4 = rand_g(4), rand_sym(4)
    S = shape_operator(gv4, H4, 4)
    # split induced by Hc, Hs through the same tangent construction
    Hc = H4 - sp.diag(*[H4[i, i] for i in range(4)])
    Hs = sp.diag(*[H4[i, i] for i in range(4)])
    Amat = shape_operator(gv4, Hc, 4)
    Bmat = shape_operator(gv4, Hs, 4)
    a1, b1 = Amat.trace(), Bmat.trace()
    a2, b2 = (Amat * Amat).trace(), (Bmat * Bmat).trace()
    c = (Amat * Bmat).trace()
    a3, b3 = (Amat * Amat * Amat).trace(), (Bmat * Bmat * Bmat).trace()
    d = (Amat * Amat * Bmat).trace()
    e = (Amat * Bmat * Bmat).trace()
    K30 = (a1**3 - 3 * a1 * a2 + 2 * a3) / 6
    K21 = (a1**2 * b1 - 2 * a1 * c - b1 * a2 + 2 * d) / 2
    K12 = (a1 * b1**2 - a1 * b2 - 2 * b1 * c + 2 * e) / 2
    K03 = (b1**3 - 3 * b1 * b2 + 2 * b3) / 6
    if sp.simplify(K30 + K21 + K12 + K03 - sigma_r_of(S, 3)) != 0:
        ok = False
check("C6 n=4 Gauss-Kronecker grid sums to sigma_3(S) exactly", ok)

# ---- C7: exact sequence -------------------------------------------------------
# Sigma: R^3 -> R is onto (obvious); kernel = zero-sum plane; gauge displacement
# vector lies in the kernel identically in (u,v,w):
disp = sp.Matrix([sp.expand(chg[(2, 0)] - ch[(2, 0)]),
                  sp.expand(chg[(1, 1)] - ch[(1, 1)]),
                  sp.expand(chg[(0, 2)] - ch[(0, 2)])])
check("C7 gauge displacement lies in ker(Sigma_channel) identically",
      sp.simplify(disp[0] + disp[1] + disp[2]) == 0 and sp.simplify(disp[0]) != 0)

print()
if failures:
    print("STAGE 2 GATE FAILED:", failures)
    sys.exit(1)
print("STAGE 2 GATE PASSED: sigma_2 normalization, channel split, graph gauge, "
      "keystone, gauge kernel transport, n=4 grid — all exact.")
