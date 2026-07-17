#!/usr/bin/env python3
"""f4_battery.py -- STAGE F4 (CL-F4 n-uniformity), PREREG_F4 battery.
Probe: Molien counts via conjugacy-class cycle index (rep_utils classes).
Referee (independent): canonical-form multigraph enumeration on <= 2d
vertices with support filter. Exact integers/Fractions only.
Deterministic; run twice for x2. Usage: f4_battery.py OUTPATH
Defs first, dispatch last."""
import sys, os, json, hashlib, itertools
from fractions import Fraction as Fr
from math import factorial
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(HERE + '/../../../../evals/dbp_involution'))
import rep_utils as RU

GRADER_CLAUSES = {
 "PF4.1": "exact Molien counts a_d(n) via conjugacy-class cycle index, d = 1,2,3, n = 3..8; MUST reproduce certified anchors a₂(5,6,7) = 3 and a₃(5) = 7, a₃(6) = a₃(7) = 8",
 "PF4.2": "independent multigraph enumeration m_d(n) (canonical forms on ≤ 2d vertices, support filter ≤ n) satisfies m_d(n) == a_d(n) at EVERY grid point d ≤ 3, n = 3..8",
 "PF4.3": "stabilization: a_d(n) = a_d(2d) for all n ≥ 2d on the grid (d=1: n≥2; d=2: n≥4; d=3: n≥6)",
 "PF4.4": "the full closed table staked EXACTLY: a₁(n≥2) = 1; a₂(3) = 2, a₂(n≥4) = 3; a₃(3) = 3, a₃(4) = 6, a₃(5) = 7, a₃(n≥6) = 8; boundary mechanism: a₃ deficits below n=6 are exactly the types with support > n (3-matching at n=5; +adjacent-pair+disjoint at n=4; +all support-4 types at n=3)",
 "PF4.5": "per-type support census: battery independently recomputes each stable d=3 type's vertex support and matches the staked list (2,3,4,3,4,4,5,6)",
}

def sha256_file(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def gate():
    pins = {}
    for line in open(HERE + '/freeze_pins_f4.sha256'):
        h, path = line.split()
        pins[path] = h
    for path, h in pins.items():
        full = os.path.normpath(os.path.join(HERE, path))
        if sha256_file(full) != h:
            print("REFUSE_MISMATCH " + path); sys.exit(2)
    pre = open(HERE + '/PREREG_F4.md', encoding='utf-8').read()
    for cid, cl in GRADER_CLAUSES.items():
        if cl not in pre:
            print("CLAUSE_DRIFT " + cid); sys.exit(3)
    return pins

def perm_from_cycle_type(mu, n):
    p, at = list(range(n)), 0
    for c in mu:
        cyc = list(range(at, at + c))
        for i in range(c):
            p[cyc[i]] = cyc[(i + 1) % c]
        at += c
    return tuple(p)

def fixed_pairs(p, n):
    cnt = 0
    for i, j in itertools.combinations(range(n), 2):
        a, b = p[i], p[j]
        if (min(a, b), max(a, b)) == (i, j): cnt += 1
    return cnt

def molien(n):
    # a_d(n) for d=1,2,3 via cycle index of Sym^d over conjugacy classes
    a1 = a2 = a3 = Fr(0)
    for mu, sz in RU.conjugacy_classes(n):
        p = perm_from_cycle_type(mu, n)
        p2 = tuple(p[p[i]] for i in range(n))
        p3 = tuple(p[p[p[i]]] for i in range(n))
        f1, f2, f3 = (fixed_pairs(x, n) for x in (p, p2, p3))
        a1 += sz * f1
        a2 += sz * Fr(f1 * f1 + f2, 2)
        a3 += sz * Fr(f1**3 + 3 * f1 * f2 + 2 * f3, 6)
    N = factorial(n)
    return a1 / N, a2 / N, a3 / N

def multigraph_classes(d):
    # canonical forms of d-edge multigraphs on vertex set [2d]
    V = 2 * d
    prs = list(itertools.combinations(range(V), 2))
    perms = list(itertools.permutations(range(V)))
    seen, classes = set(), []
    for ms in itertools.combinations_with_replacement(prs, d):
        key = tuple(sorted(ms))
        if key in seen: continue
        canon, orbit = None, set()
        for p in perms:
            img = tuple(sorted(tuple(sorted((p[i], p[j]))) for i, j in ms))
            orbit.add(img)
            if canon is None or img < canon: canon = img
        seen |= orbit
        support = len({v for e in canon for v in e})
        classes.append({"canon": canon, "support": support})
    return classes

def main():
    outp = sys.argv[1]
    pins = gate()
    rows = []
    led = {"role": "probe", "prereg": "PREREG_F4.md",
           "battery_sha256": sha256_file(os.path.abspath(__file__))}
    A = {}
    for n in range(3, 9):
        a1, a2, a3 = molien(n)
        assert a1.denominator == a2.denominator == a3.denominator == 1
        A[n] = (int(a1), int(a2), int(a3))
        rows.append({"row": "MOLIEN", "n": n, "a1": A[n][0],
                     "a2": A[n][1], "a3": A[n][2]})
    # PF4.1 anchors
    v1 = (A[5][1] == A[6][1] == A[7][1] == 3 and A[5][2] == 7
          and A[6][2] == 8 and A[7][2] == 8)
    assert v1, "K-F40 anchor mismatch"
    # referee: multigraph enumeration
    M = {}
    for d in (1, 2, 3):
        cls = multigraph_classes(d)
        for n in range(3, 9):
            M[(d, n)] = sum(1 for c in cls if c["support"] <= n)
        if d == 3:
            stable_supports = sorted(c["support"] for c in cls)
    v2 = all(M[(d, n)] == A[n][d - 1]
             for d in (1, 2, 3) for n in range(3, 9))
    rows.append({"row": "REFEREE", "m_table": {f"{d},{n}": M[(d, n)]
                 for d in (1, 2, 3) for n in range(3, 9)}, "agree": v2})
    # PF4.3 stabilization
    v3 = (all(A[n][0] == 1 for n in range(3, 9)) and
          all(A[n][1] == A[4][1] for n in range(4, 9)) and
          all(A[n][2] == A[6][2] for n in range(6, 9)))
    # PF4.4 staked table
    stake = {3: (1, 2, 3), 4: (1, 3, 6), 5: (1, 3, 7),
             6: (1, 3, 8), 7: (1, 3, 8), 8: (1, 3, 8)}
    v4 = all(A[n] == stake[n] for n in range(3, 9))
    # PF4.5 support census
    v5 = (stable_supports == sorted([2, 3, 4, 3, 4, 4, 5, 6]))
    rows.append({"row": "SUPPORTS_D3", "sorted": stable_supports,
                 "staked_sorted": sorted([2, 3, 4, 3, 4, 4, 5, 6]),
                 "pass": v5})
    verdicts = {"PF4.1": v1, "PF4.2": v2, "PF4.3": v3,
                "PF4.4": v4, "PF4.5": v5}
    rows.append({"row": "VERDICTS", "verdicts": verdicts,
                 "a_table": {str(n): A[n] for n in range(3, 9)},
                 "ledger": led, "pins": pins})
    with open(outp, 'w') as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    print(json.dumps(verdicts, sort_keys=True, indent=1))
    print("A_TABLE", {n: A[n] for n in range(3, 9)})
    print("F4_DONE")

main()
