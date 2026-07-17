#!/usr/bin/env python3
"""f3_battery.py -- STAGE F3 (CL-F3 local tier), PREREG_F3 battery, n=5.
role=probe. Probe: exact Fraction Gaussian-elimination ranks. Referee
(independent): sympy rank of the same matrices; must agree everywhere.
Deterministic; run twice for x2. Usage: f3_battery.py OUTPATH
Defs first, dispatch last."""
import sys, os, json, hashlib, itertools
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(HERE + '/../../../../evals/dbp_involution'))
import rep_utils as RU

GRADER_CLAUSES = {
 "PF3.0": "gates: pins; clauses; projector ranks (1,4,5) + idempotency + partition of identity; a₂ = 3 by Molien; a₃(Molien) == rank(orbit-sum span); conj-tangents lie in ker(dê) exactly (σ conj-invariance seen by the differentials), all fixtures",
 "PF3.1": "rank of stacked dê_r (r=1..4) at each fixture = 4 (⟹ σ-fiber smooth of dim 6 locally)",
 "PF3.2": "rank of the 6 conjugation tangents δO_X at each fixture = 6 (⟹ conj-orbits generically OPEN in σ-fibers — the brief §4 banked side-question)",
 "PF3.3": "THE LOCAL SUMMIT CLAUSE: rank of the degree-≤3 invariant differentials restricted to the fiber tangent (ker dê, dim per PF3.1) = 6 at each fixture ⟹ the invariant vector is locally separating on the σ-fiber at the pinned strata",
 "PF3.4": "deficit of the degree-≤2 layer: rank of deg-≤2 invariant differentials on the fiber tangent, per fixture (upper bound 4 by count: 1 + 3 rows)",
}
N5, NP = 5, 10
PAIRS = list(itertools.combinations(range(N5), 2))
PIDX = {p: k for k, p in enumerate(PAIRS)}

def sha256_file(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def gate_pins_clauses():
    pins = {}
    for line in open(HERE + '/freeze_pins_f3.sha256'):
        h, path = line.split()
        pins[path] = h
    for path, h in pins.items():
        full = os.path.normpath(os.path.join(HERE, path))
        if sha256_file(full) != h:
            print("REFUSE_MISMATCH " + path); sys.exit(2)
    pre = open(HERE + '/PREREG_F3.md', encoding='utf-8').read()
    for cid, cl in GRADER_CLAUSES.items():
        if cl not in pre:
            print("CLAUSE_DRIFT " + cid); sys.exit(3)
    return pins

def det(A):
    M = [row[:] for row in A]; m = len(M); s = Fr(1)
    for c in range(m):
        piv = next((i for i in range(c, m) if M[i][c] != 0), None)
        if piv is None: return Fr(0)
        if piv != c:
            M[c], M[piv] = M[piv], M[c]; s = -s
        for i in range(c + 1, m):
            if M[i][c] != 0:
                f = M[i][c] / M[c][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[c])]
    for c in range(m): s *= M[c][c]
    return s

def rank_gauss(rows):
    M = [r[:] for r in rows]; n, m = len(M), len(M[0]) if M else 0; r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if M[i][c] != 0), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        inv = Fr(1) / M[r][c]; M[r] = [x * inv for x in M[r]]
        for i in range(n):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r

def nullspace(rows, m):
    # rows: list of length-m Fraction rows; returns basis of kernel
    M = [r[:] for r in rows]; n = len(M); r = 0; pivcols = []
    for c in range(m):
        piv = next((i for i in range(r, n) if M[i][c] != 0), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        inv = Fr(1) / M[r][c]; M[r] = [x * inv for x in M[r]]
        for i in range(n):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        pivcols.append(c); r += 1
    free = [c for c in range(m) if c not in pivcols]
    basis = []
    for fc in free:
        v = [Fr(0)] * m; v[fc] = Fr(1)
        for ri, pc in enumerate(pivcols):
            v[pc] = -M[ri][fc]
        basis.append(v)
    return basis

def sym_from_pairs(O, diag=None):
    M = [[Fr(0)] * N5 for _ in range(N5)]
    for (i, j), v in zip(PAIRS, O):
        M[i][j] = M[j][i] = Fr(v)
    if diag:
        for i in range(N5): M[i][i] = Fr(diag[i])
    return M

def O_of(H, g):
    return [H[i][j] - g[i]*H[j][j]/(2*g[j]) - g[j]*H[i][i]/(2*g[i])
            for (i, j) in PAIRS]

def ehat(O, g, r):
    H = sym_from_pairs(O)
    tot = Fr(0)
    for I in itertools.combinations(range(N5), r + 1):
        m = [[Fr(0)] * (r + 2) for _ in range(r + 2)]
        for a, i in enumerate(I):
            m[0][a+1] = m[a+1][0] = Fr(g[i])
            for b, j in enumerate(I):
                m[a+1][b+1] = H[i][j]
        tot += det(m)
    return (-1) ** (r + 1) * tot

def interp_lin_coeff(pts):
    # exact linear coefficient of the interpolating polynomial at x=0
    tot = Fr(0)
    for i, (xi, yi) in enumerate(pts):
        d = Fr(1); s = Fr(0)
        for j, (xj, _) in enumerate(pts):
            if j == i: continue
            d *= (xi - xj)
        # derivative of Lagrange basis at 0
        for j, (xj, _) in enumerate(pts):
            if j == i: continue
            p = Fr(1)
            for k, (xk, _) in enumerate(pts):
                if k in (i, j): continue
                p *= (0 - xk)
            s += p
        tot += yi * s / d
    return tot

def dE_rows(O, g):
    rows = []
    for r in (1, 2, 3, 4):
        row = []
        for k in range(NP):
            pts = []
            for tv in range(5):
                Ot = list(O); Ot[k] = Ot[k] + Fr(tv)
                pts.append((Fr(tv), ehat(Ot, g, r)))
            row.append(interp_lin_coeff(pts))
        rows.append(row)
    return rows

def conj_tangent_rows(O, g):
    ws = []
    for k in range(1, N5):
        w = [Fr(0)] * N5; w[0] = Fr(g[k]); w[k] = -Fr(g[0])
        ws.append(w)
    H = sym_from_pairs(O)
    rows = []
    for a in range(4):
        for b in range(a + 1, 4):
            X = [[ws[a][i]*ws[b][j] - ws[b][i]*ws[a][j]
                  for j in range(N5)] for i in range(N5)]
            HX = [[sum(H[i][k]*X[k][j] for k in range(N5))
                   for j in range(N5)] for i in range(N5)]
            XH = [[sum(X[i][k]*H[k][j] for k in range(N5))
                   for j in range(N5)] for i in range(N5)]
            dH = [[HX[i][j] - XH[i][j] for j in range(N5)]
                  for i in range(N5)]
            dHs = [[(dH[i][j] + dH[j][i]) / 2 for j in range(N5)]
                   for i in range(N5)]
            rows.append(O_of(dHs, g))
    return rows

def pair_perm(p):
    # returns index permutation on PAIRS
    out = []
    for (i, j) in PAIRS:
        a, b = p[i], p[j]
        out.append(PIDX[(min(a, b), max(a, b))])
    return out

def projectors5():
    from math import factorial
    Ps = []
    perms = list(itertools.permutations(range(N5)))
    for lam in ((5,), (4, 1), (3, 2)):
        d = RU.specht_dim(lam)
        P = [[Fr(0)] * NP for _ in range(NP)]
        for p in perms:
            chi = RU.specht_char(lam, RU.cycle_type(p))
            if chi == 0: continue
            pp = pair_perm(p)
            for k in range(NP):
                P[pp[k]][k] += chi
        c = Fr(d, factorial(N5))
        Ps.append([[c * P[i][j] for j in range(NP)] for i in range(NP)])
    return Ps

def gate_projectors(Ps):
    assert tuple(rank_gauss(P) for P in Ps) == (1, 4, 5), "K-F30 ranks"
    for P in Ps:
        PP = [[sum(P[i][k]*P[k][j] for k in range(NP)) for j in range(NP)]
              for i in range(NP)]
        assert PP == P, "K-F30 idempotency"
    S = [[Ps[0][i][j] + Ps[1][i][j] + Ps[2][i][j] for j in range(NP)]
         for i in range(NP)]
    assert S == [[Fr(int(i == j)) for j in range(NP)] for i in range(NP)], \
        "K-F30 partition"

def molien_counts():
    perms = list(itertools.permutations(range(N5)))
    def fixp(p):
        return sum(1 for k, m in enumerate(pair_perm(p)) if m == k)
    a2n = a3n = Fr(0)
    for p in perms:
        p1 = fixp(p)
        p2_ = fixp(tuple(p[p[i]] for i in range(N5)))
        p3_ = fixp(tuple(p[p[p[i]]] for i in range(N5)))
        a2n += Fr(p1*p1 + p2_, 2)
        a3n += Fr(p1**3 + 3*p1*p2_ + 2*p3_, 6)
    return a2n / 120, a3n / 120

def deg3_orbit_sums():
    gens = [tuple([1, 0, 2, 3, 4]), tuple([1, 2, 3, 4, 0])]
    gperms = [pair_perm(p) for p in gens]
    monos = [tuple(sorted(t)) for t in
             itertools.combinations_with_replacement(range(NP), 3)]
    mset = set(monos)
    seen, orbits = set(), []
    for m in monos:
        if m in seen: continue
        orb, stack = {m}, [m]
        while stack:
            cur = stack.pop()
            for gp in gperms:
                nxt = tuple(sorted(gp[i] for i in cur))
                if nxt not in orb:
                    orb.add(nxt); stack.append(nxt)
        seen |= orb
        orbits.append(sorted(orb))
    assert all(m in mset for orb in orbits for m in orb)
    return orbits

def grad_deg3(orbit, O):
    g = [Fr(0)] * NP
    for m in orbit:
        for pos in range(3):
            k = m[pos]
            rest = m[:pos] + m[pos+1:]
            g[k] += O[rest[0]] * O[rest[1]]
    # each monomial x_a x_b x_c contributes to d/dx_k once per occurrence;
    # multiplicity handled by iterating positions
    return g

def sympy_rank(rows):
    import sympy as sp
    if not rows: return 0
    return sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in r]
                      for r in rows]).rank()

def main():
    outp = sys.argv[1]
    pins = gate_pins_clauses()
    fx = json.load(open(HERE + '/fixtures_f3.json'))
    Ps = projectors5()
    gate_projectors(Ps)
    a2, a3 = molien_counts()
    assert a2 == 3, "K-F30 Molien a2 != 3"
    orbits = deg3_orbit_sums()
    assert a3 == len(orbits), "K-F30 a3(Molien) != orbit-sum count"
    rows_out = [{"row": "GATES", "a2": str(a2), "a3": str(a3),
                 "deg3_orbit_sums": len(orbits), "pass": True}]
    led = {"role": "probe", "prereg": "PREREG_F3.md",
           "battery_sha256": sha256_file(os.path.abspath(__file__))}
    v1 = v2 = v3 = True
    deficits = {}
    for f in fx['fixtures']:
        g = [Fr(x) for x in f['g']]
        O = [Fr(x) for x in f['O']]
        dE = dE_rows(O, g)
        r1 = rank_gauss(dE)
        assert r1 == sympy_rank(dE), "probe/referee disagree dE"
        fib = nullspace(dE, NP)
        conj = conj_tangent_rows(O, g)
        for cr in conj:
            for er in dE:
                assert sum(a*b for a, b in zip(er, cr)) == 0, \
                    "K-F31 conj tangent escapes fiber"
        r2 = rank_gauss(conj)
        assert r2 == sympy_rank(conj), "probe/referee disagree conj"
        inv_rows = [[Fr(1)] * NP]
        for P in Ps:
            PO = [sum(P[i][j] * O[j] for j in range(NP)) for i in range(NP)]
            inv_rows.append([2 * x for x in PO])
        for orb in orbits:
            inv_rows.append(grad_deg3(orb, O))
        proj = [[sum(r[k] * b[k] for k in range(NP)) for b in fib]
                for r in inv_rows]
        r3 = rank_gauss(proj)
        assert r3 == sympy_rank(proj), "probe/referee disagree inv"
        r4 = rank_gauss(proj[:4])
        assert r4 == sympy_rank(proj[:4]), "probe/referee disagree deg2"
        fdim = NP - r1
        v1 = v1 and (r1 == 4)
        v2 = v2 and (r2 == 6)
        v3 = v3 and (r3 == fdim == 6)
        deficits[f['id']] = {"dE_rank": r1, "fiber_dim": fdim,
                             "conj_rank": r2, "inv_rank_on_fiber": r3,
                             "deg2_rank_on_fiber": r4,
                             "deficit_deg3": fdim - r3,
                             "deficit_deg2": fdim - r4}
        rows_out.append({"row": "FIX", "fixture": f['id'], **deficits[f['id']]})
    verdicts = {"PF3.0": True, "PF3.1": v1, "PF3.2": v2, "PF3.3": v3,
                "PF3.4_recorded": {k: d["deg2_rank_on_fiber"]
                                   for k, d in deficits.items()}}
    rows_out.append({"row": "VERDICTS", "verdicts": verdicts,
                     "ledger": led, "pins": pins})
    with open(outp, 'w') as fh:
        for r in rows_out:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    print(json.dumps(verdicts, sort_keys=True, indent=1))
    print("F3_DONE")

main()
