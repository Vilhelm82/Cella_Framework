# DBP Curvature Role Reduction — Canonical Statement + Stress-Test Brief

**Status:** DRAFT for adversarial stress-testing. Not canonical until signed off.
**Provenance:** merge of `Canonical_Invariant_Reduction_Theorem.md` (the channel-density tower)
with three additions carried over from the role-reduction derivation (`[+ADDED]`), plus a **Riemannian / Gauss–Lovelock elevation (§14)** that subsumes the Euclidean surface statement as a special case and four engine-verified attack results folded throughout.
**Verification substrate:** `dbp_curvature_reduction_harness.py` (exact-ℚ, stdlib-only; retrodiction gate **CLEAN**, invariant sweep upheld n=3,4,5) **+ `dbp_riemannian_checks.py`** (the §14 elevation gate: A1 tensor channelisation, A2 rational-metric exactness, A3 σ₄/parity, **KC8** ambient-nonlinearity wall — **CLEAN**).
**Grade tags:** `[PROVEN]` analytic, `[MEASURED]` exact-ℚ on engine, `[ANALYTIC]` derived but not exhaustively run, `[OPEN]` conjecture/lead.

---

## §0. Mission for CC

This document is one self-contained theorem plus a runnable substrate. Two jobs:

1. **Stress-test the lot.** Run **both** retrodiction gates first — `dbp_curvature_reduction_harness.py` and `dbp_riemannian_checks.py` (the §14 elevation gate, **KC8** armed) — both must stay clean. Then attack every boxed claim with exact-ℚ variations — dimensions, ranks, degeneracies, gauge directions, edge structures, **and curved/space-form ambients**. The **kill conditions** (§13) are armed and falsifiable: a single exact-ℚ counterexample to any of them breaks the theorem, and that is a win, not a failure. Report counterexamples with the exact (g, H) and the offending quantity.
2. **Hunt for structural upgrades by exhaustive variation.** §13.3 lists the open leads (L5 is now **resolved**, §14.5) — places where the structure may be richer than stated: orientation dof (L1), odd-order √q diagnostic (L2), higher jets (L3), the κ_{r;p,q} grid for n≥4 (L4), the Lorentzian signature for general (n,r) (L6), singular-strata typing (L7). Vary widely and look for invariants, recursions, or vanishing patterns not yet named. **KC8 is also a hunting ground:** if any generic metric family makes the ambient `R̄` additive/bilinear in ḡ, that breaches the §14.4 wall and is a genuine discovery.

Discipline: exact ℚ only (no floats, no tolerances), byte-stable, frozen pre-registration before any sweep, every claim grade-tagged. Nothing here is canonical until Will signs off.

---

## §1. Setup

Let `F : ℝⁿ → ℝ` define a smooth hypersurface `F = 0` at a regular point `x`, with

```
g = ∇F(x),   H = ∇²F(x),   q = gᵀg ≠ 0.
```

Fix a coordinate basis and split the Hessian into **self** and **coupling** parts:

```
H = H_s + H_c,   H_s = diag(H),   H_c = H − H_s.
```

Write `n = g/√q` (unit normal), `P = I − ggᵀ/q` (tangent projector, `Pg = 0`), and

```
S = −PHP/√q          (shape operator; eigenvalues = principal curvatures, one zero along n).   [+ADDED]
```

**Regularity (well-posedness).** Everything below lives on the regular locus `∏ gᵢ ≠ 0` for the role/edge results; on `gᵢ = 0` (a normal coordinate vanishes) the corresponding active output chart does not exist and the object must **refuse**, not divide by zero (see §13.3, lead L7). `[ANALYTIC]`

**Frame.** The self/coupling split is taken in this **DBP coordinate frame** — *not* an orthonormal vielbein. The σ_r are frame-independent invariants, but the channels carry their D/S/P meaning only in the coordinate frame, and orthonormalising (a √ of the metric) is the *sole* source of irrationality — see §14.3. Orthonormalising also rotates the channels off the role axes, mixing them. `[ANALYTIC]`

---

## §2. The channel-density tower

For `1 ≤ r ≤ n−1`, define the **channel-density polynomial**

```
Ĉ_r(t,u) = (−1)^{r+1} Σ_{|I|=r+1}  det [ 0    g_Iᵀ ]
                                       [ g_I  (t·H_c + u·H_s)_I ]
```

`Ĉ_r` is homogeneous of degree `r` in `(t,u)`. Expand

```
Ĉ_r(t,u) = Σ_{p+q=r} t^p u^q · κ̂_{r;p,q}.
```

Normalized channel curvatures and the **canonical elementary curvature invariant**:

```
κ_{r;p,q} = κ̂_{r;p,q} / q^{(r+2)/2}
σ_r       = Σ_{p+q=r} κ_{r;p,q} = Ĉ_r(1,1) / q^{(r+2)/2}.
```

The channel vector `C_r = (κ_{r;r,0}, …, κ_{r;0,r})` has the **reduction map**

```
Σ : C_r ↦ Σ κ_{r;p,q} = σ_r,     ker Σ = { δC_r : Σ δκ_{r;p,q} = 0 }.
```

> **The channel decomposition is not itself an intrinsic scalar invariant.** It is an exact account of how the invariant curvature `σ_r` is distributed across self / coupling / interaction channels in a chosen chart, basis, and defining-function gauge. The total is invariant; the channel account is a representative in the affine fiber over it.

**n = 3 specialisation.** `r = 2`, `C_2 = (κ_c, κ_int, κ_s)`, and (this is the flat case; the curved-ambient generalisation is §14)

```
K_G = κ_c + κ_s + κ_int,    ker Σ = {(a,b,c) : a+b+c = 0}.
```

Keystone `F = x₁² + x₁x₂ + x₃² − 3` at `(1,1,1)`:

```
(κ_c, κ_s, κ_int) = (−1/49, 1/49, −3/49),   K_G = −3/49.      [MEASURED]
```

---

## §3. Shape-operator grounding `[+ADDED]`

The σ_r are not an ad-hoc construction: **σ_r is the r-th elementary symmetric function of the shape operator S's eigenvalues** (the principal curvatures). Equivalently `Ĉ_r(1,1) = (−1)^{r+1} Σ_{|I|=r+1} det(bordered H_I)` is the standard bordered-minor expression for the r-th Gauss–Kronecker curvature numerator.

This is *why* `{σ_1, …, σ_{n−1}}` is the **complete set of scalar curvature invariants**: any role-invariant scalar of the curvature 2-jet is a function of S's spectrum, and the elementary symmetric functions generate all symmetric functions of the principal curvatures. A statement like "σ_r is *the* intrinsic invariant" is true per-rung; **completeness is the whole tower.** `[ANALYTIC]`

Verified anchors (n=3): `σ_2·q = e₂(PHP)` and `σ_1·q⁻¹·(−1) = tr(PHP)`, i.e. `σ_2 = K_G` and `σ_1 = tr(S)`. `[MEASURED]`

> Scope caveat: `{σ_r}` exhausts the *scalar* invariants. The shape operator also carries the orientation of its principal directions, which is **not** a scalar and not captured by `{σ_r}`. Whether the channel vector secretly encodes that orientation is upgrade lead **L1**.

---

## §4. Parity law `[+ADDED]`

The normalization exponent `(r+2)/2` is an **integer when r is even and a half-integer when r is odd**. Therefore:

```
r even  →  σ_r ∈ ℚ           (rational; even-order curvature)
r odd   →  σ_r ∈ ℚ(√q)       (carries √q; odd-order curvature)
```

`Ĉ_r(1,1)` (the numerator) is always rational; the √q enters only through `q^{(r+2)/2}`. `[ANALYTIC + MEASURED]`

**Consequences.**
- n=3: `σ_2 = K_G ∈ ℚ` (even), `σ_1 = 2·mean curvature ∈ ℚ(√q)` (odd). The three-channel object lives in ℚ precisely because it refines the *even* invariant K_G.
- n=4: `σ_2 ∈ ℚ`, but the Gauss–Kronecker `σ_3 ∈ ℚ(√q)` — only its density is rational. `[MEASURED]`
- **Cella bridge:** this is why `κ²` and `H²` are exact in ℚ in the eval tier — squaring kills the √q. Any n>3 exactness gate must test the rational *numerators* / the densities, not the odd-order curvatures themselves.
- **Lovelock connection (§14.2):** the intrinsic scalar tower uses **only the even** σ_{2j} — exactly the rational ones above. Reason: intrinsic curvature is contractions of Riemann, and Riemann ~ S∧S carries *two* shape factors, so every intrinsic scalar has an **even** number of S-factors → even σ → ℚ. **The parity law is the Lovelock parity.** The √q (odd) sector is the extrinsic-only, mean-curvature-type part that never enters an intrinsic scalar. `[ANALYTIC + MEASURED]`

---

## §5. Canonical invariant reduction

The construction is the short exact sequence

```
0  →  ker Σ  →  ChannelAccount_r  --Σ-->  InvariantCurvature_r  →  0.
```

In words:

```
channel account  =  canonical invariant  +  zero-sum gauge residue.
```

> **Compute the full channel spectrum, then reduce by the summation quotient. The quotient is the intrinsic curvature invariant σ_r; the fiber is the exact channel account explaining how that invariant is represented in the chosen chart, basis, and gauge.**

---

## §6. Gauge transport law

A defining-function gauge `F̃ = μF` with `μ(x) = 1`, `a = ∇log μ(x)`, fixes the gradient and shifts the Hessian:

```
g̃ = g,    H̃ = H + gaᵀ + agᵀ.
```

Because `Pg = 0`, `P(gaᵀ + agᵀ)P = 0`. Hence the shape operator S is unchanged, **every σ_r is preserved**, and the channel account shifts inside `ker Σ`:

```
C_r(g̃, H̃) − C_r(g, H) ∈ ker Σ      (n=3:  δκ_c + δκ_s + δκ_int = 0).      [MEASURED]
```

This is the true chart-change action: not scalar change, but zero-sum redistribution of channel account.

---

## §7. Passive role permutations are trivial

For a permutation matrix `P_σ`, `(g,H) ↦ (P_σ g, P_σ H P_σᵀ)` is a passive relabelling. Since `diag(P_σ H P_σᵀ) = P_σ diag(H) P_σᵀ`, the self/coupling split is equivariant and

```
C_r(P_σ g, P_σ H P_σᵀ) = C_r(g, H).      [MEASURED]
```

The passive Sₙ orbit collapses to a singleton — a covariance check, not an invariant. The nontrivial role action is **active recharting** (§9): solving the relation in a different output role changes the defining function, hence induces a gauge transport.

---

## §8. Single-edge coupling corollary (n=3)

Weighted coupling-edge vector `ν = (g₁H₂₃, g₂H₁₃, g₃H₁₂)`. Then

```
Δ_c = νᵀ(2I − 𝟙𝟙ᵀ)ν      — a Lorentzian quadratic form, signature (2,1).
```

For a single-axis gauge `a = t·e_i`, with `{i,j,k} = {1,2,3}`:

```
δκ_c(t·e_i) = 4t · g₁g₂g₃ · H_jk / q²        (H_jk = the coupling edge opposite vertex i)
⟹  t·e_i pins κ_c  ⟺  H_jk = 0.      [PROVEN + MEASURED, 200 surfaces × 3 axes]
```

When the opposite edge vanishes, the displacement lies on the κ_c-null ray `(0,1,−1)` of `ker Σ`; geometrically, the endpoint gauges of the active edge move ν along **null directions** of the Lorentzian form. `∏g = e₃` of the projective normal, so κ_c also goes rigid on the normal-coordinate boundary.

---

## §9. Active role recharting → the three DBP output charts

Solving `F = 0` for each output variable gives three **graph charts**, each with `κ_int = 0` (a graph chart has no interaction channel). For a graph `z = h(x,y)` with first jet `(α,β)` and second jet `(L,M,N)`:

```
κ_c = −M²/Q²,   κ_s = LN/Q²,   κ_int = 0,   K_G = (LN−M²)/Q²,   Q = 1+α²+β².
```

The three output roles `{P, D, S}` are the three `κ_int = 0` points on the gauge orbit, all sharing K_G:

```
OutputRoleCurvSpec(f) = {C_P, C_D, C_S}      (input swaps collapse 6 ordered charts → 3 spectra).   [MEASURED]
```

The implicit (non-graph) representation is a fourth point on the same orbit with `κ_int ≠ 0`. The continuous gauge orbit (§6) is the ambient; the three DBP roles are its three graph-normalization sections.

---

## §10. Placement in Theorem 8.1′ `[+ADDED]`

Theorem 8.1′ (orbit/quotient form): a local order-r function φ is a **DBP invariant ⟺ φ factors through the S₃ role-jet orbit** `𝔎_r⁺ = Orb_{S₃}(D,S,P, jʳ(⊕))`. The orbit is the universal carrier of all local DBP invariants; coupling-structural invariants are exactly the orbit functions that do **not** descend to the value-only quotient `(D,S,P)/S₃`.

**This curvature reduction is the order-2 projection of that theorem.** At `r = 2` the carrier is the orbit of `(g, H)` under the role action; its invariant quotient is the shape-operator spectrum `{σ_1, …, σ_{n−1}}` (parity-split per §4), and the channel decomposition is a *section of the gauge fiber over* `σ_{n−1}` (and over each σ_r). That single line is why a scalar channel split is representation-relative and why the σ_r alone survive the role action. The whole §2–§9 structure is "what Theorem 8.1′ looks like when you read it through second-order curvature."

---

## §11. Reference implementation

Full runnable substrate: **`dbp_curvature_reduction_harness.py`** (already on disk; exact-ℚ, stdlib-only). Core functions (lift directly):

```python
from fractions import Fraction as Q
from itertools import combinations, permutations

def channel_density(g, H, r, t, u):
    n = len(g)
    M = [[(t*H[i][j] if i != j else u*H[i][j]) for j in range(n)] for i in range(n)]
    tot = Q(0)
    for I in combinations(range(n), r+1):
        gI = [g[i] for i in I]; MI = [[M[i][j] for j in I] for i in I]; k = len(I)
        B = [[Q(0)]+gI] + [[gI[a]]+MI[a] for a in range(k)]
        tot += det(B)
    return ((-1)**(r+1)) * tot

def q_of(g):              return sum(x*x for x in g)
def sigma_numerator(g,H,r): return channel_density(g, H, r, Q(1), Q(1))   # σ_r = this / q^((r+2)/2)
def channel_vector(g,H,r):                                                # κ̂_{r;p,q}
    nodes = list(range(r+1))
    V = [[Q(s)**p for p in range(r+1)] for s in nodes]
    y = [channel_density(g, H, r, Q(s), Q(1)) for s in nodes]
    a = solve(V, y); return {(p, r-p): a[p] for p in range(r+1)}
def gauge_H(g,H,a):       return [[H[i][j]+g[i]*a[j]+a[i]*g[j] for j in range(len(g))] for i in range(len(g))]
```

(`det`, `solve`, `PHP`, `e2` are in the harness.) The channel vector is recovered exactly by solving a Vandermonde system on the homogeneous-degree-r polynomial — works for any `n, r`.

---

## §12. Verification record (all green)

| check | result | report |
|---|---|---|
| passive orbit trivial; active 6→3 spectra | PASS | `theorem_8_1_curvature_orbit_probe.py` |
| gauge transport law exact (4 gauges + sheet) | PASS | `gauge_channel_transport_probe.py` |
| active spectra == canonical object; keystone graph charts κ_int=0, K_G shared | PASS | `curv_orbit_gauge_crosscheck` |
| two invariants {K_G, H_mean}; channels see only K_G; parity | PASS | `invariant_reduction_check` |
| general (n,r) tower reduces to verified n=3; n=4 parity | PASS | `canonical_reduction_tower_check` |
| **retrodiction gate + invariant sweep n=3,4,5** | **CLEAN** | `dbp_curvature_reduction_harness` |
| A1 — extrinsic Riemann **tensor** channelises `R_ext = R_cc + R_int + R_ss` (81 tangent 4-tuples, n=4) | PASS | `dbp_riemannian_checks` |
| A2 — exact-ℚ rational metric (`ḡ≠I → −9/169`); genuinely curved ambient `K = −2/3`, no √ | PASS | `dbp_riemannian_checks` |
| A3 — σ₄ channelises (Σ⁴⊂ℝ⁵, rational); σ₃ parity (numerator rational, carries √q) | PASS | `dbp_riemannian_checks` |
| **KC8 — ambient `R̄` non-additive in ḡ (nonlinearity wall holds)** | **PASS** | `dbp_riemannian_checks` |

---

## §13. Stress-test & exhaustive-variation protocol

### 13.1 Kill conditions (armed; a single exact-ℚ counterexample falsifies)

- **KC1 — gauge invariance.** ∃ (g,H), gauge a, r with `sigma_numerator(g, gauge_H(g,H,a), r) ≠ sigma_numerator(g,H,r)`.
- **KC2 — zero-sum residue.** ∃ gauge where the channel-vector shift `Σ(C_r(g̃,H̃) − C_r(g,H)) ≠ 0`.
- **KC3 — passive triviality.** ∃ permutation that changes `channel_vector(g,H,r)`.
- **KC4 — shape-operator identity (n=3).** `σ_2 ≠ channel sum`, or `σ_2·q ≠ e₂(PHP)`, or `σ_1·q⁻¹ ≠ −tr(PHP)`.
- **KC5 — parity / rational numerator.** ∃ r with `sigma_numerator(g,H,r) ∉ ℚ` (it must always be rational; the √q lives only in the denominator).
- **KC6 — single-edge law (n=3).** ∃ single-axis gauge with `δκ_c(t·e_k) ≠ 4t·∏g·H_opp/q²`.
- **KC7 — completeness sanity.** ∃ two surfaces, same `{σ_1,…,σ_{n−1}}` and same orientation data, that are *not* related by gauge+permutation. (Soft; flags a missing invariant.)
- **KC8 — ambient nonlinearity wall (guards §14.4).** The ambient curvature `R̄` must be **non-additive** in the metric: `R̄[ḡ_a + ḡ_b] ≠ R̄[ḡ_a] + R̄[ḡ_b]` for generic rational metrics — this is precisely what forbids a *bilinear* channelisation of the ambient (unlike the extrinsic `S∧S`, which is bilinear and therefore *does* channelise, §14.1). KC8 **fires** iff some generic family shows `R̄` additive/bilinear in ḡ; that would breach the §14.4 wall and mean a bilinear ambient channelisation exists — **a real discovery, not a bug.** Implemented in `dbp_riemannian_checks.py` (currently holds: `R[A+B] ≠ R[A]+R[B]`).

`check_surface(g,H)` already tests KC1–KC3 per surface; extend it with KC4–KC6.

### 13.2 Variation space (sweep exhaustively)

- **Dimension:** n = 3 … 8 (det cost grows; cap r-sweeps or sample permutations for large n).
- **Hessian rank:** full, rank-deficient, rank-1, zero (plane). Watch σ_r at rank thresholds.
- **Coupling-edge topology:** no edges (separable), single edge, two edges sharing a vertex, triangle, complete graph, bipartite, star. The edge lemma (§8) is the single-edge case — does an analogous rank-k law hold for multi-edge?
- **Degenerate strata (the frontier):** `gᵢ = 0` (normal-coordinate boundary — active recharting must refuse), umbilic points (κ₁=κ₂), repeated/zero principal curvatures, discriminant `Δ_n = 0` (role stabiliser), tangent contact, the cone apex.
- **Gauge directions:** single-axis, axis pairs, generic, large magnitude, large-denominator rationals. Confirm motion stays in `ker Σ` everywhere.
- **Named surfaces:** developables (`σ_{n−1}=0`), spheres (umbilic), saddles, monomials `x^m y^n`, the Theorem-8.1 role-jet orbit points, the cone.
- **Adversarial:** surfaces engineered to make a channel blow up, vanish, or coincide; surfaces where odd-order `σ_r` happens to land in ℚ (√q-coefficient vanishes) — characterise that locus.

### 13.3 Structural-upgrade leads (hunt here)

- **L1 — orientation dof.** `{σ_r}` are the scalar invariants; S also carries principal-direction orientation. Does the channel vector encode it? Is there a finer *role-covariant frame* whose invariant part is exactly `{σ_r}` and whose covariant part is a clean orientation observable? `[OPEN]`
- **L2 — odd-order diagnostic.** σ_odd ∈ ℚ(√q). Is the √q-tier a useful coupling diagnostic distinct from the rational tier? Two-tier reduction (rational = Cella-exact even curvatures; √q = odd). Ties to the transfer-function exponent-family paper (radical chains). `[OPEN]`
- **L3 — higher jets.** This is order-2. Theorem 8.1′ has the full r-jet orbit. Is there an order-3 curvature analog (cubic / third fundamental form), and does the channel split extend to the holonomy tower `HolSpec_r`? `[OPEN]`
- **L4 — the κ_{r;p,q} grid (n≥4).** For n≥4 the channel vector has many components. Hidden structure in the (p,q) grid — generating function, recursion, Pascal-like identities, channels that are always zero or always equal? `[OPEN]`
- **L5 — basis-independent split. RESOLVED (strong direction, §14.5).** The self/coupling split is frame-dependent, but the right frame isn't an arbitrary vielbein — it's the **DBP coordinate frame the application supplies**. The full O(n) frame group is *not* a symmetry of a DBP system (it scrambles D/S/P), so the channels are genuine invariants of the DBP-structured surface, invariant under the actual symmetry group (S₃ + signs). Verified: a generic rational `R∈O(3)` keeps σ₂, σ₁ while moving the channels; permutations fix them. The apparent gauge freedom was the artifact, introduced only by orthonormalising away the role structure. `[MEASURED + ANALYTIC]`
- **L6 — Lorentzian signature.** n=3 gives `Δ_c = νᵀ(2I−𝟙𝟙ᵀ)ν`, signature (2,1). Does the channel quadratic form have a fixed signature for general (n,r)? A light-cone reading where null directions = gauge-rigid directions? `[OPEN]`
- **L7 — singular-strata typing.** Classify the curvature object on the boundary where the reduction degenerates (`gᵢ=0`, umbilic, `Δ_n=0`), as typed strata with explicit refusal — consistent with the substrate axiom "degeneracy is a stratum, not a failure." `[OPEN]`

---

## §14. Riemannian elevation: the Gauss–Lovelock channel reduction  `[+ADDED]`

§2–§10 are the **Euclidean** statement: the ambient is flat, so the intrinsic Gaussian curvature *equals* the extrinsic Gauss–Kronecker `σ_{n−1}`. In a curved ambient those two part company, and the reduction lifts cleanly once stated correctly. **Frame:** the self/coupling split below is taken in the **DBP coordinate frame**, never an orthonormal vielbein — orthonormalising rotates the channels off the D/S/P axes (mixing them) and is the *only* thing that forces irrationality (§14.3). The σ_r are frame-independent invariants; the channels carry their role meaning only in the coordinate frame.

### 14.1 Gauss equation and the tensor-level split  `[PROVEN + MEASURED]`

For `Σᵐ ⊂ (Mᵐ⁺¹, ḡ)`, unit normal ν, shape operator S, ambient curvature R̄:

```
R^Σ = R̄ᵀ + S∧S,    (S∧S)(X,Y,Z,W) = ⟨SX,Z⟩⟨SY,W⟩ − ⟨SX,W⟩⟨SY,Z⟩.
```

`S∧S` (Kulkarni–Nomizu) is **bilinear in S**, so `S = S_c + S_s` lifts to a three-channel split of the entire extrinsic curvature **tensor**:

```
S∧S = R_cc + R_int + R_ss,    R_cc = S_c∧S_c,  R_ss = S_s∧S_s,  R_int = S_c∧S_s + S_s∧S_c.
```

The reduction is therefore **not scalar-confined** — it is a (0,4)-tensor statement whose contractions give the scalar channels. Holds on all 81 tangent 4-tuples of a dim-3 hypersurface; a sample sectional curvature equals `κ_c+κ_int+κ_s` exactly. (Check A1, `dbp_riemannian_checks.py`.)

### 14.2 The scalar tower — the surface law is the m=2 shadow

Contracting the Gauss equation gives the universal scalar-curvature law, valid in **every** dimension m:

```
Scal_Σ = Scal̄ − 2 Ric̄(ν,ν) + 2 σ₂(S),     2σ₂(S) = (tr S)² − tr(S²) = 2(κ_c + κ_int + κ_s).
```

For m=2 (`Scal_Σ = 2K_Σ`, `Scal̄ − 2Ric̄(ν,ν) = 2K̄(TΣ)`, `σ₂ = det S`) this collapses to the §2 surface law:

```
K_Σ = K̄(TΣ) + κ_c + κ_s + κ_int.      ← the Euclidean statement, now one shadow of the tower.
```

The full even tower is the Lovelock scalars `L_k` of `R^Σ = R̄ᵀ + S∧S`:

```
L_k^Σ = L_k(R̄ᵀ) + Σ_{j=1}^k Σ_{p+q=2j} Λ_{k,j;p,q}        (exact channel decomposition, ANY ambient).
```

Each `Λ_{k,j;p,q}` is a genuine channel term: p coupling-factors and q self-factors of S contracted against k−j ambient-curvature factors (the p-vs-q split keeps the role semantics; the ambient *weights* it). **In a space form** `R̄ᵀ = c·(g∧g)` the weighting degenerates to a scalar and the channels collapse to pure σ-channels:

```
L_k^Σ = C(m,2k)(2k)! Σ_{j=0}^k C(k,j) c^{k−j} σ_{2j}(S)/C(m,2j),    σ_{2j} = Σ_{p+q=2j} κ_{2j;p,q}.
```

k=1: `Scal_Σ = m(m−1)c + 2σ₂`.  k=2: `L₂ = m(m−1)(m−2)(m−3)c² + 4(m−2)(m−3)c·σ₂ + 24σ₄`.  Flat (c=0): `L_k^Σ = (2k)!·σ_{2k}`. `[k=1,2 coefficients checked by hand against the contracted Gauss equation; σ₄ channelisation MEASURED on Σ⁴⊂ℝ⁵, exact-ℚ — check A3]`

### 14.3 Exactness is a rational-metric property, not a flat one  `[PROVEN + MEASURED]`

`K_G = det(II)/det(I)` in a **rational tangent frame** stays in ℚ for **any rational metric** — `ḡ ≠ I` gives `K_G = −9/169` (exact, ≠ Euclidean −3/49). The **ambient** curvature of a genuinely curved rational metric is exact-ℚ too: `ds² = dx² + (1+x²/2)² dy²` → `K = −2/3`, **no √ anywhere**. Reason: curvature is a *rational* function of `(g, ∂g, ∂²g)` — Christoffels and Riemann never introduce a root. The √ enters **only** via orthonormalisation (the vielbein, a √ of ḡ) and the odd-order normalisation.

> **Parity law, extended to the ambient:** even-order curvature — intrinsic *and* ambient — lies in ℚ for a rational metric; the √q sector is exactly the odd-order, extrinsic-only part. And the Gauss–Lovelock tower uses **only even** σ_{2j} — because Riemann ~ S∧S carries *two* shape factors, every intrinsic scalar carries an even number of S-factors. **The §4 parity law IS the Lovelock parity.** `[ANALYTIC + MEASURED]`

The vielbein was a self-inflicted wound; the DBP coordinate frame keeps both ℚ and the role semantics.

### 14.4 The ambient does not channelise — a proven boundary (KC8)

A **bilinear** channelisation of the ambient curvature R̄ does **not** exist, for an exact reason: R̄ is **nonlinear** in the metric (`Γ ~ ḡ⁻¹∂ḡ`, `R̄ ~ ∂Γ + ΓΓ`), whereas the channel scheme works *because* `S∧S` is bilinear in S. A nonlinear object has no linear self/coupling/interaction partition. This is a derived wall, not a hedge. Around it:

1. The ambient is **exact-ℚ computable** (§14.3), so it isn't opaque — it is *input* geometry contributed by the manifold, **not by F**, hence never the theorem's to channelise.
2. Ambient **coupling** lives in the metric's off-diagonal / position-dependence: a **product** manifold (block-diagonal ḡ in the DBP frame) has zero mixed sectional curvature, so ambient coupling ⟺ the variables share curved geometry, readable straight off ḡ. `[ANALYTIC, standard]`
3. The space-form case (§14.2) is exactly where the ambient weighting degenerates to a scalar `c` and the channels go clean.

Honest general statement:

```
intrinsic curvature  =  ambient (input; exact-ℚ; irreducible by nonlinearity)
                      +  extrinsic (fully channelised — tensor §14.1, Lovelock scalars §14.2; exact-ℚ on even rungs §14.3).
```

**KC8 guards this wall** (§13.1): R̄ must stay non-additive in ḡ. If a generic family ever shows R̄ additive/bilinear, the wall is breached and a bilinear ambient channelisation may exist — a real discovery.

### 14.5 L5 resolved — channels are genuine invariants of the DBP structure  `[MEASURED + ANALYTIC]`

The earlier worry (channels move under the O(n) frame gauge, ∴ "irreducibly gauge-relative") was the wrong posture. The full O(n) is **not a symmetry of a DBP system** — it scrambles directive, substrate, and product, which are physically distinct *by construction*. The channels are invariant under the actual symmetry group (S₃ role permutations + signs; §7), and look like gauge only if you discard the very distinction that defines a DBP. Verified: a generic rational rotation `R ∈ O(3)` keeps `σ₂ = −3/49` and `σ₁`'s numerator while the channels move to `(−961, −3627, 2713)/30625` (still summing to −3/49); a permutation leaves them fixed. **So the DBP coordinate frame is the physical section, not a canonicalising one, and the channels are genuine invariants of the DBP-structured surface.**

---

## §15. Known gaps / honest scope

1. **Completeness is for scalar invariants** (§3): `{σ_r}` generate the role-invariant *scalars*; the orientation dof (L1) is outside it. Not yet proven that no other role-invariant scalar exists once only discrete permutation + gauge (not full tangent rotation) is in play — KC7 probes this.
2. **The general-(n,r) shape-operator identity** (σ_r = r-th elementary symmetric of S) is verified exactly for n=3, r=1,2 `[MEASURED]` and is standard bordered-minor theory `[ANALYTIC]`; a general exact-ℚ check is blocked by the √q in odd ranks (test the rational numerators instead, per KC5).
3. **Active recharting = gauge** is established as "same surface ⟹ gauge-equivalent defining functions" `[ANALYTIC]` plus shared-K_G/κ_int=0 `[MEASURED]`; the explicit connecting gauge vector is not solved (circular for prediction, consistent for verification).
4. **Singular strata** (L7) are flagged but not yet typed.
5. **The ambient curvature is the one proven *non*-channelisable boundary** (§14.4): no *bilinear* channelisation of `R̄` exists, because `R̄` is nonlinear in the metric. This is not a gap to close but a wall with a named cause — KC8 guards it. The ambient enters as exact-ℚ-computable *input* (the extrinsic part is fully channelised at tensor and Lovelock-scalar level).
6. **Closed since the merge:** the headline is no longer surface-only (the extrinsic *tensor* channelises, §14.1; the surface law is the m=2 shadow of the Lovelock tower, §14.2); exact-ℚ is established as a rational-metric — not flat — property (§14.3); and **L5 is resolved** in the strong direction (§14.5). The remaining genuinely open leads are L1 (orientation dof), L2 (odd-order √q diagnostic), L3 (higher jets), L4 (the κ_{r;p,q} grid for n≥4), L6 (Lorentzian signature for general (n,r)), and L7 (singular-strata typing).
