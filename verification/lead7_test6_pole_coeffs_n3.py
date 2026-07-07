"""
LEAD-7 TEST 6 — EXACT leading pole COEFFICIENTS at the reflection-fixed role divisors
(KN retrodiction tier, coefficient level). FRESH, zero-import. sympy + mpmath (declared).
Byte-stable (fixed dps + fixed points).

Test 5 pinned the ORDERS (extremal 3 / Omega=0 4 / Phi_e=0 4). This file gives the exact
CLOSED FORMS of the leading coefficients on the two reflection-fixed divisors, from a
universal structural identity, and verifies them against direct high-precision curvature.

UNIVERSAL IDENTITY (T6-a, symbolic). For a diagonal 3D metric that near a reflection face
(small coordinate x, the metric even in x) has the vanishing component g_x = B(y,z) x^2 +
O(x^4) and the other two components finite, the Ricci scalar's leading Laurent coefficient
is
        R = -14 / B(y,z) * x^{-4} + O(x^{-2}),
independent of every other metric datum (proved by a symbolic Laurent expansion of the
diagonal Ricci with generic even-in-x components).

Applied to g_F(u=0) on Kerr-Newman (M^2 = U(S,J,Q)), whose vanishing component on each
reflection face is computed in closed form from the exact mass-charge couplings
(Lambda = 2M(U_ii U_j - U_i U_ij)/U_i^3, Test 4) and the chart norm q_i:

  Omega=0 (J->0):  R ~ C_Omega(S,Q)/J^4,  C_Omega = -14 / B_J,
     B_J = (4U0 + U_S0^2 + U_Q0^2)^2 /(4 U0) * (1/U_S0^2 + 1/U_Q0^2),
     U0 = U(S,0,Q) = S/(4pi)+Q^2/2+pi Q^4/(4S),  U_S0 = (S^2-pi^2 Q^4)/(4pi S^2),
     U_Q0 = Q(1+pi Q^2/S).
  Phi_e=0 (Q->0):  R ~ C_Phi(S,J)/Q^4,  C_Phi = -14 / B_Q  (same shape, J<->Q roles):
     B_Q = (4U0' + U_S0'^2 + U_J0^2)^2/(4 U0') * (1/U_S0'^2 + 1/U_J0^2),
     U0' = U(S,J,0) = S/(4pi)+pi J^2/S,  U_S0' = (S^2-4pi^2 J^2)/(4pi S^2),  U_J0 = 2pi J/S.

Factored (T6-c):
  C_Omega = -3584 Q^2 S^5 pi^3 (pi Q^2 - S)^2
            / [ (pi^2 Q^4 + 16 pi^2 Q^2 S^2 - 2 pi Q^2 S + S^2)
              * (pi^2 Q^4 + 16 pi^2 Q^2 S^2 - 2 pi Q^2 S + 16 pi S^3 + S^2)^2 ].
  C_Phi   = -14336 J^2 S^5 pi^5 (2pi J - S)^2 (2pi J + S)^2 (4pi^2 J^2 + S^2)
            / [ (16 pi^4 J^4 + 64 pi^4 J^2 S^2 - 8 pi^2 J^2 S^2 + S^4)
              * (16 pi^4 J^4 + 64 pi^3 J^2 S^3 + 64 pi^4 J^2 S^2 - 8 pi^2 J^2 S^2 + 16 pi S^5 + S^4)^2 ].
The corner factor (pi Q^2 - S)^2 in C_Omega vanishes on Omega=0 ∩ extremal (S_ext=pi Q^2 at
J=0); (2pi J - S)^2 in C_Phi vanishes on Phi_e=0 ∩ extremal (S_ext=2pi J at Q=0): the
coefficients degenerate exactly at the divisor corners.

The extremal (order-3, generic) coefficient C_ext(J,Q) is a different (branch-point)
structure -- recorded to high precision in reports/LEAD7_retrodiction_n3.md; its closed
form is the remaining open sub-item.
"""
import sympy as sp
import mpmath as mp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)

# ---- T6-a: universal identity R ~ -14/B * x^-4 (symbolic Laurent of the diagonal Ricci) ----
Sy, x, Qy = sp.symbols('S x Q', positive=True)          # x = boundary coordinate (J on Omega=0)
A = sp.Function('A')(Sy, Qy); B = sp.Function('B')(Sy, Qy); C = sp.Function('C')(Sy, Qy)
a0 = sp.Function('a0')(Sy, Qy); c0 = sp.Function('c0')(Sy, Qy); b4 = sp.Function('b4')(Sy, Qy)
g = [A/x**2 + a0, B*x**2 + b4*x**4, C/x**2 + c0]         # even-in-x metric, middle slot vanishes
Xc = [Sy, x, Qy]; nn = 3
gi = [1/g[i] for i in range(nn)]
def dd(f, k): return sp.diff(f, Xc[k])
Gam = [[[sp.Rational(1, 2)*gi[a]*((dd(g[a], b) if a == c else 0) + (dd(g[a], c) if a == b else 0)
        - (dd(g[b], a) if b == c else 0)) for c in range(nn)] for b in range(nn)] for a in range(nn)]
def Ric(b, d):
    s = 0
    for a in range(nn):
        s += dd(Gam[a][b][d], a) - dd(Gam[a][b][a], d)
        for e in range(nn):
            s += Gam[a][a][e]*Gam[e][b][d] - Gam[a][d][e]*Gam[e][b][a]
    return s
Rsym = sum(gi[b]*Ric(b, b) for b in range(nn))
c4 = sp.simplify(sp.series(Rsym*x**4, x, 0, 1).removeO().subs(x, 0))
check("T6-a.universal_-14/B",
      sp.simplify(c4 + 14/B) == 0 and not c4.has(a0) and not c4.has(c0) and not c4.has(b4),
      "R's x^-4 coefficient = -14/B(y,z), independent of A,C and all subleading terms")

# ---- closed forms ----
S, J, Q, pi = sp.symbols('S J Q pi', positive=True)
U0 = S/(4*pi) + Q**2/2 + pi*Q**4/(4*S); Us0 = (S**2 - pi**2*Q**4)/(4*pi*S**2); Uq0 = Q*(1 + pi*Q**2/S)
BJ = (4*U0 + Us0**2 + Uq0**2)**2/(4*U0)*(1/Us0**2 + 1/Uq0**2)
C_Omega = -14/BJ
U0p = S/(4*pi) + pi*J**2/S; Us0p = (S**2 - 4*pi**2*J**2)/(4*pi*S**2); Uj0 = 2*pi*J/S
BQ = (4*U0p + Us0p**2 + Uj0**2)**2/(4*U0p)*(1/Us0p**2 + 1/Uj0**2)
C_Phi = -14/BQ

# ---- T6-c: factored closed forms are exact identities ----
C_Omega_fac = (-3584*Q**2*S**5*pi**3*(pi*Q**2 - S)**2
               / ((pi**2*Q**4 + 16*pi**2*Q**2*S**2 - 2*pi*Q**2*S + S**2)
                  * (pi**2*Q**4 + 16*pi**2*Q**2*S**2 - 2*pi*Q**2*S + 16*pi*S**3 + S**2)**2))
C_Phi_fac = (-14336*J**2*S**5*pi**5*(2*pi*J - S)**2*(2*pi*J + S)**2*(4*pi**2*J**2 + S**2)
             / ((16*pi**4*J**4 + 64*pi**4*J**2*S**2 - 8*pi**2*J**2*S**2 + S**4)
                * (16*pi**4*J**4 + 64*pi**3*J**2*S**3 + 64*pi**4*J**2*S**2 - 8*pi**2*J**2*S**2 + 16*pi*S**5 + S**4)**2))
check("T6-c.factored_Omega", sp.simplify(C_Omega - C_Omega_fac) == 0,
      "C_Omega closed form = factored form (corner factor (pi Q^2 - S)^2 = Omega=0 ∩ extremal)")
check("T6-c.factored_Phi", sp.simplify(C_Phi - C_Phi_fac) == 0,
      "C_Phi closed form = factored form (corner factor (2pi J - S)^2 = Phi_e=0 ∩ extremal)")

# ---- T6-b: closed forms vs direct high-precision curvature of g_F(u=0) ----
M, Se = sp.symbols('M S_e', positive=True); n = 3; XS = (Se, J, Q)
disc = M**4 - M**2*Q**2 - J**2
fS = pi*(2*M**2 - Q**2 + 2*sp.sqrt(disc)); w = Se/(2*pi) - M**2 + Q**2/2
fJ = sp.sqrt(M**4 - M**2*Q**2 - w**2); fQ = sp.sqrt(-Se/pi + (2/pi)*sp.sqrt(pi*Se*M**2 - pi**2*J**2))
def Fm(f, ins):
    m, c1, c2 = ins; LmA = sp.diff(f, m, c1); LmB = sp.diff(f, m, c2)
    q = 1 + sp.diff(f, ins[0])**2 + sp.diff(f, ins[1])**2 + sp.diff(f, ins[2])**2
    return q**2*(1/LmA**2 + 1/LmB**2)
Mval = sp.sqrt(Se/(4*pi) + pi*J**2/Se + Q**2/2 + pi*Q**4/(4*Se))
Gm = [Fm(fS, (M, J, Q)).subs(M, Mval).subs(pi, sp.pi), Fm(fJ, (M, Se, Q)).subs(M, Mval).subs(pi, sp.pi),
      Fm(fQ, (M, Se, J)).subs(M, Mval).subs(pi, sp.pi)]
mp.mp.dps = 50
print("  [T6-b] lambdifying (~1 min)...")
val = [sp.lambdify(XS, gg, 'mpmath') for gg in Gm]
d1 = [[sp.lambdify(XS, sp.diff(gg, XS[k]), 'mpmath') for k in range(n)] for gg in Gm]
d2 = [[[sp.lambdify(XS, sp.diff(gg, XS[k], XS[l]), 'mpmath') for l in range(n)] for k in range(n)] for gg in Gm]
def Rscalar(pt):
    gg = [val[i](*pt) for i in range(n)]
    dg = [[d1[i][k](*pt) for k in range(n)] for i in range(n)]
    ddg = [[[d2[i][k][l](*pt) for l in range(n)] for k in range(n)] for i in range(n)]
    giv = [1/gg[i] for i in range(n)]
    def Gm2(a, b, c):
        gac = dg[a][b] if a == c else mp.mpf(0); gab = dg[a][c] if a == b else mp.mpf(0)
        gbc = dg[b][a] if b == c else mp.mpf(0)
        return mp.mpf('0.5')*giv[a]*(gac + gab - gbc)
    def dGm(a, b, c, m):
        g2 = (ddg[a][b][m] if a == c else mp.mpf(0)) + (ddg[a][c][m] if a == b else mp.mpf(0)) \
             - (ddg[b][a][m] if b == c else mp.mpf(0))
        g0 = (dg[a][b] if a == c else mp.mpf(0)) + (dg[a][c] if a == b else mp.mpf(0)) \
             - (dg[b][a] if b == c else mp.mpf(0))
        return mp.mpf('0.5')*(-dg[a][m]/gg[a]**2)*g0 + mp.mpf('0.5')*giv[a]*g2
    R = mp.mpf(0)
    for b in range(n):
        Rbb = mp.mpf(0)
        for a in range(n):
            Rbb += dGm(a, b, b, a) - dGm(a, b, a, b)
            for e in range(n):
                Rbb += Gm2(a, a, e)*Gm2(e, b, b) - Gm2(a, b, e)*Gm2(e, b, a)
        R += giv[b]*Rbb
    return R
def rich(fn, expo):   # lim eps->0 fn(eps)*eps^expo, Richardson in eps^2
    h = mp.mpf('1e-4'); Aa = [fn(h/2**k)*(h/2**k)**expo for k in range(4)]
    Bb = [(Aa[k+1]*4 - Aa[k])/3 for k in range(3)]; Cc = [(Bb[k+1]*16 - Bb[k])/15 for k in range(2)]
    return (Cc[1]*64 - Cc[0])/63
COm = sp.lambdify((S, Q), C_Omega.subs(pi, sp.pi), 'mpmath')
CPh = sp.lambdify((S, J), C_Phi.subs(pi, sp.pi), 'mpmath')
ok_om = True
for (Sv, Qv) in [(mp.mpf(20), mp.mpf(1)), (mp.mpf(30), mp.mpf('1.5'))]:
    num = rich(lambda e: Rscalar([Sv, e, Qv]), 4); form = COm(Sv, Qv)
    ok_om = ok_om and abs(num - form) < mp.mpf('1e-18')
check("T6-b.C_Omega_numeric", ok_om, "C_Omega closed form = direct curvature (Richardson, ~20 digits)")
ok_ph = True
for (Sv, Jv) in [(mp.mpf(20), mp.mpf(3)), (mp.mpf(30), mp.mpf(2))]:
    num = rich(lambda e: Rscalar([Sv, Jv, e]), 4); form = CPh(Sv, Jv)
    ok_ph = ok_ph and abs(num - form) < mp.mpf('1e-18')
check("T6-b.C_Phi_numeric", ok_ph, "C_Phi closed form = direct curvature (Richardson, ~20 digits)")

# ---- verdict ----
ntot = 5
if FAILS:
    print(f"VERDICT: FAIL ({len(FAILS)}): {', '.join(FAILS)}")
    raise SystemExit(1)
print(f"VERDICT: LEAD-7 TEST 6 CLEAN -- {ntot}/{ntot}. EXACT leading pole coefficients at "
      f"the two reflection-fixed KN role divisors of g_F(u=0), from the universal identity "
      f"R ~ -14/B x^-4 (symbolic): C_Omega(S,Q) on Omega=0 and C_Phi(S,J) on Phi_e=0, both "
      f"closed rational forms in (S,J/Q,pi), matched to direct curvature to ~20 digits. "
      f"Corner factors (pi Q^2-S)^2 / (2pi J-S)^2 vanish exactly on the divisor corners. "
      f"With Test 5 (orders 3/4/4) this certifies the n=3 complementarity order law AND the "
      f"reflection-fixed coefficients. Open: the extremal (order-3) coefficient closed form.")
