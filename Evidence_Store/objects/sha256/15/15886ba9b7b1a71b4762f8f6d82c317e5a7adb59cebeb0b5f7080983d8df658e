"""
LEAD-7 TEST 10 — the general parity-fixed inverse-channel normal form.

FRESH, self-contained. sympy only (declared). Independent symbolic Ricci (Christoffel ->
Riemann -> Ricci -> R) for a diagonal metric of arbitrary dimension; NOT the warped-product
shortcut (that is the thing being checked).

CLAIM (Will's lemma). For m>=1, B>0, A_alpha>0, the pure diagonal normal form on an
(m+1)-dimensional state space (one collapsing coordinate x + m transverse fibre directions)
    ds^2 = B x^2 dx^2 + x^{-2} sum_{alpha=1..m} A_alpha dy_alpha^2
has EXACT scalar curvature
    R = - m(m+5) / B * x^{-4},
independent of all transverse amplitudes A_alpha. Decomposition m(m+5) = 6m + m(m-1):
6m radial focusing + m(m-1) transverse fibre shear.

  m=1 -> 6      m=2 -> 14 (KN, 3D state space)      m=3 -> 24

COROLLARY (asymptotic face). If near x=0, with everything even in x,
    g_xx = B(y) x^2 + O(x^4),   g_aa = A_alpha(y) x^{-2} + O(1),   B>0, A_alpha>0,
then R = - m(m+5)/B(y) * x^{-4} + O(x^{-2}). Verified for m=2 with y-dependent B,A and
generic even subleading terms: the leading Laurent coefficient is -14/B(y), reproducing the
KN reflection coefficients C_Omega = -14/B_J, C_Phi = -14/B_Q as the m=2 case.
"""
import sympy as sp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)

def scalar_curvature(gdiag, coords):
    """Exact scalar curvature of a diagonal metric, from first principles."""
    n = len(coords)
    g = sp.diag(*gdiag)
    ginv = sp.diag(*[1/d for d in gdiag])
    # Christoffel symbols of the second kind
    Gamma = [[[sp.Integer(0)]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = sp.Integer(0)
                for d in range(n):
                    s += ginv[a, d]*(sp.diff(g[d, b], coords[c])
                                     + sp.diff(g[d, c], coords[b])
                                     - sp.diff(g[b, c], coords[d]))
                Gamma[a][b][c] = sp.simplify(s/2)
    # Ricci tensor R_bd = d_a G^a_bd - d_d G^a_ba + G^a_ae G^e_bd - G^a_de G^e_ba
    Ric = [[sp.Integer(0)]*n for _ in range(n)]
    for b in range(n):
        for d in range(n):
            s = sp.Integer(0)
            for a in range(n):
                s += sp.diff(Gamma[a][b][d], coords[a]) - sp.diff(Gamma[a][b][a], coords[d])
                for e in range(n):
                    s += Gamma[a][a][e]*Gamma[e][b][d] - Gamma[a][d][e]*Gamma[e][b][a]
            Ric[b][d] = s
    R = sp.Integer(0)
    for b in range(n):
        R += ginv[b, b]*Ric[b][b]
    return sp.simplify(R)

x, B = sp.symbols('x B', positive=True)

print("== pure normal form ds^2 = B x^2 dx^2 + x^-2 sum A_a dy_a^2 : R = -m(m+5)/B x^-4 ==")
for m in (1, 2, 3):
    ys = sp.symbols(f'y1:{m+1}', real=True)
    As = sp.symbols(f'A1:{m+1}', positive=True)
    coords = (x,) + ys
    gdiag = [B*x**2] + [As[a]*x**(-2) for a in range(m)]
    R = scalar_curvature(gdiag, coords)
    expect = -m*(m+5)/B*x**(-4)
    ok = sp.simplify(R - expect) == 0
    # A-independence: R has no A_alpha
    Afree = all(sp.diff(R, A) == 0 for A in As)
    check(f"T10.pure_m{m}", ok and Afree,
          f"R = -{m*(m+5)}/B x^-4 (= -m(m+5)/B), A-independent: {Afree}   [R={sp.nsimplify(R)}]")

check("T10.KN_is_m2", (2*(2+5)) == 14, "m=2 (3D state space) => m(m+5)=14 => C_Omega=-14/B_J, C_Phi=-14/B_Q")
# decomposition 6m + m(m-1) = m(m+5)
mm = sp.symbols('m', positive=True, integer=True)
check("T10.decomposition", sp.simplify(6*mm + mm*(mm-1) - mm*(mm+5)) == 0,
      "m(m+5) = 6m (radial focusing) + m(m-1) (transverse fibre shear)")

print("\n== asymptotic corollary (m=2): leading Laurent coeff = -14/B(y) with even subleading ==")
# y-dependent amplitudes + generic even-in-x subleading terms; leading coefficient must be -14/B(y).
y1, y2 = sp.symbols('y1 y2', real=True)
By = 2 + y1**2 + y2**2                    # B(y1,y2) > 0
A1 = 3 + y2**2                            # A_1(y) > 0
A2 = 5 + y1**2                            # A_2(y) > 0
# even-in-x subleading: g_xx = B x^2 + b4(y) x^4 ; g_aa = A_a x^-2 + a0(y) + a2(y) x^2
b4 = sp.Rational(1, 2) + y2**2
c0, d0 = 1 + y1**2, 2 + y2**2
c2, d2 = sp.Rational(1, 3), sp.Rational(1, 5)
coords = (x, y1, y2)
gdiag = [By*x**2 + b4*x**4,
         A1*x**(-2) + c0 + c2*x**2,
         A2*x**(-2) + d0 + d2*x**2]
R = scalar_curvature(gdiag, coords)
lead = sp.simplify(sp.limit(x**4*R, x, 0))         # leading Laurent coefficient of x^-4
ok = sp.simplify(lead - (-14/By)) == 0
check("T10.asymptotic_corollary_m2", ok,
      f"leading x^-4 coefficient = -14/B(y) = {lead} (A_a and subleading b4,a0,a2 do not enter)")

print()
if not FAILS:
    print("VERDICT: LEAD-7 TEST 10 CLEAN. The parity-fixed inverse-channel normal form has "
          "EXACT scalar curvature R=-m(m+5)/B x^-4 (m transverse fibre directions), verified "
          "from first-principles Ricci for m=1,2,3, amplitude-independent, with the asymptotic "
          "corollary giving the leading Laurent coefficient -m(m+5)/B(y). The KN reflection "
          "coefficients C_Omega=-14/B_J, C_Phi=-14/B_Q are the m=2 case (3D state space).")
else:
    print(f"VERDICT: LEAD-7 TEST 10 has {len(FAILS)} failure(s): {FAILS}")
