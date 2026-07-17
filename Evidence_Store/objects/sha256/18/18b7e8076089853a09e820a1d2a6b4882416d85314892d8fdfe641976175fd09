# MCG Discovery Campaign — Handoff — 2026-05-19

**Purpose:** Build the MCG idea. This is a **discovery campaign**: research and testing to *find and characterize* candidate primitives and invariants that carry the structural "shapes" the M ⊕ C ⊕ G decomposition needs. It is exploratory and inductive, not confirmatory.

**Status:** This supersedes the *gate/kill-switch campaign* framing for MCG. That framing was the error — it applied confirmatory machinery (pre-registry, kill-switch, EP predictions) to a research direction that had not been started. **Gate 0 results stand and are untouched** (see "Leave alone").

**Prior context:** `session_handoff_2026_05_18_bacl_substrate_invariant_arc.md` (BACL/c2/Conjecture C state) and the conversation arc of 2026-05-18/19. Provenance anchor, not a reading assignment.

---

## TL;DR — what MCG actually is, and what this campaign does

MCG asks whether a computation's measured floating-point residue admits a meaningful decomposition **R = M ⊕ C ⊕ G**:

- **M — substrate-mandated.** **SOLVED.** This is BACL: the BACL-mandated integer-ulp lattice component. M is not a research question; it is a **tool**. M-subtraction is used to *filter* candidates, not as a test.
- **C — conditioning.** Undefined. Needs a *positive definition with a named mechanism*. Candidate instrument: V3's existing Hessian / eigenvalue / condition-number apparatus.
- **G — geometric / representational.** Undefined. The heart of this campaign. The task is to **find** candidate observables that survive M-subtraction, are not explained by C, and carry fixture- / route- / geometry-discriminating structure **with a named mechanism for why**.

This campaign **finds and characterizes** candidates for C and G. It does **not** pre-register tests of them. Confirmatory work comes later, gated, only after a mechanism-bearing candidate exists.

---

## Carried forward — already done, do not redo or relitigate

- **BACL** — proven, multi-format. M = solved tool.
- **Conjecture C** — definition-grounded (Gate 0 landed this session: mpmath-from-definition recompute, precision-bound lemma, tie-impossibility one-liner, minimal-spine note). Independent substrate result. **Leave alone.**
- **c2 lattice theorem** — tightened to j_BACL ∈ {−1, 0, +1} (Amendment IV). Keep.
- **Forensic/refinery duality + three-verdict bloat certifier** — real, sound, MCG-independent. **This is the strongest existing seed for a G candidate** (it already has a mechanism). Feeds Phase 1 as candidate **G-1**.
- **Methodology constraint** — cancellation-residue-type observables are substrate-dominated *by construction* and are excluded as G candidates (this is Discipline Rule 4, not a narrative).

---

## The central correction (stated once)

A sound protocol applied to a non-hypothesis produces a confident non-result that looks rigorous and is therefore dangerous. The prior MCG attempt skipped the only first step — *designing what G is* — and leapt to a kill-switch around an undefined observable, which then "failed" tautologically. **Discovery phase ≠ confirmatory phase.** Looking, sifting, prototyping, following hunches *is the work* in Phases 0–2. Pre-registration / kill-switches apply only at Phase 3+, once a candidate has a named mechanism. That distinction is the spine of this campaign.

---

## Phase 0 — Operational criteria for a G candidate (the skipped step)

Define what makes something a G candidate *before* enumerating any. A candidate is an observable `O(fixture, route)` such that:

1. **Computable** from the residue.
2. **Survives M-subtraction** — after the BACL-mandated integer-ulp component is removed, `O` retains nonzero structure. (Failing this → it is M. This is the filter the c2-cancellation residue failed by construction.)
3. **Discriminates** — the retained structure varies with something of interest: fixture identity, algebraic route, or constraint-surface geometry.
4. **Has a named mechanism** — a stated reason *why* `O` would carry that discrimination, and *why that mechanism is not merely C (conditioning) or M (substrate)*.

Phase 0 deliverable: this list, ratified/sharpened by CC into the campaign's working definition. Cheap. Do first.

---

## Phase 1 — Candidate enumeration & characterization (the core, discovery)

Generate a slate of candidate observables. For **each**: definition, mechanism hypothesis, structural risk of being M or C, and what an exploratory positive vs. null *characterization* looks like (a characterization — **not** a kill-switch, **not** pre-registered).

### Seed candidate G-1 — post-M-subtraction route divergence (strongest; mechanism already exists)

- **Definition:** for two algebraically-equivalent routes `r1, r2` computing the same value on the same fixture, compute each residue, subtract the BACL-mandated M component from each, measure divergence of the *remaining* structure between routes.
- **Mechanism:** distinct algebraic routes traverse distinct operation sequences; the off-lattice residue (the part M does not mandate) encodes route-specific rounding history. If this divergence varies with constraint-surface geometry rather than arbitrary route choice, it carries G.
- **Confound control:** must show divergence is not merely C — compare routes of *equal* conditioning so any divergence cannot be attributed to differing condition number.
- **Exploratory positive:** nonzero, structured, route-discriminating divergence that correlates with a geometric property across fixtures of differing geometry.
- **Exploratory null:** divergence is pure conditioning or unstructured noise → drop, record as filtering information.

### Further seed candidates (enumerate with same template)

- **j_BACL sequence structure** — not the collapsed residue (that is M), but the *pattern/sequence* of which lattice point j is selected across a sweep. BACL mandates the residue is *on* the lattice; it does **not** mandate *which* point. Mechanism to be stated; confound risk: C may drive j-selection.
- **Cross-binade transition statistics** under route or geometry variation. Mechanism TBD; high M-risk near boundaries — Phase 0 criterion 2 must be checked hard.
- **Fingerprint-atlas slot structure after M-subtraction** — which atlas slots retain discriminating power once M is removed.

### Anti-candidates (excluded up front)

Cancellation-residue-type observables (e.g. σ1 on c2-style residue). Substrate-dominated by construction. Do not propose as G.

Phase 1 deliverable: characterized candidate slate with mechanisms; ranked by which survive M-subtraction *and* have a stated mechanism. No tests pre-registered.

---

## Phase 2 — Positive definition of C (parallel track)

Build a positive C-extractor from V3's Hessian / eigenvalue / condition-number apparatus. Characterize C on fixtures with **known** conditioning: well-conditioned controls vs. deliberately ill-conditioned / near-singular fixtures.

- **Mechanism:** conditioning amplifies substrate error through ill-conditioned maps; C should track condition number / Hessian spectrum monotonically on known-conditioning fixtures.
- **Acceptance:** C is a positively-defined, measurable quantity with a named mechanism and a characterized response on known-conditioning fixtures — **not** "everything that isn't M or G."

Runs in parallel with Phase 1. Discovery, not confirmatory.

---

## Phase 3 — Separation probe (FIRST confirmatory step; gated)

**Entry gate:** ≥1 Phase 1 G-candidate with a named mechanism survives M-subtraction **AND** Phase 2 has produced a positively-defined C. Not before.

On one fixture, test whether M (proven), C (Phase 2), and the surviving G-candidate(s) are additively separable or entangled. **This is where pre-registration re-enters** — because now there is operational content to confirm or falsify. Pre-registry, decision rules, positive controls apply here, correctly, for the first time.

---

## Phase 4 — Unification question (last; gated behind Phase 3 separability)

Only if Phase 3 shows separability: is M ⊕ C ⊕ G the substrate shadow of D⊕S=P? The original ambition, correctly placed last, gated behind everything actually existing.

---

## Discipline rules (load-bearing only)

1. **Discovery vs confirmatory.** Phases 0–2: look, sift, prototype, characterize freely. Confirmatory machinery (pre-registry, kill-switch, EP predictions) is **forbidden** until Phase 3.
2. **Named mechanism is the graduation gate** from "investigate" to "test." Required before *testing*, never before *investigating*.
3. **M is a filter, not a test.** An observable that vanishes under M-subtraction is substrate — drop it. That is successful filtering, not a HALT, not a severity event.
4. **Exclude cancellation-residue-type observables** as G candidates (substrate by construction).
5. **Negative exploratory results are filtering information.** Do not severity-rate routine discovery outcomes. Report, drop or keep, move on.

---

## Immediate next action

1. Ratify/sharpen Phase 0 criteria into the campaign working definition (cheap, first).
2. Begin Phase 1 characterization of **candidate G-1 (route divergence)** on 2–3 fixtures of differing geometry — exploratory, no pre-registration. Equal-conditioning route pairs to control C.
3. In parallel, begin Phase 2 C-extractor build using V3's Hessian/eigenvalue apparatus on known-conditioning fixtures.
4. Report characterizations. Iterate the candidate slate. No Phase 3 work until its entry gate is met.

Create campaign reports under `Build_Docs/Reports/mcg_discovery/` following existing `CAMPAIGN_DISCIPLINE.md` conventions, but tagged **discovery** (characterization logs, not pre-registries) for Phases 0–2.

---

## Leave alone

- **Gate 0 / Conjecture C** — definition-grounded, landed, independent of MCG. Do not reopen.
- **BACL, c2, Amendment IV** — proven/tightened. Stand as-is; M is consumed as a tool here, not re-derived.

---

*Scope: this campaign builds MCG from step zero — defining and finding C and G — as the user originally intended. The gate/kill-switch framing is retired for MCG. Confirmatory discipline returns at Phase 3, applied to something real.*
