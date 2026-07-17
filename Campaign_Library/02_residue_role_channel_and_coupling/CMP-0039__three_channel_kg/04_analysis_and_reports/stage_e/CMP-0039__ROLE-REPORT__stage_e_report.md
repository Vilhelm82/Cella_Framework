# c001 · three_channel_kg — STAGE E REPORT (parity / σ₂ exactness)

- **Date:** 2026-06-23
- **Stage:** stage_e — parity / σ₂ exactness (CL-c5, n=3 CORE)
- **Mode:** FAN-OUT stage, parallel with siblings B/C/D. A FAIL here halts ONLY
  this stage and routes to Will; siblings continue.
- **Authority:** Frozen objects under `results/three_channel_kg/`
  (`manifest_v1.json`, `SCHEMA.md`, `FIXTURES.md`, `CLAIM_LEDGER.md`) verified vs
  `freeze_pins_sha256.json` (the three pinned objects match; CLAIM_LEDGER
  intentionally unpinned, sha recorded). Built + frozen bench under
  `src/lloyd_v4/evals/three_channel_kg/` imported READ-ONLY by exact file path
  and pinned in `depends_on` (re-verified at runtime). ORCHESTRATOR OVERRIDE
  honoured: no `v4-campaign-discipline` skill loaded; frozen objects + the
  embedded covenant are the SOLE binding authority.
- **Prereg pin (`prereg_sha256.pin`):**
  `0e714fed74de39a6a8f5fba9d8ce35efafbc5c27826ba6fed83e0308be521891`
- **Records sha256 (`records.jsonl`):**
  `c78220f855c6d03f34fef5274d33b39a2230c7ee2154451ca2c92adbda107787`
- **Byte-stable note:** the battery was run TWICE; both runs produced a
  byte-identical records jsonl (same sha256 above; `cmp` clean). The canonical
  `records.jsonl` equals the twice-run sha. Determinism: every record value is a
  `fractions.Fraction` serialised `frac:n/d`; `json.dumps(sort_keys=True)`; no
  float / time / randomness reaches any record field. The K10 mutant uses
  `math.sqrt` ONLY to forge a lying numeric σ₁, then rationalises with a fixed
  `limit_denominator(10**9)` bound (deterministic) — the forged value enters a
  record only as a `frac:n/d` string.
- **Suite exit code:** `0` (17 tests; `test_stage_e.py`, run under
  `PYTHONPATH=/home/wlloyd/Lloyd_Engine_V4/src python3 -m pytest -q`).

## Scope (frozen)

- **Claim:** CL-c5 — parity ⟹ `K_G = σ₂` even ⟹ exact-ℚ. **n=3 CORE ONLY.** The
  `n≥4` tower is NOT established and is OUT of scope (successor c002).
- **Armed kill:** K10 — parity-type (type gate): fires if an odd-order /
  radical-bearing invariant is emitted as if exact-ℚ, or if the even/odd parity
  distinction is violated.
- **Fixture:** F13 keystone, rungs r=1 (σ₁, odd) and r=2 (σ₂ = K_G, even).
  Keystone jet g=(3,1,2), H=[[2,1,0],[1,0,0],[0,0,2]], q=14 (so √q = √14).
- **Anchors:** `σ₂ = −3/49 ∈ ℚ` (even, exact-ℚ, == keystone `K_G`),
  `Ĉ₁ = −24 ∈ ℚ` (even, exact-ℚ, == `−2·det(H_b)`), `σ₁ ∈ ℚ(√14)` (odd,
  radical-bearing; `σ₁² = 72/343 ∈ ℚ` but 14 is a non-square so `σ₁ ∉ ℚ`).
- **Preconditions:** P-self-cert (oracle external to A/B/B′) and P-frame (F13
  carries its frame annotation) — both hold; run not void.

## Verdicts table

| Prediction | Statement (n=3 parity core) | Result |
|---|---|---|
| **P1_sigma2_even_exact_Q** | EVEN-order σ₂ = −3/49 is a `Fraction` and == keystone `K_G` on Path B total, Path B′ det2(P H P)/q, Path C oracle, and == `−det(H_b)/q²`. | **PASS** |
| **P2_sigma1_odd_radical** | ODD-order σ₁ ∈ ℚ(√14)\ℚ: tr(P H P)=12/7 ≠ 0, σ₁²=72/343 ∈ ℚ, 14 not a perfect square ⟹ σ₁ ∉ ℚ; oracle withholds σ₁ (no attr; no numeric note). | **PASS** |
| **P3_C1hat_even_exact_Q** | EVEN-order Ĉ₁ = −24 is a `Fraction`, == `−2·det(H_b)`, det(H_b)=12. | **PASS** |
| **P4_parity_witness_contrast** | The contrast holds: even σ₂ & Ĉ₁ emitted exact-ℚ; odd σ₁ radical-bearing & withheld. σ₂ ∈ ℚ vs σ₁ ∈ ℚ(√14) is the parity witness. | **PASS** |
| **P5_K10_silent_on_truth** | On the unmutated bench, no odd/radical invariant is emitted as exact-ℚ; parity distinction intact ⟹ K10 silent. P-self-cert & P-frame OK. | **PASS** |
| **P6_K10_fires_on_mutant** | A battery-owned mutant emits σ₁ as a `Fraction` m; exactness witness `m² ≠ σ₁²=72/343` (forging √14 ∈ ℚ is impossible) ⟹ K10 FIRES. Even σ₂ does NOT trip K10. | **PASS** |

**Counts:** 6/6 PASS, 0 FAIL.

## Headline

**The n=3 parity core holds, exact-ℚ, with the type gate biting both ways.** The
even-order Gaussian invariant `K_G = σ₂ = −3/49` is √q-free and exact-ℚ
(corroborated independently across Path B total, the Path B′ det2 shape-operator,
and the Path C oracle, and by `−det(H_b)/q²`); the second even-order anchor
`Ĉ₁ = −24 = −2·det(H_b)` is likewise exact-ℚ. The odd-order `σ₁` carries the
un-squared radical (tr(P H P)=12/7 ≠ 0, so `σ₁ = −(1/√14)(12/7) ∈ ℚ(√14)`, with
`σ₁² = 72/343 ∈ ℚ` but `σ₁ ∉ ℚ` because 14 is a non-square) — and the frozen
oracle correctly WITHHOLDS it as a numeric value. The parity-type gate **K10** is
**silent on truth** (nothing radical-bearing is emitted as exact-ℚ) and **fires
on a constructed mutant** that emits `σ₁` as a `Fraction` (caught by the
exactness witness `m² ≠ 72/343`, which no rational can satisfy). The even/odd
contrast `σ₂ ∈ ℚ` vs `σ₁ ∈ ℚ(√14)` is the parity witness.

## Proposed status move

- **CL-c5 → DEMONSTRATED (n=3 CORE ONLY).** Warrant: parity ⟹ `K_G = σ₂` even ⟹
  exact-ℚ, demonstrated on the frozen keystone F13 parity row (exact ℚ). The
  even/odd type contrast holds (σ₂ ∈ ℚ vs σ₁ ∈ ℚ(√14)); K10 is silent on truth
  and fires on a constructed mutant that emits σ₁ as exact-ℚ. Gated by P1 ∧ P2 ∧
  P3 ∧ P4 ∧ P5 ∧ P6 (all PASS). Verified-finite exact-ℚ parity/type contrast —
  **NOT** a symbolic-over-ℚ[g,H] universal, **NOT** n≥4.
- **`n≥4` tower: NOT established (OPEN; successor c002).** The status move covers
  the core ONLY, not the tower. Do NOT claim the tower.
- **K10 disposition:** ARMED; silent on truth (P5), fires on the mutant (P6).
- **Tier:** eval-tier; **no substrate promotion**; **nothing canonical until Will
  signs off.**

## Defect-chain count

**NONE (0).** All gates (prereg-pin, clause-drift, bench-pin) passed as-shipped
and bite a tampered contract (proven by the suite's gate tests). All 6
predictions PASS; no prediction FAIL; no HALT triggered. Records byte-stable.

## Will's desk

- **What you're being asked to accept:** move **CL-c5** from `NOT_YET_PROBED` to
  **DEMONSTRATED for the n=3 core only** (parity ⟹ `K_G = σ₂` even ⟹ exact-ℚ),
  with **K10 armed** and exercised both ways. The `n≥4` tower stays explicitly
  **NOT established** (successor c002).
- **One surfaced finding (NOT a defect):** this worktree branches from the
  **pre-bench base**, so the frozen bench is absent under the worktree-relative
  `src/`. Per the launch instruction, the battery resolves `BENCH_DIR` by trying
  the `__file__`-relative path first (correct after the merge-packager places
  this stage on `main`, matching Stage A's relocatable pattern) and falling back
  to the **stable main checkout** `/home/wlloyd/Lloyd_Engine_V4/src/lloyd_v4/
  evals/three_channel_kg` named in the launch block. No ephemeral worktree path
  is baked in; the `depends_on` sha256 gate re-verifies the resolved bench
  content-for-content against the frozen pins, and records content is
  path-independent (records sha unchanged either way). For this run the bench
  resolved to the stable main checkout. This is a campaign-mechanics note, not a
  science finding — flag it so the merge-packager confirms the `__file__`-relative
  branch activates post-merge on `main`.
- **No other halts, no other cross-stage dependencies, no frozen-spec
  contradictions.** Wrote only inside `results/three_channel_kg/stage_e/`.
