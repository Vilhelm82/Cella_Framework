<!--
  c001 · three_channel_kg — STAGE C ledger close block (CLEAN RE-RUN).
  The merge-packager APPENDS this to results/three_channel_kg/CLAIM_LEDGER.md
  (append-only; never rewrite a prior row). The stage-runner did NOT touch the
  shared CLAIM_LEDGER.md. Eval-tier; nothing canonical until Will signs off.
-->

## Stage C close — gauge / single-edge (2026-06-23, clean re-run)

**Graded against** the frozen `stage_c/prereg.json`
(pin `8e2a26444c8440daf82b9ce17f561f3d59ae4018db52cbaf4bd73b010a681464`), records
`stage_c/records.jsonl` (sha256 `65d601637a428655c6a8e5140895b5b2a78a64a7f2961b5a9d60bb1d72a2ea5a`,
two-run byte-identical), suite exit 0. Predictions **9/9 PASS**; kills fired **NONE** (K4
silent); preconditions **hold** (P-self-cert, P-frame; run not void); defect-chain count **0**.
This is a clean re-run per Will's ruling: the CORRECT grader from the first scored run, NO mid-run
grader fix, reproducing the prior verified science with a clean transcript.

| Claim | Statement (n=3, regular, rational `(g,H)`, declared DBP frame) | Move | Status |
|---|---|---|---|
| CL-c4 | gauge preserves every `σ_r`; `δC∈ker Σ`; single-edge `δκ_c(t·e_i)=4t·∏g·H_{jk}/q²` | `NOT_YET_PROBED →` | **DEMONSTRATED** |

- **CL-c4 → DEMONSTRATED (R2; symbolic over ℚ).** Gating predictions PC1–PC9 all PASS. The
  single-edge gauge is the border shear `H → H + t(g e_iᵀ + e_i gᵀ)` (g unchanged). Because
  `P g = 0` (the tangent projector `P = I − g gᵀ/q` annihilates the gradient), the gauge
  generator satisfies `P(g e_iᵀ + e_i gᵀ)P = 0`, so the tangent shape operator `P H P` is
  **exactly fixed** — proven SYMBOLICALLY over ℚ (PC6: `q²·(PH′P − PHP)` is the zero 3×3
  matrix on every edge). Hence **every** `σ_r` is preserved (σ₂ = K_G = −3/49 ∈ ℚ; σ₁ =
  tr(PHP)/|g| ∈ ℚ(√14), rational handle tr(PHP) = 12/7 invariant), not merely the sum.
  `δC ∈ ker Σ` (PC4: `Σ(δC)=0` on e₁/e₂/e₃ at every witness t; the channel triple trades
  within the fiber — **δκ_c pins on e₁/e₂ while κ_s and κ_int move oppositely**; the pin/move is
  keyed on the coupling channel δκ_c, not the whole vector C). The single-edge law
  `δκ_c(t·e_i) = 4t·∏g·H_{jk}/q²` is a **symbolic identity over ℚ[g,H,t]** (PC5: zero-polynomial
  residual on every edge), witnessed exactly at the keystone F8 (PC1/PC2: **e₁ pins**, **e₂ pins**,
  **e₃ moves 6/49** per unit t). Concrete witness (e₁, t=1): base `(κ_c,κ_s,κ_int)=(−1/49,1/49,−3/49)`
  → gauged `(−1/49,4/49,−6/49)`, `δC=(0, 3/49, −3/49)`, `Σ(δC)=0`, `K_G=−3/49` invariant (the vector
  moves, δκ_c pins). K_G invariant on Paths A/B/B′; the two channel derivations agree on the moved
  decomposition (PC7). **Warrant scope:** R2 — channels frame-relative in the supplied DBP
  frame, the sum K_G (= σ₂) intrinsic; symbolic-over-ℚ for the law + σ_r invariance, keystone
  witness for the pin/move. **Eval-tier; NOT a substrate promotion; PENDING Will's sign-off.**

**Armed kill K4 (gauge / single-edge) — silent on truth; each branch shown to bite a mutant:**
a raw diagonal-bump "gauge" (`H_ii += t`, NOT the border shear) changes K_G on every edge
(σ_r not preserved → K4 fires); a wrong-law mutant using the diagonal `H_ii` in place of the
complementary off-diagonal `H_{jk}` differs from the true law; an "e₁ moves" claim is FALSE
against the true `δκ_c = 0`; a non-shear gauge leaves a nonzero symbolic PHP/det residual
(PC5/PC6 non-vacuous).

**Scope:** Stage C graded CL-c4 only and armed K4 with P-self-cert/P-frame over the
GAUGE_SINGLE_EDGE fixture set (keystone F8 perturbed along `t·e₁, t·e₂, t·e₃`). All other
kills (K1/K2/K3/K5/K6/K7/K8/K9/K10/K11) and fixtures belong to sibling stages (B/D/E) and
Stage A.

**Discipline:** exact ℚ, no tolerance; eval-tier only (geometry spine fence stays CLOSED; no
substrate promotion); proposed move PENDING Will's sign-off — nothing canonical until then.
