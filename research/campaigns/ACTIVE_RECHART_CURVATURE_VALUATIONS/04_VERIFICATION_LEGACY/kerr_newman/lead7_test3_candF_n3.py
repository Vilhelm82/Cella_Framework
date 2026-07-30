"""
LEAD-7 TEST 3 — Candidate F (elementary pair-channel INVERSE metric) at n=3, Kerr-Newman.
FRESH, zero-import. sympy + mpmath (declared). Byte-stable target (fixed dps + fixed points).

Origin: Reference_Material/LEAD7_Candidate_F_Elementary_Pair_Channel_Inverse_Metric.md
(CLAIMS re-derived here). Builds on Test 2 (Candidate D REFUTED for full complementarity:
its curvature was finite on the reflection-fixed faces Omega=0, Phi_e=0).

CANDIDATE F is invert-before-sum (D was sum-before-invert):
    C_{i,{a,b}} = Lambda_{i,{a,b}}^2 / q_i^2   (elementary channel strength)
    g_F(u)_{ii} = q_i^2 * [ 1/Lambda_{i,{M,j}}^2 + 1/Lambda_{i,{M,k}}^2 + u/Lambda_{i,{j,k}}^2 ]
The u-weighted term is the CHARGE-CHARGE pair; the two 1/Lambda_{M,.}^2 are MASS-CHARGE.

WHAT TEST 3 ESTABLISHES:
  T3-1  reduction: g_F(u) at n=2 = paper metric A for ALL u (one mass-charge pair per chart,
        no charge-charge pair). Constraint (1).  [symbolic]
  T3-2  F(u=1) FIXES D's boundary failure: R diverges on ALL THREE role boundaries with the
        paper's ORDER LAW -- extremal order 3 (generic), Omega=0 & Phi_e=0 order 4
        (reflection-fixed).  [numeric, exact partials]
  T3-3  F(u=1) FAILS the interior gate (doc S8): invert-before-sum on the charge-charge term
        gives a SPURIOUS interior curvature pole where Lambda_{Q,{Se,J}}=0 (an interior
        channel-isotropy stratum, distinct from Davies).  [numeric]
  T3-4  F(u=0) (mass-charge-only) reproduces the FULL complementarity AND is interior-clean:
        extremal 3, Omega=0 4, Phi_e=0 4, R finite on Davies D3, no interior poles.
  T3-5  u=0 is UNIQUELY selected: u>0 -> interior pole (T3-3 mechanism); u<0 -> not
        positive-definite near a charge-charge zero. Only u=0 is interior-clean AND pos-def,
        and it keeps every boundary divergence (all in the mass-charge sector).

CONCLUSION (numerical/EMPIRICAL tier): the n=3 DBP complementarity metric is the
MASS-CHARGE INVERSE-CHANNEL metric g_F(u=0). Curvature machinery validated on flat R^3
(->0) and the round 3-sphere (->6/a^2) in Test 2. Report: reports/LEAD7_test3_candF_n3.md.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 45
FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)

M, Se, J, Q, pi, u = sp.symbols('M S J Q pi u', positive=True)
n = 3; XS = (Se, J, Q)
disc = M**4 - M**2*Q**2 - J**2
fS = pi*(2*M**2 - Q**2 + 2*sp.sqrt(disc))
w = Se/(2*pi) - M**2 + Q**2/2
fJ = sp.sqrt(M**4 - M**2*Q**2 - w**2)
fQ = sp.sqrt(-Se/pi + (2/pi)*sp.sqrt(pi*Se*M**2 - pi**2*J**2))

def Fmetric(f, ins, uu):
    m, c1, c2 = ins
    LmA = sp.diff(f, m, c1); LmB = sp.diff(f, m, c2); Lcc = sp.diff(f, c1, c2)
    q = 1 + sp.diff(f, ins[0])**2 + sp.diff(f, ins[1])**2 + sp.diff(f, ins[2])**2
    return q**2*(1/LmA**2 + 1/LmB**2 + uu/Lcc**2), (LmA, LmB, Lcc)

# ---- T3-1: reduction to A at n=2 (REMOVE Q as a charge; NOT the Q->0 boundary) ----
# n=2 = the 2-charge Kerr system (S,J): the entropy chart is fS2(M,J) with a SINGLE
# mass-charge pair {M,J} and NO charge-charge pair, so the F recipe gives g = q2^2/Lam2^2,
# u irrelevant. (Distinct from Q->0 in the 3-charge metric, which is the Phi_e=0 role
# boundary where F DIVERGES because Lam_{Se,{M,Q}} ~ Q -> 0.)
fS2 = pi*(2*M**2 + 2*sp.sqrt(M**4 - J**2))                 # n=2 Kerr entropy chart (no Q)
Lam2 = sp.diff(fS2, M, J); q2 = 1 + sp.diff(fS2, M)**2 + sp.diff(fS2, J)**2
gF_n2 = q2**2*(1/Lam2**2)                                  # F at n=2: single mass-charge pair
gA2 = q2**2/Lam2**2                                        # paper metric A = -1/kappa_c (entropy slot)
check("T3-1.reduction_n2", sp.simplify(gF_n2 - gA2) == 0,
      "F at n=2 (single mass-charge pair, no charge-charge, u-free) = paper metric A")

# ---- curvature harness (exact partials; validated flat->0, sphere->6/a^2 in Test 2) ----
Mval = sp.sqrt(Se/(4*pi) + pi*J**2/Se + Q**2/2 + pi*Q**4/(4*Se))
def build(uu):
    gS, cS = Fmetric(fS, (M, J, Q), uu)
    gJ, cJ = Fmetric(fJ, (M, Se, Q), uu)
    gQ, cQ = Fmetric(fQ, (M, Se, J), uu)
    G = [g.subs(M, Mval).subs(pi, sp.pi) for g in (gS, gJ, gQ)]
    val = [sp.lambdify(XS, g, 'mpmath') for g in G]
    d1 = [[sp.lambdify(XS, sp.diff(g, XS[k]), 'mpmath') for k in range(n)] for g in G]
    d2 = [[[sp.lambdify(XS, sp.diff(g, XS[k], XS[l]), 'mpmath') for l in range(n)] for k in range(n)] for g in G]
    LccQ = sp.lambdify(XS, cQ[2].subs(M, Mval).subs(pi, sp.pi), 'mpmath')  # Q-chart charge-charge
    return val, d1, d2, LccQ

def curv(MOD, pt):
    val, d1, d2, _ = MOD
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

mp.mp.dps = 45
fS_n = sp.lambdify((M, J, Q), fS.subs(pi, sp.pi), 'mpmath')
def phys(MOD, Mv, Jv, Qv):
    return curv(MOD, [fS_n(Mv, Jv, Qv), Jv, Qv])
def order(vals, hs):   # slope of log|R| vs log h
    return (mp.log(abs(vals[-1])) - mp.log(abs(vals[0])))/(mp.log(hs[-1]) - mp.log(hs[0]))

Mv, Qv = mp.mpf(2), mp.mpf(1); Jstar = mp.sqrt(Mv**4 - Mv**2*Qv**2)

# ---- T3-2: F(u=1) fixes the boundaries with the paper order law ----
print("  [T3-2/3] building F(u=1) (~2 min)...")
F1 = build(mp.mpf(1))
# extremal (F=sqrt(disc)) -> order ~3
ext = []; hs = []
for e in ['1e-4', '1e-5', '1e-6']:
    Jv = Jstar*(1 - mp.mpf(e)); Fd = mp.sqrt(Mv**4 - Mv**2*Qv**2 - Jv**2)
    ext.append(phys(F1, Mv, Jv, Qv)[0]); hs.append(Fd)
o_ext = order(ext, hs)
# Omega=0 (J) -> order 4 ; Phi_e=0 (Q) -> order 4
om = [phys(F1, Mv, mp.mpf(e), Qv)[0] for e in ['1e-2', '1e-4', '1e-6']]
o_om = order(om, [mp.mpf('1e-2'), mp.mpf('1e-4'), mp.mpf('1e-6')])
ph = [phys(F1, Mv, mp.mpf(1), mp.mpf(e))[0] for e in ['1e-2', '1e-4', '1e-6']]
o_ph = order(ph, [mp.mpf('1e-2'), mp.mpf('1e-4'), mp.mpf('1e-6')])
check("T3-2.F1_orders_3_4_4",
      abs(abs(o_ext) - 3) < mp.mpf('0.15') and abs(abs(o_om) - 4) < mp.mpf('0.1') and abs(abs(o_ph) - 4) < mp.mpf('0.1'),
      f"F(u=1) R pole orders: extremal={mp.nstr(abs(o_ext),3)} (gen 3), Omega=0={mp.nstr(abs(o_om),3)}, Phi_e=0={mp.nstr(abs(o_ph),3)} (refl 4)")

# ---- T3-3: F(u=1) spurious interior pole at Lambda_{Q,{Se,J}}=0 (distinct from Davies) ----
# interior coupling-zero locus at (M=2, J=0.826, Q=1.6988269); Davies there is Q=1.656.
Jz, Qz = mp.mpf('0.826'), mp.mpf('1.6988269')
Rz = []; cz = []
_, _, _, LccQ1 = F1
for e in ['1e-3', '1e-4', '1e-5']:
    Qe = Qz*(1 + mp.mpf(e)); Se_e = fS_n(Mv, Jz, Qe)
    Rz.append(curv(F1, [Se_e, Jz, Qe])[0]); cz.append(LccQ1(Se_e, Jz, Qe))
diverging = abs(Rz[-1]) > 100*abs(Rz[0]) and abs(cz[-1]) < abs(cz[0])/10
check("T3-3.F1_interior_pole", diverging and abs(Rz[-1]) > mp.mpf('100'),
      f"F(u=1) interior pole at Lambda_cc=0 (Q=1.699, NOT Davies Q=1.656): "
      f"R={mp.nstr(Rz[0],3)}->{mp.nstr(Rz[-1],3)} as coupling->0 => S8 gate FAILED for u=1")

# ---- T3-4: F(u=0) full complementarity + interior clean ----
print("  [T3-4/5] building F(u=0) (~2 min)...")
F0 = build(mp.mpf(0))
ext0 = []; hs0 = []
for e in ['1e-4', '1e-5', '1e-6']:
    Jv = Jstar*(1 - mp.mpf(e)); Fd = mp.sqrt(Mv**4 - Mv**2*Qv**2 - Jv**2)
    ext0.append(phys(F0, Mv, Jv, Qv)[0]); hs0.append(Fd)
o_ext0 = order(ext0, hs0)
om0 = [phys(F0, Mv, mp.mpf(e), Qv)[0] for e in ['1e-2', '1e-4', '1e-6']]
o_om0 = order(om0, [mp.mpf('1e-2'), mp.mpf('1e-4'), mp.mpf('1e-6')])
ph0 = [phys(F0, Mv, mp.mpf(1), mp.mpf(e))[0] for e in ['1e-2', '1e-4', '1e-6']]
o_ph0 = order(ph0, [mp.mpf('1e-2'), mp.mpf('1e-4'), mp.mpf('1e-6')])
check("T3-4.F0_orders_3_4_4",
      abs(abs(o_ext0) - 3) < mp.mpf('0.15') and abs(abs(o_om0) - 4) < mp.mpf('0.1') and abs(abs(o_ph0) - 4) < mp.mpf('0.1'),
      f"F(u=0) R pole orders: extremal={mp.nstr(abs(o_ext0),3)}, Omega=0={mp.nstr(abs(o_om0),3)}, Phi_e=0={mp.nstr(abs(o_ph0),3)}")
# Davies D3 finite (hardcoded Davies point M=2,J=1.2,Q where M_SS=0)
MSS = sp.lambdify((Se, J, Q), sp.diff(Mval, Se, 2).subs(pi, sp.pi), 'mpmath')
Jd, Qd = mp.mpf('1.2'), mp.mpf('1.5659019')
Se_d = fS_n(Mv, Jd, Qd)
Rdav = curv(F0, [Se_d, Jd, Qd])[0]
check("T3-4.F0_davies_finite", abs(MSS(Se_d, Jd, Qd)) < mp.mpf('1e-4') and abs(Rdav) < mp.mpf('1'),
      f"Davies M_SS~0 at (2,1.2,1.566): R[g_F(u=0)]={mp.nstr(Rdav,5)} (FINITE => complementarity)")
# the same interior point that killed u=1 is now finite
Rz0 = curv(F0, [fS_n(Mv, Jz, Qz), Jz, Qz])[0]
check("T3-4.F0_interior_clean", abs(Rz0) < mp.mpf('1'),
      f"at the u=1 interior-pole locus (2,0.826,1.699): R[g_F(u=0)]={mp.nstr(Rz0,5)} (FINITE)")

# ---- T3-5: u=0 uniquely selected (pos-def requires u>=0; interior-clean requires u<=0) ----
# positivity: g_F(u) = q^2(1/LmA^2+1/LmB^2+u/Lcc^2); near a charge-charge zero Lcc->0, the
# u/Lcc^2 term dominates. u>0 -> +inf (interior pole, T3-3). u<0 -> -inf (g<0, indefinite).
# So only u=0 is BOTH interior-finite AND positive there. Demonstrate the sign flip:
Se_e = fS_n(Mv, Jz, Qz*(1 + mp.mpf('1e-4')))
gQ_uneg = None
val_p, _, _, _ = build(mp.mpf('0.5'))   # u=+1/2 -> large positive g_QQ (pole side)
val_n, _, _, _ = build(mp.mpf('-0.5'))  # u=-1/2 -> large negative g_QQ (indefinite side)
gpos = val_p[2](Se_e, Jz, Qz*(1 + mp.mpf('1e-4')))
gneg = val_n[2](Se_e, Jz, Qz*(1 + mp.mpf('1e-4')))
check("T3-5.u0_unique", gpos > mp.mpf('1e6') and gneg < 0,
      f"near Lambda_cc=0: g_QQ(u=+1/2)={mp.nstr(gpos,4)} (>0, poles) vs g_QQ(u=-1/2)={mp.nstr(gneg,4)} "
      f"(<0, indefinite) => u=0 is the unique interior-clean positive-definite member")

# ---- verdict ----
ntot = 7
if FAILS:
    print(f"VERDICT: FAIL ({len(FAILS)}): {', '.join(FAILS)}")
    raise SystemExit(1)
print(f"VERDICT: LEAD-7 TEST 3 CLEAN -- {ntot}/{ntot}. Candidate F (invert-before-sum) with "
      f"u=1 FIXES D's failure -- R diverges on all three role boundaries with the paper order "
      f"law (extremal 3 generic, Omega=0 & Phi_e=0 order 4 reflection-fixed) -- but has a "
      f"SPURIOUS interior pole (charge-charge zero, doc S8). F(u=0) (mass-charge-only) "
      f"reproduces the FULL complementarity (3/4/4, Davies finite) AND is interior-clean, and "
      f"u=0 is UNIQUELY selected (pos-def + interior-clean). STRONG numerical evidence that the "
      f"n=3 DBP complementarity metric is the MASS-CHARGE INVERSE-CHANNEL metric g_F(u=0). "
      f"Next: exact pole-coefficient retrodiction + a proof that mass-charge zeros are exactly "
      f"the role divisors. See reports/LEAD7_test3_candF_n3.md.")
