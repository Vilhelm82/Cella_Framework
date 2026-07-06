"""RE-CERTIFICATION: the gauge-channel transport law (n=3, order 2).

Re-verification rule (README rule 3): origin documents' statuses are claims,
not evidence. This script re-derives everything from scratch — stdlib only,
exact Fractions, no code or values imported except as PINNED EXPECTATIONS to
retrodict (which is the test, not the trust).

What is re-proven here (each a named check):
  T1  Channel decomposition reproduces pinned exact values on independent
      surfaces (keystone; pure-coupling positive; pure-coupling negative).
  T2  Total K_G is invariant under defining-function gauge H -> H + ga^T+ag^T
      (all fixtures x all gauges).
  T3  Channel shifts sum to zero (ker-Sigma law), same sweep.
  T4  The four gauge rows pinned in the origin transport document are
      retrodicted exactly (claims tested, not believed).
  T5  Carrier O is gauge-invariant and linear in H (fresh formula).
  T6  GROUP-ELEMENT LEDGER REQUIREMENT: gauge parameters compose additively
      at the H level (translation law), while channel displacements do NOT
      add — witness printed. The R-ledger must carry the parameter.

Run:  python verification/recert_transport_law.py   (exit 0 iff all pass)
Byte-stability: run twice, sha256 the stdout.
"""

import sys
from fractions import Fraction as Q

FAILS = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)


def det(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    total = Q(0)
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in M[1:]]
        total += (-1) ** j * M[0][j] * det(minor)
    return total


def c2_density(g, H, t, u):
    """Channel-density polynomial C^_2(t,u) = (-1)^(r+1) det(bordered), r=2, n=3."""
    M = [[(t if i != j else u) * H[i][j] for j in range(3)] for i in range(3)]
    B = [[Q(0)] + list(g)] + [[g[i]] + M[i] for i in range(3)]
    return -det(B)


def channels(g, H):
    """(kappa_c, kappa_int, kappa_s) exact; K_G = their sum."""
    q = sum(x * x for x in g)
    f0 = c2_density(g, H, Q(0), Q(1))
    f1 = c2_density(g, H, Q(1), Q(1))
    f2 = c2_density(g, H, Q(2), Q(1))
    c_t2 = (f2 - 2 * f1 + f0) / 2          # t^2 coeff  -> coupling
    c_tu = f1 - f0 - c_t2                  # tu  coeff  -> interaction
    c_u2 = f0                              # u^2 coeff  -> self
    return (c_t2 / q**2, c_tu / q**2, c_u2 / q**2)


def gauge(g, H, a):
    return [[H[i][j] + g[i] * a[j] + a[i] * g[j] for j in range(3)] for i in range(3)]


def carrier_O(g, H):
    return tuple(
        H[i][j] - g[i] * H[j][j] / (2 * g[j]) - g[j] * H[i][i] / (2 * g[i])
        for (i, j) in ((0, 1), (0, 2), (1, 2))
    )


# ---------------- fixtures (independent surfaces, exact jets) ----------------
KEY_G = (Q(3), Q(1), Q(2))
KEY_H = [[Q(2), Q(1), Q(0)], [Q(1), Q(0), Q(0)], [Q(0), Q(0), Q(2)]]

FIXTURES = [
    ("keystone x1^2+x1x2+x3^2-3 @ (1,1,1)", KEY_G, KEY_H),
    ("pure-coupling+  x1x2+x2x3+x3x1-3 @ (1,1,1)",
     (Q(2), Q(2), Q(2)),
     [[Q(0), Q(1), Q(1)], [Q(1), Q(0), Q(1)], [Q(1), Q(1), Q(0)]]),
    ("pure-coupling-  x3-x1x2 @ (1,1,1)",
     (Q(-1), Q(-1), Q(1)),
     [[Q(0), Q(-1), Q(0)], [Q(-1), Q(0), Q(0)], [Q(0), Q(0), Q(0)]]),
    ("generic jet",
     (Q(2), Q(-1), Q(3)),
     [[Q(1), Q(2), Q(-1)], [Q(2), Q(0), Q(3)], [Q(-1), Q(3), Q(2)]]),
]

GAUGES = [
    (Q(1), Q(0), Q(0)),
    (Q(0), Q(1), Q(0)),
    (Q(1), Q(-2), Q(3)),
    (Q(-1, 2), Q(5), Q(1)),
    (Q(2), Q(3), Q(-1)),
]

# T1 — pinned exact values (claims from origin docs, retrodicted fresh)
kc, ki, ks = channels(KEY_G, KEY_H)
check("T1 keystone channels (-1/49, -3/49, 1/49)",
      (kc, ki, ks) == (Q(-1, 49), Q(-3, 49), Q(1, 49)))
check("T1 keystone K_G = -3/49", kc + ki + ks == Q(-3, 49))
for name, g, H in FIXTURES[1:3]:
    got = sum(channels(g, H))
    expect = Q(1, 12) if "coupling+" in name else Q(-1, 9)
    check(f"T1 K_G pinned: {name}", got == expect, f"K_G={got}")

# T2 / T3 — invariance + ker-Sigma across all fixtures x gauges
for name, g, H in FIXTURES:
    base = channels(g, H)
    K = sum(base)
    for a in GAUGES:
        moved = channels(g, gauge(g, H, a))
        check(f"T2 K_G invariant [{name}] a={tuple(map(str, a))}", sum(moved) == K)
        dC = tuple(m - b for m, b in zip(moved, base))
        check(f"T3 shift sums to 0 [{name}] a={tuple(map(str, a))}", sum(dC) == 0)

# T4 — the origin transport doc's four pinned rows (kappa_c, kappa_s, kappa_int)
PINNED_ROWS = {
    (Q(1), Q(0), Q(0)): (Q(-1, 49), Q(4, 49), Q(-6, 49)),
    (Q(0), Q(1), Q(0)): (Q(-1, 49), Q(2, 7), Q(-16, 49)),
    (Q(1), Q(-2), Q(3)): (Q(-97, 49), Q(-130, 49), Q(32, 7)),
    (Q(-1, 2), Q(5), Q(1)): (Q(62, 49), Q(247, 98), Q(-377, 98)),
}
for a, (pc, ps, pi) in PINNED_ROWS.items():
    c, i, s = channels(KEY_G, gauge(KEY_G, KEY_H, a))
    check(f"T4 pinned row a={tuple(map(str, a))}", (c, s, i) == (pc, ps, pi),
          f"got (kc,ks,kint)=({c},{s},{i})")

# T5 — carrier: gauge-invariant and linear in H
for name, g, H in FIXTURES:
    O = carrier_O(g, H)
    for a in GAUGES:
        check(f"T5 O gauge-invariant [{name}] a={tuple(map(str, a))}",
              carrier_O(g, gauge(g, H, a)) == O)
H1, H2 = FIXTURES[0][2], FIXTURES[3][2]
Hsum = [[H1[i][j] + H2[i][j] for j in range(3)] for i in range(3)]
lin = tuple(x + y for x, y in zip(carrier_O(KEY_G, H1), carrier_O(KEY_G, H2)))
check("T5 O linear in H (same g)", carrier_O(KEY_G, Hsum) == lin)

# T6 — group-element ledger requirement
a1, a2 = (Q(1), Q(0), Q(0)), (Q(0), Q(0), Q(1))
a12 = tuple(x + y for x, y in zip(a1, a2))
two_step = gauge(KEY_G, gauge(KEY_G, KEY_H, a1), a2)
one_step = gauge(KEY_G, KEY_H, a12)
check("T6 parameters compose additively at H level", two_step == one_step)
base = channels(KEY_G, KEY_H)
d = lambda a: tuple(m - b for m, b in zip(channels(KEY_G, gauge(KEY_G, KEY_H, a)), base))
d1, d2, d12 = d(a1), d(a2), d(a12)
sum_sep = tuple(x + y for x, y in zip(d1, d2))
check("T6 channel displacements do NOT add (witness)", d12 != sum_sep,
      f"dC(a1+a2)={tuple(map(str,d12))} vs dC(a1)+dC(a2)={tuple(map(str,sum_sep))}")

print()
if FAILS:
    print(f"RE-CERTIFICATION: FAIL ({len(FAILS)} failed)")
    sys.exit(1)
print("RE-CERTIFICATION: CLEAN — transport law re-proven in-repo from fresh code.")
sys.exit(0)
