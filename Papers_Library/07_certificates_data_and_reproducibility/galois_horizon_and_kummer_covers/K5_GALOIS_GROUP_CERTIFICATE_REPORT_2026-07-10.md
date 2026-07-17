# k=5 Axial Norm Galois Group — Certificate Report

> **Succession notice (2026-07-17).** This dated report remains the exact
> specialization certificate establishing the generic `k=5` base group
> `S_16`. Its forward-looking R11 language below is historical: the completed
> paper `GENERIC_SYMMETRIC_MONODROMY_OF_WEIGHTED_MULTIQUADRATIC_SUMS_v1.0.md`
> (`PAP-0509`) now proves generic base monodromy `S_{delta_k}` for every
> `k>=3`, and the live status surface is
> `GALOIS_K_ELLIPSE_RESEARCH_MAP_v1_6.md`. The report's separate warning that
> the `k=5` Kummer-decorated closure still requires a square-class-rank
> certificate remains current.

**Date:** 2026-07-10
**Target:** Generic Galois group of the five-charge axial mass norm
**Verdict:** **PASS. Gal(N_5/F) = S_16 generically**, by exact specialization
certificate. The symmetric-group branch of the higher-charge fork fires; the
affine (torsor) alternative is refuted.

## 1. Claim being certified

Let

```text
F   = Q(M, N_1, ..., N_5),
N_5(u) = prod over eps in {+-1}^5 of (4M - sum_i eps_i sqrt(u + N_i^2)),
deg_u N_5 = 16          (degree law, odd k: 2^(k-1)).
```

Generic irreducibility of `N_5` is banked (R10, generic half). The claim
certified here:

```text
Gal(N_5 / F) = S_16.
```

## 2. Certificate logic

Three witnesses suffice, by the following chain.

1. **Transitivity.** A prime with irreducible reduction proves `N_5`
   irreducible over `Q` at the specialization; the Frobenius element is a
   16-cycle.
2. **Primitivity.** A Frobenius type containing an 11- or 13-cycle yields,
   after raising to the lcm of the remaining cycle lengths (coprime to 11
   resp. 13), a pure p-cycle with `p > 8`. A block system on 16 points has
   2, 4, or 8 blocks of size 8, 4, or 2. A p-cycle with `p > 8` can neither
   permute at most 8 blocks nontrivially (p prime exceeds the block count)
   nor act within blocks of size at most 8 (its cycle exceeds the block
   size). No block system survives: the group is primitive.
3. **Jordan.** A primitive group of degree 16 containing a p-cycle with
   `p <= 13 = 16 - 3` contains `A_16` (Jordan, 1873).
4. **Parity.** Any Frobenius type that is an odd permutation (parity
   `16 - #cycles` odd; a 16-cycle qualifies) excludes `A_16`.
5. **Specialization embedding.** The Galois group of a separable rational
   specialization of full degree embeds in the generic group — the same
   principle load-bearing in the k=4 S_5 certificate. Specialized `S_16`
   therefore forces generic `S_16`.

## 3. Specialization point

```text
4M = 128,   N = (4, 8, 16, 32, 64)      [Q = (1, 2, 4, 8, 16)]
```

- Strict chamber: `128 > 4+8+16+32+64 = 124`.
- `N_i` nonzero, `N_i^2` pairwise distinct.
- Every signed subset sum `sum_D eps_i N_i` is nonzero automatically: the
  2-adic valuation of the smallest included term survives in any signed sum
  of distinct powers of two. No accidental sub-balance coincidences at the
  point.
- No wall passes through the point: `max |sum eps_i N_i| = 124 < 128`, so
  `N_5(0) != 0`.

## 4. Construction and self-checks

`N_5` is built by iterated quadratic norms: with `p_0(x) = x` and

```text
p_j(x) = p_{j-1}(x - w_j) p_{j-1}(x + w_j) = A^2 - (u + N_j^2) B^2,
```

where `A, B` are the even/odd parts of `p_{j-1}(x + w_j)` in `w_j` after
reduction by `w_j^2 = u + N_j^2`; then `N_5(u) = p_5(4M)`, taken primitive
with positive leading coefficient. All arithmetic exact integer.

Checks passed:

1. **Banked-artifact anchor.** The identical routine at the k=4 Point-B data
   `(4M, N) = (60; 4, 8, 12, 20)` reproduces the banked Point-B quintic
   coefficient-for-coefficient (crown certificate report, section 2.2).
2. **Degree law.** `deg_u = 16`.
3. **Constant term.** The unreduced `f_raw(0)` equals the direct product of
   the 32 wall values `128 - sum eps_i N_i`, computed independently.
4. **Leading coefficient (structural).** Primitive
   `lc(N_5) = 1476225 = 3^10 * 5^2`, exactly

   ```text
   lc = prod over sign-pair classes of (imbalance)^2
      = 1^(2*10) * 3^(2*5) * 5^(2*1),
   ```

   ten pair classes of imbalance 1, five of imbalance 3, one of imbalance 5.
   For odd `k` there are no balanced sign pairs, so the mass drops out of the
   leading coefficient entirely — in contrast to k=4, where the six balanced
   pairs contribute `lc = -2^24 M^6`. The computed value confirms the sheet
   asymptotics to the digit.

## 5. Frobenius witnesses

Cycle types of `N_5` mod p (distinct-degree factorization, exact; full table
in `k5_N5_pointA.txt`):

```text
p = 23 : [1, 3, 12]            odd permutation (parity 13)
p = 37 : [1, 4, 11]            sigma^4 is a pure 11-cycle
p = 73 : [16]                  irreducible: transitive + 16-cycle (odd)
```

Supporting occurrences: further 16-cycles at p = 157, 167, 181, 193; a
13-cycle at p = 79 (type [3, 13]); another 11-cycle at p = 173.

Chain: transitive (p = 73) + primitive and A_16 (p = 37, Jordan) + odd
element (p = 23 or p = 73) gives specialized group `S_16`; the embedding
lemma gives generic `S_16`. No conditional steps remain beyond the standard
good-specialization lemma already load-bearing at k=4.

## 6. Structural corollaries

1. **The affine alternative is refuted.** For odd `k` the roots are
   canonically a torsor under `(C_2)^k / {+-1} = (C_2)^(k-1)`; at k=5 the
   sixteen roots carry an affine `F_2^4` structure, and the natural
   structured-subgroup candidate is `AGL(4,2)`, order
   `322560 = 2^10 * 3^2 * 5 * 7`. Neither 11 nor 13 divides this order, so
   the p = 37 witness alone excludes every subgroup of `AGL(4,2)`.
   Elimination annihilates the sign-label algebra: monodromy sees no residue
   of the torsor structure. This negative is a theorem, not an absence of
   evidence.
2. **Shadow mixing is total.** `S_16` is 16-transitive-enough: no invariant
   pairing, partition, or labeling of the sixteen shadow sectors survives
   passage to the observables. The five-charge analogue of the k=4 statement
   "the algebra cannot tell the hole from its shadows" holds in the
   strongest possible form.

## 7. Scope and guardrails

1. Generic is not universal: special charge vectors can degenerate (compare
   the k=4 example `N_4 = 2^30 (3-u)(15-u)^4`). Physical instances of
   interest still require per-point certificates.
2. The result is the base group of the k=5 mass cover. The Kummer-decorated
   closure tower above it (the k=5 analogue of R9) remains open; with the
   base group maximal, that tower is again governed entirely by the
   square-class module.
3. Nothing here promotes the k=4 closure monodromy (R9) or any rotating
   statement.

## 8. Program consequences

```text
R10  five-charge degree-16 group:        promote to ESTABLISHED
     (generic S_16; specialized instances per-point as always).
R11  generic higher-k Galois groups:     upgrade from OPEN to CONJECTURED
     ALL-k SYMMETRIC: Gal(N_k/F) = S_{delta_k} for all k >= 4;
     proved at k = 4 (S_5) and k = 5 (S_16).
Paper III fork (strategic memo section 5): the symmetric-group branch
     fires. Target theorem: all-k generic symmetric monodromy. Proof shape:
     transitivity is banked for all k; a transposition arises at any simple
     sheet-collision divisor; primitivity is the open step.
```

## 9. Reproducibility record

```text
script:  k5_galois_certificate.py   (stdlib only, exact arithmetic)
script SHA-256:
106930038f3e3325ab765c136c87a4460c6b695e803cd36e268cb41c9ba135f4

deterministic stdout SHA-256 (two consecutive runs):
aa9d970a5c9d44ded79d925d761bdbd86427844875b124500a922f10b85c907b
aa9d970a5c9d44ded79d925d761bdbd86427844875b124500a922f10b85c907b

artifacts: k5_N5_pointA.txt (full N_5 coefficients + Frobenius table),
           k5_certificate_output.txt (run transcript).
```

## 10. Bottom line

The five-charge experiment was designed as a discriminator and it
discriminated: the generic group is fully symmetric, the affine torsor
structure on the shadow sectors is destroyed by elimination, and the
higher-charge programme is now an all-k symmetric monodromy conjecture with
its first two cases proved. The base of every k=5 tower question is settled;
what remains above it is Kummer.
