# Claude Code Handoff — 2026-05-19

**Purpose:** Orient on the new strategic direction (M⊕C⊕G decomposition as V4's generative core; V3-on-V4 composition architecture) and the *gated readiness sequence* that must be cleared **before** any unification campaign is pre-registered.

**Status:** Direction confirmed. Campaign **NOT** started and **must not** start until all gates are green. This handoff defines the gates, their acceptance criteria, and the scheduling inversion that governs execution order.

**Prior context:** [`session_handoff_2026_05_18_bacl_substrate_invariant_arc.md`](session_handoff_2026_05_18_bacl_substrate_invariant_arc.md) — BACL proven, c2 lattice theorem, Conjecture C, fingerprint atlas, dual-arm probe. Read it first; this handoff builds directly on it.

---

## TL;DR — the direction

V4 stops being a scattered set of substrate observations and becomes a **generative engine with one master invariant and one decomposition law**, structurally mirroring what K_G + D⊕S=P were for V3 — but with a *proven* substrate floor underneath, which V3 never had.

- **Master invariant:** the BACL-deviation observable. Lattice-rank deficit relative to the BACL-mandated minimal route is *simultaneously* the route fingerprint (forensic) and the bloat metric (remediation). This duality is V4's K_G-equivalent.
- **Decomposition law:** **R = M ⊕ C ⊕ G** (measured Residue = substrate-**M**andated ⊕ **C**onditioning ⊕ **G**eometric/representational signal). This is V4's D⊕S=P-equivalent. **M is provable (BACL); D⊕S=P never had a proven term.**
- **Architecture:** V3-on-V4 by **composition, not reimplementation**. V4 is the proven Layer-4 metrology that certifies V3's Layer-3 geometry. V3's domain adapters are *wrapped and certified*, never rebuilt.
- **Ultimate target (NOT yet a campaign):** prove M⊕C⊕G is the substrate-level shadow of D⊕S=P. If true, V4 is not a second engine — D⊕S=P extends to the substrate *with a proof attached*, and the entire V3 deliverable catalogue inherits the floor.

This handoff is about **earning the right to start that campaign**, not starting it.

---

## The architecture (calibrated)

### Master observable
The deviation of a computation's residue from the BACL-mandated integer-ulp lattice is one quantity read with opposite intent:
- **Forensic:** which algebraic route produced this result (fingerprint atlas / barcode).
- **Remediation:** how much avoidable rounding this route carries (refinery / bloat metric).

Operational consequence already established: **fingerprint first, refine second, never the reverse.** Refinery normalises routes and therefore erases the route-distinguishing residue the atlas reads. Any pipeline that refines upstream of fingerprinting is sterilising its own evidence.

### The decomposition
| Term | Meaning | Maturity | Mechanism |
|---|---|---|---|
| **M** | Substrate-mandated lattice structure; zero physical information by construction | Primitive **proven** (BACL); operational clause **open** | Binade spacing (BACL) |
| **C** | Conditioning amplification (ill-conditioning, catastrophic cancellation) | **Undefined** — residual definition only | Hypothesised: V3 Hessian/eigenvalue apparatus |
| **G** | Geometric / representational signal — the target | **Doubly residual**; candidate observables measured pre-decomposition only | TBD |

### Three-attack resolution (why this architecture *is* the thesis defense)
- **Attack #3 (self-reference: Hessian conditioning and signal scale identically):** dissolves — M is provably separable, so signal and substrate stop being indistinguishable for the slice M covers.
- **Attack #1 (non-algebraic singularities → meaningless exponents):** becomes an honest **OUT-OF-SCOPE** verdict from the three-verdict certifier. Refusing to answer is a deliverable, not a failure.
- **Attack #2 (family-dependence / transversality):** becomes a concrete **G-invariance test across families**.

The engine architecture and the falsifiability defense are the same object. Build one, you get the other.

---

## Maturity audit — carry this honesty forward

**Do not let the elegance of the architecture license premature confidence. The most mature asset in V4 is the methodology discipline, and the single biggest threat to it is that this architecture is seductive enough to start a campaign on before C exists.**

- **M:** BACL primitive solid (proven, multi-format, ~31k records). BUT the exact-result clause (open problem #5) — the clause M-subtraction operationally *needs* — is **open and mode-dependent**. Conjecture C is currently on the **(A) branch**: libm-grounded with a libm cross-check (hardcoded `0x6a09e667f3bcd`, the float64 mantissa of √2, sourced from libm then checked against libm). The definition-grounded recompute has been *run and passed* (1,022/0) but is **not yet landed** into the report, and the precision-bound lemma is **not written**.
- **C:** maturity **zero**. Residual definition ("everything not M or G"). Proposed instrument (V3 Hessian eigenvalues) is an **untested hypothesis**.
- **G:** doubly residual. σ1 = 1.000 and the α−1 family were measured on **raw, pre-decomposition** residue. They are *candidate* G observables, not established ones.
- **⊕:** asserted, not shown. Separability of M, C, G is unproven; entanglement near binade boundaries is a live possibility.

**Net:** one leg proven-but-incomplete, one leg undefined, the ⊕ unproven, existing tooling measures pre-decomposition quantities. **Not campaign-ready.**

---

## The gate sequence

Gates are dependency-ordered **except Gate 3**, which is a cheap global kill-switch and is **pulled to the front, out of order**, deliberately.

### ▶ Gate 3 — KILL-SWITCH (RUN FIRST, before Gates 1–2)

**Why first:** cheapest possible falsifier of the entire program. A negative result here makes Gates 0/1/2/4 and the whole campaign moot. Highest expected value action available. ~1 day.

**Requirement:** take **one** singularity fixture — Schwarzschild gravitational redshift approaching the horizon, *or* a conical compatibility singularity from the GR paper. Compute the blowup exponent / G-candidate observable **twice**: (i) raw residue, (ii) M-subtracted (BACL-mandated component removed). Additionally audit **BACL hypothesis coverage** in that fixture's deep-cancellation regime — does `ulp(a) ≥ ulp(b)` actually hold where the interesting cancellation happens, or is the subtractable floor thin exactly where it's needed?

**Pre-register the decision rule BEFORE running (binding):**
- If σ1 = 1.000 (or the relevant G observable) **survives M-subtraction substantially unchanged** → G is plausibly real post-decomposition → **GREEN**, proceed to Gate 0.
- If it **degrades or vanishes** under M-subtraction → the candidate G was substrate-universality masquerade → **HALT**, the architecture's G term is artifact, reassess before spending an hour on the expensive gates.
- Record coverage fraction regardless; if BACL hypothesis coverage in the cancellation regime is low, flag the M-subtraction reach as scope-limited even on a GREEN.

**Acceptance:** experiment run, decision rule applied as pre-registered, verdict + coverage fraction recorded in a closeout following `CAMPAIGN_DISCIPLINE.md` conventions.

---

### Gate 0 — Close Conjecture C

**Status:** ~80% done; the hard part (definition-grounded recompute) already passed in analysis. This is *landing + lemma*, not new research.

**Requirement:**
1. Land the definition-grounded recompute into `conjecture_c_proof_audit/`: replace the `math.sqrt` + hardcoded `0x6a09e667f3bcd` construction with exact-mpmath-√ → round-to-nearest-even-from-definition over the 1,022 odd-k normal-range boundaries. (Verified result: definition-grounded R_above matches libm in every case, matches the original bit pattern, R² > 2^k strict in every case. 1,022/0.)
2. Write the **precision-bound lemma**. Spine: for α = √(2^k), any dyadic rational p/2^q satisfies |2^k − p²/2^(2q)| ≥ 1/2^(2q) (nonzero integer over 2^(2q)), hence |√(2^k) − p/2^q| ≥ 1/(2^(2q)·2√D); plug q ≈ 53, D ≈ 2^k for an explicit minimum separation; state the mpmath working precision actually used; show it clears the bound. Add the one-liner that **ties-to-even is vacuous here**: √(2^k) for odd k is irrational, float64 midpoints are dyadic, an irrational is never a dyadic rational, so no tie can occur in any of the 1,022 cases — deletes an entire fragility class.
3. Note in the closeout that the even-k enumeration proves nothing (even k ⟹ √(2^k)=2^(k/2) exact, R·R=2^k exact, RN(2^k)=2^k); the entire deductive load reduces to **RN monotone + odd-k boundary strictness**. State the proof's minimal spine that bare.

**Acceptance:** c2 lattice theorem's only non-deductive atom is gone. No libm trust, no asserted bit patterns, no "looked like enough." Closeout updated. `C_proven` is then *honestly* `C_proven`.

---

### Gate 1 — Prove BACL's exact-result clause (open problem #5)

**Requirement:** prove the operational clause M-subtraction needs: not merely that the *real* difference a−b lies on the j·ulp(b) lattice (trivially true under hypothesis), but **when the floating-point result fl(a−b) is exactly equal to a−b** (e = 0). This is mode-dependent — characterise the dependence; do not paper over it. State the theorem connecting the BACL exact-result set to the **TwoSum e = 0 set** (conjectured equality — prove or bound it).

**Acceptance:** a proven predicate of the form "given (a,b) satisfying the BACL hypothesis and [explicit conditions], fl(a−b) = a−b exactly," with scope and rounding-mode dependence explicitly stated. Until this exists, M-subtraction is *describable but not deployable*.

---

### Gate 2 — Define C positively (the crux)

**Requirement:** C must stop being "everything that isn't M or G." Test the hypothesis that V3's Hessian-eigenvalue / condition-number apparatus **is** the C instrument. Build a C-extractor. Characterise C on fixtures with *known* conditioning: well-conditioned controls vs deliberately ill-conditioned / near-singular fixtures. Name the mechanism (methodology lesson #2 — a frozen/undefined term without a named mechanism is a discipline failure).

**Acceptance:** C is a positively-defined, measurable quantity with a named mechanism, pre-registered, carrying three-verdict scope honesty. Proof preferred; a pre-registered empirical model with explicit scope is the minimum bar. **Nothing downstream is honest until this gate is green.**

---

### Gate 4 — Establish ⊕ (separability)

**Requirement:** on one trusted fixture, test whether M, C, G are additively separable or entangled. Subtract M, bound C, check G is stable under probe perturbation and that cross-terms vanish (or characterise the entanglement and reformulate the decomposition if they don't).

**Acceptance:** separability empirically established within stated scope, OR entanglement characterised and R = M ⊕ C ⊕ G restated accordingly. The ⊕ notation must be earned, not asserted.

---

### Only then — the unification campaign

With Gates 0–4 green, **M ⊕ C ⊕ G ≟ D⊕S=P** may be pre-registered as a campaign on a foundation where every term is defined, M is proven, and separability is at least empirically established. Not before.

---

## Hard rules — non-negotiable discipline (carried from prior arc)

1. **Do not start the unification campaign until every gate is green.** Your own pre-registration discipline will force an embarrassing mid-campaign halt around iteration 3 if C is still undefined. The elegance of the architecture is the risk, not the reassurance.
2. **Pre-registration is binding pre-measurement.** Especially Gate 3's decision rule — write it, freeze it, then run.
3. **Sampling is evidence; exhaustive enumeration over a finite-defined domain is proof.** Keep the distinction explicit in every closeout.
4. **When freezing/deferring a sub-result, name the mechanism that fails.** No residual definitions surviving into the next gate.
5. **Three-verdict honesty everywhere:** CERTIFIED / CLEAN-IN-SCOPE / OUT-OF-SCOPE. Refusing to answer in the out-of-scope regime is a feature.
6. **Composition, not reimplementation.** Do not rebuild K_G, D⊕S=P, or the 38 adapters inside V4. V4 wraps and certifies V3's output. If you find yourself porting V3 logic into V4, stop — that's the wrong architecture.
7. **BACL leverage is the well-conditioned regime only.** Deep cancellation is OUT-OF-SCOPE by construction (~96–98% off-lattice regardless of route). Never claim V3-equivalent *universality*; claim V3-equivalent *deliverable types with explicit scope verdicts*.

---

## Immediate next action

**Run Gate 3 (kill-switch) — first, before anything else.** Pick the fixture (Schwarzschild horizon approach is the cleaner starting choice), pre-register the decision rule from the Gate 3 spec verbatim, compute raw vs M-subtracted G-observable, record verdict + BACL coverage fraction. One day's work. A negative result saves the entire program; a positive result is the first real evidence the edifice stands.

Do **not** begin Gate 0/1/2 work until Gate 3 returns GREEN.

---

## File / repo integration

Follow existing `Lloyd_Engine_V4/Build_Docs/` and `CAMPAIGN_DISCIPLINE.md` conventions. Relevant existing artifacts:

| Artifact | Role in this campaign |
|---|---|
| `Build_Docs/Reports/conjecture_c_proof_audit/` | Gate 0 target — land definition-grounded recompute + precision lemma here |
| `Build_Docs/Reports/c2_lattice_sharpness_audit/` | c2 theorem inheriting C; update scope language post-Gate-0 |
| `Build_Docs/Reports/bacl_invariant_audit/` | M primitive; Gate 1 (exact-result clause) extends this |
| `Build_Docs/Reports/blowup_exponent_v4_audit/` | Gate 3 — raw G-observable baseline (σ1 = 1.000) to compare M-subtracted against |
| `Build_Docs/Reports/substrate_fingerprint_atlas_phase_delta/` | Master-observable extractor (forensic side) |
| `Build_Docs/Reports/hardened_dual_arm_probe/` | Seed of the V4-holonomy / G-path-invariance deliverable (post-campaign) |
| V3 `lv3_`-prefixed tools (Hessian eigenvalues, K_G) | Candidate **C instrument** — Gate 2 |

New reports for Gates 0–4 should be created as siblings under `Build_Docs/Reports/` with pre-registry + closeout + byte-stable artifact, matching the established pattern.

---

## Open theorems / parked (post-campaign)

- **The unification theorem:** M⊕C⊕G ≟ substrate shadow of D⊕S=P. The single highest-value target — but downstream of all gates.
- V4-holonomy (G-invariance under computation path) as the centrifuge-equivalent deliverable.
- M/C crossover detector as the near_umbilic-equivalent (singularity localisation).
- G-trajectory drift as the Predictive-Gap-equivalent.
- BACL literature audit (expected verdict: "folklore, confirmed" — does not block any gate; cleanup only).
- float128 BACL verification; BACL under non-RN modes; Lean/Coq formalisation of BACL.

---

*Discipline reference: `Lloyd_Engine_V4/Build_Docs/CAMPAIGN_DISCIPLINE.md`. Strategic derivation: 2026-05-18/19 conversation arc — BACL substrate invariant → forensic/refinery duality → M⊕C⊕G generative core → V3-on-V4 composition → gated readiness audit.*
