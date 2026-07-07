# LEAD-7 — the n=3 DBP metric / complementarity lift (h_3) — CAMPAIGN BRIEF

**Status:** OPEN (2026-07-07). The GTD/DBP paper's own named open problem: at n=2 the
DBP metric `g^DBP = −h⁻¹`, `h = Σ_i κ_{c,i} dE^i⊗dE^i` exists with the complementarity
law; at n=3 each output chart carries several off-diagonal couplings, so `h` must be
generalized. **Does a canonical n=3 DBP metric exist?**
Source: `Reference_Material/gtd_vs_dbp.pdf` (re-verification rule: origin is claims, not
evidence). Prerequisite RC-5 structure tier: `verification/recert_gtd_dbp_n2.py`
(`d047d21b`, 11/11, byte-stable ×2).

## Candidate F (mass-charge inverse-channel) — LIKELY THE n=3 DBP METRIC (2026-07-07)

Will surfaced `Reference_Material/LEAD7_Candidate_F_Elementary_Pair_Channel_Inverse_Metric.md`
(invert-before-sum, fixing D's zero-blind aggregation). Ran Test 3
(`verification/lead7_test3_candF_n3.py`; report `reports/LEAD7_test3_candF_n3.md`):

- **F(u=1)** (full invert-before-sum) FIXES D's failure: R diverges on ALL THREE role
  boundaries with the **paper order law** — extremal order 3 (generic), Ω=0 & Φ_e=0 order 4
  (reflection-fixed). BUT it has a **spurious interior curvature pole** where the
  charge-charge coupling `Λ_{Q,{Se,J}}=0` (interior, ≠ Davies) — the doc's §8 failure.
- **F(u=0)** (mass-charge couplings only) reproduces the **FULL complementarity AND is
  interior-clean**: orders 3/4/4, R finite on Davies D3, no spurious interior poles
  (scanned M∈{1.5,2,3}, ~1300 pts + direct coupling zero-hunts). Reduces to A at n=2.
- **u=0 is UNIQUELY selected**: u>0 → interior pole; u<0 → not positive-definite. Only u=0
  is both interior-clean and pos-def, and it keeps every boundary divergence (all in the
  mass-charge sector).

**LEAD-7 CENTRAL QUESTION ANSWERED (numerical/EMPIRICAL tier): YES, a canonical n=3 DBP
metric exists — the mass-charge inverse-channel metric**
`g_DBP,ii = q_i² · Σ_{mass-charge pairs ρ of chart i} 1/Λ_{i,ρ}²`. Not the norm-inverse (D,
too coarse), not the pullback (B, wrong valuation), not full invert-before-sum (F u>0, too
sharp — interior poles). Selection rule banked: **zero-sensitive at the mass-charge channel
level, exclude the charge-charge couplings** (their zeros are LEAD-2 isotropy strata).
NEXT (EMPIRICAL→certified): prove mass-charge zeros = role divisors exactly; exact pole
coefficients (KN retrodiction tier).

**UPDATE — mass-charge zeros = role divisors PROVEN** (`verification/lead7_test4_masscharge_zeros.py`,
11/11 ×2, symbolic; report `reports/LEAD7_masscharge_zeros_theorem.md`). Uniform implicit
formula `Λ_{i,{M,j}} = 2M(U_ii U_j − U_i U_ij)/U_i³`; the six numerators factor as
(charge/U_S factor)×(nonneg-coefficient bracket); `U_S = √disc/S_+ > 0` on the **outer
physical wedge** `W₊ = {S,J,Q>0, U_S>0} = {S²>π²(4J²+Q⁴)}` (horizon Vieta). Domain is
`W₊`, NOT `{disc>0}` — the latter includes the inner branch (`U_S<0`) where a numerator can
vanish interiorly (counterexample `(π√3/2,1/4,1)`, cert T4-e). On `W₊` every mass-charge
coupling is strictly nonzero — its zeros/native-poles are supported EXACTLY on `{J=0}=Ω=0`,
`{Q=0}=Φ_e=0`, `{U_S=0}=T=0` (extremal enters as the native `U_i³` pole, not a numerator
zero). So `g_F(u=0)` is analytic positive-definite on `W₊` ⟹ finite analytic curvature ⟹
**no interior curvature singularity** — Test 3's interior-cleanliness is now a theorem, and
the u=0 selection is structural (the charge-charge couplings, excluded at u=0, are the ones
with interior zeros = LEAD-2 isotropy strata).

**UPDATE — KN retrodiction tier** (`lead7_test5_pole_orders_n3.py` 12/12 ×2 orders;
`lead7_test6_pole_coeffs_n3.py` reflection coefficients; report
`reports/LEAD7_retrodiction_n3.md`). Pole ORDERS of R[g_F(u=0)] pinned to exact integers:
extremal T=0 order 3 (generic), Ω=0 and Φ_e=0 order 4 (reflection-fixed) — the n=3 Result-6
law. Reflection-fixed COEFFICIENTS in EXACT closed form via a universal identity (R's
reflection-face leading coefficient = −14/B, B = leading coeff of the collapsing metric
component, symbolic): C_Ω(S,Q) = −3584 Q²S⁵π³(πQ²−S)²/[...], C_Φ(S,J) = −14336
J²S⁵π⁵(2πJ−S)²(2πJ+S)²(4π²J²+S²)/[...], matched to direct curvature to ~20 digits; corner
factors (πQ²−S)², (2πJ−S)² vanish on the divisor corners (Ω=0∩extremal, Φ_e=0∩extremal).
**Extremal coefficient CLOSED (`lead7_test7_extremal_coeff_n3.py`):** C_ext(S,Q) is an
EXACT rational function of (S,Q,π), via the structural identity C_ext=(1/A₂)∂_S ln(g_JJ g_QQ)
at extremal with A₂=(4U+U_J²+U_Q²)²/(4U)(1/U_J²+1/U_Q²) (same shape as the reflection B).
Key: the implicit-formula couplings are RADICAL-FREE (rational in S,J,Q,π), so g_JJ,g_QQ and
A₂ are rational and on the extremal surface J²=(S²−π²Q⁴)/(4π²) the whole coefficient is
rational; verified vs direct curvature.

**METRIC NORMALIZATION (correction, byte-verified):** the certified metric carries the graph
"1+": q_i=1+|∇f_i|²=1+(4U+U_a²+U_b²)/U_i² (n=2 norm q0=1+a²+b², recert_gtd_dbp_n2.py), so
G_i=(U_i²+4U+U_a²+U_b²)²·U_i²/(4U)·Σ(1/D²). The +U_i² is essential — the graph-norm metric
reproduces the banked direct-curvature C_ext EXACTLY (−0.0660176096 to 10 digits), the no-"1+"
form gives −0.0656…; it matters only in the finite transverse channels (on a collapsing channel
q→∞, so A₂/C_Ω/C_Φ are normalization-independent, B_J identical either way). The no-"1+" gate
script `lead7_test8_extremal_gate_replacement.py` is REFUTED (wrong metric), kept as the
mis-step record.

**Extremal N_ext gate CLOSED for the graph-norm metric (`lead7_test8_extremal_gate_graphnorm.py`,
byte-stable ×2):** C_ext<0 at EVERY open point of the extremal edge (not merely on a dense grid),
so the extremal pole has exact order 3 throughout T=0 (upgrades "generic open points" → "all
open points"). Full-edge coefficient-positivity certificate: sign(C_ext)=sign(L_ext),
L_ext=∂_S log(g_JJ g_QQ)|ext; parametrise the edge by q=Q²>0, t=S/(πQ²)>1 so L_ext=−P/D; after
extracting positive monomials and substituting t=1+r (r>0), π²=9+b (b>0, from π>3), D factors
into 9 coefficient-positive factors and P=Aq²+Bq+C has B,C coefficient-positive with
A=C₀·π²t²·(π²F+G), F=(t−1)·t³(t+3)³·H̃, H̃=2t⁵+5t⁴−15t³−7t²+15t+8 degree-5 positive on [1,∞)
(Sturm), 9F+G>0 on [1,∞) (Sturm); since π²>9, π²F+G=(π²−9)F+(9F+G)>0 ⟹ A>0 ⟹ P>0, D>0 ⟹ L_ext<0.

**GENERAL PARITY-FIXED NORMAL FORM (Test 10, first-principles Ricci m=1,2,3, clean ×2):** the
−14/B reflection identity is the m=2 case of `ds²=Bx²dx²+x⁻²Σ_{α=1..m}A_α dy_α²` ⟹
`R=−m(m+5)/B·x⁻⁴` EXACTLY, amplitude-independent (m=1→−6, m=2→−14, m=3→−24). Split
m(m+5)=6m+m(m−1) (radial focusing + transverse fibre shear). Corollary: y-dependent B(y),A(y) +
even subleading ⟹ leading coeff −m(m+5)/B(y). So C_Ω=−14/B_J, C_Φ=−14/B_Q are inevitable (3D
state space, m=2), not symbolic coincidences.

**DOUBLE-REFLECTION (SCHWARZSCHILD) CORNER (Test 9, exact-partial curvature, clean ×2):** where
Ω=0 ∩ Φ_e=0 meet (J=Q=0, S=s), the curvature is MILDEST not wildest. Along Q=ε, J=ρε^a:
balanced (a=1) radial order EXACTLY 2 (R₀(1,1)=−1801.25<0 finite); Newton wedge
m(a)=max(4a−2,4−2a), vertex (1,2), min m=2 on the diagonal (two order-4 collapses partially
cancel). Metric limits closed-form: ε⁶G_S→N₀²s⁵/[π(s+8πρ²)²] (N₀=s/π+1/(16π²); the "1.04×
schematic" = (1+1/(16πs))² graph-norm correction), G_J→N₀²πρ²/s, G_Q→N₀²s/(4πρ²). Boundary
links κ_Ω=−3584π³s/(16πs+1)², κ_Φ=−14336π⁵/[s(16πs+1)²] (exact residues of C_Ω,C_Φ). R₀ is NOT
the two-face sum: mixed excess M(1,1)=−89.70 (G_S mixed-denominator fingerprint).

**n=3 COMPLEMENTARITY RETRODICTION COMPLETE (fully symbolic):** orders 3/4/4, all three
leading coefficients (C_Ω, C_Φ, C_ext) in exact closed form, AND the extremal order-3 pole
established at every open point (gate closed, Test 8). Combined with the metric identification
(Test 3), u=0 selection + interior-cleanliness theorem (Test 4), the n=3 DBP metric
g_F(u=0) = mass-charge inverse-channel metric is fully established and its complementarity
law fully retrodicted. LEAD-7 central question resolved. Formal proof paper drafted
(`paper/lead7_kn_n3_dbp_metric.tex`). Remaining (optional, LEVER payoff): lift the
metric-identification/orders from EMPIRICAL to a closed-form proof (replace Test 5 numeric
fits with the exact Laurent lemmas), and the physics-novelty writeup.

## Candidate D (output-channel norm inverse) — TEST 1/2 VERDICT (2026-07-07)

Will surfaced `Reference_Material/LEAD7_Candidate_D_Output_Channel_Norm_Inverse_Metric.md`
(the direct n=3 generalization of the paper's diagonal metric A: per output chart,
`C_i(t)=[Λ²_{M,j}+Λ²_{M,k}+t·Λ²_{j,k}]/q_i²`, `g_D,ii=1/C_i`). Ran Tests 1 & 2.

- **Test 1** (`verification/lead7_test1_candD_n2.py`, 6/6 ×2): D reduces **exactly** to the
  paper metric A at n=2 (`g_D,ii=1/C_i=−1/κ_c,i`), the weight `t` is structurally absent
  (no charge-charge pair at n=2), and `R[g_D]` reproduces the paper's order law
  (extremal 3, Schwarzschild 4, finite on Davies). Constraint (1) holds.
- **Test 2** (`verification/lead7_test2_candD_n3.py`, 9/9 ×2; report
  `reports/LEAD7_test2_candD_n3.md`): D_Frob (t=1) on Kerr-Newman
  `M²=S/4π+πJ²/S+Q²/2+πQ⁴/4S` — **correct n=2 lift** (exact t-independent Q→0 reduction to
  Kerr by Q-parity; positive-definite; `g~F²` role-boundary collapse; curvature diverges
  on extremal T=0), but its intrinsic curvature (Ricci scalar AND Kretschmann, exact
  partials, formula validated on flat/sphere) is **FINITE on the reflection-fixed faces
  Ω=0 (J=0) and Φ_e=0 (Q=0)**. The t-scan (t=0,½,1,2,5) shows the miss is **not repairable
  by t**. So the diagonal `D(t)` family does NOT reproduce the full three-boundary
  complementarity — it diverges on only 1 of 3 physical role boundaries.

**Consequence:** this confirms the doc's own fallback — the diagonal ansatz is too weak; the
missing divergences live in the off-diagonal/interaction structure `D` discards. LEAD-7
routes to **Candidate E (pair-channel tensor)** with a charge-charge incidence form in
`dE_j−dE_k`. Mapped to the kill-list this is **K-2-adjacent** (the non-descent of the
complementarity to a canonical *diagonal* S₃-equivariant lift is itself a result). The
banked LEAD-7 guard held decisively: judge by R[g]/K, never by metric collapse — the metric
DOES collapse on all three faces, but the curvature does not.

## The metric design decision (Will's flag, 2026-07-07) — UPDATED after the pole check

**POLE-ORDER VERDICT (`reports/LEAD7_pole_orders.md`):** the head-to-head is decided at
n=2. Candidate A (paper diagonal) gives R[g] pole orders **exactly 3 (extremal) / 4
(Schwarzschild)**, matching the paper's Result 6 — method validated. **Candidate B (the
carrier-pullback) FAILS:** R diverges order ~8 on extremal and does NOT diverge on
Schwarzschild — not even complementary. My earlier promotion of B was on the weaker
"metric-diverges-on-boundary" check; the *curvature* pole order (the real diagnostic)
refutes it. **Candidate C (three-channel)** is complementary but with wrong orders
(~8/4). So the paper's "cheap" A carries the canonical n=2 law; the pullback shortcut
does not. Primary is now: **generalize the diagonal construction to n=3** (or find a
different curvature-matching metric — the pullback is out). The candidate list below is
kept for the record; the verdict supersedes its "Candidate B primary" recommendation.

Will: the paper's `g^DBP = −h⁻¹` (channel-inverse, **diagonal**) was the "cheap and
easy" first-pass choice. The brief originally adopted a candidate as primary and tested
it head-to-head (now decided against it):

- **CANDIDATE A — the diagonal channel-inverse (paper's "cheap" one):**
  `h = diag(κ_{c,i})`, `g^DBP = −h⁻¹`. Diagonal ⟹ discards off-diagonal/interaction
  structure; inverts channel *values* (dimensionally odd); **has no canonical n=3
  generalization** — you must guess how to arrange the several off-diagonal couplings.
  This ambiguity IS the paper's stated open problem.

- **CANDIDATE B — the carrier-pullback (information) metric [PRIMARY, recommended]:**
  ```
  g_ab = Σ_ρ (∂ κ_c^ρ / ∂E^a)(∂ κ_c^ρ / ∂E^b)   = (dO)ᵀ(dO),
  ```
  the pullback of the flat metric on carrier-space via the faithful carrier map
  `O = (κ_c^ρ)`. Why it is better:
  1. **Canonical** — forced by the faithful carrier (orbit-calculus Cor.: `det ∂O =
     8Λ_PΛ_DΛ_S/q₀⁶`), no ad-hoc diagonal/inverse choice.
  2. **S₃-equivariant + factors through O by construction** — canonicity constraints
     (2),(3) are automatic, not later checks.
  3. **Degenerates exactly on the isotropy/role-boundary loci** (`Λ_ρ=0`) — constraint
     (5) automatic.
  4. **GENERALIZES to all n with zero ambiguity** — `O` is defined for every n
     (n=3: `O∈ℝ³`; n=4: `ℝ⁶`), so `(dO)ᵀ(dO)` is the n=3 metric *without* the "arrange
     the couplings" guess that stalls Candidate A. **This dissolves the paper's open
     problem rather than working around it.**
  5. **Complementarity CONFIRMED numerically on Kerr (n=2)** — `g₀₀` diverges on both
     physical boundaries (extremal `σ→J`: 6.5e9→5.9e21; Schwarzschild `J→0`:
     3.8e6→1.5e11) and is finite on Davies (6.9e-5). Same qualitative complementarity
     as the paper's `g^DBP`, from the more principled construction. (Probe:
     `reports/LEAD7_pullback_probe.md`.)

- **Other candidates to keep on the bench:** the anisotropy-Hessian metric
  `Hess(A_c)` (A_c = the natural DBP invariant, degree-2 in O); a three-channel metric
  reproducing `K_G = κ_c+κ_int+κ_s` (uses interaction/self, not just coupling).

## Canonicity constraints (all six bind, per LEADS)

(1) exact reduction to the n=2 construction; (2) S₃-symmetry; (3) factors through O;
(4) controlled sign/definiteness on the Kerr-Newman wedge; (5) degenerates/blows up on
the role-boundary divisors `T=0, Ω=0, Φ_e=0`; (6) testable against the Kerr-Newman
Davies surface D3 (the complementarity). Candidate B satisfies (2),(3),(5) by
construction and (4),(6) empirically at n=2; (1) and the n=3 (6) are the campaign work.

## Prerequisite RC-5 (n=2 GTD/DBP spine, re-verified in-repo)

- **Structure tier: DONE** (`recert_gtd_dbp_n2.py` `d047d21b`, 11/11 ×2): Christodoulou,
  Davies, the 2-jet + channels (fixture (σ,J)=(8,6)), radical cancellation, `g^DBP`
  positive-definite, boundary=chart-singularity.
- **Retrodiction tier: NEXT** — the paper's pinned pole-order coefficients `C_ext =
  2(8J+1)/(π(4J+1)³)`, `C_sch = −96πS/(16πS+1)²` (π-frame, ℚ(π)), plus the complementarity
  order law (order-3 generic / order-4 reflection-fixed). DO-NOT-CITE: paper eq. (28),
  Mahanta `m_sg=0`.

## Stages

- **Stage 0 (prereq):** RC-5 retrodiction tier + fix the pole-order law for BOTH
  candidate metrics at n=2 (which reproduces the paper's order-3/4 law?).
- **Stage A:** the n=3 lift. Candidate B is defined immediately (`(dO)ᵀ(dO)`, O the n=3
  carrier). Verify (1) reduction to n=2, (4) definiteness on the KN wedge, then (6) the
  D3 complementarity test — does the DBP curvature diverge on the KN role boundaries and
  stay finite on the n=3 Davies surface? Pole orders + leading coefficients recorded.
  Candidate A (if pursued) needs the coupling-arrangement enumeration first.
- **Stage B (branch):** if Candidate B passes (6), it is the canonical n=3 DBP metric
  (a cleaner result than the paper's target). If it fails, enumerate the S₃-equivariant
  bilinear forms on O and screen (the original LEADS plan) — Candidate B is then one
  screened form among them.

## Kills / exit ramp

K-1: Candidate B fails reduction to n=2 (constraint 1) → drop to the enumeration.
K-2: no S₃-equivariant form on O reproduces the complementarity at n=3 → the deliverable
is the **obstruction theorem** (nonexistence of a canonical S₃-equivariant lift is a
result, not a failure). K-3: the two candidates give different n=2 pole orders and only
one matches the paper → that one is selected, the mismatch banked.

## Output ledger

RC-5 cert (done, extend to retrodiction tier) · the metric-candidate comparison at n=2
· `reports/LEAD7_pullback_probe.md` · Stage-A n=3 lift + D3 test · LEAD-7 verdict ·
BOOT/LEADS update. Physics-novelty channel (GTD LEVER Tier-2 row) is the payoff.
