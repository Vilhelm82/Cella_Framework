# Generic Simplicity and Separation of the Axial Caustic

**Date:** 2026-07-10  
**Target:** Condition `(GS)` in the all-`k` monodromy theorem  
**Status:** Proof complete for every `k >= 3`  
**Consequence:** The generic axial mass-norm monodromy is `S_{delta_k}` for every `k >= 3`

## 1. The statement

Fix `k >= 3`. Put

```text
a_i = N_i^2,
w_i^2 = u+a_i,
sigma = w_1+...+w_k.
```

Let `B` be the open parameter space on which

```text
a_i != 0,
a_i != a_j for i != j,
```

and, for even `k`, every balanced infinity coefficient

```text
sum_i eta_i a_i
```

is nonzero. Let `X_a` be the smooth projective multiquadratic curve with function field

```text
C(u)(sqrt(u+a_1),...,sqrt(u+a_k)).
```

### Theorem (GS)

There is a nonempty Zariski-open subset `B_GS subset B` such that, for every parameter point in `B_GS`:

1. every critical point of `sigma:X_a -> P^1` is a nondegenerate fold; and
2. distinct critical points have distinct critical values.

Equivalently, the map `sigma` is simply branched over pairwise distinct finite branch values.

## 2. Boundary reduction

The banked boundary lemmas show that `sigma` is unramified:

```text
at every place above u=infinity;
at every radical branch place u=-a_i;
at every balanced infinity place when k is even.
```

Consequently every critical point is finite and lies away from `w_i=0`. There `u` is a local coordinate and

```text
d sigma/du
  = (1/2) C_1,

C_1 = sum_i 1/w_i.                            (2.1)
```

Differentiating once more gives

```text
d^2 sigma/du^2
  = -(1/4) C_3,

C_3 = sum_i 1/w_i^3.                          (2.2)
```

Thus a critical point is degenerate exactly when

```text
C_1 = C_3 = 0.                                (2.3)
```

## 3. Universal critical incidence

Work on

```text
Y = A^1_u x (G_m)^k_w
```

with the parameter map

```text
q:Y -> A^k_a,
q(u,w)_i = w_i^2-u.                           (3.1)
```

The universal finite critical locus is the hypersurface

```text
C = {C_1=0} subset Y.                         (3.2)
```

The equation `C_1=0` is irreducible on the torus. Indeed, after choosing `w_1,...,w_{k-1}`, it uniquely determines

```text
1/w_k = -sum_{i<k}1/w_i,
```

and the right side cannot vanish at a point of `C`. Hence `C` is isomorphic to a nonempty open subset of

```text
A^1_u x (G_m)^(k-1),
```

so `C` is irreducible of dimension `k`.

The map `C -> B` is dominant and generically finite. One route is the banked Riemann–Hurwitz count: every generic fiber has the finite positive ramification degree

```text
2^(k-1)(k-3)+2 delta_k,
```

and all ramification lies in the finite locus (2.1).

## 4. Generic nondegeneracy

The function `C_3` is not identically zero on `C`. To see this, take

```text
w_1=...=w_{k-1}=1,
w_k=-1/(k-1).
```

Then

```text
C_1 = (k-1)-(k-1) = 0,

C_3 = (k-1)-(k-1)^3
    = (k-1)(1-(k-1)^2) != 0                  (4.1)
```

for every `k>=3`.

Since `C` is irreducible, the degenerate locus

```text
D = {C_1=C_3=0}
```

is a proper closed subset of `C`, of dimension at most `k-1`. Its image in the `k`-dimensional parameter space therefore has proper Zariski closure. Remove that closure from `B`.

On the resulting nonempty open subset `B_1`, every critical point satisfies `C_3!=0`, so (2.2) shows that every critical point is a nondegenerate fold.

Equivalently, the relative critical scheme

```text
R -> B_1
```

is finite étale: finiteness follows because it is a closed quasi-finite subscheme of the proper family `X -> B_1`, and étaleness is the implicit-function consequence of `C_3!=0`.

## 5. Variation of a critical value

Étale-locally on `B_1`, choose a critical section

```text
P(a)=(u(a),w_1(a),...,w_k(a)).
```

Differentiating

```text
w_i^2=u+a_i
```

gives

```text
2w_i dw_i = du+da_i.
```

At the critical point,

```text
d sigma
 = sum_i dw_i
 = (1/2)(sum_i 1/w_i)du
   +(1/2)sum_i da_i/w_i.
```

The first term vanishes by `C_1=0`. Therefore the differential of the critical value is

```text
d c_P
  = (1/2) sum_i da_i/w_i(P).                  (5.1)
```

In coordinates on the parameter space,

```text
partial c_P/partial a_i = 1/(2w_i(P)).         (5.2)
```

This formula is the separation mechanism.

## 6. Generic separation of critical values

Form the off-diagonal ordered-pair scheme

```text
P = (R x_{B_1} R) minus diagonal.              (6.1)
```

It is finite étale over `B_1`. On it, let the two critical points be denoted

```text
P=(u,w_1,...,w_k),
Q=(v,z_1,...,z_k),
```

and define the critical-value difference

```text
h = c_P-c_Q = sum_i w_i-sum_i z_i.            (6.2)
```

By (5.1),

```text
d h
 = (1/2) sum_i (1/w_i-1/z_i) da_i.            (6.3)
```

The covector in (6.3) never vanishes on the off-diagonal pair scheme. If it vanished, then

```text
1/w_i = 1/z_i for every i,
```

so `w_i=z_i` for every `i`. The relations

```text
w_i^2=u+a_i,
z_i^2=v+a_i
```

would then give `u=v`, making `P=Q`, contrary to (6.1).

Therefore `h` is not identically zero on any irreducible component of the pair scheme. Its zero locus has codimension one wherever nonempty. Because the pair scheme is finite over `B_1`, the image of this zero locus is a proper closed subset of `B_1`.

Remove the union of these images and call the remaining nonempty open subset `B_GS`. For every parameter point in `B_GS`, no two distinct critical points have equal critical value.

Together with Section 4, this proves (GS). ∎

## 7. Return to the charge parameters

The original parameters are `N_i`, with `a_i=N_i^2`. On the open set `N_i!=0`, the map

```text
(N_1,...,N_k) -> (a_1,...,a_k)
```

is finite étale. The inverse image of `B_GS` is therefore a nonempty Zariski-open subset of the charge-parameter space. Thus (GS) holds for generic `N` for every `k>=3`.

No rational witness point is needed: the statement required by the generic monodromy theorem is precisely the nonemptiness of this geometric open set.

## 8. All-k monodromy consequence

The banked inertia-localization and fold criterion now apply without a remaining hypothesis:

1. all ramification of `sigma` occurs at the finite critical locus;
2. by (GS), each branch value contains exactly one simple fold;
3. every local branch cycle is therefore a transposition;
4. the cover is transitive because the mass norm is irreducible; and
5. a transitive group generated by transpositions is the full symmetric group.

Hence:

### Theorem — all-k symmetric monodromy

For every `k>=3`, with

```text
delta_k = 2^(k-1)                                  for k odd,
delta_k = 2^(k-1)-(1/2)binom(k,k/2)                for k even,
```

one has

```text
Gal(N_k / Q(M,N_1,...,N_k)) = S_{delta_k}          (8.1)
```

generically.

The certified cases `k=3,4,5,6` remain valuable as independent arithmetic witnesses, but they are no longer load-bearing for the unrestricted theorem.

## 9. Exact splice for the existing theorem note

Replace the open Section 7 with Sections 3–7 of this proof, then make the following status changes:

```text
Summary:
  Theorem D (generic Morse property): PROVED for all k>=3.
  All-k conclusion: Gal(N_k/F)=S_{delta_k} generically.

Remove:
  "Conjecture (all k>=3)"
  "single remaining obstruction"
  the hierarchical-charge and per-k certificate routes as proof obligations.

Retain:
  the k=3,4,5,6 certificates as independent checks;
  generic-is-not-universal guardrail;
  the genus, caustic, and pole-count formulas.
```

## 10. Scope

This theorem concerns the base monodromy of the axial mass norm. It does not by itself compute Kummer-decorated normal closures. Those are supplied separately by the wreath-lifting theorem: full symmetric base monodromy is the quotient input, while conjugate square-class independence determines the kernel.

## 11. Bottom line

Condition (GS) is not an additional arithmetic miracle and does not require an infinite sequence of certificates. It is the generic Morse property of the universal critical incidence. Degenerate critical points occupy a proper parameter locus, and the critical-value gradient

```text
(1/(2w_1),...,1/(2w_k))
```

separates every pair of distinct critical points. The all-`k` symmetric-monodromy theorem is therefore complete.
