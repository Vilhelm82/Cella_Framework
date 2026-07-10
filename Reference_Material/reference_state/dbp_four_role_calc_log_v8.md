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

## CALC-15 — order axis r: the parity law is the normalization; no new rep structure this way  (`order_axis_v1.py`)

**What:** open the order axis (F1, the largest frontier blank). Generalise the channel density `Ĉ_r(t,u)` — the role-channel paper's **§8** higher-order conjecture (the r=2 `(t,u)`-reduction itself traces to the orbit-calculus foundational paper, not role-channel §6) — bordered minors of `M = tH_c + uH_s` (H_c off-diagonal/coupling, H_s diagonal/self), normalised by `q^((r+2)/2)`, from the hardcoded top order `r=n−1` to arbitrary r. Gate, then compute r=1..4 and test the paper's conjectured parity law (`role_channel_anisotropy.tex` §8: ℚ for even r, ℚ(√q) for odd r).

**Gates (retrodiction, exact).** GATE-A ambient `Ĉ_2` on the keystone → −1/49, −3/49, +1/49, K_G=−3/49 ✓. GATE-B per-chart `Ĉ_2` on the A_c surface → κ_c^{P,D,S} = −25/196, −1/441, −1/49, A_c = 42793/1555848 ✓. Parametric machinery validated against both prior results.

**Parity law — CONFIRMED, and it is the normalization (not a deep arithmetic fact).** On a concrete n=5 surface, q = 495 = 9·55 (√q = 3√55 irrational): every coefficient of `Ĉ_1`, `Ĉ_3` lies in ℚ(√q); every coefficient of `Ĉ_2`, `Ĉ_4` lies in ℚ. **Mechanism (structural, proven):** the bordered-minor total is a polynomial in the rational jet, so the field is fixed entirely by `norm = q^((r+2)/2)` — an integer power of q for even r (→ ℚ), and `q^k·√q` for odd r (→ ℚ(√q)). Odd-r coefficients are **pure** √q multiples (no rational part), and √q does not cancel (leading coupling ≠ 0). Geometrically this is the even/odd mean-curvature dichotomy: even orders clear the normal normalization, odd orders carry one factor of the unit normal (the √q).

**Order-r role anisotropy `A_c^(r)` (= std-irrep norm² of the per-chart t^r coupling family):** nonzero for r=2,3,4 and **rational for all r** — including r=3, where the densities themselves carry √q — because `A_c^(r)` is degree-2 in the densities and a pure-√q term clears under squaring. So the parity √q lives at the *oriented-density* level and is **invisible to the anisotropy invariant** (rational at every order). The √q is a feature of signed curvature, not of the role variance.

**Honest verdict — what the order axis did and did not give.** The paper's named conjecture is discharged (true, but it is the normal-bundle √q, not an arithmetic miracle), measured on our own machinery and explained. But the per-chart std-norm anisotropy **stays in the same irrep (std) at every order** — climbing r this way surfaces **no new representation structure**, in sharp contrast to the role axis (→ Sym²(std), deeper Specht modules). The genuine open frontier on the order axis is the **order-r per-(chart, (r+1)-subset) coupling carrier** — an r×r coupling minor of the Hessian, a degree-r (nonlinear) object — whose S_n-content *could* carry the deeper Specht modules S^(n−r,r). That is a design problem, not a quick computation, and is the real (r,n)-plane work.

**Tier:** gates `[computer-verified]`; parity law `[computer-verified on n=5; normalization mechanism proven]`; `A_c^(r)` rational `[computer-verified; squaring-clears-√q proven]`; the deeper-rep order-r carrier `[open design problem]`.

**CALC-15a — cross-check against the compiled role-channel PDF (`verify_against_paper.py`).** The PDF was uploaded mid-session (it was *not* in `/mnt/project/` at start — only the `.tex` was); this re-verifies the machinery against the paper's exact numbers now that the compiled source is in hand. Confirmed exactly: Def-1 channel triple (Λ_P,Λ_D,Λ_S) = (−5/4, 1/6, 1/2); κ_c = (−25/196, −1/441, −1/49); A_c = 42793/1555848. **Remark 1 (§5) precision:** the paper warns the *plain* bordered Hessian is a different (Gauss–Kronecker-type) invariant, not the coupling channel — verified (it returns ±1/2 on chart P, ≠ Λ_P = −5/4). Our graded `Ĉ_r` is on the right side of this: at u=0 only `H_c` survives, and the t²-coefficient returns −25/196 = κ_c^P, so the `(t,u)`-grading is exactly what recovers the coupling channel. **Design consequence for the v2 order-r carrier:** use **coupling-mode (`H_c`) minors** (the t^r part), never full bordered Hessians, or it computes the Gauss–Kronecker object the paper rules out. `[computer-verified against PDF]`

---

## CALC-16 — characteristic axis: Campaign H's char-2 boundary generalises to all n  (`char2_generalization.py`)

**Context.** Will's parallel **Campaign H** (uploaded `CHAR2_BOUNDARY_REPORT.md`, `RAW_CHART_ROLECHSPEC_REPORT.md`; CL-H8/H9/H10) studies the *same carrier as CALC-14*, at n=3, on a new axis: **field characteristic**. Their gauge `G_g(a) = g_i a_j + g_j a_i` **is** our gauge `G = {v⊗g + g⊗v}` (v=a); their "carrier O" = `Sym₃/Im(G_g)` is our `Im(L)` at n=3; their faithfulness CL-H4 is the n=3 case of CALC-14, reached by an independent route (explicit minors, Gröbner saturation) — **independent corroboration**. Campaign H finds: faithful over char ≠ 2; a *derived* wall at char 2 (gauge goes diagonal-blind, carrier jumps 3→4-dim); resolved by a **phantom** `g gᵀ` that escapes the char-2 gauge image but stays invisible (CL-H10).

**What:** test whether the char-2 boundary generalises to all n, as the CALC-14 gauge structure predicts.

**Verified (n=3..7, exact, general symbolic g):**
- char ≠ 2: gauge rank = n (CALC-14 step 1) → carrier `Sym²(ℝ^n)/G` = C(n,2)-dim.
- char 2: the diagonal action `2g_i a_i` vanishes; the off-diagonal kernel condition flips from `g_i a_j = −g_j a_i` (forces a=0 over ℚ) to `g_i a_j = +g_j a_i` (allows a ∝ g), so the gauge **rank drops n → n−1**, kernel = ⟨g⟩. (Confirmed: `M·g = 2g_ig_j ≡ 0 mod 2`; some (n−1)-minor odd; all n-minors even.)
- the **phantom** `g gᵀ = G_g(g/2)` has diagonal `g_i²`, absent from the (purely off-diagonal) char-2 gauge image → independent, **restores exactly 1 dimension**.
- **Net: the carrier is C(n,2)-dimensional in EVERY characteristic, for all n.** The wall is the −1→+1 sign flip; the phantom `g gᵀ` (the pure defining-function-rescaling direction v∝g, = the `Sym²(triv)` gauge summand at the symmetric jet) restores the lost dimension.

**Relation to Campaign H / what remains.** This generalises the *gauge/carrier-dimension* skeleton of CL-H8/H9 (n=3) to all n. The remaining piece — that RoleChSpec is actually **faithful** on this C(n,2)-dim carrier in char 2 (i.e. the channel map's char-2 kernel is *exactly* `gauge ⊕ ⟨g gᵀ⟩`, the all-n analog of CL-H10) — needs the channel engine reduced mod 2 and is **not** checked here.

**Tier:** gauge/carrier dimension `[computer-verified n=3..7; mechanism proven]`; all-n RoleChSpec faithfulness in char 2 `[open — CL-H10 analog]`.

---

## CALC-17 — Campaign H spine (H1–H5) audited; the O-parity; compilation status  (`verify_campaignH_parity.py`)

**Context.** Uploaded Campaign H docs (`GAUGE_NORMAL_FORM_PROOF`, `SYMBOLIC_ROLECHSPEC_FORMULAS`, `INJECTIVITY_IDEAL_REPORT`, `EXCEPTIONAL_LOCUS_REPORT`) = the full **n=3** faithfulness proof: H1 (unique gauge-normal form `H_perp`: zero diagonal, off-diag = obstruction `O`; `Sym₃/Im(G_g) ≅ ℚ³`), H2 (RoleChSpec gauge-invariant), H3 (closed `(g,O)` formulas + the O-parity), H4 (injectivity via r=1 linear recovery, 6×3 rank 3), H5 (exceptional locus → char ≠ 2, the `32 = 2⁵` obstruction).

**Audit (our own channel engine, gauge-normal coords, exact).** κ_int = 0 every chart ✓; **O-parity** r=1 ODD / r=2 EVEN in O ✓; r=1 coefficient matrix rank 3 (injective) ✓; coupling-rows minor numerator carries the constant `32 = 2⁵` (char ≠ 2 obstruction) ✓ — modulo our `q^((r+2)/2)` normalization vs Campaign H's channel normalization (exact minor differs by normalization; substance agrees). **Campaign H's spine is independently confirmed.**

**Cross-connections.**
- H1–H5 (n=3) = the n=3 case of CALC-14 (all-n role-pair module), via a **third independent route** (gauge-normal form + linear recovery) — alongside CALC-14's character argument and the role-channel paper's Prop 1.
- **A second parity, distinct from CALC-15's.** Campaign H's **O-parity** — the order-r density is degree-r in the carrier O, hence EVEN in O for even r (blind to `O ↦ −O`) / ODD for odd r (resolves it) — is the load-bearing fact for **injectivity**: r=1 (odd) fixes the O-sign that r=2 (even) cannot. This is *not* CALC-15's **field-parity** (coeffs ℚ for even r / ℚ(√q) for odd r, = the `q^((r+2)/2)` normalization). Two real parity-by-r structures, one in the carrier, one in the field; the §8 conjecture names the field one, Campaign H found the injectivity one.

**Compilation status (Will's question).** Campaign H is **not** in the role-channel paper. The paper proves n=3 faithfulness via **Prop 1** (the `(A,B,C)→(Λ)` linear iso, det = −1) in **jet** coords and removes poles via the **projective normal** — different machinery. Campaign H = the gauge-theoretic reformulation + the §8 `Ĉ_r` conjecture made concrete (paper: "stated as targets; none verified here") + the **characteristic axis** (absent from the paper). [Orbit-calculus paper `dbp_orbit_calculus.pdf` not re-read this session; the gauge/bordered-minor machinery may partly live there.]

**Synthesis target.** Three parallel n=3 treatments now agree — paper Prop 1 / Campaign H H1–H5 / CALC-14. Unification = **all-n RoleChSpec injectivity at general g** (the all-n H1–H5) + the **all-n char-2 faithfulness** (CL-H10 analog); CALC-14 (gauge quotient, symmetric jet) + CALC-16 (char-2 dimension, all n) are the partial scaffold.

**Tier:** Campaign H spine `[computer-verified — independent re-derivation]`; the two parities `[computer-verified]`; compilation status `[assessment]`.

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

**F1 — Order axis r (largest blank by area).** All results are r=2 (Gaussian). The channel bipolynomial `Ĉ_r(t,u)` is defined for all 1 ≤ r ≤ n−1; only the r=2 line is ever evaluated. Unmapped: r=1 (mean-curvature channels), r ≥ 3, the conjectured parity law (ℚ for even r, ℚ(√q) for odd — untested past r=2), a generating function `Σ_r Ĉ_r s^r`, and the kernel of Σ above the zero-sum plane. **→ PARTIALLY MAPPED in CALC-15:** `Ĉ_r` generalised to all r (gated on keystone + A_c); parity law **confirmed and explained** — it is exactly the `q^((r+2)/2)` normalization (the normal-bundle √q at odd order), not a deep arithmetic fact; the order-r role anisotropy `A_c^(r)` is rational and nonzero at every order (the √q is invisible to the squared invariant). What this **left open and reframed**: climbing r via per-chart std-norm surfaces no new representation content (stays in std). The live order-axis target is now the **order-r per-(chart, (r+1)-subset) coupling carrier** (r×r coupling minor, degree-r/nonlinear), whose S_n-content could carry the deeper Specht modules S^(n−r,r) — the genuine (r,n)-plane analog of the role-axis theorem. *[r=1..4 mapped; parity discharged; the deeper order-r carrier is an open design problem]*

**F2 — Role axis n, and the solvability cliff at n=4→5.** Walked 3→4, stopped. Deeper miss: the n=4 cleanliness is an exceptional-group accident. The loss factoring through S₄/V₄ ≅ S₃ exists *because* V₄ ◁ S₄. S₅ has no proper normal subgroup but A₅; its only abelian quotient is Z/2 (sign). So "loss governed by a small symmetric quotient" appears to break at n=5. **⚠ Import flag (Abel–Ruffini):** the "cannot survive to n=5" reading is *imported* (classical Galois road), not produced on our path, and it **mislabels** the event — our actual n=3→4 transition lives *entirely inside* the solvable region (S₃, S₄ both solvable), so solvability is structurally blind to it. The real driver is the normal-subgroup lattice (Lattice frame above), not solvability per se. Pending: path-native derivation (Open list). **→ DISCHARGED in CALC-11:** the wall is now *measured* (derived series stalls at S₅, on our own commutators), and the carrier transition is shown finer than solvability — the shape is the Specht module S^{(n−2,2)}, quotient at n=4, faithful at n=5. *[the bare-S_n facts are proven group theory; that solvability is the right reading of OUR transition is refuted at n=3→4; the carrier law is computer-verified at n=3,4,5]*

**F3 — Degeneracy loci: ranks, never varieties.** Faithfulness reported "rank at a generic point" throughout. At n=3 we had the exact locus `Λ_P Λ_D Λ_S = 0` (four lines); at n=4 we never factored the degeneracy variety (the analog of `8 Λ_P Λ_D Λ_S / q₀⁶` — a 6×6 minor of `J_A`). The isotropy-locus dimension law `dim Z_Σ = 2 − r` is an n=3 statement, never lifted. The boundary where structure fails is the actual geometry, and it is blank. *[generic ranks have; boundary varieties unmapped]*

**F4 — The local↔global isthmus.** The residue↔cycle-type bridge — A_c's pole residue at a role boundary ↔ the monodromy cycle type at that ramification locus — is named as open in the role-channel, GTD, *and* monodromy papers, computed in none. The papers assert local and global are "a quotient and its total space," but the projection map itself is uncomputed. *[named in 3 papers; never calculated]*

**F5 — Separable→non-separable and solvable→non-solvable walls (monodromy side).** Wreath laws mapped only for separable pure-power surfaces (the Lemma C strip). Non-separable cross-terms: does seam-imprimitivity survive or shatter? Named open, never probed. Independent solvability cliff: `Sym(m) ≀ Sym(m)` contains A_m, non-solvable for m ≥ 5; the cubic's `S₃ ≀ S₃` is solvable; the "backward/expensive non-abelian part" is qualitatively different above m=4, only measured at m ≤ 3. The abelianization was pinned ((Z/2)² always) — but abelianization is **blind** to solvability; we read the one invariant that doesn't see the cliff. **⚠ Import flag (Abel–Ruffini), partial:** F5 is *closer to native* than F2 — solvability here is a property of the derived series of `Sym(m) ≀ Sym(m)`, the actual group we built, and we already computed its first rung (abelianization (Z/2)²). But the paper's native questions were abelianization + imprimitivity, not "solvable y/n", so "non-solvable for m ≥ 5" is still imported framing. Path-native move: compute the *full* derived series for m = 2..6 and locate where it stops terminating — measure the transition in our object instead of citing it. *[m ≤ 3 measured; full derived series + m ≥ 5 + non-separable unmapped]*

**F6 — The ambient-curvature wall: never walked along.** R^T doesn't channelize (not bilinear in the shape operator) — a proven, bounded wall. We stopped at it facing forward. Never walked along it: are there special ambients (constant curvature, Einstein, symmetric spaces) where R^T *does* split, or where the obstruction itself carries channel structure? A wall with its length unmapped may have a gate. *[wall proven; its length / possible gates unmapped]*

**F7 — Points standing in for maps.** Nearly every n=3 claim (nowhere-isotropic, the gauge-transport laws, A_c > 0) is witnessed on the *single* keystone surface; the n=4 (2,2) population on one surface, one point. "Generic" is asserted, never shown Zariski-dense. We have pins, not a chart of the surface moduli — and the difference matters exactly where a pin happens to sit on a special locus we haven't identified. *[pins have; moduli chart blank]*

**F8 — Characteristic / field-of-definition axis (opened by Campaign H; extended in CALC-16).** All CALC results are over ℚ (char 0). Campaign H (Will's parallel n=3 work, CL-H8/H9/H10) walks the characteristic: faithful over char ≠ 2; a *derived* wall at char 2 (gauge diagonal-blind, the −1→+1 kernel sign flip), resolved by the phantom `g gᵀ`. CALC-16 generalised the gauge/carrier-dimension skeleton to all n (carrier C(n,2)-dim in every characteristic). Unmapped: the **all-n RoleChSpec faithfulness in char 2** (CL-H10 analog — is the channel map's char-2 kernel exactly `gauge ⊕ ⟨g gᵀ⟩`?); **other primes** (char 3, p) and the **modular representation theory** of the carrier — does `S^(n−2,2)` stay irreducible mod p, and do new phantoms appear at primes dividing structure constants?; the interaction of the characteristic axis with the role-count axis (where the carrier decomposition itself can change mod p). *[char-2 gauge/carrier dimension mapped all n; RoleChSpec char-2 faithfulness all-n + modular rep theory open]*

<!-- ───────── APPEND NEW CALCULATIONS BELOW THIS LINE (CALC-23, …) ───────── -->

## CALC-18 — Prime-2 structure: validation of the three-task Codex spec (∧² absent from the linear carrier; integral carrier ℤ/2; ∧² realized at degree 2 — corrects CALC-15)

**Context.** Will crystallised the unifying thesis: the carrier is `Sym²(std)`; every fault line is where symmetric-square information loses sign / orientation / faithfulness; the prime 2 is the boundary between coupling-as-magnitude (`Sym²`) and coupling-as-oriented-structure (`∧²`), via the swap involution `τ` on `std⊗std` (clean over ℤ[1/2], degenerate at 2). Before handing Codex the three-task probe (`codex_task_dbp_prime2_structure.md`), validated each task's load-bearing computation in-container (`validate_three_specs.py`). Murnaghan–Nakayama irreducible characters built from scratch and norm-checked before use.

**Finding 1 — the alternating companion is absent from the linear carrier.** *[computer-verified, n=4..7]*
`∧²(std)` has character `½(χ_std² − χ_std∘sq)` and decomposes as the single irreducible `S^(n−2,1,1)` (‖·‖²=1, dim `C(n−1,2)`). Inner product `⟨χ_{Im(L)}, χ_{S^(n−2,1,1)}⟩ = 0` for n=4..7 → the linear coupling carrier `Im(L) = Sym²(std) = triv ⊕ std ⊕ S^(n−2,2)` contains **no** alternating content. The orientation half is not in `Im(L)`; "coupling as oriented structure" has no carrier at first order.

**Finding 2 — the integral carrier is `ℤ^{C(n,2)} ⊕ ℤ/2`, the ℤ/2 = the phantom, uniform in n.** *[computer-verified, n=4..7]*
Smith normal form over ℤ of the gauge inclusion `M_G : ℤ^n → Sym²(ℤ^n)` (columns `G_g(e_a)` at `g=(1,…,1)`, entry `a_k+a_l`) gives invariant factors `[1,…,1,2]` — exactly one factor of 2 — for **every** n=4,5,6,7. Hence `Sym²(ℤ^n)/Im(G_g) ≅ ℤ^{C(n,2)} ⊕ ℤ/2`, generator the phantom `[g gᵀ]` (`2·g gᵀ = G_g(g) ∈ Im`, but `g gᵀ ∉ Im` over ℤ — needs `a=g/2`). So the char-2 phantom (Campaign H, CL-H10) **is** the 2-torsion of the integral carrier — the char-0 / char-2 stories are one lattice fact. Critically the torsion is the **same ℤ/2** at n=4 as at n≥5 — no spike at n=4 → evidence the phantom and the n=4 V₄ quotient are **distinct** 2-phenomena (uniform lattice torsion vs. an n=4 representation accident), *not* a single fact. [The full-`L` cokernel + the V₄ / modular reconciliation is the open T1 / T3 extension.]

**Finding 3 — CORRECTION to CALC-15: `∧²(std)` IS reachable from the symmetric Hessian, at degree 2.** *[computer-verified, n=5,6]*
Plethysm screen `⟨χ_{Sym^r(Sym²std)}, χ_{S^(n−2,1,1)}⟩` = **1** at r=2, and **8** (n=5) / **10** (n=6) at r=3. The alternating companion **appears in the degree-2 invariants of the coupling** and grows thereafter. CALC-15 concluded "climbing r surfaces no new representation content (stays in std)" — that verdict measured only the per-chart **std-norm**, a single scalar that by construction sees only triv⊕std. The full degree-2 content (`Sym²(Sym²std)`) is rich and already carries `S^(n−2,1,1)`. **The order axis is not shallow; CALC-15 tunneled on the wrong observable.** F1 reopens: live targets are the explicit degree-2 coupling invariant realising the alternating piece, and the full `Sym²(Sym²std)` decomposition (T2 extension).

**Refined thesis (to confirm / refute via the Codex tasks).** The prime 2 governs **three distinct layers**, not one: (a) the `ℤ/2` lattice torsion `[g gᵀ]` = the char-2 phantom, uniform in n; (b) the degree at which the alternating companion `S^(n−2,1,1)` enters the local invariants — degree 2, *not* the monodromy; (c) the 2-modular behaviour of the Specht modules `S^(n−2,2)` / `S^(n−2,1,1)`, where magnitude and orientation may or may not collide — with the n=4 V₄ accident belonging to layer (c), not (a). The thesis "every fault line is one fact" is too strong; the correct statement is a stratification across these three layers.

**Artifacts.** `validate_three_specs.py` (in-container validation, char tables built + norm-checked); `codex_task_dbp_prime2_structure.md` (the three-task spec — T1 integral torsion / phantom-vs-V₄; T2 realise `∧²` as explicit degree-2 invariant + full `Sym²(Sym²std)`; T3 2-modular collision). Each Codex task carries the validated gate above plus an open extension.

## CALC-19 — CORRECTION to CALC-18 Finding 2: the phantom ℤ/2 is gauge non-saturation (lives in ker L), not a torsion of the realised carrier Im(L) — which is torsion-free (Codex T1, independently reverified)

**Trigger.** Codex executed T1. Gate reproduced the gauge-inclusion SNF `[1,…,1,2]` exactly (n=4..7), confirming CALC-18 Finding 2's *gauge* computation. The T1 **extension** (full carrier `L` over ℤ, n=4..8) returned: `coker(L)` **torsion-free** — SNF(L) all-unit nonzero invariant factors, no ℤ/2, no n=4 spike. Reverified independently in-container (`verify_T1_fullL.py`, n=4,5,6): `rank(L)=C(n,2)`, SNF(L) nonunit factors `= []`, `L·(g gᵀ)=0` over ℤ, `L·gauge=0`.

**Resolution — two presentations of the carrier that agree over ℚ and split over ℤ by the phantom.**
- **Quotient model** `Sym²(ℤⁿ)/gauge_ℤ`: torsion `ℤ/2` (gate). Generator `[g gᵀ]`; the torsion is exactly the non-saturation `sat(gauge)/gauge ≅ ℤ/2` (`2·g gᵀ = G_g(g) ∈ gauge` but `g gᵀ ∉ gauge`).
- **Image model** `Im(L_ℤ) ⊂ flags`: torsion-free, saturated (SNF all 1). `ker(L_ℤ)` is saturated (kernels of integer maps always are) and `L` annihilates `g gᵀ`, so `ker(L_ℤ) = sat(gauge) ⊋ gauge`. `L` quotients by the **saturated** gauge → `Im(L) ≅ Sym²/sat(gauge) = ℤ^{C(n,2)}`, free. **L washes the phantom out.**

**What CALC-18 Finding 2 got wrong.** It stated "the integral carrier is `ℤ^{C(n,2)} ⊕ ℤ/2`." True of the *quotient* model, **false** of the realised carrier `Im(L)`. The phantom is a feature of the **gauge** (the redundancy / the kernel), not of the numerators the construction emits. CALC-18 conflated the two presentations. *[CALC-18 left intact as record per the no-silent-edit discipline; this is the correction.]*

**Why Campaign H still sees it.** Campaign H works in the quotient model and over F₂, where the non-saturation becomes a visible dimension jump: `dim(Sym²/gauge ⊗ F₂) = n(n+1)/2 − (n−1) = C(n,2)+1`, the "+1" = the phantom (CALC-16). `Im(L) ⊗ F₂` has rank `C(n,2)` (saturated, no jump). The phantom is real in the char-2 / quotient setting (Campaign H's setting) and absent from the numerator image — both true, different objects.

**Effect on the stratification (CALC-18 refined thesis) — strengthened, not weakened.** Layer (a) the phantom is now pinned to the **gauge / kernel** (upstream of `L`, washed out in the image). Layer (c) the 2-modular Specht behaviour, where V₄ lives, is in the **realised image** `Im(L) ⊗ F₂`. Provably different objects (kernel vs. image) → cannot be one fact. V₄ confirmed distinct from the phantom (no n=4 torsion in either model). The prime-2 story is a genuine stratification: (a) gauge non-saturation, (b) degree at which `∧²` enters [T2, pending], (c) modular Specht collision [T3, pending].

**Status.** T1 complete (gate + extension + V₄ reconciliation, Codex + independent reverify agree). T2, T3 pending Codex. `verify_T1_fullL.py` in container/outputs.

## CALC-20 — Cross-check audit: second independent campaign (102 graded claims, byte-stable ×2) reproduces CALC-19 independently; the open decisive test (local degree-2 ∧², = T2) is untested by both runs

**Trigger.** Will ran a second independent campaign (`evals/dbp_involution/`, benches PAIR-SPLIT / Sym-Wedge Boundary / Alternating-Half Hunt; 102 records all `COMPUTER_VERIFIED`, two runs content-byte-stable) as a cross-check. Audited it against CALC-14/18/19 and Codex T1; verified two load-bearing integral/modular pieces in-container (`audit_second_campaign.py`, `audit_pd3.py`).

**Independent reproductions (no contradictions).**
- Stage 0: banked role-pair theorem, loss `=S^(n−2,2)` (dims 0,2,5,9,14,20 n=3..8), faithfulness margin `2(n−3)` / V₄ at n=4. (Reverified the n=4 corroboration myself: S₄ on the three 2+2 partitions has character (3,1,3,0,1) = triv ⊕ S^(2,2), the std rep of S₄/V₄.) ✓ = CALC-14.
- Stage A: `∧²(std)=S^(n−2,1,1)` has multiplicity 0 in the linear carrier `Im(L)`; carrier is entirely `Sym²` content (Schur + explicit projector). ✓ = CALC-18 Finding 1.
- Stage B: `O`-parity is degree-parity (`τ_O=+I` on the symmetric carrier), **not** the tensor-swap `τ`. ✓ = the spec/CALC-18 note, reached independently.
- Stage C: `L_flag` cokernel **torsion-free**; gauge quotient `Sym²/Im(G_g) = ℤ^{C(n,2)} ⊕ ℤ/2` single uniform phantom; their "honesty note" flags the other torsion presentation as a `½`-clearing convention artifact. **= CALC-19's two-presentation resolution, reached independently.** ✓
- Stage D: char-2 phantom generalises (linear core); `ker(channel mod 2)=gauge_mod2 ⊕ ⟨g gᵀ⟩`, all-n analog of CL-H10. ✓ consistent with CALC-19.

**Verified in-container.**
- (1) The campaign's `(ℤ/2)^{C(n,2)}` "Sym/∧ split cokernel" (exps 3,6,10,15,21,28) is the square of the **n-dim permutation lattice `ℤⁿ⊗ℤⁿ`** — `coker(Sym²(ℤᵐ)⊕∧²(ℤᵐ) ↪ ℤᵐ⊗ℤᵐ) = (ℤ/2)^{C(m,2)}`, m=n (verified m=3..6 → 3,6,10,15). The row label "std⊗std" is loose; genuine `std⊗std` (dim n−1) gives `(ℤ/2)^{C(n−1,2)} = 1,3,6,10,15,21`. The canonical claim (gauge `ℤ/2` phantom) is unaffected. *[labeling nuance, math correct]*
- (2) P-D3 char-2: `rank(L mod 2)=C(n,2)` (n=4..7) — **no mod-2 rank drop**, consistent with `Im(L)` saturated (CALC-19); gauge mod 2 rank n−1; `g gᵀ ∈ ker(L mod 2)` and independent of the gauge image; `ker(L mod 2)=gauge_mod2 ⊕ ⟨g gᵀ⟩` dim n. Exactly as reported. ✓

**The scope gap that matters.** The campaign's Stage E tested the **global / monodromy** route to `∧²` and found it non-canonical: at n=3, `∧²(std₃)=sign` appears as the block-action sign character (mult 1) in the alternating sheet-pairs of `S₃≀S₃`, but the 3 blocks are root-sheets of the stage-2 trinomial, not the 3 roles — no role-canonical bijection (CALC-10's wall). Verdict `no_canonical_comparison_map`. **This is NOT the local degree-2 route.** Neither campaign has tested whether the geometry **realises** `S^(n−2,1,1)` in the second-order coupling invariants (CALC-18 Finding 3 / spec T2): the plethysm places `∧²` in the *ambient* `Sym²(Sym²std)` (mult 1 at degree 2), but realizability is open.

**Reframing.** `THESIS_CONFIRMED_LOCAL_ONLY` is accurate for the first-order carrier + the monodromy route, but silent on second-order-local. By closing the global route as non-canonical, the cross-check makes **T2 the main live hope** for an actual `∧²` carrier: if `∧²` is realised at degree 2 locally, the oriented companion exists *without* the role-canonical cover the report says is missing. T2 (realizability of `S^(n−2,1,1)` in the degree-2 coupling) is now the decisive test untouched by **both** runs. Banked open thread from the campaign matching ours: all-n *nonlinear* RoleChSpec faithfulness in char 2 (= CALC-16).

**Status.** Cross-check passed, no contradictions, triangulation strong (CALC-19 independently confirmed). T2 = decisive open test; T3 (2-modular collision) pending. Audit scripts in container/outputs.

## CALC-21 — T2 realizability RESOLVED (positive): the existing r=2 channel curvature realizes ∧²=S^(n−2,1,1) locally — the oriented companion has a concrete degree-2 observable carrier

**Trigger.** Will resolved the local degree-2 question: the full gauge-normal quadratic algebra on `O` carries `∧²(std)` (central projector on degree-2 `O`-monomials: n=4 rank 3 / target 3, n=5 rank 6 / target 6, witness `O_01·O_02` nonzero). Sharp caveat: this certifies the *full quadratic algebra*, not the narrower claim that the **existing r=2 channel-density observable** specifically hits that component (density-realization vs ambient-only — the open T2 extension). Resolved here.

**Structural reduction to one scalar.** The r=2 channel curvature is `κ_c = −Λ²/q²` per flag, and per-(chart,pair) the numerator `Λ` is exactly `L`. At the symmetric jet `q²` is a constant, so `κ_c = const · (Hadamard square of L(O))` — the density is the component-wise square of `Im(L) ⊂ M_flags`. Its `∧²` content is the `S^(n−2,1,1)`-component of the Hadamard-product map `μ : Sym²(Im L) → M_flags` (`μ` = diagonal extraction). Both `Sym²(Im L)=Sym²(Sym²std)` and `M_flags` carry `S^(n−2,1,1)` with **multiplicity 1**, so by Schur this is a single scalar `c` per n; `c≠0 ⇔ realized`.

**Target screen (necessary condition, passed).** `M_flags` (per-(chart,pair), the L-flags) contains `S^(n−2,1,1)` with mult 1 for n=4..7 — so the density is *not* blind by target. (Contrast: per-chart target `ℝⁿ=triv⊕std` has no `∧²` — blind. The per-(chart,3-subset) module has it for n≥5, mult 0 at n=4.)

**Verdict — REALIZED.** *[computer-verified n=4,5,6]* `density_realizes_wedge.py` / `density_wedge_n6.py`: the `S^(n−2,1,1)`-projection of the density's quadratic image has rank `3,6,10` = **full** `dim S^(n−2,1,1)` for n=4,5,6. In fact the density's quadratic image is **all** of `M_flags` (rank `12,30,60`) — maximally nondegenerate. Sanity gates: projector rank `= dim S^(n−2,1,1)` exactly; `Im(L)` projects to 0 (linear carrier blind, as required). So `c≠0`: the existing per-(chart,pair) channel curvature carries the full oriented companion.

**Reconciles CALC-15 completely.** Realization is **granularity-dependent**. The natural §8 r=2 bordered-minor density is per-(chart,pair) (target `M_flags`) → realizes `∧²`. The **aggregate per-chart** observable (target `ℝⁿ=triv⊕std`, e.g. the std-norm `A_c`) is blind to `∧²` by target — exactly what CALC-15 measured. So CALC-15's "order axis stays in std" was blind on *two* counts: aggregate granularity *and* the norm projection. The genuine §8 density at the correct granularity carries the alternating half in full.

**Consequence for the prime-2 thesis.** "Coupling as oriented structure" has a concrete, local, degree-2 observable carrier: the per-(chart,pair) channel curvature `κ_c`. The oriented companion is **realized**, not merely ambient — and **locally**, so the global/monodromy route (CALC-20 Stage E, `no_canonical_comparison_map`) is *not required* for the alternating half to have a carrier. The stratification stands: (a) phantom `ℤ/2` in the gauge/kernel; (b) `∧²` realized at degree 2 in the local channel curvature [now closed, positive]; (c) 2-modular Specht collision [T3, pending].

**Status.** T2 fully resolved (realized, n=4,5,6; structural Schur reduction + direct projection). T3 (2-modular collision) the remaining open task. `density_target_screen.py`, `density_realizes_wedge.py`, `density_wedge_n6.py` in container/outputs.

## CALC-22 — T3 RESOLVED: magnitude and orientation collide mod 2, generically — [S^(n−2,1,1)] = [S^(n−2,2)] + [D^(n)] (orientation = shape + trivial), n=4..7; V₄ is the n=4 special case, not the mechanism

**Trigger.** Writing the T3 handoff; validated the modular-collision core in-container (`t3_modular_validate.py`, `t3_modular_fixed.py`), which closed the question. `dim D^μ` = F₂-rank of the James polytabloid Gram form, validated against knowns (D^(2,1)=2, D^(3,1)=2, D^(4,1)=4, D^(3,2)=4, trivials 1). Decomposition numbers recovered by dominance-decreasing peeling of Brauer characters; every result non-negative and dimension-checked by assertion.

**Result.** *[computer-verified n=4..7]*
- n=4: shape `S^(2,2)=D^(3,1)`; orient `S^(2,1,1)=D^(4)+D^(3,1)`.
- n=5: shape `S^(3,2)=D^(5)+D^(3,2)`; orient `S^(3,1,1)=2·D^(5)+D^(3,2)`.
- n=6: shape `S^(4,2)=D^(6)+D^(5,1)+D^(4,2)`; orient `S^(4,1,1)=2·D^(6)+D^(5,1)+D^(4,2)`.
- n=7: shape `S^(5,2)=D^(5,2)`; orient `S^(5,1,1)=D^(7)+D^(5,2)`.

**Pattern (all 4 cases): `[S^(n−2,1,1)] = [S^(n−2,2)] + [D^(n)]`** in the mod-2 Grothendieck group — orientation = shape + one trivial. So every composition factor of the shape is a factor of the orientation: the collision is **total** (shape ⊆ orient factors), shared = all shape factors. *[all-n is conjecture; strong evidence, 4 consecutive cases, dimension-verified]*

**Interpretation.** The Specht-level content of the Sym/∧ split failing at 2 (CALC-20). Over F₂ the symmetric-shape `S^(n−2,2)` and the alternating `∧²(std)=S^(n−2,1,1)` become equal up to a trivial — magnitude and orientation genuinely collide mod 2. The extra trivial `D^(n)` is the candidate fingerprint of the diagonal / polarization (possibly = the phantom `g gᵀ`, CALC-19 — open).

**V₄ reconciliation.** The collision is GENERIC (all n) → not a V₄ phenomenon. At n=4, `S^(2,2)=D^(3,1)` is the lift of modular `std_{S₃}` through `S₄/V₄`, but that normality is n=4-only, whereas `orient=shape+trivial` holds at every n. So V₄ is the n=4 SPECIAL CASE of the generic collision, distinct from the mechanism — consistent with CALC-19/20 (phantom and V₄ distinct), now extended (modular collision and V₄ also distinct).

**STRATIFICATION CLOSED.** The prime-2 thesis resolves into three distinct, individually-pinned layers:
- (a) phantom `ℤ/2` in the gauge/kernel, washed out of the image, uniform in n [CALC-19/20];
- (b) `∧²` realised at degree 2 in the local channel curvature, full projection [CALC-21];
- (c) magnitude & orientation collide mod 2 generically, `orient=shape+trivial`, V₄ the n=4 special case [CALC-22].
Unifying object: `std⊗std` with swap `τ` — carrier = `+1` (symmetric) eigenspace, `∧²` = `−1`, prime 2 = where the eigenspace split fails, manifesting as (a) lattice torsion, (b) the degree at which `−1`-content enters the local observable, (c) the mod-2 collision of the `+1`-shape and `−1`-orientation Specht modules. "Every fault line is one fact" → false; the correct statement is this stratification.

**Open (genuine remaining math).** Prove `[S^(n−2,1,1)]=[S^(n−2,2)]+[D^(n)]` for all n (theorem); identify the extra trivial (= phantom?); extend computation to higher n. = the T3 handoff.

**Status.** T1, T2, T3 all resolved in-container. Handoff = independent reproduction + the all-n proof. Scripts `t3_modular_validate.py`, `t3_modular_fixed.py`.

---

# ═══════════ PHASE 2 — TRANSCENDENTAL HUNT (distinct program) ═══════════
*Phase-1 (CALC-01…22) mapped the prime-2 representation structure of the coupling carrier. Phase-2 hunts genuine transcendentals/irrationals in the framework. The framework is exact-ℚ at every finite n,r,depth by construction, so a transcendental cannot be algebraic-combinatorial — it must come from a genuine analytic operation (a limit, or a period/integral). This narrows the search to (i) limits n/r/depth→∞ and (ii) periods/integrals/geodesic/monodromy cycles. Method: build a "constant trap" (compute to high precision, identify by PSLQ + analytic reduction), not "does π appear?".*

## CALC-23 — TRAP #1 (Gauss–Bonnet) FIRED & FULLY IDENTIFIED: the total Gaussian curvature of the DBP constraint surface is a genuine NON-CM elliptic period (j=128) — provably not π·algebraic, not Γ(1/3), not Γ(1/4)

**Trap.** Total curvature `∫∫_S K_G dA` (Gauss–Bonnet "constant trap") of the DBP constraint surface `D²+DS+P²=3` — a one-sheeted hyperboloid, signature (2,1), topologically a cylinder (χ=0, non-compact). A period of the surface itself (place (ii)).

**Sanity gate — PASSED.** The induced-metric Gaussian curvature at the keystone `(1,1,1)` is exactly `−3/49`, identical to the orbit-calculus keystone (CALC chain) and to the implicit-surface value `−det(bordered Hess)/|∇F|⁴ = −12/196`. So the parametrization carries DBP's *intrinsic* geometry, not an extrinsic artifact. *[computer-verified + proven]* — **Stronger (new):** the bordered-Hessian determinant evaluates to `4(D²+DS+P²)` for this `F`, hence `≡ 12` *identically on the surface* `D²+DS+P²=3`. So the curvature field has the clean global closed form `K_G = −12/|∇F|⁴ = −12/[(2D+S)²+D²+4P²]²` everywhere — not merely the keystone point value. *[proven]* (And under the parametrization the gradient simplifies: `2D+S = 2√3·cosh t·cosθ`, the `sinh t` cancelling.)

**Value.** *[computer-verified by three mutually independent routes]*
```
∫∫_S K_G dA = −5.010490702660418769050021160526777648057…  =  (−1.594888725…)·π
```
Three routes, each independent of the others' machinery: **(A)** raw 2D surface integral over the `(t,θ)` parametrization, made **truncation-free** by the `t=artanh u` compactification (the whole `t∈ℝ` tail folds into a bounded smooth integrand on `[−1,1]`) — confirms to **60 digits**, cross-confirmed independently on a separate machine, and via two *independent* `K_G` implementations (full bordered-Hessian `det`, and the derived global form `−12/|∇F|⁴`); independent of *all* downstream Gauss-map/elliptic reductions; **(B)** the `κ_g` triple-product 1D integral — independent of the elliptic reduction; **(C)** the elliptic `J2` / Byrd–Friedman route. All three routes agree to **60 digits**. *Methodological note:* a fixed `[−L,L]` cutoff on route (A) freezes a systematic tail bias `~e^{−2L}` that byte-stability across working precisions cannot detect — both precisions resolve the same truncated integrand and cross-validate to 60+ digits while silently sharing the bias (an `L≈30` cutoff caps true agreement at ~25 digits regardless of dps). Compactification removes it by tying precision and tail-reach together. *(Caught live: a fixed-`L` raw run mismatched at digit 25 by exactly `7.71e-26 = e^{−60}`; the compactified rerun then matched all three routes to 60.)* `val/π` is non-algebraic (PSLQ minpoly deg≤4 returns only ~10⁶-scale noise). Standard (un-sheared) hyperboloid gives the clean `−2√2·π` — so the constant is **surface-specific: the `DS` shear is exactly what breaks the algebraic·π cleanliness.**

**Reduction chain.** *[proven; each link checked numerically to 40–61 digits]*
The total curvature is the signed area of the Gauss image = `−2×` the total geodesic curvature of the asymptotic-cone Gauss curve `C₊` (verified on the standard hyperboloid → `−2√2π`). The κ_g integrand collapses symbolically: `γ=n/L` unit ⟹ `det(γ,γ',γ'')=det(n,n',n'')/L³`, and `det(n,n',n'')=4` (constant); the `|γ'|²` denominator reduces to exactly `8(3−cosφ)`. Hence
```
∫∫_S K_G dA = −2∮_{C₊}κ_g ds = −∫₀^{2π} √(cos²φ−2cosφ+5)/(3−cosφ) dφ
            = −8 ∫₀^{π/2} sin²θ /√(1+sin⁴θ) dθ          (note L² = 4(1+sin⁴(φ/2)))
            = −4 ∫₀¹ w dw /√(w(1−w)(1+w²))               (w = sin²θ)
```

**Elliptic structure.** *[proven]* Lives on `y² = w(1−w)(1+w²)`, branch points `{0, 1, i, −i}`, cross-ratio `−i`, **j-invariant = 128 (sympy exact)**. 128 is NOT among the 13 class-number-1 CM `j`-values `{0, 1728, −3375, 8000, 54000, 287496, −32768, −884736, …}`, and it is rational so it cannot be higher class number ⟹ **definitively non-CM**. This is *why* Γ(1/4) (lemniscatic, j=1728) and Γ(1/3) (equianharmonic, j=0) sweeps both failed: a non-CM curve has no Chowla–Selberg Γ-evaluation.

**Period data.** First-kind period `J1 ≔ ∫₀¹ dw/√Q = 2^{3/4}·K(k)`, `k² = (2−√2)/4` *[proven via Byrd–Friedman modulus `k²=[(α−β)²−(A−B)²]/(4AB)` with A²=2,B²=1; computer-verified to 30 digits]* — a NON-singular modulus (consistent with non-CM). Period relation `J1+J2 = 2J3` (which collapses the object to `loop = 2J2`) is **proven** via the curve involution `w ↦ (1−w)/(1+w)`: it swaps the real branch points `0↔1`, sends `Q(v) = 4Q(w)/(1+w)⁴` so `dw/√Q` is anti-invariant, and the integrand-function `(w²+2w−1)/(1+w)` is also anti-invariant (`h(v)=−h(w)`) — forcing `∫₀¹(w²+2w−1)/((1+w)√Q)dw` to equal its own negative, hence `=0`. *[proven + computer-verified to 50 digits]*

**CLOSED FORM.** *[computer-verified to 61 digits; derivation proven link-by-link via the B&F substitution `w(u)=(1−cn u)/((1+√2)+(√2−1)cn u)`, characteristic `n=(4−3√2)/8` from the cn-form→Legendre Π conversion]*
```
∫∫_S K_G dA  =  −2^{7/4} · [ (3+2√2)·Π( (4−3√2)/8 ; (2−√2)/4 )  −  (2+2√2)·K( (2−√2)/4 ) ]
```
(Π = Legendre complete elliptic integral of the 3rd kind, K = 1st kind; modulus parameter `m=k²=(2−√2)/4`, characteristic `n=(4−3√2)/8`.)

**THE FINDING.** The DBP total curvature is a **genuine non-CM elliptic period** (first + third kind on `y²=w(1−w)(1+w²)`, j=128). It is provably transcendental and provably NOT expressible via π, radicals, logarithms, or Γ-values at rational arguments — the non-CM structure is the rigorous backbone (no Chowla–Selberg), with PSLQ to 70–90 digits against π/Γ(1/3)/Γ(1/4)/lemniscatic/equianharmonic bases as corroboration. Not "π shows up" (forced) but a *new* period tied specifically to the role-shear `DS`. The trap caught exactly the kind of object the framework's exact-ℚ finiteness predicted: an honest analytic period, fully closed-form.

**Open / loose ends.** (1) ~~`J1+J2=2J3` empirical~~ — **now CLOSED**: proven via the curve involution `w↦(1−w)/(1+w)` (the real-branch-swap of `y²=w(1−w)(1+w²)`; see Period data). (2) The non-CM transcendentality of Π-periods is rigorous at the structural level; a fully formal "not a Γ-value" proof would invoke Wüstholz/period-theory machinery (not carried out here). (3) Other traps unexplored: place-(i) limits (generating function `Σ_r Ĉ_r s^r` at special points; n→∞ asymptotics) and place-(ii) monodromy period (the self-glue cubic — different analytic object, possibly a *different* constant).

**Files (container `/home/claude/`).** `trap_gauss_bonnet.py`, `trap_gb2.py`, `trap_highprec.py`, `trap_val.py`, `trap_kappa.py`, `trap_elliptic.py`, `trap_legendre.py`, `trap_final.py`, `trap_pi_scan.py`, `trap_ke.py`, `trap_closedform.py`, `trap_cf2.py`, `trap_cap2.py` (raw-2D capstone), `trap_involution.py` (J1+J2=2J3 proof), `trap_cap3.py` (36-digit capstone), `trap_compact.py` (60-digit truncation-free capstone), `trap_match.py` (3-route cross-confirm), `val.txt`.

**Status.** Trap #1 fully resolved & closed-form. Phase-2 vein open → **Trap #2 (monodromy) now fired in CALC-24**; place-(i) limit traps still next.

---

## CALC-24 — TRAP #2 (monodromy) FIRED + the ANISOTROPY ARITHMETIC LANDSCAPE: curvature and monodromy are two registers of one S₄ with the SAME Γ(1/3) → non-CM → Γ(1/4) skeleton; CM walls sit at coupling-degeneration loci

**Frame.** Asked whether the curvature period goes "special" (CM) as a function of coupling / role count, to test the n=4 V₄ accident arithmetically. Result in four parts: (A) the literal n-family hits a dimension wall, but the curvature `j` maps exactly over coupling anisotropy; (B) the curvature `j` is structurally *blind* to V₄ (it is the S₄-magnitude invariant); (C) the V₄/shape arithmetic lives in the monodromy register, which fired and hands back Γ(1/3); (D) both registers share one arithmetic skeleton.

### Part A — dimension wall + curvature anisotropy landscape
**Dimension wall.** The canonical n=4 surface (CALC-04, `Σyᵢ²+Σ_{i<j}yᵢyⱼ−65`) is a 3-manifold in ℝ⁴ (one equation, four variables). The total-curvature *elliptic* period is a 2-surface object (cone → conic cross-section → elliptic curve); for n≥4 roles the surface is (n−1)-dimensional and the invariant changes species (Gauss–Kronecker / Chern–Gauss–Bonnet). So "the n-role curvature elliptic period" does not type-check past n=3 — the elliptic handle is **bonded to the 3-role / 2-surface geometry**. *[proven]*

**Anisotropy landscape.** Parametrize coupling: `Q_s = x² + s·xy + z²` (s=1 = keystone). Correct cone normal `n(φ;s) = (cosφ, (s/2)(cosφ−1), sinφ)` ⟹ `n·n = 1 + s²·sin⁴(φ/2)` (the keystone's `1+sin⁴` with `s²` threaded in). So the total-curvature elliptic curve is `y² = w(1−w)(1+s²w²)`, branch points `{0, 1, ±i/s}`, and
```
j(s) = (1728 s⁶ − 1728 s⁴ + 576 s² − 64) / (s⁶ + 2 s⁴ + s²)
```
*[proven from branch points; computer-verified — the form-route geodesic-curvature integral lives on this curve, ratio `|∮κ_g ds| = s·2J2` clean across s=1,2,3,1/√3, and s=1 reproduces the keystone 2.5052]*

The landscape (`j` **monotone increasing** on `(0,∞)`, from `−∞` to `1728` — *[proven]*: `dj/ds = 128(3s²−1)²(9s²+1)/[s³(s²+1)³] ≥ 0` (note `s⁶+2s⁴+s² = s²(s²+1)²`; **correction** — earlier drafts wrote the denominator `(s⁶+2s⁴+s²)²`, too large by the shared factor `s(s²+1)`, which cancels once from `N′Den−NDen′`; sign-definiteness and the unique-`s` consequence are unchanged), so every `J<1728` has a *unique* `s`; the `(3s²−1)²` double zero at `s=1/√3` is why `j=0` is a triple-contact `(3u−1)³` tangency, not a crossing):
- `s → 0` : degenerate (nodal, j→−∞) — isotropic / no-coupling limit → **rational·π**
- *(small s)* : a discrete CM ladder at negative `j` (disc −7, −11, −19, −27, −43, −67, −163), all in the weak-coupling band `s<1/√3` — **mapped exactly in Part E**
- `s = 1/√3` : **j = 0**, equianharmonic, CM ℤ[ω] → **Γ(1/3)**
- `s = 1` : **j = 128**, **non-CM** (the keystone — no Γ-value; this is CALC-23)
- `s → ∞` : **j = 1728**, lemniscatic, CM ℤ[i] → **Γ(1/4)**

Keystone sits generic, flanked by Γ(1/3) (below, s=1/√3) and Γ(1/4) (s→∞). Every classical period-constant is a specific coupling strength of one trap.

### Part B — why curvature is BLIND to V₄ (the magnitude/shape split, in geometry)
The curvature curve has four branch points `{0,1,±i/s}` (its 2-torsion); S₄ permutes them. **`j(s)` is the S₄-symmetric invariant** of those points (the modular invariant) — invariant under *all* of S₄, including V₄ — so **`j` cannot see the V₄ pairing.** The resolvent cubic of the four points has roots `{1/s², ±i/s}`, discriminant `−4(s²+1)²/s¹⁰` (always `<0`, never `0` for real s>0 ⟹ resolvent Galois = S₃ = S₄/V₄ across the whole family). *[computer-verified, exact]*

This is the carrier's magnitude/shape split (CALC-08/10) realized in the curvature setting:

| carrier (representation theory) | curvature trap (geometry) |
|---|---|
| per-chart **magnitude** `(C)` — S₄-symmetric, faithful nowhere at n=4 | the **`j`-invariant** — S₄-symmetric, blind to V₄ |
| the **(2,2) shape loss** — what `(C)` discards `= S₄/V₄` | the **resolvent cubic** — what `j` discards `= S₄/V₄` |

So curvature (Trap #1) was never going to detect V₄: `j` lives on the **magnitude** side of the split. The V₄ / shape arithmetic is the **monodromy** register. *[proven structural; corroborates CALC-08/10 — the (2,2) doublet IS resolvent-cubic monodromy]*

### Part C — TRAP #2 (monodromy) FIRED: the self-glue cubic → Γ(1/3)
The self-glue cubic fixture `F = D³ + DS + P² − 3` (self_glue_monodromy §2, m_D=3) is itself an **elliptic fibration over the substrate**: `P² = 3 − D³ − SD` ⟹ `y² = x³ + S x + 3` (x=D, y=P). Hence
```
j(S) = 6912 S³ / (4 S³ + 243)
```
*[proven from the y²=x³+ax+b j-formula]*
- `S = 0` : **j = 0**, equianharmonic, CM ℤ[ω] → **Γ(1/3)**. Real period `= Γ(1/3)³ · (3/2)^{1/3} / π` *[computer-verified: `(period·π / Γ(1/3)³)³ = 3/2` exact]*
- `S = 1` : **j = 6912/247**, **non-CM**
- `S → ∞` : **j = 1728**, lemniscatic → **Γ(1/4)**

`S = 0` is the framework's own **omega-substrate degeneration** (self_glue §8: `S₂=0` slaves the product branch to the seam) — the Γ(1/3) wall sits at a **coupling collapse**, not a random point. Will's original prediction ("if the self-glue cubic is equianharmonic it hands back Γ(1/3)") confirmed.

### Part D — UNIFICATION: two registers, one arithmetic skeleton

| register | Γ(1/3) wall | non-CM generic | Γ(1/4) wall |
|---|---|---|---|
| **curvature** (shear `s`) | `s = 1/√3` | `s=1`: `j=128` | `s → ∞` |
| **monodromy** (substrate `S`) | `S = 0` | `S=1`: `j=6912/247` | `S → ∞` |

Two **independent** machineries — geometric curvature (magnitude / S₄-symmetric register) and Galois monodromy (shape / S₄÷V₄ register) — map to **identical arithmetic**: Γ(1/3) at one coupling-degeneration limit, Γ(1/4) at the other, non-CM generic between. The CM/Γ walls **coincide with coupling-degeneration loci**, and the two registers independently agree on those loci.

**THE FINDING.** The arithmetic class of a DBP surface (CM vs non-CM, *which* Γ-value) is a **closed-form function of coupling**, in *both* registers; the Γ-value walls are the **coupling-degeneration loci**; generic/healthy coupling is **non-CM in both**. The diagnostic-ladder hypothesis — "arithmetic class reports coupling health; a fault drops you onto a special wall" — is now exact and **cross-validated across two disjoint lenses**. The keystone's non-CM `j=128` is the generic value of a *working* coupling; Γ(1/3) / Γ(1/4) are the arithmetic fingerprints of it *breaking*, visible identically through curvature and through monodromy.

### Part E — the exact CM ladder (resolves Part-A open item)
Each class-number-1 CM `j`-value `J` pins a coupling strength via the rung equation in `u=s²` (the cleared `j(s)=J`):
```
(1728−J) u³ − (1728+2J) u² + (576−J) u − 64 = 0        [coeffs = (1728−J, −(1728+2J), 576−J, −64)]
```
take the unique real root in `(0,⅓)` (uniqueness = monotonicity, Part A). The full `h=1` ladder, ordered by increasing `s` (= increasing `j`, weakest coupling → Γ(1/3) floor):

| `d` | `j(d)` | coupling `s` | exact `s` / minimal polynomial in `u=s²` |
|---:|---:|---|---|
| −163 | −262537412640768000 | 1.56133×10⁻⁸ | root of `4102147072512027u³+8204294145023973u²+4102147072512009u−1` |
| −67 | −147197952000 | 2.08516×10⁻⁵ | root of `2299968027u³+4599935973u²+2299968009u−1` |
| −43 | −884736000 | 0.000268957 | root of `13824027u³+27647973u²+13824009u−1` |
| −27 | −12288000 | 0.00228211 | root of `192027u³+383973u²+192009u−1` |
| −19 | −884736 | 0.00850179 | root of `13851u³+27621u²+13833u−1` |
| −11 | −32768 | 0.0437308 | root of `539u³+997u²+521u−1` |
| −7 | −3375 | 0.125988 | **`s = 1/(3√7) = √7/21`**, exact (`u=1/63`; cubic factors `(63u−1)(81u²+81u+64)`) |
| −3 | 0 | 0.577350 | **`s = 1/√3`**, Γ(1/3) floor (triple contact) |

*[proven: rung equation + monotone uniqueness; computer-verified: roots to 50 digits, `ladder.py`]*

**Structure of the ladder:**
1. **`d=−7` is the only exact-closed-form rung** — `u=1/63` rational, `s=1/(3√7)` (the `√7` under the disc-`−7` wall is a factorization coincidence, but a clean one). Every other rung is **irreducible degree-3 in `u=s²`** (degree-6 in `s`); the minimal polynomial *is* the exact object. *[proven]*
2. **The whole discrete ladder is a weak-coupling phenomenon** — every `h=1` CM wall sits at `s<1/√3`, compressing geometrically toward `s=0` as `s ≈ 8/√(−j_d)`; the deep Heegner discriminants `−67,−163` are crushed against zero coupling (`s~10⁻⁵, 10⁻⁸`). *[proven]*
3. **The operational band is `h=1`-clean (but not `h=2`-clean)** — `s∈(1/√3,∞)` (containing the keystone `s=1`) has **no class-number-1 CM walls**: the `h=1` values above `1728` (`8000, 54000, 287496, 16581375`) are *unreachable* since `j<1728` for every finite `s`. So the *rational-`j`* ladder runs uninterrupted from Γ(1/3) floor to Γ(1/4) ceiling, and the keystone's `j=128` sits in open `h=1` water. *[proven for h=1]* (Class number `h≥2` **does** populate the band — but at fixed `h` it is a **finite, enumerated** set, not the dense `h→∞` arc. Complete `h=2` list — 7 walls, nearest `d=−32` at `s≈1.148` — is **Part E.2**.)

### Part E.2 — operational-band `h=2` walls (resolves the strong-side hedge)

The `h=1` ladder is the weak-side `s<1/√3` signature. The band `s>1/√3` (`j∈(0,1728)`, keystone `s=1, j=128`) carries no `h=1` wall (fact 3) but **does** carry `h=2` walls. At fixed class number this set is finite and exactly enumerable — "dense on the unit arc" is an `h→∞` statement and does not apply. Complete `h=2` band list, nearest-keystone first (true `j`, normalization `j(i)=1728`):

| `d` | order | true `j` | coupling `s` | `|s−1|` |
|---:|---|---:|---:|---:|
| −32 | cond-2 / ℚ(√−2) | 232.8623 | 1.1479222 | 0.1479 |
| −403 | ℚ(√−403) fund. | 44.3753 | 0.8423555 | 0.1576 |
| −91 | ℚ(√−91) fund. | 371.2387 | 1.3228862 | 0.3229 |
| −15 | ℚ(√−15) fund. | 632.8329 | 1.6613241 | 0.6613 |
| −187 | ℚ(√−187) fund. | 846.0736 | 1.9899749 | 0.9900 |
| −35 | ℚ(√−35) fund. | 1137.7668 | 2.6311057 | 1.6311 |
| −99 | cond-3 / ℚ(√−11) | 1493.2804 | 4.5032540 | 3.5033 |

Count stable across `|D|≤2000, 4000, 8000` ⟹ **complete** (the `h=2` order set is finite). Each wall's `j` is a root of the degree-2 `H_d`; the nearest, `d=−32`, has band-`j` = the small root of `H₋₃₂(x) = x²−52250000x+12167000000`. Map `j→s` by the rung cubic `(1728−J)u³−(1728+2J)u²+(576−J)u−64=0`, `u=s²`, band root `u>1/3`.

**Bracket.** `d=−403 (s≈0.842) < keystone (s=1) < d=−32 (s≈1.148)`: the keystone sits in an open `h=2`-clean gap, ≈±0.15 in `s` either side.

*(Hazard caught live: `mpmath.kleinj` is the 1728-**normalized** invariant — `kleinj(i)=1`, not 1728. A first pass filtering `0<kleinj<1728` admitted walls above the Γ(1/4) ceiling; the band filter is `0<kleinj<1`, true `j=1728·kleinj`.)*

*[proven: rung cubic + monotone uniqueness, `H₋₃₂` exact; computer-verified: `kleinj` at the reduced CM forms to 50–60 digits, completeness scan `|D|≤8000`]*

### Part E.3 — fault-injection test + the carrier invariant is tan(2θ), not coupling magnitude (resolves open item 1, a=c regime)

Open item (1) — "fault → CM wall pending a fault-injection test on a real surface" — is now run on the **general pipeline**, not the `j(s)` shortcut, so the test is non-circular. Faults are modeled as perturbations of the coupled block `[[λ,h],[h,b]]` (keystone `[[1,½],[½,0]]`: D-self `λ`, S-self `b`, coupling `h`; P decoupled). Pipeline: slice the asymptotic cone `Q=0` by `y=y₀`, circular section, normal `n=Mx`, `n·n` in `w=sin²(φ/2)`, curve `y²=w(1−w)·n·n(w)`, branch points → cross-ratio → `j`. Gated three ways: keystone `j=128`, slice-independent in `y₀`, coupling family reproduces `j(s)`. *[computer-verified]*

**The invariant `j` reads (exact identity, supersedes the "coupling strength s" reading):**
```
σ = 2h/(λ−b) = tan(2θ)        with   j(M) ≡ j_formula(σ)      [proven, symbolic]
```
`σ` = off-diagonal over diagonal-difference of the coupled block = **tangent of its principal-axis rotation angle**. The whole CM ladder reports the **mixing angle of the coupled pair**, not coupling magnitude. Part E's `j(s)` is exactly the `λ=1, b=0` slice (`σ=s`). A pre-registered alternative `σ²=4(h²−λb)/λ²` was tested and **falsified** — the geometry uses `tan(2θ)`, full stop.

**Fault triggers a wall (through the full pipeline).** A fault perturbing *only the S self-term* `b` (coupling `h` untouched) lands exactly on CM walls:
- `b = 1−√3` → `j = 0` (Γ(1/3) floor) *[computer-verified]*
- `b = 1−3√7` → `j = −3375` (d=−7) *[computer-verified]*

A pure self-fault hits the coupling ladder — the diagnostic claim's actual content holds, but the triggering fault need not be a coupling change.

**Blind spot, exact.** `j` is one scalar over a multi-dim fault space; its level sets are `tan(2θ)=const`. `(h=½,b=0)`, `(h=1,b=−1)`, `(h=¼,b=½)` are three distinct forms, all `σ=1`, all `j=128`. A coupling increase and a self-contrast decrease that preserve the ratio are **arithmetically indistinguishable**; the diagnostic reports mixing, not which component faulted. *[computer-verified]*

**Honest boundary (named) — RESOLVED in Part E.4 (FALSE).** The circular-section regime forces `a=c`, conflating D-self and P-self. The `tan(2θ)` reading *predicted* P drops out and `σ=2h/(a−b)` is a coupled-block invariant. **The `a≠c` elliptic-section pass (Part E.4) refutes this:** the spectator P-self `G` enters the period curve (in `α` and `γ`), sweeps `j` across CM walls by itself, and is the unique knob that breaks the Γ(1/4) ceiling. The `tan(2θ)` law is only the `G=A` slice; the true carrier is a conformal invariant of the full asymptotic cone, 2-parameter not 1.

### Part E.4 — a≠c elliptic-section pass: the spectator P-self is NOT inert; the carrier reads the full asymptotic cone

The `a=c` regime (E.3) conflated D-self and P-self. Lifting it requires the elliptic-section generalization of CALC-23. **Result: the curvature-period j depends on the full quadratic form, the decoupled role's self-term included.**

**Instrument (derived + gated).** For `M=[[A,h,0],[h,b,0],[0,0,G]]` (A=D-self, b=S-self, G=P-self, h=coupling), the asymptotic-cone Gauss–Bonnet integrand collapses analytically: with `m(φ)=(√A·cosφ, (h/√A)cosφ−ρ, √G·sinφ)`, `ρ=√(h²/A−b)`, the numerator `det(m,m′,m″)=√(AG)·ρ` is **constant** and the `κ_g` denominator `D(C)` is a **pure polynomial** in `C=cosφ`. So the rational `κ_g` factor lies in `ℂ(C)` and cannot move the branch points. Hence
```
period curve   y² = (1−C²)(αC²+βC+γ),   branch points {+1, −1, roots of αC²+βC+γ}
α = A + h²/A − G,   β = −2h√(h²/A−b)/√A,   γ = h²/A − b + G
```
No integral needed; j is the cross-ratio invariant of the 4 branch points. *[proven]* Gated: keystone `j=128`; `a=c` family reproduces `j_formula(s)`; **the `G=A` slice collapses to `j_formula(2h/(A−b))` exactly** — the `tan(2θ)` law (E.3) is the `G=A` cross-section. *[computer-verified]*

**Spectator P-self enters (E.3 conjecture FALSE).** `G` sits in `α` and `γ`. Block fixed at keystone (`A=1,b=0,h=½`, D–S mixing unchanged), turning only `G`:

| `G` | `j` | |
|---:|---:|---|
| ½ | 1728 | Γ(1/4) lemniscatic *(exact)* |
| 1 | 128 | keystone |
| 3/2 | 8000 | d=−8 CM *(exact; extra branch pt `−1+2√2`)* |
| 2 | 61714.3 | |

A fault on a **completely decoupled role's self-energy** walks the surface onto CM walls, with zero change to actual coupling. *[computer-verified; CM hits exact]*

**Spectator = unique ceiling-breaker.** The two extra branch points are complex-conjugate while `G < A+h²/A` (→ `j<1728`, the coupled-block band); at `G=A+h²/A` the quadratic degenerates (`α=0`); above it they go **real** and `j` can exceed `1728`. The coupled-block-only family (any `h,b` at `a=c`) is **capped at the Γ(1/4) ceiling**; only the spectator self-scale, by driving all four branch points real, breaks past it. *[proven]*

**Consequence for the diagnostic.** The arithmetic class is **not** a coupling readout — it is a conformal invariant of the asymptotic cone `Ax²+2hxy+by²+Gz²`, i.e. of the *whole* quadratic form. Coupling `h` is one ingredient; self-scales are others; the decoupled role contributes. `tan(2θ)` looked block-local only because `a=c` pinned the complex branch-pair's real part to `1`; free `G` slides it off. The carrier is a **2-parameter** invariant (the complex pair's position relative to `{±1}`), not 1-parameter, and the blind spot is correspondingly larger: coupling, coupled-pair self-contrast, and spectator self-scale all alias into the one scalar `j`. *[interpretation; curve and ceiling-break are proven]*

**Tier.** `[proven]` (curve derivation via the constant-det / polynomial-D collapse, `G=A`→`tan(2θ)` reduction, exact CM hits `G=½→Γ¼` and `G=3/2→d=−8`, ceiling-break at `α=0`) / `[computer-verified]` (gates, G-sweep).

**Diagnostic reading (corrected — in the true invariant σ=tan(2θ), Part E.3).** The ladder coordinate is the coupled-block mixing `σ=2h/(λ−b)=tan(2θ)`, not coupling magnitude. **Down the ladder** (`σ→0`, `−7→−11→−19→…`): `θ→0`, the block diagonalizes — the pair **decouples** — reached by `h→0` *or* by the self-terms splitting `|λ−b|→∞` (same motion; these alias). **Up the ladder** (`σ→∞`, toward the Γ(1/4) ceiling, past the first `h=2` wall `d=−32` at `σ≈1.148`, Part E.2): `θ→45°`, the coupled pair's **self-terms equalize** (`λ→b`) at fixed coupling — a nameable degeneration, *not* "more coupling," and it hits walls. A weakening motion that stays in-band (`1/√3<σ<1`) strikes `d=−403` at `σ≈0.842` first. Both directions are populated; the earlier "over-coupling has no rungs" asymmetry was an artifact of reading `s` as magnitude. Fault-injection confirms a wall is reachable by a *pure self-fault* (Part E.3). **Part E.4 generalizes this: the `tan(2θ)` coordinate is only the `a=c` slice — the spectator self-scale `G` is an independent ladder driver and the sole knob that breaks the Γ(1/4) ceiling.** *[interpretation; the σ=tan(2θ) law and wall locations are proven / computer-verified]*

**Open / next.** (1) ~~The diagnostic claims (fault → CM wall) are structural conjectures pending a fault-injection test on a real surface~~ — **TESTED (Part E.3, a=c regime):** fault → wall confirmed; carrier invariant `σ=tan(2θ)`; aliasing blind spot mapped. **a≠c pass DONE (Part E.4):** spectator P-self `G` enters the period curve, sweeps `j` onto CM walls, and is the sole knob breaking the Γ(1/4) ceiling — the E.3 spectator-inertness conjecture is **false**; the carrier is a conformal invariant of the full asymptotic cone, 2-parameter not 1. (2) ~~The small-s CM ladder is unmapped~~ — **RESOLVED** (Part E: `h=1` weak-side ladder exact; Part E.2: complete `h=2` band walls enumerated, 7 of them, nearest `d=−32`; remaining strong-side question is only `h≥3`, diagnostically marginal). (3) Place-(i) limit traps (generating-function / n→∞) still unexplored.

**Files (container `/home/claude/`).** `shear_j.py`, `shear_fix2.py`, `shear_land.py`, `resolvent.py` (curvature landscape + V₄ resolvent), `selfglue_j.py`, `selfglue_period.py` (monodromy trap), `ladder.py` (exact CM ladder, Part E), `h2_walls.py` (complete `h=2` band + `H₋₃₂`, Part E.2), `deriv_resolve.py` (Part A `dj/ds` correction), `faultb_pipeline.py` (general M→j, gated), `faultb_invariant.py` (σ=tan(2θ) identity + wall-landings + aliasing, Part E.3), `aneqc_derive.py` (a≠c curve derivation: constant-det / polynomial-D collapse), `aneqc_probe.py` (gates + G-sweep), `aneqc_finding.py` (exact spectator CM hits + ceiling-break, Part E.4).

**Tier.** `[proven]` (j-formulas, branch points, S₄-invariance, dimension wall, monotone uniqueness, rung equation + ladder uniqueness, `d=−7` closed form, `H₋₃₂` exact, σ=2h/(λ−b)=tan(2θ) carrier-invariant identity, ladder-end degenerations, a≠c period curve `y²=(1−C²)(αC²+βC+γ)` via constant-det/polynomial-D collapse, `G=A`→tan(2θ) reduction, spectator CM hits `G=½→Γ¼` & `G=3/2→d=−8`, ceiling-break at `α=0`) / `[computer-verified]` (form-route validation, resolvent discriminant, S=0 period = Γ(1/3), `h=1` ladder roots to 50 digits, corrected `dj/ds = 128(3s²−1)²(9s²+1)/[s³(s²+1)³]`, complete `h=2` band enumeration to `|D|≤8000`, fault-injection pipeline gates, pure-self-fault wall-landings `b=1−√3→Γ(1/3)` and `b=1−3√7→d=−7`, tan(2θ) aliasing triple, a≠c gates + G-sweep) / `[interpretation]` (diagnostic-ladder reading).

### Part E.5 / CALC-25 — METHODOLOGICAL PIVOT: scalar `j` → self-glue monodromy; the `j=128` aliasing triple tested in-sandbox by exact Galois — the abstract group is ALSO blind (all `D₄`); the discriminating invariant is the branch CONFIGURATION (omega-multiplicity + signature), not the group

**Why the pivot.** The scalar curvature invariant `j` is the modular invariant of four branch points — `S₄`-symmetric — hence blind to `V₄` (Part B). But `V₄` is the carrier's diagnostic content (`S₄/V₄` = the `(2,2)` shape loss, CALC-06/08/10). E.3 made this concrete: the triple `(λ,h,b) = (1,½,0), (1,1,−1), (1,¼,½)` all have `σ = tan(2θ) = 2h/(λ−b) = 1`, hence all `j = 128`. Pivot to the self-glue monodromy (`self_glue_monodromy.tex`), whose keystone product cover is `D₄ = Stab_{S₄}{{0,1},{2,3}}` — the order-8 "`V₄`-core" — i.e. it is built on exactly the partition `j` erases.

**General coupled-block self-glue (derived + verified, exact `ℚ`).** Surface `F = λD² + 2h·DS + b·S² + P² − 3`; forward glue `D₂:=P₁`, eliminate seam:
```
A = 3 − (λD₁² + 2h·D₁S₁ + b·S₁²)   (= P₁²)
B = 3 − λA − b·S₂²
F̃(D₁,S₁,S₂,P₂) = (B − P₂²)² − 4h²·S₂²·A
```
Verified: at `(1,½,0)` reduces to the paper's keystone `(B−A)² − A·S₂²`, `B=3−P₂²`. [proven]

**The three forms are NOT the same surface** (so the test is not pre-null):
| form | `(λ,h,b)` | signature | real surface |
|---|---|---|---|
| F1 | `(1,½,0)` | indefinite (`det=−¼`) | hyperboloid |
| F2 | `(1,1,−1)` | indefinite (`det=−2`) | hyperboloid |
| F3 | `(1,¼,½)` | **pos-definite** (`det=7/16`) | **compact ellipsoid** |
`j` is blind to this signature split. [proven]

**Method — no continuation harness needed.** The monodromy group of a cover = the Galois group of the cover polynomial over the function field. Computed exactly in `ℚ` (Claude's container, `mono_galois.py`), no certified-continuation / motion-ratio harness required.

**Result — the abstract group is blind too.**
- **Product cover** (biquadratic `P₂⁴ − 2B·P₂² + q`, `q = B²−4h²S₂²A`): irreducible for all three; `q` non-square and `A·q` non-square for all three ⟹ **`G_product = D₄` (order 8) for F1, F2, F3.** Gate F1 = paper's `D₄` ✓. [proven, biquadratic Galois classification: `q□→V₄`, `Aq□→C₄`, else `D₄`]
- **Directive cover** (general quartic in `D₁`): `D₄`-class for all three via generic specialization (Hilbert irreducibility); F2/F3 show occasional reducible specializations — **[open]**, candidate finer signal.
- ⟹ The abstract monodromy **group `D₄` aliases the triple exactly as `j` did.** Both over-collapse.

**The discriminating invariant (the actual answer) — branch configuration, finer than `j` AND the group:**
- **Omega-branch multiplicity.** Product branches (`P₂=0`, fixed `(D₁,S₁)`) solve `b·S₂² ± 2h√A·S₂ + (λA−3) = 0`: **F1 (`b=0`) LINEAR → 1 per seam sign (2 total)**; **F2, F3 (`b≠0`) QUADRATIC → 2 per seam sign (4 total)**. The framework's own omega knob `S₂` has double the branch structure for `b≠0`. [proven]
- **Block signature.** F3 positive-definite (compact), F1/F2 indefinite. [proven]
- **Together** `(mult, signature)`: F1=`(2,indef)`, F2=`(4,indef)`, F3=`(4,def)` — **all three separated.** Both coordinates are branched-cover geometry invisible to `j` and to `D₄`.

**Finding.** Both the scalar `j` and the abstract monodromy group `D₄` over-collapse the `j=128` triple. The diagnostic carrier is the cover's **branch divisor + omega-multiplicity + real structure**, not the Galois group and not a scalar. The pivot (scalar → monodromy) is correct but sharpened: it is the cover's *configuration*, not its *group type*, that resolves what the scalar aliased. [interpretation; the group results, multiplicities, and signatures are proven]

**Open / next (for a fresh session).** (1) Resolve the directive-cover reducibility on F2/F3 — specialization artifact or genuine finer discriminator? (2) `C₄`-vs-`D₄` confirmation on the directive cover. (3) Full certified continuation + **real** monodromy (loops in the real base) — the signature split predicts the real monodromy differs even where the complex group agrees; this is the un-run part of T3. (4) Promote `(omega-multiplicity, signature)` to a defined diagnostic coordinate and retrodict the existing curvature ladder against it.

**Files (Claude container `/home/claude/`).** `mono_galois.py` (cover Galois groups), `preglue.py` (signatures + eliminant + branch loci), `omega_check.py` (omega-multiplicity + real type). Spec with all verified algebra embedded: `codex_task_monodromy_aliasing_triple.md`. *(Container scripts reset between sessions; CALC-25 embeds the equations to re-create them.)*

**Tier.** `[proven]` (eliminant reduction, product-cover `D₄` all three, omega-multiplicity linear-vs-quadratic, signatures) / `[computer-verified]` (directive-cover specialization) / `[interpretation]` (configuration-as-carrier) / `[open]` (directive reducibility, `C₄`/`D₄`, real monodromy).

---

## CALC-26 — L4 ANSWERED (affirmative): the FULL bidegree channel spectrum RESOLVES the `S^(n−2,2)`/`V₄` shape at n=4 (rank 2) — refuting the "scalars are blind to the shape" prediction; a *single* scalar aliases, the *complete* spectrum resolves (`shape_vs_channels.py`)

**Question (lead L4, `DBP_Curvature_Role_Reduction.md` §13.3).** Does the full bidegree channel grid `κ_{r;p,q}` (the all-`n` channel tower, orbit-calculus §6.2) *see* the `S^(n−2,2)`/`V₄` shape, or alias it the way the single scalar `j` aliased the `j=128` triple (CALC-25)? Prediction going in (Claude): blind/aliasing — "the shape needs the structure, not a scalar."

**Setup (n=4).** The off-diagonal Hessian `H_c` (= the coupling obstruction, 6-dim pair module `M^(2,2)`) decomposes into `S₄`-isotypics via the three pair-partitions `A=12|34`, `B=13|24`, `C=14|23`:
- **triv** (1-dim) = sum of all 6 entries;
- **std = S^(3,1)** (3-dim) = within-partition differences `w_A=H₁₂−H₃₄`, `w_B=H₁₃−H₂₄`, `w_C=H₁₄−H₂₃`;
- **S^(2,2)** (2-dim, the V₄/shape piece, = `S₃`-standard pulled back through `S₄/V₄`) = partition-sum differences `u_i−u_j` where `u_A=H₁₂+H₃₄`, etc.

Pure-`S^(2,2)` deformation (keeps triv & std FIXED), two directions:
- `dir1 (ε)`: `H₀₁+=ε/2, H₂₃+=ε/2, H₀₂−=ε/2, H₁₃−=ε/2`  (`u_A+ε, u_B−ε`)
- `dir2 (η)`: `H₀₂+=η/2, H₁₃+=η/2, H₀₃−=η/2, H₁₂−=η/2`  (`u_B+η, u_C−η`)

Base: `g=(2,1,3,1)`, `H_s=diag(1,2,1,3)`, `H_c=(H₀₁,H₀₂,H₀₃,H₁₂,H₁₃,H₂₃)=(1,2,1,1,2,1)`. Compute all 9 channel numerators `κ̂_{r;p,q}` (`r=1,2,3`), Jacobian w.r.t. `(ε,η)`.

**RESULT — rank 2 (FULL). The full bidegree channel spectrum resolves the `S^(2,2)` shape.** `[computer-verified, exact ℚ]`
```
              k₁;₀₁ k₁;₁₀  k₂;₀₂ k₂;₁₁ k₂;₂₀  k₃;₀₃ k₃;₁₂ k₃;₂₁ k₃;₃₀
   ∂/∂ε  [    0    -2      0     15     29      0    -25    -32     63 ]
   ∂/∂η  [    0     2      0    -14    -29      0     24     35    -63 ]   rank = 2
```
- **Pure-self channels `k_{r;0,r}` (cols 1,3,6) = CONSTANT** (built from `H_s` only): genuinely shape-blind. *This* is the `κ_c`/`K_G`/`j`-alone blindness — over-generalized to "all scalars" in CALC-23/25.
- **Coupling channels `k_{r;p,q}` with `p≥1`, across all orders** carry the shape; together rank 2.

**Finding.** Prediction REFUTED. A *single* scalar (`j`, `K_G`, or one channel) aliases the shape; the *complete* bidegree spectrum (all `r`, all `(p,q)`) resolves it. Reconciles the `j=128` triple: one global scalar aliased them, but their full local spectra differ — same separation the monodromy branch-config gave (CALC-25). The "scalar is the wrong instrument, need monodromy to SEE the shape" premise was too strong: true for one scalar, false for the full spectrum.

**Tier.** `[computer-verified]` (rank 2, exact ℚ). **Refutes** Claude's standing "channels blind to shape" claim (CALC-23/25 framing).

---

## CALC-27 — THE CARRIER = the gauge-invariant Hessian quotient (gauge-normal form `CL-H1`); the rank-2 resolution is GAUGE-INVARIANT; and the clean line is a DIMENSION THRESHOLD — scalars resolve the shape **iff n ≤ 4**, exactly the carrier-faithfulness threshold (`gauge_help.py` + dimension table)

**Inputs.** `Gauge_Channel_Transport_Law.md` + `GAUGE_NORMAL_FORM_PROOF.md` (Campaign H, Lemma H1). Gauge action `H̃ = H + gaᵀ + agᵀ` (same gradient); moves channels inside `ker Σ` (zero-sum), `σ_r` fixed.

**(1) Carrier identification — settles the open item "confirm `L`'s image = `H_c` space".** `CL-H1`: for regular `g`, every `H` has a UNIQUE gauge-normal representative with diagonal killed (`a_i=H_ii/2g_i`) and off-diagonals the obstruction `O_ij = H_ij − g_i H_jj/(2g_j) − g_j H_ii/(2g_i)`; `Sym_n/Im(G_g) ≅ ℚ^{n(n−1)/2}` via `[H]↦O`. **Verified dim count:** `dim O = n(n−1)/2 = dim M^(n−2,2)` at every `n` (n=3→3, n=4→6, n=5→10), transforming as the pair module. **⟹ the session's carrier `M^(n−2,2)` IS the framework's gauge-invariant Hessian quotient — the same object.** The diagonal/self part is pure gauge; the gauge-invariant residue is exactly the off-diagonal coupling obstruction. `[proven + computer-verified]`

**(2) The CALC-26 rank-2 result is gauge-robust (not a chart artifact).** Verified at n=4: `σ_r` are gauge-invariant (`σ=(−39,−25,16)` under arbitrary `a=(3,−1,2,−2)`, base = gauged). Under the CALC-26 `(ε,η)` deformation, the obstruction `O` has triv & std components **constant** — only `S^(2,2)` (`u_i−u_j`) moves linearly in `(ε,η)`. So the deformation is pure-`S^(2,2)` on the *invariant* `O`, and the gauge-invariant `σ_r`-Jacobian still has **rank 2**: `[[−2,44,6],[2,−43,−4]]ᵀ`. The shape-detection lives in the invariants, not the gauge freedom. `[computer-verified]`

**(3) THE THRESHOLD (the clean, gauge-invariant line).** Carrier `dim = n(n−1)/2`, but only `n−1` scalar invariants `σ_r`. Shape `dim S^(n−2,2) = C(n,2)−C(n,1) = n(n−3)/2`. Scalars resolve the shape iff `n−1 ≥ n(n−3)/2 ⟺ n²−5n+2 ≤ 0 ⟺ n ≤ 4`: `[proven]`
```
 n | dim shape n(n-3)/2 | #σ_r (n-1) | resolve?
 3 |        0           |     2      | absent
 4 |        2           |     3      | YES  (V₄ accident — small enough)   [= CALC-26 rank 2]
 5 |        5           |     4      | NO   (kernel ≥ 1, forced by dimension, gauge-invariant)
 6 |        9           |     5      | NO   (kernel ≥ 4)
 7 |       14           |     6      | NO   (kernel ≥ 8)
```
At `n≥5` the `σ_r`-Jacobian on the shape is `(n−1) × dim_shape` with `n−1 < dim_shape` → rank-deficient *by dimension alone*, no computation needed. **This coincides with the carrier-faithfulness threshold (faithful `n≥5`, CALC-11/12/14).**

**Finding / corrections.** The clean separator between "scalars suffice" and "need the carrier/monodromy" is a **dimension threshold (n≤4 / n≥5)**, not a discriminant locus. This corrects BOTH: (a) Claude's CALC-26-turn overcorrection ("full spectrum resolves the shape") — holds only `n≤4`; (b) the original "scalars can't see the shape, need monodromy" — right for `n≥5` and for a single scalar at any `n`, wrong for the full `σ_r` at `n=4`. The `j=128` triple aliased because *one* scalar can't resolve even the 2-dim `n=4` shape; three `σ_r` can. The monodromy/carrier earns its place at `n≥5` (and globally), not on a special `n=4` subvariety.

**Tier.** `[proven]` (carrier dim = pair-module dim; threshold algebra; n≥5 rank-deficiency by dimension) / `[computer-verified]` (`σ_r` gauge-invariance, `O` triv/std-fixed under the deformation, rank 2 at n=4).

---

## CALC-28 — the n=4 aliasing-locus conjecture (rank-drop locus = `Δ_n`) is REFUTED — codim-2 vs codim-1, and an n=3/n=4 category error; a CONDITIONAL bridge survives on the std-free slice (`rankdrop.py`, `rankdrop2.py`)

**Conjecture tested.** At n=4 the gauge-invariant shape-resolution drops rank on a locus; is that locus the discriminant/role-degeneracy `Δ_n = (a−b)²(a+1)²(b+1)²` / the CM walls? Method: `g` symbolic, deform along `S^(2,2)`, `σ_r`-shape-Jacobian (3×2 in `g`), rank-drop = {all three 2×2 minors vanish}, factor across base couplings.

**Multi-base result.** `[computer-verified]`
```
base A (std-free coupling)  : GCD of rank-drop minors = g₁ − g₃     ← clean role-coincidence
base B, C (generic)         : GCD = 1                                ← no common hypersurface
symmetric coupling          : GCD = 0                                ← rank-deficient everywhere
```
The clean `g₁−g₃` came from a SPECIAL base: base A has `H₀₁=H₂₃, H₀₂=H₁₃, H₀₃=H₁₂` → its obstruction has **zero `S^(3,1)` (std) component**. Generic coupling: `GCD=1`.

**VERDICT — conjecture REFUTED.** Two reasons: **(1) codimension mismatch** — rank-drop of a `3×2` Jacobian (`rank≤1`) is **codim 2**, while `Δ_n`/role-degeneracy `{g_i=g_j}` is **codim 1**; different dimensions, can't coincide; generic `GCD=1` confirms no clean hypersurface factor. **(2) Category error** — `Δ_n` is an `n=3` object, where the shape is *absent*; it detects the role-*stabilizer of the jet*, whereas the rank-drop detects *shape-aliasing at n=4*. Different phenomena pattern-matched across a dimension where one doesn't exist. `[proven]`

**Conditional bridge that DOES survive.** On the **std-free slice** (obstruction reduced to `triv ⊕ S^(2,2)` — the pure `V₄` content, `S^(3,1)` stripped), the rank-drop *does* collapse onto a role-coincidence hyperplane `{g_i=g_j}` (base A → `g₁−g₃`). So once the std channel is quotiented out, the `S^(2,2)` shape's aliasing locus **is** role degeneracy. The generic codim-2 mess is `S^(2,2)`/`S^(3,1)` degeneracies interfering. `[computer-verified + interpretation]`

**Finding.** No clean single-hypersurface aliasing locus. The clean invariant is the **dimension threshold (CALC-27)**, not a locus; role-degeneracy is the aliasing locus only conditionally (std-free). Verify-before-assert caught an over-clean conjecture.

**Tier.** `[computer-verified]` (GCDs across 5 bases) / `[proven]` (codim mismatch) / `[interpretation]` (conditional std-free bridge). **Refutes** the CALC-27-turn "rank-drop = `Δ_n`" conjecture.

---

## CALC-29 — RECONCILIATION with the two published papers: `dbp_orbit_calculus.pdf` + `role_channel_anisotropy.pdf` are the **n=3 spine**; this session is its **general-n lift** — and the anisotropy paper's linear channel map explains *why* CALC-28's clean conjecture failed

**Claim.** The Active Role-Jet Orbit Calculus and Role-Channel Anisotropy papers (Lloyd, June 2026) already contain, **at n=3**, the conceptual spine the session has been generalizing. Not new ground — a lift. `[interpretation; correspondences grounded in the papers]`

**Correspondence table.**
| session (general n) | papers (n=3) |
|---|---|
| coupling module `M^(n−2,2) = triv ⊕ std ⊕ S^(n−2,2)` | coupling carrier `O=(κ_c^P,κ_c^D,κ_c^S) ∈ triv ⊕ std` (orbit §7, anis §2) |
| shape `S^(n−2,2)` — **new at n≥4** | **absent** — only triv⊕std at n=3 |
| CALC-26/27 carrier resolution + threshold | faithfulness corollary `det ∂O/∂(A,B,C)=8Λ_PΛ_DΛ_S/q₀⁶`, rank 3 off isotropy (orbit §7.3) |
| dimension threshold (CALC-27): resolve iff n≤4 | **dimension law `dim Z_Σ = 2−r`**, `r=rank d(P₂κ_c)`, sharp because `2=dim std` (anis §3) — the **n=3 shadow** |
| `κ_{r;p,q}` bidegree tower | published general-n, orbit §6.2 |
| gauge-invariance (CALC-27) | gauge transport, `ker Σ` zero-sum plane (orbit §8) |
| anisotropy of the carrier | `A_c = 3‖P₂O‖²` = std-irrep norm (anis §2); `A_c(keystone)=42793/1555848` |

**Why CALC-28's clean conjecture failed — the anisotropy paper says it (Prop 1).** At n=3 the channel map `(A,B,C)↦(Λ_P,Λ_D,Λ_S)` is **LINEAR with `det=−1`**, so `κ_c` is an invertible quadratic image of the jet and `Z_Σ` is a *clean* union of four sign-branch lines (codim 2). **That cleanness is special to n=3's linear channel map.** At n=4 the map into the shape isn't that linear thing, so the locus doesn't factor — exactly CALC-28's generic `GCD=1`. The conjecture expected n=3-cleanliness one dimension up, where the producing linearity doesn't survive.

**Two distinct "faithful"s (keep separate).** Papers' *faithful carrier* = the **map** `(A,B,C)↦O` separates jets (Jacobian rank 3, orbit §7.3). Session's *faithful at n≥5* = the **representation** has no kernel (the V₄ accident at n=4). Different "faithful"s — don't cross-wire the corollary with the rep theory.

**Discharged.** Anisotropy §8 "Higher-order channels (unverified)" — the conjectured parity law (`σ_even∈ℚ`, `σ_odd∈ℚ(√q)`, `A_c` the `r=2` instance) is **PROVEN** in `DBP_Curvature_Role_Reduction.md` §4 (= the Lovelock parity). `[proven]`

**The live frontier (anisotropy §8 central open question — "same S₃?").** The monodromy's standard-2 (global, from degree-3 cube-root extraction, self-glue companion / CALC-25) vs the local `A_c`'s standard-2 (the role `S₃`). Both faces built this session: local `A_c` lifted to general n (CALC-26/27) + global monodromy aliasing-triple (CALC-25). **RESOLVED (CALC-36): the two S₃'s are DISTINCT — role S₃ permutes charts, within-block S₃ permutes directive-roots; A_c ⊥ disc_directive (Jacobian rank 2). Formerly 'not yet welded.'** Lead at n=4: `S^(2,2)` factors through `S₄/V₄ ≅ S₃` — it *is* an `S₃`-rep (the V₄ accident); the `V₄`-quotient `S₃` is where a "same S₃" proof would start. `[conjecture/open]`

**Tier.** `[interpretation]` (correspondences, Prop-1 explanation — grounded in the papers) / `[proven]` (parity-law discharge) / `[conjecture/open]` ("same S₃").



---

## CALC-30 — FINITE TWO-STATE WITNESS for the (2,2) shape: an exact n=4 pair, identical magnitude carrier (C), distinct shape carrier (A); CALC-07 closed, and the kernel-shortcut failure shown STRUCTURAL (positive-definite Q₀ on the shape plane)  (container; recreatable from CALC-14 Λ + the pair below)

**What:** exhibit the finite two-state witness deferred at CALC-07 and named in Open/next — two distinct real Hessians `H₀ ≠ H` with `(C)(H) = (C)(H₀)` (identical per-chart coupling magnitudes) yet `(A)(H) ≠ (A)(H₀)` (distinct full role-pair carrier): the magnitude summary collapses them, the carrier separates them. Solve the 4-equation fiber `(C)(H) = (C)(H₀)` in the 6 gauge-fixed Hessian unknowns for a real point off `H₀`.

**Gate (instrument checked before use).** Numerators per CALC-14, `Λ_{k,{j,l}}(H) = −(H_{jl} − H_{jk} − H_{kl} + H_{kk})`. Reproduced CALC-06/08 exactly: `rank L = 6` (ambient `Sym²(ℝ⁴)` 10-dim, `ker` = 4-dim gauge); `(A)` injective on the gauge slice `H_{0a}=0` (6 coords); `rank J_C = 4`; `ker(J_C) = 2`. `[computer-verified]`

**Why the kernel shortcut had to fail (CALC-07, explained not just deferred).** On the (2,2) tangent plane `ker(J_C)` through `H₀`, the magnitude restricts to `Q₀ = 5a² − 4ab + 2b²` (with `Q₁=Q₂=Q₃ = 2(a−b)²`). `Q₀` is **positive-definite** (disc = −24): `(C)` strictly increases in every pure-shape direction, so the only equal-magnitude point on the linear shape plane is `H₀` itself. The witness cannot live on the tangent — it exists only where the fiber curves off-plane, paying for shape motion by bending through the `triv⊕std` magnitude directions. CALC-07's kernel line ("returns only s=0") is the 1-D shadow of this. `[proven]`

**The witness (exact ℚ; gauge-fixed slice, role-0 row = 0):**
```
            (H11,H22,H33)   (H12,H13,H23)
   H₀   =     ( 2, −1,  3)    ( 1, −2,  1)
   H    =     (−2, −2, −6)    ( 2, −1, −1)
```
- Magnitude carrier **identical**: `(C)(H₀) = (C)(H) = (6, 33, 33, 54)` — all four charts, exact, equal.
- Shape carrier **distinct**: `A(H₀) = (−1,2,−1, −1,−4,−4, 2,2,5, −5,−2,−5)`; `A(H) = (−2,1,1, 4,1,4, 4,1,4, 5,5,2)` — all 12 components differ; `(A)` injective ⇒ genuine, not a gauge ghost. `H ≠ H₀`, `≠ −H₀`, `≠` any permutation of `H₀` (an off-orbit fiber point).
- Difference carries genuine shape: isotypic norms of `A(H)−A(H₀)` — triv 147, std 153, **(2,2) = 24**, sgn = std⊗sgn = 0; Parseval `Σ = 324 = ‖ΔA‖²`. The difference lives entirely in `Im(L) = triv⊕std⊕(2,2)` (CALC-08), with nonzero (2,2) — the doublet the magnitude is blind to.

**Finding.** The (2,2) shape loss (CALC-08; Standing conclusion 3) now has a **concrete finite witness**, not merely an infinitesimal kernel: two genuine coupling Hessians that the per-chart magnitude cannot tell apart and the role-pair carrier can. The named-invariant n=4 analog of the Kerr–Newman two-state demo (the n=3 GTD/DBP version, `kn_two_state_demonstration_LOCAL.py`). **Closes the Open/next item** "Finite two-state witness against the (2,2) shape invariant (distinct shape, identical magnitude)."

**Tier.** `[computer-verified]` (exact-ℚ: the witness, `(C)`-equality, `(A)`-difference, the isotypic Parseval `324=324`, and the CALC-06/08 rank gate — all exact) / `[proven]` (positive-definite `Q₀` ⇒ no on-tangent witness). Eval-tier, computed in container this session; no float in any verdict.

---

## CALC-31 — F1 ORDER-AXIS TARGET SCREEN: the order-r density target is NEVER blind to the depth-r two-row shape `S^(n−r,r)` — PROVEN for all r, all n≥2r (dominance); F1-deep cannot be capped at the target level, so the bottleneck is realizability, not target-blindness (`f1_screen.py`)

**Question (F1, the largest blank by area; cheap discriminating cut taken BEFORE building the deep instrument).** The order-r per-(chart, r-subset) coupling carrier (r×r coupling minor, degree-r/nonlinear) is an unbuilt object. Before constructing it, run a necessary-condition target screen: does the natural order-r flag module even CONTAIN the depth-r shape `S^(n−r,r)` — the two-row generalization of the Phase-1 loss `S^(n−2,2)`? If blind by target, F1-deep is capped before any instrument is built. (Same move CALC-21 used one rung down at r=2.)

**Object.** Order-r flag module = permutation module on flags `(output chart k, r-subset T ⊆ roles\{k})`:
```
M_flags^(r) = Ind_{S_1 × S_r × S_{n−1−r}}^{S_n}(triv) = M^λ,   λ = sort_desc(1, r, n−1−r)
```
Flag stabilizer = `S_1`(fix k) × `S_r`(permute T) × `S_{n−1−r}`(permute the rest). Each flag's order-r principal minor is `S_r`-invariant (principal minors are symmetric under simultaneous row+column permutation) ⟹ `Ind(triv)` is the correct target for the value. Multiplicity of `S^μ` in `M^λ` = Kostka `K_{μλ}`. `[proven]`

**GATE — machinery validated against CALC-21 (r=2).** `[computer-verified]` Reproduced exactly: `M_flags^(2)` contains `S^(n−2,1,1)` [=∧²] with **mult 1 for n=4..7**, and the Phase-1 shape `S^(n−2,2)` (mult 1 at n=4, mult 2 for n≥5). Dimensions `n·C(n−1,2) = 12,30,60,105` all check. The SSYT/Kostka counter is sound.

**SCREEN RESULT (r=3, n=6..10).** `[computer-verified, exact ℤ]` `S^(n−3,3)` is PRESENT at every live n (n≥2r=6):
```
 n  | λ          | target    | mult S^(n−3,3) | dim = n·C(n−1,3)
 6  | (3,2,1)    | S^(3,3)   |      1         |  60  (check OK)
 7  | (3,3,1)    | S^(4,3)   |      2         | 140  (check OK)
 8  | (4,3,1)    | S^(5,3)   |      2         | 280  (check OK)
 9  | (5,3,1)    | S^(6,3)   |      2         | 504  (check OK)
 10 | (6,3,1)    | S^(7,3)   |      2         | 840  (check OK)
```
Mult **1 at the threshold n=2r=6**, stabilizing to **mult 2 for n≥7**. Full decompositions stabilize in shape (representation-stability / FI-module behaviour): the constituent set translates rigidly in n for n≥2r+1.

**GENERAL THEOREM (stronger than the r=3 screen — proven for all r, all n≥2r).** `[proven]`
```
S^(n−r, r) ⊆ M_flags^(r)   for every order r ≥ 1 and every n ≥ 2r.
```
Proof. Kostka `K_{μλ} > 0 ⟺ μ ⊵ λ` (dominance). Here `μ=(n−r,r)`, `λ=sort_desc(1, r, n−1−r)`. Dominance `(n−r,r) ⊵ λ` holds in all cases:
- `n ≥ 2r+1`: `λ=(n−1−r, r, 1)`; partial sums `μ=(n−r, n)` vs `λ=(n−1−r, n−1, n)`: `n−r ≥ n−1−r`, `n ≥ n−1`, `n ≥ n` ✓.
- `n = 2r`: `λ=(r, r−1, 1)`, `μ=(r,r)`: sums `r≥r`, `2r≥2r−1`, `2r≥2r` ✓.
Hence `K > 0`, hence `S^(n−r,r) ⊆ M_flags^(r)` always. ∎

**FINDING.** The target screen does not merely pass at r=3 — it can NEVER cap F1-deep by target-blindness for the depth-r two-row shape, at any order. The order-r density target always carries `S^(n−r,r)`. Therefore the only thing that can cap F1-deep is **realizability** — whether the order-r channel density's degree-r *image* actually populates that component — NOT the target. This is the exact r=3 analog of the question CALC-21 answered *positively* at r=2 (the degree-2 density's Hadamard image populated `S^(n−2,1,1)` in full). The screen converts the largest blank on the Frontier map from "is there anything here?" into "the only remaining gate is the one r=2 already cleared." **Scope:** certifies the two-row depth-r shape only; other order-r irreps (alternating-type `S^(n−r,1^r)`, three-row shapes) are not screened here.

**Prediction status.** Going-in expectation (Claude): screen likely passes by analogy with r=2. **Confirmed, and strengthened to an all-r theorem.** Does NOT confirm the deeper hope (that the geometry realizes the depth-r tower) — that remains open and is the next gate.

**Tier.** `[proven]` (the all-r/all-n dominance theorem; the per-n Kostka multiplicities are exact representation theory) / `[computer-verified]` (CALC-21 gate reproduction, r=3 multiplicities n=6..10, all dimension checks). Exact integer arithmetic throughout; no float in any verdict.

**Next gate (does NOT enter the log until run).** Realizability at r=3: build the order-3 per-(chart, 3-subset) channel density, compute its degree-3 image as an `S_n`-module, and test whether the `S^(n−3,3)`-projection is nonzero (the CALC-21 Hadamard-image computation, one order up). Screen passing means this is now the live, non-capped question — the genuine (r,n)-plane analog of the role-axis theorem.

**Files.** `f1_screen.py` (container; recreatable — the object is `M^{sort(1,r,n−1−r)}` and the verdict is the dominance theorem above).

---

## CALC-32 — F1-DEEP REALIZABILITY at r=3 RESOLVED (POSITIVE): the order-3 coupling minor `κ_{3;3,0}=Λ·Λ·Λ` FULLY realizes the depth-3 shape `S^(n−3,3)` (rank-full n=6,7); the pure-self (ambient-diagonal-only) channel is BLIND ⟹ coupling REQUIRED — the (r,n)-plane analog of the role-axis theorem holds at order 3 (`f1_realize.py`)

**Question (the live gate after CALC-31).** CALC-31 proved the order-r flag target always *contains* `S^(n−r,r)` (never blind by target). Realizability is the separate, map-specific question: does the actual order-3 channel density's degree-3 *image* populate `S^(n−3,3)`? Faithful one-order-up analog of CALC-21 (degree-2 density's Hadamard image populates `S^(n−2,1,1)` in full).

**Object (the named "r×r coupling minor", CALC-15 reframe; = pure-coupling bidegree `κ_{3;3,0}`).** For a 3×3 symmetric matrix with zero diagonal, `det[[0,a,b],[a,0,c],[b,c,0]]=2abc`, so the order-3 pure-coupling channel per (chart k, 3-subset {j,l,m}) is the product of the three coupling numerators:
```
D_{k,jlm}(O) = Λ_{k,{j,l}} · Λ_{k,{j,m}} · Λ_{k,{l,m}}      (= ½ × 3×3 coupling minor)
Λ_{k,{j,l}}(H) = −(H_jl − H_jk − H_kl + H_kk)               (CALC-14 carrier; = g=(1,…,1)-jet graph-Hessian off-diag)
```
A genuine **cubic** `S_n`-equivariant map `O → M_flags^(3)` (product of three *distinct* flag-components of `L`). Realizability of `S^(n−3,3)` = the `S^(n−3,3)`-isotypic component of the realized submodule `M_real = span{D(O)}` is nonzero.

**Method (exact, certified).** Exact isotypic projector `P_W = (f^W/n!)·Σ_g χ^W(g)·ρ(g)` on the flag module (`χ^W` via Murnaghan–Nakayama, accumulated as an integer matrix then rationally scaled). Sampled exact-ℚ Hessians, applied `P_W` to `D(H)`, rank over ℚ. Exact-ℚ ⟹ a witnessed rank is a *certified* lower bound; rank = full isotypic dim ⟹ certified FULL realization.

**Projector GATE (independent cross-validation vs CALC-31).** `[computer-verified]` `P²=P`; `trace(P_{(3,3)})=5=mult·dim`; cross-gates `trace P_{(6,)}=1, P_{(5,1)}=10, P_{(4,2)}=18, P_{(4,1,1)}=10, P_{(3,2,1)}=16` — **reproduce CALC-31's multiplicities exactly**. Projector sound.

**RESULT — FULLY REALIZED.** `[computer-verified, exact ℚ — certified]`
- **n=6** (threshold, mult 1): `rank P_{(3,3)}·D = 5 = dim S^(3,3)`. Raw realized span `= 60 = all of M_flags^(3)` (maximally nondegenerate, as CALC-21 at r=2).
- **n=7** (mult 2): `rank P_{(4,3)}·D = 28 = 2·dim S^(4,3)` = full isotypic. Not a threshold accident.

**CONTROL — pure-self channel is BLIND ⟹ coupling REQUIRED.** `[computer-verified, exact]` Genuine ambient bidegree-(0,3) channel (CALC-26's "H_s only" object): substitute the diagonal-only ambient Hessian into the graph-Hessian formula → `f_s` has diagonal `−(H_jj+H_kk)` and every off-diagonal `−H_kk`; the channel is `det` of its 3×3 over T, built from ambient **diagonal entries only**. Result: `rank P_{(3,3)}·D_self = 0` (vanishes on 150 generic samples in 6 diagonal vars; cubic space dim 56 ≪ 150 ⟹ identically zero, certified). The depth-3 shape is **unreachable from pure self-data**; off-diagonal coupling is necessary. Extends CALC-26's "pure-self shape-blind" (depth-2, n=4) to the depth-3 shape at n=6. Raw self-span dim = 15 (diagonal-only data is constrained; `M_real` for coupling was full 60).

**Methodological catch (verify-before-assert, own error).** A first control used `S_{k,j}=H_jj−2H_jk+H_kk` (the *graph-Hessian* diagonal) and spuriously "fully realized" `S^(3,3)`. That numerator silently includes the off-diagonal `H_jk` — not pure-self. The genuine ambient-diagonal-only channel is blind. Contaminated control caught and corrected before entering as a finding; the spurious "self realizes" was coupling content in disguise, consistent with the corrected verdict.

**FINDING — the order axis is not shallow; the (r,n)-plane analog of the role-axis theorem holds at r=3.** Phase-1 role-axis theorem: climbing `n`, the carrier acquires the depth-2 shape `S^(n−2,2)`. Order-axis r=3 result: the order-3 coupling minor acquires the depth-3 shape `S^(n−3,3)` — a Specht module *absent* from the linear r=2 carrier (`Im L = triv⊕std⊕S^(n−2,2)`, depth ≤ 2) and *unreachable* from pure-self data. Climbing `r` via the correct observable (the coupling minor) reaches genuinely deeper Specht content, exactly as CALC-15's reframe hoped and CALC-18/21 began at degree 2. The screen (CALC-31) proved the room exists for all `r`; this fills it at `r=3`.

**Prediction status.** Going-in (the F1 hope): the deeper order-r carrier *could* carry `S^(n−r,r)`. **Confirmed at r=3, with coupling-necessity control.** One own-error (contaminated self-control) caught and corrected mid-run.

**Scope / not-yet.** Realization certified n=6,7 (matching CALC-21's finite-n scope); all-n is conjecture (supported by the CALC-31 target-presence theorem + 2 realized cases + rep-stability), not proven — realizability is map-specific, no all-n argument yet. Only pure-coupling `κ_{3;3,0}` and pure-self `κ_{3;0,3}` tested; mixed channels `(2,1),(1,2)` and the full order-3 density not separately decomposed. Other depth-3 irreps (alternating `S^(n−3,1³)`, three-row) not screened.

**Tier.** `[computer-verified, certified]` (full realization n=6,7; pure-self blindness; projector gates vs CALC-31) / `[conjecture]` (all-n realization). Exact integer/ℚ arithmetic throughout; no float in any verdict.

**Files.** `f1_realize.py` (container; MN characters + exact isotypic projector + cubic density image rank).

**Next (does NOT enter until run).** (1) Mixed bidegree channels `κ_{3;2,1}`, `κ_{3;1,2}`: do they also carry `S^(n−3,3)`, and is there a bidegree threshold (`p≥?` required to reach depth 3)? (2) The role-axis theorem's full-form demand: an **all-r realization** statement (`κ_{r;r,0}` always realizes `S^(n−r,r)`?) — a general argument, not case-by-case. (3) r=4 → `S^(n−4,4)`, the next depth.

---

## CALC-33 — ALL-r MECHANISM for κ_{r;r,0} realizing `S^(n−r,r)`: the ENGINE proven all-r (minor collapses to `(1−r)∏x_i²`, top-Specht nonvanishing by monomial independence); FULL realization proven r=3,4,5,6 via an independent chart-forget+down-map method; the all-r full theorem reduced to one named lift obligation (`f1_mechanism.py`, `f1_mech2/3.py`)

**Goal.** Turn CALC-32's two certified cases (r=3, n=6,7) into a mechanism: is `S^(n−r,r)` realized by the order-r coupling minor for ALL r, n≥2r? Theorem requires a proof, not more cases.

**Clean reduction (by hand).** Gauge-invariant obstruction `O_ij = H_ij − (H_ii+H_jj)/2` kills the diagonal and gives the explicit linear carrier
```
Λ_{k,{j,l}} = O_jk + O_kl − O_jl
```
So the order-r coupling minor per (chart k, r-subset T={i₁..i_r}) is `D_{k,T} = det(N)`, the **hollow** symmetric matrix `N_{ab}=O_{i_a k}+O_{i_b k}−O_{i_a i_b}` (a≠b; diagonal 0). `[proven, exact]`

**(A) THE ENGINE — proven for all r.** Specialize `O_ij=x_i x_j` and set the chart variable `x_k=0`. Then `N_{ab}=−x_{i_a}x_{i_b}` off-diagonal, so `N = diag(x²) − x_T x_Tᵀ`, and the matrix-determinant lemma gives the collapse
```
D_{k,T} |_{x_k=0}  =  (1 − r) · ∏_{i∈T} x_i²
```
*Symbolic verification:* identity holds exactly for r=2,3,4,5 (`f1_mech2.py`). `[computer-verified + proven]`
*Nonvanishing (proven all r):* the function `T ↦ ∏_{i∈T} x_i²` has nonzero projection onto the top Specht `S^(n−1−r,r)` for generic x. Proof: if `P_top(∏_{i∈T}w_i)_T ≡ 0` in `w` (`w_i=x_i²`), then since the monomials `∏_{i∈T}w_i` over distinct r-subsets T are linearly independent in ℚ[w], `P_top(δ_T)=0` for every T, forcing `P_top≡0` — contradicting that `S^(n−1−r,r)` is a constituent of `ℂ[r-subsets]` (valid for n≥2r+1). Hence `(1−r)≠0` (r≥2) times a vector with nonzero top component ⟹ **the fixed-chart order-r coupling minor realizes the top Specht `S^(n−1−r,r)` of `S_{n−1}`, all r.** `[proven]`

**(B) Why the engine is NOT sufficient — the lift gap (precise).** The chart-z top-Specht `S^(n−1−r,r)` of `S_{n−1}` appears in the restriction (branching, remove-a-box) of THREE `S_n`-irreps: `S^(n−r,r)`, `S^(n−1−r,r+1)`, and `S^(n−1−r,r,1)`. So "the chart realizes `S^(n−1−r,r)`" does not pin the content to `S^(n−r,r)` — it could sit entirely in the other two. The engine is necessary infrastructure but cannot, alone, disambiguate the `S_n`-irrep. Genuine gap. `[proven obstruction to the naive lift]`

**(C) FULL realization — proven r=3,4,5,6 via chart-forget + down-map (the disambiguator).** Equivariant chart-forget `Φ : M_flags^(r) → ℂ[r-subsets]`, `Φ(D)(T)=Σ_{k∉T} D_{k,T}`. The down-map kernel `ker(d) ⊆ ℂ[r-subsets]` is **exactly** the top Specht `S^(n−r,r)` (mult 1), so a positive `Φ`-result projects onto precisely the right irrep — disambiguating what the engine couldn't. Test: `Φ(D)` has nonzero top component ⟺ `Φ(D) ∉ colspace(dᵀ)` ⟺ appending `Φ(D)` to `dᵀ` raises rank. Done over `GF(p)`, p=2³¹−1 (a positive mod-p rank increase is RIGOROUS over ℚ: if `v∈colspace_ℚ(dᵀ)` with integer `v,dᵀ` then `v∈colspace_p`, contrapositive gives the result). Generic integer O, n=2r+1:
```
 r | n  | dim ℂ[r-subsets] | rank(dᵀ) → augmented | realizes S^(n−r,r)
 3 |  7 |        35        |     21 → 22           | YES   (also = CALC-32, independent method)
 4 |  9 |       126        |     84 → 85           | YES
 5 | 11 |       462        |    330 → 331          | YES
 6 | 13 |      1716        |   1287 → 1288         | YES
```
Each a certified realization theorem-instance via a method **independent** of CALC-32's full isotypic projector (cross-checks r=3). `[computer-verified — rigorous over ℚ]` (r=7, n=15 exceeded the compute budget — a time limit, not a wall.)

**STATUS — honest.** Engine **proven all r**. Full realization **proven r=3,4,5,6** (clean independent method, r=3 double-confirmed). All-r full realization is **conjectured**, reduced to a single named obligation: the nonvanishing of `P_top∘Φ∘D^(r)` for all r (equivalently, the lift `S^(n−1−r,r)_{S_{n−1}} ⊆ M_real ⟹ S^(n−r,r)_{S_n} ⊆ M_real`). This is a branching / symmetric-function nonvanishing question, NOT an open-ended search — the mechanism is identified and the remaining step is sharply posed.

**FINDING.** The (r,n)-plane analog of the role-axis theorem is now mechanism-level, not example-level. The order-r coupling minor reaches the depth-r shape `S^(n−r,r)` by an explicit collapse (engine) to a pure product, whose top-Specht content is generic; assembling the charts (the lift) is proven case-by-case to r=6 and reduced to one clean nonvanishing for all r. Depth grows with order via a uniform, provable mechanism — the order axis is not just non-shallow at r=3 (CALC-32) but non-shallow by a named all-r engine.

**Prediction status.** Aim: an all-r mechanism. **Engine delivered (proven); full theorem reduced to one obligation, certified to r=6.** No overclaim: the all-r full statement is conjecture, with the exact remaining step named (and the reason the engine alone fails — branching ambiguity — proven).

**Tier.** `[proven]` (engine collapse + monomial-independence nonvanishing; branching obstruction to the naive lift) / `[computer-verified — rigorous over ℚ]` (full realization r=3,4,5,6 via Φ+down-map; engine collapse symbolic r=2..5) / `[conjecture]` (all-r full realization; the `P_top∘Φ∘D^(r)` nonvanishing). Exact ℚ / GF(p)-positive (⟹ℚ) throughout; no float in any verdict.

**Files.** `f1_mechanism.py`, `f1_mech2.py`, `f1_mech3.py` (container; symbolic engine + Φ/down-map GF(p) rank tests).

**Next (does NOT enter until run).** (1) The lift lemma: prove `P_top∘Φ∘D^(r) ≢ 0` for all r — a closed form for the top-Specht component of `Φ(D)` (e.g. at O=xx) would close the all-r theorem. (2) Threshold n=2r (engine needs n≥2r+1): the n=2r boundary case per r (CALC-32 did n=6 directly). (3) Mixed bidegree `κ_{r;p,q}`, p≥1: minimal p to reach depth r.

---

## CALC-34 — ALL-r LIFT CLOSED → THEOREM: `κ_{r;r,0}` realizes the depth-r Specht module `S^(n−r,r)` for ALL r≥2, n≥2r+1. Closed-form pairing witness `⟨Φ(D),w'⟩ = (−1)^r 2^{r−2}(r−1)(r−4)∏(c_{q_a}−c_{p_a})` (r≠4) + explicit rank-one witness (r=4). Discharges the CALC-33 obligation (`f1_lift.py`, `f1_r4.py`)

**What this closes.** CALC-33 proved the engine all-r and full realization r=3..6, reducing the all-r theorem to ONE obligation: nonvanishing of `P_top∘Φ∘D^(r)` for all r (the lift from fixed-chart top-Specht of `S_{n−1}` to `S^(n−r,r)` of `S_n`, which the engine alone cannot do — branching ambiguity, CALC-33(B)). This entry discharges it with a closed form.

**Reduction (rigorous).** Chart-forget `Φ: M_flags^(r) → ℂ[r-subsets]`, `Φ(D)(T)=Σ_{k∉T}D_{k,T}`, is `S_n`-equivariant. The deletion map `∂: ℂ[r-subsets]→ℂ[(r−1)-subsets]`, `∂(T)=Σ_{i∈T}(T∖i)`, has `ker(∂)=S^(n−r,r)` (mult 1, for r≤n/2). For any `w'∈ker(∂)`: `⟨Φ(D),w'⟩≠0 ⟹ P_{S^(n−r,r)}(Φ(D))≠0 ⟹ P_{S^(n−r,r)}(D)≠0` (Φ equivariant, invariant inner product) `⟹ realized`. Since `⟨Φ(D),w'⟩` is polynomial in O, realization ⟺ this polynomial is **not identically zero**. `[proven]`

**Test vector.** Mark 2r elements as r columns `(p_a,q_a)`; the matching polytabloid `w' = Σ_{S⊆[r]}(−1)^{|S|}δ_{B(S)}`, `B(S)` = transversal (column a contributes `q_a` if a∉S, `p_a` if a∈S). `∂(w')=0` (for each deleted column a, the a∈S and a∉S terms give equal (r−1)-subsets with opposite sign → cancel), so `w'∈ker(∂)=S^(n−r,r)`. `[proven]`

**THE CLOSED FORM (star-O witness).** Take `O` = a star at one unmarked vertex z (`O_{zj}=c_j`, all other edges 0). Then (CALC-33 star analysis, here re-confirmed by summing over ALL charts) only chart z survives, `Φ(D)(T)=det(hollow(c_a+c_b)_{a,b∈T})`. Matrix-determinant lemma gives
```
det(hollow(γ_a+γ_b)) = (−1)^r 2^{r−2}·[(r−2)² e_r(γ) − e_1(γ) e_{r−1}(γ)]      [proven; verified r=2..7]
```
The pairing alternating-sums this over transversals = iterated finite difference in each column variable. For a degree-r polynomial in r variables, only the multilinear monomial `γ_1⋯γ_r` survives all r differences; its coefficient in `(r−2)²e_r − e_1 e_{r−1}` is `(r−2)² − r = (r−1)(r−4)`. Hence
```
⟨Φ(D), w'⟩ = (−1)^r 2^{r−2} (r−1)(r−4) ∏_{a=1}^r (c_{q_a} − c_{p_a})      [proven; verified EXACTLY r=2..7]
```
`[proven + computer-verified, exact integer]`

**Realization, all r≥2, n≥2r+1.**
- **r≠4** (and r≥2): closed form `≠0` for generic c (pick `c_{q_a}≠c_{p_a}`; `(r−1)(r−4)≠0`) ⟹ pairing polynomial ≢0 ⟹ **realized**. `[proven]`
- **r=4**: star-O closed form vanishes (`(r−4)=0`, the lone star-degenerate order). The rank-one witness `O_ij=x_i x_j` gives an explicit nonzero pairing (e.g. `−2464416` at a specific integer x; verified) ⟹ polynomial ≢0 ⟹ **realized**. `[computer-verified — explicit witness, exact integer]` (Robustness: rank-one `O=xx` is generically nonzero for ALL r=2..7, including 4.)

> **THEOREM.** For all `r≥2` and `n≥2r+1`, the order-r pure-coupling channel `κ_{r;r,0}` (the r×r coupling minor) realizes the depth-r Specht module `S^(n−r,r)`. `[proven, r≠4]` / `[proven via explicit witness, r=4]`

**r=4 degeneracy (interpretation).** The star-O witness's zero at r=4 is intrinsic to the **potential form** `c_a+c_b` (a rank-2 structure); it is a degeneracy of *that witness*, not of the phenomenon (r=4 is realized, by the rank-one witness and independently by CALC-32/33). A curious echo of the n=4 V₄ accident in the role axis — same flavor (an order-4/role-4 accidental degeneracy), different mechanism; flagged, not claimed equivalent. `[interpretation]`

**Status — the all-r mechanism is now a THEOREM.** Engine (CALC-33, proven all-r) + lift (this entry, proven all-r via closed form r≠4 / explicit witness r=4) ⟹ the (r,n)-plane analog of the role-axis theorem holds as a proven all-r statement for n≥2r+1. The order axis reaches depth-r symmetric content `S^(n−r,r)` for every order, by an explicit, provable mechanism — no longer example-level or conjecture-level.

**Prediction status.** CALC-33 named the obligation; this entry **discharges it**. The conjecture is now a theorem (n≥2r+1). No outstanding overclaim.

**Scope / not-yet (honest).** (1) Threshold `n=2r` is NOT covered (star needs 2r+1 vertices); it is a single boundary value per r — CALC-32 verified n=6=2·3 directly via the full projector, general n=2r per-r remains `[open]`. (2) Only the pure-coupling bidegree `κ_{r;r,0}`; mixed `κ_{r;p,q}` (1≤p<r) untouched. (3) Other depth-r irreps (alternating `S^(n−r,1^r)`, three-row) not addressed.

**Tier.** `[proven]` (reduction; `w'∈ker∂`; det-hollow closed form; pairing closed form; realization r≥2,r≠4) / `[computer-verified, exact — explicit witness]` (r=4; all closed-form checks r=2..7) / `[open]` (threshold n=2r per r) / `[interpretation]` (r=4↔n=4 accident echo). Exact integer arithmetic throughout; no float anywhere.

**Files.** `f1_lift.py` (closed-form verification r=2..7), `f1_r4.py` (rank-one witness, r=4 coverage). Engine + Φ-route: `f1_mechanism.py`, `f1_mech2.py`, `f1_mech3.py` (CALC-33).

**Next (does NOT enter until run).** (1) Threshold `n=2r`: close the boundary per r (or a uniform argument). (2) Mixed bidegree `κ_{r;p,q}`: minimal p to reach depth r (CALC-26 found p≥1 needed at depth 2; general threshold open). (3) A single uniform closed-form witness covering r=4 (cosmetic — theorem already complete). (4) The deeper structural question: is the FULL order-r density (sum of all bidegrees) surjective onto `M_flags^(r)`, as observed at r=3 n=6 (CALC-32 raw span = 60)?

---

## CALC-35 — THRESHOLD n=2r CLOSED → the (r,n)-plane theorem is COMPLETE: `κ_{r;r,0}` realizes `S^(n−r,r)` for ALL r≥2 and ALL n≥2r. Threshold closed-form witness `⟨Φ(D),w'⟩ = (−1)^r 2^{r−2}[∏_{a≥1}(c_{q_a}−c_{p_a})]·C_r`, `C_r=(r−1)(r−4)c_{q_0}−Σ_{a≥1}(c_{q_a}+c_{p_a})` — a nonzero linear form for every r≥3 (no degenerate order) (`f1_threshold.py`, `f1_thresh_star.py`, `f1_thresh_proof.py`)

**What this closes.** CALC-34's theorem required n≥2r+1 (the star needs a spare vertex). The threshold n=2r was the sole remaining gap — and the *actual* wall, because at n=2r the depth-r content is not in any single chart: the per-chart module `ℂ[r-subsets of (2r−1)]` tops out at `S^(r,r−1)` (depth r−1), so `S^(r,r)` is a pure chart-assembly phenomenon (the engine, single-chart, cannot see it). This entry closes it with a closed form.

**Certified cases first (generic-O, rigorous).** Same Φ+down-map machine as CALC-33/34, retargeted to n=2r (`ker(∂)=S^(r,r)`, dim `Catalan(r)=C(2r,r)/(r+1)`, confirmed). `Φ(D) ∉ colspace(dᵀ)` over `GF(p)` ⟹ realized over ℚ:
```
 r | n=2r | dim ℂ[r-subsets] | rank(dᵀ) → aug | realizes S^(r,r)
 3 |  6   |        20        |    15 → 16      | YES  (= CALC-32, independent method)
 4 |  8   |        70        |    56 → 57      | YES
 5 | 10   |       252        |   210 → 211     | YES
 6 | 12   |       924        |   792 → 793     | YES
```
`[computer-verified — rigorous over ℚ]`

**THE CLOSED FORM (star-at-marked-vertex witness).** No spare vertex exists at n=2r, so put the star at a marked vertex z=p₀. For r≥3 this makes ONLY chart p₀ contribute (the column-0-picks-p₀ terms give rank-≤2 minors, det 0), freezing column 0 to q₀ and reducing to the iterated-difference machine over the other r−1 columns. Surviving monomials of `F=(r−2)²e_r − e_1 e_{r−1}`: the full multilinear gives `(r−1)(r−4)·c_{q_0}`, each one-column-squared gives `−(c_{q_a}+c_{p_a})`. Result:
```
⟨Φ(D), w'⟩ = (−1)^r 2^{r−2} · [∏_{a=1}^{r−1}(c_{q_a}−c_{p_a})] · C_r
C_r = (r−1)(r−4)·c_{q_0} − Σ_{a=1}^{r−1}(c_{q_a}+c_{p_a})
```
*Verification:* symbolic factorization matches at r=3,4; direct-vs-formula matches EXACTLY at r=3,4,5,6,7. `[proven (iterated-difference derivation) + computer-verified r=3..7]`

**Realization, all r≥2, n=2r.**
- **r≥3:** `C_r` is a LINEAR FORM with coefficient `−1` on every `c_{q_a},c_{p_a}` (a=1..r−1, and r−1≥2 such terms) ⟹ `C_r` is NEVER identically zero ⟹ generic c makes the pairing nonzero ⟹ **realized**. `[proven]`
- **r=2:** direct (`⟨Φ(D),w'⟩ = 4c_{q_0}(c_{p_1}−c_{q_1}) ≠ 0`; also CALC-21). `[proven]`

**No degenerate order at threshold (the clean twist).** Unlike the interior witness (CALC-34) whose cofactor was the *scalar* `(r−1)(r−4)`, vanishing at r=4 and forcing a separate rank-one witness, the threshold cofactor is a *linear form*. The `(r−1)(r−4)` only kills the `c_{q_0}` coefficient (at r=4); the free-column sum (coefficient −1) always survives. So r=4 is handled by the SAME closed form at threshold — the boundary is structurally cleaner than the interior. `[proven]` `[interpretation: depth-promotion upgrades scalar→linear-form cofactor at the self-complementary middle level]`

> **THEOREM (complete (r,n)-plane).** For all `r≥2` and all `n≥2r`, the order-r pure-coupling channel `κ_{r;r,0}` (the r×r coupling minor) realizes the depth-r Specht module `S^(n−r,r)`. `[proven]`
> *Proof.* n≥2r+1: CALC-34 (closed form r≠4, explicit witness r=4). n=2r: this entry (closed form r≥3, direct r=2). ∎

**Status — the (r,n)-plane analog of the role-axis theorem is now a COMPLETE all-(r,n) theorem, no gaps.** The role axis (Phase 1): climb n → gain depth-2 `S^(n−2,2)`. The order axis (now proven): climb r → gain depth-r `S^(n−r,r)`, for every order and every admissible n, by explicit closed-form witnesses. The order axis reaches arbitrarily deep symmetric Specht content via the coupling minor — provably, with the realization boundary `n=2r` included.

**Prediction status.** CALC-34 named n=2r as the open boundary; this entry **closes it**. The all-(r,n) theorem stands with no remaining obligations. (Started this session as F1, "the largest blank by area"; now a proven theorem across the whole admissible (r,n) range.)

**Scope / not-yet (honest, what remains beyond this theorem).** (1) Only the pure-coupling bidegree `κ_{r;r,0}`; mixed `κ_{r;p,q}` (1≤p<r) still untouched — minimal p for depth r is open (CALC-26: p≥1 at depth 2). (2) Other depth-r irreps: alternating `S^(n−r,1^r)`, three-row `S^(n−r−1,r,1)`, etc. — not addressed. (3) n<2r (the partition `(n−r,r)` invalid) — vacuous, no target. (4) Surjectivity of the FULL order-r density onto `M_flags^(r)` (CALC-32 saw it at r=3,n=6) — open.

**Tier.** `[proven]` (complete (r,n)-plane theorem; threshold closed form via iterated-difference derivation; `C_r` nonzero linear form r≥3; r=2 direct) / `[computer-verified — rigorous over ℚ]` (threshold generic-O cases r=3..6; closed-form direct-vs-formula r=3..7) / `[interpretation]` (scalar→linear-form cofactor promotion at the middle level) / `[open]` (mixed bidegrees; other depth-r irreps; full-density surjectivity). Exact integer / GF(p)-positive(⟹ℚ) throughout; no float in any verdict.

**Files.** `f1_threshold.py` (generic-O threshold cases), `f1_thresh_witness.py` (rank-one threshold check), `f1_thresh_star.py` (symbolic factorization), `f1_thresh_proof.py` (closed-form confirmation r=3..7). Interior: `f1_lift.py`, `f1_r4.py` (CALC-34); engine/Φ: `f1_mechanism.py`, `f1_mech2.py`, `f1_mech3.py` (CALC-33).

**Next (does NOT enter until run).** (1) Mixed bidegree `κ_{r;p,q}`: minimal coupling-degree p to reach depth r (the natural next axis now that pure-coupling is fully resolved). (2) Other depth-r irreps via the same Φ+down-map + closed-form-witness method. (3) Full-density surjectivity onto `M_flags^(r)`.

---

## CALC-36 — "Same S₃?" (anisotropy §8 / line-797 frontier) RESOLVED: **NO.** Local role S₃ ≠ global within-block S₃ — certified two ways. Also corrects the line-797 framing of the global S₃.

**Closes the standing open item** (line 797; anisotropy §8 central open question). Will concurs (session confirmation). Source: `self_glue_monodromy.pdf` read in full this session (the `/mnt/project` copy is a **corrupt zip** — flag for repo repair; uploaded copy readable). Anchor GATED: keystone `A_c = 42793/1555848` verified exactly in-container.

**Framing correction (important).** Line 797 tied the global standard-2 to "degree-3 cube-root extraction, self-glue companion / CALC-25" — the aliasing-triple `S₄/V₄` side. That is the WRONG global S₃. Per self_glue_monodromy §5/§8/§10 the within-block S₃ is the **Galois group of the DIRECTIVE cubic** `A = 3 − D₁³ − D₁S₁` (solve for D₁; the mD=3 extraction), permuting the 3 directive-roots within an A-block; the cube-root phases `e^{±2πi/3}` are its 3-cycle's std-2 eigenvalues. It exists **only at mD=3**. The keystone (mD=mP=2) is D₄ on both covers with NO 3-cycle — the paper's *adversarial-falsification* surface. The aliasing-triple `S₄/V₄` (CALC-25) is a DIFFERENT S₃, not this one.

**The two objects (cubic F = D³+DS+P²−3 @ (1,1,1)):**
```
LOCAL  role S3:  (κc_P,κc_D,κc_S)=(−4/49,−1/441,−4/441);  A_c(cubic)=2258/194481.  permutes ROLES {D,S,P}.
GLOBAL within-block S3: directive cubic D³+D−2=0 @ (S,P)=(1,1); roots {1,(−1±i√7)/2};
                        disc=−112 (non-square) ⇒ Galois S3.  permutes directive-ROOTS.
```

**Result 1 — structural obstruction `[proven]`.** A role transposition maps to a DIFFERENT surface (swap P↔S: F → D³+DP+S²−3). So role S₃ permutes role-CHARTS (moves between surfaces); within-block S₃ permutes directive-ROOTS of ONE chart. No common object; no canonical bijection {D,S,P} ↔ {3 directive-roots} (roots carry no role labels). S₃ has a unique standard-2, so "both have a standard-2" is vacuous (the paper's "coincidence of dimension"); a non-vacuous "same S₃" needs a canonical group identification, which the obstruction blocks.

**Result 2 — computational certification `[certified]`.** Parametrize cubic points by (D,S). Local std-2 datum `A_c(D,S)`; global std-2 datum = discriminant of the directive cubic `t³ + S·t − D(D²+S)`, i.e. `disc(D,S) = −4S³ − 27D²(D²+S)²`. Jacobian det of `(A_c, disc)` wrt `(D,S)` is NONZERO at every generic point:
```
(D,S)=(1,1):    A_c=2258/194481,  disc=−112,     Jdet=−238720/194481   ≠ 0
(D,S)=(1/2,2):  Jdet ≠ 0     (2,−1): Jdet ≠ 0     (−1,3): Jdet ≠ 0
```
Rank 2 ⇒ `A_c ⊥ disc_directive` (functionally independent). The two standard-2 data carry independent information ⇒ not "two readings of one representation."

**Verdict.** Role S₃ and within-block S₃ are **distinct**; the shared standard-2 is a coincidence of dimension — exactly the null the paper flagged. Anisotropy §8 / line-797 frontier CLOSED, **negative.**

**Tier.** framing correction (global S₃ = directive-cubic Galois, not CALC-25 S₄/V₄) `[proven — self_glue_monodromy §5/§8/§10]`; structural obstruction `[proven]`; functional-independence `[certified — exact-ℚ Jacobian rank 2]`; A_c gate `[computer-verified]`.

**Files.** In-session exact-ℚ (sympy): keystone-A_c gate, cubic A_c, directive-cubic Galois, (A_c,disc) Jacobian-rank test. Source: `self_glue_monodromy.pdf` (uploaded).

**Session note.** This session (retrieval-architecture exploration) produced orphaned entries on a stale v5 base with colliding CALC-30..34 numbers; that lineage is abandoned. Only this result — the same-S₃ negative — enters the authoritative v7 lineage, here as CALC-36.
