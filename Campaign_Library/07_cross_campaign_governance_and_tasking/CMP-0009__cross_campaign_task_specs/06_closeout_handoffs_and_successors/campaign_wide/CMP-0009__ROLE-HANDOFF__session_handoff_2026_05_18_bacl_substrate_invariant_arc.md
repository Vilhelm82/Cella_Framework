# Session Handoff — 2026-05-18

Long session. Major arc: V4 produces a named substrate-level geometric invariant of IEEE 754 (BACL), proven from first principles, with the c2 lattice theorem and other V4 lattice-based results as derived corollaries. Plus: hardened dual-arm probe, four-phase fingerprint-atlas / barcode investigation, V3-reference blowup-exponent audit.

## Headline findings (calibrated)

### Proven results

1. **BACL (Binade-Aligned Cancellation Lattice)** — substrate-level geometric invariant of IEEE 754 binary floating-point.
   - **Statement**: For `a, b ∈ 𝔽⁺` in any IEEE 754 binary format, if `ulp(a) ≥ ulp(b)`, then `a − b = j · ulp(b)` for some integer `j ∈ ℤ`.
   - **Proof**: 5 lines from binade-spacing axioms; no Sterbenz, no scaling invariance, no rounding-mode hypothesis.
   - **Verified at**: float16, float32, float64 (normal + subnormal each); ≈ 31,000 empirical records, zero violations.
   - **Sharpness**: empirically demonstrated; ~96–98% of `ulp(a) < ulp(b)` pairs produce non-integer differences.
   - **Novelty status**: folklore-likely; named explicitly and proven as a standalone V4 substrate primitive. Web-search literature audit deferred.

2. **Conjecture C** — proven for IEEE 754 binary64 normal range.
   - **Statement**: For `f ∈ float64` in binade `[2^k, 2^(k+1))` (normal range), if `R = round-to-nearest-even(sqrt(f))`, then `round-to-nearest-even(R · R) ≥ 2^k`.
   - **Proof**: case analysis (even/odd k) + finite enumeration over 2,044 normal-range binade boundaries + monotonicity argument for in-binade extension.
   - **Verified**: 220,444 empirical checks; zero counterexamples.
   - **Mechanism**: scaling invariance (`RN(x · 2^m) = RN(x) · 2^m`). **Breaks in subnormal.** C_subnormal remains an open problem requiring different machinery (gradual-underflow arithmetic).

3. **c2 lattice theorem** — unconditional within explicit scope.
   - **Statement**: For `f_float = round(1 − x_term)` in IEEE 754 binary64 with **`f_float ≥ 2^(−1021)`**, if `R = round(sqrt(f_float))` and `V_2 = round(R · R)`, then `c2 = round(V_2 + round(x_term − 1)) = j · ulp(f_float)` for integer `j ∈ ℤ`.
   - **Derivation**: 3-line corollary of BACL + Conjecture C.
   - **Verified**: 90,000 empirical records (full range sweep, c1 foil, float32 generalization, n=4,5 quartic/quintic, perturbed-window robustness test) — zero violations.
   - **Scope bound**: `f_float ≥ 2^(−1021)` comes from Conjecture C, not from BACL. Scope gate audit verified all known V4 fixtures keep ≥ 970 binades of margin above the floor.

### Methodology contributions

4. **Fingerprint-atlas / barcode framing** — 4 phases (α, β, γ, δ).
   - **Phase α**: hypothesis test — bimodal slot coverage exposed (F2 aliasing fired).
   - **Phase β**: cross-family aliasing fixed — slot 13 universal added; 15/15 pairs distinguishable.
   - **Phase γ**: stress-test under probe-point perturbation; smoothness preserved.
   - **Phase δ**: barcode-scan use case **validated** — distance 0.0 between canonical SR and perturbed-window SR; cheap 6-slot fingerprint uniquely identifies all 6 fixtures.

5. **Hardened dual-arm probe (V1)** — 6 operational conditions enforced as code, not just doc.
   - 15/15 tests pass; F2 wide / F4 microscope SR fixture produces 16 `gap_resolved` records.
   - Construction-time gates: route-kind allow-list, activation-rule, selection-rule, frozen dataclass, same-channel opt-in, ARM-N validity-predicate signature inspection.

6. **Blowup-exponent V4-native audit** (V3 reproduction) — σ1 = 1.000 universally across 15 simple zeros of ζ, J₀, Ai.
   - Linearization-order signature is structurally universal (calculus invariant).
   - V3's specific K_G result not directly reproducible without using V3's substrate; V4-native signatures showed universality at linearization depth.

## The substrate invariant arc — chronological

A multi-iteration cycle that produced the strongest V4 result yet, through five external-review iterations:

### Iteration 1 — c2 substrate derivation ([`c2_lattice_substrate_derivation/`](../Lloyd_Engine_V4/Build_Docs/Reports/c2_lattice_substrate_derivation/))

Goal: explain Test A's empirical observation (c2 is integer-lattice) from IEEE 754 axioms. Produced a 6-line proof with universality theorem confirmed across 24,995 measurements (4 fixtures × 5000 grid pts). **Verdict: succeeded.** Discovered route-dependence finding (np.cbrt vs `** (1/3)` produce different lattice ranks for n=3).

### Iteration 2 — Sharpness audit ([`c2_lattice_sharpness_audit/`](../Lloyd_Engine_V4/Build_Docs/Reports/c2_lattice_sharpness_audit/))

Goal: test where the theorem's hypothesis is necessary. Discovered the original Sterbenz-based hypothesis was **wrong** (proof-error) — empirically c2 was integer-lattice across the full natural range, not just the formal Sterbenz region for `x_term − 1`. **90,000 records, 0 violations.**

**External critique (Amendment II)** identified: my Line 5 of the proof was too strong as stated. The proviso `V_n ∈ [f_float/2, 2·f_float]` admits lower-adjacent-binade V_n which produces half-integer lattice generically. Empirical check via adversarial R confirmed half-integer lattice IS reachable when V_n drops to lower binade. Theorem became conjecture-conditional on **Conjecture C**: round(R·R) ≥ floor_binade(f) for correctly-rounded sqrt.

### Iteration 3 — Conjecture C proof ([`conjecture_c_proof_audit/`](../Lloyd_Engine_V4/Build_Docs/Reports/conjecture_c_proof_audit/))

Dedicated audit: case analysis (k even / k odd) + finite enumeration over 1,022 + 1,022 = 2,044 normal-range binade boundaries + monotonicity argument for in-binade extension. **220,444 records; verdict: C_proven.** The empirical step (correctly-rounded sqrt picks the upper neighbor at every odd-k binade boundary) is verified by exhaustive enumeration over a finite domain → constitutes proof.

### Iteration 4 — Scope critique and Amendment III ([`c2_theorem_scope_gate/`](../Lloyd_Engine_V4/Build_Docs/Reports/c2_theorem_scope_gate/))

**External critique**: "(normal range)" caveat in the promoted theorem is load-bearing, not parenthetical. The proof's mechanism (scaling invariance) dies in subnormal. The campaign's natural trajectory (deep cancellation) points at this floor. Before any promotion to unconditional: verify actual fixtures stay above `2^(−1021)`.

Scope gate audit: 14 campaign grids × actual sweeps; all stay ≥ 968 binades above the proven floor. The fixtures' algebraic structure (`f = 1 − x_term` with `x_term ∈ [0, 1)`) inherently bounds `f ≥ ulp(1) = 2^(−52)`, so reaching subnormal would require restructuring the fixture algebra. **Theorem promoted to unconditional with explicit `f_float ≥ 2^(−1021)` bound in the head, not in parentheses.** C_subnormal frozen as open.

### Iteration 5 — BACL extraction ([`bacl_invariant_audit/`](../Lloyd_Engine_V4/Build_Docs/Reports/bacl_invariant_audit/))

**User direction**: extract the geometric content as a property of float pairs, independent of any algebraic chain. Result:

> **BACL**: for `a, b ∈ 𝔽⁺` with `ulp(a) ≥ ulp(b)`, `a − b = j · ulp(b)` for integer j.

Proof reduces to 5 lines using only binade-spacing axioms. The c2 theorem becomes a **3-line corollary** of BACL applied to `(V_2, f_float)` under Conjecture C. Verified across 7 algebraic chains × 2 formats = 7,000 records. **Folklore-likely; named explicitly as V4 substrate primitive.**

### Iteration 6 — BACL_subnormal ([`bacl_subnormal_audit/`](../Lloyd_Engine_V4/Build_Docs/Reports/bacl_subnormal_audit/))

**User direction**: investigate subnormal analog. Discovered BACL extends to subnormal **natively** when the hypothesis is restated as `ulp(a) ≥ ulp(b)` instead of `floor_binade(a) ≥ floor_binade(b)`. The proof's mechanism (binade spacing) extends to subnormal — only Conjecture C's mechanism (scaling invariance) genuinely dies there. **8,000 records; 0 violations; sharpness 97.8%.**

### Iteration 7 — Multi-format extension ([`bacl_multi_format_audit/`](../Lloyd_Engine_V4/Build_Docs/Reports/bacl_multi_format_audit/))

BACL verified at float16 and float32 with identical proof structure. **16,000 records; 0 violations.** float128 (x86 80-bit extended on this platform) deferred — its subnormal range `2^(−16445)` underflows in float64-based exact-rational checks.

## Cumulative results table

| Result | Scope | Records | Violations |
|---|---|---|---|
| c2 lattice theorem (n=2, normal range) | f_float ≥ 2^(−1021), float64 | 90,000 | 0 |
| Conjecture C | float64 normal range | 220,444 | 0 |
| Scope gate (campaign fixtures) | 14 campaign grids | per-grid min f tracked | gate passes; ≥ 968 binades margin |
| BACL (original, normal range) | 7 algebraic chains × 2 formats | 7,000 | 0 |
| BACL_subnormal (extended) | 4 pair classes × float64 normal+sub | 8,000 | 0 |
| BACL multi-format | float16, float32 × 4 classes | 16,000 | 0 |
| Fingerprint atlas Phase δ (barcode validation) | 6 fixtures, 1 perturbed-window probe | distance 0.0 exact | — |
| Hardened dual-arm V1 | 10 specified tests + 5 bonus | 15 tests + 1 SR-fixture run | 0 |
| Blowup-exponent V4-native | 3 functions × 5 zeros × 5 signatures × 3 precisions | 225 fits | σ1 = 1.000 ± 0.000 universal |

## The mechanism contrast (substantive lesson)

Two theorems on float lattice structure with very different scope properties depending on proof mechanism:

| Theorem | Proof mechanism | Subnormal behavior | Format-agnostic? |
|---|---|---|---|
| **Conjecture C** | Scaling invariance (`R_above(m) = mantissa_pattern · 2^m` for fixed pattern, varying m) | **Breaks** — subnormals have fixed minimum exponent; construction fails | Format-specific (each format has different mantissa of sqrt(2)) |
| **BACL** | Binade spacing (every float is `N · ulp` for integer N) | **Holds** — subnormals are `N · 2^(emin − precision + 1)` for integer N | Format-agnostic — only ulp value changes |

**Pattern recorded**: when freezing a sub-result as "open," explicitly identify which mechanism dies under hypothesis violation. If no specific mechanism is named, the freeze may be over-conservative — as the original "BACL_subnormal frozen as open" was.

## The methodology iteration arc

| Iter | What was claimed | What was wrong | Fix |
|---|---|---|---|
| 1 | Test A: c2 is integer-lattice | nothing wrong (empirical observation) | proceed to derive |
| 2 | Substrate derivation: theorem with Sterbenz hypothesis | hypothesis was misstated (proof line had wrong condition) | drop Sterbenz from proof |
| 3 | Sharpness: theorem extends to full natural range, all n, all formats | proof's Line 5 too strong; admits lower-adjacent-binade producing half-integer | conjecture-conditional headline; freeze C |
| 4 | Conjecture C audit: theorem unconditional | "(normal range)" parenthetical was load-bearing | scope gate; explicit bound in head; freeze C_subnormal |
| 5 | Amendment III: theorem unconditional within scope | result is algebraic-chain-specific | extract BACL as geometric invariant |
| 6 | BACL audit: normal range only; BACL_subnormal frozen as open | over-cautious freeze; mechanism doesn't actually break | unified hypothesis covers normal + subnormal |
| 7 | BACL_subnormal investigation: extends natively | multi-format extension still pending | float16 + float32 verified; float128 deferred |

Each step removed an over-claim and named what was actually proven. The result is a calibrated substrate primitive with verified scope at the format and range level.

## Files / artifact reference

### Reports created this session

| Directory | Status |
|---|---|
| `Build_Docs/Reports/substrate_fingerprint_atlas/` | Phase α — preregistry + closeout + artifact |
| `Build_Docs/Reports/substrate_fingerprint_atlas_phase_beta/` | Phase β — same + amendment |
| `Build_Docs/Reports/substrate_fingerprint_atlas_phase_gamma/` | Phase γ |
| `Build_Docs/Reports/substrate_fingerprint_atlas_phase_delta/` | Phase δ — barcode validated |
| `Build_Docs/Reports/hardened_dual_arm_probe/` | V1 — 15/15 tests, 16 resolved records |
| `Build_Docs/Reports/blowup_exponent_v4_audit/` | σ1 = 1.000 universal across 15 zeros |
| `Build_Docs/Reports/c2_lattice_substrate_derivation/` | First c2 theorem attempt |
| `Build_Docs/Reports/c2_lattice_sharpness_audit/` | + Amendments I, II, III |
| `Build_Docs/Reports/conjecture_c_proof_audit/` | C proven for float64 normal range |
| `Build_Docs/Reports/c2_theorem_scope_gate/` | Campaign fixtures verified above floor |
| `Build_Docs/Reports/bacl_invariant_audit/` | + Amendment II |
| `Build_Docs/Reports/bacl_subnormal_audit/` | BACL extends to subnormal |
| `Build_Docs/Reports/bacl_multi_format_audit/` | BACL at float16, float32 |

### Code created this session

| Path | Purpose |
|---|---|
| `scratch/hardened_dual_arm_probe.py` | Dual-arm probe with 6 conditions enforced |
| `tests/test_hardened_dual_arm_probe.py` | 15 tests; all pass |
| `scratch/substrate_fingerprint_atlas.py` | Phase α |
| `scratch/substrate_fingerprint_atlas_phase_beta.py` | Phase β |
| `scratch/substrate_fingerprint_atlas_phase_gamma.py` | Phase γ |
| `scratch/substrate_fingerprint_atlas_phase_delta.py` | Phase δ |
| `scratch/blowup_exponent_v4_audit.py` | V3 reproduction; σ1 = 1.000 finding |
| `scratch/c2_lattice_substrate_derivation.py` | First c2 theorem run |
| `scratch/c2_lattice_sharpness_audit.py` | 90,000-record full-range sweep |
| `scratch/c2_lattice_binade_danger_zone.py` | 58,000-record danger-zone probe |
| `scratch/conjecture_c_proof_audit.py` | C proof + 220,444-record verification |
| `scratch/c2_theorem_scope_gate.py` | Campaign-fixtures-vs-proven-floor gate |
| `scratch/bacl_invariant_audit.py` | BACL across 7 chains × 2 formats |
| `scratch/bacl_subnormal_audit.py` | BACL subnormal verification with exact rationals |
| `scratch/bacl_multi_format_audit.py` | float16 + float32 verification |

### Documents not modified

All `Lloyd_Engine_V4/Build_Docs/Architecture/` axiom/principles documents remain as is. The BACL substrate-lemma integration into `Build_Docs/Architecture/` is logged Phase next.

## Open problems / Phase next

Ordered by priority:

1. **Web-search literature audit on BACL.** Confirm or refute the "folklore-likely" novelty assessment via focused web search.
2. **Substrate-lemma integration**: add BACL as a named lemma in `Build_Docs/Architecture/` cited by the c2 lattice theorem, fingerprint atlas slot 16, dual-arm probe principles.
3. **Conjecture C_subnormal** — if/when a future fixture's algebra produces `f_float < 2^(−1021)`. Different mechanism required (gradual-underflow arithmetic).
4. **float128 BACL verification** with proper float128-aware exact arithmetic (mpmath or custom bit-pattern extraction).
5. **BACL under non-RN rounding modes** — first part (real-difference lattice) is mode-independent; second part (float result = exact) is mode-dependent.
6. **Decimal IEEE 754 BACL analog** — different ulp structure; separate theorem.
7. **Lean / Coq formalization** of BACL — 5-line proof; tractable in either system. Deferred at user direction this session.
8. **Methodology paper draft** — V4 typed substrate + structural-vs-empirical separation + pre-registration + dual-arm + AI cross-validation + BACL as the named substrate primitive worth recording.
9. **Phase 3B (α−1) negative-space mapping** — still parked; control-silence quirk + per-fixture discrimination remain prerequisites.
10. **Other V3 reproductions** — Kerr extremal limit (Investigation 2), Kerr equatorial photon 4D, additional V3 Domain_tests beyond what's been done.
11. **Fingerprint atlas Phase ε** — slot 16 redesign for orthogonality with slot 13; more cross-family slots; near-miss tests on every fixture; cheap-slot prediction modeling.
12. **Dual-arm probe extensions** — apply hardened probe to non-SR fixtures (Schwarzschild, cube_root) once dual-arm channels are defined for them.

## Where V4 sits after this arc

Before this session, V4 had:
- Strong empirical/eval-layer infrastructure (typed substrate, byte-stable artifacts, pre-registration discipline)
- A scattered set of observations (sub-lattice alignment, null-tangent alignment, observability rule, etc.)
- Multiple "candidate-novel" findings without formal substrate-derivation backing

After this session, V4 has:
- **A named geometric invariant of IEEE 754** (BACL) — proven from axioms, verified empirically at 3 precisions × normal+subnormal
- **A proven theorem with explicit scope** (c2 lattice, n=2, float64 normal range f ≥ 2^(−1021)) deriving from BACL + Conjecture C
- **An empirically-validated barcode framing** (fingerprint atlas Phase δ — perturbed-SR matches canonical SR at distance 0.0)
- **A hardened dual-arm probe** with the 6 operational conditions enforced as code
- **An explicit methodology arc** showing seven iterations of over-claim → correction → calibrated result
- **A clear separation** between proven substrate primitives, observed empirical signatures, and frozen open problems

The "noise as fingerprint" / "turbulence-as-diagnostic" framing from the earlier session now has a substrate-level foundation: BACL is the mechanism by which V4's lattice-based measurements (fingerprint slots, dual-arm path separation, c2 vs c1 contrast) acquire their integer-lattice structure.

## Calibrated novelty assessment

| Claim | V4 contribution | Likely literature status |
|---|---|---|
| BACL (the property itself) | Explicit statement + proof + multi-format verification + named primitive | **Folklore-likely**, not formally named at this level. Phase next literature audit. |
| BACL used as a substrate primitive for multiple V4 results | Original contribution | Original |
| c2 vs c1 routing distinction producing integer vs sub-lattice | Original framing as a substrate signature | The arithmetic is in the literature; the framing as a fixture-discriminating signature is V4's |
| Sub-lattice alignment universality across 4 fixtures (paper Observation 2 from earlier session) | Cross-fixture universality | MISS at medium-high confidence per prior literature audit |
| Null-tangent alignment |cos θ| = 1.0000 across 18 cases | Striking universal | E2 literature audit pending |
| Barcode framing — finite-precision residual as fixture fingerprint | V4 methodological inversion | Mirrors turbulence-as-diagnostic pattern; specific application to IEEE 754 substrate is novel framing |

## Methodology lessons recorded (for future use)

1. **Parentheticals in theorem statements deserve scrutiny by default.** If the parenthetical names a hypothesis the proof's mechanism depends on, it is **not** parenthetical.

2. **When freezing a sub-result as "open," name the specific mechanism that fails under hypothesis violation.** If no specific mechanism is identified, the freeze may be over-conservative.

3. **Pre-registration must be binding pre-measurement.** Multiple iterations this session involved pre-measurement amendments — those are honest if (a) flagged explicitly and (b) made before measurement data is admitted.

4. **Verification by exhaustive enumeration over a finite domain IS proof.** The Conjecture C audit verified an empirical step across 2,044 binade boundaries — this constitutes proof, not just evidence.

5. **Verification by sampling is evidence, not proof.** The original 58k-record BACL sweep was evidence; it became proof only after the case-analysis structure + finite enumeration was added.

6. **External review iterations sharpen results.** Seven iterations on the c2/BACL arc, each removing one form of over-claim. The final result is stronger and more honest than any individual iteration's framing.

7. **Extract the geometric content.** When a result is fixture-specific, ask: what's the underlying lattice property? The c2 theorem (about a specific algebraic chain) reduces to BACL (about float pairs) via this move.

## References

- Previous session handoff: [`session_handoff_2026_05_17_dual_arm_and_lifted_singularity.md`](session_handoff_2026_05_17_dual_arm_and_lifted_singularity.md)
- Test A foundation: [`task032_cross_fixture_refinery_audit/`](../Lloyd_Engine_V4/Build_Docs/Reports/task032_cross_fixture_refinery_audit/)
- Lifted-singularity audit foundation: [`lifted_singularity_v4_audit/`](../Lloyd_Engine_V4/Build_Docs/Reports/lifted_singularity_v4_audit/)
- All reports cited in §"Files / artifact reference" above
- Discipline: `Lloyd_Engine_V4/Build_Docs/CAMPAIGN_DISCIPLINE.md`
- Strategic framing: 2026-05-18 conversation — turbulence-as-diagnostic parallel, barcode hypothesis, BACL as natural geometric invariant
