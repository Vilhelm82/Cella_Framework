# DBP Native Relative-Period Route Theorem

## Pole-free finite-interval compilation, v1.0

**Date:** 2026-07-12  
**Depends on:** `DBP_LANDEN_TRACE_THEOREM_COMPLETE_v1.1.md`  
**Verification:** `verify_dbp_native_relative_period_route.py`  
**Scope:** the two DBP relative paths on the fixed curve (E_{128}); this is not a general elliptic-integral evaluator

---

## 0. Result

Let

\[
E_{128}:\qquad Y^2=X^3-X^2+X-1=(X-1)(X^2+1)
\]

and

\[
\Theta=8\frac{X-3}{X+7}\frac{dX}{Y}.
\]

The corrected Landen--Trace theorem reduces the two DBP constants to

\[
I_{\rm primary}=\frac12J_+-2\pi,
\qquad
I_{\rm dual,CPV}=\frac12H_-,
\]

where

\[
J_+=\int_{\Gamma_+}\Theta,
\qquad
H_-=-i\operatorname{CPV}\int_{\Gamma_-}\Theta.
\]

Both (J_+) and (H_-) admit ordinary, pole-free integrals over the compact interval
([0,1]):

\[
\boxed{
J_+=\int_0^1 g_+(t)\,dt
}
\tag{0.1}
\]

and

\[
\boxed{
H_-=\int_0^1 g_-(t)\,dt.
}
\tag{0.2}
\]

Put (w=1-t) and (s=\sqrt2). Then

\[
P_+(t)=t^4+2t^2w^2+2w^4,
\]

\[
\boxed{
g_+(t)=
16\frac{t^2-2w^2}{t^2+8w^2}\frac1{\sqrt{P_+(t)}}
}
\tag{0.3}
\]

and

\[
P_-(t)=t^4-2t^2w^2+2w^4=(t^2-w^2)^2+w^4,
\]

\[
\boxed{
g_-(t)=
-\frac{16t^2}
{\sqrt{P_-(t)}\left(t^2+2w^2+s\sqrt{P_-(t)}\right)}.
}
\tag{0.4}
\]

The radicands are strictly positive on ([0,1]), and both integrands extend
continuously to the endpoints. No principal-value operation remains in (0.4).

---

## 1. Primary path

The primary trace path is

\[
\Gamma_+: X=1\longrightarrow+\infty,
\qquad Y>0.
\]

Set

\[
X=1+z^2,\qquad z\in[0,\infty).
\]

Then

\[
Y=z\sqrt{z^4+2z^2+2}
\]

and therefore

\[
J_+
=
\int_0^\infty
16\frac{z^2-2}{z^2+8}
\frac{dz}{\sqrt{z^4+2z^2+2}}.
\tag{1.1}
\]

Now set

\[
z=\frac{t}{1-t}=\frac{t}{w}.
\]

After clearing the common power (w^{-4}) under the square root, (1.1)
becomes (0.1)--(0.3). The endpoint values are

\[
g_+(0)=-2\sqrt2,
\qquad
g_+(1)=16.
\tag{1.2}
\]

Since (P_+) is a sum of nonnegative terms and (t,w) cannot vanish
simultaneously, (P_+>0) on the closed interval.

---

## 2. Dual path and exact polar subtraction

The dual trace path is

\[
\Gamma_-: X=1\longrightarrow-\infty,
\]

with the physical sheet

\[
Y=+i\sqrt{-(X-1)(X^2+1)}
\qquad (X<1).
\]

Set

\[
X=1-z^2,\qquad z\in[0,\infty).
\]

For the real differential (β=-i\Theta),

\[
H_-
=
\operatorname{CPV}\int_0^\infty h_-(z)\,dz,
\]

\[
h_-(z)=
16\frac{z^2+2}{z^2-8}
\frac1{\sqrt{z^4-2z^2+2}}.
\tag{2.1}
\]

The pole is at

\[
z_0=\sqrt8=2\sqrt2
\]

and has residue (4). Introduce the exact polar kernel

\[
p(z)=\frac{16\sqrt2}{z^2-8}.
\tag{2.2}
\]

It has the same residue, and

\[
p(z)=
\frac{d}{dz}
\left[
4\log\left|\frac{z-2\sqrt2}{z+2\sqrt2}\right|
\right].
\]

Consequently,

\[
\operatorname{CPV}\int_0^\infty p(z)\,dz=0.
\tag{2.3}
\]

Thus

\[
H_-=\int_0^\infty r_-(z)\,dz,
\]

\[
r_-(z)=
\frac{16}{z^2-8}
\left(
\frac{z^2+2}{\sqrt{z^4-2z^2+2}}-\sqrt2
\right).
\tag{2.4}
\]

The apparent singularity in (2.4) is removable. Its value at (z_0) is

\[
r_-(z_0)=-\frac{16\sqrt2}{25}.
\tag{2.5}
\]

---

## 3. Cancellation of the removable singularity before evaluation

Use (z=t/w), and write

\[
A=t^2+2w^2,
\qquad
D=t^2-8w^2.
\]

The compactified form of (2.4) is initially

\[
16\frac{A/\sqrt{P_-}-\sqrt2}{D}.
\tag{3.1}
\]

The exact identity

\[
A^2-2P_-=-t^2D
\tag{3.2}
\]

rationalizes the numerator and cancels (D) identically. This gives (0.4)
without a branch or pole test at runtime.

The endpoint values are

\[
g_-(0)=0,
\qquad
g_-(1)=16(1-\sqrt2).
\tag{3.3}
\]

At the former pole, where

\[
t_0=\frac{2\sqrt2}{1+2\sqrt2},
\]

the smooth formula has value

\[
g_-(t_0)
=
-\frac{128+144\sqrt2}{25}.
\tag{3.4}
\]

Finally,

\[
P_-=(t^2-w^2)^2+w^4>0
\]

on ([0,1]), so (0.4) is real and finite everywhere.

---

## 4. Evaluator consequences

For these two DBP claims, the native evaluator may compile directly to the two
fixed algebraic kernels (0.3) and (0.4). In particular:

1. the primary route needs one ordinary integral plus a certified value of (π);
2. the dual route needs one ordinary integral and no runtime CPV operation;
3. the dual pole and its residue remain in the certificate ledger even though they
   disappear from the execution kernel;
4. complete (K), (E), and (Π) atoms are not execution dependencies;
5. AGM, Carlson forms, Arb, mpmath, SymPy, and generic elliptic libraries are not
   production dependencies;
6. decimal pins are regression oracles only and must never be used to form a
   certificate.

This route retires generic elliptic evaluation only for the two stated DBP path
claims. It does not retire general period normal forms or general elliptic
evaluation methods.

---

## 5. Numerical regression pins

Using the standing independent values from the corrected DBP corpus,

\[
I_{\rm primary}
\approx
-5.01049070266041876905002116052677764805699485672160,
\]

\[
I_{\rm dual,CPV}
\approx
-3.988001085974558097719762257539087379694121855552360291.
\]

Therefore the transformed targets have the regression prefixes

\[
J_+
\approx
2.54538920903833541575053121206445624067468788405722,
\]

\[
H_-
\approx
-7.976002171949116195439524515078174759388243711104720582.
\]

These decimals are not part of the proof. A successful native run must emit a
dyadic bracket that contains the target and independently rounds to these prefixes.

