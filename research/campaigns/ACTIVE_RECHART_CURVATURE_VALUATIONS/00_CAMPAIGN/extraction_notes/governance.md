# Extraction note: governance / disposition-authority sources

**Extracted:** 2026-07-30, for the theorem-consolidation campaign (AUTHORITY_FREEZE input).
**Extractor scope:** the three campaign governance documents only. Formulas below are quoted
verbatim from those documents; where a governance document itself truncates a formula (e.g.
`C_Ω … /[…]`), the truncation is preserved and flagged — the governance layer is *disposition*
authority, not formula authority.

---

## 1. SOURCE LIST

| # | Source (absolute path) | Role (one line) |
|---|---|---|
| S1 | `/home/user/Cella_Framework/research/campaigns/ACTIVE_RECHART_CURVATURE_VALUATIONS/00_CAMPAIGN/DBP_PAPER_SUCCESSION_AND_REDUNDANCY_MAP_v1.0.md` | The executed succession audit (2026-07-15, updated through 2026-07-18): per-artifact dispositions, theorem-level succession matrix, variant-twin resolutions, retirement candidates, open walls, safe merge order. **This is the disposition authority.** |
| S2 | `/home/user/Cella_Framework/research/campaigns/ACTIVE_RECHART_CURVATURE_VALUATIONS/00_CAMPAIGN/DBP_PAPER_ENSEMBLE_ARCHITECTURE_v1.0.md` | Frozen ensemble architecture (2026-07-14): paper boundaries I–V, theorem ownership per paper, release gates, spine policy ("never a proof source"), **sole holder** of the Paper V gate spec and the §7.3 elliptic (a,b,c) gap. |
| S3 | `/home/user/Cella_Framework/research/campaigns/ACTIVE_RECHART_CURVATURE_VALUATIONS/00_CAMPAIGN/CODEX_HANDOFF_DBP_PAPER_SUCCESSION_AND_REDUNDANCY_AUDIT_v1.0.md` | The audit mandate that produced S1: subsumption test (8 conditions), classification vocabulary (10 dispositions), operating principles, known status constraints. Governs *how* succession is decided; carries no theorem content of its own. |

Precedence for consolidation decisions: **S1 (dispositions) > S2 (boundaries/gates) > S3 (method)**.
S1 explicitly post-dates and updates S2's plan (e.g. CCE-5/6 already inserted into Paper III; gaps
I1–I3, III1–III4, IV1, IV3–IV5, V1 closed). Where S2's plan and S1's executed state differ, S1 wins.

### 1.1 Per-source authority list (AUTHORITY_FREEZE.json input)

Which document is canonical for which theorem, per S1 §§3–9 and S2 §§2–6.

**Paper I — role covers / active recharting**
- `dbp_orbit_calculus.tex` (+.pdf) — CANONICAL paper; owns S3 action, Orbit Thm, rational closure,
  channel reduction, RoleChSpec biconditional (I1), all-finite-order recurrence (I2), ambient-n /
  n=4 grid (I3), Gaussian 3-channel, named channels/faithfulness, keystone.
- `theorem_8_1.tex` — INDEPENDENT_COMPANION; owns abstract Invariant-Preservation (additive split + κ-dichotomy).
- `Canonical_Invariant_Reduction_Theorem.md` — PROOF_SUPPLEMENT; **sole proof authority** for the Lorentzian single-edge corollary.
- `Gauge_Channel_Transport_Law.md` — PROOF_SUPPLEMENT; **sole proof authority** for the full Lorentzian pinning derivation.
- `GAUGE_NORMAL_FORM_PROOF.md` — PROOF_SUPPLEMENT; **sole proof authority** for `Sym₃/Im(G_g)≅ℚ³`.
- `CCE_8_FINITE_TOWER_NATURALITY_THEOREM_v1.0.md` — CANONICAL atomic theorem (finite-tower naturality; NOT infinite-germ convergence).
- `Theorem_8_1_Curvature_Orbit_Correction.md` — MERGE_THEN_RETIRE (transfers listed at [GOVERNANCE-T57]).
- `DBP_Curvature_Role_Reduction.md` — INDEPENDENT_COMPANION (§14 Gauss–Lovelock elevation).
- `THEOREM_CANDIDATES.md` — COMPUTATIONAL_SUPPLEMENT (5298-class finite bound; open converse).

**Paper II — local curvature / Kerr–Newman (TWO independent papers)**
- `pfc_normal_forms.tex` — CANONICAL general-theory paper (collapse laws, parity law, corner rule).
- `lead7_kn_n3_dbp_metric.tex` — CANONICAL KN-realization paper (selection u=0, reflection coeffs, extremal sign, 3/4/4). KN cites pfc, not vice versa; neither subsumes the other.
- `LOCAL_CURVATURE_CALCULUS_COMPLETE_v1.0.md` — CANONICAL full proof spine (superset of pfc).
- `LEAD7_VARIABLE_TRANSVERSE_WEIGHTED_JET_THEOREM_v1.0.md` — CANONICAL newest strengthening (nondegenerate stratum `P1/P0+R1/R0≠0`).
- `LEAD7_masscharge_zeros_theorem.md` — PROOF_SUPPLEMENT (fuller proof of mass-role zeros, condensed in KN paper).
- `LOCAL_CURVATURE_CALCULUS_COMPANION.md` — MERGE_THEN_RETIRE (only §9 dual-constants block; belongs to Paper III close-off, see [GOVERNANCE-T58]).
- `Local_Curvature_Calculus_for_Inverse-Channel_Metrics.txt` — HISTORICAL_ONLY (Stage 1–10 roadmap; **never proof authority**).
- `kerr_retrograde_45_over_16_derivation.md` — INDEPENDENT_COMPANION.

**Paper III — DBP curvature periods**
- `DBP_CURVATURE_PERIODS_OF_THE_DBP_QUADRIC_v1.0.md` — CANONICAL consolidated paper (CCE-5/CCE-6 incorporated 2026-07-17); currently misfiled in tier 05.
- `DBP_LANDEN_TRACE_THEOREM_COMPLETE_v1.1.md` (un-suffixed copy) — CANONICAL **atomic proof authority**, named dependency across the corpus (fails subsumption condition 6; must not be retired).
- `DBP_CCE5_ABSOLUTE_CALIBRATION_THEOREM_v1.0.md` — PROOF_SUPPLEMENT; proof authority for the calibrated §7F insertion (λ↑/λ↓, route matrices, trace coordinates).
- `DBP_NATIVE_SURFACE_SWEEP_CLEARANCE_THEOREM_v1.0.md` — PROOF_SUPPLEMENT; proof authority for Lemma 7F.B and its exact bounds.
- `DBP_SURFACE_TO_LINK_CLOSEOFF_v1.0.md` — PROOF_SUPPLEMENT (III §7A delegates Stokes boundary + link-length proof).
- `DBP_DUAL_SURFACE_CYCLE_STAGE1/2/3_v0.1.md` — PROOF_SUPPLEMENT ×3 (III §7B/7C/7D delegate; gates 22/17/22 live here).
- `DBP_EXACT_CORRIDOR_POSITIVE_CLEARANCE_THEOREM_v1.0.md` — PROOF_SUPPLEMENT (Lemma 7F.A segment/29-disk clearance).
- `DUAL_CONSTANT_CLOSEOFF.md` — **dbp_role_channel copy is canonical** (adds §4A); the `cella_residue` copy is a misfiled older revision (SUPERSEDED_VARIANT).
- `CCE_6_WHOLE_SURFACE_TOPOLOGY_OBSTRUCTION_v1.0.md` — INDEPENDENT_COMPANION; unique rank-4-in-12 open-wall record.
- `LANDEN_TYPE_THEOREM_SOURCE.md` — INDEPENDENT_COMPANION (still-open primary↔dual Landen relation).
- `CCE_2_PAPER_III_INSERTION_NOTE_v1.0.md` — HISTORICAL_ONLY (insertion applied, hash-confirmed).

**Paper IV — Galois horizon / Kummer covers**
- `galois_horizon_cover_v1_0.tex` (+pdf + publication package) — CANONICAL released paper (splitting–temperature, area product, S₅ obstruction, chamber/selection results).
- `GENERIC_SYMMETRIC_MONODROMY_OF_WEIGHTED_MULTIQUADRATIC_SUMS_v1.0.md` (`PAP-0509`, DAG node `DBP:paper:weighted_multiquadratic_monodromy`) — CANONICAL reusable all-k, all-nonzero-weight base-monodromy authority; **supersedes** `DBP:note:allk_monodromy` as proof authority.
- `ALL_K_TWO_RADICAL_KUMMER_CLOSURE_v1.0.tex` (`PAP-0513`, node `DBP:paper:all_k_two_radical_kummer_closure`) — CANONICAL all-k Kummer-rank / `C₂² wr S_{δₖ}` closure; closes `DBP:gap:IV3`.
- `ALL_K_MONODROMY_THEOREM_NOTE_2026-07-10.md` — COMPUTATIONAL_SUPPLEMENT only; **no longer proof authority** (low-k certificates + development record retained).
- `GS_GENERIC_MORSE_LEMMA_PROOF_2026-07-10.md` — PROOF_SUPPLEMENT (independent cited route; no longer sole authority).
- `KUMMER_MODULE_WREATH_LIFT`, `ROTATING_KUMMER_RANK_JUMP`, `R9_STATIC_CLOSURE`, `ROTATING_THREE_CHANNEL_WREATH`, `WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1` — PROOF_SUPPLEMENT ×5 (proofs the preprint only states).
- `self_glue_monodromy.tex` (62546 B un-suffixed) — INDEPENDENT_COMPANION; `__5ff2665e` variant superseded.
- `GALOIS_K_ELLIPSE_RESEARCH_MAP_v1_6.md` — CANONICAL program dashboard (**true head**; v1.1/v1_3/v1_4 superseded); dashboard, not proof authority.
- `[live] research/campaigns/CELLA_CONTINUATION_ENGINE/08_cce7_horizon/*` — CANONICAL sole spec of the OPEN complex-braid residual.

**Paper V / ensemble (Paper V DOES NOT EXIST — held conjecture)**
- `SELECTED_QUOTIENT_GROUPOIDS_FOUNDATION_v1.0.md` — CANONICAL SQG category foundation.
- `R3_AC_FOLD_INDEPENDENT_REALIZATION_THEOREM_v1.0.md` — CANONICAL/INDEPENDENT R3 realization (+ non-faithfulness).
- `DBP_PAPER_ENSEMBLE_ARCHITECTURE_v1.0.md` (S2) — CANONICAL; **sole** Paper V gate/gap spec; orphan risk if retired.
- `POST_8_AUTHORITY_SOURCE_MANIFEST_v1.0.md`, `POST_8_OUTCOME_GAP_LEDGER_v1.0.md`, `POST_8_UNIVERSALIZATION_REDUCTION_R3_FINAL_REPORT_v1.0.md` — CANONICAL sole SHA-map / P8-01..P8-21 enumeration / WP ledgers.
- `[live] DBP_CCE_ARTIFICIAL_RESTRICTION_LIVE_RECONCILIATION_v1.0.md` — CANONICAL sole AR-01..AR-26 ledger.
- `DBP_UNIFIED_THEOREM_SPINE_DRAFT_v0_1 (2).tex` (= v0.3, the "(2)" copy) — CANONICAL *draft ledger only*, **never a proof source**; plain `.tex` (v0.2) SUPERSEDED_VARIANT.

**Never-authority class (freeze as `authority: none`):**
spine drafts (any version); historical roadmaps (`Local_Curvature_Calculus_for_Inverse-Channel_Metrics.txt`, campaign BRIEF/README/CLAIMS/LOG files); insertion notes already applied; hashed run-log families (`CLAIM_LEDGER__*`, `MANIFEST__*`, `MUTATION_REPORT__*`, `PREREG__*`, `EXCEPTIONAL_LOCUS_REPORT__*`, `prediction_verdicts__*`); `Reports_Library`/`Campaign_Library`/`Evidence_Store` (every Evidence_Store `authority` value is a `*_reference`/`*_retirement_source` label — **never canonical**); the Encyclopedia `audit/` tree (pre-reorg paths; content scaffold only); `docs/files/` drops (EXACT_MIRROR of Papers_Library canon).

---

## 2. EXACT STATEMENTS

All quotes verbatim from S1/S2. Line references are to the source files as read 2026-07-30.

### 2.1 Governing rules (S1 preamble, S2 §0/§11, S3)

[GOVERNANCE-T72] Central succession question (S1 lines 15–18; S3 blockquote):
```
does a newer canonical paper preserve every mathematical contribution of an older document, under
the same or weaker hypotheses, while adding stronger results — so the older document has no
remaining unique mathematical, proof, computational, or expository value except historical
provenance?
```

[GOVERNANCE-T73] Subsumption test — HISTORICAL_ONLY allowed only if ALL hold (S3 "Subsumption test"):
```
1. Every mathematical unit maps to an explicit location in a retained successor.
2. The successor uses the same or weaker hypotheses, or any stronger hypothesis is justified and
   the lost generality is documented.
3. Exact constants, signs, orientations, coefficient rings, boundary conventions, and
   normalization choices are preserved.
4. Proof substance is retained in the successor or in a separately retained proof supplement.
5. Unique examples, counterexamples, and failure modes are preserved or deliberately catalogued
   as historical only.
6. No current source cites the older document as the sole proof authority for a live theorem.
7. No unresolved contradiction exists between the older and newer statements.
8. The proposed successor is itself canonical and present on disk.
```

[GOVERNANCE-T74] Classification vocabulary — exactly one primary disposition per artifact (S3):
```
CANONICAL_RETAIN / INDEPENDENT_COMPANION / MERGE_THEN_RETIRE / PROOF_SUPPLEMENT_RETAIN /
COMPUTATIONAL_SUPPLEMENT_RETAIN / HISTORICAL_ONLY / EXACT_MIRROR / FORMAT_RENDER /
SUPERSEDED_VARIANT / UNRESOLVED
```

[GOVERNANCE-T75] Decisive editorial rules (S2 §0):
```
1. Merge Landen--Trace and Native Relative-Period Route.
2. Absorb Surface-to-Link and Surface-Cycle Stages 1--3 into the same
   elliptic paper, with detailed calculations retained as appendices or
   proof dossiers.
3. Keep Galois Horizon Cover mathematically independent.
4. Keep the local role-cover foundation separate from its Kerr--Newman
   metric realization.
5. Do not publish the categorical capstone until equivalence, closure,
   and an independently sourced third realization are proved.
6. The unified spine is a ledger, not a sixth proof source.
```

[GOVERNANCE-T76] Spine policy (S2 §11):
```
The spine must never be cited as the proof source and must never allow the
capstone conjecture to prove one of its component realizations.
```
Also (S2 §1): "Paper III and Paper IV may cite Paper I for motivation and terminology, but
their mathematical proofs must not depend on the conjectural capstone."

[GOVERNANCE-T77] "Retire" semantics (S1 preamble; S3): `"Retire" throughout means *eligible to
move to a historical archive after maintainer review*, never automatic deletion.` And (S3
principle 5): `Hashes may establish byte identity or mirror duplication. They are not
mathematical evidence and must not become release gates.`

### 2.2 Paper I units (S1 §3 table — statements verbatim from the "Statement" column)

[GOVERNANCE-T1] Active role S₃ (source `dbp_orbit_calculus.tex:131`):
```
s(a,b)=(b,a), t(a,b)=(1/a,−b/a);  s²=t²=(st)³=e;  birational on regular jets
```
[GOVERNANCE-T2] Orbit theorem (`:187`):
```
φ order-r DBP-invariant ⟺ factors through X_r/S₃
```
[GOVERNANCE-T3] Exact rational closure (`:221`):
```
J_r∈ℚ ⇒ G·J_r ⊂ ℚ[Δ⁻¹]
```
[GOVERNANCE-T4] Channel reduction / exact sequence (`Canonical_Invariant_Reduction_Theorem.md`; `:259`):
```
σ_r = Ĉ_r(1,1)/q^{(r+2)/2};   0 → kerΣ → C_r → I_r → 0
```
[GOVERNANCE-T5] RoleChSpec gauge-orbit converse (orbit_calculus §7; closes I1 on regular n=3 locus):
```
equal fingerprints iff O_g(H₂−H₁)=0 iff H₂−H₁ ∈ Im G_g;  recovery determinant 32/(g₁g₂g₃)
```
[GOVERNANCE-T6] All-finite-order active recharting (orbit_calculus App.A; CCE-8; closes I2):
```
homogeneous recurrence q_d = −a⁻¹ R_d;  triangular truncation naturality for every finite word in ⟨s,t⟩
```
[GOVERNANCE-T7] Ambient-n / n=4 channel grid (orbit_calculus §6; closes I3; no n≥4 injectivity claim):
```
coordinate-triple sum for σ₂;  explicit K_{3,0}, K_{2,1}, K_{1,2}, K_{0,3} Newton grid
```
[GOVERNANCE-T8] Gaussian 3-channel (`:274`):
```
K_G = κc + κint + κs;  graph gauge  κc = −M²/Q²,  κs = LN/Q²,  κint = 0
```
[GOVERNANCE-T9] Named channels / faithfulness (`:336`):
```
Λ_P = B,  Λ_D = (Ab−aB)/a,  Λ_S = (Ca−bB)/b;   Jacobian det = 8Λ_PΛ_DΛ_S/q₀⁶
```
[GOVERNANCE-T10] Keystone (`:485`):
```
at (1,1,1):  κc = −1/49,  κs = 1/49,  κint = −3/49,  K_G = −3/49
```
[GOVERNANCE-T11] Lorentzian coupling-edge lemma (proof-supplement only; `Gauge_Channel_Transport_Law.md`, `Canonical_Invariant_Reduction_Theorem.md`):
```
ν = (g₁H₂₃, g₂H₁₃, g₃H₁₂),   Δc = ν^T (2I−J) ν   signature (2,1)
```
[GOVERNANCE-T12] Gauge-normal-form quotient (proof-supplement only; `GAUGE_NORMAL_FORM_PROOF.md`):
```
unique H⊥,   Sym₃/Im(G_g) ≅ ℚ³
```
[GOVERNANCE-T13] Invariant-Preservation 8.1 (companion, abstract form; `theorem_8_1.tex:94`):
```
additive φ = φ_K + φ_sym;   κ=0 / κ>0 dichotomy
```
[GOVERNANCE-T14] CCE-8 finite-tower naturality (`CCE_8_FINITE_TOWER_NATURALITY_THEOREM_v1.0.md`):
```
τ_{N,r}(w·f) = w·τ_{N,r}(f),  all finite N ≥ r ≥ 2
```

### 2.3 Paper II units (S1 §3)

[GOVERNANCE-T15] Lamé diagonal curvature engine (`LOCAL_CURVATURE_CALCULUS_COMPLETE_v1.0.md §2`):
```
R = −2 Σ_{i<j} (1/H_iH_j)[∂β + ∂β + Σββ]
```
[GOVERNANCE-T16] Divisor-channel decomposition (`COMPLETE Thm 3.1`):
```
R = Σ z^{−P_a−2e_a} F_a + Σ z^{−P_μ} F_μ
```
[GOVERNANCE-T17] Generic quadratic collapse, order 3 (`pfc_normal_forms.tex:94`; `COMPLETE 5.2`):
```
R = (1/A) Σ (P_{α1}/P_{α0}) x⁻³ + O(x⁻²)
```
[GOVERNANCE-T18] Parity-fixed reflection, order 4 (`pfc_normal_forms.tex:53`):
```
R = −m(m+5)/B · x⁻⁴;   m=2 → −14/B
```
[GOVERNANCE-T19] Corner vertex rule, closed (`pfc_normal_forms.tex:151`; `COMPLETE 7.4`):
```
A = −p₀² + p₀p₁ − p₀p₂ + 2p₀ + p₁p₂ − p₂² + 2p₂
```
[GOVERNANCE-T20] Variable-transverse weighted jet (`LEAD7_VARIABLE_TRANSVERSE_WEIGHTED_JET_THEOREM_v1.0.md`; canonical on nondegenerate stratum):
```
leading laws hold with arbitrary (y,z)-functions;  no transverse derivative in leading coeff;
nondegenerate stratum:  P1/P0 + R1/R0 ≠ 0
```
[GOVERNANCE-T21] DBP metric selection (`lead7_kn_n3_dbp_metric.tex:267`):
```
u=0 unique pos-def + interior-regular member on W₊
```
[GOVERNANCE-T22] Mass-role zeros = role divisors (`LEAD7_masscharge_zeros_theorem.md`; KN `:375`):
```
singular support ⊆ {J=0} ∪ {Q=0} ∪ {U_S=0}
```
[GOVERNANCE-T23] Reflection coefficients (KN `:481`) — **truncated in S1 itself; see RF13**:
```
C_Ω = −3584 Q²S⁵π³(S−πQ²)²/[…];   C_Φ analogous
```
[GOVERNANCE-T24] Strict-negative extremal coefficient (KN `:567`):
```
C_ext < 0 on whole open edge (two Sturm counts)
```
[GOVERNANCE-T25] n=3 complementarity (KN `:649`):
```
T=0→3, Ω=0→4, Φ_e=0→4;  Schwarzschild corner min 2
```

### 2.4 Paper III units (S1 §3 absorption table)

[GOVERNANCE-T26] Complementary params / involution (Paper III §1 = Landen v1.1 §1):
```
mε = (2−εs)/4 … Bε = 2+2εs;   m₊+m₋ = 1,  m₊m₋ = 1/8
```
[GOVERNANCE-T27] Degree-2 isogenies → E₁₂₈ (§2):
```
j(Cε) = 10976,  j(E₁₂₈) = 128,  Φ₂ = 0
```
[GOVERNANCE-T28] Common trace differential Θ (§3 Thm 3.1):
```
Θ = 8·(X−3)/(X+7)·dX/Y
```
[GOVERNANCE-T29] Exact logarithmic anti-differential (§5 Thm 5.1; MR-002 corrected sector present):
```
αε = Rε · dlog fε;   R₊ = 4i,  R₋ = 4
```
[GOVERNANCE-T30] Primary/dual anti-periods (§6):
```
primary −4π;  dual CPV 0;  one-sided ±4πi;  diff 8πi
```
[GOVERNANCE-T31] Native pole-free kernels (§7E Thm 7E.1):
```
P₊ = t⁴ + 2t²w² + 2w⁴;   A² − 2P₋ = −t²D
```
[GOVERNANCE-T32] Native morphism / signed transfer (§7F Thm 7F.1):
```
R_ℤ L_ℤ = 4·id;   coeff diamond ℤ / ℤ[½] / ℤ[i] / ℤ[½,i]
```
[GOVERNANCE-T33] Primary surface→link→period (§7A; proof delegated to `DBP_SURFACE_TO_LINK_CLOSEOFF_v1.0.md`):
```
∫_{S₁} K_G dA = −2L(Γ₁⁺) = I_primary
```
[GOVERNANCE-T34] Dual boundary + surface-cycle lift + PL transport (§7B/7C/7D; proofs in Stages 1/2/3, gates 22/17/22):
```
𝓑₋,  L_ℤ,   δ₋↑ − δ₋↓ = −μ₋
```
[GOVERNANCE-T35] Exact corridor reps, CCE-2 (§7F Lemma 7F.A; proof in `DBP_EXACT_CORRIDOR_POSITIVE_CLEARANCE_THEOREM_v1.0.md`):
```
words a₊ / a₋⁻¹;  radius-1/8 tube;  29-disk cover
```
[GOVERNANCE-T36] λ resolution + braid matrices, CCE-5 (`DBP_CCE5_ABSOLUTE_CALIBRATION_THEOREM_v1.0.md`; incorporated in §7F):
```
λ↑ = B₋,  λ↓ = −B₋;   M↑/M↓;   trace coordinates (1,0,0)/(1,0,1)
```
[GOVERNANCE-T37] Native surface-sweep clearance, CCE-6 (`DBP_NATIVE_SURFACE_SWEEP_CLEARANCE_THEOREM_v1.0.md`; incorporated in Lemma 7F.B):
```
Disc_Ξ(N) = −4(1−c)TD₂;   Res = c²D₁²;   ε∗ = 1/105186307200
```
[GOVERNANCE-T38] Dual constant closed form + branch (`DUAL_CONSTANT_CLOSEOFF.md`, dbp_role_channel copy):
```
I_dual = −2^{7/4}[K(k′²) − (3−2√2)Π(2√2−2; k′²)];   PSLQ refutes lattice completion
```
[GOVERNANCE-T39] Rank obstruction (`CCE_6_WHOLE_SURFACE_TOPOLOGY_OBSTRUCTION_v1.0.md`; unique open-wall record):
```
rank H₂(X,Y;ℤ) = 12,   rank im L_ℤ ≤ 4
```

### 2.5 Paper IV units (S1 §3, §1)

[GOVERNANCE-T40] Splitting–temperature (`galois_horizon_cover_v1_0.tex:248`):
```
roots of z² − e₁z + e₂,   e₁ = 2π(2M²−Q²),   e₂ = π²(4J²+Q⁴);   Θ = S·T Galois-odd
```
[GOVERNANCE-T41] Area-product invariant (`:385`):
```
Ŝ₊Ŝ₋ = P
```
[GOVERNANCE-T42] S₅ obstruction (`:435`):
```
quintic norm generic S₅ ⇒ Abel–Ruffini non-solvable
```
[GOVERNANCE-T43] Realization-poset certificate (`REALIZATION_POSET_RUN_REPORT…` + M2 suite):
```
incidence degrees (48, 2, 64, 192, 6, 8, 24)
```
[GOVERNANCE-T44] Weighted exact degree (`GENERIC_SYMMETRIC_MONODROMY…v1.0.md`, Prop. 2.3 / Thm 3.3):
```
d(c) = #{ {η,−η} : Σηᵢcᵢ ≠ 0 };   the weighted radical sum is primitive
```
[GOVERNANCE-T45] Genus and full ramification count (same, Thms 3.1 and 4.4):
```
g = 1 + 2^{k−2}(k−3)   and   deg Ram = 2^{k−1}(k−3) + 2d(c)
```
[GOVERNANCE-T46] Weighted generic monodromy (same, Thm 7.1 / Cor. 7.2):
```
for every fixed cᵢ ≠ 0, generic geometric and arithmetic monodromy are S_{d(c)}
```
[GOVERNANCE-T47] Equal-weight DBP specialization (same, §8; supersedes ALL_K as proof authority):
```
Gal(Nₖ/F) = S_{δₖ} for every k ≥ 3, with exact signed-pole degree δₖ
```
[GOVERNANCE-T48] All-k Thm A/B/C development record (`ALL_K_MONODROMY_THEOREM_NOTE…md`; retained supplement):
```
inertia localization;  certified k=3..6 groups S₄ / S₅ / S₁₆ / S₂₂;  independent low-k checks
```
[GOVERNANCE-T49] Generic Morse development proof (`GS_GENERIC_MORSE_LEMMA_PROOF…md`; retained supplement):
```
critical-value gradient (1/2wᵢ) and (GS) route
```
[GOVERNANCE-T50] Kummer/wreath lift interface (`GENERIC_SYMMETRIC_MONODROMY…v1.0.md` §10):
```
Gal(L/F) ≅ C₂^s wr S_{d(c)} when the s·d(c) conjugate square classes are independent;
full valuation-parity rank is sufficient
```
[GOVERNANCE-T51] All-k two-radical Kummer closure (`ALL_K_TWO_RADICAL_KUMMER_CLOSURE_v1.0.tex`, PAP-0513; closes DBP:gap:IV3; S1 lines 92–99):
```
γ_k = 2(α_k + P);   γ_k(γ_k − 4P) = 4uβ_k²;
two universal signed-contact rows (1,0) and (1,1);
rank 2δ_k and closure C₂² wr S_{δ_k} for every k ≥ 3
```
Caveat verbatim (S1): "only the four-charge member currently carries the established physical
entropy interpretation" / "This algebraic statement is all-`k`; its physical entropy reading is
asserted only at `k=4`."

### 2.6 Paper V / ensemble units (S1 §3; S2 §§6–9)

[GOVERNANCE-T52] SQG category (`SELECTED_QUOTIENT_GROUPOIDS_FOUNDATION_v1.0.md §3`):
```
R-selected quotient groupoids + native R-morphisms form SQG_R
```
[GOVERNANCE-T53] Flat scalar extension (same §4):
```
Ext_R^S : SQG_R → SQG_S with associativity iso
```
[GOVERNANCE-T54] R3 native AC fold (`R3_AC_FOLD_INDEPENDENT_REALIZATION_THEOREM_v1.0.md §1`):
```
F(v) = v² + (2QX − E²)v + X²(P² + Q²),   Δ = E⁴ − 4E²QX − 4P²X²;  integer winding groupoid
```
[GOVERNANCE-T55] R3 skeleton functor (same §3):
```
Z → C_2 full + ess-surjective, not faithful (kernel 2Z);  full-carrier equivalence not claimed
```
[GOVERNANCE-T56] Full unreduced carrier equivalence (`POST_8_OUTCOME_GAP_LEDGER_v1.0.md`):
```
REFUTED (P8-16, AR-23)
```

### 2.7 MERGE_THEN_RETIRE required transfers (S1 §8 — only two in the corpus)

[GOVERNANCE-T57] `Theorem_8_1_Curvature_Orbit_Correction.md` → `dbp_orbit_calculus.tex` §7. Transfer exactly:
```
numeric worked example (a,b,A,B,C) = (5,7,2,3,4);
explicit self-channel form  κ_{s,D} = A·R/(a²q₀²);
transverse-quadratic identity  R = a²C − 2abB + b²A
```
[GOVERNANCE-T58] `LOCAL_CURVATURE_CALCULUS_COMPANION.md` → `LOCAL_CURVATURE_CALCULUS_COMPLETE_v1.0.md`. Transfer only the §9 dual-constants block:
```
I_primary ≈ −5.01049…,   I_dual ≈ −3.98800…,   residue 4
```
Caveat (S1): this block belongs to the elliptic-period family — "it should land in the Paper III
dual-constant close-off, not the curvature spine."

### 2.8 Architecture-only statements (S2 — sole holder; see UNIQUE MATERIAL)

[GOVERNANCE-T59] Central coefficient theorem (S2 §4):
```
integral lateral transport       exists over Z
CPV meridian midpoint            first exists over Q
Galois phase normalization       first exists over C
```
[GOVERNANCE-T60] Closed results that must not be reopened + settled negatives (S2 §4):
```
EP-C1  primary surface-to-link reduction
EP-C2  metric quartic--Legendre isomorphism
EP-C3  degree-two isogenies and common E_128 trace differential
EP-C4  exact logarithmic closure of the anti differential
EP-C5  exact primary and dual anti-periods
EP-C6  residue four and lateral/CPV bookkeeping
EP-C7  dual boundary chain and Borel--Moore surface lift
EP-C8  path-specific integral Picard--Lefschetz classes modulo A/B periods
EP-C9  CPV midpoint rational but nonintegral
EP-C10 boundary obstruction to absorbing i into an integral class
EP-C11 pole-free native evaluator for the two DBP claims

NO  primary plus dual form a complete period lattice
NO  the normalized dual class is an integral class modulo compact periods
NO  a second real or classically forbidden DBP surface region has been found
```
[GOVERNANCE-T61] Paper II remaining symbolic gates (S2 §3):
```
KN-G1  interior zero-exclusion / existence theorem
KN-G2  exact six-factor metric audit
KN-G3  nonremovable scalar-curvature pole theorem
KN-G4  extremal Sturm or exact noncancellation theorem
KN-G5  reflection residues
KN-G6  corner coefficients and specialization maps
```
[GOVERNANCE-T62] §7.3 Relative Trace-Path Equivalence gap — the elliptic (a,b,c) integers (S2 §7.3; **sole holder**):
```
E^o = E_128 minus {P,-P}
D   = {Q=(1,0), O}
H   = H_1(E^o,D;Z)
H = <A, B, mu, Gamma_+>.

[Gamma_-^up]   = [Gamma_+] + a[A] + b[B] + c[mu]
[Gamma_-^down] = [Gamma_+] + a[A] + b[B] + (c+1)[mu]

(up to the chosen meridian sign; the exact integers (a,b,c) are not yet known)

[Gamma_-^CPV]  = [Gamma_+] + a[A] + b[B] + (c+1/2)[mu].
```
S2 note: "This is a Relative Trace-Path Equivalence Theorem. It is not a claim that the two
numerical constants are scalar algebraic multiples of one another."
[GOVERNANCE-T63] Provisional coefficient-typed selected quotient object (S2 §6):
```
O_R = (
    base B,
    carrier X_R,
    groupoid G => X_R,
    quotient q: X_R -> |G|,
    admissible chamber C,
    selected section s,
    stratified wall W,
    boundary/stabilizer labels nu
)
```
with `R` one of `Z`, `Q`, or `C`; "provisional until the data-minimization theorem is proved."
[GOVERNANCE-T64] THEOREM E target (S2 §7.2; Paper V gate SQG-E):
```
THEOREM E — Common Quotient--Selection Skeleton and Strict
             Non-Equivalence of Full Carriers

1. The full local and global structured carriers are not equivalent.
2. Explicit reduction functors send them to a common selected quotient skeleton.
3. Those reduced presentations are equivalent in the selected quotient category.
4. The reduction is maximal: restoring the discarded account-fibre or
   root-label data destroys the equivalence.
```
Fibre-type evidence against full equivalence (S2 §7.1):
```
local channel account fibre  = positive-dimensional affine fibre ker(Sigma_r)
global horizon/root fibre    = generically finite discrete fibre
```
Morita preservation list: `quotient / admissible chamber / selected section / stabilizer-inertia
type / wall incidence / boundary normal-form label`.
[GOVERNANCE-T65] THEOREM C target (S2 §8; Paper V gate SQG-C):
```
THEOREM C — Coefficient-Typed Selected Quotient Closure

For each admissible coefficient ring R, selected quotient objects and
native morphisms form a category and are closed, under explicit hypotheses, under:
    identities and composition
    invariant-open restriction
    chamber restriction
    admissible base change
    quotient by a normal symmetry subgroupoid
    quotient by a saturated sub-local system
    transverse or compatible fibre product
    boundary specialization to typed wall strata
Selected sections remain branch-free on chamber interiors, while
stabilizer, inertia, wall, and valuation data specialize functorially at boundaries.
```
[GOVERNANCE-T66] Scalar-extension ladder (S2 §8):
```
SQG_Z  ->  SQG_Q  ->  SQG_C
integral lateral class      in SQG_Z
CPV midpoint                in SQG_Q but not SQG_Z
i-normalized class          in SQG_C but not SQG_Z
```
"Scalar extension is a functor. It is not an equivalence and need not admit descent."
[GOVERNANCE-T67] Elliptic closure below the capstone (S2 §8):
```
rho: pi_1(parameter base) -> Aut(H_1(E^o,D;Z))
```
on basis `(A,B,mu,delta)`; DBP relative periods form an affine torsor over
```
Z period_A + Z period_B + Z residue_period.
```
"The current Stage-3 theorem determines the lateral coset and residue column, not the complete
A/B monodromy matrices."
[GOVERNANCE-T68] R3 recommended candidate — lossless two-bus AC power-flow fold cover (S2 §9):
```
v^2 + (2 Q X - E^2) v + X^2(P^2 + Q^2) = 0.

Delta = (E^2 - 2 Q X)^2 - 4 X^2(P^2 + Q^2)
      = E^4 - 4 E^2 Q X - 4 P^2 X^2.

At no load, the roots are  v = E^2, 0
```
Realization data: `carrier = the two voltage sheets; symmetry = C2 sheet exchange; quotient =
polynomial coefficients / discriminant data; chamber = Delta > 0 with positive voltage;
selection = high-voltage branch continued from no load; wall = Delta = 0 saddle-node voltage
collapse; boundary type = square-root fold`.
[GOVERNANCE-T69] R3 independence criteria (S2 §9):
```
R3-1  its source equations are not a base change, quotient, isogeny,
      or reparameterization of an existing realization;
R3-2  its symmetry and wall structure are derived independently;
R3-3  its selection rule has an independent mathematical or physical origin;
R3-4  it realizes every required datum and a nontrivial native morphism;
R3-5  it has an interior branch-avoidance theorem and typed boundary form;
R3-6  it produces at least one prediction not inserted into the axioms;
R3-7  membership is proved without using the conjectural capstone theorem.
```
Plus the S2 §9 warning: the elliptic transport system "should therefore not be used by itself to
discharge the independent-third gate" (derived via link quotient / elliptic isomorphism / isogeny
/ surface lift).
[GOVERNANCE-T70] Groupoid typing of the three arms (S2 §6):
```
role recharting        -> partial rational / etale groupoid
horizon continuation   -> covering and monodromy groupoid
elliptic continuation  -> fundamental groupoid acting on a
                          relative-homology local system
```
[GOVERNANCE-T71] Release boundary and Paper V gates (S2 §12):
```
RELEASE-INDEPENDENT:  Paper I, Paper II (once symbolic gates close),
                      Paper III (after consolidation), Paper IV
HOLD:                 Paper V
PAPER V RELEASE GATES:
  SQG-E   equivalence / strict non-equivalence theorem
  SQG-C   categorical closure theorem
  R3      independently sourced third realization
```

### 2.9 DAG / provenance constants (S1 §1 — needed to freeze authority lineage)

[GOVERNANCE-T78] Weighted-monodromy paper registration:
```
artifact PAP-0509;  DAG node DBP:paper:weighted_multiquadratic_monodromy;
46,909 bytes;  source digest 3cefa244a61d701a9f0184ae5756e62c71efbbb7f30274ca12f951ae351df6fd
```
Declared relations (verbatim): supersedes `DBP:note:allk_monodromy` as proof authority;
supplements released Paper IV with the arbitrary-k, arbitrary-nonzero-weight base theorem;
cites `DBP:proof:gs_morse` as a retained proof source; supplements `DBP:thm:kummer_wreath_lift`
by fixing its exact square-class/rank interface.
[GOVERNANCE-T79] Canonical DAG revisions (`cella-dbp-frontier`):
```
sha256:acd9d4c392fb9e65353db0d4a35d82dcb69f5e1ef913dc99435cd1254fe39ca3
  -> sha256:becb3d9136f4dea9314b48b768ed114c861aeccfce28d847d4354f261494a272   (paper admission)
  -> sha256:00ef143b0e00f29f8a8f97ee4583907262db1c829ff6ba8c236cb71a3719fec1   (status cleanup;
     resolved gaps IV1, IV4, IV5; removed two obsolete opens_gap edges)
graph at that point: 2,294 nodes / 4,311 edges / 0 errors / 0 warnings
k=5 certificate notice: artifact PAP-0083, empty graph impact, revision unchanged
PAP-0513 = ALL_K_TWO_RADICAL_KUMMER_CLOSURE_v1.0 (node DBP:paper:all_k_two_radical_kummer_closure; closes DBP:gap:IV3)
```
[GOVERNANCE-T80] Corpus counts: catalogue snapshot `508 unique artifacts / 547 origin paths / 39
byte-mirrors / 219 binding relationships`; effective current corpus `513` after PAP-0509..PAP-0513
(LEDGER not yet rebuilt — see RF10). DBP census: 115/57/24/82/62 per family, `340 in the
adjudicated census snapshot`.

---

## 3. CONVENTIONS

- **Sector index:** ε ∈ {+,−}; subscripted objects `m₊/m₋`, `B₋`, `R₊=4i / R₋=4`, `P₊/P₋`.
- **Lateral-correction sign convention (CCE-5):** `λ↑ = B₋`, `λ↓ = −B₋` (up positive, down
  negative). NOTE: S3 writes this as `lambda_up = B`, `lambda_down = -B` without the minus
  subscript — see RF12.
- **Trace-path coefficient tuple order:** `(a,b,c)` in the expansion
  `[Γ] = [Γ₊] + a[A] + b[B] + c[μ]` over the fixed integral basis `H = <A, B, μ, Γ₊>`
  (closure-theorem basis is `(A,B,μ,δ)`). Fixed-curve comparison value `(a,b,c) = (1,0,0)`;
  CCE-5 trace coordinates quoted as `(1,0,0)/(1,0,1)` (up/down); CPV midpoint shifts μ-coefficient
  by `+1/2`. Meridian sign is "up to the chosen meridian sign".
- **Period sign/normalization:** primary anti-period `−4π`; dual CPV `0`; one-sided `±4πi`;
  difference `8πi`; residue `4`; transfer normalization `R_ℤL_ℤ = 4·id`.
- **Coefficient-ring ladder:** `Z → Q → C` (SQG_Z → SQG_Q → SQG_C); coefficient diamond
  `ℤ / ℤ[½] / ℤ[i] / ℤ[½,i]`. Coefficient ring is part of every ledger entry (S2 §11).
- **Channel naming/order:** `K_G = κc + κint + κs` (curvature, interaction, self); named channels
  ordered `Λ_P, Λ_D, Λ_S` with Jacobian `det = 8Λ_PΛ_DΛ_S/q₀⁶`; channel normalization
  `σ_r = Ĉ_r(1,1)/q^{(r+2)/2}`; keystone evaluation point `(1,1,1)`.
- **Lorentzian signature convention:** `Δc = ν^T(2I−J)ν` has signature `(2,1)` with
  `ν = (g₁H₂₃, g₂H₁₃, g₃H₁₂)`.
- **Signed-contact rows (all-k Kummer closure):** universal rows `(1,0)` and `(1,1)`; rank `2δₖ`;
  wreath closure written `C₂² wr S_{δₖ}` (generic-weight form `C₂^s wr S_{d(c)}`).
- **Degree symbols:** `d(c)` = weighted signed-pair degree `#{ {η,−η} : Σηᵢcᵢ ≠ 0 }`;
  `δₖ` = exact signed-pole degree of the equal-weight DBP specialization.
- **Theorem-family prefixes (spine ledger, S2 §11):** `RC-*` role-cover, `KN-*` Kerr–Newman,
  `EP-*` elliptic periods, `HC-*` horizon-cover, `SQG-*` selected quotient groupoids, `R3-*`
  independent third realization. Gap IDs used by S1: `DBP:gap:I1..I3, III1..III4, IV1..IV5, V1`;
  ledgers `P8-01..P8-21`, `AR-01..AR-26`; closed-result IDs `EP-C1..EP-C11`; gates `KN-G1..G6`.
- **Disposition vocabulary:** exactly one primary disposition per artifact, from the 10-value
  list [GOVERNANCE-T74]. "Retire" = eligible for historical archive after maintainer review,
  never deletion. Hashes are byte evidence only, never mathematical evidence or release gates.
- **Library naming:** `__<hash>` filename suffix = collision-rename for same-basename,
  different-content origins (kept side by side, never overwritten). Un-suffixed copy is canonical
  in every resolved twin of S1 §5(c) except the spine draft, where the **"(2)" copy** is canonical.
- **O_R tuple order (S2 §6):** `(base B, carrier X_R, groupoid G⇒X_R, quotient q, admissible
  chamber C, selected section s, stratified wall W, boundary/stabilizer labels ν)`.
- **Tier layout:** `subject_family × category tier` (`01_completed_papers` …
  `09_historical_and_superseded_versions`).

---

## 4. UNIQUE MATERIAL (exists ONLY in these governance documents — must not be lost)

1. **The per-artifact disposition tables themselves** (S1 §4–§10): the only place every DBP
   artifact carries an adjudicated disposition, with variant-twin resolutions (§5c), the
   two-and-only-two MERGE_THEN_RETIRE transfers ([GOVERNANCE-T57]/[T58]), and the
   HISTORICAL_ONLY successor evidence table.
2. **Paper V gate spec** ([GOVERNANCE-T64], [T65], [T71]) and the **§7.3 elliptic (a,b,c) gap**
   ([GOVERNANCE-T62]) — S2 is flagged by S1 as the **sole holder**; "orphan risk if retired…
   Retiring any of these would silently close open problems."
3. **EP-C1..EP-C11 closed-result registry + the three settled negatives** ([GOVERNANCE-T60]) and
   **KN-G1..KN-G6 gate list** ([GOVERNANCE-T61]) — only enumerated in S2.
4. **R3 independence criteria R3-1..R3-7 and the AC power-flow candidate dossier**
   ([GOVERNANCE-T68], [T69]) — only in S2.
5. **The open-wall registry that survives consolidation** (S1 §12, 7 walls, each pinned to its
   sole specifying source — incl. off-diagonal covariance at
   `LEAD7_VARIABLE_TRANSVERSE_WEIGHTED_JET_THEOREM_v1.0.md:96`, CCE-8 finite-tower fence at
   `:42`, rank-4-in-12, primary↔dual Landen target, CCE-7 braid residual, P8-17/P8-18).
6. **The safe merge order** (S1 §13, 6 steps) and **post-consolidation directory architecture**
   (S1 §14), incl. the "single most important move": promote Paper III from tier 05 to
   `01_completed_papers/dbp_periods_landen_and_elliptic_structure/`.
7. **DAG lineage constants** ([GOVERNANCE-T78]–[T80]): PAP-0509/PAP-0513/PAP-0083 registrations,
   the three `cella-dbp-frontier` sha256 revisions, node/edge counts, gap closures IV1/IV3/IV4/IV5,
   and the declared supersession relation over `DBP:note:allk_monodromy`.
8. **The subsumption test and disposition vocabulary** ([GOVERNANCE-T72]–[T74]) — the audit
   method itself lives only in S3 (restated in part by S1).
9. **The verifier-shim defect record and its fix** (RF1 below) — recorded only in S1 §9.
10. **Consistency attestations** (S1 §11): "No mathematical contradictions were found," with the
    named cross-checked constants (`κc=−1/49, κs=1/49, κint=−3/49`; `det=8Λ_PΛ_DΛ_S/q₀⁶`;
    residue 4; `−4π/±4πi/8πi`; `R_ℤL_ℤ=4·id`; `Ŝ₊Ŝ₋=P`).

---

## 5. RED FLAGS

- **RF1 — Broken verifier shim (the audit's flagged reproducibility defect).** S1 §9, verbatim:
  ```
  Reproducibility defect flagged (not a math issue):
  07_…/local_curvature…/lead7_variable_transverse_weighted_jet.py shims to a
  parents[1]/…/CELLA_CONTINUATION_ENGINE/… path that does not exist under the
  Papers_Library layout; the real verifier sits beside it. Fix the runpath to
  Path(__file__).with_name(...).
  ```
  Correct fix: replace the `parents[1]/…/CELLA_CONTINUATION_ENGINE/…` shim with
  `Path(__file__).with_name(...)` so the script resolves the verifier sitting in its own
  directory. Reiterated in S1 §13 step 3 ("Fix the broken verifier runpath").
- **RF2 — Historical roadmaps/ledgers must never be cited as proof authority.** The unified
  spine (any version) is "a ledger, not a sixth proof source" and "must never be cited as the
  proof source" ([GOVERNANCE-T75]/[T76]); `Local_Curvature_Calculus_for_Inverse-Channel_Metrics.txt`
  is a Stage 1–10 roadmap, HISTORICAL_ONLY, "no unique math"; `GALOIS_K_ELLIPSE_RESEARCH_MAP_v1_6`
  is a dashboard, not proof authority; applied insertion notes are provenance only. S3 principle 2:
  "Campaign status prose does not" determine succession.
- **RF3 — Spine filename naming trap.** `DBP_UNIFIED_THEOREM_SPINE_DRAFT_v0_1 (2).tex` is the
  NEWER v0.3 (internal `\date{}` 13 Jul); the plain-named `.tex` is the OLDER v0.2 (10 Jul).
  "filename is a naming trap."
- **RF4 — Stale research-map citations.** The brief and the Encyclopedia cite
  `GALOIS_K_ELLIPSE_RESEARCH_MAP` v1_4, which is **stale**; live disk head is v1_6 (verified newest).
- **RF5 — Date-based, not byte-verified disposition.** `lead7_kn_n3_dbp_metric_v2.pdf` is filed
  SUPERSEDED_VARIANT on file dates only (Jul 7 vs Jul 13); "label misleading; not byte-verified —
  flagged." Byte-verify before filing (S1 §13 step 3).
- **RF6 — Paper V does not exist.** It is a held conjecture; foundations proved, but SQG-E,
  SQG-C, and R3 gates are open. Never cite Paper V as a paper, and the capstone conjecture must
  never prove a component realization.
- **RF7 — Do not relabel the native image as the whole surface lattice.** Native transfer exact
  only on `im L_ℤ` (rank ≤ 4) inside `rank H₂ = 12`; `¼R_ℤ` not claimed integral; whole-surface
  surjectivity REFUTED by the rank 4-in-12 obstruction; saturation/Smith/Landen/transcendence open.
- **RF8 — DUAL_CONSTANT_CLOSEOFF misfile.** The `cella_residue` copy is a misfiled OLDER revision
  (no §4A); the `dbp_role_channel` copy is canonical (two agents concur).
- **RF9 — Paper III tier misfiling.** The canonical Paper III sits in `05_expository_companions`,
  not `01`/`02`; CCE-2/5/6 theorem files are dual-filed (byte-identical) in `02_theorems…` and the
  live campaign; `docs/files/` holds an older byte-identical Galois drop.
- **RF10 — Stale catalogue counts.** `_catalogue/LEDGER` still reports the 2026-07-15 snapshot
  (508 artifacts); effective corpus is 513 after PAP-0509..PAP-0513. Refresh before publication.
- **RF11 — Paper IV publication-integration debt (reserved for maintainer k=4 work).** The
  released Paper IV TeX/PDF/package does NOT yet cite or absorb the weighted all-k paper; the
  supersession of the ALL_K note is real, but the render set must be revised as one unit.
  Publication integration, not open mathematics.
- **RF12 — λ notation discrepancy between S3 and S1.** S3 writes `lambda_up = B, lambda_down = -B`;
  S1/CCE-5 give `λ↑ = B₋, λ↓ = −B₋` (sector-subscripted). Treat the CCE-5 theorem file as the
  formula authority; the S3 form drops the `₋` subscript.
- **RF13 — Truncated formula in the governance layer.** [GOVERNANCE-T23] `C_Ω` denominator appears
  only as `/[…]` in S1. The governance documents are disposition authority, NOT formula authority;
  pull the full `C_Ω`/`C_Φ` expressions from `lead7_kn_n3_dbp_metric.tex:481`.
- **RF14 — Scope fence on the all-k Kummer closure.** The `C₂² wr S_{δₖ}` closure is all-k
  algebra, but "its physical entropy reading is asserted only at k=4." Do not propagate the
  entropy interpretation to general k.
- **RF15 — Encyclopedia is pre-reorg.** Its `audit/` tree references pre-reorg
  `cella:research/paper/…` origins; used only as a content scaffold. All dispositions anchor to
  live Cella `Papers_Library` (constraint C-003 re-verification rule). Never freeze authority
  from Encyclopedia paths.
- **RF16 — Orphan risk on sole-holder ledgers.** `DBP_PAPER_ENSEMBLE_ARCHITECTURE_v1.0.md`
  (Paper V gates + §7.3 (a,b,c) gap), `POST_8_OUTCOME_GAP_LEDGER` (P8-01..P8-21), and
  `DBP_CCE_ARTIFICIAL_RESTRICTION_LIVE_RECONCILIATION` (AR-01..AR-26) are sole enumerations of
  live gaps; retiring any would silently close open problems. Architecture may be reclassified
  historical only at S1 §13 step 6, after its gate spec is preserved in a successor.
- **RF17 — Sole-proof-authority hazards before transfer.** Paper I units U10/U11 live only in
  `Canonical_Invariant_Reduction_Theorem.md` / `Gauge_Channel_Transport_Law.md` /
  `GAUGE_NORMAL_FORM_PROOF.md` ("do not retire before transfer"); Paper III delegates proofs to
  the stage dossiers and CCE-5/6 theorem files. Freezing those files' authority is mandatory.
- **RF18 — S2 is a frozen plan partially outrun by S1.** S2 (2026-07-14) still describes CCE-5/6
  insertion, gap closures, and the weighted paper as future work; S1 (through 2026-07-18) records
  them executed. For any AUTHORITY_FREEZE conflict, S1's executed state supersedes S2's plan;
  S2 remains authoritative only for the Paper V gates, EP-C/KN-G registries, R3 criteria, and
  the §7.3 gap.
