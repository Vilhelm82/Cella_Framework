#!/usr/bin/env python3
"""CV-E2 -- Stage 0 engine lemma E2: canonical gauge.

CLAIMS (tier target: computer-verified; scope stated per check):
(A) Boundary robustness on the parity-fixed pure model (m=2)
      ds^2 = B x^2 dx^2 + x^{-2}(A1 dy1^2 + A2 dy2^2)
    under the boundary-adapted change  x = c(y1)*xp + k*xp^2
    (c > 0 arbitrary smooth, k a constant). The transformed metric acquires
    an off-diagonal g_{xp,y1} (diagonality is a gauge), and:
      A1: leading pole order in xp is 4, with coefficient -14/Bp where
          Bp := lim g_{xp,xp}/xp^2 = B c^4 -- the law -m(m+5)/B is
          form-invariant, reading B from the transformed germ.
      A2: the xp^{-3} coefficient equals 56 k/(B c^5): nonzero exactly when
          the change breaks parity (k != 0). Absence of the odd pole is
          invariant precisely under parity-preserving boundary changes.
(B) Metric-distance normalization, d = proper distance to the face:
      B1: pure parity model, m in {2,3}: R * d^2 == -m(m+5)/4 IDENTICALLY
          (a pure number; B and all amplitudes absorbed by the ruler).
      B2: generic truncated model (m=2), g_x = A x^2, g_a = P_a0 + P_a1 x:
          intrinsic rate 3/2, with
          lim R d^{3/2} = (P11/P10 + P21/P20) A^{-1/4} / 2^{3/2},
          and lim R d^2 = 0.
Referee: first-principles Christoffel/Ricci on the full (non-diagonal where
applicable) metric. Deterministic output; exit 0 iff all checks pass.
"""
import sys
import sympy as sp


def scalar_R_full(g, coords):
    """Referee: R from Christoffels of an arbitrary symmetric metric matrix."""
    n = len(coords)
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


def scalar_R_diag(gdiag, coords):
    return scalar_R_full(sp.diag(*gdiag), coords)


def check_A():
    """Boundary robustness under x = c(y1)*xp + k*xp^2 (m=2 pure model)."""
    xp, y1, y2 = sp.symbols('xp y1 y2', real=True, positive=True)
    B, A1, A2 = sp.symbols('B A1 A2', positive=True)
    k = sp.symbols('k', real=True)
    c = sp.Function('c', positive=True)(y1)

    X = c * xp + k * xp**2
    Xp = sp.diff(X, xp)
    Xy = sp.diff(X, y1)

    g = sp.zeros(3, 3)
    g[0, 0] = B * X**2 * Xp**2
    g[0, 1] = g[1, 0] = B * X**2 * Xp * Xy
    g[1, 1] = A1 * X**(-2) + B * X**2 * Xy**2
    g[2, 2] = A2 * X**(-2)

    R = sp.together(scalar_R_full(g, [xp, y1, y2]))

    Bp = sp.limit(g[0, 0] / xp**2, xp, 0)
    okBp = sp.simplify(Bp - B * c**4) == 0

    L4 = sp.simplify(sp.limit(R * xp**4, xp, 0))
    okA1 = sp.simplify(L4 + 14 / Bp) == 0

    L3 = sp.simplify(sp.limit((R - L4 / xp**4) * xp**3, xp, 0))
    okA2 = (sp.simplify(L3 - 56 * k / (B * c**5)) == 0) and (L3.subs(k, 0) == 0)
    return okBp, okA1, okA2


def check_B1():
    """Pure parity model: R * d^2 == -m(m+5)/4 identically, m in {2,3}."""
    x = sp.symbols('x', positive=True)
    B = sp.symbols('B', positive=True)
    results = []
    for m in (2, 3):
        As = list(sp.symbols(f'A1:{m+1}', positive=True))
        ys = sp.symbols(f'y1:{m+1}')
        gdiag = [B * x**2] + [As[a] * x**(-2) for a in range(m)]
        R = scalar_R_diag(gdiag, [x] + list(ys))
        d2 = B * x**4 / 4          # d = sqrt(B) x^2 / 2, so d^2 = B x^4 / 4
        results.append(sp.simplify(R * d2 + sp.Rational(m * (m + 5), 4)) == 0)
    return results


def check_B2():
    """Generic truncated model (m=2): intrinsic rate 3/2 and its coefficient."""
    x = sp.symbols('x', positive=True)
    A = sp.symbols('A', positive=True)
    P10, P11, P20, P21 = sp.symbols('P10 P11 P20 P21', positive=True)
    y1, y2 = sp.symbols('y1 y2')
    gdiag = [A * x**2, P10 + P11 * x, P20 + P21 * x]
    R = sp.together(scalar_R_diag(gdiag, [x, y1, y2]))
    drift = P11 / P10 + P21 / P20
    ok_x3 = sp.simplify(sp.limit(R * x**3, x, 0) - drift / A) == 0
    d = sp.sqrt(A) * x**2 / 2
    target = drift * A**sp.Rational(-1, 4) / 2**sp.Rational(3, 2)
    ok_d32 = sp.simplify(sp.limit(R * d**sp.Rational(3, 2), x, 0) - target) == 0
    ok_d2 = sp.limit(R * d**2, x, 0) == 0
    return ok_x3, ok_d32, ok_d2


def main():
    ok = True

    okBp, okA1, okA2 = check_A()
    print("A0  Bp = B*c(y1)^4 (transformed collapsing amplitude)      :",
          "PASS" if okBp else "FAIL")
    print("A1  order 4 invariant, coefficient == -14/Bp (form-invar.) :",
          "PASS" if okA1 else "FAIL")
    print("A2  xp^-3 coeff == 56k/(B c^5); zero iff parity-preserving :",
          "PASS" if okA2 else "FAIL")
    ok = ok and okBp and okA1 and okA2

    r_m2, r_m3 = check_B1()
    print("B1  m=2: R*d^2 == -14/4 identically (pure number)          :",
          "PASS" if r_m2 else "FAIL")
    print("B1  m=3: R*d^2 == -24/4 identically (pure number)          :",
          "PASS" if r_m3 else "FAIL")
    ok = ok and r_m2 and r_m3

    ok_x3, ok_d32, ok_d2 = check_B2()
    print("B2  sanity: lim R*x^3 == drift/A                           :",
          "PASS" if ok_x3 else "FAIL")
    print("B2  intrinsic rate 3/2: lim R*d^(3/2) == drift*A^(-1/4)/2^(3/2):",
          "PASS" if ok_d32 else "FAIL")
    print("B2  lim R*d^2 == 0 (rate strictly below 2)                 :",
          "PASS" if ok_d2 else "FAIL")
    ok = ok and ok_x3 and ok_d32 and ok_d2

    print("CV-E2 VERDICT:", "PASS (all checks)" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
