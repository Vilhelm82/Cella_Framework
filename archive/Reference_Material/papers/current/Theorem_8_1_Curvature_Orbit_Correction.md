# Theorem 8.1 — §13 Curvature Orbit Correction and Extension

**Object corrected:** §13 of `Theorem_8_1_New_Math_Extension.md`.

**Verdict:** the original §13 action

\[
(g,H)\mapsto (P_\sigma g,\;P_\sigma H P_\sigma^T)
\]

is a passive coordinate permutation. Under that action, the three-channel curvature spectrum is invariant by relabelling, so the six-point orbit collapses to one spectrum. That makes the written `CurvRoleSpec` tautological, not a new role diagnostic.

The nontrivial role-curvature object is obtained only after **active role recharting**: solve the DBP relation in each output role and compute the graph-normalized curvature channels in that role chart. This produces a three-output-role spectrum, or a six-chart object if ordered input labels are retained.

---

## 1. Why the written §13 orbit is trivial

The three-channel spec defines

\[
H=H_c+H_s,
\qquad
H_s=\operatorname{diag}(H),
\qquad
H_c=H-H_s.
\]

For a permutation matrix \(P_\sigma\),

\[
\operatorname{diag}(P_\sigma H P_\sigma^T)=P_\sigma\operatorname{diag}(H)P_\sigma^T,
\]

so

\[
H_s\mapsto P_\sigma H_sP_\sigma^T,
\qquad
H_c\mapsto P_\sigma H_cP_\sigma^T.
\]

The monomial channel determinants \(\Delta_c,\Delta_s,\Delta_m\) are complete symmetric sums over the coordinate labels. A coordinate permutation only renames the indices. Therefore

\[
\boxed{
\operatorname{ChannelSpectrum}(P_\sigma g,P_\sigma HP_\sigma^T)
=
\operatorname{ChannelSpectrum}(g,H)
}
\]

for every \(\sigma\in S_3\).

So the old object

\[
\left\{
\operatorname{ChannelSpectrum}(P_\sigma g,P_\sigma HP_\sigma^T):\sigma\in S_3
\right\}
\]

is just

\[
\left\{\operatorname{ChannelSpectrum}(g,H)\right\}.
\]

That is useful as a covariance sanity check, but not as a Theorem 8.1 role orbit.

---

## 2. Passive permutation versus active role recharting

For a local DBP graph

\[
P=f(D,S),
\]

write

\[
a=f_D,
\qquad
b=f_S,
\qquad
A=f_{DD},
\qquad
B=f_{DS},
\qquad
C=f_{SS}.
\]

The graph defining function in the product role is

\[
F_P(D,S,P)=P-f(D,S).
\]

A passive role permutation merely reorders coordinates. That cannot create a new curvature-channel spectrum.

An active role transposition instead changes which variable is solved as product/output. For example, the \(D\)-output chart solves

\[
D=q(P,S),
\]

and uses

\[
F_D(P,S,D)=D-q(P,S).
\]

Similarly the \(S\)-output chart solves

\[
S=r(D,P),
\]

and uses

\[
F_S(D,P,S)=S-r(D,P).
\]

These graph-normalized defining functions are related to the original defining function by a nonconstant gauge on the surface, e.g.

\[
F_D=-{1\over a}F_P+O(F_P^2),
\qquad
F_S=-{1\over b}F_P+O(F_P^2).
\]

Total Gaussian curvature is unchanged by this gauge. The individual channels are not. That is the missing nontriviality.

---

## 3. Graph-channel formula

For any local graph

\[
z=h(x,y),
\]

with first jet

\[
\alpha=h_x,
\qquad
\beta=h_y,
\]

and second jet

\[
L=h_{xx},
\qquad
M=h_{xy},
\qquad
N=h_{yy},
\]

the graph defining function is

\[
F=z-h(x,y).
\]

Then

\[
g=(-\alpha,-\beta,1),
\qquad
H=\begin{pmatrix}
-L&-M&0\\
-M&-N&0\\
0&0&0
\end{pmatrix}.
\]

The three-channel spec gives

\[
Q=1+\alpha^2+\beta^2,
\]

\[
\boxed{
\kappa_c=-{M^2\over Q^2},
\qquad
\kappa_s={LN\over Q^2},
\qquad
\kappa_{int}=0,
}
\]

and

\[
\boxed{
K_G={LN-M^2\over Q^2}.
}
\]

So a graph-normalized DBP chart always has zero graph-channel interaction. Interaction reappears either in a non-graph implicit gauge, or in the gauge transport between output roles.

---

## 4. The active output-role curvature spectrum

Let

\[
q_0=1+a^2+b^2.
\]

The product-output chart \(P=f(D,S)\) gives

\[
\boxed{
C_P=
\left(
K,
-{B^2\over q_0^2},
{AC\over q_0^2},
0
\right),
}
\]

where

\[
K={AC-B^2\over q_0^2}.
\]

The directive-output chart \(D=q(P,S)\) has derivatives

\[
q_P={1\over a},
\qquad
q_S=-{b\over a},
\]

\[
q_{PP}=-{A\over a^3},
\qquad
q_{PS}={Ab-aB\over a^3},
\qquad
q_{SS}={-Ab^2+2abB-a^2C\over a^3}.
\]

After applying the graph-channel formula, this gives

\[
\boxed{
C_D=
\left(
K,
-{(Ab-aB)^2\over a^2q_0^2},
{A(Ab^2-2abB+a^2C)\over a^2q_0^2},
0
\right).
}
\]

The substrate-output chart \(S=r(D,P)\) gives

\[
r_D=-{a\over b},
\qquad
r_P={1\over b},
\]

\[
r_{DD}={-Ca^2+2abB-b^2A\over b^3},
\qquad
r_{DP}={Ca-bB\over b^3},
\qquad
r_{PP}=-{C\over b^3}.
\]

Thus

\[
\boxed{
C_S=
\left(
K,
-{(Ca-bB)^2\over b^2q_0^2},
{C(Ca^2-2abB+b^2A)\over b^2q_0^2},
0
\right).
}
\]

The identities

\[
A(Ab^2-2abB+a^2C)-(Ab-aB)^2=a^2(AC-B^2),
\]

and

\[
C(Ca^2-2abB+b^2A)-(Ca-bB)^2=b^2(AC-B^2)
\]

prove that all three output-role charts have the same total Gaussian curvature \(K\), as they must.

---

## 5. Six charts collapse to three spectra, not one

The full role set has six graph readings:

\[
P|D,S,
\quad
P|S,D,
\quad
D|P,S,
\quad
D|S,P,
\quad
S|D,P,
\quad
S|P,D.
\]

If we retain the ordered jet, these are six role charts.

If we retain only the scalar curvature-channel tuple

\[
(K,\kappa_c,\kappa_s,\kappa_{int}),
\]

then input swaps inside a fixed output role collapse:

\[
C_{P|D,S}=C_{P|S,D},
\]

\[
C_{D|P,S}=C_{D|S,P},
\]

\[
C_{S|D,P}=C_{S|P,D}.
\]

Therefore the honest scalar object is

\[
\boxed{
\operatorname{OutputRoleCurvSpec}(f)
=
\{C_P,C_D,C_S\}.
}
\]

The honest sixfold object is not a scalar spectrum. It is the labelled role-jet curvature object

\[
\boxed{
\operatorname{RoleChartCurvJet}(f)
=
\left\{
(\rho,\alpha_\rho,\beta_\rho,L_\rho,M_\rho,N_\rho,C_\rho)
:\rho\in S_3
\right\}.
}
\]

The input-order degeneracy is a feature, not a failure: Gaussian curvature is symmetric in the two tangent/input axes of a graph chart.

---

## 6. Role-coupling numerators

Define the three output-role mixed numerators

\[
\Lambda_P=B,
\]

\[
\Lambda_D={Ab-aB\over a}={b\over a}A-B,
\]

\[
\Lambda_S={Ca-bB\over b}={a\over b}C-B.
\]

Then

\[
\boxed{
\kappa_{c,P}=-{\Lambda_P^2\over q_0^2},
\qquad
\kappa_{c,D}=-{\Lambda_D^2\over q_0^2},
\qquad
\kappa_{c,S}=-{\Lambda_S^2\over q_0^2}.
}
\]

These are exact role-holonomy curvature numerators. They measure how much mixed curvature survives after choosing each role as output.

Define also the transverse quadratic

\[
R=a^2C-2abB+b^2A=(b,-a)
\begin{pmatrix}A&B\\B&C\end{pmatrix}
\begin{pmatrix}b\\-a\end{pmatrix}.
\]

Then

\[
\boxed{
\kappa_{s,D}={AR\over a^2q_0^2},
\qquad
\kappa_{s,S}={CR\over b^2q_0^2},
\qquad
\kappa_{s,P}={AC\over q_0^2}.
}
\]

The tuple

\[
\boxed{
\left(
B^2,
\left({b\over a}A-B\right)^2,
\left({a\over b}C-B\right)^2
\right)
}
\]

is a new exact role-coupling spectrum for Theorem 8.1.

---

## 7. New diagnostic classes

### 7.1 Output-role anisotropy

A scalar curvature role-anisotropy is

\[
\boxed{
\mathcal A_c=
(\kappa_{c,P}-\kappa_{c,D})^2+
(\kappa_{c,D}-\kappa_{c,S})^2+
(\kappa_{c,S}-\kappa_{c,P})^2.
}
\]

It vanishes exactly when all three output-role coupling channels agree.

### 7.2 Product-role excess

\[
\boxed{
E_P=\kappa_{c,P}-\frac12(\kappa_{c,D}+\kappa_{c,S}).
}
\]

This detects whether the declared product role is geometrically special relative to the two inverse roles.

### 7.3 Gauge transport vector

\[
\boxed{
G_{P\to D}=C_D-C_P,
\qquad
G_{P\to S}=C_S-C_P.
}
\]

This records how graph normalization moves curvature between pure coupling and pure self while preserving total \(K\).

---

## 8. Example: a generic exact jet

Take

\[
a=5,
\qquad
b=7,
\qquad
A=2,
\qquad
B=3,
\qquad
C=4.
\]

Then

\[
q_0=75,
\qquad
K=-{1\over 5625}.
\]

The product-output chart gives

\[
C_P=
\left(
-{1\over5625},
-{1\over625},
{8\over5625},
0
\right).
\]

The directive-output chart gives

\[
C_D=
\left(
-{1\over5625},
-{1\over140625},
-{8\over46875},
0
\right).
\]

The substrate-output chart gives

\[
C_S=
\left(
-{1\over5625},
-{1\over275625},
-{16\over91875},
0
\right).
\]

So the active chart orbit is nontrivial, but only across output roles. The passive coordinate orbit would have returned the same tuple six times.

---

## 9. Correct replacement for §13

Replace the old §13 object with two objects:

### Passive covariance check

\[
\boxed{
\operatorname{PassiveCurvCov}(F)=
\left[
\operatorname{ChannelSpectrum}(P_\sigma g,P_\sigma HP_\sigma^T)
=\operatorname{ChannelSpectrum}(g,H)
\right]_{\sigma\in S_3}.
}
\]

This is a sanity check, not an invariant generator.

### Active role-chart curvature object

\[
\boxed{
\operatorname{ActiveCurvRoleSpec}_2(f)=
\left\{
C_\rho:
\rho\in\{P|D,S,\ P|S,D,\ D|P,S,\ D|S,P,\ S|D,P,\ S|P,D\}
\right\}.
}
\]

Modulo input swaps, this reduces to

\[
\boxed{
\operatorname{OutputRoleCurvSpec}_2(f)=\{C_P,C_D,C_S\}.
}
\]

If Theorem 8.1 needs a true sixfold carrier, use labelled jets, not scalar curvature spectra:

\[
\boxed{
\operatorname{RoleChartCurvJet}_2(f)=
\left\{
(\rho,\alpha_\rho,\beta_\rho,L_\rho,M_\rho,N_\rho,C_\rho)
\right\}_{\rho\in S_3}.
}
\]

---

## 10. Consequence for Theorem 8.1

The quotient theorem still survives, but §13 must not claim that a passive curvature-channel permutation supplies a nontrivial role orbit.

The corrected hierarchy is:

1. **Implicit three-channel spectrum:** intrinsic total \(K_G\), basis-relative channels; passive role permutation is covariance only.
2. **Active graph role spectra:** three nontrivial output-role curvature decompositions; total \(K_G\) fixed, channel split moves by gauge.
3. **Role-jet orbit:** full sixfold exact rational object; needed if ordered role data matters.

That gives Theorem 8.1 a real curvature-side object without smuggling in a tautological orbit.

