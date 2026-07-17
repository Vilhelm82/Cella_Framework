# DBP Paper Succession and Redundancy Map v1.0

**Original audit date:** 2026-07-15  
**Updated through:** 2026-07-17 (weighted all-\(k\) monodromy succession and DAG admission)  
**Scope:** the DBP-related paper and theorem corpus across the Cella Framework and Lloyd
Mathematics Encyclopedia repositories.
**Nature:** repository-led succession audit, followed by a non-destructive session update. The
original 2026-07-15 audit was read-only. The 2026-07-16/17 update added one completed paper and
admitted it through the transactional Cella DAG submission path; no prior paper was edited,
moved, retired, or deleted. "Retire" throughout means *eligible to move to a historical archive
after maintainer review*, never automatic deletion.

This report is self-contained. It answers one question per artifact: **does a newer canonical
paper preserve every mathematical contribution of an older document, under the same or weaker
hypotheses, while adding stronger results — so the older document has no remaining unique
mathematical, proof, computational, or expository value except historical provenance?**

---

## 1. Repository and corpus snapshot

| Repository | Root | Branch | HEAD | Status |
|---|---|---|---|---|
| Cella Framework | `/home/williaml/Cella Framework` | `main` | `42259fd` | dirty (preserved; see below) |
| Lloyd Mathematics Encyclopedia | `/home/wlloyd/Lloyd_Mathematics_Encyclopedia` | `main` | `8a203af` | clean |

- At the original audit, the handoff's expected Cella commit `4f016aa` was HEAD exactly and
  Encyclopedia `c964366` was an ancestor of HEAD `8a203af`. The live Cella checkout is now at
  `42259fd`; the paper, DAG admission, receipt, and this map update are uncommitted session work.
- Cella dirty worktree (all pre-existing work **preserved**): `M STATE/CONSTRAINTS.md`; untracked
  library and campaign regions. Session additions are confined to the weighted paper, canonical
  DAG admission/submission/receipt, and this `research/campaigns/Succession_Map/` document.
- **Maintainer note applied:** the Encyclopedia is **not yet updated for the Cella reorg /
  taxonomy**. Its `audit/` tree (spine + gapfill unit extractions, `relations.json`,
  `maintainer_rulings.md`, `synthesis.json`) references pre-reorg `cella:research/paper/…`
  origins. It was used **only** as a mathematical-content scaffold and relationship-hypothesis
  source; every disposition and path in this report is anchored to the **live Cella
  `Papers_Library`** and re-verified on the Cella side (constraint C-003, re-verification rule).

### Canonical library

`Papers_Library/` is a **non-destructive union library** built by
`Papers_Library/_catalogue/build_library.py` from both the Cella Framework and Lloyd_Engine_V4
trees. Its catalogue reports **508 unique artifacts** from **547 origin paths**, with **39 exact
byte-mirrors** collapsed and **219 binding relationships** (certificate / render-pair /
embedded-digest). Layout is **subject_family × category tier** (`01_completed_papers` …
`09_historical_and_superseded_versions`). The `__<hash>` filename suffix is the library's
collision-rename for two origins that share a basename but differ in content — preserved side by
side, never silently overwritten.

A prior consolidation (`_catalogue/RETIREMENT_DELETION_RECEIPT.md`, 2026-07-15) deleted **only 9
byte-identical loose originals** (35,801 B) after verifying library copies + no inbound
references. **No mathematical retirement has occurred.** This audit sits *above* the library's
byte-level dedup: the library resolved exact mirrors and render pairs; succession is a
mathematical relation the byte layer cannot decide.

### Post-audit corpus delta — 2026-07-16/17

The session added the completed paper
`GENERIC_SYMMETRIC_MONODROMY_OF_WEIGHTED_MULTIQUADRATIC_SUMS_v1.0.md` under
`01_completed_papers/galois_horizon_and_kummer_covers/`. It is 46,909 bytes, has source digest
`3cefa244a61d701a9f0184ae5756e62c71efbbb7f30274ca12f951ae351df6fd`, and is registered as
artifact `PAP-0509` and DAG node `DBP:paper:weighted_multiquadratic_monodromy`.

The transactional admission advanced `cella-dbp-frontier` from revision
`sha256:acd9d4c392fb9e65353db0d4a35d82dcb69f5e1ef913dc99435cd1254fe39ca3` to
`sha256:becb3d9136f4dea9314b48b768ed114c861aeccfce28d847d4354f261494a272`.
The applied submission is
`DAG_Library/submissions/applied/submit-weighted-multiquadratic-monodromy-v1-0.json`; its receipt
is `DAG_Library/receipts/submit-weighted-multiquadratic-monodromy-v1-0.receipt.json`.
The follow-up status cleanup advanced the graph again to
`sha256:00ef143b0e00f29f8a8f97ee4583907262db1c829ff6ba8c236cb71a3719fec1`, resolved DAG gaps
IV1, IV4 and IV5, and removed their two obsolete `opens_gap` edges. Its applied submission and
receipt are `DAG_Library/submissions/applied/submit-paper-iv-status-cleanup-2026-07-17.json` and
`DAG_Library/receipts/submit-paper-iv-status-cleanup-2026-07-17.receipt.json`.
The final `k=5` certificate notice was admitted as artifact `PAP-0083` by the artifact-only
submission `submit-k5-certificate-succession-notice-2026-07-17`; its graph impact was empty, so
the canonical revision correctly remained unchanged. The applied record and receipt are
`DAG_Library/submissions/applied/submit-k5-certificate-succession-notice-2026-07-17.json` and
`DAG_Library/receipts/submit-k5-certificate-succession-notice-2026-07-17.receipt.json`.
The live graph validates at **2,294 nodes / 4,311 edges / 0 errors / 0 warnings**. Its four
declared relations say that the new paper:

- **supersedes** `DBP:note:allk_monodromy` as proof authority;
- **supplements** released Paper IV with the arbitrary-\(k\), arbitrary-nonzero-weight base
  theorem;
- **cites** `DBP:proof:gs_morse` as a retained proof source; and
- **supplements** `DBP:thm:kummer_wreath_lift` by fixing its exact square-class/rank interface.

The `_catalogue/LEDGER` has not yet been rebuilt, so its 508-artifact figure remains the
2026-07-15 generated snapshot. Counting the admitted paper gives an effective current corpus of
**509 unique artifacts**; generated catalogue totals should be refreshed before publication.

### DBP-relevant census

Five subject families carry the DBP ensemble. Deduplicated by content:

| Subject family | Paper | Unique artifacts |
|---|---|---:|
| `dbp_role_channel_and_orbit_geometry` | Paper I + spine/ensemble | 115 |
| `local_curvature_and_black_hole_metrics` | Paper II | 57 |
| `dbp_periods_landen_and_elliptic_structure` | Paper III | 24 |
| `galois_horizon_and_kummer_covers` | Paper IV + weighted all-\(k\) successor | 82 |
| `cella_residue_and_coupling_theory` | Paper V / cross-program | 62 |
| **Total** | | **340 unique** (339 in the generated ledger + post-audit `PAP-0509`) |

Generated-snapshot extension mix (before `PAP-0509`): 165 `.md`, **87 `.py`** (verifiers → computational supplements), 27
`.json`, 24 `.txt`, 13 `.pdf`, 9 `.tex`, 9 `.m2`, 3 `.zip`, 2 `.bak`. Roughly **79 distinct
mathematical units** were extracted and adjudicated across the five families; the new Markdown
paper is the 166th effective `.md` artifact and adds the weighted all-`k` proof unit described
below.

### The other three library regions are binding/mirror infrastructure, not independent math

- **`Reports_Library`** (954 rows): role-tagged report copies; 158 bound to
  `paper_artifact_ids`, 392 to `campaign_ids`.
- **`Campaign_Library`** (952 rows): **176 are literal `papers_library_symlink`** to
  Papers_Library; 776 are campaign-internal clones.
- **`Evidence_Store`** (3017 rows): a byte-hash evidence registry; every `authority` value is a
  `*_reference` or `*_retirement_source` label (Lloyd_Engine_V4 retirement + Cella references) —
  **never canonical**.

These three are dispositioned **as a class** (§5), not row-by-row: their catalogue LEDGERs are
the evidence that each entry mirrors or binds a Papers_Library / campaign artifact already
adjudicated here.

---

## 2. Canonical paper ensemble after the audit

```
                         DBP PAPER ENSEMBLE (post-audit)
                         ═══════════════════════════════

 Paper I  ── Active Role-Jet Orbit Calculus ................ dbp_orbit_calculus.tex   [RELEASED]
   │         (S3 birational action, Orbit Thm, 3-channel K_G split, gauge transport)
   │         companion: theorem_8_1.tex (abstract Invariant-Preservation)
   │         strengthened across the finite truncation tower by CCE-8 naturality
   │
 Paper II ── Local Curvature Calculus ..................... TWO independent papers   [RELEASED]
   │         general theory:  pfc_normal_forms.tex   ⟵ cites ⟶   KN realization: lead7_kn_n3_dbp_metric.tex
   │         full proof spine: LOCAL_CURVATURE_CALCULUS_COMPLETE_v1.0.md (superset of pfc)
   │         newest strengthening: LEAD7_VARIABLE_TRANSVERSE_WEIGHTED_JET_THEOREM_v1.0
   │
 Paper III ─ DBP Curvature Periods of the DBP Quadric ..... DBP_CURVATURE_PERIODS_…_v1.0.md
   │         (Landen–Trace, native route, surface-to-link, dual-surface Stages 1–3, CCE-2)   [CONSOLIDATED,
   │         ⚠ contains CCE-2 but NOT CCE-5 / CCE-6 — two proven theorems await insertion]     INCOMPLETE]
   │
 Paper IV ── Galois Theory of the Horizon Cover .......... galois_horizon_cover_v1_0.tex + pub package  [RELEASED]
   │         (splitting/temperature, S5 obstruction, Kummer modules, wreath closures, realization poset)
   │         all-k successor: GENERIC_SYMMETRIC_MONODROMY_OF_WEIGHTED_MULTIQUADRATIC_SUMS_v1.0.md [RELEASED]
   │         (arbitrary nonzero weights, exact degree/genus/ramification, generic geometric + arithmetic S_d)
   │         independent companion: self_glue_monodromy.tex (imprimitive wreath monodromy)
   │         retained development sources: ALL_K_MONODROMY_NOTE + GS_GENERIC_MORSE_LEMMA_PROOF
   │         remaining all-k wall: concrete Kummer/crown square-class independence R=0
   │
 Paper V  ── Selected Quotient Groupoids (capstone) ....... DOES NOT EXIST — held conjecture   [NOT A PAPER]
             foundations proved & on disk: SQG foundation, R3 AC-fold realization, CCE-8
             gates open: DBP-arm reduction functors, three-way coherence, general closure
             sole gate/gap spec: DBP_PAPER_ENSEMBLE_ARCHITECTURE_v1.0.md  (must be retained)
```

**Headline facts the audit establishes or corrects:**

1. **Paper I** — `dbp_orbit_calculus.tex` is the released, standalone canonical paper. The
   frozen `DBP_PAPER_ENSEMBLE_ARCHITECTURE_v1.0.md` marks it `RELEASE-INDEPENDENT` and rules the
   unified spine an *internal ledger, "never cited as the proof source."*
2. **Paper II is two independent companion papers** (hypothesis confirmed): `pfc_normal_forms`
   (general theory) and `lead7_kn_n3_dbp_metric` (Kerr–Newman realization). KN cites pfc, not
   vice versa. Neither subsumes the other.
3. **Paper III exists on disk but is mathematically incomplete**: it consolidates the Landen–
   Trace theorem, native route, surface-to-link close-off, dual-surface Stages 1–3, and CCE-2,
   but it still records λ↑/λ↓ as *unresolved* (§7F.10, verified live at line 1543) and carries an
   informal *"choose thin tubular neighbourhoods"* (§7F.5, line 1559). The **CCE-5** calibration
   (λ↑=B₋, λ↓=−B₋; (a,b,c)=(1,0,0)) and **CCE-6** sweep-clearance theorem resolve exactly these
   and are proven — but live *outside* Paper III.
4. **Paper IV** — `galois_horizon_cover_v1_0` + its byte-identical publication package remains
   the released case-specific paper. The new weighted paper is the canonical reusable successor
   for its base-monodromy front: it proves the exact degree, genus and ramification, and generic
   geometric and arithmetic `S_d` for every `k≥3` and every fixed nonzero weight vector. The
   older ALL_K note is superseded as proof authority but retained for development provenance and
   low-`k` computations. Maximal Kummer/wreath closure is still conditional on proving `R=0` for
   the concrete conjugate radicands.
5. **Paper V does not exist.** It is a held capstone conjecture; its foundations (SQG category, R3
   realization, CCE-8) are proved, but the equivalence/closure/coherence theorems are open.

---

## 3. Theorem-level succession matrix

Each row: a mathematical unit, its current home, and where a canonical successor preserves it.
`✅` preserved with proof; `⚠` statement absorbed but proof delegated to a retained supplement;
`❌` **not yet** in the family's canonical paper (successor is a separate on-disk theorem).

### Paper I — role covers & active recharting

| Unit | Statement (exact where it matters) | Source | Successor |
|---|---|---|---|
| Active role S₃ | `s(a,b)=(b,a)`, `t(a,b)=(1/a,−b/a)`; `s²=t²=(st)³=e`; birational on regular jets | `dbp_orbit_calculus.tex:131` | ✅ orbit_calculus |
| Orbit theorem | φ order-r DBP-invariant ⟺ factors through `X_r/S₃` | `:187` | ✅ orbit_calculus §4 |
| Exact rational closure | `J_r∈ℚ ⇒ G·J_r ⊂ ℚ[Δ⁻¹]` | `:221` | ✅ §5.2 |
| Channel reduction / exact sequence | `σ_r=Ĉ_r(1,1)/q^{(r+2)/2}`; `0→kerΣ→C_r→I_r→0` | `Canonical_Invariant_Reduction_Theorem.md`; `:259` | ✅ §6 |
| Gaussian 3-channel | `K_G=κc+κint+κs`; graph gauge `κc=−M²/Q², κs=LN/Q², κint=0` | `:274` | ✅ §6.3 |
| Named channels / faithfulness | `Λ_P=B, Λ_D=(Ab−aB)/a, Λ_S=(Ca−bB)/b`; Jacobian `det=8Λ_PΛ_DΛ_S/q₀⁶` | `:336` | ✅ §7 |
| Keystone | at (1,1,1): `κc=−1/49, κs=1/49, κint=−3/49, K_G=−3/49` | `:485` | ✅ App.B |
| Lorentzian coupling-edge lemma | `ν=(g₁H₂₃,g₂H₁₃,g₃H₁₂)`, `Δc=ν^T(2I−J)ν` signature (2,1) | `Gauge_Channel_Transport_Law.md`; `Canonical_Invariant_Reduction_Theorem.md` | ⚠ **proof-supplement only** |
| Gauge-normal-form quotient | unique `H⊥`, `Sym₃/Im(G_g)≅ℚ³` | `GAUGE_NORMAL_FORM_PROOF.md` | ⚠ **proof-supplement only** |
| Invariant-Preservation 8.1 | additive `φ=φ_K+φ_sym`; κ=0/κ>0 dichotomy | `theorem_8_1.tex:94` | companion (abstract form) |
| CCE-8 finite-tower naturality | `τ_{N,r}(w·f)=w·τ_{N,r}(f)`, all finite N≥r≥2 | `CCE_8_FINITE_TOWER_NATURALITY_THEOREM_v1.0.md` | strengthens the S₃ action across the truncation tower |

### Paper II — local curvature & Kerr–Newman

| Unit | Statement | Source | Successor |
|---|---|---|---|
| Lamé diagonal curvature engine | `R=−2Σ_{i<j}(1/H_iH_j)[∂β+∂β+Σββ]` | `LOCAL_CURVATURE_CALCULUS_COMPLETE_v1.0.md §2` | ✅ canonical |
| Divisor-channel decomposition | `R=Σ z^{−P_a−2e_a}F_a+Σ z^{−P_μ}F_μ` | `COMPLETE Thm 3.1` | ✅ canonical |
| Generic quadratic collapse (ord 3) | `R=(1/A)Σ(P_{α1}/P_{α0})x⁻³+O(x⁻²)` | `pfc_normal_forms.tex:94`; `COMPLETE 5.2` | ✅ canonical |
| Parity-fixed reflection (ord 4) | `R=−m(m+5)/B·x⁻⁴`; `m=2→−14/B` | `pfc_normal_forms.tex:53` | ✅ canonical |
| Corner vertex rule (closed) | `A=−p₀²+p₀p₁−p₀p₂+2p₀+p₁p₂−p₂²+2p₂` | `pfc_normal_forms.tex:151`; `COMPLETE 7.4` | ✅ canonical |
| Variable-transverse weighted jet | leading laws hold with arbitrary (y,z)-functions; **no transverse derivative in leading coeff** | `LEAD7_VARIABLE_TRANSVERSE_WEIGHTED_JET_THEOREM_v1.0.md` | ✅ canonical (nondegenerate stratum `P1/P0+R1/R0≠0`) |
| DBP metric selection | `u=0` unique pos-def + interior-regular member on `W₊` | `lead7_kn_n3_dbp_metric.tex:267` | ✅ canonical |
| Mass-role zeros = role divisors | singular support ⊆ `{J=0}∪{Q=0}∪{U_S=0}` | `LEAD7_masscharge_zeros_theorem.md`; KN `:375` | ⚠ paper states; fuller proof in supplement |
| Reflection coefficients | `C_Ω=−3584 Q²S⁵π³(S−πQ²)²/[…]`; `C_Φ` analogous | KN `:481` | ✅ canonical |
| Strict-negative extremal coeff | `C_ext<0` on whole open edge (two Sturm counts) | KN `:567` | ✅ canonical |
| n=3 complementarity | `T=0→3, Ω=0→4, Φ_e=0→4`; Schwarzschild corner min 2 | KN `:649` | ✅ canonical |

### Paper III — DBP elliptic periods, cycles, continuation (absorption table)

| Unit | Statement (constants) | Current source | In canonical Paper III? |
|---|---|---|---|
| Complementary params / involution | `mε=(2−εs)/4 … Bε=2+2εs`; `m₊+m₋=1, m₊m₋=1/8` | Paper III §1 | ✅ (= Landen v1.1 §1) |
| Degree-2 isogenies → E₁₂₈ | `j(Cε)=10976, j(E₁₂₈)=128, Φ₂=0` | §2 | ✅ |
| Common trace differential Θ | `Θ=8·(X−3)/(X+7)·dX/Y` | §3 Thm 3.1 | ✅ |
| Exact logarithmic anti-differential | `αε=Rε·dlog fε`; `R₊=4i, R₋=4` | §5 Thm 5.1 | ✅ (**MR-002 corrected sector present**) |
| Primary/dual anti-periods | primary `−4π`; dual CPV `0`; one-sided `±4πi`; diff `8πi` | §6 | ✅ |
| Native pole-free kernels | `P₊=t⁴+2t²w²+2w⁴`; `A²−2P₋=−t²D` | §7E Thm 7E.1 | ✅ full proof in III |
| Native morphism / signed transfer | `R_ℤL_ℤ=4·id`; coeff diamond `ℤ/ℤ[½]/ℤ[i]/ℤ[½,i]` | §7F Thm 7F.1 | ✅ |
| Primary surface→link→period | `∫_{S₁}K_G dA=−2L(Γ₁⁺)=I_primary` | §7A | ⚠ statement; boundary proof in `DBP_SURFACE_TO_LINK_CLOSEOFF_v1.0.md` |
| Dual boundary + surface-cycle lift + PL transport | `𝓑₋`, `L_ℤ`, `δ₋↑−δ₋↓=−μ₋` | §7B/7C/7D | ⚠ statements; proofs in Stages 1/2/3 (gates 22/17/22) |
| Exact corridor reps (CCE-2) | words `a₊ / a₋⁻¹`; radius-1/8 tube; 29-disk cover | §7F Lemma 7F.A | ⚠ statement; segment/disk proof in `DBP_EXACT_CORRIDOR_POSITIVE_CLEARANCE_THEOREM_v1.0.md` |
| **λ resolution + braid matrices (CCE-5)** | **λ↑=B₋, λ↓=−B₋**; `M↑/M↓`; `(a,b,c)=(1,0,0)` | `DBP_CCE5_ABSOLUTE_CALIBRATION_THEOREM_v1.0.md` | ❌ **NOT in Paper III** (III §7F.10 unresolved) |
| **Native surface-sweep clearance (CCE-6)** | `Disc_Ξ(N)=−4(1−c)TD₂`; `Res=c²D₁²`; `ε∗=1/105186307200` | `DBP_NATIVE_SURFACE_SWEEP_CLEARANCE_THEOREM_v1.0.md` | ❌ **NOT in Paper III** (III §7F.5 informal thin-tube) |
| Dual constant closed form + branch | `I_dual=−2^{7/4}[K(k′²)−(3−2√2)Π(2√2−2;k′²)]`; PSLQ refutes lattice completion | `DUAL_CONSTANT_CLOSEOFF.md` (dbp_role_channel) | ⚠ branch in III §6/§8; closed form + certs unique to close-off |
| Rank obstruction | `rank H₂(X,Y;ℤ)=12, rank im L_ℤ≤4` | `CCE_6_WHOLE_SURFACE_TOPOLOGY_OBSTRUCTION_v1.0.md` | ❌ open-wall record, unique |

### Paper IV — Galois horizon & Kummer covers

| Unit | Statement | Source | Successor |
|---|---|---|---|
| Splitting–temperature | roots of `z²−e₁z+e₂`, `e₁=2π(2M²−Q²)`, `e₂=π²(4J²+Q⁴)`; `Θ=S·T` Galois-odd | `galois_horizon_cover_v1_0.tex:248` | ✅ paper |
| Area-product invariant | `Ŝ₊Ŝ₋=P` | `:385` | ✅ paper |
| S₅ obstruction | quintic norm generic `S₅` ⇒ Abel–Ruffini non-solvable | `:435` | ✅ paper |
| Conjugate Kummer module / wreath lift | Thm 3.1/4.1/5.1/6.1 + Cor 6.2 | `KUMMER_MODULE_WREATH_LIFT_THEOREM…md` | ⚠ paper `:574` states; proof in supplement |
| Static full closure (R9) | rank-10 valuation matrix ⇒ full conjugate Kummer-wreath closure | `R9_STATIC_CLOSURE_OPENING_DERIVATION…md` | ⚠ paper `:672`; proof in supplement |
| Rotating rank jump | rotation adds a private prime ⇒ Kummer rank jump | `ROTATING_KUMMER_RANK_JUMP_LEMMA_REPORT…md` | ⚠ paper `:699`; proof in supplement |
| Realization-poset certificate | incidence degrees (48,2,64,192,6,8,24) | `REALIZATION_POSET_RUN_REPORT…` + M2 suite | ⚠ paper `:822`; certs in supplement |
| **Weighted exact degree** | `d(c)=#{ {η,−η}: Σηᵢcᵢ≠0 }`; the weighted radical sum is primitive | `GENERIC_SYMMETRIC_MONODROMY…v1.0.md`, Prop. 2.3 / Thm 3.3 | ✅ new canonical reusable paper |
| **Genus and full ramification count** | `g=1+2^{k−2}(k−3)` and `deg Ram=2^{k−1}(k−3)+2d(c)` | same, Thms 3.1 and 4.4 | ✅ new canonical reusable paper |
| **Weighted generic monodromy** | for every fixed `cᵢ≠0`, generic geometric and arithmetic monodromy are `S_{d(c)}` | same, Thm 7.1 / Cor. 7.2 | ✅ new canonical reusable paper |
| **Equal-weight DBP specialization** | `Gal(Nₖ/F)=S_{δₖ}` for every `k≥3`, with exact signed-pole degree `δₖ` | same, §8 | ✅ supersedes ALL_K as proof authority |
| **All-k Thm A/B/C development record** | inertia localization; certified k=3..6 groups S₄/S₅/S₁₆/S₂₂; independent low-k checks | `ALL_K_MONODROMY_THEOREM_NOTE…md` | ⚠ retained computational/development supplement; theorem absorbed and strengthened |
| **Generic Morse development proof** | critical-value gradient `(1/2wᵢ)` and (GS) route | `GS_GENERIC_MORSE_LEMMA_PROOF…md` | ⚠ retained proof supplement; argument rebuilt through a finite relative ramification scheme |
| **Kummer/wreath lift interface** | `Gal(L/F)≅C₂^s wr S_{d(c)}` when the `sd(c)` conjugate square classes are independent; full valuation-parity rank is sufficient | `GENERIC_SYMMETRIC_MONODROMY…v1.0.md`, §10 | ✅ criterion complete; concrete `R=0` remains case-specific |

### Paper V — foundations (no capstone yet)

| Unit | Statement | Source | Successor |
|---|---|---|---|
| SQG category | R-selected quotient groupoids + native R-morphisms form `SQG_R` | `SELECTED_QUOTIENT_GROUPOIDS_FOUNDATION_v1.0.md §3` | ❌ eventual Paper V (self-canonical now) |
| Flat scalar extension | `Ext_R^S : SQG_R→SQG_S` with associativity iso | same §4 | ❌ Paper V / Theorem C |
| R3 native AC fold | `F(v)=v²+(2QX−E²)v+X²(P²+Q²)`, `Δ=E⁴−4E²QX−4P²X²`; integer winding groupoid | `R3_AC_FOLD_INDEPENDENT_REALIZATION_THEOREM_v1.0.md §1` | ❌ Paper V Gate R3 (self-canonical) |
| R3 skeleton functor | `Z→C_2` full + ess-surjective, **not faithful (kernel 2Z)**; full-carrier equivalence *not claimed* | same §3 | — |
| Full unreduced carrier equivalence | **REFUTED** (P8-16, AR-23) | `POST_8_OUTCOME_GAP_LEDGER_v1.0.md` | negative result (retained) |
| Post-8 outcomes | P8-01..P8-21 (5 REFUTED, 5 promoted-core, rest ACTIVE_PROOF) | same ledger | ledger = sole enumeration |

---

## 4. Document disposition table

Every artifact carries exactly one primary disposition. Below: the **individually adjudicated
theorem/proof/companion/draft core**, followed by **class-level** dispositions for the bulk
(campaign run-logs, certificates, mirrors). Paths are relative to
`Papers_Library/` unless marked `[live]` (research/campaign tree), `[docs]`, or `[archive]`.

### Disposition counts (adjudicated core)

| Disposition | Count (core artifacts) | Notes |
|---|---:|---|
| `CANONICAL_RETAIN` | ~28 | released papers, atomic theorems, sole live ledgers |
| `INDEPENDENT_COMPANION` | ~12 | distinct mathematical role |
| `MERGE_THEN_RETIRE` | 2 | unique material must transfer first |
| `PROOF_SUPPLEMENT_RETAIN` | ~14 | headline absorbed, workings unique |
| `COMPUTATIONAL_SUPPLEMENT_RETAIN` | ~9 classes (87 `.py` + M2 + gate-dumps) | reproducible exact computation |
| `HISTORICAL_ONLY` | ~10 (+ hashed run-log families) | fully subsumed; successor named |
| `SUPERSEDED_VARIANT` | ~12 | earlier version replaced |
| `EXACT_MIRROR` / `FORMAT_RENDER` | 39 collapsed + `docs/files/`, package, symlink layers | byte-identical / render pairs |
| `UNRESOLVED` | 0 mathematical | 3 filing/editorial items flagged (§11) |

No artifact required an `UNRESOLVED` mathematical disposition — every unit maps to a retained
source and no constant/sign/ring contradiction was found. The unresolved items in §11 are
**editorial/filing**, not mathematical conflicts.

### Core adjudications (by family)

**Paper I**

| Artifact | Disposition | Successor / note |
|---|---|---|
| `01_completed…/dbp_orbit_calculus.tex` (+`.pdf`) | CANONICAL_RETAIN | released Paper I |
| `02_theorems…/theorem_8_1.tex` (+`.pdf`) | INDEPENDENT_COMPANION | abstract Invariant-Preservation; additive `φ_K+φ_sym` + κ-dichotomy not in orbit_calculus |
| `02_theorems…/Theorem_8_1_Curvature_Orbit_Correction.md` | MERGE_THEN_RETIRE | → orbit_calculus §7 (see §8) |
| `Canonical_Invariant_Reduction_Theorem.md` | PROOF_SUPPLEMENT_RETAIN | sole Lorentzian single-edge corollary |
| `Gauge_Channel_Transport_Law.md` | PROOF_SUPPLEMENT_RETAIN | sole full Lorentzian pinning derivation |
| `03_proofs…/GAUGE_NORMAL_FORM_PROOF.md` | PROOF_SUPPLEMENT_RETAIN | sole `Sym₃/Im(G_g)≅ℚ³` proof |
| `05_…/DBP_Curvature_Role_Reduction.md` | INDEPENDENT_COMPANION | adds §14 Gauss–Lovelock elevation |
| `02_…/THEOREM_CANDIDATES.md` | COMPUTATIONAL_SUPPLEMENT_RETAIN | measured 5298-class finite bound; open converse |

**Paper II**

| Artifact | Disposition | Successor / note |
|---|---|---|
| `01_…/pfc_normal_forms.tex` | CANONICAL_RETAIN | released general-theory paper |
| `01_…/lead7_kn_n3_dbp_metric.tex` | CANONICAL_RETAIN | released KN-realization paper |
| `01_…/LOCAL_CURVATURE_CALCULUS_COMPLETE_v1.0.md` | CANONICAL_RETAIN | fullest proof spine (superset of pfc) |
| `02_…/LEAD7_VARIABLE_TRANSVERSE_WEIGHTED_JET_THEOREM_v1.0.md` | CANONICAL_RETAIN | newest strengthening (Jul 15) |
| `03_…/LOCAL_CURVATURE_CALCULUS_COMPANION.md` | MERGE_THEN_RETIRE | → COMPLETE_v1.0 (see §8) |
| `05_…/Local_Curvature_Calculus_for_Inverse-Channel_Metrics.txt` | HISTORICAL_ONLY | → COMPLETE + both papers (Stage 1–10 roadmap; no unique math) |
| `02_…/LEAD7_masscharge_zeros_theorem.md` | PROOF_SUPPLEMENT_RETAIN | fuller standalone proof condensed in KN paper |
| `03_…/kerr_retrograde_45_over_16_derivation.md` | INDEPENDENT_COMPANION | Kerr ISCO subtopic |
| `01_…/lead7_kn_n3_dbp_metric_v2.pdf` | SUPERSEDED_VARIANT | dated Jul 7 = older than current build (label misleading; **not byte-verified**) |

**Paper III**

| Artifact | Disposition | Successor / note |
|---|---|---|
| `05_…/DBP_CURVATURE_PERIODS_OF_THE_DBP_QUADRIC_v1.0.md` | CANONICAL_RETAIN | consolidated Paper III (hash matches corpus-cited canonical) |
| `02_…/DBP_LANDEN_TRACE_THEOREM_COMPLETE_v1.1.md` (un-suffixed) | CANONICAL_RETAIN (atomic) | named proof-authority dependency across corpus (fails subsumption cond. 6) |
| `DBP_CCE5_ABSOLUTE_CALIBRATION_THEOREM_v1.0.md` | INDEPENDENT_COMPANION → pending insertion | proves λ↑=B₋, λ↓=−B₋, (a,b,c)=(1,0,0); not yet in III |
| `DBP_NATIVE_SURFACE_SWEEP_CLEARANCE_THEOREM_v1.0.md` | INDEPENDENT_COMPANION → pending insertion | divisor reduction replacing III's thin-tube; not yet in III |
| `CCE_6_WHOLE_SURFACE_TOPOLOGY_OBSTRUCTION_v1.0.md` | INDEPENDENT_COMPANION | unique rank-4-in-12 open-wall record |
| `03_…/DBP_SURFACE_TO_LINK_CLOSEOFF_v1.0.md` | PROOF_SUPPLEMENT_RETAIN | III §7A delegates the Stokes boundary + link-length proof |
| `04_…/DBP_DUAL_SURFACE_CYCLE_STAGE1/2/3_v0.1.md` | PROOF_SUPPLEMENT_RETAIN (×3) | III §7B/7C/7D delegate; gates 22/17/22 live here |
| `DBP_EXACT_CORRIDOR_POSITIVE_CLEARANCE_THEOREM_v1.0.md` | PROOF_SUPPLEMENT_RETAIN | III §7F Lemma 7F.A delegates segment/29-disk clearance |
| `03_…/dbp_role_channel/DUAL_CONSTANT_CLOSEOFF.md` | PROOF/COMPUTATIONAL_SUPPLEMENT_RETAIN | unique closed form + two-route CPV cert + PSLQ refutation |
| `05_…/LANDEN_TYPE_THEOREM_SOURCE.md` | INDEPENDENT_COMPANION | targets still-open primary↔dual Landen relation |
| `CCE_2_PAPER_III_INSERTION_NOTE_v1.0.md` | HISTORICAL_ONLY | insertion already applied (hash-confirmed); provenance |

**Paper IV**

| Artifact | Disposition | Successor / note |
|---|---|---|
| `01_…/galois_horizon_cover_v1_0.tex` (+`.pdf`) + `[docs] …publication_package/` | CANONICAL_RETAIN | released paper + package |
| `01_…/GENERIC_SYMMETRIC_MONODROMY_OF_WEIGHTED_MULTIQUADRATIC_SUMS_v1.0.md` (`PAP-0509`) | CANONICAL_RETAIN | reusable all-`k`, all-nonzero-weight proof authority; DAG-released |
| `KUMMER_MODULE_WREATH_LIFT`, `ROTATING_KUMMER_RANK_JUMP`, `R9_STATIC_CLOSURE`, `ROTATING_THREE_CHANNEL_WREATH`, `WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1` | PROOF_SUPPLEMENT_RETAIN (×5) | proofs the preprint summarizes (bundled in package) |
| `ALL_K_MONODROMY_THEOREM_NOTE_2026-07-10.md` | COMPUTATIONAL_SUPPLEMENT_RETAIN | superseded as proof authority; preserves low-`k` certificates and development record |
| `GS_GENERIC_MORSE_LEMMA_PROOF_2026-07-10.md` | PROOF_SUPPLEMENT_RETAIN | cited independent route and provenance; no longer sole proof authority |
| `05_…/GALOIS_K_ELLIPSE_RESEARCH_MAP_v1_6.md` | CANONICAL_RETAIN | **true head** (verified newest on disk) |
| `…RESEARCH_MAP_v1.1 / v1_3 / v1_4.md` | SUPERSEDED_VARIANT (×3) | → v1_6 |
| `01_…/self_glue_monodromy.tex` (62546 B) | INDEPENDENT_COMPANION | distinct imprimitive-wreath-monodromy paper |
| `[live] …/08_cce7_horizon/*` (gap ledger, stage report, normalized-incidence import) | CANONICAL_RETAIN (live) | sole spec of the OPEN complex-braid residual |

**Paper V / ensemble**

| Artifact | Disposition | Successor / note |
|---|---|---|
| `SELECTED_QUOTIENT_GROUPOIDS_FOUNDATION_v1.0.md` | CANONICAL_RETAIN | proved category foundation |
| `R3_AC_FOLD_INDEPENDENT_REALIZATION_THEOREM_v1.0.md` | CANONICAL_RETAIN / INDEPENDENT_COMPANION | exact independent realization + non-faithfulness |
| `CCE_8_FINITE_TOWER_NATURALITY_THEOREM_v1.0.md` | CANONICAL_RETAIN | Paper I supplement (projective-system) |
| `DBP_PAPER_ENSEMBLE_ARCHITECTURE_v1.0.md` | CANONICAL_RETAIN | **sole** holder of Paper V gate spec + §7.3 elliptic (a,b,c) gap — orphan risk if retired |
| `POST_8_AUTHORITY_SOURCE_MANIFEST_v1.0.md`, `POST_8_OUTCOME_GAP_LEDGER_v1.0.md`, `…R3_FINAL_REPORT_v1.0.md` | CANONICAL_RETAIN | sole SHA map / P8 enumeration / WP ledgers |
| `[live] DBP_CCE_ARTIFICIAL_RESTRICTION_LIVE_RECONCILIATION_v1.0.md` | CANONICAL_RETAIN | sole AR-01..AR-26 residual-gap ledger |
| `DBP_UNIFIED_THEOREM_SPINE_DRAFT_v0_1 (2).tex` (v0.3) | CANONICAL_RETAIN (draft ledger) | latest spine draft; **never a proof source** |
| `DBP_UNIFIED_THEOREM_SPINE_DRAFT_v0_1.tex` (v0.2) | SUPERSEDED_VARIANT | → the (2)/v0.3 content |
| `03_…/cella_residue/DUAL_CONSTANT_CLOSEOFF.md` | SUPERSEDED_VARIANT | → dbp_role_channel copy (misfiled older revision) |
| `CODEX_HANDOFF_CELLA_CONTINUATION_ENGINE_v0.2.md` | HISTORICAL_ONLY | operative historical CCE design record |

### Class-level dispositions (bulk)

- **`Reports_Library/` (954), `Campaign_Library/` (776 clones + 176 symlinks), `Evidence_Store/`
  (3017)** → `EXACT_MIRROR` / binding infrastructure. Each entry mirrors or binds a
  Papers_Library / campaign artifact adjudicated above; the catalogue LEDGERs are the evidence.
- **`docs/files/…` DBP copies** → `EXACT_MIRROR` of Papers_Library canon (older live drop; verified
  byte-identical for the Galois family; same pattern elsewhere).
- **All `verify_*.py`, `pfc_test*`, `lead7_test*`, Macaulay2 `stage*.m2`/`.out.txt`, gate-dump
  `.txt`, build-kit `.zip`, `prediction_verdicts*.json`** → `COMPUTATIONAL_SUPPLEMENT_RETAIN`
  (reproducible exact computation backing the theorems).
- **Hashed run-log families** — `CLAIM_LEDGER__*`, `MANIFEST__*`, `MUTATION_REPORT__*`,
  `PREREG__*`, `EXCEPTIONAL_LOCUS_REPORT__*`, `prediction_verdicts__*` → `HISTORICAL_ONLY`
  (campaign iteration logs; no unique theorem; superseded by their consolidated unhashed head).
- **`09_historical_and_superseded_versions/…`** → `HISTORICAL_ONLY` / `SUPERSEDED_VARIANT` as
  already filed (e.g. `Theorem_8_1_New_Math_Extension.md`, `*.bak`, `LEAD7_Candidate_D…`).

---

## 5. Exact-mirror and variant groups

### (a) Exact byte-mirrors — already resolved at the library layer
Same sha256, `mirror_count=2/3` (multiple origins collapsed to one library copy). Designate the
Papers_Library copy canonical; origins in `research/`, `docs/files/`, `archive/`,
`Reports_Library`, `Campaign_Library` symlinks are mirrors. Examples: `dbp_orbit_calculus.tex`,
`gtd_vs_dbp.pdf`, `role_channel_anisotropy.pdf`, `galois_horizon_cover_v1_0.tex` (×3),
`theorem_8_1.pdf`, `KUMMER_MODULE_WREATH_LIFT_THEOREM…md`, `R9_STATIC_CLOSURE…md`,
`REALIZATION_POSET_RUN_REPORT…md`, the whole Macaulay2 `stage1..6 .m2/.out.txt` suite,
`horizon_wreath_inertia_model.m2`, `stage.zip`, `DEGREE_20_CROWN_CERTIFICATE_REPORT…md`,
`verify_dbp_landen_trace_theorem*.py`, `CCE_2_PAPER_III_INSERTION_NOTE`, and the
publication-package `supporting_reports/` + `certificates/`.

### (b) Format-render pairs
`.tex`↔`.pdf`: `pfc_normal_forms`, `lead7_kn_n3_dbp_metric`, `galois_horizon_cover_v1_0`,
`self_glue_monodromy`, `DBP_UNIFIED_THEOREM_SPINE_DRAFT`. Keep the source; the render is
`FORMAT_RENDER`.

### (c) Material variant twins (the audit-critical group — resolved by content)

| Twin | Canonical | Superseded / older | Basis |
|---|---|---|---|
| `DBP_LANDEN_TRACE…v1.1.md` (15411 B) vs `__b6ac0c13.md` (13696 B) | un-suffixed | `__b6ac0c13` (lacks §7A surface-to-period interface, ~50 lines math) | content diff 72 lines; §7A present only in canonical |
| `DBP_NATIVE_RELATIVE_PERIOD_ROUTE…v1.0.md` (6422 B) vs `__eee8e122.md` (5287 B) | un-suffixed | `__eee8e122` (lacks §0A geometric-status block) | diff 43 lines |
| `DUAL_CONSTANT_CLOSEOFF.md` — `dbp_role_channel` (6640 B) vs `cella_residue` (5567 B) | **dbp_role_channel** | `cella_residue` (misfiled older; no §4A) | dbp copy adds §4A Primary Geometric Interface; **two agents concur** |
| `self_glue_monodromy.tex` (62546 B) vs `__5ff2665e.tex` (24361 B) | un-suffixed (current expanded) | `__5ff2665e` + `__bac90067.pdf` (earlier variant) | diff ≈ full (materially different documents) |
| `DBP_UNIFIED_THEOREM_SPINE_DRAFT_v0_1 (2).tex` (v0.3) vs plain `.tex` (v0.2) | **the "(2)" copy** (newer, adds proved surface-to-link theorem) | plain (older v0.2) | internal `\date{}`: v0.3 13 Jul vs v0.2 10 Jul — **filename is a naming trap** |
| `GALOIS_K_ELLIPSE_RESEARCH_MAP` v1.1/v1_3/v1_4/**v1_6** | **v1_6** (verified newest, 18:01) | v1.1/v1_3/v1_4 | brief + Encyclopedia named v1_4 — **stale**; live disk has v1_6 |
| `lead7_kn_n3_dbp_metric_v2.pdf` vs current `.pdf` | current build (Jul 13) | `_v2.pdf` (Jul 7, older despite label) | dates; **not byte-verified — flagged** |

### (d) Same-basename collisions that are NOT twins
`BRIEF.md` (KN campaign brief) vs `BRIEF__502c516c.md` (PFC campaign brief) — two different
documents. `README.md` vs `README__6ab278b8.md` — CV root vs `sweeps/` subfolder. Both are
basename collisions the library correctly kept apart; each is `HISTORICAL_ONLY` on its own terms.

---

## 6. `CANONICAL_RETAIN` list

Released papers, atomic theorem sources, and sole live ledgers — the spine of the ensemble.

1. `dbp_orbit_calculus.tex` (+`.pdf`) — **Paper I**.
2. `pfc_normal_forms.tex` — **Paper II general theory**.
3. `lead7_kn_n3_dbp_metric.tex` — **Paper II KN realization**.
4. `LOCAL_CURVATURE_CALCULUS_COMPLETE_v1.0.md` — Paper II full proof spine.
5. `LEAD7_VARIABLE_TRANSVERSE_WEIGHTED_JET_THEOREM_v1.0.md` — newest Paper II strengthening.
6. `DBP_CURVATURE_PERIODS_OF_THE_DBP_QUADRIC_v1.0.md` — **Paper III** (incomplete; see §11/§13).
7. `DBP_LANDEN_TRACE_THEOREM_COMPLETE_v1.1.md` (un-suffixed) — atomic proof authority.
8. `DBP_CCE5_ABSOLUTE_CALIBRATION_THEOREM_v1.0.md` — proven λ/(a,b,c) resolution (awaits insertion).
9. `DBP_NATIVE_SURFACE_SWEEP_CLEARANCE_THEOREM_v1.0.md` — proven divisor reduction (awaits insertion).
10. `galois_horizon_cover_v1_0.tex` (+ publication package) — **Paper IV**.
11. `GENERIC_SYMMETRIC_MONODROMY_OF_WEIGHTED_MULTIQUADRATIC_SUMS_v1.0.md` — **canonical
    weighted all-`k` base-monodromy successor** (`PAP-0509`).
12. `GALOIS_K_ELLIPSE_RESEARCH_MAP_v1_6.md` — program dashboard (true head).
13. `SELECTED_QUOTIENT_GROUPOIDS_FOUNDATION_v1.0.md` — SQG foundation.
14. `R3_AC_FOLD_INDEPENDENT_REALIZATION_THEOREM_v1.0.md` — R3 independent realization.
15. `CCE_8_FINITE_TOWER_NATURALITY_THEOREM_v1.0.md` — finite-tower naturality.
16. `DBP_PAPER_ENSEMBLE_ARCHITECTURE_v1.0.md` — ensemble map + **sole Paper V gate/gap spec**.
17. `POST_8_AUTHORITY_SOURCE_MANIFEST_v1.0.md`, `POST_8_OUTCOME_GAP_LEDGER_v1.0.md`,
    `POST_8_UNIVERSALIZATION_REDUCTION_R3_FINAL_REPORT_v1.0.md` — sole authority/gap/WP ledgers.
18. `[live] DBP_CCE_ARTIFICIAL_RESTRICTION_LIVE_RECONCILIATION_v1.0.md` — sole AR ledger.
19. `[live] research/campaigns/CELLA_CONTINUATION_ENGINE/08_cce7_horizon/*` — sole open-braid spec.
20. `DBP_UNIFIED_THEOREM_SPINE_DRAFT_v0_1 (2).tex/.pdf` (v0.3) — latest draft ledger (never a proof source).

---

## 7. `INDEPENDENT_COMPANION` list

Overlap in vocabulary or topic, but a distinct mathematical role — **not** redundant.

- `theorem_8_1.tex` — abstract Invariant-Preservation (additive `φ_K+φ_sym`, κ-dichotomy).
- `DBP_Curvature_Role_Reduction.md` — adds §14 Gauss–Lovelock (m=2 shadow) elevation.
- `kerr_retrograde_45_over_16_derivation.md` — Kerr ISCO geodesic subtopic.
- `self_glue_monodromy.tex` — imprimitive wreath monodromy of self-composed constraint surfaces.
- `CCE_6_WHOLE_SURFACE_TOPOLOGY_OBSTRUCTION_v1.0.md` — rank-4-in-12 obstruction record.
- `LANDEN_TYPE_THEOREM_SOURCE.md` — targets the still-open primary↔dual Landen relation.
- `R3_AC_FOLD_INDEPENDENT_REALIZATION_THEOREM_v1.0.md` — independent AC-fold (also CANONICAL).
- `DBP_CCE5_ABSOLUTE_CALIBRATION_THEOREM_v1.0.md`, `DBP_NATIVE_SURFACE_SWEEP_CLEARANCE_THEOREM_v1.0.md`
  — pending insertion into Paper III (companion until absorbed).
- Galois strategic memo, emergence ledger, prior-art report — meta/provenance companions.

---

## 8. `MERGE_THEN_RETIRE` list (with required transfers)

Only two documents hold unique material that a canonical successor should absorb *before* the
document itself is retired. Nothing else in the corpus qualifies as merge-then-retire.

1. **`Theorem_8_1_Curvature_Orbit_Correction.md`** → merge into `dbp_orbit_calculus.tex` §7,
   then retire. **Transfer:** the numeric worked example `(a,b,A,B,C)=(5,7,2,3,4)`; the explicit
   self-channel form `κ_{s,D}=A·R/(a²q₀²)`; and the transverse-quadratic identity
   `R=a²C−2abB+b²A`. (≈90% of the document — the C_P/C_D/C_S charts — is already in §7.1.)

2. **`LOCAL_CURVATURE_CALCULUS_COMPANION.md`** → merge into
   `LOCAL_CURVATURE_CALCULUS_COMPLETE_v1.0.md`, then retire. **Transfer:** only the §9
   dual-constants block (`I_primary≈−5.01049…`, `I_dual≈−3.98800…`, residue 4). *Caveat:* the
   companion itself flags this block as belonging to the elliptic-period family — it should land
   in the Paper III dual-constant close-off, not the curvature spine. Everything else in the
   companion (Thms A/B, master quadric, gauge, Lamé, KN table) is already reproduced in COMPLETE.

---

## 9. `PROOF_SUPPLEMENT_RETAIN` and `COMPUTATIONAL_SUPPLEMENT_RETAIN`

### PROOF_SUPPLEMENT_RETAIN — headline absorbed, workings unique and load-bearing
- Paper I: `Canonical_Invariant_Reduction_Theorem.md` (Lorentzian single-edge corollary),
  `Gauge_Channel_Transport_Law.md` (full Lorentzian pinning derivation),
  `GAUGE_NORMAL_FORM_PROOF.md` (`Sym₃/Im(G_g)≅ℚ³`). **These three carry sole proof authority for
  units the released paper only states — do not retire before transfer.**
- Paper II: `LEAD7_masscharge_zeros_theorem.md` (6-numerator factorization + inner-branch
  counterexample condensed in the KN paper).
- Paper III: `DBP_SURFACE_TO_LINK_CLOSEOFF_v1.0.md` (Stokes boundary eval + tan-substitution
  link-length), `DBP_DUAL_SURFACE_CYCLE_STAGE1/2/3_v0.1.md` (convergence/residue/lattice gates
  22/17/22), `DBP_EXACT_CORRIDOR_POSITIVE_CLEARANCE_THEOREM_v1.0.md` (segment/29-disk clearance),
  `DUAL_CONSTANT_CLOSEOFF.md` (dbp copy — regular closed form + two-route CPV cert + PSLQ
  refutation).
- Paper IV: `KUMMER_MODULE_WREATH_LIFT`, `ROTATING_KUMMER_RANK_JUMP`, `R9_STATIC_CLOSURE`,
  `ROTATING_THREE_CHANNEL_WREATH_CLOSURE`, `WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1`,
  `GS_GENERIC_MORSE_LEMMA_PROOF` (independent cited route), `AUDIT_REPORT_R6_R7_GENERIC_DESCENT`,
  `LOG_ENTRY_R5/R6_R7` v2. The weighted paper is now the proof authority; these remain retained
  because their derivations, audits, and case-specific calculations are not byte- or content-null.

### COMPUTATIONAL_SUPPLEMENT_RETAIN — reproducible exact computation
- All `verify_*.py` across families; Paper II `pfc_test*` / `lead7_test*` + gate-dump `.txt`
  (`Lext.txt`, `num_factor.txt`, `P_coeff_*`, `positive_core_P.txt`); Paper III `periods.py`,
  `legendre_native.py`, `gate_*`, native-evaluator build-kit/contracts/release reports; Paper IV
  Macaulay2 `stage1..6 .m2/.out.txt`, `horizon_wreath_inertia_model.m2`, `stage.zip`,
  `DEGREE_20_CROWN_CERTIFICATE_REPORT`, `REALIZATION_POSET_RUN_REPORT`,
  `MACAULAY2_REALIZATION_POSET_WORKFLOW`, `prediction_verdicts*.json`.
- **Reproducibility defect flagged** (not a math issue):
  `07_…/local_curvature…/lead7_variable_transverse_weighted_jet.py` shims to a
  `parents[1]/…/CELLA_CONTINUATION_ENGINE/…` path that does **not** exist under the
  Papers_Library layout; the real verifier sits beside it. Fix the runpath to
  `Path(__file__).with_name(...)`.

---

## 10. `HISTORICAL_ONLY` retirement candidates (successor evidence)

Fully subsumed; retain for provenance only. Each has a named canonical successor and no unique
surviving mathematical unit.

| Candidate | Successor | Evidence no unique unit remains |
|---|---|---|
| `Local_Curvature_Calculus_for_Inverse-Channel_Metrics.txt` | `LOCAL_CURVATURE_CALCULUS_COMPLETE_v1.0` + both papers | Stage 1–10 roadmap; proposed the 2-paper split that was executed; its Thms A/B are now proven in COMPLETE |
| Paper II `BRIEF.md`, `BRIEF__502c516c.md` | KN paper / pfc note | campaign briefs; central questions resolved and papers drafted |
| Paper II `LEAD7_pole_orders / pullback_probe / retrodiction / candidate` reports (`05_…`) | `lead7_kn_n3_dbp_metric.tex` | candidate-selection trail; conclusions in the Selection Theorem; failure modes catalogued |
| Paper II `README.md`, `README__6ab278b8.md`, `CLAIMS.md`, `LOG.md`, `CV_HANDOFF…` | `LOCAL_CURVATURE_CALCULUS_COMPLETE_v1.0` | CV campaign scaffolding; CLAIMS empty, math already banked |
| `CCE_2_PAPER_III_INSERTION_NOTE_v1.0.md` | Paper III §7F (already inserted) | hash confirms CCE-2 insertion applied; note is provenance |
| `CODEX_HANDOFF_CELLA_CONTINUATION_ENGINE_v0.2.md` | POST_8 handoff | manifest types it "operative *historical* CCE design" |
| Hashed run-log families (`CLAIM_LEDGER__*`, `MANIFEST__*`, `MUTATION_REPORT__*`, `PREREG__*`, `EXCEPTIONAL_LOCUS_REPORT__*`) | consolidated unhashed head ledgers | campaign iteration logs; no theorem |
| `09_historical…/Theorem_8_1_New_Math_Extension.md`, `*.bak`, `HANDOFF*.md`, `probe_run_output.txt` | `Theorem_8_1_Curvature_Orbit_Correction.md` (corrects §13) | already filed historical; §13 curvature orbit shown passive/tautological |
| Paper V `09_historical…/cella_residue` (11 files) | superseded planning | Jun-18 alpha-jet/warp-stage probes + HR planning |

---

## 11. Unresolved conflicts or missing sources

**No mathematical contradictions** were found: constants, signs, orientations, coefficient rings,
and boundary conventions are consistent across sources (e.g. keystone `κc=−1/49, κs=1/49,
κint=−3/49`; faithfulness `det=8Λ_PΛ_DΛ_S/q₀⁶`; period residue 4, `−4π/±4πi/8πi`, `R_ℤL_ℤ=4·id`;
Galois `Ŝ₊Ŝ₋=P`). The open items are **editorial / filing / reproducibility**, not conflicts of
theorem content:

1. **Paper III canonical-completeness gap (highest priority).** The on-disk Paper III contains
   CCE-2 but **not CCE-5 or CCE-6** (verified: λ still "unresolved" at line 1543; informal
   thin-tube at line 1559). The proven `CCE5_ABSOLUTE_CALIBRATION` and
   `NATIVE_SURFACE_SWEEP_CLEARANCE` theorems must be **retained**, and a **CCE-5 Paper III
   insertion note is missing** (only a CCE-6 insertion note exists). This is a live editorial
   obligation, not a redundancy.
2. **Missing successor for two proven theorems.** Because of (1), subsumption condition 8 ("the
   successor is canonical and present on disk") is satisfied for CCE-5/CCE-6 only as *standalone*
   theorem files — Paper III is not yet their successor. They stay `INDEPENDENT_COMPANION` until
   inserted.
3. **Paper-IV manuscript integration debt (proof-status cleanup completed).** The completed
   weighted paper supersedes `ALL_K_MONODROMY_THEOREM_NOTE` as proof authority; the note now marks
   Theorem D proved and identifies its successor, and the live v1.6 research map records R8/R9/R10/R11
   at their current statuses. The released k=4,5 Paper IV has not yet cited or absorbed the new
   arbitrary-`k` theorem because its TeX/PDF/publication-package render set must be revised
   together. This remaining item is publication integration, not an open base-monodromy theorem.
4. **Filing / taxonomy inconsistencies (not math).** Paper III lives in tier
   `05_expository_companions` rather than `01`/`02`; the CCE-2/5/6 theorem files are dual-filed in
   `02_theorems…/dbp_role_channel` **and** the live campaign (byte-identical). `docs/files/` holds
   an older byte-identical drop of the Galois family.
5. **Two dispositions rest on file dates, not byte-diff:** `lead7_kn_n3_dbp_metric_v2.pdf`
   (SUPERSEDED_VARIANT) — a PDF text-diff against the current build would confirm.

**Orphan risk (must not retire):** `DBP_PAPER_ENSEMBLE_ARCHITECTURE_v1.0.md` is the **sole**
holder of (i) the Paper V gate structure (Theorem E strict-non-equivalence + reduced-skeleton
target; Theorem C closure hypotheses) and (ii) the §7.3 elliptic Relative Trace-Path integers
`[Γ₋^CPV]=[Γ₊]+a[A]+b[B]+(c+½)[μ]` gap. Likewise the `POST_8_OUTCOME_GAP_LEDGER` (P8-01..P8-21)
and `DBP_CCE_ARTIFICIAL_RESTRICTION_LIVE_RECONCILIATION` (AR-01..AR-26) are sole enumerations of
live gaps. Retiring any of these would silently close open problems.

---

## 12. Genuine open mathematical walls that survive consolidation

These remain open regardless of any document merge; each is named with its sole/primary specifying
source so consolidation cannot accidentally declare it closed.

1. **Off-diagonal / general-order role-rechart covariance** (Papers I & II, corroborated
   independently). Diagonal local-germ laws are closed on the nondegenerate stratum
   (`P1/P0+R1/R0≠0`); the off-diagonal tensor pullback + curvature replay is **not** done.
   Source: `LEAD7_VARIABLE_TRANSVERSE_WEIGHTED_JET_THEOREM_v1.0.md:96`; `THEOREM_CANDIDATES.md`.
2. **Infinite-order / global chart gluing** (Paper I). CCE-8 strengthens the S₃ action to
   naturality across the *finite* truncation tower only — explicitly not analytic-germ
   convergence or global gluing. Source: `CCE_8_FINITE_TOWER_NATURALITY_THEOREM_v1.0.md:42`.
3. **Codimension ≥3 corners & front-face coefficient classification** (Paper II). Source:
   `pfc_normal_forms.tex:174`; `PREREG_PFC4`; `COMPLETE §7.8`.
4. **Full regular-plane monodromy / whole-surface saturation / rank-4-in-12** (Paper III). The
   native transfer is exact only on `𝒮_ℤ^nat=im L_ℤ` (`rank ≤ 4` inside `rank H₂=12`); the whole
   surface lattice is not saturated and `¼R_ℤ` is not claimed integral. **Do not relabel the
   native image as the whole surface lattice.** Sources:
   `CCE_6_WHOLE_SURFACE_TOPOLOGY_OBSTRUCTION_v1.0.md`; Paper III §9 "Not claimed".
5. **Primary↔dual Landen transformation** `I_primary(λ)=α(√2)·I_dual(1−λ)+correction` (Paper III).
   Source: `LANDEN_TYPE_THEOREM_SOURCE.md`.
6. **All-k Kummer/crown instantiation** (Paper IV): the universal base group is now
   `S_{d(c)}`, but maximal decorated closure still requires proving independence of the concrete
   `sd(c)` conjugate square classes, equivalently `R=0`. A valuation-parity matrix of full column
   rank is sufficient, not automatic. Sources: `GENERIC_SYMMETRIC_MONODROMY…v1.0.md §10–11`;
   `KUMMER_MODULE_WREATH_LIFT_THEOREM_2026-07-10.md`; DAG gap `DBP:gap:IV3`.
7. **Generic complex Paper-IV monodromy / braid route** (Paper IV): exact complex loop
   representatives, braid execution, refinement independence, and CCE-5-route cross-transport
   compatibility. The normalized-incidence cover + inertia catalogue are *established*; the
   residual is the braid campaign over them. Sources:
   `08_cce7_horizon/CCE_7_NORMALIZED_INCIDENCE_INERTIA_IMPORT_REPORT_v1.0.md`,
   `CCE_7_STAGE_REPORT_v1.0.md`, `CCE_7_GAP_LEDGER_v1.0.md`.
8. **Paper V category-equivalence walls**: missing DBP-arm reduction functors (P8-17); three-way
   coherence (P8-18); general categorical closure (Theorem C); componentwise comparison diagrams.
   Full unreduced carrier equivalence is **refuted** (P8-16) — any positive theorem must concern
   explicit reductions or a common selected skeleton. Sources:
   `POST_8_OUTCOME_GAP_LEDGER_v1.0.md`; `R3_AC_FOLD…§3`; architecture §7.2/§8.

---

## 13. Minimal editorial sequence for later merges (safe order)

Each step is independently safe and reversible; no source is deleted — "retire" = move to
`09_historical…` after the transfer lands and the maintainer approves.

1. **Paper III completion (do first — it closes the only theorem-level gap).**
   (a) Insert CCE-5 (`λ↑=B₋, λ↓=−B₋`, braid `M↑/M↓`, `(a,b,c)=(1,0,0)`) into Paper III §7F.10,
   replacing the "unresolved corrections" text; author the **missing** CCE-5 Paper III insertion
   note. (b) Apply the existing CCE-6 insertion note: replace the §7F.5 informal thin-tube with
   the `NATIVE_SURFACE_SWEEP_CLEARANCE` divisor reduction. (c) Re-hash Paper III; update the
   authority manifest. **Then** the two theorem files drop `INDEPENDENT_COMPANION →
   PROOF_SUPPLEMENT_RETAIN`.
2. **Paper I proof-transfers.** Copy units U10 (Lorentzian coupling-edge lemma) and U11
   (gauge-normal-form quotient) into `dbp_orbit_calculus.tex` (or a permanently-linked proof
   appendix). Only after they land may `Canonical_Invariant_Reduction_Theorem.md`,
   `Gauge_Channel_Transport_Law.md`, `GAUGE_NORMAL_FORM_PROOF.md` be reduced from proof-supplement
   to historical. Merge `Theorem_8_1_Curvature_Orbit_Correction.md`'s worked example + self-channel
   identities into §7, then retire it.
3. **Paper II tidy.** Move the `COMPANION.md` §9 dual-constants block to the Paper III dual-constant
   close-off; retire `COMPANION.md` and the `.txt` roadmap to historical. Fix the broken verifier
   runpath. Byte-verify `lead7_kn_n3_dbp_metric_v2.pdf` before filing it superseded.
4. **Paper IV publication integration.** The ALL_K status splice and v1.6 map cleanup are complete.
   Next, revise the released Paper IV TeX, PDF and publication-package copies as one render-verified
   unit so they cite the weighted all-`k` paper and route reusable base-monodromy claims to it.
   Preserve the ALL_K note as a low-`k` computational and historical supplement. Leave IV3 open
   until a concrete full-rank square-class/valuation proof establishes `R=0`.
5. **Variant-twin cleanup.** For each `__<hash>` twin resolved in §5(c), move the superseded copy
   to `09_historical…`; fix the DUAL_CONSTANT misfile (the `cella_residue` copy is the older
   revision). Resolve the spine naming trap (the `(2)` file is the newer v0.3).
6. **Ensemble bookkeeping (last).** Only after 1–5, and only once the Paper V gate spec + §7.3
   elliptic (a,b,c) gap + P8/AR enumerations are preserved in a successor (this map, or a future
   capstone), may `DBP_PAPER_ENSEMBLE_ARCHITECTURE` and the spine draft be reclassified from
   canonical/reference toward historical. Not before.

---

## 14. Proposed post-consolidation directory architecture

Keep the `Papers_Library` union-library machinery; adjust **placement**, not the build. Target
layout (subject_family is retained; the change is that each family's *canonical paper* sits in
`01_completed_papers`, proofs in `03`, supplements in `07`, superseded in `09`):

```
Papers_Library/
  01_completed_papers/
    dbp_role_channel_and_orbit_geometry/   dbp_orbit_calculus.{tex,pdf}         [Paper I]
    local_curvature_and_black_hole_metrics/ pfc_normal_forms.{tex,pdf}          [Paper II-general]
                                            lead7_kn_n3_dbp_metric.{tex,pdf}    [Paper II-KN]
                                            LOCAL_CURVATURE_CALCULUS_COMPLETE_v1.0.md
    dbp_periods_landen_and_elliptic_structure/ DBP_CURVATURE_PERIODS_…_v1.0.md  [Paper III ← MOVE here from 05,
                                                                                 after CCE-5/6 inserted]
    galois_horizon_and_kummer_covers/       galois_horizon_cover_v1_0.{tex,pdf} + publication_package/  [Paper IV]
                                            GENERIC_SYMMETRIC_MONODROMY_OF_WEIGHTED_MULTIQUADRATIC_SUMS_v1.0.md
                                                                                  [weighted all-k successor]
                                            self_glue_monodromy.{tex,pdf}       [companion]
    cella_residue_and_coupling_theory/      (SQG, R3, CCE-8 stay as foundations; Paper V when it exists)
  02_theorems_and_lemmas/    atomic theorems still cited as proof authority (Landen v1.1, CCE-8, R3;
                             ALL_K retained as computational/development supplement)
  03_proofs_derivations_and_audits/   proof supplements (surface-to-link, dual-surface stages, gauge-normal-form,
                                      Kummer/R9/rotating reports, GS Morse proof)
  05_expository_companions_and_research_maps/  research maps (GALOIS_K_ELLIPSE_v1_6), briefs, method notes
  06_hypotheses…/            open-program specs (ensemble architecture gate spec until a capstone absorbs it)
  07_certificates_data_and_reproducibility/   all verify_*.py, Macaulay2 suite, gate dumps, build kits
  09_historical_and_superseded_versions/   every __<hash> superseded twin, hashed run-logs, retired drafts
  _catalogue/               LEDGER.{csv,json}, ORIGIN_AND_BINDING_LEDGER.md, build_library.py, receipts
```

Governance regions unchanged: authority ledgers (`POST_8_*`, artificial-restriction
reconciliation, CCE gap ledgers) remain live under
`research/campaigns/CELLA_CONTINUATION_ENGINE/`; `Reports_Library`, `Campaign_Library`, and
`Evidence_Store` remain the binding/mirror/evidence layers, regenerated by their catalogue
builders. **Single most important move:** promote Paper III from tier 05 to
`01_completed_papers/dbp_periods_landen_and_elliptic_structure/` *after* it is mathematically
completed (§13 step 1) — until then it is canonical-in-role but not canonical-in-completeness.

---

## Completion statement

- Every relevant artifact discovered in the expanded census has a disposition (individually for
  the theorem/proof/companion/draft core; by class for the mirror/binding/certificate bulk).
- Every `HISTORICAL_ONLY` candidate has a named canonical successor and stated absence of unique
  units (§10).
- Every unique proof and exact construction is preserved (proof-supplement / computational-
  supplement retentions in §9); the remaining sole-proof-authority risks are Paper I U10/U11
  and the Paper III stage dossiers and CCE-5/6 theorems. Paper IV's GS route is retained as an
  independent derivation, while the weighted paper is now the canonical reusable proof authority.
- All exact mirrors and materially different variants are distinguished (§5).
- No open problem was declared closed by consolidation, and no closed theorem is described as a
  missing foundation (§12; the CCE-5/6 and normalized-incidence results are recorded as
  established).
- The original audit moved or deleted nothing. The 2026-07-16/17 update added one completed paper,
  applied the paper admission, graph-status cleanup and artifact-only certificate submissions,
  spliced the ALL_K theorem status, refreshed the live v1.6 map, and added non-destructive
  succession notices to five dated proof/audit/certificate records, including the `k=5`
  certificate whose historical R11 forecast is now superseded by the all-`k` theorem. No document
  was moved or deleted, and no commit or push was performed.
