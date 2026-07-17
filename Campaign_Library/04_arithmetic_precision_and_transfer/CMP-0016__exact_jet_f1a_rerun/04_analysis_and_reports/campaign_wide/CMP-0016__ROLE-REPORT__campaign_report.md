# Exact Jet Primitive — Campaign Report

**Date:** 2026-06-10 · **Branch:** `campaign/exact-jet-primitive` (based on Quiet HEAD `24690f6`) · **Manifest:** v1 FROZEN, pin `0a80bc05…` · **Quiet fixture pin verified:** `9a1d7ec6…` · **Scoreboard rows:** A6 (primary), A4 (indirect)

Every number below is read from committed byte-stable records through committed code; measurement vs inference marked.

---

## 1. The composition law as built

`RESULT_TYPES_AMENDMENT_PROPOSAL.md`, approved by Will with four rulings (all applied pre-freeze): the **Membrane Rule** verbatim; **scale-free DIV_AMPLIFICATION** (measured output-vs-input lane binade growth — the original absolute-denominator draft was the HR130 E-rule failure pattern, named and replaced before freeze); `observable = selectable` with the **consumer obligation** (conditioning must be consulted before claim-grade use; observable ≠ endorsed); `pow` constant-exponent-only with the B4 route-fingerprint note; thresholds 26/40 (cancellation) and 60/150 (amplification) binades as **frozen calibration candidates**.

Three pre-execution corrections during test implementation, recorded in `ADDENDUM.md` before any campaign record existed:
- **A1** — division brought law-faithful (`a/b = a·recip(b)`, two accumulator-fed ops; the first build's direct quotient rule deviated from the frozen §2 — caught by the battery).
- **A2** — internal lane-sum cancellation screening: the battery exposed `q''(100)` carrying a 21-ulp Hessian error with a WELL_CONDITIONED self-report (~11 binades cancelling *inside* the mul Hessian sum) — unflagged-wrongness at micro scale, exactly what this engine exists to prevent. Lane sums inside mul/chain/recip are now screened, attributed per op. Strictly more detection (Axiom 3).
- **A3** — battery grading is condition-scaled ulp (8 ulp × 2^cancel + 1e-3 sanity ceiling): raw ulp is unsatisfiable where the route honestly self-reports cancellation (the deep F1a battery point loses ~28 binades in `1−2/r` by construction).

One membrane defect found by smoke and fixed pre-commit: `math.exp` raises `OverflowError` rather than returning inf — routed into the typed NONFINITE path (DP2).

## 2. Prediction verdicts (mechanical, `prediction_verdicts.json`, verbatim regardless of direction)

| prediction (frozen verbatim) | verdict | receipt |
|---|---|---|
| **P1** — jet-route I3 within 64 ulp-relative of I1 at every rung δ=10⁰…10⁻¹⁵ | **PASS** | max gap 15/64 ulp (k=6); every rung graded, per-rung rows in the verdicts file |
| **P2** — zero unflagged confidently-wrong; `fd_unresolved` must not fire; new floors route-appropriately flagged | **PASS** | zero wrong rungs at all; `fd_unresolved` extinct; conditioning channel carries the route's state |
| **P3** — conditioning channel responds measurably across the ladder | **PASS** | cancellation 2 → 51 binades, monotone; all three strata appear; stratification lands **exactly on the frozen prediction** (WELL→WARNING@k=8→ILL@k=12) — the threshold calibration candidates pass their declared test (Will's ruling 4: no retune was needed) |

## 3. The headline [measured]

**Depth parity restored.** The jet-route I3 reads F1a κ(δ) within tol at **all 16 rungs** (errors 4e-16…8e-15 vs the arbiter — riding the same noise floor as I1 and V3). HR130's last trustworthy rung for the FD route was k=3; it is now k=15, equal to I1 and I2. **The −12 decade deficit is 0.** The overlay figure (`resolution_vs_proximity_overlay.png`, generated from committed records only) shows the FD curve exploding through tol at k=4 while the exact-jet curve never leaves the noise floor.

[inference, high confidence] This confirms the campaign thesis: HR130's depth negative was the *extraction route* (the ε^(1/4) second-difference wall), not the substrate theory. The HR129 reconstruction consumes the same float64 operand as I1's closed form; with differencing noise removed, the two routes agree to ≤15 ulp everywhere.

[measured nuance worth keeping] At deep rungs the conditioning channel reports WARNING/ILL (the `1−2/r` operand genuinely loses 28–51 binades) while the κ *reading* stays perfect — because κ saturates at 4.0 and forgives operand error (dκ/dw → 0). The channel is honest about the **route**, conservative about the **quantity**. That gap (route-conditioning vs quantity-conditioning) is real, measured, and is the precise technical content behind the consumer obligation: observable ≠ endorsed, and conditioning ≠ wrongness — it is cancellation exposure.

## 4. Honest-failure section

- **RESOLVED (Will's Option-B ruling, 2026-06-10):** the lineage-gate conflict (eval-tier TypedResult with unregistered operation_id) is closed by the **explicit eval-tier operation registry** (`tests/_audit_helpers/eval_tier_operations.py`) — a ledger, not a bypass: every entry cites its authorizing campaign/brief (condition 2a), the companion gate bars eval-registered operations from the substrate manifest with promotion moving entries atomically into LAYER_MANIFEST and the trail preserved in `EVAL_TIER_PROMOTED` (condition 2b), and a third invariant forbids phantom entries (every active entry must be declared in evals source). The terminal-lineage gate accepts eval-tier-registered terminals pending promotion. The approved composition law is unchanged (ruling 4; options A and C declined). Full suite after resolution: **1115 passed, 1 skipped, exit 0.** During implementation a second collector-based gate surfaced (`test_task010c_lineage_terminates_in_primitive`) — same root cause, same registry resolution, recorded here rather than silently absorbed.
- Two further pre-execution corrections: the **first build violated its own frozen law twice** (division formulation A1; unscreened lane sums A2) — both caught by the battery before any record, which is the battery doing its job, but worth saying plainly. A4: the "hyperdual" token (OG class name) was caught by the campaign's own source-audit grep in the expression-path tag and renamed before finalization.
- The conditioning channel's WARNING/ILL at deep rungs would, under the Quiet P2 flag definition, mark perfectly-good readings as "flagged" — conservative in the safe direction, but a consumer using conditioning as a rejection gate would discard 8 good rungs. The route-vs-quantity gap (§3) is filed as the follow-up question (see gaps).
- The Quiet channel rule (`format_precision_pinned` from |w|<1e-4) still fires from k=4 — unchanged this campaign (HR130 gap, explicitly not retuned here).
- F1b/F2 were not re-run (the brief scoped F1a only); A4's "indirect" service is the route-noise removal for future blowup work, nothing measured here.

## 5. Gaps filed (none required new primitives; DP4 never triggered)

1. **Route-conditioning vs quantity-conditioning** [new; ACCEPTED AS FILED, Will 2026-06-10, with this note attached]: *resolution shape = claim-conditioning composed from operand damage × quantity sensitivity, where the jet's own gradient supplies the sensitivity factor. Future amendment; out of scope here.* (The jet's conditioning channel grades operand cancellation; a quantity insensitive to the cancelled operand — κ's saturation — reads perfectly under an ILL flag.)
2. **E-unsafe threshold recalibration** [carried from HR130, still open].
3. **Option-A re-open trigger** [recorded per ruling 2]: per-op typed scalars become worth building when a consumer demonstrates per-op granularity need — candidate: separator M2 per-route provenance (`CAMPAIGN_SEPARATING_ESTIMATOR_DRAFT.md`).

## 6b. The lineage-gate conflict — RESOLVED by Will's Option-B ruling (2026-06-10)

The collision (approved law §1 mandates a TypedResult boundary; the lineage gates mandate manifest registration for any TypedResult minted under `src/`; DP4 defers registration to promotion) was stopped for approval and resolved as **Option B — the explicit eval-tier operation registry** (`tests/_audit_helpers/eval_tier_operations.py`), under conditions 2a (per-entry authorizing citation; the registry is a ledger, not a bypass) and 2b (companion gate: eval-registered ops barred from the substrate manifest; promotion moves entries atomically, `EVAL_TIER_PROMOTED` preserves the trail). Option A was declined (Non-Goal violation: full typed-transcendental rework) and Option C declined (nominal gate evasion + post-hoc law amendment). The approved composition law is unchanged.

## 6. Merge-ordering implication (Will's ruling 5)

This branch is based on `campaign/shape-of-the-quiet` (`24690f6`), NOT main — the re-run gate needs the Quiet manifest + records, which main does not contain. **Merge order is therefore: quiet branch first (or together); this branch must never be merged to main without it.** The two campaigns' living-doc updates (HR130, HR131, ledger entries) remain uncommitted in the worktree for Will.

## 7. Acceptance criteria

1. Pre-reads ticked with citations — ✓ (committed in the brief).
2. Composition law recorded before implementation; tests enforce it — ✓ (proposal frozen + pinned before `exact_jet.py` existed; `test_jet_typed_composition.py` enforces the mapping case-by-case incl. threshold boundaries).
3. P1–P3 graded mechanically, verdicts verbatim — ✓ (§2; `prediction_verdicts.json`).
4. Five test files green; full suite exit 0; source audit clean — ✓ (31 jet tests green; full suite **1115 passed, 1 skipped, exit 0** after the Option-B eval-tier registry landed; source audit clean, zero V3/OG imports or vocabulary post-A4).
5. F1a re-run byte-stable — ✓ (re-execution diff identical, records + verdicts).
6. HR131 draft + A6 row draft for Will — ✓ (`HISTORICAL_RECORD.md` appended, uncommitted; `A6_ROW_DRAFT.md` in this folder).

## 8. Plain-language answer

*Did removing the FD route restore depth parity while keeping honesty?* **Yes — both, completely, on this fixture.** The typed probe now reads the Schwarzschild deep approach to the edge of float64 representability, exactly as deep as the naive float and the V3 oracle, while remaining the only instrument that reports its own state per operation: every rung carries its cancellation count, its amplification record, and its conditioning stratum, and the stratification landed precisely where the frozen thresholds predicted. The Quiet campaign proved the probe could not be confidently wrong; this campaign proves that honesty was never the price of depth — the FD differencing was.

## 9. Reproduction

```bash
PYTHONPATH=src python -m pytest tests/test_jet_*.py tests/test_quiet_rerun_gate.py
PYTHONPATH=src python -m lloyd_v4.evals.exact_jet_f1a_rerun       # refuses on either pin break
PYTHONPATH=src python -m lloyd_v4.evals.exact_jet_overlay_figure
```
