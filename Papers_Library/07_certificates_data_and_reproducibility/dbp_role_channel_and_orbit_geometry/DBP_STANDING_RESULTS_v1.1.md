# DBP / Lloyd Framework — STANDING RESULTS

**Version:** v1.1 **CANONICAL** — grounded in-session S-2026-07-02 (Will: "Go"); supersedes v1.0. (Renamed `10_DBP_STANDING_RESULTS.md` at the 2026-07-02 sweep; stale rename note struck S-2026-07-03) · **Changelog v1.1:** added V.4a (independent rederivation of the wreath law, [CONTAINER]) and V.4b (degree/closed-form layer; dedup vs the superseding .txt CLOSED S-2026-07-03 — three-part verdict in V.4b, one novelty flag withdrawn). Nothing else touched.
**Date:** 2026-07-01 · **Purpose:** the dashboard that retires the `dbp_four_role_calc_log` diary. Organized by mathematical object (not by session), deduplicated, tier-graded, with self-corrections folded in and superseded items quarantined (Part VII).

## How to read this
- **This is STATE, not history.** The calc log recorded what each session *did*, including sessions that re-opened settled questions. This records what is *true now*. Where they conflict, this wins.
- **Source-of-truth order:** persistent evals > this dashboard > calc log (history) > container scripts (ephemeral).
- **Certification substrate** is marked per result: `[EVAL]` = runnable persistent eval under `evals/`; `[CONTAINER]` = computed in an ephemeral `/home/claude/` script (result recorded, script may not persist); `[PAPER]` = proven/computer-verified in a writeup under `tmp/pdfs/`.
- **Tiers:** `[proven]` (complete argument) · `[computer-verified]` (exact CAS on instances) · `[interpretation]` · `[open]`. Exact-ℚ / GF(p)-rigorous throughout the corpus; no float in any verdict.

## Certification substrate map
- `evals/dbp_involution/` (stage0/A/B/C/D/E) — the 102-claim byte-stable-×2 campaign (CALC-20). Certifies Parts I, II, and the same-S₃ negative. **[EVAL]**
- `evals/constant_hunt/` (alt_scalar, dbp_total_curvature, run_constant_hunt) — Sym² alt-scalar + total-curvature constant.
- `tmp/pdfs/constant_hunt/self_glue_monodromy.txt` — the wreath-law monodromy writeup (Part V.4). **[PAPER]**
- Parts IV (r,n-theorem) and V.1–V.3 were computed in ephemeral container scripts (`f1_*.py`, `trap_*.py`). **[CONTAINER]** — recorded proven/verified; scripts not persisted.
- Papers (`/mnt/project/`): `role_channel_anisotropy`, `dbp_orbit_calculus`, `self_glue_monodromy` = the n=3 spine this corpus lifts.

---

# PART I — THE LINEAR COUPLING CARRIER (role axis) · Phase 1

### I.1 Central theorem — the carrier is the role-pair module
For all `n ≥ 3`, the realizable coupling carrier is
```
Im(L) ≅ M^(n−2,2) = ℂ[C(n,2) role-pairs] = triv ⊕ std(n−1,1) ⊕ S^(n−2,2)
```
Proof: `ker L =` the defining-function gauge `G = {v⊗g + g⊗v}`, so `Im(L) ≅ Sym²(ℝⁿ)/G ≅ Sym²(std)`, character `C(fix,2)+#2cycles` = role-pair character. `[proven, all n]` (load-bearing steps computer-verified n=4..9). Source: CALC-14 · **[EVAL]** stage0.

### I.2 The loss (what any magnitude summary discards) = the shape S^(n−2,2)
Per-role coupling magnitude `(C)` spans the marginal `triv ⊕ std`; the discarded part is exactly `S^(n−2,2)`, `dim = n(n−3)/2`:
- n=3: `(n−2,2)` invalid → **no shape**; `A_c` is the whole story.
- n=4: the exceptional **quotient** doublet `(2,2)`, factoring through `S₄/V₄ ≅ S₃` (the V₄ accident).
- n≥5: **faithful**, faithfulness margin `= 2(n−3)` (linear growth), singular dip to 0 at n=4.
`[proven for S^(n−2,2); loss identity computer-verified n=4..8]`. CALC-08/11/12/13 · **[EVAL]** stage0.

### I.3 Gauge-normal form — the carrier IS the gauge-invariant Hessian quotient
For regular `g`, every `H` has a unique gauge-normal representative (diagonal killed), off-diagonal = the obstruction
```
O_ij = H_ij − g_i·H_jj/(2g_j) − g_j·H_ii/(2g_i) ,   Λ_{k,{j,l}} = O_jk + O_kl − O_jl
dim O = n(n−1)/2 = dim M^(n−2,2)   (carrier = framework's gauge-invariant Hessian quotient)
```
`σ_r` are gauge-invariant; channels move inside `ker Σ` (zero-sum). `[proven + computer-verified]`. CALC-27 (Campaign H Lemma H1).

### I.3a The n=3 coupling channel is a signed isotypic moment `[CANONICAL — auto-filed per PA-1, Will S-2026-07-02]`
The transport law's "Lorentzian coupling metric" is the isotypic form on the pair module:
```
Δ_c(ν) = νᵀ(2I−J)ν = 2‖π_std ν‖² − ‖π_triv ν‖² ,   ν = (g₁H₂₃, g₂H₁₃, g₃H₁₂)
eig(2I−J) = {+2 on std (dim 2), −1 on triv (dim 1)}   — signature (2,1) = (dim std, dim triv)
```
`[CONTAINER, symbolic, n=3]` (S-2026-07-02; matches the doc's own keystone instance Δ_c = 4). Consequences: the transport law is the **n=3 member of the isotypic-moment family** — `m2_shape` at n≥5 (Part III witness) is its sibling; the κ_c-pinning null sheets (§6–7) are null directions of the isotypic form. Caveats carried: the opposite-vertex weighting `ν_k = g_k H_ij` is n=3-specific (pair↔vertex duality dies at n≥4); the statement lives pre-gauge-quotient (channel *allocation* motion — invariants live on O). → registry-20 row; source `Gauge_Channel_Transport_Law.md` §5–7.

### I.3b Triangle decomposition + shadow law of the coupling channel, general n `[PROVEN + CERTIFIED ×2 — GROUNDED, Will S-2026-07-05b "file the HR-row-equivalent deltas"]`
```
Δ_c^(n)(h) = q·Σ_e h_e² − |H_c·g|²                    (closed form of −q·e_2(P H_c P))
Q_ν = Σ_{|S|=3} T_S·(2I−J)_S ,   T_S = 1/∏_{m∉S} g_m²   (master identity)
shadow(Q_ν) = s(g)·[(n−2)I − A₁(Johnson J(n,2))] ,   s(g) = e_3(g²)/(C(n,3)·e_n(g²))
```
The general-n coupling channel is a T_S-weighted sum of n=3 keystone forms over vertex-triangles; its full invariant content is the Johnson operator with one g-borne scalar. **I.3a = the n=3 member** (one triangle, (n−2)I−A₁ = 2I−J, s ≡ 1 — the constant coefficients were the scalar collapsing). Proven consequences: fixed-g three-moment expansion of Δ_c is FALSE at n≥4 (flagship Stage B K-B1) because the triangle-weight fluctuation is generically nonzero; residual triv-triv block ≡ 0. n=4 block sparsity = label-module selection rule [STRUCTURAL, unproven]. Opens the CL-ENG2 fault-semantics route (self-faults have δν = 0 by construction). `[BOX, symbolic n=4 + exact ℚ 15/15 fixtures, byte-stable ×2]` Authority: `campaigns/shape_witness/stage_B_succession/SHADOW_LAW_THEOREM.md` + records `ca2741a0`/`68698bf2`/`ef2851e9`. W-prod normalization; g entries nonzero; prior-art sweep owed at claim boundary (Johnson algebra classical — Delsarte; novelty candidate = the decomposition of THIS channel).

### I.4 A_c keystone anchor (THE GATE)
On `F = D²+DS+P²−3` at `(1,1,1)`: `κ_c^(P,D,S) = (−25/196, −1/441, −1/49)`, `A_c = 42793/1555848`. Every downstream instrument is gated against this exact value. `[computer-verified]`. CALC-02/15a.

### I.5 The resolvent S₃ is a role-QUOTIENT, not independent (the "same-S₃" answer)
The `(2,2)` shape doublet is the standard rep of the resolvent `S₃ = S₄/V₄`, `V₄` its kernel — **role-determined, NOT an independent third S₃**. The self-glue monodromy's within-block S₃ acts on root-sheets of the stage-2 trinomial, which carry no canonical bijection to the 3 roles ⟹ **the role S₃ and the monodromy S₃ are distinct**; verdict `no_canonical_comparison_map`. `[computer-verified / proven]`. CALC-10 · **[EVAL]** `stageE_monodromy_alt_probe.py` (this is the authoritative closure; see Part VII re CALC-36).

### I.6 Finite two-state witness for the (2,2) shape
Exact n=4 pair `H₀ ≠ H`, gauge-fixed (role-0 row = 0):
```
H₀ = (H11,H22,H33)=(2,−1,3), (H12,H13,H23)=(1,−2,1)
H  = (H11,H22,H33)=(−2,−2,−6), (H12,H13,H23)=(2,−1,−1)
(C)(H₀) = (C)(H) = (6,33,33,54)  identical magnitude ;  (A) differs in all 12 comps
ΔA isotypic norms: triv 147, std 153, (2,2)=24, sgn=0 ;  Parseval Σ=324
```
Magnitude cannot separate them; the role-pair carrier can. `[computer-verified]` / `[proven]` (pos-def Q₀ on shape plane ⇒ no on-tangent witness, closes CALC-07). CALC-30 · **[CONTAINER]**.

### I.7 Solvability wall + char-2, all n
- Derived series measured on own commutators: S₃,S₄ solvable; **S₅ stalls at A₅**. `S₄'' = V₄` = the shape-quotient kernel — one structure, three appearances. `[computer-verified]`. CALC-11.
- Carrier is `C(n,2)`-dim in **every** characteristic; at char 2 the gauge rank drops n→n−1, restored by the phantom `g gᵀ`. `[computer-verified n=3..7; mechanism proven]`. CALC-16 · **[EVAL]** stageD.

---

# PART II — PRIME-2 / MODULAR STRATIFICATION · Phase 1

The prime 2 governs **three distinct layers** (the thesis "every fault line is one fact" is FALSE; the correct statement is this stratification). Unifying object: `std⊗std` with swap `τ`; carrier = `+1` (symmetric) eigenspace, `∧² = −1`; prime 2 = where the split fails. CALC-22 · **[EVAL]** stageA/B/C/D.

- **(a) Phantom `ℤ/2` — lives in the gauge/kernel, washed out of the image.** `Im(L)` is torsion-free/saturated; the `ℤ/2 = sat(gauge)/gauge`, generator `[g gᵀ]`, uniform in n. Visible in Campaign H's quotient model over F₂, absent from the numerator image. `[computer-verified n=4..8]`. CALC-19 (corrects CALC-18 Finding 2).
- **(b) The alternating companion `∧²(std) = S^(n−2,1,1)` IS realized at degree 2**, locally, in the per-(chart,pair) channel curvature `κ_c` — full projection (rank = dim S^(n−2,1,1), n=4,5,6). The global/monodromy route is NOT required. `[computer-verified n=4,5,6]`. CALC-21.
- **(c) Magnitude and orientation collide mod 2, generically:**
```
[S^(n−2,1,1)]  =  [S^(n−2,2)]  +  [D^(n)]      (orientation = shape + one trivial), n=4..7
```
V₄ is the n=4 special case, NOT the mechanism (collision is all-n). `[computer-verified n=4..7; all-n conjectured]`. CALC-22.

Cross-checked independently by the 102-claim campaign (byte-stable ×2), no contradictions. CALC-20.

---

# PART III — DIMENSION THRESHOLD (scalars vs shape)

**The clean separator between "scalars suffice" and "need the carrier/monodromy" is a DIMENSION THRESHOLD, not a discriminant locus.** With `n−1` scalar invariants `σ_r` and shape `dim = n(n−3)/2`:
```
scalars resolve the shape  ⟺  n−1 ≥ n(n−3)/2  ⟺  n²−5n+2 ≤ 0  ⟺  n ≤ 4
```
n=4: the full `σ_r` spectrum resolves the `(2,2)` shape (rank 2 — the V₄ accident is small enough). n≥5: rank-deficient by dimension alone. This **coincides with the carrier-faithfulness threshold** (faithful n≥5). `[proven]`. CALC-26/27.
- A *single* scalar (`j`, `K_G`, one channel) aliases the shape at every n; the full `σ_r` spectrum resolves it iff n≤4. The `j=128` aliasing triple aliased because one scalar can't resolve even the 2-dim n=4 shape.
- Pure-self channels `κ_{r;0,r}` are genuinely shape-blind (built from diagonal only); coupling channels `p≥1` carry the shape. CALC-26.
- The rank-drop locus is **codim 2** (≠ the codim-1 role-degeneracy `Δ_n`); no clean single-hypersurface aliasing locus. Conditional bridge survives only on the std-free slice. CALC-28.
- **n=5 explicit witness `[CERTIFIED ×2, records sha 39bed555]` (grounded S-2026-07-02, Will: "confirmed"):** full σ-spectrum tied exactly by **g-stabilizing rational conjugation** `H2 = RᵀH1R`, `R = Cayley(uvᵀ−vuᵀ)`, `u,v ⊥ g` — similarity mechanism ties ALL orders `[PROVEN]`, certified by two independent routes (bordered sums `Ê_r = (244,−2620,−7912,−1384)` both; q-cleared tangential charpolys identical in ℚ[z]). Shape components differ **10/10** coords; separated by the degree-2 invariant `m2_shape = ‖π_shape(O)‖²` = `68/3 vs 19914692/1366875`. **The dimension threshold realized constructively.** Scoped: one (g, H1, A); genericity + n>5 family `[open]`; degree-2 generic sufficiency `[open]`. Session gauge lemma banked: `Ê_r(H+gbᵀ+bgᵀ)=Ê_r(H)` all r `[PROVEN, row/col reduction]`. → `campaigns/shape_witness/` (predecl pin `967c7909`, `witness_battery.py`). Flagship (completeness via 8.1′) UNBLOCKED, not opened.

---

# PART IV — THE (r,n)-PLANE DEPTH THEOREM (order axis) · COMPLETE

> **THEOREM.** For all `r ≥ 2` and all `n ≥ 2r`, the order-r pure-coupling channel `κ_{r;r,0}` (the r×r coupling minor) realizes the depth-r Specht module `S^(n−r,r)`. `[proven — complete, no gaps]`

The order-axis analog of the role-axis theorem (Part I): climbing role-count `n` gains depth-2 `S^(n−2,2)`; climbing order `r` gains depth-r `S^(n−r,r)`, for every order and every admissible n. Built and closed across CALC-31…35 · **[CONTAINER]** (`f1_*.py`):
- **Target screen** `[proven]`: `S^(n−r,r) ⊆ M_flags^(r)` for all r, all n≥2r (Kostka dominance) — never blind by target. CALC-31.
- **Realizability** `[computer-verified, certified]`: r=3 fully realized n=6,7; pure-self control BLIND ⟹ coupling required. CALC-32.
- **All-r engine** `[proven]`: minor collapses `D_{k,T}|_{x_k=0} = (1−r)∏_{i∈T}x_i²`; top-Specht nonvanishing by monomial independence. CALC-33.
- **Lift (interior n≥2r+1)** `[proven]`: closed-form pairing `⟨Φ(D),w'⟩ = (−1)^r 2^{r−2}(r−1)(r−4)∏(c_{q_a}−c_{p_a})` for r≠4; explicit rank-one witness for r=4. CALC-34.
- **Threshold n=2r** `[proven]`: star-at-marked-vertex closed form; cofactor `C_r` is a nonzero linear form for all r≥3 (no degenerate order). CALC-35.

Open beyond the theorem: mixed bidegrees `κ_{r;p,q}` (minimal p for depth r); other depth-r irreps (`S^(n−r,1^r)`, three-row); full-density surjectivity onto `M_flags^(r)`. (See Part VI.)

---

# PART V — TRANSCENDENCE / ARITHMETIC LANDSCAPE · Phase 2

### V.1 Total curvature is a genuine non-CM elliptic period (j=128)
```
∫∫_S K_G dA = −5.010490702660418769050021160526777648057…  (three independent routes, 60 digits)
   on  y² = w(1−w)(1+w²), branch pts {0,1,±i}, cross-ratio −i, j = 128 (exact)
CLOSED FORM = −2^{7/4}[(3+2√2)·Π((4−3√2)/8; (2−√2)/4) − (2+2√2)·K((2−√2)/4)]
global curvature field:  K_G = −12/|∇F|⁴  (bordered-Hess det ≡ 12 on the surface)
```
**V.1a addendum (2026-07-02) `[PROPOSED — pending grounding]`:** minimal Weierstrass model `Y² = X³ − X² + X − 1`: Δ_min = −256 = −2⁸, c4 = −32, j = 128 exact; **minimality PROVEN** (scaling needs 2¹²|Δ; 4096∤256); bad-reduction support = {2} exactly. Quartic invariants I=−2, J=20 ⟹ j=128 in both cubic conventions (quartic↔minimal-form link verified). Closed form re-verified in-container to 6e−61 against the 60-digit constant · **[CONTAINER]** (this session).

j=128 is rational and not among the 13 class-number-1 CM values ⟹ **provably non-CM** ⟹ no Chowla–Selberg Γ-evaluation; provably not π·algebraic, not Γ(1/3), not Γ(1/4). The `DS` shear is exactly what breaks the algebraic·π cleanliness. `[computer-verified to 60–61 digits; reduction proven link-by-link]`. CALC-23 · **[CONTAINER]** (constant also in **[EVAL]** `constant_hunt/dbp_total_curvature.py`).

### V.2 The arithmetic landscape is a closed-form function of coupling
```
curvature register:  j(s) = (1728s⁶−1728s⁴+576s²−64)/(s⁶+2s⁴+s²) ,  s = shear
monodromy register:  j(S) = 6912 S³/(4S³+243) ,  S = substrate
both:  Γ(1/3) at one coupling-degeneration limit → non-CM generic → Γ(1/4) at the other
```
- `j(s)` monotone on (0,∞): `dj/ds = 128(3s²−1)²(9s²+1)/[s³(s²+1)³] ≥ 0` ⟹ unique s per j<1728. Γ(1/3)@`s=1/√3`, keystone non-CM `j=128`@`s=1`, Γ(1/4)@`s→∞`. `[proven]`
- The true carrier invariant is `σ = 2h/(λ−b) = tan(2θ)` (mixing angle of the coupled block), NOT coupling magnitude. Full carrier is a conformal invariant of the whole asymptotic cone (2-parameter): the spectator P-self `G` enters and is the sole knob breaking the Γ(1/4) ceiling. `[proven / computer-verified]`. CALC-24 E.3–E.4.
- CM ladder (class-number-1, all in the weak band s<1/√3): `d = −7,−11,−19,−27,−43,−67,−163`; **only d=−7 has a closed form** (`s = 1/(3√7)`), every other rung is irreducible degree-3 in `u=s²`. h=2 band walls enumerated (7, nearest d=−32). `[proven + computer-verified]`. CALC-24 E, E.2 · **[CONTAINER]** (`ladder.py`, `h2_walls.py`).

### V.3 The j=128 aliasing triple — the group is blind; branch config resolves
Three distinct forms `(λ,h,b) = (1,½,0),(1,1,−1),(1,¼,½)` all have `σ=1`, all `j=128`. The abstract monodromy group is `D₄` for all three (both scalar `j` AND the Galois group over-collapse). The discriminating invariant is the **branch configuration**: omega-multiplicity (2 vs 4) + block signature (indef/def) separates all three. `[proven; group + multiplicities + signatures]`. CALC-25 · **[CONTAINER]** (`mono_galois.py`).

### V.4 Self-glue monodromy wreath law
```
Lemma C (gcd law):  cover x^m + s x^k − c  has monodromy  C_d ≀ S_{m/d}, d = gcd(m,k)   [proven]
product cover      =  C_mP ≀ C_mP  (cyclic wreath, order mP^{mP+1})                     [proven]
```
Corrects the original paper's `Sym(mP)≀Sym(mP)`; answers "does the product side climb to S₃≀S₃": **no, cyclic**. Certified continuation across coprime (3,2)(4,3)(6,5) and non-coprime (4,2)(6,2)(6,3)(9,3). `[proven / computer-verified]`. **[PAPER]** `tmp/pdfs/constant_hunt/self_glue_monodromy.txt` (supersedes CALC-25's open wreath items; see drift ledger DRIFT-2).

**V.4a — Independent in-container rederivation (2026-07-02) `[GROUNDED S-2026-07-02]`.** Wreath law re-certified without access to the [PAPER] substrate: (i) containment `Mon(product) ⊆ C_mP ≀ C_mP` for ALL (m_D,m_P) `[proven]` (Kummer ratio-of-continuations; refutes Sym≀Sym for mP≥3 by order alone; m_D enters nowhere); (ii) Lemma C containment `Mon ⊆ C_d ≀ S_{m/d}` via `x^m+sx^k−c = g(x^d)` `[proven]`; (iii) fullness engine = the omega signature (`∂A/∂S₂=0` ⟹ one ζ_mP-rotation per block, measured e^(2πi/3) at (3,3)) `[proven modulo standard Puiseux]`; (iv) all seven Lemma-C instances + product covers (3,2),(2,2),(3,3),(2,3) hit the proven bounds exactly, gates ≤1.3e−15, byte-stable ×2 · **[CONTAINER]** `mono_rederive.py`.

**V.4b — Degree/closed-form layer (2026-07-02) `[GROUNDED S-2026-07-02 — dedup vs the .txt CLOSED S-2026-07-03]`.** Dedup verdict vs `self_glue_monodromy.txt`: (i) KEEP — genuine advance: eqs (2)/(3) upgraded from the .txt §2's `[symbolic, m_D≤5]` to `[proven]` ALL m_D. (ii) FLAG WITHDRAWN — "m_P=3 NEW beyond the paper" was wrong: .txt §9's n-stage law is verified across (2,2),(3,2),(2,3),(3,3) at n=2,3, and its n=2 slice IS the single-glue spectrum, so m_P=3 was already inside the paper's verified set; the check stands as independent re-verification only. (iii) KEEP — beyond the .txt: the general proof route (its §9 spectrum stays `[symbolic]`). Paper eqs (2)/(3) `[proven]` for ALL m_D via `Res(Z²−A,g)=g(√A)g(−√A)` (verified m_D=2..7 exact); degree spectrum `(m²_D, m_D, m_P, m²_P)` `[computer-verified]` at m_P∈{2,3}, m_D∈{2,3,4} — [novelty flag withdrawn S-2026-07-03, see verdict (ii) above]; general-(m_D,m_P) proof route identified (product formula over seam roots; one leading-coefficient check open) ⟹ n-stage induction ⟹ recovery asymmetry `(m_D/m_P)^n` upgrades to `[proven]` once closed · **[CONTAINER]** `verify_paper.py`.

---

# PART VI — GENUINELY OPEN (the live frontier)

- **P-F3 chassis verdict + SPLIT LAW `[GROUNDED — Will "accept defaults" S-2026-07-05]`:** all 9 slices (8 registered + fresh perturbed s8) of the two-Cayley chassis CERTIFIED rational-point-free ×2 (dual independent certificates on 6). Tie locus per slice: deg 704 = two Q-irreducible Galois orbits of 352 [CERTIFIED 9/9, intrinsic + slate-generic + gauge-stable]; interiors independent full S_352 [EMPIRICAL, 120-prime Frobenius battery]; square-lead law is D-borne (dies under separating-form change) [CERTIFIED discriminating test]; 3 = chassis structural prime (factor 27 in tie generators, all slices). Identity target: class of N(D1·D2) in Q*/(Q*)². Authority: `campaigns/shape_witness/HUNT_ADDENDUM_v2_4.md` + `SPLIT_PROBE_PREDECL.md` (+A1/A2) + `rabinowitsch_records/`. Mechanism [OPEN]: formula-level factorization of the elimination — sole surviving class. Currency S-2026-07-05b: split probe FULLY GRADED (3a: pointwise-h REFUTED, norm-level identity; 3b.2: PER-DENOMINATOR, no cross-term law; A6/A7: all signs +1 ⟹ **N(D1)=+□, N(D2)=+□ individually at s1; N(D1·D2)=+□ all nine slices**); remaining OPEN = proof of the norm identity + formula origin (3b.3 miniature, gated).

- **p=2 reduction↔representation bridge `[OBSERVED — one data point, PROPOSED frontier]`:** keystone period curve has bad reduction only at 2; the invariant theory walls (V₄ collision, ℤ/2 phantom, Campaign-H char≠2) also live at 2. Non-numerological version: does bad-reduction support of the s-family period curves stay inside the characteristic walls for ALL s (CALC-24 landscape, j(s) exact)? **Kill:** support scatters with the primes of j(s) — the prior. **Survive:** first sighting of a reduction-type ↔ representation-collision correspondence. Test = s-family minimal-discriminant sweep; parked (transcendence arm; flip_cartography holds priority).

Checked against the evals; these have no closure on disk and are the real return targets.
- **Order-axis, beyond the depth theorem:** mixed bidegrees `κ_{r;p,q}` — minimal coupling degree `p` to reach depth r (CALC-26: p≥1 at depth 2; general threshold open); other depth-r irreps (alternating `S^(n−r,1^r)`, three-row `S^(n−r−1,r,1)`); full-density surjectivity of the order-r density onto `M_flags^(r)` (seen at r=3,n=6). `[open]`
- **Modular (Part II) all-n:** prove `[S^(n−2,1,1)] = [S^(n−2,2)] + [D^(n)]` for all n; identify the extra trivial `D^(n)` (= phantom?). `[open]`
- **char-2 / modular rep theory:** all-n RoleChSpec faithfulness in char 2 (CL-H10 analog); other primes; does `S^(n−2,2)` stay irreducible mod p. `[open]`
- **Arithmetic diagnostic (CALC-25 open 4):** promote `(omega-multiplicity, signature)` to a *defined diagnostic coordinate* and retrodict the curvature ladder against it. `[open]`
- **Place-(i) limit traps (Phase 2):** generating function `Σ_r Ĉ_r s^r` at special points; n→∞ asymptotics — the untried transcendence vein. `[open]`
- **Frontier map F3/F4/F6/F7:** degeneracy varieties (not just generic ranks); the local↔global residue↔cycle-type isthmus (named in 3 papers, computed in none); ambient-curvature wall gates; moduli chart vs single-surface pins. `[open]`

---

# PART VII — SUPERSEDED / REFUTED (do not resurrect)

The diary's failure mode was re-opening these. They are settled; do not re-derive.
- **CALC-36 (same-S₃, my re-derivation) — SUPERSEDED.** The role S₃ ≠ monodromy S₃ result is CALC-10 / `stageE_monodromy_alt_probe.py` (Part I.5). CALC-36 re-derived it by a weaker Jacobian-rank check and adds nothing. Never lived in v7; do not bank. (See `_audit/CALC_LOG_DRIFT_LEDGER_2026-07-01.md` DRIFT-1.)
- **"Order axis is shallow / stays in std" (CALC-15) — REFUTED** by CALC-18/21: `∧²` is realized at degree 2; the depth tower is real (Part IV). CALC-15 measured only the per-chart std-norm (blind by construction).
- **"Integral carrier has ℤ/2 torsion" (CALC-18 Finding 2) — CORRECTED** by CALC-19: `Im(L)` is torsion-free; the phantom is gauge non-saturation (Part II.a).
- **"Scalars blind to shape, need monodromy" (CALC-23/25 framing) — CORRECTED** by CALC-26/27: the full `σ_r` spectrum resolves the shape iff n≤4 (dimension threshold, Part III). True only for a single scalar, or for n≥5.
- **"Rank-drop locus = Δ_n" (CALC-27-turn conjecture) — REFUTED** by CALC-28 (codim 2 vs codim 1; category error). Conditional bridge survives only on the std-free slice.

---

# PART VIII — PARITY LAW (proven, load-bearing)

```
σ_even ∈ ℚ ,   σ_odd ∈ ℚ(√q)      (= Lovelock parity)
```
The even scalar curvature is rational; the mean-curvature / odd orders carry one factor `√q` (the unit normal). It is the `q^((r+2)/2)` normalization, not a deep arithmetic fact; invisible to the squared anisotropy invariant `A_c^(r)` (rational at every order). Two *distinct* by-r parities exist: this **field parity** (CALC-15) and Campaign H's **O-parity** (degree-r in the carrier O — the injectivity-load-bearing one, CALC-17). `[proven]` (`DBP_Curvature_Role_Reduction.md` §4). Discharges anisotropy §8.

---
*End of standing results. Retire the calc log to `_archive/`; keep the evals and this dashboard as state. When a new result lands: add it here by object, cite its eval, and let the diary stay dead.*
