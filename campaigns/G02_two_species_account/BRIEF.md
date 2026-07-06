# G0.2 CAMPAIGN — the two-species single account

**Status:** OPEN · drafted 2026-07-06 · governed by the three standing rules.
No prior status is trusted; Stage 0 re-proves every input this campaign leans on.

## Campaign goal

Determine whether measurement defects (M) and representation defects (R) compose under
one account algebra — and derive that algebra's exact form — so Layer 0 can be built
whole, with `residue.py` implemented from a settled design rather than a guess.

## Target claim (the corrected conjecture)

```
TWO-SPECIES ACCOUNT (corrected 2026-07-06):
A finite chain of observation maps, each of species M (measurement: additive
defect on a free Q-module carrier) or species R (representation: a GROUP
ELEMENT acting on the representation space, its defect confined to a declared
invisible subspace), has a single derivable account (rho_M, rho_R) with:

 (i)   RECONSTRUCTION - truth exactly recoverable from (output, rho_M) on the
       covered class; typed refusal otherwise.
 (ii)  PURITY - every declared invariant depends only on the M-corrected
       output, never on rho_R.
 (iii) OWNED HOLONOMY - interleaving-dependence is itself exactly accounted:
       accounts of two interleavings differ by a computable holonomy term,
       identically zero on the certified commuting class.
```

Corrections carried from the source sweep: clause (iii) replaces the naive
"interleaving-independence" (route-difference is real and must be *owned*, not denied);
the R-slot carries the **parameter, never the displacement** — channel displacements
provably do not add (witness T6, re-certified in-repo: `dC(a1+a2)=(12/49,-23/49,11/49)
≠ dC(a1)+dC(a2)=(6/49,-11/49,5/49)`).

## Mathematical objects

Representation space `Sym_3(Q)` (design generic-n per freeze rule 3); gauge image
`Im(G_g)`, `G_g(a) = g a^T + a g^T` — the invisible subspace; carrier
`O_ij = H_ij - g_i H_jj/(2 g_j) - g_j H_ii/(2 g_i)`; M-species as translations by exact
residues; R-species as the translation group `(Q^3, +)` acting through `G_g`; the
account pair `(rho_M, rho_R)` and the splitting `Sym_3 = Im(G_g) ⊕ carrier`.

## Stage 0 — re-prove the inputs (re-verification rule)

| ID | Input | Status |
|---|---|---|
| RC-1 | Transport law: K_G invariance, ker-Sigma, four pinned gauge rows, O gauge-invariance + linearity (fixture tier), group-element witness | **CLEAN** — `verification/recert_transport_law.py`, 71/71, byte-stable ×2 (`d370daae`) |
| RC-2 | Normal form, symbolic tier: `H_perp` uniqueness, `O` = complete same-g invariant, `rank Im(G_g) = 3` on the regular locus — fresh symbolic derivation, not fixture-level | OWED |
| RC-3 | Account holonomy instance: commutator-as-account-gap re-certified from fresh code on a small fixture, before clause (iii) cites it | OWED |

**Gate: Stage A does not open until RC-2 and RC-3 are CLEAN.**

## Stage A — the exact-parameter theorem (provable core)

**T-A:** with `g` exact, defects decompose uniquely across `Im(G_g) ⊕ carrier`; the
account is `(O-visible component, gauge component)`; composition is additive; purity is
exact because `O` annihilates `Im(G_g)`; interleavings commute (translations).
Target: symbolic proof + certification battery. This is expected to close as a
direct-sum linear-algebra theorem — failing to close it is itself a major finding.

## Stage B — the defective base point (the derivation target)

When `g` carries an M-defect `E_g`, the invisible subspace `Im(G_{g+E})` rotates and
the splitting moves. Derive `O_{g+E}(H) − O_g(H)` in closed form (exact, first-order
and exact-total); classify the cross-term; prove or refute: **cross-terms land in M by
the reconstruction criterion and the R-ledger stays pure.** Membership is decided by
criterion (affects reconstruction ⟹ M; provably invisible to all invariants ⟹ R),
never by pedigree.

## Stage C — the adversarial battery (the gate itself)

- Interleavings: M·R·M vs R·M·M vs M·M·R, exact parameters — expect identical accounts.
- Defective `a`, defective `g` — the live cross-term cases from Stage B.
- **Multiplicative-escape (REINSTATED — the old non-test is void with its source):**
  relative-error cells; `μ·F` gauges read at F-level; test whether any covered-class
  map's defect escapes additive accounting.
- Quotient-carrier adversarial: attempt additive reconstruction of O-level data across
  representative changes — the carrier/⊕ question inherited from the old program,
  re-asked fresh here.
- Holonomy: a non-commuting pair with its exact holonomy term; zero on the commuting
  class.
- Mutants: at least one deliberately wrong account design — R-ledger carried as
  displacement (the T6 seed) — must FAIL the battery, proving the battery bites.

## Expected failure modes (how this campaign could fool us)

Fixture-level results mistaken for symbolic (RC-2 exists for this); a battery of only
commuting interleavings; cross-terms hidden by keystone symmetry (use generic jets with
no zero entries alongside the keystone); defining M by pedigree instead of criterion.

## Certification strategy

Exact ℚ end to end; fresh code only; every stage byte-stable ×2; PASS/FAIL verdict
lines; no float constructible on any verdict path.

## Kill conditions (armed)

- **K-1:** a covered-class M-defect fails additive composition → A-001 scope shrinks;
  the factoring question reopens hard.
- **K-2:** R-ledger contamination — an R-motion alters reconstruction *without*
  defective parameters → the species distinction collapses; A-002 DISPLACED. Design
  freeze rule 1 already prices this: no consuming code breaks.
- **K-3:** a cross-term escapes the exact carrier → the account is incomplete there;
  the enclosure-or-refusal boundary moves into Layer 0 and is documented, not hidden.

## Stop conditions

Stage A unprovable after honest attempts → close PARTIAL (certified-only); Layer 0
builds on the two-ledger form. Stage B cross-term closed form blocked → park with the
blocker named; battery runs with exact numeric cross-term tracking instead.

## Novelty payoff

If T-A and Stage B close: the account algebra — module with group action and owned
holonomy — becomes the engine's foundation statement, derived and certified in-repo;
and the carrier/⊕-universality question this program inherited gets its fresh answer
here rather than by citation.

## Output ledger

`verification/recert_*` (Stage 0) · `campaigns/G02_two_species_account/stage_a/`,
`stage_b/`, `battery/`, `VERDICTS.md` · on close: `residue.py` implemented from the
settled design; ADMISSIONS A-002 updated with the result either way.
