"""RC-3 RE-CERTIFICATION: route holonomy is the account gap — owned exactly.

Re-verification rule (README rule 3): fresh instance, fresh code, stdlib only.
This certifies the fact behind conjecture clause (iii) (OWNED HOLONOMY) before
the G0.2 campaign is allowed to cite it:

    Two routes to the same true quantity, through lossy observation maps,
    may disagree at the value level. The disagreement (the holonomy) is not
    noise to tolerate — it EQUALS the difference of the two routes' residue
    accounts, exactly, in Q. Reconstruction holds per route; holonomy is
    zero on the flat (all-ops-exact) class; and a ledger with one dropped
    residue provably breaks both laws (the battery bites).

Instance: the mixed-difference commutator (the Clairaut shape). Four node
truths T_ij in Q are observed onto the float lattice (species-M defect per
node). The mixed second difference is combined along two routes:
    Route A (column-first): (f11 - f01) - (f10 - f00)
    Route B (row-first):    (f11 - f10) - (f01 - f00)
Each float subtraction is tracked by TwoSum (Knuth, branch-free), and every
EFT identity is itself VERIFIED in Q in-run (H0) — the error-free property
is checked, never assumed.

Checks:
  H0  every TwoSum op satisfies  a + b == s + e  exactly in Q
  H1  per-node reconstruction: v_ij + r_ij == T_ij exactly
  H2  per-route reconstruction: v_route + rho_route == T_exact (composed
      from per-op + per-node residues with route-correct signs)
  H3  the TRUE commutator vanishes: T_A == T_B in Q (order-free truth)
  H4  OWNED HOLONOMY: v_A - v_B == rho_B - rho_A exactly in Q, and the
      witness is NONZERO on the rounding fixture (the law has content)
  H5  flat control (integer lattice): all residues 0, v_A == v_B,
      holonomy == 0 — zero on the commuting class
  H6  MUTANT: dropping one op-residue from a ledger breaks H2 and H4
      (the certificate is falsifiable, not vacuous)

Run:  python verification/recert_holonomy.py   (exit 0 iff all pass)
Byte-stability: run twice, sha256 the stdout.
"""

import sys
from fractions import Fraction as Q

FAILS = []
EFT_CHECKS = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)


def two_sum(a: float, b: float):
    """Knuth branch-free TwoSum: returns (s, e) with a + b == s + e exactly."""
    s = a + b
    bp = s - a
    e = (a - (s - bp)) + (b - bp)
    EFT_CHECKS.append(Q(a) + Q(b) == Q(s) + Q(e))
    return s, e


def sub(a: float, b: float):
    """Tracked float subtraction: a - b = s + e exactly."""
    return two_sum(a, -b)


def f_true(x: Q, y: Q) -> Q:
    """The surface: f(x, y) = x*y*(x+y), exact in Q."""
    return x * y * (x + y)


def observe(t: Q):
    """Species-M observation: round exact truth onto the float lattice."""
    v = float(t)  # correctly rounded
    return v, t - Q(v)


def run_instance(label, x0, y0, h, k, expect):
    """expect: 'nonzero' (holonomy must be != 0), 'zero_rounding' (residues
    nonzero but routes coincide — zero holonomy is NOT only a flat phenomenon),
    'flat' (all ops exact, everything zero)."""
    xs, ys = (x0, x0 + h), (y0, y0 + k)
    T = {(i, j): f_true(xs[i], ys[j]) for i in range(2) for j in range(2)}
    V, R = {}, {}
    for ij, t in sorted(T.items()):
        V[ij], R[ij] = observe(t)
    check(f"H1 [{label}] node reconstruction v+r==T (4 nodes)",
          all(Q(V[ij]) + R[ij] == T[ij] for ij in T))

    # true mixed difference, both orders (H3)
    TA = (T[(1, 1)] - T[(0, 1)]) - (T[(1, 0)] - T[(0, 0)])
    TB = (T[(1, 1)] - T[(1, 0)]) - (T[(0, 1)] - T[(0, 0)])
    check(f"H3 [{label}] true commutator vanishes (T_A == T_B)", TA == TB)

    node_part = R[(1, 1)] - R[(0, 1)] - R[(1, 0)] + R[(0, 0)]

    # Route A: column-first
    d1, e1 = sub(V[(1, 0)], V[(0, 0)])
    d2, e2 = sub(V[(1, 1)], V[(0, 1)])
    vA, e3 = sub(d2, d1)
    rhoA = Q(e3) + Q(e2) - Q(e1) + node_part

    # Route B: row-first
    c1, f1 = sub(V[(0, 1)], V[(0, 0)])
    c2, f2 = sub(V[(1, 1)], V[(1, 0)])
    vB, f3 = sub(c2, c1)
    rhoB = Q(f3) + Q(f2) - Q(f1) + node_part

    check(f"H2 [{label}] route A reconstructs: vA + rhoA == T exactly",
          Q(vA) + rhoA == TA)
    check(f"H2 [{label}] route B reconstructs: vB + rhoB == T exactly",
          Q(vB) + rhoB == TB)

    hol = Q(vA) - Q(vB)
    gap = rhoB - rhoA
    check(f"H4 [{label}] OWNED HOLONOMY: v_A - v_B == rho_B - rho_A exactly",
          hol == gap, f"holonomy={hol}")
    if expect == "nonzero":
        check(f"H4 [{label}] holonomy witness NONZERO (law has content)", hol != 0)
    elif expect == "zero_rounding":
        check(f"H5 [{label}] zero holonomy WITHOUT flatness: routes coincide "
              f"while residues are nonzero (zero holonomy != flat)",
              hol == 0 and (rhoA != 0 or rhoB != 0))
    else:  # flat
        check(f"H5 [{label}] flat class: holonomy == 0 and all residues == 0",
              hol == 0 and rhoA == 0 and rhoB == 0)
    return {"vA": vA, "rhoA": rhoA, "TA": TA, "vB": vB, "rhoB": rhoB, "TB": TB,
            "hol": hol, "opsA": (e1, e2, e3), "opsB": (f1, f2, f3)}


# nonzero-holonomy fixture (pinned by deterministic search 2026-07-06:
# routes disagree, vA - vB = -1/2^58 region on this lattice)
res = run_instance(
    "rounding/nonzero", Q(1, 10), Q(1, 10), Q(1, 10), Q(1, 3), expect="nonzero")

# zero-holonomy rounding fixture (kept deliberately: the original RC-3 draft
# fixture — residues nonzero, routes bit-identical; the law owns 0 too)
run_instance(
    "rounding/zero", Q(1, 10), Q(1, 3), Q(1, 7), Q(1, 11), expect="zero_rounding")

# flat control: integer lattice, every op exact
run_instance("flat", Q(1), Q(2), Q(1), Q(3), expect="flat")

# H0 — every EFT identity verified in Q
check(f"H0 all TwoSum identities exact in Q ({len(EFT_CHECKS)} ops)",
      all(EFT_CHECKS))

# H6 — mutant: drop the FIRST NONZERO op residue (deterministic choice) from
# its route's ledger; reconstruction must break. A zero residue would be a
# no-op "mutation" — dropping nothing is correctly undetectable.
labeled_ops = ([("A", i, e) for i, e in enumerate(res["opsA"])] +
               [("B", i, e) for i, e in enumerate(res["opsB"])])
nonzero = [(r, i, e) for (r, i, e) in labeled_ops if Q(e) != 0]
check("H6 a nonzero op residue exists on the nonzero-holonomy fixture",
      len(nonzero) > 0, f"nonzero op residues: {len(nonzero)}/6")
route, idx, e_drop = nonzero[0]
if route == "A":
    broke = (Q(res["vA"]) + (res["rhoA"] - Q(e_drop)) != res["TA"])
else:
    broke = (Q(res["vB"]) + (res["rhoB"] - Q(e_drop)) != res["TB"])
check("H6 mutant (dropped nonzero op residue) BREAKS reconstruction",
      broke, f"dropped route-{route} op#{idx+1} residue {Q(e_drop)}")

print()
if FAILS:
    print(f"RC-3: FAIL ({len(FAILS)})")
    sys.exit(1)
print("RC-3: CLEAN — holonomy re-certified as the account gap, exactly in Q; "
      "zero on the flat class; ledger tampering detected.")
sys.exit(0)
