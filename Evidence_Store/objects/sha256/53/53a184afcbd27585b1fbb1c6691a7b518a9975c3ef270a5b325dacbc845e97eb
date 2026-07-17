# Arm I claim ledger (append-only)

| Claim | Statement | Stage | Status | Evidence |
|---|---|---|---|---|
| CL-I1 | value + ledger == TRUE in Z for the fixed-width ring fragment {add, sub, mul, divmod, shifts} — universal on the battery | A | **NOT_YET_PROBED** | — |
| CL-I2 | UNIFICATION: integer shift-death (residue == 0 iff val2(a) >= k) and HR133 dyadic death (e_q = 0 iff q >= L) are ONE law — the residue dies when dyadic valuation covers the discard window | A | **NOT_YET_PROBED** | — |
| CL-I3 | division-semantics fingerprint law: route readings split across trunc/floor/euclid exactly when a semantics-distinguishing discard occurs; two-sided | B | **NOT_YET_PROBED** | — |
| CL-I4 | the carry-ledger orbit analysis recovers the Hull–Dobell full-period conditions on the pinned LCG set (the theorem as external referee) — the arm's non-triviality bar | C | **NOT_YET_PROBED** | — |
| CL-I5 | seam residues typed and exact: int<->float casts carry rounding/truncation accounts schema-indistinguishable from arithmetic residues | D | **NOT_YET_PROBED** | — |
| CL-I6 | (demo) the fast-inverse-sqrt poster fully accounted per stage | D | **NOT_YET_PROBED** | — |

Scope per Will's ruling 2026-06-12: bitwise UNBOUNDED — anything with an exact account is fair game; the Z/F2 domain seam is a typed record mechanism, not a fence. Kill conditions armed per brief section 7: K-I1 (halt-until-fixed on any closure failure), K-I2 (refute CL-I3), K-I3 (triviality kill: CL-I4 fails => the arm added nothing beyond divmod's restatement; close honestly and say so).

---

**Stage A close (2026-06-12, machine date) — status moves per the frozen
prereg's rules (pin 3c57f579…), graded against the native-ℤ referee and
the imported HR133 instrument:**

| Claim | Status change | Evidence |
|---|---|---|
| CL-I1 | NOT_YET_PROBED → **DEMONSTRATED** | PIA.1 5/5 chains: deviation-fold reconstruction == independent native-ℤ referee exactly, every per-op closure identity holding at every step ∧ PIA.3 every-entry corruption sweeps all-break + both exhibits (FXIA4: value 0 carries nothing, ledger reconstructs 2³²; FXIA3: value == truth coincidentally — 4 nonzero discards cancel in the fold, right-by-cancellation certified lawful) ∧ PIA.4 3/3 typed refusal probes + zero refusals on the lawful battery; `stage_a/prediction_verdicts.json`, records sha `5be68f70…` |
| CL-I2 | NOT_YET_PROBED → **DEMONSTRATED** | PIA.2 19/19: ONE predicate — ν₂(operand) ≥ window_floor — agreed with BOTH instruments on every pinned case: 12/12 integer (shr_w; both sides of the val₂ boundary; negatives) + 7/7 float (HR133's rn, IMPORTED never rebuilt; both sides of every death boundary). **Integer shift-death and float dyadic death are one law: the residue dies when dyadic valuation covers the discard window.** The account was born in float64; this is the first certificate that it was never about floats. |

Defect chains: NONE (clean chain end-to-end; the corruption-granularity
law was an authoring-time test finding, locked by test, pinned battery
unaffected). HR-note question (#6, reserved): CL-I2 certification is
now in hand — whether HR133's row gains the dated unification note is
Will's ruling.

---

**Stage B close (2026-06-12, machine date) — status moves per the frozen
prereg's rules (pin b3b4901d…), graded against the native-ℤ referee:**

| Claim | Status change | Evidence |
|---|---|---|
| CL-I3 | NOT_YET_PROBED → **DEMONSTRATED** | PIB.1 16/16 (pair, semantics) closure rows — q·b + r == a exactly with the per-semantics remainder laws, width-wrap entries closing where the quotient wraps ∧ PIB.2 16/16 the fingerprint law TWO-SIDED: measured pairwise splits == the derived sign-configuration predicates everywhere, zero splits at every exact division (no fingerprint without a distinguishing discard), grid informative on all three comparisons ∧ PIB.3 exhibits: INT_MIN//−1 quotient-WRAP fires with zero semantics fingerprint (wrap is a width event, not a rounding-mode event) + 13//3 discard-without-distinguisher ∧ PIB.4 2/2 typed refusal probes, zero on the lawful battery; `stage_b/prediction_verdicts.json`, records sha `82f69910…`. K-I2 never fired. |

Defect chains: NONE (second consecutive clean chain).

---

**Stage C close (2026-06-12, machine date) — status moves per the frozen
prereg's rules (pin d012925d…), the Hull–Dobell theorem as external
referee:**

| Claim | Status change | Evidence |
|---|---|---|
| CL-I4 | NOT_YET_PROBED → **DEMONSTRATED — THE BAR CLEARED, K-I3 NEVER FIRED** | PIC.1 3/3 orbit ledger exactness (carry fold == closed form a^n·x₀ + c(a^n−1)/(a−1) at all 5 pinned steps incl. n=65536) ∧ PIC.2 3/3 towers == pinned fingerprints, mapping one-to-one onto the three exact Hull–Dobell profiles (full: P_k=2^k everywhere; c1-broken: P₁=1 parity window FROZEN, invariance measured; c3-broken: P₂=2 mod-4 window fails to double) WITH the discrimination clause: both broken LCGs share total period 32768 — the plain period cannot distinguish them, the projection tower can (total period IS divmod restatement; the tower is ledger-window structure) ∧ PIC.3 capped rows honest (MINSTD zero fixed point + typed budget refusal consistent-not-proof; xorshift32 𝔽₂-linearity 10/10 w/ F2 seam typed) ∧ PIC.4 exactly the 2 pinned refusals; `stage_c/prediction_verdicts.json`, records sha `bf12f568…` |

Defect chains: NONE (third consecutive clean chain).

---

**Stage D close (2026-06-12, machine date) — status moves per the frozen
prereg's rules (pin ce838bdc…), exact-ℚ referee:**

| Claim | Status change | Evidence |
|---|---|---|
| CL-I5 | NOT_YET_PROBED → **DEMONSTRATED** | PID.1 11/11 seam rows closing exactly in ℚ (int→f64 incl. the 2⁵³ textures; trunc with the sign law; the SEAM FOLD: 3·start == final + r₃ + r₂ + 3·r₁ — Stage A's fold unchanged across the int/float boundary) ∧ PID.2 24/24 structural checks (cast entries: same common core, same enum, same schema, roundtrip intact) ∧ PID.4 3/3 typed refusal probes; `stage_d/prediction_verdicts.json`, records sha `8b153575…` |
| CL-I6 | NOT_YET_PROBED → **DEMONSTRATED (demo-tier)** | PID.3 5/5 poster inputs: every bit-route stage accounted (1 shifted-out bit + 2 typed bitcasts + 5 exact-ℚ float32 rounding residues per input); ε(y) = y²x−1 exact at y0/y1 == pinned; contraction certified per input by exact comparison; gap from the certified isqrt enclosure == pinned exact ℚ interval; magic±1 profile resolves. Demo-tier per the frozen clause: exhibits the vocabulary, mints no law. |

Defect chains: NONE (fourth consecutive clean chain).

**ALL SIX CLAIM ROWS RESOLVED: CL-I1..I6 DEMONSTRATED (I6 demo-tier).
Stages A–D complete; kill conditions K-I1/K-I2/K-I3 armed throughout,
none ever fired. The arm's close draft follows; canonical writes await
Will's sign-off.**
