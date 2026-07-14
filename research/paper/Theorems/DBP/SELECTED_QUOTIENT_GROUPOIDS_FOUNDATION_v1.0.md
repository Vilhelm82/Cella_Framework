# Selected Quotient Groupoids

## Coefficient-typed objects, native morphisms, and category formation, v1.0

**Date:** 2026-07-14  
**Version:** 1.0  
**Role:** Step 3 foundation for the DBP paper ensemble  
**Status:** the category, native morphisms, presentation equivalences, and
flat scalar-extension functors are defined and proved. Equivalence of the
component realizations, closure under additional constructions, and an
independent third realization remain separate gates.

---

## 0. Result and scope

For each commutative ring \(R\), this report defines a locally small category

\[
\mathbf{SQG}_R
\]

whose quotient is the coefficient module relevant to the ensemble: an
equivariant module \(M\) modulo a declared null submodule \(K\). In the
elliptic realization, \(M\) is relative integral homology and \(K\) is the
ordinary compact-period sub-local system.

The exact coefficient rings used by the DBP transport system are

\[
\mathbb Z,\qquad
\mathbb Z[1/2],\qquad
\mathbb Z[i],\qquad
\mathbb Z[1/2,i].
\tag{0.1}
\]

The familiar ladder

\[
\mathbf{SQG}_{\mathbb Z}
\longrightarrow
\mathbf{SQG}_{\mathbb Q}
\longrightarrow
\mathbf{SQG}_{\mathbb C}
\tag{0.2}
\]

is only a coarse scalar-extension ladder. It does not say that a CPV
midpoint first exists over \(\mathbb Q\), or that a phase-normalized class
first exists over \(\mathbb C\).

No equivalence of DBP realizations is asserted here.

---

## 1. Coefficient-typed selected quotient groupoids

Fix a commutative ring \(R\). Regard a poset as a category in the usual way.

### Definition 1.1 — object

An \(R\)-selected quotient groupoid is a tuple

\[
\mathbb X=(\mathcal G,\mathcal A,P,\ell,M,K,s)
\tag{1.1}
\]

with the following data.

1. \(\mathcal G\) is a small groupoid. Its arrows encode native symmetry or
   transport.

2. \(\mathcal A\subseteq\mathcal G\) is a full subgroupoid, called the
   admissible chamber groupoid.

3. \(P\) is a small poset and

   \[
   \ell:\mathcal G\longrightarrow P
   \tag{1.2}
   \]

   is a functor. Because arrows of \(\mathcal G\) are invertible and a poset
   has no nontrivial isomorphisms, \(\ell\) is constant on groupoid orbits.
   It records regular, wall, and boundary-stratum types.

4. \(M:\mathcal G\to R\text{-}\mathbf{Mod}\) is an \(R\)-linear
   representation whose fibres are finitely generated \(R\)-modules.

5. \(K\subseteq M\) is a \(\mathcal G\)-stable subrepresentation.

6. Write

   \[
   Q_{\mathbb X}:=M/K.
   \tag{1.3}
   \]

   There is a natural transformation

   \[
   s:R_{\mathcal A}\longrightarrow Q_{\mathbb X}|_{\mathcal A},
   \tag{1.4}
   \]

   where \(R_{\mathcal A}\) is the constant rank-one representation. Thus
   \(s\) is a flat selected quotient class on the admissible subgroupoid.

The symmetry quotient is represented by \(\mathcal G\) itself, or by its
quotient stack; (1.3) is the independent coefficient quotient. Primitivity,
positivity, uniqueness, and nonzero boundary are realization theorems, not
axioms of Definition 1.1.

---

## 2. Native morphisms

Let

\[
\mathbb X=(\mathcal G,\mathcal A,P,\ell,M,K,s),\qquad
\mathbb X'=(\mathcal G',\mathcal A',P',\ell',M',K',s').
\]

### Definition 2.1 — native \(R\)-morphism

A native morphism

\[
(F,\varphi,f):\mathbb X\longrightarrow\mathbb X'
\tag{2.1}
\]

consists of

\[
F:\mathcal G\longrightarrow\mathcal G',\qquad
\varphi:P\longrightarrow P',\qquad
f:M\longrightarrow F^*M',
\tag{2.2}
\]

where \(F\) is a functor, \(\varphi\) is monotone, and \(f\) is a natural
\(R\)-linear transformation, subject to

\[
F(\mathcal A)\subseteq\mathcal A',\qquad
\ell'F=\varphi\ell,\qquad
f(K)\subseteq F^*K'.
\tag{2.3}
\]

The last condition induces

\[
\bar f:M/K\longrightarrow F^*(M'/K').
\tag{2.4}
\]

The selected quotient class must be preserved exactly:

\[
\boxed{
\bar f|_{\mathcal A}\circ s=(F|_{\mathcal A})^*s'.
}
\tag{2.5}
\]

An orientation reversal or coefficient phase must consequently appear in
\(f\); it is not silently discarded by the definition.

---

## 3. Category formation

### Theorem 3.1 — coefficient-typed selected quotient groupoids

For every commutative ring \(R\), small \(R\)-selected quotient groupoids and
native \(R\)-morphisms form a locally small category
\(\mathbf{SQG}_R\).

#### Proof

For every object, the triple

\[
(\operatorname{id}_{\mathcal G},\operatorname{id}_P,
\operatorname{id}_M)
\tag{3.1}
\]

satisfies (2.3)--(2.5) and is its identity.

For native morphisms

\[
(F,\varphi,f):\mathbb X\to\mathbb X',\qquad
(G,\psi,g):\mathbb X'\to\mathbb X'',
\]

define

\[
(G,\psi,g)\circ(F,\varphi,f)
=
(GF,\psi\varphi,F^*g\circ f).
\tag{3.2}
\]

The module map is well typed:

\[
M\mathop{\longrightarrow}^{f}F^*M'
\mathop{\longrightarrow}^{F^*g}F^*G^*M''=(GF)^*M''.
\tag{3.3}
\]

It preserves the null subrepresentation because

\[
(F^*g\circ f)(K)
\subseteq F^*g(F^*K')
\subseteq F^*G^*K''.
\tag{3.4}
\]

Admissibility and stratum typing are preserved since

\[
(GF)(\mathcal A)\subseteq G(\mathcal A')\subseteq\mathcal A'',
\qquad
\ell''GF=\psi\ell'F=\psi\varphi\ell.
\tag{3.5}
\]

On quotients,

\[
\overline{F^*g\circ f}=F^*\bar g\circ\bar f.
\tag{3.6}
\]

Therefore

\[
\begin{aligned}
(F^*\bar g\circ\bar f)\circ s
&=F^*\bar g\circ F^*s'\\
&=F^*(\bar g\circ s')\\
&=F^*G^*s'',
\end{aligned}
\tag{3.7}
\]

which is (2.5) for the composite. Associativity follows from associativity of
functor composition and natural transformations; (3.1) is two-sided. The
groupoids are small, so functors and natural transformations between fixed
objects form sets. Hence \(\mathbf{SQG}_R\) is locally small. \(\square\)

---

## 4. Scalar extension and exact coefficient typing

### Theorem 4.1 — flat scalar extension

Let \(\rho:R\to S\) be a flat homomorphism of commutative rings. Objectwise
extension of scalars defines a functor

\[
\operatorname{Ext}_R^S:
\mathbf{SQG}_R\longrightarrow\mathbf{SQG}_S.
\tag{4.1}
\]

For flat \(R\to S\to T\), there is a canonical natural isomorphism

\[
\operatorname{Ext}_R^T
\cong
\operatorname{Ext}_S^T\circ\operatorname{Ext}_R^S.
\tag{4.2}
\]

#### Proof

Keep \(\mathcal G,\mathcal A,P,\ell\) fixed and put

\[
M_S=S\otimes_RM,\qquad K_S=S\otimes_RK.
\tag{4.3}
\]

Flatness preserves \(K\hookrightarrow M\) and yields the canonical exact
identification

\[
M_S/K_S\cong S\otimes_R(M/K).
\tag{4.4}
\]

Tensoring (1.4) and using (4.4) defines the selected class \(s_S\). A native
morphism extends by \(1\otimes f\); (2.3) and (2.5) survive tensoring.
Tensor product preserves identities and composition, proving functoriality.
The standard associativity isomorphism

\[
T\otimes_S(S\otimes_RM)\cong T\otimes_RM
\]

is natural and proves (4.2). \(\square\)

All localizations and ring inclusions in

\[
\mathbb Z
\longrightarrow
\mathbb Z[1/2],\ \mathbb Z[i]
\longrightarrow
\mathbb Z[1/2,i]
\tag{4.5}
\]

are flat; so are \(\mathbb Z\to\mathbb Q\to\mathbb C\).

### Proposition 4.2 — minimal DBP coefficient rings

In the curve-level Picard--Lefschetz quotient proved in Paper III, let
\(\delta^\uparrow,\delta^\downarrow\) be the two integral lateral classes and
\(\mu\) the primitive meridian, with

\[
\delta^\uparrow-\delta^\downarrow=-\mu.
\tag{4.6}
\]

Then the coefficient types are:

| selected class | minimal displayed coefficient ring | reason |
|---|---:|---|
| \(\delta^\uparrow,\delta^\downarrow\) | \(\mathbb Z\) | integral transport |
| \(\delta^{\rm CPV}=\tfrac12(\delta^\uparrow+\delta^\downarrow)\) | \(\mathbb Z[1/2]\) | primitive half-meridian |
| \(i\delta^\uparrow,i\delta^\downarrow\) | \(\mathbb Z[i]\) | phase \(i\) |
| \(i\delta^{\rm CPV}\) | \(\mathbb Z[1/2,i]\) | midpoint and phase |

Here “minimal displayed” means minimal among the four rings in (0.1). The
primitive endpoint-boundary obstruction proves that the \(i\)-normalized
lateral class does not descend to \(\mathbb Z\); primitivity of \(\mu\)
proves that the midpoint does not descend to \(\mathbb Z\). These are
non-descent statements, not failures of scalar extension.

---

## 5. Presentation equivalence

### Definition 5.1 — strong presentation equivalence

A native morphism
\((F,\varphi,f):\mathbb X\to\mathbb X'\) is a strong presentation
equivalence if:

\[
\begin{gathered}
F:\mathcal G\to\mathcal G'\text{ is an equivalence of groupoids},\\
F|_{\mathcal A}:\mathcal A\to\mathcal A'\text{ is an equivalence},\\
\varphi\text{ is an order isomorphism on the realized strata},\\
f:M\mathop{\longrightarrow}^{\sim}F^*M',\qquad
f(K)=F^*K'.
\end{gathered}
\tag{5.1}
\]

Two objects are **presentation-equivalent** if they are connected by a finite
zigzag of strong presentation equivalences. This is an equivalence relation,
and flat scalar extension preserves it.

This definition fixes the comparison target for the later equivalence paper.
It does not prove that any two current DBP realizations satisfy it. If the
eventual realizations require topological or analytic groupoids, (5.1) may be
strengthened to selected Morita equivalence without changing Sections 1--4.

---

## 6. Elliptic specialization and completion boundary

For the proved elliptic corridor, the specialization is:

| datum | elliptic value |
|---|---|
| \(\mathcal G\) | fundamental groupoid of one admissible parameter corridor |
| \(\mathcal A\) | its oriented lateral admissible subgroupoid |
| \(M\) | integral relative-homology local system |
| \(K\) | ordinary compact elliptic-period sub-local system |
| \(M/K\) | transport classes modulo compact periods |
| \(s\) | selected upper or lower lateral transport coset |

On the explicitly lift-generated surface subrepresentation, the Stage-2
fiber lift is a native \(\mathbb Z\)-morphism because it commutes with the
admissible continuation, sends compact elliptic cycles to compact surface
periods, and preserves the selected lateral coset. The upper and lower
corridors define separate admissible objects because their endpoint classes
differ by the pole meridian.

The following are now closed:

| status | result |
|---|---|
| closed | definition of \(\mathbf{SQG}_R\) |
| closed | native morphisms, identities, and composition |
| closed | strong presentation equivalence as a comparison notion |
| closed | flat scalar extension |
| closed | exact DBP coefficient-ring typing |

The following remain later ensemble theorems:

| status | gate |
|---|---|
| open | equivalence of the component realizations |
| open | closure under the additional operations selected for the capstone |
| open | construction of an independent third realization |
| open | any whole-surface extension beyond the native swept subrepresentation |

---

*End of Selected Quotient Groupoids, v1.0.*
