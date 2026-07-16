# Weighted Multiquadratic Monodromy Paper Design

**Date:** 2026-07-16  
**Status:** Approved design  
**Deliverable:** one finished-proof Markdown paper

## Objective

Create a self-contained paper that extracts the reusable theorem behind the
DBP all-`k` axial monodromy calculation.  The paper will replace the
equal-weight, application-specific presentation by a theorem for arbitrary
fixed nonzero weights on a multiquadratic cover, recover the DBP axial family
as a specialization, and give the exact conditional interface to conjugate
Kummer/wreath lifts.

The paper must be mathematically complete at its declared scope.  It may not
use phrases such as "banked", "imported fact", or "proof supplied elsewhere"
for a load-bearing step.

## Output

Create:

`Papers_Library/01_completed_papers/galois_horizon_and_kummer_covers/GENERIC_SYMMETRIC_MONODROMY_OF_WEIGHTED_MULTIQUADRATIC_SUMS_v1.0.md`

No existing paper, theorem note, DAG node, catalogue, or source file will be
retired or mutated in this task.  DAG registration and editorial propagation
into Paper IV are later maintenance actions.

## Governing setup

Let `K` be a characteristic-zero field and work geometrically over an
algebraic closure when computing monodromy.  Fix:

- an integer `k >= 3`;
- nonzero weights `c_1, ..., c_k`;
- parameters `a_1, ..., a_k` with `a_i != a_j` for `i != j`;
- the smooth projective multiquadratic curve `X_a` with function field
  `K(u)(w_1, ..., w_k)`, where `w_i^2 = u + a_i`;
- the weighted radical-sum map
  `f_c = sum_i c_i w_i : X_a -> P^1`.

For a sign vector `eta`, modulo the global sign relation
`eta ~ -eta`, define

```text
A_eta(c)   = sum_i eta_i c_i,
B_eta(a,c) = sum_i eta_i c_i a_i,
```

and

```text
d(c) = #{ sign-pairs {eta,-eta} : A_eta(c) != 0 }.
```

The boundary-good parameter locus `B_c` is the complement of:

1. the diagonals `a_i = a_j`; and
2. each hyperplane `B_eta(a,c) = 0` for which `A_eta(c) = 0`.

The paper will prove the existence of a further nonempty Zariski-open subset
`B_GS(c) subset B_c`.  It will not claim the theorem at every point of
`B_c`.

## Main theorem

For every fixed nonzero weight vector `c` and every `k >= 3`, there is a
nonempty Zariski-open `B_GS(c) subset B_c` such that for every
`a in B_GS(c)`:

1. `X_a` is a connected smooth projective curve;
2. `deg(f_c) = d(c)`;
3. every ramification point of `f_c` is finite and away from the radical
   contacts `w_i = 0`;
4. every critical point is a nondegenerate fold;
5. distinct critical points have distinct critical values;
6. the geometric monodromy group of `f_c` is `S_{d(c)}`;
7. the corresponding generic arithmetic group is also `S_{d(c)}`;
8. the curve genus and ramification degree are

   ```text
   g(X_a) = 1 + 2^(k-2)(k-3),
   deg R_f = 2^(k-1)(k-3) + 2 d(c).
   ```

The theorem is generic, not universal.  The exceptional locus and the role
of every removed condition must be explicit.

## DBP specialization

For `c_i = 1`, the paper will derive

```text
d(c) = delta_k
     = 2^(k-1),                                  k odd,
     = 2^(k-1) - (1/2) binom(k,k/2),             k even.
```

With `a_i = N_i^2` and `f_c = 4M`, this gives the generic axial mass-norm
result

```text
Gal(N_k / Q(M,N_1,...,N_k)) = S_{delta_k}
```

for every `k >= 3`, subject to the displayed genericity conditions.  The
previous `k=3,4,5,6` certificates will be retained as independent examples,
not used as proof obligations.

## Proof architecture

### 1. Multiquadratic field and primitive element

Prove directly that the square classes of the distinct linear polynomials
`u+a_i` are independent, hence

```text
Gal(K(u)(w_1,...,w_k)/K(u)) ~= (C_2)^k.
```

Prove that `f_c` has trivial stabilizer under the sign group.  The proof must
use individual sign-flip subtraction: if a nonempty flip set `D` fixed
`f_c`, then `sum_{i in D} c_i w_i = 0`; flipping one `j in D` and subtracting
gives `2 c_j w_j = 0`, a contradiction.  The older claim that one odd
valuation automatically prevents cancellation will not be repeated.

Conclude `K(u,f_c) = K(u)(w_1,...,w_k)` and identify the normalization of the
weighted norm plane curve by its function field.

### 2. Boundary geometry, degree, and genus

At the infinity place indexed by `{eta,-eta}`, use `t=u^(-1/2)` to prove

```text
f_c = A_eta t^(-1) + (1/2) B_eta t + O(t^3).
```

Thus an unbalanced class gives one simple pole, while a balanced class on
`B_c` gives a simple zero.  Prove separately that every radical-contact
place `w_i=0` is unramified because its local linear coefficient is
`eta_i c_i != 0`.  Pole counting then gives `deg f_c=d(c)`.

Compute the genus of `X_a` by a complete Riemann--Hurwitz calculation for
the degree-`2^k` map to the `u`-line, including the number and index of the
places over each finite branch point and infinity.

### 3. Proper relative critical scheme

Construct the relative smooth projective family over `B_c`, for example by
normalizing `P^1_u x B_c` in the multiquadratic function-field extension.
Define the relative ramification scheme as the zero scheme of `df_c`.
Use the boundary computations to show it misses the omitted affine charts.
It is then proper and quasi-finite over the relevant parameter open, hence
finite.  This replaces the current proof's unproved finiteness/properness
assertion.

### 4. Generic nondegeneracy

On the finite critical incidence use

```text
C_1 = sum_i c_i/w_i,
C_3 = sum_i c_i/w_i^3.
```

Prove the critical incidence `C_1=0` is irreducible of dimension `k`.  With
`x_i=c_i/w_i`, prove that `C_3=sum_i x_i^3/c_i^2` is not identically zero
on `sum_i x_i=0`.  A three-variable restriction produces a nonzero mixed
coefficient `-3/c_r^2`.  Therefore the degenerate locus has dimension at
most `k-1`, and its parameter image has proper closure.

After removing that closure, the relative critical scheme is finite etale
and every critical point is a fold.

### 5. Generic separation of critical values

For an etale-local critical section `P`, derive

```text
d(value_P) = (1/2) sum_i (c_i/w_i(P)) da_i.
```

On the off-diagonal ordered-pair scheme, the differential of the value
difference has coefficients

```text
(1/2)c_i(1/w_i(P)-1/w_i(Q)).
```

Show this covector cannot vanish off the diagonal.  Its zero locus therefore
has a proper closed image in parameter space.  Removing those images defines
`B_GS(c)`.

### 6. Full symmetric monodromy

Prove that the connected degree-`d(c)` cover is transitive.  Simple folds
over distinct branch values give transpositions.  A transitive permutation
group generated by transpositions is the full symmetric group, so the
geometric group is `S_{d(c)}`.  Derive the arithmetic generic group by the
standard geometric-subgroup inclusion.

### 7. Conditional Kummer-wreath lift

Include a self-contained downstream theorem, without promoting a
DBP-specific all-`k` closure:

- for a degree-`d` separable sheet field with normal closure group `G`, and
  `s` nonzero radicands, define the conjugate square-class module;
- prove that full column rank of the valuation-parity matrix makes all `sd`
  conjugate radicands independent;
- prove that the resulting normal-closure group is
  `C_2^s wreath_I G`;
- specialize conditionally to `G=S_{d(c)}`.

This turns the downstream all-`k` decorated-cover problem into the explicit
task of constructing and verifying an invertible sheet-level parity matrix.

## Sharpness and counterexamples

The paper will include exact examples showing why the theorem is generic:

1. **Critical-value collision in `B_c`:** for `k=3`, equal weights, and a
   primitive cube root `zeta`, the points
   `w=(1,zeta,zeta^2)` and `-w` are distinct simple critical points with
   common value zero.
2. **Degenerate critical point in `B_c`:** for `k=5`, equal weights, take
   `x=1/w=(-20,-14,-1,17,18)` and `a_i=x_i^(-2)`; then
   `sum x_i=sum x_i^3=0` with distinct `a_i`.
3. **Necessity of the balanced-infinity condition:** for `k=4`, equal
   weights, `eta=(1,1,-1,-1)`, and `a=(1,4,2,3)`, both the leading and
   first balanced moments vanish, yielding cubic rather than linear local
   behavior at infinity.

## Downstream effect

The paper will:

- close the mathematical content behind DAG gaps `DBP:gap:IV1` and
  `DBP:gap:IV2` at the base-monodromy level;
- replace the stale all-`k` conjecture language with a proved theorem;
- provide Paper IV with an arbitrary-`k` base group;
- make `DBP:gap:IV3` a precise valuation/parity-matrix application rather
  than a vague monodromy problem;
- provide a reusable theorem for non-DBP weighted radical-sum systems.

## Nonclaims

The paper will not claim:

- simple branching for every point of `B_c`;
- a theorem at coincident `a_i`, vanishing weights, or bad balanced moments;
- characteristic-`p` generality;
- full Kummer independence for a DBP all-`k` decoration without the required
  valuation matrix;
- explicit complex braid words or resolution of DAG gap `DBP:gap:IV7`;
- closure results for self-glue towers;
- a physical branch-selection theorem at special nongeneric charge vectors.

## Verification

Before completion:

1. scan the paper for stale terms: `conjecture`, `open lemma`, `banked`,
   `imported`, `proof elsewhere`, and `Paper III`;
2. verify every use of `d(c)`, `B_c`, and `B_GS(c)` is consistent;
3. check the equal-weight specialization gives the stated `delta_k` formula;
4. independently recompute the three exact counterexamples;
5. check every theorem hypothesis is repeated where a corollary uses it;
6. run a source-level claim audit against the live Cella DAG and the three
   governing source files;
7. request an adversarial mathematical review of the finished paper;
8. make no completeness claim until every review defect is resolved.

## Governing sources

- `DBP:note:allk_monodromy` — inertia localization, degree/genus/ramification
  counts, and the former all-`k` theorem note;
- `DBP:proof:gs_morse` — the generic Morse and value-separation proof;
- `DBP:thm:kummer_wreath_lift` — the conjugate Kummer-module theorem;
- `DBP:paper:IV` — the downstream released paper;
- `DBP:gap:IV1`, `IV2`, `IV3`, `IV7` — exact editorial/application boundaries;
- `LOG_ENTRY_R6_R7_generic_descent_v2.md` and
  `AUDIT_REPORT_R6_R7_GENERIC_DESCENT.md` — source material to be re-proved,
  not cited as a substitute for proof.

