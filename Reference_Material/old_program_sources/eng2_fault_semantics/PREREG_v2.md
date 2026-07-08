# FLAGSHIP STAGE B (SUCCESSION) — PREREG v2 (FROZEN, S-2026-07-05b, pre-battery)
**Supersedes PREREG_DRAFT.md (v1, retained in repo).** v1→v2 delta, in ink:
v1's PB.1 staked "Δ_c^(n) exact quadratic in ν" while DF-B2 cited the
Strong_Spec partition, whose general-n coupling channel κ_c = det(Ŝ_c) has
DEGREE n−1 in coupling entries (Spec §12) — the v1 prediction was
definitionally impossible at n≥4; the n=3 quadratic was the accident
n−1=2. Collision caught PRE-freeze, pre-battery, during referee
implementation. v2 re-aims at the object that IS the n=3 form at all n.
Authorized under Will's Stage-B GO + PA-5 (arithmetic-forced repair,
certified calibration below); Will's veto stands at stage acceptance.

## DF-B2 (v2, frozen): the succession object
```
q = g·g ,  P = I − g gᵀ/q ,  H_c = off-diagonal part of H
Δ_c^(n) := −q · e_2(P H_c P) ,   e_2(M) = (tr(M)² − tr(M²))/2
```
e_2 = second elementary symmetric function of the coupling shape operator
(E_r tower language, Extension §1). **CERTIFIED (container, S-2026-07-05b,
symbolic, all g and all H_c):** at n=3, −q·e_2(P H_c P) ≡ Δ_c of Strong_Spec
§4 identically — det = e_2 for 2×2 ⟹ the succession is verbatim, and
Δ_c^(n) is exactly quadratic in H_c entries at every n (e_2 is degree-2 in
matrix entries; P H_c P linear in H_c). Keystone anchor: Δ_c=4, κ_c=−1/49.

## DF-B1 (carried from v1 unchanged): weight fork, pre-declared
ν_ij = W(i,j)·H_ij; candidates EXACTLY: **W-prod** = ∏_{k∉{i,j}} g_k,
**W-sum** = Σ_{k∉{i,j}} g_k (both = g_k·H_ij at n=3). No post-freeze
candidates. Q_ν = D_W⁻¹ Q_raw D_W⁻¹ where Δ_c^(n) = hᵀQ_raw h, h = H_c
offdiag vector, pair order per fixtures file.

## DF-B0 (imported): isotypic frame
Projectors P_triv (λ=(n)), P_std (λ=(n−1,1)), P_shape (λ=(n−2,2)) built by
character averaging (rep_utils) on the pair module; runtime gates: ranks
(1, n−1, n(n−3)/2), idempotency, pairwise orthogonality, partition of
identity (pair module = triv⊕std⊕shape EXACTLY for all n≥4, Young's rule /
CL-F1 mechanism; dims 1 + (n−1) + n(n−3)/2 = n(n−1)/2; the sum-to-identity
gate is therefore enforced, not optional). m2_X(ν) = νᵀP_Xν.

## OG clause (embedded verbatim; grader string-matches)
"κ_c / K_G is invariant under uniform gradient scaling. Coupling faults
change the ratio; self-faults preserve it." (OG_lloyd_decomposition.md §10.2)

## Predictions (FROZEN; graded mechanically; clauses embedded in battery)
| id | statement | class | prediction |
|---|---|---|---|
| PB.0 | (i) in-battery symbolic gate: −q·e_2(PH_cP) ≡ Spec-§4 Δ_c at n=3, all g, all H_c; (ii) keystone: Δ_c^(3)=4, Q_ν = 2I−J exactly in ν-coords (both weights), (c_triv,c_std)=(−1,2); (iii) projector gates at n=4,5,6: ranks (1,n−1,n(n−3)/2), idempotent, orthogonal, sum = I on pair module | sanity | MUST HOLD (else K-B0 pipeline defect, no verdicts) |
| PB.1 | for ≥1 weight cell: Q_ν(g) ∈ span_Q{P_triv,P_std,P_shape} EXACTLY (zero residual, exact ℚ) at ALL FOUR fixtures n4a,n4b,n5a,n5b ⟹ Δ_c^(n) = c_triv·m2_triv + c_std·m2_std + c_shape·m2_shape | discriminating | LOW-to-moderate: HOLDS for ≥1 cell; the n=3 miracle may be n=3-only — a clean both-cells-FAIL is equally structural (K-B1 routes it) |
| PB.2 | on surviving cell(s): coefficients g-INDEPENDENT (equal across the two g-fixtures at each n) AND the unique deg-≤2 polynomial in n through n=3,4,5 values RETRODICTS n=6 exactly (c_shape: linear through n=4,5, retrodicts n=6; n=3 unconstrained, shape dim 0). Ansatz ladder FROZEN: deg-≤2 polynomial only; no post-hoc function families | discriminating | open prior — g-independence is the sharper half; FAIL ⟹ K-B2 (values stand as certified numbers, CL-F5 PARTIAL) |
| PB.3 | fault semantics (CL-ENG2): sub-predecl B.3 frozen AFTER PB.1/PB.2 grade, BEFORE any B.3 battery (A1/A2 staging pattern); will stake self-fault δν=0 exactness + coupling-fault ratio motion + symbolic theorem | staged | no prediction staked here beyond the staging |

## Kill conditions (armed)
- **K-B0:** any PB.0 gate fails ⟹ pipeline defect; HALT, no verdicts graded.
- **K-B1:** both weight cells fail PB.1 ⟹ bridge-as-stated DEAD at the
  quadratic layer; HALT stage, route to Will. No third candidate, no
  alternative quadratic object, invented post-freeze.
- **K-B2:** PB.2 fails ⟹ CL-F5 → PARTIAL (certified numeric coefficients);
  not a halt; closed-form hunt requires a NEW versioned freeze.
- **K-B3:** (B.3-inherited, armed at its sub-freeze.)
- Envelope 1200 s / 8192 MB; exceed = datum. Byte-stable ×2 mandatory.

## Pins (Rule 1.9 — enforced by battery gate at runtime)
See `freeze_pins.sha256` beside this file: this PREREG, fixtures_stageB.json,
evals/dbp_involution/rep_utils.py, and the two definitional authorities
(Build_Docs/reference/DBP_Curvature_Role_Reduction/{Three_Channel_KG_Strong_Spec,
Gauge_Channel_Transport_Law}.md — tracked copies). Battery reads fixtures +
rep_utils + this file ONLY; refuses on any sha mismatch (REFUSE_MISMATCH) or
clause drift (CLAUSE_DRIFT). role=probe + ledger in every record; probe does
not import the referee path (span residual vs. generator-equivariance are
independently computed and must agree).

## Status moves (frozen)
PB.0+PB.1 PASS ⟹ CL-F5 → STRUCTURAL (bridge exists, exact, fixture-certified);
+PB.2 PASS ⟹ closed form recorded, symbolic derivation owed for PROVEN
(separate, no new battery needed). Any FAIL: per kill table. CL-ENG2 moves
only at B.3. Departure from v1 noted: witness-battery 39bed555 control
dropped (engine-harness already certifies it; foreign-battery run would
muddy this stage's scope) — v1→v2 delta item 2.

frozen: true · v2 · author Claude-session · substrate [BOX] · S-2026-07-05b
