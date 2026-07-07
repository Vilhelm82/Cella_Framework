# LEAD-7 — the n=3 DBP metric / complementarity lift (h_3) — CAMPAIGN BRIEF

**Status:** OPEN (2026-07-07). The GTD/DBP paper's own named open problem: at n=2 the
DBP metric `g^DBP = −h⁻¹`, `h = Σ_i κ_{c,i} dE^i⊗dE^i` exists with the complementarity
law; at n=3 each output chart carries several off-diagonal couplings, so `h` must be
generalized. **Does a canonical n=3 DBP metric exist?**
Source: `Reference_Material/gtd_vs_dbp.pdf` (re-verification rule: origin is claims, not
evidence). Prerequisite RC-5 structure tier: `verification/recert_gtd_dbp_n2.py`
(`d047d21b`, 11/11, byte-stable ×2).

## The metric design decision (Will's flag, 2026-07-07)

Will: the paper's `g^DBP = −h⁻¹` (channel-inverse, **diagonal**) was the "cheap and
easy" first-pass choice. The brief adopts a **better candidate as primary** and tests
it head-to-head:

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
