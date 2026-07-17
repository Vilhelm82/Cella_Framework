# KB.1 FIRED — audit record (Stage B, rung k=1)
**Date:** 2026-07-02 · **Substrate:** [BOX run-1 battery] + [CONTAINER audit] · **Status:** stage HALTED per prereg; routed to Will. Prediction PB.1 preserved verbatim; nothing softened.

## What fired
Battery run-1 (`stageB_gens.py`, sha `a671eb4442b1e620`, log `stage_B/run1_k1.log` on box): 68 real
witnesses scanned on the inv-branch eliminant, 20 energy-gate violations (2c1+c2 > 1). KB.1 = HALT.

## Audit findings (two distinct defects)
**D1 — harness bug (mine): saturation skipped.** The battery's corner gate stripped only (1+x^2)
factors; the frozen honest-T_k definition requires saturation by cleared denominators / lc artifacts.
CERTIFIED: the mult-4 line factor is exactly `x2`, and `x2 | lc_2(E_2 in t1)` — a resultant
leading-coefficient artifact, textbook brief failure-mode #1. Fix: proper saturation in the harness.
No prereg change needed; the frozen text already required this.

**D2 — formalization gap (what KB.1 actually caught): the frozen T_k is ANY-BRANCH; the energy
gate binds only the principal branch.** The step correspondence is a 32-branch implicit object.
Real non-principal branches exist and teleport: at witness (x2=1, x1 = root of the deg-(14,24)
honest factor), the certified-real fiber jumps circle-1 by 101.9 deg and takes bob 2 from
c2 = 0 (sideways) to c2 = -1 (inverted) in ONE h=1/40 step [diagnostic float, gated, match 1.2e-15].
No energy argument constrains such branches — the gate derivation assumes the physically-continued
sheet. Therefore PB.1, as frozen over the any-branch object, is REFUTED-BY-DERIVATION (second
prereg observable this campaign to die by the campaign's own structure; recorded loudly, P1b pattern).

## The structural reading
The algebra computes the FULL correspondence; the physics rides one sheet. The flip fractal is a
principal-sheet object; the any-branch variety is strictly larger and energy-unbounded. This split
is itself an instrument (ghost-sheet census), not merely a nuisance.

## Proposed amendment — PREREG v2 (requires Will's gate; v1 stays frozen as the record)
- **DF-7 (branch discipline):** principal branch := the solution branch that is the h->0
  continuation of the identity, certified per point by interval Newton from the explicit predictor
  (Stage-0 gated-continuation pattern). Physical T_k := honest T_k points whose certified chain is
  principal at every step.
- **PB.1':** energy gate restated over principal-sheet Physical T_k (same exact test, same KB.1).
- **PB.5 (new, measure-don't-kill):** ghost-sheet census — count/location of real non-principal
  components of T_k per rung.
- PB.2, PB.3, PB.4, pins, primes: unchanged.

## State
Run-2 (byte-stability) not yet run — deferred until harness fix + v2 gate. Box DC link went down
mid-audit; run-1 log to be committed from the box when the link returns.
