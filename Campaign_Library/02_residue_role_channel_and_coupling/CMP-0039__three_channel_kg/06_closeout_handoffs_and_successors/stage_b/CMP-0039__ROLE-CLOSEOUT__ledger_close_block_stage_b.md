<!--
c001 three_channel_kg — STAGE B ledger close block.
The merge-packager APPENDS this block to results/three_channel_kg/CLAIM_LEDGER.md
(append-only; never rewrite a prior row). The stage-runner does NOT touch the
shared CLAIM_LEDGER.md. Eval-tier only; nothing canonical until Will signs off.
-->

## Stage B close — non-negativity impossibility (2026-06-23)

**Authority:** frozen objects verified vs `freeze_pins_sha256.json` (manifest `a28042d9…`, SCHEMA
`fe0eb353…`, FIXTURES `3d933e39…`); bench imported read-only and re-pinned in `depends_on`.
**Prereg pin:** `6602b9e9511bc40d9ef6d8f08928dadd628e9c9b671f334ff4027a79461a467d`
**Records sha256:** `b26a3eb9ee6bbef2d732592b2d603643ec9194374ae9273655c47c44b4e0c1f2` (byte-stable, two runs).
**Suite:** exit 0. **Predictions:** 10/10 PASS. **Defect-chain:** NONE (0). **Halt:** none.

Graded against the frozen `stage_b/prereg.json` `status_move_rules` (R1/R2 dispositions). Status moves
proposed (each gated by ALL listed predictions passing):

| Claim | Statement (n=3, regular, rational `(g,H)`, declared DBP frame) | Status | Warrant / gating |
|---|---|---|---|
| CL-c3 | no **non-negative scalar** can represent signed `K_G` | **DEMONSTRATED [PROVEN]** | R1 logic-forced (impossibility/existence): negative witness `K_G(F8)=−3/49<0` refutes every `p≥0`; positive witness `K_G(F6)=+1>0` confirms two-signedness; K1 silent on true object, fired by all sign-blind proxies. Gates: P1∧P2∧P3∧P7. |
| CL-c3b | numerator indefinite ⟹ `K_G` attains both signs (structural) | **DEMONSTRATED [PROVEN]** | R1 UNIVERSAL: symbolic identity over `ℚ[g,H]` established — `det(H_b)` indefinite (specialises to `K_G(t)=+t`, nonconstant, both signs on a regular family); `q²>0` premise underwritten by K11 refusal. NOT downgraded to finite-only. Gates: P4∧P8 (+P3/P7). |
| CL-c3c-i | `Σ:ℚ³→ℚ` has 2-dim kernel | **DEMONSTRATED [PROVEN]** | exact-ℚ linear algebra: `Σ=[[1,1,1]]` rank 1 ⟹ nullity `3−1=2`; `(1,−1,0),(1,0,−1)` independent kernel vectors. Gate: P5. |
| CL-c6 | channel tuple non-collapsible on the family (both signs of `κ_int`) | **DEMONSTRATED** | finite both-sign witnesses on the frozen family: F10 `κ_int=−1/9<0`, F11 `κ_int=+2/9>0`, agreeing across Path A/B′/C. Warrant scope: the frozen family (finite, exact ℚ), NOT a ℚ[g,H] universal. Gate: P6 (+P7). |

**Armed kills:** K1 (sign-blindness, MANDATORY) — true signed F8 object PASSES (no false positive);
all sign-blind proxies (`K_G²=9/2401`, `H²=18/343`, `p≥0`, drop-`Δ_m` `κ_c+κ_s=0`, omit-tuple) FIRE.
K8 (√q-leak) and K11 (singular-lie/refuse-not-lie) held. No kill fired against the object.

**Pinned note (carried from Stage A finding #2, honoured):** manifest `stage0_controls` `κ²=9/2401` is
`K_G²=(−3/49)²` (squared TOTAL, a legitimate sign-blind proxy), NOT the channel-norm
`κ_c²+κ_s²+κ_int²=11/2401`; recorded as such (no transcription error).

**Scope:** eval-tier only; geometry spine fence stays CLOSED; no substrate promotion. Nothing canonical
until Will signs off. Out of Stage-B scope: K2/K3/K4/K5/K6/K7/K9/K10 and the F12 family (other stages).
