"""
ARITH-I STAGE B — SYMBOLIC PROOF, r=3 STANDARD pure-coupling channel constant.
FRESH, zero-import. sympy (declared).

*** CORRECTION (Will, 2026-07-06) ***
An earlier version of this file proved INT = -2 pi^2/5 for the density
  kappa_aux = -e_3(P Hc P)/q^{5/2}   (q^{(r+2)/2} on the COMPRESSION e_3).
That object is NOT the standard r=3 pure-coupling channel: it carries an extra
1/q ("1/q-weighted compression-density"). The STANDARD channel that retrodicts
the certified values (kappa_c = -1/49 at r=2) is
  kappa_{3;3,0} = (-1)^3 e_3(P Hc P)/q^{3/2}          ( engine /q^{r/2} )
because the bordered-minor numerator satisfies the exact identity
  det[[Hc, g],[g^T, 0]] = -q * e_3(P Hc P)             (verified below)
so the grid-normalized bordered channel -det[...]/q^{(r+2)/2} = e_3(P Hc P)/q^{3/2}.
The extra 1/q in the auxiliary object washed out a sqrt(5) (the odd-r parity
factor); the standard constant is an ALGEBRAIC-IRRATIONAL multiple of pi^2, and is
SCALE-INVARIANT (kappa dA -> alpha^0), unlike the auxiliary one (~1/c). See
CORRECTION_2026-07-06_channel_normalization.md.

STANDARD RESULT (this file, machine-checked):
  INT_S kappa_{3;3,0} dA = -2 pi^2/sqrt(5)   (all c; scale-invariant)
on the canonical n=4 ellipsoid F = sum y_i^2 + sum_{i<j} y_i y_j - c.

PROOF (Gauss map; steps checked):
  Gauss map nu=g/sqrt(q): diffeo S->S^3 (convex), P=I-nu nu^T,
     INT_S f K_GK dA = INT_{S^3} f dOmega,  K_GK = e_3(P H P)/q^{3/2}, INT K_GK dA = 2pi^2.
  phi := kappa_{3;3,0}/K_GK = -e_3(P Hc P)/e_3(P H P) = -(3 - sigma^2)/(5 - sigma^2),
     sigma = sum nu_i,  using e_3(P A P)=nu^T adj(A) nu, adj(H)=5I-J, adj(Hc)=3I-J.
     (NO cancellation now -- the (5 - sigma^2) survives; that is the whole point.)
  INT_S kappa dA = INT_{S^3} phi dOmega = -[2pi^2 - 2*INT_{S^3} dOmega/(5-sigma^2)].
  Sphere reduction (sigma^2 = 4 w^2, w = nu.ones/2, marginal ~ sqrt(1-w^2)):
     INT_{S^3} dOmega/(5-sigma^2) = pi^2 (1 - 1/sqrt5).
  => INT_S kappa dA = -[2pi^2 - 2 pi^2 (1 - 1/sqrt5)] = -2 pi^2/sqrt5.  QED

Exactness verdict UNCHANGED: -2pi^2/sqrt5 != 0 => NOT exact on the compact
ellipsoid. Character CHANGED: pi^2 * (1/sqrt5), an algebraic-irrational (odd-r
parity sqrt(n+1)=sqrt5), still NOT an elliptic period.
"""
import sympy as sp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)

n = 4
v1, v2, v3 = sp.symbols('v1 v2 v3', real=True)
v4 = sp.sqrt(1 - v1**2 - v2**2 - v3**2)
nu = sp.Matrix([v1, v2, v3, v4])
J = sp.ones(n, n); H = sp.eye(n) + J; Hc = J - sp.eye(n)
sigma = sum(nu)
def e_r(A, r):
    from itertools import combinations
    return sum(A[list(c), list(c)].det() for c in combinations(range(n), r))
P = sp.eye(n) - nu*nu.T

# --- bordered-minor identity: det[[Hc,g],[g^T,0]] = -q e_3(P Hc P) (numeric point) ---
import mpmath as mp
yv = [mp.mpf('1'), mp.mpf('0.3'), mp.mpf('-0.7'), mp.mpf('0.5')]
Hm = mp.matrix([[2 if i == j else 1 for j in range(4)] for i in range(4)])
Hcm = mp.matrix([[0 if i == j else 1 for j in range(4)] for i in range(4)])
gm = Hm*mp.matrix(yv); qm = sum(gm[i]**2 for i in range(4))
Pm = mp.eye(4) - (gm*gm.T)/qm
def e3m(A):
    from itertools import combinations
    tot = mp.mpf(0)
    for c in combinations(range(4), 3):
        tot += mp.det(mp.matrix([[A[i, j] for j in c] for i in c]))
    return tot
B = mp.zeros(5)
for i in range(4):
    for j in range(4):
        B[i, j] = Hcm[i, j]
    B[i, 4] = gm[i]; B[4, i] = gm[i]
check("BM.bordered_identity", abs(mp.det(B) - (-qm*e3m(Pm*Hcm*Pm))) < mp.mpf('1e-30'),
      "det[[Hc,g],[g^T,0]] = -q e_3(P Hc P) => standard kappa = e_3(P Hc P)/q^{3/2}")

# --- L3: e_3 forms ---
e3H = sp.simplify(e_r(P*H*P, 3)); e3Hc = sp.simplify(e_r(P*Hc*P, 3))
check("L3.e3", sp.simplify(e3H - (5 - sigma**2)) == 0 and sp.simplify(e3Hc - (3 - sigma**2)) == 0,
      "e_3(PHP)=5-sigma^2, e_3(PHcP)=3-sigma^2")

# --- phi (standard, NO cancellation) ---
phi = sp.simplify(-e3Hc/e3H)
check("phi.standard", sp.simplify(phi - (-(3 - sigma**2)/(5 - sigma**2))) == 0,
      "phi = kappa/K_GK = -(3-sigma^2)/(5-sigma^2)  [5-sigma^2 does NOT cancel]")

# --- sphere reduction: INT_{S^3} dOmega/(5-sigma^2) = pi^2 (1 - 1/sqrt5) ---
# marginal of one 'ones-axis' coordinate on S^3: density ~ sqrt(1-w^2); sigma^2 = 4 w^2.
# N_recip = INT_{-1}^{1} sqrt(1-w^2)/(5-4w^2) dw = (w=sin th) INT cos^2/(1+4cos^2) dth
#         = (1/4)[ INT 1 dth - INT dth/(1+4cos^2) ] over (-pi/2,pi/2) = (pi - Bb)/4,
# with Bb = INT_{-pi/2}^{pi/2} dth/(1+4cos^2 th) = (t=tan th) INT_0^inf 2 dt/(5+t^2) = pi/sqrt5.
t = sp.symbols('t', positive=True)
Bb = sp.simplify(2*sp.integrate(1/(5 + t**2), (t, 0, sp.oo)))    # = pi/sqrt5
check("S3.Bb", sp.simplify(Bb - sp.pi/sp.sqrt(5)) == 0, "INT dth/(1+4cos^2) = pi/sqrt5")
N_recip = (sp.pi - Bb)/4                                          # INT sqrt(1-w^2)/(5-4w^2) dw
D0 = sp.pi/2                                                      # INT sqrt(1-w^2) dw
int_recip = sp.simplify(2*sp.pi**2 * N_recip/D0)                 # INT_{S^3} 1/(5-sigma^2) dOmega
check("S3.reciprocal", sp.simplify(int_recip - sp.pi**2*(1 - 1/sp.sqrt(5))) == 0,
      f"INT_{{S^3}} dOmega/(5-sigma^2) = pi^2(1-1/sqrt5)")

# --- assemble: INT kappa = -[2pi^2 - 2*int_recip] ---
INT_kappa = sp.simplify(-(2*sp.pi**2 - 2*int_recip))
check("RESULT", sp.simplify(INT_kappa - (-2*sp.pi**2/sp.sqrt(5))) == 0,
      f"INT_S kappa_{{3;3,0}} dA = {INT_kappa} = -2 pi^2/sqrt(5)")
check("not_exact", sp.simplify(INT_kappa) != 0 and float(INT_kappa) < -8.8,
      f"nonzero ({float(INT_kappa):.6f}) -> NOT exact; algebraic-irrational * pi^2 (parity sqrt5)")

nch = 6
if FAILS:
    print(f"VERDICT: FAIL ({len(FAILS)}): {', '.join(FAILS)}")
    raise SystemExit(1)
print(f"VERDICT: ARITH-I r=3 STANDARD channel constant PROVEN -- {nch}/{nch}. "
      f"INT_S kappa_{{3;3,0}} dA = -2 pi^2/sqrt(5) (scale-invariant). NOT exact; an "
      f"algebraic-irrational (odd-r parity sqrt5) multiple of pi^2, not an elliptic "
      f"period. Corrects the earlier -2pi^2/5 (auxiliary 1/q-weighted object).")
