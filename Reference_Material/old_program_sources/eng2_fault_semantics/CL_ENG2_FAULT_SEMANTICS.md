# CL-ENG2 — FAULT SEMANTICS IN INVARIANT LANGUAGE (corrected + upgraded)
**Status: clauses 1, 2, 4a PROVEN (derivations below); clauses 3, 4b
DEMONSTRATED at pinned fixtures ×2 (records `b6c3e0e6`, PREREG_ENG2 pin
`0c11ef30`). GROUNDED — Will, S-2026-07-05b (correction row + CL-ENG2 row
canonical-track on his confirmation).**
**Scope: hypersurface channel functionals at fixed base point; exact-ℚ;
tiers Δ_c (e_2, triangle-decomposed per I.3b) and κ̂_c = e_{n−1}(PH_cP),
K̂ = e_{n−1}(PHP); at n=3, κ̂_c/K̂ = κ_c/K_G verbatim.**

## The theorem (four clauses)
**1. Numerator exactness [PROVEN, all n, all faults].** Every functional of
(g, H_c) alone — the full tower e_r(P H_c P), r = 1..n−1, hence Δ_c, κ̂_c,
and every triangle channel Δ_S — is EXACTLY invariant under any self-fault
(perturbation supported on diag H). Proof: diagonal perturbations do not
enter H_c; δν = 0 identically. ∎ (Battery: constant-polynomial certificates,
all fixtures, all self-families.)

**2. Scale invariance [PROVEN, all n] — stronger than OG's clause.**
P(tg) = P(g) (the projector depends on g only through the ray), so every
q-cleared channel e_r(PH_cP) and e_r(PHP) is INVARIANT outright under
uniform gradient scaling — numerator and denominator separately, not
merely their ratio. OG's ratio-invariance is the shadow of this. ∎

**3. Coupling sensitivity [DEMONSTRATED ×2; generic, not universal].**
d/dt[κ̂_c/K̂] ≠ 0 at t=0 for the pre-declared single-edge and generic
coupling-fault families at every pinned fixture (n = 3,4,5). Scope fence:
non-vanishing is a genericity statement certified at fixtures; special
(g,H) with accidental orthogonality exist in principle.

**4. The OG ratio law, corrected.**
(a) [PROVEN + DEMONSTRATED] Self-faults preserve κ̂_c exactly (clause 1) but
move K̂ generically, so **the literal OG clause "self-faults preserve the
ratio" is FALSE** — refuted at every fixture including the n=3 keystone
itself (d/dt[κ̂_c/K̂] = 1/18 under the vertex-0 self-fault). (b) The law's
operational content survives in corrected, sharper form: **the self-fault
invariant is the numerator κ̂_c (indeed the whole coupling tower), not the
ratio.** A sensor built on κ̂_c alone strictly dominates the OG ratio
sensor: same coupling sensitivity, exact (not approximate) self-fault
blindness, and scale invariance without needing the quotient.
→ registry-20 correction row PROPOSED for `OG_lloyd_decomposition.md` §10.2.

**5. Localization — the V4 upgrade [support PROVEN; non-vanishing
DEMONSTRATED ×2].** Under a single-edge coupling fault at e*, the moved
triangle channels are exactly {Δ_S : S ⊇ e*} (support inclusion is immediate
from I.3b: δν is supported on e*; equality certified at all n≥4 fixtures).
The fault's edge is recoverable from which triangle channels move — a
localization sensor the scalar OG ratio never had. With n−2 moved triangles
out of C(n,3), the faulted edge is the common intersection.

## Machine record
PREREG_ENG2 frozen pre-battery (pins `0c11ef30`/`8678c095`; OG clause
embedded verbatim, gate enforced — one CLAUSE_DRIFT refusal fired during
build when the grader's copy didn't match the frozen wrapping; grader
conformed to the frozen text, never the reverse). Battery ×2 byte-identical
`b6c3e0e6`; probe = exact polynomial-in-t interpolation, referee = direct
evaluation at t = 1/7, agreement enforced per functional per family. Zero
defect chains.

*Nothing canonical until Will signs. Prior-art posture: fault-diagnosis via
principal-minor towers is engineering-adjacent; the localization clause
rides the I.3b decomposition (novelty candidate lives there, sweep owed).*
