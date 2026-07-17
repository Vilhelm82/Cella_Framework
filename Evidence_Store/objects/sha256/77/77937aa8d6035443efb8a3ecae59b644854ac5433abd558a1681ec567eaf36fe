# Degree-20 Crown Certificate — Audit and Strengthened Proof

**Date:** 2026-07-10  
**Target:** Static four-charge ordered-horizon field  
**Verdict:** **PASS.** The Point-B square-class certificate is independently reconstructed and exact. In addition, the generic degree-20 result admits a shorter intrinsic proof from parity valuations on the signed axial-contact divisor. The specialization argument can therefore be retained as an audit witness rather than used as the load-bearing generic proof.

## 1. Claim being certified

Let

```text
F = Q(M,N_1,N_2,N_3,N_4),
K = F(u),                    u = m^2,
w_i^2 = u + N_i^2,          sum_i w_i = 4M,
P = product_i N_i.
```

For four charges the mass norm is generically irreducible of degree five, so `[K:F]=5`. Define

```text
alpha = e_4(w) + u e_2(w) + u^2,
beta  = e_3(w) + u e_1(w),
gamma = 2(alpha + P),
y^2   = gamma.
```

The degree-20 crown is the assertion

```text
[u] and [gamma] are independent in K^*/K^{*2};
[K(sqrt(u),sqrt(gamma)):K] = 4;
[K(m,y):F] = 20.
```

In characteristic different from two, independence is equivalent to all three elements

```text
u, gamma, u*gamma
```

being nonsquares in `K`.

## 2. Exact Point-B certificate

### 2.1 Specialization data

```text
M = 15,
Q = (1,2,3,5),
N = (4,8,12,20),
4M = 60,
P = 7680.
```

This point is in the strict chamber because `60 > 4+8+12+20 = 44`. The `N_i` are nonzero and the `N_i^2` are pairwise distinct.

### 2.2 Specialized mass quintic

The exact signed-radical norm gives the primitive integer quintic

```text
N_B(u) =
  11390625 u^5
- 34962080625 u^4
+ 40515442790400 u^3
- 21548253194223616 u^2
+ 4906654632404582400 u
- 292521804394659840000.
```

Modulo `29`, its monic reduction, listed low coefficient first, is

```text
[28, 28, 7, 10, 17, 1].
```

The exact Rabin test returns

```text
gcd(f, x^29 - x) = 1,
x^(29^5) - x = 0 mod f.
```

Therefore the reduction is irreducible of degree five. Hence `N_B` is irreducible over `Q`; it is also separable, and

```text
K_B = Q[u]/(N_B),       [K_B:Q] = 5.
```

### 2.3 Entropy element

In the monic quotient presentation of `K_B`, the reconstructed element `gamma` has coefficients, low power first,

```text
[
  7092451981243392/24507764213,
  15547544077436543/20218905475725,
 -349218144409977/483097048166656,
 -1471032978009075/494691377322655744,
  494116351875/494691377322655744
].
```

The reconstruction denominator is coprime to `N_B`. Exact quotient-ring checks establish

```text
e_4(w)^2 = product_i (u+N_i^2),
alpha^2 - u beta^2 = P^2,
gamma = 2(alpha+P).
```

Moreover

```text
Norm_{K_B/Q}(beta) = 13384016229040128000 != 0,
```

so `beta` is nonzero at Point B.

### 2.4 Kummer square-class witnesses

The exact rational norms factor as follows:

```text
Norm(u)
  = 2^38 * 7^2 * 11 * 13 / (3 * 5^2),

Norm(gamma)
  = 2^52 * 3^2 * 5^2 * 7^3 * 11 * 617^2,

Norm(u*gamma)
  = 2^90 * 3 * 7^5 * 11^2 * 13 * 617^2.
```

Thus

```text
v_3(Norm(u))       = -1,
v_7(Norm(gamma))   =  3,
v_3(Norm(u*gamma)) =  1.
```

None of the three norms is a rational square. If an element of `K_B` were a square, its rational norm would be a square. Consequently

```text
u, gamma, and u*gamma are nonsquares in K_B.
```

Therefore `[u]` and `[gamma]` are independent and

```text
[K_B(m,y):K_B] = 4,
Gal(K_B(m,y)/K_B) = V_4,
[K_B(m,y):Q] = 20.
```

This independently closes the old “Entry 4” certificate gate.

## 3. Stronger generic proof by contact-wall parity

The Point-B certificate is sufficient, subject to the usual good-specialization lemma. It is not necessary. The geometry of the signed contact walls proves independence directly over the generic field.

### 3.1 Signed contact divisors

For a sign vector `epsilon = (epsilon_1,...,epsilon_4)` define

```text
ell_epsilon = 4M - sum_i epsilon_i N_i,
s_epsilon   = product_i epsilon_i in {+1,-1}.
```

On the corresponding branch above `u=0`,

```text
w_i = epsilon_i N_i
      + (epsilon_i/(2N_i)) u
      + O(u^2).
```

The incidence equation gives

```text
ell_epsilon
  = (u/2) sum_i epsilon_i/N_i + O(u^2).
```

At the generic point of this wall, `sum_i epsilon_i/N_i != 0`. Hence the wall is transverse and its discrete valuation satisfies

```text
v_epsilon(u) = 1.
```

This is already a direct generic witness that `u` is not a square in `K`.

### 3.2 The decisive identity

Set

```text
A = product_i(w_i+m) = alpha + m beta,
B = product_i(w_i-m) = alpha - m beta.
```

Since `AB=P^2`, one has

```text
alpha^2 - u beta^2 = P^2.
```

With `gamma=2(alpha+P)`, this becomes

```text
gamma (gamma - 4P) = 4u beta^2.              (Crown identity)
```

At `u=0` on the `epsilon` wall,

```text
alpha = e_4(w) = s_epsilon P,
beta  = s_epsilon P sum_i epsilon_i/N_i,
gamma = 2P(1+s_epsilon).
```

Because `P` and `beta` are units at the generic point, the crown identity gives the exact parity table:

| Sign parity | `v(u)` | `v(gamma)` | `v(gamma-4P)` | `v(u*gamma)` |
|---|---:|---:|---:|---:|
| `s_epsilon=+1` (even number of minus signs) | 1 | 0 | 1 | 1 |
| `s_epsilon=-1` (odd number of minus signs) | 1 | 1 | 0 | 2 |

Choose one even-parity wall and one odd-parity wall. Then:

```text
u is nonsquare:       v_even(u)       = 1;
gamma is nonsquare:   v_odd(gamma)    = 1;
u*gamma is nonsquare: v_even(u*gamma) = 1.
```

Squares have even valuation at every prime divisor. Hence `[u]` and `[gamma]` are generically independent, with no specialization transfer required.

### 3.3 New structural interpretation

The crown identity also identifies the third Kummer character:

```text
[gamma-4P] = [u*gamma]  in K^*/K^{*2}.
```

Indeed `gamma(gamma-4P)=4u beta^2`, and `4 beta^2` is a square. If

```text
m^2 = u,
y^2 = gamma,
z^2 = gamma-4P,
yz  = 2m beta,
```

then the three quadratic subextensions of the crown are represented by

```text
K(m) : [u],
K(y) : [gamma],
K(z) : [u*gamma].
```

Among the sixteen signed axial-contact components:

```text
all 16 walls witness the axial class [u];
the 8 odd-parity walls witness the entropy-sum class [gamma];
the 8 even-parity walls witness the entropy-difference class [u*gamma].
```

The physical all-plus BPS wall has even parity. Accordingly `z=S_+-S_-` vanishes there while `y=S_++S_-` remains nonzero. The odd-parity walls are shadow-sector components on which the entropy sum, rather than the entropy difference, vanishes.

This is stronger than a degree count: sign parity resolves the branch characters of the `V_4` crown.

## 4. Ordered-horizon field

Use normalized horizon entropies

```text
S_hat_+ = S_+/pi,
S_hat_- = S_-/pi,
y = S_hat_+ + S_hat_-,
z = S_hat_+ - S_hat_-.
```

The identities

```text
S_hat_+ = (y+z)/2,
S_hat_- = (y-z)/2,
z = 2m beta/y
```

give

```text
F(S_hat_+,S_hat_-) subseteq K(m,y).
```

Conversely, `y^2=gamma`, `K=F(gamma)`, and `beta!=0` imply

```text
K subseteq F(S_hat_+,S_hat_-),
m = yz/(2beta) in F(S_hat_+,S_hat_-).
```

Therefore

```text
F(S_hat_+,S_hat_-) = K(m,y).
```

Since `S_hat_+ S_hat_- = P` lies in `F`, either nonzero horizon alone recovers the other. Thus, generically,

```text
[F(S_hat_+):F] = [F(S_hat_-):F] = 20.
```

## 5. Independent degree-20 annihilator

For `t=m+y`, the four conjugates over `K` satisfy

```text
q_u(t) = (t^2-u-gamma)^2 - 4u gamma.
```

Square-class independence makes `q_u` irreducible of degree four over `K`. The exact norm

```text
F_B(t) = Norm_{K_B/Q}(q_u(t))
```

is a degree-20 annihilator. Its primitive integer coefficients, low power first, are

```text
[
288069676593994546546445848979887430052763157470109130814012784640000,
0,
19385946370033462376826664716649448263383153979198178813018112000,
0,
427552396466850480558278065051910916848602741996339907788800,
0,
2890320390159071471173781268422247837186217560149852160,
0,
1390800897739257627264608629802218188664635129856,
0,
-45011443031675745509587193841599038409932800,
0,
-104488486458235320429120474826997760000,
0,
103444826166153829672744896000000,
0,
513744842767833043737890625,
0,
468744099249199218750,
0,
129746337890625
].
```

This polynomial is a cross-check, not the logical basis of the degree claim. Its irreducibility over `Q` is not asserted: degree 20 already follows from the quintic degree and Kummer independence.

## 6. Proof stops and scope boundaries

Before this is inserted into the canonical paper, stop and make the following points explicit.

1. **Formal divisor lemma.** State that each generic signed wall defines a height-one prime on the normalization and use the displayed nonzero linear coefficient to prove `ord_D(u)=1`. This is a proof-writing obligation, not a remaining computational gate.
2. **Standing open set.** Work in characteristic zero with `N_i!=0`, pairwise distinct `N_i^2`, `P!=0`, and away from the reciprocal sub-balance loci `sum epsilon_i/N_i=0`.
3. **Generic is not universal.** Exceptional specializations still need their own checks. The result is generic and Point B is one exact good specialization.
4. **Do not promote the closure group.** The field degree and `V_4` group over `K` are proved. The Galois/monodromy group of the normal closure over `F` remains R9.
5. **Do not oversell the displayed eliminant.** It is a degree-20 annihilator for `m+y`; no claim of irreducibility or primitive generation over `Q` is needed.
6. **Finite versus infinite divisors.** The parity proof resolves the finite signed axial-contact contribution on `P!=0`. Places at infinity and charge-zero boundary components remain outside this certificate.

## 7. Recommended program updates

After the formal divisor lemma is inserted and audited:

```text
R8:       promote to ESTABLISHED GENERICALLY;
PRED-004: promote from CONDITIONAL to CONFIRMED;
live-front table: remove the degree-20 certificate gate;
R9:       leave OPEN without modification.
```

Add a named result along the lines of:

> **Parity-resolved crown theorem.** On the generic four-charge axial cover, the even and odd signed contact divisors separately detect the two independent Kummer classes of the ordered-horizon lift; consequently the lift is biquadratic over the quintic field and has degree 20 over the observable field.

The Point-B norm calculation should remain in an appendix as an independent exact audit witness.

## 8. Reproducibility record

Exact checker:

```text
crown_degree20_certificate.py
```

It uses only the Python standard library and performs all polynomial, quotient-ring, determinant, finite-field, and norm arithmetic exactly.

```text
script SHA-256:
cfab6d08bef3dbaf9e11af4cf63590c20c0c7c063bdab6c6cfd33ed9155502cb

deterministic stdout SHA-256 (two consecutive runs):
acc836df89d1b8c63de7c72505b37efd7bb0476bbd244d0944cf5047392d5973
acc836df89d1b8c63de7c72505b37efd7bb0476bbd244d0944cf5047392d5973
```

## 9. Bottom line

The degree-20 crown is no longer merely a plausible transfer from a remembered Entry 4. It has:

1. an exact, independently reproducible Point-B certificate; and
2. a stronger generic proof whose mechanism is visible in the wall geometry itself.

The high-value addition is the parity-resolved branch picture: the crown is not just a biquadratic extension sitting above the quintic. Its three quadratic characters are geometrically labelled by the full, odd-parity, and even-parity signed contact arrangements.
