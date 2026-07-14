# CCE-6 whole-surface topology investigation

## Result

The native swept transfer is **not surjective** onto the whole surface
relative-homology group.  This is a rank obstruction, not a missing proof
budget:

\[
\operatorname{rank}H_2(X,Y;\mathbb Z)=12,
\qquad
\operatorname{rank}\operatorname{im}L_{\mathbb Z}\leq4.
\]

Consequently the completed CCE-6 native-image theorem cannot be promoted to
a whole-surface equivalence.  The remaining meaningful expansion is narrower:
determine the saturation of the rank-four native sublattice, or construct an
integral functional on the rank-twelve group that detects the lifted
meridian.  That question controls whether the CPV half-meridian remains
nonintegral in the whole group.

This result does not repeat the completed clearance theorem.  It investigates
the strictly larger whole-surface claim that the package deliberately left
open.

## 1. Projective norm cover

Homogenizing the Stage-2 norm cover in
\([x:y:z:t:w]\in\mathbb P^4\) gives the complete intersection

\[
 S=\left\{
 \begin{aligned}
 ax^2-by^2+z^2-3t^2&=0,\\
 w^2-4(a^2x^2+b^2y^2+z^2)&=0.
 \end{aligned}
 \right.
\]

For the two DBP Galois values, with
\(\varepsilon=+1\) on the primary sheet and \(\varepsilon=-1\) on the
dual sheet,

\[
 a=\frac{1+\varepsilon\sqrt2}{2},
 \qquad
 b=\frac{-1+\varepsilon\sqrt2}{2},
 \qquad a-b=1.
\]

The five diagonal degeneration parameters of the pencil are

\[
 -4a,\quad 4b,\quad -4,\quad 0,\quad\infty.
\]

They are pairwise distinct on both sheets.  The standard gradient criterion
for a diagonal intersection of two quadrics therefore shows that \(S\) is
smooth.  The hyperplane sections

\[
 D_q=S\cap\{w=0\},\qquad D_\infty=S\cap\{t=0\}
\]

are smooth genus-one curves: their four pencil parameters are respectively
\((-4a,4b,-4,0)\) and \((-4a,4b,-4,\infty)\), again pairwise distinct.
Their intersection is transverse and has

\[
 D_q\cdot D_\infty=H^2=\deg S=4
\]

points.  Put

\[
 X=S\setminus D_q,
 \qquad
 Y=D_\infty\setminus(D_q\cap D_\infty).
\]

This is exactly the pair used by the CCE-6 surface lift.

## 2. Homology of the complement

Adjunction gives \(K_S=-H\).  A smooth \((2,2)\) complete-intersection
surface has

\[
 c_2(TS)=2H^2,
 \qquad \int_Sc_2=8.
\]

Lefschetz gives \(H_1(S;\mathbb Z)=0\), hence \(b_2(S)=6\).  The
hyperplane class is primitive (equivalently, the degree-four del Pezzo
surface contains a line, on which \(H\) has degree one).

The integral Gysin sequence for the complement of the smooth elliptic
divisor \(D_q\) now has the relevant part

\[
 0\longrightarrow
 \mathbb Z[D_q]\longrightarrow H^2(S;\mathbb Z)
 \longrightarrow H^2(X;\mathbb Z)
 \longrightarrow H^1(D_q;\mathbb Z)\longrightarrow0.
\]

The first map is primitive and the groups on either side are free.  Thus

\[
 H_1(X;\mathbb Z)=0,
 \qquad
 H_2(X;\mathbb Z)\cong\mathbb Z^7.
\]

Meanwhile \(Y\) is a genus-one curve with four punctures, so

\[
 H_1(Y;\mathbb Z)\cong\mathbb Z^{2(1)+4-1}=\mathbb Z^5,
 \qquad H_2(Y;\mathbb Z)=0.
\]

The long exact sequence of \((X,Y)\) reduces to

\[
 0\longrightarrow\mathbb Z^7
 \longrightarrow H_2(X,Y;\mathbb Z)
 \longrightarrow\mathbb Z^5\longrightarrow0.
\]

It splits as an extension of free abelian groups, proving

\[
 \boxed{H_2(X,Y;\mathbb Z)\cong\mathbb Z^{12}.}
\]

## 3. Native rank and the killed expansion

The source curve \(C^\circ\) is elliptic with two punctures, hence
\(H_1(C^\circ;\mathbb Z)\cong\mathbb Z^3\).  Adding the two relative
endpoints contributes the primitive boundary generator \(\beta\), giving

\[
 H_1(C^\circ,\{Q_0,Q_m\};\mathbb Z)\cong\mathbb Z^4.
\]

The theorem-bound basis is \((A,B,\mu,\delta)\).  The CCE-6 identity
\(R_{\mathbb Z}L_{\mathbb Z}=4\operatorname{id}\) makes
\(L_{\mathbb Z}\) injective on its admissible source.  Therefore its image
has rank at most four, whereas the target has rank twelve.  In particular,

\[
 \boxed{\operatorname{im}L_{\mathbb Z}\neq H_2(X,Y;\mathbb Z).}
\]

There are at least eight independent whole-surface directions outside the
native swept carrier.

## 4. What remains genuinely open

The rank calculation decides surjectivity but not saturation.  A rank-four
subgroup of \(\mathbb Z^{12}\) can be primitive or nonprimitive.  The
existing equation \(R_{\mathbb Z}L_{\mathbb Z}=4I\), defined only on the
native transfer subcomplex, does not determine the Smith factors of the
embedding into the whole group.

The smallest useful next calculation is therefore one of the following
equivalent pieces of data:

1. an integral intersection matrix for the four native generators against
   a basis of dual relative cycles in \(H_2(X,Y;\mathbb Z)\);
2. the Smith normal form of the inclusion
   \(\operatorname{im}L_{\mathbb Z}\hookrightarrow H_2(X,Y;\mathbb Z)\);
3. an integral extension of the signed reduction, or a local-product
   functional, whose value on \(L_{\mathbb Z}(\mu)\) proves or disproves
   divisibility by two in the whole lattice.

Until that calculation is supplied, whole-lattice CPV non-descent remains
open.  Whole-surface surjectivity does not: it is false.

## 5. Machine audit

`verify_cce6_whole_surface_topology.py` checks the two exact quadratic-field
pencils and replays every rank in the argument.  The topology proof above,
not the script alone, is the proof-bearing artifact.
