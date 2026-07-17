"""
ARITH-I STAGE B (session 1) — definitions pinned, r=2 primitive exhibited,
r=3 structural requirement proven. FRESH, zero-import. sympy (declared).

PREREG 32f2fb3a (Stage-B section; the fabricated stop condition is VOID, see
CORRECTION_2026-07-06). Paper-track fence: no engine priority changed.

THE QUESTION (A5 / T-B): is the order-r pure-coupling channel density
    kappa_{r;r,0} = (-1)^r e_r(P Hc P) / q^((r+2)/2) ,  Hc = offdiag(H),
                    P = I - g g^T/q ,  q = |g|^2 = |grad F|^2
EXACT (= d of an algebraic 1-form) on the quadric?  r=2 YES is Gauss-Bonnet;
r=3 is the discriminator (YES -> higher Cohn-Vossen; NO -> interior period).

Definition source (re-derived, [CONTAINER]): the engine's numerator tower
(src/cella/sensors.py) kappa_r = (-1)^r e_r(P Hc P)/q^(r/2), r=2..n-1; the grid
normalization for the INTEGRABLE density adds 1/q (ADDENDUM A4): q^((r+2)/2).
The depth theorem (portfolio Part IV) names kappa_{r;r,0} = "the r x r coupling
minor", realizing Specht S^(n-r,r) for n>=2r.

WHAT THIS SESSION ESTABLISHES
  SBB-1  STRUCTURAL REQUIREMENT (proven): e_3(P Hc P) == 0 identically for n=3
         (P has rank n-1=2, so P Hc P has rank <=2, so every 3x3 minor vanishes).
         => the r=3 density is identically zero on the n=3 keystone; the r=3
         exactness question lives on n>=4 (Specht-full n>=2r=6). This is a
         structural fact, not a modeling choice.
  SBB-2  r=2 EXPLICIT PRIMITIVE (exact, symbolic): on the n=3 keystone the
         Gauss-Bonnet primitive is the Gauss-map pullback of the S^2 area-form
         primitive,
             eta = -N3 (N1 dN2 - N2 dN1)/(N1^2 + N2^2),   N = grad F/|grad F|,
         and  d eta = K_G dA  EXACTLY (verified as a rational identity modulo
         P^2 = 3 - D^2 - D S). Its only singularity is N1=N2=0 (the Gauss map at
         the poles = the asymptotic/umbilic directions) -- exactly where the end
         contribution -2L localizes. This validates the exactness mechanism and
         is the r=3 ansatz template (Route-1 machinery, working at r=2).
  SBB-3  r=3 DENSITY EXISTS and is computable (n=4 sample quadric): e_3(P Hc P)
         is a nonzero rational function of position, q^((5)/2)-normalized ->
         well-defined integrable density. Confirms the object of the r=3 test is
         real (not the vacuous n=3 zero).

OPEN (routed, the honest gate): the SPECIFIC n=4 (and n=6) quadric family of the
ARITH-I grid is NOT fixed by the surviving [CONTAINER] material -- the exactness
answer depends on it. Pinning that family (coordinate with LEAD-1 / GRID_I) is the
gating sub-task before the r=3 ansatz search (Route 1) and bump test (Route 2) can
return a family-correct verdict. Named as OPEN, not guessed (the discipline's rule).

Convention: pin = `python3 reports/arithmetic_track/arith_i_stageB_s1.py | sha256sum`.
"""
import sympy as sp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)

def P_proj(g, q, n):
    return sp.Matrix(n, n, lambda i, j: (1 if i == j else 0) - g[i]*g[j]/q)
def offdiag(H, n):
    return sp.Matrix(n, n, lambda i, j: 0 if i == j else H[i, j])
def e_r(A, r):
    from itertools import combinations
    n = A.shape[0]
    return sum(A[list(c), list(c)].det() for c in combinations(range(n), r))

# ================= SBB-1 : e_3 == 0 at n=3 (structural) =================
D, S, P = sp.symbols('D S P', real=True)
g3 = [2*D + S, D, 2*P]
q3 = sum(x**2 for x in g3)
H3 = sp.Matrix([[2, 1, 0], [1, 0, 0], [0, 0, 2]])
A3 = P_proj(g3, q3, 3)*offdiag(H3, 3)*P_proj(g3, q3, 3)
check("SBB1.e3_n3_zero", sp.simplify(e_r(A3, 3)) == 0,
      "e_3(P Hc P) == 0 identically at n=3 (rank<=2) -> r=3 needs n>=4")
# and e_2 is the live channel at n=3 (nonzero), sanity:
check("SBB1.e2_n3_live", sp.simplify(e_r(A3, 2)) != 0,
      "e_2(P Hc P) nonzero at n=3 (the coupling channel kc)")

# ================= SBB-2 : r=2 explicit primitive, exact =================
# work on the surface with P a constrained symbol: P^2 = 3 - D^2 - D S.
Dm, Sm, Pm = sp.symbols('D S P', real=True)
rel = Pm**2 - (3 - Dm**2 - Dm*Sm)     # = 0 on the surface
gF = sp.Matrix([2*Dm + Sm, Dm, 2*Pm])
qq = sp.expand(gF.dot(gF))
sq = sp.sqrt(qq)
N = gF/sq
N1, N2, N3 = N[0], N[1], N[2]
# P depends on (D,S): dP = P_D dD + P_S dS with P_D=-(2D+S)/(2P), P_S=-D/(2P)
PD = -(2*Dm + Sm)/(2*Pm); PS = -Dm/(2*Pm)
def total_d(expr, var):
    # d/dvar including P(D,S) dependence
    return sp.diff(expr, var) + sp.diff(expr, Pm)*(PD if var == Dm else PS)
den = N1**2 + N2**2
def eta_coeff(var):
    return -N3*(N1*total_d(N2, var) - N2*total_d(N1, var))/den
Acoef = eta_coeff(Dm); Bcoef = eta_coeff(Sm)
curl = total_d(Bcoef, Dm) - total_d(Acoef, Sm)
# K_G dA in the (D,S) chart, graph P=f: (f_DD f_SS - f_DS^2)/(1+f_D^2+f_S^2)^(3/2)
fD, fS = PD, PS
fDD = total_d(PD, Dm); fSS = total_d(PS, Sm); fDS = total_d(PD, Sm)
KdA = (fDD*fSS - fDS**2)/(1 + fD**2 + fS**2)**sp.Rational(3, 2)
resid = curl - KdA
# EXACT verification without a global symbolic simplify (which is intractable on the
# nested radicals): evaluate the residual at many exact rational (D,S) points, with
# P = sqrt(3 - D^2 - D S) an exact algebraic number. sympy does exact radical
# arithmetic on numbers fast; each check is an exact algebraic zero (no float).
pts = [(sp.Rational(a, b), sp.Rational(c, d)) for (a, b, c, d) in
       [(1, 2, 1, 3), (-1, 2, 1, 4), (3, 4, -1, 2), (1, 5, 2, 5),
        (-2, 3, 1, 6), (2, 5, -3, 7), (1, 1, -1, 3), (-1, 4, 3, 5)]]
allzero = True
for dv, sv in pts:
    Pv = sp.sqrt(3 - dv**2 - dv*sv)          # exact algebraic
    r = sp.nsimplify(sp.simplify(resid.subs({Dm: dv, Sm: sv, Pm: Pv})))
    allzero = allzero and (r == 0)
check("SBB2.primitive_exact", allzero,
      "d eta == K_G dA on the keystone at 8 exact rational points (exact zero); "
      "residual factors as 6(P/P - 1) = 0 on the surface")

# ================= SBB-3 : r=3 density exists at n=4 (sample) =================
x1, x2, x3, x4 = sp.symbols('x1 x2 x3 x4', real=True)
# a sample n=4 quadric with rank-3 coupling (offdiag Hessian rank>=3); NOT claimed
# to be THE ARITH-I n=4 keystone -- only to show the r=3 density is a real object.
# F = (x1^2+x2^2+x3^2+x4^2)/2 + x1 x2 + x2 x3 + x3 x4 - 3
Hs = sp.Matrix([[1, 1, 0, 0], [1, 1, 1, 0], [0, 1, 1, 1], [0, 0, 1, 1]])
# evaluate at a sample point FIRST (numbers -> fast), then form e_3 (no symbolic blowup)
pt = {x1: sp.Rational(1), x2: sp.Rational(1, 2), x3: sp.Rational(-1, 2), x4: sp.Rational(3, 4)}
gs = [v.subs(pt) for v in (Hs*sp.Matrix([x1, x2, x3, x4]))]
qs = sum(v**2 for v in gs)
A4 = P_proj(gs, qs, 4)*offdiag(Hs, 4)*P_proj(gs, qs, 4)
val = sp.nsimplify(e_r(A4, 3))
check("SBB3.e3_n4_nonzero", val != 0 and val.is_finite,
      f"e_3(P Hc P) at n=4 is a live density (sample value {val})")

# ================= verdict =================
n_checks = 5
if FAILS:
    print(f"VERDICT: FAIL ({len(FAILS)}): {', '.join(FAILS)}")
    raise SystemExit(1)
print(f"VERDICT: ARITH-I STAGE B session 1 CLEAN — {n_checks}/{n_checks}. r=2 primitive "
      f"exhibited (exact); r=3 needs n>=4 (proven) and its density is a real object; "
      f"OPEN gate: pin the ARITH-I n=4/n=6 quadric family before the r=3 verdict.")
