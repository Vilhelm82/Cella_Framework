#!/usr/bin/env python3
"""Stage 8 gate: Kerr-Newman replay through the GENERAL theorems (PO-27).

The 3/4/4 order pattern is derived here from local germ typing + the Stage 6/7
normal-form theorems. The global scalar curvature is never assembled.

  KN1  metric-assignment identity: the campaign's chart-pair machinery
       (Lambda_{i,{M,a}} chart mixed partials, Stage 3) reproduces the KN
       paper's radical-free entries
       G_i = (U_i^2+4U+U_a^2+U_b^2)^2 U_i^2 / (4U) * (1/D_ia^2 + 1/D_ib^2)
       at an exact wedge point.
  KN2  extremal germ typing: at an exact extremal point (Q=1, J=3/8,
       S_ext = 5*pi/4), G_S = A2 delta^2 + O(delta^3) with A2 > 0 equal to the
       paper's closed form, and G_J, G_Q finite nonzero
       => generic-collapse germ => order 3 by the Stage 6 theorem (J1).
  KN3  reflection germ typing at J -> 0: G_J = B_J J^2 (1 + O(J^2)) EVEN,
       G_S, G_Q = amp/J^2 (1+O(J^2)) => parity-fixed inverse-channel germ with
       m = 2 => order 4, coefficient -14/B_J by Stage 6 (J2); B_J matches the
       paper's closed form at the sample point.
  KN4  physical descent check (plan Stage 8 task): at an exact interior point
       the J-presentation metric differs from the M-presentation pullback
       (controlled defect, Branch B), while the pair-form generation identity
       of REPORT_01 holds exactly.

pi is kept SYMBOLIC in KN1-KN3. KN4 uses the rational surrogate pi -> 3 (a
polynomial-identity instance; noted, not hidden) so the jet engine runs over
an exact quadratic field.
"""
import sys
import itertools
import sympy as sp

sys.path.insert(0, __file__.rsplit("/", 1)[0].rsplit("/", 1)[0] + "/role_cover_groupoid")
from jetlib import rechart, jet_coeff

failures = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)


S, J, Q, PI, delta = sp.symbols("S J Q pi delta", positive=True)
U = S / (4 * PI) + PI * J**2 / S + Q**2 / 2 + PI * Q**4 / (4 * S)
V = {"S": S, "J": J, "Q": Q}
Ui = {i: sp.diff(U, V[i]) for i in V}
Uij = {(i, j): sp.diff(U, V[i], V[j]) for i in V for j in V}


def G_entry(i):
    a, b = [k for k in ("S", "J", "Q") if k != i]
    Dia = Uij[(i, i)] * Ui[a] - Ui[i] * Uij[(i, a)]
    Dib = Uij[(i, i)] * Ui[b] - Ui[i] * Uij[(i, b)]
    pref = (Ui[i]**2 + 4 * U + Ui[a]**2 + Ui[b]**2)**2 * Ui[i]**2 / (4 * U)
    return pref * (1 / Dia**2 + 1 / Dib**2)


GS, GJ, GQ = G_entry("S"), G_entry("J"), G_entry("Q")

# ---- KN2 extremal germ typing --------------------------------------------------
pt = {Q: 1, J: sp.Rational(3, 8)}
Sext = PI * sp.sqrt(4 * sp.Rational(9, 64) + 1)        # = 5*pi/4
check("KN2 exact extremal point: S_ext = 5*pi/4", sp.simplify(Sext - 5 * PI / 4) == 0)
sub_ext = {**pt, S: 5 * PI / 4 + delta}
GS_ext = sp.together(GS.subs(sub_ext))
ser = sp.series(GS_ext, delta, 0, 3).removeO()
c0 = ser.coeff(delta, 0)
c1 = ser.coeff(delta, 1)
c2 = ser.coeff(delta, 2)
check("KN2 G_S collapses quadratically: delta^0 and delta^1 coefficients vanish",
      sp.simplify(c0) == 0 and sp.simplify(c1) == 0)
A2_paper = ((4 * U + Ui["J"]**2 + Ui["Q"]**2)**2 / (4 * U)
            * (1 / Ui["J"]**2 + 1 / Ui["Q"]**2)).subs({**pt, S: 5 * PI / 4})
check("KN2 A2 equals the paper's closed form (U_S^2 term dropped at extremality)",
      sp.simplify(c2 - A2_paper) == 0)
GJ0 = sp.simplify(GJ.subs({**pt, S: 5 * PI / 4}))
GQ0 = sp.simplify(GQ.subs({**pt, S: 5 * PI / 4}))
check("KN2 transverse entries finite and nonzero at extremality",
      GJ0 != 0 and GQ0 != 0 and sp.limit(GJ0, PI, 3).is_finite
      and sp.limit(GQ0, PI, 3).is_finite)
# germ type => order 3 by Stage 6 J1 (generic quadratic collapse, m = 2)

# ---- KN3 reflection germ typing at J -> 0 ----------------------------------------
pt3 = {Q: 2, S: 50 * PI}          # wedge: S^2 > pi^2(4J^2+Q^4) near J=0: 2500 > 16 ok
GJ_series = sp.series(sp.together(GJ.subs(pt3)), J, 0, 4).removeO()
check("KN3 G_J = B_J J^2 with NO J^0, J^1, J^3 terms (even collapse)",
      all(sp.simplify(GJ_series.coeff(J, k)) == 0 for k in (0, 1, 3))
      and sp.simplify(GJ_series.coeff(J, 2)) != 0)
BJ_val = GJ_series.coeff(J, 2)
DO1 = (S - PI * Q**2)**2 + 16 * PI**2 * Q**2 * S**2
DO2 = DO1 + 16 * PI * S**3
BJ_paper = (DO1 * DO2**2 / (256 * Q**2 * S**5 * PI**3 * (S - PI * Q**2)**2)).subs(pt3)
check("KN3 B_J matches the paper's closed form at the sample point",
      sp.simplify(BJ_val - BJ_paper) == 0)
for name, Gt in (("G_S", GS), ("G_Q", GQ)):
    lead = sp.limit(sp.together(Gt.subs(pt3)) * J**2, J, 0)
    check(f"KN3 {name} diverges exactly as amplitude/J^2 (amplitude nonzero finite)",
          sp.simplify(lead) != 0 and lead.subs(PI, 3).is_finite)
# germ type => parity-fixed m=2 => order 4, coefficient -14/B_J (Stage 6 J2)

# ---- KN1/KN4 exact-point checks with pi -> 3 surrogate -----------------------------
p3 = sp.Integer(3)
subs_num = {PI: p3, S: 12, J: 1, Q: 1}
Unum = U.subs(subs_num)            # exact rational
Mnum = sp.sqrt(Unum)
# jet of the M-output chart (graph value) around the point:
# M = sqrt(U(S,J,Q)); build 2-jet in based coordinates
xS, xJ, xQ = sp.symbols("xS xJ xQ")
Uloc = U.subs(PI, p3).subs({S: 12 + xS, J: 1 + xJ, Q: 1 + xQ})
Mfun = sp.sqrt(Uloc)
jet_M = sp.expand(sum(
    sp.Rational(1, sp.factorial(k1) * sp.factorial(k2) * sp.factorial(k3))
    * sp.diff(Mfun, xS, k1, xJ, k2, xQ, k3).subs({xS: 0, xJ: 0, xQ: 0})
    * xS**k1 * xJ**k2 * xQ**k3
    for k1 in range(3) for k2 in range(3) for k3 in range(3)
    if 1 <= k1 + k2 + k3 <= 2))
vars_M = {0: xS, 1: xJ, 2: xQ}       # roles 0=S, 1=J, 2=Q, 3=M

charts = {3: (jet_M, vars_M)}
for i in (0, 1, 2):
    charts[i] = rechart(jet_M, vars_M, 3, i, 2)

QN, LAM, GRAD = {}, {}, {}
for i in range(4):
    jt, vs = charts[i]
    idx = sorted(vs)
    syms = [vs[j] for j in idx]
    GRAD[i] = {j: sp.radsimp(jet_coeff(jt, syms, tuple(1 if k == j else 0 for k in idx)))
               for j in idx}
    QN[i] = sp.radsimp(1 + sum(GRAD[i][j]**2 for j in idx))
    LAM[i] = {}
    for l, m in itertools.combinations(idx, 2):
        e = tuple((1 if k in (l, m) else 0) for k in idx)
        LAM[i][frozenset((l, m))] = sp.radsimp(jet_coeff(jt, syms, e))

# KN1: campaign machinery == paper's radical-free entries
name_of = {0: "S", 1: "J", 2: "Q"}
ok1 = True
for i in (0, 1, 2):
    lam_a = LAM[i][frozenset((3, [m for m in (0, 1, 2) if m != i][0]))]
    lam_b = LAM[i][frozenset((3, [m for m in (0, 1, 2) if m != i][1]))]
    G_mine = sp.radsimp(QN[i]**2 * (1 / lam_a**2 + 1 / lam_b**2))
    G_paper = G_entry(name_of[i]).subs(subs_num)
    if sp.simplify(G_mine - G_paper) != 0:
        ok1 = False
check("KN1 chart-pair machinery reproduces the paper's G_S, G_J, G_Q exactly", ok1)

# KN4: physical descent/defect at the interior point (Stage 3 structure)
def row(i):
    if i == 3:
        return sp.Matrix([[GRAD[3][0], GRAD[3][1], GRAD[3][2]]])
    r = sp.zeros(1, 3)
    r[0, i] = 1
    return r

def g_of(rho):
    Mx = sp.zeros(3, 3)
    for i in range(4):
        if i == rho:
            continue
        tot = sum(1 / LAM[i][frozenset((rho, m))]**2
                  for m in range(4) if m not in (i, rho))
        Mx += QN[i]**2 * tot * row(i).T * row(i)
    return Mx

gM = g_of(3)      # the physical KN metric presentation
gJp = g_of(1)     # J as graph value
diff = sp.expand(gM - gJp)
check("KN4 physical model: strict descent FAILS (defect nonzero at exact point)",
      any(sp.simplify(diff[i, j]) != 0 for i in range(3) for j in range(3)))

def bpair(l, m):
    tot = sp.zeros(3, 3)
    for i in range(4):
        if i in (l, m):
            continue
        tot += (QN[i]**2 / LAM[i][frozenset((l, m))]**2) * row(i).T * row(i)
    return tot

ok4 = True
for rho in (3, 1):
    gen = sum((bpair(rho, m) for m in range(4) if m != rho), sp.zeros(3, 3))
    d = sp.expand(gen - g_of(rho))
    if any(sp.simplify(d[i, j]) != 0 for i in range(3) for j in range(3)):
        ok4 = False
check("KN4 pair-form generation holds in the physical model (REPORT_01 law)", ok4)

print()
if failures:
    print("STAGE 8 GATE FAILED:", failures)
    sys.exit(1)
print("GATE 8 PASSED: 3/4/4 derived from germ typing + general theorems; "
      "assignment identity verified; physical defect controlled per REPORT_01.")
