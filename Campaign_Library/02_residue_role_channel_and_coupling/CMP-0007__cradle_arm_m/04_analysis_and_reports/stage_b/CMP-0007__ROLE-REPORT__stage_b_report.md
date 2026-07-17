# Arm M Stage B Report — mixed tower + the keystone (CL-M2, CL-M3)

**Date:** 2026-06-12 (machine date). **Authority:** brief §4 Arm M
Stage B + Will's Stage-B GO; checkpoint VERIFIED chat-side (90-ordering
completeness verified analytically: 6!/(2!2!2!)). **Prereg:** FROZEN
pre-emission, pin
`b2d2e61bcd38f9a7032148ac7f55b35a1b2d1789ea8f1e98f2cf4249fd0edd97`.
**Records:** `stage_b/records/stage_b_records.jsonl`, sha256
`e9c40ef4b47ce2da9e45174da23cc0cb546956f3278fbd96c049cc92fb4fe1ce`,
byte-stable ×2 (PMB.5). Suite exit 0.

## Verdicts

| Prediction | Verdict | Result |
|---|---|---|
| PMB.1 tower exactness | **PASS 6/6** | Every lane-certified sample (Stage A's organ composed — reading + D) equals the independent transformed-tree referee exactly; every mixed difference exact in ℚ, anisotropic dyadic steps, n=2 and n=3 scored. |
| PMB.2 the commutator | **PASS 6/6 — K-M2 NEVER FIRED** | 197 distinct axis orderings across the battery, all yielding identical iterated differences — including the full 90-ordering trivariate (2,2,2) sets. The lane-side difference calculus commutes exactly. |
| PMB.3 the keystone | **PASS 6/6** | The Newton tensor inversion recovered the full coefficient tensor — every mixed partial at the base point, exactly in ℚ, no error term — verified by step-invariance (a second ladder, identical tensor), the dual-eval first-order slice, and entry-for-entry hand-pins. HR134's univariate Taylor recovery, lifted whole to tensors. |
| PMB.4 termination | **PASS 7/7** | Super-degree differences vanish identically on every polynomial; at-degree entries nonzero; the rational contrast does NOT terminate — the certificate withholds correctly at the class boundary. |
| PMB.5 determinism | **PASS** | byte-stable ×2, sha `e9c40ef4…`. |

## What the stage establishes

The difference calculus gains direction and loses nothing: mixed
differences over certified samples are exact, commute exactly (the
lattice Clairaut, measured 197 ways), terminate exactly at total
degree, and invert exactly — **derivatives of all orders, in all
variables, recovered from lattice samples with no error term**, on
two and three variables alike. The thesis's calculus clause is now
demonstrated on every axis it names.

## Status moves (frozen rules)

- **CL-M2 → DEMONSTRATED** (PMB.1 ∧ PMB.2 ∧ PMB.4).
- **CL-M3 → DEMONSTRATED** — the keystone, on schedule.

## Defect chains

None at the battery. One dry-run catch pre-freeze (FXMA2's pinned
super-degree index exceeded its own termination grid; re-pinned),
preserved in the checkpoint record.

## Will's desk

- Stage-B acceptance → **Stage C GO**: the novel-physics stage —
  the RAW commutator / Clairaut defect / plaquettes (CL-M4's
  conditional fingerprint law with derived witness; CL-M5's plaquette
  holonomy + partition), where Stage A's banked fingerprint-preview
  row becomes the law's first exhibit.
- Then Stage D (directional smoothness) and Stage E (landing
  decomposition + the T1 stretch + CL-M9's curvature measurement).
