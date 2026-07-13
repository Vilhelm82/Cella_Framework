#!/usr/bin/env python3
"""CV-E1 -- Stage 0 engine lemma E1: Lame scalar-curvature formula, diagonal metrics.

CLAIM (tier target: computer-verified):
  For g = sum_i H_i^2 (dx^i)^2 with Lame coefficients H_i and
  beta_ij = (d_i H_j)/H_i (i != j), the scalar curvature satisfies
    R = -2 * sum_{i<j} (1/(H_i H_j)) * [ d_i beta_ij + d_j beta_ji
                                         + sum_{k != i,j} beta_ki beta_kj ].
CHECKS (referee = first-principles Christoffel/Ricci; probe never calls referee):
  E1.1  n=3, fully general: entries F1,F2,F3 arbitrary smooth positive
        functions of ALL three coordinates.
  E1.2  n=4, fixed deterministic polynomial Lame coefficients in ALL four
        coordinates (g_i = H_i^2; sqrt-free by construction).
SCOPE: dimensions 3 and 4 as stated. Deterministic output; exit 0 iff all pass.
"""
import sys
import sympy as sp


def referee_R(gdiag, coords):
    """Referee: R from Christoffel symbols of the diagonal metric."""
    n = len(coords)
    g = sp.diag(*gdiag)
    ginv = g.inv()
    Gam = [[[sp.Rational(1, 2) * sum(
        ginv[l, m] * (sp.diff(g[m, i], coords[j]) + sp.diff(g[m, j], coords[i])
                      - sp.diff(g[i, j], coords[m]))
        for m in range(n)) for j in range(n)] for i in range(n)] for l in range(n)]
    Ric = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            t = 0
            for l in range(n):
                t += sp.diff(Gam[l][i][j], coords[l]) - sp.diff(Gam[l][i][l], coords[j])
                for m in range(n):
                    t += Gam[l][l][m] * Gam[m][i][j] - Gam[l][j][m] * Gam[m][i][l]
            Ric[i, j] = t
    return sum(ginv[i, j] * Ric[i, j] for i in range(n) for j in range(n))


def probe_R(H, coords):
    """Probe: the Lame expression in the Lame coefficients H_i. Never calls referee."""
    n = len(coords)

    def beta(i, j):
        return sp.diff(H[j], coords[i]) / H[i]

    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            term = sp.diff(beta(i, j), coords[i]) + sp.diff(beta(j, i), coords[j])
            for k in range(n):
                if k != i and k != j:
                    term += beta(k, i) * beta(k, j)
            total += -2 * term / (H[i] * H[j])
    return total


def main():
    ok = True

    # E1.1 -- n=3, fully general diagonal metric
    u, v, w = sp.symbols('u v w', real=True)
    F1 = sp.Function('F1', positive=True)(u, v, w)
    F2 = sp.Function('F2', positive=True)(u, v, w)
    F3 = sp.Function('F3', positive=True)(u, v, w)
    gdiag = [F1, F2, F3]
    H = [sp.sqrt(f) for f in gdiag]
    d1 = sp.simplify(referee_R(gdiag, [u, v, w]) - probe_R(H, [u, v, w]))
    p1 = (d1 == 0)
    ok = ok and p1
    print("E1.1 n=3 fully-general diagonal metric: diff == 0 :",
          "PASS" if p1 else "FAIL")

    # E1.2 -- n=4, fixed deterministic polynomial Lame coefficients
    x1, x2, x3, x4 = sp.symbols('x1 x2 x3 x4', real=True)
    Hp = [2 + x1**2 + x2 * x3,
          3 + x2**2 + x1 * x4,
          2 + x3**2 + x2 * x4,
          1 + x4**2 + x1 * x3]
    gdiag4 = [h**2 for h in Hp]
    diff4 = referee_R(gdiag4, [x1, x2, x3, x4]) - probe_R(Hp, [x1, x2, x3, x4])
    d2 = sp.expand(sp.numer(sp.together(diff4)))
    p2 = (d2 == 0)
    ok = ok and p2
    print("E1.2 n=4 polynomial Lame coefficients:  diff == 0 :",
          "PASS" if p2 else "FAIL")

    print("CV-E1 VERDICT:", "PASS (all checks)" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
