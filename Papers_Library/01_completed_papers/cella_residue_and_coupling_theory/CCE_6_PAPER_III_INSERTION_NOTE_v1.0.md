# Paper III insertion note — CCE-6 exact native-sweep clearance

**Status:** authorized mathematical insertion  
**Target:** immediately after the admissible-corridor conditions preceding
Theorem 7F.1, with the proof cited in the CCE-6 clearance theorem

## Replacement text

Replace the sentence that merely asks for thin tubular neighbourhoods on
which the swept boundary avoids its surface divisors by the following lemma.

> **Lemma 7F.A — native-sweep clearance is inherited from refined curve
> admissibility.** Put \(A=\rho+1\), \(B=\rho-1\),
> \(c=B/A\), and use homogeneous angular and fibre coordinates
> \([V:T]\), \([\Xi:H]\).  With
> \(D_1=T-cV\), \(D_2=T-c^2V\), the norm and polar pullbacks are
> \[
> N=D_2\Xi^2+(1-c)TH^2,
> \qquad T(\Xi^2+H^2)=0.
> \]
> Their fibre discriminant and resultant are
> \[
> \operatorname{Disc}_{\Xi}(N)=-4(1-c)TD_2,
> \qquad
> \operatorname{Res}(N,\Xi^2+H^2)=c^2D_1^2.
> \]
> Under the Stage-1 birational coordinate,
> \(T=0,D_1=0,D_2=0\) are respectively
> \(x=x_p,x=1,x=\infty\).  The certified corridor bounds give
> \(|c|\ge1/320\), \(|1-c|\ge2/5\), and
> \(|1+c|\ge1/5\).  Therefore transport of the primary relative
> representative in the curve complement of \(x_p,1,\infty\) has a
> collision-free four-quadrant angular and relative-fibre sweep over either
> exact corridor.  At \(V=0\) only the \(C\)-branches glue; at \(V=T\) only
> the \(S\)-branches glue; the norm endpoints remain distinct on both faces.
> Thus the native swept chains form an integral isotopy, and surface lift
> commutes with the two certified Gauss--Manin transports.

## Quantitative sentence for the proof

After the lemma, add:

> If a normalized refined curve representative has exact witnesses
> \(|T|\ge\varepsilon_\infty\),
> \(|D_1|\ge\varepsilon_1\), and
> \(|D_2|\ge\varepsilon_2\), then
> \(|\operatorname{Disc}(N)|\ge(8/5)\varepsilon_\infty\varepsilon_2\)
> and
> \(|\operatorname{Res}(N,\Xi^2+H^2)|\ge
> \varepsilon_1^2/102400\).  On both released corridors one may take
> \(\varepsilon_\infty=\varepsilon_1=\varepsilon_2
> =1/105186307200\), obtained from the exact chordal separation of
> \([1:0],[1:c],[1:c^2],[0:1],[1:1]\).

## Scope sentence

Retain the native-image restriction and add:

> This clearance result applies to
> \(\mathscr S_{\mathbb Z}^{\rm nat}=\operatorname{im}L_{\mathbb Z}\);
> it neither identifies that image with whole surface homology nor makes
> \((1/4)R_{\mathbb Z}\) integral.
