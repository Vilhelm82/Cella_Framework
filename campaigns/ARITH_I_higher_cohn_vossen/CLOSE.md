# ARITH-I — CAMPAIGN CLOSE

**Date:** 2026-07-06/07. **Verdict: both central questions resolved.** Paper-track
fence held throughout — no engine priority was changed. PREREG `32f2fb3a` (with the
fabricated stop-condition clause VOID, `CORRECTION_2026-07-06_fabricated_stop_condition.md`).

## What closed

**Stage A COMPLETE — the r=2 reduction, family-wide** (`STAGE_A_COMPLETE.md`):
- Full closed form, every constant an OUTPUT of the shear `s`:
  `∫_S K_G dA = −2L(s)`, `L(s) = 2g[Π(n;A) − (1−C)K(A)]`, `k²=A(s)=½−1/(2√(1+s²))`,
  `n(s)=(A−C)/(1−C)`, `g(s)=2√((1−A)/(C(1−C)))`; keystone reproduces the certified Booth
  form symbolically (`n(1)=(4−3√2)/8`, weights `2^(7/4)(3+2√2),(2+2√2)`).
  (`arith_i_stageA_family.py` `4d60e109`.)
- Curve modulus PROVEN `k²=A(s)`; **K-2 CLOSED family-wide** — `Φ₂(j_reg(s),j_λ(s))≡0`,
  the register curve 2-isogenous to the differential curve for all `s`
  (`arith_i_stageA_s2.py` `b2d29718`). This extends the arithmetic-track keystone
  isogeny (j=128↔10976) to the whole family.
- Open pins re-derived (`arith_i_open_pins.py` `a2ef103d`). K-1/K-4 clean.

**Stage B CLOSED — the r=3 exactness discriminator** (`STAGE_B_VERDICT.md`,
`CORRECTION_2026-07-06_channel_normalization.md`):
- Structural key: the canonical n=4 surface `F=Σy_i²+Σ_{i<j}y_iy_j−c` is a COMPACT
  ELLIPSOID (`M=(I+J)/2 ≻ 0`), so exact ⟺ ∫=0. (`e_3(P Hc P)≡0` at n=3 forces the
  question to n≥4; CALC-24 Part A species-change confirmed — the elliptic handle is
  bonded to n=3.)
- **VERDICT: `∫_S κ_{3;3,0} dA = −2π²/√5 ≠ 0` → NOT EXACT** (`arith_i_stageB_proof.py`
  `f2f851ea`, machine-checked). Value is `π²·(1/√5)`, an algebraic-irrational
  (odd-`r` parity `√5=√(n+1)`), NOT an elliptic period. Resolves T-B/T-C with a THIRD
  outcome (C1 exact FALSE, C2 elliptic-period wrong character). K-3 not triggered.
- **Normalization correction (Will):** the standard channel is `−e_3(P Hc P)/q^{3/2}`
  (bordered identity `det[[Hc,g],[gᵀ,0]]=−q·e_3`), not the `/q^{5/2}` auxiliary
  1/q-weighted object that gave the earlier rational `−2π²/5`. Tells banked: odd-`r`
  constants carry `√q`; the standard density is scale-invariant.

## Consistency check (external doc, 2026-07-07)

Will's `DBP_Curvature_Constants_Corrected_Formulation.md` was cross-verified against
this campaign + the arithmetic-track close-off: `I_primary=−5.0104907…` (45+ digits),
closed form, `k²`, `n`, `λ(1−λ)=1/8`, `j(E_λ)=10976`, `j(E_128)=128`, `Φ₂(128,10976)=0`,
dual CPV `…9694121855…`, `Res_DBP=4`, `±4πi/8πi` — all match. It is the **n=3/r=2
elliptic-period story**; the Stage-B `−2π²/√5` is the **n≥4 compact Gauss–Kronecker
story** — complementary, consistent, non-overlapping. My K-2 result is the family-wide
generalization of its keystone isogeny. No conclusion revised.

## Open follow-ups (paper-track — do NOT set engine priority)

1. General-n top-order (r=n−1) channel constant: redo with the standard `q^{(n−1)/2}`
   (the auxiliary-normalized `−(n−2)/(2(n+1))`/`−1/(n+1)` are VOID); expect a `√(n+1)`
   odd-parity factor. Confirm n=5 (predicts `−…/√6`-type).
2. r=3 with n>4 fixed (where `e_3` is not the full compression determinant) — a
   genuinely different computation, still open.
3. Stage-A family-tier: a §I.3b Johnson-operator re-derivation of the closed form, if a
   role-channel-language write-up is wanted.
4. Prior-art sweep before any external novelty claim (Chern–Lashof, Gauss–Kronecker of
   symmetric quadrics, Willmore) — explicitly out of scope here per Will.

## Ledger

Kills: K-1 clean, K-2 CLOSED family-wide, K-3 not triggered, K-4 clean. LEAD-8 verdict:
both central questions resolved. Case law banked: (a) fabricated stop condition VOID;
(b) channel normalization (bordered vs compression, the `q`-power). ARITH-I: CLOSED.
