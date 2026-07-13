# c001 · three_channel_kg — CLAIM LEDGER (append-only)

Campaign `three_channel_kg` (cycle `c001`). Opened at the Stage-0 freeze; every claim at
`NOT_YET_PROBED`. A status moves **only** by a stage prereg's frozen `status_move_rules`, graded
against the independent referee. Append-only — never rewrite a prior row. Status vocabulary:
`NOT_YET_PROBED → DEMONSTRATED | REFUTED | PARTIAL`.

| Claim | Statement (n=3, regular, rational `(g,H)`, declared DBP frame) | Status |
|---|---|---|
| CL-c1 | `det(H_b)=Δ_c+Δ_s+Δ_m` ⟹ `K_G=κ_c+κ_s+κ_int`, exhaustive & disjoint | **NOT_YET_PROBED** |
| CL-c2 | bordered-determinant channels ≡ split-shape-operator channels (κ_s non-mirror) | **NOT_YET_PROBED** |
| CL-c3 | no **non-negative scalar** can represent signed `K_G` | **NOT_YET_PROBED** |
| CL-c3b | numerator indefinite ⟹ `K_G` attains both signs (structural) | **NOT_YET_PROBED** |
| CL-c3c-i | `Σ:ℚ³→ℚ` has 2-dim kernel | **NOT_YET_PROBED** |
| CL-c3c-ii | no **invariant** scalar (factoring through `Σ`) recovers the channel representative | **NOT_YET_PROBED** (OPEN — blocked on `{σ_r}`-completeness / L1) |
| CL-c4 | gauge preserves every `σ_r`; `δC∈ker Σ`; single-edge `δκ_c(t·e_i)=4t·∏g·H_{jk}/q²` | **NOT_YET_PROBED** |
| CL-c5 | parity ⟹ `K_G=σ₂` even ⟹ exact-ℚ (core); n≥4 tower NOT established | **NOT_YET_PROBED** |
| CL-c6 | channel tuple non-collapsible on the family (both signs of `κ_int`) | **NOT_YET_PROBED** |
| CL-c7 | frame honesty — sum intrinsic; channels frame-relative, `S₃`+signs invariants (n=3); completeness OPEN | **NOT_YET_PROBED** (PARTIAL by design) |
| CL-c8 | wider tower / `m=2` / tensor / Lovelock / n≥4 grid | **OPEN / successor** — not c001 load-bearing |

## Armed kill conditions (exact ℚ, no tolerance; a FAIL **halts the stage and routes to Will**, chain preserved verbatim)

- **K1 sign-blindness (MANDATORY, refute)** — on F8: `K_G≥0`, or `K_G≠Σchannels`, or `κ_int` absent, or `Δ_m` dropped. *(meta-thesis; CL-c3)*
- **K2 partition (refute)** — `det(H_b)−(Δ_c+Δ_s+Δ_m)≠0`. *(CL-c1)*
- **K3 two-derivation (refute)** — Path-A channels ≠ Path-B′ channels (incl. κ_s-mirror mutant). *(CL-c2)*
- **K4 gauge / single-edge (refute)** — `σ_r` changes under gauge, or `δC∉ker Σ`, or single-edge law fails (e₁/e₂ fail to pin, e₃ fails to move). *(CL-c4)*
- **K5 wrong-sign (refute)** — bordered-Hessian sign flip inverts an expected sign (F3/F7/F8). *(object integrity)*
- **K6 rank-heuristic (refute)** — nonzero on the developable cone F9. *(CL-c6)*
- **K7 frame-undeclared (refute)** — a legitimate rechart reported as a curvature error, or `σ₂` not held invariant under F12. *(CL-c7)*
- **K8 √q-leak (type gate)** · **K9 tolerance-leak (type gate)** · **K10 parity-type (type gate)** · **K11 singular-lie (refuse-not-lie)**.
- **K-soft completeness (flag, non-refuting)** — two surfaces, identical `{σ_r}`+orientation, not gauge+permutation related. *(L1; CL-c3c-ii / CL-c7 completeness)*
- **Preconditions** — **P-self-cert**, **P-frame** (run-void on failure).

## Scope & recorded dispositions

**IN:** the signed n=3 three-channel `K_G`, regular rational jets, exact-ℚ, declared DBP frame
(CL-c1..c7); the HR138 relabel + Theorem-8.1 freeze-hold **re-established** (adoption is
Records'/Will's, not this campaign's).
**OUT (→ c002):** the carrier / ⊕-universality re-ask (WARP Q2; §5.1/5.2 multiplicative-escape with
its rational-op-class / Richardson-wall cost); n≥4 grid; `m=2`/tensor/Lovelock; "one spine or a
family"; substrate promotion (**eval-tier only — the geometry spine fence stays closed**).

**Prior-art gate:** cleared — Archivist audit `c001__PRIOR_ART_AUDIT` read first-hand; its one
fundamental finding (A1, sequencing) is already absorbed by the merged spec (c001 = the 138 redo;
carrier/⊕ deferred to c002).

**Reserved-ruling dispositions (recorded by Records; Will may override):**
- **R3 (F12 pin) — CLOSED.** `R∈SO(3)`, rotated jet, and tuples pinned in `FIXTURES.md` (exact ℚ).
- **R1 ([PROVEN] warrant) — disposition: logic-forced, not discretionary.** A verified finite
  exact-ℚ both-sign witness earns `[PROVEN]` for an *impossibility / existence* claim (CL-c3);
  *universal* claims (CL-c1, CL-c3b) require the symbolic identity over `ℚ[g,H]`. The stage prereg
  encodes this in `status_move_rules`.
- **R2 (supplied-frame) — disposition: the channels are frame-relative in the supplied DBP frame;
  only the sum `K_G` is intrinsic** (the merged spec's own stance §1/§3.1; the "connection, not
  metric" reading concurs — channels as gauge components, the sum/holonomy as the invariant).
  CL-c7 is graded accordingly.

---

*Stage close blocks are appended below as each stage grades against its frozen prereg.*


---

<!--
  c001 · three_channel_kg — STAGE A ledger close block.
  The merge-packager APPENDS this to results/three_channel_kg/CLAIM_LEDGER.md
  (append-only; never rewrite a prior row). The stage-runner did NOT touch the
  shared CLAIM_LEDGER.md. Eval-tier; nothing canonical until Will signs off.
-->

## Stage A close — retrodiction spine + Stage-0 controls (2026-06-23)

**Graded against** the frozen `stage_a/prereg.json`
(pin `ecced952d202c140b54a69d9042f78120326dfbee4090dd3a17574dcb4dad628`), records
`stage_a/records.jsonl` (sha256 `53321e5c53dcd43294539120f1c5f1625b68b9e5489c023260b5b416bc917376`,
two-run byte-identical), suite exit 0. Predictions **13/13 PASS**; kills fired **NONE**; preconditions
**hold** (P-self-cert, P-frame; run not void); defect-chain count **0**.

| Claim | Statement (n=3, regular, rational `(g,H)`, declared DBP frame) | Move | Status |
|---|---|---|---|
| CL-c1 | `det(H_b)=Δ_c+Δ_s+Δ_m` ⟹ `K_G=κ_c+κ_s+κ_int`, exhaustive & disjoint | `NOT_YET_PROBED →` | **DEMONSTRATED** |
| CL-c2 | bordered-determinant channels ≡ split-shape-operator channels (κ_s non-mirror) | `NOT_YET_PROBED →` | **DEMONSTRATED** |

- **CL-c1 → DEMONSTRATED (universal warrant, R1-compliant).** Gating predictions P1, P2, P3, P11,
  P12, P13 all PASS. R1 (universal claim) satisfied via the **symbolic identity over ℚ[g,H]** (P12):
  the cofactor-expanded `det(H_b)` minus `Δ_c+Δ_s+Δ_m` is the zero polynomial (0 residual monomials;
  12 det / 12 partition monomials; pairwise-disjoint supports whose union equals the det support) —
  NOT downgraded to a finite-only warrant. Finite family (P1/P2/P3/P11/P13, exact ℚ across Paths
  A/B/B′/C, keystone F8 pinned) corroborates. K2 (partition) silent.
- **CL-c2 → DEMONSTRATED (frozen family; non-R1).** Gating predictions P1, P2, P4 all PASS. The two
  disjoint channel derivations — Path A monomial vs Path B′ split-shape-operator — agree
  channel-for-channel across the frozen family `{F1..F11}`; K3 silent; the **non-mirror** κ_s is
  established (the naive κ_s-mirror mutant is rejected by K3 on the trap set F5/F6/F8). Warrant scope:
  the frozen Stage-A family (finite, exact ℚ), NOT a symbolic-over-ℚ[g,H] universal (CL-c2 is not an
  R1 universal claim).

**Armed kills (all silent on truth; each shown to fire on a constructed mutant):**
K2 (partition) — residual `0` on all 11, Path-A det = Path-B det. K3 (two-derivation) — A==B′ on all
11; κ_s-mirror mutant differs on F5/F6/F8. K5 (wrong-sign) — true sign matches oracle on F3/F7/F8;
sign-flip inverts. K6 (rank-heuristic) — F9 developable cone exactly `0` on A/B/B′/C. K8 (√q-leak) —
all emitted values `Fraction`; float operand raises `TypeError`. K9 (tolerance-leak) — `+1/10⁹`
near-miss on F8 → row-pass FALSE (no tolerance). K11 (singular-lie) — genuine `q=0` (g=(0,0,0)) typed
REFUSED on A/B/B′; F6 single `g_i=0` (q=4) → `K_G=1` (no spurious refusal).

**Scope:** Stage A graded CL-c1, CL-c2 and armed K2/K3/K5/K6/K8/K9/K11 with P-self-cert/P-frame over
fixtures F1–F11, F13. K1/K4/K7/K10 and F12/F12a/F12b are out of Stage-A scope (other stages).

**Discipline:** exact ℚ, no tolerance; eval-tier only (geometry spine fence stays CLOSED; no substrate
promotion); proposed moves PENDING Will's sign-off — nothing canonical until then.


---

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


---

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


---

<!--
STAGE D ledger close block. Written into stage_d/ by the stage-runner; the
merge-packager APPENDS this to the shared results/three_channel_kg/CLAIM_LEDGER.md
(append-only). The stage-runner does NOT edit the shared ledger.
-->

## Stage D close — frame honesty (CL-c7, PARTIAL by design) — 2026-06-23

**Prereg pin:** `ae399cb1d4fe5cd37afc615cdb2c5e4e2e2246e1ee9b6542d3484f73930e118a`
**Records sha256:** `0aceffdd3133713a0985381e347b958c730e012c2e0958e48f045c355a87238d` (12 records; byte-stable over two runs)
**Suite:** exit 0 · **Predictions:** 9/9 PASS · **Defect-chain:** 0

| Claim | Prior status | Stage-D verdict | New status (proposed) |
|---|---|---|---|
| CL-c7 | NOT_YET_PROBED (PARTIAL by design) | provable frame-honesty core graded on the frozen F12 pin (R3): F12a channels MOVE `(−1/49,1/49,−3/49)→(−961/30625,2713/30625,−3627/30625)` while `K_G=σ₂=−3/49` INVARIANT (frame-relativity / R2); F12b signed permutation FIXES channels and `K_G` invariant (`S₃⋉{±}` at n=3); K7 NOT fired; completeness left OPEN | **PARTIAL** (NOT DEMONSTRATED) |
| CL-c3c-ii | NOT_YET_PROBED (OPEN — blocked on `{σ_r}`-completeness / L1) | recorded OPEN; NOT closed by Stage D; K-soft raised as a non-refuting FLAG | **OPEN** (no move) |

**Kills:** K7 (frame-undeclared, refute) — **NOT FIRED** (recharts legitimate/orthogonal, `σ₂` held
invariant under both F12a/F12b). K-soft (completeness) — **non-refuting FLAG** raised
("completeness unestablished"; no in-scope refuting witness manufactured; does not refute, does not
fail a prediction).

**Dispositions encoded:** R2 (channels frame-relative in the supplied DBP frame; only the sum `K_G`
intrinsic) · R3 (F12 pin CLOSED; exact-ℚ tuples from FIXTURES.md used verbatim).

**Scope/fences:** eval-tier only; no substrate promotion; nothing canonical until Will signs off.
PARTIAL by design — the `{σ_r}`-completeness / L1 question (CL-c3c-ii) stays OPEN as a successor.

*Authority: frozen objects under `results/three_channel_kg/` verified vs `freeze_pins_sha256.json`;
bench imported read-only and pinned in `stage_d/prereg.json` `depends_on`. Covenant loop; prereg
frozen pre-emission; clauses embedded verbatim + gated; two-run byte-stability; mutation guards prove
a lying engine is caught.*


---

<!--
Stage-E ledger close block. The merge-packager APPENDS this verbatim to the
shared results/three_channel_kg/CLAIM_LEDGER.md after consolidation. The
stage-runner does NOT touch the shared CLAIM_LEDGER.md (covenant step 6).
-->

## Stage E close — parity / σ₂ exactness (CL-c5, n=3 core) — 2026-06-23

**Authority:** frozen objects under `results/three_channel_kg/` verified vs
`freeze_pins_sha256.json`; frozen bench imported read-only + pinned in
`depends_on` (re-verified at runtime). Prereg frozen pre-emission.
**Prereg pin:** `0e714fed74de39a6a8f5fba9d8ce35efafbc5c27826ba6fed83e0308be521891`
**Records sha256 (byte-stable, two identical runs):**
`c78220f855c6d03f34fef5274d33b39a2230c7ee2154451ca2c92adbda107787`
**Suite exit:** 0. **Defect-chain count:** NONE (0).

| Claim | Prior status | Graded result | New status |
|---|---|---|---|
| CL-c5 | NOT_YET_PROBED | parity ⟹ `K_G=σ₂` even ⟹ exact-ℚ — n=3 CORE verified (P1–P6 all PASS); even/odd type contrast holds (`σ₂=−3/49∈ℚ` vs `σ₁∈ℚ(√14)`); K10 silent on truth, fires on the constructed mutant | **DEMONSTRATED (n=3 core only)** |

- **Warrant scope:** the n=3 keystone (F13) parity row, exact ℚ. `σ₂ = K_G = −3/49`
  even-order exact-ℚ (Path B total, Path B′ det2 shape-operator, Path C oracle, and
  `−det(H_b)/q²` all agree); `Ĉ₁ = −24 = −2·det(H_b)` even-order exact-ℚ; `σ₁` odd-order
  in `ℚ(√14)` (`σ₁²=72/343∈ℚ`, `σ₁∉ℚ` since 14 is a non-square), correctly WITHHELD by the
  oracle. Verified-finite exact-ℚ parity/type contrast — **NOT** a symbolic-over-ℚ[g,H]
  universal.
- **`n≥4` tower:** **NOT established (OPEN; successor c002).** This close covers the
  **core only**, not the tower.
- **K10 (parity-type, type gate):** ARMED — **silent** on the unmutated bench (no
  odd/radical invariant emitted as exact-ℚ; parity distinction intact) and **fires** on a
  battery-owned mutant that emits `σ₁` as a `Fraction` (exactness witness `m²≠72/343`).
- **Tier:** eval-tier; **no substrate promotion**; **canonical only on Will's sign-off.**
- **Surfaced finding (mechanics, not a defect):** Stage-E worktree branches from the
  pre-bench base; the battery resolves the frozen bench via the `__file__`-relative path
  (post-merge on `main`) with a fallback to the stable main checkout (named in the launch
  block). `depends_on` sha256 re-verifies the resolved bench content-for-content; records
  content is path-independent. Merge-packager: confirm the `__file__`-relative branch
  activates post-merge.
- **Other stages / shared files:** untouched. Wrote only inside `stage_e/`.

---

## Campaign acceptance — Will's sign-off (2026-06-23)

**Will accepted the proposed status moves as c001's standing results.** The claims below are no
longer *proposed*; they stand as the campaign's results at the statuses graded above. Recorded here
as the single eval-to-canonical gate; the prior naming ceremony (HR rows, glossary, alias/WORKING_SET
bookkeeping) is **expunged by Will's instruction** — no further close stage runs.

| Claim | Standing status (accepted) |
|---|---|
| CL-c1 | **DEMONSTRATED** — universal (R1 symbolic identity over ℚ[g,H]) |
| CL-c2 | **DEMONSTRATED** — frozen family (non-R1) |
| CL-c3 | **DEMONSTRATED [PROVEN]** — impossibility/existence (R1) |
| CL-c3b | **DEMONSTRATED [PROVEN]** — R1 universal |
| CL-c3c-i | **DEMONSTRATED [PROVEN]** — exact-ℚ linear algebra |
| CL-c4 | **DEMONSTRATED** — gauge/single-edge (R2; symbolic over ℚ) |
| CL-c5 | **DEMONSTRATED (n=3 core only)** — n≥4 tower OPEN → c002 |
| CL-c6 | **DEMONSTRATED** — frozen family, both signs of κ_int |
| CL-c7 | **PARTIAL (by design)** — frame-honesty core; completeness OPEN |
| CL-c3c-ii | **OPEN** — no move; K-soft raised as a non-refuting flag |
| CL-c8 | **OPEN / successor (c002)** — not c001 load-bearing |

**Scope of this acceptance.** Eval-tier only. Accepting these results does **not** promote anything to
the V4/Cella substrate and does **not** unfence the spine — the geometry-spine fence stays **CLOSED**.
c001 stands as hardened evidence on the geometry arm; the algebra arm (carrier / ⊕-universality, WARP
Q2), n≥4, and the tensor/Lovelock elevation remain owed to c002. Promotion, if ever, is a separate
exercise on Will's hand.

*— Campaign c001 `three_channel_kg` CLOSED, accepted. Recorded by the Dev Role Manager on Will's
sign-off. Append-only; prior rows unchanged.*
