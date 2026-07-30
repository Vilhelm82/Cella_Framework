# EXTRACTION NOTE — four_role_frontier
**Source:** `research/campaigns/ACTIVE_RECHART_CURVATURE_VALUATIONS/01_SOURCES_CORE/paper_I_active_rechart/dbp_four_role_calc_log_v8.md` (1,065 lines, read in full 2026-07-30)
**Focus:** the all-n role-pair carrier scaffold (CALC-01..36): what is claimed at n+1 = 4 roles and for general n; computed vs conjectured formulas; higher-order (order-axis r) findings; characteristic-axis findings; candidate formal lemmas.
**Tags:** `[computed]` = exact-ℚ/exact-ℤ CAS verification recorded in the log for specific instances; `[claimed]` = asserted proven in prose (rep theory / hand derivation), proof sketch or citation in-log but no independent artifact in this file; `[speculative]` = the log's own `[conjecture]` / `[interpretation]` / `[open]` tiers.

---

## 1. SOURCE LIST

| Source | Role (one line) |
|---|---|
| `dbp_four_role_calc_log_v8.md` (this file) | Master running calc log, CALC-01..36 + standing conclusions + Frontier map F1–F8; the only complete record of the all-n role-pair theorem chain and its corrections. |
| `role_channel_anisotropy.tex` (+ mid-session PDF), `/mnt/project/` | Definition source: §6 channel reduction, §7.3 faithfulness, §8 higher-order conjecture, A_c, Prop 1. NOT in this log; log explicitly states "Definitions are NOT in this file." |
| `dbp_orbit_calculus.pdf`, `/mnt/project/` | Definition source: Active Role-Jet, κ_{r;p,q} bidegree tower (§6.2), gauge transport (§8), faithfulness corollary (§7.3). |
| `self_glue_monodromy.pdf`, `/mnt/project/` | Definition source: self-glue covers, monodromy S₃×S₃, D₄ keystone; the `/mnt/project` copy is flagged **corrupt zip** in CALC-36. |
| `imL_pair_module_theorem.md` (same directory as log, per header) | Self-contained proof note for CALC-14 (the central theorem). Referenced, contents not reproduced in log. |
| Scripts `step1_carrier.py`, `faithfulness.py`, `loss_location.py`, `resolvent_s3.py`, `n5_test.py`, `n6_test.py`, `ladder_faithfulness.py`, `prove_imL.py` | Phase-1 computation artifacts (CALC-01..14), stated to live "this directory". |
| Container-only scripts (CALC-15..36; e.g. `order_axis_v1.py`, `f1_screen.py`, `f1_realize.py`, `f1_mechanism.py`, `f1_lift.py`, `f1_threshold.py`, `t3_modular_*.py`, `trap_*.py`, `ladder.py`, `h2_walls.py`, `mono_galois.py`, `shear_*.py`, `aneqc_*.py`) | Computation artifacts in ephemeral container `/home/claude/`; log states container scripts reset between sessions — the log's embedded equations are the only re-creation route. |
| Session transcripts `2026-06-29-04-10-49-lloyd-dbp-role-pair-proof.txt`, `2026-06-29-02-02-48-lloyd-dbp-four-role-carrier.txt` | Full-detail transcripts of the proof session and the opening n=3→4 session. |
| Campaign H docs (`CHAR2_BOUNDARY_REPORT.md`, `RAW_CHART_ROLECHSPEC_REPORT.md`, `GAUGE_NORMAL_FORM_PROOF`, `SYMBOLIC_ROLECHSPEC_FORMULAS`, `INJECTIVITY_IDEAL_REPORT`, `EXCEPTIONAL_LOCUS_REPORT`) | Will's parallel n=3 characteristic-axis campaign (CL-H1..H10); audited in CALC-16/17; "uploaded", archival location not given. |
| `DBP_Curvature_Role_Reduction.md` | Referenced for lead L4 (§13.3) and as the place the §8 parity law is "PROVEN" (§4, "Lovelock parity"); location not given in log. |
| `evals/dbp_involution/` (second independent campaign, 102 records) | Cross-check campaign audited in CALC-20; independently reproduces CALC-19. |
| `codex_task_dbp_prime2_structure.md`, `codex_task_monodromy_aliasing_triple.md` | Hand-off task specs (T1/T2/T3 prime-2 probe; monodromy aliasing triple) with validated gates embedded. |

---

## 2. EXACT STATEMENTS

### 2.1 What exactly is claimed at n+1 = 4 roles (the four-role layer)

**[FOUR_ROLE_FRONTIER-T4]** n=4 faithfulness clinch (CALC-06) — `[computed]` (ranks exact-ℚ) + `[claimed]` (dimension argument):
```
dim(second jet) = 6.
carrier (A): R⁶ → R¹², rank 6 → FAITHFUL.
carrier (C): R⁶ → R⁴, rank 4 → NOT FAITHFUL. Codomain dim 4 < 6 ⇒ rank ≤ 4 everywhere
⇒ (C) is faithful nowhere (not merely on a degeneracy locus).
ker(J_C) is 2-dimensional; both kernel directions visible to (A) (J_A · dir nonzero in 11/12 components each).
```

**[FOUR_ROLE_FRONTIER-F6]** n=4 abstract 12-component module (CALC-03) — `[claimed]` (character orthogonality, "hand- and code-verified"):
```
ordered-pairs permutation character χ = (12, 2, 0, 0, 0) over classes (e, (12), (12)(34), (123), (1234))
12-dim module = trivial ⊕ 2·standard ⊕ (standard⊗sign) ⊕ (2,2)
multiplicities (1, 0, 2, 1, 1) for (triv, sign, std, std⊗sgn, 2dim). Dim check = 12.
anisotropy (non-trivial) dimension = 11.
n=3 comparison: 3-component module = triv ⊕ std(2-dim of S₃), exactly one nontrivial irrep.
```

**[FOUR_ROLE_FRONTIER-F7]** Concrete n=4 carrier instance (CALC-04) — `[computed]` (one surface):
Inputs: `F = Σ y_i² + Σ_{i<j} y_i y_j − 65` at `(1,2,3,4)`, gradient `(11,12,13,14)`.
```
(0,1) -8836/12006225   (0,2) -361/592900     (0,3) -6241/12006225
(1,0) -529/893025      (1,2) -361/893025     (1,3) -5041/14288400
(2,0) -27889/67076100  (2,1) -5776/16769025  (2,3) -4489/16769025
(3,0) -6241/19448100   (3,1) -5329/19448100  (3,2) -529/2160900
```
Isotypic norms: trivial, standard, std⊗sgn, twodim all nonzero; sign zero; Parseval ✓. Caveat in-log: squared carrier at asymmetric frame; std⊗sgn population is a quadratic shadow (superseded by CALC-08/09).

**[FOUR_ROLE_FRONTIER-F9]** Loss location at n=4 (CALC-08) — `[computed]`:
```
(C)_k = −(1/q²) Σ_pairs Λ²        (per-chart sum of squares of coupling numerators)
L: Hessian(R⁶) → numerators(R¹²) has rank 6 (injective)
Im(L) (realizable coupling numerators, 6-dim) = trivial ⊕ standard ⊕ (2,2)
(C) resolves triv ⊕ std (4 per-chart magnitudes)
THE LOSS sits entirely in the 2-dimensional (2,2) irrep; lost dimension = 2 = dim ker(J_C)
The (2,2) irrep factors through S₄/V₄ ≅ S₃.
```

**[FOUR_ROLE_FRONTIER-F10]** Minimal faithful carrier at n=4 (CALC-09) — `[computed]`:
```
minimal faithful carrier = 4 magnitudes + 2 shape (the (2,2) doublet) = 6 = dim(second jet)
augmented Jacobian rank 6 → FAITHFUL; the full 12 components of (A) are redundant.
```

**[FOUR_ROLE_FRONTIER-F11]** V₄ / resolvent-S₃ structure (CALC-10) — `[computed]` + `[claimed]` (quotient-vs-independent structural):
```
V₄ = {e, (01)(23), (02)(13), (03)(12)} = ker(S₄ → Sym(3 partitions)); quotient order 6 = |S₃|
permutation rep on the three 2+2 partitions: character (3,1,3,0,1) = triv ⊕ (2,2)
Galois bridge: x⁴ − x − 1 (Gal S₄) → resolvent cubic y³ + 4y − 1, irreducible,
discriminant −283 (non-square) → Gal = S₃ = S₄/V₄
```
Verdict: the resolvent S₃ is a new group (absent at n=3) but NOT independent — it is the role group's resolvent quotient; contrast with the independent monodromy-S₃ (S₃×S₃) of the self-glue paper.

**[FOUR_ROLE_FRONTIER-T19]** Finite two-state witness, n=4 (CALC-30) — `[computed]` (exact ℚ) + `[claimed]` (Q₀ positive-definiteness argument):
```
gauge-fixed slice, role-0 row = 0; columns (H11,H22,H33)(H12,H13,H23):
   H₀ =  ( 2, −1,  3)  ( 1, −2,  1)
   H  =  (−2, −2, −6)  ( 2, −1, −1)
(C)(H₀) = (C)(H) = (6, 33, 33, 54)     — all four charts, exact, equal
A(H₀) = (−1,2,−1, −1,−4,−4, 2,2,5, −5,−2,−5)
A(H)  = (−2,1,1, 4,1,4, 4,1,4, 5,5,2)
isotypic norms of A(H)−A(H₀): triv 147, std 153, (2,2) = 24, sgn = std⊗sgn = 0; Σ = 324 = ‖ΔA‖²
```
Structural companion (why the CALC-07 kernel shortcut had to fail):
```
On ker(J_C) through H₀: Q₀ = 5a² − 4ab + 2b²  (positive-definite, disc = −24);  Q₁=Q₂=Q₃ = 2(a−b)²
⇒ the only equal-magnitude point on the linear shape plane is H₀ itself; witness must curve off-plane.
```

### 2.2 The all-n role-pair carrier scaffold (the central theorem chain)

**[FOUR_ROLE_FRONTIER-T1]** THE CENTRAL THEOREM (CALC-14) — `[claimed]` proven for all n; load-bearing steps `[computed]` n=4..9:
```
Theorem. For all n ≥ 3, Im(L) ≅ M^(n−2,2) = ℂ[role-pairs] = triv ⊕ std ⊕ S^(n−2,2) as S_n-reps.
```
Proof steps as recorded:
```
Numerator  Λ_{k,{j,l}}(H) = −(H_{jl} − H_{jk} − H_{kl} + H_{kk})   on ambient H ∈ Sym²(ℝ^n); S_n-equivariant.
Step 1 [gauge].    ker L = G = {v⊗g + g⊗v}  (defining-function rescaling F → φF, shifting H by ∇φ⊗g + g⊗∇φ)
                   explicit construction: v_a = H_{a0} − ½H_{00};  rank L = dim Sym²(ℝ^n) − n = C(n,2)
                   (verified n=4..7)
Step 2 [quotient]. Im(L) ≅ Sym²(ℝ^n)/G ≅ Sym²(std), since Sym²(ℝ^n) = triv ⊕ std ⊕ Sym²(std)
                   and G is exactly Sym²(triv) ⊕ (triv⊗std)
Step 3 [character]. χ_{Sym²std}(g) = ½(χ_std(g)² + χ_std(g²)) = C(fix,2) + #2cycles = role-pair character
                   (verified n=4..9).  So Sym²(std) ≅ M^(n−2,2).  ∎
```

**[FOUR_ROLE_FRONTIER-T2]** Loss corollary (CALC-14, drawing on CALC-11/12/13) — `[claimed]` proven (given T1):
```
(C) (per-role coupling magnitude) spans the marginal triv ⊕ std; the loss = S^(n−2,2) for all n:
absent n=3 ((n−2,2)=(1,2) invalid → no shape; A_c whole story),
quotient (2,2) at n=4 (V₄ accident; factors through S₄/V₄),
faithful n≥5 with margin 2(n−3).
Loss dim = dim S^(n−2,2) = n(n−3)/2;   1 + (n−1) + n(n−3)/2 = n(n−1)/2 = dim(2nd jet) for all n.
```

**[FOUR_ROLE_FRONTIER-T3]** Faithfulness-margin law (CALC-13) — `[claimed]` proven rep theory; loss-identity part `[computed]` n=4..8:
```
χ_shape(g) = C(fix,2) + #2cycles − fix       (= χ_pair − χ_triv − χ_std, exact identity)
margin := dim − max_{g≠e} χ_shape(g)
n=4: kernel = V₄ (order 4), not faithful, margin 0
n≥5: kernel trivial, margin = 2(n−3) exactly
least-faithful element settles to a single transposition for n≥7 (χ_shape = (n−3)(n−4)/2)
```

**[FOUR_ROLE_FRONTIER-F16]** n=5 decisive data (CALC-11) — `[computed]`:
```
rank L = 10 (injective), all Q_k = 5; rank J_A = 10 → (A) faithful; rank J_C = 5 → loss = 5-dim
Im(L) (10-dim) = triv(5) ⊕ std(4,1) ⊕ (3,2);  LOSS = (3,2), single 5-dim FAITHFUL irrep
```

**[FOUR_ROLE_FRONTIER-F17]** Solvability wall measured (CALC-11) — `[computed]`:
```
derived series orders — S₃: [6, 3, 1] solvable; S₄: [24, 12, 4, 1] solvable; S₅: [120, 60] STALLS at A₅
S₄'' = order 4 = V₄ = the n=4 shape-quotient kernel
```

**[FOUR_ROLE_FRONTIER-F18]** n=6 confirmation (CALC-12) — `[computed]` (S₆ character table built from scratch via Murnaghan–Nakayama, norm-checked):
```
rank L = 15, all Q_k = 6; rank J_A = 15; rank J_C = 6 → loss = 9 = n(n−3)/2
Im(L) = triv(6) ⊕ std(5,1) ⊕ (4,2);  LOSS = S^(4,2), dim 9, FAITHFUL
S₆ derived series [720, 360] stalls at A₆
```
Also CALC-13(A): rank L = C(n,2) and χ_Im(L) = χ_pair on every class for n=5,6,7,8 (`[computed]`, n=7,8 "numerically verified, integer-clean").

**[FOUR_ROLE_FRONTIER-F5]** n=3 anchors (CALC-01/02/05, CALC-15a) — `[computed]`, cross-checked against compiled PDF:
```
CALC-01 (keystone in x-coords, F = x₁² + x₁x₂ + x₃² − 3 at (1,1,1), g=(3,1,2), q = gᵀg = 14):
  κ_c (t²) = −1/49; κ_int (t·u) = −3/49; κ_s (u²) = +1/49; K_G = −3/49
CALC-02 (F = D² + DS + P² − 3 at (1,1,1)):
  f_jl = −(F_jl + F_jk f_l + F_kl f_j + F_kk f_j f_l)/F_k        [implicit 2nd-derivative formula]
  κ_c^(P) = −25/196; κ_c^(D) = −1/441; κ_c^(S) = −1/49
  A_c = (κ_P−κ_D)² + (κ_D−κ_S)² + (κ_S−κ_P)² = 42793/1555848
CALC-05 (n=3 faithfulness):
  det ∂O/∂(A,B,C) = 8 Λ_P Λ_D Λ_S / q₀⁶,  Λ_P = B, Λ_D = (Ab−aB)/a, Λ_S = (Ca−bB)/b, q₀ = 1+a²+b²
CALC-15a (paper cross-check): Def-1 triple (Λ_P,Λ_D,Λ_S) = (−5/4, 1/6, 1/2);
  plain bordered Hessian on chart P returns ±1/2 ≠ Λ_P = −5/4  (Gauss–Kronecker object, ruled out by paper Remark 1 §5)
CALC-29: A_c = 3‖P₂O‖² (anis §2); dimension law dim Z_Σ = 2−r (anis §3); Prop 1 channel map linear, det = −1
```

### 2.3 Higher-order findings (order axis r)

**[FOUR_ROLE_FRONTIER-F19]** Ĉ_r parity law and normalization (CALC-15) — parity `[computed]` on one n=5 surface (q = 495 = 9·55); mechanism `[claimed]` proven:
```
Ĉ_r = bordered minors of M = tH_c + uH_s, normalised by q^((r+2)/2), 1 ≤ r ≤ n−1
even r: every coefficient ∈ ℚ; odd r: every coefficient ∈ ℚ(√q), pure √q multiples (no rational part)
mechanism: field fixed entirely by norm = q^((r+2)/2) — integer power of q (even r) vs q^k·√q (odd r)
A_c^(r) (std-irrep norm² of the per-chart t^r coupling family): nonzero r=2,3,4 and RATIONAL for all r
```
CALC-15 verdict "climbing r surfaces no new representation structure (stays in std)" — **superseded** (see CALC-18 F3/CALC-21; flagged in §5).

**[FOUR_ROLE_FRONTIER-T7]** Alternating companion absent at first order (CALC-18 Finding 1) — `[computed]` n=4..7:
```
∧²(std) has character ½(χ_std² − χ_std∘sq), = single irreducible S^(n−2,1,1) (dim C(n−1,2))
⟨χ_{Im(L)}, χ_{S^(n−2,1,1)}⟩ = 0 for n=4..7 — no alternating content in the linear carrier
```

**[FOUR_ROLE_FRONTIER-F23]** Plethysm screen (CALC-18 Finding 3) — `[computed]` n=5,6:
```
⟨χ_{Sym^r(Sym²std)}, χ_{S^(n−2,1,1)}⟩ = 1 at r=2;  = 8 (n=5) / 10 (n=6) at r=3
```

**[FOUR_ROLE_FRONTIER-T9]** ∧² realized at degree 2 (CALC-21, T2 resolved positive) — `[computed]` n=4,5,6; Schur reduction `[claimed]`:
```
κ_c = −Λ²/q² per flag; at symmetric jet κ_c = const · (Hadamard square of L(O))
S^(n−2,1,1)-projection of the density's quadratic image has rank 3, 6, 10 = FULL dim S^(n−2,1,1) (n=4,5,6)
density's quadratic image = ALL of M_flags (rank 12, 30, 60); Im(L) projects to 0 (linear carrier blind)
realization is granularity-dependent: per-(chart,pair) target M_flags carries ∧²; aggregate per-chart target ℝⁿ = triv⊕std is blind
```

**[FOUR_ROLE_FRONTIER-T20]** Full bidegree spectrum resolves the n=4 shape (CALC-26) — `[computed]` exact ℚ:
Setup: `H_c` isotypics via pair-partitions A=12|34, B=13|24, C=14|23; `u_A=H₁₂+H₃₄` etc.; std components `w_A=H₁₂−H₃₄` etc.; pure-S^(2,2) deformations `dir1(ε): u_A+ε, u_B−ε`, `dir2(η): u_B+η, u_C−η`; base `g=(2,1,3,1)`, `H_s=diag(1,2,1,3)`, `H_c=(1,2,1,1,2,1)`.
```
              k₁;₀₁ k₁;₁₀  k₂;₀₂ k₂;₁₁ k₂;₂₀  k₃;₀₃ k₃;₁₂ k₃;₂₁ k₃;₃₀
   ∂/∂ε  [    0    -2      0     15     29      0    -25    -32     63 ]
   ∂/∂η  [    0     2      0    -14    -29      0     24     35    -63 ]   rank = 2
```
Pure-self channels k_{r;0,r} constant (shape-blind); coupling channels (p≥1) carry the shape.

**[FOUR_ROLE_FRONTIER-T11]** Carrier = gauge-invariant Hessian quotient + the dimension threshold (CALC-27) — `[claimed]` proven + `[computed]`:
```
Gauge-normal form (CL-H1, regular g): a_i = H_ii/2g_i kills diagonal;
obstruction O_ij = H_ij − g_i H_jj/(2g_j) − g_j H_ii/(2g_i);  Sym_n/Im(G_g) ≅ ℚ^{n(n−1)/2} via [H] ↦ O
dim O = n(n−1)/2 = dim M^(n−2,2)  ⟹ session carrier = framework's gauge-invariant Hessian quotient
Threshold: scalars (n−1 invariants σ_r) resolve the shape iff  n−1 ≥ n(n−3)/2 ⟺ n²−5n+2 ≤ 0 ⟺ n ≤ 4
 n | dim shape n(n-3)/2 | #σ_r (n-1) | resolve?
 3 |        0           |     2      | absent
 4 |        2           |     3      | YES  (V₄ accident)   [= CALC-26 rank 2]
 5 |        5           |     4      | NO   (kernel ≥ 1, by dimension)
 6 |        9           |     5      | NO   (kernel ≥ 4)
 7 |       14           |     6      | NO   (kernel ≥ 8)
```
Gauge-robustness check: σ = (−39,−25,16) invariant under a=(3,−1,2,−2); σ_r-Jacobian under (ε,η) = `[[−2,44,6],[2,−43,−4]]ᵀ`, rank 2. `[computed]`

**[FOUR_ROLE_FRONTIER-T12]** Aliasing-locus conjecture refuted (CALC-28) — `[computed]` (GCDs) + `[claimed]` (codim argument):
```
Δ_n = (a−b)²(a+1)²(b+1)²   (the tested n=3 discriminant object)
base A (std-free coupling): GCD of rank-drop minors = g₁ − g₃; base B, C (generic): GCD = 1; symmetric coupling: GCD = 0
Refutation: rank-drop of 3×2 Jacobian is codim 2; Δ_n / {g_i=g_j} is codim 1 — cannot coincide.
Conditional bridge: on the std-free slice the rank-drop collapses onto role-coincidence {g_i=g_j}.
```

**[FOUR_ROLE_FRONTIER-T13]** Order-r target-presence theorem (CALC-31) — `[claimed]` proven all r, all n≥2r; instances `[computed]`:
```
M_flags^(r) = Ind_{S_1 × S_r × S_{n−1−r}}^{S_n}(triv) = M^λ,   λ = sort_desc(1, r, n−1−r)
THEOREM:  S^(n−r, r) ⊆ M_flags^(r)   for every order r ≥ 1 and every n ≥ 2r.
Proof: Kostka K_{μλ} > 0 ⟺ μ ⊵ λ (dominance); both cases n≥2r+1 (λ=(n−1−r,r,1)) and n=2r (λ=(r,r−1,1)) check. ∎
r=3 multiplicities: n=6: mult 1 (target S^(3,3), dim 60); n=7..10: mult 2 (dims 140, 280, 504, 840)
Gate reproduction: M_flags^(2) contains S^(n−2,1,1) mult 1 (n=4..7); S^(n−2,2) mult 1 at n=4, mult 2 n≥5; dims n·C(n−1,2) = 12,30,60,105
```

**[FOUR_ROLE_FRONTIER-T14]** r=3 realizability + coupling-necessity control (CALC-32) — `[computed, certified]` n=6,7:
```
det[[0,a,b],[a,0,c],[b,c,0]] = 2abc  ⟹  D_{k,jlm}(O) = Λ_{k,{j,l}} · Λ_{k,{j,m}} · Λ_{k,{l,m}}  (= ½ × 3×3 coupling minor)
projector P_W = (f^W/n!)·Σ_g χ^W(g)·ρ(g); gates: trace(P_{(3,3)})=5; traces 1,10,18,10,16 reproduce CALC-31
n=6: rank P_{(3,3)}·D = 5 = dim S^(3,3); raw realized span = 60 = all of M_flags^(3)
n=7: rank P_{(4,3)}·D = 28 = 2·dim S^(4,3) = full isotypic
CONTROL: genuine ambient-diagonal-only channel → rank P_{(3,3)}·D_self = 0 (identically; 150 samples ≫ cubic dim 56)
```

**[FOUR_ROLE_FRONTIER-T15]** All-r engine (CALC-33) — engine `[claimed]` proven all r (+ symbolic check r=2..5); Φ-route realizations `[computed]` r=3..6:
```
O_ij = H_ij − (H_ii+H_jj)/2  (symmetric-jet obstruction);   Λ_{k,{j,l}} = O_jk + O_kl − O_jl
D_{k,T} = det(N),  N_{ab} = O_{i_a k} + O_{i_b k} − O_{i_a i_b}  (a≠b; diagonal 0)
ENGINE (O_ij = x_i x_j, x_k = 0):   D_{k,T}|_{x_k=0} = (1 − r) · ∏_{i∈T} x_i²
Nonvanishing: T ↦ ∏_{i∈T} x_i² has nonzero top-Specht S^(n−1−r,r) projection (monomial independence), n≥2r+1
LIFT GAP [claimed proven obstruction]: S^(n−1−r,r) of S_{n−1} branches from THREE S_n-irreps:
   S^(n−r,r), S^(n−1−r,r+1), S^(n−1−r,r,1) — engine alone cannot disambiguate
Φ chart-forget + down-map (GF(p), p=2³¹−1; positive rank-increase rigorous over ℚ), n=2r+1:
 r | n  | dim ℂ[r-subsets] | rank(dᵀ) → augmented | realizes S^(n−r,r)
 3 |  7 |        35        |     21 → 22           | YES
 4 |  9 |       126        |     84 → 85           | YES
 5 | 11 |       462        |    330 → 331          | YES
 6 | 13 |      1716        |   1287 → 1288         | YES
```

**[FOUR_ROLE_FRONTIER-T16]** All-r lift theorem, interior (CALC-34) — `[claimed]` proven r≠4; r=4 `[computed]` explicit witness:
```
deletion map ∂: ℂ[r-subsets] → ℂ[(r−1)-subsets], ∂(T) = Σ_{i∈T}(T∖i);  ker(∂) = S^(n−r,r) (mult 1, r ≤ n/2)
test vector: w' = Σ_{S⊆[r]} (−1)^{|S|} δ_{B(S)}  (matching polytabloid over r columns (p_a,q_a));  ∂(w') = 0
det(hollow(γ_a+γ_b)) = (−1)^r 2^{r−2}·[(r−2)² e_r(γ) − e_1(γ) e_{r−1}(γ)]      [verified r=2..7]
⟨Φ(D), w'⟩ = (−1)^r 2^{r−2} (r−1)(r−4) ∏_{a=1}^r (c_{q_a} − c_{p_a})           [verified EXACTLY r=2..7]
THEOREM. For all r≥2 and n≥2r+1, κ_{r;r,0} (the r×r coupling minor) realizes S^(n−r,r).
r=4: star closed form vanishes ((r−4)=0); rank-one witness O_ij = x_i x_j gives pairing −2464416 ≠ 0 ⟹ realized.
```

**[FOUR_ROLE_FRONTIER-T17]** Threshold n=2r closed → complete (r,n)-plane theorem (CALC-35) — `[claimed]` proven (derivation) + `[computed]` r=3..7 checks and r=3..6 generic-O certifications:
```
⟨Φ(D), w'⟩ = (−1)^r 2^{r−2} · [∏_{a=1}^{r−1}(c_{q_a}−c_{p_a})] · C_r
C_r = (r−1)(r−4)·c_{q_0} − Σ_{a=1}^{r−1}(c_{q_a}+c_{p_a})
r≥3: C_r a never-identically-zero linear form ⟹ realized;  r=2 direct: ⟨Φ(D),w'⟩ = 4c_{q_0}(c_{p_1}−c_{q_1}) ≠ 0
ker(∂) = S^(r,r), dim = Catalan(r) = C(2r,r)/(r+1)
 r | n=2r | dim ℂ[r-subsets] | rank(dᵀ) → aug | realizes S^(r,r)
 3 |  6   |        20        |    15 → 16      | YES
 4 |  8   |        70        |    56 → 57      | YES
 5 | 10   |       252        |   210 → 211     | YES
 6 | 12   |       924        |   792 → 793     | YES
THEOREM (complete (r,n)-plane). For all r≥2 and all n≥2r, κ_{r;r,0} realizes S^(n−r,r).  [proven]
```
Note the clean twist (log's `[interpretation]`, `[speculative]` here): threshold cofactor is a linear form, so no degenerate order at n=2r (unlike interior r=4).

### 2.4 Characteristic-axis findings

**[FOUR_ROLE_FRONTIER-T10]** Char-2 boundary generalises to all n (CALC-16) — `[computed]` n=3..7 general symbolic g; mechanism `[claimed]` proven:
```
char ≠ 2: gauge rank = n → carrier Sym²(ℝ^n)/G is C(n,2)-dim
char 2: diagonal action 2g_i a_i vanishes; off-diagonal kernel condition flips
        g_i a_j = −g_j a_i (forces a=0 over ℚ)  →  g_i a_j = +g_j a_i (allows a ∝ g)
        gauge rank drops n → n−1, kernel = ⟨g⟩   (M·g = 2g_ig_j ≡ 0 mod 2; some (n−1)-minor odd; all n-minors even)
phantom g gᵀ = G_g(g/2): diagonal g_i², absent from the purely off-diagonal char-2 gauge image → restores exactly 1 dim
NET: carrier is C(n,2)-dimensional in EVERY characteristic, for all n.
```
Open (log's own tier): all-n RoleChSpec faithfulness in char 2 (CL-H10 analog) — `[speculative]`.

**[FOUR_ROLE_FRONTIER-T21]** Campaign H spine audit + the two parities (CALC-17) — `[computed]` (independent re-derivation):
```
κ_int = 0 every chart in gauge-normal coords; O-parity: r=1 ODD / r=2 EVEN in O;
r=1 coefficient matrix rank 3 (injective); coupling-rows minor numerator carries constant 32 = 2⁵ (char ≠ 2 obstruction)
Two parities, distinct: O-parity (degree-r in carrier O → injectivity; r=1 fixes the O-sign)
                        vs field-parity (ℚ / ℚ(√q), = the q^((r+2)/2) normalization, CALC-15)
```

**[FOUR_ROLE_FRONTIER-F21]** Integral / 2-torsion structure (CALC-18 Finding 2 as CORRECTED by CALC-19) — `[computed]` n=4..8 + independent Codex + second-campaign reproductions:
```
SNF(M_G : ℤ^n → Sym²(ℤ^n)), columns G_g(e_a) at g=(1,…,1), entry a_k+a_l:  invariant factors [1,…,1,2]  (n=4..7)
Quotient model:  Sym²(ℤⁿ)/gauge_ℤ ≅ ℤ^{C(n,2)} ⊕ ℤ/2, generator [g gᵀ]  (2·g gᵀ = G_g(g) ∈ gauge, g gᵀ ∉ gauge)
   torsion = non-saturation  sat(gauge)/gauge ≅ ℤ/2
Image model:  coker(L) torsion-free; ker(L_ℤ) = sat(gauge) ⊋ gauge; Im(L) ≅ Sym²/sat(gauge) = ℤ^{C(n,2)}, free
   ⟹ L washes the phantom out; the phantom lives in the gauge/kernel, NOT in the realised carrier
char-2 dims: dim(Sym²/gauge ⊗ F₂) = n(n+1)/2 − (n−1) = C(n,2)+1 (the +1 = phantom);  rank(Im(L) ⊗ F₂) = C(n,2)
CALC-20 verifications: coker(Sym²(ℤᵐ)⊕∧²(ℤᵐ) ↪ ℤᵐ⊗ℤᵐ) = (ℤ/2)^{C(m,2)} (m=3..6 → 3,6,10,15);
   rank(L mod 2) = C(n,2) (n=4..7, no mod-2 rank drop); ker(L mod 2) = gauge_mod2 ⊕ ⟨g gᵀ⟩, dim n
```

**[FOUR_ROLE_FRONTIER-F25]** 2-modular collision (CALC-22) — `[computed]` n=4..7; all-n pattern `[speculative]` (log: conjecture, 4 cases):
```
n=4: shape S^(2,2) = D^(3,1);                     orient S^(2,1,1) = D^(4) + D^(3,1)
n=5: shape S^(3,2) = D^(5) + D^(3,2);             orient S^(3,1,1) = 2·D^(5) + D^(3,2)
n=6: shape S^(4,2) = D^(6) + D^(5,1) + D^(4,2);   orient S^(4,1,1) = 2·D^(6) + D^(5,1) + D^(4,2)
n=7: shape S^(5,2) = D^(5,2);                     orient S^(5,1,1) = D^(7) + D^(5,2)
PATTERN (conjecture all-n):  [S^(n−2,1,1)] = [S^(n−2,2)] + [D^(n)]   in the mod-2 Grothendieck group
(validation anchors: D^(2,1)=2, D^(3,1)=2, D^(4,1)=4, D^(3,2)=4, trivials 1)
```
Stratification statement (CALC-22, `[claimed]` as closed): prime-2 = three distinct layers — (a) phantom ℤ/2 in gauge/kernel; (b) ∧² enters at degree 2 in local channel curvature; (c) generic mod-2 collision, orient = shape + trivial; V₄ is the n=4 special case of (c), distinct from (a).

### 2.5 Phase-2 (transcendental hunt) — exact formulas recorded here only

**[FOUR_ROLE_FRONTIER-F31]** Gauss–Bonnet trap (CALC-23) — value `[computed]` (3 independent routes, 60 digits); reduction chain `[claimed]` proven link-by-link; "provably NOT a Γ-value" **overclaimed** (see §5 R3):
```
K_G = −12/|∇F|⁴ = −12/[(2D+S)²+D²+4P²]²   on D²+DS+P²=3   (bordered-Hessian det = 4(D²+DS+P²) ≡ 12 on surface)
∫∫_S K_G dA = −5.010490702660418769050021160526777648057…  =  (−1.594888725…)·π
∫∫_S K_G dA = −2∮_{C₊}κ_g ds = −∫₀^{2π} √(cos²φ−2cosφ+5)/(3−cosφ) dφ
            = −8 ∫₀^{π/2} sin²θ /√(1+sin⁴θ) dθ          (L² = 4(1+sin⁴(φ/2)))
            = −4 ∫₀¹ w dw /√(w(1−w)(1+w²))               (w = sin²θ)
elliptic curve y² = w(1−w)(1+w²), branch points {0, 1, i, −i}, cross-ratio −i, j-invariant = 128 (non-CM)
J1 := ∫₀¹ dw/√Q = 2^{3/4}·K(k), k² = (2−√2)/4;   J1+J2 = 2J3 (proven via involution w ↦ (1−w)/(1+w))
CLOSED FORM: ∫∫_S K_G dA = −2^{7/4} · [ (3+2√2)·Π( (4−3√2)/8 ; (2−√2)/4 ) − (2+2√2)·K( (2−√2)/4 ) ]
standard (un-sheared) hyperboloid: −2√2·π  (the DS shear breaks algebraic·π cleanliness)
```

**[FOUR_ROLE_FRONTIER-F32]** Curvature anisotropy landscape (CALC-24 Parts A/B) — `[claimed]` proven formulas + `[computed]` checks:
```
Q_s = x² + s·xy + z²;  n(φ;s) = (cosφ, (s/2)(cosφ−1), sinφ);  n·n = 1 + s²·sin⁴(φ/2)
curve y² = w(1−w)(1+s²w²), branch points {0, 1, ±i/s}
j(s) = (1728 s⁶ − 1728 s⁴ + 576 s² − 64) / (s⁶ + 2 s⁴ + s²)
dj/ds = 128(3s²−1)²(9s²+1)/[s³(s²+1)³] ≥ 0   (s⁶+2s⁴+s² = s²(s²+1)²; earlier-draft denominator error corrected in-log)
landmarks: s→0 nodal j→−∞ (rational·π); s = 1/√3: j = 0 (Γ(1/3)); s = 1: j = 128 non-CM (keystone); s→∞: j = 1728 (Γ(1/4))
resolvent cubic of branch points: roots {1/s², ±i/s}, discriminant −4(s²+1)²/s¹⁰ ⟹ resolvent Galois S₃ = S₄/V₄ always
magnitude/shape dictionary: j = S₄-symmetric invariant (blind to V₄) ↔ (C); resolvent cubic ↔ the (2,2) shape loss
```

**[FOUR_ROLE_FRONTIER-F34]** Monodromy trap (CALC-24 Part C) — `[claimed]` proven + `[computed]`:
```
F = D³ + DS + P² − 3  ⟹  y² = x³ + S x + 3 (x=D, y=P);   j(S) = 6912 S³ / (4 S³ + 243)
S = 0: j = 0, CM ℤ[ω] → Γ(1/3); real period = Γ(1/3)³ · (3/2)^{1/3} / π   [(period·π/Γ(1/3)³)³ = 3/2 exact]
S = 1: j = 6912/247 non-CM;  S → ∞: j = 1728 → Γ(1/4)
```

**[FOUR_ROLE_FRONTIER-F35]** Exact CM ladders (CALC-24 Parts E/E.2) — `[claimed]` rung equation proven + `[computed]` roots to 50–60 digits:
```
rung equation in u = s²:  (1728−J) u³ − (1728+2J) u² + (576−J) u − 64 = 0
h=1 ladder (all at s < 1/√3): d = −163, −67, −43, −27, −19, −11 (irreducible cubics in u, recorded in-log);
d = −7: s = 1/(3√7) = √7/21 exact, u = 1/63, cubic factors (63u−1)(81u²+81u+64); d = −3: s = 1/√3 (triple contact (3u−1)³)
h=2 band walls (complete, scan |D|≤8000): d = −32 (s≈1.1479222), −403 (0.8423555), −91, −15, −187, −35, −99
H₋₃₂(x) = x² − 52250000x + 12167000000  (nearest wall);  bracket: −403 (s≈0.842) < keystone (s=1) < −32 (s≈1.148)
```

**[FOUR_ROLE_FRONTIER-F37]** Carrier invariant & fault injection (CALC-24 Parts E.3/E.4) — E.3 identity `[claimed]` proven symbolic; landings `[computed]`; E.3's spectator-inertness `[speculative]` and REFUTED by E.4:
```
σ = 2h/(λ−b) = tan(2θ)   with  j(M) ≡ j_formula(σ)     (coupled block [[λ,h],[h,b]]; keystone [[1,½],[½,0]])
fault landings: b = 1−√3 → j = 0 (Γ(1/3));  b = 1−3√7 → j = −3375 (d=−7)
aliasing triple: (h=½,b=0), (h=1,b=−1), (h=¼,b=½) — all σ=1, all j=128
E.4 (M = [[A,h,0],[h,b,0],[0,0,G]]):  m(φ) = (√A·cosφ, (h/√A)cosφ−ρ, √G·sinφ), ρ = √(h²/A−b);
det(m,m′,m″) = √(AG)·ρ constant;  period curve y² = (1−C²)(αC²+βC+γ), C = cosφ
α = A + h²/A − G,   β = −2h√(h²/A−b)/√A,   γ = h²/A − b + G
G-sweep at keystone block: G=½ → j=1728 (exact); G=1 → 128; G=3/2 → 8000 (d=−8, extra branch pt −1+2√2); G=2 → 61714.3
ceiling: coupled-block-only family capped at j=1728; broken only at α=0, i.e. G = A + h²/A (branch points go real)
```

**[FOUR_ROLE_FRONTIER-F39]** Self-glue aliasing triple / D₄ (CALC-25) — `[claimed]` proven + `[computed]`:
```
F = λD² + 2h·DS + b·S² + P² − 3; forward glue D₂ := P₁:
A = 3 − (λD₁² + 2h·D₁S₁ + b·S₁²)   (= P₁²);   B = 3 − λA − b·S₂²
F̃(D₁,S₁,S₂,P₂) = (B − P₂²)² − 4h²·S₂²·A      [at (1,½,0) reduces to keystone (B−A)² − A·S₂², B = 3−P₂²]
product cover: biquadratic P₂⁴ − 2B·P₂² + q, q = B² − 4h²S₂²A;  classification q□→V₄, Aq□→C₄, else D₄
G_product = D₄ (order 8) for all three triple members  ⟹ abstract group aliases exactly as j did
discriminating invariant: omega-branch multiplicity (b·S₂² ± 2h√A·S₂ + (λA−3) = 0: linear for b=0 → 2 branches;
quadratic for b≠0 → 4) + block signature (F1 det=−¼ indef; F2 det=−2 indef; F3 det=7/16 pos-def)
⟹ (mult, signature): F1=(2,indef), F2=(4,indef), F3=(4,def) — all three separated
```

**[FOUR_ROLE_FRONTIER-F40]** Same-S₃ negative (CALC-36) — `[claimed]` structural + `[computed]` certified:
```
cubic F = D³ + DS + P² − 3 @ (1,1,1):
LOCAL role S₃:  (κc_P, κc_D, κc_S) = (−4/49, −1/441, −4/441);  A_c(cubic) = 2258/194481
GLOBAL within-block S₃: directive cubic D³ + D − 2 = 0 @ (S,P)=(1,1); roots {1, (−1±i√7)/2}; disc = −112 (non-square) ⇒ Galois S₃
disc(D,S) = −4S³ − 27D²(D²+S)²   (directive-cubic discriminant datum)
Jacobian det of (A_c, disc) wrt (D,S) at (1,1) = −238720/194481 ≠ 0; nonzero also at (1/2,2), (2,−1), (−1,3)
⟹ rank 2, A_c ⊥ disc_directive: the two standard-2 data are functionally independent; "same S₃" is NO.
```

### 2.6 Candidate formal lemmas (extraction targets)

- **L1** ← T1: Role-pair module theorem `Im(L) ≅ M^(n−2,2)` — cleanest formalization target; 3-step proof fully articulated (gauge kernel, Sym² quotient, character identity). Companion doc `imL_pair_module_theorem.md` claimed self-contained.
- **L2** ← T3: Character/margin lemma: `χ_shape = C(fix,2)+#2cycles−fix`; kernel of S^(n−2,2) is V₄ iff n=4, trivial iff n≥5; margin = 2(n−3). Pure rep theory, self-contained.
- **L3** ← T13: Dominance lemma `S^(n−r,r) ⊆ M^{sort_desc(1,r,n−1−r)}` for n≥2r (two-line Kostka/dominance proof recorded verbatim).
- **L4** ← T15: Engine collapse `det(diag(x²) − x_T x_Tᵀ hollow form) = (1−r)∏x_i²` (matrix-determinant lemma instance) + monomial-independence nonvanishing.
- **L5** ← T16/T17: Hollow-det closed form `(−1)^r 2^{r−2}[(r−2)²e_r − e_1 e_{r−1}]` and the two pairing closed forms (interior and threshold) — fully explicit, verified r=2..7; together they yield the complete (r,n)-plane theorem.
- **L6** ← T16: Branching-ambiguity lemma (the restriction of S^(n−r,r), S^(n−1−r,r+1), S^(n−1−r,r,1) all contain the chart top-Specht) — the reason the engine alone is insufficient.
- **L7** ← F21: Saturation lemma `sat(gauge)/gauge ≅ ℤ/2` generated by `[g gᵀ]`; `ker(L_ℤ) = sat(gauge)`; `Im(L_ℤ)` free of rank C(n,2).
- **L8** ← T10: Char-2 gauge rank-drop lemma (sign flip `−1 → +1` in the kernel condition; kernel = ⟨g⟩; phantom restores 1 dim; carrier C(n,2)-dim in every characteristic).
- **L9** ← T11: Scalar-threshold lemma `n−1 ≥ n(n−3)/2 ⟺ n ≤ 4` (with the gauge-normal-form identification of the carrier).
- **L10** ← T19: No-on-tangent-witness lemma (positive-definiteness of Q₀ on the shape plane) + the explicit two-state witness pair as a certified example.
- **L11** ← F32/F34: `j(s)` and `j(S)` closed forms with monotone-uniqueness of the rung inverse (dj/ds ≥ 0, corrected form).
- **L12** (conjecture target, NOT yet a lemma) ← F25: all-n `[S^(n−2,1,1)] = [S^(n−2,2)] + [D^(n)]` mod 2 — 4 cases only; flagged as the T3-handoff proof obligation.

---

## 3. CONVENTIONS

- **Arithmetic:** all exact-ℚ (sympy `Rational`/`Matrix`); later entries add exact-ℤ SNF, GF(p) with p=2³¹−1 (positive mod-p rank increase argued rigorous over ℚ), and high-precision mpmath for Phase-2 only (values never enter verdicts; "no float in any verdict" claimed from CALC-31 on).
- **Certainty tiers (the log's own):** `[computer-verified]`, `[proven]`, `[noted]`, plus later `[conjecture]`, `[interpretation]`, `[open]`, `[assessment]`, `[certified]`, `[computer-verified, certified]`, `[computer-verified — rigorous over ℚ]`. Mapping used in this note: `[proven]`→[claimed] (unless the full proof is inline and instance-checked, still [claimed] since not re-verified by this campaign), `[computer-verified]`→[computed], `[conjecture]/[interpretation]/[open]`→[speculative].
- **Framework:** DBP `D ⊕ S = P`; keystone surface `F = D² + DS + P² − 3` at `(1,1,1)` (in x-coords `x₁²+x₁x₂+x₃²−3`, g=(3,1,2), q=14); cubic fixture `F = D³ + DS + P² − 3`.
- **Carrier index conventions:** n=4 components indexed by ordered pair `(output role k, excluded input ℓ)` — CALC-04 table uses **0-based roles** `(0,1)...(3,2)`. General-n flags are `(chart k, pair {j,l})`, order-r flags `(chart k, r-subset T ⊆ roles∖{k})`. V₄ written on 0-based letters {(01)(23),(02)(13),(03)(12)}.
- **Carriers:** (A) = pair-resolved carrier (n·C(n−1,2) components); (C) = per-chart scalar magnitudes; `L` = linear map Hessian → numerators; `Im(L)` = realizable coupling numerators.
- **Sign/normalization:** numerator `Λ_{k,{j,l}}(H) = −(H_jl − H_jk − H_kl + H_kk)` (symmetric jet g=(1,…,1)); channel curvature `κ_c = −Λ²/q²`; `(C)_k = −(1/q²)ΣΛ²`; bordered-minor densities `Ĉ_r` normalized by `q^((r+2)/2)`, `q = gᵀg`; `K_G = −det(bordered Hess)/|∇F|⁴`. Bidegree `κ_{r;p,q}`: p = coupling degree (H_c), q = self degree (H_s); pure coupling = `κ_{r;r,0}`, pure self = `κ_{r;0,r}`.
- **Gauge:** action `G_g(a) = g aᵀ + a gᵀ` (= defining-function rescaling `F → φF`); gauge-normal form kills diagonal via `a_i = H_ii/2g_i`; obstruction general-g `O_ij = H_ij − g_iH_jj/(2g_j) − g_jH_ii/(2g_i)`, symmetric-jet `O_ij = H_ij − (H_ii+H_jj)/2`; the phantom is `g gᵀ = G_g(g/2)`.
- **Rep theory:** S_n irreps by partition `S^λ`; permutation modules `M^λ`; role-pair module `M^(n−2,2) = ℂ[C(n,2) pairs] = triv ⊕ std(n−1,1) ⊕ S^(n−2,2)`; n=4 class order `(e,(12),(12)(34),(123),(1234))`; multiplicity tuple order `(triv, sign, std, std⊗sgn, 2dim)`; mod-2 simples `D^μ` (James); character tables built via Murnaghan–Nakayama and norm-checked, never transcribed.
- **"Faithful" — two distinct senses (log warns explicitly, CALC-29):** papers' *faithful carrier* = the jet→carrier **map** is injective (Jacobian rank); the session's *faithful at n≥5* = the **representation** S^(n−2,2) has trivial kernel. Do not cross-wire.
- **j-invariant:** true normalization `j(i) = 1728`; recorded hazard: `mpmath.kleinj` is 1728-normalized (`kleinj(i)=1`), band filter is `0<kleinj<1`.
- **Coupled-block parametrizations:** `[[λ,h],[h,b]]` (keystone `[[1,½],[½,0]]`), shear family `Q_s = x²+s·xy+z²` (`s=1` keystone), E.4 full form `M=[[A,h,0],[h,b,0],[0,0,G]]`; substitutions `w=sin²θ`, `u=s²`, `C=cosφ`.
- **Editing discipline:** superseded entries left intact with forward-pointing corrections (CALC-18←19, CALC-15←18/21, CALC-26←27, E.3←E.4) — EXCEPT where in-place strikethroughs/edits were made (see R6).

---

## 4. UNIQUE MATERIAL (exists only here; must not be lost)

1. **The complete CALC-14 proof sketch inline** (3 steps with the explicit gauge generator `v_a = H_{a0} − ½H_{00}`) — the only other copy is `imL_pair_module_theorem.md` (unverified present).
2. **The complete (r,n)-plane theorem chain (CALC-31→35)** — target-presence dominance theorem, engine collapse, branching-gap lemma, both pairing closed forms (interior `(r−1)(r−4)∏(c_q−c_p)` and threshold `C_r` linear form), and all GF(p)-certified rank tables r=3..6. No paper version exists; container scripts are gone.
3. **Exact numeric anchors:** `A_c = 42793/1555848` (quadratic keystone), `A_c(cubic) = 2258/194481`, the CALC-04 12-component table, the CALC-30 witness pair with `(C) = (6,33,33,54)` and isotypic split 147/153/24, the CALC-26 rank-2 Jacobian rows, `σ=(−39,−25,16)`, `Jdet = −238720/194481`.
4. **The 2-modular decomposition data (CALC-22)** for `S^(n−2,2)`/`S^(n−2,1,1)`, n=4..7, and the collision pattern `orient = shape + trivial`.
5. **Phase-2 period results:** the 60-digit total curvature, the Legendre Π/K closed form, `j=128` non-CM identification, `j(s)` and `j(S)` landscape formulas, the exact h=1 CM ladder minimal polynomials, the complete h=2 band-wall list with `H₋₃₂`, the `σ = tan(2θ)` identity, the E.4 period-curve `(α,β,γ)` formulas and the Γ(1/4)-ceiling-break criterion `α=0`.
6. **The correction/refutation history** (CALC-18→19 phantom relocation; CALC-15→18/21 order-axis reversal; CALC-26→27→28 scalar-resolution threshold; E.3→E.4 spectator refutation; CALC-36 line-797 framing correction) — the epistemic audit trail exists nowhere else and directly constrains which statements may be consolidated.
7. **The Frontier map F1–F8 + methodology** (import-audit principle, Lattice frame, "solvable corner" meta-shape) — the campaign's open-problem inventory, including the still-open items: all-n RoleChSpec char-2 faithfulness (CL-H10 analog), modular rep theory at other primes, mixed bidegrees `κ_{r;p,q}`, alternating/three-row depth-r irreps, full-density surjectivity, F3 degeneracy varieties, F4 residue↔cycle-type bridge, F6 ambient-curvature wall, F7 Zariski-density.
8. **Campaign H and second-campaign audit records** (CALC-16/17/20): the identification `Campaign H gauge = CALC-14 gauge`, the O-parity vs field-parity distinction, the `32 = 2⁵` obstruction confirmation, and the triangulation table — no consolidated record elsewhere.
9. **CALC-25's discriminating invariant** (omega-multiplicity + signature separating the `j=128`/`D₄` aliasing triple) and the general coupled-block eliminant `F̃`.
10. **CALC-36's framing correction**: the global within-block S₃ is the *directive-cubic Galois group* (mD=3 only), NOT the CALC-25 `S₄/V₄` — plus the note that `/mnt/project/self_glue_monodromy.pdf` is a corrupt zip.

---

## 5. RED FLAGS

- **R1 — Superseded claim standing verbatim (extraction hazard).** CALC-18 Finding 2 states "the integral carrier is `ℤ^{C(n,2)} ⊕ ℤ/2`" — **false for `Im(L)`** (torsion-free); corrected only downstream in CALC-19. Anyone extracting CALC-18 alone inherits the error. Same pattern: CALC-15's "climbing r surfaces no new representation structure" (refuted CALC-18 F3 + CALC-21), CALC-26's "full spectrum resolves the shape" (restricted to n≤4 by CALC-27), E.3's "the geometry uses tan(2θ), full stop" (refuted E.4). **Rule for consolidation: never lift a CALC-15/18/23/25/26/E.3 verdict without its downstream correction.**
- **R2 — Headline "RESOLVED/CLOSED" over residual conjectures.** CALC-22 titles "T3 RESOLVED" and "STRATIFICATION CLOSED" while its central pattern `[S^(n−2,1,1)]=[S^(n−2,2)]+[D^(n)]` is `[conjecture]` on 4 cases. CALC-32's title says "RESOLVED (POSITIVE)" while all-n realization at r=3 is `[conjecture]` (later genuinely closed by CALC-34/35, but the r=3 title predates the proof).
- **R3 — Unproved claim labelled as proved.** CALC-23's FINDING says the period is "provably transcendental and provably NOT expressible via π, radicals, logarithms, or Γ-values at rational arguments" — but its own Open item (2) concedes a formal not-a-Γ-value proof "would invoke Wüstholz/period-theory machinery (not carried out here)". The non-CM structure + PSLQ is evidence, not the claimed proof.
- **R4 — Acknowledged formula error in earlier drafts.** CALC-24 Part A: `dj/ds` denominator previously written `(s⁶+2s⁴+s²)²` ("too large by the shared factor s(s²+1)"); corrected in place. Any copy of v≤7 of this log (or downstream notes) may carry the wrong derivative.
- **R5 — Version/lineage confusion.** File is `_v8` but CALC-36's session note says results enter "the authoritative **v7** lineage"; it also reports an abandoned session that produced orphaned entries "on a stale v5 base with **colliding CALC-30..34 numbers**". Citations to CALC-30..34 must specify this file's lineage to avoid collision with the abandoned one.
- **R6 — Inconsistent no-silent-edit discipline.** CALC-18 was left intact per "no-silent-edit discipline", but CALC-29 (line-797 block) and CALC-24 E.3 were edited in place (strikethroughs, "RESOLVED (CALC-36) ... Formerly 'not yet welded'", "RESOLVED in Part E.4 (FALSE)"). The log is not a clean append-only record.
- **R7 — Stale structural marker.** The comment `<!-- APPEND NEW CALCULATIONS BELOW THIS LINE (CALC-23, …) -->` sits at line ~354, but CALC-18..22 follow it before CALC-23; Frontier map (F1–F8) is physically located mid-file between CALC-17 and CALC-18.
- **R8 — Notation abuse at n=3.** T1 is stated "for all n ≥ 3" with `M^(n−2,2)`, but `(1,2)` is not a partition at n=3; only the ℂ[role-pairs] reading (3-dim = triv⊕std) rescues the statement. A formal lemma must state the n=3 case separately.
- **R9 — Unresolvable external dependencies.** Definitions live in `/mnt/project/` (a different environment); the `/mnt/project` copy of `self_glue_monodromy.pdf` is a corrupt zip (CALC-36 flag, "repo repair" pending); nearly all CALC-15..36 scripts lived in an ephemeral container and are gone; `DBP_Curvature_Role_Reduction.md` (cited for the §8 parity proof, "Lovelock parity" §4) and the Campaign H uploads have no recorded repo paths; transcripts are cited by filename only. The log's embedded formulas are load-bearing as the sole re-creation route.
- **R10 — Two "parity" laws and two "faithful"s share names.** Field-parity (ℚ vs ℚ(√q), CALC-15) vs O-parity (degree parity in the carrier, CALC-17); map-faithfulness (Jacobian rank) vs representation-faithfulness (trivial kernel). The log distinguishes them explicitly, but consolidated statements that drop the qualifiers will conflate genuinely different theorems.
- **R11 — Minor range inconsistencies in verification claims.** Standing conclusion 6 says load-bearing steps verified n=4..9; CALC-14 Step 1 says n=4..7 and Step 3 n=4..9; conclusion 8 says pair-module law confirmed n=4..8 while CALC-13(A) covers n=5..8 exact/numeric plus n=4..6 exact from earlier entries. Not contradictions, but a consolidated theorem statement should cite per-step ranges.
- **R12 — Speculative echoes flagged as such but adjacent to theorems.** The r=4 witness-degeneracy ↔ n=4 V₄ "accident echo" (CALC-34) and the "scalar→linear-form cofactor promotion" reading (CALC-35) are `[interpretation]`; the Lattice frame is a "working hypothesis... on 2 data points". Keep these out of any lemma extraction.

---

*End of extraction note. IDs defined: T1–T4, T7, T9–T17, T19–T21; F5–F7, F9–F11, F16–F19, F21, F23, F25, F31–F32, F34–F35, F37, F39–F40; candidate lemmas L1–L12; red flags R1–R12.*
