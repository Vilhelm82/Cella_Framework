# Campaign Brief — The Shared Residual (working charter title)
## Geometry Arm: Coupling-as-Holonomy & the Boundary Primitives (closed, on Will's desk) · Algebra Arm — THE WARP: Factorability & ⊕-Universality (this brief)

> **⛔ RETIRED 2026-06-26 (Will's ruling). THIS BRIEF IS NO LONGER LIVE.** The WARP campaign
> it specs (HR139) was retired as **subsumed by c001 / three-channel-K_G (HR140)** — both
> characterise one object, the exact account (`value + residue == TRUE in ℚ`), and c001
> established that object's structure natively at the object level while WARP circled it with
> a type-only predicate and a single-quotient ⊕-boundary whose load-bearing half was foregone.
> **Do NOT execute Stage 0 or any stage from this brief. Do NOT restart WARP.** This document is
> kept on disk as the historical record of what was specified; its "Stage 0 is CC's next
> execution unit" instruction below is **void**. See `results/the_warp/RETIRED.md`,
> HISTORICAL_RECORD HR139, and `roles/records-accounts/knowledge/RECONCILIATION_LEDGER.md`.
> Restart traps still live: "WARP", "factorability", "⊕-universality", "the carrier classifier",
> "free-module vs quotient", "Möbius reconstruction", "D_static/D_dynamic".

**Status: DRAFT — not canonical until signed by Will's hand (covenant).
Drafted chat-side 2026-06-14. Everything here is *proposed*; freezes happen
on-repo with pins, per house law. This brief sits BEHIND two gates: (a) Will's
acceptance of the geometry-arm close draft (`results/coupling_holonomy/ARM_CLOSE_DRAFT.md`),
and (b) the charter relationship ruling (§10). It does NOT jump the live queue
(cella-as-trunk charter is the standing frontier; the spine stays FENCED).**

**Supersession note:** this is the algebra arm re-authored in the campaign-brief
form (the §0–§10 BEYOND_THE_CRADLE / geometry-arm-sibling structure). It
reconciles and replaces the earlier `CAMPAIGN_THE_WARP.md` (Will: *"the warp is
wrong, don't use that"* — a task-spec shape, Phase 0 → Stage A/B, and it overstated
the geometry arm as closed/ratified). The *substance* of that draft — Q1
factorability, Q2 the ⊕-carrier, the deciders, the ℙ¹ boundary — is real and owed
and is carried here, regraded against the on-repo audit.

**Genre:** campaign brief / pre-registration scaffold. Fixture *classes* not pinned
points; *draft* claim rows; the prior-wins audit is candidates-verified-on-repo
(grep'd 2026-06-14), to be re-confirmed at freeze.

---

## 0. Charter

**Meta-thesis (one sentence, shared with the geometry arm):** the coupling/account
primitive is a property of the *act of representation*, not of floats and not of
the object's variables — and it is characterisable along two independent axes: its
**geometry** (coupling is the metric-free holonomy of the residue account; the
boundaries are two distinct primitives) and its **algebra** (the residue
composition factors, and the ⊕-algebra is universal across domains).

**Algebra-arm thesis (this brief, falsifiable):** a computation **inherits Cella's
coherence iff it factors** into observation maps each of whose defect lies in
`R_exact` and composes (factorability, **Q1**) — and that factorability is
*decidable in advance* by a structural predicate over the operation-DAG on the
rational-op class, **semi-decidable** past the transcendental (Richardson) wall;
and the reconstruction operator **`⊕` is additive exactly over free ℚ-module
carriers** and stops descending at quotient carriers (⊕-universality, **Q2** —
the *graded-universal* reading, adversarially tested against a quotient whose
natural structure is not additive).

**Relationship between arms:** sibling to the geometry arm — independent machinery,
one shared meta-thesis. The charter's meta-thesis is confirmed **only at the
charter level, only if BOTH arms survive**; neither arm alone confirms it. The
geometry arm is closed (Stages A–E + the v2 floor-correction; all eight CL-G
resolved; close draft on Will's desk). This brief specs the algebra arm — the
remaining open arm. **WARP is NOT "the last gate to the spine":** per `SPINE_STATUS.md`
(HR138) the spine unfences only when both arms survive *and a separate
spine-confirmation clears* — a charter-level disposition reserved to Will, never
asserted inside this campaign.

**Strategic placement:** load-bearing **evidence** for the `cella-as-trunk`
re-founding, downstream of the geometry arm. Its job is to convert the design
document's §7 two open questions — `CELLA_DESIGN_DOCUMENT.md` Q1 (decidability of
factoring) and Q2 (universality of `⊕`) — and the §2/§3 `[INFERENCE]` claims toward
`[MEASURED]`/`[ANALYTIC]`, **or refute them with preserved witnesses**. A refutation
that names its boundary is a success condition, not a failure. It must NOT jump
the queue ahead of the geometry-arm acceptance or the cella-as-trunk charter
dispositions.

---

## 1. Stage −1 — MANDATORY prior-wins audit (on-repo, grep'd 2026-06-14)

Per house protocol: grep `V4_GLOSSARY.md`, `LAYER_MANIFEST.md` "Provides" blocks,
and `HISTORICAL_RECORD.md` before any new derivation. Unlike the geometry-arm
brief (which audited chat-side), these hits are **verified on-repo** (content-grep
across `Build_Docs/Architecture/`); they are still to be re-confirmed at freeze.
**Three of the six materially change build-vs-grade** — the old WARP draft missed
all three.

1. **`projective_ratio` already exists in L1 substrate** (`LAYER_MANIFEST.md`
   "Provides": `ProjectiveRatioStatus`, `ProjectiveRatioValue`, `ProjectiveRatioResult`,
   `PROJECTIVE_RATIO_SPACE`, `PROJECTIVE_RATIO_PROTOCOL`, `projective_ratio`,
   `scalarize_projective_ratio`, `PROJECTIVE_RATIO_SCALARIZATION_TRANSITION_RULE`).
   **Scope-mover.** The ℙ¹(ℚ) quotient carrier for Q2's make-or-break boundary
   fixture (FX-W-F) is **not a from-scratch build** — the old draft treated "is a
   `fractions`-based projective point in scope, or a micro-task?" as open. The
   answer: a typed projective-ratio object is already substrate. WARP **consults
   it as a typed parent** (Rule 1.2 — eval-tier, no substrate edit) or builds a
   thin eval-tier ℙ¹ carrier citing it. The only genuinely-new piece is the
   **PGL₂/Möbius action** as the named native reconstruction, *if* the existing
   primitive doesn't already carry it (Stage-0 build check).

2. **`closure_grade` + `LeafKind`/`AtomKind` already partition ops by kind**
   (glossary "Closure grade … leaf-kind/atom-kind"; `src/lloyd_v4/harness/closure_grade.py`,
   `core/binding.py`). **Scope-mover.** `AtomKind` = {`FINITE_EXACT_ALGEBRAIC`
   (+−×÷√FMA), `CONSTRUCT_TO_TOLERANCE` (transcendentals), `NOT_ATOM`} is, up to
   naming, the `R_exact` / non-`R_exact` partition `D_static` must walk over the
   op-DAG, and `closure_grade` already does the static derivation-closure walk.
   `D_static` should **consult / lift** this walk and the `AtomKind` partition,
   not rebuild them. `FINITE_EXACT_ALGEBRAIC` ≈ the `R_exact`-populating set of
   design-doc §3. Build-vs-grade: the static-walk machinery exists; WARP grades
   *factorability specifically* on top of it.

3. **`required_precision` is a decidability precedent** (glossary "Required-precision
   composition floor — decidable terminal predicate"; certified-precision-spine P1).
   **Scope-mover for the framing of Q1.** A *decidable terminal predicate* over a
   restricted lattice (finite computation tree + closed-form W(k) + two atom-kinds
   + fixed format) was already **answered YES**. Factorability-decidability (Q1,
   CL-W1) is the **same shape** of question — a static structural predicate over
   the op-DAG — so CL-W1's `[ANALYTIC]` construction leg should cite this as the
   in-family precedent, not present decidability as novel. It de-risks A-P1.

4. **The geometry arm kit's additive-vs-multiplicative asymmetry** (glossary
   "additive vs multiplicative entanglement (the detection asymmetry; Will's ruling
   2026-06-14)"; CL-G5 + the `holonomy_entangled_undecidable` negative control,
   Stage C, sha `5e9caa41…`). **The single most relevant prior-win.** The geometry
   arm already located the Richardson wall on the *multiplicative* side: an additive
   symbolic term cancels in the mixed difference (refusal localises, holonomy stays
   a clean ℚ detector), a multiplicative one survives and hands the holonomy an
   *undecidable factor*. WARP **generalises this from the holonomy detector to the
   factoring/⊕ level**: CL-W3 (the Richardson wall) and CL-W5 (the quotient edge)
   are the algebra-level statements of the same asymmetry. Cite as prior evidence;
   do not re-derive.

5. **The Membrane Rule is the binding contract for WARP's instruments**
   (`RESULT_TYPES.md` Amendment 1, normative, pin `0a80bc05…`). Both deciders and
   the carrier classifier are composed-algebra modules running a private exact-ℚ
   algebra inside a membrane → one boundary `TypedResult`, deterministic byte-stable
   event accumulator, eval-tier status registration (obligation 5; the Rule 1.2
   home — `tests/_audit_helpers/eval_tier_operations.py`). "Projective state" is
   already a named `TypedResult` value kind (`RESULT_TYPES.md` Base Objects),
   dovetailing with hit #1.

6. **The scalar/multivariate exact-residue core + Arm M as Q2's `[MEASURED]` seed**
   (HR131/HR132 — value+residue==TRUE in ℚ, route holonomy; HR134 — difference
   tower, EFT lift, the conditional fingerprint law; HR137 / Cradle Arm M —
   matrix residues additive and exact in ℚ, the `graded-universal` evidence the
   design-doc §7 already cites; HR135 root-closure-atlas — the eigendecomposition
   factoring example + multiplicity certificate). WARP **cites these as the
   factoring class's worked instances and Q2's positive seed**; it adversarially
   *extends* them to a quotient carrier (FX-W-F), which Arm M did not test.

**Banked witnesses (cite, never re-derive):** HR138 `UNDERFLOW-WITNESS-ULP` (total
float-lane cancellation that still factors — `R_exact`-by-composition, R15);
HR138 CL-G5 asymmetry (#4 above); the R15 typing reconciliation (the geometry
close draft §5 — `below_detection` in this lineage is `R_exact`-by-composition,
**not** a `T_token`, **not** design-doc line-151 underflow). **WARP inherits R15's
corrected characterisation and must NOT re-freeze the wrong typing** (§10.7).

**External citations owed (Phase-0 `CITATIONS.md`, mapped to source + preconditions):**
Richardson 1968 (undecidability of expression-equality for a class containing
transcendentals — the CL-W3 `[ANALYTIC]` boundary); decidability of the
rational-function/field-of-fractions identity problem (the CL-W1 decidable core);
ℚ-module / free-module structure and ℙ¹ as a quotient with no compatible additive
structure (`PGL₂` acts, ℚ-module addition does not descend — the CL-W4/W5 boundary).

**§13 confusable surfaced:** the `⊕` in the MCG decomposition (`R = M ⊕ C ⊕ G`,
glossary) is a **decomposition** operator — distinct from WARP's **reconstruction**
`⊕` (`v ⊕ ρ == TRUE`). Flag this pair in §13 at close so a fresh session does not
conflate them (proposed §10.6 / close-time).

Freeze nothing until this audit is re-confirmed on-repo; surface hits before
derivation.

---

## 2. Algebra arm — fixture classes (manifest to be frozen as FX-W)

**Scope cap:** the **rational-op class** (`{+, −, ×, ÷, integer pow, neg, abs}`,
ℚ-representable inputs) plus the **transcendental wall** as a boundary; carriers =
free ℚ-modules (ℚ, ℚⁿ, ℚⁿˣᵐ) plus **one representative quotient, ℙ¹(ℚ)**. float64
substrate only. Larger n only as unscored smoke; no quotient atlas.

- **FX-W-A (pure `R_exact` rational-op DAGs):** varied depth and cancellation, all
  primitive maps in `R_exact`, composition residue-preserving — the decidable core.
- **FX-W-B (the `÷0` / `0^neg` token locus):** the intrinsic-token cells. Totality:
  every cell returns a typed token (`indeterminate`), **never** a wrong *factors*.
- **FX-W-C (composition-effect — factorability ≠ float-lane exactness):**
  catastrophic-cancellation cells (the banked `UNDERFLOW-WITNESS-ULP`),
  Sterbenz-protected cells, the `separated_coincidental` 33-cell class — DAGs that
  factor despite total float-lane cancellation.
- **FX-W-D (the transcendental / Richardson wall):** `sin²+cos²`, `exp(log x)`,
  `atan(tan x)` on-branch — the `D_static` *does-not-factor* / `D_dynamic`
  *factors-after-simplification* split; the semi-decidability boundary. CL-G5 is
  the geometry-arm precedent for this wall (audit #4).
- **FX-W-E (free ℚ-module carriers):** scalar (carrier ℚ), vector solve (ℚⁿ),
  Jacobian (ℚⁿˣᵐ — Arm M prior evidence). Additive reconstruction `v ⊕_add ρ == TRUE`.
- **FX-W-F (THE BOUNDARY — the quotient carrier):** `ℙ¹(ℚ)` projective points
  `[a:b] = [λa:λb]` (a quotient) **plus the `PGL₂`/Möbius action**. Representative-
  dependence of the additive residue; the make-or-break Q2 edge. *(Recorded
  non-test, carried so it is not silently re-added: the v1 multiplicative-relative-
  error cell — it cannot fire the refutation kill, the exact EFT residue of any
  rational op is additive by construction.)*

## 3. Algebra arm — claim ledger (draft rows; CL-W*)

- **CL-W1** (decidable core — `[ANALYTIC]`+confirm) On the rational-op class **away
  from the `÷0`/`0^neg` locus**, `D_static(C) ⟺ C factors`, biconditional with
  **zero false verdicts** on FX-W-A/C(non-transcendental)/E; the construction
  argument (ℚ field-closure ⇒ `R_exact`-closure on the class) is recorded — retired
  by proof, the battery confirms. **Independent gate:** `D_dynamic` (attempts the
  factoring, checks `v ⊕ ρ == TRUE`, `ρ ∈ R_exact`) against the exact-ℚ referee, on
  a path that never reads `D_static`. **Cite** the `required_precision` decidable-
  terminal-predicate precedent (audit #3).
- **CL-W2** (type property — `[MEASURED]`) Factorability reads the **operation
  type**, never the realised residue, the float-lane result, or operand-cancellation
  **exposure** (which `D_static` computes and attaches, but must not consult).
  **Independent gate:** an AST-assert that `D_static`'s verdict path provably does
  not read exposure or the float-lane value. `UNDERFLOW-WITNESS-ULP` cited (total
  cancellation, still factors). Factorability ≠ float-lane exactness.
- **CL-W3** (the Richardson wall — split-graded) The FX-W-D cells exhibit the
  predicted `D_static` *does-not-factor* / `D_dynamic` *factors-after-simplification*
  split; the split coincides with expression-equality (factoring recovered **iff**
  granted one algebraic-simplification oracle call). The **fixture split is graded
  `[MEASURED]`**; the **general semi-decidability is graded `[ANALYTIC]`**
  (Richardson 1968) and **never** claimed as measured. **Independent gate:** the
  algebraic-simplification oracle (one declared call, Rule 1.9-pinned — §10.5).
  CL-G5 cited as prior evidence of the same wall.
- **CL-W4** (additive over free modules — `[ANALYTIC]`+confirm) For every **free**
  ℚ-module carrier (FX-W-E), additive reconstruction closes against the independent
  referee, **zero failures**; the construction (`T,v ∈ M ⇒ T − v ∈ M`) is recorded
  — retired by proof, confirmed by battery. The carrier varies; the operation is the
  module's addition. **Independent gate:** an exact-ℚ truth computed **off the
  residue path** (so the check cannot certify itself). Arm M prior evidence.
- **CL-W5** (**KEYSTONE — the quotient edge, the make-or-break**) On `ℙ¹(ℚ)`
  (FX-W-F), additive reconstruction is **ill-defined** (the additive residue between
  two representatives of the same projective point *differs*), and the `PGL₂`/Möbius
  action is named as the native reconstruction: **`⊕` is additive iff the carrier is
  a free ℚ-module.** This **locates the family edge** (graded as a boundary, not a
  pass). **Independent gate:** the same off-residue-path exact-ℚ truth as CL-W4.
  *(This row adversarially tests Q2's graded-universal hypothesis against a carrier
  whose natural structure is not additive — the test the design doc §7 flags as
  never run. It is the keystone because it is the one row that can move Q2 either
  way.)*
- **CL-W6** (deliberately **PARTIAL**) Quotient / token-boundary coverage. `ℙ¹` is
  **the** representative quotient; other quotients (modular-up-to-equivalence,
  group-modulo-centre) are a **fenced extension** with their own fixtures — the edge
  is *located*, an exhaustive quotient atlas is **not** claimed. The `÷0`
  token-boundary composition algebra is **touched** (FX-W-B totality) but the
  general token-boundary `⊕` is the **thinnest leg** and stays a separate brief.
  Full coverage **never** claimed.

## 4. Algebra arm — stages, instruments, kill conditions

**Stages:** 0 (gates, schema freeze, fixture freeze, dry-runs that must **refuse**,
informativeness controls that must **fail**, economics pins) → **A — Arm F:
factorability decidability** (`D_static` vs `D_dynamic`; CL-W1, CL-W2, CL-W3) →
**B — Arm A: the free-module / quotient boundary** (the carrier classifier;
**CL-W5 is the keystone**, CL-W4 its free-module control). Checkpoints each stage;
byte-stability ×2 everywhere. *(Two scored stages, mirroring the old draft's A/B
substance but recast as charter-arm stages under the brief discipline.)*

**Instruments (all emit under the Membrane Rule, audit #5; eval-tier, Rule 1.2):**
- `D_static` — the op-DAG walker; returns *factors* iff every primitive map is in
  `R_exact` and the composition is residue-preserving, reading the operation type
  only. **Consults / lifts** the existing `closure_grade` walk + `AtomKind`
  partition (audit #2); exposure computed-and-attached but provably off the verdict
  path (CL-W2 AST-assert).
- `D_dynamic` — the exact-ℚ ground truth; attempts the factoring and checks
  `v ⊕ ρ == TRUE`, `ρ ∈ R_exact`, against the referee.
- The **carrier classifier** — free ℚ-module vs quotient; the additive-reconstruction
  check graded against an **independent** exact-ℚ truth (computed off the residue
  path). For the ℙ¹ carrier it **consults the existing `projective_ratio` primitive**
  (audit #1); the `PGL₂`/Möbius action is the named native reconstruction (Stage-0
  build check: does `projective_ratio` already carry it, or is the action a
  micro-task?).

**Referees:** `eval_exact` over ℚ (free); an **independent** exact-ℚ truth path for
the carrier check, computed off the residue account (so it cannot certify itself);
one **declared** algebraic-simplification oracle call for CL-W3's decidable cases
(Rule 1.9-pinned). V3 MCP is **not** a referee here (this arm is algebra, not
geometry) — Axiom 10 stance noted for completeness, no import. The probe never
imports the referee (covenant #7). `mpmath` referee-side only, for transcendental
enclosures; substrate/probe imports stdlib only (`fractions`, `decimal`,
`numpy.float32/64` as type containers, `random.Random(seed)`).

**Kill conditions (armed):**
- **K-W1 (halt — campaign dies):** any pure-`R_exact` rational-op DAG (away from
  `÷0`) that `D_dynamic` finds does **not** factor. The decidable-core foundational
  claim is false; the campaign stops, chain preserved.
- **K-W2 (halt arm):** `D_static ≠ D_dynamic` on the rational-op class in either
  direction (a false verdict). The decider is broken; arm halts.
- **K-W3 (refute row, continue — the make-or-break):** CL-W5 fails — either additive
  `⊕` **does** descend on `ℙ¹` (the boundary is wrong → `⊕` is more robust than
  graded-universal predicts), **or** a *free* ℚ-module carrier fails additive in
  CL-W4. Either way: halt the row, **preserve the witness, name what reconstructs
  instead**, reduce scope, keep the chain. *(Armed precisely because it adversarially
  tests Q2; a named-boundary refutation here is a charter result, not a failure.)*
- **K-W4 (refute row):** CL-W3 — the `D_static`/`D_dynamic` split does **not**
  coincide with expression-equality (the wall is located elsewhere than predicted).
- **K-W5 (descope, pre-declared):** the `ℙ¹`/`PGL₂` parent build or a quotient
  extension exceeds the Stage-0 budget → fence per the pre-registered schedule,
  never silently.

**Economics pins (taken at Stage 0, before anything depends on them):** op-DAG
walk cost (nodes/verdict); exact-ℚ referee bits/step on the carrier check;
representative-dependence battery cost for FX-W-F; the one simplification-oracle
call budgeted and pinned.

---

## 8. Schema & governance deltas (this arm)

- Records gain a **factorability verdict** field (`factors` / `does_not_factor` /
  intrinsic-token), a **carrier-sort** field (`free_module` / `quotient`), and the
  **AST-seam assertion outcome** (CL-W2). One `TypedResult` per evaluation; eval-tier
  `operation_id` cites this brief.
- New eval-tier status families (factorability verdict; carrier sort) register in
  the eval-tier operation registry per the **Membrane Rule** obligation 5 — **no
  substrate promotion in-campaign** (Rule 1.2; promotion is a separate post-closeout
  exercise).
- **Refusal-triangle note (Will's triangle):** the Richardson refusal sits on the
  **function** vertex (the map is uncontracted past the wall); the `÷0` token on the
  **substrate/format** vertex (genuine indeterminacy, no `T` to recover); a refusal
  that resists **all three** vertices (function / substrate / instrument) is a
  **FINDING**, not a bookkeeping gap.
- Two-run byte-stability, frozen preregs with pins, informativeness controls, the
  content-pin law (Rule 1.9), clause embedding (Rule 1.8), three-roles separation:
  all inherited unchanged.

## 9. Fences (explicitly OUT)

- **THE SPINE CLAIM IS FENCED** (the manifest's verbatim fence, carried). This arm
  **measures** factorability and the `⊕`-carrier on named fixtures. It carries **no**
  claim that the coupling/account primitive is the universal substrate spine, and
  **no** cross-domain G-claim. `[INFERENCE]` (cella-as-trunk) stays `[INFERENCE]`.
- **The charter unfences only if BOTH arms survive *and* a separate spine-confirmation
  clears** (`SPINE_STATUS.md` HR138). WARP closing satisfies the **algebra-arm half**
  of the charter — it is **not** the last gate to the spine; the unfence is a
  charter-level disposition reserved to Will.
- **No substrate edits** (Rule 1.2). Eval-tier only (`src/lloyd_v4/evals/the_warp/`,
  citing this brief). Promotion is post-closeout.
- **No new exactness territory.** WARP characterises *factorability and the
  `⊕`-carrier* on the tested fixtures; it does not extend the coverage envelope
  (design-doc §6) to new operation classes.
- **`ℙ¹(ℚ)` is the representative quotient.** Other quotients are a fenced extension
  with their own fixtures and own dual-use note. The campaign claims *the edge exists
  and where*, not an exhaustive quotient atlas.
- **No token-boundary composition algebra** beyond what FX-W-B's `÷0` locus touches —
  the thinnest leg, a separate brief (the geometry composed-gate is the current
  down payment).
- **No non-float lattices** (integer / bitwise / modular). Result scoped to float64 +
  the ℚ-module / quotient carriers tested; other lattices require a fresh dual-use
  assessment at that time (design-doc §8).
- **No reintroduction of the tautological multiplicative-relative-error stress
  fixture** (recorded non-test, FX-W-F): a multiplicative-relative-error cell cannot
  fire the refutation kill — the exact EFT residue of any rational op is additive by
  construction.
- **Performance excluded by covenant** (covenant 3, forever); any telemetry is
  non-verdict-bearing.

## 10. Reserved rulings (Will's hand)

**RESOLVED — Will's dispositions, ratified in session 2026-06-14:**
- **§10.1 ordering** — geometry-close gate satisfied (HR138 ratified); WARP proceeds.
- **§10.2 charter home** — `results/the_warp/` (Stages a/b); charter row stays OPEN
  until both arms close. (Folder convention, not a judgment call.)
- **§10.3 old file** — DONE: `CAMPAIGN_THE_WARP.md` + the root draft archived to
  `Build_Docs/_archive/superseded_docs/`.
- **§10.5 scope** — ℙ¹(ℚ) the sole representative quotient; n=2/3 free-module
  carriers (Arm M reuse); carrier stores raw `(num,den)`, the referee judges equality
  by cross-multiply (`a·d == b·c`); **the one algebraic-simplification oracle call for
  CL-W3 is ADMITTED** — exactly one declared, Rule-1.9-pinned referee dependency
  (non-rational-class, referee-side only, never substrate). Recon
  (`scratch/warp_stage0_recon/`): ℙ¹ carrier = consult + one thin Möbius/PGL₂ build;
  `D_static` lifts the `AtomKind` partition (partial_wrap), **not** the
  manifest-lineage walk.
- **§10.5 / CL-W5 grading** — additive-failure half graded `[ANALYTIC]` (foregone on
  ℙ¹); the measured weight sits on whether the Möbius action cleanly reconstructs.
- **§10.7 R15 inheritance** — CONFIRMED binding: `below_detection` = `R_exact`-by-
  composition, **not** a `T_token`; the Stage-0 prereg inherits it.
- **§10.4 / §10.6 / §10.8** — close-time, parked (working title stands; CL-W6
  resonance = measurement-only per F9 + glossary §13 pair at close; charter-close
  meta row reserved to charter close).

**Net: all freeze-blocking rulings ratified. Stage 0 (fixtures FX-W-*, schema,
manifest, freeze pins under `results/the_warp/`) is the next execution unit — CC's
to write and freeze. The detailed reserved-ruling text below is retained as the
record of what was decided.**

1. **Ordering vs the geometry arm.** Recommendation: WARP runs **after** you accept
   the geometry-arm close draft — its successor notes and the R15 inheritance
   (§10.7) feed this arm. Confirm the gate, or release WARP to start in parallel
   with the geometry-arm close.
2. **Charter home + results tree.** The algebra arm lives under the existing
   `the-shared-residual` charter row (the ledger is canonical; **no new campaign name
   without your blessing**). Recommendation: its own deliverable tree at
   `results/the_warp/` (Stages a/b), the charter row staying OPEN until both arms
   close. Confirm.
3. **Retire the old file.** Disposition on `CAMPAIGN_THE_WARP.md`: retire /
   archive it (superseded by this brief), or keep it for diff. Recommendation:
   archive to `_archive/superseded_docs/`.
4. **Names (candidates, no attachment):** THE WARP is a working title (the single
   tensioned thread-set every cross-thread passes through). A `## Names that fell
   out` line collects any substrate-suggested name mid-campaign; **none christened
   in-campaign** (covenant).
5. **Scope cap:** `ℙ¹(ℚ)` as **the** representative quotient; n = 2/3 free-module
   carriers (Arm M reuse). And the **one** algebraic-simplification oracle call for
   CL-W3 — ratify it as a declared, Rule-1.9-pinned referee dependency (vs a fenced
   extension). Ratify or lift.
6. **CL-W6's quotient resonance** (if a clean group-action pattern appears across
   carriers) — registered as a **measurement only**, never hunted (the F9
   discipline). Recommend yes. Plus: enter the MCG-`⊕` vs reconstruction-`⊕`
   confusable in glossary §13 at close.
7. **R15 inheritance (binding).** WARP **inherits** the geometry close's corrected
   characterisation — `below_detection` in this lineage is `R_exact`-by-composition,
   **not** a `T_token`, **not** design-doc line-151 underflow — and must **not**
   re-freeze the wrong typing in any prereg. Confirm so the freeze carries it.
8. **Charter-close meta-thesis row.** Whether the charter (both arms survived) gets a
   registered `meta_thesis_confirmed_*` row (parallels beyond-the-cradle). Reserved
   to charter close, not this campaign.

---

*Charter line, proposed (carried from the geometry arm): the account was born in
float64, Arm M showed it was never about floats, and the geometry arm showed it was
about the act of representation, not the object. This arm asks the last algebraic
question under that charter — when the representation factors, the account flows;
and where it cannot, the arm names the exact carrier on which reconstruction stops
being addition. A boundary that names itself is the win.*

**END — §10 rulings RATIFIED 2026-06-14 (Will). Stage 0 freeze is CC's next
execution unit. Spine FENCED; charter open pending this arm.**
