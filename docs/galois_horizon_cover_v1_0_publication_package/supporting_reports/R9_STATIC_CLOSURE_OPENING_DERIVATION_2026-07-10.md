# R9 Static Closure Monodromy — Full Kummer-Wreath Proof

**Date:** 2026-07-10  
**Version:** v0.2 — formal-model and normal-closure audit incorporated  
**Target:** Normal closure of the static four-charge ordered-horizon field  
**Status:** Internal proof complete; ready for independent counter-audit and canonical promotion  
**Verdict:** The signed-contact valuation data force the maximal group

```text
Gal(H_tilde/F) ~= (C_2^2)^5 semidirect S_5 = C_2^2 wreath S_5,
|Gal(H_tilde/F)| = 2^10 * 120 = 122880.
```

The proof is geometric and Kummer-theoretic. It does not require a degree-20 resolvent or a census of transitive subgroups of `S_20`.

## 1. Banked inputs

Let

```text
F = Q(M,N_1,N_2,N_3,N_4),
K = F(u),
```

where `u=m^2` satisfies the irreducible four-charge mass quintic `N_4(U)`. The following are already established:

```text
[K:F] = 5,
Gal(E/F) = S_5,
```

where `E` is the splitting field of `N_4`.

The static ordered-horizon field is

```text
H = K(sqrt(u),sqrt(gamma)),
```

where

```text
gamma = 2(alpha+P),
P = product_i N_i,
gamma(gamma-4P) = 4u beta^2.                  (1.1)
```

The degree-20 crown certificate proves that `[u]` and `[gamma]` are independent in `K^*/K^{*2}`.

The generic incidence-normalization theorem supplies regular descended channel radicals `w_i` on each mass sheet, and therefore regular functions `alpha`, `beta`, and `gamma` at the finite signed contact divisors considered below.

## 2. The normal closure as a conjugate Kummer extension

Label the five roots of the mass quintic in `E` by

```text
u_1,...,u_5.
```

Because `gamma` and `beta` are elements of `K`, their five conjugates are

```text
gamma_i = gamma(u_i),
beta_i  = beta(u_i),
```

and each conjugate satisfies

```text
gamma_i(gamma_i-4P) = 4u_i beta_i^2.          (2.1)
```

### Lemma 2.1 — normal-closure equality

The normal closure of `H/F` is

```text
H_tilde = E(
    sqrt(u_1),...,sqrt(u_5),
    sqrt(gamma_1),...,sqrt(gamma_5)
).                                             (2.2)
```

#### Proof

Let `N` be the normal closure of `H/F` in a fixed algebraic closure. Since `K subset H`, the field `N` contains the normal closure `E` of `K/F`. Every `F`-embedding of `H` restricts to one of the five embeddings of `K`, and therefore sends

```text
u -> u_i,
gamma -> gamma_i,
sqrt(u) -> +/-sqrt(u_i),
sqrt(gamma) -> +/-sqrt(gamma_i).
```

Hence `N` contains every radical displayed in (2.2), so `H_tilde subseteq N`.

Conversely, any `F`-embedding of the field on the right of (2.2) permutes the roots `u_i`, hence permutes the `gamma_i`, and sends each displayed square root to one of the two displayed square roots above the corresponding conjugate. Its image is therefore the same field. Thus the right side of (2.2) is normal and separable over `F`; it contains `H`, so `N subseteq H_tilde`. Equality follows. ∎

Define the `S_5`-stable Kummer module

```text
W = span_F2 {
      [u_1],...,[u_5],
      [gamma_1],...,[gamma_5]
    }
    subset E^*/E^{*2}.                         (2.3)
```

R9 reduces to computing `dim_F2 W`.

### 2.2 Localized integral model

Put

```text
R_0 = Q[M,N_1,N_2,N_3,N_4].
```

Choose the primitive polynomial `f(U) in R_0[U]` representing the mass quintic, with leading coefficient `a`, and write `Delta=disc_U(f)`. For the two sign vectors used below define

```text
epsilon^+ = (+1,+1,+1,+1),
epsilon^- = (-1,+1,+1,+1),

c_+ = P sum_i epsilon_i^+/N_i,
c_- = P sum_i epsilon_i^-/N_i.
```

These are nonzero polynomials in the `N_i`. Localize `R_0` by inverting

```text
2aP Delta c_+ c_- product_{i<j}(N_i^2-N_j^2),
```

and call the resulting regular UFD `R`. After dividing by the unit `a`, the polynomial `f` is monic, and

```text
A = R[U]/(f)
```

is a finite étale domain of rank five over `R`; its fraction field is `K`.

The descended channel elements belong to `A`, not merely to its fraction field. Indeed, each `w_r in K` satisfies the monic equation

```text
X^2-(U+N_r^2)=0
```

over `A`, so it is integral over `A`. A finite étale algebra over the normal ring `R` is normal; since `A` is a domain, it is integrally closed in `K`, and therefore `w_r in A`. It follows that `alpha`, `beta`, and `gamma`, being polynomial expressions in `U`, the `w_r`, and the base parameters, are regular elements of `A`.

Let `S` be the integral closure of `R` in the splitting field `E`. Because `Delta` is inverted, `S/R` is finite étale. The five embeddings `A -> S` give regular elements

```text
u_i, beta_i, gamma_i in S.
```

This supplies the integral model required for every valuation used below and rules out hidden poles of the conjugate radicands.

## 3. Signed contact divisors

For a sign vector `epsilon=(epsilon_1,...,epsilon_4)`, put

```text
ell_epsilon = 4M-sum_i epsilon_i N_i,
s_epsilon   = product_i epsilon_i.
```

At the corresponding contact component, the distinguished branch satisfies

```text
u = 0,
w_i = epsilon_i N_i.
```

The local incidence expansion is

```text
w_i = epsilon_i N_i
      +(epsilon_i/(2N_i))u
      +O(u^2),

ell_epsilon
  = (u/2) sum_i epsilon_i/N_i + O(u^2).        (3.1)
```

Away from the reciprocal sub-balance locus

```text
sum_i epsilon_i/N_i = 0,
```

equation (3.1) shows that `u` has order one on the contact divisor.

At `u=0`,

```text
alpha = s_epsilon P,
beta  = s_epsilon P sum_i epsilon_i/N_i,
gamma = 2P(1+s_epsilon).                      (3.2)
```

Hence:

| Contact parity | `gamma mod ell_epsilon` | Odd valuations on the distinguished sheet |
|---|---|---|
| `s_epsilon=+1` | `4P` | `v(u)=1`, `v(gamma)=0` |
| `s_epsilon=-1` | `0` | `v(u)=1`, `v(gamma)=1` |

The second row uses (2.1), `beta` a unit, and `gamma-4P` a unit.

## 4. The unramified-wall lemma

### Lemma 4.1

There exist an even signed contact divisor and an odd signed contact divisor whose generic points do not lie on the mass-quintic discriminant. Consequently their valuations are unramified in `E/F`.

### Exact witnesses

Take

```text
N = (4,8,12,20),     P=7680.
```

#### Even wall: all-plus

The wall equation is

```text
4M = 4+8+12+20 = 44,
M = 11.
```

The exact specialized mass polynomial has coefficients, low power first,

```text
[
0,
15319222242508800,
-216521474310144,
1095834792448,
-2342574641,
1771561
].
```

Thus `U` divides the polynomial exactly once, and an exact gcd with its derivative is `1`. The full quintic is separable on this wall specialization. Moreover

```text
sum_i 1/N_i = 61/120,
beta_contact = P*(61/120) = 3904 != 0.
```

#### Odd wall: one minus sign

Choose `epsilon=(-1,+1,+1,+1)`. The wall equation is

```text
4M = -4+8+12+20 = 36,
M = 9.
```

The exact specialized mass polynomial has coefficients

```text
[
0,
-8878502707200,
-3620457938944,
66987813888,
-353250801,
531441
].
```

Again `U` divides exactly once and the exact polynomial gcd with the derivative is `1`. Also

```text
-1/4+1/8+1/12+1/20 = 1/120,
beta_contact = -P*(1/120) = -64 != 0.
```

Since the quintic discriminant is nonzero at one rational point on each wall, neither wall equation divides the generic discriminant. Therefore the generic point of each wall is outside the mass branch divisor. The corresponding discrete valuations of `F` are unramified in the splitting field `E`. ∎

## 5. Valuations in the splitting field

Fix one of the two base-wall valuations from Lemma 4.1 and a prolongation to `E`.

Because the reduced quintic has one simple root `U=0` and four distinct nonzero roots, exactly one labelled root `u_i` has positive valuation at that prolongation. Unramifiedness and the simple wall factor give

```text
v(u_i)=1,
v(u_j)=0 for j!=i.                            (5.1)
```

The Galois group `S_5` acts transitively on the prolongations above the fixed base divisor. Thus, for every label `i`, there is a prolongation at which (5.1) holds with that prescribed `u_i` as the unique vanishing root.

For the distinguished root, equations (3.2) give the parity stated in Section 3.

For `j!=i`, the element `u_j` is a unit. The functions `gamma_j` and `beta_j` are regular at these finite incidence points. If `gamma_j` is a unit, its valuation is zero. If it vanishes, then `gamma_j-4P` is a unit and (2.1) gives

```text
v(gamma_j)=2v(beta_j),
```

which is even. Therefore every non-distinguished `gamma_j` has zero valuation modulo two.

## 6. The rank-10 valuation matrix

For each `i=1,...,5`, choose prolongations

```text
v_i^+  above the even wall,
v_i^-  above the odd wall,
```

such that `u_i` is the unique vanishing mass root.

Order the ten square-class columns as

```text
u_1,...,u_5, gamma_1,...,gamma_5.
```

Modulo two, the valuation rows are

```text
v_i^+ : (e_i | 0),
v_i^- : (e_i | e_i),                          (6.1)
```

where `e_i` is the `i`th standard basis vector of `F_2^5`.

Stacking the five even rows and five odd rows gives

```text
V = [ I_5  0  ]
    [ I_5  I_5].                              (6.2)
```

This matrix is invertible over `F_2`; subtracting the first block row from the second reduces it to `diag(I_5,I_5)`. Hence

```text
rank_F2 V = 10.
```

Any square-class relation among the ten radicands would be annihilated by every discrete valuation and therefore would give a vector in the kernel of `V`. Since `V` has trivial kernel, no nontrivial relation exists.

### Theorem 6.1 — full conjugate Kummer rank

```text
dim_F2 W = 10.                                 (6.3)
```

Equivalently,

```text
Gal(H_tilde/E) ~= (C_2)^10.                    (6.4)
```

## 7. Solution of R9

Every element of `Gal(H_tilde/F)` restricts to a permutation `sigma in S_5` of the mass roots and acts on the quadratic generators by

```text
sqrt(u_i)     -> +/- sqrt(u_{sigma(i)}),
sqrt(gamma_i) -> +/- sqrt(gamma_{sigma(i)}).
```

This gives an injective homomorphism

```text
Gal(H_tilde/F)
  -> (C_2^2)^5 semidirect S_5
   = C_2^2 wreath S_5.                         (7.1)
```

By Theorem 6.1,

```text
[H_tilde:E] = 2^10,
[E:F]       = 120,
```

so

```text
|Gal(H_tilde/F)| = 2^10*120 = 122880.          (7.2)
```

The target wreath product in (7.1) has the same order. Therefore the injection is an isomorphism.

### Theorem 7.1 — static full closure group

```text
Gal(H_tilde/F)
  ~= (C_2^2)^5 semidirect S_5
   = C_2^2 wreath S_5,

|Gal(H_tilde/F)| = 122880.                     (7.3)
```

On the twenty conjugates of one normalized horizon entropy, the group acts imprimitively with five mass-sheet blocks of size four. The `S_5` quotient permutes the five blocks, and the independent `V_4` factor in each block acts regularly on

```text
{S_+, S_-, -S_+, -S_-}
```

for that mass sheet.

## 8. Formal audit discharge

The proof-writing gates in the opening version are now discharged internally:

| Gate | Resolution |
|---|---|
| Regular localized model | Section 2.2 constructs `R`, the finite étale quintic algebra `A`, and the splitting model `S`; integrality puts all descended channel elements and their conjugates in these rings. |
| Contact primes survive localization | The exact even and odd witnesses in Section 4 show `Delta` is not divisible by either wall equation; hence both height-one wall primes remain in `Spec R`. |
| Odd valuations survive in `E` | `S/R` is finite étale, so prolongations of the selected wall valuations have ramification index one. |
| Normal-closure equality | Lemma 2.1 proves both inclusions in (2.2). |
| Kernel rank | The invertible matrix (6.2) proves rank ten without a computational group census. |
| Extension structure | The faithful signed-permutation action and order equality prove the full wreath product, not merely an extension with the same quotient and kernel. |

The result should still receive an independent counter-audit before the research map is edited, but no unresolved lemma remains inside the present proof.

Two scope fences remain deliberate:

1. The theorem is static. The rotating ordered-horizon closure uses conjugates of `[gamma]` and `[delta_J]`; the augmented rotating closure adds conjugates of `[u]`.
2. The group is `C_2^2 wreath S_5`, not `C_2 wreath S_5`: each mass sheet carries a `V_4` block.

## 9. Wreath-lifting principle and the all-k interface

The rank argument separates cleanly from the identification of the base monodromy group.

### Proposition 9.1 — two-radicand wreath lift

Let `f` be an irreducible separable polynomial of degree `d` over a characteristic-zero field `F`, let `E` be its splitting field, and let `G=Gal(E/F)` act transitively on the roots `a_1,...,a_d`. Let `b_i` be a conjugate family in `E^*`. Suppose there are two unramified base valuations such that, after choosing suitable prolongations for every label `i`, the parity rows on

```text
a_1,...,a_d,b_1,...,b_d
```

are

```text
(e_i | 0),
(e_i | e_i).
```

Then the `2d` square classes `[a_i],[b_i]` are independent and the normal closure of one decorated sheet `F(a_1)(sqrt(a_1),sqrt(b_1))` has group

```text
(C_2^2)^d semidirect G.                       (9.1)
```

#### Proof

The stacked valuation matrix is

```text
[ I_d  0  ]
[ I_d  I_d],
```

which is invertible over `F_2`. Kummer theory gives kernel `(C_2)^(2d)`. The normal closure acts faithfully by independent signs within the `d` conjugate pairs and by the permutation action of `G` on those pairs. Its order equals that of `(C_2^2)^d semidirect G`, so the faithful inclusion is an equality. ∎

The R9 theorem is Proposition 9.1 with

```text
d=5,
a_i=u_i,
b_i=gamma_i,
G=S_5.
```

Importantly, the rank-ten proof uses only irreducibility/transitivity of the mass cover. The `S_5` theorem is needed only to identify the quotient and hence name the final group as the full symmetric wreath product.

Your nearly complete all-`k` monodromy theorem therefore plugs into a reusable architecture:

```text
all-k symmetric base monodromy
    + a realization with two parity-separated radical channels
    + unramified contact walls
    => maximal two-radical wreath closure.
```

This is a conditional general mechanism, not yet an all-`k` horizon theorem: beyond four charges one must first supply the relevant decorated radicands and their two valuation types.

## 10. Consequences and next branch

The next closure problem is rotating:

```text
W_rot = span_F2 {
  [u_i], [gamma_i], [delta_{J,i}] : i=1,...,5
}.
```

The private-prime argument for `delta_J` suggests

```text
dim_F2 W_rot = 15,
```

which would give the augmented rotating closure candidate

```text
(C_2^3)^5 semidirect S_5 = C_2^3 wreath S_5.
```

The rotating ordered-horizon closure itself omits `[u_i]` and should retain a rank-10 kernel. Those statements are predictions only; they are not part of the present static proof.

## 11. Bottom line

The parity-resolved crown certificate already contained the missing R9 mechanism. Passing its even and odd contact valuations through the unramified `S_5` splitting field produces ten independent rows for the ten conjugate Kummer radicands. The resulting kernel is maximal, and the known `S_5` quotient then forces the full wreath product.

The internal proof of the static closure group is complete. Its central mechanism is the general two-radicand wreath lift of Proposition 9.1; the four-charge crown supplies the required parity-separated divisors, and the known `S_5` mass monodromy supplies the quotient.
