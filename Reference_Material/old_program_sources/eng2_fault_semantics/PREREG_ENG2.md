# STAGE ENG2 — FAULT SEMANTICS IN INVARIANT LANGUAGE (FROZEN pre-battery, S-2026-07-05b; Will: "yes run (a)")
The B.3 staging promised in PREREG_v2 PB.3, now grounded in the ratified
triangle theorem (dashboard I.3b). Objects: exact-ℚ channel functionals at
fixed g — Δ_c = −q·e_2(PH_cP) (e_2 tier, triangle-decomposed), κ̂_c :=
e_{n−1}(P H_c P) (top/OG tier), K̂ := e_{n−1}(P H P); at n=3 the two tiers
coincide and κ̂_c/K̂ = κ_c/K_G verbatim (q cancels). OG clause under test
(embedded verbatim, grader string-matches): "κ_c / K_G is invariant under
uniform gradient scaling. Coupling faults change the ratio; self-faults
preserve it." (OG_lloyd_decomposition.md §10.2.)

## Predictions (FROZEN; graded mechanically; clauses embedded)
| id | statement | class | prediction |
|---|---|---|---|
| PE.0 | n=3 keystone anchors: κ̂_c = −2/7, K̂ = −6/7, κ̂_c/K̂ = 1/3 = spec κ_c/K_G; triangle decomposition regression at all fixtures | sanity | MUST HOLD (else K-E0 pipeline defect, no verdicts) |
| PE.1 | NUMERATOR EXACTNESS: under S1 and S2 self-fault families, Δ_c(t) and κ̂_c(t) are CONSTANT polynomials in t (exact, full coefficient check, every fixture) | discriminating | HOLDS — near-certain (H_c-only functionals; the theorem's one-liner); FAIL = pipeline defect class |
| PE.2 | SCALING: κ̂_c/K̂ invariant under g → t·g at t = 2, 3 (H fixed), every fixture | discriminating | HOLDS — the OG scaling clause, exact |
| PE.3 | COUPLING FAULTS MOVE THE RATIO: d/dt[κ̂_c/K̂] at t=0 is NONZERO for F1 and F2 at every fixture | discriminating | HOLDS at generic fixtures — moderate-high; any zero = record and route (accidental orthogonality vs structure) |
| PE.4 | OG SELF-FAULT RATIO CLAUSE (discriminating test of the literal law): d/dt[κ̂_c/K̂] at t=0 under S1, S2 | discriminating | prediction: NONZERO generically (literal OG clause FAILS; corrected law = PE.1 numerator exactness) — either outcome structural; if zero anywhere, route to Will (unexpected K̂ invariance) |
| PE.5 | LOCALIZATION (the V4 sensor upgrade): for F1 on edge e* = (0,1): {S : d/dt Δ_S ≠ 0 at t=0} == {S ⊇ e*} exactly, every fixture n ≥ 4 (Δ_S = triangle channel from the I.3b decomposition) | discriminating | HOLDS — support inclusion is proven (δν supported on e*); the staked content is NON-vanishing on every S ⊇ e* at the pinned fixtures |

## Kill conditions (armed)
- **K-E0:** PE.0 fails ⟹ HALT, no verdicts.
- **K-E1:** PE.1 fails ⟹ HALT (contradicts a proven triviality ⟹ bug).
- **K-E2:** PE.3 or PE.5 fail ⟹ HALT, route to Will — the sensor-law
  content is dead or fixture-degenerate; no widening.
- PE.4: no kill either way — it is the reproof's discriminating clause;
  outcome recorded and fed to the theorem doc + registry-20 correction row
  proposal if the literal clause fails.
- Envelope 1200 s / 8192 MB; byte-stable ×2 mandatory.

## Pins (Rule 1.9) — freeze_pins_eng2.sha256
This file; fixtures_eng2.json; SHADOW_LAW_THEOREM.md (ratified authority for
the decomposition); evals/dbp_involution/rep_utils.py (unused by battery —
NOT pinned); Build_Docs/V3_OG_reference/V3_OG_Decomposition_Knowledge_Base/OG_lloyd_decomposition.md
(OG clause source). Battery refuses on sha mismatch or clause drift.
role=probe + ledger. Probe: polynomial-in-t exact expansion; referee
(independent): finite-difference exact evaluation at t = 1/7, must match the
polynomial's value — two computation paths per functional.

## Status moves (frozen)
PE.0–PE.3 + PE.5 PASS ⟹ CL-ENG2 → the fault-semantics theorem holds in
corrected-and-upgraded form at the tested tiers: numerator exactness +
scaling invariance + ratio sensitivity + triangle localization; general-n
proofs land in CL_ENG2_FAULT_SEMANTICS.md (derivation, no battery); ledger
CL-ENG2 row moves NOT_YET_PROBED → DEMONSTRATED (fixtures) + PROVEN (doc
clauses). PE.4 outcome: if literal OG clause fails ⟹ registry-20 correction
row PROPOSED for the OG artifact (correction, not refutation — OG's
operational content survives as the numerator law).

frozen: true · author Claude-session · substrate [BOX] · S-2026-07-05b
