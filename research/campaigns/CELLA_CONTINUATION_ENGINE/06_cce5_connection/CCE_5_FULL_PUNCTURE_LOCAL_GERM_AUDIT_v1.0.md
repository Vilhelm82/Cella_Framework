# CCE-5 full-puncture local-germ audit

## Outcome

`PROMOTED`: exact local connection germs at all four punctures.

`ACTIVE_PROOF`: integral geometric generator calibration at (0,1/2,1,infty),
global relations with the released corridor subgroupoid, and exact geometric
clearance representatives.

This audit does not relabel a matrix residue as geometric monodromy.

## Exact germs

For (Y' = M(m)Y) in the certified basis
((K,E,\Pi(m^2/(2m-1);m))), the finite logarithmic residues are

\[
R_0=
\begin{pmatrix}
-\tfrac12&\tfrac12&0\\
-\tfrac12&\tfrac12&0\\
-1&-\tfrac12&\tfrac12
\end{pmatrix},
\qquad
R_{1/2}=
\begin{pmatrix}
0&0&0\\0&0&0\\0&0&\tfrac12
\end{pmatrix}.
\]

In the exact infinity chart (z=1/m), the residue of
(-M(1/z)/z^2) is

\[
R_\infty=
\begin{pmatrix}
\tfrac12&0&0\\
\tfrac12&-\tfrac12&0\\
0&0&\tfrac12
\end{pmatrix}.
\]

At (m=1+x), the current basis is not logarithmic.  Its principal part is

\[
M(1+x)=\frac{N_{-2}}{x^2}+\frac{N_{-1}}x+O(1),
\]

with

\[
N_{-2}=\begin{pmatrix}0&0&0\\0&0&0\\0&\tfrac32&0\end{pmatrix},
\qquad
N_{-1}=\begin{pmatrix}0&-\tfrac12&0\\0&0&0\\1&\tfrac12&-\tfrac32\end{pmatrix}.
\]

This explicitly confirms the handoff warning: naive exponentiation of a
residue at (m=1) is invalid in the present basis.  The first missing exact
object is a source-compatible rational/meromorphic gauge (G(x)) reducing
this nilpotent double-pole germ to a proved Levelt--Turrittin or logarithmic
normal form while retaining the integral marking.  Only after that gauge is
constructed can its local analytic action be matched to a geometric loop.

## Why the full groupoid is not promoted yet

The existing `U,L,u,l` matrices are geometric because their exact lifted
corridors, orientations, sheet crossings, and clearance witnesses are bound.
The four germs above are analytic local data.  They do not supply:

- based geometric loops with exact clearance from every other puncture;
- a marking comparison between local Levelt bases and `(A,B,mu,delta)`;
- integral rather than merely complex analytic monodromy matrices; or
- global fundamental-group relations in the calibrated relative basis.

The restriction is therefore mathematical, not an old API fence.  Public
route-word composition remains `PROMOTED` on the calibrated corridor
subgroupoid; the full regular-plane geometric groupoid remains
`ACTIVE_PROOF` at the explicit (m=1) gauge-and-marking object above.
