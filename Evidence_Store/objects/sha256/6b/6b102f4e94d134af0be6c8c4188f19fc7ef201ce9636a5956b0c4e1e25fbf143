# Bigraded Jet — EFT literature map (Phase 0 deliverable)

**Rule (brief, non-goal 6):** thirty years of error-free-transformation literature is
MINED AND CITED, never re-proved. Every identity the υ-lane implementation will use is
mapped here to its source, its exactness preconditions, and what the implementation
does when a precondition fails — **a typed flag, never a wrong zero.** Stage A's tests
recast these theorems (and V4's own BACL/Conjecture-C/c2) as oracles; they do not
re-derive them.

**Platform route (Phase-0 check, 2026-06-10):** Python 3.14.4 exposes `math.fma` and it
is a TRUE fused operation on this host — verified exact against `fractions.Fraction`
for TwoProd, division-residual, and sqrt-residual spot cases. **The FMA route is
adopted**; Dekker splitting (E5) is documented as the fallback and is NOT implemented
unless a platform without fma appears.

---

## E1 — TwoSum (unordered, 6 flops)

- **Statement:** for `a, b ∈ 𝔽`, round-to-nearest: `s = fl(a+b)`; `a' = fl(s−b)`;
  `b' = fl(s−a')`; `δa = fl(a−a')`; `δb = fl(b−b')`; `e = fl(δa+δb)`. Then
  **`a + b = s + e` exactly, with `e ∈ 𝔽`.**
- **Source:** Knuth, *TAOCP* vol. 2 §4.2.2 (Theorem B and exercises); Møller (1965,
  BIT 5) for the original observation. Treated in Ogita–Rump–Oishi 2005 as Algorithm
  3.1 and in Muller et al., *Handbook of Floating-Point Arithmetic* §4.3.
- **Preconditions:** binary FP, round-to-nearest; **no overflow** in `s` or the
  intermediates. Underflow is harmless: if `fl(a+b)` is subnormal the sum is exact
  (Hauser's lemma, E10) and `e = 0`.
- **On failure:** overflow in any intermediate → υ-entry typed `OVERFLOW_FLAGGED`
  (event recorded with op index); never a silent `e = 0`.

## E2 — Fast2Sum (ordered, 3 flops)

- **Statement:** if `exponent(a) ≥ exponent(b)` (sufficient: `|a| ≥ |b|`):
  `s = fl(a+b)`; `e = fl(b − fl(s−a))`; then `a + b = s + e` exactly.
- **Source:** Dekker 1971 (*Numer. Math.* 18, "A floating-point technique for
  extending the available precision"), Theorem 4.2.1-equivalent; Handbook §4.3.1.
- **Preconditions:** the magnitude ordering, radix ≤ 3, RN, no overflow.
- **On failure:** the ordering precondition silently produces a WRONG residue —
  therefore the implementation either branches on `|a| ≥ |b|` or uses E1
  (unordered). Implementation choice recorded at Stage-A manifest freeze; the
  battery includes an ordering-violation case asserting the chosen guard.

## E3 — TwoProd via FMA (2 flops)

- **Statement:** `p = fl(a·b)`; `e = fma(a, b, −p)`; then **`a·b = p + e` exactly**.
- **Source:** Handbook of Floating-Point Arithmetic §4.4 (FMA-based exact
  multiplication); Boldo–Muller (exactness of FMA-computed residuals,
  IEEE Trans. Computers / related papers on fma error terms).
- **Preconditions (CORRECTED — see erratum below):** no overflow in `p`; the
  RESIDUE must be representable: the multiplication error's low bits extend up to
  ~2p binades below the leading bit of `a·b`, so exactness is guaranteed only when
  `e_a + e_b ≥ e_min + p − 1 = −970` (binary64). **Sufficient guard adopted:**
  `|a·b| ≥ 2^-969`. In the band `(2^-1021, 2^-969)` exactness is input-dependent —
  flagged as sufficient-condition-unsatisfied (honest gating).
- **On failure:** `|p| < 2^-969` (or nonfinite p) → υ-entry typed
  `UNDERFLOW_FLAGGED` / `OVERFLOW_FLAGGED`; the lane degrades to BOUNDED
  (RN half-ulp, always true), never claiming exactness.

## E4 — Division residual via FMA

- **Statement:** `q = fl(a/b)`; `r = fma(−q, b, a) = a − q·b` is **exactly
  representable and exactly computed**. The true quotient satisfies
  `a/b = q + r/b` (in ℝ); the *residual* `r` is the exact υ-payload. The normalized
  error term `r/b` is generally NOT a float: carrying it as a value costs one extra
  rounding (second-order error O(u²·|q|)).
- **Source:** classical representability of the division remainder under RN
  (Bohlender et al. lineage; stated and proved in Handbook §4.5 / Boldo–Daumas);
  ORO 2005 §2 for usage.
- **Preconditions (CORRECTED — see erratum below):** `b ≠ 0`; `q` finite; the
  residual's representability needs `e_q + e_b ≥ e_min + p − 1 = −970`, i.e. with
  `q·b ≈ a`: **sufficient guard `|a| ≥ 2^-969`**; the band below is flagged.
- **Implementation note (decided at Stage-A manifest):** the υ-lane carries the
  exact residual pair `(r, b)` — exactness preserved structurally — and any
  scalarized error value `fl(r/b)` is marked once-rounded. Coverage class for the
  pair: `EXACT`; for the scalarization: `BOUNDED`.
- **On failure:** division by zero is already a typed refusal in the ε-algebra
  (membrane law); underflow edge → `UNDERFLOW_FLAGGED`.

## E5 — Veltkamp splitting + Dekker product (FALLBACK ONLY — not implemented)

- **Statement:** split constant `C = 2^27 + 1` (binary64): `x_h = fl(C·x − fl(C·x − x))`,
  `x_l = fl(x − x_h)`, `x = x_h + x_l` exactly with halves of ≤ 26/27 bits; Dekker's
  product then reconstructs `a·b = p + e` exactly in 17 flops.
- **Source:** Dekker 1971; Veltkamp (unpublished, via Dekker); Handbook §4.4.1.
- **Preconditions:** `C·x` must not overflow (`|x| ≤ ~2^969`); product not subnormal.
- **Status:** documented fallback for fma-less platforms; the Phase-0 platform check
  makes it dead code — recorded here so a future port does not re-derive it.

## E6 — Sqrt residual via FMA

- **Statement:** `s = fl(√a)`; `r = fma(−s, s, a) = a − s²` is exactly representable
  and exactly computed; `√a − s ≈ r/(2s)` with one rounding (second-order exact).
- **Source:** Boldo–Muller (exactness of `a − s²` for the RN square root, *IEEE TC*
  2008-era work; Handbook §4.6).
- **Preconditions (CORRECTED — see erratum below):** `a ≥ 0`; the residual
  `a − s²` is representable only when `2·e_s ≥ e_min + p − 1 = −970`, i.e.
  **sufficient guard `a ≥ 2^-969`** (`s² ≈ a`). NOTE: this fails far above the
  subnormal range — `a = 1e-300` (fully normal) violates it: `s²` sits at
  exponent −997 and the true residual needs bits at 2^-1102, below the 2^-1074
  floor.
- **On failure:** flags as in E3/E4. `a = 0` is the ε-algebra's existing
  `sqrt_zero_derivative_pole` kink refusal — υ-lanes inherit the dead-mode.

## E7 — Compensated summation & dot product (Stage-A battery source)

- **Statement & algorithms:** Sum2 / Dot2 (cascaded TwoSum / TwoProd with error
  accumulation): result as accurate as if computed in twice the working precision
  then rounded: `|Sum2(p) − Σp| ≤ u·|Σp| + γ²_{n−1}·Σ|p|` — the cond·u² law.
  **GenDot/GenSum** (their §6) generate ill-conditioned inputs with prescribed
  condition numbers — the frozen Stage-A battery generator (cond spanning ~1e2…1e16,
  deterministic seeds replaced by frozen operand lists per determinism policy).
- **Source:** Ogita, Rump, Oishi 2005, *Accurate Sum and Dot Product*, SIAM J. Sci.
  Comput. 26(6):1955–1988 (Algorithms 4.1 Sum2, 5.3 Dot2; Prop. 4.5 / Thm 5.5
  bounds; §6 generators).
- **Preconditions:** those of E1/E3 per cascade step; bound validity needs `nu < 1`.
- **Stage-A use (A-P3):** lane-built Sum2/Dot2 must reproduce the cited behaviour —
  equal to the 200-bit truth rounded to double wherever `cond·u² ≪ 1`, with the
  measured boundary reported (not asserted).

## E8 — Classical summation error analysis (context the lanes replace)

- **Source:** Higham, *Accuracy and Stability of Numerical Algorithms* 2nd ed.,
  ch. 4 (recursive summation `γ_{n−1}` bounds, ordering effects).
- **Role:** the a-priori BOUNDS the υ-lanes supersede with exact per-evaluation
  accounting; cited for contrast in the Stage-A report, no algorithmic content used.

## E9 — Complex-step derivative (lineage only)

- **Source:** Squire & Trapp 1998, *Using Complex Variables to Estimate Derivatives
  of Real Functions*, SIAM Review 40(1):110–112.
- **Role:** historical cousin — an algebraic ε-channel that evades subtractive
  cancellation; cited for lineage of the "graded infinitesimal lane" idea. No
  algorithmic content used (the ε-algebra is HR131's, already closed).

## E10 — Supporting lemmas

- **Sterbenz 1974:** `a/2 ≤ b ≤ 2a ⇒ fl(a−b)` exact (`e ≡ 0`). Already a V4 glossary
  citizen; defines Stage C's Sterbenz-exact segments (where holonomy must read zero).
- **Hauser's lemma** (Hauser 1996, *ACM TOPLAS* 18(2), and Handbook §4.2): if
  `fl(a+b)` is subnormal, then `a+b` is exact. Closes the addition-underflow corner
  of E1/E2 with no flag needed.

## In-repo precedent (closed-results check)

- `scratch/bacl_invariant_audit.py` chain `C4_twosum_pair` (HR-era BACL audit) used a
  TwoSum-style construction to GENERATE residual pairs, and its closeout already
  noted: *"Error-free transforms (TwoSum, Dekker) use BACL lattice."* That is
  measurement precedent, not machinery: **no EFT implementation exists anywhere in
  the tree** (token sweep 2026-06-10: only the BACL audit generator + spine briefing
  prose). The connection runs the productive direction for Stage A: **BACL,
  Conjecture C and the c2 theorem are V4-proven laws about exactly the residues the
  υ-lanes will carry — they become test oracles (A-P2), not things to re-derive.**


---

## ERRATUM (2026-06-10, Stage-A amendment — the file keeps its own history)

**Original transcription (this file, first commit):** E3/E4/E6 preconditions were
stated as "result not in the subnormal range / `≥ 2^-1021`." **That is the wrong
boundary** — it guards the RESULT's normality, but the theorems' condition guards
the RESIDUE's representability: the error term of a p-bit rounding carries
significant bits up to ~p binades below the result's leading bit, so the true
condition is `e_result ≥ e_min + p − 1 = −970` (binary64), conservative guard
`2^-969`.

**What caught it:** the frozen Stage-A identity battery (A-P1 FAIL, 2/68 cases,
recorded verbatim at the original manifest pin): `sqrt(1e-300)` — a fully NORMAL
operand — produced a residual claimed PAIR_EXACT that is provably inexact in
rational arithmetic (independently verified on-host by Will: true residual needs
2^-1102 < the 2^-1074 floor, FMA residual ≠ exact while printing identically).

**Classification (Will's ruling):** transcription-fidelity correction, not a
retune — prediction text unchanged, guard moved conservative, the FAIL stays in
the record as the stage's first finding.
