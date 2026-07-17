# STAGE B — FOLD-EXTRACTION PREDECL (under PREREG v2 pin 96b3e09c)
**Status: FROZEN at commit, before any fold battery code exists.** Date 2026-07-02.

## Object
Fold point of rung k := solution (theta1*, u*) with u* > 0 of
```
s2^(k)(theta1, u) = 0        (principal-sheet flip condition, DF-7 chains)
d s2^(k) / d theta1 = 0      (double-root / edge condition)
```
The tongue edge. Mirror edge at -u* by the reflection symmetry (c,s)->(c,-s).

## Method (frozen)
mp workspace dps 80; principal chains under the DF-7 gates + motion schedule;
derivatives by central difference, step 1e-30 (accuracy floor ~1e-45); Newton on the
2x2 system; acceptance |s2| <= 1e-40 AND |ds2/dtheta1| <= 1e-30. Rungs k = 1..7.
Seeds: k<=5 from banked ladder edges; k=6,7 extrapolated (gates protect).

## Predictions
- **FP-1 (harness MUST, k=1..5):** floor(4000*u*(k)) == banked w(k)*4000 exactly
  (4, 17, 39, 70, 108). Failure = the fold solver and the ladder disagree = HALT.
- **FP-2 (harness MUST):** mirror solve returns -u*(k) to 1e-35. Failure = HALT.
- **FP-3 (graded):** r(k) := 4.5*k^2 - 4000*u*(k) is positive and strictly
  increasing for k >= 2.
- **FP-4 (exploratory, measure-don't-kill):** functional identification of r(k)
  against candidate forms {c*k^3, c*k^4, a*k^3 + b*k^4, trig-in-k}; recognition
  attempted, no verdict promised.

## Discipline
Byte-stable x2 on the box over the canonical block; exact values printed to 40 digits;
logs + script committed; FP-1/FP-2 failures HALT and route to Will.
