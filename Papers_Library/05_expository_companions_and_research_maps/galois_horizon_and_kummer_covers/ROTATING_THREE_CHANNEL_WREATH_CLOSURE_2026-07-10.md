# Rotating Three-Channel Wreath Closure

**Date:** 2026-07-10  
**Status:** Internal proof complete; ready for independent counter-audit  
**Purpose:** Close the generic rotating normal-closure problem using the conjugate Kummer-module theorem  
**Depends on:** Static R9 valuation dossier, entropy-sum primitivity, rotating rank-jump lemma, and generic base group `S_5`

## 1. Result

Let

```text
F   = Q(M,N_1,N_2,N_3,N_4),
K   = F(u),
F_J = F(J),
K_J = K(J),
```

where `N_i=4Q_i` and `u` satisfies the irreducible four-charge mass quintic. The fields written with the `N_i` or the `Q_i` are identical because `4` is invertible in `Q`.

Let `E/F` be the splitting field of the quintic. Banked results give

```text
[K:F]=5,
Gal(E/F)=S_5,
K=F(gamma).
```

Put

```text
delta_J = gamma-4P-16J^2,
P       = product_i N_i.
```

Then the normal closure of the rotating ordered-horizon field

```text
H_J = K_J(sqrt(gamma),sqrt(delta_J))
```

has group

```text
Gal(H_J_tilde/F_J)
  ~= (C_2^2)^5 semidirect S_5
   = C_2^2 wreath S_5,                       (1.1)

|Gal(H_J_tilde/F_J)|
  = 2^10*120
  = 122880.                                  (1.2)
```

The normal closure of the augmented axial--horizon field

```text
L_J = K_J(sqrt(u),sqrt(gamma),sqrt(delta_J))
```

has group

```text
Gal(L_J_tilde/F_J)
  ~= (C_2^3)^5 semidirect S_5
   = C_2^3 wreath S_5,                       (1.3)

|Gal(L_J_tilde/F_J)|
  = 2^15*120
  = 3932160.                                 (1.4)
```

Thus rotation preserves the abstract closure group of the ordered-horizon field while changing its two Kummer channels from `{u,gamma}` to `{gamma,delta_J}`. The independently adjoined axial channel produces the genuine rank-three wreath lift.

## 2. Conjugate radicands

Label the five embeddings of `K` into `E` by `i=1,...,5`, and write

```text
u_i     = i(u),
gamma_i = i(gamma),
beta_i  = i(beta),

delta_i = gamma_i-4P-16J^2 in E[J].          (2.1)
```

The static identity transports to every sheet:

```text
gamma_i(gamma_i-4P)=4u_i beta_i^2.           (2.2)
```

The entropy-sum primitive-element theorem `K=F(gamma)` implies that

```text
gamma_i != gamma_j for i!=j.                 (2.3)
```

The standing nonvanishing hypotheses give

```text
u_i != 0,
gamma_i != 0,
beta_i != 0,
gamma_i-4P != 0.                             (2.4)
```

For the final assertion, use (2.2): its right side is nonzero, hence both factors on its left are nonzero.

Set

```text
E_J=E(J).
```

Pure transcendental base extension preserves the splitting-field group:

```text
Gal(E_J/F_J)=S_5.                             (2.5)
```

## 3. The static contact rows survive rotation

The R9 dossier supplies, for every sheet `i`, geometric discrete valuations

```text
v_i^+  from an even signed contact wall,
v_i^-  from an odd signed contact wall,
```

whose parity rows on the static conjugate radicands are

```text
v_i^+ : (e_i | 0),
v_i^- : (e_i | e_i)                          (3.1)
```

on the columns `(u_1,...,u_5 | gamma_1,...,gamma_5)`.

These valuations are trivial on `Q^*`, and the R9 integral model makes every `gamma_j-4P` regular at the selected walls. Extend each valuation to the Gauss valuation on `E(J)` by

```text
v_hat(sum_n a_n J^n)=min_n v(a_n).           (3.2)
```

Because the coefficient of `J^2` in every `delta_j` is the unit `-16`,

```text
v_hat_i^+(delta_j)=0,
v_hat_i^-(delta_j)=0                         (3.3)
```

for all `i,j`. Therefore the rotating three-channel parity rows are

```text
v_hat_i^+ : (e_i | 0   | 0),
v_hat_i^- : (e_i | e_i | 0).                 (3.4)
```

No cancellation is possible in (3.2): the constant and quadratic terms have different powers of the indeterminate `J`.

## 4. Private-prime lemma

### Lemma 4.1

For each sheet `i`, there is a height-one prime `q_i` of `E[J]` such that

```text
v_{q_i}(delta_i)=1,
v_{q_i}(delta_j)=0        for j!=i,
v_{q_i}(u_j)=0,
v_{q_i}(gamma_j)=0       for every j.        (4.1)
```

The five primes `q_i` may be chosen pairwise distinct.

#### Proof

First, `delta_i` is squarefree as a polynomial in `J`. Its derivative is

```text
partial delta_i/partial J=-32J.
```

If `J` divided `delta_i`, then its constant term `gamma_i-4P` would vanish, contrary to (2.4). Hence

```text
gcd(delta_i,partial delta_i/partial J)=1.     (4.2)
```

Choose any irreducible factor `q_i` of `delta_i` in the PID `E[J]`. Equation (4.2) shows that it occurs with multiplicity one, so

```text
v_{q_i}(delta_i)=1.                          (4.3)
```

For `i!=j`,

```text
delta_i-delta_j=gamma_i-gamma_j in E^*.      (4.4)
```

By (2.3), the right side is a nonzero constant and hence a unit of `E[J]`. Thus `delta_i` and `delta_j` are coprime. No factor `q_i` of `delta_i` divides any `delta_j`, proving the second assertion in (4.1) and also proving that primes chosen for distinct sheets are distinct.

Finally, every `u_j` and `gamma_j` is a nonzero element of the coefficient field `E`, hence a unit at every polynomial prime of `E[J]`. Their `q_i`-valuations are zero. ∎

### Important strengthening

The lemma does **not** require `delta_i` to be irreducible over `E`. It may remain quadratic or split into two linear factors. Squarefreeness and pairwise coprimeness are sufficient. This removes the unjustified step of trying to transport nonsquareness from `K` into its normal closure `E`.

Modulo two, the five private-prime rows are therefore

```text
v_{q_i} : (0 | 0 | e_i).                     (4.5)
```

## 5. Rank-fifteen valuation matrix

Order the fifteen conjugate square classes as

```text
u_1,...,u_5,
gamma_1,...,gamma_5,
delta_1,...,delta_5.
```

Stack the five even contact rows, five odd contact rows, and five private-prime rows. By (3.4) and (4.5), the parity matrix is

```text
V_rot = [ I_5  0    0  ]
        [ I_5  I_5  0  ]
        [ 0    0    I_5].                    (5.1)
```

It is invertible over `F_2`. Subtracting the first block row from the second gives the identity in block-diagonal form. Therefore

```text
rank_F2 V_rot=15.                             (5.2)
```

By the valuation-separation theorem, the fifteen classes

```text
[u_i], [gamma_i], [delta_i],  i=1,...,5
```

are independent in `E_J^*/E_J^{*2}`. Consequently

```text
Gal(L_J_tilde/E_J)~=(C_2)^15.                (5.3)
```

## 6. Rank ten for the ordered-horizon closure

The ordered-horizon field uses only the conjugate families `[gamma_i]` and `[delta_i]`. Restrict the valuation data to those ten columns and retain the five odd contact rows and five private-prime rows. The resulting matrix is

```text
V_hor = [ I_5  0  ]
        [ 0    I_5],                         (6.1)
```

so

```text
rank_F2 V_hor=10.                             (6.2)
```

Thus the ten classes

```text
[gamma_i], [delta_i],  i=1,...,5
```

are independent, and

```text
Gal(H_J_tilde/E_J)~=(C_2)^10.                (6.3)
```

This global calculation is stronger than the sheetwise rank-jump lemma: that lemma proves rank two for one ordered-horizon sheet and rank three after adding `sqrt(u)`; the present matrices prove that all five conjugate copies remain simultaneously independent over the splitting field.

## 7. Normal-closure groups

The conjugate Kummer-module theorem identifies the normal closures as

```text
H_J_tilde
  = E_J(
      sqrt(gamma_i),sqrt(delta_i):1<=i<=5
    ),                                        (7.1)

L_J_tilde
  = E_J(
      sqrt(u_i),sqrt(gamma_i),sqrt(delta_i):1<=i<=5
    ).                                        (7.2)
```

Every automorphism acts by a permutation of the five sheets together with signs on the radical channels. Hence there are faithful signed-permutation representations

```text
Gal(H_J_tilde/F_J) -> C_2^2 wreath S_5,
Gal(L_J_tilde/F_J) -> C_2^3 wreath S_5.       (7.3)
```

Equations (5.3), (6.3), and (2.5) show that the source and target orders agree in each line. Both injections are therefore isomorphisms, proving (1.1)--(1.4).

## 8. Sheet degrees versus closure degrees

The rotating rank-jump lemma remains unchanged:

```text
[H_J:K_J]=4,
[H_J:F_J]=20,

[L_J:K_J]=8,
[L_J:F_J]=40.                                (8.1)
```

These are degrees of one decorated mass sheet. They must not be confused with the orders of the normal-closure groups:

| Object | Degree over observable field | Normal-closure group |
|---|---:|---|
| rotating ordered-horizon field `H_J` | `20` | `C_2^2 wreath S_5` |
| augmented axial--horizon field `L_J` | `40` | `C_2^3 wreath S_5` |

## 9. The `J=0` boundary

The generic theorem is over `F(J)`. At `J=0`, the sheetwise relation

```text
[delta_0]=[u][gamma]
```

returns, and the rank-three augmented Kummer algebra has the split special fiber described in the rotating rank-jump lemma. After selecting either branch-compatible component, one recovers the static crown and its normal closure

```text
C_2^2 wreath S_5.                             (9.1)
```

Therefore the generic augmented closure group does not specialize as a constant finite group of the same order: the `J=0` divisor is a genuine Kummer-rank-drop locus. The ordered-horizon closure has the same abstract wreath group on the generic rotating fiber and on the selected static component, but its channel interpretation changes.

## 10. Proof gates and status

| Gate | Resolution |
|---|---|
| Base `S_5` survives adjoining `J` | Purely transcendental base extension, equation (2.5) |
| Static valuation rows remain usable | Gauss extensions give the rows (3.4) |
| Third column is zero on contact walls | The coefficient `-16` of `J^2` is a valuation unit |
| Private primes exist | Squarefreeness of each `delta_i`, Lemma 4.1 |
| Private primes distinguish sheets | `delta_i-delta_j=gamma_i-gamma_j` and primitivity |
| Full augmented Kummer rank | Invertible matrix (5.1) |
| Full ordered-horizon Kummer rank | Invertible matrix (6.1) |
| Wreath product rather than an unspecified extension | Faithful signed action plus order equality |

### Remaining external action

The proof is internally complete relative to the banked inputs. Before canonical promotion it should receive an independent counter-audit focused on:

1. the use of entropy-sum primitivity to guarantee (2.3);
2. the Gauss extension of the exact R9 contact valuations; and
3. the normal-closure equalities (7.1)--(7.2).

No unresolved private-prime lemma remains.

## 11. Bottom line

The rotating closure problem is controlled by the block matrix

```text
[ 1 0 0 ]
[ 1 1 0 ]
[ 0 0 1 ].
```

The first two rows are the static even/odd contact strata carried unchanged along the `J`-line. The third row is supplied by any squarefree prime factor of `gamma_i-4P-16J^2`; different sheets cannot share such a factor because their `gamma_i` are distinct.

This proves the maximal three-channel Kummer module and therefore the generic augmented rotating wreath group

```text
C_2^3 wreath S_5.
```

The rotating ordered-horizon closure is the corresponding two-channel subtheorem

```text
C_2^2 wreath S_5.
```
