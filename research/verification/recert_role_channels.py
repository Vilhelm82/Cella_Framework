"""RC-4 RE-CERTIFICATION: the active role layer at n=3 — S3 charts, named
channels, A_c, and the faithful fingerprint.

Re-verification rule (README rule 3): origin statuses are claims, not
evidence. Everything below is re-proven from fresh code. Origin documents
(reference only, values retrodicted not trusted):
  - "The Active Role-Jet Orbit Calculus for Constraint-Surface Roles"
    (W. Lloyd, 2026-06-28) — S3 action, named channels, A_c forms,
    faithfulness corollary, exact rational closure, singular strata.
  - "Role-Channel Anisotropy of DBP Surfaces" / "Imprimitive Wreath
    Monodromy" (2026-06-28) — the keystone gate value A_c = 42793/1555848.

Two tiers, matching RC-2/RC-3 precedent:
  SYMBOLIC (sympy; identities over Q(a,b)[A,B,C] on the regular locus a,b != 0)
  FIXTURE  (stdlib Fractions; exact pins on independent surfaces)

Checks:
  S1  S3 relations for the ACTIVE maps on order-2 jets:
      s^2 = id, t^2 = id, (s.t)^3 = id  (birational, localized at a)
  S2  Three equivalent A_c forms: sum of squared gaps == 9*Var == 3*||P_2 O||^2,
      and the telescoping identity D_PD + D_DS + D_SP == 0 with
      A_c * q0^4 == D_PD^2 + D_DS^2 + D_SP^2  (the gap vector has no trivial part)
  S3  FAITHFULNESS (fingerprint witness): det d(kappa triple)/d(A,B,C)
      == 8 * Lam_P * Lam_D * Lam_S / q0^6  — rank 3 exactly off the
      channel-isotropy loci Lam_rho = 0
  S4  EXACT CLOSURE: every t-transported jet component is a polynomial in
      the jet over a denominator that is a pure power of a (Q[jet, a^-1])
  F1  Keystone (x1^2 + x1x2 + x3^2 - 3 @ (1,1,1)), graph chart P = f(D,S):
      jet, Lambda triple, kappa triple pinned; K_G = -3/49 CROSS-ROUTE
      (must equal the ambient-chart value certified in recert_transport_law)
  F2  A_c(keystone) == 42793/1555848  (the gate value, retrodicted)
  F3  ACTIVE-ORBIT ACTION REALIZED: applying t to the jet permutes the
      kappa triple by P<->D; applying s permutes by D<->S; A_c invariant
      under both (the orbit theorem, operational at order 2)
  F4  ISOTROPY WITNESS: paraboloid P = D^2 + S^2 @ (1,1,2) has Lam_P = 0,
      so the faithfulness determinant vanishes — the fingerprint map loses
      rank exactly on the CHANNEL_ISOTROPIC stratum (content, not accident)
  F5  ROLE-SINGULAR LOCUS: P = D^3 + S^2 @ (0,1,1) has a = f_D = 0; the
      D-output chart does not exist (every t-denominator is a power of a)
      — the mathematical locus behind the ROLE_CHART_UNAVAILABLE token

Run:  python verification/recert_role_channels.py   (exit 0 iff all pass)
Byte-stability: run twice, sha256 the stdout.
"""

import sys
from fractions import Fraction as Q

import sympy as sp

FAILS = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)


def is_zero(expr):
    return sp.simplify(sp.together(sp.cancel(expr))) == 0


# ============================ SYMBOLIC TIER ============================
a, b, A, B, C = sp.symbols("a b A B C")
q0 = 1 + a**2 + b**2

JET = (a, b, A, B, C)


def act_s(j):
    """Input swap s = (D S) on the order-2 jet."""
    ja, jb, jA, jB, jC = j
    return (jb, ja, jC, jB, jA)


def act_t(j):
    """Active output transposition t = (D P) on the order-2 jet."""
    ja, jb, jA, jB, jC = j
    return (
        1 / ja,
        -jb / ja,
        -jA / ja**3,
        (jA * jb - ja * jB) / ja**3,
        (-jA * jb**2 + 2 * ja * jb * jB - ja**2 * jC) / ja**3,
    )


def jet_eq(j1, j2):
    return all(is_zero(x - y) for x, y in zip(j1, j2))


# S1 — the S3 relations, active
check("S1 s.s == id (symbolic)", jet_eq(act_s(act_s(JET)), JET))
check("S1 t.t == id (symbolic)", jet_eq(act_t(act_t(JET)), JET))
st = act_s(act_t(JET))
st3 = act_s(act_t(act_s(act_t(st))))
check("S1 (s.t)^3 == id (symbolic)", jet_eq(st3, JET))

# named channels and the kappa triple
LamP = B
LamD = (A * b - a * B) / a
LamS = (C * a - b * B) / b
kP = -(LamP**2) / q0**2
kD = -(LamD**2) / q0**2
kS = -(LamS**2) / q0**2

# S2 — three equivalent A_c forms + telescoping
Ac = (kP - kD) ** 2 + (kD - kS) ** 2 + (kS - kP) ** 2
mean = (kP + kD + kS) / 3
Var = ((kP - mean) ** 2 + (kD - mean) ** 2 + (kS - mean) ** 2) / 3
check("S2 A_c == 9 * Var (symbolic)", is_zero(Ac - 9 * Var))
check("S2 A_c == 3 * ||P_2 O||^2 (symbolic)",
      is_zero(Ac - 3 * ((kP - mean) ** 2 + (kD - mean) ** 2 + (kS - mean) ** 2)))
D_PD = A * b * (2 * a * B - A * b) / a**2
D_DS = (A * b**2 - C * a**2) * (A * b**2 + C * a**2 - 2 * a * b * B) / (a**2 * b**2)
D_SP = C * a * (C * a - 2 * b * B) / b**2
check("S2 telescoping D_PD + D_DS + D_SP == 0 (symbolic)",
      is_zero(D_PD + D_DS + D_SP))
check("S2 A_c * q0^4 == D_PD^2 + D_DS^2 + D_SP^2 (symbolic)",
      is_zero(Ac * q0**4 - (D_PD**2 + D_DS**2 + D_SP**2)))

# S3 — faithfulness: the fingerprint Jacobian in closed form
Jac = sp.Matrix([kP, kD, kS]).jacobian(sp.Matrix([A, B, C]))
detJ = sp.cancel(sp.together(Jac.det()))
claim = 8 * LamP * LamD * LamS / q0**6
check("S3 det d(kappa)/d(A,B,C) == 8*LamP*LamD*LamS/q0^6 (symbolic)",
      is_zero(detJ - claim))

# S4 — exact closure: t-jet denominators are pure powers of a
ok4, seen = True, []
for comp in act_t(JET):
    den = sp.denom(sp.cancel(sp.together(comp)))
    poly_ok = den.free_symbols <= {a} and len(sp.Poly(den, a).monoms()) == 1
    ok4 &= poly_ok
    seen.append(sp.degree(den, a))
check("S4 exact closure: every t-component in Q[jet, a^-1] "
      f"(denominator a-degrees {seen})", bool(ok4))

# ============================ FIXTURE TIER =============================
def lam_triple(j):
    ja, jb, jA, jB, jC = j
    return (jB, (jA * jb - ja * jB) / ja, (jC * ja - jb * jB) / jb)


def kappa_triple(j):
    ja, jb = j[0], j[1]
    q = 1 + ja * ja + jb * jb
    return tuple(-(L * L) / (q * q) for L in lam_triple(j))


def ac_of(j):
    x, y, z = kappa_triple(j)
    return (x - y) ** 2 + (y - z) ** 2 + (z - x) ** 2


def t_num(j):
    ja, jb, jA, jB, jC = j
    return (
        Q(1) / ja,
        -jb / ja,
        -jA / ja**3,
        (jA * jb - ja * jB) / ja**3,
        (-jA * jb**2 + 2 * ja * jb * jB - ja**2 * jC) / ja**3,
    )


def s_num(j):
    ja, jb, jA, jB, jC = j
    return (jb, ja, jC, jB, jA)


# F1 — keystone in the graph chart P = f(D,S)
KEY = (Q(-3, 2), Q(-1, 2), Q(-13, 4), Q(-5, 4), Q(-1, 4))
check("F1 keystone Lambda triple == (-5/4, 1/6, 1/2)",
      lam_triple(KEY) == (Q(-5, 4), Q(1, 6), Q(1, 2)))
check("F1 keystone kappa triple == (-25/196, -1/441, -1/49)",
      kappa_triple(KEY) == (Q(-25, 196), Q(-1, 441), Q(-1, 49)))
ja, jb, jA, jB, jC = KEY
qk = 1 + ja * ja + jb * jb
KG = (jA * jC - jB * jB) / (qk * qk)
check("F1 keystone K_G (graph chart) == -3/49 == ambient-chart value "
      "(cross-route, vs recert_transport_law T1)", KG == Q(-3, 49))

# F2 — the gate value
check("F2 A_c(keystone) == 42793/1555848", ac_of(KEY) == Q(42793, 1555848))

# F3 — the active orbit, realized on the triple
base = kappa_triple(KEY)
after_t = kappa_triple(t_num(KEY))
after_s = kappa_triple(s_num(KEY))
check("F3 t swaps the P and D channels (kappa': (kD, kP, kS))",
      after_t == (base[1], base[0], base[2]))
check("F3 s swaps the D and S channels (kappa': (kP, kS, kD))",
      after_s == (base[0], base[2], base[1]))
check("F3 A_c invariant under t and s (orbit theorem, order 2)",
      ac_of(t_num(KEY)) == ac_of(KEY) == ac_of(s_num(KEY)))

# F4 — isotropy witness: fingerprint rank drop is content
PARAB = (Q(2), Q(2), Q(2), Q(0), Q(2))  # P = D^2 + S^2 @ (1,1,2): Lam_P = B = 0
lp, ld, ls = lam_triple(PARAB)
qp = 1 + PARAB[0] ** 2 + PARAB[1] ** 2
det_val = 8 * lp * ld * ls / qp**6
check("F4 isotropy witness: Lam_P == 0 on the paraboloid", lp == 0)
check("F4 faithfulness determinant == 0 there (CHANNEL_ISOTROPIC stratum)",
      det_val == 0, f"Lambda = ({lp}, {ld}, {ls})")

# F5 — role-singular locus: the D-chart does not exist at a = 0
SING = (Q(0), Q(2), Q(0), Q(0), Q(2))  # P = D^3 + S^2 @ (0,1,1): a = f_D = 0
try:
    lam_triple(SING)
    reached = True
except ZeroDivisionError:
    reached = False
check("F5 role-singular locus a == 0: D-output channel undefined "
      "(ROLE_CHART_UNAVAILABLE stratum content)", not reached)

print()
if FAILS:
    print(f"RC-4: FAIL ({len(FAILS)})")
    sys.exit(1)
print("RC-4: CLEAN — active role layer re-proven in-repo: S3 relations, "
      "A_c forms + telescoping, faithfulness det = 8*LP*LD*LS/q0^6, exact "
      "closure, keystone pins incl. A_c = 42793/1555848, orbit action on "
      "channels, isotropy + role-singular strata.")
sys.exit(0)
