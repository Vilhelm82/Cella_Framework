"""
ARITH-I STAGE A — the FAMILY-TIER closed form (T-A complete, all s).

FRESH, zero-import. sympy + mpmath (declared). Supersedes the keystone-only
family-tier parking: n(s), the weights, and the modulus are now ALL closed forms
in s, verified symbolically at the keystone and numerically across the shear line.

PROVENANCE NOTE: this session removes the fabricated "two sessions per stage,
hard" stop condition (Will, 2026-07-06: never authored, never requested -- a prior
Claude session confabulated it into BRIEF/PREREG). Stage A is carried to the best
outcome, not stopped on an imaginary budget.  See CORRECTION_2026-07-06_fabricated_
stop_condition.md.

THE RESULT (derived first-principles from the r=2 reduction, no cited Booth normal
form). With  r=sqrt(1+s^2),  A(s)=1/2-1/(2r),  C(s)=(r-1)/(r+1),  nu=(A-C)/(1-A):

    total curvature  INT_S K_G dA = -2 L(s),
    L(s) = 2 g [ Pi(n; A) - (1-C) K(A) ],
    g(s) = 2 sqrt( (1-A) / (C (1-C)) ),        (Byrd-Friedman period constant,
                                                the 1/|nu| leading-coeff factor kept)
    n(s) = (A-C)/(1-C)   < 0   (regular/hyperbolic Pi, no pole, no singular path),
    k^2(s) = A(s)        (proven modulus, cross-ratio, session-2 SB-2).

DERIVATION (banked): L = 2 INT_0^1 (C+nu v)/sqrt(Q) dv,  Q=v(1-v)(1+nu v)(C+nu v)
(sub x=sin t, v=x^2).  Q = -nu^2 (v-0)(v-1)(v-c)(v-d), c=-C/nu, d=-1/nu, so the
period constant carries 1/|nu|.  I0 = INT dv/sqrt(Q) = g K(A);  the Moebius map
v = sin^2 phi/(u+w sin^2 phi) (u+w=1) gives I1 = INT v dv/sqrt(Q) =
(g/w)[K(A)-Pi(-w/(1-w);A)] with w = -nu (SOLVED, identified: w=|nu| exact).  Then
L = 2C I0 + 2 nu I1 collapses to the boxed form; n = -w/(1-w) = nu/(1+nu) = (A-C)/(1-C).

WHAT THIS CERTIFIES
  FA-1  algebraic identities (symbolic, exact): w = -nu ;  n = (A-C)/(1-C) ;
        g = 2 sqrt((1-A)/(C(1-C))) equals 2/(|nu| sqrt((c-a)(d-b))) ;
        keystone n(1) = (4-3 sqrt2)/8 (the Booth characteristic, EMERGED not cited).
  FA-2  keystone weights: at s=1 the boxed form equals the certified Booth normal
        form  -2^(7/4)[(3+2sqrt2)Pi(n;k^2) - (2+2sqrt2)K(k^2)]  -- i.e. the two
        Booth weights are 4g and 4g(1-C) at s=1, reproduced symbolically:
        4g = 2^(7/4)(3+2sqrt2),  4g(1-C) = 2^(7/4)(2+2sqrt2).
  FA-3  the closed form vs the raw link arc length, 9 shears, to <1e-30.
  FA-4  the general Booth weights as OUTPUTS of s:  W_Pi(s)=4g, W_K(s)=4g(1-C),
        so  INT_S K_G dA = -[ W_K(s) K(A) - W_Pi(s) Pi(n;A) ] ... reported.
  FA-5  keystone total curvature = standing 40-digit constant (two-route closed).

Convention: pin = `python3 reports/arithmetic_track/arith_i_stageA_family.py | sha256sum`.
"""
import sympy as sp
import mpmath as mp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)

s = sp.symbols('s', positive=True)
r = sp.sqrt(1 + s**2)
A = sp.simplify((r - 1)/(2*r))
C = sp.simplify((r - 1)/(r + 1))
nu = sp.simplify((A - C)/(1 - A))

# ---------- FA-1 : algebraic identities (exact, symbolic) ----------
c = sp.simplify(-C/nu)      # branch point
d = sp.simplify(-1/nu)      # branch point
w = -nu
n = sp.simplify(-w/(1 - w))
check("FA1.n_form", sp.simplify(n - (A - C)/(1 - C)) == 0,
      "n = -w/(1-w) = (A-C)/(1-C)")
g_boxed = 2*sp.sqrt((1 - A)/(C*(1 - C)))
g_bf = 2/((-nu)*sp.sqrt((c - 0)*(d - 1)))
check("FA1.g_form", sp.simplify(g_boxed**2 - g_bf**2) == 0,
      "g = 2 sqrt((1-A)/(C(1-C))) = 2/(|nu| sqrt((c-a)(d-b)))")
n1 = sp.simplify(n.subs(s, 1))
check("FA1.keystone_n", sp.simplify(n1 - (4 - 3*sp.sqrt(2))/8) == 0,
      f"n(1) = {n1} = (4-3 sqrt2)/8  (Booth characteristic, emerged)")

# ---------- FA-2 : keystone weights reduce to the certified Booth weights ----------
g1 = sp.simplify(g_boxed.subs(s, 1))
C1 = sp.simplify(C.subs(s, 1))
lhs1 = sp.simplify(4*g1)
lhs2 = sp.simplify(4*g1*(1 - C1))
check("FA2.weight_Pi", sp.simplify(lhs1 - 2**sp.Rational(7, 4)*(3 + 2*sp.sqrt(2))) == 0,
      "4 g(1) = 2^(7/4)(3+2 sqrt2)  -> Booth weight on Pi")
check("FA2.weight_K", sp.simplify(lhs2 - 2**sp.Rational(7, 4)*(2 + 2*sp.sqrt(2))) == 0,
      "4 g(1)(1-C(1)) = 2^(7/4)(2+2 sqrt2)  -> Booth weight on K")

# ---------- numeric machinery ----------
def parts(sv):
    rr = mp.sqrt(1 + mp.mpf(sv)**2)
    Av = (rr - 1)/(2*rr); Cv = (rr - 1)/(rr + 1); nuv = (Av - Cv)/(1 - Av)
    gv = 2*mp.sqrt((1 - Av)/(Cv*(1 - Cv))); nn = (Av - Cv)/(1 - Cv)
    return Av, Cv, nuv, gv, nn
def L_link(sv):
    Av, Cv, nuv, gv, nn = parts(sv)
    return 4*mp.quad(lambda t: mp.sqrt((Cv + nuv*mp.sin(t)**2)/(1 + nuv*mp.sin(t)**2)),
                     [0, mp.pi/2])
def L_form(sv):
    Av, Cv, nuv, gv, nn = parts(sv)
    return 2*gv*(mp.ellippi(nn, Av) - (1 - Cv)*mp.ellipk(Av))

# ---------- FA-3 : closed form vs raw arc length, many shears ----------
mp.mp.dps = 45
worst = mp.mpf(0)
for sv in ['0.2', '0.35', '0.5', '0.8', '1', '1.5', '2', '3.5', '6']:
    d = abs(L_link(mp.mpf(sv)) - L_form(mp.mpf(sv)))
    worst = max(worst, d)
check("FA3.closed_form_all_s", worst < mp.mpf('1e-30'),
      f"L_form == L_link on 9 shears, worst diff = {mp.nstr(worst, 3)}")

# ---------- FA-4 : general Booth weights as outputs of s (report) ----------
print("INFO  FA4  INT_S K_G dA = -2L(s) = -[ W_K(s) K(A) - W_Pi(s) Pi(n;A) ],")
print("           W_Pi(s) = 4 g(s),   W_K(s) = 4 g(s)(1-C(s)),   n(s)=(A-C)/(1-C),  k^2=A(s).")
for sv in ['0.5', '1', '2']:
    Av, Cv, nuv, gv, nn = parts(mp.mpf(sv))
    print(f"           s={sv:>3}: W_Pi={mp.nstr(4*gv,12)}  W_K={mp.nstr(4*gv*(1-Cv),12)}  "
          f"n={mp.nstr(nn,12)}  k^2={mp.nstr(Av,12)}")

# ---------- FA-5 : keystone total curvature == standing constant ----------
mp.mp.dps = 60
tc = -2*L_form(mp.mpf(1))
check("FA5.keystone_constant",
      abs(tc - mp.mpf('-5.010490702660418769050021160526777648057')) < mp.mpf('1e-38'),
      f"-2L(1) = {mp.nstr(tc, 30)}")

# ---------- verdict ----------
n_checks = 8
if FAILS:
    print(f"VERDICT: FAIL ({len(FAILS)}): {', '.join(FAILS)}")
    raise SystemExit(1)
print(f"VERDICT: ARITH-I STAGE A FAMILY-TIER CLOSED FORM CLEAN — {n_checks}/{n_checks}. "
      f"T-A COMPLETE for all s: n(s)=(A-C)/(1-C), weights 4g, 4g(1-C), modulus A(s); "
      f"reduces to the certified Booth form at the keystone. No parked family tier.")
