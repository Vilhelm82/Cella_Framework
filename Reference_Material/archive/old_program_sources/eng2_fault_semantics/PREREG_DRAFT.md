# FLAGSHIP STAGE B (SUCCESSION) — PREREG **DRAFT** (S-2026-07-05b)
**Status: DRAFT — awaiting Will's freeze GO. No battery code exists; nothing
runs until this file is frozen with pins (covenant #2).**

**Naming note (no silent rewrite):** brief §6 "Stage B" = CL-F3 fiber
completeness — that stage is RE-QUEUED, not skipped. This stage carries the
desk's "Flagship Stage B (CL-F5 + CL-ENG2 — the succession theorems)" (v4.5
carry line; defaults accepted by Will S-2026-07-05). Content = brief Stage-C
bridge claim pulled forward + the engine's fault-semantics theorem.
"Succession" = succession of the OG ratio law into invariant language.

## Objects & definition freezes
- **DF-B0 (imported, frozen):** isotypic frame DF-S2 (projectors from
  rep_utils, gated); pair module; m2_X(ν) = ‖π_X ν‖², X ∈ {triv,std,shape}.
- **DF-B1 (candidate fork, PRE-DECLARED — the battery selects, we do not):**
  general-n coupling edge vector ν ∈ pair module, ν_ij = W(i,j)·H_ij with
  weight W from EXACTLY this candidate list, no additions post-freeze:
  - **W-prod:** W(i,j) = ∏_{k∉{i,j}} g_k  (opposite-vertex product; verbatim
    n=3 specialization g_k·H_ij)
  - **W-sum:** W(i,j) = Σ_{k∉{i,j}} g_k  (also specializes to g_k·H_ij at n=3)
  Selection criterion (frozen): candidate for which the coupling block of
  the bordered-determinant partition is an exact S_n-invariant quadratic
  form in ν at the pinned fixtures. Both pass ⟹ both recorded, fork routed
  to Will. Both fail ⟹ K-B1.
- **DF-B2:** coupling channel κ_c^(n) = the pure-coupling block of the
  three-channel K_G determinant partition (Three_Channel_KG_Strong_Spec,
  codim-1 border — INSIDE its certified scope fence); Δ_c^(n) = −κ_c·|g|^4
  normalization as in Transport_Law §5.
- **OG clause (embedded verbatim, grader must string-match):** "κ_c / K_G is
  invariant under uniform gradient scaling. Coupling faults change the
  ratio; self-faults preserve it." (OG_lloyd_decomposition.md §10.2.)

## Predictions (to freeze; graded mechanically)
| id | statement | class | prediction |
|---|---|---|---|
| PB.0 | pipeline reproduces I.3a verbatim at n=3 (Δ_c = 2·m2_std − m2_triv; eig {+2,−1}; keystone Δ_c=4 at ν=(0,0,2); I.4 anchor gate) AND witness_battery reproduces sha 39bed555 | sanity | MUST HOLD (else pipeline defect, no verdicts — K-SP1 analog) |
| PB.1 | for ≥1 pre-declared weight candidate, Δ_c^(n) is an exact S_n-invariant quadratic in ν decomposing as c_triv·m2_triv + c_std·m2_std + c_shape·m2_shape, g-rational, exact-ℚ, at pinned n=4 AND n=5 fixtures | discriminating | HOLDS for W-prod — moderate confidence; W-sum lower; both-fail = K-B1 |
| PB.2 | coefficient triple (c_triv, c_std, c_shape)(n) fits ONE closed form rational in n across n=3,4,5 and RETRODICTS n=6 (n=3 must give (−1,2,0), shape absent) | discriminating | HOLDS — the bridge is a projector identity underneath (Schur route); FAIL = CL-F5 PARTIAL, coefficients stand as certified numbers |
| PB.3 | fault semantics (CL-ENG2): sub-predecl B.3 frozen AFTER PB.1/PB.2 grade, BEFORE any B.3 battery — will stake: self-fault families (diagonal-H perturbations) act with δν = 0 hence preserve Δ_c exactly; coupling-fault families move the pre-declared moment ratio; exact-ℚ certificates n=3,4,5 + symbolic theorem | staged | staged freeze (A1/A2 addendum pattern); no prediction staked here beyond the staging itself |

## Kill conditions (armed at freeze)
- **K-B1:** both weight candidates fail PB.1 ⟹ bridge-as-stated DEAD; HALT
  stage, route to Will (no third candidate invented post-freeze).
- **K-B2:** PB.2 fails ⟹ CL-F5 → PARTIAL (certified numeric coefficients,
  no closed form); not a halt.
- **K-B3:** PB.3 certificate fails at any pinned fixture ⟹ HALT, route to
  Will; CL-ENG2 never softened to "approximately preserves".
- Envelope: 1200 s / 8192 MB per battery (WALL_VERDICT margins); exceed =
  datum.

## Grading, pins, deliverables (owed at freeze, before battery code)
Fixtures: keystone (I.4 anchor) + pinned rational fixtures n=4,5,6 (distinct
-entry g, generic H; + single-edge fixtures for the §7 lemma check), fixed
and sha-pinned at freeze. Content pins (Rule 1.9): this file, battery,
rep_utils, fixture file — all sha256 in freeze_pins. Clause embedding (Rule
1.8): GRADER_CLAUSES dict string-compared at runtime, incl. the OG clause
verbatim. Byte-stable ×2; suite exit 0; role=probe + ledger; substrate
[BOX]/[CONTAINER] tagged. Status moves: PB.1+PB.2 PASS ⟹ CL-F5 →
STRUCTURAL (symbolic derivation then owed for PROVEN); B.3 PASS ⟹ CL-ENG2
→ per its sub-predecl. Deliverables: stage_B_succession/{PREREG.md frozen,
freeze_pins.sha256, battery, records ×2, STAGE_B_REPORT.md}; ledger + carry
deltas PROPOSED. Nothing canonical without Will's sign-off.

DRAFT — author Claude-session S-2026-07-05b; freezes on Will's GO only.
