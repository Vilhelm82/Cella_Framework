# Pre-registration — Exact Forward M⊕C Decomposition (the definitive G-presence test)

**Status:** PRE-REGISTRATION · research-grade · eval-layer only · **retrodiction-gated**. No `src/` or `Architecture/` rules-doc edits. Instruments (`fractions.Fraction`, `mpmath`, `decimal`) are oracles per Axiom 11, never substrate.
**Date:** 2026-06-05.
**Scope (anti-restart):** This is **NOT a new campaign.** It is the intersection of `substrate-invariant-search` (Phase A — the substrate-derived invariant / G question) and `layer-3-promotion` **Gate 2** ("joint-state must reveal a *derivable* law"). It aliases the restart traps "irreducible basis search," "derive the form basis," "decision-law architecture" — file all results under those two campaigns. Do not mint "derive-F5+" or "G-discovery" as a fresh name.
**Origin:** crown jewels J1+J2 from `scratch/CONVERSATION_V4_RND_EXTRACTION_2026-06-05.md`; the reopened G status (TASKS_TO_REVISIT **R9**; HISTORICAL_RECORD HR89/HR121; glossary G-entry — "G is OPEN/untested, not absent"); the killswitch closeout §7.A.2 demand (a legitimate G test must name a positive mechanism *before* testing); and the multi-D lattice-survival lead (`scratch/lifted_sweep_fixed.py`).

---

## 1. Why this exists

The "G empirically absent in 1D" verdict was **retracted 2026-06-05** as an untested null: the Gate-3 killswitch was substrate-dominated by construction (its own §7.A: "no posterior update because there was no prior"), and the geometry-first campaign left all candidates `unresolved_candidate` with the disambiguating phases never run. G was **never given a positive construction or a named mechanism, then "tested."**

This pre-registration supplies exactly what §7.A.2 demanded — a **named mechanism and a positive, floor-free construction** — and turns the G question from an asserted null into a **definitive forward test.**

### The mechanism (J1 + J2)
- **J1 — exact-rational carry (no apparatus floor).** Every float64 intermediate is a dyadic rational, so the exact residual of the *rounded chain* is computable in `Fraction` with **zero apparatus noise** — escaping the float128 floor that made Task A ambiguous (the SR "boundary" was the 80-bit float128 floor: pull float128 and it moved 0.743→0.345).
- **J2 — `e = √f − R` is exactly computable *forward*.** W(k)'s irreversibility is a **backward** statement (residual→preimage is interval-valued). Forward, with `f` in hand, the sqrt round-off `e` is exact to any oracle precision. So the conditioning term **C becomes computed, not floor-estimated.**
- **J1 ⊕ J2 ⇒ an exact forward `M ⊕ C` decomposition of the 1D residual, with no floor to blame.** Subtract M (the BACL integer-ulp lattice, proven) and C (the now-exact round-off chain) exactly; the remainder is **G, with the apparatus excluded by construction.**

---

## 2. Pre-registered hypotheses

- **H0 (null, expected in 1D):** residual ≡ M ⊕ C exactly; G is **hard zero** in 1D. This would convert the retracted "empirically absent" into a *definitive* absence — a real result, not an asserted one.
- **H1 (the prize):** an exact-C subtraction leaves a **non-zero, structured remainder** that the computed conditioning cannot account for — G caught with the apparatus excluded by construction.
- **H2 (multi-D, where G most plausibly lives):** even if H0 holds in 1D, the lifted/multi-constraint fixtures carry fixture-distinguishing lattice structure (`lifted_sweep_fixed.py`: Morris-Thorne j_var 0.4907 vs photon-sphere 0.4117) that is **not** reducible to single-operand M⊕C — a candidate multi-D G.

Pre-registering H0 as the *expected* outcome is deliberate: it makes H1/H2 falsifiable and stops a null from being re-spun as a finding (the Obs-2 / R9 failure mode).

---

## 3. Verified inputs (measured 2026-06-05, before this spec)

- **Subnormal-sqrt round-trip is exact** (HR121): `sqrt(f)²==f`, j=0 across 35k+ exact-rational samples — the cleanest instance of "M is the fixed-grid residual." Calibration anchor.
- **F1 and F2 share a bit-identical R²** in **137/137 cells, all three fixtures** (Schw/SR/PA): the sqrt round-off `2R·e` is genuinely **common-mode** between F1 and F2. *Load-bearing premise of the common-mode-rejection step — CONFIRMED.*
- **Common-mode rejection is first-order, not bit-exact:** F1−F2 stays invariant under a 1-ulp R² perturbation in only **103/137 (Schw), 96/137 (SR), 69/137 (PA)** — F1 (one subtraction) and F2 (two) round their final assembly differently, so a **second-order rounding-asymmetry term survives** the cancellation. Account for it; do not assume bit-exact carrier removal.
- **F4 is only a *partially* independent channel:** its alt-route operand is bit-identical to the direct operand in ~60–67% of cells; it carries a genuinely different √-fractional part only in the **~33–40%** where the routing diverges. Treat F4 as cell-conditionally independent, not a global third light (consistent with HR95 F1≡F4 at signature level + the F4 stressor activation rates).

---

## 4. Experiment 1 — 1D exact forward M⊕C decomposition (definitive G-presence test)

For each fixture (Schwarzschild, SR, pure_algebraic, cbrt) over its canonical 137-pt grid, **carry everything in exact `Fraction`** (no float128 anywhere):

1. Compute the float64 chain faithfully (`R = round(√f)`, the form's rounded intermediates) — every value is dyadic, captured exactly.
2. **M:** the BACL integer-ulp lattice value `j·ulp(f)` (proven; c2 for the rounded residual).
3. **C:** the exact round-off chain — `e = √f − R` (oracle-exact) propagated forward through the form's operations as exact rationals (the squaring round-off `fl(R²) − R²`, the combination round-offs). This is the **computed** conditioning, no floor.
4. **G := residual − M − C**, computed exactly.
5. Read G across the grid.

**Pass/interpretation:** G ≡ 0 exactly ⇒ H0 confirmed *definitively* (1D residual is exactly M⊕C). G ≠ 0 with structure not attributable to the computed C ⇒ H1, flag immediately and do not over-claim — characterise before naming.

### 4a. The common-mode-rejected (dark-field) variant — run G at high contrast

**Verified 2026-06-05:** differencing F1−F2 cancels the shared bulk (bit-identical R², the `2R·e` sqrt round-off, the geometry) and leaves a **differential path-conditioning signal that is deterministic, BACL-quantized to ±1 ulp, and concentrated at the Sterbenz boundary** (Schwarzschild: 18/18 nonzero-leak cells in the near-boundary half, 0 in the far half; PA: 21 near / 15 far). This "leakage" is **not a defect of the common-mode rejection — it is the form's per-cell conditioning fingerprint** (a strictly finer discriminator than the coarse grain), and it is **C-channel, not G** (deterministic, magnitude/boundary-driven, derivable from `f`).

**Why it sharpens the G test:** F1−F2 is a **dark-field aperture** — it suppresses the bright shared signal so any faint structure shows at high contrast. So run the exact forward M⊕C decomposition (§4) **on the common-mode-rejected pair**, not only the raw residual: subtract the exactly-computed C from the ±1-ulp dark-field comb.
- Leakage → 0 under exact-C subtraction ⇒ it was pure conditioning; bank the per-cell fingerprint as a finer form-discriminator (feeds the derive-don't-select / F5+ retrodiction).
- A sub-leakage remainder survives ⇒ **G candidate, now against a dark background instead of buried under the shared bulk** — the highest-contrast G probe available in 1D.

Honest expectation: the leakage is most likely exactly C (it looks like pure Sterbenz-region conditioning — ±1 ulp, boundary-concentrated), so exact-C subtraction zeros it. That outcome is still a win: a clean, legible, BACL-quantized conditioning observable per form.

## 5. Retrodiction gate (HARD precondition — runs BEFORE any G claim)

Per the curvature-pivot mandate (never built; R3) and the derive-don't-select discipline: the decomposition must **reproduce the known forms at their known grains in burden-order before it is allowed to name anything.**
- F2 lands on its half-integer grain; F4 on integer; F3 ≡ 0 (calibration zero / the F=0 origin of the form coordinate); F1∥F2 polarity preserved.
- The exact-C subtraction must reproduce Task 017c's regular-region behaviour where it overlaps.
- **If the known forms do not land where Task 031's burden ranking says they should, the instrument is wrong — stop, do not hunt G.**

> **F2 boundary sub-result (J1 standalone, worth banking even if G is null):** run the F2 Sterbenz-region `b_k` pass in exact rationals instead of float128. This **settles the open Q5/F2 real-vs-apparatus question** — the one the whole record keeps converging on — because exact carry leaves no floor to blame. Likely outcome: the "boundary"/"resonance bump" is apparatus (matching Task A), now provable.

## 6. Experiment 2 — multi-D extension (where G most plausibly lives)

Only after Exp 1 + retrodiction gate pass. Extend the exact forward M⊕C decomposition to the **lifted/multi-constraint fixtures** (`lifted_sweep_fixed.py`, corrected from the `analyze_lifted` bug that froze the physical coords). Target: is the fixture-distinguishing lattice structure (MT 0.4907 vs photon 0.4117) reducible to per-constraint M⊕C, or is there an irreducible joint-state remainder? A joint-state remainder that survives exact M⊕C subtraction **is** the Gate-2 "derivable joint-state law" — the actual prize.

---

## 7. Discipline guards (carry verbatim)

- **Type `⊕` and `= 0`:** membership on the surface is `identity_zero` — a **symbolic / by-construction** identity check, **never** a numerical tolerance. A below-LoD near-identity admitted as membership is a false type-sticker (Axiom 9) and would **manufacture phantom forms.** Membership is non-discriminating; all signal lives in the residual coordinate `F` (with F3 at the F=0 origin).
- **1-D "curvature" is M+C, NOT K_G.** One operand chain is 1-D; do not write the decomposition's bend as Gaussian curvature — that conflation is the §9 four-layer-separation breach. Genuine geometric K_G, if it exists, needs multi-D (Exp 2).
- **`e` adds no independent information** — it is exact *attribution* of conditioning derived from `f`, not a new channel and not sub-ulp recovery. Forward only; inversion re-incurs W(k).
- **Same-form (rounded, de-rounded) pairs cannot reconstruct below the floor** (one measurement, two resolutions) — do not re-pitch as redundancy. Real redundancy needs operand/path separation (dual-arm condition 4 / different forms).
- **Byte-stable artifacts; cite, don't re-derive** BACL / c2 / Conjecture C / W(k) / HR95 / Task 017c / Task 031.

## 8. Honest limits

H1 is the low-probability branch; H0 is expected and is itself the deliverable (a *definitive* 1D absence replaces an asserted one). `e` is a deterministic but erratic ½-ulp sawtooth — exact pointwise, not a smooth model. The whole construction is forward; nothing here inverts W(k). The most likely high-value outcome is the **F2 boundary settled (Q5)** plus a **definitive 1D G-absence**, with the live G hunt then concentrated in Exp 2 (multi-D), exactly where the record always suspected G would have to live.
