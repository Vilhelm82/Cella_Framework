# STAGE B — FOLD-MECHANISM PREDECL (under PREREG v2 + FOLD_PREDECL)
**Status: FROZEN at commit, before the verification script exists.** Date 2026-07-02.

## Derivation targets (symbolic, to be written in the report)
From the variational equations at phi = theta2 - pi = 0, release from rest:
```
drive:      A(theta1) = -g*sin(2*theta1)/(2 - cos^2(theta1))
extremum:   dA/dtheta1 = 0  <=>  cos(2*theta1) = 1/3          [exact]
amplitude:  A* = g/sqrt(2)
edge law:   u*(T) = g*T^2/(4*sqrt(2)) + O(T^4),  T = k*h
grid form:  4000*u*(k) -> (6.25/sqrt(2))*k^2 = 4.419417382...*k^2
angle:      theta1*(k->0) = -arccos(1/3)/2 = -0.615479708...
```

## Verification predictions (graded against the BANKED 40-digit fold data, no new runs)
- **M1:** even-series extrapolation of 4000*u*(k)/k^2 to k->0 (fit a + b*k^2 + c*k^4 on
  k=1..5 at dps 50) satisfies |a - 6.25/sqrt(2)| <= 3e-3 (frozen h^2 band: the discrete
  scheme's fixed-h offset is not removed by the T-series fit; estimate O(h^2 * a) ~ 2.8e-3).
- **M2:** same extrapolation for theta1*(k) satisfies |a_theta + arccos(1/3)/2| <= 1e-3.
- **M3 (graded, sharp):** the fitted b in M1 is NEGATIVE (coefficient drift direction).
- **M4 (exploratory):** residuals of the even-series fit at k=6,7 (out-of-fit) reported;
  no verdict promised on the discrete-h^2 admixture structure.

## Consequence if M1+M2 pass
The ladder-report statement "leading behavior ~ (9/2)k^2 [EMPIRICAL]" is SUPERSEDED by
the derived constant (registry-20 row to be filed); the tongue-edge law gets closed-form
leading data: {g/(4*sqrt(2)), -arccos(1/3)/2}. Tier: continuum leading order [PROVEN
once the derivation is written in full]; match to discrete data [CERTIFIED-numeric].

## Kill
M1 or M2 out of band => the derivation is missing a term or the mechanism is wrong;
HALT the mechanism claim, bank the miss, route to Will.
