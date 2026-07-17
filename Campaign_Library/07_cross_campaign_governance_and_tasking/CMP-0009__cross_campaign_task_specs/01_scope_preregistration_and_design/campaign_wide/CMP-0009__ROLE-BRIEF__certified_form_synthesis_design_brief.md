# Certified Form Synthesis — design brief (DRAFT)

**Status:** DRAFT 2026-06-11 — Claire-authored, awaiting Will's review. **KILL-SEARCH EXECUTION OWED before any novelty claim** (§6; execution gates claims, not the build).
**Provenance:** HR134 closeout §9 door 4 + §10(d) QUEUED ledger stub; LIVE_CAMPAIGNS_LEDGER `certified-form-synthesis` entry.
**Naming covenant:** working path token `certified-form-synthesis`. Restart traps per ledger: "algebraic form generator", "perfect pitch compiler", "certified Herbie", "typed rewriting", "substrate-aware compilation", "fluent form compilation" — all THIS.
**Scoreboard rows:** B3/B4/B5 leverage (route laws as compilation substrate); ENDGAME bench-tier application.
**Dependency:** route-agreement registry (predecessor brief, same date) — the law supply. CFS mines nothing itself.

## 1. Thesis

Law-based, not search-based: **mine** (registry) → **certify once** (tower/canonicalizer, authoring time) → **compile fluently** (forward static analysis). Runtime is law application only. An uncertified rewrite is a type error. Output ships as **form + region guard + certificate**.

The field's strongest tools certify *bounded* error (§6). CFS certifies *exact agreement*: within the guard region the emitted form and the source form are the same function under a certified identity whose exactness-protection conditions hold — residual ≡ 0, H5-class, not |error| ≤ ε.

## 2. Consumed vs built

Consumed from HR134 (import, never rebuild): EFT lift; protection predicate L1–L4; classifier artifact format; B-P2 canonical coefficient vectors; witness-derivation pattern. Consumed from the registry: WARRANTED laws with region guards.

**THE one new build: protection typing as forward static analysis over lattice types.** Authoring-time inference walks the expression carrying a protection type (which L1–L4 conditions hold, on what region); a rewrite step is admissible iff a WARRANTED law's guard covers the inferred region; guard composition is tracked through the walk. No other new machinery.

## 3. Architecture sketch

Authoring time: source expression → registry query (applicable laws by canonical form) → admissible rewrite chains (every step law-backed; chain certificate = composed law certificates + intersected guards) → emit (form, guard, certificate). Runtime: guard check → apply form; guard violation → typed refusal (refuse-over-degrade, standing law 5). No runtime search, no runtime error estimation.

## 4. Option-A trigger evaluation (HR131 re-open condition) — REQUIRED RULING

HR131 recorded: per-op typed scalars are built when a consumer demonstrates per-op granularity need. Analysis: the forward static analysis operates at authoring time over types and regions — symbolic, not per-op runtime scalars. The protection predicate instantiates per-op *conditions*, not per-op *values*. **Claire-preliminary verdict: trigger NOT pulled by the static path.** Possible pull-path: if real guard sets turn out to need runtime per-op witnesses (e.g. a guard expressible only as "this intermediate is Sterbenz-protected at runtime"), the trigger fires. Recommendation: rule the static path now; re-evaluate at Stage 1 with the first real guard set. **Will rules.**

## 5. Pre-registered success shape (grading currency; freezes at campaign-brief time)

Given a fixture expression class: (i) emitted form agrees with source EXACTLY (exact-ℚ arbiter) at every point of a pinned grid inside the guard; (ii) outside the guard the system refuses, never emits; (iii) zero unflagged confidently-wrong across the battery; (iv) comparison column vs classical "improved" forms (bounded-error class) recorded as telemetry, permanently non-verdict-bearing.

## 6. Kill-search (protocol defined here; EXECUTION is PAPER-ORIENTED, parked)

> **Note (Will, 2026-06-13):** kill-search is a prior-art / novelty sweep — a *publication* concern. Its execution and artifacts are paper-oriented and parked with the paper work in `Build_Docs/paper/` (the prior precision-flow kill-search lives there as `KILL_SEARCH_BRIEF.md` / `KILL_SEARCH_LEDGER.md`). It is a pre-publication step, **not** a pre-build gate on CFS — CFS R&D proceeds on Will's review of this brief. The protocol below is retained as design.

Fronts — three owed by the closeout, two added from the 2026-06-11 literature pass [V = verified in that pass; TK = training-knowledge, deep-read owed]:

1. **Gappa** [TK] — proves bounds AND exactness facts (Sterbenz-class) for *given* forms/scripts; checks, does not synthesize, does not mine. Differentiation hypothesis: CFS generates and certifies; Gappa is a candidate external cross-checker (CONSUME-optional; see levers audit door 4).
2. **Herbie + egg** [V] — equality-saturation search; dynamic, unsound error measure (sampled average ULPs); rewrite rules documented unsound in print (egglog paper §6.2: "known to be unsound… cause of numerous bugs"). Differentiation: search vs law; empirical average-case vs certified exactness; no guard-as-type.
3. **FPTaylor** [V] — symbolic-Taylor worst-case bounds; analysis, not synthesis.
4. **Daisy (Rosa successor)** [V] — **STRONGEST NEIGHBOUR, added front; collision risk lives here.** Sound source-to-source compiler from real-valued specs; genetic-programming rewriting guided by sound static bounds; internal exact rationals; mixed-precision tuning. Differentiation hypothesis: Daisy is search-then-verify with *bounded-error* certificates; CFS is derive-from-law with *exactness* certificates and a machine-mined law supply; no protection typing, no region-guard-as-type, no residual-≡-0 claim class. Deep-read owed to confirm.
5. **Salsa / PRECiSA / VCFloat / Chassis** [V, sweep-level] — bounded-error transformation / verified symbolic bounds / Coq FP reasoning / target-aware Pareto synthesis. Sweep-read owed; expected same class as front 4.

Protocol: precision-flow pattern — per-front deep-read; per-claim collision/no-collision verdict; documented-silence standard; ledger filed with the paper work in `Build_Docs/paper/` (alongside the precision-flow `KILL_SEARCH_LEDGER.md`). Claims under test: (a) law-based synthesis (vs search-based); (b) exactness-class certificates (vs bounded-error); (c) machine-native law mining from measured route agreement; (d) protection typing as forward static analysis.

## 7. Staging sketch (each stage gets its own brief through TASK_TEMPLATE)

Stage 0: registry interface freeze + lattice-type design + Option-A ruling + kill-search execution. Stage 1: forward-analysis prototype, rational class, pinned fixtures. Stage 2: end-to-end compile + grading per §5.

## 8. Fences

No law mining inside CFS (registry's job). No substrate edits. Rational class first. Not a general compiler; not precision tuning; not bounded-error competition — the comparison column is telemetry only. egg admissible as authoring-time proposal engine in navigator role only (never verdict-bearing).

## 9. Open for Will

Option-A ruling (§4); kill-search timing (Claire-preliminary: execute during Stage 0, before campaign-brief freeze); registry home question (cross-ref registry brief §7.2); name covenant.
