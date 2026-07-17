# Wall-Isotropy Comparison Theorem (CMP-0040 session derivation, 2026-07-16)

**Status:** proved (session derivation + external referee pass). Supersedes the
"three-arm natural isomorphism at C_2" claim (CMP-0040-C2), which is REFUTED as
stated by the stabilizer argument in section 5 below.

## 1. Refutation of the Lorentzian gauge-selection branch

The effective gauge group preserving the channel sum is V = ker(Sigma: Q^3 -> Q),
acting by translation kappa -> kappa + a. V is divisible: every a in V is 2b for
b = a/2 in V. Hence any homomorphism phi: V -> C_2 satisfies
phi(a) = phi(2b) = 2 phi(b) = 0, so phi is trivial. The gauge action admits NO
nontrivial map to C_2 and cannot produce a two-sheeted quotient or parity.
The proposed "Lorentzian sheet-selection" mechanism is refuted. The Lorentzian
form nu^T (2I - J) nu (signature (2,1)) stratifies gauge directions into
null/transverse (channel allocation) and is orthogonal to sheet selection.

## 2. Founding ordered-root cover: fixed-point wall, canonical section

f_b(S) = S^2 - T(b) S + N(b), Delta = T^2 - 4N. Ordered-root cover
X = {(b,S) : f_b(S)=0}, deck tau(b,S) = (b, T(b) - S).
Fix(tau): T - S = S iff S = T/2, and f_b(T/2) = -Delta/4, so
Fix(tau) = {Delta = 0, S = T/2}. At the wall the geometric fibre is ONE fixed
point (the double root); scheme-theoretically ramified/nonreduced, not a free
orbit. On the real chamber Delta >= 0, s_+(b) = (b, (T + sqrt(Delta))/2) is a
continuous canonical section (larger root), extending uniquely to T/2 at the
wall. Canonicity is a real-chamber statement; complexified root ordering
disappears and monodromy survives.

## 3. AC fold: identical fixed-point geometry

F(v) = v^2 - T_AC v + N_AC with T_AC = E^2 - 2QX, N_AC = X^2(P^2+Q^2),
Delta_AC = E^4 - 4E^2QX - 4P^2X^2. Section 2 applies verbatim: fixed locus
Delta_AC = 0, high-voltage root extends to the double root. Founding and AC
walls are the same fixed-point type.

## 4. Precision flow: two distinct C_2-objects

(a) Account/state cover t -> a = t^2, tau(t) = -t: ordinary ramified quadratic,
single fixed point t = 0 at the wall (FIXED-POINT type). Rounding is constant
on the pair {+sqrt(a), -sqrt(a)} and is an output map of different type, not a
section of the state cover.
(b) Candidate-output bundle at a midpoint mu: F_mu = {mu-h, mu+h}. Reflection
fixes mu but swaps the candidates; an equivariant selector s would need
s(mu) = tau s(mu) with no tau-fixed element in F_mu. Contradiction. The
free-orbit obstruction (P4) lives in the OUTPUT BUNDLE only.

## 5. One convention bit is necessary and sufficient

For a free two-point fibre F, an orientation o: F ~ C_2 defines the selection
s(F,o) = o^{-1}(0). Exactly two orientations exist: the augmentation is exactly
one bit. Necessity: the section 4(b) no-selector proof. Sufficiency: the
displayed construction. Round-half-even supplies the bit via significand parity.

## 6. Non-identifiability (stabilizer obstruction)

For a C_2-space, equivariant isomorphisms preserve Stab(x): gx = x iff
g f(x) = f(x). Founding/AC wall points have Stab = C_2; precision output-tie
points have Stab = {1}. Therefore NO wall-preserving C_2-equivariant
isomorphism identifies the three arms. Same for action groupoids (equivalences
preserve automorphism groups). Away from walls all fibres are free transitive
C_2-sets, so fibrewise comparison is possible; global comparison requires
explicit base maps and functors and cannot cross the wall strata.

## 7. Double rounding: exact naturality counterexample

Coarse grid 2hZ, fine grid hZ, both nearest-even. x = h + eps, 0 < eps < h/2:
R_f(x) = h; h is a coarse midpoint, nearest-even gives R_c(h) = 0; but
R_c(x) = 2h. So R_c o R_f != R_c. Localization: if R_f(x) is not a coarse
midpoint then R_c(R_f(x)) = R_c(x) (else x and R_f(x) straddle a coarse
midpoint that is itself a fine-grid point closer to x, contradicting fine
rounding). Failure supported exactly on preimages of coarse tie walls.
Strict selection-preservation holds off that locus; strict naturality fails on
it. "Lax naturality" is UNDEFINED pending an explicit defect-enriched
2-category with comparison 2-cells.

## Verdict

1. Lorentzian gauge-selection branch: REFUTED (divisibility).
2. Founding and AC: fixed-point walls, canonical real sections.
3. Precision free-orbit obstruction: output bundle only.
4. One convention bit necessary and sufficient there.
5. Global wall-preserving C_2-isomorphism of the three arms: IMPOSSIBLE.
6. Refinement strictly compatible off the double-rounding locus, incompatible on it.
7. Any lax three-arm coherence requires a defined defect-enriched category.

Corrected result: a rigorous WALL-ISOTROPY COMPARISON THEOREM. The global
three-arm natural-isomorphism claim (CMP-0040-C2) is refuted as stated and
forks into: C2a chamber coherence (open, constructible) and C2b wall-isotropy
classification (proved herein).
