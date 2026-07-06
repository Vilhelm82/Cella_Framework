"""
ARITH-I OPEN PINS — re-derived at campaign open (re-verification rule; re-run
policy case (b): these results bear load in the new prereg). FRESH code, zero
import from any origin artifact. Requires sympy + mpmath (declared).

Pins re-derived here:
  P0  family definition self-check at keystone s=1: gradient, Hessian, q
      match the banked A1 forms (g = (2D+S, D, 2P), q = 5D^2+4DS+S^2+4P^2).
  P1  det B = 4*(D^2 + D*S + P^2) identically at s=1 (bordered Hessian),
      hence det B == 12 on F=0; general-s det B printed as derived info.
  P2  K_G = -det B / q^2 keystone retrodiction: K_G(1,1,1) = -3/49, q = 14.
  P3  asymptotic-cone eigenvalue algebra at s=1: eigenvalues (1±sqrt2)/2, 1;
      link-ellipse coefficient a_max^2 = (2-sqrt2)/4 == pinned Legendre k^2.
  P4  keystone total-curvature constant, TWO INDEPENDENT ROUTES:
      route 1: closed form -2^(7/4)[(3+2s2)*Pi(n;m) - (2+2s2)*K(m)],
               m = (2-sqrt2)/4, n = (4-3*sqrt2)/8 (regular path, all
               parameters in (0,1) — no singular ellippi anywhere);
      route 2: direct high-precision arc length of one component of the
               spherical link {D^2+DS+P^2=0} on S^2, total = -2L.
      Both against the standing 40-digit pin.
  P5  CALC-24 j(s) register targets BANKED (never trusted — [CONTAINER]
      currency; retrodiction targets for Stage A / kill K-2): register
      formula self-consistency j(1)=128, j(1/sqrt3)=0, j(2)=21296/25,
      s->oo limit 1728, and the banked derivative identity, all exact.

Convention: pin = `python3 verification/arith_i_open_pins.py | sha256sum`.
"""
import sympy as sp
import mpmath as mp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)

D, S, P, s = sp.symbols('D S P s', real=True)

# ---------- P0: family definition at keystone ----------
F_s = D**2 + s*D*S + P**2 - 3
F1 = F_s.subs(s, 1)
g1 = sp.Matrix([sp.diff(F1, v) for v in (D, S, P)])
H1 = sp.hessian(F1, (D, S, P))
q1 = sp.expand(g1.dot(g1))
check("P0.gradient", g1 == sp.Matrix([2*D + S, D, 2*P]))
check("P0.hessian", H1 == sp.Matrix([[2, 1, 0], [1, 0, 0], [0, 0, 2]]))
check("P0.q", q1 == sp.expand(5*D**2 + 4*D*S + S**2 + 4*P**2))

# ---------- P1: bordered-Hessian determinant ----------
def bordered_det(F):
    g = sp.Matrix([sp.diff(F, v) for v in (D, S, P)])
    H = sp.hessian(F, (D, S, P))
    B = sp.zeros(4, 4)
    B[:3, :3] = H
    B[:3, 3] = g
    B[3, :3] = g.T
    return sp.expand(B.det())

detB1 = bordered_det(F1)
check("P1.detB.s1", detB1 == sp.expand(4*(D**2 + D*S + P**2)),
      "det B = 4*(D^2+DS+P^2) identically")
onF = sp.simplify(detB1.subs(P**2, 3 - D**2 - D*S))
check("P1.detB.onF", onF == 12, "det B == 12 on F=0")
detBs = sp.factor(bordered_det(F_s))
print(f"INFO  P1.detB.general_s = {detBs}   (derived info, Stage-A input)")

# ---------- P2: K_G keystone retrodiction ----------
q_at = q1.subs({D: 1, S: 1, P: 1})
KG = sp.Rational(-12, 1) / q_at**2
check("P2.q.keystone", q_at == 14, "q(1,1,1) = 14")
check("P2.KG.keystone", KG == sp.Rational(-3, 49), "K_G = -12/q^2 = -3/49")

# ---------- P3: cone eigenvalue algebra at s=1 ----------
M1 = sp.Matrix([[1, sp.Rational(1, 2), 0], [sp.Rational(1, 2), 0, 0], [0, 0, 1]])
eigs = sorted(M1.eigenvals().keys(), key=lambda e: sp.N(e))
lam_minus, lam_plus_or_one = eigs[0], eigs[1:]
target = sorted([(1 - sp.sqrt(2))/2, (1 + sp.sqrt(2))/2, sp.Integer(1)], key=sp.N)
check("P3.eigs", [sp.simplify(a - b) == 0 for a, b in zip(eigs, target)] == [True]*3,
      "eigenvalues (1-sqrt2)/2, 1, (1+sqrt2)/2")
alpha = (1 + sp.sqrt(2))/2   # positive coupled eigenvalue
beta  = (1 - sp.sqrt(2))/2   # negative eigenvalue (cone axis)
# on the sphere: alpha x^2 + beta y^2 + z^2 = 0 & x^2+y^2+z^2 = 1
#   ==>  (alpha-beta) x^2 + (1-beta) z^2 = -beta  (ellipse in the (x,z) chart)
A_ell = sp.simplify(-beta/(alpha - beta))
C_ell = sp.simplify(-beta/(1 - beta))
check("P3.k2", sp.simplify(A_ell - (2 - sp.sqrt(2))/4) == 0,
      "a_max^2 = (2-sqrt2)/4 == pinned k^2")
check("P3.C", sp.simplify(C_ell - (3 - 2*sp.sqrt(2))) == 0,
      "z-semi-axis^2 = 3-2*sqrt2")

# ---------- P4: keystone constant, two routes ----------
mp.mp.dps = 80
s2 = mp.sqrt(2)
m_leg = (2 - s2)/4
n_leg = (4 - 3*s2)/8
route1 = -2**mp.mpf('1.75') * ((3 + 2*s2)*mp.ellippi(n_leg, m_leg)
                               - (2 + 2*s2)*mp.ellipk(m_leg))

A_n = mp.mpf(2 - s2)/4          # ellipse coefficient in x
C_n = mp.mpf(3 - 2*s2)          # ellipse coefficient in z
def speed(t):
    ct, st_ = mp.cos(t), mp.sin(t)
    y2 = 1 - A_n*ct**2 - C_n*st_**2
    dy2 = ((A_n - C_n)*st_*ct)**2 / y2
    return mp.sqrt(A_n*st_**2 + C_n*ct**2 + dy2)
L = mp.quad(speed, [0, mp.pi/2, mp.pi, 3*mp.pi/2, 2*mp.pi])
route2 = -2*L

PIN40 = mp.mpf('-5.010490702660418769050021160526777648057')
d12 = abs(route1 - route2)
check("P4.two_route", d12 < mp.mpf('1e-60'), f"|route1-route2| = {mp.nstr(d12, 3)}")
check("P4.pin", abs(route1 - PIN40) < mp.mpf('1e-38'),
      f"closed form vs standing 40-digit pin, diff = {mp.nstr(abs(route1 - PIN40), 3)}")
print(f"INFO  P4.constant = {mp.nstr(route1, 62)}")

# ---------- P5: CALC-24 register targets banked ([CONTAINER] — retrodict, never trust) ----------
j_reg = (1728*s**6 - 1728*s**4 + 576*s**2 - 64)/(s**6 + 2*s**4 + s**2)
j1 = sp.simplify(j_reg.subs(s, 1))
j3 = sp.simplify(j_reg.subs(s, 1/sp.sqrt(3)))
j2 = sp.nsimplify(sp.simplify(j_reg.subs(s, 2)))
jinf = sp.limit(j_reg, s, sp.oo)
check("P5.j.keystone", j1 == 128, "j(1) = 128")
check("P5.j.gamma13", j3 == 0, "j(1/sqrt3) = 0")
check("P5.j.s2", j2 == sp.Rational(21296, 25), "j(2) = 21296/25")
check("P5.j.limit", jinf == 1728, "j(s->oo) = 1728")
dj_claim = 128*(3*s**2 - 1)**2*(9*s**2 + 1)/(s**3*(s**2 + 1)**3)
check("P5.j.derivative", sp.simplify(sp.diff(j_reg, s) - dj_claim) == 0,
      "banked dj/ds identity exact")
print("INFO  P5 register values are RETRODICTION TARGETS for Stage A (kill K-2); "
      "they carry no evidentiary weight until derived from the family.")

# ---------- verdict ----------
n_checks = 15
if FAILS:
    print(f"VERDICT: FAIL ({len(FAILS)} of {n_checks}): {', '.join(FAILS)}")
    raise SystemExit(1)
print(f"VERDICT: ARITH-I OPEN PINS CLEAN — {n_checks}/{n_checks}")
