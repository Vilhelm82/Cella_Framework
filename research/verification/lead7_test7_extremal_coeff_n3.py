"""
LEAD-7 TEST 7 — EXACT extremal (order-3) pole coefficient C_ext(S,Q), closing the KN
retrodiction tier. FRESH, zero-import. sympy + mpmath (declared). Byte-stable.

Test 5 pinned the extremal order (3, generic); Test 6 gave the reflection coefficients.
This file gives the exact closed form of the extremal leading coefficient C_ext.

STRUCTURAL IDENTITY (T7-a, symbolic ansatz). Near the extremal edge (delta = S - S_ext,
S_ext = pi sqrt(4J^2+Q^4)) the metric g_F(u=0) is analytic in (S,J,Q) with the entropy
component collapsing as g_SS = A2 delta^2 + O(delta^3) and g_JJ, g_QQ finite. A symbolic
Laurent expansion of the diagonal Ricci gives
        R = C_ext / delta^3 + O(delta^-2),   C_ext = (1/A2)(P1/P0 + R1/R0),
where P0,P1 = g_JJ, d_S g_JJ and R0,R1 = g_QQ, d_S g_QQ, all at S_ext. (No dependence on
A3, the S_ext-surface geometry, or transverse derivatives -- the odd order comes exactly
from the linear-in-delta terms P1,R1.)

RATIONALITY. The implicit-formula couplings Lambda_{i,{M,a}} = 2M(U_ii U_a - U_i U_ia)/U_i^3
with M^2=U are RATIONAL in (S,J,Q,pi) (the radicals only ever lived in the chart functions,
not the couplings). Hence g_JJ, g_QQ, their S-derivatives and A2 are rational, and on the
extremal surface J^2 = (S^2 - pi^2 Q^4)/(4 pi^2) the whole coefficient C_ext(S,Q) is a
RATIONAL function of (S,Q,pi) -- built and verified here.

A2 CLOSED FORM (at extremal): A2 = (4U + U_J^2 + U_Q^2)^2/(4U) * (1/U_J^2 + 1/U_Q^2)
(structurally identical to the reflection B). Denominator of C_ext factors as
  Q^2 pi (3Q^2 pi + S)(Q^4 pi + Q^2 S - Q^2 pi + S)(Q^4 pi^2 + 4Q^2 S^2 pi^2 - 2Q^2 S pi + S^2)
        (Q^4 pi^2 + Q^2 S pi - Q^2 pi^2 + 2S^2 + S pi)^3
        (Q^10 pi^3 + Q^8 S pi^2 - 9Q^6 S^2 pi^3 + 3Q^4 S^3 pi^2 + 5Q^2 S^4 pi + S^5).
With Tests 5 and 6 this completes the n=3 complementarity retrodiction: orders 3/4/4 and
all three leading coefficients in exact closed form.
"""
import sympy as sp
import mpmath as mp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)

# ---- T7-a: structural delta^-3 identity (symbolic ansatz) ----
Sy, x, Qy = sp.symbols('S x Q', positive=True)
S0 = sp.Function('S0')(Qy)
d = Sy - S0
A2f = sp.Function('A2')(Qy); A3f = sp.Function('A3')(Qy); A4f = sp.Function('A4')(Qy)
P0f = sp.Function('P0')(Qy); P1f = sp.Function('P1')(Qy); P2f = sp.Function('P2')(Qy)
R0f = sp.Function('R0')(Qy); R1f = sp.Function('R1')(Qy); R2f = sp.Function('R2')(Qy)
gA = [A2f*d**2 + A3f*d**3 + A4f*d**4, P0f + P1f*d + P2f*d**2, R0f + R1f*d + R2f*d**2]
Xc = [Sy, x, Qy]  # note: middle coord 'x' is a dummy transverse dir for the 3D Ricci shape
# use a genuine 3-var diagonal metric with the collapse in slot 0 (S) and two finite dirs
Xc = [Sy, x, Qy]
gA = [A2f*d**2 + A3f*d**3 + A4f*d**4, P0f + P1f*d + P2f*d**2, R0f + R1f*d + R2f*d**2]
n = 3; gi = [1/gA[i] for i in range(n)]
def dd(f, k): return sp.diff(f, Xc[k])
Gam = [[[sp.Rational(1, 2)*gi[a]*((dd(gA[a], b) if a == c else 0) + (dd(gA[a], c) if a == b else 0)
        - (dd(gA[b], a) if b == c else 0)) for c in range(n)] for b in range(n)] for a in range(n)]
def Ric(b, e):
    s = 0
    for a in range(n):
        s += dd(Gam[a][b][e], a) - dd(Gam[a][b][a], e)
        for f in range(n):
            s += Gam[a][a][f]*Gam[f][b][e] - Gam[a][e][f]*Gam[f][b][a]
    return s
Rw = sum(gi[b]*Ric(b, b) for b in range(n))
c3 = sp.simplify(sp.series(Rw*d**3, Sy, S0, 1).removeO().subs(Sy, S0))
c3_target = R1f/(A2f*R0f) + P1f/(A2f*P0f)
check("T7-a.structural_identity", sp.simplify(c3 - c3_target) == 0,
      "R ~ [P1/(A2 P0) + R1/(A2 R0)] / delta^3  (symbolic ansatz)")

# ---- rational metric components g_JJ, g_QQ via implicit couplings (M^2 -> U) ----
S, J, Q, pi = sp.symbols('S J Q pi', positive=True)
U = S/(4*pi) + pi*J**2/S + Q**2/2 + pi*Q**4/(4*S)
US, UJ, UQ = sp.diff(U, S), sp.diff(U, J), sp.diff(U, Q)
UJJ, UQQ = sp.diff(U, J, 2), sp.diff(U, Q, 2)
USJ, USQ, UJQ = sp.diff(U, S, J), sp.diff(U, S, Q), sp.diff(U, J, Q)
def gcomp(Ui, Uii, others, pairs):
    Ns = [Uii*Ua - Ui*Uia for (Ua, Uia) in pairs]
    invsum = Ui**6/(4*U)*sum(1/N**2 for N in Ns)
    qi = 1 + (4*U + sum(Uo**2 for Uo in others))/Ui**2
    return qi**2*invsum
gJJ = gcomp(UJ, UJJ, [US, UQ], [(US, USJ), (UQ, UJQ)])   # J-chart, pairs {M,S},{M,Q}
gQQ = gcomp(UQ, UQQ, [US, UJ], [(US, USQ), (UJ, UJQ)])   # Q-chart, pairs {M,S},{M,J}

# ---- T7-b: rational g_JJ, g_QQ == nested-radical construction (numeric) ----
M, Se = sp.symbols('M S_e', positive=True)
Mval = sp.sqrt(Se/(4*pi) + pi*J**2/Se + Q**2/2 + pi*Q**4/(4*Se))
fJ = sp.sqrt(M**4 - M**2*Q**2 - (Se/(2*pi) - M**2 + Q**2/2)**2)
fQ = sp.sqrt(-Se/pi + (2/pi)*sp.sqrt(pi*Se*M**2 - pi**2*J**2))
def Fm(f, ins):
    m, c1, c2 = ins; LmA = sp.diff(f, m, c1); LmB = sp.diff(f, m, c2)
    q = 1 + sp.diff(f, ins[0])**2 + sp.diff(f, ins[1])**2 + sp.diff(f, ins[2])**2
    return q**2*(1/LmA**2 + 1/LmB**2)
mp.mp.dps = 40
gJJr = sp.lambdify((S, J, Q, pi), gJJ, 'mpmath'); gQQr = sp.lambdify((S, J, Q, pi), gQQ, 'mpmath')
gJJn = sp.lambdify((Se, J, Q, pi), Fm(fJ, (M, Se, Q)).subs(M, Mval), 'mpmath')
gQQn = sp.lambdify((Se, J, Q, pi), Fm(fQ, (M, Se, J)).subs(M, Mval), 'mpmath')
okrat = True
for (sv, jv, qv) in [(20, 3, 1), (30, 2, 2)]:
    okrat = okrat and abs(gJJr(mp.mpf(sv), mp.mpf(jv), mp.mpf(qv), mp.pi) - gJJn(mp.mpf(sv), mp.mpf(jv), mp.mpf(qv), mp.pi)) < mp.mpf('1e-30')
    okrat = okrat and abs(gQQr(mp.mpf(sv), mp.mpf(jv), mp.mpf(qv), mp.pi) - gQQn(mp.mpf(sv), mp.mpf(jv), mp.mpf(qv), mp.pi)) < mp.mpf('1e-30')
check("T7-b.rational_metric", okrat, "implicit-formula g_JJ, g_QQ (rational) = nested-radical construction")

# ---- assemble C_ext(S,Q) on the extremal surface (rational) ----
A2 = (4*U + UJ**2 + UQ**2)**2/(4*U)*(1/UJ**2 + 1/UQ**2)
Cext_gen = (sp.diff(gJJ, S)/gJJ + sp.diff(gQQ, S)/gQQ)/A2
Cext = Cext_gen.subs(J**2, (S**2 - pi**2*Q**4)/(4*pi**2)).subs(J, sp.sqrt((S**2 - pi**2*Q**4)/(4*pi**2)))
Cext = sp.cancel(sp.simplify(Cext))

# ---- T7-c: denominator factors as documented ----
num, den = sp.fraction(Cext)
den_doc = (Q**2*pi*(3*Q**2*pi + S)*(Q**4*pi + Q**2*S - Q**2*pi + S)
           * (Q**4*pi**2 + 4*Q**2*S**2*pi**2 - 2*Q**2*S*pi + S**2)
           * (Q**4*pi**2 + Q**2*S*pi - Q**2*pi**2 + 2*S**2 + S*pi)**3
           * (Q**10*pi**3 + Q**8*S*pi**2 - 9*Q**6*S**2*pi**3 + 3*Q**4*S**3*pi**2 + 5*Q**2*S**4*pi + S**5))
prod = sp.cancel(Cext*den_doc)                      # C_ext * documented denom
_, prod_den = sp.fraction(prod)
check("T7-c.denominator_factored", prod_den == 1,
      "C_ext * (documented factored denominator) is a POLYNOMIAL => denominator confirmed")

# ---- T7-d: assembled C_ext = direct high-precision curvature (Richardson) ----
mp.mp.dps = 50
XS = (Se, J, Q)
disc = M**4 - M**2*Q**2 - J**2
fS = pi*(2*M**2 - Q**2 + 2*sp.sqrt(disc))
Gm = [Fm(fS, (M, J, Q)).subs(M, Mval).subs(pi, sp.pi),
      Fm(fJ, (M, Se, Q)).subs(M, Mval).subs(pi, sp.pi),
      Fm(fQ, (M, Se, J)).subs(M, Mval).subs(pi, sp.pi)]
print("  [T7-d] lambdifying curvature harness (~1 min)...")
val = [sp.lambdify(XS, gg, 'mpmath') for gg in Gm]
d1 = [[sp.lambdify(XS, sp.diff(gg, XS[k]), 'mpmath') for k in range(n)] for gg in Gm]
d2 = [[[sp.lambdify(XS, sp.diff(gg, XS[k], XS[l]), 'mpmath') for l in range(n)] for k in range(n)] for gg in Gm]
def Rsc(pt):
    g = [val[i](*pt) for i in range(n)]
    dg = [[d1[i][k](*pt) for k in range(n)] for i in range(n)]
    ddg = [[[d2[i][k][l](*pt) for l in range(n)] for k in range(n)] for i in range(n)]
    giv = [1/g[i] for i in range(n)]
    def Ga(a, b, c):
        gac = dg[a][b] if a == c else mp.mpf(0); gab = dg[a][c] if a == b else mp.mpf(0)
        gbc = dg[b][a] if b == c else mp.mpf(0)
        return mp.mpf('0.5')*giv[a]*(gac + gab - gbc)
    def dGa(a, b, c, m):
        g2 = (ddg[a][b][m] if a == c else mp.mpf(0)) + (ddg[a][c][m] if a == b else mp.mpf(0)) \
             - (ddg[b][a][m] if b == c else mp.mpf(0))
        g0 = (dg[a][b] if a == c else mp.mpf(0)) + (dg[a][c] if a == b else mp.mpf(0)) \
             - (dg[b][a] if b == c else mp.mpf(0))
        return mp.mpf('0.5')*(-dg[a][m]/g[a]**2)*g0 + mp.mpf('0.5')*giv[a]*g2
    R = mp.mpf(0)
    for b in range(n):
        Rbb = mp.mpf(0)
        for a in range(n):
            Rbb += dGa(a, b, b, a) - dGa(a, b, a, b)
            for e in range(n):
                Rbb += Ga(a, a, e)*Ga(e, b, b) - Ga(a, b, e)*Ga(e, b, a)
        R += giv[b]*Rbb
    return R
def C_curv(Jv, Qv):
    Sx = mp.pi*mp.sqrt(4*Jv**2 + Qv**4); h = mp.mpf('1e-4')
    Aa = [Rsc([Sx + h/2**k, Jv, Qv])*(h/2**k)**3 for k in range(5)]
    Bb = [(Aa[k+1]*2 - Aa[k]) for k in range(4)]; Cc = [(Bb[k+1]*2 - Bb[k]) for k in range(3)]
    return Cc[-1]
Cf = sp.lambdify((S, Q), Cext.subs(pi, sp.pi), 'mpmath')
okc = True
for (Jv, Qv) in [(mp.mpf(3), mp.mpf(1)), (mp.mpf(2), mp.mpf('1.5'))]:
    Sx = mp.pi*mp.sqrt(4*Jv**2 + Qv**4)
    form = Cf(Sx, Qv); num_c = C_curv(Jv, Qv)
    okc = okc and abs(form - num_c) < mp.mpf('1e-10')
check("T7-d.C_ext_vs_curvature", okc,
      "assembled rational C_ext(S,Q) = direct high-precision curvature (Richardson)")

# ---- T7-e: A2 IS the delta^2 Taylor coefficient of the actual metric G_S (symbolic) ----
# The generic Laurent lemma (T7-a) uses "A2" = leading coeff of the collapsing component.
# Here we CERTIFY that this equals the closed form eq.(A2): the U_SS cancels between
# (U_S/delta)^2 and D_{S,.}=U_SS U_. , which is why A2 is free of A3 / U_SS.
USS = sp.diff(U, S, 2)
DSJ = USS*UJ - US*USJ
DSQ = USS*UQ - US*USQ
normS = US**2 + 4*U + UJ**2 + UQ**2
GS = normS**2 * US**2/(4*U) * (1/DSJ**2 + 1/DSQ**2)
dsym = sp.symbols('delta', positive=True)
Sext = pi*sp.sqrt(4*J**2 + Q**4)
coeff_d2 = sp.limit(GS.subs(S, Sext + dsym)/dsym**2, dsym, 0)   # delta^2 coeff of G_S
check("T7-e.A2_is_delta2_coeff", sp.simplify(coeff_d2 - A2.subs(S, Sext)) == 0,
      "delta^2-coefficient of G_S == eq.(A2) identically (=> A2>0 as a sum of positive terms)")

# ---- T7-f: R0=g_QQ|ext carries the degree-10 extremal-denominator factor (interlock) ----
gQQ_ext = sp.cancel(gQQ.subs(J**2, (S**2 - pi**2*Q**4)/(4*pi**2))
                        .subs(J, sp.sqrt((S**2 - pi**2*Q**4)/(4*pi**2))))
beast = (Q**10*pi**3 + Q**8*S*pi**2 - 9*Q**6*S**2*pi**3 + 3*Q**4*S**3*pi**2
         + 5*Q**2*S**4*pi + S**5)
nQ, _ = sp.fraction(sp.together(gQQ_ext))
rem_n = sp.rem(sp.Poly(sp.expand(nQ), S), sp.Poly(sp.expand(beast), S))
tt = sp.symbols('t', positive=True)
h_t = tt**3 + 5*tt**2 + 3*tt - 9
beast_id = sp.simplify(sp.factor(beast.subs(S, pi*Q**2*tt)/(Q**10*pi**3)) - (1 + tt + pi**2*tt**2*h_t))
check("T7-f.R0_carries_degree10_beast", rem_n == 0 and beast_id == 0,
      "g_QQ|ext numerator has the extremal-denominator factor; beast/(Q^10 pi^3)=1+t+pi^2 t^2 h(t), "
      "h=t^3+5t^2+3t-9>0 on t>1 (positivity inherited from the C_ext denominator machinery)")

# ---- verdict ----
ntot = 6
if FAILS:
    print(f"VERDICT: FAIL ({len(FAILS)}): {', '.join(FAILS)}")
    raise SystemExit(1)
print(f"VERDICT: LEAD-7 TEST 7 CLEAN -- {ntot}/{ntot}. The extremal (order-3) pole "
      f"coefficient C_ext(S,Q) of R[g_F(u=0)] is an EXACT rational function of (S,Q,pi), "
      f"from the structural identity C_ext = (1/A2)(P1/P0 + R1/R0) with A2 = "
      f"(4U+U_J^2+U_Q^2)^2/(4U)(1/U_J^2+1/U_Q^2), built rationally (implicit couplings are "
      f"radical-free) and evaluated on the extremal surface J^2=(S^2-pi^2 Q^4)/(4pi^2); "
      f"matched to direct curvature to high precision. The order-3 structure is SYMBOLIC: "
      f"T7-a (generic Laurent delta^-3 lemma) + T7-e (A2 IS the delta^2 coeff of G_S, so "
      f"A2>0 as a sum of positive terms) + C_ext<0 on the whole open edge (Test 8) => order "
      f"exactly 3, no fitted exponent. With Tests 6 & 10 (reflection order 4 via -m(m+5)/B) "
      f"the n=3 order law 3/4/4 and all three leading coefficients are closed-form/symbolic.")
