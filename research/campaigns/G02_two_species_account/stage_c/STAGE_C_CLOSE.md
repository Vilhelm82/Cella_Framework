# STAGE C CLOSE — the adversarial battery

**Graded against** frozen `PREREG.md` (pin `003b91bd017e07b6`, commit `42ad4e6`,
pre-battery). **Battery:** `battery_stage_c.py`, 29/29 PASS, byte-stable ×2
(stdout sha16 `3008bef71ea74fb1`). **Kills:** K-C1..C4 armed, none fired.

**Defect in ink (caught pre-close, self-audit):** the first battery build carried a
vacuous verdict row — "R-ledger identical" asserted via a hardcoded True instead of
comparing recorded logs. Fixed to compare executed-operation logs; battery re-run in
full (28/28 → 29/29, new sha). The claim was true throughout; the *row* was not
evidence until the fix. Lesson consistent with the re-verification rule: a PASS line
must be an artifact comparison, never an assertion.

## Results (all staked pre-battery; all held)

1. **The asymmetry law [TC-P1].** Defective gauge *direction* stays R (state
   untouched, `rho_M` unchanged); defective *base* generates M (Stage B). The two
   parameter slots have opposite species — and the account distinguishes them by
   construction.
2. **Two-epoch chains [TC-P2].** Recalibration mid-stream is handled by per-epoch
   folding; within-epoch orderings commute; reconstruction exact.
3. **No multiplicative escape on the covered class [TC-P3].** Relative-error chains
   compose additively when residues are current-input-evaluated (the `δ₁δ₂`
   cross-term is captured automatically; the original-truth mutant misses exactly
   `T·δ₁δ₂`). Multiplicative structure at F-level (`μF`) lands additively at the jet
   account (`Hess(μF)|₀ = H + gaᵀ + agᵀ`, symbolic n = 3,4,5). Compositional-defect
   maps remain fenced OUT (T_token territory, declared not tested). **K-C1 silent.**
4. **The quotient re-ask, answered fresh [TC-P4].** At fixed regular g the carrier
   linearizes the state quotient, so state-level ⊕ IS additive — representative-
   dependence cannot occur. The genuine quotient wall is **base drift**, and it is
   crossed exactly by the Stage-B F1 correction (verified; the uncorrected
   base-mixing mutant fails). The inherited carrier/⊕ question now has an in-repo
   answer with a named boundary and a closed-form crossing.
5. **Owned holonomy at the mixed float/exact tier [TC-P5].** Round-then-gauge vs
   gauge-then-round: R-ledger order-invariant (recorded logs compared), per-slot
   `v₁ − v₂ == ρ₂ − ρ₁` exactly in ℚ, nonzero witness, dyadic control zero, all EFT
   identities verified in-run. Clause (iii) holds where non-commutation actually
   lives. **K-C3 silent.**
6. **The false-alarm/miss discriminating pair [TC-P6].** A design typing d-defects
   as damage false-alarms; one typing `G_e(a)` as representation misses real damage
   (`O_g` shift `(1/12, −5/3, −5/12)` on the witness). The two-species account
   passes both directions; any single-species design fails one. All four mutants
   caught. **K-C4 silent.**

## Campaign standing on this close

**The G0.2 conjecture is DEMONSTRATED on the covered class** — order-2 slot,
translation actions, rational data, fixed or drifting base with F1 — with clauses:
(i) reconstruction, (ii) purity, (iii) owned holonomy (commuting class = account
equality). Certified by Stages 0/A/B/C, every input re-proven in-repo, every stage
against a frozen prereg, byte-stable ×2 throughout, zero unresolved defects.

**`residue.py` implementation is UNBLOCKED** (per the frozen Stage-C gate): two
ledgers; R-slot = group parameter; cross-terms by F1/F3, folded into M by criterion;
holonomy owned, never denied. Code certification gates G0.1–G0.4 remain the
implementation's own bar.
