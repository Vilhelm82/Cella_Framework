# substrate-invariant-search — Successor Authority (R1)

**Status:** ACTIVE authority for the `substrate-invariant-search` campaign. Fulfils the long-pending
successor designated `substrate_invariant_search_2026_05_26.md` (TASKS_TO_REVISIT **R1**), written
2026-06-07. Supersedes the retired `Build_Docs/Agent_tasks/substrate_invariant_search_2026_05_23.md`.

**This is NOT a new campaign.** It is the canonical `substrate-invariant-search` (LIVE_CAMPAIGNS_LEDGER).
Do not mint "substrate observable catalogue", "geometry-first", "K_G primitive search", or any restart
name — those are this campaign (ledger Aliases / known restart traps).

---

## 0. Mandatory pre-reads & closed-results check (anti-re-derivation gate)

Consulted before authoring (cite rows; per TASK_TEMPLATE R0):
- `LIVE_CAMPAIGNS_LEDGER.md` — `substrate-invariant-search` Active entry; Q1 status; Aliases table.
- `HISTORICAL_RECORD.md` — rows 170/183 (Phases A–I superseded; Q1 open), 132 (b_k = ULP floor coeff).
- `TASKS_TO_REVISIT.md` — **R1** (this successor), **R9** (G null closed; geometric-primitive core OPEN),
  R2 (carry surviving findings forward), R3 (curvature pivot dangling).
- `CAMPAIGN_DISCIPLINE.md` — 7 cross-cutting rules + phase template (Phase 0 + 5 mandatory).
- `V4_GLOSSARY.md` §"Things commonly confused" — `b_k` (noise floor vs conditioning), G-as-remainder.

**Closed-results verdict:** continuation-of-campaign `substrate-invariant-search`. The residual-term
G question is CLOSED (R9 — do not re-run additive-remainder G decompositions). The OPEN object is the
geometric-primitive core (Gate-2), reframed below.

---

## 1. North star (Q1) and the Gate-2 object

Q1 (`where_i_got_stuck.md`): *what is casting the substrate's residual fingerprints?* The forward
frontier (LIVE_CAMPAIGNS_LEDGER Q1 row, "Gate-2") is precise:

> **Is there a deterministic substrate observable that is a geometric invariant ACROSS fixtures?**

Fixtures: `sr_four_form`, `schwarzschild_four_form`, `pure_algebraic_four_form` (primary);
`geometry_anchor` rows excluded from headlines.

---

## 2. The corrected diagnosis — jet-order mismatch (verified against code 2026-06-07)

The campaign has been testing **0-jet** substrate observables against a **2-jet** geometric target.
Verified in source this session:

- The natural function is `y = sqrt(radicand)` — a 1D graph (`mcg_geometry_first_geometry.py:26-28,
  170-178`). **A plane curve has no intrinsic curvature**; the campaign's "K_G" is
  `principal_curvature = |y''| / (1+y'²)^{3/2}` (`mcg_geometry_first_geometry.py:446-448`) — the
  *extrinsic* plane-curve κ, a **2-jet** quantity. (The earlier intrinsic-vs-extrinsic framing was a
  category error — there was no intrinsic option.)
- `base_operand = 1 − x_term = y²` in all three fixtures (`v3_bridge.py:19-21,89`). So the headline
  observable `E = log₂|base_operand| = 2·log₂ y` is a **pure function of operand magnitude `y`** — the
  **0-jet**. Every Phase-A–I candidate (`phase_i.py:53-54`) is `ulp()`/`log2()` of single-coordinate
  operands — all 0-jet (they see *where* operands sit, never *how they move*).

**Consequences (both forced, neither informative about geometry):**
- Within-fixture `ρ(E, κ) = −1.0000` (Phase H) is the **coordinate tautology** — `E` and `κ` are both
  monotone in the 1D coordinate `t`, so their rank correlation is ±1 by construction.
- Cross-fixture `0/5` at matched κ (Phase H) is a **jet-order mismatch** — matching one 2-jet scalar does
  not match the 0-jet magnitude `y` (two curves of equal curvature sit at different heights). It is
  **not** evidence the substrate lacks geometry.

**Reframe:** eight phases of negatives mean *we never sampled the derivative*, not *the substrate is
empty*. The fix is to sample the missing jet orders by differentiating the fingerprint along the
coordinate (`S2 = d²/dt² log₂|base_operand| = (2/ln2)(y''/y − (y'/y)²)` — the operand log-acceleration,
substrate-native by construction). See Phase A spec.

---

## 3. Surviving findings — carried forward as citations (do NOT re-derive)

| Finding | Status | Source |
|---|---|---|
| `E := log₂|base_operand|` is K_G's **within-fixture rank** cousin (ρ=−1.0000, Schw + pure_alg); fixture-bound (0/5 cross-fixture) | established, **reinterpreted as 0-jet** (§2) | `Reports/substrate_invariant_search/phase_h_substrate_semantic_characterization.md` |
| Two-tier substrate encoding: Tier-1 K_G-rank (via E) + Tier-2 coordinate-position; both fixture-bound | established | Phase H §7 |
| `log2_x_term_ulp` matches cross-fixture at matched κ (5/5) but is coarse / not K_G-monotone | established | Phase H §4 |
| G-as-remainder = **proven floorless null** (1D + lifted + bilinear multi-D coupling rounds away) | **CLOSED — residual-term G** | R9; `scratch/g_forward_decomposition_exp1/2_CLOSEOUT.md`; `Reports/g_multid_coupling/closeout.md` |
| Geometric-primitive core (cross-fixture invariant) | **OPEN — the Gate-2 object** | R9 net status |
| α as per-probe local observable; log-log slope at branch; BACL as prediction engine | toolkit (now substrate: typed_finite_difference, typed_log_log_slope) | LIVE_CAMPAIGNS_LEDGER |

The 2026-05-23 Phases A–I are "not citable as substrate-physics findings" (HR row 170) **except** the
specific surviving results above (R2). Cite those; do not re-discover them.

---

## 4. Methodology (binding)

Per `CAMPAIGN_DISCIPLINE.md`, with two campaign-specific sharpenings forced by §2:

1. **Pre-registration is binding** (rule 1.1). Every phase registers predictions, the null, verdict
   thresholds, and the noise-floor formula in `Build_Docs/Agent_tasks/` BEFORE running. Frozen artifact.
2. **No substrate promotion within the campaign** (rule 1.2). All results are eval-layer
   (`src/lloyd_v4/evals/`). A V4-native curvature observable, if found, is promoted only post-closeout
   under the substrate-derivation gate.
3. **Rank correlation is RETIRED for this campaign.** It is tautology-poisoned (§2): two monotone
   functions of `t` always rank-correlate ±1. The headline test is **leave-one-fixture-out functional
   universality** — fit `C = f(T)` on two fixtures, predict the third; only a fixture-agnostic *law*
   survives. The law is the content.
4. **Shuffle-null is a Phase-0 gate** (the `wrong_clean_emit` guard, rule 1.3). The universality test
   MUST FAIL on coordinate-permuted data before any hypothesis run. A fit that confirms a permuted null
   is over-flexible (matched filter ringing on a prior — rule 1.7 / §7-discipline failure mode); reduce
   degrees of freedom until the shuffle fails. No exceptions.
5. **Phase 0 (instrument gates) and Phase 5 (closeout) are mandatory.** Phase 0 is direction-agnostic:
   it earns a trustworthy cross-fixture instrument + a defined noise floor before any hypothesis.
6. **Surprise ledger + scoped verdicts** (rules 1.4 / §3). Closeout verdict is scoped to the tested
   space; "X is true" is forbidden, "X is true within the tested space" is required.

**Blocker carried forward:** Task 1 (audit-framework extension to transfer observables,
`Docs/session_handoff_2026_05_25_audit_framework_priority.md`) blocks *audit-stamped* results; phases
run **research-grade** pending its closure.

---

## 5. Phase plan

- **Phase 0 — Instrument capability gates (MANDATORY, next).** Validate the cross-fixture
  substrate-jet instrument: route-identity control (the four algebraic forms agree per coordinate),
  the SR constant-κ slice residual, the **pure-noise shuffle null (must fail the universality test)**,
  and the declared noise floor = `max(SR-slice residual, shuffle 95th-pct error)`. Signed artifact
  before Phase A. (Phase A spec §6.)
- **Phase A — Substrate-jet curvature test.** Per
  `Build_Docs/Agent_tasks/substrate_invariant_search_phase_a_jet_order_spec.md` (the uploaded spec, to be
  committed alongside this authority): build the jet ladder (`S0/S1/S2`, arc-length `S1_s/S2_s`, lattice
  `Δ²B`) on `phase_1_geometry_table.json`; run leave-one-fixture-out universality for
  `C ∈ {S2, S2_s}` against `T ∈ {κ, y''}`; report the native combination (§4.3) and the binade
  resolution seam (§5).
  - **H_jet_geometry:** a substrate jet is a universal function of a geometric jet cross-fixture ⟹ the
    substrate carries a differential-geometric invariant.
  - **H_zero_jet_only (NULL, pre-registered as expected):** only `S0` (magnitude) is shared; `S2_s` is
    fixture-bound/noise ⟹ substrate carries magnitude, not curvature → write the clean negative, pivot
    to the seam.
- **Phase B+ —** selected by Phase A's verdict (native-invariant boundary mapping, or seam
  characterization, or — if H_zero_jet_only — formal negative + curvature-pivot retirement, closing R3).
- **Phase 5 — Closeout synthesis** (mandatory; master palette + surprise ledger + wrong_clean_emit
  summary + scoped verdict).

---

## 6. Mission tie-in

End goal: rebuild V3's curvature/conditioning diagnostics on V4 substrate (Axiom 11/12 — recover from
substrate behaviour, do not import). Phase A delivers a validated map **(substrate jet) → (geometric
quantity)** cross-fixture. Either outcome serves the rebuild: `S2_s`↔κ universal ⟹ V3's curvature
extractor rebuilds as "second arc-length derivative of operand log-magnitude"; `S2_s`↔`y''`/`G2`
universal instead ⟹ the substrate's *own* invariant is operand log-acceleration and continuum κ is its
shadow — the more V4-native rebuild. The binade resolution floor is the curvature observable's honest
typed-refusal boundary (same spirit as the P2 budget seam).

---

## 7. Anti-restart note (frozen)

This authority continues `substrate-invariant-search`. The retired 2026-05-23 authority and its Phases
A–I are superseded except the §3 surviving findings. **Do not** re-run additive-remainder G
decompositions (R9 closed). **Do not** use within-fixture rank correlation as a headline test (§2
tautology). **Do not** start a parallel curvature/observable-catalogue campaign. CORE-MATH / V3 / lv3
remain oracle-only, never design sources.
