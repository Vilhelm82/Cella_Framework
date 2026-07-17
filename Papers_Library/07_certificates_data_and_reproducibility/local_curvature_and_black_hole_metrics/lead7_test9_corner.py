"""
LEAD-7 TEST 9 — the double-reflection (Schwarzschild) corner  Omega=0 cap Phi_e=0.

FRESH, self-contained. sympy + mpmath (declared). Exact-partial 3D Ricci harness
(identical construction to lead7_test5; graph-norm metric G_i = q_i^2 * sum 1/Lambda^2,
q_i = 1 + |grad f_i|^2 via the explicit inverse charts f_S,f_J,f_Q). Validated in Test 2
on flat R^3 (R=0) and the round 3-sphere (R=6/a^2).

QUESTION. The two charge reflection faces Omega=0 (J=0) and Phi_e=0 (Q=0) each carry an
order-4 curvature pole. What happens at the corner where they meet (the Schwarzschild ray
J=Q=0, S=s free)? Approach it along the balanced diagonal Q=eps, J=rho*eps and, more
generally, along the Newton wedge J = rho*eps^a, Q = eps.

RESULTS CERTIFIED HERE.
  (A) Metric corner limits (closed form, graph-normalized), N0(s)=s/pi+1/(16 pi^2):
        eps^6 G_S -> N0^2 * s^5 / [pi (s + 8 pi rho^2)^2]
                   = (16 pi s + 1)^2 s^5 / [256 pi^5 (s + 8 pi rho^2)^2],
        G_J -> N0^2 * pi rho^2 / s,   G_Q -> N0^2 * s / (4 pi rho^2).
      The naive schematic s^7/[pi^3 (s+8 pi rho^2)^2] for eps^6 G_S is the N0 ~ s/pi
      truncation; the exact/schematic ratio is (1 + 1/(16 pi s))^2 (= 1.0402 at s=1), the
      graph-norm U_S^2 term the schematic dropped. G_J,G_Q are eps-independent and scale as
      rho^{+-2}; their product G_J G_Q -> N0^4/4 is rho-independent.
  (B) Balanced radial order is EXACTLY 2 (not 4, not 6): eps^2 R -> R0(s,rho) finite,
      negative. The eps^{-6} metric collapse loses four orders to inverse-metric
      contraction + derivative cancellation. The corner is the CALMEST boundary point:
      order 2 is the MINIMUM of the Newton exponent over all approach directions.
  (C) Newton polygon: along J=rho*eps^a, Q=eps, R ~ eps^{-m(a)} with
        m(a) = max(4a - 2, 4 - 2a),
      vertex (a=1, m=2); edges m=4-2a (a<=1, Phi-face side, m(0)=4) and m=4a-2 (a>=1,
      Omega-face side). Certified at a in {0, 1/2, 1, 3/2, 2}.
  (D) Corner limits of R0 read off C_Omega, C_Phi (their J->0 / Q->0 residues):
        kappa_Omega(s) = lim_{Q->0} C_Omega(s,Q)/Q^2 = -3584 pi^3 s / (16 pi s + 1)^2,
        kappa_Phi(s)   = lim_{J->0} C_Phi(s,J)/J^2   = -14336 pi^5 / [s (16 pi s + 1)^2],
      with  rho^4 R0 -> kappa_Omega(s) (rho->0),  R0/rho^2 -> kappa_Phi(s) (rho->inf).
  (E) R0 is NOT the two-face sum: M(s,rho) := R0 - kappa_Omega/rho^4 - kappa_Phi rho^2 is a
      genuine nonzero mixed-channel term (the G_S mixed-denominator fingerprint).
"""
import sympy as sp
import mpmath as mp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)

mp.mp.dps = 90
M, Se, J, Q, pi = sp.symbols('M S J Q pi', positive=True)
n = 3; XS = (Se, J, Q)

# ---- graph-norm metric via explicit inverse charts (same as Test 5) ----
disc = M**4 - M**2*Q**2 - J**2
fS = pi*(2*M**2 - Q**2 + 2*sp.sqrt(disc))
w = Se/(2*pi) - M**2 + Q**2/2
fJ = sp.sqrt(M**4 - M**2*Q**2 - w**2)
fQ = sp.sqrt(-Se/pi + (2/pi)*sp.sqrt(pi*Se*M**2 - pi**2*J**2))
def Fm(f, ins):
    m, c1, c2 = ins
    LmA = sp.diff(f, m, c1); LmB = sp.diff(f, m, c2)
    q = 1 + sp.diff(f, ins[0])**2 + sp.diff(f, ins[1])**2 + sp.diff(f, ins[2])**2
    return q**2*(1/LmA**2 + 1/LmB**2)
Mval = sp.sqrt(Se/(4*pi) + pi*J**2/Se + Q**2/2 + pi*Q**4/(4*Se))
G = [Fm(fS, (M, J, Q)).subs(M, Mval).subs(pi, sp.pi),
     Fm(fJ, (M, Se, Q)).subs(M, Mval).subs(pi, sp.pi),
     Fm(fQ, (M, Se, J)).subs(M, Mval).subs(pi, sp.pi)]
print("  lambdifying exact metric + partials (~1-2 min)...", flush=True)
val = [sp.lambdify(XS, g, 'mpmath') for g in G]
d1 = [[sp.lambdify(XS, sp.diff(g, XS[k]), 'mpmath') for k in range(n)] for g in G]
d2 = [[[sp.lambdify(XS, sp.diff(g, XS[k], XS[l]), 'mpmath') for l in range(n)] for k in range(n)] for g in G]

def Rscalar(pt):
    g = [val[i](*pt) for i in range(n)]
    dg = [[d1[i][k](*pt) for k in range(n)] for i in range(n)]
    ddg = [[[d2[i][k][l](*pt) for l in range(n)] for k in range(n)] for i in range(n)]
    gi = [1/g[i] for i in range(n)]
    def Gam(a, b, c):
        gac = dg[a][b] if a == c else mp.mpf(0); gab = dg[a][c] if a == b else mp.mpf(0)
        gbc = dg[b][a] if b == c else mp.mpf(0)
        return mp.mpf('0.5')*gi[a]*(gac + gab - gbc)
    def dGam(a, b, c, m):
        g2 = (ddg[a][b][m] if a == c else mp.mpf(0)) + (ddg[a][c][m] if a == b else mp.mpf(0)) \
             - (ddg[b][a][m] if b == c else mp.mpf(0))
        g0 = (dg[a][b] if a == c else mp.mpf(0)) + (dg[a][c] if a == b else mp.mpf(0)) \
             - (dg[b][a] if b == c else mp.mpf(0))
        return mp.mpf('0.5')*(-dg[a][m]/g[a]**2)*g0 + mp.mpf('0.5')*gi[a]*g2
    R = mp.mpf(0)
    for b in range(n):
        Rbb = mp.mpf(0)
        for a in range(n):
            Rbb += dGam(a, b, b, a) - dGam(a, b, a, b)
            for e in range(n):
                Rbb += Gam(a, a, e)*Gam(e, b, b) - Gam(a, b, e)*Gam(e, b, a)
        R += gi[b]*Rbb
    return R

def N0(s): return s/mp.pi + 1/(16*mp.pi**2)

# =====================================================================
# (A) metric corner limits (closed form), graph-normalized
# =====================================================================
print("\n== (A) metric corner limits along Q=eps, J=rho*eps ==")
e = mp.mpf(10)**(-10)
metric_ok = True
for (s, rho) in [(mp.mpf(1), mp.mpf(1)), (mp.mpf(3), mp.mpf('0.5')), (mp.mpf(2), mp.mpf(3))]:
    pt = [s, rho*e, e]
    gs, gj, gq = val[0](*pt), val[1](*pt), val[2](*pt)
    GS_pred = N0(s)**2 * s**5 / (mp.pi*(s + 8*mp.pi*rho**2)**2)
    GJ_pred = N0(s)**2 * mp.pi*rho**2 / s
    GQ_pred = N0(s)**2 * s / (4*mp.pi*rho**2)
    rS, rJ, rQ = e**6*gs/GS_pred, gj/GJ_pred, gq/GQ_pred
    ok = all(abs(x - 1) < mp.mpf('1e-6') for x in (rS, rJ, rQ))
    metric_ok = metric_ok and ok
    print(f"   s={float(s)} rho={float(rho)}: eps^6 G_S/pred={mp.nstr(rS,8)}, "
          f"G_J/pred={mp.nstr(rJ,8)}, G_Q/pred={mp.nstr(rQ,8)}")
check("T9-A.metric_corner_limits",
      metric_ok,
      "eps^6 G_S->N0^2 s^5/[pi(s+8pi rho^2)^2], G_J->N0^2 pi rho^2/s, G_Q->N0^2 s/(4pi rho^2)")
# exact/schematic ratio = (1+1/(16 pi s))^2
s = mp.mpf(1); rho = mp.mpf(1)
GS_pred = N0(s)**2 * s**5 / (mp.pi*(s + 8*mp.pi*rho**2)**2)
sch = s**7/(mp.pi**3*(s + 8*mp.pi*rho**2)**2)
check("T9-A.schematic_ratio",
      abs(GS_pred/sch - (1 + 1/(16*mp.pi*s))**2) < mp.mpf('1e-40'),
      f"exact/schematic = (1+1/(16 pi s))^2 = {mp.nstr((1+1/(16*mp.pi*s))**2,10)} at s=1")

# =====================================================================
# (B),(C) Newton polygon: order along J=rho*eps^a, Q=eps
# =====================================================================
def order_along(s, rho, a, base=mp.mpf('1e-4'), steps=6, ratio=mp.mpf(10)):
    epss = [base*ratio**(-k) for k in range(steps)]
    Rs = [Rscalar([s, rho*ep**a, ep]) for ep in epss]
    # slope of log|R| vs log eps over the two deepest points (subleading ~ ratio^{-1})
    return -(mp.log(abs(Rs[-1])) - mp.log(abs(Rs[-2])))/(mp.log(epss[-1]) - mp.log(epss[-2])), Rs, epss

print("\n== (C) Newton polygon m(a)=max(4a-2, 4-2a) along J=rho*eps^a, Q=eps (s=1,rho=1) ==")
s = mp.mpf(1); rho = mp.mpf(1)
poly_ok = True
for a in [mp.mpf(0), mp.mpf(1)/2, mp.mpf(1), mp.mpf(3)/2, mp.mpf(2)]:
    m_pred = max(4*a - 2, 4 - 2*a)
    slope, Rs, epss = order_along(s, rho, a)
    ok = abs(slope - m_pred) < mp.mpf('5e-3')
    poly_ok = poly_ok and ok
    print(f"   a={mp.nstr(a,4):>5}: order(numeric)={mp.nstr(slope,8):>12}  m(a)=max(4a-2,4-2a)={mp.nstr(m_pred,4)}"
          + ("" if ok else "   <-- MISMATCH"))
check("T9-C.newton_polygon", poly_ok, "m(a)=max(4a-2,4-2a); vertex (1,2); edges 4-2a and 4a-2")

# balanced order exactly 2, R0 finite negative (Richardson in eps^2)
print("\n== (B) balanced diagonal a=1: eps^2 R -> R0(s,rho), order exactly 2 ==")
def R0_extrap(s, rho, base=mp.mpf('1e-2'), steps=7):
    xs = [base*mp.mpf(2)**(-k) for k in range(steps)]           # eps ladder
    ys = [ (ep**2)*Rscalar([s, rho*ep, ep]) for ep in xs ]      # eps^2 R -> R0
    # Neville extrapolation in x^2 -> 0
    xs2 = [x**2 for x in xs]
    P = ys[:]
    for k in range(1, len(P)):
        for i in range(len(P)-k):
            P[i] = ((0 - xs2[i+k])*P[i] - (0 - xs2[i])*P[i+1])/(xs2[i] - xs2[i+k])
    return P[0]
bal_ok = True
for (s, rho) in [(mp.mpf(1), mp.mpf(1)), (mp.mpf(2), mp.mpf(1))]:
    slope, Rs, epss = order_along(s, rho, mp.mpf(1))
    R0 = R0_extrap(s, rho)
    ok = abs(slope - 2) < mp.mpf('1e-2') and R0 < 0
    bal_ok = bal_ok and ok
    print(f"   s={float(s)} rho={float(rho)}: order={mp.nstr(slope,8)}  R0={mp.nstr(R0,10)}  (finite, {'<0' if R0<0 else '>=0'})")
check("T9-B.balanced_order2_negative", bal_ok, "eps^2 R -> R0<0 finite; order exactly 2")

# =====================================================================
# (D) corner residues of C_Omega, C_Phi  ->  rho->0 and rho->inf limits of R0
# =====================================================================
print("\n== (D) R0 boundary links = EXACT corner residues of the Test 6 C_Omega, C_Phi ==")
# Exact closed forms from lead7_test6 (report LEAD7_retrodiction_n3.md). Take the corner
# residues symbolically:  kappa_Omega(S) = lim_{Q->0} C_Omega/Q^2 ; kappa_Phi(S) = lim_{J->0} C_Phi/J^2.
Ssym, Qsym, Jsym, psym = sp.symbols('S Q J p', positive=True)
C_Omega_sym = (-3584*Qsym**2*Ssym**5*psym**3*(psym*Qsym**2 - Ssym)**2
               / ((psym**2*Qsym**4 + 16*psym**2*Qsym**2*Ssym**2 - 2*psym*Qsym**2*Ssym + Ssym**2)
                  * (psym**2*Qsym**4 + 16*psym**2*Qsym**2*Ssym**2 - 2*psym*Qsym**2*Ssym
                     + 16*psym*Ssym**3 + Ssym**2)**2))
C_Phi_sym = (-14336*Jsym**2*Ssym**5*psym**5*(2*psym*Jsym - Ssym)**2*(2*psym*Jsym + Ssym)**2
             * (4*psym**2*Jsym**2 + Ssym**2)
             / ((16*psym**4*Jsym**4 + 64*psym**4*Jsym**2*Ssym**2 - 8*psym**2*Jsym**2*Ssym**2 + Ssym**4)
                * (16*psym**4*Jsym**4 + 64*psym**3*Jsym**2*Ssym**3 + 64*psym**4*Jsym**2*Ssym**2
                   - 8*psym**2*Jsym**2*Ssym**2 + 16*psym*Ssym**5 + Ssym**4)**2))
kO_sym = sp.simplify(sp.limit(C_Omega_sym/Qsym**2, Qsym, 0))
kP_sym = sp.simplify(sp.limit(C_Phi_sym/Jsym**2, Jsym, 0))
kO_expect = -3584*psym**3*Ssym/(16*psym*Ssym + 1)**2
kP_expect = -14336*psym**5/(Ssym*(16*psym*Ssym + 1)**2)
check("T9-D.kappa_Omega_exact", sp.simplify(kO_sym - kO_expect) == 0,
      "lim_{Q->0} C_Omega/Q^2 = -3584 pi^3 S/(16 pi S+1)^2")
check("T9-D.kappa_Phi_exact", sp.simplify(kP_sym - kP_expect) == 0,
      "lim_{J->0} C_Phi/J^2 = -14336 pi^5/[S(16 pi S+1)^2]")
def kappa_Omega(s): return -3584*mp.pi**3*s/(16*mp.pi*s + 1)**2
def kappa_Phi(s):   return -14336*mp.pi**5/(s*(16*mp.pi*s + 1)**2)
# Corroborating numeric trend in the resolved rho-zone (metric conditioning ~rho^{-+} toward
# each face degrades small/large rho -- the known "front-face needs secondary charts" caveat).
s = mp.mpf(1)
r_small = mp.mpf('0.25'); lim0 = r_small**4 * R0_extrap(s, r_small)
r_big = mp.mpf(5);        limi = R0_extrap(s, r_big)/r_big**2
print(f"   rho={float(r_small)}: rho^4 R0 = {mp.nstr(lim0,8)}   kappa_Omega(1) = {mp.nstr(kappa_Omega(s),8)}  (directional, under-resolved)")
print(f"   rho={float(r_big)}: R0/rho^2 = {mp.nstr(limi,8)}   kappa_Phi(1)   = {mp.nstr(kappa_Phi(s),8)}")
check("T9-D.rho_trend_consistent",
      abs(lim0/kappa_Omega(s) - 1) < mp.mpf('0.2') and abs(limi/kappa_Phi(s) - 1) < mp.mpf('0.05'),
      "rho^4 R0 -> kappa_Omega, R0/rho^2 -> kappa_Phi (numeric, conditioning-limited at extremes)")

# =====================================================================
# (E) mixed excess: R0 is NOT the two-face superposition
# =====================================================================
print("\n== (E) mixed-channel excess: R0 != two-face sum ==")
s = mp.mpf(1); rho = mp.mpf(1)
R0 = R0_extrap(s, rho)
twoface = kappa_Omega(s)/rho**4 + kappa_Phi(s)*rho**2
M = R0 - twoface
print(f"   R0(1,1)={mp.nstr(R0,10)}   two-face sum={mp.nstr(twoface,10)}   mixed M={mp.nstr(M,8)}")
check("T9-E.mixed_term_nonzero", abs(M) > mp.mpf('10') and R0 < 0,
      f"M(1,1)={mp.nstr(M,6)} is a genuine interior term (not captured by C_Omega,C_Phi alone)")

print()
if not FAILS:
    print("VERDICT: LEAD-7 TEST 9 CLEAN. The Schwarzschild double-reflection corner is the "
          "CALMEST boundary point: exact-partial curvature gives balanced radial order EXACTLY 2 "
          "(R0<0 finite), the Newton exponent m(a)=max(4a-2,4-2a) with minimum 2 at the balanced "
          "diagonal, metric corner limits in closed form (eps^6 G_S -> N0^2 s^5/[pi(s+8pi rho^2)^2], "
          "the '1.04x' = (1+1/(16 pi s))^2 graph-norm correction), rho->0/rho->inf limits set by the "
          "C_Omega,C_Phi corner residues, and a nonzero mixed-channel excess M so R0 is NOT the "
          "two-face sum.")
else:
    print(f"VERDICT: LEAD-7 TEST 9 has {len(FAILS)} failure(s): {FAILS}")
