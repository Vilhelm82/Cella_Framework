# P-F3 HUNT ADDENDUM v2 — msolve ENGINE (route b)
**Status: FROZEN at commit, pre-runner (no v2 runner code exists at freeze time). Date 2026-07-03.**
**Authority:** Will verbatim: "yes go (b) then from that result decide (a)" — S-2026-07-03. The v1 hunt grades as frozen (INCONCLUSIVE_BUDGET, pending container primary ×2; box preview sha 268f6fe00d77f51a). This addendum is a NEW frozen protocol for the same mathematical hunt; route (a) — positive-dimensional slicing — is explicitly DEFERRED pending this outcome, per the ruling.

## 1. Systems (unchanged)
The identical eight v1 slice systems: SLATES as pinned in the v1 battery; tie polynomials rebuilt per run by the validated K=6, D=15 evaluation–interpolation with fresh-point self-check (v1 machinery, imported). Fixture (g, H) = the witness fixture, unchanged. Nothing mathematical moves; only the elimination engine does.

## 2. Engine
msolve 0.10.0 (F4 Gröbner + rational univariate representation), jll prebuilt binary, **box primary substrate** (container is occupied as v1's primary and lacks the engine; running there would contend with v1's time-based abort stages — recorded as the substrate rationale). Binary sha256[:16] = `2caed4b3596acb38`; invocation `msolve -P 2 -f <slice>.ms -o <out>`, per-slice cap 600 s enforced by subprocess timeout.

## 3. Soundness of emptiness (the new verdict class)
RUR property [PROVEN, standard]: the separating element is a ℚ-linear form in the variables, so every rational point of the 0-dimensional variety maps to a rational root of the eliminating polynomial w(t), and every rational root of w maps back to a rational point via the parametrization. Hence: **w has no nonzero rational roots ⟹ the slice has no nonzero ℚ-points** — decidable exactly (rational root theorem). Parse-independence: coordinate extraction errors cannot create false witnesses (every candidate passes the unchanged exact certification) and cannot create false emptiness (emptiness reads w alone).

## 4. Frozen clauses (verbatim; runner embeds exactly, refuses on drift)
HB.1: the eight v1 slice systems are rebuilt by the pinned K=6, D=15 interpolation with fresh-point self-check and handed to msolve with integer-cleared coefficients, unchanged.
HB.2: a WITNESS_FOUND is banked only after the unchanged exact certification: all three m2 ties, Ehat ties for r=1..4, O2 != O1, at pairwise-distinct g.
HB.3: an EMPTY_CERTIFIED verdict requires msolve completion with an eliminating polynomial whose nonzero rational roots are exhaustively excluded by exact rational root finding.
HB.4: per-slice cap 600 seconds; caps, timings, and raw solver output live outside the hashed blob; the blob carries only the canonical rational-point sets and verdicts, and is byte-stable across two independent runs.
HB.5: outcome routing — any WITNESS_FOUND routes to Will same breath; eight EMPTY_CERTIFIED verdicts constitute the route-(a) decision evidence and route as such; SOLVER_INCOMPLETE and error data are banked verbatim.

## 5. Kill conditions
K-HB1 (halt): blob sha mismatch across the two runs. K-HB2 (halt): interpolation self-check failure. K-HB3 (halt): gate refusal (clause drift / pin mismatch). Caps and emptiness are outcomes, never kills.

## 6. depends_on (sha256[:16] at freeze)
| artifact | pin |
|---|---|
| FLAGSHIP_STAGE_A_PREREG.md (v1 authority) | d5e69a10fee4897d |
| flagship_stageA_battery.py (imported machinery) | 81bc3de5e0a9937b |
| msolve binary (box) | 2caed4b3596acb38 |
| campaigns/the_engine/stage_A/engine_harness.py | 7f0e5e7e4f4d54a6 |
| evals/dbp_involution/rep_utils.py | 0d838e5fd430461b |

frozen: true · version: 2 (hunt only) · referee: mechanical (exact certification; rational-root exclusion; blob equality) · author: Claude-container · activation authority: Will, S-2026-07-03 (verbatim above)
