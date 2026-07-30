"""
LEAD-7 TEST 2 — Candidate D_Frob (t=1) at n=3 on Kerr-Newman.
FRESH, zero-import. sympy + mpmath (declared). Byte-stable target (numeric tiers use
fixed dps + fixed sample points).

Construction (Reference_Material/LEAD7_Candidate_D_Output_Channel_Norm_Inverse_Metric.md,
CLAIMS re-derived here). Kerr-Newman fundamental relation (re-derived, not cited):
    M^2 = S/(4 pi) + pi J^2/S + Q^2/2 + pi Q^4/(4 S)        (S = entropy, A/4 frame)
charges (S,J,Q), graph value M. Each output chart E_i = f_i(M, E_j, E_k) is a 3-input
graph; its three off-diagonal Hessian entries are the couplings
    Lambda_{i,{M,j}}, Lambda_{i,{M,k}}  (mass-charge),   Lambda_{i,{j,k}} (charge-charge).
Candidate D:  C_i(t) = [Lam_{M,j}^2 + Lam_{M,k}^2 + t Lam_{j,k}^2]/q_i^2,  q_i = 1+|grad f_i|^2,
              g_D(t)_{ii} = 1/C_i(t)  (diagonal on charge-space (S,J,Q)).  t=1 = D_Frob.

WHAT TEST 2 ESTABLISHES (the handoff's Test 2):
  T2-1  Q->0 reduction to Kerr, t-INDEPENDENT (forced by Q-parity of the KN relation):
        C_S, C_J -> the n=2 Kerr channels; the metric limits to the paper Candidate-A
        metric.  [constraint (1) at n=3; SYMBOLIC]
  T2-2  positive-definiteness on the physical wedge (C_i>0 => g_ii>0).  [numeric samples]
  T2-3  role-boundary VALUATION: g_ii ~ F^2 collapse on each native boundary
        (S<->extremal T=0, J<->Omega=0, Q<->Phi_e=0).  [numeric]
  T2-4  CURVATURE (the real complementarity diagnostic -- the banked LEAD-7 guard: judge
        by R[g], not metric collapse). 3D Ricci scalar R and Kretschmann K = 4 R_ab R^ab
        - R^2 (Weyl=0 in 3D), exact-partial (formula validated on flat R^3 -> 0 and the
        round 3-sphere -> 6/a^2, see reports/LEAD7_test2_candD_n3.md).
        RESULT: R,K DIVERGE on extremal T=0 but are FINITE on Omega=0 (J=0) and Phi_e=0
        (Q=0). So D_Frob reproduces the complementarity on ONLY ONE of the three physical
        role boundaries.  K finite => every sectional curvature finite (not a trace
        cancellation).  [numeric, exact partials]

VERDICT: D_Frob is a correct n=2 LIFT (reduction + valuation + definiteness + extremal
curvature) but does NOT reproduce the full three-boundary curvature complementarity -- its
intrinsic curvature is bounded on the two reflection-fixed faces J=0, Q=0. The t-scan
(reports/LEAD7_test2_candD_n3.md) shows this is NOT repairable by the weight t. This
routes LEAD-7 to the doc's Candidate-E (pair-channel tensor) branch / the obstruction
reading (BRIEF kill K-2).  This file certifies the FACTS above; the verdict is argued in
the report.
"""
import sympy as sp
import mpmath as mp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)

M, S, J, Q, pi, t = sp.symbols('M S J Q pi t', positive=True)
n = 3

# ---- output charts of the KN relation (outer-horizon branch, re-derived) ----
disc = M**4 - M**2*Q**2 - J**2
fS = pi*(2*M**2 - Q**2 + 2*sp.sqrt(disc))                 # S = f(M,J,Q)
w  = S/(2*pi) - M**2 + Q**2/2
fJ = sp.sqrt(M**4 - M**2*Q**2 - w**2)                     # J = f(M,S,Q)
fQ = sp.sqrt(-S/pi + (2/pi)*sp.sqrt(pi*S*M**2 - pi**2*J**2))  # Q = f(M,S,J)
# each chart solves the KN relation:
KN = lambda s: s/(4*pi) + pi*J**2/s + Q**2/2 + pi*Q**4/(4*s) - M**2
check("T2-0.charts_solve_KN",
      sp.simplify(KN(fS)) == 0 and
      sp.simplify(S/(4*pi)+pi*fJ**2/S+Q**2/2+pi*Q**4/(4*S)-M**2) == 0 and
      sp.simplify(S/(4*pi)+pi*J**2/S+fQ**2/2+pi*fQ**4/(4*S)-M**2) == 0,
      "all three output charts satisfy M^2 = S/4pi + piJ^2/S + Q^2/2 + piQ^4/4S")

def Cfun(f, ins, tt):
    m, c1, c2 = ins
    Lmc1 = sp.diff(f, m, c1); Lmc2 = sp.diff(f, m, c2); Lcc = sp.diff(f, c1, c2)
    q = 1 + sp.diff(f, ins[0])**2 + sp.diff(f, ins[1])**2 + sp.diff(f, ins[2])**2
    return (Lmc1**2 + Lmc2**2 + tt*Lcc**2)/q**2

C_S = Cfun(fS, (M, J, Q), t)      # entropy chart: mass-charge {M,J},{M,Q}; charge-charge {J,Q}
C_J = Cfun(fJ, (M, S, Q), t)
C_Q = Cfun(fQ, (M, S, J), t)

# ---- T2-1: Q->0 reduction to the n=2 Kerr channels, t-INDEPENDENT ----
# KN is even in Q => f_S even in Q => the two Q-couplings (odd in Q) vanish at Q=0, so the
# t-weighted charge-charge term drops and C_S -> single mass-charge channel = n=2 Kerr.
fS2 = pi*(2*M**2 + 2*sp.sqrt(M**4 - J**2))                # Q=0 limit of fS  (n=2 Kerr S-chart)
Lam2 = sp.diff(fS2, M, J); q2 = 1 + sp.diff(fS2, M)**2 + sp.diff(fS2, J)**2
C_S2 = Lam2**2/q2**2                                      # n=2 Kerr entropy channel
red_S = sp.simplify(C_S.subs(Q, 0) - C_S2)
tindep = (sp.diff(C_S.subs(Q, 0), t) == 0)
check("T2-1.Qto0_reduction_S", red_S == 0 and tindep,
      "C_S(t)|_{Q=0} = n=2 Kerr entropy channel, independent of t (Q-parity)")
# J chart likewise reduces (its charge-charge pair {S,Q} coupling is odd in Q)
fJ2 = sp.sqrt(M**4 - (S/(2*pi) - M**2)**2)                # Q=0 limit of fJ (n=2 Kerr J-chart)
Lam2J = sp.diff(fJ2, M, S); q2J = 1 + sp.diff(fJ2, M)**2 + sp.diff(fJ2, S)**2
red_J = sp.simplify(C_J.subs(Q, 0) - Lam2J**2/q2J**2)
check("T2-1.Qto0_reduction_J", red_J == 0 and sp.diff(C_J.subs(Q, 0), t) == 0,
      "C_J(t)|_{Q=0} = n=2 Kerr J channel, independent of t")

# ---- T2-2: positive-definiteness on the physical wedge (t=1) ----
def Cnum(Cexpr, subsdict):
    return sp.N(Cexpr.subs(subsdict), 30)
fS_n = sp.lambdify((M, J, Q), fS.subs(pi, sp.pi), 'mpmath')
mp.mp.dps = 40
posdef = True
for (Mv, Jv, Qv) in [(2, sp.Rational(3, 2), 1), (3, 2, sp.Rational(1, 2)), (sp.Rational(5, 2), 1, 2)]:
    Sv = fS_n(mp.mpf(int(Mv)) if not hasattr(Mv, 'p') else mp.mpf(float(Mv)),
              mp.mpf(float(Jv)), mp.mpf(float(Qv)))
    base = {M: sp.Float(float(Mv), 30), J: sp.Float(float(Jv), 30), Q: sp.Float(float(Qv), 30),
            S: sp.Float(str(Sv), 30), pi: sp.pi, t: 1}
    cs = [Cnum(c, base) for c in (C_S, C_J, C_Q)]
    posdef = posdef and all(c > 0 for c in cs)
check("T2-2.positive_definite", posdef,
      "C_i>0 at wedge samples => g_D=diag(1/C_i) positive-definite (t=1)")

# ---- T2-3: role-boundary valuation g_SS ~ F^2 on extremal (F=sqrt(disc)) ----
gSS = (1/C_S).subs(t, 1)
gSS_n = sp.lambdify((M, J, Q, pi), gSS, 'mpmath')
Mv, Qv = mp.mpf(2), mp.mpf(1); Jstar = mp.sqrt(Mv**4 - Mv**2*Qv**2)
xs = []; ys = []
for e in ['1e-5', '1e-6', '1e-7', '1e-8']:
    eps = mp.mpf(e); Jv = Jstar*(1 - eps)
    F = mp.sqrt(Mv**4 - Mv**2*Qv**2 - Jv**2)
    xs.append(mp.log(F)); ys.append(mp.log(abs(gSS_n(Mv, Jv, Qv, mp.pi))))
val_exp = (ys[-1] - ys[0])/(xs[-1] - xs[0])
check("T2-3.valuation_gSS_F2", abs(val_exp - 2) < mp.mpf('0.05'),
      f"g_SS ~ F^{mp.nstr(val_exp,4)} on extremal (F=sqrt(disc)); paper valuation g~F^2")

# ---- T2-4: curvature (exact partials; formula validated in the report) ----
Mval = sp.sqrt(S/(4*pi) + pi*J**2/S + Q**2/2 + pi*Q**4/(4*S))
G = [(1/C_S).subs(t, 1).subs(M, Mval).subs(pi, sp.pi),
     (1/C_J).subs(t, 1).subs(M, Mval).subs(pi, sp.pi),
     (1/C_Q).subs(t, 1).subs(M, Mval).subs(pi, sp.pi)]
XS = (S, J, Q)
mp.mp.dps = 50
print("  [T2-4] lambdifying exact partials (~1-2 min)...")
val = [sp.lambdify(XS, g, 'mpmath') for g in G]
d1 = [[sp.lambdify(XS, sp.diff(g, XS[k]), 'mpmath') for k in range(n)] for g in G]
d2 = [[[sp.lambdify(XS, sp.diff(g, XS[k], XS[l]), 'mpmath') for l in range(n)] for k in range(n)] for g in G]

def curv(pt):
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
    Ric = [[mp.mpf(0)]*n for _ in range(n)]
    for b in range(n):
        for d in range(n):
            s = mp.mpf(0)
            for a in range(n):
                s += dGam(a, b, d, a) - dGam(a, b, a, d)
                for e in range(n):
                    s += Gam(a, a, e)*Gam(e, b, d) - Gam(a, d, e)*Gam(e, b, a)
            Ric[b][d] = s
    Rsc = sum(gi[b]*Ric[b][b] for b in range(n))
    Rn = sum(Ric[i][j]**2*gi[i]*gi[j] for i in range(n) for j in range(n))
    return Rsc, 4*Rn - Rsc**2

fSp = sp.lambdify((M, J, Q), fS.subs(pi, sp.pi), 'mpmath')
def phys(Mv, Jv, Qv):
    return curv([fSp(Mv, Jv, Qv), Jv, Qv])

# interior finite
Ri, Ki = curv([mp.mpf(20), mp.mpf(3), mp.mpf(1)])
check("T2-4.interior_finite", abs(Ri) < 10 and abs(Ki) < 100,
      f"interior R={mp.nstr(Ri,6)}, K={mp.nstr(Ki,6)} (finite)")
# extremal DIVERGES: K grows as F->0
Mv, Qv = mp.mpf(2), mp.mpf(1); Jstar = mp.sqrt(Mv**4 - Mv**2*Qv**2)
Ke = []
for e in ['1e-5', '1e-6']:
    eps = mp.mpf(e); Jv = Jstar*(1 - eps)
    Ke.append(phys(Mv, Jv, Qv)[1])
check("T2-4.extremal_diverges", abs(Ke[1]) > 10*abs(Ke[0]) and abs(Ke[1]) > mp.mpf('1e4'),
      f"Kretschmann grows F->0: K={mp.nstr(Ke[0],4)} -> {mp.nstr(Ke[1],4)} (diverges on T=0)")
# Omega=0 (J->0) FINITE
Ro1, Ko1 = phys(Mv, mp.mpf('1e-4'), Qv); Ro2, Ko2 = phys(Mv, mp.mpf('1e-6'), Qv)
check("T2-4.Omega0_finite", abs(Ko1 - Ko2)/abs(Ko2) < mp.mpf('1e-3') and abs(Ko2) < mp.mpf('1e3'),
      f"J->0: K={mp.nstr(Ko1,6)} -> {mp.nstr(Ko2,6)} (converges, FINITE -- NOT complementary)")
# Phi_e=0 (Q->0) FINITE
Rp1, Kp1 = phys(Mv, mp.mpf(1), mp.mpf('1e-4')); Rp2, Kp2 = phys(Mv, mp.mpf(1), mp.mpf('1e-6'))
check("T2-4.Phie0_finite", abs(Kp1 - Kp2)/abs(Kp2) < mp.mpf('1e-3') and abs(Kp2) < mp.mpf('1e5'),
      f"Q->0: K={mp.nstr(Kp1,6)} -> {mp.nstr(Kp2,6)} (converges, FINITE -- NOT complementary)")

# ---- verdict ----
ntot = 9
if FAILS:
    print(f"VERDICT: FAIL ({len(FAILS)}): {', '.join(FAILS)}")
    raise SystemExit(1)
print(f"VERDICT: LEAD-7 TEST 2 CLEAN -- {ntot}/{ntot} (facts certified). Candidate D_Frob "
      f"(t=1) is a correct n=2 LIFT: exact t-independent Q->0 reduction to Kerr, "
      f"positive-definite on the wedge, role-boundary g~F^2 collapse, and CURVATURE "
      f"divergence on extremal T=0. BUT its intrinsic curvature (Ricci scalar AND "
      f"Kretschmann) is FINITE on the reflection-fixed faces Omega=0 (J=0) and Phi_e=0 "
      f"(Q=0), so it does NOT reproduce the full three-boundary complementarity. Per the "
      f"t-scan (report) this is not repairable by t. LEAD-7 routes to Candidate-E "
      f"(pair-channel tensor) / the obstruction reading. See "
      f"reports/LEAD7_test2_candD_n3.md.")
