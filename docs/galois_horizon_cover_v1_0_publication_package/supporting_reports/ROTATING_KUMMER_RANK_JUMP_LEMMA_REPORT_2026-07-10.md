# Rotating Kummer Rank Jump and Axial–Horizon Decoupling

**Date:** 2026-07-10  
**Status:** Proof-complete, subject to integration into the canonical paper  
**Depends on:** Generic quintic irreducibility, entropy-sum primitivity, and the degree-20 crown certificate

## 1. Executive result

Rotation does not raise the degree of the ordered-horizon field: it remains degree 20 over the rotating observable field, and either normalized horizon entropy generates it. Rotation does, however, separate the axial square-root class from the horizon-difference class. After adjoining the axial square root, the generic rotating cover has degree 40. At `J=0` its fiber becomes reducible, with two branch-compatible components isomorphic to the static degree-20 crown.

Equivalently:

```text
static:    axial reflection and horizon swap are tied by one Kummer relation;
rotating:  axial reflection and horizon swap become independent involutions.
```

## 2. Setup and hypotheses

Let

```text
F = Q(M,Q_1,Q_2,Q_3,Q_4),
K = F(u),
```

where `u=m^2` satisfies the irreducible four-charge mass quintic `N(u)`. Put

```text
N_i = 4Q_i,
P   = product_i N_i in F.
```

Let `gamma,beta in K` be the static entropy elements satisfying

```text
gamma(gamma-4P) = 4u beta^2.                 (2.1)
```

Assume:

```text
(H1) N_i != 0 and N_i^2 != N_j^2 for i != j.

(H2) beta != 0 in K.

(H3) [u] and [gamma] are independent in K^*/K^{*2}.

(H4) K = F(gamma).
```

Here (H3) is the degree-20 crown certificate, and (H4) is the banked entropy-sum primitive-element theorem.

Let `J` be an indeterminate over `F`, and define

```text
F_J     = F(J),
K_J     = K(J),
delta_0 = gamma-4P,
delta_J = gamma-4P-16J^2 = delta_0-16J^2.
```

All fields have characteristic zero.

## 3. Main theorem

### Theorem 3.1 — Rotating Kummer rank jump

Under (H1)–(H4):

1. The three classes

   ```text
   [u], [gamma], [delta_J]
   ```

   are independent in `K_J^*/K_J^{*2}`.

2. The rotating ordered-horizon field

   ```text
   H_J = K_J(sqrt(gamma),sqrt(delta_J))
   ```

   satisfies

   ```text
   [H_J:K_J] = 4,
   Gal(H_J/K_J) = V_4,
   [H_J:F_J] = 20.
   ```

3. The augmented axial–horizon field

   ```text
   L_J = K_J(sqrt(u),sqrt(gamma),sqrt(delta_J))
   ```

   satisfies

   ```text
   [L_J:K_J] = 8,
   Gal(L_J/K_J) = (Z/2Z)^3,
   [L_J:F_J] = 40.
   ```

4. In the `J=0` fiber,

   ```text
   [delta_0] = [u][gamma],
   ```

   so the specialized Kummer span has rank two and

   ```text
   K(sqrt(gamma),sqrt(delta_0))
     = K(sqrt(u),sqrt(gamma)).
   ```

   The degree-eight Kummer algebra underlying `L_J/K_J` specializes to two isomorphic degree-four components over `K`, each equal to the static crown after a compatible choice of square-root sign.

### Proof

#### Step 1 — the quintic survives the transcendental base extension

The extension `F(J)/F` is purely transcendental and therefore regular. Equivalently, `F` is algebraically closed in `F(J)`, and `F(J)` is linearly disjoint from every finite algebraic extension of `F`.

By Gauss's lemma, the irreducible polynomial `N(u) in F[u]` remains irreducible in `F(J)[u]`. Hence

```text
[K_J:F_J] = [K:F] = 5.                       (3.1)
```

#### Step 2 — the old square classes remain independent

Suppose a constant `a in K^*` becomes a square in `K(J)`: say `a=r(J)^2`. Then `r(J)` is algebraic over `K`, being a root of `X^2-a`. Since `K` is algebraically closed in the purely transcendental field `K(J)`, one has `r(J) in K`. Thus `a` was already a square in `K`.

Consequently the natural map

```text
K^*/K^{*2} -> K(J)^*/K(J)^{*2}
```

is injective, and (H3) gives the independence of `[u]` and `[gamma]` over `K_J`.

#### Step 3 — `delta_J` has a private prime

From (2.1), using `beta!=0`,

```text
delta_0 = gamma-4P = 4u beta^2/gamma.
```

Therefore, in the square-class group,

```text
[delta_0] = [u][gamma]^{-1} = [u][gamma].    (3.2)
```

By (H3), the class `[u][gamma]` is nontrivial, so `delta_0` is a nonzero nonsquare in `K`.

It follows that

```text
delta_J = delta_0-16J^2
```

is irreducible as a quadratic polynomial in `J` over `K`: a factorization would require `delta_0/16` to be a square in `K`, equivalently `delta_0` to be a square.

Thus

```text
p = (delta_0-16J^2)
```

is a height-one prime of the PID `K[J]`. Its discrete valuation satisfies

```text
v_p(delta_J) = 1,
v_p(u)       = 0,
v_p(gamma)   = 0,                              (3.3)
```

because `u` and `gamma` are nonzero constants with respect to `J`.

Any square-class relation involving `[delta_J]` has odd `p`-valuation and is therefore impossible. Relations not involving `[delta_J]` are excluded by Step 2. Hence

```text
dim_F2 span{[u],[gamma],[delta_J]} = 3.        (3.4)
```

#### Step 4 — Kummer degrees

By Kummer theory in characteristic different from two, a rank-`r` subgroup of `K_J^*/K_J^{*2}` generates a multiquadratic extension of degree `2^r`.

The pair `[gamma],[delta_J]` is independent, so

```text
[H_J:K_J] = 4.
```

The triple `[u],[gamma],[delta_J]` is independent, so

```text
[L_J:K_J] = 8.
```

Combining these with (3.1) gives

```text
[H_J:F_J] = 4*5 = 20,
[L_J:F_J] = 8*5 = 40.
```

The stated elementary abelian Galois groups over `K_J` follow from the independent sign changes of the relevant square roots.

#### Step 5 — the `J=0` fiber

Equation (3.2) gives

```text
sqrt(delta_0) = 2 beta sqrt(u)/sqrt(gamma)     (3.5)
```

after choosing a compatible square-root sign. Thus

```text
K(sqrt(gamma),sqrt(delta_0))
  subseteq K(sqrt(u),sqrt(gamma)).
```

Conversely,

```text
sqrt(u) = sqrt(gamma)sqrt(delta_0)/(2 beta),   (3.6)
```

so the reverse inclusion holds. This proves

```text
K(sqrt(gamma),sqrt(delta_0))
  = K(sqrt(u),sqrt(gamma)).                    (3.7)
```

For the augmented generic cover, the precise fiber statement is slightly stronger than a bare “degree collapse.” Put

```text
E = K(sqrt(u),sqrt(gamma)),
c = 2 beta sqrt(u)/sqrt(gamma) in E^*.
```

At `J=0`, the final quadratic relation becomes

```text
Z^2-delta_0 = (Z-c)(Z+c)
```

over `E`. Since `c!=0` and the characteristic is zero,

```text
E[Z]/(Z^2-delta_0) ~= E x E.                  (3.8)
```

Accordingly, the degree-eight generic Kummer algebra has a reducible special fiber comprising two isomorphic degree-four components over `K`. Choosing either compatible sign in (3.5) selects one component, which is the static crown `E`. Multiplication by `[K:F]=5` makes each component degree 20 over `F`. This proves the theorem. ∎

## 4. Realization in the rotating four-charge family

Let

```text
w_i = m cosh(2 delta_i),
Pi_c = product_i cosh(delta_i),
Pi_s = product_i sinh(delta_i).
```

The charge normalization is

```text
N_i = 4Q_i = m sinh(2 delta_i),
```

and therefore

```text
P = product_i N_i = 16m^4 Pi_c Pi_s.          (4.1)
```

The rotating entropy formula is

```text
S_± = 2 pi m [
    m(Pi_c+Pi_s)
    +/- sqrt(m^2-a^2)(Pi_c-Pi_s)
].                                             (4.2)
```

All square roots below are branch-compatible algebraic roots; they are not assertions about principal analytic square roots for arbitrary signed charges.

### 4.1 The entropy sum is independent of rotation

Since

```text
w_i+m = 2m cosh(delta_i)^2,
w_i-m = 2m sinh(delta_i)^2,
```

we have

```text
A = product_i(w_i+m) = 16m^4 Pi_c^2,
B = product_i(w_i-m) = 16m^4 Pi_s^2.
```

Thus

```text
(S_+ + S_-)/pi
  = sqrt(A)+sqrt(B)
  = 4m^2(Pi_c+Pi_s).                           (4.3)
```

No `a` or `J` occurs in this expression. Therefore, if

```text
y = (S_+ + S_-)/pi,
```

then

```text
y^2 = gamma,                                   (4.4)
```

with exactly the same `gamma in K` as in the static theory.

### 4.2 The horizon product acquires the rotational term

From (4.2),

```text
S_+S_-/pi^2
 = 4m^2[
     m^2(Pi_c+Pi_s)^2
     -(m^2-a^2)(Pi_c-Pi_s)^2
   ]

 = 4m^2[
     4m^2 Pi_c Pi_s
     +a^2(Pi_c-Pi_s)^2
   ].
```

Using (4.1) and

```text
J = ma(Pi_c-Pi_s),
```

this becomes

```text
S_+S_-/pi^2 = P+4J^2.                          (4.5)
```

Define

```text
z = (S_+ - S_-)/pi.
```

Then

```text
z^2
 = y^2-4(S_+S_-/pi^2)
 = gamma-4P-16J^2
 = delta_J.                                    (4.6)
```

Equations (4.4) and (4.6) identify the rotating ordered-horizon field with `H_J`.

### 4.3 Why `J` is transcendental over the static observable field

Consider the parameter map

```text
(m,delta_1,...,delta_4,a)
    -> (M,Q_1,...,Q_4,J).
```

The static submap

```text
(m,delta_1,...,delta_4) -> (M,Q_1,...,Q_4)
```

is generically finite and separable: its inverse problem is governed by the irreducible mass quintic and the descended boost data. Hence its Jacobian has generic rank five.

At `a=0`, the full Jacobian is block triangular because `M,Q_i` are independent of `a`, while

```text
partial J/partial a = m(Pi_c-Pi_s) != 0
```

generically. The full map therefore has generic rank six and is dominant. Consequently `M,Q_1,...,Q_4,J` are algebraically independent coordinates on the observable function field, so the use of the purely transcendental extension `F(J)` is justified.

## 5. Single-horizon generation survives rotation

Define normalized horizons

```text
S_hat_+ = S_+/pi,
S_hat_- = S_-/pi.
```

Then

```text
y = S_hat_+ + S_hat_-,
z = S_hat_+ - S_hat_-,
S_hat_+ S_hat_- = P+4J^2 in F_J.              (5.1)
```

Because the product in (5.1) is a nonzero element of the base field,

```text
S_hat_- = (P+4J^2)/S_hat_+.
```

Hence `S_hat_+` recovers `S_hat_-`, and therefore recovers `y` and `z`. By (H4),

```text
K_J = F_J(gamma) = F_J(y^2),
```

so

```text
K_J subseteq F_J(S_hat_+).
```

It follows that

```text
F_J(S_hat_+)
 = F_J(S_hat_+,S_hat_-)
 = K_J(y,z)
 = H_J.                                        (5.2)
```

The same argument applies with the signs reversed. Therefore:

### Corollary 5.1 — rotating single-horizon generation

```text
F_J(S_hat_+) = F_J(S_hat_-) = H_J,

[F_J(S_hat_+):F_J]
  = [F_J(S_hat_-):F_J]
  = 20.
```

Thus R19 is stable under rotation.

## 6. Axial–horizon decoupling

The field `H_J` is the full ordered-horizon field, but it does not generically contain `sqrt(u)`. Indeed, Theorem 3.1 shows

```text
[L_J:H_J] = 2.
```

This isolates three independent quadratic characters over `K_J`:

| Square class | Radical | Geometric/physical role |
|---|---|---|
| `[u]` | `m=sqrt(u)` | axial sign cover |
| `[gamma]` | `y=sqrt(gamma)` | entropy-sum sign |
| `[delta_J]` | `z=sqrt(delta_J)` | ordered-horizon swap |

The horizon swap fixes `y` and sends `z` to `-z`. The axial involution sends `m` to `-m`. For transcendental `J`, these are independent automorphisms of the augmented field `L_J`.

At `J=0`, equation (3.5) ties the signs together:

```text
z = 2 beta m/y.
```

Holding `y` fixed, the axial sign change then forces `z` to change sign. This recovers the static identification of axial reflection with horizon swap.

Rotation therefore produces a precise symmetry separation:

> The static coincidence between axial reflection and horizon swap is a rank-two specialization of a rank-three rotating Kummer cover.

## 7. Scope and proof guardrails

1. **The degree-40 field is not the ordered-horizon field.** The rotating ordered-horizon field is `H_J`, of degree 20. Degree 40 belongs to the augmented field `L_J` after independently adjoining `sqrt(u)`.
2. **Use fiber language at `J=0`.** Evaluation at `J=0` is taken in an integral model over the `J`-line. The degree-eight generic Kummer algebra has a reducible special fiber `E x E`; it does not become a single degree-four algebra without selecting a component.
3. **Retain branch-compatible square roots.** In particular, `sqrt(B)=4m^2 Pi_s` is an algebraic branch choice and need not be the principal real square root for signed charge configurations.
4. **Keep (H4) explicit.** The equality `K=F(gamma)` is required for the single-horizon reconstruction statement, though not for the rank-three Kummer calculation itself.
5. **Do not promote closure monodromy.** The normal-closure Galois group over `F(J)` remains open. The theorem determines only the displayed relative Kummer groups and degrees.
6. **Generic versus specialized rotation.** The private-prime proof treats `J` as transcendental. Particular algebraic values of `J`, including additional rank-drop fibers, require separate specialization checks.

## 8. Program consequences

The result supports the following updates after audit and canonical integration:

```text
R13  rotating entropy obstruction:
     promote the generic field-degree and reconstruction component to ESTABLISHED;
     leave rotating closure monodromy open.

R19  single-horizon generation:
     promote to J-STABLE.

E-003 axial reflection realizes horizon swap:
     label explicitly STATIC;
     add the rotating decoupling theorem as its generic extension.
```

The strongest paper-level statement is:

> **Axial–horizon decoupling theorem.** The generic rotating four-charge ordered-horizon field is a degree-20 biquadratic extension of the same non-Galois quintic mass field as in the static theory, and either horizon entropy generates it. Adjoining the axial square root produces a degree-40 elementary Kummer extension. Its `J=0` fiber splits into two branch-compatible copies of the static degree-20 crown, where axial reflection and horizon swap coincide.

## 9. Final assessment

The proposed track is correct after the explicit addition of entropy-sum primitivity and the split-fiber correction. Its main value is not another degree computation. It identifies rotation as a deformation that separates two deck symmetries which are accidentally identified in the static limit.
