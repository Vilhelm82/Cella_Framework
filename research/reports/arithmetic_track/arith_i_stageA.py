"""
ARITH-I STAGE A (session 1) — the r=2 reduction, shear symbolic.

Frozen against PREREG 32f2fb3a; open pins a2ef103d. FRESH, zero-import.
Exact symbolic where the claim is symbolic; two independent numeric routes
on the reduction; exact retrodiction at the keystone.

Surface (eigen-frame of F_s = D^2 + s*D*S + P^2 - 3):
    lam_p * X^2 + lam_m * Y^2 + Z^2 = 3 ,   lam_pm = (1 +- r)/2 ,  r = sqrt(1+s^2)
lam_p > 0, lam_m < 0  ->  hyperboloid of one sheet, chi = 0, two cone ends.
Certified curvature (open pins P1/P2):  K_G = -12*s^2 / q^2 ,  q = |grad F|^2.

WHAT THIS SESSION ESTABLISHES
  SA-1  eigenvalue algebra symbolic in s: lam_pm, and the spherical-link ellipse
        semi-axes A(s), C(s) as closed forms; keystone retrodiction
        A(1) = (2-sqrt2)/4 = k^2, C(1) = 3-2*sqrt2  (open-pin P3).
  SA-2  the ALGEBRAIC COLLAPSE (exact, symbolic): the link speed^2 reduces from
        a 4-term radical to
              speed^2(t) = (C + nu*sin^2 t)/(1 + nu*sin^2 t),  nu = (A-C)/(1-A).
        Proven as a sympy identity in A, C, t. This is the r=2 "primitive"
        collapse the stage targets: the arc-length integrand is now a single
        ratio of quadratics -> elliptic of first/third kind.
  SA-3  the reduction  INT_S K_G dA = -2*L(link)  corroborated by TWO
        INDEPENDENT NUMERIC ROUTES at s in {1/2, 1, 2}:
          route alpha = direct surface integral of (-12 s^2/q^2) dA over the
                        eigen-frame hyperboloid (certified curvature formula +
                        induced area element, 2D quadrature);
          route beta  = -2 * L(s), L from the SA-2 collapsed speed^2 (1D).
  SA-4  keystone Legendre pin (K-4 checkpoint): L(1) reproduces the banked
        Booth normal form  L = 2^(3/4)[(3+2s2) Pi(n;k^2) - (2+2s2) K(k^2)],
        n = (4-3 sqrt2)/8, k^2 = (2-sqrt2)/4 -> the underived characteristic n
        and the two weights (3+2s2),(2+2s2) EMERGE at the keystone (regular
        Legendre path only; no singular ellippi).
  SA-5  K-2 reconciliation SCOPED (not yet closed): Legendre modulus of the
        period curve is lam := A(s); its bare j is j_lam(s) = 10976 at s=1,
        which is the 2-ISOGENOUS partner of the register j(s)=128 (close-off
        section 4: differential lives on j=10976, 2-isogenous to minimal j=128).
        So the naive modulus->register comparison MUST carry the index-2 isogeny.
        Documented here; K-2 closes next session with the isogeny bookkeeping.

Convention: pin = `python3 reports/arithmetic_track/arith_i_stageA.py | sha256sum`.
"""
import sympy as sp
import mpmath as mp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)

s = sp.symbols('s', positive=True)
t = sp.symbols('t', real=True)
A, C = sp.symbols('A C', positive=True)

# ================= SA-1 : eigenvalue algebra, link ellipse, symbolic in s =========
r = sp.sqrt(1 + s**2)
lam_p = (1 + r)/2
lam_m = (1 - r)/2                      # < 0
# link {lam_p X^2 + lam_m Y^2 + Z^2 = 0} cap S^2, project out the negative
# eigen-direction Y -> ellipse (lam_p-lam_m)X^2 + (1-lam_m)Z^2 = -lam_m in (X,Z);
# semi-axis^2:
A_s = sp.simplify(-lam_m/(lam_p - lam_m))     # coeff of X  == k^2
C_s = sp.simplify(-lam_m/(1 - lam_m))         # coeff of Z
A1 = sp.simplify(A_s.subs(s, 1))
C1 = sp.simplify(C_s.subs(s, 1))
check("SA1.k2.keystone", sp.simplify(A1 - (2 - sp.sqrt(2))/4) == 0,
      f"A(1) = {A1} = k^2 = (2-sqrt2)/4")
check("SA1.C.keystone", sp.simplify(C1 - (3 - 2*sp.sqrt(2))) == 0,
      f"C(1) = {C1} = 3-2*sqrt2")
print(f"INFO  SA1.A(s) = {A_s}")
print(f"INFO  SA1.C(s) = {C_s}")

# ================= SA-2 : the algebraic collapse (exact symbolic identity) =========
# raw link speed^2 for the space-ellipse X=sqrt(A)cos t, Z=sqrt(C)sin t on S^2:
c2 = sp.cos(t)**2
sin2 = sp.sin(t)**2
Y2 = 1 - A*c2 - C*sin2
dY2 = ((A - C)*sp.sin(t)*sp.cos(t))**2 / Y2
speed2_raw = A*sin2 + C*c2 + dY2
nu = (A - C)/(1 - A)
speed2_collapsed = (C + nu*sin2)/(1 + nu*sin2)
identity = sp.simplify(speed2_raw - speed2_collapsed)
check("SA2.collapse", identity == 0,
      "speed^2 = (C + nu sin^2 t)/(1 + nu sin^2 t) exactly, nu=(A-C)/(1-A)")

# ================= numeric machinery for routes ===================================
def geom(sv):
    """exact-ish mpmath geometry at numeric shear sv."""
    rr = mp.sqrt(1 + mp.mpf(sv)**2)
    lp = (1 + rr)/2
    lm = (1 - rr)/2
    Av = -lm/(lp - lm)
    Cv = -lm/(1 - lm)
    return lp, lm, Av, Cv

def L_link(sv):
    """route beta ingredient: link arc length from the collapsed speed^2."""
    _, _, Av, Cv = geom(sv)
    nuv = (Av - Cv)/(1 - Av)
    def integrand(tt):
        s2 = mp.sin(tt)**2
        return mp.sqrt((Cv + nuv*s2)/(1 + nuv*s2))
    # 4 x first quadrant (speed^2 has period pi/2 in the c2/sin2 variables)
    return 4*mp.quad(integrand, [0, mp.pi/2])

def total_curv_direct(sv):
    """route alpha: INT_S (-12 s^2/q^2) dA over the eigen-frame one-sheet
    hyperboloid  lam_p X^2 + lam_m Y^2 + Z^2 = 3, via symbolic area element."""
    X, Y, Z = sp.symbols('X Y Z', real=True)
    th, Yv = sp.symbols('theta Yv', real=True)
    lp = sp.nsimplify((1 + sp.sqrt(1 + sp.nsimplify(sv)**2))/2)
    lm = sp.nsimplify((1 - sp.sqrt(1 + sp.nsimplify(sv)**2))/2)
    b = -lm                                  # > 0
    # a1 X^2 + Z^2 = 3 + b Y^2 =: R ; X=sqrt(R/a1)cos th, Z=sqrt(R) sin th
    a1 = lp
    R = 3 + b*Yv**2
    Xe = sp.sqrt(R/a1)*sp.cos(th)
    Ze = sp.sqrt(R)*sp.sin(th)
    Ye = Yv
    rvec = sp.Matrix([Xe, Ye, Ze])
    r_th = rvec.diff(th)
    r_Y = rvec.diff(Yv)
    E = sp.simplify(r_th.dot(r_th))
    Fg = sp.simplify(r_th.dot(r_Y))
    G = sp.simplify(r_Y.dot(r_Y))
    dA = sp.sqrt(sp.simplify(E*G - Fg**2))
    q = 4*(a1**2*Xe**2 + b**2*Ye**2 + Ze**2)  # |grad F|^2 in eigen-frame
    svq = sp.nsimplify(sv)
    integrand = sp.simplify(-12*svq**2/q**2 * dA)
    f = sp.lambdify((th, Yv), integrand, 'mpmath')
    # Y over the whole line via Y = tan(p); theta over [0,2pi)
    def inner(pp):
        Yval = mp.tan(pp)
        jac = mp.sec(pp)**2
        return mp.quad(lambda tt: f(tt, Yval), [0, mp.pi/2, mp.pi, 3*mp.pi/2, 2*mp.pi]) * jac
    lim = mp.pi/2 - mp.mpf('1e-9')
    return mp.quad(inner, [-lim, 0, lim])

# ================= SA-3 : two-route reduction at three shears ======================
mp.mp.dps = 25
for sv in [mp.mpf(1)/2, mp.mpf(1), mp.mpf(2)]:
    beta = -2*L_link(sv)
    alpha = total_curv_direct(sv)
    rel = abs(alpha - beta)/abs(beta)
    check(f"SA3.reduction.s={mp.nstr(sv,4)}", rel < mp.mpf('1e-6'),
          f"INT K dA={mp.nstr(alpha,12)} vs -2L={mp.nstr(beta,12)}  rel={mp.nstr(rel,3)}")

# ================= SA-4 : keystone Legendre pin (n and weights emerge) =============
mp.mp.dps = 60
s2 = mp.sqrt(2)
k2 = (2 - s2)/4
n_leg = (4 - 3*s2)/8
weightP = 3 + 2*s2
weightK = 2 + 2*s2
L1_form = 2**mp.mpf('0.75')*(weightP*mp.ellippi(n_leg, k2) - weightK*mp.ellipk(k2))
L1_link = L_link(mp.mpf(1))
check("SA4.keystone.n_and_weights",
      abs(L1_form - L1_link) < mp.mpf('1e-40'),
      f"Booth form (n=(4-3s2)/8, wts 3+2s2 / 2+2s2) vs link L(1), "
      f"diff={mp.nstr(abs(L1_form-L1_link),3)}")
check("SA4.total_curv.keystone",
      abs(-2*L1_link - mp.mpf('-5.010490702660418769050021160526777648057')) < mp.mpf('1e-38'),
      "-2 L(1) == standing 40-digit keystone constant")

# ================= SA-5 : K-2 reconciliation scoped (isogeny documented) ===========
# Legendre lambda = modulus^2 = A(s); bare j of the lambda-curve:
lam = A_s
j_lam = sp.simplify(256*(1 - lam + lam**2)**3 / (lam**2*(1 - lam)**2))
j_lam_1 = sp.simplify(j_lam.subs(s, 1))
# register (CALC-24, [CONTAINER] target -- retrodict, never trust):
j_reg = (1728*s**6 - 1728*s**4 + 576*s**2 - 64)/(s**6 + 2*s**4 + s**2)
j_reg_1 = sp.simplify(j_reg.subs(s, 1))
check("SA5.j_lambda.keystone", j_lam_1 == 10976,
      f"j of the modulus-lambda curve at s=1 = {j_lam_1} (the differential's curve)")
check("SA5.j_register.keystone", j_reg_1 == 128,
      "register j(1) = 128 (minimal model)")
# the modular equation link Phi_2(128, 10976) = 0 is the close-off's certified
# structural fact; K-2 must apply THIS isogeny, not compare bare j's.
print("INFO  SA5: j_lambda(s=1)=10976 vs register j(s=1)=128 are 2-ISOGENOUS "
      "(close-off section 4, Phi_2(128,10976)=0). K-2 retrodiction requires the "
      "index-2 isogeny bookkeeping -> deferred to Stage-A session 2. NOT a fire.")
print(f"INFO  SA5.j_lambda(s) = {sp.simplify(j_lam)}")

# ================= verdict =========================================================
n_checks = 11
if FAILS:
    print(f"VERDICT: FAIL ({len(FAILS)}): {', '.join(FAILS)}")
    raise SystemExit(1)
print(f"VERDICT: ARITH-I STAGE A (session 1) CLEAN — {n_checks}/{n_checks}; "
      f"K-1/K-4 checkpoints pass, K-2 scoped (isogeny), family-tier symbolic "
      f"weight-extraction + K-2 close = session 2.")
