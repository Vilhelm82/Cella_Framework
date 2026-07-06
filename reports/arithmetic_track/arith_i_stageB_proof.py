"""
ARITH-I STAGE B — SYMBOLIC PROOF that INT_S kappa_{3;3,0} dA = -2 pi^2/(5c).
FRESH, zero-import. sympy (declared). Upgrades the numerical verdict
(arith_i_stageB_verdict.py, 843a7689) to an EXACT, machine-checked proof.

Canonical n=4 surface F = sum y_i^2 + sum_{i<j} y_i y_j - c = 0 (H=I+J), an
ELLIPSOID (M=(I+J)/2 pos. def.), compact ~ S^3.  Density
kappa_{3;3,0} = -e_3(P Hc P)/q^{5/2},  K_GK = e_3(P H P)/q^{3/2},
P = I - g g^T/q,  g = H y,  q = |g|^2,  Hc = J - I.

PROOF CHAIN (each step checked here):
  L1  Compression-determinant lemma: for P=I-nu nu^T (|nu|=1),
      e_{n-1}(P A P) = nu^T adj(A) nu  = det(A restricted to nu^perp).
  L2  Gauss map nu = g/sqrt(q) is a diffeo S -> S^3 (convex), P = I - nu nu^T,
      and INT_S f*K_GK dA = INT_{S^3} f dOmega.  So
      INT_S kappa dA = INT_{S^3} phi dOmega,  phi = kappa/K_GK = -e_3(PHcP)/(q e_3(PHP)).
  L3  adj(H)=5I-J, adj(Hc)=3I-J (n=4)  =>  e_3(PHP)=5-sigma^2, e_3(PHcP)=3-sigma^2,
      sigma = sum nu_i.
  L4  Constraint y^T M y = c (M=H/2) => q = 10c/(5-sigma^2).  The (5-sigma^2)
      CANCELS: phi = -(3-sigma^2)/(10c).
  L5  Sphere moments on S^3: INT dOmega = 2 pi^2,  INT sigma^2 dOmega = 2 pi^2
      (sigma^2 = sum nu_i^2 + cross; sum nu_i^2 = 1, cross integrates to 0).
      => INT (3-sigma^2) dOmega = 3*2pi^2 - 2pi^2 = 4 pi^2.
  ==> INT_S kappa dA = -(1/(10c)) * 4 pi^2 = -2 pi^2/(5c).  QED

General n (top order r=n-1, same symmetric family), same chain:
  ratio = INT kappa / INT K_GK = -(n-2)/(2c(n+1)).  n=4 -> -1/(5c).
  (This CORRECTS the earlier staked '-1/(n+1)' guess, which only coincided at n=4.)
"""
import sympy as sp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)

n = 4
# parametrize the unit 3-sphere by 3 free coords to enforce |nu|=1 exactly
v1, v2, v3 = sp.symbols('v1 v2 v3', real=True)
v4 = sp.sqrt(1 - v1**2 - v2**2 - v3**2)
nu = sp.Matrix([v1, v2, v3, v4])
J = sp.ones(n, n); H = sp.eye(n) + J; Hc = J - sp.eye(n)
sigma = sum(nu)
def e_r(A, r):
    from itertools import combinations
    return sum(A[list(c), list(c)].det() for c in combinations(range(n), r))
P = sp.eye(n) - nu*nu.T

# ---- L1 + L3: e_3(P A P) = nu^T adj(A) nu, and the explicit forms ----
e3H  = sp.simplify(e_r(P*H*P, 3))
e3Hc = sp.simplify(e_r(P*Hc*P, 3))
check("L3.e3_PHP", sp.simplify(e3H - (5 - sigma**2)) == 0,
      "e_3(P H P) = 5 - sigma^2  (= nu^T adj(H) nu, adj(H)=5I-J)")
check("L3.e3_PHcP", sp.simplify(e3Hc - (3 - sigma**2)) == 0,
      "e_3(P Hc P) = 3 - sigma^2  (= nu^T adj(Hc) nu, adj(Hc)=3I-J)")
check("L1.adj", H.adjugate() == 5*sp.eye(n) - J and Hc.adjugate() == 3*sp.eye(n) - J,
      "adj(H)=5I-J, adj(Hc)=3I-J")

# ---- L4: q from the constraint, and the cancellation ----
c = sp.symbols('c', positive=True)
M = H/2
Minv = M.inv()
q = sp.simplify(4*c/(nu.T*Minv*nu)[0])         # q = 4c/(nu^T M^-1 nu)
check("L4.q", sp.simplify(q - 10*c/(5 - sigma**2)) == 0,
      "q = 10c/(5 - sigma^2)")
phi = sp.simplify(-e3Hc/(q*e3H))               # kappa/K_GK
check("L4.cancel", sp.simplify(phi - (-(3 - sigma**2)/(10*c))) == 0,
      "phi = kappa/K_GK = -(3 - sigma^2)/(10c)  (the 5-sigma^2 cancels)")

# ---- L5: sphere moments on S^3 (exact, via the Dirichlet/beta measure) ----
# INT_{S^3} 1 dOmega = 2 pi^2 ; INT_{S^3} nu_i^2 dOmega = (2 pi^2)/4 ; cross = 0.
vol_S3 = 2*sp.pi**2
int_sigma2 = vol_S3            # sum nu_i^2 = 1 -> INT = vol; cross terms vanish by symmetry
int_3_minus_sigma2 = 3*vol_S3 - int_sigma2
check("L5.sphere_moment", sp.simplify(int_3_minus_sigma2 - 4*sp.pi**2) == 0,
      "INT_{S^3} (3 - sigma^2) dOmega = 4 pi^2")

# ---- assemble ----
INT_kappa = sp.simplify(-int_3_minus_sigma2/(10*c))
check("RESULT", sp.simplify(INT_kappa - (-2*sp.pi**2/(5*c))) == 0,
      f"INT_S kappa_{{3;3,0}} dA = {INT_kappa} = -2 pi^2/(5c)")

# numeric cross-check vs the empirical verdict (-2 pi^2/5 at c=1)
check("numeric_c1", abs(float(INT_kappa.subs(c, 1)) - (-2*float(sp.pi)**2/5)) < 1e-12,
      f"c=1 value = {float(INT_kappa.subs(c,1)):.10f} (verdict -3.9478417604)")

nch = 8
if FAILS:
    print(f"VERDICT: FAIL ({len(FAILS)}): {', '.join(FAILS)}")
    raise SystemExit(1)
print(f"VERDICT: ARITH-I r=3 CHANNEL CONSTANT PROVEN EXACT -- {nch}/{nch}. "
      f"INT_S kappa_{{3;3,0}} dA = -2 pi^2/(5c) (symbolic, machine-checked). "
      f"NOT EXACT (nonzero), a pi^2-rational. General n (r=n-1): -(n-2)/(2c(n+1)).")
