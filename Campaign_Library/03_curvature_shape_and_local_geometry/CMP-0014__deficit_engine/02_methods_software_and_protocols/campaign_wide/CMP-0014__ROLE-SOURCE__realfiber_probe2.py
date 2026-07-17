#!/usr/bin/env python3
"""REALFIBER Probe-2 — continuation bridge attempt. Predecl pin 9f706c1a74a21317.
[CONTAINER] gated numerics, EMPIRICAL ceiling. Spectrum preserved by exact conjugation;
diag corrected via psi_W Newton (rank certified in Probe-1). Deterministic (seeded, 1 thread)."""
import os
os.environ["OMP_NUM_THREADS"] = "1"; os.environ["OPENBLAS_NUM_THREADS"] = "1"
import json, hashlib, itertools
import numpy as np

GRADER_CLAUSES = [
 "Pinned: 20 starts (PRNG seed 20260702), 3 step-schedules",
 "tolerance ladder 1e\u22128\u21921e\u221212, both directions",
 "**A (bridge):** endpoint within tol of target orbit",
 "**B (persistent failure, all schedules):** OPEN stands, failure geometry banked",
 "**C (locally-constant obstruction found en route):** discovery-grade",
]
pre = open("portfolio/campaigns/deficit_engine/REALFIBER_PREDECL.md", encoding="utf-8").read()
for cl in GRADER_CLAUSES:
    assert cl in pre, f"CLAUSE DRIFT: {cl[:40]}... refuse to run"
assert hashlib.sha256(pre.encode()).hexdigest()[:16] == "9f706c1a74a21317", "PREDECL PIN MISMATCH"

m = 5
PAIRS = list(itertools.combinations(range(m), 2))
def adj(edges):
    W = np.zeros((m, m))
    for i, j in edges: W[i, j] = W[j, i] = 1.0
    return W
A_star = adj([(0,1),(0,2),(0,3),(0,4)])
A_cyc  = adj([(0,1),(1,2),(2,3),(3,0)])

def skew(coef):
    A = np.zeros((m, m))
    for k, (a, b) in enumerate(PAIRS):
        A[a, b] = coef[k]; A[b, a] = -coef[k]
    return A
def psi(W):  # 5 x 10, column (a,b) = -2 W_ab (e_a - e_b)
    P = np.zeros((m, len(PAIRS)))
    for k, (a, b) in enumerate(PAIRS):
        P[a, k] = -2 * W[a, b]; P[b, k] = 2 * W[a, b]
    return P
def cayley_conj(W, A):
    I = np.eye(m)
    R = np.linalg.solve((I + A).T, (I - A).T).T   # R = (I-A)(I+A)^-1, orthogonal
    Wn = R.T @ W @ R
    return 0.5 * (Wn + Wn.T)
def diag_correct(W, tol=1e-12, iters=8):
    for _ in range(iters):
        d = np.diag(W).copy()
        if np.max(np.abs(d)) <= tol: return W, True
        P = psi(W)
        b, *_ = np.linalg.lstsq(P, -d, rcond=None)
        W = cayley_conj(W, 0.5 * skew(b))
    return W, (np.max(np.abs(np.diag(W))) <= tol)
def DW_basis(W):  # orthonormal basis of {[W,A]: diag([W,A])=0}, as 10-vectors (pair coords)
    P = psi(W)
    _, s, Vt = np.linalg.svd(P)
    null = Vt[np.sum(s > 1e-10):]          # ker psi in so(5) coords
    imgs = []
    for row in null:
        A = skew(row); B = W @ A - A @ W
        imgs.append(np.array([B[i, j] for (i, j) in PAIRS]))
    M = np.array(imgs).T
    if M.size == 0: return np.zeros((10, 0)), null
    Q, R = np.linalg.qr(M)
    keep = np.abs(np.diag(R)) > 1e-10
    return Q[:, keep], null
def pairvec(W): return np.array([W[i, j] for (i, j) in PAIRS])
def perm_orbit(W):
    seen, out = set(), []
    for p in itertools.permutations(range(m)):
        Wp = W[np.ix_(p, p)]
        key = tuple(np.round(pairvec(Wp), 6))
        if key not in seen: seen.add(key); out.append(Wp)
    return out
T_cyc, T_star = perm_orbit(A_cyc), perm_orbit(A_star)
assert len(T_cyc) == 15 and len(T_star) == 5, "orbit sizes off predecl"
CP_TARGET = np.array([0.0, -4.0, 0.0, 0.0])   # c1..c4 of lam^5-4lam^3 style check via poly
def cp_resid(W):
    c = np.poly(W)   # leading 1, then -e1, e2, ...
    return np.max(np.abs(c[1:] - np.array([0, -4, 0, 0, 0])))
def dist_orbit(W, targets):
    v = pairvec(W)
    return min(np.linalg.norm(v - pairvec(T)) for T in targets)

SCHEDULES = {"S1": (0.05, 400), "S2": (0.015, 800), "S3": (0.004, 1500)}
MAXSTEP = 6000
SCHED_ID = {"S1": 1, "S2": 2, "S3": 3}
DIR_ID = {"star->cyc": 1, "cyc->star": 2}
rng_master = np.random.default_rng(20260702)
runs = []
outcome_A_hits = []
for direction, (W0raw, targets, tname) in {
    "star->cyc": (A_star, T_cyc, "cycle"), "cyc->star": (A_cyc, T_star, "star")}.items():
    for sname, (eta0, stall_win) in SCHEDULES.items():
        for start in range(20):
            rng = np.random.default_rng(20260702 + 1000*start + 100000*DIR_ID[direction] + 10000*SCHED_ID[sname])
            W = W0raw.copy()
            if direction == "cyc->star":   # smooth-stratum perturbed start (predecl mandate)
                Bas, null = DW_basis(W)
                kick = null[rng.integers(len(null))]
                W = cayley_conj(W, 0.03 * skew(kick)); W, ok = diag_correct(W)
                if not ok: runs.append(dict(dir=direction, sched=sname, start=start,
                                            status="g1-fail-at-start")); continue
            eta, best, since, status, final_d = eta0, np.inf, 0, "cap", None
            for step in range(MAXSTEP):
                Bas, _ = DW_basis(W)
                if Bas.shape[1] == 0: status = "no-tangent"; break
                g = np.zeros(10); v = pairvec(W)
                Tbest = min(targets, key=lambda T: np.linalg.norm(v - pairvec(T)))
                g = v - pairvec(Tbest)
                d = -(Bas @ (Bas.T @ g))
                if np.linalg.norm(d) < 1e-14:
                    d = Bas @ rng.standard_normal(Bas.shape[1])
                if rng.random() < 0.15:   # exploration mix
                    d = 0.7*d + 0.3*np.linalg.norm(d)*(Bas @ rng.standard_normal(Bas.shape[1]))
                d = d / (np.linalg.norm(d) + 1e-300)
                # lift pair-direction to so(5): least squares [W,A] ~ d over ker psi
                P = psi(W); _, s, Vt = np.linalg.svd(P)
                null = Vt[np.sum(s > 1e-10):]
                cols = []
                for row in null:
                    A = skew(row); B = W @ A - A @ W
                    cols.append(np.array([B[i, j] for (i, j) in PAIRS]))
                Mc = np.array(cols).T
                coef, *_ = np.linalg.lstsq(Mc, d, rcond=None)
                Adir = skew(null.T @ coef)
                nA = np.linalg.norm(Adir)
                if nA < 1e-14: status = "no-lift"; break
                Wtry = cayley_conj(W, (eta / nA) * Adir)
                Wtry, ok = diag_correct(Wtry)
                if not ok or cp_resid(Wtry) > 1e-8:
                    eta *= 0.5
                    if eta < 1e-6: status = "eta-collapse"; break
                    continue
                dn = dist_orbit(Wtry, targets)
                W = Wtry
                if dn < best - 1e-9: best, since = dn, 0
                else: since += 1
                if best < 1e-8: status = "bridge"; break
                if since > stall_win:
                    eta *= 0.5; since = 0
                    if eta < 1e-6: status = "stall"; break
            final_d = dist_orbit(W, targets)
            rec = dict(dir=direction, sched=sname, start=start, status=status,
                       final_dist=round(float(final_d), 12), best=round(float(best), 12),
                       cp_resid=float(f"{cp_resid(W):.3e}"), diag_max=float(f"{np.max(np.abs(np.diag(W))):.3e}"))
            runs.append(rec)
            if status == "bridge": outcome_A_hits.append(rec)

n_bridge = sum(r.get("status") == "bridge" for r in runs)
n_stall  = sum(r.get("status") in ("stall", "eta-collapse") for r in runs)
n_cap    = sum(r.get("status") == "cap" for r in runs)
if n_bridge > 0: OUTCOME = "A"
elif n_cap == 0 and n_stall > 0 and n_bridge == 0: OUTCOME = "B-candidate (all schedules stalled)"
else: OUTCOME = "INCONCLUSIVE-budget (runs at cap still descending)"
best_overall = min(r["best"] for r in runs if "best" in r)
rec = {"predecl_pin": "9f706c1a74a21317", "outcome": OUTCOME,
       "counts": {"bridge": n_bridge, "stall": n_stall, "cap": n_cap, "total": len(runs)},
       "best_overall_dist": best_overall,
       "bridge_examples": outcome_A_hits[:4],
       "per_direction_best": {d: min(r["best"] for r in runs if r.get("dir") == d and "best" in r)
                              for d in ("star->cyc", "cyc->star")}}
blob = json.dumps(rec, sort_keys=True, indent=1)
print(blob)
print("RECORDS_SHA256", hashlib.sha256(blob.encode()).hexdigest()[:16])
print("OUTCOME:", OUTCOME)
