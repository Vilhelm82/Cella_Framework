# STAGE B — T^4 COEFFICIENT PREDECL (under MECH_PREDECL pin c413c3f8)
**Status: FROZEN at commit, before the CAS derivation script exists.** Date 2026-07-02.

## Targets (already banked, no free parameters)
From the frozen M1/M2 even-series fit on the 40-digit folds (mech_verify.py, sha 9d510157):
- **T1:** grid k^4 coefficient of 4000*u*(k):  b_banked = -0.0026780449
- **T2:** grid k^2 coefficient of theta1*(k) drift: b_theta (refit in-script from banked
  th*(k), k=1..5, printed before grading)

## Derivation route (CAS, mechanical)
Exact continuum EOM theta_dd = F(theta, theta_d) for the frozen system; from rest the
Taylor series is even: theta(t) = theta0 + (t^2/2) F + (t^4/24)[F_theta . F + F_vv[F,F]] + O(t^6).
Symbolic phi0; solve phi(T)=0 as series phi0 = p2 T^2 + p4 T^4; u0 = -tan(phi0/2);
extremize over a as series a* = a0 + d2 T^2. Outputs: G := coefficient of T^4 in u*(T),
d2 := T^2 drift of the extremal angle. Grid predictions: b_pred = G/640,
b_theta_pred = d2 * h^2 = d2/1600.

## Predictions (graded)
- **P-T4a:** |b_pred - b_banked| <= 0.15*|b_banked|   (band: k^6-truncation + h^2 admixture)
- **P-T4b:** |b_theta_pred - b_theta| <= 0.20*|b_theta|
- **Candidate on record, expected to die:** hand expansion gave G ~= -12.8
  (b ~= -0.0199), already in 7x tension with T1 — a term is missing from the hand
  computation; the CAS result supersedes it either way.

## Kill
P-T4a out of band => the T^4 mechanism as modeled is incomplete (missing physics, not
missing algebra); HALT the mechanism-extension claim, bank the miss, route to Will.
