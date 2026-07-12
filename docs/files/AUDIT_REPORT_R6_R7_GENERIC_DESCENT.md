# Audit Report — R6 + R7 Generic Birationality and Reflection Descent

**Audited target:** `LOG_ENTRY_DRAFT_R6_R7_generic_descent.md`  
**Scope:** mathematical correctness, claim status, field-theoretic consequences, and required repairs before promotion.  
**Verdict:** The core generic proofs are valid. Promote R6 and R7 after the normalization repair in §4. The generic degree-20 ordered-horizon claim remains conditional on independent verification of the Entry 4 square-class certificate and the ordered-field identification in §8.

---

## 1. Executive conclusion

The draft establishes, under

```text
H1: N_i != 0,
H2: N_i^2 != N_j^2 for i != j,
```

the generic chain

```text
L(s) = W
    ->
Phi_k(m,M) irreducible
    ->
W = F(m)
    ->
N_k(u) irreducible over F
    ->
[K:F] = delta_k
    ->
[W:K] = 2
    ->
W^tau = K
    ->
w_i in K.
```

This genuinely closes the generic descent gap: the conclusion

```text
w_i in K
```

no longer rests on point-B evidence.

The draft also proves a new all-`k` generic minimality result:

```text
deg_F(m) = D_k,
deg_F(u) = delta_k = D_k/2,

D_k = 2^k                              for k odd,
D_k = 2^k - binom(k,k/2)               for k even.
```

Hence

```text
k=5: [F(u):F] = 16,
k=6: [F(u):F] = 22
```

generically. The higher-charge census remains needed for fully specialized rational witnesses and Galois-group identification.

---

## 2. Claim-by-claim audit

| Target statement | Verdict | Required action |
|---|---|---|
| Lemma 0: square-class independence | PASS | None |
| Lemma 1: signed sub-balance nonvanishing | PASS | None |
| Theorem 2(i–iv): primitivity and irreducibility in `M` | PASS | Minor wording improvement only |
| Theorem 2(v): birationality | PASS | Repair normalization conclusion/proof |
| Lemma 3: transcendence of `s` over `F0` | PASS | None |
| Theorem 4: observable-field identification | PASS | None |
| Generic irreducibility of `N_k(u)` | PASS | None |
| Generic minimal degrees for all `k` | PASS | Clarify generic versus fully specialized |
| Theorem 5: reflection descent `w_i in K` | PASS | None |
| C1: polynomial representatives `g_i(u)` | PASS | None |
| C2: degree-20 biquadratic compositum | CONDITIONAL | Verify Entry 4 and prove ordered-field equality |
| C3: `AB=P^2` | PASS | None |
| C4: higher-`k` generic minimality | PASS | Clarify specialization scope |
| Ramification remark | OVERSTATED | Replace with valuation criterion |
| Discriminant description in §9 | INCOMPLETE | Add critical-sheet component |
| R9 normal-closure group | Correctly open | Leave open |

---

## 3. Confirmed core proofs

### 3.1 Lemma 0 — square-class independence

The UFD proof in `F0[m]` is correct. Under `H1` and `H2`,

```text
d_i = m^2 + N_i^2
```

are individually squarefree and pairwise coprime. Every nonempty product

```text
prod_{i in S} d_i
```

therefore has an irreducible factor of odd valuation and is not a square in

```text
L = F0(m).
```

Thus

```text
[W:L] = 2^k,
Gal(W/L) = (Z/2)^k.
```

### 3.2 Lemma 1 — sub-balance nonvanishing

This is correct. If

```text
t = sum_{i in S} eps_i w_i = 0,
```

then flipping one radical in the nonempty support gives

```text
sigma_j(t) - t = -2 eps_j w_j = 0,
```

contradicting

```text
w_j^2 = d_j != 0.
```

### 3.3 Theorem 2(i–iv) — primitivity and irreducibility

The proof that

```text
s = sum_i w_i
```

is primitive is correct. Its `2^k` signed sums are pairwise distinct, so

```text
[L(s):L] = 2^k,
L(s) = W.
```

The norm

```text
Phi_k(m,M)
 = product_{eps in {+1,-1}^k}
   (4M - sum_i eps_i w_i)
```

is therefore the minimal polynomial of `s/4` over `L`, up to a nonzero scalar. It is irreducible in

```text
L[M]
```

and, by Gauss's lemma, in

```text
F0[m,M].
```

The evenness in `m` is valid. State it directly through

```text
m -> -m,
w_i -> w_i,
```

which fixes `Phi_k`.

### 3.4 Lemma 3 — transcendence

The derivation proof is valid:

```text
D(s) = m sum_i 1/w_i
     = m e_{k-1}(w)/e_k(w).
```

The sign-flip argument correctly proves

```text
e_{k-1}(w) != 0.
```

Hence `D(s)!=0`, while every element algebraic over `F0` is killed by the extended derivation. Therefore `s` is transcendental over `F0`.

### 3.5 Theorem 4 — observable-field identification

This is the key successful proof move. Under

```text
M -> s/4,
m -> m,
```

the kernel is exactly

```text
(Phi_k).
```

After localization at

```text
F = F0(M),
```

the source is a finite-dimensional field over `F`. Its image contains `m` and `s`, hence is all of

```text
F0(m,s) = L(s) = W.
```

Thus

```text
F[m]/(Phi_k) ~= W,
W = F(m),
[W:F] = D_k.
```

Since

```text
Phi_k(m,M) = N_k(m^2),
```

a factorization of `N_k(u)` would factor `Phi_k(m,M)`. Therefore

```text
N_k(u) is irreducible over F,
[K:F] = delta_k.
```

This proves generic minimality for every `k`, including

```text
k=5: delta_5=16,
k=6: delta_6=22.
```

### 3.6 Theorem 5 — reflection descent

The reflection

```text
tau(m) = -m,
tau(w_i) = w_i
```

is a valid automorphism of `W`. It fixes `s`, `M=s/4`, `u=m^2`, `F`, and `K=F(u)`. Because

```text
[W:K] = D_k/delta_k = 2,
```

it generates the full relative Galois group:

```text
Gal(W/K) = <tau>,
W^tau = K.
```

Consequently

```text
w_i in K.
```

This is the generic reflection-descent theorem required by R7.

---

## 4. Required repair — normalization in Theorem 2(v)

### Problem

The statement

```text
Birational integral curves have isomorphic normalizations.
```

is false for affine curves in general.

### Required replacement proof

Retain birationality, then add:

```text
Under (H1) and (H2), C is smooth.

The Jacobian rows of

    w_i^2 - m^2 - N_i^2 = 0

are

    (-2m, 0,...,2w_i,...,0).

A rank failure can occur only if some w_i=0. By (H2), at most one
w_i can vanish. By (H1), w_i=0 implies m^2=-N_i^2 and hence m!=0.
The m-column then prevents a nontrivial linear dependence among the
Jacobian rows. Thus C is smooth, hence normal.

The coordinate ring A_C is finite over A_X because each w_i is integral
over F0[m] and F0[m] is contained in A_X. The map C -> X is finite and
birational, with the same function field. Since C is normal, C is the
affine normalization of X.
```

After this insertion, the exact R6 statement is:

```text
The signed-distance incidence curve C is the affine normalization
of the axial k-ellipse curve X.
```

---

## 5. Required repair — ramification and physical interpretation

### Problem

The remark that

```text
W/K ramifies exactly over u=0 and the places at infinity
```

is too broad.

### Correct statement

For

```text
W = K(m),
m^2 = u,
```

a place `v` of `K` ramifies precisely when

```text
ord_v(u) is odd.
```

Finite affine ramification is generically supported on

```text
u = 0.
```

The infinity places require a separate valuation computation.

### Required physical qualifier

The divisor

```text
u = 0
```

contains all signed axial-contact wall components. Only its all-plus component in the physical chamber is the physical BPS/extremal contact locus.

Use:

```text
The finite fixed divisor is the signed axial-contact divisor u=0;
its all-plus physical component is the static BPS/extremal locus.
```

Do not identify the entire signed algebraic divisor with the physical extremal locus.

---

## 6. Required repair — discriminant mechanisms

### Problem

The draft treats signed sub-balances as all components of

```text
Disc_u N_k.
```

They are only one source of discriminant vanishing.

### Correct decomposition

There are at least two mechanisms:

```text
1. Sheet collision:

   s_eps = s_eps'.

   Equivalently, a signed sub-balance vanishes.

2. Critical point of one signed sheet:

   d/du [4M - s_eps(u)] = 0,

   equivalently,

   sum_i eps_i / w_i = 0.
```

Replace the absolute wording with:

```text
Signed sub-balance varieties contribute the sheet-collision components
of the discriminant. Critical-sheet components must be treated separately.
```

---

## 7. Conditional degree-20 theorem

### What this entry proves by itself

The entry proves generically:

```text
w_i in K,
alpha, beta, gamma in K,
W = K(m),
m^2 = u.
```

Thus the entropy tower is generically well-defined.

### What still depends on Entry 4

The degree-20 compositum requires

```text
[u] != 1,
[gamma] != 1,
[u*gamma] != 1

in K^*/K^2.
```

If these square classes are independent, then

```text
[K(m,y):K] = 4,
Gal(K(m,y)/K) = V_4,
[K(m,y):F] = 20.
```

The logic is correct. The Entry 4 certificate itself must be independently checked before this report authorizes R8 promotion.

### Required good-specialization statement

If nonsquareness is transferred from point B, record that B is a good specialization:

```text
the quintic is separable;
leading coefficients remain nonzero;
u, gamma and u*gamma are regular and nonzero;
the specialization avoids all denominator and ramification loci.
```

An irreducible specialized degree-20 eliminant is an equally clean route.

---

## 8. Required theorem — identify the ordered-horizon field

To call `K(m,y)` the full ordered-horizon field, insert:

```text
Proposition (ordered-horizon field).
Assume K=F(gamma), beta!=0, and define

    y = (S_+ + S_-)/pi,
    z = (S_+ - S_-)/pi.

Then

    F(S_+,S_-) = K(m,y).

Proof.
The identities

    z = 2m beta/y,
    S_+/pi = (y+z)/2,
    S_-/pi = (y-z)/2

show F(S_+,S_-) is contained in K(m,y). Conversely,

    K = F(y^2)

is contained in F(S_+,S_-), and, since beta!=0,

    m = yz/(2beta)

belongs to F(S_+,S_-). Hence K(m,y) is contained in F(S_+,S_-).
```

Once square-class independence holds, this gives

```text
[F(S_+):F] = [F(S_-):F] = 20.
```

Indeed

```text
S_+ S_- in F,
S_- = (S_+S_-)/S_+,
```

so either individual horizon generates the full ordered-horizon field.

---

## 9. Temperature parity remains a separate paper correction

The current entry establishes axial reflection, but it does not amend the temperature claim in the horizon-cover paper.

The required entropy-field action is:

```text
tau(m)   = -m,
tau(y)   =  y,
tau(z)   = -z,
tau(S_+) =  S_-,
tau(S_-) =  S_+.
```

Therefore

```text
tau(T_+) = T_-,
```

not

```text
tau(T_+) = -T_+.
```

The pure anti-invariant covariant is

```text
Theta = S*T,
tau(Theta) = -Theta.
```

---

## 10. Correct promotion status

| Item | Audit decision |
|---|---|
| R6 — incidence normalization | Promote to **ESTABLISHED** after §4 repair |
| R7 — reflection descent | Promote to **ESTABLISHED** |
| Generic all-`k` minimality | **ESTABLISHED** |
| `k=5` generic degree 16 | **ESTABLISHED** |
| `k=6` generic degree 22 | **ESTABLISHED** |
| R8 — degree-20 full ordered horizon field | Conditional until Entry 4 and §8 are closed |
| R9 — normal-closure group over `F` | **OPEN** |
| Specialized rational-charge Galois census | **OPEN** |
| Total reality/interlacing | **OPEN**, independent LMI track |
| Rotating, gauged, weighted, higher-dimensional extensions | **OPEN** |

---

## 11. Apply checklist

```text
[ ] Replace the false affine-normalization implication with the smooth +
    finite birational normalization proof.

[ ] Replace the ramification sentence by ord_v(u) odd.

[ ] Qualify u=0 as the signed axial-contact divisor; isolate the all-plus
    physical BPS/extremal component.

[ ] Split discriminant discussion into sheet-collision and critical-sheet
    mechanisms.

[ ] Add the ordered-horizon-field proposition and verify beta!=0 generically.

[ ] Verify Entry 4's square-class certificate with an explicit
    good-specialization statement or a degree-20 irreducibility certificate.

[ ] Update the horizon-cover paper: temperature is mixed under the horizon
    swap; S*T is the anti-invariant quantity.

[ ] Preserve the distinction:
    generic theorem / rational-charge specialization with M transcendental /
    fully specialized rational witness.
```

---

## 12. Final audit judgment

The core generic descent theorem is mathematically sound and materially upgrades the program:

```text
The signed-distance incidence curve is generically the normalization of the
axial k-ellipse. Its mass polynomial is irreducible over the observable field.
The quotient coordinate u=m^2 has the half-degree dictated by the k-ellipse,
and every signed distance descends through the reflection quotient.
```

For four charges:

```text
[K:F] = 5,
[W:K] = 2,
W^tau = K,
w_i in K.
```

This removes the generic-descent caveat. The remaining work is sharply bounded: formal normalization, correct ramification/discriminant language, verification of the independent square-class evidence, and identification of the ordered-horizon field.

