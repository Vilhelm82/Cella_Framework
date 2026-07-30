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

Tracked in PROOF_OBLIGATION_LEDGER.md beside this file; each PO closes only with a passing
gate verifier or a written proof in 06_DERIVATIONS.

## Standing red lines

- No stage may call the chartwise metrics "the same tensor" until D_(rho,sigma) = 0 is proved
  (it is NOT — see REPORT_01; the red line is now permanent: the metric atlas language is mandatory).
- Finite-tower naturality is never cited as analytic convergence.
- Off-diagonal codimension >= 2 claims are out of scope for the first paper.
- Kerr-Newman identities never enter a universal proof.
