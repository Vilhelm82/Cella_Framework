#!/usr/bin/env python3
"""wall_scout.py — E1 flagship Stage 0 WALL_SCOUT (THE ENGINE Stage C).
Governing predecl: portfolio/campaigns/shape_witness/WALL_SCOUT_PREDECL.md, pin b8d6c404131e7db7.
Measurement battery: cost (time+RSS) of the flagship's exact-Q pipeline ops at n=6,7.
First consumer of engine_harness primitives (clause_gate, pin_gate, records_sha).
Timings/RSS live OUTSIDE the hashed records blob (MC.1: blob = math content only).
"""
import sys, os, json, time, resource
from fractions import Fraction as Fr
from itertools import combinations, permutations

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "portfolio", "campaigns", "the_engine", "stage_A"))
sys.path.insert(0, os.path.join(REPO, "evals", "dbp_involution"))
import engine_harness as EH
from rep_utils import specht_char_dict, specht_dim, cycle_type, partitions, class_rep, class_size
import sympy as sp

PREDECL = os.path.join(REPO, "portfolio", "campaigns", "shape_witness", "WALL_SCOUT_PREDECL.md")
PREDECL_PIN = "b8d6c404131e7db7"

WALL_CLAUSES = {
 "MC.1": "MC.1: the scout computes OP1, OP2, OP3 at n=6 and n=7 in exact rational arithmetic on the pinned fixtures, and the records blob RECORDS_SHA256 is equal across two independent runs per substrate.",
 "MC.2": "MC.2: envelope constants are ENVELOPE_T = 1200 seconds wall per op-run and ENVELOPE_M = 8192 MB peak RSS; the measured cost of an (op, n) is the maximum over the two primary runs.",
 "MC.3": "MC.3: the inclusion verdict per n is INCLUDED iff all three ops fit both envelope constants on the primary substrate; otherwise WALL_AT(n, op, t_s, rss_mb) \u2014 a measured wall is the answer, never a failure.",
 "MC.4": "MC.4: the primary substrate is the container per PA-2 B2 verbatim; a box run of the same battery is banked as secondary substrate-comparison data with no threshold authority.",
 "MC.5": "MC.5: calibration control \u2014 witness_battery.py reproduces RECORDS_SHA256 39bed5552c805f4d via engine_harness certify on the primary substrate before the scout is graded.",
 "MC.6": "MC.6: Molien degree-2 and degree-3 invariant counts at n=6 and n=7 are RECORDED as frozen numbers for the flagship; grading of P-F1 belongs to flagship Stage A, not to this scout.",
 "MC.7": "MC.7: projector gates (rank triple (1, n-1, n(n-3)/2), idempotency, partition of identity) must pass at both n; a projector-gate failure is a mathematical halt, not a cost wall.",
}
PINS = {
 "portfolio/campaigns/shape_witness/BRIEF_v1_DRAFT.md": "3b3fca4292bc8aa7",
 "portfolio/campaigns/shape_witness/witness_battery.py": "abff00bd15d22c84",
 "portfolio/campaigns/shape_witness/WITNESS_PREDECL.md": "967c7909450ef944",
 "evals/dbp_involution/rep_utils.py": "0d838e5fd430461b",
 "portfolio/campaigns/the_engine/stage_A/engine_harness.py": "7f0e5e7e4f4d54a6",
 "portfolio/campaigns/the_engine/stage_A/STAGE_A_PREDECL.md": "44a2c8019b2929b2",
 "portfolio/80_PROCESS_AMENDMENTS.md": "d03842f39c1e699b",
}

FIX = {
 6: {"g": [1, 2, 3, 5, 7, 11],
     "offd": [Fr(x) for x in (1, -2, 3, 1, 2, -1, 4, -3, 1, 2, -5, 2, 3, -1)] + [Fr(7, 2)]},
 7: {"g": [1, 2, 3, 5, 7, 11, 13],
     "offd": [Fr(x) for x in (1, -2, 3, 1, 2, -1, 4, -3, 1, 2, -5, 2, 3, -1)] + [Fr(7, 2)]
             + [Fr(1), Fr(-4), Fr(5, 2), Fr(3), Fr(-2), Fr(9)]},
}

def rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0

def pair_index(n):
    P = list(combinations(range(n), 2))
    return P, {p: k for k, p in enumerate(P)}

def pair_perm(p, PAIRS, IDX):
    return [IDX[tuple(sorted((p[i], p[j])))] for (i, j) in PAIRS]

# ---- OP1: isotypic projectors, full n!-sum (DF-S2 / witness pattern) ----
def op1(n, PAIRS, IDX):
    N = len(PAIRS)
    lams = [(n,), (n - 1, 1), (n - 2, 2)]
    chis = [specht_char_dict(l) for l in lams]
    dims = [specht_dim(l) for l in lams]
    fact = 1
    for k in range(2, n + 1): fact *= k
    Ps = [[[Fr(0)] * N for _ in range(N)] for _ in lams]
    for p in permutations(range(n)):
        ct = cycle_type(p)
        pi = pair_perm(p, PAIRS, IDX)
        cs = [Fr(dims[a] * int(chis[a][ct]), fact) for a in range(3)]
        for k in range(N):
            d = pi[k]
            for a in range(3):
                Ps[a][d][k] += cs[a]
    # gates (MC.7)
    M = [sp.Matrix(N, N, lambda i, j, P=P: sp.Rational(P[i][j])) for P in Ps]
    ranks = tuple(m.rank() for m in M)
    want = (1, n - 1, n * (n - 3) // 2)
    idem = all((m * m - m).is_zero_matrix for m in M)
    part = (M[0] + M[1] + M[2] - sp.eye(N)).is_zero_matrix
    return Ps, {"ranks": list(ranks), "ranks_expected": list(want),
                "rank_gate": ranks == want, "idempotent": bool(idem), "partition": bool(part)}

# ---- OP2: exact Molien to t^3 via class reps; det(I - tP) = prod(1 - t^len) ----
def op2(n, PAIRS, IDX):
    t = sp.symbols("t")
    fact = 1
    for k in range(2, n + 1): fact *= k
    total = sp.Integer(0)
    for mu in partitions(n):
        rep = class_rep(mu, n)
        pi = pair_perm(rep, PAIRS, IDX)
        seen, den = [False] * len(pi), sp.Integer(1)
        for s in range(len(pi)):
            if not seen[s]:
                L, c = 0, s
                while not seen[c]:
                    seen[c] = True; c = pi[c]; L += 1
                den *= (1 - t ** L)
        total += sp.Rational(class_size(mu, n)) / den
    series = sp.series(total / fact, t, 0, 4).removeO().expand()
    a = [int(series.coeff(t, k)) for k in (1, 2, 3)]
    return {"a1": a[0], "a2": a[1], "a3": a[2]}

# ---- OP3: bordered-Jacobian rank op at the pinned fixture ----
def op3(n, PAIRS, IDX, Ps, g, offd):
    N = len(PAIRS)
    H = [[Fr(0)] * n for _ in range(n)]
    for (i, j), v in zip(PAIRS, offd):
        H[i][j] = H[j][i] = v
    O = [H[i][j] - Fr(g[i]) * H[j][j] / (2 * Fr(g[j])) - Fr(g[j]) * H[i][i] / (2 * Fr(g[i]))
         for (i, j) in PAIRS]
    Evals, Jrows = [], []
    for r in (1, 2, 3, 4):
        tot = Fr(0)
        row = [sp.Rational(0)] * N
        sgn = (-1) ** (r + 1)
        for I in combinations(range(n), r + 1):
            m = sp.zeros(r + 2)
            for a, i in enumerate(I):
                m[0, a + 1] = m[a + 1, 0] = sp.Rational(g[i])
                for b, j in enumerate(I):
                    m[a + 1, b + 1] = sp.Rational(H[i][j])
            tot += Fr(sp.Rational(m.det()))
            adj = m.adjugate()
            for a in range(len(I)):
                for b in range(a + 1, len(I)):
                    k = IDX[(I[a], I[b])]
                    row[k] += adj[b + 1, a + 1] + adj[a + 1, b + 1]
        Evals.append(sgn * tot)
        Jrows.append([sgn * x for x in row])
    for P in Ps:  # m2 rows = 2 * (P_X O)
        v = [2 * sum(P[i][k] * O[k] for k in range(N)) for i in range(N)]
        Jrows.append([sp.Rational(x) for x in v])
    J = sp.Matrix(Jrows)
    return {"Ehat": [str(e) for e in Evals], "J_shape": [7, N], "J_rank": int(J.rank()),
            "O_echo_sha": EH.records_sha(json.dumps([str(x) for x in O]))}

def main():
    EH.clause_gate(PREDECL, WALL_CLAUSES, PREDECL_PIN)
    EH.pin_gate(PINS)
    print("GATES_GREEN predecl_pin", PREDECL_PIN, "content_pins", len(PINS))
    blob_math, timings = {}, {}
    for n in (6, 7):
        PAIRS, IDX = pair_index(n)
        rec, tm = {}, {}
        t0 = time.perf_counter(); Ps, pg = op1(n, PAIRS, IDX)
        tm["OP1"] = {"wall_s": round(time.perf_counter() - t0, 3), "rss_mb": round(rss_mb(), 1)}
        rec["projectors"] = pg
        t0 = time.perf_counter(); rec["molien"] = op2(n, PAIRS, IDX)
        tm["OP2"] = {"wall_s": round(time.perf_counter() - t0, 3), "rss_mb": round(rss_mb(), 1)}
        t0 = time.perf_counter()
        rec["bordered_jacobian"] = op3(n, PAIRS, IDX, Ps, FIX[n]["g"], FIX[n]["offd"])
        tm["OP3"] = {"wall_s": round(time.perf_counter() - t0, 3), "rss_mb": round(rss_mb(), 1)}
        rec["fixture"] = {"g": FIX[n]["g"], "offd": [str(x) for x in FIX[n]["offd"]], "N": len(PAIRS)}
        blob_math[f"n{n}"] = rec
        timings[f"n{n}"] = tm
        if not (pg["rank_gate"] and pg["idempotent"] and pg["partition"]):
            blob = json.dumps(blob_math, sort_keys=True, indent=1)
            print(blob); print("RECORDS_SHA256", EH.records_sha(blob))
            print("K-C2 PROJECTOR GATE FAILURE at n =", n); sys.exit(2)
    blob = json.dumps(blob_math, sort_keys=True, indent=1)
    print(blob)
    print("RECORDS_SHA256", EH.records_sha(blob))
    print("TIMINGS_JSON", json.dumps(timings, sort_keys=True))
    print("SCOUT_COMPLETE")

if __name__ == "__main__":
    main()
