"""STAGE B BATTERY — graded against PREREG.md (pin 984b967d3205123e).

Symbolic tier (sympy; n = 3, 4, 5): F1, diag-only corollary, radial
invisibility + ray-dependence, wedge witness, F2, F3, attribution theorem.
Exact-Q tier (stdlib; n = 3): F1 numeric, full defective-base chain with
M-folded cross-terms, exactness typing, three mutants.

Run:  python campaigns/G02_two_species_account/stage_b/battery_stage_b.py
Exit 0 iff all predictions pass and all mutants are caught. Byte-stable x2.
"""

import sys
from fractions import Fraction as Q

import sympy as sp

FAILS = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)


# ============================ SYMBOLIC TIER ============================

def sym_part(n):
    g = [sp.Symbol(f"g{i}", nonzero=True) for i in range(n)]
    e = [sp.Symbol(f"e{i}") for i in range(n)]
    lam = sp.Symbol("lam", nonzero=True)
    t = sp.Symbol("t")
    a = [sp.Symbol(f"a{i}") for i in range(n)]
    a2 = [sp.Symbol(f"c{i}") for i in range(n)]
    H = [[sp.Symbol(f"H{min(i,j)}{max(i,j)}") for j in range(n)] for i in range(n)]
    E1 = [[sp.Symbol(f"P{min(i,j)}{max(i,j)}") for j in range(n)] for i in range(n)]
    gp = [g[i] + e[i] for i in range(n)]

    def O(M, base):
        return {(i, j): M[i][j] - base[i] * M[j][j] / (2 * base[j])
                        - base[j] * M[i][i] / (2 * base[i])
                for i in range(n) for j in range(i + 1, n)}

    def Gmat(base, vec):
        return [[base[i] * vec[j] + vec[i] * base[j] for j in range(n)]
                for i in range(n)]

    add = lambda *Ms: [[sum(M[i][j] for M in Ms) for j in range(n)] for i in range(n)]
    zero = lambda x: sp.expand(sp.cancel(sp.together(x))) == 0
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    w = {(i, j): g[i] * e[j] - g[j] * e[i] for (i, j) in pairs}

    # TB-P1 — F1 exact total
    Og, Ogp = O(H, g), O(H, gp)
    F1 = {(i, j): (w[(i, j)] / 2) * (H[j][j] / (g[j] * gp[j])
                                     - H[i][i] / (g[i] * gp[i]))
          for (i, j) in pairs}
    check(f"TB-P1 n={n} F1: O_g' − O_g == wedge form (symbolic, exact total)",
          all(zero(Ogp[p] - Og[p] - F1[p]) for p in pairs))
    offdiag_slots = [(k, l) for k in range(n) for l in range(k + 1, n)]
    check(f"TB-P1 n={n} corollary: cross-term reads diag(H) only",
          all(sp.diff(Ogp[p] - Og[p], H[k][l]) == 0
              for p in pairs for (k, l) in offdiag_slots))

    # TB-P2 — radial invisibility + ray dependence
    subs_rad = {e[i]: t * g[i] for i in range(n)}
    check(f"TB-P2 n={n} e = t·g  ==>  Delta == 0 (symbolic)",
          all(zero((Ogp[p] - Og[p]).subs(subs_rad)) for p in pairs))
    Olam = O(H, [lam * g[i] for i in range(n)])
    check(f"TB-P2 n={n} O(H; lam·g) == O(H; g) — carrier depends on the RAY only",
          all(zero(Olam[p] - Og[p]) for p in pairs))

    # TB-P3 — wedge control witness: H = unit diag at i
    i0, j0 = 0, 1
    Hdiag = [[sp.Integer(0)] * n for _ in range(n)]
    Hdiag[i0][i0] = sp.Integer(1)
    Od1, Od2 = O(Hdiag, gp), O(Hdiag, g)
    staked = -w[(i0, j0)] / (2 * g[i0] * gp[i0])
    check(f"TB-P3 n={n} witness: unit-diag H gives Delta_01 == -w01/(2 g0 g'0)",
          zero(Od1[(i0, j0)] - Od2[(i0, j0)] - staked))

    # TB-P4 — F2, F3
    F2diff = [[Gmat(gp, a)[i][j] - Gmat(g, a)[i][j] - Gmat(e, a)[i][j]
               for j in range(n)] for i in range(n)]
    check(f"TB-P4 n={n} F2: G_g'(a) − G_g(a) == G_e(a) (symbolic)",
          all(zero(F2diff[i][j]) for i in range(n) for j in range(n)))
    OGe = O(Gmat(e, a), g)
    F3 = {(i, j): e[i] * a[j] + a[i] * e[j]
                  - (g[i] / g[j]) * e[j] * a[j] - (g[j] / g[i]) * e[i] * a[i]
          for (i, j) in pairs}
    check(f"TB-P4 n={n} F3: O_g(G_e(a)) closed form (symbolic)",
          all(zero(OGe[p] - F3[p]) for p in pairs))
    check(f"TB-P4 n={n} O_g(G_e(a)) not identically 0 (genuine damage exists)",
          any(sp.expand(sp.cancel(sp.together(OGe[p]))) != 0 for p in pairs))

    # TB-P5 — attribution theorem, symbolic chain
    suma = [a[i] + a2[i] for i in range(n)]
    Hfin = add(H, E1, Gmat(gp, suma))
    rhoMstar = add(E1, Gmat(e, suma))
    corrected = [[Hfin[i][j] - rhoMstar[i][j] for j in range(n)] for i in range(n)]
    Ocorr, OH0 = O(corrected, g), O(H, g)
    check(f"TB-P5 n={n} O_g(H_final − rho_M*) == O_g(H_0) (symbolic)",
          all(zero(Ocorr[p] - OH0[p]) for p in pairs))


for n in (3, 4, 5):
    sym_part(n)

# ============================ EXACT-Q TIER =============================

N = 3
g = (Q(3), Q(1), Q(2))
e = (Q(1, 2), Q(1, 4), Q(-1, 3))
gp = tuple(g[i] + e[i] for i in range(N))
assert all(x != 0 for x in g) and all(x != 0 for x in gp)

H0 = [[Q(1), Q(2), Q(-1)], [Q(2), Q(3), Q(4)], [Q(-1), Q(4), Q(2)]]
Es = [
    [[Q(1), Q(0), Q(2)], [Q(0), Q(-1), Q(1)], [Q(2), Q(1), Q(3)]],
    [[Q(0), Q(1, 2), Q(0)], [Q(1, 2), Q(2), Q(-1)], [Q(0), Q(-1), Q(0)]],
]
As = [(Q(1), Q(0), Q(-1)), (Q(0), Q(2), Q(1))]

pairsQ = [(0, 1), (0, 2), (1, 2)]


def OQ(M, base):
    return tuple(M[i][j] - base[i] * M[j][j] / (2 * base[j])
                 - base[j] * M[i][i] / (2 * base[i]) for (i, j) in pairsQ)


def GmQ(base, vec):
    return [[base[i] * vec[j] + vec[i] * base[j] for j in range(N)] for i in range(N)]


def maddQ(A, B):
    return [[A[i][j] + B[i][j] for j in range(N)] for i in range(N)]


def msubQ(A, B):
    return [[A[i][j] - B[i][j] for j in range(N)] for i in range(N)]


wQ = {(i, j): g[i] * e[j] - g[j] * e[i] for (i, j) in pairsQ}

# TB-P1 exact: F1 numeric on H0
delta = tuple(x - y for x, y in zip(OQ(H0, gp), OQ(H0, g)))
f1 = tuple((wQ[p] / 2) * (H0[p[1]][p[1]] / (g[p[1]] * gp[p[1]])
                          - H0[p[0]][p[0]] / (g[p[0]] * gp[p[0]])) for p in pairsQ)
check("TB-P1 exact: F1 matches direct Delta on generic fixture",
      delta == f1, f"Delta={tuple(map(str, delta))}")

# TB-P2 exact: radial defect invisible
e_rad = tuple(Q(1, 5) * g[i] for i in range(N))
g_rad = tuple(g[i] + e_rad[i] for i in range(N))
check("TB-P2 exact: radial e = g/5 gives Delta == 0 on H0",
      OQ(H0, g_rad) == OQ(H0, g))

# TB-P5 exact: full defective-base chain, cross-terms folded into M
suma = tuple(x + y for x, y in zip(*As))
Hfin = maddQ(maddQ(maddQ(H0, Es[0]), Es[1]), GmQ(gp, suma))
rhoMstar = maddQ(maddQ(Es[0], Es[1]), GmQ(e, suma))
check("TB-P5 exact: O_g(H_final − rho_M*) == O_g(H_0)",
      OQ(msubQ(Hfin, rhoMstar), g) == OQ(H0, g))
check("TB-P5 exact: R-ledger = intended parameters only (pure)",
      suma == (Q(1), Q(2), Q(0)))

# TB-P6 exactness typing: every computed quantity is a Fraction
flat = list(delta) + list(f1) + [x for r in rhoMstar for x in r] + list(suma)
check("TB-P6 all cross-terms Fraction-typed in Q (no float, no radical)",
      all(type(x) is Q for x in flat))

# TB-P7 mutants
# (i) first-order mutant
f1_mut = tuple((wQ[p] / 2) * (H0[p[1]][p[1]] / (g[p[1]] ** 2)
                              - H0[p[0]][p[0]] / (g[p[0]] ** 2)) for p in pairsQ)
check("TB-P7(i) first-order mutant CAUGHT: differs from exact Delta at finite e",
      f1_mut != delta)

# (ii) R-contamination mutant: G_e(a) claimed to be a gauge at g
witness = OQ(GmQ(e, As[0]), g)
check("TB-P7(ii) R-contamination mutant CAUGHT: O_g(G_e(a1)) != 0 "
      "==> G_e(a1) not in Im(G_g) (RC-2: ker O = Im G_g)",
      any(x != 0 for x in witness), f"O_g(G_e(a1))={tuple(map(str, witness))}")

# (iii) dropped-correction mutant: omit G_e(suma) from rho_M*
rhoM_naive = maddQ(Es[0], Es[1])
check("TB-P7(iii) dropped-correction mutant CAUGHT: reconstruction breaks",
      OQ(msubQ(Hfin, rhoM_naive), g) != OQ(H0, g))

print()
if FAILS:
    print(f"STAGE B: FAIL ({len(FAILS)})")
    sys.exit(1)
print("STAGE B: ALL PREDICTIONS PASS — staked closed forms hold; the base-point "
      "cross-term is exactly M-attributable; the R-ledger stays pure.")
sys.exit(0)
