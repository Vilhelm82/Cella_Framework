"""
*** SUPERSEDED OBJECT (Will, 2026-07-06): this file integrates the AUXILIARY
1/q-weighted density -e_3(P Hc P)/q^{5/2} and gets -2 pi^2/5. That is NOT the
standard r=3 channel (which is /q^{3/2}, giving -2 pi^2/sqrt5). See
CORRECTION_2026-07-06_channel_normalization.md and arith_i_stageB_proof.py
(f2f851ea) for the corrected constant. The EXACTNESS VERDICT (nonzero -> not exact)
stands for both objects; only the value/character changed. Kept as the (correct)
computation of the auxiliary density and the K_GK=2pi^2 machinery control. ***

ARITH-I STAGE B — the r=3 exactness VERDICT (T-B resolved). FRESH, zero-import.
numpy (declared). Deterministic grid integration -> byte-stable.

PREREG 32f2fb3a (Stage-B; fabricated stop condition VOID). Refs: OPEN_B1_RESOLVED.md
(canonical n=4 surface + density, from the surfaced calc log v8 / standing results
v1.1). Paper-track fence: no engine priority changed.

THE QUESTION (T-B). Is the order-3 pure-coupling channel density
    kappa_{3;3,0} = -e_3(P Hc P)/q^{5/2},   Hc=offdiag(H), P=I-gg^T/q, q=|Hy|^2
exact on the canonical n=4 surface?

THE STRUCTURAL KEY (this session). The canonical n=4 surface
    F = sum y_i^2 + sum_{i<j} y_i y_j - c
has quadratic-form matrix M=(I+J)/2 with eigenvalues 5/2, 1/2, 1/2, 1/2 -- POSITIVE
DEFINITE. So (unlike the n=3 keystone hyperboloid, non-compact) it is an ELLIPSOID:
a COMPACT connected oriented 3-manifold (diffeo S^3). On a compact oriented M^m, a
top-form omega is EXACT  <=>  INT_M omega = 0. So T-B reduces to: is INT_S kappa = 0?
This is the "species change" CALC-24 Part A predicted for n>=4 (Gauss-Kronecker /
Chern-Gauss-Bonnet, not the 2-surface elliptic period).

RESULT.
  CONTROL   INT_S K_GK dA = 2*pi^2 = vol(S^3)   [K_GK = e_3(P H P)/q^{3/2}, the full
            Gauss-Kronecker curvature; Gauss-map degree 1 for a convex hypersurface]
            -- validates the area element + integration machinery.
  VERDICT   INT_S kappa_{3;3,0} dA = -3.948... != 0   =>  NOT EXACT.
  VALUE     ratio INT kappa / INT K_GK = -1/5 (to 7 digits at c=1)  =>
            INT_S kappa_{3;3,0} dA = -2*pi^2/5  (at c=1); scales as 1/c
            (kappa->a^-5, dA->a^3 under y->a y, so INT kappa ~ 1/c; K_GK topological).
            A RATIONAL MULTIPLE of vol(S^3) -- a pi^2-rational, NOT an elliptic period.

RESOLUTION OF T-B / T-C (a THIRD outcome, beyond the BRIEF's binary).
  - C1 (higher Cohn-Vossen: density exact / end data): FALSE -- INT != 0.
  - C2 (interior period of the double cover, transcendental): NOT the character here
    -- the value is pi^2-rational, not an elliptic/transcendental period.
  The BRIEF's YES/NO dichotomy was premised on the NON-COMPACT 2-surface (n=3)
  picture; it does not extend, exactly as CALC-24 Part A warned. On the canonical
  n>=4 surface the geometry is a compact ellipsoid, the integral is Gauss-Kronecker-
  species, and the r=3 channel constant is a rational multiple of vol(S^3).
  KILL K-3 (primitive found AND bump moves): NOT triggered (no primitive claimed;
  non-exactness established directly by the compact-integral criterion).

STAKED CONJECTURE (not proven): ratio = -1/(n+1) for general n (n=4 -> -1/5).

Convention: pin = `python3 reports/arithmetic_track/arith_i_stageB_verdict.py | sha256sum`.
"""
import numpy as np
from itertools import combinations

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)

n = 4
H = np.ones((n, n)) + np.eye(n)      # I + J
Hc = np.ones((n, n)) - np.eye(n)     # offdiag ones
# orthonormal eigen-frame of M=(I+J)/2: ones-direction (eig 5/2), 3 perp (eig 1/2)
U = [np.ones(n) / np.sqrt(n)]
for e in np.eye(n):
    w = e - sum(np.dot(e, u) * u for u in U)
    if np.linalg.norm(w) > 1e-9:
        U.append(w / np.linalg.norm(w))
U = np.array(U).T
Mlam = np.array([(1 + n) / 2.0, 0.5, 0.5, 0.5])

def e3(A):
    return sum(np.linalg.det(A[np.ix_(c, c)]) for c in combinations(range(4), 3))

def dens(y):
    g = H @ y; q = g @ g
    P = np.eye(n) - np.outer(g, g) / q
    return -e3(P @ Hc @ P) / q**2.5, e3(P @ H @ P) / q**1.5   # kappa_{3;3,0}, K_GK

def integrate(c, N1, N2, N3):
    a = np.sqrt(c / Mlam)
    t1 = (np.arange(N1) + 0.5) / N1 * np.pi
    t2 = (np.arange(N2) + 0.5) / N2 * np.pi
    t3 = (np.arange(N3) + 0.5) / N3 * 2 * np.pi
    d = (np.pi / N1) * (np.pi / N2) * (2 * np.pi / N3)
    Ik = IK = 0.0
    for x1 in t1:
        c1, s1 = np.cos(x1), np.sin(x1)
        for x2 in t2:
            for x3 in t3:
                s = np.array([c1, s1 * np.cos(x2), s1 * np.sin(x2) * np.cos(x3),
                              s1 * np.sin(x2) * np.sin(x3)])
                y = U @ (a * s)
                ds1 = np.array([-s1, c1 * np.cos(x2), c1 * np.sin(x2) * np.cos(x3),
                                c1 * np.sin(x2) * np.sin(x3)])
                ds2 = np.array([0.0, -s1 * np.sin(x2), s1 * np.cos(x2) * np.cos(x3),
                                s1 * np.cos(x2) * np.sin(x3)])
                ds3 = np.array([0.0, 0.0, -s1 * np.sin(x2) * np.sin(x3),
                                s1 * np.sin(x2) * np.cos(x3)])
                T = [U @ (a * z) for z in (ds1, ds2, ds3)]
                G = np.array([[Ti @ Tj for Tj in T] for Ti in T])
                dA = np.sqrt(max(np.linalg.det(G), 0.0))
                k, K = dens(y)
                Ik += k * dA * d; IK += K * dA * d
    return Ik, IK

Ik, IK = integrate(1.0, 56, 56, 112)
two_pi2 = 2 * np.pi**2
print(f"INFO  INT K_GK dA = {IK:.6f}  (2 pi^2 = {two_pi2:.6f})")
print(f"INFO  INT kappa   = {Ik:.6f}  (-2 pi^2/5 = {-two_pi2/5:.6f})")
print(f"INFO  ratio INT kappa / INT K_GK = {Ik/IK:.7f}  (-1/5 = -0.2)")

check("VB1.control_KGK", abs(IK - two_pi2) / two_pi2 < 2e-3,
      "INT K_GK dA = 2 pi^2 (Gauss-map degree) -- machinery validated")
check("VB2.not_exact", abs(Ik) > 1.0,
      "INT kappa_{3;3,0} dA clearly nonzero -> NOT EXACT (compact ellipsoid criterion)")
check("VB3.value_ratio", abs(Ik / IK - (-0.2)) < 1e-4,
      "INT kappa / INT K_GK = -1/5 -> INT kappa = -2 pi^2/5 at c=1 (pi^2-rational)")

nch = 3
if FAILS:
    print(f"VERDICT: FAIL ({len(FAILS)}): {', '.join(FAILS)}")
    raise SystemExit(1)
print(f"VERDICT: ARITH-I STAGE B r=3 EXACTNESS RESOLVED -- {nch}/{nch}. The r=3 channel "
      f"density is NOT EXACT on the canonical n=4 ellipsoid; INT = -2 pi^2/5 (pi^2-"
      f"rational, a rational multiple of vol(S^3)) -- neither higher Cohn-Vossen (C1) "
      f"nor an elliptic interior period (C2). The compact-ellipsoid reframing (CALC-24 "
      f"Part A) is the resolution. K-3 not triggered.")
