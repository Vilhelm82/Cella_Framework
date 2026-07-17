# Mathematics-First Plan for a Local Curvature Calculus

## Core objective

The central mathematical claim to develop is:

$$
\boxed{
\text{Scalar-curvature singularities of inverse-channel diagonal metrics can be read from local divisor data.}
}
$$

The goal is to replace

$$
\text{compute the full curvature scalar}
$$

with

$$
\text{compute the curvature valuation near a collapsing divisor}.
$$

The Kerr--Newman calculation should become the flagship application, not the whole foundation. The more mature body of work should be a local geometric calculus whose inputs are divisor/channel data and whose outputs are scalar-curvature pole orders, leading coefficients, and corner approach laws.

---

## Mathematics-first north star

The work should be organized around one engine:

$$
\boxed{
\text{derive the Kerr--Newman }3/4/\text{corner law from a local Lamé valuation machine, not from the full }R.
}
$$

Everything else is secondary. Prose, motivation, and arXiv polish can wait until the theorem spine exists.

---

## Master local curvature formula

For a diagonal metric

$$
g=\sum_i H_i^2 (dx^i)^2,
$$

define the Lamé coefficients

$$
H_i=\sqrt{g_i},
\qquad
\beta_{ij}:=\frac{\partial_i H_j}{H_i},
\qquad i\neq j.
$$

The sectional curvature of the coordinate \(ij\)-plane is

$$
K_{ij}
=
-\frac{1}{H_iH_j}
\left(
\partial_i\beta_{ij}
+
\partial_j\beta_{ji}
+
\sum_{k\neq i,j}\beta_{ki}\beta_{kj}
\right).
$$

Therefore the scalar curvature is

$$
\boxed{
R
=
-2\sum_{i<j}
\frac{1}{H_iH_j}
\left(
\partial_i\beta_{ij}
+
\partial_j\beta_{ji}
+
\sum_{k\neq i,j}\beta_{ki}\beta_{kj}
\right).
}
$$

This should become the first engine lemma. The local valuation calculus should be derived from this formula.

---

## Main theorem ladder

### Lemma 1 — Diagonal scalar-curvature formula

Prove the Lamé scalar-curvature formula for diagonal metrics.

This is the computational source for all valuation statements.

---

### Theorem 1 — Constant-exponent single-face theorem

Let

$$
g
=
B x^a dx^2
+
\sum_{\alpha=1}^{m} A_\alpha x^{b_\alpha}dy_\alpha^2,
\qquad
A_\alpha,B>0,
$$

with constant leading units.

Then the leading radial scalar-curvature term is

$$
\boxed{
R
=
\frac{
2(a+2)\sum_\alpha b_\alpha
-
\sum_\alpha b_\alpha^2
-
\left(\sum_\alpha b_\alpha\right)^2
}
{4B}
x^{-(a+2)}
+
\cdots .
}
$$

This theorem should make the special cases look structural, not bespoke.

---

### Corollary 1 — Parity-fixed inverse-channel face

For the parity-fixed inverse-channel face,

$$
a=2,
\qquad
b_\alpha=-2
\quad
\text{for all }\alpha.
$$

Then

$$
\sum_\alpha b_\alpha=-2m,
\qquad
\sum_\alpha b_\alpha^2=4m,
$$

so Theorem 1 gives

$$
R
=
-\frac{m(m+5)}{B}x^{-4}
+
\cdots .
$$

Thus

$$
\boxed{
R
=
-\frac{m(m+5)}{B}x^{-4}
+
O(x^{-2}).
}
$$

For \(m=2\),

$$
R=-\frac{14}{B}x^{-4}+O(x^{-2}),
$$

which is the structural source of the Kerr--Newman reflection-face coefficient.

---

### Corollary 2 — Generic extremal collapse is a cancellation case

For generic extremal collapse,

$$
a=2,
\qquad
b_\alpha=0.
$$

Then the \(x^{-4}\) coefficient in Theorem 1 vanishes. The generic face therefore drops to the next term.

Assume

$$
g_x=A x^2+O(x^3),
$$

and

$$
g_{y_\alpha}=P_{\alpha0}+P_{\alpha1}x+O(x^2).
$$

Then

$$
\boxed{
R
=
\frac{1}{A}
\sum_{\alpha=1}^{m}
\frac{P_{\alpha1}}{P_{\alpha0}}
x^{-3}
+
O(x^{-2}).
}
$$

Conceptual message:

$$
\boxed{
\text{Generic quadratic collapse detects transverse first drift.}
}
$$

This explains why the Kerr--Newman extremal face has an order-3 pole and why its coefficient is governed by transverse monotonicity.

---

### Theorem 2 — Finite-jet principle

Do **not** claim that exponent data alone determines the pole in all cases.

The correct statement is:

$$
\boxed{
\text{The curvature pole is determined by exponent data plus a finite leading-unit jet.}
}
$$

More precisely:

- For parity-fixed inverse-channel faces, the zeroth leading units determine the \(x^{-4}\) coefficient.
- For generic quadratic collapse, the \(x^{-4}\) term cancels and the \(x^{-3}\) coefficient depends on the first transverse unit drift.
- For corners, the surviving Newton face coefficients are required.

This distinction is not a nuisance. It is the calculus.

---

## Definitions to build cleanly

### Diagonal divisor-monomial metric germ

Near a normal-crossing divisor

$$
D=\{x_1\cdots x_k=0\},
$$

consider a diagonal metric

$$
g=\operatorname{diag}(g_0,\ldots,g_m)
$$

where each coefficient has a monomial-unit expansion

$$
g_i
=
h_i(x,y)
x_1^{p_{i1}}\cdots x_k^{p_{ik}},
\qquad
h_i(0,y)\neq 0.
$$

Call this a **diagonal divisor-monomial metric germ**.

Useful notions:

- collapsing coordinate;
- transverse channel;
- metric valuation;
- parity-fixed germ;
- curvature valuation;
- boundary defining function;
- canonical channel coordinate.

The key scalar object is

$$
\operatorname{val}_D(R[g]),
$$

the pole order of scalar curvature along the divisor \(D\).

---

### Inverse-channel subclass

The inverse-channel subclass should not be merely motivational. It should impose extra structure.

At a parity-fixed face, the characteristic pattern is

$$
g_x\sim Bx^2,
\qquad
g_{y_\alpha}\sim A_\alpha x^{-2}.
$$

More generally, inverse-channel assemblies should arise from channel functions \(\Lambda_\rho\) through entries of the form

$$
g_{ii}
\sim
\sum_\rho
\Lambda_\rho^{-2}
\times
\text{unit}.
$$

This distinguishes the project from arbitrary diagonal metric asymptotics.

---

## Coordinate robustness

Coordinate robustness should be proved as a valuation statement, not as a claim that diagonal form is preserved.

Under a boundary-adapted coordinate change

$$
x'=c(y)x+O(x^2),
\qquad
c(y)>0,
$$

the functions \(x\) and \(x'\) generate the same divisor filtration.

Therefore the scalar pole order of \(R[g]\) is invariant.

If

$$
R\sim C(y)x^{-r},
$$

then in the new defining function,

$$
R\sim C(y)c(y)^r(x')^{-r}.
$$

So:

$$
\boxed{
\text{pole order is invariant, while the coefficient depends on the defining function.}
}
$$

The coefficient becomes meaningful only after choosing a canonical defining function, such as a channel coordinate \(x=\Lambda\) or a role divisor coordinate \(J,Q,U_S\).

Important warning:

Boundary-adapted coordinate changes can introduce off-diagonal metric terms. The theorem should not claim diagonality is preserved. The correct statement is:

$$
\boxed{
\text{the diagonal normal form is a computational gauge; the scalar valuation is coordinate-invariant.}
}
$$

---

## Corner calculus

The codimension-two case is probably the strongest novelty candidate.

Let

$$
D=\{xy=0\}.
$$

Start with monomial data

$$
g_i=h_i(s)x^{p_i}y^{q_i}.
$$

For pure monomial diagonal data, the curvature support should be controlled by candidate vertices of the form

$$
V_x=(-(p_x+2),-q_x),
$$

$$
V_y=(-p_y,-(q_y+2)),
$$

and, for a spectator coordinate \(s\),

$$
V_s=(-p_s,-q_s).
$$

More generally, the scalar curvature should have a finite curvature Newton support generated by the Lamé curvature terms:

$$
\frac{\partial_i\beta_{ij}}{H_iH_j},
\qquad
\frac{\partial_j\beta_{ji}}{H_iH_j},
\qquad
\frac{\beta_{ki}\beta_{kj}}{H_iH_j}.
$$

---

### Theorem 3 — Codimension-two curvature Newton support

A target theorem:

> Let \(g\) be a diagonal Newton-admissible metric germ near \(D=\{xy=0\}\). Then \(R[g]\) has a finite curvature Newton support \(\mathcal V_R(g)\) generated by the Lamé curvature terms. Along \(x=\rho\varepsilon^a,\ y=\varepsilon^b\), the scalar-curvature pole order is
>
> $$
> m(a,b)
> =
> \max_{v\in\mathcal V_R(g)}
> -\langle (a,b),v\rangle,
> $$
>
> after deleting vertices whose leading face coefficients vanish at the slope.

The deletion clause is essential. Without it, the theorem is only tropical bookkeeping. With it, it becomes a curvature theorem.

---

### Cancellation / deletion rule

Write the leading expansion along a weighted approach as

$$
R
=
\sum_v
C_v(\rho,s)\varepsilon^{\langle w,v\rangle}
+
\text{higher weighted order}.
$$

A candidate vertex survives if

$$
C_v(\rho,s)\not\equiv 0
$$

on the relevant slope chamber.

Equivalently,

$$
v\in\mathcal V_R^{\mathrm{surv}}
\quad\Longleftrightarrow\quad
C_v(\rho,s)\not\equiv 0.
$$

This is where the real mathematics lives: structural cancellations, surviving mixed-channel terms, and corner transitions.

---

## Beyond monomial-unit germs

The Kerr--Newman corner is probably too rich for the smallest monomial-unit class.

The balanced corner has slope-dependent leading coefficients, for example terms depending on

$$
(s+8\pi\rho^2)^2.
$$

That is not captured by a single monomial unit in \(J,Q\). It is a Newton/blow-up leading form.

So the mature class should allow rational Newton-admissible germs:

$$
g_i
=
x^{p_i}y^{q_i}
\frac{F_i(x,y,s)}{G_i(x,y,s)},
$$

where \(F_i,G_i\) have finite Newton leading support and positive nonvanishing face polynomials on the relevant blown-up quadrant.

For a weighted approach

$$
x=\rho\varepsilon^a,
\qquad
y=\varepsilon^b,
$$

define

$$
\nu_{a,b}(F)
=
\min_{(\mu,\nu)\in \operatorname{supp}(F)}
(a\mu+b\nu).
$$

For rational germs,

$$
\nu_{a,b}\!\left(\frac{F}{G}\right)
=
\nu_{a,b}(F)-\nu_{a,b}(G),
$$

provided the leading face polynomial does not vanish at the slope.

---

## Generalization to codimension \(k\)

Do not fully solve this immediately. State it as a conjecture or partial theorem after codimension two is solid.

For

$$
D=\{x_1\cdots x_k=0\},
$$

and

$$
g_i=h_i x_1^{p_{i1}}\cdots x_k^{p_{ik}},
$$

seek a finite set of curvature exponent vectors

$$
\mathcal V(g)\subset \mathbb Z^k
$$

such that along

$$
x_j=\varepsilon^{a_j},
$$

the curvature pole order is

$$
m(a)
=
\max_{v\in\mathcal V(g)}
-\langle a,v\rangle.
$$

This would be the mature form of the theory:

$$
\boxed{
\text{scalar-curvature asymptotics become tropical/Newton-polytope data.}
}
$$

---

## Kerr--Newman as flagship application

Only after the local theory is clear should the Kerr--Newman application be presented.

The structure should be:

$$
\text{local theorem}
\Longrightarrow
\text{KN divisor classification}
\Longrightarrow
\text{no need to print the massive curvature fraction}.
$$

The current Kerr--Newman divisor table is:

| Divisor | Local type | Pole order |
|---|---:|---:|
| \(T=0\) | generic quadratic collapse | \(3\) |
| \(\Omega=0\), equivalently \(J=0\) | parity-fixed inverse-channel face | \(4\) |
| \(\Phi_e=0\), equivalently \(Q=0\) | parity-fixed inverse-channel face | \(4\) |
| \(J=Q=0\) | codimension-two corner | Newton polygon / approach-dependent |

The KN paper then becomes evidence that the local calculus solves a real computational problem.

---

## Minimal example set

Use only a small number of examples.

1. Generic quadratic collapse.
2. Parity-fixed inverse-channel face.
3. Kerr--Newman Schwarzschild corner.
4. One synthetic non-Kerr--Newman example.

Avoid a catalog. A catalog dilutes the theorem spine.

---

## Reproducibility layer

For each theorem:

1. give a human-readable proof;
2. give a small symbolic verification script;
3. give one minimal example;
4. give one failure/cancellation example.

The certificates should verify:

- generic single-face collapse;
- parity-fixed single-face collapse;
- codimension-two vertex rule;
- Kerr--Newman divisor reductions.

But the proofs must stand without the code.

---

## Immediate work order

The next mathematical deliverable should be a short internal theorem sheet.

Include only:

1. Lemma 1: Lamé formula for diagonal scalar curvature.
2. Theorem 1: constant-exponent single-face coefficient.
3. Theorem 2: generic-collapse post-cancellation coefficient.
4. Theorem 3: parity-fixed inverse-channel coefficient.
5. Theorem 4: codimension-two curvature Newton support.
6. Kerr--Newman divisor table.

Everything else can wait.

---

## What not to overclaim

Do not claim:

$$
\text{exponent data alone determines the curvature pole.}
$$

It does not.

The generic collapse coefficient depends on

$$
\sum_\alpha \frac{P_{\alpha1}}{P_{\alpha0}}.
$$

So two metrics can have the same valuation vector and different leading curvature behaviour if this sum cancels.

The correct claim is:

$$
\boxed{
\text{the pole is determined by exponent data plus a finite leading-unit jet.}
}
$$

Do not lead with black-hole physics claims.

Do not claim the metric is “the correct thermodynamic metric.”

Do not rely on large CAS output as evidence.

Do not make the whole project depend on the DBP interpretation.

Instead, lead with:

$$
\boxed{
\text{a local geometric theorem about curvature poles.}
}
$$

Then use Kerr--Newman as a natural hard application.

---

## Possible paper architecture

### Paper 1 — Mathematical core

Possible title:

> Curvature Valuations of Diagonal Metrics Near Collapsing Divisors

Main content:

- Lamé scalar-curvature formula;
- single-face normal forms;
- parity-fixed inverse-channel theorem;
- finite-jet principle;
- coordinate robustness;
- codimension-two Newton polygon rule;
- synthetic examples;
- Kerr--Newman divisor table as a teaser or application.

### Paper 2 — Kerr--Newman application

Possible title:

> Inverse-Channel Curvature and Role-Divisor Singularities in Kerr--Newman Thermodynamics

Main content:

- DBP/inverse-channel metric;
- selection theorem;
- rationality and interior regularity;
- application of the local calculus;
- exact \(3/4/4\) complementarity law;
- Schwarzschild corner behaviour;
- reproducibility package.

---

## Highest-value next step

Write a short internal document called:

> Definitions and Theorem Statements for Curvature Valuations

Include only:

1. the class of metric germs;
2. the definition of curvature valuation;
3. Theorem A: constant-exponent single face;
4. Theorem B: generic quadratic face;
5. Theorem C: parity-fixed inverse-channel face;
6. Theorem D: codimension-two Newton polygon;
7. one Kerr--Newman table.

No motivation, no physics, no arXiv formatting.

Once those theorem statements are crisp, the project has a real spine.

---

## Bottom line

The research direction is:

$$
\boxed{
\text{develop a local divisor-valued scalar-curvature calculus for diagonal inverse-channel metrics.}
}
$$

The Kerr--Newman computation is the motivating hard example. The normal-form and Newton-polytope theory is the likely mathematical novelty.
