# Theorem 8.1 — New Mathematical Extension Notes

**Object:** `theorem_8_1(3).tex`, *Invariant Preservation under Role Transposition*  
**Aim:** expand the theorem mathematically, not stylistically.  
**Verdict:** the theorem wants to become a quotient/orbit theorem for exact role-transposed jets. The strongest version is not merely “`K` is invariant”; it is that the **role orbit of the local coupling jet** is the universal carrier for all local DBP invariants. Once stated that way, the theorem generates new exact operations: role-jet transposition maps, first-jet spectral invariants, higher-jet rational closures, Reynolds/anti-Reynolds projections, power/exponent spectra, holonomy towers, and three-channel curvature orbit probes.

---

## 1. Core repair: raw derivative data transforms; the orbit is invariant

The TeX statement defines role transposition as an `S_3` action on the roles `(D,S,P)`, and defines a coupling kernel

\[
K=(K_{\rm spec},K_{\rm hol},\kappa),
\]

where `K_spec` includes the Jacobian and higher derivative data. The subtle issue is that a **raw Jacobian is not literally invariant** under role transposition. It transforms by the inverse-function theorem. What is invariant is either:

1. a canonical set of symmetric functions of the transformed derivative data, or
2. the full `S_3` orbit of the local jet.

So the strengthened theorem should replace

\[
K(\mathcal T_\sigma\tau)=K(\tau)
\]

with the more precise object

\[
\boxed{
\mathfrak K_r(\tau)
=
\operatorname{Orb}_{S_3}\big(j^r(\oplus)_\tau\big)
}
\]

or, if values are allowed to enter the invariant,

\[
\boxed{
\mathfrak K_r^+(\tau)
=
\operatorname{Orb}_{S_3}\big(D,S,P, j^r(\oplus)_\tau\big).
}
\]

Then the theorem becomes a universal quotient statement:

\[
\boxed{
\varphi\text{ is a local order-}r\text{ DBP invariant}
\iff
\varphi\text{ factors through }\mathfrak K_r^+.
}
\]

The coupling-structural invariants are precisely the functions of this orbit that do **not** descend to the value-only quotient `(D,S,P)/S_3`.

This avoids the false burden of proving that a chosen finite tuple `K_spec, K_hol, κ` is complete unless it has actually been made orbit-complete.

---

## 2. Exact role-transposition as a birational `S_3` action

Work in a local chart

\[
P=f(D,S),
\]

with

\[
a=f_D,
\qquad
b=f_S.
\]

Full role well-posedness requires

\[
a\neq 0,
\qquad
b\neq 0,
\]

because solving for `D` and solving for `S` both use inverse-function denominators.

The first-order role orbit consists of six derivative pairs:

\[
\boxed{
\mathcal O_1(a,b)=
\left\{
(a,b),
(b,a),
\left({1\over a},-{b\over a}\right),
\left(-{b\over a},{1\over a}\right),
\left(-{a\over b},{1\over b}\right),
\left({1\over b},-{a\over b}\right)
\right\}.
}
\]

Equivalently, the two generating involutions are

\[
s(a,b)=(b,a),
\]

and

\[
t(a,b)=\left({1\over a},-{b\over a}\right),
\]

with

\[
s^2=t^2=e,
\qquad
(st)^3=e.
\]

Thus role transposition is not an informal relabelling. It is an exact birational representation of `S_3` on the jet coordinates.

**Cella consequence.** If `a,b ∈ ℚ` and `ab ≠ 0`, every role-transposed first derivative is again in `ℚ`. Role transposition itself is an exact rational operation.

---

## 3. First-jet projective kernel and explicit invariants

The first derivative data is most cleanly encoded as the projective normal to the graph surface

\[
F(D,S,P)=P-f(D,S)=0.
\]

At the operating point,

\[
g=(F_D,F_S,F_P)=(-a,-b,1).
\]

Let

\[
(u,v,w)=(-a,-b,1).
\]

Role transposition permutes the three coordinates of the projective normal line `[u:v:w]`. Therefore the role-invariant first-order quotient is the `S_3` quotient of `\mathbb P^2`.

The elementary symmetric coordinates are

\[
e_1=u+v+w=1-a-b,
\]

\[
e_2=uv+uw+vw=ab-a-b,
\]

\[
e_3=uvw=ab.
\]

Because the normal is projective, the scale-free first-jet invariants may be taken as

\[
\boxed{
I_1={e_1e_2\over e_3}
={ (1-a-b)(ab-a-b)\over ab},
}
\]

and

\[
\boxed{
I_2={e_1^3\over e_3}
={ (1-a-b)^3\over ab}.
}
\]

A third useful diagnostic is the discriminant of the normal cubic:

\[
\boxed{
\Delta_n=(u-v)^2(u-w)^2(v-w)^2
=(a-b)^2(a+1)^2(b+1)^2.
}
\]

`Δ_n=0` detects a nontrivial role stabilizer: equal input elasticities/sensitivities, or a derivative equal to the inverse-role boundary `−1`.

---

## 4. Second-order jet action: exact rational formulas

Let

\[
A=f_{DD},\qquad B=f_{DS},\qquad C=f_{SS}.
\]

Under the input swap `s`,

\[
\boxed{
s(a,b,A,B,C)=(b,a,C,B,A).
}
\]

Under the role swap `t=(D\;P)`, the new chart solves

\[
D=q(P,S).
\]

Its first and second derivatives are

\[
q_P={1\over a},
\qquad
q_S=-{b\over a},
\]

\[
\boxed{
q_{PP}=-{A\over a^3},
}
\]

\[
\boxed{
q_{PS}={Ab-aB\over a^3},
}
\]

\[
\boxed{
q_{SS}={-Ab^2+2abB-a^2C\over a^3}.
}
\]

So the second-order generator is

\[
\boxed{
t(a,b,A,B,C)=
\left(
{1\over a},
-{b\over a},
-{A\over a^3},
{Ab-aB\over a^3},
{-Ab^2+2abB-a^2C\over a^3}
\right).
}
\]

These formulas satisfy

\[
t^2=e,
\qquad
s^2=e,
\qquad
(st)^3=e.
\]

So the order-2 role action is again an exact rational `S_3` representation.

**Immediate native operation:**

```text
role_transpose_jet2(a,b,A,B,C, sigma) -> exact Fraction tuple
```

This is a mathematically cleaner primitive than a hand-waved `K is invariant` assertion.

---

## 5. Third-order jet action: a concrete higher-order reach extension

Let the third derivatives be

\[
E=f_{DDD},
\qquad
F=f_{DDS},
\qquad
G=f_{DSS},
\qquad
H=f_{SSS}.
\]

Again solve `D=q(P,S)`. The third derivatives are:

\[
\boxed{
q_{PPP}={3A^2-aE\over a^5},
}
\]

\[
\boxed{
q_{PPS}={-3A^2b+3aAB+abE-a^2F\over a^5},
}
\]

\[
\boxed{
q_{PSS}={
3A^2b^2-6aABb+a^2AC+2a^2B^2-ab^2E+2a^2bF-a^3G
\over a^5},
}
\]

\[
\boxed{
q_{SSS}={
-3A^2b^3+9aABb^2-3a^2ACb-6a^2B^2b+3a^3BC+ab^3E-3a^2b^2F+3a^3bG-a^4H
\over a^5}.
}
\]

Thus the role-transposition tower continues rationally. The denominator pattern is the multivariate inverse-function pattern: third order lands over `a^5`; second order over `a^3`; first order over `a`.

**Cella consequence.** Every finite role-jet transposition is a rational map on the jet coordinates, localized at `a b ≠ 0`. Therefore exact `ℚ` account closure is natural:

\[
\boxed{
\mathsf{RoleJet}_r:
\mathbb Q[j^r f][a^{-1},b^{-1}]
\longrightarrow
\mathbb Q[j^r f][a^{-1},b^{-1}].
}
\]

---

## 6. Corrected Theorem 8.1: quotient form

Let `J_r(τ)` be the local order-`r` coupling jet in one graph chart. Let `G=S_3` act by the exact rational role-jet maps above. Define

\[
\mathfrak K_r(\tau)=G\cdot J_r(\tau),
\]

and, if role-value couplings are allowed,

\[
\mathfrak K_r^+(\tau)=G\cdot(D,S,P,J_r(\tau)).
\]

Then:

### Theorem 8.1′ — Orbit-complete invariant preservation

For local order-`r` functions `φ`,

\[
\boxed{
\phi\text{ is DBP-invariant}
\iff
\phi\text{ factors through }\mathfrak K_r^+.
}
\]

If `φ` is forbidden to depend on the role-labelled values except through the coupling jet, replace `\mathfrak K_r^+` by `\mathfrak K_r`.

### Proof sketch

The quotient map

\[
\pi:X\to X/G
\]

has the universal property that a function `φ:X→Y` is constant on `G`-orbits iff there exists `ψ:X/G→Y` such that

\[
\phi=\psi\circ\pi.
\]

Here `X` is the local jet space, or the value-plus-jet space. The orbit kernel is exactly the quotient datum. No informal dichotomy is needed.

This is stronger and safer than the current theorem because it does not require guessing whether a hand-chosen `K` captured all coupling data.

---

## 7. A real counter-pressure: mixed value-coupling invariants

The TeX proof says every function depends on coupling data or role-labelled values. That part is useful, but the proposed classification needs a third operational distinction: **mixed invariants**.

Given values

\[
x=(D,S,P)
\]

and projective normal coordinates

\[
g=(-a,-b,1),
\]

the simultaneous contraction

\[
\boxed{
M_{1,1}=x\cdot g=-Da-Sb+P
}
\]

is invariant under simultaneous coordinate permutation of values and normal data. It is coupling-structural because it depends on `g`, but it is not a function of the unordered values alone.

If the original `K` excludes values, then `M_{1,1}` is a coupling-structural DBP invariant that does **not** factor through `K`. Therefore the theorem is safest only when either:

1. `K` includes the value-plus-jet orbit, or
2. the allowed invariant class excludes all value-jet contractions.

This is not a demolition. It is a useful strengthening: Theorem 8.1 should be an orbit quotient theorem, not a finite-kernel assertion unless the finite kernel is proven complete.

The general mixed moment family is

\[
\boxed{
M_{r,s}=\sum_{i=1}^3 x_i^r g_i^s.
}
\]

These are diagonal-`S_3` invariants. For `s>0`, they are coupling-structural. They generate a large class of mixed value-coupling diagnostics.

---

## 8. Reynolds and anti-Reynolds operations

For any candidate expression `m` in values and jet coordinates, define the role Reynolds operator

\[
\boxed{
\mathcal R[m]={1\over 6}\sum_{\sigma\in S_3} m(\mathcal T_\sigma\tau).
}
\]

Then `R[m]` is automatically DBP-invariant.

Define also the alternating projection

\[
\boxed{
\mathcal A[m]={1\over 6}\sum_{\sigma\in S_3}\operatorname{sgn}(\sigma)m(\mathcal T_\sigma\tau).
}
\]

`A[m]` is a signed role detector. Squaring it gives an invariant. For values alone this recovers the Vandermonde discriminant:

\[
\boxed{
\Delta_x=(D-S)^2(D-P)^2(S-P)^2.
}
\]

For first-jet normal coordinates this gives

\[
\boxed{
\Delta_n=(a-b)^2(a+1)^2(b+1)^2.
}
\]

These are not just formal gadgets. They are exact `ℚ` operations whenever the input jet is exact rational.

---

## 9. Power-law reach: role exponent orbit

For power-law couplings

\[
P=D^mS^n,
\]

pass to log coordinates:

\[
\log P=m\log D+n\log S.
\]

The exponent normal is

\[
\ell=(-m,-n,1).
\]

Role transposition permutes the three entries of the projective exponent normal. Therefore the exponent-pair orbit is

\[
\boxed{
\mathcal E(m,n)=
\left\{
(m,n),
(n,m),
\left({1\over m},-{n\over m}\right),
\left(-{n\over m},{1\over m}\right),
\left(-{m\over n},{1\over n}\right),
\left({1\over n},-{m\over n}\right)
\right\}.
}
\]

This is the exact same `S_3` birational action as the first-jet slope orbit, now acting on log-elasticities.

The role-degree spectrum is the multiset of exponent sums in each chart:

\[
\boxed{
\operatorname{DegSpec}(m,n)=
\left\{
 m+n,
 m+n,
 {1-n\over m},
 {1-n\over m},
 {1-m\over n},
 {1-m\over n}
\right\}.
}
\]

Examples:

### Multiplication

For `P=DS`, `(m,n)=(1,1)`,

\[
\operatorname{DegSpec}(1,1)=\{2,2,0,0,0,0\}.
\]

The forward chart is degree `2`; inverse charts such as `D=P/S` are degree `0`.

### Cubic mixed power

For `P=D^2S`, `(m,n)=(2,1)`,

\[
\operatorname{DegSpec}(2,1)=\{3,3,0,0,-1,-1\}.
\]

This distinguishes it sharply from ordinary multiplication despite both being purely monomial.

### Projective exponent invariants

Let

\[
e_1^\ell=1-m-n,
\qquad
 e_2^\ell=mn-m-n,
\qquad
 e_3^\ell=mn.
\]

Then scale-free exponent invariants are

\[
\boxed{
I_1^\ell={e_1^\ell e_2^\ell\over e_3^\ell}
={ (1-m-n)(mn-m-n)\over mn},
}
\]

\[
\boxed{
I_2^\ell={ (e_1^\ell)^3\over e_3^\ell}
={ (1-m-n)^3\over mn}.
}
\]

The exponent discriminant is

\[
\boxed{
\Delta_\ell=(m-n)^2(m+1)^2(n+1)^2.
}
\]

This detects exponent-role degeneracy.

---

## 10. Power derivative tower for arbitrary exponents

For a chart

\[
z=Cx^\alpha y^\beta,
\]

all mixed derivatives are

\[
\boxed{
\partial_x^i\partial_y^j z
=\alpha^{\underline i}\beta^{\underline j}{z\over x^iy^j},
}
\]

where

\[
\alpha^{\underline i}=\alpha(\alpha-1)\cdots(\alpha-i+1).
\]

Therefore a power-law DBP operation has a full role-transposed derivative tower:

\[
\boxed{
\mathsf{PowJet}_{r}(m,n;D,S,P)
=
\left\{
\alpha_\sigma^{\underline i}\beta_\sigma^{\underline j}
{z_\sigma\over x_\sigma^iy_\sigma^j}
:
1\le i+j\le r,
\sigma\in S_3
\right\}.
}
\]

This is exact rational whenever the exponents and operating-point values are rational and the denominators are nonzero.

This gives a much stronger “scope of powers” extension than the original theorem: role transposition does not merely preserve invariance; it generates a complete exact tower of all transposed power derivatives.

---

## 11. Euler tower: degree detection from local jets

In a chart

\[
z=f(x,y),
\]

with normalized implicit equation

\[
F=x_3-f(x_1,x_2)=z-f(x,y),
\]

define Euler tensor contractions

\[
\mathcal E_1=z-xf_x-yf_y,
\]

\[
\mathcal E_2=-\left(x^2f_{xx}+2xyf_{xy}+y^2f_{yy}\right),
\]

\[
\mathcal E_3=-\left(x^3f_{xxx}+3x^2yf_{xxy}+3xy^2f_{xyy}+y^3f_{yyy}\right).
\]

If `f` is homogeneous of degree `r`, then on the graph `z=f(x,y)`:

\[
\boxed{
\mathcal E_1=(1-r)z,
}
\]

\[
\boxed{
\mathcal E_2=-r(r-1)z,
}
\]

\[
\boxed{
\mathcal E_3=-r(r-1)(r-2)z.
}
\]

If `r\neq 1`, then the degree is locally recoverable by

\[
\boxed{
r={\mathcal E_2\over \mathcal E_1}.
}
\]

The third-order consistency gate is

\[
\boxed{
\mathcal E_3\mathcal E_1=\mathcal E_2^2-2\mathcal E_1\mathcal E_2.
}
\]

More generally,

\[
\boxed{
\mathcal E_k=-r^{\underline k}z
\quad (k\ge 2).
}
\]

Thus Theorem 8.1 naturally grows a **power-degree observable**:

```text
RoleEulerTower_r = multiset over all role charts of (E1,E2,...,Er)
```

This detects the power/exponent structure of the coupling exactly from local jets.

---

## 12. Holonomy tower: mixed derivative content across all role charts

For a chart `z=f(x,y)`, the finite rectangle holonomy is

\[
\Delta_{h,k}f
=f(x+h,y+k)-f(x+h,y)-f(x,y+k)+f(x,y).
\]

Its Taylor tower is

\[
\Delta_{h,k}f
=
\sum_{i,j\ge 1}{h^ik^j\over i!j!}\partial_x^i\partial_y^jf.
\]

So define the role-holonomy tower

\[
\boxed{
\operatorname{HolSpec}_r(\tau)=
\left\{
\partial_x^i\partial_y^jf_\sigma:
 i,j\ge 1,
 i+j\le r,
 \sigma\in S_3
\right\}.
}
\]

For separable charts, all mixed terms vanish. For power charts, the exact formula is

\[
\boxed{
\partial_x^i\partial_y^jf_\sigma
=\alpha_\sigma^{\underline i}\beta_\sigma^{\underline j}
{z_\sigma\over x_\sigma^iy_\sigma^j}.
}
\]

This creates a direct bridge between role transposition, holonomy, powers, and exact rational derivative accounting.

---

## 13. Relation to three-channel curvature

The local coupling graph

\[
F(D,S,P)=0
\]

also has a second-order geometric object: gradient plus Hessian. Under pure coordinate role permutation,

\[
g\mapsto P_\sigma g,
\qquad
H\mapsto P_\sigma H P_\sigma^T.
\]

Therefore the three-channel curvature spectrum should be made role-aware by taking the orbit

\[
\boxed{
\operatorname{CurvRoleSpec}(F)=
\left\{
\operatorname{ChannelSpectrum}(P_\sigma g,P_\sigma HP_\sigma^T):
\sigma\in S_3
\right\}.
}
\]

For `n=3`, the channel spectrum is

\[
(K_G,\kappa_c,\kappa_s,\kappa_{int}).
\]

For higher dimension, replace it by the full elementary curvature channel spectrum

\[
\{\sigma_{r;p,q}\}.
\]

This is the clean connection between the strengthened Theorem 8.1 and the three-channel `K_G` build: Theorem 8.1 should not choose one scalar projection as primary. It should define the orbit-complete typed geometric object and let scalar projections factor through it.

---

## 14. Exact implementation gates

### Gate A — first-order group law

For random exact rational `(a,b)` with `ab ≠ 0`, verify:

\[
s^2=t^2=e,
\qquad
(st)^3=e.
\]

### Gate B — second-order group law

For random exact rational `(a,b,A,B,C)` with `ab ≠ 0`, verify the same identities using the second-order formulas.

### Gate C — third-order group law

For random exact rational third jets, verify the third-order formulas also satisfy the `S_3` relations.

### Gate D — power orbit pins

For `P=D^mS^n`, pin:

\[
\mathcal E(m,n)=
\left\{
(m,n),(n,m),(1/m,-n/m),(-n/m,1/m),(-m/n,1/n),(1/n,-m/n)
\right\}.
\]

### Gate E — Euler tower pins

For `P=D^mS^n`, verify in the forward chart:

\[
\mathcal E_2/\mathcal E_1=m+n
\]

when `m+n≠1`, and verify the third-order identity

\[
\mathcal E_3\mathcal E_1=\mathcal E_2^2-2\mathcal E_1\mathcal E_2.
\]

### Gate F — invariant candidate checker

For a candidate scalar `φ`, compute

\[
\{\phi(\mathcal T_\sigma\tau):\sigma\in S_3\}.
\]

Then:

```text
DBP invariant iff the six exact values are equal.
```

No tolerance. No numerics. Exact fractions only.

---

## 15. Minimal exact-ℚ probe sketch

```python
from fractions import Fraction as Q


def s1(j):
    # first-order input swap
    a, b = j
    return (b, a)


def t1(j):
    # role swap D <-> P, chart D = q(P,S)
    a, b = j
    if a == 0:
        raise ZeroDivisionError("role transposition undefined: a=0")
    return (Q(1, 1) / a, -b / a)


def s2(j):
    a, b, A, B, C = j
    return (b, a, C, B, A)


def t2(j):
    a, b, A, B, C = j
    if a == 0:
        raise ZeroDivisionError("role transposition undefined: a=0")
    return (
        Q(1, 1) / a,
        -b / a,
        -A / a**3,
        (A*b - a*B) / a**3,
        (-A*b*b + 2*a*b*B - a*a*C) / a**3,
    )


def compose(f, g):
    return lambda x: f(g(x))


def assert_s3_jet2(j):
    assert s2(s2(j)) == j
    assert t2(t2(j)) == j
    st = compose(s2, t2)
    assert st(st(st(j))) == j


def first_projective_invariants(a, b):
    e1 = Q(1) - a - b
    e2 = a*b - a - b
    e3 = a*b
    if e3 == 0:
        raise ZeroDivisionError("projective invariant chart singular: ab=0")
    I1 = e1 * e2 / e3
    I2 = e1**3 / e3
    Delta = (a-b)**2 * (a+1)**2 * (b+1)**2
    return I1, I2, Delta
```

---

## 16. Strongest revised summary

Theorem 8.1 should be upgraded from:

```text
K is invariant, therefore functions through K are invariant.
```

to:

```text
Role transposition is an exact rational S3 action on local coupling jets.
The orbit of the value-plus-jet is the universal carrier of local DBP invariants.
Coupling-structural invariants are exactly the orbit functions that do not descend to the value-only quotient.
Power laws, holonomy residues, and curvature channels are all special projections of this orbit object.
```

That version gives new operations immediately:

1. `role_transpose_jet_r` — exact rational role maps for arbitrary finite jet order.
2. `role_orbit_fingerprint` — canonical exact hash of a coupling point.
3. `first_projective_kernel` — two scale-free spectral invariants plus discriminant.
4. `reynolds_invariant(expr)` — automatic DBP-invariant generator.
5. `anti_reynolds(expr)^2` — role-asymmetry discriminator.
6. `PowJet_r` — full derivative tower for power-law couplings.
7. `DegSpec` — role-degree spectrum for monomial/power operations.
8. `HolSpec_r` — mixed-derivative holonomy tower across all role charts.
9. `CurvRoleSpec` — role orbit of the three-channel curvature spectrum.

This is the mathematically stronger form of Theorem 8.1: not a prose theorem about invariance, but an exact quotient calculus for role-transposed coupling jets.
