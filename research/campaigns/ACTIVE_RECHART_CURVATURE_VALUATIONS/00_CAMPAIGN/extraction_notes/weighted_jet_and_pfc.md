# Extraction note: variable-transverse weighted-jet theorem + PFC normal forms + companion dual-constant block

Campaign: ACTIVE_RECHART_CURVATURE_VALUATIONS. Prefix for all IDs: `WEIGHTED_JET_AND_PFC`.
Extraction date: 2026-07-30. All statements quoted verbatim from source; no equation is paraphrased.

---

## 1. SOURCE LIST

| # | File | Role |
|---|------|------|
| S1 | `01_SOURCES_CORE/paper_II_local_curvature/LEAD7_VARIABLE_TRANSVERSE_WEIGHTED_JET_THEOREM_v1.0.md` | Extension of the diagonal LEAD-7 germ laws to arbitrary transverse-coordinate-dependent coefficients (m=2, channels named P,R), with weighted-valuation proof and exact SymPy replay metadata. |
| S2 | `01_SOURCES_CORE/paper_II_local_curvature/pfc_normal_forms.tex` | Draft paper: parity-fixed inverse-channel normal forms for general m; pure normal form (exact), asymptotic face corollary, generic collapse, codim-2 corner Newton polytope, corner vertex rule, Kerr-Newman m=2 application. |
| S3 | `09_HISTORICAL_REFERENCE/LOCAL_CURVATURE_CALCULUS_COMPANION.md` | Self-containment companion to `Local_Curvature_Calculus_for_Inverse-Channel_Metrics.txt`: frozen definitions, Theorems A/B, intrinsic gauge Lemma E2, master quadric, boundary robustness, Lame formula (engine E1), Kerr-Newman tables, and the dual-constant block (global context only). |

Referenced verification scripts (all confirmed present in repo, e.g. under `research/campaigns/ACTIVE_RECHART_CURVATURE_VALUATIONS/04_VERIFICATION_LEGACY/` and `Papers_Library/07_certificates_data_and_reproducibility/local_curvature_and_black_hole_metrics/`):
`verify_lead7_variable_transverse_weighted_jet.py`, `pfc_test1_local_normal_forms.py`, `pfc_test2_corner_valuation.py`, `pfc_test3_vertex_rule.py`. S2 also cites `lead7_test6,7,8,9,10` for the Kerr-Newman instances.

---

## 2. EXACT STATEMENTS

### From S1 (LEAD-7 variable-transverse weighted-jet theorem, v1.0)

#### [WEIGHTED_JET_AND_PFC-T1] Variable-transverse weighted-jet theorem, generic germ (m=2, variable coefficients)

Hypotheses (verbatim): "Let (x) be the collapsing coordinate and let all displayed coefficients be arbitrary sufficiently differentiable functions of transverse coordinates ((y,z))." Generic diagonal germ, with `A_2 P_0 R_0 != 0`:

```
g=\operatorname{diag}
\left(A_2x^2+A_3x^3+O(x^4),
P_0+P_1x+O(x^2),
R_0+R_1x+O(x^2)\right),
```

Conclusion:

```
R[g]=
\frac{P_1/P_0+R_1/R_0}{A_2}\,x^{-3}+O(x^{-2}).
```

Weighted jet that determines the leading coefficient: `(A_2; P_0, P_1; R_0, R_1)` — the weight-2 coefficient of g_xx and the 1-jets of both transverse channels. `A_3` and all higher data do not enter.

#### [WEIGHTED_JET_AND_PFC-T2] Variable-transverse weighted-jet theorem, reflection germ (m=2, variable coefficients)

Hypotheses: same variable-coefficient convention; reflection germ with `B C_1 C_2 != 0`:

```
g=\operatorname{diag}
\left(Bx^2+B_4x^4+O(x^6),
C_1x^{-2}+C_{10}+O(x^2),
C_2x^{-2}+C_{20}+O(x^2)\right),
```

Conclusion:

```
R[g]=-\frac{14}{B}\,x^{-4}+O(x^{-3}).
```

Weighted jet that determines the leading coefficient: `B` alone (weight-2 coefficient of g_xx). Verbatim on the corrections: "The corrections (B_4,C_{10},C_{20}) begin two valuation steps later and cannot change this coefficient."

#### [WEIGHTED_JET_AND_PFC-T3] No-transverse-derivative claim

Verbatim: "Neither leading coefficient contains a (y)- or (z)-derivative of any coefficient function."

(Replay-checked as "absence of transverse derivative atoms in both coefficients"; also checked: "absence of any more singular scalar-curvature terms in both germs", i.e. no pole worse than x^{-3} / x^{-4} respectively.)

#### [WEIGHTED_JET_AND_PFC-T4] Weighted-valuation dominant part (proof engine of T1-T3)

With `E=g_xx`, `P=g_yy`, `Q=g_zz`; "Transverse differentiation preserves (x)-valuation, while differentiation by (x) lowers it by one." The part of scalar curvature capable of reaching the lowest valuations for a diagonal metric:

```
-\frac{P_{xx}}{EP}-\frac{Q_{xx}}{EQ}
+\frac{P_x^2}{2EP^2}+\frac{Q_x^2}{2EQ^2}
-\frac{P_xQ_x}{2EPQ}
+\frac{E_xP_x}{2E^2P}+\frac{E_xQ_x}{2E^2Q}.
```

Verbatim valuation bound: "All omitted terms contain a transverse derivative. Direct valuation of the diagonal Christoffel formula shows those terms have valuation at least (-2) in the generic germ and at least (-3) in the reflection germ. They therefore cannot contribute to (x^{-3}) or (x^{-4}), respectively."

#### [WEIGHTED_JET_AND_PFC-T5] Generic-germ term identification

For generic valuations `(v(E),v(P),v(Q))=(2,0,0)`, only the last two terms of T4 reach valuation -3:

```
\frac{E_xP_x}{2E^2P}\sim\frac{P_1}{A_2P_0}x^{-3},
\qquad
\frac{E_xQ_x}{2E^2Q}\sim\frac{R_1}{A_2R_0}x^{-3}.
```

#### [WEIGHTED_JET_AND_PFC-T6] Reflection-germ per-term contributions

For reflection valuations `(2,-2,-2)`, the seven displayed terms of T4 contribute, in order,

```
-\frac6B,-\frac6B,
+\frac2B,+\frac2B,
-\frac2B,-\frac2B,-\frac2B,
```

to the x^{-4} coefficient; "Their sum is (-14/B)."

#### [WEIGHTED_JET_AND_PFC-T7] Replay certificate metadata (S1)

`verify_lead7_variable_transverse_weighted_jet.py`: finite Laurent jet ring, arbitrary SymPy functions of (y,z), truncated Christoffel/Ricci assembly; "It passed six exact assertions in 1.257 seconds": both leading coefficients; absence of transverse-derivative atoms in both; absence of more singular terms in both germs.

#### [WEIGHTED_JET_AND_PFC-T8] Scope boundary (S1)

Verbatim: "This closes the arbitrary-transverse-coefficient extension of the diagonal LEAD-7 local-germ laws. It does not prove full role-rechart covariance, which still requires the off-diagonal tensor pullback and curvature replay."

---

### From S2 (pfc_normal_forms.tex)

Setting: `g = diag(g_x, g_{y_1}, ..., g_{y_m})` diagonal on an (m+1)-dimensional state space near a face {x=0}; R = scalar curvature. Parity convention: "A germ is parity-fixed if every component is even in x (invariant under x -> -x); then R is even in x and all odd-order poles vanish identically."

#### [WEIGHTED_JET_AND_PFC-T9] Theorem 1 (thm:pure) — Pure parity-fixed normal form (EXACT, all orders)

Hypotheses: `m >= 1`, `B > 0`, `A_alpha > 0`.

```
\dd s^2=Bx^2\,\dd x^2+x^{-2}\sum_{\alpha=1}^{m}A_\alpha\,\dd y_\alpha^2,
```

Conclusion — the scalar curvature is exactly

```
R=-\frac{m(m+5)}{B}\,x^{-4},
```

"independent of all transverse amplitudes A_alpha. In particular m=2 gives R = -14 x^{-4}/B."

Proof mechanism (recorded because it is unique to S2): substitution `r = (1/2)\sqrt{B} x^2`, so `\dd r=\sqrt B\,x\,\dd x` and `x^{-2}=\sqrt B/(2r)`; warped product `\dd s^2=\dd r^2+w(r)^2 h_{flat}` with `w^2=\sqrt B/(2r)`, i.e. `w \propto r^{-1/2}`; flat-fibre warped-product formula

```
R=-2m\,w''/w-m(m-1)(w'/w)^2;
```

with `w'/w=-1/(2r)` and `w''/w=3/(4r^2)`,

```
R=-\frac{6m}{4r^2}-\frac{m(m-1)}{4r^2}=-\frac{m(m+5)}{4r^2},
```

and `4r^2=Bx^4`. Interpretation: "radial focusing (6m)" plus "transverse fibre shear (m(m-1))"; amplitudes cancel because they only rescale a flat fibre.

#### [WEIGHTED_JET_AND_PFC-T10] Corollary 2 (cor:asymp) — Asymptotic parity-fixed face

Hypotheses: near x=0, with all components even in x,

```
g_x=B(y)x^2+O(x^4),\qquad g_{y_\alpha}=A_\alpha(y)x^{-2}+O(1),\qquad B,A_\alpha>0,
```

Conclusion:

```
R=-m(m+5)\,x^{-4}/B(y)+O(x^{-2}).
```

"The odd pole x^{-3} is absent by parity, and the leading coefficient is independent of the amplitudes A_alpha(y) and of all even subleading data." (Note the remainder is O(x^{-2}), stronger than S1's O(x^{-3}) — see RED FLAGS RF4.)

#### [WEIGHTED_JET_AND_PFC-T11] Proposition 3 (prop:generic) — Generic quadratic collapse (general m)

Hypotheses: transverse channels stay finite, germ breaks parity at first order:

```
g_x=Ax^2+O(x^3),\qquad g_{y_\alpha}=P_{\alpha0}+P_{\alpha1}x+O(x^2),\qquad A,P_{\alpha0}\neq0.
```

Conclusion:

```
R=\frac1A\sum_{\alpha=1}^{m}\frac{P_{\alpha1}}{P_{\alpha0}}\,x^{-3}+O(x^{-2})
=\frac1A\sum_{\alpha}\partial_x\log P_\alpha\Big|_{0}\,x^{-3}+O(x^{-2}),
```

"independent of A_3 and of the quadratic transverse data P_{alpha 2}." (A_3 is not defined in the hypothesis line — see RF5.)

Mechanism statement (prose, verbatim gist kept): the odd x^{-3} pole is produced by the parity-breaking linear drift P_{alpha 1}; a parity-fixed face has no drift, so the x^{-3} term vanishes identically and the leading pole is the even x^{-4} term with dimension-universal coefficient -m(m+5)/B. "The order is not an accident of a particular fundamental relation; it is read off the parity of the germ."

#### [WEIGHTED_JET_AND_PFC-T12] Proposition 4 (prop:corner) — Codimension-2 corner valuation (Newton-polytope rule)

Hypotheses: two faces {x=0} and {y=0} meet at a corner, with single-face curvature orders `p_x, p_y` and corner-residue weights `r_x, r_y` ("the power with which each face's leading coefficient vanishes or blows up on approach to the corner").

Conclusion: near the corner R has a polar Newton polytope with vertices

```
v_x=(-p_x,\,r_y),\qquad v_y=(r_x,\,-p_y),
```

and along `x=\rho\,\epsilon^{a_x}`, `y=\epsilon^{a_y}` the order is the support function

```
m(a)=\max_{v}\bigl(-\langle a,v\rangle\bigr)=\max\bigl(p_x a_x-r_y a_y,\ p_y a_y-r_x a_x\bigr).
```

Stated consequences: (i) order is piecewise linear; `min_a m(a)` can drop below both single-face orders — "two order-4 faces can meet at an order-2 corner"; (ii) at a facet-parallel (balanced) direction the leading coefficient collects the entire facet — a projective "front-face coefficient" neither single face resolves; (iii) face data and raw metric weights are equivalent inputs via the explicit shift in T13. Verification stated only "for synthetic (4,4) and (4,3) corners by direct curvature (certificate pfc_test2)" — see RF2.

#### [WEIGHTED_JET_AND_PFC-T13] Theorem 5 (thm:vertex) — Corner vertex rule (closed identity)

Setting: weight form `g_i=h_i(s)\,x^{p_i}y^{q_i}\,u_i` with `u_i` a corner unit (`i=0` spectator, `1,2` the two coordinates x,y).

Conclusion: the polar part of R near the corner is supported on at most the three monomials

```
V_1=(-(p_1+2),-q_1),\quad V_2=(-p_2,-(q_2+2)),\quad V_0=(-p_0,-q_0),
```

with coefficients `A(p_0,p_1,p_2)/(2h_1)`, `B(q_0,q_1,q_2)/(2h_2)`, and an s-jet `C_0`, where

```
A=-p_0^2+p_0p_1-p_0p_2+2p_0+p_1p_2-p_2^2+2p_2,
```

"B the same in the q's" (see RF1 for the ambiguity), and `C_0` depends only on `(h_i, h_i', h_i'')`. The corner order is the support function of the polar, nonzero-coefficient vertices. Dictionary to T12:

```
p_x=p_1+2,\quad p_y=q_2+2,\quad r_x=-p_2,\quad r_y=-q_1,
\quad\text{giving}\quad V_1=(-p_x,r_y),\ V_2=(r_x,-p_y).
```

Cancellation condition: "A vertex disappears exactly when its coefficient vanishes (A=0, B=0, or a degenerate s-jet)"; "the spectator vertex V_0 contributes only when it is polar (p_0>0 or q_0>0)."

Proof status (verbatim): "The theorem is proved by an exact scalar-curvature computation with symbolic weights (certificate pfc_test3); unit factors leave the vertices, hence the order, unchanged." (See RF3.)

Kerr-Newman instantiation (verbatim data): `g_S ~ x^{-6}`, `g_Q ~ x^2 y^{-2}`, `g_J ~ x^{-2} y^2`; spectator `V_0=(6,0)` non-polar; `A=-84 != 0`, `B=-12 != 0`; polytope `{V_1,V_2}={(-4,2),(2,-4)}`; `m(a)=\max(4a-2,4-2a)`.

Open (verbatim): "Codimension >= 3 (a Newton polytope in R^k) and the front-face coefficient classification remain open."

#### [WEIGHTED_JET_AND_PFC-T14] Kerr-Newman m=2 divisor table (S2 version, with leading coefficients)

```
divisor                          | local type                       | order | leading coefficient
T=0 (extremal)                   | generic collapse (Prop. generic) | 3     | A_2^{-1} \partial_S \log(G_J G_Q)|_ext
Omega=0 (spin)                   | parity-fixed (Cor. asymp)        | 4     | -14/B_J
Phi_e=0 (charge)                 | parity-fixed (Cor. asymp)        | 4     | -14/B_Q
Omega=Phi_e=0 (Schwarzschild)    | double corner (Sec. corner)      | wedge | mixed stratum
```

Verbatim gloss: "The number 14 is 6*2 + 2*1: radial focusing plus transverse fibre shear for a two-dimensional fibre."

#### [WEIGHTED_JET_AND_PFC-T15] Certificate mapping (S2)

thm:pure ("first-principles Ricci for m=1,...,4 and the symbolic-in-m warped reduction"), cor:asymp, prop:generic -> `verification/pfc_test1_local_normal_forms.py`; prop:corner -> `verification/pfc_test2_corner_valuation.py`; thm:vertex (closed symbolic identity) -> `verification/pfc_test3_vertex_rule.py`. "All are run twice with identical output. The Kerr-Newman instances are in lead7_test6,7,8,9,10."

---

### From S3 (LOCAL_CURVATURE_CALCULUS_COMPANION.md)

#### [WEIGHTED_JET_AND_PFC-T16] Frozen definitions (Companion Sec. 1)

1.1 Diagonal divisor-monomial metric germ: `g = diag(g_0,...,g_m)` near normal-crossing divisor `D={x_1...x_k=0}` with

```
g_i = h_i(x,y)\, x_1^{p_{i1}}\cdots x_k^{p_{ik}},\qquad h_i(0,y)\ne 0.
```

1.2 Inverse-channel subclass (parity-fixed face): `g_x ~ B x^2`, `g_{y_alpha} ~ A_alpha x^{-2}`, all components even in x.

1.3 Curvature valuation: `val_D(R[g]) := pole order of the scalar curvature R along D`.

1.4 Metric valuation vector: the exponent matrix `(p_i)` (or `(p_i,q_i)` in codimension two).

#### [WEIGHTED_JET_AND_PFC-T17] Theorem A — Generic quadratic collapse (Companion)

Hypothesis:

```
g_x = A x^2 + O(x^3),\qquad
g_{y_\alpha} = P_{\alpha 0} + P_{\alpha 1} x + O(x^2).
```

Conclusion:

```
R = \frac{1}{A} \sum_{\alpha=1}^{m} \frac{P_{\alpha 1}}{P_{\alpha 0}} \, x^{-3} + O(x^{-2}).
```

"Message. Generic collapse detects transverse first drift. Pole order = 3; leading coefficient = transverse first drift scaled by 1/A." (Identical content to T11; note S3 omits the nondegeneracy condition `A, P_{alpha 0} != 0` that S2 states — RF5.)

#### [WEIGHTED_JET_AND_PFC-T18] Theorem B — Parity-fixed inverse-channel face (Companion)

Hypothesis:

```
g_x = B x^2 + O(x^4),\qquad
g_{y_\alpha} = A_\alpha x^{-2} + O(1),
```

all components even in x. Conclusion:

```
R = -\frac{m(m+5)}{B}\, x^{-4} + O(x^{-2}).
```

Exact model (pure parity-fixed):

```
ds^2 = B x^2\, dx^2 + x^{-2}\sum_{\alpha=1}^{m} A_\alpha\, dy_\alpha^2
\quad\Longrightarrow\quad
R = -\frac{m(m+5)}{B}\, x^{-4}.
```

Special case m=2 (Kerr-Newman faces):

```
R = -\frac{14}{B}\, x^{-4}.
```

#### [WEIGHTED_JET_AND_PFC-T19] Lemma E2 — Intrinsic (metric-distance) gauge

Let d be proper distance to the face.

Parity-fixed faces:

```
R\cdot d^2 \equiv -\frac{m(m+5)}{4}
```

"(pure number; the collapsing amplitude B is completely absorbed)."

Generic faces: intrinsic rate `d^{-3/2}`; more precisely

```
\lim R\cdot d^{3/2} = \Bigl(\sum\frac{P_{\alpha1}}{P_{\alpha0}}\Bigr) A^{-1/4}/2^{3/2}.
```

"This is the coordinate-free form that kills the objection 'pole order is a chart artifact.'" (Both formulas independently rechecked here from T11/T18 via d = sqrt(A or B) x^2/2: they are correct.)

#### [WEIGHTED_JET_AND_PFC-T20] Master quadric

```
C(p) = -\frac12 \Biggl( \sum_a p_a^2 + \sum_{a<b} p_a p_b - (p_0+2)\sum_a p_a \Biggr).
```

Three jobs: (1) single-face monomial coefficient; (2) both corner vertex coefficients (evaluate per face); (3) cancellation condition (vanishing locus of C).

Key evaluation:

```
C(2,-2,\dots,-2) = -m(m+5).
```

Vanishing locus contains: generic faces (`p_a=0`); flat cones; scalar-flat isotropic exponents `p_a = 4/(m+1)` — "(the metric dr^2 + \sum r^{4/(m+1)} dy^2 is exactly scalar-flat, not merely leading-order)."

Index convention here: `p_0` = collapsing-coordinate exponent of g_xx, `p_a` (a=1..m) = transverse exponents. Cross-check against T13: for the KN x-face, C evaluated per face gives -42 while T13's A = -84 = 2C; the vertex coefficient in T13 is A/(2h_1) = C/h_1 — a factor-2 bookkeeping difference between S2 and S3 that is nowhere documented (RF7).

#### [WEIGHTED_JET_AND_PFC-T21] Boundary robustness (E2, computer-verified claims)

Under a boundary-adapted change

```
x = c(y)\, x' + k\, (x')^2,\qquad c>0,
```

- transformed collapsing amplitude: `B' = B c^4`;
- order-4 pole law form-invariant read with B':

```
\text{leading coefficient} = -\frac{m(m+5)}{B'};
```

- "the odd (order-3) coefficient vanishes if and only if the change preserves parity (k=0)."

"Thus pole order is invariant, and the normalised leading coefficient is form-invariant under parity-preserving boundary changes."

#### [WEIGHTED_JET_AND_PFC-T22] Codimension-two corner data (Companion Sec. 6)

For a normal-crossing corner D={xy=0}, polar support of R controlled by vertices

```
V_1 = \bigl(-(p_1+2),-q_1\bigr),\quad
V_2 = \bigl(-p_2,-(q_2+2)\bigr),\quad
V_0 = (-p_0,-q_0)
```

"after deletion of vertices whose coefficients vanish (master-quadric cancellation)."

Kerr-Newman spectator fan (validated cross-check):
- Wedge support: `max(4a-2, 4-2a)`.
- Vertex coefficients (balanced assignment): `A=-84`, `B=-12`.
- Sector-weight alternative (one side): `-28 = 2*(-14)`.
- "(The B1 crown experiment decides which weighting is realised.)" (RF6.)

#### [WEIGHTED_JET_AND_PFC-T23] Kerr-Newman divisor table (Companion Sec. 7 version, no coefficients)

```
Divisor              | Local type       | Pole order
T=0                  | generic collapse | 3
Omega=0 or J=0       | parity-fixed     | 4
Phi_e=0 or Q=0       | parity-fixed     | 4
J=Q=0                | corner           | Newton polygon
```

(Note the divisor labels differ from T14: S3 identifies Omega=0 with J=0 and Phi_e=0 with Q=0; T14 uses Omega=Phi_e=0 = Schwarzschild for the corner where S3 uses J=Q=0.)

#### [WEIGHTED_JET_AND_PFC-T24] Lame formula (engine E1)

For a diagonal metric `g=\sum_i H_i^2 (dx^i)^2` with Lame coefficients H_i and

```
\beta_{ij} = \frac{\partial_i H_j}{H_i}\quad(i\neq j),
```

the scalar curvature is

```
R = -2\sum_{i<j} \frac{1}{H_i H_j}
\Biggl[ \partial_i\beta_{ij} + \partial_j\beta_{ji}
+ \sum_{k\neq i,j} \beta_{ki}\beta_{kj} \Biggr].
```

Verification status (verbatim): "Verified for fully general n=3; n=4 polynomial fixtures exist but need lightening before re-run." (RF8.)

#### [WEIGHTED_JET_AND_PFC-T25] Dual-constant block (Companion Sec. 9; global context only, "Not required by the local calculus")

Primary (physical total curvature):

```
I_{\rm primary} = -2^{7/4} \Bigl[ (3+2\sqrt{2})\,\Pi(n;k^2) - (2+2\sqrt{2})\,K(k^2) \Bigr],
```

with

```
k^2=(2-\sqrt{2})/4,\qquad n=(4-3\sqrt{2})/8.
```

Numerical pin:

```
I_{\rm primary} \approx -5.01049070266041876905\ldots
```

Dual (Galois conjugate, CPV): obtained by `\sqrt{2} \mapsto -\sqrt{2}`;

```
I_{\rm dual,CPV} \approx -3.98800108597455809772\ldots
```

"Residue of the DBP-weighted third-kind differential = exactly 4; one-sided jumps +-4\pi i."

Status (verbatim): "Status of dual as physical ambient light: unsupported until a cycle is exhibited."

#### [WEIGHTED_JET_AND_PFC-T26] Outstanding-debt list and minimal core (Companion Secs. 10-11)

Owed by the local program (verbatim list, abridged labels): (1) full human-readable proofs of Theorems A and B ("the statements are here; the write-ups are not"); (2) general curvature-valuation formula for arbitrary diagonal monomial-unit germs; (3) complete codimension-two Newton-polygon theorem (cancellation classification); (4) coordinate-robustness theorem as formal statement + proof; (5) the "Definitions and Theorem Statements" spine document (Stage 10); (6) one synthetic non-KN example with full calculation.

Minimal self-contained core (six items): defs 1.1 and 1.2; Theorem A; Theorem B; intrinsic gauge `R d^2 = -m(m+5)/4`; master quadric with `C(2,-2,...) = -m(m+5)`.

---

## 3. CONVENTIONS

- **Coordinates.** x = collapsing coordinate; transverse coordinates (y,z) in S1 (m=2, channels labelled P and R), y_alpha (alpha=1..m) in S2/S3. State-space dimension = m+1; m = transverse fibre dimension. Kerr-Newman is m=2.
- **Component names.** S1: `E=g_xx, P=g_yy, Q=g_zz`. S2: `g_x, g_{y_alpha}`. S3 Lame engine: `H_i` with `g=sum H_i^2 (dx^i)^2` (so g_ii = H_i^2).
- **Valuation.** x-valuation v(.) of Laurent series; transverse differentiation preserves x-valuation, `\partial_x` lowers it by 1 (S1). `val_D(R)` = pole order of R along D (S3 1.3). "Order p" means pole x^{-p}.
- **Parity.** Parity-fixed = every metric component even in x (invariant under x -> -x); then R is even in x and all odd-order poles vanish identically (S2 Convention paragraph).
- **Sign conventions.** Scalar curvature R with warped-product formula `R = -2m w''/w - m(m-1)(w'/w)^2` over a flat m-fibre (S2 proof of T9); consequently parity-fixed leading coefficient is negative, `-m(m+5)/B` with `B>0`. Decomposition of 14 at m=2: `6m + m(m-1) = 12 + 2`.
- **Amplitude symbols (COLLIDING).** Collapsing amplitude: `A_2` (S1 generic; also KN table in S2), `A` (S2 prop:generic, S3 Theorem A), `B` (all reflection/parity-fixed statements). Transverse amplitudes: `A_alpha` (S2 thm:pure, S3) — the symbol A is thus used for both roles across sources.
- **Tuple orders (corner).** Lattice points are (x-exponent, y-exponent); polar vertices carry negated exponents, `V=(-p,-q)` polar iff a component positive. Weight form `g_i = h_i(s) x^{p_i} y^{q_i} u_i`, index i=0 spectator, i=1 the x-coordinate component, i=2 the y-coordinate component. Directions: `x = rho eps^{a_x}, y = eps^{a_y}`, order = support function `m(a) = max_v(-<a,v>)`. Face dictionary: `p_x=p_1+2, p_y=q_2+2, r_x=-p_2, r_y=-q_1`.
- **Master quadric index order.** In `C(p)`: p_0 = collapsing exponent (of g_xx), p_a (a>=1) = transverse exponents; sums over a and a<b are transverse-only. Key evaluation C(2,-2,...,-2) = -m(m+5) (m arguments of -2).
- **Intrinsic gauge.** d = proper distance to the face; on parity faces d = sqrt(B) x^2/2 implicitly (giving R d^2 = -m(m+5)/4); generic faces R ~ d^{-3/2}.
- **Boundary-change normalization.** Under `x = c(y) x' + k (x')^2` (c>0): B' = B c^4; parity preserved iff k=0.
- **Normalization of the vertex-rule coefficients (S2).** Vertex coefficients written as `A/(2h_1)` and `B/(2h_2)` with the quadrics A, B of T13; relative to S3's master quadric, A = 2*C(per-face arguments).

---

## 4. UNIQUE MATERIAL (exists only in these files; must not be lost)

From S1:
- U1. The 7-term dominant-part expression (T4) — the explicit "part of scalar curvature capable of reaching the lowest valuations" for diagonal metrics; nowhere in S2/S3.
- U2. The quantitative valuation bound on transverse-derivative terms: >= -2 (generic germ), >= -3 (reflection germ) (T4). This is the actual proof of the no-transverse-derivative claim T3.
- U3. Term-by-term generic identification (T5) and the reflection per-term ledger -6,-6,+2,+2,-2,-2,-2 over B (T6).
- U4. The no-transverse-derivative claim as an explicit theorem clause (T3) — S2/S3 state coefficient formulas with B(y), A_alpha(y) but never assert absence of transverse derivatives as such.
- U5. Variable-coefficient (functions of y,z) generality for BOTH germs at m=2, including named nondegeneracy `A_2 P_0 R_0 != 0`, `B C_1 C_2 != 0`, and the "two valuation steps later" independence statement for B_4, C_10, C_20.
- U6. Replay metadata: 6 exact assertions, 1.257 s, finite Laurent jet ring design (T7).
- U7. The scope boundary: role-rechart covariance explicitly NOT proved; off-diagonal pullback + curvature replay still needed (T8). Load-bearing for this campaign's rechart goal.

From S2:
- U8. Theorem 1 as an EXACT (all-orders) identity, with the warped-product proof, the substitution r = (1/2)sqrt(B)x^2, and the 6m / m(m-1) focusing-vs-shear decomposition (T9). S3 records only the statement.
- U9. General-m corollary with variable B(y), A_alpha(y) and O(x^{-2}) remainder (T10).
- U10. The parity mechanism paragraph (order read off germ parity) and prop:generic's independence claims (T11).
- U11. prop:corner with the residue-weight formalism (r_x, r_y), the support-function formula, and the three consequences including order-drop below both faces and the front-face coefficient notion (T12).
- U12. The corner vertex rule in full: the explicit quadric A, coefficient normalization A/(2h_1), the V_0 spectator polar criterion, the exact cancellation condition, and the vertex dictionary to prop:corner (T13). The A-quadric formula appears nowhere else (S3 only points to the master quadric).
- U13. KN weight data `g_S ~ x^{-6}, g_Q ~ x^2 y^{-2}, g_J ~ x^{-2} y^2` with V_0=(6,0), A=-84, B=-12, m(a)=max(4a-2,4-2a) (T13/T14).
- U14. The extremal-face leading coefficient `A_2^{-1} \partial_S log(G_J G_Q)|_ext` (T14) — not in S3's table.
- U15. Explicit open problems: codim >= 3 polytope, front-face coefficient classification (T13); certificate-to-theorem mapping incl. "run twice with identical output" and lead7_test6-10 (T15).

From S3:
- U16. Frozen definitions 1.1-1.4, in particular the divisor-monomial germ class and val_D (T16).
- U17. Lemma E2 intrinsic gauge — both the pure number -m(m+5)/4 and the generic limit `(sum P_a1/P_a0) A^{-1/4}/2^{3/2}` (T19). Only coordinate-free formulation anywhere.
- U18. The master quadric C(p), its three jobs, C(2,-2,...,-2) = -m(m+5), and the vanishing-locus inventory including the exactly-scalar-flat isotropic exponents p_a = 4/(m+1) (T20).
- U19. Boundary robustness: B' = B c^4, form-invariance of -m(m+5)/B', odd coefficient vanishes iff k=0 (T21). The only recorded coordinate-robustness result (S1 explicitly does not prove covariance).
- U20. The sector-weight alternative -28 = 2*(-14) vs balanced (A,B)=(-84,-12), with the B1 crown experiment as the decider (T22).
- U21. The entire dual-constant block: I_primary closed form with Pi(n;k^2), K(k^2), k^2=(2-sqrt2)/4, n=(4-3sqrt2)/8, both 20-digit numerical pins, residue exactly 4, jumps +-4 pi i, and the "unsupported" status flag (T25).
- U22. The debt list (six missing items) and the six-item minimal core (T26) — a ready-made completeness checklist for the consolidation.
- U23. Lame formula with beta_ij convention and its verification status n=3 general / n=4 pending (T24).

---

## 5. RED FLAGS

- **RF1 (ambiguous formula in a Theorem).** T13 defines only the quadric A and says "B the same in the q's". Literal substitution q_i -> p_i in A gives, for the KN data (q_0,q_1,q_2)=(0,-2,2), B = -4, NOT the stated B = -12. The stated -12 is reproduced only by ALSO swapping the roles of indices 1 and 2 (i.e. `B = -q_0^2 - q_0 q_1 + q_0 q_2 + 2q_0 + q_1 q_2 - q_1^2 + 2q_1`), which is the natural face-symmetric reading but is never written down. Consolidation must fix the explicit B-formula (check against `pfc_test3_vertex_rule.py`).
- **RF2 (proposition proved only by examples).** prop:corner (T12) is stated as a Proposition, but the only support cited is verification "for synthetic (4,4) and (4,3) corners" (pfc_test2). S3 Sec. 10 item 3 concedes the "complete codimension-two Newton-polygon theorem (cancellation classification)" is still owed. Status should be downgraded to verified-conjecture / restricted theorem.
- **RF3 (machine certificate presented as proof; human proofs missing).** thm:vertex (T13) says "proved by an exact scalar-curvature computation with symbolic weights"; cor:asymp and prop:generic likewise rest on pfc_test1. S3 Sec. 10 item 1 states outright that human-readable proofs of Theorems A and B do not exist. Only T9 (thm:pure, warped-product argument) and S1's T1-T6 (weighted-valuation argument) have written mathematical proofs.
- **RF4 (remainder-order mismatch).** Reflection/parity-fixed remainder: S1 claims O(x^{-3}); S2 cor:asymp and S3 Theorem B claim O(x^{-2}). S1's germ is even in x, so by S2's parity convention the x^{-3} term vanishes and O(x^{-2}) should hold — S1 is not wrong, just strictly weaker. Consolidated statement should carry O(x^{-2}) with the parity hypothesis made explicit.
- **RF5 (notation collisions / undefined symbols).** (a) `A` = collapsing amplitude (S2 prop:generic, S3 Thm A) vs `A_alpha` = transverse amplitudes (S2 thm:pure, S3 Thm B) vs `A_2, A_3` = collapsing Taylor coefficients (S1; also S2's KN table uses A_2^{-1} while its own proposition used A). (b) prop:generic asserts independence "of A_3" but its hypothesis `g_x = Ax^2 + O(x^3)` never defines A_3. (c) S3 Theorem A omits the nondegeneracy hypotheses `A, P_{alpha 0} != 0` present in S2/S1.
- **RF6 (unresolved empirical fork).** S3 Sec. 6: balanced vertex-coefficient assignment (A=-84, B=-12) vs sector-weight alternative (-28 = 2*(-14)); "The B1 crown experiment decides which weighting is realised." An absorption table must not record either weighting as settled.
- **RF7 (undocumented factor-2 discrepancy).** S3 claims the master quadric C(p) yields "both corner vertex coefficients (evaluate per face)", but per-face evaluation gives C = -42 for the KN x-face while S2's vertex quadric gives A = -84 = 2C (coefficient A/(2h_1) = C/h_1). Consistent, but the conversion factor is stated nowhere.
- **RF8 (partially verified engine).** Lame formula (T24) verified fully general only for n=3; "n=4 polynomial fixtures exist but need lightening before re-run." Any n>=4 use of E1 is currently uncertified.
- **RF9 (covariance gap).** S1 explicitly does not prove role-rechart covariance (T8), and S3 Sec. 10 item 4 lists the coordinate-robustness theorem as unwritten; the only robustness available is the restricted boundary-change result T21 (computer-verified claims, no formal proof). The campaign must not cite pole order/coefficient chart-invariance beyond T19/T21's scope.
- **RF10 (table label divergence, minor).** S2's KN table names divisors Omega=0 / Phi_e=0 and the corner Omega=Phi_e=0 (Schwarzschild); S3's table writes "Omega=0 or J=0", "Phi_e=0 or Q=0", corner J=Q=0. Same content assuming the divisor identifications, but the identification is asserted, not derived, in these files.
- **RF11 (external-path drift, minor).** S2 cites `verification/pfc_test1..3.py` relative paths; in this repo the scripts live under `research/verification/`, `04_VERIFICATION_LEGACY/local_curvature/`, and `Papers_Library/07_certificates.../`. Scripts exist (checked 2026-07-30), but citations need repointing at consolidation. S3's host document `Local_Curvature_Calculus_for_Inverse-Channel_Metrics.txt` also exists in-repo (4 copies).

*End of extraction note.*
