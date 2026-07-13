# STAGE A PREREG — the exact-parameter theorem (T-A)

**FROZEN before any battery code is written or run** (commit timestamp is the freeze).
Gates and kills below are law for this stage; the battery conforms to this text,
never the reverse.

## Setting (all objects per RC-2's certified notation)

Regular `g`, exact (no defect on `g` or on gauge parameters — that is Stage B).
Representation space `Sym_n`; M-map = translation by `E ∈ Sym_n` (measurement defect,
pedigree-recorded); R-map = translation by `G_g(a)`, `a ∈ Q^n` (representation change,
parameter-recorded). A chain is any finite interleaving. The pedigree account is
`(rho_M, rho_R) = (Σ E_k, Σ a_j)`.

## Predictions (all must pass; symbolic = identity in ALL indeterminates, per n ∈ {3,4,5})

- **TA-P1 (canonical form).** Every interleaving yields
  `H_final = H_0 + Σ E_k + G_g(Σ a_j)`. Symbolic: two contrasting orders of an
  E,a,E,a chain both equal the canonical form. Battery (n=3, exact ℚ): all 720
  orderings of a fixed 3-M + 3-R multiset agree.
- **TA-P2 (reconstruction).** `O(H_final − rho_M) == O(H_0)` — the M-corrected output
  carries the initial state exactly, whatever the R-ledger. Symbolic + battery.
- **TA-P3 (purity).** (a) Symbolic: `O(H_final − rho_M)` contains no `a`-symbols
  identically. (b) Exact-ℚ n=3: `K_G(M-corrected) == K_G(H_0)` on every chain, and
  `K_G(H_final) == K_G(H_0 + Σ E)` (R-motion never moves an invariant).
- **TA-P4 (pedigree vs splitting — the cross-species entanglement, exact tier).**
  For total displacement `D = Σ E + G_g(Σ a)`, the RC-2 splitting recovers
  `alpha(D) == Σ a + a*(Σ E)` and `Z(D) == (Σ E)_perp` symbolically, where
  `a*(E)_i = E_ii/(2 g_i)`. Corollary: the geometric splitting recovers the pedigree
  iff `a*(Σ E) = 0`; a generic witness must show them differing. **Consequence in
  ink: the account is pedigree-primary; the splitting is state-primary; they are
  exactly interconvertible by the stated identity — this is the Stage-B seed.**
- **TA-P5 (zero holonomy of the exact-parameter class).** All orderings yield
  identical `(H_final, rho_M, rho_R)` — accounts equal, not merely values. This
  certifies the exact-parameter chains as a commuting class in clause (iii)'s sense
  (account equality, per the RC-3 finding).
- **TA-P6 (mutants — battery must bite).**
  (i) *False-alarm mutant*: typing R as M. On a measurement-free chain (all `E = 0`,
  some `a ≠ 0`) it must report `rho_M ≠ 0` while the true-damage referee is 0 —
  the Layer-0 instance of the recalibration false positive.
  (ii) *Displacement-ledger mutant*: recording R as channel displacement must fail
  composition (`dC(a1+a2) ≠ dC(a1)+dC(a2)` re-witnessed inside this battery).
  (iii) *Dropped-residue mutant*: deleting one nonzero `E_k` from `rho_M` must break
  TA-P2.

## Grading gate

T-A → **DEMONSTRATED (symbolic tier, n = 3,4,5; general-n by the RC-2 index-local
argument, noted not certified)** iff TA-P1..P5 all PASS and all three mutants are
caught. Exact-ℚ throughout; two runs byte-identical; no float on any verdict path.

## Kills (armed)

- **K-A1** — any symbolic identity nonzero → T-A false as stated → STAGE HALT.
- **K-A2** — any ordering discrepancy in the battery → the exact-parameter commuting
  claim is false → clause (iii) rewrite before anything else runs.
- **K-A3** — any mutant undetected → battery vacuous → no close permitted.
