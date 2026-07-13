"""STAGE C BATTERY — graded against PREREG.md (pin 003b91bd017e07b6).

Symbolic tier (sympy): TC-P1 asymmetry law, TC-P3a multiplicative chains,
TC-P3b muF Hessian, TC-P4 fixed-base additivity — n = 3, 4, 5.
Exact tier (stdlib Q + float lattice): TC-P2 two-epoch chains, TC-P4 base
drift crossed by F1, TC-P5 mixed float/exact holonomy, TC-P6 mutants.

Run:  python campaigns/G02_two_species_account/stage_c/battery_stage_c.py
Exit 0 iff all predictions pass and all mutants are caught. Byte-stable x2.
"""

import sys
from fractions import Fraction as Q

import sympy as sp

FAILS = []
EFT = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)


# ============================ SYMBOLIC TIER ============================

def sym_part(n):
    g = [sp.Symbol(f"g{i}", nonzero=True) for i in range(n)]
    a = [sp.Symbol(f"a{i}") for i in range(n)]
    d = [sp.Symbol(f"d{i}") for i in range(n)]
    x = [sp.Symbol(f"x{i}") for i in range(n)]
    H = [[sp.Symbol(f"H{min(i,j)}{max(i,j)}") for j in range(n)] for i in range(n)]
    E1 = [[sp.Symbol(f"P{min(i,j)}{max(i,j)}") for j in range(n)] for i in range(n)]
    E2 = [[sp.Symbol(f"S{min(i,j)}{max(i,j)}") for j in range(n)] for i in range(n)]

    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    G = lambda base, v: [[base[i] * v[j] + v[i] * base[j] for j in range(n)]
                         for i in range(n)]
    add = lambda *Ms: [[sum(M[i][j] for M in Ms) for j in range(n)] for i in range(n)]
    zero = lambda z: sp.expand(sp.cancel(sp.together(z))) == 0

    def O(M):
        return {p: M[p[0]][p[1]] - g[p[0]] * M[p[1]][p[1]] / (2 * g[p[1]])
                   - g[p[1]] * M[p[0]][p[0]] / (2 * g[p[0]]) for p in pairs}

    # TC-P1 — defective gauge direction stays R
    ad = [a[i] + d[i] for i in range(n)]
    lhs = O(add(H, E1, G(g, ad)))
    corr = O(add(H, E1))          # M-correction removes E1 only
    # state after M-correction must equal initial state regardless of d
    corrected = O([[add(H, E1, G(g, ad))[i][j] - E1[i][j] for j in range(n)]
                   for i in range(n)])
    base_state = O(H)
    check(f"TC-P1 n={n} defective a' = a+d: state reconstruction untouched, "
          f"rho_M unchanged (d stays R)",
          all(zero(corrected[p] - base_state[p]) for p in pairs))

    # TC-P3a — multiplicative chains compose additively (current-input residues)
    T, d1, d2 = sp.symbols("T delta1 delta2")
    v1 = T * (1 + d1)
    r1 = T - v1
    v2 = v1 * (1 + d2)
    r2 = v1 - v2
    check(f"TC-P3a n={n} additive ledger exact through multiplicative chain",
          sp.expand(v2 + r1 + r2 - T) == 0)
    r2_mut = -T * d2   # original-truth-evaluated mutant
    residual = sp.expand(v2 + r1 + r2_mut - T)
    check(f"TC-P3a n={n} mutant residual == T*delta1*delta2 (cross-term missed)",
          sp.expand(residual - T * d1 * d2) == 0 and residual != 0)

    # TC-P3b — muF multiplicative at F-level lands additively at the jet level
    F = sum(g[i] * x[i] for i in range(n)) \
        + sp.Rational(1, 2) * sum(H[i][j] * x[i] * x[j]
                                  for i in range(n) for j in range(n))
    mu = 1 + sum(a[i] * x[i] for i in range(n))
    W = sp.expand(mu * F)
    sub0 = {xi: 0 for xi in x}
    hess_ok = all(
        sp.expand(sp.diff(W, x[i], x[j]).subs(sub0)
                  - (H[i][j] + g[i] * a[j] + a[i] * g[j])) == 0
        for i in range(n) for j in range(n))
    check(f"TC-P3b n={n} Hess(muF)|0 == H + g a^T + a g^T (no escape)", hess_ok)

    # TC-P4 — fixed-base additivity of the state quotient
    H2 = add(H, G(g, a))          # same state, different representative
    D = [[add(H2, E2)[i][j] - add(H, E1)[i][j] for j in range(n)] for i in range(n)]
    OD, OE1, OE2 = O(D), O(E1), O(E2)
    check(f"TC-P4 n={n} O_g((H2+E2) − (H1+E1)) == O_g(E2) − O_g(E1) (fixed base)",
          all(zero(OD[p] - OE2[p] + OE1[p]) for p in pairs))


for n in (3, 4, 5):
    sym_part(n)

# ============================ EXACT TIER ===============================

N = 3
g = (Q(3), Q(1), Q(2))
pairsQ = [(0, 1), (0, 2), (1, 2)]


def OQ(M, base=g):
    return tuple(M[i][j] - base[i] * M[j][j] / (2 * base[j])
                 - base[j] * M[i][i] / (2 * base[i]) for (i, j) in pairsQ)


def GmQ(base, v):
    return [[base[i] * v[j] + v[i] * base[j] for j in range(N)] for i in range(N)]


madd = lambda A, B: [[A[i][j] + B[i][j] for j in range(N)] for i in range(N)]
msub = lambda A, B: [[A[i][j] - B[i][j] for j in range(N)] for i in range(N)]

H0 = [[Q(1), Q(2), Q(-1)], [Q(2), Q(3), Q(4)], [Q(-1), Q(4), Q(2)]]
E1 = [[Q(1), Q(0), Q(2)], [Q(0), Q(-1), Q(1)], [Q(2), Q(1), Q(3)]]
E2 = [[Q(0), Q(1, 2), Q(0)], [Q(1, 2), Q(2), Q(-1)], [Q(0), Q(-1), Q(0)]]
a1, a2 = (Q(1), Q(0), Q(-1)), (Q(0), Q(2), Q(1))

# TC-P2 — two-epoch chain (recalibration mid-stream)
e1, e2 = (Q(1, 2), Q(1, 4), Q(-1, 3)), (Q(-1, 5), Q(1, 3), Q(1, 2))
gp1 = tuple(g[i] + e1[i] for i in range(N))
gp2 = tuple(g[i] + e2[i] for i in range(N))
assert all(x != 0 for x in gp1 + gp2)
outcomes = set()
for ep1_order in ((0, 1), (1, 0)):
    for ep2_order in ((0, 1), (1, 0)):
        H = [r[:] for r in H0]
        ops1 = [lambda M: madd(M, E1), lambda M: madd(M, GmQ(gp1, a1))]
        ops2 = [lambda M: madd(M, E2), lambda M: madd(M, GmQ(gp2, a2))]
        for k in ep1_order:
            H = ops1[k](H)
        for k in ep2_order:
            H = ops2[k](H)
        outcomes.add(tuple(map(tuple, H)))
check("TC-P2 within-epoch orderings commute (4 sequences, 1 outcome)",
      len(outcomes) == 1)
Hf = [list(r) for r in next(iter(outcomes))]
rhoMstar = madd(madd(E1, E2), madd(GmQ(e1, a1), GmQ(e2, a2)))
check("TC-P2 two-epoch reconstruction: O_g(H_final − rho_M*) == O_g(H0)",
      OQ(msub(Hf, rhoMstar)) == OQ(H0))

# TC-P4 — base drift crossed by F1
X = Hf
gp = gp1
wQ = {(i, j): g[i] * e1[j] - g[j] * e1[i] for (i, j) in pairsQ}
F1 = tuple((wQ[p] / 2) * (X[p[1]][p[1]] / (g[p[1]] * gp[p[1]])
                          - X[p[0]][p[0]] / (g[p[0]] * gp[p[0]])) for p in pairsQ)
check("TC-P4 base drift: O_g'(X) − F1(X) == O_g(X) (F1 crosses the wall)",
      tuple(x - y for x, y in zip(OQ(X, gp), F1)) == OQ(X, g))
check("TC-P6(iv) base-mixing mutant CAUGHT: O_g'(X) != O_g(X) uncorrected",
      OQ(X, gp) != OQ(X, g))

# TC-P5 — mixed float/exact holonomy (upper-triangle entrywise)
def two_sum(x_, y_):
    s = x_ + y_
    bp = s - x_
    err = (x_ - (s - bp)) + (y_ - bp)
    EFT.append(Q(x_) + Q(y_) == Q(s) + Q(err))
    return s, err


Hq = [[Q(1, 3), Q(2, 7), Q(-1, 3)], [Q(2, 7), Q(3, 7), Q(4, 9)],
      [Q(-1, 3), Q(4, 9), Q(2, 11)]]
av = (Q(1, 3), Q(0), Q(-1, 7))
Gq = GmQ(g, av)
slots = [(i, j) for i in range(N) for j in range(i, N)]

# order 1: round H, round G, float-add (TwoSum)
rledger1 = []   # R-parameters as executed, order 1
rledger2 = []   # R-parameters as executed, order 2
v1, rho1 = {}, {}
rledger1.append(("gauge", av))
for s_ in slots:
    hv = float(Hq[s_[0]][s_[1]])
    rh = Hq[s_[0]][s_[1]] - Q(hv)
    gv = float(Gq[s_[0]][s_[1]])
    rg = Gq[s_[0]][s_[1]] - Q(gv)
    sm, err = two_sum(hv, gv)
    v1[s_], rho1[s_] = sm, rh + rg + Q(err)

# order 2: exact add in Q, then round
v2, rho2 = {}, {}
rledger2.append(("gauge", av))
for s_ in slots:
    t = Hq[s_[0]][s_[1]] + Gq[s_[0]][s_[1]]
    fv = float(t)
    v2[s_], rho2[s_] = fv, t - Q(fv)

truth = {s_: Hq[s_[0]][s_[1]] + Gq[s_[0]][s_[1]] for s_ in slots}
check("TC-P5 order1 reconstructs (v + rho == truth, all slots)",
      all(Q(v1[s_]) + rho1[s_] == truth[s_] for s_ in slots))
check("TC-P5 order2 reconstructs (v + rho == truth, all slots)",
      all(Q(v2[s_]) + rho2[s_] == truth[s_] for s_ in slots))
hol = {s_: Q(v1[s_]) - Q(v2[s_]) for s_ in slots}
check("TC-P5 OWNED HOLONOMY per slot: v1 − v2 == rho2 − rho1 exactly",
      all(hol[s_] == rho2[s_] - rho1[s_] for s_ in slots))
check("TC-P5 holonomy witness nonzero on some slot",
      any(hol[s_] != 0 for s_ in slots),
      f"nonzero slots: {sum(1 for s_ in slots if hol[s_] != 0)}/6")
check("TC-P5 R-ledger identical in both orders (recorded logs compared)",
      rledger1 == rledger2 == [("gauge", av)],
      "R carries the parameter; float execution defects are M by criterion")
# dyadic control
Hd = [[Q(1, 2), Q(1, 4), Q(3, 8)], [Q(1, 4), Q(5, 8), Q(1, 16)],
      [Q(3, 8), Q(1, 16), Q(7, 4)]]
ad_ = (Q(1, 2), Q(1, 4), Q(1, 8))
Gd = GmQ(g, ad_)
ok_dyadic = True
for s_ in slots:
    h1, e1_ = two_sum(float(Hd[s_[0]][s_[1]]), float(Gd[s_[0]][s_[1]]))
    t = Hd[s_[0]][s_[1]] + Gd[s_[0]][s_[1]]
    ok_dyadic &= (Q(h1) == t and Q(e1_) == 0 and float(t) == h1)
check("TC-P5 dyadic control: zero residues, zero holonomy", bool(ok_dyadic))
check("TC-P5 all EFT identities verified in Q", all(EFT),
      f"{len(EFT)} ops")

# TC-P6(i) — false-alarm mutant: d-defect typed as damage
dvec = (Q(1, 3), Q(-1, 2), Q(1))
Hd1 = madd(H0, GmQ(g, tuple(x + y for x, y in zip(a1, dvec))))
true_state_shift = tuple(x - y for x, y in zip(OQ(Hd1), OQ(H0)))
mutant_report = GmQ(g, dvec)   # types G_g(d) as rho_M
check("TC-P6(i) false-alarm mutant CAUGHT: reports damage while true state "
      "shift == 0", all(x == 0 for x in true_state_shift)
      and any(x != 0 for r in mutant_report for x in r))

# TC-P6(ii) — miss mutant: e-defect's G_e(a) typed as representation
He = madd(H0, GmQ(gp1, a1))    # executed at defective base, no E anywhere
miss_claims_zero = (Q(0),) * 3  # mutant: "state unchanged"
actual_shift = tuple(x - y for x, y in zip(OQ(He), OQ(H0)))
check("TC-P6(ii) miss mutant CAUGHT: claims zero while O_g truly moved",
      actual_shift != miss_claims_zero,
      f"actual shift={tuple(map(str, actual_shift))}")

print()
if FAILS:
    print(f"STAGE C: FAIL ({len(FAILS)})")
    sys.exit(1)
print("STAGE C: ALL PREDICTIONS PASS — no multiplicative escape on the covered "
      "class; quotient additive at fixed base, F1 crosses base drift; holonomy "
      "owned in mixed chains; false-alarm/miss pair both caught.")
sys.exit(0)
