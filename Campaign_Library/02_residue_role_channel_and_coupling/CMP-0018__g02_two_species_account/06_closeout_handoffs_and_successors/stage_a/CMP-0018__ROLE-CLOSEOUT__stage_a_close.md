# STAGE A CLOSE — the exact-parameter theorem (T-A)

**Graded against** the frozen `PREREG.md` (pin `ce44136c6418f48a`, frozen pre-battery
at commit `7dd3562`). **Battery:** `battery_stage_a.py`, 27/27 PASS, two runs
byte-identical (stdout sha16 `a90f4cbfe66ed79e`). **Kills:** K-A1/K-A2/K-A3 armed,
none fired. **Defects:** none.

## Result

**T-A holds.** With `g` exact, the two-species account exists and is canonical:

```
H_final = H_0 + rho_M + G_g(rho_R)         for EVERY interleaving      [TA-P1]
O(H_final - rho_M) = O(H_0)                reconstruction               [TA-P2]
M-corrected invariants free of rho_R       purity (O-level symbolic;
                                            K_G-level exact, n=3)       [TA-P3]
alpha(D) = rho_R + a*(rho_M)               pedigree <-> splitting,
Z(D)     = (rho_M)_perp                    exact interconversion        [TA-P4]
(H_final, rho_M, rho_R) order-independent  zero holonomy of the class   [TA-P5]
```

Tier: symbolic identities in all indeterminates at n = 3, 4, 5 (general-n by the
RC-2 index-local argument — noted, not certified); exact-ℚ battery at n = 3 including
all 720 interleavings of a 3-M + 3-R chain, values **and accounts** identical.

## The TA-P4 consequence (in ink — the Stage-B seed)

The account is **pedigree-primary**; the geometric splitting is **state-primary**;
they are exactly interconvertible by `alpha = rho_R + a*(rho_M)`. The splitting alone
cannot recover the pedigree whenever `diag(rho_M) ≠ 0` (witnessed:
`a*(SumE) = (−1/6, 1/2, 1)`), because an M-defect's diagonal leaks into the gauge
direction. **This leak is the exact-tier shadow of Stage B's cross-term**: when `g`
itself carries defect, the same leak happens through a *moving* splitting. Stage B's
question is whether it stays exactly attributable there too.

## Mutants (battery bites)

False-alarm mutant (R typed as M) reports damage on a damage-free chain — the
Layer-0 recalibration false positive, caught. Displacement-ledger mutant fails
composition, caught. Dropped-residue mutant breaks reconstruction, caught.

## Status moves

Conjecture clauses (i)/(ii): **DEMONSTRATED at the exact-parameter tier** (symbolic
per n + battery). Clause (iii): the exact-parameter class is **certified commuting**
(account equality, per the RC-3 refinement). The open front is exactly Stage B
(defective base point) and Stage C (adversarial battery incl. multiplicative-escape).

*Next: Stage B — derive `O_{g+E}(H) − O_g(H)` in closed form and grade the cross-term
attribution claim.*
