# Extraction Note — gauge_reduction cluster

Campaign: ACTIVE_RECHART_CURVATURE_VALUATIONS / theorem-consolidation
Extracted: 2026-07-30
Scope: defining-function gauge law, tangent projection identity, channel exact sequence, Lorentzian single-edge corollary and pinning conditions, gauge-normal-form quotient Sym_3/Im(G_g) ≅ Q^3.

---

## 1. SOURCE LIST

| # | File | Role |
|---|------|------|
| S1 | `02_PROOF_SUPPLEMENTS/gauge_reduction/Gauge_Channel_Transport_Law.md` | Keystone-specific exact gauge transport law for the three channels (κ_c, κ_s, κ_int), retrodiction table, κ_c-pinning surface, Lorentzian coupling-edge lemma and general single-edge lemma. |
| S2 | `02_PROOF_SUPPLEMENTS/gauge_reduction/GAUGE_NORMAL_FORM_PROOF.md` | Campaign H Lemma H1 (CL-H1): unique gauge-normal representative, obstruction coordinates O_ij, and the quotient Sym_3(Q)/Im(G_g) ≅ Q^3, with SymPy-verified proof steps. |
| S3 | `02_PROOF_SUPPLEMENTS/gauge_reduction/Canonical_Invariant_Reduction_Theorem.md` | General-n, general-r theorem: channel-density polynomial, Σ reduction map, exact sequence 0 → ker Σ → ChannelAccount → Invariant → 0, tangent projection identity, passive-permutation triviality, single-edge corollary at n=3. |

---

## 2. EXACT STATEMENTS

All formulas transcribed verbatim (LaTeX/code as in source). IDs are stable.

### [GAUGE_REDUCTION-T1] Defining-function gauge law (S1 §1; also S3 "Gauge transport law")

S1 form: for gauge-renormalized defining function `\widetilde F=\mu F`, with `\mu=1` on the point, `a=\nabla\log\mu=(u,v,w)`; on the surface point `\widetilde g=g`, and

```
\widetilde H=H+ga^T+ag^T.
```

S3 form (identical content, general n):

```
\widetilde F=\mu F,  \mu(x)=1,  a=\nabla\log\mu(x)
\widetilde g=g,
\widetilde H=H+ga^T+ag^T.
```

### [GAUGE_REDUCTION-T2] Tangent projection identity (S3 "Gauge transport law")

```
P = I - gg^T/q,   Pg = 0   =>   P(ga^T+ag^T)P = 0.
```

Verbatim: "Because the tangent projector \(P=I-gg^T/q\) satisfies \(Pg=0\), \(P(ga^T+ag^T)P=0\). Therefore every total elementary curvature \(\sigma_r\) is preserved, while the channel account may change."

Consequence (boxed in S3):

```
C_r(\widetilde g,\widetilde H)-C_r(g,H)\in\ker\Sigma.
```

For n=3, r=2 (boxed):

```
\delta\kappa_c+\delta\kappa_s+\delta\kappa_{int}=0.
```

### [GAUGE_REDUCTION-T3] Channel-density polynomial and canonical invariant (S3 Theorem)

Setup: `g=\nabla F(x)`, `H=\nabla^2F(x)`, `q=g^Tg\ne0`; split `H=H_s+H_c`, `H_s=\operatorname{diag}(H)`, `H_c=H-H_s`. For `1\le r\le n-1`:

```
\widehat{\mathcal C}_r(t,u)
=
(-1)^{r+1}
\sum_{|I|=r+1}
\det
\begin{pmatrix}
0 & g_I^T\\
g_I & (tH_c+uH_s)_I
\end{pmatrix}.
```

Expansion:

```
\widehat{\mathcal C}_r(t,u)=\sum_{p+q=r}t^pu^q\widehat\kappa_{r;p,q}.
```

Normalization:

```
\kappa_{r;p,q}=\frac{\widehat\kappa_{r;p,q}}{q^{(r+2)/2}}.
```

Canonical elementary curvature invariant (boxed):

```
\sigma_r=\sum_{p+q=r}\kappa_{r;p,q}=\frac{\widehat{\mathcal C}_r(1,1)}{q^{(r+2)/2}}.
```

Channel vector and reduction map (boxed):

```
C_r=(\kappa_{r;r,0},\kappa_{r;r-1,1},\ldots,\kappa_{r;0,r})
\Sigma:C_r\longmapsto\sum_{p+q=r}\kappa_{r;p,q}=\sigma_r.
```

Quotient statement (boxed):

```
C_r/\ker\Sigma\cong\sigma_r,
\ker\Sigma=\{\delta C_r:\sum\delta\kappa_{r;p,q}=0\}.
```

### [GAUGE_REDUCTION-T4] Channel exact sequence (S3 "Canonical invariant reduction")

Boxed verbatim:

```
0\longrightarrow\ker\Sigma
\longrightarrow
\operatorname{ChannelAccount}_r
\xrightarrow{\ \Sigma\ }
\operatorname{InvariantCurvature}_r
\longrightarrow0.
```

In-words form (boxed):

```
channel account = canonical invariant + zero-sum gauge residue.
```

Pure form (blockquote): "Compute the full channel spectrum, then reduce by the summation quotient. The quotient is the intrinsic curvature invariant; the fiber is the exact channel account explaining how that invariant is represented in the chosen chart."

### [GAUGE_REDUCTION-T5] Three-variable Gaussian case (S3)

```
C_2=(\kappa_c,\kappa_{int},\kappa_s),
K_G=\kappa_c+\kappa_s+\kappa_{int}.          (boxed)
\ker\Sigma=\{(a,b,c):a+b+c=0\}.              (boxed)
\kappa_c+\kappa_s+\kappa_{int}=K_G.          (boxed, transport plane)
```

Keystone base representative (boxed):

```
F=x_1^2+x_1x_2+x_3^2-3  at  (1,1,1):
(\kappa_c,\kappa_s,\kappa_{int})=\left(-\frac1{49},\frac1{49},-\frac3{49}\right),
K_G=-\frac3{49}.
```

### [GAUGE_REDUCTION-T6] Keystone gauge data (S1 §1)

```
g=(3,1,2),
H=\begin{pmatrix}2&1&0\\1&0&0\\0&0&2\end{pmatrix},
\widetilde H=
\begin{pmatrix}
2+6u&1+u+3v&2u+3w\\
1+u+3v&2v&2v+w\\
2u+3w&2v+w&2+4w
\end{pmatrix},
|g|^4=(3^2+1^2+2^2)^2=14^2=196.
```

### [GAUGE_REDUCTION-T7] Exact keystone channel transport law (S1 §2) — all boxed

```
\kappa_c(u,v,w)={12uv+6uw+18vw+6w-1\over 49}.
\kappa_s(u,v,w)={12uv+6uw+3u+18vw+13v+2w+1\over 49}.
\kappa_{int}(u,v,w)=-{24uv+12uw+3u+36vw+13v+8w+3\over 49}.
\kappa_c(u,v,w)+\kappa_s(u,v,w)+\kappa_{int}(u,v,w)=-{3\over49}.
\Delta\kappa_c+\Delta\kappa_s+\Delta\kappa_{int}=0.
```

Gauge shifts relative to base triple `(-1/49, 1/49, -3/49)` (all boxed):

```
\Delta\kappa_c={6(2uv+uw+3vw+w)\over49},
\Delta\kappa_s={12uv+6uw+3u+18vw+13v+2w\over49},
\Delta\kappa_{int}=-{24uv+12uw+3u+36vw+13v+8w\over49}.
```

### [GAUGE_REDUCTION-T8] Retrodiction table of four observed gauges (S1 §3)

| gauge a=(u,v,w) | K_G | (κ_c, κ_s, κ_int) |
|---|---|---|
| (1,0,0)      | -3/49 | (-1/49, 4/49, -6/49) |
| (0,1,0)      | -3/49 | (-1/49, 2/7, -16/49) |
| (1,-2,3)     | -3/49 | (-97/49, -130/49, 32/7) |
| (-1/2,5,1)   | -3/49 | (62/49, 247/98, -377/98) |

"All four are direct evaluations of the transport law above." (Independently re-verified arithmetically during extraction: all four rows match T7.)

### [GAUGE_REDUCTION-T9] κ_c-pinning surface, keystone (S1 §4)

Δκ_c = 0 exactly when (boxed):

```
2uv+uw+3vw+w=0.
w(u+3v+1)+2uv=0.          (equivalent, boxed)
w=-{2uv\over u+3v+1}      (rational sheet, boxed, when u+3v+1\neq0)
```

Every pure e1-axis gauge (u,0,0) and pure e2-axis gauge (0,v,0) preserves κ_c for all rational u,v. The pure e3-axis does not:

```
\Delta\kappa_c(0,0,w)={6w\over49}.
```

### [GAUGE_REDUCTION-T10] Lorentzian coupling-edge lemma (S1 §5; S3 "Single-edge coupling corollary")

Coupling edge vector:

```
\nu=(\nu_1,\nu_2,\nu_3)=(g_1H_{23},\;g_2H_{13},\;g_3H_{12}).
```

S1 form (boxed; NOTE the `u^T` typo, see RED FLAGS R1):

```
\Delta_c=2\|\nu\|^2-(\mathbf 1\cdot\nu)^2=u^T(2I-J)\nu,   J=\mathbf1\mathbf1^T.
```

S3 form (boxed, correct quadratic form):

```
\Delta_c=\nu^T(2I-\mathbf1\mathbf1^T)\nu.
```

"The metric \(2I-J\) has signature \((2,1)\). The pure coupling channel is therefore a Lorentzian quadratic form in the weighted coupling-edge vector." (Signature independently verified: eigenvalues of 2I-J are {-1, 2, 2}.)

Edge-vector shift under gauge a=(a_1,a_2,a_3), from `H'_{ij}=H_{ij}+g_i a_j+a_i g_j` (all boxed):

```
\delta\nu_1=g_1(g_2a_3+g_3a_2),
\delta\nu_2=g_2(g_1a_3+g_3a_1),
\delta\nu_3=g_3(g_1a_2+g_2a_1).
```

Coupling-channel shift (boxed):

```
\delta\Delta_c=2\nu^T(2I-J)\delta\nu+\delta\nu^T(2I-J)\delta\nu.
```

Sign convention linking channel to form:

```
\kappa_c=-{\Delta_c\over |g|^4}.
```

### [GAUGE_REDUCTION-T11] Keystone null-direction analysis (S1 §6)

Keystone: `H_{12}=1, H_{13}=H_{23}=0`, base coupling vector `\nu=(0,0,2)`.

```
pure e1-gauge:  \delta\nu=(0,2u,2u).
pure e2-gauge:  \delta\nu=(6v,0,6v).
pure e3-gauge:  \delta\nu=(3w,3w,0),  \Delta\kappa_c={6w\over49}.
```

Claim: e1, e2 shifts "are null directions for the Lorentzian coupling metric and are tangent to the \(\Delta_c\)-level surface through \(\nu=(0,0,2)\)", hence preserve Δ_c and κ_c exactly; e3 shift "is not tangent to the same level surface." (See R8: the e3 shift is ALSO null; tangency, not nullity, is the operative condition.)

### [GAUGE_REDUCTION-T12] General single-edge lemma (S1 §7)

Hypothesis: at the point exactly one nonzero coupling edge `H_{ij}=h`, with `H_{ik}=H_{jk}=0`, k the remaining index; then `\nu_k=g_kh` is the only nonzero component. Conclusions (boxed):

```
\delta\kappa_c(t e_i)=0,  \delta\kappa_c(t e_j)=0     (for all rational t)
\delta\Delta_c=-4t\,g_i g_j g_k h,                     (gauge along opposite vertex e_k)
\delta\kappa_c={4t\,g_i g_j g_k h\over |g|^4}.
```

Keystone check: `(i,j,k)=(1,2,3)`, `g=(3,1,2)`, `h=1`, `|g|^4=196`:

```
\delta\kappa_c={4t\cdot3\cdot1\cdot2\over196}={6t\over49}.
```

### [GAUGE_REDUCTION-T13] Lorentzian single-edge corollary with exact pinning condition, n=3 (S3)

For a pure single-axis gauge `a=te_i`, with `\{i,j,k\}=\{1,2,3\}` (boxed):

```
\delta\kappa_c(te_i)=\frac{4t\,g_1g_2g_3H_{jk}}{q^2}.
```

Exact pinning condition (boxed):

```
te_i pins \kappa_c  \iff  H_{jk}=0.
```

"For the keystone, the only active coupling edge is \(H_{12}=1\). Therefore the \(e_1\) and \(e_2\) gauges preserve \(\kappa_c\), while the \(e_3\) gauge moves it."

### [GAUGE_REDUCTION-T14] Gauge-normal form / quotient theorem (S2, Lemma H1, CL-H1)

Statement, verbatim: For regular `g` (`g1 g2 g3 ≠ 0`), every `H ∈ Sym_3(Q)` has a unique gauge-normal representative

```
H_perp = H − G_g(a),   a_i = H_ii/(2 g_i),   G_g(a) = g a^T + a g^T
```

with `diag(H_perp) = 0` and off-diagonals exactly the obstruction coordinates:

```
H_perp = [[0, O12, O13], [O12, 0, O23], [O13, O23, 0]],
O_ij = H_ij − g_i H_jj/(2 g_j) − g_j H_ii/(2 g_i).
```

Hence:

```
Sym_3(Q)/Im(G_g) ≅ Q^3   via   [H] ↦ O_g(H).
```

### [GAUGE_REDUCTION-T15] Proof of T14 / uniqueness (S2, "verified symbolically, exact SymPy")

Verbatim proof steps:

- Diagonal killed: `H_perp_ii = H_ii − 2 g_i a_i = H_ii − 2 g_i · H_ii/(2 g_i) = 0` — verified `sp.simplify(H_perp[i,i]) = 0` for all i.
- Off-diagonal = obstruction: `H_perp_ij = H_ij − (g_i a_j + a_i g_j) = O_ij` — verified `sp.simplify(H_perp_ij − O_ij) = 0`.
- Im(G_g) is 3-dimensional: the symmetric 6-vectors of `G_g(e1), G_g(e2), G_g(e3)` have rank 3 on the regular locus (`gauge_image_rank(g) = 3`).
- Obstruction map surjective onto Q^3: the Jacobian of `(O_12, O_13, O_23)` w.r.t. `(H11,H22,H33,H12,H13,H23)` has rank 3, and `Im(G_g)` (rank 3) is exactly its kernel (the obstruction is gauge-invariant: `O(H + G_g(b)) = O(H)`, verified symbolically). So `Sym_3(Q) = Im(G_g) ⊕ {gauge-normal}` and the quotient is `Q^3`.

Uniqueness clause, verbatim: "**CL-H1: PASS.** Uniqueness of `a` follows from `g_i ≠ 0` (the diagonal equations `2 g_i a_i = H_ii` have a unique solution). The gauge-normal carrier `O = O_g(H)` is the complete invariant of the same-gradient gauge class."

### [GAUGE_REDUCTION-T16] Passive role permutations are trivial (S3)

For a permutation matrix `P_\sigma`, `(g,H)\mapsto(P_\sigma g,P_\sigma HP_\sigma^T)` is passive relabelling; since

```
\operatorname{diag}(P_\sigma HP_\sigma^T)=P_\sigma\operatorname{diag}(H)P_\sigma^T,
```

the self/coupling split is equivariant, hence (boxed):

```
C_r(P_\sigma g,P_\sigma HP_\sigma^T)=C_r(g,H)   (up to label order)
```

"The passive \(S_n\) orbit collapses to a singleton. It is a covariance check, not a new invariant. The nontrivial role action is active recharting: solving the same relation in a different output role changes the defining function, hence induces a gauge transport."

### [GAUGE_REDUCTION-T17] Interpretation summary statements (S1 §8) — boxed prose

```
gauge changes do not alter K_G, but act nontrivially on the channel allocation.
endpoint gauges of the active coupling edge preserve \kappa_c; opposite-vertex gauges move it.
```

Also: `K_G=-{3\over49}` fixed; channel triple moves inside plane `\kappa_c+\kappa_s+\kappa_{int}=-{3\over49}`.

---

## 3. CONVENTIONS

- **Base objects:** `g=\nabla F(x)`, `H=\nabla^2 F(x)` at a regular point of the hypersurface `F=0`; scalar `q=g^Tg\ne0`; `|g|^4 = q^2` (S1 writes `|g|^4`, S3 writes `q^2` — same quantity).
- **Gauge convention:** `\widetilde F=\mu F` with `\mu=1` AT THE POINT ONLY; gauge vector `a=\nabla\log\mu(x)`. Gradient invariant (`\widetilde g=g`), Hessian shifts by `+ga^T+ag^T` (T1). S2 uses the SAME operator `G_g(a)=ga^T+ag^T` but SUBTRACTS it to normalize (`H_perp = H − G_g(a)`); direction differs, operator identical.
- **Keystone datum:** `F=x_1^2+x_1x_2+x_3^2-3` at `(1,1,1)`; `g=(3,1,2)`; `H=[[2,1,0],[1,0,0],[0,0,2]]`; `q=14`, `q^2=196`; base triple `(\kappa_c,\kappa_s,\kappa_{int})=(-1/49, 1/49, -3/49)`; `K_G=-3/49`. Gauge components named `(u,v,w)`.
- **Channel split:** in the privileged coordinate basis, `H_s=\operatorname{diag}(H)` (self), `H_c=H-H_s` (coupling); channel polynomial grades t↦coupling, u↦self; `\kappa_{r;p,q}` has p = coupling degree, q = self degree. Sign prefactor `(-1)^{r+1}` on the bordered-determinant sum; normalization by `q^{(r+2)/2}`.
- **Tuple order (INCONSISTENT across sources, see R3):** S3 general definition gives `C_2=(\kappa_c,\kappa_{int},\kappa_s)` (t^2, tu, u^2 order); S1 tables and the S3 keystone box use `(\kappa_c,\kappa_s,\kappa_{int})`.
- **Coupling channel sign:** `\kappa_c=-\Delta_c/|g|^4` with `\Delta_c=\nu^T(2I-J)\nu`, `\nu=(g_1H_{23}, g_2H_{13}, g_3H_{12})`, `J=\mathbf1\mathbf1^T`. Note the ANTI-cyclic index pattern: component i of ν pairs g_i with the OPPOSITE edge H_{jk}.
- **Lorentzian metric:** `2I-J` on R^3, signature `(2,1)` (eigenvalues -1, 2, 2).
- **Single-axis gauge sign pattern:** `\delta\Delta_c=-4t\,g_ig_jg_kh` (negative), hence `\delta\kappa_c=+4t\,g_1g_2g_3H_{jk}/q^2` (positive) — the two signs are consistent through `\kappa_c=-\Delta_c/q^2`.
- **Field of scalars:** S1/S3 say "for every rational gauge vector"; S2 works over `Q` explicitly (`Sym_3(Q)`, `Q^3`). The framework treats rational-exactness as the ambient convention; the formulas are polynomial identities valid over any field of characteristic 0.
- **Regularity for gauge-normal form:** `g_1g_2g_3\ne0` ("regular locus") is REQUIRED for T14/T15; the transport law T1–T13 needs only `q\ne0`.
- **Symbol overloads to watch:** `q` = scalar g^Tg AND self-degree index in `\kappa_{r;p,q}` (S3, same formula); `P` = tangent projector AND `P_\sigma` = permutation matrix (S3); `u` = first gauge component (S1 §1-4) AND second grading variable of `\widehat{\mathcal C}_r(t,u)` (S3) AND the typo'd vector in S1 §5 (R1).

---

## 4. UNIQUE MATERIAL (exists ONLY here — must not be lost)

- **S1 only:**
  - The exact closed-form keystone transport polynomials for all three channels as functions of (u,v,w) [T7] — nowhere else in the cluster; the retrodiction table [T8] depends on them.
  - The κ_c-pinning surface in explicit form: `2uv+uw+3vw+w=0`, factored `w(u+3v+1)+2uv=0`, and the rational sheet `w=-2uv/(u+3v+1)` [T9]. This is the full 2-parameter pinning locus, strictly stronger than the axis-pinning statements elsewhere.
  - The explicit gauge shift of the coupling-edge vector, componentwise: `\delta\nu_i = g_i(g_j a_k + g_k a_j)` pattern [T10], and the exact second-order shift formula `\delta\Delta_c=2\nu^T(2I-J)\delta\nu+\delta\nu^T(2I-J)\delta\nu` (the only place the quadratic term is written).
  - The keystone null-vector computations `\delta\nu=(0,2u,2u), (6v,0,6v), (3w,3w,0)` [T11].
  - The single-edge lemma in Δ_c form with the sign `-4t\,g_ig_jg_kh` [T12].
  - The gauge matrix `\widetilde H` fully written out for the keystone [T6].
- **S2 only:**
  - The gauge-normal form itself: normalizing gauge `a_i=H_ii/(2g_i)`, zero-diagonal representative, obstruction coordinates `O_ij = H_ij − g_iH_jj/(2g_j) − g_jH_ii/(2g_i)` [T14]. No other file in the cluster defines O_ij.
  - The quotient/direct-sum statement `Sym_3(Q)=Im(G_g)\oplus\{gauge-normal\}` and `Sym_3(Q)/Im(G_g)\cong Q^3` [T14–T15].
  - The rank-3 facts (Im(G_g) rank 3 on regular locus; obstruction Jacobian rank 3; Im(G_g) = kernel of obstruction) and gauge-invariance `O(H+G_g(b))=O(H)` [T15].
  - The uniqueness argument for `a` (diagonal equations `2g_ia_i=H_ii`) and the "complete invariant of the same-gradient gauge class" claim [T15].
  - Campaign bookkeeping token "CL-H1: PASS".
- **S3 only:**
  - The general-(n,r) channel-density polynomial `\widehat{\mathcal C}_r(t,u)` with `(-1)^{r+1}` prefactor and `q^{(r+2)/2}` normalization [T3].
  - The tangent projection identity `P(ga^T+ag^T)P=0` as the mechanism for σ_r invariance [T2].
  - The exact sequence `0 → ker Σ → ChannelAccount_r → InvariantCurvature_r → 0` [T4].
  - The general pinning biconditional `te_i pins κ_c ⟺ H_{jk}=0` [T13] (S1 §7 only proves the single-edge special case; the iff is only in S3).
  - The passive-permutation equivariance/triviality statement [T16].

Cross-file redundancy (safe to consolidate): T1 (gauge law) appears in S1 and S3; the Lorentzian form Δ_c appears in S1 §5 and S3; keystone base triple appears in S1 and S3; single-axis δκ_c coefficient `4t g_1g_2g_3 H_{jk}/q^2` appears in S1 §7 (as h-special-case) and S3 (general).

---

## 5. RED FLAGS

- **R1 (typo, load-bearing formula).** S1 §5: `\Delta_c=2\|\nu\|^2-(\mathbf 1\cdot\nu)^2 = u^T(2I-J)\nu` — the `u^T` is wrong; it must be `\nu^T(2I-J)\nu` (as S3 has it, and as the first equality requires). The stray `u` also collides with the gauge component u. Consolidated statement should use the S3 form.
- **R2 (broken LaTeX).** S1 §7: "A pure gauge along either endpoint \(e_i or \(e_j\)" — unclosed math delimiter on `e_i`.
- **R3 (tuple-order inconsistency).** S3 defines `C_2=(\kappa_c,\kappa_{int},\kappa_s)` (from the general grading order), but S1's table header, S1's base triple, and S3's own keystone box all use order `(\kappa_c,\kappa_s,\kappa_{int})`. Any consolidated theorem must fix one order.
- **R4 (symbol overload in one formula).** S3: `\kappa_{r;p,q}=\widehat\kappa_{r;p,q}/q^{(r+2)/2}` uses `q` simultaneously as the self-degree index (subscript) and as the scalar `g^Tg` (denominator). Needs renaming on consolidation.
- **R5 (proof gap labelled as theorem).** S3 asserts "Therefore every total elementary curvature σ_r is preserved" directly from `P(ga^T+ag^T)P=0` [T2]. The link between the bordered-determinant definition of `\widehat{\mathcal C}_r(1,1)` and the projected Hessian `PHP` is never stated or derived in this file; the invariance of σ_r under gauge is a sketch, not a written proof, though the document is titled "Theorem".
- **R6 (unreproducible verification reference).** S2's proof rests on SymPy checks (`sp.simplify(...) = 0`, `gauge_image_rank(g) = 3`) but cites no script path, notebook, or artifact anywhere in the file. The verification cannot be reproduced from this document alone; the referenced function `gauge_image_rank` is dangling.
- **R7 (rationals-only phrasing).** S1 states results "for every rational gauge vector (u,v,w)" / "for all rational t". The identities are polynomial and hold over R; the rational restriction is a framework convention but reads as a mathematical limitation. Consolidation should state the identity level explicitly.
- **R8 (misleading nullity argument).** S1 §6 attributes e1/e2 preservation to their δν being "null directions ... and tangent". In fact the e3 shift `\delta\nu=(3w,3w,0)` is ALSO null for `2I-J` (checked: `2\cdot18w^2-(6w)^2=0`); nullity kills only the quadratic term `\delta\nu^T(2I-J)\delta\nu`. The discriminating condition is tangency, i.e. vanishing of the cross term `2\nu^T(2I-J)\delta\nu`. The prose is not wrong but invites the false inference null ⇒ pinning.
- **R9 (scope mismatch, not an error).** S3's "Single-edge coupling corollary" formula `\delta\kappa_c(te_i)=4t\,g_1g_2g_3H_{jk}/q^2` is actually exact for ARBITRARY H (the single-axis δν is always null, so the shift is exactly linear in t); only the pinning application needs the single-edge hypothesis. S1 §7 states the same formula only under the single-edge hypothesis. The consolidated corollary should carry the general statement (S3's) with the general-H validity made explicit.
- **R10 (loose quotient notation).** S3 writes `C_r/\ker\Sigma\cong\sigma_r` — quotienting a vector by a subspace and identifying with a scalar; the intended object is (affine fiber space of channel vectors)/ker Σ ≅ R (value σ_r). Harmless but should be cleaned in the consolidated statement.
- **Verification note (not a flag):** all four retrodiction rows [T8], the base triple, the zero-sum identity, the pinning-surface factorization, the keystone δν vectors, the signature of 2I-J, and the `6t/49` cross-check between T7, T12, and T13 were independently re-verified arithmetically during extraction and all agree.
