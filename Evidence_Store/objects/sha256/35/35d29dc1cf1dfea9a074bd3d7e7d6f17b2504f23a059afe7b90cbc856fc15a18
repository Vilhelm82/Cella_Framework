# LEAD-7 variable-transverse weighted-jet theorem

## Statement

Let (x) be the collapsing coordinate and let all displayed coefficients be
arbitrary sufficiently differentiable functions of transverse coordinates
((y,z)).

For the generic diagonal germ

\[
g=\operatorname{diag}
\left(A_2x^2+A_3x^3+O(x^4),
P_0+P_1x+O(x^2),
R_0+R_1x+O(x^2)\right),
\]

with (A_2P_0R_0\ne0), the scalar curvature satisfies

\[
R[g]=
\frac{P_1/P_0+R_1/R_0}{A_2}\,x^{-3}+O(x^{-2}).
\]

For the reflection germ

\[
g=\operatorname{diag}
\left(Bx^2+B_4x^4+O(x^6),
C_1x^{-2}+C_{10}+O(x^2),
C_2x^{-2}+C_{20}+O(x^2)\right),
\]

with (BC_1C_2\ne0),

\[
R[g]=-\frac{14}{B}\,x^{-4}+O(x^{-3}).
\]

Neither leading coefficient contains a (y)- or (z)-derivative of any
coefficient function.

## Weighted-valuation proof

Write (E=g_{xx}), (P=g_{yy}), and (Q=g_{zz}).  Transverse
differentiation preserves (x)-valuation, while differentiation by (x)
lowers it by one.  For a diagonal metric, the part of scalar curvature capable
of reaching the lowest valuations is

\[
-\frac{P_{xx}}{EP}-\frac{Q_{xx}}{EQ}
+\frac{P_x^2}{2EP^2}+\frac{Q_x^2}{2EQ^2}
-\frac{P_xQ_x}{2EPQ}
+\frac{E_xP_x}{2E^2P}+\frac{E_xQ_x}{2E^2Q}.
\]

All omitted terms contain a transverse derivative.  Direct valuation of the
diagonal Christoffel formula shows those terms have valuation at least
(-2) in the generic germ and at least (-3) in the reflection germ.  They
therefore cannot contribute to (x^{-3}) or (x^{-4}), respectively.

For the generic valuations ((v(E),v(P),v(Q))=(2,0,0)), only the last two
terms reach valuation (-3):

\[
\frac{E_xP_x}{2E^2P}\sim\frac{P_1}{A_2P_0}x^{-3},
\qquad
\frac{E_xQ_x}{2E^2Q}\sim\frac{R_1}{A_2R_0}x^{-3}.
\]

For the reflection valuations ((2,-2,-2)), the seven displayed terms
contribute, in order,

\[
-\frac6B,-\frac6B,
+\frac2B,+\frac2B,
-\frac2B,-\frac2B,-\frac2B,
\]

to the (x^{-4}) coefficient.  Their sum is (-14/B).  The corrections
(B_4,C_{10},C_{20}) begin two valuation steps later and cannot change this
coefficient.

## Exact replay

`verify_lead7_variable_transverse_weighted_jet.py` implements a finite Laurent
jet ring.  It retains arbitrary SymPy functions of (y,z), performs truncated
Christoffel and Ricci assembly, and extracts only the relevant coefficients.
It passed six exact assertions in 1.257 seconds:

- both displayed leading coefficients;
- absence of transverse derivative atoms in both coefficients; and
- absence of any more singular scalar-curvature terms in both germs.

## Scope boundary

This closes the arbitrary-transverse-coefficient extension of the diagonal
LEAD-7 local-germ laws.  It does not prove full role-rechart covariance, which
still requires the off-diagonal tensor pullback and curvature replay.
