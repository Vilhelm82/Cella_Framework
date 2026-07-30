# OPEN OBLIGATIONS LEDGER

Live ledger. An obligation leaves this file only by being (a) discharged with a named gate
verifier, (b) converted into a typed stratum/hypothesis, or (c) explicitly moved out of scope
with its mathematical cause stated.

## GOVERNANCE CORRECTION (2026-07-30, post-release)

**Rule, effective immediately and for every successor campaign:** a manifest item named
by the plan that cannot be located in the repository is a **HALT condition at Stage 0**,
not a record-and-proceed event. The campaign owner produces or dispositions the item
before formal consolidation begins. The v1.0 release below proceeded past four missing
scripts (one from the REQUIRED 5.4 list, three conditional); the resulting scope
narrowing (all-n carrier demoted to frontier evidence; general-n pair-form generation
gated only at 3 and 4 roles) is a consequence of that process error, not a mathematical
necessity. Awaiting the owner-produced scripts; on arrival: hash into MANIFEST, run,
wire into run_all.py, and re-open the affected walls.

## Missing computational supplements (Stage 0 finding — CORRECTED by staleness audit, 2026-07-30)

**Stage 0's search was path-only and never looked inside archives. That was an audit error.**
The V4 retirement manifest (`V4PKG-0034__legacy_engine_source.json`) records the harness and
the Campaign H suite inside the git-tracked cold-recovery tarball; recovered and hash-verified:

| Item | Status | Detail |
|---|---|---|
| `dbp_curvature_reduction_harness.py` | **RECOVERED** | sha256 matches V4PKG-0034 byte-exact; stdlib-only; runs standalone; n=3/4/5 sweep PASSES (25/25 surfaces each) |
| `test_campaign_h_*.py` (9 scripts) + `run_campaign_h.py` | **RECOVERED** | full Campaign H executable suite from cold storage, packaged under 04_VERIFICATION_LEGACY/campaign_h/ |
| `char2_generalization.py` | MISSING under this name | no file by this name anywhere incl. cold storage; nearest survivor `test_campaign_h_char2_boundary.py` — owner to confirm substitution |
| `verify_campaignH_parity.py` | MISSING under this name | nearest survivors: Campaign H suite — owner to confirm |
| `verify_against_paper.py` | MISSING under this name | nearest survivor `test_campaign_h_retrodict_campaign_g.py` — owner to confirm |

Consequence update: the all-`n` role/channel invariant sweep now HAS executable support in
the package (the recovered harness passes at n=3,4,5). The all-n wall is partially reopened;
full reopening awaits owner confirmation of the Campaign H substitutions and any newer
owner-side maturation not present in this repository.

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
