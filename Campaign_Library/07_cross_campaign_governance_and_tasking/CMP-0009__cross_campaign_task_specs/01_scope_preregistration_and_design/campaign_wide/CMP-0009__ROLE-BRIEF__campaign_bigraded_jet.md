# CAMPAIGN — BIGRADED JET (placeholder object name: J^(m,k))

**Status:** AUTHORED 2026-06-10 (Will's delegation, reserve-pile clearance session). QUEUED.
**Branch:** `campaign/bigraded-jet` from post-merge `main` (c8d664d or later).
**Naming covenant:** the object's project name is deliberately deferred — *"the name will fall out of the substrate; we have to be watching for it."* Use J^(m,k) / "bigraded jet" throughout. Every stage report carries a `## Names that fell out` section recording any candidate the substrate suggests. Do not christen; collect. **Collected (pre-Stage-A):** `FocusDual` — Will, 2026-06-10, ADHD meta joke (dual numbers × Focalin). Accidentally apt: the ε-lane is the task, the υ-lanes are everything noticed anyway, the mixed lanes are knowing which distractions mattered. Source: founder, not substrate — filed, not adopted. Variant: `FocusDual75` (Will, 2026-06-10, post-Stage-A-stop — dosage-strength naming; the 75 is the 7.5% naive-float64 error on the cond=1e16 A-P3 case the lanes treated to the last bit).

## Authority & rows served

- **Primary driver:** the HR131 §5 filed gap — route-conditioning ≠ quantity-conditioning, with Will's resolution-shape note attached: *claim-conditioning = operand damage × quantity sensitivity; the jet's own gradient supplies the sensitivity.* This campaign builds the object whose mixed lanes compute that product. **The gap that found the object grades the object** (Stage B, prediction B-P2).
- **Scoreboard rows:** A4 / A6 wave-two depth (the υ-lanes are the substrate channel the separator needs); Section-B leverage B3 (noise floor as law) and B4 (route-dependent fingerprints, now carried per-evaluation).
- **Normative law:** `RESULT_TYPES.md` Amendment 1 (composed-algebra membrane pattern). The `events` tuple is the **designated docking slot** for υ-lanes — written into the law on 2026-06-10 for exactly this campaign.
- **Downstream consumer:** `CAMPAIGN_SEPARATING_ESTIMATOR_DRAFT.md` is re-specified by this object (M1 deconvolution → exact bookkeeping; M2 route-ensemble → lane reports). Do NOT revise the separator draft inside this campaign; it waits for Stage B results.

## The object (one paragraph, binding)

A number is an expansion in TWO infinitesimals at once. **ε (analytic grading):** perturbation of the input; lanes compose by the chain rule; this is the closed exact-jet algebra (HR131), unchanged. **υ (substrate grading):** perturbation by the machine; lanes carry the *exact* rounding residues of operations, composed by the error-free-transformation laws (TwoSum: a+b = s+e exactly, e ∈ 𝔽 — floating point relocates information, it does not destroy it). **Mixed lanes (∂ε∂υ):** substrate damage propagated through analytic sensitivity = claim-conditioning, computed not classified. Truncation orders (m,k) are typed claims: the υ-cascade truncated at order k is itself reported at u^(k+1) scale. The υ-composition law is value-dependent — a connection on the computation graph; route differences are its path-dependence; closed rewrite loops measure its holonomy (Stage C).

## Non-goals (hard fences)

1. **No substrate edits.** Eval-tier entry only, via the Option-B registry (`tests/_audit_helpers/eval_tier_operations.py`, entries cite this brief). Promotion is a separate future event.
2. **No transcendental υ-exactness.** sin/cos/exp/log υ-entries are typed `BOUNDED` (correctly-rounded-libm half-ulp bound or honest `UNKNOWN`), clearly marked; exact transcendental residues are a future campaign. Stage A's exact coverage is the rational core + sqrt only.
3. **No route optimization / lattice navigation.** Stage C *measures* route difference; choosing routes is future work.
4. **No separator revision in-campaign** (see above).
5. **No naming** (see covenant).
6. **No re-derivation of compensated-arithmetic lore.** Thirty years of EFT literature is MINED AND CITED (Phase 0), never re-proved. Re-deriving Ogita–Rump–Oishi is the loop in a new costume.

## Phase 0 — pre-reads, literature pass, sufficiency gate (STOP for Will after)

**Mandatory pre-reads & closed-results check (cite each):** HR129 (G2≡S2, jet vocabulary), HR130 (the quiet; E-rule failure pattern), HR131 (exact-jet closure; §3 forgiveness observation; §5 gap text verbatim), `RESULT_TYPES.md` Amendment 1, `results/exact_jet_f1a_rerun/RESULT_TYPES_AMENDMENT_PROPOSAL.md` (pin `0a80bc05…`), the eval-tier registry + its three invariants, glossary §13 (JetBundle vs derivative jets), BACL / Conjecture C / c2 theorem statements (they become test oracles), `CAMPAIGN_SEPARATING_ESTIMATOR_DRAFT.md` (consumer context only).

**ORO literature pass (deliverable: `results/bigraded_jet/CITATIONS.md`):** map every EFT identity the implementation will use to its source + exactness preconditions. Minimum set: Dekker 1971 (Fast2Sum + splitting); Knuth TwoSum (unordered); Ogita–Rump–Oishi 2005 *Accurate Sum and Dot Product* (compensated algorithms + ill-conditioned generators — the Stage-A battery source); FMA-based TwoProd and division/sqrt residues (Muller et al., *Handbook of Floating-Point Arithmetic*; Boldo–Muller); Higham *ASNA* ch. 4 (context + bounds the laws replace); Squire–Trapp 1998 complex-step (historical cousin, cited for lineage). Each identity entry: statement, source, preconditions (no overflow; binade constraints), what the implementation does when preconditions fail (**typed flag, never a wrong zero**).

**Primitive-sufficiency gate:** enumerate typed parents. Expected: TypedResult carrier (exists), eval-tier registry (exists, Option B), exact-jet ε-algebra (exists, closed). **Platform check (genuine Phase-0 unknown): `math.fma` availability** — if present, TwoProd/div/sqrt residues via FMA; if absent, Dekker splitting for TwoProd (exactness preserved, more ops) and document the route in CITATIONS.md. Any *missing* parent: STOP and present the micro-task list — do not build parents unapproved.

**Phase 0 report to Will, then STOP.**

## Stage A — υ alone: J^(0,1) (STOP for Will after)

**Deliverable:** `src/lloyd_v4/evals/bigraded_jet.py` (or `evals/upsilon_lanes.py` — executor's call, recorded) — typed compensated arithmetic under the membrane: private internal algebra, every op feeds the accumulator, υ-residues live in the value object, ONE TypedResult per evaluation. Eval-tier operation_id registered with citation to this brief. Coverage typing per op: `EXACT` (add/sub/mul/fma; div and sqrt residues via FMA where available) / `BOUNDED` / `UNKNOWN` — coverage is part of the value, honestly marked.

**Tests (the theorems become oracles):**
- Identity battery: per-op exactness vs 200-bit mpmath reconstruction.
- **BACL oracle:** every subtraction residue satisfies lattice membership where the theorem's preconditions hold — three months of proofs, recast as assertions.
- **Conjecture-C / c2 invariants** on the frozen boundary battery's residue streams.
- **ORO battery:** compensated sum/dot built *from the υ-lanes* on the cited ill-conditioned generators (condition numbers spanning to ~1e16).
- Membrane integrity (op counts vs frozen battery), byte-determinism, typed-refusal totality.

**Pre-registered predictions (freeze in the Stage-A manifest before implementation):**
- **A-P1 (exactness):** for every `EXACT`-covered op in the frozen battery, value ⊕ residue reconstructed at 200-bit precision equals the true real-arithmetic result of that operation with **zero gap**; every precondition violation (overflow, subnormal-edge) emits a typed flag — no silent wrong zeros.
- **A-P2 (lattice law):** 100% of in-precondition subtraction residues pass the BACL membership check; Conjecture-C / c2 invariants hold on the frozen boundary set.
- **A-P3 (literature reproduction):** lane-built compensated summation/dot reproduces the ORO reference results on the cited battery — equal to the 200-bit-truth-rounded-to-double wherever cond·u² ≪ 1, per the cited theorem, with the campaign reporting the measured boundary.

**Stage-A report (incl. `## Names that fell out`), then STOP.**

## Stage B — fusion: J^(2,1) (STOP for Will after)

**Deliverable:** the ε-algebra (exact_jet) and υ-lanes fused in one membrane: each ε-lane carries its υ-residue account; **mixed lanes** compute claim-conditioning = (operand υ-damage) × (jet-supplied sensitivity ∂quantity/∂operand). Conditioning becomes a *computed continuous quantity*; the 26/40 + 60/150 strata survive **as display mapping only** — nothing triggers on them.

**Pre-registered predictions:**
- **B-P1 (non-perturbation):** the ε-content of J^(2,1) on the full F1a ladder is **byte-identical** to the closed J^(2,0) records (HR131 pins verified) — fusion adds lanes, never perturbs them.
- **B-P2 (the gap grades the object):** mixed-lane claim-error prediction for κ at rungs k=8..15 falls within a frozen factor band **[1/8, 8]** of the measured |κ_jet − arbiter| per rung — reproducing HR131 §3's forgiveness (28–51 binades of operand damage, ~zero claim error) **from the lanes alone**, no thresholds anywhere in the path.
- **B-P3 (strata demoted to display):** computed claim-conditioning, passed through the declared display strata, reproduces the HR131 stratification within **±1 rung** (WELL→WARNING k=8±1; →ILL k=12±1).

**Stage-B report, then STOP.** (This is the result that re-specifies the separator.)

## Stage C — the connection made visible (STOP: campaign close)

**Fixture (frozen):** two algebraically equivalent routes for the same quantity — minimum pair `(a−b)·(a+b)` vs `a²−b²` over a frozen operand battery spanning Sterbenz-exact and lossy-cancellation regions (the E primitive identifies which is which — consume it, don't rebuild it). Plus one closed rewrite loop over the route pair.

**Pre-registered predictions:**
- **C-P1 (phenomenon invariance):** ε-lanes bitwise identical across routes at every battery point.
- **C-P2 (lanes own the gap):** per point, the υ-lane difference between routes equals the measured float-value difference between the routes **exactly**, wherever coverage is `EXACT` — the lanes account for route-dependence to the last bit (B4, carried per-evaluation).
- **C-P3 (holonomy):** the closed-loop υ-transport reading is **zero on Sterbenz-exact segments**, nonzero where fingerprints differ, and equals the lane-predicted value exactly — recorded as the **first measured curvature of the substrate connection**. Candidate scoreboard addendum; placement is Will's.

**Campaign close-out:** report, HR row draft (HR132+, reserved to Will), ledger update, `## Names that fell out` consolidated across stages.

## Standing rules (inherited, binding)

Membrane Rule per Amendment 1 (υ-lanes live INSIDE the one TypedResult; the `events` tuple is the docking slot). Commits cite scoreboard rows / this brief. Canonical worktree only. V3/OG are oracle and reference — zero imports, zero source reads (frozen-token source audit inherited from HR131, list unchanged). Degenerate cases → typed refusals; no escaping exceptions. Gaps are filed with reasons, never retuned in-campaign. Each stage: manifest frozen + pinned BEFORE implementation; predictions graded mechanically; byte-stable re-run; full suite exit 0 at stage close. Missing-parent discoveries STOP the campaign for approval.

## Acceptance criteria

1. Phase-0 pre-reads cited; CITATIONS.md complete; sufficiency gate reported; platform fma route recorded.
2. Stage manifests frozen pre-implementation with predictions verbatim; mechanical grading in `prediction_verdicts.json` per stage.
3. A-P1..3, B-P1..3, C-P1..3 graded (PASS/FAIL each — a FAIL stops the stage for Will, it does not soften the prediction).
4. Full suite exit 0 at each stage close; byte-stable re-runs; source audit clean.
5. Records under `results/bigraded_jet/stage_{a,b,c}/`; HR draft rows produced; ledger updated at each close.
6. Naming covenant honoured: candidates recorded, none adopted.
