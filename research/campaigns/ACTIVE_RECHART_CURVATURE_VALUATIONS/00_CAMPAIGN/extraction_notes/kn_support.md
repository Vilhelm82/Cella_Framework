# Extraction note — KN support trio (mass-charge zeros theorem, n=3 retrodiction, LEAD-2 valuation brief)

**Extracted:** 2026-07-30, for the theorem-consolidation campaign.
**Focus mandate:** six-numerator factorization; inner-branch counterexample (exact point + what fails);
retrodiction dictionary (physical boundary -> local normal form); earlier valuation terminology map
(old term -> new term).

All quoted material in Section 2 is **verbatim** from source (including any typos); commentary is
outside the code blocks. Source tags: **[A]**, **[B]**, **[C]** per Section 1.

---

## 1. SOURCE LIST

- **[A]** `02_PROOF_SUPPLEMENTS/masscharge_support/LEAD7_masscharge_zeros_theorem.md` (2026-07-07) —
  the interior-cleanliness **theorem**: mass-charge coupling zeros/poles of `g_F(u=0)` are exactly the
  role divisors on the outer physical wedge `W₊`; contains the six-numerator factorization and the
  inner-branch counterexample. Certificate `verification/lead7_test4_masscharge_zeros.py`.
- **[B]** `03_APPLICATION_KERR_NEWMAN/reports/LEAD7_retrodiction_n3.md` (2026-07-07) — the n=3
  retrodiction tier: symbolic pole orders 3/4/4, the `−m(m+5)/B` parity-fixed normal form, exact
  closed-form coefficients `C_Ω`, `C_Φ`, `C_ext`, the `N_ext` gate closure, and the Schwarzschild
  double-reflection corner. Certificates `lead7_test5..test10`.
- **[C]** `03_APPLICATION_KERR_NEWMAN/reports/LEAD2_Role_Singularity_Valuation_Brief.md` (banked
  2026-07-06) — **external, conjectural** ChatGPT-origin theorem brief for the Role-Singularity
  Valuation Law (n=2 seed), preserved verbatim under a provenance/trust header; source of the older
  valuation terminology and the header's old->new reconciliation map. NOT a certificate.

---

## 2. EXACT STATEMENTS

### 2.1 From [A] — mass-charge zeros theorem

**[KN_SUPPORT-D1] KN fundamental relation and domain (outer physical wedge).** Verbatim [A]:

```
Let the Kerr-Newman graph be `M² = U(S,J,Q)`,
`U = S/(4π) + πJ²/S + Q²/2 + πQ⁴/(4S)`. The theorem holds on the **outer physical wedge**
W₊ = {S,J,Q > 0, U_S > 0} = {S,J,Q > 0, S² > π²(4J²+Q⁴)},
equivalently the outer-horizon branch `S = S₊ = π(2M²−Q²+2√disc)`, `disc>0`. **Not**
`{S,J,Q>0, disc>0}` alone: `disc>0` also contains the **inner** branch `S=S₋` where
`U_S<0`, on which a numerator can vanish in the interior (see the counterexample below).
`U_S>0` is positive Hawking temperature; `W₊` is the thermodynamically physical region and
the domain on which the metric `g_F(u=0)` lives.
```

**[KN_SUPPORT-T1] Main theorem statement.** Verbatim [A]:

```
Each output chart `E_i = f_i(M, E_j, E_k)` solves `M²=U` for `E_i`; its **mass-charge
couplings** are the mixed second partials `Λ_{i,{M,j}} = ∂²E_i/∂M∂E_j` (pairs joining the
graph value `M` to one charge `E_j`).

**Theorem.** On `W₊`, every mass-charge coupling `Λ_{i,{M,j}}` is finite and nonzero. In
the closure `W̄₊`, every numerator zero **and** every native pole of the mass-charge
couplings is supported on
`{J=0} ∪ {Q=0} ∪ {U_S=0} = Ω=0 ∪ Φ_e=0 ∪ T=0`. Consequently the mass-charge inverse-channel
metric `g_F(u=0)_{ii} = q_i²·Σ_{mass-charge j} 1/Λ_{i,{M,j}}²` has **no interior curvature
singularity** — all its curvature divergences lie on the role boundaries.
```

**[KN_SUPPORT-F1] Uniform coupling formula (proof step 1, cert T4-a).** Verbatim [A]:

```
∂E_i/∂M = 2M/U_i,          Λ_{i,{M,j}} = ∂²E_i/∂M∂E_j = 2M·(U_ii U_j − U_i U_ij)/U_i³.
```

with the surrounding verbatim identifications:

```
The **pole** is the native divisor `U_i=0` (`U_S=0` ⇔ T=0 for the entropy chart, `U_J=0` ⇔
Ω=0, `U_Q=0` ⇔ Φ_e=0). The **zero** is the numerator `N_{ij} = U_ii U_j − U_i U_ij`.
Verified against explicit differentiation of the solved chart functions `f_S, f_J, f_Q`
for all six couplings (numeric, max mismatch ~10⁻³⁷). *(cert: T4-a)*
```

**[KN_SUPPORT-F2] THE SIX-NUMERATOR FACTORIZATION (proof step 2, cert T4-b).** Verbatim table [A]:

```
| coupling | `N_{ij}` factorization | zero locus |
|---|---|---|
| `Λ_{S,{M,J}}` | `(J/2S²)·[π²(4J²+Q⁴)/S² + 1]` | J=0 (Ω=0) |
| `Λ_{S,{M,Q}}` | `(πQ/S²)·[(4J²+Q⁴)(1+πQ²/S)/2S + Q²U_S]` | Q=0 (Φ_e=0) |
| `Λ_{J,{M,S}}` | `(2π/S)U_S + 4π²J²/S³` | U_S=0 ∧ J=0 |
| `Λ_{J,{M,Q}}` | `(2π/S)·Q·(1+πQ²/S)` | Q=0 (Φ_e=0) |
| `Λ_{Q,{M,S}}` | `(1+3πQ²/S)U_S + πQ⁴(1+πQ²/S)/S²` | U_S=0 ∧ Q=0 |
| `Λ_{Q,{M,J}}` | `(2πJ/S)·(1+3πQ²/S)` | J=0 (Ω=0) |
```

(Extractor spot-check: expanded `N_{S,J} = U_SS U_J − U_S U_SJ` by hand from `U`; it reproduces row 1
exactly. Row-3 form matches the counterexample expression in [KN_SUPPORT-C1].)

**[KN_SUPPORT-F3] Vieta relations / positivity of `U_S` (proof step 3, cert T4-c).** Verbatim [A]:

```
`S_± = π(2M²−Q² ± 2√disc)` are the two roots of the entropy quadratic, with
`S_+S_− = π²(4J²+Q⁴)` and `S_+−S_− = 4π√disc`. Hence on the outer branch `S=S₊`
U_S = [S² − π²(4J²+Q⁴)]/(4πS²) = √disc / S_+  > 0   on W₊,   = 0 ⇔ disc=0 (extremal).
```

**[KN_SUPPORT-L1] Nonnegative-coefficient brackets (proof step 4, cert T4-d).** Verbatim [A]:

```
After clearing positive powers of `S`, each bracket in the table is a polynomial with
**nonnegative** coefficients in the strictly positive variables `(S,J,Q,U_S,π)` —
equivalently, a positive monomial denominator times a nonnegative-coefficient polynomial
(cert T4-d). So each bracket is `> 0` on `W₊`.
```

**[KN_SUPPORT-L2] Role of the extremal divisor (corrected).** Verbatim [A]:

```
Generic `U_S=0` (`T=0`) is **not** a numerator zero: `N_{J,S}` and `N_{Q,S}` vanish only
where `U_S=0` **and** (`J=0` or `Q=0`), i.e. codim-2 corners. `T=0` enters as the **native
pole** of the entropy-chart couplings, through the `U_i³ = U_S³` denominator of the uniform
formula.
```

**[KN_SUPPORT-T2] Curvature corollary (analytic).** Verbatim [A]:

```
Each `Λ_{i,{M,j}}` is analytic, finite and nonzero on `W₊`, so each `1/Λ²` is analytic on
`W₊`. Since `q_i>0` in the interior, every diagonal entry `g_{ii}` is positive and
analytic, hence `det(g)=∏_i g_{ii} ≠ 0` on `W₊`. Therefore `g⁻¹`, the Christoffel symbols,
and the curvature tensor/scalar are finite analytic functions on `W₊`, so no interior
curvature singularity occurs.
```

**[KN_SUPPORT-C1] THE INNER-BRANCH COUNTEREXAMPLE (cert T4-e).** Verbatim [A]:

```
`{disc>0}` is **too big** — it admits an interior numerator zero on the inner branch. At
S = π√3/2,  J = 1/4,  Q = 1  ⟹  M² = U = 1/2 + 1/√3,  disc = 1/48 > 0,
one has `U_S = −1/(6π) < 0` (inner branch) and `N_{J,S} = (S²+4π²J²−π²Q⁴)/(2S³) = 0`. This
point satisfies `disc>0` but is excluded by `W₊ = {U_S>0}`. So the theorem must be stated on
`W₊`, not on `{disc>0}` (cert T4-e). This is exactly the physical/unphysical split: the
outer horizon has `T>0` (`U_S>0`), the inner horizon `T<0`.
```

What fails, precisely: at the exact point `(S,J,Q) = (π√3/2, 1/4, 1)` the numerator of the coupling
`Λ_{J,{M,S}}` vanishes (`N_{J,S}=0`) at an interior point of `{S,J,Q>0, disc>0}`, so on that larger
domain the metric component would pole in the interior; the point lies on the inner branch `S=S₋`
(`U_S<0`, i.e. `T<0`). (Extractor re-verified all four numbers: `S²+4π²J²−π²Q⁴ = 3π²/4+π²/4−π² = 0`;
`U_S = (3π²/4 − 5π²/4)/(4π·3π²/4) = −1/(6π)`; `U = √3/8 + 1/(8√3) + 1/2 + 1/(2√3) = 1/2 + 1/√3`;
`(S/π − (2M²−Q²))²/4 = (√3/2 − 2/√3)²/4 = 1/48`, and `S/π = √3/2` equals the lower Vieta root, so
`S = S₋`. All exact.)

**[KN_SUPPORT-C2] Charge-charge contrast (why u=0; interior zero of a charge-charge coupling).**
Verbatim [A]:

```
the charge-charge couplings `Λ_{i,{j,k}}` are *not* covered by this theorem and do have
interior zeros (e.g. `Λ_{Q,{S,J}}=0` at (M,J,Q)=(2,0.826,1.699), Test 3 T3-3) — these are
the LEAD-2 channel-isotropy strata. That is precisely why the metric must exclude them
(u=0): including them (u>0) would pole in the interior. The theorem makes the u=0 selection
structural.
```

**[KN_SUPPORT-S0] What [A] says remains open (superseded — see RED FLAG R1).** Verbatim [A]:

```
**Remaining for full certification:** the exact pole *coefficients* at each role divisor
(the KN analogue of the n=2 RC-5 retrodiction tier `C_ext`, `C_sch` in the π-frame). The
orders 3/4/4 are numeric; a closed form for the leading coefficients would complete the
retrodiction.
```

### 2.2 From [B] — n=3 retrodiction tier

**[KN_SUPPORT-T3] The order law (retrodiction dictionary core).** Verbatim table [B]:

```
| divisor | coordinate | order | type | how it's fixed (symbolic) |
|---|---|---|---|---|
| extremal `T=0` | `δ = S − S_ext`, `S_ext=π√(4J²+Q⁴)` | **3** | generic | generic Laurent δ⁻³ lemma (Test 7 T7-a) + `A₂>0` (T7-e: `A₂` = δ²-coeff of `G_S` identically, a sum of positives) + `C_ext<0` (Test 8) |
| `Ω=0` | `J` | **4** | reflection-fixed | `−m(m+5)/B` lemma at `m=2` (Test 10) + `B_J>0` (Test 6) |
| `Φ_e=0` | `Q` | **4** | reflection-fixed | `−m(m+5)/B` lemma at `m=2` (Test 10) + `B_Q>0` (Test 6) |
```

and verbatim framing:

```
This is the n=3 realization of the paper's Result-6 law (order-3 generic / order-4
reflection-fixed), now with **both** charge reflections (`Ω=0`, `Φ_e=0`) as the
reflection-fixed pair and the extremal edge as the generic divisor.
```

**[KN_SUPPORT-DICT1] RETRODICTION DICTIONARY (assembled from [B]; physical boundary -> local normal
form).** Not a verbatim block — this is the consolidation view; every entry traces to a verbatim ID:

| physical boundary | defining locus / coordinate | local normal form | order | leading coeff | trace |
|---|---|---|---|---|---|
| Extremal horizon `T=0` (generic edge) | `δ = S − S_ext`, `S_ext = π√(4J²+Q⁴)`; metric analytic, only `g_SS ~ A₂δ²` collapses | odd-order Laurent `R ~ C_ext·δ⁻³`, `C_ext = A₂⁻¹·∂_S ln(g_JJ g_QQ)|_ext` | 3 | exact rational in `(S,Q,π)` on extremal surface; `C_ext<0` everywhere (gate CLOSED) | T3, F8, F9, T5 |
| Static limit `Ω=0` (reflection face, `J↦−J`) | `J→0`; collapsing `g_x=B_J·J²+O(J⁴)`, transverse components `~J⁻²` | `R = −14/B_J·J⁻⁴ + O(J⁻²)` (`m=2` case of `−m(m+5)/B`) | 4 | `C_Ω(S,Q)` exact closed form (F5) | T3, T4, F4, F5 |
| Uncharged limit `Φ_e=0` (reflection face, `Q↦−Q`) | `Q→0`; same structure with `B_Q` | `R = −14/B_Q·Q⁻⁴ + O(Q⁻²)` | 4 | `C_Φ(S,J)` exact closed form (F6) | T3, T4, F4, F6 |
| Schwarzschild double-reflection corner | `J=Q=0`, ray `S=s` free; approach `Q=ε`, `J=ρεᵃ` | Newton wedge `R ~ ε^{−m(a)}`, `m(a)=max(4a−2, 4−2a)`; balanced diagonal order exactly 2, `ε²R → R₀(s,ρ) < 0` with genuine mixed term | 2 (mildest boundary point) | `R₀` finite negative; residues `κ_Ω(s)`, `κ_Φ(s)` exact | T6 |
| Reflection-face ∩ extremal corners | `Ω=0∩ext` (`S_ext=πQ²`), `Φ_e=0∩ext` (`S_ext=2πJ`) | reflection coefficient degenerates — `C_Ω ∝ (πQ²−S)²`, `C_Φ ∝ (2πJ−S)²` vanish there; face pole "heals" into generic extremal pole | — | — | F7 |
| Davies locus | (transition, not role boundary) | finite for `g_F(u=0)` (Test 3 numeric, per [A]); GTD order 2 per paper-level [C] | finite | — | S0-adjacent; [C] S2 |

**[KN_SUPPORT-T4] The parity-fixed normal-form lemma (Test 10, "Will's m(m+5)").** Verbatim [B]:

```
For `ds² = B x² dx² + x⁻² Σ_{α=1..m} A_α dy_α²` (`B>0`, `A_α>0`), a first-principles Ricci
computation gives **exactly**

R = − m(m+5)/B · x⁻⁴,     independent of all transverse amplitudes A_α.
```

with verbatim qualifications:

```
Verified symbolically for `m=1,2,3` → `R = −6, −14, −24` times `x⁻⁴/B` (`lead7_test10`, clean
×2). The split `m(m+5) = 6m + m(m−1)` is *radial focusing* + *transverse fibre shear*; the
amplitudes drop out because they only rescale a flat fibre (warp curvature sees only `w'/w`,
`w''/w` with `w ∝ r^{−1/2}` after `r = √B x²/2`). **Asymptotic corollary:** with `y`-dependent
`B(y), A_α(y)` and even subleading terms, the leading Laurent coefficient is `−m(m+5)/B(y)`.
For a 3D state space (KN) `m=2`, giving `14` — so `C_Ω = −14/B_J`, `C_Φ = −14/B_Q` are
inevitable, not symbolic coincidences.
```

**[KN_SUPPORT-F4] KN reflection-face application (Test 6) — transverse poles essential.** Verbatim [B]:

```
Near a reflection face, even in the small coordinate `x`, with the collapsing native
component `g_x = B(y,z)·x² + O(x⁴)` and the two transverse components diverging as `x⁻²`,
`g_y = A x⁻² + O(1)`, `g_z = C x⁻² + O(1)`:

R = −14 / B(y,z) · x⁻⁴ + O(x⁻²),

depending only on `B`. **The transverse `x⁻²` poles are essential** — with *finite*
transverse components the identity is false (`B x² dx² + dy² + dz²` is flat, `R=0`; an
earlier draft here mis-stated the transverse components as finite). The real KN reflection
faces do carry the transverse `x⁻²` poles (`G_S ~ A/J²` on `Ω=0`, etc.), so the lemma
applies, and each reflection coefficient is `−14` over the collapsing component's leading
coefficient `B`.
```

**[KN_SUPPORT-F5] Exact `C_Ω` (Ω=0, `R ~ C_Ω(S,Q)/J⁴`).** Verbatim [B]:

```
C_Ω(S,Q) = −3584·Q²·S⁵·π³·(πQ² − S)²
         / [ (π²Q⁴ + 16π²Q²S² − 2πQ²S + S²)
           · (π²Q⁴ + 16π²Q²S² − 2πQ²S + 16πS³ + S²)² ].
```

**[KN_SUPPORT-F6] Exact `C_Φ` (Φ_e=0, `R ~ C_Φ(S,J)/Q⁴`).** Verbatim [B]:

```
C_Φ(S,J) = −14336·J²·S⁵·π⁵·(2πJ − S)²·(2πJ + S)²·(4π²J² + S²)
         / [ (16π⁴J⁴ + 64π⁴J²S² − 8π²J²S² + S⁴)
           · (16π⁴J⁴ + 64π³J²S³ + 64π⁴J²S² − 8π²J²S² + 16πS⁵ + S⁴)² ].
```

Both verbatim glossed as: `Both are −14/B with B the closed-form collapsing-component coefficient
(C_Ω = −14/B_J, C_Φ = −14/B_Q; see the certificate for B_J, B_Q). Verified against direct
high-precision curvature (Richardson) to ~20 digits.` (Note: `3584 = 14·256`, `14336 = 14·1024` —
consistent with the `−14/B` reading.)

**[KN_SUPPORT-F7] Corner degeneration of the reflection coefficients.** Verbatim [B]:

```
`C_Ω` carries the factor `(πQ² − S)²`, which vanishes exactly on `Ω=0 ∩ extremal`
(`S_ext = πQ²` at `J=0`); `C_Φ` carries `(2πJ − S)²`, vanishing on `Φ_e=0 ∩ extremal`
(`S_ext = 2πJ` at `Q=0`). The coefficients degenerate precisely where two role divisors
meet — the reflection-face pole "heals" into the generic extremal pole at the corner.
(The `(2πJ + S)²` factor in `C_Φ` is the `J→−J` reflection image, always present.)
```

**[KN_SUPPORT-F8] Extremal coefficient structural identity + `A₂` (Test 7).** Verbatim [B]:

```
C_ext = (1/A₂)·(P₁/P₀ + R₁/R₀) = (1/A₂)·∂_S ln(g_JJ·g_QQ)|_{S_ext},
```

```
A₂ = (4U + U_J² + U_Q²)²/(4U) · (1/U_J² + 1/U_Q²)   at extremal.
```

with `P₀,P₁ = g_JJ, ∂_S g_JJ` and `R₀,R₁ = g_QQ, ∂_S g_QQ` at extremal; the odd order 3 comes from
the linear-`δ` terms `P₁,R₁`; only `g_SS ~ A₂δ²` collapses (`M=√U` smooth in `(S,J,Q)`).

**[KN_SUPPORT-F9] Rationality + extremal denominator factorization.** Verbatim [B]:

```
den ∝ Q²π·(3Q²π+S)·(Q⁴π+Q²S−Q²π+S)·(Q⁴π²+4Q²S²π²−2Q²Sπ+S²)
      ·(Q⁴π²+Q²Sπ−Q²π²+2S²+Sπ)³·(Q¹⁰π³+Q⁸Sπ²−9Q⁶S²π³+3Q⁴S³π²+5Q²S⁴π+S⁵),
```

with verbatim context: the couplings `Λ = 2M(U_ii U_a − U_i U_ia)/U_i³` are *rational* in
`(S,J,Q,π)`; on the extremal surface `J²=(S²−π²Q⁴)/(4π²)` the whole coefficient is a rational
function of `(S,Q,π)`; numerator `N_ext` has degree 14 in `S`, 28 in `Q`. Sample values, verbatim:

```
C_ext(20,1) = −0.0660176096,  C_ext(30,1) = −0.0727822594,  C_ext(20,2) = −0.000549074077.
```

**[KN_SUPPORT-F10] Metric normalization — the graph "1+".** Verbatim [B]:

```
The DBP chart norm is `q_i = 1+|∇f_i|² = 1+(4U+U_a²+U_b²)/U_i²` (the n=2 norm `q0=1+a²+b²`,
`recert_gtd_dbp_n2.py`), so `G_i = q_i²·U_i⁶/(4U)·Σ(1/D²) = (U_i²+4U+U_a²+U_b²)²·U_i²/(4U)·Σ(1/D²)`.
```

Verbatim consequences: the "1+" is **essential** — graph-norm metric reproduces banked `C_ext`
values EXACTLY; dropping it to `|∇f|²` gives `−0.0656…, −0.0727…, −0.0002345…`; the "1+" matters
only in finite *transverse* channels (on a collapsing channel `U_i→0` makes `q_i→∞`, so `A₂`,
`C_Ω`, `C_Φ` are normalization-independent; `B_J` identical to 10+ digits either way).
`lead7_test8_extremal_gate_replacement.py` dropped the "1+" and is **refuted as the LEAD-7
certificate** (kept only as the record of the mis-step).

**[KN_SUPPORT-T5] The `N_ext` gate — CLOSED (Test 8, coefficient positivity).** Verbatim [B]
(the four-step argument):

```
1. *Sign reduction:* since `A₂>0`, `g_JJ|ext>0`, `g_QQ|ext>0`,
   `sign(C_ext) = sign(∂_S log(g_JJ g_QQ))|_ext =: sign(L_ext)` — the gate is exactly
   *"`g_JJ·g_QQ` is strictly decreasing in `S` at the extremal surface"* (drops the `A₂`
   division and the huge numerator).
2. *Edge parametrisation:* write `q=Q²>0`, `t=S/(πQ²)>1`; then `L_ext = −P/D` for polynomials
   `P,D` in `(q,t,π)`.
3. *Coefficient positivity:* after extracting positive monomials in `π,q,t` and substituting
   `t=1+r` (`r>0`), `π²=9+b` (`b>0`, from `π>3`), each residual factor is a nonzero polynomial
   in the positive variables `q,r,b` with nonnegative coefficients, hence positive. `D` factors
   into **nine** such factors. `P` is quadratic in `q`, `P=A q²+B q+C`; `B,C` are
   coefficient-positive, and (after removing a positive monomial) `A=C₀·π²t²·(π²F+G)` with
   `F(t)=(t−1)·t³(t+3)³·H̃(t)`, `H̃=2t⁵+5t⁴−15t³−7t²+15t+8` of degree 5 and positive on `[1,∞)`
   (Sturm), so `F>0` for `t>1`; a second Sturm count gives `9F+G>0` on `[1,∞)`. Since `π²>9`
   and `F>0`, `π²F+G=(π²−9)F+(9F+G)>0`, so `A>0`. Therefore `P>0`, `D>0`, `L_ext=−P/D<0`.
```

Status verbatim: `C_ext<0 at *every* open point of the extremal edge (not merely on a dense grid).
… the extremal pole has exact order 3 throughout, completing the fully symbolic retrodiction.`

**[KN_SUPPORT-T6] Schwarzschild double-reflection corner (Test 9).** Verbatim [B]:

```
- **Metric corner limits (closed form, graph-norm),** `N₀(s)=s/π+1/(16π²)`:
  `ε⁶ G_S → N₀²s⁵/[π(s+8πρ²)²] = (16πs+1)²s⁵/[256π⁵(s+8πρ²)²]`, `G_J → N₀²πρ²/s`,
  `G_Q → N₀²s/(4πρ²)`. `G_S` collapses as `ε⁶`; `G_J,G_Q` are ε-independent, scale `ρ^{±2}`,
  product `G_JG_Q→N₀⁴/4` ρ-independent. The schematic `s⁷/[π³(s+8πρ²)²]` drops the graph-norm
  `U_S²=1/(16π²)` term; exact/schematic `= (1+1/(16πs))²` (≈1.04 at s=1, s-dependent).
- **Balanced radial order is exactly 2** (not 4, not 6): `ε²R → R₀(s,ρ)` finite, **negative**
  (`R₀(1,1)=−1801.25`, `R₀(2,1)=−263.64`). The `ε⁻⁶` metric collapse loses four orders to
  inverse-metric contraction + derivative cancellation.
- **Newton wedge:** along `J=ρε^a`, `R ~ ε^{−m(a)}` with `m(a)=max(4a−2, 4−2a)` — vertex
  `(1,2)`, edges `4−2a` (a≤1, Φ side, `m(0)=4`) and `4a−2` (a≥1, Ω side). **Minimum m=2 on the
  balanced diagonal:** the corner is the *mildest* point of the whole boundary.
- **Boundary links (exact residues of `C_Ω,C_Φ`):** `κ_Ω(s)=lim_{Q→0}C_Ω/Q²=−3584π³s/(16πs+1)²`,
  `κ_Φ(s)=lim_{J→0}C_Φ/J²=−14336π⁵/[s(16πs+1)²]`, with `ρ⁴R₀→κ_Ω` (ρ→0), `R₀/ρ²→κ_Φ` (ρ→∞).
- **Genuine mixed term:** `R₀` is *not* the two-face sum — `R₀(1,1)=−1801.25` vs superposition
  `κ_Ω+κ_Φ=−1711.56`, an excess `M=−89.70` (the cross term in `G_S`'s mixed denominator that
  neither single face resolves). So state `R₀<0`, but not as `−κ_Ω/ρ⁴−κ_Φρ²`.
```

(Extractor spot-check: `lim_{Q→0} C_Ω/Q²` computed from F5 gives `−3584π³S/(16πS+1)²` and
`lim_{J→0} C_Φ/J²` from F6 gives `−14336π⁵/[S(16πS+1)²]` — both match κ_Ω, κ_Φ exactly.)

### 2.3 From [C] — the earlier (n=2, conjectural) valuation brief

**[KN_SUPPORT-M1] TERMINOLOGY MAP — explicit reconciliations from the provenance header
(old term -> new term; these OVERRIDE the body).** Verbatim [C] header:

```
> (1) The body's "RC-5" Stage A is the ALREADY-ASSIGNED RC-5 (n=2 GTD/DBP spine —
>     see reports/RC5_SCOPING.md, incl. its DO-NOT-CITE flags); the valuation
>     campaign proper is named LEAD2_VALUATION_I.
> (2) The valuation ledger must carry the frame split: pole ORDERS are invariant
>     under the S = 2*pi*sigma rescale (exact-Q structure tier); leading
>     COEFFICIENTS are Q(pi)-frame quantities (retrodiction tier). Without this
>     split, kill K-C9 fires on frame artifacts.
> (3) "Lead C" maps to LEAD-2 in this register — no second numbering scheme.
> (4) Toy-model scope, hand-checked at review: generic order 2m+2-l is correct;
>     the reflection-fixed case is NOT derivable from the diagonal toy (it predicts
>     2m, not the observed 4) — the exact Brioschi valuation ledger is obligatory
>     there, exactly as the body itself warns in section 6.2.
> (5) The truncated-Taylor-jets-over-Q machinery demonstrated in the RC-5 scoping
>     spike IS the Stage-B "valuation ledger engine" — Laurent orders without full
>     CAS curvature.
> (6) The `fileciteturn...` markers below are artifacts of the originating tool.
```

Condensed old->new table (header-explicit entries marked EXPLICIT; cross-file correspondences
marked INFERRED — inferred entries are the extractor's consolidation reading, not verbatim source):

| old term ([C] body / n=2 paper) | new term (current register) | status |
|---|---|---|
| "Lead C" | LEAD-2 | EXPLICIT (header 3) |
| body's "RC-5" Stage A campaign name | RC-5 = already-assigned n=2 GTD/DBP spine (`reports/RC5_SCOPING.md`, has DO-NOT-CITE flags) | EXPLICIT (header 1) |
| the valuation campaign proper | `LEAD2_VALUATION_I` | EXPLICIT (header 1) |
| Stage-B "valuation ledger engine" | the truncated-Taylor-jets-over-Q machinery from the RC-5 scoping spike | EXPLICIT (header 5) |
| single-tier pole data | frame split: pole ORDERS = exact-Q structure tier (invariant under `S = 2πσ` rescale); leading COEFFICIENTS = Q(π)-frame retrodiction tier | EXPLICIT (header 2) |
| `g_DBP = −h⁻¹`, `h = Σ κ_{c,i} dE_i⊗dE_i` (n=2) | `g_F(u=0)` mass-charge inverse-channel metric (n=3), `g_{ii} = q_i²·Σ_j 1/Λ_{i,{M,j}}²` | INFERRED ([C] §3.5 vs [A] Statement) |
| `q₀ = 1 + a² + b²` (n=2 chart norm) | `q_i = 1+|∇f_i|² = 1+(4U+U_a²+U_b²)/U_i²` (graph norm, "1+" essential) | EXPLICIT lineage in [B] ("the n=2 norm q0=1+a²+b², recert_gtd_dbp_n2.py") |
| role boundary / role-singular stratum | role divisor (`{J=0} ∪ {Q=0} ∪ {U_S=0}` = `Ω=0 ∪ Φ_e=0 ∪ T=0`) | INFERRED ([C] §3.2 vs [A]) |
| `ROLE_CHART_UNAVAILABLE` (a=0 or b=0) | native pole divisor `U_i=0` of the uniform coupling formula | INFERRED ([C] §3.2 vs [A] step 1) |
| `CHANNEL_ISOTROPIC` (`Λ_ρ = 0`) | LEAD-2 channel-isotropy strata = interior zeros of charge-charge couplings `Λ_{i,{j,k}}` (excluded by u=0) | EXPLICIT in [A] ("these are the LEAD-2 channel-isotropy strata") |
| `C_sch` (n=2 Kerr Schwarzschild coefficient, `J=0`) | n=3: split into `C_Ω` (Ω=0 face) and `C_Φ` (Φ_e=0 face); "Schwarzschild" now names the double-reflection CORNER `J=Q=0` (order 2) | INFERRED ([A] "C_ext, C_sch" vs [B]) |
| reflection-fixed boundary, order 4 "symmetry correction" | `−m(m+5)/B` parity-fixed normal form at `m=2` (`R = −14/B·x⁻⁴`) | INFERRED ([C] §6.2/Thm 4 vs [B] Test 10) |
| generic simple role boundary, order 3 | extremal edge `T=0`, generic Laurent δ⁻³, `C_ext = A₂⁻¹∂_S ln(g_JJ g_QQ)|_ext` | INFERRED ([C] §2.4 vs [B] Test 7) |
| transition locus (Davies/spinodal): GTD order 2, DBP finite | Davies finite for `g_F(u=0)` (Test 3, numeric) | INFERRED ([C] §4 vs [A]) |

**[KN_SUPPORT-F12] Valuation definition.** Verbatim [C] §3.1:

```
f(t) = t^k u(t),   u(0) ≠ 0,
v_t(f) = k.
pole(f) = max(0, -v_t(f)).
```

**[KN_SUPPORT-F13] n=2 output-role channel formulas (paper-level seed).** Verbatim [C] §3.4–3.5:

```
Λ_P = B
Λ_D = (A b - a B) / a
Λ_S = (C a - b B) / b
κ_{c,i} = -Λ_i^2 / q_0^2
q_0 = 1 + a^2 + b^2
```

```
h = Σ_i κ_{c,i} dE_i ⊗ dE_i
g_DBP = -h^{-1}
```

with jet convention `(a,b,A,B,C) = (f_D, f_S, f_DD, f_DS, f_SS)` for local graph `P = f(D,S)`
([C] §3.2), and [C]'s own caveat: `This must be re-certified before being used as load-bearing
proof currency.`

**[KN_SUPPORT-F14] Diagonal toy-model order derivation (hand-checked, toy scope only).**
Verbatim [C] §6.1:

```
ds² = E(t,y) dt² + G(t,y) dy²
K = -1/(2√(E G)) [ ∂_t( (∂_t G)/√(E G) ) + ∂_y( (∂_y E)/√(E G) ) ]
E(t,y) ~ e₂(y) t^(2m),  G(t,y) ~ g₀(y) + g_ℓ(y) t^ℓ + ...
K ~ t^(ℓ - 2 - 2m)
PoleOrder = 2m + 2 - ℓ.
```

with `ℓ=1 ⟹ PoleOrder = 2m+1`; `m=1 ⟹ 3`. Header override: valid for the GENERIC case only;
the diagonal toy predicts `2m` (wrong) for the reflection-fixed case.

**[KN_SUPPORT-S1] Candidate theorem v0 + conjectural higher-m formulas.** Verbatim [C] §2.3–2.4
(key fragments):

```
v_t(y) = m > 0
Λ_i(t) ~ t^{-m} · unit(t)
κ_{c,i}(t) = -Λ_i(t)^2 / q_0(t)^2
```

```
generic simple role boundary:          pole order 3
reflection-fixed simple role boundary: pole order 4
transition locus (Davies/spinodal):    GTD order 2, DBP finite
```

```
generic:            PoleOrder ≈ 2m + 1
reflection-fixed:   PoleOrder ≈ 2m + 2
```

[C]'s own label, verbatim: `These higher-`m` formulas are **not proven** and should be treated as
conjectural until exact families are generated.`

**[KN_SUPPORT-S2] Seed evidence table (paper-level, uncertified).** Verbatim [C] §4:

```
| Surface | Role boundary / transition | Known/paper-level behavior | Proposed stratum type |
|---|---|---:|---|
| Kerr | Extremal `T=M_S=0`, `S=2πJ` | `R[g_DBP] ~ (S-2πJ)^(-3)` | generic simple role boundary |
| Kerr | Schwarzschild `Ω=M_J=0`, `J=0` | `R[g_DBP] ~ J^(-4)` | reflection-fixed role boundary |
| RN | Extremal | order 3 | generic simple role boundary |
| RN | `Q=0` | order 4 | reflection-fixed role boundary |
| vdW | `P=0` boundary | order 3 | generic simple role boundary |
| Kerr/RN | Davies | GTD order 2, DBP finite | transition, not role-boundary |
| vdW | spinodal | GTD order 2, DBP finite | transition, not role-boundary |
```

**[KN_SUPPORT-S3] Expected theorem deliverable (target shape).** Verbatim [C] §11:

```
Theorem (Role-Singularity Valuation Law, n=2 seed).

Let F(D,S,P)=0 be a regular 3-role constraint surface away from the role
boundary, with channel-inverse metric g_DBP=-h^{-1}. Let γ(t) cross a simple
role boundary at t=0 where one output derivative vanishes to order 1.

If the boundary is not fixed by a role-reflection symmetry and the transverse
channel has nonzero first variation, then R[g_DBP] has pole order 3.

If the boundary is fixed by an involutive role-reflection symmetry forcing the
cross-coupling derivative to vanish, and the native channel collapse is simple,
then R[g_DBP] has pole order 4.

In both cases, the leading coefficient is determined by the valuation ledger of
the native role channel and the first non-cancelling Brioschi numerator term.
Transition loci such as Davies/spinodal are not role-boundary strata and are
not detected by this pole law.
```

**[KN_SUPPORT-F15] Keystone channel-tuple convention guard.** Verbatim [C] §13:

```
(κ_c, κ_s, κ_int) = (-1/49, +1/49, -3/49)
K_G = -3/49
κ_c + κ_s = 0
κ_int survives
```

with the rule, verbatim: `**Never quote a channel tuple without slot labels.**` and the hazard
record ([C] §1 item 7): stdout once printed `(-1/49,-3/49,+1/49)` unlabelled — slot order
`(κ_c, κ_int, κ_s)` — creating a false contradiction. `Unlabelled channels = (...) is banned.`

**[KN_SUPPORT-K1] Kill conditions K-C1..K-C9.** Verbatim [C] §10:

```
K-C1: A re-derived Kerr DBP curvature does not have order 3 at extremal or order 4 at Schwarzschild.
K-C2: A re-derived RN or vdW surface contradicts the claimed 3/4 order transfer.
K-C3: A generic simple role boundary with v(a)=1 or v(b)=1 yields a pole order other than 3.
K-C4: A reflection-fixed simple role boundary yields no order lift, or a non-reflection boundary
      yields order 4 without an additional mechanism.
K-C5: The proposed exponent formula depends only on Specht-module dimension and fails on a
      certified counterexample.
K-C6: Any proof uses floats/tolerances on a verdict path.
K-C7: Any channel tuple is emitted or compared without slot labels.
K-C8: The theorem cannot distinguish transition loci from role-boundary loci.
K-C9: Brioschi numerator valuation cannot be made invariant under allowed coordinate changes /
      chart choices.
```

(Line-wrapped here for width; content verbatim. Also [C] §5, verbatim anti-target:
`pole order = dimension of lost Specht module` is `too simple and likely false`; better:
`Pole exponent = valuation ledger + symmetry correction. Representation theory labels which
component enters the ledger.`)

---

## 3. CONVENTIONS

- **KN fundamental relation:** `M² = U(S,J,Q)`, `U = S/(4π) + πJ²/S + Q²/2 + πQ⁴/(4S)`. This is
  the **π-frame** (Q(π)-frame); per [C] header (2), pole orders are invariant under `S = 2πσ`
  rescale but leading coefficients (`C_Ω`, `C_Φ`, `C_ext`) are π-frame quantities.
- **Domain:** everything n=3 lives on `W₊ = {S,J,Q>0, U_S>0} = {S,J,Q>0, S² > π²(4J²+Q⁴)}` —
  NOT on `{disc>0}` (see C1). `U_S>0 ⇔ T>0` (outer horizon).
- **Subscript convention:** `U_i = ∂U/∂E_i`, `U_ij` second partials, `(E_1,E_2,E_3)=(S,J,Q)`;
  in [B]'s rationality passage `a,b` range over the two non-native charges (`U_a, U_b`).
- **Coupling indexing:** `Λ_{i,{M,j}}` = mixed partial `∂²E_i/∂M∂E_j` of the chart solving for
  `E_i`; "mass-charge" = pairs `{M, E_j}`; "charge-charge" = pairs `{E_j, E_k}` (excluded at u=0).
- **Divisor <-> intensive-variable dictionary:** `J=0 ⇔ Ω=0`; `Q=0 ⇔ Φ_e=0`; `U_S=0 ⇔ T=0`
  (extremal); `U_J=0 ⇔ Ω=0`, `U_Q=0 ⇔ Φ_e=0` as native poles.
- **Extremal surface:** `S_ext = π√(4J²+Q⁴)`; equivalently `J² = (S²−π²Q⁴)/(4π²)`; expansion
  coordinate `δ = S − S_ext`. Corners: `S_ext = πQ²` at `J=0`; `S_ext = 2πJ` at `Q=0`.
- **Vieta:** `S_± = π(2M²−Q² ± 2√disc)`, `S₊S₋ = π²(4J²+Q⁴)`, `S₊−S₋ = 4π√disc`.
- **Metric normalization (load-bearing):** graph norm `q_i = 1 + |∇f_i|²` — the "1+" is part of
  the certified metric; diagonal entries `G_i = q_i²·U_i⁶/(4U)·Σ(1/D²)`. Coefficients `C_ext`
  depend on the "1+"; `A₂, C_Ω, C_Φ, B_J` do not (collapsing channels wash it out).
- **Curvature harness:** exact-partial 3D Ricci (validated flat ℝ³ → 0, 3-sphere → 6/a²);
  scalar-curvature sign convention implied by that calibration (sphere positive).
- **Normal-form tuple order:** in `ds² = B x² dx² + x⁻² Σ A_α dy_α²`, `x` is always the collapsing
  (small) coordinate, `B` the collapsing component's leading coefficient, `A_α` transverse.
- **Corner approach parametrization:** `Q = ε`, `J = ρ ε^a`; `a` is the wedge slope, `ρ` the
  balanced-diagonal modulus; `N₀(s) = s/π + 1/(16π²)`.
- **Valuation ([C]):** `v_t(f) = k` for `f = t^k u(t)`, `u(0)≠0`; `pole(f) = max(0, −v_t(f))`;
  componentwise for tensors.
- **n=2 jet tuple order ([C]):** `(a,b,A,B,C) = (f_D, f_S, f_DD, f_DS, f_SS)` for `P = f(D,S)`.
- **Channel tuple slot labels ([C], mandatory):** certified keystone `(κ_c, κ_s, κ_int) =
  (−1/49, +1/49, −3/49)`; some internal code uses `(κ_c, κ_int, κ_s)`; unlabelled tuples banned
  (kill K-C7).
- **Trust convention ([C] header):** external brief formulas re-derive before load-bearing use;
  `fileciteturn...` markers are dead artifacts of the originating tool, not repo references.

---

## 4. UNIQUE MATERIAL (exists ONLY in these three files — must not be lost)

1. **The six-numerator factorization table** with per-coupling zero loci (F2) and the
   nonnegative-coefficient-bracket positivity mechanism (L1) — the entire proof body of the
   interior-cleanliness theorem lives only in [A].
2. **The inner-branch counterexample with exact coordinates** `(S,J,Q) = (π√3/2, 1/4, 1)`,
   `M² = 1/2 + 1/√3`, `disc = 1/48`, `U_S = −1/(6π)`, `N_{J,S} = (S²+4π²J²−π²Q⁴)/(2S³) = 0` (C1) —
   the only recorded witness that `{disc>0}` is the wrong domain and `W₊` is forced.
3. **The corrected role of the extremal divisor** (L2): `T=0` is a native POLE (through `U_S³`),
   not a generic numerator zero; numerator zeros touch it only at codim-2 corners.
4. **The charge-charge interior-zero witness** `Λ_{Q,{S,J}}=0` at `(M,J,Q)=(2,0.826,1.699)` and
   the structural u=0 selection argument (C2).
5. **The exact closed-form coefficients** `C_Ω(S,Q)` and `C_Φ(S,J)` (F5, F6) with their corner
   factors `(πQ²−S)²`, `(2πJ−S)²` and the reflection-image factor `(2πJ+S)²` (F7).
6. **The `−m(m+5)/B` parity-fixed normal form** with the amplitude-independence statement, the
   `6m + m(m−1)` focusing/shear split, the `w ∝ r^{−1/2}` warp mechanism, and the essentiality of
   the transverse `x⁻²` poles (T4, F4) — including the record that finite transverse components
   make the identity FALSE.
7. **The extremal structural identity** `C_ext = A₂⁻¹·∂_S ln(g_JJ g_QQ)|_ext`, the closed form of
   `A₂`, the rationality argument, the extremal denominator factorization (deg-14/28 `N_ext`),
   and the three banked sample values (F8, F9, F11-in-F9).
8. **The graph-norm "1+" discriminator** (F10): exact numeric fingerprints distinguishing the
   correct metric (−0.0660176096, …) from the refuted one (−0.0656…, −0.0002345…), plus the
   certificate genealogy (`_graphnorm` valid; `_replacement` refuted; `_extremal_gate` superseded).
9. **The full `N_ext` gate-closure argument** (T5): the sign reduction to monotonicity of
   `g_JJ·g_QQ`, the `(q,t) = (Q², S/(πQ²))` edge parametrization, the `t=1+r`, `π²=9+b`
   substitutions, the nine-factor `D`, and the explicit degree-5 Sturm polynomial
   `H̃ = 2t⁵+5t⁴−15t³−7t²+15t+8`.
10. **The Schwarzschild corner package** (T6): closed-form metric limits with `N₀(s)`, the exact
    corner order 2, the Newton wedge `m(a) = max(4a−2, 4−2a)`, the exact residues
    `κ_Ω(s) = −3584π³s/(16πs+1)²`, `κ_Φ(s) = −14336π⁵/[s(16πs+1)²]`, and the genuine mixed term
    (`R₀(1,1) = −1801.25` vs `κ_Ω+κ_Φ = −1711.56`, excess `−89.70`).
11. **The provenance-header reconciliation map** ([C] header items 1–6): Lead C -> LEAD-2, RC-5
    disambiguation, LEAD2_VALUATION_I naming, the ORDERS/COEFFICIENTS frame split, the
    jets-over-Q = Stage-B ledger-engine identification, and the hand-checked verdict that the
    diagonal toy gives `2m+2−ℓ` generically but predicts `2m` (wrongly) at reflection-fixed loci.
12. **The n=2 conjectural scaffold** unique to [C]: higher-`m` formulas `2m+1` / `2m+2`
    (labelled unproven), the five-theorem proof architecture with per-theorem kill conditions,
    kill list K-C1..K-C9, the Specht-dimension anti-target, the keystone tuple-label case law,
    and the Stage B valuation-ledger schema (`v(a) … v(R[g_DBP])` record fields).
13. **Certificate name registry** embedded in [A]/[B]: `lead7_test4_masscharge_zeros.py` (T4-a..e),
    `lead7_test5_pole_orders_n3.py`, `lead7_test6_pole_coeffs_n3.py`,
    `lead7_test7_extremal_coeff_n3.py` (T7-a, T7-e), `lead7_test8_extremal_gate_graphnorm.py`
    (valid) / `_replacement` (refuted) / `_extremal_gate` (superseded), `lead7_test9_corner.py`,
    `lead7_test10_reflection_lemma.py`, `recert_gtd_dbp_n2.py`.

---

## 5. RED FLAGS

- **R1 — Same-day status contradiction between [A] and [B] (both dated 2026-07-07).** [A]'s
  closing section says `The orders 3/4/4 are numeric` and lists closed-form coefficients as
  `Remaining for full certification`; [B] declares the orders **symbolic**, all three coefficients
  **exact closed form**, and the retrodiction `fully symbolic — no fitted exponents survive`.
  [A]'s "what remains" section is stale relative to [B]. Consolidation must cite [B] for status
  and keep [A] only for the theorem + factorization + counterexample (tagged S0 above).
- **R2 — Numeric-looking values on load-bearing narrative paths.** (a) The charge-charge witness
  `(M,J,Q) = (2, 0.826, 1.699)` (C2) is quoted to 3 decimals, sourced to numeric Test 3 — fine as
  motivation, but it is not an exact-Q point and must not be promoted to certificate currency
  (would trip [C]'s K-C6 analogue). (b) Corner numbers `R₀(1,1)=−1801.25`, `−263.64`, excess
  `−89.70` are 2-decimal numerics inside a report whose κ residues are claimed exact; the mixed
  term `M=−89.70` has no closed form recorded anywhere.
- **R3 — Admitted prior errors preserved in-line in [B].** (a) `an earlier draft here mis-stated
  the transverse components as finite` (reflection normal form). (b)
  `lead7_test8_extremal_gate_replacement.py` is **refuted** (dropped the "1+") and
  `_extremal_gate.py` **superseded** — three near-identically named Test-8 scripts exist with
  only one valid. Any consolidation citing "Test 8" must name `_graphnorm` explicitly.
- **R4 — [C] is wholly conjectural but theorem-formatted.** It is an external ChatGPT brief,
  `NOT a certificate`, containing paper-level claims (n=2 orders 3/4, RN/vdW transfer, GTD
  order 2, `g_DBP=−h⁻¹` definition) that per its own header and ADMISSIONS require re-derivation.
  Its "Candidate theorem statement, v0" and §11 deliverable text read like theorems; none is
  proven in [C]. Do not lift any [C] formula into the consolidated theorem without a current
  certificate.
- **R5 — Broken/dead references in [C].** All `fileciteturn22file*` markers are unresolvable
  tool artifacts (header item 6 flags them); the body also cites `gtd vs dbp.pdf`,
  `REVIEW_Exact_Role_Channel_Geometry.md`, `RC1_transport_law_stdout.txt`, `LEADS.md`,
  `ADMISSIONS.md` without paths, and its Stage-A campaign name "RC-5" collides with the
  already-assigned RC-5 (header item 1 overrides).
- **R6 — Toy-model/reflection tension inside [C].** Body §2.4 proposes reflection-fixed
  `PoleOrder ≈ 2m+2`, but the header's hand-check says the diagonal toy predicts `2m` for the
  reflection case (both agree it is not derivable from the toy). [B]'s Test 10 (`−m(m+5)/B` with
  ONE collapsing coordinate against an m-flat fibre) is the resolution for the KN faces, but note
  its `m` is the FIBRE dimension, not [C]'s valuation `m = v_t(y)` — same letter, different
  meaning. Consolidation must rename one of them.
- **R7 — Davies finiteness is asserted, never proved, in this trio.** [A] cites `Test 3 …
  finite on Davies` (numeric scan) and [C] carries it only at paper level; no symbolic Davies
  statement exists in these files.
- **R8 — `B_J, B_Q` closed forms not recorded here.** [B] says `see the certificate for B_J, B_Q`;
  the collapsing-component coefficients behind `C_Ω=−14/B_J`, `C_Φ=−14/B_Q` live only in
  `lead7_test6_pole_coeffs_n3.py`. If certificates are pruned, those closed forms are lost.
- **R9 — Minor internal-consistency checks passed (for the record):** F2 row 1 re-derived by hand;
  row 3 matches C1's `N_{J,S}` expression; C1's four exact values re-verified; κ_Ω, κ_Φ re-derived
  as residues of F5/F6; `3584 = 14·256`, `14336 = 14·1024` consistent with `−14/B`. No arithmetic
  discrepancies found in the quoted formulas.
