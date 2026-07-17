# CCE hash-certificate cleanup report

Date: 2026-07-14

## Decision

The campaign's evidence standard is the mathematics, its exact proof data, and
direct replay of the asserted identities and inequalities.  Cryptographic
hashes are not a per-artifact admission requirement.

The sole retained hash baseline is
`01_cce0_recertification/CCE_0_BASELINE_LOCK_v1.1.json`.  Its purpose is limited
to comparing later Pathfinder behavior with the frozen starting baseline.

## Removed hash-only files

- `00_campaign_authority/CCE_4_8_RELEASE_MANIFEST_v1.0.json`
- `00_campaign_authority/CCE_5_8_RELEASE_BUNDLE_v1.0.json`
- `03_cce2_corridors/DBP_EXACT_CORRIDOR_ROUTE_DIGESTS_v1.0.json`
- `04_cce3_relative_classes/CCE_3_CERTIFICATE_BUNDLE_v1.0.json`
- `04_cce3_relative_classes/CCE_3_RELATIVE_CLASS_CERTIFICATE_SCHEMA_v1.0.json`
- `05_cce4_evaluator/CCE_4_BOUNDED_EVALUATION_CERTIFICATE_SCHEMA_v1.0.json`
- `05_cce4_evaluator/CCE_4_CERTIFICATE_BUNDLE_v1.0.json`
- `10_post8_universalization/POST_8_PROMOTED_CERTIFICATE_BUNDLE_v1.0.json`
- `shared_schemas/CCE_CERTIFICATE_SCHEMA_v2.0.json`
- `shared_schemas/CCE_CHECKPOINT_SCHEMA_v1.0.json`

No theorem, derivation, stage report, benchmark report, gap ledger, refusal
matrix, mathematical data witness, or handoff was deleted.

## Retained mathematical witnesses

Two artifacts retain `CERTIFICATE` in their historical filenames because they
contain substantive exact proof data rather than only file hashes:

- `03_cce2_corridors/DBP_EXACT_CORRIDOR_CLEARANCE_CERTIFICATES_v1.0.json`
  contains the exact tube bounds and divisor separations used by the corridor
  proof.
- `07_cce6_surface/CCE_6_COMPLETE_PACKAGE_v1.0/DBP_NATIVE_SURFACE_SWEEP_CLEARANCE_CERTIFICATE_v1.0.json`
  contains the surface identities, boundary-face reductions, and rational
  clearance transfer.

Their filenames are retained to avoid unnecessary retrieval churn.  They are
proof-witness datasets, not campaign admission tokens.

## Replay changes

The historical replay filenames were retained, but their behavior was changed
from digest/bundle comparison to direct mathematical checks:

- CCE-3 checks typed relative classes, quotient coordinates, CPV midpoint,
  compact ambiguity, boundary obstruction, and refusal behavior.
- CCE-4 checks exact dyadic enclosure ordering and achieved precision.
- CCE-5--8 checks the DBP K/E/Pi connection identity, Picard--Lefschetz and
  corridor groupoid algebra, CCE-6 proof-witness scope, the CCE-7 norm
  polynomial, and exact finite-role laws.
- Post-8 checks finite-tower naturality and the rational AC-fold root
  isolation directly.
- The supplied CCE-6 replay no longer requires the removed route-digest ledger;
  it reads the retained exact corridor-clearance witness and replays the
  polynomial and rational inequalities directly.

Historical reports may still mention the removed release bundles as records of
the workflow that produced them.  Those mentions are historical prose, not
live dependencies or current evidence requirements.

## Direct replay results

The cleanup was checked with the retained proof paths:

- CCE-2 exact routes: 12 assertions passed.
- CCE-2 exact corridor clearance: 17 assertions passed.
- CCE-2 lift and lateral class: 18 assertions passed.
- CCE-3 typed relative classes: 22 assertions passed.
- CCE-4 bounded evaluator: 6/6 exact dyadic enclosures passed at 192, 256,
  and 384 requested bits for both released targets.
- CCE-5 four-puncture local germs: 6 assertions passed.
- CCE-6 native surface clearance: 77 assertions passed after removing the
  route-digest dependency.
- CCE-6 whole-surface topology audit: 19 assertions passed.
- CCE-5--8 direct cross-stage mathematics: 14 assertions passed.
- Post-CCE-8 finite-tower and AC-fold mathematics: 6 assertions passed.

## Safety and event record

The hash-only deletion began while the campaign directory was still untracked,
so no pre-deletion Git snapshot existed.  Work stopped when this was noticed.
The user elected to continue.  Commit `d1499d7` then recorded the surviving
campaign reports, mathematical artifacts, organization, and direct replay
entry points before further changes.
