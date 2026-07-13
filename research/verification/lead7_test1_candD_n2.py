"""
LEAD-7 TEST 1 — Candidate D (output-channel norm inverse metric) at n=2.
FRESH, zero-import. sympy + mpmath (declared). Byte-stable target.

Origin of the construction: Reference_Material/LEAD7_Candidate_D_Output_Channel_Norm_
Inverse_Metric.md (a design handoff -> CLAIMS, not evidence; re-derived here from the
role-channel calculus). Prerequisite spine: verification/recert_gtd_dbp_n2.py (d047d21b,
11/11 x2). Pole-order machinery mirrors reports/LEAD7_pole_orders.md.

CANDIDATE D. For each output charge E_i = f_i(M, E_{j..}) collect the off-diagonal
role-couplings Lambda_{i,{.,.}} in that output chart, aggregate their normalized squares
into a scalar strength
    C_i(t) = [ sum_{mass-charge pairs} Lambda^2  +  t * sum_{charge-charge pairs} Lambda^2 ] / q_i^2 ,
and set the diagonal metric g_D(t)_{ii} = 1 / C_i(t).  (h_D = -sum_i C_i dE^i(x)dE^i,
g_D = -h_D^{-1}.)

WHAT TEST 1 CHECKS (the handoff's Test 1 = "D at n=2"):
  (a) reduction: at n=2 each output chart has exactly ONE input pair {M, E_j} -- a
      mass-charge pair, no charge-charge pair -- so C_i = Lambda_i^2/q0^2 = -kappa_c,i and
      g_D,ii = 1/C_i = -1/kappa_c,i = the paper metric g_A. D IS A at n=2 (constraint 1).
  (b) t drops out: the charge-charge sum is empty at n=2, so C_i(t) is independent of t.
  (c) pole orders of R[g_D]: extremal 3, Schwarzschild 4, finite on Davies -- recomputed
      from the D construction (Brioschi), matching the paper's Result-6 law.

Kerr (n=2), sigma-frame S=2 pi sigma: M(sigma,J)=sqrt((sigma^2+J^2)/(2 sigma)).
Role numerators (dbp_orbit_calculus): Lambda_D=(A b - a B)/a, Lambda_S=(C a - b B)/b;
q0 = 1 + a^2 + b^2; kappa_c^rho = -Lambda_rho^2/q0^2.  The two SOLVABLE output charts at
n=2 are E=sigma (uses Lambda_D) and E=J (uses Lambda_S); Lambda_P=B is the directive
channel (carried, not an inverted output), so the n=2 DBP metric is diag over (D,S) --
exactly as in RC-5.
"""
import sympy as sp
import mpmath as mp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)

sg, J, t = sp.symbols('sigma J t', positive=True)
M = sp.sqrt((sg**2 + J**2)/(2*sg))
FIX = {sg: sp.Integer(8), J: sp.Integer(6)}

a = sp.diff(M, sg); b = sp.diff(M, J)
A = sp.diff(M, sg, 2); B = sp.diff(M, sg, J); C = sp.diff(M, J, 2)
q0 = 1 + a**2 + b**2

# role couplings on the two output charts (sigma-output uses D, J-output uses S)
LamD = (A*b - a*B)/a          # coupling in the sigma output chart
LamS = (C*a - b*B)/b          # coupling in the J output chart
kcD = -LamD**2/q0**2          # paper channel kappa_c^D
kcS = -LamS**2/q0**2          # paper channel kappa_c^S

# ---- Candidate D construction (built from the D definition, NOT assuming reduction) ----
# each n=2 output chart has ONE input pair {M, E_j}: a mass-charge pair. no charge-charge
# pair exists, so the t-weighted sum is empty. C_i = (single mass-charge Lambda)^2 / q0^2.
massD = LamD**2                # sum of mass-charge coupling squares, sigma chart
massS = LamS**2                # sum of mass-charge coupling squares, J chart
chchD = sp.Integer(0)         # charge-charge coupling squares, sigma chart (none at n=2)
chchS = sp.Integer(0)         # charge-charge coupling squares, J chart (none at n=2)
C_D = (massD + t*chchD)/q0**2
C_S = (massS + t*chchS)/q0**2
gD_ss = 1/C_D                  # Candidate D metric, sigma-sigma
gD_jj = 1/C_S                  # Candidate D metric, J-J

# ---- T1-1: reduction to the paper metric A (constraint 1) ----
gA_ss = -1/kcD                 # paper diagonal
gA_jj = -1/kcS
check("T1-1.reduction",
      sp.simplify(gD_ss - gA_ss) == 0 and sp.simplify(gD_jj - gA_jj) == 0,
      "g_D,ii = 1/C_i = -1/kappa_c,i = g_A  (D reduces EXACTLY to the paper metric at n=2)")

# ---- T1-2: t is structurally absent at n=2 (no charge-charge pair) ----
check("T1-2.t_irrelevant",
      sp.diff(C_D, t) == 0 and sp.diff(C_S, t) == 0,
      "dC_i/dt = 0: the charge-charge sum is empty at n=2, so C_i(t) is t-independent")

# ---- T1-3: fixture values match RC-5's channels ----
# kappa_c^D(8,6) = -230400/53919649  ->  g_D,ss = -1/kcD = 53919649/230400
# kappa_c^S(8,6) = -6400/9903609     ->  g_D,jj = -1/kcS = 9903609/6400
check("T1-3.fixture",
      sp.simplify(gD_ss.subs(FIX) - sp.Rational(53919649, 230400)) == 0 and
      sp.simplify(gD_jj.subs(FIX) - sp.Rational(9903609, 6400)) == 0,
      "g_D(8,6) = diag(53919649/230400, 9903609/6400)  (= -1/kappa_c^{D,S}, RC-5)")

# ---- T1-4: pole orders of R[g_D] recomputed from the D construction ----
# g_D = diag(gD_ss, gD_jj). Gaussian curvature via Brioschi (diagonal metric), pole order
# = -slope(log|R| vs log eps) into each boundary. mpmath, dps=50.
mp.mp.dps = 50
Ess = sp.lambdify((sg, J), gD_ss, 'mpmath')          # E(sigma,J) = g_11
Gjj = sp.lambdify((sg, J), gD_jj, 'mpmath')          # G(sigma,J) = g_22
# first/second partials of E,G (F=0 diagonal)
dEs = sp.lambdify((sg, J), sp.diff(gD_ss, sg), 'mpmath')
dEj = sp.lambdify((sg, J), sp.diff(gD_ss, J), 'mpmath')
dEss = sp.lambdify((sg, J), sp.diff(gD_ss, sg, 2), 'mpmath')
dEjj = sp.lambdify((sg, J), sp.diff(gD_ss, J, 2), 'mpmath')
dGs = sp.lambdify((sg, J), sp.diff(gD_jj, sg), 'mpmath')
dGj = sp.lambdify((sg, J), sp.diff(gD_jj, J), 'mpmath')
dGss = sp.lambdify((sg, J), sp.diff(gD_jj, sg, 2), 'mpmath')
dGjj = sp.lambdify((sg, J), sp.diff(gD_jj, J, 2), 'mpmath')

def Rbrio(s, j):
    E = Ess(s, j); G = Gjj(s, j); F = mp.mpf(0)
    Es = dEs(s, j); Ej = dEj(s, j); Ejj = dEjj(s, j)
    Gs = dGs(s, j); Gj = dGj(s, j); Gss = dGss(s, j)
    M1 = mp.matrix([[-Ejj/2 - Gss/2, Es/2, -Ej/2],
                    [-Gs/2, E, F],
                    [Gj/2, F, G]])
    M2 = mp.matrix([[0, Ej/2, Gs/2],
                    [Ej/2, E, F],
                    [Gs/2, F, G]])
    return (mp.det(M1) - mp.det(M2))/(E*G - F**2)**2

def order(ap):
    xs = []; ys = []
    for e in ['1e-2', '1e-3', '1e-4', '1e-5']:
        eps = mp.mpf(e)
        s, j = (6 + eps, mp.mpf(6)) if ap == 'ext' else (mp.mpf(8), eps)
        R = Rbrio(s, j); ys.append(mp.log(abs(R))); xs.append(mp.log(eps))
    return -(ys[-1] - ys[0])/(xs[-1] - xs[0])

sD = 6*mp.sqrt(3 + 2*mp.sqrt(3))                       # Davies point (sigma, J=6)
o_ext = order('ext'); o_sch = order('sch'); R_dav = Rbrio(sD, mp.mpf(6))
check("T1-4.extremal_order3", abs(o_ext - 3) < sp.Rational(1, 10),
      f"R[g_D] extremal pole order = {mp.nstr(o_ext, 4)} (target 3)")
check("T1-4.schwarzschild_order4", abs(o_sch - 4) < sp.Rational(1, 10),
      f"R[g_D] Schwarzschild pole order = {mp.nstr(o_sch, 4)} (target 4)")
check("T1-4.davies_finite", abs(R_dav) < mp.mpf('1e-3'),
      f"R[g_D](Davies) = {mp.nstr(R_dav, 5)} (finite, complementarity)")

# ---- verdict ----
n = 6
if FAILS:
    print(f"VERDICT: FAIL ({len(FAILS)}): {', '.join(FAILS)}")
    raise SystemExit(1)
print(f"VERDICT: LEAD-7 TEST 1 CLEAN -- {n}/{n}. Candidate D reduces EXACTLY to the "
      f"paper metric A at n=2 (g_D,ii = 1/C_i = -1/kappa_c,i), the weight t is "
      f"structurally absent (no charge-charge pair), and R[g_D] reproduces the paper's "
      f"order law: extremal 3, Schwarzschild 4, finite on Davies. Constraint (1) "
      f"(n=2 reduction) HOLDS. NEXT: Test 2 -- Candidate D_Frob (t=1) at n=3 on "
      f"Kerr-Newman.")
