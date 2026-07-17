# HUNT ADDENDUM v2.4 — SWEEP CLOSURE + SPLIT LAW (S-2026-07-05)
**Status: GROUNDED — Will, S-2026-07-05, "accept defaults" (PA-5 desk item 3). Author: Claude-box. Substrate: [BOX], byte-stable ×2 throughout.**
**Provenance: built exclusively on the honest Rabinowitsch saturation (v2.3 correction). No struck object (dim-1 tie curves, T4, deg-3528 screen, composite-modulus runs) is cited or used.**

## 1. Scope
Completes the P-F3 rational-witness hunt on the two-Cayley conjugation chassis
`A = cay(u1+t1·e, v1)·cay(u2+t2·e+t3·v1, v2)`, witness fixture (g,H) at n=5,
across ALL EIGHT pre-registered 3-parameter slices (B.SLATES[0..7]).

## 2. New banked tools (this session)
- `screen_slices.py` — verified-prime rational-point screen; P1 (dim==0) gate,
  P2 (degree-preserving prime) GATES P3 (root count); Euclid-by-%; every
  modulus asserted prime; deterministic pool = first 6 of the sympy nextprime
  chain from 576460752303424600; selftest mode (parse vs literal_eval,
  known root counts, P2-fire check) — PASSED live before deployment.
- `slice_factor.py` — exact Z-factorization of the slice eliminant w
  (flint fmpz_poly, deterministic) + per-factor diagnostics at the pool:
  root counts, pairwise gcd degrees, full mod-p splitting types.
- Certificate class A (screen): zero roots of w at one degree-preserving
  prime ⟹ zero rational roots [PROVEN; denominator divides lead(w)].
- Certificate class B (factorization): msolve RUR bijection (0-dim radical,
  separating form y) ⟹ rational tie point ⟹ rational root of w ⟹ integer
  linear factor. NO degree-1 factor ⟹ slice certified rational-point-free.
  Classes A and B are independent.

## 3. Sweep verdict — THE CHASSIS TABLE (all entries byte-stable ×2)
| slice | RUR (dim, ideal_deg, lf) | cert A (zero-root prime) | cert B (no linear factor) | spectrum | lead(f1)/lead(f2) |
|---|---|---|---|---|---|
| s0 | 0, 704, y | ✓ …424801 | ✓ | 352+352 | 1 |
| s1 | 0, 704, y | ✓ …424621 (new this session) | ✓ | 352+352 | 1 |
| s2 | 0, 704, y | ✓ …424661 | ✓ | 352+352 | 1 |
| s3 | 0, 704, y | ✓ …424661 | ✓ | 352+352 | 9 = 3² |
| s4 | 0, 704, y | ✓ …424621 | ✓ | 352+352 | 6561 = 3⁸ |
| s5 | 0, 704, y | — (pool min count 1) | ✓ | 352+352 | 1 |
| s6 | 0, 704, y | — (pool min count 1) | ✓ | 352+352 | 1 |
| s7 | 0, 704, y | ✓ …424699 | ✓ | 352+352 | 1 |

**VERDICT [CERTIFIED ×2, two independent certificate classes on 6/8 slices]:
all eight pre-registered two-Cayley 3-parameter slices contain NO rational
tie points. The slice route on this chassis is EXHAUSTED-NEGATIVE.**
Scope fence: this certifies the 8 frozen slates, not every conceivable slice
of the chassis. P-F3 (witness existence) remains OPEN as a claim.

## 4. The split law (NEW STRUCTURAL RESULT, unplanned)
```
[CERTIFIED as exact computation, 8/8 slices, byte-stable ×2]
  w_s = f1 · f2,  deg f1 = deg f2 = 352,  both irreducible over Z, content 1
  ⟹ the 704 tie points on every slice form exactly TWO Galois orbits of 352.

[CERTIFIED, 8/8]  lead(w_s) is a perfect square (exact isqrt).
[CERTIFIED, 8/8]  lead(f1), lead(f2) lie in the same square class of Q*/(Q*)²;
                  the ratio is 1 on six slices, 3² on s3, 3⁸ on s4.
[EMPIRICAL, s1, 6/6 pool primes]  mod-p splitting types of f1 vs f2 differ at
                  every tested prime ⟹ the two degree-352 fields are
                  NON-ISOMORPHIC (caveat: index divisibility at those primes;
                  morally negligible for 60-bit primes). Split-type data for
                  all 8 slices is banked in the factorization summaries;
                  cross-slice Frobenius statistics NOT yet analyzed.
```

## 5. Mechanism state
- **REFUTED: Q-rational orbit swap.** A Q-rational involution of the tie
  variety exchanging the orbits would commute with Galois, forcing the orbits
  to be isomorphic G_Q-sets — contradicted by the s1 mod-p data. [PROVEN
  conditional on the s1 non-isomorphism reading.]
- **REFUTED: naive y-symmetries.** f2 ≠ ±f1(±y); no reciprocal relation;
  neither factor self-symmetric (exact checks, s1).
- **REFUTED: slate-coordinate 3-adic origin of the s3/s4 slippage.** All
  eight slates have v3 ≡ 0 on every coordinate (numerators AND denominators).
  **CORRECTION (S-2026-07-05, in ink): this check was run on the RAW slate
  coordinates; the pipeline consumes perp(slate) = w − (⟨w,g⟩/|g|²)·g, which
  can acquire 3-denominators through |g|² and the projections. The refutation
  stands for raw slates only; the pipeline-object trace is SP.6 of
  SPLIT_PROBE_PREDECL (frozen this session).** Deeper normalization routes
  (perp(), poly_to_ms content, msolve RUR
  normalization) NOT yet excluded.
- **CANDIDATE [PLAUSIBLE, not constructed]:** an involution ι on the
  saturated tie variety defined over a quadratic extension (slice-dependent),
  swapping the orbits, with (D1·D2)∘ι = (D1·D2)·(3-power factor, trivial on
  6/8 slates). Compatible with every certified fact above. Natural hunting
  ground: Stab(g)-translations preserving the two-Cayley slice; the
  y = 1/(D1·D2) covering's deck structure.
- Numerology flag, unweighted: 704 = 2⁶·11, 352 = 2⁵·11; v11(leads) = 0
  on all slices — the 11 lives in the point count, not the lead arithmetic.

## 6. Records banked (rabinowitsch_records/)
`screen_s34.log` + `_x2.sha`, `screen_s567.log` + `_x2.sha`,
`s{0..7}_factorization.log` + `_x2.sha`, `s{0..7}_factors.txt` (full exact
factor coefficients — the field-structure raw material), `rab_out_shas.txt`
extended to s3–s7. Raw RURs remain on box /tmp per standing practice, sha'd.
s1's first-generation factorization artifacts (s1_factor.py route) are
superseded in the working tree by the uniform slice_factor.py versions;
originals preserved in git history (commit 034c406).

## 7. What this arms (Will's desk — do NOT start unprompted)
1. The strategic fork of HANDOFF_S2026-07-03 §"Strategic fork", now with a
   complete negative sweep: π-rotation boundary chassis [SPECULATION,
   designed not built] vs new slices vs chassis-verdict-and-pivot.
2. A NEW branch the handoff did not anticipate: the split-law mechanism hunt
   (the ι-involution). Cheap next probes if authorized: (a) cross-slice
   Frobenius/cycle-type statistics from banked split types (Galois group
   constraints on the 352-factors); (b) exact 3-valuation trace through
   perp()/content conventions on s3/s4; (c) Stab(g) slice-preservation audit.
3. Slice-1 diagnostic asymmetry note from the handoff ("Ê ties hold trivially
   on the conjugation family") — possibly the same structure the split law
   is seeing; not yet connected. [OPEN]

frozen: false · certainty tiers as marked · every number above traceable to a
byte-stable ×2 artifact in rabinowitsch_records/ or /tmp with recorded sha.
