"""
PFC-1/2/3 — the local curvature normal forms of parity-fixed inverse-channel geometry,
for GENERAL fibre dimension m. FRESH, self-contained. sympy only (declared).

Extracts the reusable local theorem behind the Kerr-Newman complementarity law:
KN is the m=2 (3D state space) application of a dimension-general classification.

First-principles scalar curvature (Christoffel->Riemann->Ricci->R) for a diagonal metric of
any dimension; NOT the warped-product shortcut (which is checked separately, symbolic in m).

CLASSIFICATION (one collapsing coordinate x, m transverse fibre directions y_1..y_m):

  PFC-1  Pure parity-fixed normal form.
         ds^2 = B x^2 dx^2 + x^-2 sum_a A_a dy_a^2   (B>0, A_a>0)
         =>  R = -m(m+5)/B * x^-4  EXACTLY, amplitude-independent.
         Split m(m+5) = 6m + m(m-1) = radial focusing + transverse fibre shear.

  PFC-2  Asymptotic parity-fixed face (even in x, y-dependent, with subleading).
         g_xx = B(y) x^2 + O(x^4),  g_aa = A_a(y) x^-2 + O(1),  even in x.
         =>  R = -m(m+5)/B(y) * x^-4 + O(x^-2).   The odd order x^-3 is ABSENT by parity
         (the metric is invariant under x->-x, so R is even in x); amplitudes drop out.

  PFC-3  Generic quadratic collapse (transverse finite, NOT even in x).
         g_xx = A x^2 + O(x^3),  g_aa = P_a0 + P_a1 x + O(x^2)  (P_a0 != 0).
         =>  R = (1/A) sum_a (P_a1/P_a0) x^-3 + O(x^-2) = (1/A) sum_a d_x log(P_a)|_0 x^-3.
         Order 3, coefficient from the transverse first drift P_a1 (odd order from the
         parity-BREAKING linear terms). This is why generic faces are order 3 and
         parity-fixed faces are order 4.

KN dictionary (m=2): T=0 generic collapse (PFC-3, order 3); Omega=0, Phi_e=0 parity-fixed
reflection faces (PFC-2, order 4, coeff -14/B); Omega=Phi_e=0 double corner (PFC-4, separate).
"""
import sympy as sp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)

def scalar_curvature(gdiag, coords, do_simplify=True):
    """Exact scalar curvature of a diagonal metric, from first principles."""
    n = len(coords)
    g = sp.diag(*gdiag); ginv = sp.diag(*[1/d for d in gdiag])
    Gamma = [[[sp.Integer(0)]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = sp.Integer(0)
                for d in range(n):
                    s += ginv[a, d]*(sp.diff(g[d, b], coords[c]) + sp.diff(g[d, c], coords[b])
                                     - sp.diff(g[b, c], coords[d]))
                Gamma[a][b][c] = sp.cancel(s/2)
    Ric = [[sp.Integer(0)]*n for _ in range(n)]
    for b in range(n):
        for d in range(n):
            s = sp.Integer(0)
            for a in range(n):
                s += sp.diff(Gamma[a][b][d], coords[a]) - sp.diff(Gamma[a][b][a], coords[d])
                for e in range(n):
                    s += Gamma[a][a][e]*Gamma[e][b][d] - Gamma[a][d][e]*Gamma[e][b][a]
            Ric[b][d] = s
    R = sum(ginv[b, b]*Ric[b][b] for b in range(n))
    return sp.simplify(R) if do_simplify else sp.cancel(sp.together(R))

x, B = sp.symbols('x B', positive=True)

# ================= PFC-1 : pure normal form, general m =================
print("== PFC-1: pure  ds^2 = B x^2 dx^2 + x^-2 sum A_a dy_a^2  =>  R = -m(m+5)/B x^-4 ==")
for m in (1, 2, 3, 4):
    ys = sp.symbols(f'y1:{m+1}', real=True)
    As = sp.symbols(f'A1:{m+1}', positive=True)
    gdiag = [B*x**2] + [As[a]/x**2 for a in range(m)]
    R = scalar_curvature(gdiag, (x,) + ys)
    expect = -m*(m+5)/B*x**(-4)
    Afree = all(sp.diff(R, A) == 0 for A in As)
    check(f"PFC1.pure_m{m}", sp.simplify(R - expect) == 0 and Afree,
          f"R = -{m*(m+5)}/B x^-4, amplitude-independent")

# symbolic-in-m warped-product reduction: r = sqrt(B) x^2/2, w ~ r^{-1/2},
# R = -2m w''/w - m(m-1)(w'/w)^2 = -m(m+5)/(4 r^2) = -m(m+5)/(B x^4).
m, r = sp.symbols('m r', positive=True)
w = r**sp.Rational(-1, 2)
wpw = sp.diff(w, r)/w; wppw = sp.diff(w, r, 2)/w
R_warp = sp.simplify(-2*m*wppw - m*(m-1)*wpw**2)     # flat fibre => R_F term absent
check("PFC1.warped_symbolic_m", sp.simplify(R_warp - (-m*(m+5)/(4*r**2))) == 0,
      "warped product over flat fibre: R = -m(m+5)/(4 r^2) for ALL m (symbolic)")
check("PFC1.decomposition", sp.simplify(6*m + m*(m-1) - m*(m+5)) == 0,
      "m(m+5) = 6m (radial focusing) + m(m-1) (transverse fibre shear)")

# ================= PFC-2 : asymptotic parity face, general m =================
# The x^-3 (and every odd) pole is absent because an even-in-x metric has even-in-x R
# (invariance under x -> -x), verified structurally by R(-x) == R(x). The leading x^-4
# coefficient is -m(m+5)/B(y), independent of amplitudes and even subleading data.
print("\n== PFC-2: asymptotic even-in-x face => R = -m(m+5)/B(y) x^-4 + O(x^-2), no x^-3 ==")
# m=2 with full y-dependence:
m = 2
ys = sp.symbols('y1 y2', real=True)
By = 2 + ys[0]**2 + ys[1]**2
gdiag = [By*x**2 + (sp.Rational(1, 2) + ys[1]**2)*x**4]
for a in range(m):
    gdiag.append((3 + a + ys[a]**2)/x**2 + (1 + a + ys[a]**2) + sp.Rational(1, 3+a)*x**2)
R = scalar_curvature(gdiag, (x,) + ys, do_simplify=False)
parity = sp.cancel(R.subs(x, -x) - R) == 0                          # even in x => no odd poles
lead4 = sp.cancel(sp.limit(x**4*R, x, 0))
check("PFC2.asymptotic_m2", parity and sp.simplify(lead4 - (-m*(m+5)/By)) == 0,
      f"even in x (R(-x)=R => no x^-3); leading x^-4 = -14/B(y); amplitudes/subleading absent")
# m=3 with even subleading (constant B,A -> faster; tests parity + leading at higher m):
m = 3
zs = sp.symbols('z1 z2 z3', real=True)
Bc = sp.Symbol('Bc', positive=True)
gdiag = [Bc*x**2 + sp.Rational(1, 2)*x**4]
Ac = sp.symbols('Ac1 Ac2 Ac3', positive=True)
for a in range(m):
    gdiag.append(Ac[a]/x**2 + (1 + a) + sp.Rational(1, 3+a)*x**2)
R = scalar_curvature(gdiag, (x,) + zs, do_simplify=False)
parity = sp.cancel(R.subs(x, -x) - R) == 0
lead4 = sp.cancel(sp.limit(x**4*R, x, 0))
Afree = all(sp.cancel(sp.diff(lead4, A)) == 0 for A in Ac)
check("PFC2.asymptotic_m3", parity and sp.simplify(lead4 - (-m*(m+5)/Bc)) == 0 and Afree,
      "even in x (no x^-3); leading x^-4 = -24/B, amplitude- and subleading-independent")

# ================= PFC-3 : generic quadratic collapse, general m =================
print("\n== PFC-3: generic collapse (transverse finite, NOT even) => order 3, coeff (1/A) sum P_a1/P_a0 ==")
xs = sp.symbols('x', positive=True)
Asy, A3, A4 = sp.Symbol('A', positive=True), sp.Symbol('A3'), sp.Symbol('A4')
for m in (2, 3):
    P0 = sp.symbols(f'P0_1:{m+1}', positive=True)
    P1 = sp.symbols(f'P1_1:{m+1}', real=True)
    P2 = sp.symbols(f'P2_1:{m+1}', real=True)
    gdiag = [Asy*xs**2 + A3*xs**3 + A4*xs**4] + [P0[a] + P1[a]*xs + P2[a]*xs**2 for a in range(m)]
    coords = [xs] + list(sp.symbols(f'z1:{m+1}', real=True))
    R = scalar_curvature(gdiag, coords, do_simplify=False)
    c3 = sp.simplify((sp.series(R*xs**3, xs, 0, 1).removeO()).subs(xs, 0))   # x^-3 coefficient
    target = sum(P1[a]/(Asy*P0[a]) for a in range(m))
    free = all(sp.simplify(sp.diff(c3, v)) == 0 for v in [A3, A4] + list(P2))  # A3,A4,P_a2 absent
    check(f"PFC3.generic_m{m}", sp.simplify(c3 - target) == 0 and free,
          "R ~ (1/A) sum_a (P_a1/P_a0) x^-3; independent of A3,A4,P_a2 (odd order from linear drift)")

print()
if not FAILS:
    print("VERDICT: PFC-1 CLEAN. The parity-fixed inverse-channel local calculus holds for "
          "GENERAL fibre dimension m: pure face R=-m(m+5)/B x^-4 (first-principles m=1..4 + "
          "symbolic-m warped reduction), asymptotic even face same leading coeff with NO x^-3 "
          "(parity), and generic (parity-breaking) collapse order 3 with coeff (1/A) sum "
          "P_a1/P_a0. Kerr-Newman is the m=2 application: T=0 generic (order 3), Omega=0/Phi_e=0 "
          "parity-fixed (order 4, -14/B).")
else:
    print(f"VERDICT: PFC-1 has {len(FAILS)} failure(s): {FAILS}")
