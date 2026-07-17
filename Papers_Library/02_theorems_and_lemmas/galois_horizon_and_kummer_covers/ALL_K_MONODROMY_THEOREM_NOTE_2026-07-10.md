# All-k Monodromy of Axial k-Ellipse Norms — Theorem Note

**Date:** 2026-07-10
**Status updated 2026-07-17:** Parts A, B and the counting corollaries are
proved below; Part C retains the independent certified computations for
`k=3,4,5,6`. Lemma (GS) was subsequently proved for every `k>=3`. The
unrestricted equal-weight theorem is therefore complete. This note is retained
as a development and computational supplement, while the canonical reusable
proof authority is
`GENERIC_SYMMETRIC_MONODROMY_OF_WEIGHTED_MULTIQUADRATIC_SUMS_v1.0.md`
(`PAP-0509`), which repairs the primitive-element argument and strengthens the
result to every fixed nonzero weight vector.

## 0. Summary of results

```text
Theorem A (inertia localization).   UNCONDITIONAL, all k >= 3.
  All monodromy of the axial family is generated at the critical-sheet
  locus sum_i eta_i / w_i = 0. The sheet-collision (sub-balance)
  discriminant components are nodes with trivial inertia. The boundary
  places (u = infinity, contact places w_i = 0, balanced places) are
  unramified for the M-cover.

Theorem B (fold criterion).         UNCONDITIONAL reduction.
  If condition (GS) holds at one N-point for a given k, then
  Gal(N_k / Q(M, N_1..N_k)) = S_{delta_k} generically for that k.

Theorem C (verified range).         CERTIFIED.
  k = 3, 4, 5, 6: the generic group is S_4, S_5, S_16, S_22.

Counting corollaries.               UNCONDITIONAL.
  deg(sigma) = delta_k            (the degree law = pole count of sigma)
  g(X_k)     = 1 + 2^(k-2)(k-3)
  deg(ramification divisor of sigma) = 2^(k-1)(k-3) + 2 delta_k,
  supported entirely on the critical-sheet locus.

Theorem D (all k >= 3): Gal(N_k/F) = S_{delta_k} generically; (GS) is proved.
```

## 1. Setting and imported facts

Fix k >= 3 and a base field `F_0` of characteristic zero containing
`N_1, ..., N_k` with `N_i != 0`, `N_i^2` pairwise distinct, and (for even k)
`sum_i eta_i N_i^2 != 0` for every balanced sign vector `eta`
(`sum eta_i = 0`). The two cases used below are `F_0 = C(N)` (geometry, N
generic) and `F_0 = Q(N)` (arithmetic).

```text
E = F_0(u)(w_1, ..., w_k),   w_i^2 = u + N_i^2,
sigma = w_1 + ... + w_k in E,
N_k(u; M) = prod over eta in {+-1}^k of (4M - sum_i eta_i w_i)
          = Norm_{E / F_0(u)} (4M - sigma),
delta_k = 2^(k-1)                        (k odd)
        = 2^(k-1) - (1/2) binom(k, k/2)  (k even).
```

**Imported facts** (the generic normalization–reflection chain; banked). The
proofs are valuation-theoretic and use only characteristic zero and the
distinctness of the `N_i^2`; they are therefore valid over any `F_0` as
above, in particular over `C(N)`:

- (I1) `[E : F_0(u)] = 2^k` with Galois group `H = (C_2)^k`, because the
  square classes of the `u + N_i^2` (distinct monic linear polynomials in
  `u`, hence squarefree and coprime) are independent.
- (I2) The `H`-stabilizer of `sigma` is trivial: a nontrivial sign flip on a
  set `D` changes `sigma` by `-2 sum_{i in D} w_i`, which is nonzero because
  at a place over `u = -N_i^2` (any `i in D`) the term `w_i` has odd
  valuation while the others are units. Hence `E = F_0(u)(sigma)`.
- (I3) `N_k` is irreducible over `F_0(M)` of `u`-degree `delta_k`.

Let `X` denote the smooth projective model of `E` over `F_0 = C(N)` — the
full signed cover of the `u`-line, of degree `2^k`.

**Proposition 1.1 (normalization identification).** The normalization of the
plane curve `{N_k(u, M) = 0}` over `C(N)` is `X`, via the pair of functions
`(u, sigma/4)`.

*Proof.* The function field of the plane curve is
`C(N)(u, M)`-with-relation, i.e. `C(N)(u_root, M)`; under `4M = sigma` this
is the subfield `C(N)(u, sigma)` of `E`, which equals `E` by (I2). A smooth
projective curve with function field `E` is `X`. This is the `M`-level
instance of the R6 mechanism. QED

Consequently:

```text
Gal(N_k / C(N)(M)) = monodromy group of the map  sigma/4 : X -> P^1.
```

By (I3) this group is transitive on the `delta_k` sheets. Since
`C(N)(M)` contains `Q(M, N)`, fullness of the geometric group forces
fullness of the arithmetic group. (For loop arguments below, specialize `N`
to a very general complex point; the generic geometric group is computed
there, by standard spreading-out.)

## 2. Local behavior of sigma: the three boundary lemmas

Ramification of the cover `X` over the `u`-line is classical: it occurs
exactly over `u = -N_i^2` (the subextension by `w_i`) and over `u =
infinity` (all `w_i ~ sqrt(u)`), in each case with `2^(k-1)` places of
ramification index 2. This gives the genus (Section 5). What matters for
the monodromy is where the **map sigma** ramifies.

**Lemma 2.1 (places over u = infinity).** The completion of `E` at
`u = infinity` is a product of `2^(k-1)` copies of `C(N)((t))`,
`t = u^(-1/2)`, indexed by sign classes `{eta, -eta}`. At the place of class
`eta`,

```text
sigma = a_eta t^(-1) + (B_eta / 2) t + O(t^3),
a_eta = sum_i eta_i,      B_eta = sum_i eta_i N_i^2.
```

If `a_eta != 0` (unbalanced class): `sigma` has a simple pole, so the map
`sigma : X -> P^1` is **unramified** there and the place maps to
`M = infinity` with local degree one. If `a_eta = 0` (balanced class, even
k): by the standing hypothesis `B_eta != 0`, `sigma` has a simple zero, so
the map is **unramified** there as well.

*Proof.* `w_i = sqrt(u) sqrt(1 + N_i^2/u) = t^(-1) (1 + N_i^2 t^2 / 2 +
O(t^4))` after the branch choice defining the place; summing with signs
gives the display. A simple pole or simple zero of a map to `P^1` is an
unramified point. QED

**Corollary 2.2 (degree law = pole count).**
`deg(sigma : X -> P^1) = #{unbalanced classes} = delta_k.` This re-derives
the NPS degree law (R2) as the pole divisor of `sigma` and identifies the
even-k binomial correction as the count of balanced places, where `sigma`
is finite.

**Lemma 2.3 (contact places).** At each of the `2^(k-1)` places over
`u = -N_i^2`, with uniformizer `tau = w_i` (so `u = tau^2 - N_i^2`),

```text
sigma = eta_i tau + sum_{j != i} eta_j w_j(tau^2 - N_i^2),
d sigma / d tau = eta_i + O(tau) != 0.
```

The map `sigma` is **unramified** at every contact place.

*Proof.* The `j != i` terms are analytic in `tau^2`, hence even; their
`tau`-derivative vanishes at `tau = 0`. The `w_j(0) = sqrt(N_j^2 - N_i^2)`
are nonzero units by distinctness of the `N_j^2`. QED

**Lemma 2.4 (finite non-contact places).** At every other place of `X`, `u`
is a local uniformizer and

```text
d sigma / d u = (1/2) sum_i eta_i / w_i .
```

The map `sigma` ramifies exactly where this vanishes.

*Proof.* Direct differentiation of `w_i^2 = u + N_i^2`. QED

## 3. Theorem A: inertia localization and the mechanism dichotomy

**Theorem A.** For k >= 3 and generic N:

1. The ramification divisor of `sigma : X -> P^1` is supported entirely on
   the finite critical locus `{sum_i eta_i / w_i = 0}` — the
   **critical-sheet locus**. In particular, the entire monodromy group of
   the axial family over the M-line is generated by local monodromies at
   critical-sheet values.
2. The sheet-collision (sub-balance) components of the discriminant of
   `N_k` with respect to `u` are, over generic N, crossings of two branches
   of the plane model that are separately analytic in `M`: nodes of the
   plane curve, at which the normalization `X` is **unramified** over the
   M-line. Their local monodromy is trivial.

*Proof.* (1) is Lemmas 2.1, 2.3, 2.4: every non-finite-critical place is
unramified; over `P^1` the monodromy group is generated by the local
monodromies around the branch points, which all lie under the critical
locus. (2) A sub-balance crossing is a point where two roots `u_eta(M)`,
`u_eta'(M)` of distinct sign classes coincide. For generic N (so that
`N_i^2 != N_j^2`, excluding the identically-collapsing |D| = 2 mechanism),
each root satisfies its own sheet equation `s_eta(u) = 4M` with
`d s_eta / d u != 0` at the crossing (the crossing is transverse in `u`
because the slope difference is `(1/2) sum_{i in D} eta_i / w_i != 0`
generically); by the implicit function theorem each root is analytic in
`M` near the crossing. Two analytic branches meeting at a point form a node
of the plane model; on the normalization they are two distinct points,
each unramified over the M-line. Trivial inertia. QED

**Remark (the banked two-mechanism decomposition, explained).** The
corpus's discriminant decomposition — sheet-collision plus critical-sheet —
acquires its monodromic content: the collisions are monodromically inert;
the critical sheets generate everything. This also explains structurally
why the k = 5 computation destroyed the affine (C_2)^4 torsor labeling: a
fold exchanges two roots of a single local analytic branch, an operation
with no relation to the sign-class labels, so no label structure can be
monodromy-invariant once folds exist.

## 4. Theorem B: the fold criterion

**Condition (GS)(k, N).** Every zero of `d sigma` on `X` is simple (the
critical point is a nondegenerate fold: `sigma'' != 0` in a local
coordinate) and no two critical points share a critical value.

**Theorem B.** (GS)(k, N) at a single point N implies
`Gal(N_k / Q(M, N_1..N_k)) = S_{delta_k}` for generic N at that k.

*Proof.* Under (GS), each branch point of `sigma` lies under exactly one
simple fold; the fiber degenerates by exactly one quadratic merge, so the
local monodromy is a single transposition. The monodromy group `G` is
generated by these transpositions (Theorem A(1)) and is transitive (I3).
The orbits of the subgroup generated by all transpositions in `G` are the
connected components of the transposition graph; since that subgroup is
`G` itself, transitivity makes the graph connected; a connected
transposition graph on `delta_k` vertices generates `S_{delta_k}`. Hence
the geometric group is full; the arithmetic group, squeezed between it and
`S_{delta_k}`, is full. (GS) is a Zariski-open condition on N (simplicity
and distinctness of critical values are open), so one witness point gives
the generic statement. QED

## 5. Counting corollaries

**Genus.** `X` over the `u`-line: degree `2^k`, ramified with index 2 at
`2^(k-1)` places over each of `u = -N_1^2, ..., -N_k^2, infinity` — `k+1`
branch points in all. Riemann–Hurwitz:

```text
2g - 2 = 2^k (-2) + (k+1) 2^(k-1)  =>  g(X_k) = 1 + 2^(k-2) (k-3).
```

Checks: `g = 0` at `k = 2` — the curve is rational, which **is** the
two-charge closed form (the wall-product seed); `g = 1` at `k = 3` — the
solvable quartic rides an elliptic curve; `g = 5, 17, 49` at
`k = 4, 5, 6`.

**Caustic count.** Riemann–Hurwitz for `sigma : X -> P^1` of degree
`delta_k`:

```text
deg(ramification divisor) = 2g - 2 + 2 delta_k
                          = 2^(k-1) (k-3) + 2 delta_k,
```

supported entirely on the critical-sheet locus (Theorem A). Under (GS)
this is exactly the number of folds. Values: 8 (k=3), 18 (k=4), 64 (k=5),
140 (k=6). Unconditionally this counts the solutions of
`sum_i eta_i / w_i = 0` on `X` with multiplicity — a closed-form census of
the critical-sheet mechanism.

**Symmetry of the caustic.** The global sign flip `w_i -> -w_i` (all i) is
an automorphism of `X` carrying `sigma` to `-sigma`; critical points pair
off with opposite critical values. Branch points of the M-cover therefore
come in pairs `4M = +-c`. No further deck symmetry preserves `sigma`, so no
symmetry forces critical-value coincidences: there is no structural
obstruction to (GS).

## 6. Theorem C: the verified range

Arithmetic Dedekind certificates bypass (GS) entirely: a separable
full-degree rational specialization embeds its Galois group in the generic
group. Verified:

```text
k = 3, degree 4  (point 4M=32,  N=(4,8,16)):
  p=17 irreducible [4] (transitive + odd); p=7 type [1,3] (3-cycle:
  among transitive quartic groups only A4, S4 contain 3-torsion);
  p=11 type [1,1,2] (odd)  =>  S_4.
  Primitive lc = 9 = 1^(2*3) * 3^2: the odd-k pole formula
  lc = prod over sign-pair classes of (imbalance)^2, confirmed.

k = 4, degree 5:  banked S_5 certificate (points A, B, C).

k = 5, degree 16 (point 4M=128, N=(4,8,16,32,64)):
  p=73 irreducible [16]; p=37 type [1,4,11] (11-cycle => primitive +
  Jordan); p=23 type [1,3,12] (odd)  =>  S_16.

k = 6, degree 22 (point 4M=256, N=(4,8,16,32,64,128)):
  p=199 irreducible [22]; p=43 type [1,8,13] (sigma^8 is a pure 13-cycle,
  13 > 22/2 kills both block shapes 2x11 and 11x2; Jordan with
  13 <= 19 = n-3 gives A_22; parity of [1,8,13] is odd)  =>  S_22.
```

The primitivity mechanism, uniform in n: a p-cycle with prime
`p > n/2` acts trivially on any block system (p exceeds the block count,
so each block is preserved; then its cycle would have to fit inside a
block of size < p). Combined with Jordan (`p <= n-3`) this forces
`A_n <= G`.

The first even case beyond k = 4 behaves identically to the odd cases: the
balanced classes are zeros of `sigma`, unramified and monodromically
invisible (Lemma 2.1), exactly as the fold principle predicts.

## 7. The former open lemma — closed

**Theorem D (generic Morse property).** For every `k>=3`, there is a
nonempty Zariski-open parameter set on which every critical point of `sigma`
is nondegenerate and distinct critical points have distinct critical values.

The dedicated proof
`GS_GENERIC_MORSE_LEMMA_PROOF_2026-07-10.md` closes the old Lemma (GS) by
studying the universal critical incidence and the exact critical-value
gradient

```text
(1/(2w_1),...,1/(2w_k)).
```

The canonical successor `GENERIC_SYMMETRIC_MONODROMY_OF_WEIGHTED_MULTIQUADRATIC_SUMS_v1.0.md`
rebuilds that argument through a finite relative ramification scheme and
extends it to arbitrary fixed nonzero weights. Consequently every local
branch cycle on the generic locus is a transposition, and connectedness gives
the full symmetric group. The per-`k` certificates below remain independent
arithmetic checks, not proof steps in the unrestricted theorem.

## 8. Guardrails

1. Generic is not universal: special charge vectors degenerate (the banked
   `2^30 (3-u)(15-u)^4` example); physical instances need per-point
   certificates, unchanged.
2. Nothing here computes closure monodromy (R9) at any k; this note settles
   base groups. The inertia-localization theorem will, however, feed the
   R9 divisor table: all base branch cycles come from the critical-sheet
   locus.
3. Theorem A's node statement is for generic N (in particular
   `N_i^2 != N_j^2`); on the identically-collapsing loci `N_i^2 = N_j^2`
   the analysis is different and not claimed.
4. The caustic count is always with multiplicity. On the generic Morse open
   set supplied by Theorem D it equals the fold count; special parameter
   vectors may still collide or degenerate.

## 9. Program consequences

```text
R10:  k=5 group S_16 (established today) now flanked by k=3 (S_4) and
      k=6 (S_22).
R11:  generic higher-k groups: ESTABLISHED ALL-k SYMMETRIC;
      Gal(N_k/F)=S_{delta_k} for every k>=3.
NEW (this note): inertia localization theorem — the critical-sheet
      mechanism generates all monodromy; sub-balance collisions are inert.
NEW (this note): genus formula g = 1 + 2^(k-2)(k-3); caustic degree
      2^(k-1)(k-3) + 2 delta_k; degree law as pole count of sigma.
Paper IV succession: the weighted all-k paper is now the reusable proof
      authority; this note supplies the development record and low-k checks.
```

## 10. Reproducibility

```text
k=3/k=6 script: allk_monodromy_certificates.py  (stdlib, exact)
script SHA-256:
b2cb71a8bca69ca33e16a4281aa0aa87f89d062e98f50e16e797811abe724af4
deterministic stdout SHA-256 (two runs):
a18e7035ad0708009c61824dc4d0950534facbe11d4ab54ef4f522bf83901640

k=5 certificate: see K5_GALOIS_GROUP_CERTIFICATE_REPORT_2026-07-10.md.
k=4 certificate: banked (paper appendix; points A, B, C).
Anchor: both scripts rebuild the banked Point-B quintic exactly before
any new computation.
```

## 11. Bottom line

The all-`k` base-monodromy problem is closed. The monodromy of the axial
family lives entirely at the critical-sheet locus, sheet collisions are
inert, the degree law is the pole divisor of the entropy-sum function, the
genus and caustic degree are counted in closed form, and the generic group is
`S_{delta_k}` for every `k>=3`. The certified cases `k=3,4,5,6` remain useful
independent arithmetic witnesses. The next genuinely case-specific problem
is not another base-group census: it is proving independence of the concrete
conjugate Kummer classes (`R=0`) in an all-`k` decorated realization.
