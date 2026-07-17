# CAMPAIGN BRIEF — FLIP CARTOGRAPHY (double pendulum, exact discriminant/event varieties)

**Date:** 2026-07-02 · **Status:** FROZEN — grounded in-session S-2026-07-02 (Will: "Go"). Prereg immutable; amendments = new version. Was: DRAFT until grounding · **Substrate:** [CONTAINER] exact-ℚ throughout; byte-stable ×2 on every banked computation; dashboard patch after every banked result.

---

## CAMPAIGN GOAL
Stand up the first working organ of the sequential simulation engine: **discriminant cartography** — exact algebraic curves in initial-condition space that predict qualitative fate (flip / no-flip) of a genuinely chaotic mechanical system, derived from the composed DBP step correspondence, and validated against an adversarial float grid.

Secondary goal (forced by the vector seam): first construction pass at the **Seam Imprimitivity Theorem** machinery — elimination ideals replacing the single-variable resultant.

## TARGET CLAIM (scoped — the fence against overreach)
For the discrete double pendulum (frozen scheme, rational parameters), released from rest on the (θ₁,θ₂) torus:

> **C1.** The exact flip-event varieties T_k (grazing-inversion at step k) for k ≤ K_max are computable in ℚ[c₁,s₁,c₂,s₂]/(torus constraints), and their real loci coincide with the discrete integrator's own float flip-boundary at matched k (this is a consistency MUST — same object).
> **C2.** The energy no-flip gate is recovered exactly as a certified bound respected by all T_k (kill condition if violated).
> **C3.** The T_k ∪ discriminant strata refine/envelope the *continuous* (RK) early-flip boundary within a quantified (h,k)-band, by a frozen Hausdorff-type metric.

Explicitly NOT claimed: the full fractal boundary at long horizons. The claim covers the **earliest-flip tongues** (k ≤ K_max). K_max is itself a measured deliverable — the first exact reading of the scale wall.

## MATHEMATICAL OBJECTS
- **Step correspondence** F_h(x, y) = 0: implicit-midpoint variational (discrete Euler–Lagrange) integrator on the torus embedding x = (c₁,s₁,c₂,s₂,p₁,p₂), cᵢ²+sᵢ²=1, denominators cleared, ∈ ℚ[x,y,h]. Chosen self-adjoint **deliberately** (see P1).
- **k-step eliminant / ideal**: vector-seam glue, seam = full intermediate state; elimination ideal of intermediates. The seam-fiber block tower = the imprimitivity structure.
- **Flip-event variety T_k**: k-step ideal + inversion-grazing condition at step k (exact predicate frozen in Stage 0, DF-3 — the between-samples grazing subtlety is a named freeze item, not hand-waved).
- **Discriminant strata**: branch locus of the k-step correspondence over the release-from-rest torus.
- **Role-resolved degree spectrum**: per-variable degrees of the k-step eliminant (initial block vs terminal block vs seam) — the dynamical-degree instrument.

## PREREGISTERED PREDICTIONS (frozen before Stage A runs)
- **P1a (reversibility symmetry).** Self-adjoint scheme ⟹ F_h(x,y)=0 ⟺ F_{−h}(y,x)=0 ⟹ the k-step degree spectrum is symmetric under (initial↔terminal, h↦−h). The conservative pendulum is a keystone-type system: m_D = m_P.
- **P1b (arrow of time, the sharp one).** Adding Rayleigh damping (linear in p, stays polynomial) breaks self-adjointness ⟹ degree spectrum becomes asymmetric with **backward-inference degree > forward-production degree**. The recovery asymmetry reads as physics: dissipation = where the past gets expensive. Kill condition: asymmetry in the wrong direction refutes the framework's arrow story on real mechanics.
- **P2 (energy gate).** No real component of any T_k intrudes into the certified no-flip region (discrete shadow-energy bound; continuous gate 3cosθ₁+cosθ₂ ≥ 2-type curve recovered in the h→0 check — exact constant derived, not assumed, in Stage 0). Intrusion = formalization bug = halt and audit.
- **P3 (self-consistency MUST).** T_k real loci = the discrete integrator's own float flip set at step k, to grid resolution. Failure = harness bug, not physics.
- **P4 (the payoff claim).** Exact-curve vs RK-grid early-flip boundary: Hausdorff distance at matched k below (frozen) c·(grid pitch) + C·h² band. Metric and constants frozen at Stage C entry, before the overlay is computed.
- **P5 (bridge, exploratory — measure, don't kill).** log(per-step degree growth) vs float finite-time Lyapunov/entropy proxy on the same slice. Guarded: correspondence entropy bounds selected-branch entropy is [plausible/open]; this stage produces a measurement and a conjecture, not a verdict.

## TEST SURFACE
Equal masses/lengths, rational g and h (frozen Stage 0 after an h-scan); IC slice = release from rest, the (θ₁,θ₂) torus (the classic picture's slice); k = 1..K_max; contrast pair conservative vs damped; h-refinement at one 1-D slice for the O(h²) claim.

## STAGES & GATES
- **Stage 0 — Formalization freeze + tooling bake-off.** Derive F_h exactly; verify constraint propagation, symbolic h→0 consistency with the continuous EOM, self-adjointness identity, discrete-energy behavior; derive the exact energy gate; freeze DF-1 (parameters), DF-2 (scheme), DF-3 (flip predicate), DF-4 (metrics). Tooling: sympy vs python-flint vs apt Singular/Macaulay2 for elimination — pick by benchmark on the 2-step ideal. GATE: all consistency checks pass; degrees of F_h recorded.
- **Stage 0.5 — Instrument calibration on known ground.** Run the whole pipeline (glue, eliminant degrees, discriminant loci) on the **Hénon map**, where dynamical degree 2 and entropy log 2 are [known background]. Instruments must reproduce literature values exactly. GATE: calibration match.
- **Stage A — k=2,3 glue.** Elimination ideals, saturation against cleared denominators + constraint junk (named trap, see failure modes); degree spectrum; **test P1a**; discriminant strata on the rest-torus. GATE: P1a verdict + saturated, witness-pointed components only.
- **Stage B — T_k ladder, k ≤ K_max.** Push until the degree wall; record the wall exactly (which tool, what degree, what memory — the wall gets named, per house rules). **Test P2.** Stretch technique (not promised): doubling composition k+k→2k via structured resultants.
- **Stage C — Adversarial grids.** Two grids: discrete-truth (same scheme, float) and continuous RK (tight tolerance). **Test P3 (must), P4 (payoff).** Certified interval tracking on boundary-adjacent samples (real-sheet confusion guard).
- **Stage D — Instruments on the damped contrast.** **Test P1b.** Exploratory P5 measurement. Role-resolved degree table, conservative vs damped, banked to dashboard.

## EXPECTED FAILURE MODES (how this fools us)
1. **Spurious components** from denominator-clearing (mass-matrix degenerate locus) and torus complexification — every banked variety saturated + witness point per component, else not banked.
2. **Discretization ≠ physics** — two-grid design + h-refinement isolates it; claims are stated per-object (discrete vs continuous) never blurred.
3. **Grazing/between-samples flip definition** — DF-3 frozen before any boundary is computed; no post-hoc predicate tuning.
4. **Under-generation vs true wall** — a failed elimination is reported as "tool wall at (k, degrees, RAM)", never as "impossible".
5. **Narrative overfit** — P1a could fail from a non-self-adjoint scheme bug rather than framework failure; the self-adjointness identity is checked symbolically in Stage 0 precisely so P1 tests the framework, not the code.

## CERTIFICATION STRATEGY
Exact-ℚ algebra only in verdicts; floats confined to grids and continuation, always gated (assignment-bijective transport, motion-ratio, residual, closure) as in `mono_rederive.py`; byte-stable ×2 per banked run; scripts named per result; dashboard patch + present_files after every bank; **nothing canonical until Will signs off**.

## NOVELTY PAYOFF (with prior-art obligations)
- Exact finite-time flip-event varieties beyond the energy curve — [novelty candidate; OBLIGATION: prior-art sweep — Levien–Tan AJP 1993 lineage, "double pendulum flip fractal" literature, discrete-integrability/algebraic-entropy corpus (Bellon–Viallet, Dinh–Sibony) before any novelty claim].
- Vector-seam imprimitivity machinery — the theorem the whole engine needs, forced into existence on a real system.
- Role-resolved dynamical degrees + the conservative/damped asymmetry contrast — the arrow-of-time claim as a preregistered, falsifiable degree statement.
- Template: certified structural overlay on float simulation — the engine's first organ, reusable.

## STOP CONDITIONS & FALLBACK LADDER
Stage 0 consistency fails twice → halt, audit formalization. K_max < 3 on the pendulum → descend: (i) single pendulum full rotation (control with closed-form answer), (ii) Hénon/McMillan deep pass (calibration becomes destination), report the pendulum wall with its cause and the route through it (tool upgrade, structured elimination, or basis change). Budget: this brief expires for re-scoping after the earlier of Stage C completion or evidence the wall sits below k=3.

## OUTPUT LEDGER
`STAGE0_step_ideal.md` + `step_ideal.py`; degree tables (conservative + damped); `T_k` exact polynomial files + witness points; discriminant strata files; overlay plots (PNG) + both grid datasets; per-stage dashboard patches; this brief, frozen, with sign-off line.

## NEARBY BRANCHES — SEEN, NOT CHASED NOW
(a) Full monodromy/wreath ID of the vector-seam correspondence (Stage A will *see* the block tower; group ID is its own campaign). (b) Fluid triads / Lorenz-63 (next system after the template exists). (c) Cella-typed certified-numerics tier (bulk-scale integration comes after the exact core works once).

---
**SIGN-OFF (required before Stage 0 runs):** ______
