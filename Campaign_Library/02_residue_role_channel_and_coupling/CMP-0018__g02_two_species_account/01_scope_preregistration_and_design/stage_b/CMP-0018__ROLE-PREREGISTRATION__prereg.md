# STAGE B PREREG — the defective base point

**FROZEN before any battery code is written or run.** The closed forms below are
STAKED derivations — the battery's job is to break them symbolically and exactly.
A staked formula failing is K-B1 (halt, re-derive), not an adjustable parameter.

## Setting

Base defect on the gradient slot: true `g`, held `g' = g + e`, `e ∈ Q^n` (species M
on the parameter). Both `g` and `g'` regular. `w_ij := g_i e_j − g_j e_i` (the wedge
`g ∧ e`). All other notation per RC-2 / Stage A.

## Staked closed forms (derived 2026-07-06, pre-battery)

```
(F1)  O_{g',ij}(H) − O_{g,ij}(H)  =  (w_ij / 2) · [ H_jj/(g_j g'_j) − H_ii/(g_i g'_i) ]

      — EXACT TOTAL (not first-order); rational in (g, e, H).

(F2)  G_{g'}(a) − G_g(a)  =  G_e(a)          (= e a^T + a e^T)

(F3)  O_g(G_e(a))_ij  =  e_i a_j + a_i e_j − (g_i/g_j) e_j a_j − (g_j/g_i) e_i a_i
```

## Predictions

- **TB-P1 (closed form).** F1 holds symbolically (n = 3, 4, 5, all indeterminates).
  *Corollary staked:* the cross-term reads **only diag(H)** — `∂Δ/∂H_kl = 0` for every
  off-diagonal slot. The base-point contamination lives entirely in self-data.
- **TB-P2 (radial invisibility).** `e ∥ g ⟹ Δ ≡ 0`; stronger: `O(H; λg) = O(H; g)`
  for all `λ ≠ 0` — the carrier depends only on the RAY of g. The g-slot defect
  therefore decomposes into an **invisible radial part and a visible wedge part** —
  the two-species pattern recursing into the parameter slot. [STRUCTURAL if it holds]
- **TB-P3 (wedge control).** Δ vanishes for ALL H iff `w = 0`; constructive witness:
  if `w_ij ≠ 0`, then `H = unit diag at i` gives `Δ_ij = −w_ij/(2 g_i g'_i) ≠ 0`.
- **TB-P4 (gauge-execution defect).** F2, F3 symbolic; witness `O_g(G_e(a)) ≠ 0`
  generically — an R-step executed at a defective base moves the TRUE state:
  genuine damage, not representation motion. By RC-2 (`ker O = Im G_g`) this proves
  `G_e(a) ∉ Im(G_g)` generically.
- **TB-P5 (attribution theorem — the Stage-B claim).** For a mixed chain executed at
  defective base `g'`: fold the cross-terms into M —
  `rho_M* = Σ E_k + G_e(Σ a_j)`, `rho_R = Σ a_j` (intended parameters only). Then
  `O_g(H_final − rho_M*) == O_g(H_0)` exactly (symbolic + exact-ℚ chain), and the
  per-reading correction is F1. **The R-ledger stays pure; every contamination is
  M-attributed in closed form.**
- **TB-P6 (exact carrier).** Every cross-term (F1, F2, F3 values) is Fraction-typed
  on rational data end-to-end — no radical, no float, no enclosure. (K-3 probe.)
- **TB-P7 (mutants — must all be caught).**
  (i) *First-order mutant*: `H_jj/g_j²` in place of `H_jj/(g_j g'_j)` must FAIL exact
  equality at finite `e`.
  (ii) *R-contamination mutant*: absorbing `G_e(a)` into the R-ledger (claiming some
  `a''` with `G_g(a'') = G_e(a)`) must be refuted by the witness `O_g(G_e(a)) ≠ 0`.
  (iii) *Dropped-correction mutant*: omitting `G_e(Σa)` from `rho_M*` on a wedge
  fixture must break TB-P5 reconstruction.

## Grading gate

Stage B closes DEMONSTRATED iff TB-P1..P6 all PASS (symbolic tier n = 3,4,5 where
stated; exact-ℚ battery n = 3) and all three mutants are caught. Byte-stable ×2.

## Kills (armed)

- **K-B1** — a staked formula fails → derivation error → STAGE HALT, re-derive; the
  failed form is preserved verbatim.
- **K-B2** — contamination provably NOT exactly M-attributable → the Stage-B claim of
  the conjecture is REFUTED → finding, not failure: A-002 record updated, account
  design moves to the two-ledger fallback with a named boundary.
- **K-B3** — any cross-term leaves ℚ on rational data → the enclosure-or-refusal
  boundary moves into Layer 0; document, do not hide.
- **K-B4** — any mutant undetected → battery vacuous → no close.
