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
10/10 ×2, symbolic; report `reports/LEAD7_masscharge_zeros_theorem.md`). Uniform implicit
formula `Λ_{i,{M,j}} = 2M(U_ii U_j − U_i U_ij)/U_i³`; the six numerators factor as
(charge/U_S factor)×(all-positive bracket); `U_S = √disc/S_+ > 0` in the open wedge (horizon
Vieta). Hence every mass-charge coupling is strictly nonzero in the interior — its zeros are
EXACTLY `{J=0}=Ω=0`, `{Q=0}=Φ_e=0`, `{disc=0}=T=0`. So `g_F(u=0)` has **no interior
curvature singularity** — Test 3's interior-cleanliness is now a theorem, and the u=0
selection is structural (the charge-charge couplings, excluded at u=0, are the ones with
interior zeros = LEAD-2 isotropy strata). REMAINING: exact pole coefficients (KN
retrodiction tier), the only piece of the n=3 complementarity still at numeric tier.

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
