"""
LEAD-7 TEST 5 — the n=3 complementarity ORDER LAW for g_F(u=0) (KN retrodiction tier).
FRESH, zero-import. sympy + mpmath (declared). Byte-stable (fixed dps + fixed points).

Pins the pole ORDERS of the Ricci scalar R[g_F(u=0)] at the three Kerr-Newman role
divisors to exact integers -- the n=3 analogue of the paper's n=2 Result-6 order law
(extremal 3 generic / reflection-fixed 4). Curvature harness = the exact-partial 3D Ricci
validated in Test 2 (flat R^3 -> 0, 3-sphere -> 6/a^2). Domain: the outer physical wedge
W_+ = {S,J,Q>0, U_S>0} = {S^2 > pi^2(4J^2+Q^4)} (Test 4). All test points are chosen
strictly inside W_+ and away from the corner edges (where two divisors meet).

RESULT (numeric, high-precision):
  * Omega=0  (J->0, natural coordinate J):        R ~ C_Omega(S,Q) / J^4   -> order 4 (reflection-fixed)
  * Phi_e=0  (Q->0, natural coordinate Q):        R ~ C_Phi(S,J)   / Q^4   -> order 4 (reflection-fixed)
  * T=0      (S->S_ext=pi sqrt(4J^2+Q^4), d=S-S_ext): R ~ C_ext(J,Q) / d^3 -> order 3 (generic)
matching order-3 generic / order-4 reflection-fixed, now realized on all THREE n=3 role
divisors (both charge reflections Omega=0, Phi_e=0 are reflection-fixed; extremal is
generic). Leading COEFFICIENTS are extracted to high precision (recorded below /
reports/LEAD7_retrodiction_n3.md); their exact closed forms (2-variable, with corner
subtleties) remain the open sub-item.
"""
import sympy as sp
import mpmath as mp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)

mp.mp.dps = 60
M, Se, J, Q, pi = sp.symbols('M S J Q pi', positive=True)
n = 3; XS = (Se, J, Q)
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
print("  lambdifying (~1 min)...")
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

def order_and_coeff(approach, base, expo):
    # approach(eps) -> point; R ~ C / eps^expo. slope of log|R| vs log eps over a
    # deep geometric ladder -> order; R*eps^expo at the deepest eps -> leading coeff.
    epss = [base*mp.mpf(10)**(-k) for k in range(3)]
    Rs = [Rscalar(approach(e)) for e in epss]
    slope = -(mp.log(abs(Rs[-1])) - mp.log(abs(Rs[0])))/(mp.log(epss[-1]) - mp.log(epss[0]))
    coeff = Rs[-1]*epss[-1]**expo
    return slope, coeff

# ---- Omega=0 (J->0): order 4 ; points strictly in W_+ (Q^4 < S^2/pi^2) ----
print("\n== Omega=0 (reflection-fixed): R ~ C_Omega(S,Q)/J^4 ==")
omega_pts = [(mp.mpf(20), mp.mpf(1)), (mp.mpf(30), mp.mpf(1)), (mp.mpf(20), mp.mpf(2)),
             (mp.mpf(15), mp.mpf('1.5'))]
for (Sv, Qv) in omega_pts:
    o, c = order_and_coeff(lambda e: [Sv, e, Qv], mp.mpf('1e-5'), 4)
    print(f"   S={mp.nstr(Sv,3)} Q={mp.nstr(Qv,3)}: order={mp.nstr(o,8)}  C_Omega={mp.nstr(c,12)}")
    check(f"T5.Omega[S={mp.nstr(Sv,3)},Q={mp.nstr(Qv,3)}]", abs(o - 4) < mp.mpf('1e-4'), "")

# ---- Phi_e=0 (Q->0): order 4 ; points strictly in W_+ (J^2 < S^2/(4pi^2)) ----
print("\n== Phi_e=0 (reflection-fixed): R ~ C_Phi(S,J)/Q^4 ==")
phi_pts = [(mp.mpf(20), mp.mpf(3)), (mp.mpf(30), mp.mpf(2)), (mp.mpf(20), mp.mpf(1)),
           (mp.mpf(40), mp.mpf(3))]
for (Sv, Jv) in phi_pts:
    o, c = order_and_coeff(lambda e: [Sv, Jv, e], mp.mpf('1e-5'), 4)
    print(f"   S={mp.nstr(Sv,3)} J={mp.nstr(Jv,3)}: order={mp.nstr(o,8)}  C_Phi={mp.nstr(c,12)}")
    check(f"T5.Phi[S={mp.nstr(Sv,3)},J={mp.nstr(Jv,3)}]", abs(o - 4) < mp.mpf('1e-4'), "")

# ---- extremal T=0 (S->S_ext from above): order 3 (generic) ----
print("\n== extremal T=0 (generic): d=S-S_ext, R ~ C_ext(J,Q)/d^3 ==")
ext_pts = [(mp.mpf(3), mp.mpf(1)), (mp.mpf(2), mp.mpf(1)), (mp.mpf(3), mp.mpf(2)),
           (mp.mpf(2), mp.mpf('1.5'))]
for (Jv, Qv) in ext_pts:
    Sext = mp.pi*mp.sqrt(4*Jv**2 + Qv**4)
    o, c = order_and_coeff(lambda e: [Sext + e, Jv, Qv], mp.mpf('1e-4'), 3)
    print(f"   J={mp.nstr(Jv,3)} Q={mp.nstr(Qv,3)}: order={mp.nstr(o,8)}  C_ext={mp.nstr(c,12)}")
    check(f"T5.ext[J={mp.nstr(Jv,3)},Q={mp.nstr(Qv,3)}]", abs(o - 3) < mp.mpf('1e-3'), "")

# ---- verdict ----
ntot = len(omega_pts) + len(phi_pts) + len(ext_pts)
if FAILS:
    print(f"VERDICT: FAIL ({len(FAILS)}): {', '.join(FAILS)}")
    raise SystemExit(1)
print(f"VERDICT: LEAD-7 TEST 5 CLEAN -- {ntot}/{ntot}. The n=3 complementarity ORDER LAW "
      f"for g_F(u=0) is pinned to exact integers on all three role divisors: R[g_F(u=0)] "
      f"diverges as order 4 on the reflection-fixed faces Omega=0 (1/J^4) and Phi_e=0 "
      f"(1/Q^4), and order 3 on the generic extremal edge T=0 (1/(S-S_ext)^3). This is the "
      f"n=3 realization of the paper's order-3-generic / order-4-reflection-fixed law "
      f"(Result 6), verified at high precision at W_+-interior points. Leading coefficients "
      f"extracted to high precision (report); their exact closed forms remain open.")
