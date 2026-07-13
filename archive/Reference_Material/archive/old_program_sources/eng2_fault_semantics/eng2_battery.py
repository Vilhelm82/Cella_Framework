#!/usr/bin/env python3
"""eng2_battery.py -- STAGE ENG2 fault-semantics battery, PREREG_ENG2.
role=probe. Probe path: exact polynomial-in-t interpolation of each channel
functional. Referee path (independent): direct evaluation at t = 1/7
compared against the interpolated polynomial. Exact Fractions throughout.
Deterministic; run twice for x2. Usage: eng2_battery.py OUTPATH
Defs first, dispatch last."""
import sys, os, json, hashlib, itertools
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))

GRADER_CLAUSES = {
 "PE.0": "n=3 keystone anchors: κ̂_c = −2/7, K̂ = −6/7, κ̂_c/K̂ = 1/3 = spec κ_c/K_G; triangle decomposition regression at all fixtures",
 "PE.1": "NUMERATOR EXACTNESS: under S1 and S2 self-fault families, Δ_c(t) and κ̂_c(t) are CONSTANT polynomials in t (exact, full coefficient check, every fixture)",
 "PE.2": "SCALING: κ̂_c/K̂ invariant under g → t·g at t = 2, 3 (H fixed), every fixture",
 "PE.3": "COUPLING FAULTS MOVE THE RATIO: d/dt[κ̂_c/K̂] at t=0 is NONZERO for F1 and F2 at every fixture",
 "PE.4": "OG SELF-FAULT RATIO CLAUSE (discriminating test of the literal law): d/dt[κ̂_c/K̂] at t=0 under S1, S2",
 "PE.5": "LOCALIZATION (the V4 sensor upgrade): for F1 on edge e* = (0,1): {S : d/dt Δ_S ≠ 0 at t=0} == {S ⊇ e*} exactly, every fixture n ≥ 4 (Δ_S = triangle channel from the I.3b decomposition)",
}
OG_CLAUSE = "κ_c / K_G is invariant under\nuniform gradient scaling. Coupling faults change the ratio; self-faults\npreserve it."

def sha256_file(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def gate():
    pins = {}
    for line in open(HERE + '/freeze_pins_eng2.sha256'):
        h, path = line.split()
        pins[path] = h
    for path, h in pins.items():
        full = os.path.normpath(os.path.join(HERE, path))
        if sha256_file(full) != h:
            print("REFUSE_MISMATCH " + path); sys.exit(2)
    prereg = open(HERE + '/PREREG_ENG2.md', encoding='utf-8').read()
    for cid, clause in GRADER_CLAUSES.items():
        if clause not in prereg:
            print("CLAUSE_DRIFT " + cid); sys.exit(3)
    if OG_CLAUSE not in prereg:
        print("CLAUSE_DRIFT OG"); sys.exit(3)
    return pins

def pairs_of(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]

def det(A):
    M = [row[:] for row in A]; n = len(M); s = Fr(1)
    for c in range(n):
        piv = next((i for i in range(c, n) if M[i][c] != 0), None)
        if piv is None: return Fr(0)
        if piv != c:
            M[c], M[piv] = M[piv], M[c]; s = -s
        for i in range(c + 1, n):
            if M[i][c] != 0:
                f = M[i][c] / M[c][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[c])]
    for c in range(n): s *= M[c][c]
    return s

def e_top(A):
    n = len(A)
    tot = Fr(0)
    for k in range(n):
        sub = [[A[i][j] for j in range(n) if j != k]
               for i in range(n) if i != k]
        tot += det(sub)
    return tot

def mat_mul(A, B):
    k, l = len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(l)]
            for i in range(len(A))]

def tangent_P(g):
    n = len(g); q = sum(Fr(x) * x for x in g)
    return [[(Fr(1) if i == j else Fr(0)) - Fr(g[i]) * g[j] / q
             for j in range(n)] for i in range(n)], q

def build_H(n, offd, diag):
    M = [[Fr(0)] * n for _ in range(n)]
    for idx, (i, j) in enumerate(pairs_of(n)):
        M[i][j] = M[j][i] = Fr(offd[idx])
    for i in range(n): M[i][i] = Fr(diag[i])
    return M

def split_c(M):
    n = len(M)
    Hc = [[M[i][j] if i != j else Fr(0) for j in range(n)]
          for i in range(n)]
    return Hc

def channels(g, M):
    P, q = tangent_P(g)
    Hc = split_c(M)
    kc = e_top(mat_mul(mat_mul(P, Hc), P))
    K = e_top(mat_mul(mat_mul(P, M), P))
    tr2 = sum(2 * M[i][j] * M[i][j]
              for i in range(len(M)) for j in range(i + 1, len(M)))
    A = mat_mul(mat_mul(P, Hc), P)
    trA = sum(A[i][i] for i in range(len(A)))
    trA2 = sum(A[i][j] * A[j][i]
               for i in range(len(A)) for j in range(len(A)))
    delta_c = -q * ((trA * trA - trA2) / 2)
    return kc, K, delta_c, q

def fault_H(n, base_offd, base_diag, fam, t):
    offd = [Fr(x) for x in base_offd]; diag = [Fr(x) for x in base_diag]
    N = len(offd)
    if fam == 'F1':
        offd[0] += t
    elif fam == 'F2':
        dc = [1, -1, 2, 1, -2, 1, 3, -1, 1, 2][:N]
        offd = [o + t * d for o, d in zip(offd, dc)]
    elif fam == 'S1':
        diag[0] += t
    elif fam == 'S2':
        ds = [1, -2, 1, 3, -1][:n]
        diag = [o + t * d for o, d in zip(diag, ds)]
    return build_H(n, offd, diag)

def interp_poly(pts):
    # exact Lagrange -> coefficient list (low to high degree)
    m = len(pts)
    coeffs = [Fr(0)] * m
    for i, (xi, yi) in enumerate(pts):
        basis = [Fr(1)]
        denom = Fr(1)
        for j, (xj, _) in enumerate(pts):
            if j == i: continue
            denom *= (xi - xj)
            new = [Fr(0)] * (len(basis) + 1)
            for k, c in enumerate(basis):
                new[k] += c * (-xj); new[k + 1] += c
            basis = new
        for k, c in enumerate(basis):
            coeffs[k] += yi * c / denom
    while len(coeffs) > 1 and coeffs[-1] == 0: coeffs.pop()
    return coeffs

def poly_eval(coeffs, x):
    tot = Fr(0)
    for c in reversed(coeffs): tot = tot * x + c
    return tot

def triangle_channels_d1(n, g, base_offd, base_diag):
    # d/dt Delta_S at t=0 for family F1 (edge (0,1)); exact via 3-pt interp
    prs = pairs_of(n); idx = {p: k for k, p in enumerate(prs)}
    W = []
    for (i, j) in prs:
        w = Fr(1)
        for k in range(n):
            if k not in (i, j): w *= g[k]
        W.append(w)
    out = {}
    for S in itertools.combinations(range(n), 3):
        d = Fr(1)
        for m in range(n):
            if m not in S: d *= Fr(g[m]) * g[m]
        T = 1 / d
        es = [idx[p] for p in itertools.combinations(S, 2)]
        pts = []
        for t in (Fr(0), Fr(1), Fr(2)):
            offd = [Fr(x) for x in base_offd]; offd[0] += t
            nu = [offd[e] * W[e] for e in range(len(prs))]
            loc = sum(nu[a] * nu[a] for a in es) \
                - sum(nu[a] * nu[b] for a in es for b in es if a != b)
            pts.append((t, T * loc))
        c = interp_poly(pts)
        out[str(S)] = (c[1] if len(c) > 1 else Fr(0))
    return out

def main():
    outp = sys.argv[1]
    pins = gate()
    fx = json.load(open(HERE + '/fixtures_eng2.json'))
    rows = []
    led = {"role": "probe", "prereg": "PREREG_ENG2.md",
           "battery_sha256": sha256_file(os.path.abspath(__file__))}
    # PE.0 anchors
    k3 = fx['fixtures'][0]
    M3 = build_H(3, k3['Hc_offdiag'], k3['H_diag'])
    kc, K, dc, q = channels(k3['g'], M3)
    a_ok = (kc == Fr(-2, 7) and K == Fr(-6, 7) and kc / K == Fr(1, 3)
            and dc == 4)
    assert a_ok, "K-E0 keystone anchors"
    rows.append({"row": "PE0", "anchors": True, "pass": True})
    verdicts = {"PE.0": True}
    pe = {k: True for k in ("PE.1", "PE.2", "PE.3", "PE.5")}
    pe4 = {}
    for f in fx['fixtures']:
        n, g = f['n'], f['g']
        base_o, base_d = f['Hc_offdiag'], f['H_diag']
        for fam in ('F1', 'F2', 'S1', 'S2'):
            pts_kc, pts_K, pts_dc = [], [], []
            for tv in range(n + 2):
                t = Fr(tv)
                M = fault_H(n, base_o, base_d, fam, t)
                kc, K, dc, q = channels(g, M)
                pts_kc.append((t, kc)); pts_K.append((t, K))
                pts_dc.append((t, dc))
            ckc, cK, cdc = (interp_poly(pts_kc), interp_poly(pts_K),
                            interp_poly(pts_dc))
            # referee: direct eval at t=1/7 vs polynomial
            M7 = fault_H(n, base_o, base_d, fam, Fr(1, 7))
            kc7, K7, dc7, _ = channels(g, M7)
            ref = (poly_eval(ckc, Fr(1, 7)) == kc7 and
                   poly_eval(cK, Fr(1, 7)) == K7 and
                   poly_eval(cdc, Fr(1, 7)) == dc7)
            assert ref, "probe/referee disagree"
            kc0, K0 = ckc[0], cK[0]
            dkc = ckc[1] if len(ckc) > 1 else Fr(0)
            dK = cK[1] if len(cK) > 1 else Fr(0)
            dratio = (dkc * K0 - kc0 * dK) / (K0 * K0)
            if fam in ('S1', 'S2'):
                const_ok = (len(ckc) == 1 and len(cdc) == 1)
                pe["PE.1"] = pe["PE.1"] and const_ok
                pe4[f['id'] + '_' + fam] = str(dratio)
            else:
                pe["PE.3"] = pe["PE.3"] and (dratio != 0)
            rows.append({"row": "FAM", "fixture": f['id'], "family": fam,
                         "kc_const": len(ckc) == 1, "dc_const": len(cdc) == 1,
                         "dratio_t0": str(dratio), "referee_ok": ref})
        # PE.2 scaling
        M = build_H(n, base_o, base_d)
        kc, K, dc, q = channels(g, M)
        for tv in fx['scaling_test_t']:
            g2 = [x * tv for x in g]
            kc2, K2, dc2, q2 = channels(g2, M)
            pe["PE.2"] = pe["PE.2"] and (kc2 / K2 == kc / K)
        # PE.5 localization (n >= 4)
        if n >= 4:
            d1 = triangle_channels_d1(n, g, base_o, base_d)
            moved = {S for S, v in d1.items() if v != 0}
            want = {str(S) for S in itertools.combinations(range(n), 3)
                    if 0 in S and 1 in S}
            ok5 = (moved == want)
            pe["PE.5"] = pe["PE.5"] and ok5
            rows.append({"row": "PE5", "fixture": f['id'],
                         "moved": sorted(moved), "expected": sorted(want),
                         "pass": ok5})
    verdicts.update(pe)
    verdicts["PE.4_dratio_selffault"] = pe4
    verdicts["PE.4_literal_OG_clause_holds"] = all(
        Fr(v) == 0 for v in pe4.values())
    rows.append({"row": "VERDICTS", "verdicts": verdicts, "ledger": led,
                 "pins": pins})
    with open(outp, 'w') as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    print(json.dumps(verdicts, sort_keys=True, indent=1))
    print("ENG2_DONE")

main()
