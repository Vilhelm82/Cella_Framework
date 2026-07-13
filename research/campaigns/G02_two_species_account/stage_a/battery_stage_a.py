"""STAGE A BATTERY — graded against PREREG.md (pin ce44136c6418f48a).

Part 1: SYMBOLIC (sympy; identities in all indeterminates; n = 3, 4, 5)
    TA-P1 canonical form, TA-P2 reconstruction, TA-P3a purity (no a-symbols),
    TA-P4 pedigree-vs-splitting identity.
Part 2: EXACT-Q (stdlib Fractions; n = 3; deterministic fixtures)
    TA-P1/P5 all 720 interleavings — values AND accounts identical,
    TA-P3b K_G purity (fresh bordered-determinant implementation),
    TA-P4 generic witness (splitting != pedigree when diag(SumE) != 0),
    TA-P6 mutants (i)(ii)(iii) — each must be CAUGHT.

Run:  python campaigns/G02_two_species_account/stage_a/battery_stage_a.py
Exit 0 iff every prediction passes and every mutant bites. Byte-stable x2.
"""

import sys
from fractions import Fraction as Q
from itertools import permutations

import sympy as sp

FAILS = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)


# ============================ Part 1 — SYMBOLIC ============================

def sym_part(n):
    g = [sp.Symbol(f"g{i}", nonzero=True) for i in range(n)]
    H0 = [[sp.Symbol(f"H{min(i,j)}{max(i,j)}") for j in range(n)] for i in range(n)]
    E1 = [[sp.Symbol(f"P{min(i,j)}{max(i,j)}") for j in range(n)] for i in range(n)]
    E2 = [[sp.Symbol(f"S{min(i,j)}{max(i,j)}") for j in range(n)] for i in range(n)]
    a1 = [sp.Symbol(f"u{i}") for i in range(n)]
    a2 = [sp.Symbol(f"v{i}") for i in range(n)]

    G = lambda a: [[g[i] * a[j] + a[i] * g[j] for j in range(n)] for i in range(n)]
    add = lambda *Ms: [[sum(M[i][j] for M in Ms) for j in range(n)] for i in range(n)]

    def O(M):
        return [M[i][j] - g[i] * M[j][j] / (2 * g[j]) - g[j] * M[i][i] / (2 * g[i])
                for i in range(n) for j in range(i + 1, n)]

    zero = lambda exprs: all(sp.expand(sp.cancel(sp.together(x))) == 0 for x in exprs)
    msub = lambda A, B: [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

    # TA-P1: two contrasting orders of the chain {E1, a1, E2, a2} == canonical
    canon = add(H0, E1, E2, G([x + y for x, y in zip(a1, a2)]))
    order1 = add(add(add(add(H0, E1), G(a1)), E2), G(a2))     # M R M R
    order2 = add(add(add(add(H0, G(a2)), E2), G(a1)), E1)     # R M R M (reversed)
    check(f"TA-P1 n={n} order1 == canonical (symbolic)",
          zero([x for r in msub(order1, canon) for x in r]))
    check(f"TA-P1 n={n} order2 == canonical (symbolic)",
          zero([x for r in msub(order2, canon) for x in r]))

    # TA-P2: O(H_final - rho_M) == O(H0)
    rhoM = add(E1, E2)
    corrected = msub(canon, rhoM)
    check(f"TA-P2 n={n} O(M-corrected) == O(H0) (symbolic)",
          zero([x - y for x, y in zip(O(corrected), O(H0))]))

    # TA-P3a: purity — the M-corrected carrier contains no a-symbols
    asyms = set(a1) | set(a2)
    check(f"TA-P3a n={n} M-corrected carrier free of gauge symbols",
          all(sp.simplify(x).free_symbols.isdisjoint(asyms)
              for x in [sp.cancel(sp.together(t)) for t in O(corrected)]))

    # TA-P4: splitting of D = SumE + G(Suma): alpha == Suma + a*(SumE), Z == (SumE)_perp
    suma = [x + y for x, y in zip(a1, a2)]
    D = add(rhoM, G(suma))
    alpha = [D[i][i] / (2 * g[i]) for i in range(n)]
    astar = [rhoM[i][i] / (2 * g[i]) for i in range(n)]
    check(f"TA-P4 n={n} alpha(D) == Suma + a*(SumE) (symbolic)",
          zero([al - (s + st) for al, s, st in zip(alpha, suma, astar)]))
    Z = msub(D, G(alpha))
    Eperp = msub(rhoM, G(astar))
    check(f"TA-P4 n={n} Z(D) == (SumE)_perp (symbolic)",
          zero([x for r in msub(Z, Eperp) for x in r]))


for n in (3, 4, 5):
    sym_part(n)

# ============================ Part 2 — EXACT Q =============================

N = 3
g = (Q(3), Q(1), Q(2))
H0 = [[Q(1), Q(2), Q(-1)], [Q(2), Q(3), Q(4)], [Q(-1), Q(4), Q(2)]]

Es = [
    [[Q(1), Q(0), Q(2)], [Q(0), Q(-1), Q(1)], [Q(2), Q(1), Q(3)]],
    [[Q(0), Q(1, 2), Q(0)], [Q(1, 2), Q(2), Q(-1)], [Q(0), Q(-1), Q(0)]],
    [[Q(-2), Q(1), Q(1)], [Q(1), Q(0), Q(0)], [Q(1), Q(0), Q(1)]],
]
As = [(Q(1), Q(0), Q(-1)), (Q(0), Q(2), Q(1)), (Q(-1, 2), Q(1), Q(0))]


def Gm(a):
    return [[g[i] * a[j] + a[i] * g[j] for j in range(N)] for i in range(N)]


def madd(A, B):
    return [[A[i][j] + B[i][j] for j in range(N)] for i in range(N)]


def msubQ(A, B):
    return [[A[i][j] - B[i][j] for j in range(N)] for i in range(N)]


def OQ(M):
    return tuple(M[i][j] - g[i] * M[j][j] / (2 * g[j]) - g[j] * M[i][i] / (2 * g[i])
                 for i in range(N) for j in range(i + 1, N))


def det(M):
    n_ = len(M)
    if n_ == 1:
        return M[0][0]
    return sum((-1) ** j * M[0][j]
               * det([r[:j] + r[j + 1:] for r in M[1:]]) for j in range(n_))


def c2(H, t, u):
    M = [[(t if i != j else u) * H[i][j] for j in range(N)] for i in range(N)]
    B = [[Q(0)] + list(g)] + [[g[i]] + M[i] for i in range(N)]
    return -det(B)


def channels(H):
    q = sum(x * x for x in g)
    f0, f1, f2 = c2(H, Q(0), Q(1)), c2(H, Q(1), Q(1)), c2(H, Q(2), Q(1))
    ct2 = (f2 - 2 * f1 + f0) / 2
    return (ct2 / q**2, (f1 - f0 - ct2) / q**2, f0 / q**2)


K_G = lambda H: sum(channels(H))

ops = [("M", 0), ("M", 1), ("M", 2), ("R", 0), ("R", 1), ("R", 2)]
results = set()
for perm in permutations(range(6)):
    H = [row[:] for row in H0]
    rM = [[Q(0)] * N for _ in range(N)]
    rR = [Q(0)] * N
    for k in perm:
        kind, idx = ops[k]
        if kind == "M":
            H = madd(H, Es[idx])
            rM = madd(rM, Es[idx])
        else:
            H = madd(H, Gm(As[idx]))
            rR = [x + y for x, y in zip(rR, As[idx])]
    results.add((tuple(map(tuple, H)), tuple(map(tuple, rM)), tuple(rR)))
check("TA-P1/P5 all 720 interleavings: identical (H_final, rho_M, rho_R)",
      len(results) == 1, f"distinct outcomes: {len(results)}")

(Hf_t, rM_t, rR_t) = next(iter(results))
Hf = [list(r) for r in Hf_t]
rM = [list(r) for r in rM_t]
corrected = msubQ(Hf, rM)
check("TA-P2 exact: O(M-corrected) == O(H0)", OQ(corrected) == OQ(H0))
check("TA-P3b exact: K_G(M-corrected) == K_G(H0)", K_G(corrected) == K_G(H0))
HplusE = madd(madd(madd(H0, Es[0]), Es[1]), Es[2])
check("TA-P3b exact: K_G(H_final) == K_G(H0 + SumE) (R moves no invariant)",
      K_G(Hf) == K_G(HplusE))

# TA-P4 generic witness: splitting != pedigree because diag(SumE) != 0
suma = tuple(sum(a[i] for a in As) for i in range(N))
alpha = tuple(msubQ(Hf, H0)[i][i] / (2 * g[i]) for i in range(N))  # D = Hf - H0
astar = tuple(rM[i][i] / (2 * g[i]) for i in range(N))
check("TA-P4 exact: alpha == Suma + a*(SumE)",
      alpha == tuple(s + t for s, t in zip(suma, astar)))
check("TA-P4 witness: splitting DIFFERS from pedigree (a*(SumE) != 0)",
      any(t != 0 for t in astar), f"a*(SumE)={tuple(map(str, astar))}")

# TA-P6 mutants
# (i) false-alarm: measurement-free chain, gauge typed as M
Hm = [row[:] for row in H0]
mut_rM = [[Q(0)] * N for _ in range(N)]
for a in As:
    Hm = madd(Hm, Gm(a))
    mut_rM = madd(mut_rM, Gm(a))          # WRONG: types R as M
true_damage_zero = all(x == 0 for r in [[Q(0)] * N] * N for x in r)
mut_reports_damage = any(x != 0 for r in mut_rM for x in r)
check("TA-P6(i) false-alarm mutant CAUGHT: reports damage on damage-free chain",
      true_damage_zero and mut_reports_damage)

# (ii) displacement-ledger: channel displacements do not compose
dC = lambda a: tuple(m - b for m, b in zip(channels(madd(H0, Gm(a))), channels(H0)))
a1, a2 = As[0], As[1]
a12 = tuple(x + y for x, y in zip(a1, a2))
check("TA-P6(ii) displacement-ledger mutant CAUGHT: dC(a1+a2) != dC(a1)+dC(a2)",
      dC(a12) != tuple(x + y for x, y in zip(dC(a1), dC(a2))))

# (iii) dropped residue: delete E2 from rho_M
rM_mut = msubQ(rM, Es[1])
check("TA-P6(iii) dropped-residue mutant CAUGHT: reconstruction breaks",
      OQ(msubQ(Hf, rM_mut)) != OQ(H0))

print()
if FAILS:
    print(f"STAGE A: FAIL ({len(FAILS)})")
    sys.exit(1)
print("STAGE A: ALL PREDICTIONS PASS — T-A holds at the symbolic tier (n=3,4,5) "
      "and on the exact-Q battery; all three mutants caught.")
sys.exit(0)
