# RESEARCH_LOG.md — Galois Horizon Program
**Rules (standing):** append-only; one dated entry per work unit; corrections are
LOGGED as errata, never silently patched; paper edits accumulate in PENDING EDITS
and land in single revision passes; provenance over purity. A fresh session resumes
from STANDING STATE + the latest entries.

---

## STANDING STATE (pointer block — the one section that gets updated in place)

**The theory (current shape):** multifocal (k-ellipse) covers with reflection
invariant theory + non-solvable Galois descent + equivariant horizon thermodynamics.
Physical instance: multi-charge black holes; the 4-charge hole lives on an axial
4-ellipse (foci at heights N_i, sum of distances 4M).

**Papers:** galois_horizon_cover_v0.1.tex (sha 8ae94cfd…) — v0.2 single pass pending
(see PENDING EDITS). Prior-art: PRIOR_ART_REPORT_2026-07-10.md.

**Submission gates (open):** INSPIRE full-text sweep; domain-expert consult;
NPS / k-ellipse literature sweep (new, opened 07-10); Twofold-KN check (1006.4097)
for the charge-parity observation; Ω_L grep in CGLP §3.

**Artifact inventory (exact, sha-256 prefixes):**
- collision_field_read.py — f6a2486a — KN temperature-face field discriminator
- kn_three_face_field.py — 2cebac1a — three-face rationality (lead7 fusion)
- four_charge_crown.py — 8ff83aef — e2 = π²(4J²+N1N2N3N4); anchors
- abel_ruffini_black_holes.py — 675b3ced — S5 mass fiber; 3 points; (2,3) witnesses
- entropy_sum_resolvent.py — 7f778cb8 — entropy degree 10; γ primitive; V4 run rebuilt on it
- galois_horizon_cover_v0.1.tex — 8ae94cfd — paper draft
- CCAF_GALOIS_UPGRADES_v0.md — CCAF consumer/instrument spec
- PRIOR_ART_REPORT_2026-07-10.md — Will's sweep (method-gap disclosed)

**Campaign queue:** Q1 monodromy of the cover (braid generators = signed sub-balance
loci; coincidence strata certified); Q2 valuation↔inertia dictionary on the charge
ladder (needs DBP-on-algebraic-surfaces = Curvature Valence + CCAF target);
family Abel–Ruffini (all k≥4); equivariant sector theory (isotypic first laws;
shadow-trace invariants); arithmetic statistics (solvable thin set; wall primes);
rotating extension of the entropy theorem; T_{L,R} certification; e1..e4 wall
structure; Q-picture central charges; NPS determinantal lift (⇒ total reality).

---

## 2026-07-09 — Entry 0 (retro-summary: founding session)
KN: entropies = roots of z²−e1z+e2, e1=2π(2M²−Q²), e2=π²(4J²+Q⁴) rational; deck =
horizon swap; past disc<0 conjugate pair, Re frozen e1/2; branch simple off origin.
Splitting–heat identity S+−S− = 4π√Δ = 8πM S+T+ (Vieta identities certified on both
sheets). L/R dictionary from the grading: S_L=e1/2, S_R=2π√Δ; T_L=1/4πM, T_R=√Δ/(Me1);
harmonic 1/T± = 1/T_L ± 1/T_R; ratio² = 1−4e2/e1²; sector first laws + Smarr pair
[KNOWN: CGLP 1806.11134]; Ω_L≡0; charge-parity observation; Cardy/CMS/Wang–Liu match;
extremal chirality; attractor = Vieta (S_ext=√e2); EM duality = Sym(e2), doublets,
dyonic Smarr. Four-charge: e2 = π²(4J²+N1N2N3N4) double-anchored; S5 theorem (3 points,
(2,3) at p=53/23/31, totally real, physical root verified); ladder 1/1/4/5, k=2 seed =
wall product/M²; entropy non-radical (degree exactly 10; S_L² = (π²/4)γ primitive; five
sheets = all-plus + four single-flips); wall-norm ∏branches = 256∏₁₆(walls)/M⁶,
lc = −2²⁴M⁶; prior-art report (CGLP overlap central; obstruction layer NOT-FOUND;
2403.11823 confabulation killed by grep); paper v0.1 drafted+compiled.

## 2026-07-10 — Entry 1: k-ellipse identification
4M = Σ√(m²+N_i²) is the axial section of a 4-ellipse (foci (0,N_i)). Degrees match the
NPS k-ellipse formula at k=1..4; k=5 prediction 16 CONFIRMED by constructor. Opens:
determinantal lift (⇒ seeds as symmetric-pencil eigenvalues ⇒ total reality),
hyperbolicity-cone reading of the physical chamber, kinematics corollary (common-mass
reconstruction unsolvable for k≥4). GATE OPENED: NPS-lineage sweep before novelty wording.

## 2026-07-10 — Entry 2: degree & leading-coefficient theorem (Will)
Uniform pairing proof, no genericity: deg_u N_k = 2^{k−1} − ½C(k,k/2)·[k even].
Unified lc formula: lc = (−1)^{2^{k−1}−b_k} (16M²)^{b_k} ∏_{s_ε>0} s_ε², b_k = balanced
pairs. Odd k: sign +, M-free, PERFECT SQUARE (k=5: 1215²; k=3: 9 — both machine-certified,
M symbolic). Even k reproduces certified −2²⁴M⁶. Corollary certified at k=5: odd-k wall
identity ∏branches = 4³²∏₃₂(walls)/1215² (constant denominator — the M-weight of lc lives
entirely in balanced pair-decay classes). Note for NPS lift: odd-k positive-square lc is
determinantal-friendly normalization.

## 2026-07-10 — Entry 3: ERRATUM E1 + reflection geometry (Will's k-ellipse note)
**ERRATUM E1.** Draft §2 and ledger claim "T is odd under the swap, T² invariant" is
FALSE as a covariance statement: σ(T+) = T− ≠ −T+ (sheet-dependent denominator).
CORRECT: Θ := S·T is the canonical odd covariant — σ(Θ) = −Θ; certificate already
in-session (T+S+ = −T−S− = √Δ/2M, verified True/True). T is MIXED (odd numerator over
branch-dependent denominator). Survives: T_R odd, T_L even (√Δ grading); all identities.
**Geometry (new):** horizon swap = axial reflection τ: m→−m of the multifocal axis;
S± = π√(∏(w_i±m)) swap under τ. Parity dictionary: odd {m, S+−S−, S·T};
even {u, S++S−, S+S−, w_i}.
**Cover tower (new):** axis cover deg 10 in m —(τ-quotient)→ quintic deg 5 in u.
Quadratic lifts: m (m²=u) and y (y²=γ). Involutions: (m→−m) = horizon swap;
(y→−y) = simultaneous entropy-sign conjugation; both = signed swapped conjugation.
**Descent theorem (architecture accepted, write-up owed):** w_i ∈ F(m) on the
normalized axis component (signs locally constant); w_i even under τ ⇒ w_i ∈ F(m)^τ
= F(u) = K generically. Point-B certificates RE-TYPED: from foundation to exact
specialization witness of the generic descent. Proof chain: normalization → F(m) →
τ-fixed → K → α,β ∈ K → α²−uβ² = P² → γ ∈ K → entropy field K(√γ).
Also proven-in-prose: u not a square in K via the wall norm (16 distinct linear
factors at odd exponent; 256/M⁶ = (16/M³)² square).

## 2026-07-10 — Entry 4: V4 certification — tower CLOSED
Run (rebuilt on entropy_sum_resolvent machinery, point B): E_u = Res(N, Y²−u) and
E_{uγ} = Res(N, Y²−uγ) both degree 10, both IRREDUCIBLE over Q. With E_γ (prior run):
u, γ, uγ all non-squares ⇒ square classes of u and γ independent in K*/K*² ⇒
Gal(K(m,y)/K) = V4 at B ⇒ generic (specialization). THEOREM: the full static
ordered-horizon cover has degree 20 over the physical field — a biquadratic (V4)
lift of the S5 quintic core. Slogans now theorem-grade:
(i) horizon swap is axial reflection; S·T its canonical odd covariant;
(ii) the horizon cover is a biquadratic lift of the S5 reflection quotient of an
axial 4-ellipse;
(iii) signed distances descend through the reflection-fixed field F(m²)
[(iii) pending write-up; witnessed].

---

## PENDING PAPER EDITS (accumulate here; land as ONE v0.2 pass)
1. §2 ERRATUM E1: replace "T odd, T² invariant" with Θ = S·T odd-covariant statement
   + parity dictionary; soften abstract/intro "temperature is the Galois-odd datum"
   → "the heat content S·T is the canonical odd covariant; temperature data lives in
   the odd sector (T_R odd, T_L even)".
2. Appendix B → general degree + lc proposition (Entry 2), with k=3/5 certificates
   and the odd-k square law; add odd-k wall identity remark (k=5 instance).
3. New section: multifocal identification (Entry 1) — foci = charges, NPS degree
   match through k=5, determinantal-lift target. GATED on NPS sweep.
4. New subsection: reflection geometry + cover tower + V4 theorem (Entries 3–4);
   degree-20 ordered-horizon statement; involution table.
5. Reframe Thm 4.4: descent theorem as the proof, point-B as specialization witness
   (once write-up lands).
6. Kinematics corollary remark (common-mass reconstruction, k≥4).
7. Citation TODOs from v0.1 bib (Ansorg–Hennig pin, Cvetič–Youm 4D pin, 1912.08988,
   class-numbers author list).

## OPEN CERTIFICATIONS / PROOF DEBTS
- Descent theorem write-up (normalization + component-sign argument + irreducibility
  hypotheses stated cleanly).
- Rotating extension (same tower over same quintic + J bookkeeping).
- T_{L,R} non-radicality; e1..e4 wall structure; Q-picture central charges.
- NPS determinantal lift → total-reality proof.
- Q1 monodromy campaign (roadmap: complex sub-balance loci as braid generators;
  inertia at coincidence strata; check against self-glue gcd-indexed taxonomy).

## 2026-07-10 — Entry 5: audit of GALOIS_K_ELLIPSE_RESEARCH_MAP (Will's doc)
Verdict: structurally sound; status vocabulary adopted program-wide. Updates
applied in v1.1 (outputs/collision/):
- PROMOTIONS (map predated Entry 4): K(m) deg-10 ESTABLISHED; u*gamma
  certified; K(m,y) = 20, V_4 ESTABLISHED; R8 promoted; Stage 3 complete
  except closure-group (R9); Stage 6 item 2 (k=5 degree 16) done.
- MISSING THEOREMS ADDED: lc law + odd-k square + odd-k wall identity (R16);
  physical-sheet isolation + collision classification (R17).
- MATHEMATICAL CORRECTIONS (Branch H): locus 6 ≡ locus 2 identically
  (z^2 = gamma - 4P); statically 1 ≡ 2 ≡ 6 by AM-GM (alpha >= P, equality iff
  m=0, since beta > 0); locus 5 (gamma=0) never on the real physical branch
  (gamma >= 4P > 0). Six loci reduce to four on the static family.
- STATUS SHARPENING: k=5,6 norm degrees are theorem-grade (pairing proof +
  k=5 constructor); only irreducibility/minimality remains predicted.
- GUARDRAILS: #2 retargeted to the closure group; #6 sharpened (field
  statements generic by specialization; DESCENT genericity awaits the
  normalization lemma — distinct); #10 added (CGLP attribution).
- ANCHORS VERIFIED: NPS math/0702005 (degree theorem + determinantal rep +
  weighted/higher-dim extension confirmed from source); Jiang-Han 1908.01414
  exists (contents unswept). CY 9603147 pin still on the sweep list.
