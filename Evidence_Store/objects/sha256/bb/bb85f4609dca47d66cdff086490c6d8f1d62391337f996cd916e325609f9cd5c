# Conjecture C — Subnormal Cube Root (n=3) — Closeout

**Date promoted:** 2026-06-05 (work 2026-05-30/31). **Status:** PARTIAL — qualified bound, eval-layer, research-grade. Companion to the n=2 sqrt close (HR121). Promoted from `scratch/Phase2B_Subnormal_Cbrt_Combinatorics_Proof.md` + `phase2B_adversarial_verify.py`.

## Statement

For binary64 **subnormal** `f`, the cube-root round-trip residual `V − f` (with `R = cbrt(f)`, `V = R*R*R`) lies on the fixed subnormal lattice `2⁻¹⁰⁷⁴` — it is an **integer multiple `j·2⁻¹⁰⁷⁴`** — but, unlike sqrt(n=2) which pins `j = 0`, the cbrt set is **bounded but non-trivial and implementation-dependent**:

> Under numpy `cbrt` + float64 cubing: residual `j ∈ {−4,…,+1}` for ~**98.7%** of large subnormal samples (dense 5.5M run), with documented rare excursions to `{−7,…,+3}`. Under a correctly-rounded cbrt the set tightens toward `{−1,0,+1}`.

## Verification (2026-06-05, this promotion)

Re-ran the adversarial verifier (`phase2B_adversarial_verify.py`, boundary-dense + binary-halving sample of 64 mantissas):
- **n=3 cbrt: all_on_lattice = True**, distinct `j ∈ {−4,−3,−2,−1,0,1}`.
- **numpy.cbrt vs mpmath correctly-rounded cbrt diverge in 27/64 samples** (≤1 ulp on R) — yet the round-trip residual still lands on the `2⁻¹⁰⁷⁴` lattice. **Residual-integrality ≠ correct-rounding of R.**
- Contrast (same run): n=2 sqrt is `j ∈ {0}` exactly (HR121).

## Reading

- **The lattice survives into subnormal cbrt (the BACL integer-ulp mechanism, HR73), but the Conjecture-C *scaling* mechanism does not** — once spacing stops being magnitude-proportional, the residual is a *bounded small-integer* lattice, not pinned to 0.
- The dividing line from the sqrt close is the **IEEE correctly-rounded mandate**: sqrt has it (→ j=0, clean); cbrt does not (→ j wanders on the same lattice, impl-dependent). This is the same mandate-vs-no-mandate boundary documented in HR121.

## Scope / caveats

- **Qualified bound only** — numpy-implementation-dependent; not a clean closed theorem. Cite HR73 (BACL subnormal) as the proven parent; this *extends* it to the cbrt round-trip residual, it does not re-prove it.
- C_subnormal for **n=2 is CLOSED** (HR121); **n≥3 remains qualified/open** (this result); C_3/C_4/C_5 (the original frozen-open set) untouched.
- No regression test yet (the n=2 sqrt has one: `tests/test_conjecture_c_subnormal_sqrt.py`); a cbrt test would have to pin the numpy-version dependence.
