# Extraction Note — Role Reduction (Paper I) + Legacy Three-Channel Extension

**Extraction ID prefix:** `ROLE_REDUCTION_LEGACY`
**Extracted:** 2026-07-30, for the theorem-consolidation campaign (ACTIVE_RECHART_CURVATURE_VALUATIONS).
**Scope of this note:** order-2 reduction theorem, continuous gauge orbit, Gauss–Lovelock elevation, legacy channel formulas, tuple-ordering conventions, and cross-document disagreements.
**Rule followed:** all equations verbatim in code blocks (including source typos, which are flagged, never silently repaired).

---

## 1. SOURCE LIST

| # | File | Role |
|---|------|------|
| S1 | `/home/user/Cella_Framework/research/campaigns/ACTIVE_RECHART_CURVATURE_VALUATIONS/01_SOURCES_CORE/paper_I_active_rechart/DBP_Curvature_Role_Reduction.md` | Canonical DRAFT statement of the channel-density tower, order-2 reduction theorem, gauge orbit, kill conditions, and the §14 Riemannian/Gauss–Lovelock elevation. |
| S2 | `/home/user/Cella_Framework/research/campaigns/ACTIVE_RECHART_CURVATURE_VALUATIONS/02_PROOF_SUPPLEMENTS/gauge_reduction/Three_Channel_KG_New_Math_Extension.md` | Legacy mathematical-extension notes: explicit legacy channel formulas (Δ-normalized), r=1 trace channels, generating functions, phase-space normal form, power/Fermat/quadratic families, pure-gauge null direction. No grade tags. |

Referenced but not on the extraction path (existence not verified here): `dbp_curvature_reduction_harness.py`, `dbp_riemannian_checks.py`, `Canonical_Invariant_Reduction_Theorem.md`, the "canonical three-channel specification" that S2 §3 leans on for `Δ_c^{ijk}, Δ_s^{ijk}, Δ_m^{ijk}`.

---

## 2. EXACT STATEMENTS

### 2.1 From S1 (`DBP_Curvature_Role_Reduction.md`)

**[ROLE_REDUCTION_LEGACY-T1] Setup / objects (S1 §1).**
```
g = ∇F(x),   H = ∇²F(x),   q = gᵀg ≠ 0.
```
```
H = H_s + H_c,   H_s = diag(H),   H_c = H − H_s.
```
```
S = −PHP/√q          (shape operator; eigenvalues = principal curvatures, one zero along n).   [+ADDED]
```
with `n = g/√q` (unit normal), `P = I − ggᵀ/q` (tangent projector, `Pg = 0`). Regularity: role/edge results live on `∏ gᵢ ≠ 0`; on `gᵢ = 0` the active output chart "must **refuse**, not divide by zero". Frame: split taken in the **DBP coordinate frame**, not an orthonormal vielbein. `[ANALYTIC]`

**[ROLE_REDUCTION_LEGACY-T2] Channel-density polynomial (S1 §2).**
```
Ĉ_r(t,u) = (−1)^{r+1} Σ_{|I|=r+1}  det [ 0    g_Iᵀ ]
                                       [ g_I  (t·H_c + u·H_s)_I ]
```
`Ĉ_r` homogeneous of degree `r` in `(t,u)`; expansion:
```
Ĉ_r(t,u) = Σ_{p+q=r} t^p u^q · κ̂_{r;p,q}.
```

**[ROLE_REDUCTION_LEGACY-T3] Normalization and canonical invariant (S1 §2).**
```
κ_{r;p,q} = κ̂_{r;p,q} / q^{(r+2)/2}
σ_r       = Σ_{p+q=r} κ_{r;p,q} = Ĉ_r(1,1) / q^{(r+2)/2}.
```

**[ROLE_REDUCTION_LEGACY-T4] Reduction map (S1 §2).**
```
Σ : C_r ↦ Σ κ_{r;p,q} = σ_r,     ker Σ = { δC_r : Σ δκ_{r;p,q} = 0 }.
```
Channel vector: `C_r = (κ_{r;r,0}, …, κ_{r;0,r})`. Boxed caveat verbatim: "**The channel decomposition is not itself an intrinsic scalar invariant.** ... The total is invariant; the channel account is a representative in the affine fiber over it."

**[ROLE_REDUCTION_LEGACY-T5] n=3 specialisation + keystone (S1 §2).**
```
K_G = κ_c + κ_s + κ_int,    ker Σ = {(a,b,c) : a+b+c = 0}.
```
with `C_2 = (κ_c, κ_int, κ_s)` (NOTE the order — see CONVENTIONS). Keystone `F = x₁² + x₁x₂ + x₃² − 3` at `(1,1,1)`:
```
(κ_c, κ_s, κ_int) = (−1/49, 1/49, −3/49),   K_G = −3/49.      [MEASURED]
```

**[ROLE_REDUCTION_LEGACY-T6] Shape-operator grounding + verified anchors (S1 §3).**
σ_r is the r-th elementary symmetric function of S's eigenvalues; `{σ_1,…,σ_{n−1}}` is the complete set of *scalar* curvature invariants ("completeness is the whole tower"). `[ANALYTIC]` Verified anchors (n=3):
```
σ_2·q = e₂(PHP)   and   σ_1·q⁻¹·(−1) = tr(PHP),   i.e.  σ_2 = K_G  and  σ_1 = tr(S).   [MEASURED]
```
(⚠ σ_1 anchor is dimensionally suspect as written — see RED FLAG R1.) Scope caveat: `{σ_r}` exhausts scalars only; principal-direction orientation is outside (lead L1).

**[ROLE_REDUCTION_LEGACY-T7] Parity law (S1 §4).**
```
r even  →  σ_r ∈ ℚ           (rational; even-order curvature)
r odd   →  σ_r ∈ ℚ(√q)       (carries √q; odd-order curvature)
```
`Ĉ_r(1,1)` always rational; √q enters only via `q^{(r+2)/2}`. `[ANALYTIC + MEASURED]` Consequences verbatim include: n=3 `σ_2 = K_G ∈ ℚ`, `σ_1 = 2·mean curvature ∈ ℚ(√q)`; n=4 `σ_2 ∈ ℚ`, `σ_3 ∈ ℚ(√q)`; Cella bridge (`κ²`, `H²` exact because squaring kills √q); "**The parity law is the Lovelock parity.**"

**[ROLE_REDUCTION_LEGACY-T8] Canonical invariant reduction / short exact sequence (S1 §5).**
```
0  →  ker Σ  →  ChannelAccount_r  --Σ-->  InvariantCurvature_r  →  0.
```
```
channel account  =  canonical invariant  +  zero-sum gauge residue.
```

**[ROLE_REDUCTION_LEGACY-T9] Gauge transport law — the continuous gauge orbit (S1 §6).**
Gauge `F̃ = μF`, `μ(x) = 1`, `a = ∇log μ(x)`:
```
g̃ = g,    H̃ = H + gaᵀ + agᵀ.
```
Because `Pg = 0`, `P(gaᵀ + agᵀ)P = 0`; S unchanged, every σ_r preserved, and:
```
C_r(g̃, H̃) − C_r(g, H) ∈ ker Σ      (n=3:  δκ_c + δκ_s + δκ_int = 0).      [MEASURED]
```
"This is the true chart-change action: not scalar change, but zero-sum redistribution of channel account."

**[ROLE_REDUCTION_LEGACY-T10] Passive role permutations trivial (S1 §7).**
```
C_r(P_σ g, P_σ H P_σᵀ) = C_r(g, H).      [MEASURED]
```
Passive Sₙ orbit collapses to a singleton; the nontrivial role action is active recharting.

**[ROLE_REDUCTION_LEGACY-T11] Single-edge coupling corollary, n=3 (S1 §8).**
Weighted coupling-edge vector `ν = (g₁H₂₃, g₂H₁₃, g₃H₁₂)`.
```
Δ_c = νᵀ(2I − 𝟙𝟙ᵀ)ν      — a Lorentzian quadratic form, signature (2,1).
```
```
δκ_c(t·e_i) = 4t · g₁g₂g₃ · H_jk / q²        (H_jk = the coupling edge opposite vertex i)
⟹  t·e_i pins κ_c  ⟺  H_jk = 0.      [PROVEN + MEASURED, 200 surfaces × 3 axes]
```
When the opposite edge vanishes, displacement lies on "the κ_c-null ray `(0,1,−1)` of `ker Σ`" (⚠ tuple order of this ray is ambiguous — see RED FLAG R5); "`∏g = e₃` of the projective normal, so κ_c also goes rigid on the normal-coordinate boundary" (⚠ garbled — RED FLAG R8).

**[ROLE_REDUCTION_LEGACY-T12] Active role recharting → three DBP output charts (S1 §9).**
For a graph `z = h(x,y)`, first jet `(α,β)`, second jet `(L,M,N)`:
```
κ_c = −M²/Q²,   κ_s = LN/Q²,   κ_int = 0,   K_G = (LN−M²)/Q²,   Q = 1+α²+β².
```
```
OutputRoleCurvSpec(f) = {C_P, C_D, C_S}      (input swaps collapse 6 ordered charts → 3 spectra).   [MEASURED]
```
"The implicit (non-graph) representation is a fourth point on the same orbit with `κ_int ≠ 0`. The continuous gauge orbit (§6) is the ambient; the three DBP roles are its three graph-normalization sections."

**[ROLE_REDUCTION_LEGACY-T13] THE ORDER-2 REDUCTION THEOREM — placement in Theorem 8.1′ (S1 §10). Verbatim:**
```
Theorem 8.1′ (orbit/quotient form): a local order-r function φ is a DBP invariant ⟺ φ factors through
the S₃ role-jet orbit 𝔎_r⁺ = Orb_{S₃}(D,S,P, jʳ(⊕)). The orbit is the universal carrier of all local
DBP invariants; coupling-structural invariants are exactly the orbit functions that do NOT descend to
the value-only quotient (D,S,P)/S₃.

This curvature reduction is the order-2 projection of that theorem. At r = 2 the carrier is the orbit
of (g, H) under the role action; its invariant quotient is the shape-operator spectrum {σ_1, …, σ_{n−1}}
(parity-split per §4), and the channel decomposition is a section of the gauge fiber over σ_{n−1}
(and over each σ_r).
```
"The whole §2–§9 structure is 'what Theorem 8.1′ looks like when you read it through second-order curvature.'"

**[ROLE_REDUCTION_LEGACY-T14] Kill conditions KC1–KC8 (S1 §13.1), condensed verbatim heads.**
```
KC1 — gauge invariance:  ∃ (g,H), gauge a, r with sigma_numerator(g, gauge_H(g,H,a), r) ≠ sigma_numerator(g,H,r).
KC2 — zero-sum residue:  ∃ gauge where Σ(C_r(g̃,H̃) − C_r(g,H)) ≠ 0.
KC3 — passive triviality: ∃ permutation that changes channel_vector(g,H,r).
KC4 — shape-operator identity (n=3): σ_2 ≠ channel sum, or σ_2·q ≠ e₂(PHP), or σ_1·q⁻¹ ≠ −tr(PHP).
KC5 — parity / rational numerator: ∃ r with sigma_numerator(g,H,r) ∉ ℚ.
KC6 — single-edge law (n=3): ∃ single-axis gauge with δκ_c(t·e_k) ≠ 4t·∏g·H_opp/q².
KC7 — completeness sanity (soft).
KC8 — ambient nonlinearity wall: fires iff some generic family shows R̄ additive/bilinear in ḡ.
```
(KC4's σ_1 clause inherits RED FLAG R1.)

**[ROLE_REDUCTION_LEGACY-T15] Gauss equation + tensor-level channel split (S1 §14.1) `[PROVEN + MEASURED]`.**
```
R^Σ = R̄ᵀ + S∧S,    (S∧S)(X,Y,Z,W) = ⟨SX,Z⟩⟨SY,W⟩ − ⟨SX,W⟩⟨SY,Z⟩.
```
```
S∧S = R_cc + R_int + R_ss,    R_cc = S_c∧S_c,  R_ss = S_s∧S_s,  R_int = S_c∧S_s + S_s∧S_c.
```
"The reduction is therefore **not scalar-confined**" — verified on all 81 tangent 4-tuples of a dim-3 hypersurface (check A1).

**[ROLE_REDUCTION_LEGACY-T16] Gauss–Lovelock scalar tower (S1 §14.2).**
Universal scalar law, every dimension m:
```
Scal_Σ = Scal̄ − 2 Ric̄(ν,ν) + 2 σ₂(S),     2σ₂(S) = (tr S)² − tr(S²) = 2(κ_c + κ_int + κ_s).
```
m=2 shadow (the Euclidean surface law):
```
K_Σ = K̄(TΣ) + κ_c + κ_s + κ_int.      ← the Euclidean statement, now one shadow of the tower.
```
Lovelock elevation, ANY ambient:
```
L_k^Σ = L_k(R̄ᵀ) + Σ_{j=1}^k Σ_{p+q=2j} Λ_{k,j;p,q}        (exact channel decomposition, ANY ambient).
```
Space-form collapse (`R̄ᵀ = c·(g∧g)`):
```
L_k^Σ = C(m,2k)(2k)! Σ_{j=0}^k C(k,j) c^{k−j} σ_{2j}(S)/C(m,2j),    σ_{2j} = Σ_{p+q=2j} κ_{2j;p,q}.
```
```
k=1: Scal_Σ = m(m−1)c + 2σ₂.
k=2: L₂ = m(m−1)(m−2)(m−3)c² + 4(m−2)(m−3)c·σ₂ + 24σ₄.
Flat (c=0): L_k^Σ = (2k)!·σ_{2k}.
```
Grade verbatim: `[k=1,2 coefficients checked by hand against the contracted Gauss equation; σ₄ channelisation MEASURED on Σ⁴⊂ℝ⁵, exact-ℚ — check A3]`. (Extractor note: I re-derived the k=1,2 coefficients from the C(m,2k) formula; they are internally consistent.)

**[ROLE_REDUCTION_LEGACY-T17] Exactness is a rational-metric property (S1 §14.3) `[PROVEN + MEASURED]`.**
`K_G = det(II)/det(I)` in a rational tangent frame stays in ℚ for any rational metric — `ḡ ≠ I` gives `K_G = −9/169` (≠ Euclidean −3/49); curved-ambient example:
```
ds² = dx² + (1+x²/2)² dy²   →   K = −2/3,  no √ anywhere.
```
"The √ enters **only** via orthonormalisation (the vielbein, a √ of ḡ) and the odd-order normalisation." Extended parity: "even-order curvature — intrinsic *and* ambient — lies in ℚ for a rational metric... **The §4 parity law IS the Lovelock parity.**" `[ANALYTIC + MEASURED]`

**[ROLE_REDUCTION_LEGACY-T18] The ambient does not channelise — proven boundary (S1 §14.4).**
R̄ is nonlinear in the metric (`Γ ~ ḡ⁻¹∂ḡ`, `R̄ ~ ∂Γ + ΓΓ`) ⟹ no *bilinear* self/coupling/interaction partition of the ambient. Honest general statement:
```
intrinsic curvature  =  ambient (input; exact-ℚ; irreducible by nonlinearity)
                      +  extrinsic (fully channelised — tensor §14.1, Lovelock scalars §14.2; exact-ℚ on even rungs §14.3).
```
Guarded by KC8 (currently holds: `R[A+B] ≠ R[A]+R[B]`).

**[ROLE_REDUCTION_LEGACY-T19] L5 resolved — channels are genuine DBP invariants (S1 §14.5) `[MEASURED + ANALYTIC]`.**
Full O(n) is not a symmetry of a DBP system; actual symmetry group is S₃ role permutations + signs. Verified numbers: generic rational `R ∈ O(3)` keeps `σ₂ = −3/49` and σ₁'s numerator while channels move to
```
(−961, −3627, 2713)/30625   (still summing to −3/49)
```
"the DBP coordinate frame is the physical section, not a canonicalising one."

**[ROLE_REDUCTION_LEGACY-T20] Reference implementation core (S1 §11), verbatim signature-level:**
```python
def channel_density(g, H, r, t, u):   # (−1)^{r+1} Σ_{|I|=r+1} det(bordered (t·H_c+u·H_s)_I)
def q_of(g):              return sum(x*x for x in g)
def sigma_numerator(g,H,r): return channel_density(g, H, r, Q(1), Q(1))   # σ_r = this / q^((r+2)/2)
def channel_vector(g,H,r):  # κ̂_{r;p,q} via Vandermonde solve on nodes s=0..r, y_s = Ĉ_r(s,1)
def gauge_H(g,H,a):       return [[H[i][j]+g[i]*a[j]+a[i]*g[j] ...]]
```
Vandermonde recovery of the channel vector "works for any n, r".

### 2.2 From S2 (`Three_Channel_KG_New_Math_Extension.md`) — legacy formulas

**[ROLE_REDUCTION_LEGACY-T21] Legacy Δ-normalized channel definitions (S2 header).**
```
K_G = κ_c + κ_s + κ_int,    κ_c = −Δ_c/q²,   κ_s = −Δ_s/q²,   κ_int = −Δ_m/q².
```
with `H = H_c + H_s`, `H_s = diag(H)`, `H_c = H − H_s`, `g = ∇F`, `q = gᵀg`. NOTE: `Δ_m` is the legacy name for the interaction determinant (m = "mixed"); the Δ_* determinant definitions themselves are NOT restated in S2 — they are inherited from the external "canonical spec" (RED FLAG R7).

**[ROLE_REDUCTION_LEGACY-T22] σ_r generating definition (S2 §1).**
```
det(I+zS) = Σ_{r=0}^{m} z^r σ_r(S),   σ_0 = 1,   m = n−1.
```
σ_1 = tr S, σ_m = Gaussian-Kronecker.

**[ROLE_REDUCTION_LEGACY-T23] Bordered-minor lift (S2 §1) — S2's counterpart of T2/T3.**
```
E_r(t,u) = (−1)^{r+1} Σ_{|I|=r+1} det( 0    g_Iᵀ )
                                      ( g_I  (tH_c+uH_s)_I )

σ_r(S) = E_r(1,1) / q^{(r+2)/2}

σ_{r;p,q} = [t^p u^q] E_r(t,u) / q^{(r+2)/2},   p+q = r

σ_r(S) = Σ_{p+q=r} σ_{r;p,q}.
```
(S2 writes `𝓔_r`; identical to S1's `Ĉ_r` up to symbol. Presented boxed as universal with no grade tag — RED FLAG R6.)

**[ROLE_REDUCTION_LEGACY-T24] Density parity law (S2 §1).**
```
r even  →  σ_{r;p,q} ∈ ℚ
r odd   →  σ_{r;p,q} ∈ ℚ/√q,  unless q is a rational square.

σ̂_{r;p,q} := [t^p u^q] E_r(t,u) ∈ ℚ      (the universally exact curvature density).
```
(Notation `ℚ/√q` vs S1's `ℚ(√q)` — RED FLAG R4. The "unless q is a rational square" refinement is unique to S2.)

**[ROLE_REDUCTION_LEGACY-T25] r=1 channelized mean/trace curvature (S2 §2) — UNIQUE.**
```
τ_c = 2Σ_{i<j} g_i g_j H_{ij} / q^{3/2} = gᵀH_c g / q^{3/2}

τ_s = (gᵀH_s g − q·tr(H_s)) / q^{3/2} = −Σ_i (q − g_i²) H_{ii} / q^{3/2}

tr S = τ_c + τ_s

H_mean = (τ_c + τ_s)/(n−1)

τ̂_c = 2Σ_{i<j} g_i g_j H_{ij},    τ̂_s = gᵀH_s g − q·tr(H_s)      (exact rational densities)
```
(Extractor re-derivation from S = −PHP/√q confirms both τ formulas.)

**[ROLE_REDUCTION_LEGACY-T26] Triple-kernel σ₂ for all n (S2 §3) — UNIQUE.**
```
σ_{2,c}   = −Σ_{i<j<k} Δ_c^{ijk} / q²
σ_{2,s}   = −Σ_{i<j<k} Δ_s^{ijk} / q²
σ_{2,int} = −Σ_{i<j<k} Δ_m^{ijk} / q²
```
"the existing n=3 K_G channel formula ... is the atomic triple formula for the second elementary curvature in any ambient dimension." n=3: σ₂=K_G; n=4: σ₂ = k₁k₂+k₁k₃+k₂k₃; all r=2 channels exact in ℚ.

**[ROLE_REDUCTION_LEGACY-T27] Gauss–Kronecker generating polynomial, any n (S2 §4) — UNIQUE.**
```
𝒦(t,u) = (−1)^n det( 0   gᵀ )
                    ( g   tH_c + uH_s )

K_{GK;p,q} = [t^p u^q] 𝒦(t,u) / q^{(n+1)/2},   p+q = n−1
```
n=3 identification:
```
K_{GK;2,0} = κ_c,   K_{GK;1,1} = κ_int,   K_{GK;0,2} = κ_s.
```
n=4:
```
K_GK = K_{3,0} + K_{2,1} + K_{1,2} + K_{0,3};   exact-ℚ object is K̂_{p,q} = [t^p u^q] 𝒦(t,u)   (q^{5/2} denominator).
```

**[ROLE_REDUCTION_LEGACY-T28] Curvature fingerprint polynomial (S2 §5) — UNIQUE.**
```
χ(z;t,u) = det(I + z(tS_c + uS_s)) = Σ_{r=0}^{n−1} z^r Σ_{p+q=r} t^p u^q σ_{r;p,q}.
```
n=3:
```
χ = 1 + z(tτ_c + uτ_s) + z²(t²κ_c + tu·κ_int + u²κ_s).
```
n=4:
```
χ = 1 + z(tσ_{1;c} + uσ_{1;s}) + z²(t²σ_{2;2,0} + tu·σ_{2;1,1} + u²σ_{2;0,2})
      + z³(t³K_{3,0} + t²u·K_{2,1} + tu²K_{1,2} + u³K_{0,3}).
```

**[ROLE_REDUCTION_LEGACY-T29] Power traces of the split shape operator (S2 §6) — UNIQUE.** `A = S_c`, `B = S_s`, `P_k(t,u) = tr(tA+uB)^k`:
```
P_1 = t·trA + u·trB.
P_2 = t²·trA² + 2tu·tr(AB) + u²·trB².
P_3 = t³·trA³ + 3t²u·tr(A²B) + 3tu²·tr(AB²) + u³·trB³.
P_4 = t⁴·trA⁴ + 4t³u·tr(A³B) + 4tu³·tr(AB³) + u⁴·trB⁴ + 4t²u²·tr(A²B²) + 2t²u²·tr(ABAB).
```

**[ROLE_REDUCTION_LEGACY-T30] Newton-identity GK channel pieces, n=4 (S2 §6) — UNIQUE.** With `a₁=trA, b₁=trB, a₂=trA², b₂=trB², c=tr(AB), a₃=trA³, b₃=trB³, d=tr(A²B), e=tr(AB²)`:
```
K_{3,0} = (a₁³ − 3a₁a₂ + 2a₃)/6
K_{2,1} = (a₁²b₁ − 2a₁c − b₁a₂ + 2d)/2
K_{1,2} = (a₁b₁² − a₁b₂ − 2b₁c + 2e)/2
K_{0,3} = (b₁³ − 3b₁b₂ + 2b₃)/6.
```

**[ROLE_REDUCTION_LEGACY-T31] Ambient trace formula for channel words (S2 §7) — UNIQUE.**
```
tr(S_{X₁}···S_{X_k}) = (−1)^k q^{−k/2} tr(P H_{X₁} P H_{X₂} ··· P H_{X_k} P),   X_i ∈ {c,s},  P = I − ggᵀ/q.
```
Even k → rational; odd k → ℚ/√q unless density-scaled.

**[ROLE_REDUCTION_LEGACY-T32] 3D phase-space normal form (S2 §8) — UNIQUE.** Assume `g₁g₂g₃ ≠ 0`. Coupling vector (boxed as `u` in source, used as `ν` — RED FLAG R3):
```
ν = (g₁H₂₃, g₂H₁₃, g₃H₁₂)

w = ( (g₂g₃/g₁)H₁₁, (g₁g₃/g₂)H₂₂, (g₁g₂/g₃)H₃₃ )

Δ_c = 2‖ν‖² − (𝟙·ν)²
Δ_s = ½‖w‖² − ½(𝟙·w)² = −(w₁w₂ + w₁w₃ + w₂w₃)
Δ_m = 2ν·w
```
Pure coupling metric `2I − J`, eigenvalues `2, 2, −1` (Lorentzian):
```
Δ_c > 0: spacelike coupling, κ_c < 0
Δ_c = 0: lightlike coupling, κ_c = 0 despite possible nonzero coupling Hessian
Δ_c < 0: timelike coupling, κ_c > 0
```
Retrodiction readings: open chain = lightlike (κ_c=0); closed triangle = timelike (κ_c>0); saddle = spacelike (κ_c<0).

**[ROLE_REDUCTION_LEGACY-T33] Total determinant numerator + completed square (S2 §8) — UNIQUE.** Verbatim including source corruption (`rac12` = broken `\frac12`, i.e. ½ — RED FLAG R2):
```
Δ = Δ_c + Δ_s + Δ_m = 2‖ν‖² − (𝟙·ν)² + ½‖w‖² − rac12(𝟙·w)² + 2ν·w

Δ = ½‖2ν + w‖² − (𝟙·ν)² − rac12(𝟙·w)²
```
Curvature channels are `−Δ_*/q²`.

**[ROLE_REDUCTION_LEGACY-T34] Keystone in phase-space form (S2 §8) — UNIQUE data.**
```
F = x₁² + x₁x₂ + x₃² − 3  at (1,1,1):
g = (3,1,2),  q = 14,  ν = (0,0,2),  w = (4/3, 0, 3)
Δ_c = 4,  Δ_s = −4,  Δ_m = 12
κ_c = −1/49,  κ_s = +1/49,  κ_int = −3/49,  K_G = −3/49.
```
"exact cancellation of the Lorentzian coupling and self quadratic forms, leaving only the bilinear interaction pairing." (Extractor verified every number; agrees exactly with S1 keystone T5.)

**[ROLE_REDUCTION_LEGACY-T35] Pure-gauge channels + gauge-null direction (S2 §9) — UNIQUE.** For pure gauge Hessian `H = G = gaᵀ + agᵀ` in ℝ³:
```
Δ_c = Δ_s = −4g₁g₂g₃(a₁a₂g₃ + a₁a₃g₂ + a₂a₃g₁)
Δ_m       = +8g₁g₂g₃(a₁a₂g₃ + a₁a₃g₂ + a₂a₃g₁)
Δ_c + Δ_s + Δ_m = 0

(κ_c, κ_s, κ_int) = λ(1,1,−2)      — the gauge-null channel direction.
```
Consequences verbatim (numbered 1–4), incl. #4: gauge-invariant channel diagnostics require splitting AFTER projecting to `B = PHP` — "a different object ... not be mixed with the canonical keystone channels without an explicit mode label." Closing: "This is not a defect; it is an account law."

**[ROLE_REDUCTION_LEGACY-T36] Sensitivity gradients in phase coordinates (S2 §10) — UNIQUE.**
```
∇_ν Δ_c = 4ν − 2(𝟙·ν)𝟙,    ∇_w Δ_s = w − (𝟙·w)𝟙
∇_ν Δ_m = 2w,               ∇_w Δ_m = 2ν.
```

**[ROLE_REDUCTION_LEGACY-T37] Monomial hypersurface family (S2 §11) — UNIQUE.** `F = x^a y^b z^c − 1` on F=0, `q = (a/x)² + (b/y)² + (c/z)²`:
```
κ_c   =  3a²b²c² / (x²y²z²q²)
κ_s   =  abc(3abc − 2ab − 2ac − 2bc + a + b + c) / (x²y²z²q²)
κ_int = −2abc(3abc − ab − ac − bc) / (x²y²z²q²)
K_G   =  abc(a+b+c) / (x²y²z²q²)
```
At (1,1,1): `q = a²+b²+c²`, `K_G = abc(a+b+c)/(a²+b²+c²)²`. Cases:
```
a=b=c=1:      K_G = 1/3,  κ_c = 1/3,  κ_s = 0,  κ_int = 0.
a=2,b=1,c=1:  K_G = 2/9,  κ_c = 1/3,  κ_s = 0,  κ_int = −1/9.
```
(Extractor verified both cases against the closed forms; consistent, including κ_c>0 via timelike ν ∝ (1,1,1).)

**[ROLE_REDUCTION_LEGACY-T38] Additive Fermat-type surfaces (S2 §12) — UNIQUE.** `F = Ax^a + By^b + Cz^c − D`:
```
κ_c = 0,   κ_int = 0,   K_G = κ_s

K_G = ( g_x²H_yy H_zz + g_y²H_xx H_zz + g_z²H_xx H_yy ) / (g_x² + g_y² + g_z²)²
```
with `g_x = Aa x^{a−1}`, `H_xx = Aa(a−1)x^{a−2}` (and cyclic).

**[ROLE_REDUCTION_LEGACY-T39] Quadratic mixed surfaces classifier (S2 §13) — UNIQUE.** `F = ax² + by² + cz² + 2fxy + 2exz + 2dyz − C`, so `H₁₁=2a, H₂₂=2b, H₃₃=2c, H₁₂=2f, H₁₃=2e, H₂₃=2d`; wherever `g₁g₂g₃ ≠ 0`:
```
ν = (2dg₁, 2eg₂, 2fg₃),    w = ( 2ag₂g₃/g₁, 2bg₁g₃/g₂, 2cg₁g₂/g₃ )
Δ_c = 2‖ν‖² − (𝟙·ν)²,   Δ_s = ½‖w‖² − rac12(𝟙·w)²,   Δ_m = 2ν·w      [rac12 corruption again]
```

**[ROLE_REDUCTION_LEGACY-T40] Channel barycentric ratios (S2 §14) — UNIQUE.** When `K_G ≠ 0`:
```
R_c = κ_c/K_G,   R_s = κ_s/K_G,   R_int = κ_int/K_G,   R_c + R_s + R_int = 1.
Keystone: (R_c, R_s, R_int) = (1/3, −1/3, 1).
```
"the interaction channel contributes 100% of the final curvature after pure coupling and pure self cancel each other exactly."

**[ROLE_REDUCTION_LEGACY-T41] ChannelSpectrum carrier target (S2 §15) — UNIQUE.**
```
Channel geometry = { σ_{r;p,q} : 1 ≤ r ≤ n−1,  p+q = r }

ChannelSpectrum(r, p, q, σ̂_{r;p,q}, q, parity, normalization, provenance).
```
n=3 specialization: trace/mean channels (τ_c, τ_s); Gaussian channels (κ_c, κ_s, κ_int); power traces P_k(t,u) "reducible by Cayley-Hamilton after k=2."

---

## 3. CONVENTIONS

**C1 — Hessian split.** `H_s = diag(H)`, `H_c = H − H_s`. S1 writes `H = H_s + H_c`; S2 writes `H = H_c + H_s` (same object, cosmetic order).

**C2 — Shape operator sign.** `S = −PHP/√q` (S1 §1; S2 §7 consistent via `(−1)^k q^{−k/2}`). Eigenvalues = principal curvatures; one structural zero along the normal.

**C3 — Bordered-minor sign.** Global prefactor `(−1)^{r+1}` on the size-(r+1) bordered minors (S1 `Ĉ_r` = S2 `𝓔_r`); GK special case r = n−1 gives `(−1)^n` (S2 §4). Consistent across both docs.

**C4 — Normalization.** Channel and total normalizer is `q^{(r+2)/2}` (both docs). r=2 in any n: `q²`. GK in ambient n: `q^{(n+1)/2}`. Legacy n=3 form: `κ_* = −Δ_*/q²` (the minus sign lives in the Δ→κ conversion, S2; equal to the bordered-minor values, S1).

**C5 — TUPLE ORDERS FOUND (conversion target: canonical `(σ₂; κ_c, κ_int, κ_s)`).**
- S1 §2 channel vector: `C_2 = (κ_c, κ_int, κ_s)` — already canonical channel order `(p,q) = (2,0),(1,1),(0,2)`.
- S1 §2 keystone and S2 §9/§14: legacy triple `(κ_c, κ_s, κ_int)` — swap last two entries to canonicalize.
- S2 §8 keystone box lists in order `κ_c, κ_s, κ_int, K_G` (total LAST); the campaign's stated legacy order `(K, kc, ks, kint)` (total FIRST) appears in NEITHER document verbatim — the legacy order actually attested here is `(κ_c, κ_s, κ_int)` with `K_G` written separately (usually last). Any consolidation pass must normalize BOTH legacy variants to `(σ₂; κ_c, κ_int, κ_s)`.
- S2 ratio tuple `(R_c, R_s, R_int)` also uses the (c, s, int) legacy order.
- S2 GK grid order is `(p,q)` descending in p: `K_{3,0}, K_{2,1}, K_{1,2}, K_{0,3}` — matches canonical channel-vector order (coupling-power first).
- Conversion rule: legacy `(K, κ_c, κ_s, κ_int)` or `(κ_c, κ_s, κ_int, K)` → canonical `(σ₂; κ_c, κ_int, κ_s)` with `σ₂ ≡ K_G`; components map identity on κ_c, swap κ_s ↔ κ_int positions 2↔3.

**C6 — Symbol synonyms.** `Ĉ_r ≡ 𝓔_r`; `κ̂_{r;p,q} ≡ σ̂_{r;p,q}` (densities); `κ_{r;p,q} ≡ σ_{r;p,q}`; `Δ_m ≡` interaction determinant (`Δ_int` never used); `K_G ≡ σ₂` (n=3) `≡ σ_{n−1} = K_GK` only when n=3; S2 `𝒦(t,u)` = GK generating polynomial; S1 `ν` (§8) = S2 `ν` (=boxed `u`, §8); `t` multiplies the COUPLING part, `u` multiplies the SELF part, in both docs.

**C7 — Parity / number-field.** Numerators/densities always ∈ ℚ for rational (g,H). Even r → σ ∈ ℚ; odd r → S1 says `ℚ(√q)`, S2 says `ℚ/√q` (sharper: rational multiple of 1/√q) with the exception "unless q is a rational square". Cella exactness gates must test densities (or even rungs), not odd normalized curvatures.

**C8 — Frame doctrine.** Split is taken in the DBP coordinate frame; O(n)/vielbein orthonormalisation is NOT a DBP symmetry (S1 §14.5); actual symmetry group: S₃ role permutations + signs. Gauge action on channels is zero-sum (ker Σ); pure-gauge direction in legacy (c,s,int) order is `(1,1,−2)` (S2 §9), which in canonical (κ_c, κ_int, κ_s) order reads `(1,−2,1)`.

**C9 — Regularity/refusal.** Role/edge results require `∏gᵢ ≠ 0`; on `gᵢ = 0` the object must refuse (typed stratum), not divide by zero. S2 §8/§13 formulas assume `g₁g₂g₃ ≠ 0` explicitly.

---

## 4. UNIQUE MATERIAL (must not be lost)

**Only in S1:**
- U1: The order-2 reduction theorem statement itself — curvature reduction as the r=2 projection of Theorem 8.1′ (T13). This is the campaign's central claim; it exists nowhere in S2.
- U2: Continuous gauge orbit picture: 3 graph-chart sections (κ_int = 0) + implicit 4th point; `OutputRoleCurvSpec`, 6→3 collapse (T12).
- U3: Single-edge pinning law `δκ_c(t·e_i) = 4t·g₁g₂g₃·H_jk/q²` and the pin ⟺ opposite-edge-vanishes criterion (T11).
- U4: Entire §14 Gauss–Lovelock elevation: tensor-level split of S∧S (T15), Lovelock tower + space-form collapse with explicit C(m,2k) coefficients (T16), rational-metric exactness incl. `−9/169` and `K = −2/3` witnesses (T17), the ambient non-channelisation wall + KC8 (T18), L5 resolution with the O(3)-rotation witness `(−961, −3627, 2713)/30625` (T19).
- U5: Kill conditions KC1–KC8, variation-space protocol, leads L1–L4, L6, L7, and the §15 honest-scope list (incl. the admission that the general-(n,r) bordered-minor identity is only MEASURED for n=3, r=1,2).
- U6: Grade-tag discipline and verification-record table (§12).
- U7: Short-exact-sequence formulation (T8) and the parity=Lovelock identification (T7/T17).

**Only in S2:**
- U8: r=1 channelized mean curvature: τ_c, τ_s closed forms, H_mean, and densities (T25). S1 never gives explicit r=1 channel formulas.
- U9: Triple-kernel formula: n=3 Δ-partition as the atomic kernel for σ₂ in ALL ambient dimensions (T26).
- U10: GK generating polynomial 𝒦(t,u) closed form and the n=4 four-piece grid (T27).
- U11: Fingerprint polynomial χ(z;t,u) — the whole-tower generating function (T28).
- U12: Power traces P₁–P₄ with the noncommutative `tr(ABAB)` term, and Newton-identity closed forms K_{3,0..0,3} (T29, T30).
- U13: Basis-free ambient trace formula for arbitrary channel words (T31).
- U14: Phase-space normal form (ν, w), Lorentzian classification (spacelike/lightlike/timelike ↔ sign of κ_c), retrodiction explanations, completed-square Δ, keystone phase data ν=(0,0,2), w=(4/3,0,3) (T32–T34).
- U15: Pure-gauge channel determinants and the gauge-null direction λ(1,1,−2); the "split after projection B = PHP is a different object, needs a mode label" warning (T35).
- U16: Sensitivity gradients (T36); monomial family closed forms (T37); Fermat-type reduction (T38); quadratic-mixed classifier (T39); barycentric ratios R_* with keystone (1/3, −1/3, 1) (T40); ChannelSpectrum carrier spec (T41).
- U17: The parity exception clause "unless q is a rational square" (T24) — S1 only gestures at this locus in §13.2.

---

## 5. RED FLAGS

- **R1 — σ₁ anchor formula is inconsistent as written (S1 §3 and KC4).** `σ_1·q⁻¹·(−1) = tr(PHP)` cannot hold for the NORMALIZED σ₁: from `S = −PHP/√q`, `σ_1 = tr S = −tr(PHP)/√q`, so the correct normalized anchor is `σ_1·√q = −tr(PHP)`. The formula as written is correct only if σ₁ there denotes the NUMERATOR `Ĉ_1(1,1) = σ_1·q^{3/2}` (then `Ĉ_1(1,1)/q = −tr(PHP)` holds). But the σ₂ anchor in the same line (`σ_2·q = e₂(PHP)`) uses the normalized σ₂. The line mixes normalized and numerator conventions; KC4 inherits the same defect, so the kill condition as literally coded would misfire or vacuously pass depending on which σ₁ the harness computes. S2 §7 (k=1 case) gives the correct relation. MUST be repaired in consolidation.
- **R2 — LaTeX corruption in S2.** Three occurrences of `rac12` (broken `\frac12`) at the total-Δ formula, the completed square (S2 §8), and the quadratic classifier (S2 §13). Intended value ½ is recoverable from the duplicate correct occurrences (`\frac12‖w‖²...` in §8/§10), but the source is byte-corrupted.
- **R3 — Variable-name collision in S2 §8.** The coupling vector is boxed as `u = (g₁H₂₃, g₂H₁₃, g₃H₁₂)` but every subsequent formula uses `ν`; `u` also collides with the channel-generating variable `u` in E_r(t,u). Consolidation should use ν exclusively (matching S1 §8).
- **R4 — Number-field notation disagreement.** S1: odd σ_r ∈ `ℚ(√q)` (field extension). S2: odd σ_{r;p,q} ∈ `ℚ/√q` (coset `(1/√q)·ℚ`), plus the square-q exception. S2's is the sharper true statement (odd σ is always a rational multiple of 1/√q); S1's is a weaker superset. Not a contradiction, but a precision mismatch to canonicalize (recommend S2's characterization stated inside S1's field).
- **R5 — Internal tuple-order inconsistency in S1.** §2 defines `C_2 = (κ_c, κ_int, κ_s)` (canonical) but the keystone one line later is reported as `(κ_c, κ_s, κ_int) = (−1/49, 1/49, −3/49)` (legacy order). §8's "κ_c-null ray (0,1,−1) of ker Σ" does not say which order it is in (in canonical C₂ order it means δκ_int = −δκ_s; same conclusion in legacy order by coincidence of the leading 0, which is exactly why the ambiguity has gone unnoticed). All tuples must be restated in `(σ₂; κ_c, κ_int, κ_s)`.
- **R6 — Universality asserted without grade in S2.** S2 boxes `σ_r(S) = E_r(1,1)/q^{(r+2)/2}` and the fingerprint identity `χ(z;t,u)` (T23, T28) as established for all (n,r), with no grade tags anywhere in the document. S1 §15 gap 2 explicitly admits the general-(n,r) shape-operator identity is `[MEASURED]` only for n=3, r=1,2 and `[ANALYTIC]` (standard bordered-minor theory) otherwise, with exact-ℚ checks blocked in odd ranks. S2's χ identity additionally assumes e_r(tS_c+uS_s) matches the bordered channel pieces for all (t,u) — plausible by the same bordered-minor argument applied to tH_c+uH_s, but nowhere proved or measured in either document. Consolidated statement must carry S1's honest grade, not S2's boxed confidence.
- **R7 — Dangling definitions in S2.** §Header and §3 use `Δ_c, Δ_s, Δ_m` and `Δ_c^{ijk}, Δ_s^{ijk}, Δ_m^{ijk}` ("the canonical 3D determinant partition") without defining them — they are inherited from an external "canonical spec" not in this pair of files. The phase-space forms (T32) define them only on the `g₁g₂g₃ ≠ 0` locus. Consolidation must import the determinant-level definitions from the canonical spec or derive them from T2's bordered minors.
- **R8 — Garbled sentence in S1 §8.** "`∏g = e₃` of the projective normal, so κ_c also goes rigid on the normal-coordinate boundary" — as written this is not parseable (∏g is presumably e₃ of the normal components g_i, tying the δκ_c prefactor to the normal-coordinate boundary). Needs authorial repair; do not propagate verbatim into the canonical statement.
- **R9 — Scope drift risk on "PROVEN" tags.** S1 header says nothing is canonical until sign-off, yet §8 carries `[PROVEN + MEASURED]` and §14.1/§14.3 carry `[PROVEN]`. §14.1 bilinearity is genuinely elementary, but §14.3's "K_G stays in ℚ for any rational metric" is asserted from two witnesses (−9/169, −2/3) plus the rationality-of-Christoffels argument; the argument is sound but the PROVEN tag on the general claim exceeds the two exhibited checks. Flag for the grade audit, not necessarily wrong.
- **R10 — S2 gauge computation is the pure-gauge point, not the general transport.** T35's `Δ_c = Δ_s`, `Δ_m = −2Δ_c` and direction (1,1,−2) hold for `H = G` exactly (quadratic in a); the general gauge shift of a channel account at H ≠ 0 contains H–G cross terms (S1's KC6 linear law is that cross term; extractor re-derived δκ_c(t·e₁) = +4t·g₁g₂g₃H₂₃/q² from T32's quadratic form — it agrees with S1 exactly, and the quadratic term vanishes identically for single-axis gauges). The two documents are consistent, but neither states the FULL finite gauge displacement decomposition (linear cross term along edge-dependent directions + pure-gauge (1,1,−2) term); the consolidated theorem should.
- **R11 — Keystone consistency confirmed (anti-flag, for the record).** Independent recomputation of the keystone from F = x₁²+x₁x₂+x₃²−3 confirms g=(3,1,2), q=14, ν=(0,0,2), w=(4/3,0,3), (Δ_c,Δ_s,Δ_m)=(4,−4,12), (κ_c,κ_s,κ_int)=(−1/49,1/49,−3/49), K_G=−3/49 in BOTH documents, and the monomial cases of T37 check out. The two sources agree on all shared numerics.
