# STAGE B PREREG — the T_k ladder (flip_cartography)
**Status: FROZEN — grounding gate cleared S-2026-07-02 (Will: "Go", following the four-sentence statement in-session). Immutable; amendments = new version.**
**Date:** 2026-07-02 · **Substrate:** [CONTAINER]+[BOX], exact-ℚ / GF(p) verdict paths only · **Depends on:** BRIEF_v1 (FROZEN, sha `b57e1e2bb32eb509`), DF-1 (h=1/40, m=ℓ=1, g=10), DF-2 (scheme), DF-3 (flip predicate), corner-gate mechanism (MECH_ideal_locus.md, sha `6514d0d2b5d0d68e`), P1a theorem (STAGEA_glue.md, sha `094de38228cbff67`).

## Object definitions (frozen)
```
Rest slice:   p1(0) = p2(0) = 0,  (c1,s1,c2,s2) in T^2  (phi_1 = phi_2 = 0)
Chain ideal:  I_k = < step generators for steps 1..k , phi constraints at every level >
Raw T_k:      J_k = I_k + < s2(k) >, restricted to the rest slice,
              eliminated down to the initial torus variables (c1,s1,c2,s2)
Honest T_k:   the eliminant of J_k after (i) saturation by cleared denominators,
              (ii) removal of isotropic-corner ghost factors (t^2+1 class, per the
              proven corner mechanism), (iii) squarefree part.
Physical T_k: real locus of honest T_k intersected with the semialgebraic side
              condition c2(k) < 0 (DF-3 branch selection), certified per component
              by a rational witness point or isolating interval.
```

## Route (declared, not itself a prediction)
Ladder k = 1, 2, 3, ... by the modular spectrum engine (multi-prime GF(p) elimination
+ exact-degree interpolation + holdout gates, the Stage-A k=2 pattern), corner gate
applied at every rung, flint Z-GB as cross-check where feasible. Push until the wall.
Stretch (not promised): doubling composition k+k -> 2k via structured resultants.

## Content pins
- Primes (all verified prime, < 2^30, int64-safe): p1 = 1073741789, p2 = 1073741783, p3 = 1073741741.
  Every GF(p) certification runs at >= 2 of these; any cross-prime disagreement = HALT.
- Step-generator source: single script `stageB_gens.py`, sha recorded in RUN_LOG at first
  freeze-verify, byte-identical across all runs of the stage.
- Corner-gate implementation: ported verbatim from the MECH report's identity; the gate
  self-tests on the k=1 eliminant (must strip exactly the proven (t^2+1) factor) before
  any k >= 2 use.

## Predictions (verbatim, falsifiable)
- **PB.1 — Energy gate (the brief's P2, armed).** Every real point of every computed
  Physical T_k satisfies `2*c1 + c2 <= 1` (point-bob no-flip gate, PROVEN Stage 0).
  Exact-Q test on every certified witness + interval exclusion on every real component.
- **PB.2 — Reversal identity (harness MUST).** R fixes the rest slice pointwise and
  R.Phi.R = Phi^-1 [P1a, PROVEN] => the backward-k flip eliminant equals the forward-k
  flip eliminant on the rest slice, exactly, after normalization, at every computed k.
- **PB.3 — Corner persistence.** The raw k-step flip eliminant contains the isotropic-corner
  ghost factor at every computed k, and the corner gate strips it leaving a basepoint-free
  honest eliminant (generic-clause check per MECH report at every rung).
- **PB.4 — Real thinning on the ladder (EXPLORATORY — measure, don't kill).** The number of
  real components of Physical T_k grows sub-multiplicatively in k (echo of the 224 < 256
  Stage-A reading). Produces a measurement and, at best, a conjecture.

## Expectations (graded against, units declared)
- deg(honest T_1) on the torus: a finite integer, recorded exactly (no frozen value —
  first reading of the instrument at this slice).
- Ladder deliverable: table (k, raw degree, honest degree, # complex components,
  # real components, # physical components, P2 margin min over witnesses).
- **K_wall deliverable:** the exact rung where every route fails, recorded as
  (k, tool, degree at failure, RAM, wall-clock). A tool wall is NOT a kill — it is
  the campaign's promised "first exact reading of the scale wall" (K_max).

## Kill conditions (typed, armed)
- **KB.1 (fires on PB.1 failure):** any real physical T_k point with 2*c1 + c2 > 1
  => HALT stage, route to Will, audit formalization (brief: "intrusion = formalization
  bug"). Never soften.
- **KB.2 (fires on PB.2 failure):** forward/backward eliminant mismatch at any k => HALT,
  harness bug hunt before any further rung (the P1b control discipline).
- **KB.3 (fires on PB.3 failure):** corner factor absent or gate leaves basepoints => HALT,
  mechanism audit (would contradict a PROVEN identity — most likely a porting bug, but
  the chain is preserved verbatim either way).
- Cross-prime disagreement or byte-instability across the x2 rerun => HALT (covenant).

## Carried-in items (bookkeeping, no brief amendment)
- Stage-A leftover "discriminant strata on the rest slice" rides this stage as **B4**:
  real-discriminant locus of the 1-step correspondence over the rest torus (where the
  16-real-branch count drops), branch 12 (the 2/30 real-multiplicity outlier) as the
  named witness target. Same machinery, same pins, same kill discipline. Deliverable:
  strata equations + witness points; feeds the real-growth story (PB.4).

## Out of scope (fence)
- Float-grid overlays, Hausdorff metrics, RK comparison — Stage C (DF-4 still deferred
  by design).
- Any claim about the fractal boundary at long horizon, per the brief's fence.

## Discipline line
Prereg frozen before any battery code exists. Byte-stable x2 per banked run. Exact-Q/GF(p)
verdicts only; floats confined to continuation and always gated. Nothing canonical until
Will signs off. FAIL halts and routes to Will.
