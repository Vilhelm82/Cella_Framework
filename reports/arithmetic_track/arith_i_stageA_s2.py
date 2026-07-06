"""
ARITH-I STAGE A (session 2) — close K-2 family-wide + curve modulus + family-tier
refutations. FRESH, zero-import. Requires sympy + mpmath (declared).

Builds on session 1 (`arith_i_stageA.py`, ba9f270e). PREREG 32f2fb3a; open pins
a2ef103d. Paper-track fence: no engine priority changed.

WHAT THIS SESSION ESTABLISHES
  SB-1  K-2 CLOSED FAMILY-WIDE.  The classical modular polynomial Phi_2 vanishes
        IDENTICALLY in s on (register j(s), differential-curve j_lambda(s)):
              Phi_2( j_reg(s), j_lambda(s) ) == 0   for all s.
        i.e. the CALC-24 register curve is 2-isogenous to the r=2 total-curvature
        differential's modular curve across the WHOLE shear line, not merely at
        the keystone (session 1 had it at s=1 only). The family F_s retrodicts the
        register up to the certified index-2 isogeny. K-2 does not fire.
  SB-2  CURVE MODULUS PINNED: lambda = A(s) (corrects session-1 scoping).  The
        arc-length differential lives on Y^2 = (C+nu x^2)(1+nu x^2)(1-x^2); the
        cross-ratio of its four branch points is lambda = A(s) exactly (proven
        symbolically), so k^2(s) = A(s) = 1/2 - 1/(2 sqrt(1+s^2)) is the genuine
        Legendre modulus^2, and j_lambda(s) = 256(1-A+A^2)^3/(A^2(1-A)^2).
  SB-3  FAMILY-TIER NAIVE CLOSED FORMS REFUTED (banked negative results, the
        five-minute discriminators the BRIEF mandates before leaning on algebra):
        (a) n=(4-3r)/8 with weights (3+2r),(2+2r) [r=sqrt(1+s^2)] reproduces the
            keystone (P^(4/3)=2 at s=1) but FAILS off it (P not clean, complex at
            s=2). The keystone Booth form does NOT generalize by naive
            r-substitution.
        (b) L(s) = wK(r)K(A) + wE(r)E(A) with wK,wE polynomials in r (deg<=3):
            no fit (residual ~1e-3 on a held-out shear). The natural (K,E) weights
            are not low-degree rational in r.
  SB-4  KEYSTONE OUTPUTS re-affirmed exact (session-1 SA-4 cross-check): at s=1
        n=(4-3 sqrt2)/8 and weights (3+2sqrt2),(2+2sqrt2) reproduce the standing
        constant; k^2(1)=(2-sqrt2)/4=A(1).

STAGE A CLOSE (per stop condition, 2 sessions/stage HARD, this is session 2):
  keystone-COMPLETE (n, weights, constant as OUTPUTS; K-1/K-4 clean; K-2 CLOSED
  family-wide; k^2(s)=A(s) closed-form + proven modulus).  Family-tier symbolic
  n(s),w1(s),w2(s): PARKED with the blocker named -- the arc-length reduction is
  naturally (K,E) on the A-curve and the Booth (K,Pi) presentation uses a
  special-n reduction of Pi whose s-dependence is not a naive r-substitution
  (SB-3 kills both naive routes).  Stage B inherits: exhibit the explicit r=2
  algebraic primitive eta (d eta = density) as the validation of the primitive-
  ansatz machinery, then run it at r=3.

Convention: pin = `python3 reports/arithmetic_track/arith_i_stageA_s2.py | sha256sum`.
"""
import sympy as sp
import mpmath as mp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)

s, x = sp.symbols('s x', positive=True)

# ---------- geometry, symbolic in s ----------
r = sp.sqrt(1 + s**2)
A = sp.simplify((r - 1)/(2*r))          # = 1/2 - 1/(2r)
C = sp.simplify((r - 1)/(r + 1))
nu = sp.simplify((A - C)/(1 - A))

# ---------- SB-2 : curve modulus = A via cross-ratio ----------
# differential curve Y^2 = (C+nu X^2)(1+nu X^2)(1-X^2); in v=X^2 the branch points
# (roots of (C+nu v)(1+nu v)(1-v)) are v = -C/nu, -1/nu, 1. cross-ratio lambda:
e1, e2, e3 = sp.Integer(1), -C/nu, -1/nu
lam = sp.simplify((e2 - e1)/(e3 - e1))
check("SB2.modulus", sp.simplify(lam - A) == 0,
      "cross-ratio lambda = A(s) exactly  => k^2(s)=A(s) is the curve modulus")

def jlam(l):
    return sp.simplify(256*(1 - l + l**2)**3/(l**2*(1 - l)**2))
j_lambda = jlam(A)
j_reg = (1728*s**6 - 1728*s**4 + 576*s**2 - 64)/(s**6 + 2*s**4 + s**2)

# ---------- SB-1 : Phi_2(j_reg, j_lambda) == 0 identically in s (K-2 closed) ----------
X, Y = sp.symbols('X Y')
Phi2 = (X**3 + Y**3 - X**2*Y**2
        + 1488*(X**2*Y + X*Y**2) - 162000*(X**2 + Y**2)
        + 40773375*X*Y + 8748000000*(X + Y) - 157464000000000)
expr = sp.cancel(Phi2.subs({X: j_reg, Y: j_lambda}))   # rational function of s
num, den = sp.fraction(sp.together(expr))
check("SB1.K2.identity", sp.expand(num) == 0,
      "Phi_2(j_reg(s), j_lambda(s)) == 0 identically  => register 2-isogenous "
      "to the differential curve for ALL s. K-2 CLOSED family-wide.")
print(f"INFO  SB1.j_lambda(s) = {sp.simplify(j_lambda)}")
print(f"INFO  SB1.j_reg(s)    = {sp.simplify(j_reg)}")

# ---------- numeric helpers ----------
def geom(sv):
    rr = mp.sqrt(1 + mp.mpf(sv)**2); Av = (rr - 1)/(2*rr)
    Cv = (rr - 1)/(rr + 1); nuv = (Av - Cv)/(1 - Av)
    return rr, Av, Cv, nuv
def L_link(sv):
    _, Av, Cv, nuv = geom(sv)
    return 4*mp.quad(lambda t: mp.sqrt((Cv + nuv*mp.sin(t)**2)/(1 + nuv*mp.sin(t)**2)),
                     [0, mp.pi/2])

# ---------- SB-4 : keystone outputs exact ----------
mp.mp.dps = 60
s2 = mp.sqrt(2)
k2_1 = (2 - s2)/4
n_1 = (4 - 3*s2)/8
L1_form = 2**mp.mpf('0.75')*((3 + 2*s2)*mp.ellippi(n_1, k2_1) - (2 + 2*s2)*mp.ellipk(k2_1))
check("SB4.keystone", abs(-2*L1_form - mp.mpf('-5.010490702660418769050021160526777648057')) < mp.mpf('1e-38'),
      "keystone n,(weights) reproduce the standing constant (SA-4 cross-check)")
A1_num = mp.mpf(str(sp.N(A.subs(s, 1), 60)))
check("SB4.k2==A", abs(k2_1 - A1_num) < mp.mpf('1e-50'),
      "k^2(1) = A(1) = (2-sqrt2)/4")

# ---------- SB-3 : naive family-tier closed forms REFUTED (deterministic) ----------
mp.mp.dps = 40
def P_naive(sv):
    rr, Av, Cv, nuv = geom(sv)
    n = (4 - 3*rr)/8
    val = (3 + 2*rr)*mp.ellippi(n, Av) - (2 + 2*rr)*mp.ellipk(Av)
    return L_link(sv)/val
P_key = P_naive(mp.mpf(1))
P_off = P_naive(mp.mpf(2))
# keystone: P^(4/3) == 2 ; off-keystone the naive ratio is not even real-clean
key_ok = abs(P_key**(mp.mpf(4)/3) - 2) < mp.mpf('1e-20')
off_bad = abs(P_off**(mp.mpf(4)/3) - 2) > mp.mpf('1')       # wildly off (in fact complex)
check("SB3.naive_booth_refuted", key_ok and off_bad,
      f"n=(4-3r)/8 & wts (3+2r),(2+2r): P^(4/3)=2 at s=1 but |.-2|={mp.nstr(abs(P_off**(mp.mpf(4)/3)-2),4)} at s=2")

# polynomial-in-r (K,E) fit residual on a held-out shear must be large
shears = [mp.mpf(v) for v in ['0.4', '0.7', '1', '1.5', '2', '2.5', '3', '4']]
Amat = mp.matrix(len(shears), 8); bvec = mp.matrix(len(shears), 1)
for i, sv in enumerate(shears):
    rr, Av, Cv, nuv = geom(sv); K = mp.ellipk(Av); E = mp.ellipe(Av)
    for j in range(4):
        Amat[i, j] = rr**j*K; Amat[i, 4 + j] = rr**j*E
    bvec[i, 0] = L_link(sv)
coef = mp.lu_solve(Amat, bvec)
sv = mp.mpf('1.2'); rr, Av, Cv, nuv = geom(sv); K = mp.ellipk(Av); E = mp.ellipe(Av)
model = sum(coef[j]*rr**j for j in range(4))*K + sum(coef[4 + j]*rr**j for j in range(4))*E
resid = abs(model - L_link(sv))
check("SB3.poly_KE_refuted", resid > mp.mpf('1e-6'),
      f"deg<=3-in-r (K,E) weights do not fit: held-out residual {mp.nstr(resid,4)}")

# ---------- verdict ----------
n_checks = 6
if FAILS:
    print(f"VERDICT: FAIL ({len(FAILS)}): {', '.join(FAILS)}")
    raise SystemExit(1)
print(f"VERDICT: ARITH-I STAGE A session 2 CLEAN — {n_checks}/{n_checks}. "
      f"K-2 CLOSED family-wide; modulus=A(s) proven; keystone exact; naive "
      f"family-tier forms refuted. STAGE A CLOSED keystone-complete; family-tier "
      f"symbolic weights parked with blocker named.")
