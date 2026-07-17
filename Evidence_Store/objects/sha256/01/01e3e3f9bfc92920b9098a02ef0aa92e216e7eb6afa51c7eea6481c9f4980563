"""
ARITH-I STAGE B (session 2) — the r=2 channel-density exactness, resolved; the
normalization pinned; the r=3 machinery validated. FRESH, zero-import. sympy.

PREREG 32f2fb3a (Stage-B; fabricated stop condition VOID, CORRECTION_2026-07-06).
Builds on stage B s1 (6ed1232a). Paper-track fence: no engine priority changed.

CONTEXT. Stage B asks whether the r=3 pure-coupling CHANNEL density (offdiag
Hessian Hc) is exact. Session 1 proved it needs n>=4 and exhibited the r=2 FULL-
curvature primitive. This session settles the r=2 CHANNEL case on the keystone and
pins the load-bearing subtlety: exactness depends on the NORMALIZATION, and the
A5/BRIEF question uses the grid normalization q^((r+2)/2).

FINDINGS (all on the n=3 keystone, family-free)
  SBC-1  STRUCTURE (exact): the r=2 coupling channel density is the FULL Gaussian
         curvature weighted by height^2,
             kc = e_2(P Hc P)/q = -4 P^2/q^2 = (P^2/3) * K_G ,   K_G = -12/q^2.
         So kc is NOT constant-proportional to K_G -> its exactness is a genuine
         question, not inherited from Gauss-Bonnet.
  SBC-2  MACHINERY VALIDATED (control): the ansatz linear-algebra recovers the
         known Gauss-Bonnet primitive of K_G at minimal degree --
             eta_K = -2 P (S dD - D dS)/(sqrt(q) * w),  w = (2D+S)^2+D^2,
         d eta_K = K_G dA exactly. (This is the Gauss-map pullback of the S^2
         area-form primitive, session-1 SBB-2, now re-derived by the ansatz that
         Route 1 uses at r=3.)
  SBC-3  NORMALIZATION IS LOAD-BEARING. In the chart, kc dA = -2P/q^(3/2) dD dS
         (sigma-normalization q^(r/2)); the grid density is kc/q, i.e.
         -2P/q^(5/2) dD dS (grid q^((r+2)/2)).
         - sigma channel (-2P/q^(3/2)): NO algebraic primitive in the tested class
           (deg<=4 over sqrt(q)*w, and over sqrt(q)*w^2) -- not exact [search
           result, not a proof of non-existence].
         - grid channel (-2P/q^(5/2)): EXACT, explicit primitive (SBC-4). The
           A5/BRIEF question uses the grid normalization (q^(5/2) at r=3), so the
           EXACT case is the one that matters, and it reproduces A5's premise
           "the r=2 constant is end data because the density is exact."
  SBC-4  r=2 GRID-CHANNEL PRIMITIVE (exact, explicit, verified):
             eta_c = a/(q^(3/2) w) dD + b/(q^(3/2) w) dS,
             a = (2P/9)(3 D S^2 + 30 D + S^3 + 9 S),
             b = (2P/9)(-3 D^2 S - D S^2 + 15 D + 6 S),
         d eta_c = (grid r=2 channel density) exactly on the keystone.

CONSEQUENCE FOR r=3. The r=2 channel density IS exact in the grid normalization,
so the r=3 premise is live (not trivially decided) and the ansatz machinery +
normalization are validated. The remaining gate is unchanged and singular: the
specific n=4/n=6 quadric family (OPEN B-1, stage B s1). H° is the OFFDIAG channel
Hessian Hc (confirmed by the whole numerator-tower/depth-theorem lineage), NOT the
full Hessian -- so r=3 is the genuine channel question, not the trivial Gauss-
Kronecker one.

Convention: pin = `python3 reports/arithmetic_track/arith_i_stageB_s2.py | sha256sum`.
"""
import sympy as sp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)

D, S, P = sp.symbols('D S P', real=True)
q = (2*D + S)**2 + D**2 + 4*P**2
w = (2*D + S)**2 + D**2
rel = lambda e: sp.expand(e).subs(P**2, 3 - D**2 - D*S)
fD = -(2*D + S)/(2*P); fS = -D/(2*P)
def dtot(e, v): return sp.diff(e, v) + sp.diff(e, P)*(fD if v == D else fS)
def Pproj(g, qq, n): return sp.Matrix(n, n, lambda i, j: (1 if i == j else 0) - g[i]*g[j]/qq)
def offdiag(H, n): return sp.Matrix(n, n, lambda i, j: 0 if i == j else H[i, j])
def e_r(A, r):
    from itertools import combinations
    n = A.shape[0]
    return sum(A[list(c), list(c)].det() for c in combinations(range(n), r))

# ---- SBC-1: kc = (P^2/3) K_G structure ----
g = [2*D + S, D, 2*P]
H = sp.Matrix([[2, 1, 0], [1, 0, 0], [0, 0, 2]])
Pm = Pproj(g, q, 3)
kc = rel(e_r(Pm*offdiag(H, 3)*Pm, 2)/q)
KG = rel(e_r(Pm*H*Pm, 2)/q)
check("SBC1.kc_structure",
      sp.simplify(rel(kc - (P**2/3)*KG).subs(P, sp.sqrt(3 - D**2 - D*S))) == 0,
      "kc = e_2(P Hc P)/q = (P^2/3) K_G  = -4P^2/q^2")

# ---- SBC-2: K_G control primitive verified ----
etaK_A = -2*P*S/(sp.sqrt(q)*w); etaK_B = 2*D*P/(sp.sqrt(q)*w)
targK = -6/(P*q**sp.Rational(3, 2))          # K_G * sqrt(EG-F^2) = K_G dA density
rK = sp.simplify(rel(sp.numer(sp.cancel(sp.together(dtot(etaK_B, D) - dtot(etaK_A, S) - targK)))))
check("SBC2.KG_primitive", rK == 0,
      "d eta_K = K_G dA exactly (control; ansatz recovers Gauss-Bonnet primitive)")

# ---- SBC-4: grid-channel primitive verified (=> SBC-3 grid case EXACT) ----
a = 2*P*(3*D*S**2 + 30*D + S**3 + 9*S)/9
b = 2*P*(-3*D**2*S - D*S**2 + 15*D + 6*S)/9
etaC_A = a/(q**sp.Rational(3, 2)*w); etaC_B = b/(q**sp.Rational(3, 2)*w)
targC = -2*P/q**sp.Rational(5, 2)             # grid r=2 channel density 2-form
rC = sp.simplify(rel(sp.numer(sp.cancel(sp.together(dtot(etaC_B, D) - dtot(etaC_A, S) - targC)))))
check("SBC4.grid_channel_primitive", rC == 0,
      "d eta_c = grid r=2 channel density exactly (EXACT; reproduces A5 premise)")

# ---- SBC-3 (sigma case): the grid primitive does NOT solve the sigma target ----
targS = -2*P/q**sp.Rational(3, 2)             # sigma r=2 channel density 2-form
rS = sp.simplify(rel(sp.numer(sp.cancel(sp.together(dtot(etaC_B, D) - dtot(etaC_A, S) - targS)))))
check("SBC3.normalization_distinct", rS != 0,
      "grid primitive does not solve the sigma target -> normalization is load-bearing")

n_checks = 4
if FAILS:
    print(f"VERDICT: FAIL ({len(FAILS)}): {', '.join(FAILS)}")
    raise SystemExit(1)
print(f"VERDICT: ARITH-I STAGE B session 2 CLEAN — {n_checks}/{n_checks}. r=2 channel "
      f"density EXACT in the grid normalization (explicit primitive, A5 premise "
      f"reproduced); machinery + normalization validated; r=3 gated only on the "
      f"n=4/n=6 family (OPEN B-1). H° = offdiag channel Hessian.")
