# c2 Theorem Scope Gate Audit — Closeout

Date: 2026-05-18.
Code: [`../../../scratch/c2_theorem_scope_gate.py`](../../../scratch/c2_theorem_scope_gate.py).
Artifact: [`artifact.json`](artifact.json).

## 1. Purpose

The Conjecture C proof audit ([`../conjecture_c_proof_audit/closeout.md`](../conjecture_c_proof_audit/closeout.md)) established the no-binade-drop property for correctly-rounded sqrt in IEEE 754 binary64 **normal range** (`f_float ≥ 2^(−1021)`). The proof's mechanism is scaling invariance: `RN(x · 2^m) = RN(x) · 2^m` exact in normal range, but structurally broken in subnormal due to gradual underflow.

This audit is the **scope gate**: before the c2 lattice theorem can be promoted from "conditional on C" to "unconditional," verify that actual V4 campaign fixtures keep `f_float ≥ 2^(−1021)`.

The user's critique (2026-05-18) noted that the c2 / fold-readback campaign's scientific target is the deep-cancellation regime — small f, low binades, toward the proved-floor at 2^(−1021). "Normal range" is not parenthetical. Verify-don't-assume.

## 2. Headline verdict

**`GATE_PASSES_actual_fixtures_in_normal_range`.** Every known V4 campaign fixture (14 distinct sweep grids across 4 fixtures × multiple campaign phases) keeps `f_float ≥ 2^(−1021)` with margin **≥ 968 binades**.

| Campaign / fixture | Min f_float (binade) | Margin above 2^(−1021) |
|---|---|---|
| c2 sharpness audit / SR | 2^(−9) | 1012 binades |
| c2 sharpness audit / Schwarzschild | 2^(−11) | 1010 binades |
| c2 sharpness audit / pure_algebraic | 2^(−10) | 1011 binades |
| c2 sharpness audit / cube_root | 2^(−10) | 1011 binades |
| v11 fold-readback densified SR | 2^(−16) | 1005.7 binades |
| Test A (4 fixtures, Sterbenz region) | 2^(−1) | 1020 binades |
| Hypothetical deep SR near β=1 (1 − 2^(−e), e ∈ [1, 52]) | 2^(−51) | 970 binades |

Theoretical minima per fixture (limited by float64 precision near 1):

| Fixture | Theoretical min f_float | Margin |
|---|---|---|
| SR | 2^(−52) | 969 binades |
| Schwarzschild | 2^(−53) | 968 binades |
| pure_algebraic | 2^(−52) | 969 binades |
| cube_root | 2^(−52) | 969 binades |

**The minimum any current fixture can reach** (limited by `ulp(1) = 2^(−52)` for f = `1 − x_term`) is **~970 binades above the proven floor**. The campaign trajectory cannot reach subnormal without restructuring the fixture algebra.

## 3. Why "normal range" is not parenthetical

The Conjecture C proof's structure (case analysis on parity of k + finite enumeration over normal-range binade boundaries) relies on scaling invariance: `R_above(m) = 0x1.6a09e667f3bcdp+m` is the correctly-rounded sqrt at every odd-k binade boundary, where `0x6a09e667f3bcd` is the fixed mantissa pattern of sqrt(2) and `m` is the exponent. This construction is valid for `m ∈ [−1022, +1023]` (normal range).

In subnormal range, the construction breaks:
- Subnormal floats have a fixed minimum exponent (−1074).
- The significand width decreases as values approach zero (gradual underflow).
- The "shift exponent, preserve significand" property fails.

Therefore the proof of C is **scope-bound**, not "scope-restricted-for-tidiness." The proof's mechanism dies at the subnormal-normal boundary.

The c2 lattice theorem, which uses C as its load-bearing lemma, inherits this scope bound. Stating "(normal range)" as a parenthetical in the theorem head misrepresents this as stylistic. Stating it as an explicit hypothesis with a checked gate is honest.

## 4. The scope gate as methodology discipline

Going forward, **any new fixture, dual-arm probe variant, or substrate-fingerprint slot that uses the c2 routing must pass this gate**:

```
PRECONDITION: min(f_float) >= 2**(-1021) across the fixture's parameter sweep.
ON_VIOLATION: c2 lattice theorem does not apply; verify lattice property
              separately, or prove Conjecture C_subnormal.
```

The reference implementation is [`c2_theorem_scope_gate.py`](../../../scratch/c2_theorem_scope_gate.py). Adding a fixture's grid spec and re-running the gate is a one-line operation.

## 5. What this audit does not cover

- **Conjecture C_subnormal.** The audit identifies that subnormal is the scope boundary, but does not address whether an analog of C holds there. C_subnormal is frozen as a separate open problem.
- **Future fixtures with deeper f.** Compound algebraic operations (e.g., `(1 − x₁) · (1 − x₂)`, chained sqrts) could produce f_float well below 2^(−52). Such fixtures would need re-checking against this gate.
- **Other float formats.** float32, float128, bfloat16 each have their own normal-range floors and would need their own gate.
- **Other rounding modes.** Round-toward-zero, round-toward-infinity, etc. have different scope properties.

## 6. Reproducibility

```
$ PYTHONPATH=src:. python scratch/c2_theorem_scope_gate.py
$ cp Build_Docs/Reports/c2_theorem_scope_gate/artifact.json /tmp/run1.json
$ PYTHONPATH=src:. python scratch/c2_theorem_scope_gate.py
$ diff /tmp/run1.json Build_Docs/Reports/c2_theorem_scope_gate/artifact.json
(empty) — BYTE-IDENTICAL ✓
```

## 7. Honest reflection

The user's three critiques each sharpened the c2 lattice theorem:
1. Amendment I (Sterbenz hypothesis was misstated, n-scope overclaim) → mechanism corrected.
2. Amendment II (C demoted to footnote with quasi-proof language) → conjecture-conditional framing.
3. Amendment III + this gate (scope-bound treated as parenthetical) → explicit-bound theorem with gated promotion.

Each iteration removed one form of over-claim. The result is a theorem that:
- States its scope explicitly in the head, not in a parenthetical.
- Has its scope **verified** by a reproducible audit, not assumed.
- Names what's outside scope (C_subnormal) as a frozen open problem.
- Has a methodology gate that prevents future over-extension.

This is the V4 idiom applied honestly. The drawer's remaining content (C_subnormal) is one item, not two, and it's clearly named.

## 8. References

- Conjecture C proof: [`../conjecture_c_proof_audit/closeout.md`](../conjecture_c_proof_audit/closeout.md)
- c2 lattice sharpness audit (Amendment III): [`../c2_lattice_sharpness_audit/closeout.md`](../c2_lattice_sharpness_audit/closeout.md)
- 2026-05-18 conversation: user-directed scope critique
- IEEE 754 binary64 standard (gradual underflow, subnormal arithmetic)
- Discipline: `CAMPAIGN_DISCIPLINE.md` Rule 1.1
