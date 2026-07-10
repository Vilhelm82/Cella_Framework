# DBP Four-Role Coupling Carrier — Running Calculation Log

## ▶ COLD OPEN — read this first (zero-context start)

**What this is.** The Lloyd/DBP framework (Directive-Based Products, `D ⊕ S = P`) diagnoses coupling faults and constraint-surface geometry through the intrinsic curvature `K_G` of a defining surface `F = 0`. *This* log is one workstream: take the multi-role coupling up the role-count axis and pin down exactly **what invariant the coupling carries** under the role-permutation symmetry `S_n`, and **what a compressed summary of it discards**.

**Definitions are NOT in this file.** "Active Role-Jet", channel reduction (§6), carrier-faithfulness (§7.3), the keystone surfaces, `A_c` — all defined in `/mnt/project/`: `role_channel_anisotropy.tex`, `dbp_orbit_calculus.pdf`, `self_glue_monodromy.pdf`. Read those for the machinery. The working register (anti-sycophantic, exact-ℚ, certainty-tiered, "no eulogies on gaps") is in memory, not here.

**What's settled.** Proved for all n (CALC-14): the carrier is the role-pair module `Im(L) ≅ triv ⊕ std ⊕ S^(n−2,2)`; magnitude-only summaries keep `triv ⊕ std` and discard the shape `S^(n−2,2)`. Standing conclusions 1–8 are the settled set, each carrying its tier — `[proven]` items are **closed; do not relitigate them.**

**Where it's live.** The central theorem is closed, so the workstream is at a **fork**, not mid-derivation. Open directions are the Frontier map (F1–F7) and the Open/next list — pick deliberately; nothing is forced. The most concrete loose thread is the finite two-state witness (the Kerr–Newman analog), which needs the 2-dim fiber actually solved, not just dimension-counted.

### ▶ Methodology — how this workstream is run (load-bearing, not preamble)

**(1) Map the space — do not tunnel on a target.** The objective is never "prove T". It is: **exhaust each identity — map where it reaches and where it breaks, and mark where it branches and joins.** Naming a single target narrows the search and forfeits everything the surrounding space would have revealed. Operationally: every time a computation walks *one* axis hard (order `r`, role-count `n`, separability, solvability…), the **transverse** territory it skipped is logged as a standing return target — that is exactly what the **Frontier map (F1–F7)** below is: a deliberate inventory of single-direction cuts and their blank margins. Closing the nearest result and moving on is the failure mode; keeping the map honest is the method. (The map is also where the project's *shape* is recorded — e.g. that everything clean so far lives in the "solvable corner": `r = 2`, `n ≤ 4`, separable. That observation is itself a lead, not a comfort.)

**(2) Imported math is a suspect, never an authority.** A named theorem / named formula / off-the-shelf decomposition carries the **conclusion of a *different* investigative path** — it brings that path's vocabulary and its tacit claim to be *the* natural articulation. Imported as substrate it forecloses on what our own machinery would find, and it can **mislabel our own transitions**. Standing protocol when an import names one of our phenomena:
- **demote** it to a *navigation target* (where to aim), never a closing argument;
- **reproduce** the phenomenon on our own machinery (measure the wall on our own commutators; build the table from scratch, not transcribed);
- **keep any transition the import is blind to** as positive evidence that it mislabels the event.

*Worked example (load-bearing).* Abel–Ruffini "explains" the n=4→5 boundary as the solvable/non-solvable line — but it is structurally **blind** to the n=3→4 transition (none → quotient shape), which is the carrier's most important move and sits *entirely inside* the solvable region (S₃, S₄ both solvable). So solvability is the **wrong reading** of our transition; the honest object underneath is the **normal-subgroup lattice**, of which solvability is just one lossy projection. We then *measured* the wall ourselves — the derived series stalling at A₅ (CALC-11) — instead of citing the theorem. This is **Axiom 11** in practice: named theorems are domain articulations, not substrate. Full statements: Import-audit principle + Lattice frame in the Frontier map below.

---

**Workstream:** extend the Active Role-Jet / role-channel theory up the role-count axis (n = 3 onward) and characterise the invariant the coupling actually carries. **STATUS — central result PROVED for all n (CALC-14):** the realizable coupling carrier is the role-pair permutation module, and what any per-chart-magnitude summary discards is exactly the Specht module S^(n−2,2). The n = 3→4 extension that opened the workstream (CALC-01…10) is now a single case of a general theorem.

**Convention:** all arithmetic exact-ℚ (sympy `Rational`/`Matrix`). Certainty tiers inline: `[computer-verified]` (exact CAS on a specific instance), `[proven]` (exact algebraic fact / representation theory), `[noted]` (observation, not a theorem).

**Source framework — definitions live here, NOT in this log.** The DBP role-channel + Active Role-Jet papers in `/mnt/project/`: `role_channel_anisotropy.tex`, `dbp_orbit_calculus.pdf`, `self_glue_monodromy.pdf`. The keystone surfaces, A_c, and the §6 / §7.3 references throughout point into these. A reader new to "Active Role-Jet", "channel reduction", "graph Hessian", or "the carrier" should read those first (and the persona/register lives in memory, not here).

**Scripts (this directory):** `step1_carrier.py` (CALC-01…04) · `faithfulness.py` (05–07) · `loss_location.py` (08–09) · `resolvent_s3.py` (10) · `n5_test.py` (11) · `n6_test.py` (12) · `ladder_faithfulness.py` (13) · `prove_imL.py` (14). **Proof note (self-contained):** `imL_pair_module_theorem.md`.

**Full detail / transcripts:** this session (n=5…14 + the proof) is `2026-06-29-04-10-49-lloyd-dbp-role-pair-proof.txt`; the opening n=3→4 carrier work is `2026-06-29-02-02-48-lloyd-dbp-four-role-carrier.txt`. Computations below were run with the visible exact outputs recorded inline.

---

**BOTTOM LINE (current).** For all n ≥ 3, the realizable coupling carrier **`Im(L) ≅ M^(n−2,2) = triv ⊕ std ⊕ S^(n−2,2)`** — the permutation module of S_n on the C(n,2) role-pairs — **proved** (CALC-14, via: ker L = the defining-function gauge ⇒ Im(L) ≅ Sym²(std), whose character is the role-pair character). The per-role coupling magnitudes **(C) span the marginal `triv ⊕ std`**; the **loss** — what every magnitude-only summary discards — is exactly the **shape `S^(n−2,2)`**: *absent* at n=3 (A_c is then the whole story), the exceptional **quotient** doublet (2,2) at n=4 (the V₄ accident), and **faithful** for n ≥ 5 with faithfulness margin growing linearly as 2(n−3). Loss dim = n(n−3)/2. **A_c = 42793/1555848** (on the keystone `D²+DS+P²−3` at (1,1,1)) is the n=3 shadow of this structure. The n=4 reading — carrier forced to 12 components, minimal faithful carrier = 4 magnitudes + a (2,2) doublet — survives as standing conclusions 1 & 4, now corollaries rather than the headline.

---

## CALC-01 — §6 channel reduction, keystone retrodiction  (`step1_carrier.py`, P1)

**What:** implement the section-6 channel-density bordered-minor reduction (ambient implicit form) and reproduce the single-chart Gaussian decomposition on the keystone.
**Inputs:** `F = x₁² + x₁x₂ + x₃² − 3` at `(1,1,1)`. `g = (3,1,2)`, `q = gᵀg = 14`, `H` split into off-diagonal `H_c` + diagonal `H_s`.
**Results (all match the paper, exact):**
- `κ_c (t²) = −1/49`
- `κ_int (t·u) = −3/49`
- `κ_s (u²) = +1/49`
- `K_G = κ_c + κ_int + κ_s = −3/49`

**Tier:** `[computer-verified]`. Validates the §6 machinery.

---

## CALC-02 — Coupling carrier / A_c retrodiction — THE GATE  (`step1_carrier.py`, P2)

**What:** build the coupling carrier from the three per-output-chart graph Hessians and reproduce A_c. This is the gate that validates the carrier definition against the existing role-channel paper before any n=4 extension.
**Inputs:** `F = D² + DS + P² − 3` at `(1,1,1)`. Graph jets computed per output chart via the implicit second-derivative formula `f_jl = −(F_jl + F_jk f_l + F_kl f_j + F_kk f_j f_l)/F_k`.
**Results (exact, all match):**
- `κ_c^(P) = −25/196`
- `κ_c^(D) = −1/441`
- `κ_c^(S) = −1/49`
- `A_c = (κ_P−κ_D)² + (κ_D−κ_S)² + (κ_S−κ_P)² = 42793/1555848`  ← target hit exactly.

**Tier:** `[computer-verified]`. **GATE PASS.**

---

## CALC-03 — n=4 carrier (A): S₄ representation of the 12 components  (`step1_carrier.py`, P3)

**What:** carry the same rule to n=4. Each output chart now has 3 input-pairs, so a component is indexed by (output role k, input-pair) ≡ ordered pair `(k, ℓ)` of distinct roles (ℓ = excluded input). S₄ permutes the 12 ordered pairs. Decompose the module via character inner products with the five S₄ irreps.
**Results:**
- ordered-pairs permutation character `χ = (12, 2, 0, 0, 0)` over classes `(e, (12), (12)(34), (123), (1234))`.
- **12-dim module = trivial ⊕ 2·standard ⊕ (standard⊗sign) ⊕ (2,2)** — multiplicities `(1, 0, 2, 1, 1)` for `(triv, sign, std, std⊗sgn, 2dim)`. Dim check = 12.
- anisotropy (non-trivial) dimension = 11.
- n=3 comparison: 3-component module = `triv ⊕ std(2-dim of S₃)`, exactly **one** nontrivial irrep → A_c is the lone anisotropy invariant. The collapse to a single invariant is special to n=3.

**Tier:** `[proven]` (representation theory; character orthogonality, hand- and code-verified).

---

## CALC-04 — n=4 carrier on a concrete surface; isotypic populations  (`step1_carrier.py`, P4)

**What:** compute the 12 exact-ℚ carrier components on a minimal 4-role surface and project onto S₄ isotypic blocks (preliminary population evidence; Parseval check).
**Inputs:** `F = Σ y_i² + Σ_{i<j} y_i y_j − 65` (fully-coupled symmetric quadratic) at the asymmetric point `(1,2,3,4)`; gradient `(11,12,13,14)` (regular).
**12 carrier components (exact-ℚ), indexed (output, excluded):**
```
(0,1) -8836/12006225   (0,2) -361/592900     (0,3) -6241/12006225
(1,0) -529/893025      (1,2) -361/893025     (1,3) -5041/14288400
(2,0) -27889/67076100  (2,1) -5776/16769025  (2,3) -4489/16769025
(3,0) -6241/19448100   (3,1) -5329/19448100  (3,2) -529/2160900
```
**Isotypic norms ‖P_V v‖²:** trivial, standard, std⊗sgn, twodim all **nonzero**; sign **zero**. Parseval: isotypic norms sum to `‖v‖²` ✓.
**Caveat / superseded:** this projects the *squared* carrier at an *asymmetric* frame, so the std⊗sgn population here is a quadratic shadow, not independent realizable content (see CALC-08).

**Tier:** `[computer-verified, one surface]`.

---

## CALC-05 — n=3 faithfulness Jacobian retrodiction  (`faithfulness.py`, i)

**What:** sanity-check the Jacobian machinery by reproducing the paper's §7.3 carrier-faithfulness determinant at n=3.
**Inputs:** quadratic graph `P = f(D,S)` with symbolic 2-jet `(a,b,A,B,C)`, carrier `O = (κ_c^P, κ_c^D, κ_c^S)`.
**Results:**
- `det ∂O/∂(A,B,C) = 8 Λ_P Λ_D Λ_S / q₀⁶` with `Λ_P=B, Λ_D=(Ab−aB)/a, Λ_S=(Ca−bB)/b, q₀=1+a²+b²` — **symbolic match True**.
- rank 3 at generic jet `(a,b,A,B,C)=(2,3,1,5,7)` = dim(second jet) → faithful at n=3.

**Tier:** `[computer-verified]`. Validates the Jacobian setup used for the n=4 clinch.

---

## CALC-06 — n=4 faithfulness: carrier (A) vs (C) — THE CLINCH  (`faithfulness.py`, ii)

**What:** the second jet at n=4 (graph Hessian) is 6-dimensional. Faithfulness ⇔ carrier-map Jacobian has rank 6. Compare the pair-resolved carrier (A) against any per-chart-scalar carrier (C).
**Inputs:** quadratic 4-role surface, fixed generic 1-jet `(a₁,a₂,a₃)=(2,3,5)`, symbolic 6-entry Hessian, generic evaluation `H=(1,2,4,3,5,7)`.
**Results:**
- `dim(second jet) = 6`.
- **carrier (A): R⁶ → R¹², rank 6 → FAITHFUL.**
- **carrier (C): R⁶ → R⁴, rank 4 → NOT FAITHFUL.** Codomain dim 4 < 6 ⇒ rank ≤ 4 *everywhere* ⇒ (C) is faithful **nowhere** (not merely on a degeneracy locus).
- `ker(J_C)` is **2-dimensional**; both kernel directions are visible to (A) (`J_A · dir` nonzero in 11/12 components each). The information (C) discards is exactly what (A) retains.

**Tier:** `[computer-verified]` (ranks, exact) / `[proven]` (dimensional argument for (C)). **Carrier (A) is forced by the completeness criterion.**

---

## CALC-07 — Finite two-jet witness attempt  (`faithfulness.py`, iii)

**What:** try to exhibit two distinct Hessians with identical (C) but different (A) (the n=4 analog of the Kerr-Newman two-state demo), by moving along a `ker(J_C)` line.
**Result:** along the single kernel line tried, the only common return root of `(C)(s) − C₀` is `s = 0`. The §7.3 criterion is the *local-diffeomorphism / Jacobian* test, so the infinitesimal kernel (CALC-06) already establishes the failure rigorously. A genuine finite pair requires solving the 2-dim fiber `(C)(H) = (C)(H₀)` (4 eqns, 6 unknowns) rather than a straight kernel line — deferred.

**Tier:** `[noted]`.

---

## CALC-08 — Locating the loss: size vs shape, and Im(L) decomposition  (`loss_location.py`)

**What:** determine *where* the (C)-loss sits, at the S₄-**symmetric** first jet (gradient `(1,1,1,1)`, i.e. `a_i = −1`) so the active role action is a genuine linear S₄ representation and isotypic statements are exact.
**Key identity (by construction):** `(C)_k = −(1/q²) Σ_pairs Λ²` = **per-chart sum of squares of the coupling numerators** → (C) keeps each chart's coupling *magnitude*, discards within-chart *shape*. Verified.
**Results:**
- linear map `L: Hessian(R⁶) → numerators(R¹²)` has **rank 6** (injective); `J_A` rank 6, `J_C` rank 4, `ker(J_C)` dim 2 — consistent with CALC-06 at the symmetric jet.
- **Im(L) (realizable coupling numerators, 6-dim) = trivial ⊕ standard ⊕ (2,2)** — confirmed S₄-invariant subrep, dim check 6.
- (C) resolves `triv ⊕ std` (the 4 per-chart magnitudes, transforming as the 4-chart permutation rep).
- **THE LOSS sits entirely in the 2-dimensional (2,2) irrep** — lost dimension = 2, exactly `dim ker(J_C)`. One irreducible doublet, the whole of it.
- The (2,2) irrep **factors through S₄/V₄ ≅ S₃**: the lost shape coordinate is governed by the S₃ quotient of S₄.

**Tier:** `[computer-verified]` (exact-ℚ; isotypic projectors built from the S₄ permutation rep).

---

## CALC-09 — Constructive payoff: minimal faithful carrier  (`loss_location.py`, appended)

**What:** test whether (C)'s 4 magnitudes augmented with the (2,2) shape doublet is already faithful.
**Inputs:** augmented carrier `[ (C) (4) ; P_{(2,2)} κ (2-dim block) ]`, symmetric jet, generic Hessian.
**Result:** augmented Jacobian **rank 6 → FAITHFUL**. So the minimal faithful carrier = **4 magnitudes + 2 shape (the (2,2) doublet) = 6 = dim(second jet)**; the full 12 components of (A) are redundant.

**Refinement of earlier claim (CALC-03/04):** the abstract 12-component module has room for `2·std ⊕ std⊗sgn ⊕ 2dim`, but the *realizable* numerators occupy only `triv ⊕ std ⊕ (2,2)`. So the genuinely independent new content beyond the magnitudes is the **single (2,2) doublet**; the std⊗sgn seen in CALC-04 is a quadratic shadow of the (2,2)+magnitude data, not an independent invariant.

**Tier:** `[computer-verified]`.

---

## CALC-10 — Is the resolvent S₃ a third independent S₃?  (`resolvent_s3.py`)

**What:** the (2,2) shape doublet (CALC-08) is governed by an S₃. Test whether it is a *third independent* S₃ — like the monodromy-S₃ the self-glue paper found independent of role-S₃ (the S₃ × S₃ commuting pair) — or a quotient of the role group. Discriminator (the monodromy paper's own test): an S₃ is independent only if it acts on a set with no canonical bijection to the roles.
**Results:**
- V₄ = {e, (01)(23), (02)(13), (03)(12)} is exactly `ker(S₄ → Sym(3 partitions))`; quotient order 6 = |S₃|, surjective onto Sym(3 partitions). `[computer-verified]`
- Each double-transposition acts as the **identity** on the (2,2) block but **nontrivially** on the carrier overall and on the std blocks — the shape doublet sees only the quotient; V₄ does real work elsewhere. `[computer-verified]`
- Permutation rep on the three 2+2 partitions: character `(3,1,3,0,1)` = `triv ⊕ (2,2)`. So the (2,2) shape doublet **is** the standard rep of the resolvent S₃ on the partitions, V₄ its kernel. `[computer-verified]`
- Galois/monodromy bridge: `x⁴ − x − 1` (Gal S₄) → resolvent cubic `y³ + 4y − 1`, irreducible, discriminant −283 (non-square) → Gal = S₃ = S₄/V₄. The resolvent S₃ is realised as the monodromy of the resolvent cubic — but that monodromy is again S₄/V₄. `[computer-verified]`

**Verdict:** the resolvent S₃ is a *new* group (S₄/V₄, absent at n=3) but **NOT an independent** S₃. It is the role group's resolvent **quotient**, canonically determined by the role action (the partitions are built from the roles), unlike the monodromy-S₃ which acted on root-sheets with no canonical role-bijection. It IS genuinely the resolvent-cubic monodromy — a concrete bridge to cover/Galois machinery — but still role-determined. A genuinely independent factor (the n=4 analog of S₃ × S₃) would require a four-role branched cover, whose sheets are not role-canonical (→ F-list below).

**Tier:** `[computer-verified]` / `[proven]` (quotient-vs-independent is structural).

---

## CALC-11 — n=5 decisive test: loss goes faithful; solvability wall measured  (`n5_test.py`)

**What:** the decisive test of the Lattice frame at the lattice-collapse point. Compute the n=5 carrier (S₅, 30 components, 10-dim second jet), localize the loss, check whether it can stay quotient-shaped (frame says it **cannot** — S₅'s only proper quotient is Z/2, so only triv/sign factor through it). Companion: *measure* the solvability transition via the derived series (actual commutators), demoting the Abel–Ruffini import.
**Carrier results (S₅-symmetric jet, exact-ℚ):**
- rank L = 10 (injective), all Q_k = 5. rank J_A = 10 → **(A) faithful at n=5**. rank J_C = 5 → loss = 5-dim.
- **Im(L) (realizable numerators, 10-dim) = triv(5) ⊕ std(4,1) ⊕ (3,2)**. dim check 10.
- (C) resolves triv ⊕ std(4,1) (the 5 per-chart magnitudes).
- **LOSS = (3,2), a single 5-dimensional FAITHFUL irrep** — all 5 dims faithful, 0 quotient. Prediction (≥4 of 5 faithful) **CONFIRMED**, in fact all 5.

**Structural law (what the test surfaced).** The loss/shape is the Specht module **S^{(n−2,2)}**, the non-magnitude summand of `Im(L) = S^{(n)} ⊕ S^{(n−1,1)} ⊕ S^{(n−2,2)}` (trivial ⊕ standard ⊕ shape):
- n=3: (n−2,2) = (1,2) is not a valid partition → **no shape**; (C)=(A), no loss, A_c is the faithful whole story.
- n=4: (2,2), the **exceptional quotient** irrep (factors through S₄/V₄) → shape = quotient doublet (CALC-08/10).
- n≥5: faithful → shape = faithful irrep ((3,2) at n=5).
Loss dim = dim S^{(n−2,2)} = **n(n−3)/2** [confirmed n=4→2, n=5→5], and `1 + (n−1) + n(n−3)/2 = n(n−1)/2 = dim(2nd jet)` for all n. *[computer-verified at n=3,4,5; the all-n law is conjecture]*

**Derived series — solvability wall MEASURED (commutators, not citation):**
- S₃: orders [6, 3, 1] → solvable. S₄: [24, 12, 4, 1] → solvable. S₅: [120, 60] → **STALLS at A₅ (perfect)** → non-solvable.
- S₄'' = order 4 = **V₄** = the n=4 shape-quotient kernel (CALC-10). The carrier's shape mechanism *is* the second derived subgroup of S₄.

**Verdict.** The Lattice frame holds at its decisive point and predicted the transition; "loss = quotient doublet" was the n=4 V₄-accident, not a law. The shape survives for all n≥4 but changes character **quotient → faithful at exactly n=5** — the lattice-collapse / solvability-failure point. The carrier-shape is the **finer** reading: it transitions at *both* n=3→4 (none→quotient, solvability blind) and n=4→5 (quotient→faithful, solvability also fails). Two distinct projections of the lattice, carrier strictly finer — now confirmed at a second point. The Abel–Ruffini import (F2/F5) is demoted to a measured fact: the wall sits at n=5 for our role groups, produced on our own commutators.

**Tier:** `[computer-verified]` (n=5 carrier + derived series, exact) / `[conjecture]` (the all-n Specht S^{(n−2,2)} law).

---

## CALC-12 — n=6: Specht law confirmed (2nd faithful point); loss = role-pair module  (`n6_test.py`)

**What:** confirm the Specht loss law at a *second* faithful point. n=6 carrier (S₆, 60 components, 15-dim jet). The S₆ character table is built from scratch via **Murnaghan–Nakayama** and verified (dims {1,1,5,5,9,9,10,10,5,5,16}, sign character, all 11 norms = 1) before use — no transcribed table.
**Results (S₆-symmetric jet, exact-ℚ):**
- rank L = 15 (injective), all Q_k = 6. rank J_A = 15 → (A) faithful. rank J_C = 6 → loss = 9 = n(n−3)/2.
- Im(L) = triv(6) ⊕ std(5,1) ⊕ (4,2). dim 15.
- **LOSS = S^(4,2), single irrep, dim 9, FAITHFUL** — exactly predicted. Second faithful data point after (3,2) at n=5.
- S₆ derived series [720, 360] stalls at A₆ → non-solvable (wall persists).

**Upgrade — the clean form of the law.** Across n=4,5,6, `Im(L) = triv ⊕ std(n−1,1) ⊕ S^(n−2,2)`, which is exactly the decomposition of the **permutation module of S_n on the C(n,2) role-pairs**, M^(n−2,2) = ℂ[role-pairs]. So the realizable coupling carrier **is** the role-pair permutation module (dim C(n,2)); the n−2 chart-views of each pair are redundant (n·C(n−1,2) carrier components collapse to C(n,2) realizable). (C) keeps the **marginal** part triv ⊕ std (per-pair magnitudes summed to per-chart); the **loss is the S^(n−2,2) part** — absent at n=3 ((n−2,2) invalid → no loss, A_c whole story), the exceptional **quotient** (2,2) at n=4 (the V₄ accident), **faithful** for all n≥5 ((3,2), (4,2), …). Loss dim = dim S^(n−2,2) = n(n−3)/2.

**Tier:** `[computer-verified n=3,4,5,6]` (MN table independently verified) / `[conjecture]` (all-n; the role-pair-module identification makes it a clean target for a general proof, likely provable directly).

---

## CALC-13 — climbing past n=6: the faithfulness-margin pattern  (`ladder_faithfulness.py`)

**What:** climb past n=6 to (i) confirm the role-pair-module law at more rungs and (ii) ask whether "how faithful each rung is" forms a pattern. Cheap exact handle: the loss S^(n−2,2) has character `χ_shape(g) = C(fix,2) + #2cycles − fix` (= χ_pair − χ_triv − χ_std), an exact rep-theory identity.

**(A) Pair-module law — confirmed at n=7, 8.** rank L = C(n,2) and `χ_Im(L)(g) = χ_pair(g) = C(fix,2)+#2cycles` on *every* conjugacy class, for n=5,6,7,8. So Im(L) **is** the role-pair module M^(n−2,2) at n=4,5,6 (exact, CALC-08/11/12) and n=7,8 (numerically verified, integer-clean). Loss = S^(n−2,2) at every rung tested.

**(B) The faithfulness margin — a clean graded pattern.** Define `margin := dim − max_{g≠e} χ_shape(g)` (how far the nearest non-identity element is from acting trivially; 0 = unfaithful). Computed n=3..20:
- n=3: no shape rep (A_c whole story).
- n=4: kernel = **V₄** (order 4: identity + 3 double-transpositions), **not faithful, margin 0**.
- n≥5: kernel trivial, faithful, **margin = 2(n−3)** exactly — 4, 6, 8, 10, 12, … growing linearly.
The least-faithful element settles to a single transposition for n≥7 (`χ_shape = (n−3)(n−4)/2`, giving margin 2(n−3)).

**The pattern.** Faithfulness grows **linearly up the ladder** (margin 2(n−3)) — each rung strictly more robustly faithful — with a **singular collapse to 0 at n=4** (the margin sits *below* the extrapolated line: 0, not the 2 that 2(n−3) would give). The dip is the V₄ accident: at n=4 the double-transpositions form a normal subgroup **and** act trivially on S^(2,2) (which factors through S₄/V₄). This is the **same V₄** as the shape-quotient kernel (CALC-08/10) and S₄'' in the derived series (CALC-11) — one structure, three appearances.

**Tier:** margin = 2(n−3) and kernel = V₄-only-at-n=4 are `[proven]` rep-theory facts about S^(n−2,2) (χ_shape is its exact character); "loss = S^(n−2,2)" is `[computer-verified n=4..8; all-n conjecture]`.

---

## CALC-14 — PROOF: Im(L) ≅ role-pair module (conjecture → theorem)  (`prove_imL.py`, `imL_pair_module_theorem.md`)

**What:** prove the all-n conjecture (CALC-12/13) that the realizable coupling carrier is the role-pair permutation module. Reduces to two elementary facts; load-bearing steps verified n=4..9, proof general.

**Theorem.** For all n ≥ 3, `Im(L) ≅ M^(n−2,2) = ℂ[role-pairs] = triv ⊕ std ⊕ S^(n−2,2)` as S_n-reps.

**Proof (3 steps).** Numerator `Λ_{k,{j,l}}(H) = −(H_{jl} − H_{jk} − H_{kl} + H_{kk})` on ambient `H ∈ Sym²(ℝ^n)`; S_n-equivariant.
- **Step 1 [gauge].** `ker L = G = {v⊗g + g⊗v}` = the defining-function rescaling freedom `F → φF` (which shifts H by `∇φ⊗g + g⊗∇φ`). Proven by explicit construction `v_a = H_{a0} − ½H_{00}`. So `rank L = dim Sym²(ℝ^n) − n = C(n,2)`. *(verified n=4..7: rank L = C(n,2), ker dim = n, gauge generators independent and span ker)*
- **Step 2 [quotient].** `Im(L) ≅ Sym²(ℝ^n)/G ≅ Sym²(std)`, since `Sym²(ℝ^n) = triv ⊕ std ⊕ Sym²(std)` and G is exactly the g-involving part `Sym²(triv) ⊕ (triv⊗std)`.
- **Step 3 [character].** `χ_{Sym²std}(g) = ½(χ_std(g)² + χ_std(g²)) = C(fix,2) + #2cycles` = role-pair character. *(verified n=4..9)* So `Sym²(std) ≅ M^(n−2,2)`.
∴ `Im(L) ≅ M^(n−2,2)`. ∎

**Corollary (loss).** (C) (per-role coupling magnitude) spans the marginal `triv ⊕ std`; the **loss = S^(n−2,2)** for all n: absent n=3, quotient (2,2) at n=4, faithful n≥5 with margin 2(n−3) (CALC-13).

**Consequence.** Standing conclusion 6 is now `[proven for all n]`. The loss-shape law, the dimension n(n−3)/2, the quotient→faithful transition, and the faithfulness margin 2(n−3) with its V₄ dip — all CALC-08…13 empirics — were rep-theory facts about S^(n−2,2) awaiting this identification; they are now theorems.

**Tier:** `[proven]` (general proof; load-bearing steps computer-verified n=4..9).

---

## Standing conclusions (as of this log)

1. The n=4 coupling carrier is **forced** to be the 12-component pair-resolved object (faithfulness, CALC-06). `[proven]`
2. A_c is the n=3 shadow: S₃ is the unique role count whose carrier collapses to a single nontrivial irrep. `[proven]`
3. Any per-chart-magnitude summary (incl. §6's `κ_{2;2,0}` and the top-order Gauss-Kronecker reading) loses exactly a **2-dim (2,2) shape doublet**, governed by S₃ = S₄/V₄. `[computer-verified]`
4. Minimal faithful carrier = 4 magnitudes + (2,2) shape doublet = 6 components. `[computer-verified]`
5. The S₃ governing the shape doublet is the role group's resolvent quotient S₄/V₄ (= resolvent-cubic monodromy), **not** an independent third S₃; the monodromy-S₃ of the cubic self-glue *was* independent (S₃ × S₃) because it acts on root-sheets, not roles. `[computer-verified/proven]`
6. **The realizable coupling carrier is the role-pair permutation module** `Im(L) ≅ M^{(n−2,2)} = ℂ[C(n,2) pairs] = triv ⊕ std(n−1,1) ⊕ S^{(n−2,2)}`, **proved for all n** (CALC-14): `ker L` = the defining-function gauge `G = {v⊗g+g⊗v}`, so `Im(L) ≅ Sym²(ℝ^n)/G ≅ Sym²(std)`, whose character `C(fix,2)+#2cycles` is the role-pair character. (C) keeps the marginal (triv ⊕ std); **the loss is the shape S^{(n−2,2)}**: absent at n=3 (A_c whole story), exceptional **quotient** (2,2) at n=4 (V₄ accident), **faithful** for n≥5 with margin 2(n−3). Loss dim = n(n−3)/2. `[proven for all n; load-bearing steps computer-verified n=4..9]`
7. **Solvability wall measured on our own commutators** (not Abel–Ruffini): derived series of S₃ [6,3,1], S₄ [24,12,4,1] solvable; S₅ [120,60] stalls at A₅. S₄'' = V₄ = the carrier's shape-quotient kernel. Carrier-shape is the *finer* reading of the normal-subgroup lattice — it transitions at n=3→4 (solvability blind) as well as n=4→5. `[computer-verified]`
8. **Faithfulness of the loss is graded, not binary:** margin (distance of nearest non-identity element from acting trivially) = **2(n−3)** for n≥5 — linear growth, each rung strictly more faithful — with a **singular dip to 0 at n=4** (the V₄ collapse, below the line). Same V₄ as conclusions 3/5/7. Pair-module law confirmed n=4..8. `[proven for S^(n−2,2); loss identity computer-verified n=4..8]`

## Open / next (not yet computed)
- Finite two-state witness against the (2,2) shape invariant (distinct shape, identical magnitude) — the named-invariant n=4 analog of the Kerr-Newman demo.
- Characterize the n=4 isotropy locus where `J_A` drops below rank 6 (factor a 6×6 minor → the n=4 analog of `8Λ_PΛ_DΛ_S/q₀⁶`).
- Prove the (2,2) content nonzero on a Zariski-dense set (genericity, beyond the single surface of CALC-04).
- Physical 4-charge instance where the (2,2) shape coordinate is a live diagnostic.
- **Path-native solvability/lattice derivation** (demotes the Abel–Ruffini imports in F2/F5): compute the normal-subgroup lattice of the role group `S_n` and the *full* derived series of `Sym(m) ≀ Sym(m)` as n,m grow; derive *both* the carrier-quotient mechanism and the solvability filtration from the lattice ourselves; locate every transition, including ones solvability is blind to (n=3→4). Confirm or refute that the wall sits at n=5 / m=5 for our specific modules rather than for bare S_n.

## Frontier map — single-direction cuts and their blank margins

Survey of where the computation walked one axis hard and left the transverse territory unmapped. Each `F#` is a standing return target. Tags mark what is already proven vs. genuinely open. The "Open / next" list above is the near-term tactical subset; this is the strategic survey.

**Meta-shape.** The project has a strong line along **r = 2, n ≤ 4, separable, solvable** — everything clean lives in the solvable corner of symmetric-group structure. Two stacked accidents hold it together: A_c being a single invariant (n=3, S₃ multiplicity-free) and the loss living in a small quotient (n=4, V₄ ◁ S₄). The unmapped territory is everything *transverse* to that line. I earlier called the n=4→5 boundary "the solvable/non-solvable line of classical Galois theory" — **that is an imported reading, flagged below (F2/F5).** The candidate *complete* object underneath both walls is the **normal-subgroup lattice of the role group**, of which solvability and the carrier-quotient mechanism are two distinct projections (Lattice frame, next).

**Import-audit principle (standing).** A named theorem imported as substrate carries the *conclusion* of a different investigative path; jumping to it can rob us of what searching our own space would find. When an import names one of our transitions, demote it to a navigation target, reproduce the phenomenon with our own machinery, and keep any transition the import is *blind to* as evidence it mislabels the event. Cf. Axiom 11 (named theorems are domain articulations, not substrate).

**Lattice frame (working hypothesis, not a result).** Both transitions we can actually see are readings of the role group's normal-subgroup lattice: S₃ has only {1, A₃, S₃}; S₄ **gains the normal V₄** (and A₄) — exactly the V₄ whose quotient S₄/V₄ ≅ S₃ carries the (2,2) shape doublet (CALC-10); S₅ collapses it (nothing proper but the simple A₅). So **n=3→4 = lattice gains V₄ → carrier gains the shape doublet, solvability unchanged**; **n=4→5 = lattice collapses → resolvent mechanism lost *and* solvability fails, simultaneously**. Solvability and the carrier-quotient mechanism are therefore *distinct* readings of one lattice — they **diverge** at n=3→4 (carrier moves, solvability blind) and only **coincide** at n=4→5 where the lattice itself collapses. Not two halves of each other; two projections of the lattice. *[both transitions verified — CALC-03/08/10 + solvability of S₃,S₄; lattice-as-common-source is a working frame on 2 data points]*

**F1 — Order axis r (largest blank by area).** All results are r=2 (Gaussian). The channel bipolynomial `Ĉ_r(t,u)` is defined for all 1 ≤ r ≤ n−1; only the r=2 line is ever evaluated. Unmapped: r=1 (mean-curvature channels), r ≥ 3, the conjectured parity law (ℚ for even r, ℚ(√q) for odd — untested past r=2), a generating function `Σ_r Ĉ_r s^r`, and the kernel of Σ above the zero-sum plane. *[object defined; tower unmapped]*

**F2 — Role axis n, and the solvability cliff at n=4→5.** Walked 3→4, stopped. Deeper miss: the n=4 cleanliness is an exceptional-group accident. The loss factoring through S₄/V₄ ≅ S₃ exists *because* V₄ ◁ S₄. S₅ has no proper normal subgroup but A₅; its only abelian quotient is Z/2 (sign). So "loss governed by a small symmetric quotient" appears to break at n=5. **⚠ Import flag (Abel–Ruffini):** the "cannot survive to n=5" reading is *imported* (classical Galois road), not produced on our path, and it **mislabels** the event — our actual n=3→4 transition lives *entirely inside* the solvable region (S₃, S₄ both solvable), so solvability is structurally blind to it. The real driver is the normal-subgroup lattice (Lattice frame above), not solvability per se. Pending: path-native derivation (Open list). **→ DISCHARGED in CALC-11:** the wall is now *measured* (derived series stalls at S₅, on our own commutators), and the carrier transition is shown finer than solvability — the shape is the Specht module S^{(n−2,2)}, quotient at n=4, faithful at n=5. *[the bare-S_n facts are proven group theory; that solvability is the right reading of OUR transition is refuted at n=3→4; the carrier law is computer-verified at n=3,4,5]*

**F3 — Degeneracy loci: ranks, never varieties.** Faithfulness reported "rank at a generic point" throughout. At n=3 we had the exact locus `Λ_P Λ_D Λ_S = 0` (four lines); at n=4 we never factored the degeneracy variety (the analog of `8 Λ_P Λ_D Λ_S / q₀⁶` — a 6×6 minor of `J_A`). The isotropy-locus dimension law `dim Z_Σ = 2 − r` is an n=3 statement, never lifted. The boundary where structure fails is the actual geometry, and it is blank. *[generic ranks have; boundary varieties unmapped]*

**F4 — The local↔global isthmus.** The residue↔cycle-type bridge — A_c's pole residue at a role boundary ↔ the monodromy cycle type at that ramification locus — is named as open in the role-channel, GTD, *and* monodromy papers, computed in none. The papers assert local and global are "a quotient and its total space," but the projection map itself is uncomputed. *[named in 3 papers; never calculated]*

**F5 — Separable→non-separable and solvable→non-solvable walls (monodromy side).** Wreath laws mapped only for separable pure-power surfaces (the Lemma C strip). Non-separable cross-terms: does seam-imprimitivity survive or shatter? Named open, never probed. Independent solvability cliff: `Sym(m) ≀ Sym(m)` contains A_m, non-solvable for m ≥ 5; the cubic's `S₃ ≀ S₃` is solvable; the "backward/expensive non-abelian part" is qualitatively different above m=4, only measured at m ≤ 3. The abelianization was pinned ((Z/2)² always) — but abelianization is **blind** to solvability; we read the one invariant that doesn't see the cliff. **⚠ Import flag (Abel–Ruffini), partial:** F5 is *closer to native* than F2 — solvability here is a property of the derived series of `Sym(m) ≀ Sym(m)`, the actual group we built, and we already computed its first rung (abelianization (Z/2)²). But the paper's native questions were abelianization + imprimitivity, not "solvable y/n", so "non-solvable for m ≥ 5" is still imported framing. Path-native move: compute the *full* derived series for m = 2..6 and locate where it stops terminating — measure the transition in our object instead of citing it. *[m ≤ 3 measured; full derived series + m ≥ 5 + non-separable unmapped]*

**F6 — The ambient-curvature wall: never walked along.** R^T doesn't channelize (not bilinear in the shape operator) — a proven, bounded wall. We stopped at it facing forward. Never walked along it: are there special ambients (constant curvature, Einstein, symmetric spaces) where R^T *does* split, or where the obstruction itself carries channel structure? A wall with its length unmapped may have a gate. *[wall proven; its length / possible gates unmapped]*

**F7 — Points standing in for maps.** Nearly every n=3 claim (nowhere-isotropic, the gauge-transport laws, A_c > 0) is witnessed on the *single* keystone surface; the n=4 (2,2) population on one surface, one point. "Generic" is asserted, never shown Zariski-dense. We have pins, not a chart of the surface moduli — and the difference matters exactly where a pin happens to sit on a special locus we haven't identified. *[pins have; moduli chart blank]*

<!-- ───────── APPEND NEW CALCULATIONS BELOW THIS LINE (CALC-15, …) ───────── -->
