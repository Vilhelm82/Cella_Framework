# DBP Galois-Dual Surface-Cycle Route

## Stage 3: integral Picard--Lefschetz transport modulo compact periods, v0.1

**Date:** 2026-07-14  
**Depends on:** `DBP_DUAL_SURFACE_CYCLE_STAGE1_v0.1.md`,
`DBP_DUAL_SURFACE_CYCLE_STAGE2_v0.1.md`  
**Status:** the two branch-loop transports are identified modulo ordinary
compact elliptic periods; an integral-class replacement for the coefficient
\(i\) is ruled out

---

## 0. Result

Let \(\sigma\) denote the shear parameter and put

\[
r=\sqrt{1+\sigma^2},\qquad
c=\frac{r-1}{r+1},\qquad
m=\frac{c}{1+c}=\frac12-\frac1{2r},
\qquad
n=-\frac{m^2}{1-2m}.
\tag{0.1}
\]

At the primary keystone \((\sigma,r)=(1,\sqrt2)\), these are
\((c_+,m_+,n_+)\). Analytic continuation once around either branch point
\(\sigma=\pm i\) changes \(r\) to \(-r\), and hence

\[
(c,m,n)\longmapsto(c^{-1},1-m,1-n)
=(c_-,m_-,n_-).
\tag{0.2}
\]

Fix the standard based path from \(\sigma=1\) to a small circle about
\(+i\) through the upper half-plane, wind once, and return on the same stem.
Let \(T_{+i}\) be its Gauss--Manin/Picard--Lefschetz transport. Define
\(T_{-i}\) analogously using the lower half-plane and \(-i\). Then, modulo
ordinary compact elliptic periods,

\[
\boxed{
T_{+i}[\delta_+]=[\delta_-^\uparrow],
\qquad
T_{-i}[\delta_+]=[\delta_-^\downarrow].
}
\tag{0.3}
\]

Let \(\mathfrak C_+\) denote the primary integral curvature class whose end
pushforward is \(\delta_+\). The Stage-2 fiber lift gives the corresponding
surface statement

\[
\boxed{
T_{+i}[\mathfrak C_+]=[\mathfrak C_-^\uparrow],
\qquad
T_{-i}[\mathfrak C_+]=[\mathfrak C_-^\downarrow]
\pmod{\text{compact-period surface classes}}.
}
\tag{0.4}
\]

Thus there is no single loop-independent integral CPV transport. There are
two canonical integral lateral transports once the branch route is fixed.
If \(\mu_-\) is the positively oriented primitive meridian of the dual pole,
then

\[
[\delta_-^\uparrow]-[\delta_-^\downarrow]=-[\mu_-],
\qquad
[\delta_-^{\rm CPV}]
=[\delta_-^\uparrow]+\frac12[\mu_-].
\tag{0.5}
\]

Consequently the CPV midpoint is rational, not integral, in the punctured
relative lattice.

Most importantly, the coefficient \(i\) cannot be absorbed into an integral
Picard--Lefschetz class by adding compact cycles. If \(\beta\) is the
primitive endpoint boundary of either lateral chain, then

\[
\partial(i\delta_-^\uparrow)=i\beta.
\tag{0.6}
\]

An integral relative class has an integral boundary, whereas compact period
cycles have boundary zero. Since \(i\beta\) is not in the integral boundary
lattice, no integral class is congruent to \(i\delta_-^\uparrow\), or to
\(i\delta_-^{\rm CPV}\), modulo compact periods. The same obstruction holds
after the surface lift. Therefore

\[
\boxed{
\text{the canonical integral transport is lateral, and it does not replace
the coefficient }i.
}
\tag{0.7}
\]

The phase \(i\) remains a normalization of the analytically continued
differential (or, equivalently, a complex coefficient on the cycle), not an
integral Picard--Lefschetz multiplicity.

---

## 1. The branch loop and the Galois involution

For the diagonal shear family, the two coefficients are

\[
a=\frac{1+r}{2},\qquad b=\frac{r-1}{2},
\qquad r^2=1+\sigma^2.
\tag{1.1}
\]

The metric-quotient parameter used in Stages 1 and 2 is

\[
c=\frac ba=\frac{r-1}{r+1},
\tag{1.2}
\]

and its Legendre parameter is

\[
m=\frac{c}{1+c}=\frac{r-1}{2r}.
\tag{1.3}
\]

The only branch points of \(r\) are \(\sigma=\pm i\). An odd winding about
either one sends \(r\mapsto-r\). Direct substitution gives

\[
c(-r)=\frac1{c(r)},
\qquad
m(-r)=1-m(r),
\tag{1.4}
\]

and, using \(n=-m^2/(1-2m)\),

\[
n(-r)=1-n(r).
\tag{1.5}
\]

At \(\sigma=1\), the two sheets therefore give

\[
m(\sqrt2)=\frac{2-\sqrt2}{4}=m_+,
\qquad
m(-\sqrt2)=\frac{2+\sqrt2}{4}=m_-.
\tag{1.6}
\]

This proves that the branch-loop continuation is exactly the DBP Galois
involution, rather than a merely numerical path between the two parameters.

---

## 2. Tracking the pole fixes the lateral class

Use the relative Legendre coordinate

\[
u=\frac{x}{m}.
\tag{2.1}
\]

The primary path is \(0\leq u\leq1\). The upper-sheet pole has

\[
u_p=\frac{x_p}{m}=\frac1n
=\frac{2m-1}{m^2},
\qquad
x_p=\frac mn=2-\frac1m.
\tag{2.2}
\]

On the return stem from \(+i\), \(\sigma\) lies in the first quadrant. The
principal value of \(r\) then has positive imaginary part, while the
continued sheet has \(r=-r_{\rm principal}\). Hence

\[
\operatorname{Im}m
=\operatorname{Im}\left(\frac12-\frac1{2r}\right)<0.
\tag{2.3}
\]

Near the endpoint \(m=m_-\),

\[
\frac{du_p}{dm}=\frac{2(1-m)}{m^3}>0,
\qquad
\frac{dx_p}{dm}=\frac1{m^2}>0.
\tag{2.4}
\]

Thus the pole approaches the real interval from below. The transported
interval lies above it and limits to the upper indentation
\(\delta_-^\uparrow\). The lower-half-plane return from \(-i\) is the
complex-conjugate sign calculation: \(\operatorname{Im}m>0\), the pole
approaches from above, and the path limits to
\(\delta_-^\downarrow\).

Away from the pole, changing the detailed branch loop changes a relative
transport only by the usual Picard--Lefschetz term

\[
\gamma\longmapsto
\gamma+\langle\gamma,\nu\rangle\nu,
\tag{2.5}
\]

where \(\nu\) is a closed vanishing cycle. Such a term is an ordinary compact
elliptic period. The pole-side calculation is therefore precisely the datum
that survives modulo compact periods and proves (0.3).

---

## 3. The integral relative lattice and the meridian

Let

\[
E_-^\circ
=C_{m_-}\setminus\{P_-^+,P_-^-\},
\qquad
\mathcal H_-
=H_1(E_-^\circ,\{Q_0,Q_m\};\mathbb Z),
\tag{3.1}
\]

where \(Q_0,Q_m\) are the path endpoints and \(P_-^+\) is the pole met by
the upper-sheet path. Let \(\Lambda_-^{\rm ell}\) be the subgroup generated
by the ordinary \(A\)- and \(B\)-cycles. The pole meridian \(\mu_-\) is a
closed compact loop in the punctured curve, but it is not an ordinary
elliptic period: it is killed when the puncture is filled and is detected by
the residue.

With \(\mu_-\) positively oriented, Stage 1 gives

\[
\operatorname{Res}_{P_-^+}\omega_-=4,
\qquad
\int_{\mu_-}\omega_-=8\pi i.
\tag{3.2}
\]

The local difference of the two indentations is clockwise, hence

\[
\delta_-^\uparrow-\delta_-^\downarrow=-\mu_-.
\tag{3.3}
\]

This is also forced by

\[
\int_{\delta_-^\uparrow-\delta_-^\downarrow}\omega_-
=-8\pi i.
\tag{3.4}
\]

Since a meridian about a single puncture is primitive,

\[
\delta_-^{\rm CPV}
=\frac12(\delta_-^\uparrow+\delta_-^\downarrow)
=\delta_-^\uparrow+\frac12\mu_-
\tag{3.5}
\]

does not lie in \(\mathcal H_-\). It lies in
\(\mathcal H_-\otimes\mathbb Q\).

More explicitly, the relative exact sequence contains

\[
0\longrightarrow H_1(E_-^\circ;\mathbb Z)
\longrightarrow\mathcal H_-
\mathop{\longrightarrow}^{\partial}\mathbb Z\beta
\longrightarrow0.
\tag{3.6}
\]

The quotient is free, so the absolute subgroup is primitive in
\(\mathcal H_-\). Therefore the primitive meridian \(\mu_-\) cannot become
twice another relative integral class; the half-meridian in (3.5) is a
genuine denominator.

There are therefore two useful quotient conventions:

1. modulo \(\Lambda_-^{\rm ell}\), the two branch transports remain distinct
   and differ by the residue meridian;
2. modulo every closed cycle in \(E_-^\circ\), including \(\mu_-\), both
   transports reduce to the same primitive open-chain generator determined
   by the endpoint boundary.

The first convention is the one meant by "modulo compact periods" in the
earlier DBP reports, where ordinary elliptic periods and residue jumps were
kept separate.

---

## 4. Surface lift of the transport class

Stage 2 constructs a linear fiber-lift map on admissible chains,

\[
\delta\longmapsto\mathfrak C(\delta),
\qquad
\int_{\mathfrak C(\delta)}\mathcal K
=\int_\delta\Omega.
\tag{4.1}
\]

It commutes with continuation as long as the base path avoids the norm
discriminant, which the two lateral paths do. Applying it to (0.3) gives
(0.4). If

\[
\mathfrak M_-=\mathfrak C(\mu_-),
\tag{4.2}
\]

then

\[
\mathfrak C_-^\uparrow-
\mathfrak C_-^\downarrow=-\mathfrak M_-,
\tag{4.3}
\]

and

\[
\int_{\mathfrak M_-}\mathcal K=8\pi,
\qquad
\mathfrak C_-^{\rm CPV}
=\mathfrak C_-^\uparrow+\frac12\mathfrak M_-.
\tag{4.4}
\]

The surface meridian is primitive because its boundary pushforward is the
primitive base meridian. Hence the geometric CPV surface midpoint is likewise
rational rather than integral.

For the literal geometric curvature form, the two integral transports have
periods

\[
\boxed{
\int_{T_{+i}\mathfrak C_+}\mathcal K
\equiv-iI_{\rm dual,CPV}-4\pi,
\qquad
\int_{T_{-i}\mathfrak C_+}\mathcal K
\equiv-iI_{\rm dual,CPV}+4\pi
\pmod{\Lambda_{\mathcal K}^{\rm ell}}.
}
\tag{4.5}
\]

Here \(\Lambda_{\mathcal K}^{\rm ell}\) is the ordinary compact-period
module obtained by lifting the elliptic \(A\)- and \(B\)-cycles. Equation
(4.5) is the requested canonical transport class modulo compact periods.

---

## 5. Why no integral class can absorb \(i\)

The obstruction is integral and precedes any period evaluation. The endpoint
boundary map is

\[
\partial:\mathcal H_-
\longrightarrow
\widetilde H_0(\{Q_0,Q_m\};\mathbb Z),
\tag{5.1}
\]

and either lateral class has

\[
\partial\delta_-^\uparrow
=\partial\delta_-^\downarrow
=\beta:=[Q_m]-[Q_0].
\tag{5.2}
\]

The vector \(\beta\) is primitive and nonzero. Every ordinary compact period
and every pole meridian has boundary zero.

Assume that an integral relative class \(z\in\mathcal H_-\) could replace the
coefficient \(i\) modulo compact cycles. After complexification this would
mean

\[
z-i\delta_-^\uparrow\in
H_1(E_-^\circ;\mathbb C).
\tag{5.3}
\]

Applying \(\partial\) gives

\[
\partial z=i\beta.
\tag{5.4}
\]

But \(\partial z\) belongs to the integral lattice
\(\mathbb Z\beta\), while \(i\beta\notin\mathbb Z\beta\). This is a
contradiction. Replacing the lateral chain by its CPV midpoint changes no
endpoint boundary, so the same contradiction applies to
\(i\delta_-^{\rm CPV}\).

Any integral surface replacement would push forward at the ends to an
integral boundary replacement and would therefore contradict (5.4). Thus
neither Picard--Lefschetz monodromy nor addition of compact surface periods
can implement the scalar \(i\).

This is a statement about the integral transport **class**. It does not claim
a transcendence theorem excluding every accidental numerical equality
between one special third-kind period and a combination of other periods.
Such a numerical coincidence, even if it existed, would not be an integral
homological replacement for \(i\).

---

## 6. Interpretation of the phase

Stage 1 proved the exact endpoint identity

\[
\Phi_-^*\omega_-=i\Omega_-.
\tag{6.1}
\]

Stage 3 shows that this \(i\) cannot be moved into the integral transport
lattice. The two legitimate formulations of the real-normalized dual period
remain

\[
I_{\rm dual,CPV}
=\int_{\mathfrak C_-^{\rm CPV}}i\mathcal K
=\int_{i\mathfrak C_-^{\rm CPV}}\mathcal K.
\tag{6.2}
\]

The first uses a Galois-normalized differential; the second uses a
complex-coefficient cycle. Neither is an integral Picard--Lefschetz cycle.
The actual integral continuations are the two lateral cycles in (0.4), with
the unnormalized periods (4.5).

---

## 7. Completion ledger

```text
CLOSED       shear branch loop r -> -r realizes (c,m,n) -> (1/c,1-m,1-n)
CLOSED       upper branch route -> upper lateral integral class mod A/B periods
CLOSED       lower branch route -> lower lateral integral class mod A/B periods
CLOSED       lateral difference is the primitive residue meridian
CLOSED       CPV midpoint is rational, not integral
CLOSED       surface lift of both Picard--Lefschetz classes
CLOSED       boundary-lattice obstruction to absorbing the coefficient i
NOT CLAIMED  a second real surface region
NOT CLAIMED  transcendence or algebraic independence of special period values
```
