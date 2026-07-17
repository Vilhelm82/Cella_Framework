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
