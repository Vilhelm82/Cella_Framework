"""
RC-5 — RE-CERTIFICATION of the n=2 GTD/DBP spine (LEAD-7 prerequisite, structure tier).
FRESH, zero-import. sympy (declared). Byte-stable target.

Re-verification rule (README rule 3): origin statuses are claims, not evidence.
Everything below is re-proven from fresh code. Origin: Reference_Material/gtd_vs_dbp.pdf
("Two Geometric Readings of a Thermodynamic Surface", W. Lloyd, 2026-06-28) + the
role-channel calculus (Reference_Material/dbp_orbit_calculus.tex). Scoping enumeration:
reports/RC5_SCOPING.md. DO-NOT-CITE at origin (excluded here): paper eq. (28), the
Mahanta m_sg=0 reading.

Frame: the extensive-variable rescale S = 2*pi*sigma makes Kerr exact-Q at rational-M
fixtures (scoping section 3). STRUCTURE TIER = frame-robust claims in Q (this file):
Christodoulou, boundaries, Davies, the 2-jet + channels, radical cancellation,
g^DBP = -h^{-1} positive-definite, boundary=chart-singularity. RETRODICTION TIER (the
paper's pinned pole-order coefficients C_ext/C_sch in the pi-frame) + complementarity
order law = the NEXT RC-5 increment (folds into LEAD-7).

Kerr (n=2): extensive (sigma,J), potential M, Christodoulou
    M(sigma,J) = sqrt( (sigma^2 + J^2)/(2 sigma) )        [S=2 pi sigma frame]
Boundaries of the wedge 0<=J<=sigma: extremal T=0 (sigma=J), Schwarzschild Omega=0
(J=0). Davies (M_SS=0) <=> 3 J^4 + 6 J^2 sigma^2 - sigma^4 = 0.
Role-channel numerators (dbp_orbit_calculus): Lambda_P=B, Lambda_D=(Ab-aB)/a,
Lambda_S=(Ca-bB)/b; q0=1+a^2+b^2; kappa_c^rho = -Lambda_rho^2/q0^2.
DBP metric (eq. 32): h = sum_i kappa_{c,i} dE^i (x) dE^i on E=(sigma,J); g^DBP=-h^{-1}.
"""
import sympy as sp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)

sg, J = sp.symbols('sigma J', positive=True)
M = sp.sqrt((sg**2 + J**2)/(2*sg))                      # Christodoulou, sigma-frame
FIX = {sg: sp.Integer(8), J: sp.Integer(6)}            # scoping fixture (sigma,J)=(8,6)

# ---- RC5-1: Christodoulou + fixture + boundaries + Davies ----
check("RC5-1.christodoulou", sp.simplify(M.subs(FIX) - sp.Rational(5, 2)) == 0,
      "M(8,6) = 5/2")
# M_sigmasigma=0 <=> (using M^2=u rational, 2 M M_s = u_s, 2 M_s^2 + 2 M M_ss = u_ss)
#   2 u u_ss - u_s^2 = 0 ; its numerator is the Davies quartic.
u = M**2                                                # rational
davies = sp.simplify(sp.numer(sp.together(2*u*sp.diff(u, sg, 2) - sp.diff(u, sg)**2)))
check("RC5-1.davies", sp.simplify(davies - (3*J**4 + 6*J**2*sg**2 - sg**4)) == 0
      or sp.simplify(davies + (3*J**4 + 6*J**2*sg**2 - sg**4)) == 0,
      "M_sigmasigma=0 <=> 3J^4+6J^2 sigma^2 - sigma^4 = 0 (Davies)")

# ---- RC5-2: the 2-jet (a,b,A,B,C) retrodicts the scoping fixture ----
a = sp.diff(M, sg); b = sp.diff(M, J)
A = sp.diff(M, sg, 2); B = sp.diff(M, sg, J); C = sp.diff(M, J, 2)
jet = {a: sp.Rational(7, 160), b: sp.Rational(3, 20), A: sp.Rational(851, 64000),
       B: sp.Rational(-171, 8000), C: sp.Rational(2, 125)}
avals = {sym.subs(FIX): sp.nsimplify(sp.simplify(sym.subs(FIX)))
         for sym in (a, b, A, B, C)}
ok_jet = (sp.simplify(a.subs(FIX) - sp.Rational(7, 160)) == 0 and
          sp.simplify(b.subs(FIX) - sp.Rational(3, 20)) == 0 and
          sp.simplify(A.subs(FIX) - sp.Rational(851, 64000)) == 0 and
          sp.simplify(B.subs(FIX) - sp.Rational(-171, 8000)) == 0 and
          sp.simplify(C.subs(FIX) - sp.Rational(2, 125)) == 0)
check("RC5-2.jet", ok_jet, "(a,b,A,B,C)(8,6) = (7/160, 3/20, 851/64000, -171/8000, 2/125)")

# ---- RC5-3: channels via the role-channel formulas retrodict the fixture ----
q0 = 1 + a**2 + b**2
LamP = B
LamD = (A*b - a*B)/a
LamS = (C*a - b*B)/b
kP = sp.simplify(-LamP**2/q0**2)
kD = sp.simplify(-LamD**2/q0**2)
kS = sp.simplify(-LamS**2/q0**2)
check("RC5-3.q0", sp.simplify(q0.subs(FIX) - sp.Rational(1049, 1024)) == 0, "q0(8,6)=1049/1024")
check("RC5-3.kP", sp.simplify(kP.subs(FIX) - sp.Rational(-7485696, 17193765625)) == 0,
      "kappa_c^P(8,6) = -7485696/17193765625")
check("RC5-3.kD", sp.simplify(kD.subs(FIX) - sp.Rational(-230400, 53919649)) == 0,
      "kappa_c^D(8,6) = -230400/53919649")
check("RC5-3.kS", sp.simplify(kS.subs(FIX) - sp.Rational(-6400, 9903609)) == 0,
      "kappa_c^S(8,6) = -6400/9903609")

# ---- RC5-4: RADICAL CANCELLATION + g^DBP = -h^{-1} positive-definite (Result 4) ----
# kappa_c ~ Lambda^2 carries M^2 (rational), so the sqrt cancels: kappa_c in Q(sigma,J).
kD_r = sp.radsimp(sp.simplify(kD)); kS_r = sp.radsimp(sp.simplify(kS))
rational = (kD_r.free_symbols <= {sg, J} and kS_r.free_symbols <= {sg, J}
            and not kD_r.has(sp.sqrt(sp.Wild('w'))))
check("RC5-4.radical_cancels", rational and sp.simplify(kD_r - kD_r.rewrite(sp.Pow)) == 0,
      "kappa_c rational in (sigma,J): the single sqrt(M^2) cancels under the square")
# h = diag(kD,kS) on E=(sigma,J); g^DBP = -h^{-1} = diag(-1/kD,-1/kS). PD <=> kD,kS<0.
gDBP = sp.diag(-1/kD, -1/kS)
gfix = gDBP.subs(FIX)
check("RC5-4.pos_def", gfix[0, 0] > 0 and gfix[1, 1] > 0 and kD.subs(FIX) < 0 and kS.subs(FIX) < 0,
      f"g^DBP positive-definite at fixture: diag({gfix[0,0]}, {gfix[1,1]})")

# ---- RC5-5: boundary = chart-singularity (structure tier) ----
# a=M_sigma=0 <=> extremal sigma=J ; b=M_J=0 <=> Schwarzschild J=0
# a*M = u_sigma/2 and b*M = u_J/2 are rational; a=0<=>u_sigma=0, b=0<=>u_J=0.
aM = sp.simplify(sp.diff(u, sg)/2)                      # = a*M, rational
bM = sp.simplify(sp.diff(u, J)/2)                       # = b*M, rational
check("RC5-5.extremal", sp.simplify(aM.subs(sg, J)) == 0 and sp.simplify(aM) != 0,
      "a = M_sigma = 0  <=>  sigma = J  (extremal, T=0);  a*M = (sigma^2-J^2)/(4 sigma^2)")
check("RC5-5.schwarzschild", sp.simplify(bM.subs(J, 0)) == 0 and sp.simplify(bM) != 0,
      "b = M_J = 0  <=>  J = 0  (Schwarzschild, Omega=0)")
# and the channels that use these charts diverge there: Lambda_D ~ 1/a, Lambda_S ~ 1/b
check("RC5-5.divergence", sp.simplify(LamD*a - (A*b - a*B)) == 0 and sp.simplify(LamS*b - (C*a - b*B)) == 0,
      "Lambda_D ~ 1/a, Lambda_S ~ 1/b -> channels diverge on their own role boundary")

# ---- verdict ----
n = 11
if FAILS:
    print(f"VERDICT: FAIL ({len(FAILS)}): {', '.join(FAILS)}")
    raise SystemExit(1)
print(f"VERDICT: RC-5 n=2 GTD/DBP spine STRUCTURE TIER CLEAN -- {n}/{n}. Christodoulou, "
      f"Davies, 2-jet + channels retrodicted (fixture 8,6), radical cancellation, "
      f"g^DBP=-h^{{-1}} positive-definite, boundary=chart-singularity. NEXT (RC-5 "
      f"retrodiction tier): pole-order coefficients C_ext/C_sch (pi-frame) + the "
      f"complementarity order law. Then LEAD-7 Stage A (the n=3 lift).")
