# OPEN OBLIGATIONS LEDGER

Live ledger. An obligation leaves this file only by being (a) discharged with a named gate
verifier, (b) converted into a typed stratum/hypothesis, or (c) explicitly moved out of scope
with its mathematical cause stated.

## Missing computational supplements (Stage 0 finding)

| Item | Status | Cause |
|---|---|---|
| `dbp_curvature_reduction_harness.py` | MISSING from repository | named in plan 5.4; no copy exists anywhere in the repo tree |
| `char2_generalization.py` | MISSING | named in plan 5.4 (all-n scaffold); referenced by dbp_four_role_calc_log_v8.md |
| `verify_campaignH_parity.py` | MISSING | same |
| `verify_against_paper.py` | MISSING | same |

Consequence: the all-`n` carrier claims of the four-role log remain frontier evidence with NO
executable support in this package. They are not load-bearing for the first paper (plan 5.4
"optional"), and nothing below cites them as proof.

## Broken shim path (plan 5.4 audit flag)

`lead7_variable_transverse_weighted_jet.py` imports its verifier from a nonexistent parent-tree
location. Disposition: packaged copy in 04_VERIFICATION_LEGACY/weighted_jet/ sits BESIDE
`verify_lead7_variable_transverse_weighted_jet.py`; the new-verification runner calls the
verifier directly, never through the shim. (Discharged by 05_VERIFICATION_NEW/regression/run_all.py.)

## Proof obligations (PO-1 .. PO-27)

Tracked in PROOF_OBLIGATION_LEDGER.md beside this file. FINAL STATE 2026-07-30: all 27
closed, retained-with-witness, or resolved-vacuous (PO-12: obstruction class is zero, so
the strong no-descent theorem is unnecessary — see REPORT_01).

## Remaining open walls (successor-campaign targets, each with cause)

| wall | cause |
|---|---|
| off-diagonal codimension >= 2 | determinant/inverse/cancellation control not established |
| r >= 3 channel transport faithfulness | kernel geometry unproved beyond n=4 grid identity |
| all-n carrier faithfulness | RoleChSpec rank recovery is dimension-3-specific |
| n > 4 pair-form generation | proved at 3 and 4 roles; general-n statement has a one-line combinatorial proof sketch in REPORT_01 but NO gate |
| characteristic p <= r | divided-power jets required |
| curved-ambient channelization | ambient curvature not bilinear in role data |
| global gluing / monodromy of the role cover | local theory only |

## Standing red lines

- No stage may call the chartwise metrics "the same tensor" until D_(rho,sigma) = 0 is proved
  (it is NOT — see REPORT_01; the red line is now permanent: the metric atlas language is mandatory).
- Finite-tower naturality is never cited as analytic convergence.
- Off-diagonal codimension >= 2 claims are out of scope for the first paper.
- Kerr-Newman identities never enter a universal proof.
