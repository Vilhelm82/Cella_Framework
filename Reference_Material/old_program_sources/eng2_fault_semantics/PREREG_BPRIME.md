# STAGE B′ — DIRECTION-LAW PROBE (FROZEN pre-battery, S-2026-07-05b; Will: "accept, go B-prime")
Succeeds Stage B (K-B1 accepted). Object: the g-family of quadratic forms
Q_ν(g) = D_W⁻¹ Q_raw(g) D_W⁻¹, W = W-prod, per PREREG_v2 DF-B1/B2 (imported
unchanged; W-sum retired with Stage B — its shadow was structureless).

**Named form (prior-wins audit line):** solving the observed direction in
the association-scheme basis gives
```
Q_univ(n) = (n−2)·I − A_1     A_1 = Johnson scheme J(n,2) adjacency
                               (pairs sharing exactly one vertex)
n=3:  A_1 = J−I  ⟹  Q_univ = 2I−J   = I.3a's form verbatim
```
spectrum (−(n−2), 2, n) on (triv, std, shape). Johnson-scheme spectra are
KNOWN (Delsarte/Bannai–Ito classical). NOVELTY CANDIDATE: the coupling
shape-operator e_2 form's equivariant shadow landing on exactly this
operator with ONE g-borne scalar — the general-n succession of I.3a.

## Predictions (FROZEN; graded mechanically; clauses embedded)
| id | statement | class | prediction |
|---|---|---|---|
| PBp.0 | regression: recomputed Q_ν and shadow coefficients at the six Stage-B (n,g) fixtures match the pinned Stage-B run-1 records exactly; projector gates n=4,5,6 | sanity | MUST HOLD (else K-Bp0 pipeline defect, no verdicts) |
| PBp.1 | SYMBOLIC in g at n=4: (n−2)·c_std(g) + 2·c_triv(g) ≡ 0 AND (n−2)·c_shape(g) + n·c_triv(g) ≡ 0 as exact rational-function identities (c_X = tr(Q_ν P_X)/tr(P_X)) — equivalently shadow(Q_ν) = s(g)·((n−2)I − A_1) | discriminating | HOLDS — moderate-high (2 exact g-fixtures per n already agree); FAIL = K-Bp1 |
| PBp.1b | same two identities SYMBOLIC at n=5 | discriminating | HOLDS; envelope-exceed = datum-not-fail (wall-scout convention) |
| PBp.2 | direction (−(n−2) : 2 : n) at NINE fresh g-fixtures (3 per n ∈ {4,5,6}), exact ℚ | discriminating | HOLDS all 9; any FAIL = K-Bp1 |
| PBp.3 | scalar s(g) := −c_triv(g)/(n−2): (a) staked: s is a symmetric rational function of g, homogeneous of degree 6−2n; (b) measurement: record s(g) in factored form at n=4 (and n=5 if PBp.1b lands) | mixed | (a) moderate; (b) record-only |
| PBp.4 | residual R(g) = Q_ν − s·Q_univ: record rank(R) and isotypic block support (P_X R P_Y norms²) at all 15 fixtures | measurement | record-only — feeds the covariant-completion design; NO structure staked |

## Kill conditions (armed)
- **K-Bp0:** PBp.0 fails ⟹ pipeline defect; HALT, no verdicts.
- **K-Bp1:** PBp.1 fails symbolically OR any PBp.2 fresh fixture fails ⟹
  direction law dies; HALT, route to Will (the 2-fixture agreement was
  coincidence — record and close honestly).
- **K-Bp3:** PBp.3(a) fails ⟹ refute the sub-claim row only, continue
  (record actual homogeneity/symmetry behaviour).
- Envelope 1200 s / 8192 MB per run; exceed = datum. Byte-stable ×2.

## Pins (Rule 1.9) — freeze_pins_bprime.sha256
This file; fixtures_bprime.json; PREREG_v2.md (imported definitions);
fixtures_stageB.json (regression g-vectors — pin-completeness fix added
pre-battery, S-2026-07-05b, before any run; noted in report);
records/stageB_records_run1.jsonl (regression source, = `ca2741a0…`);
evals/dbp_involution/rep_utils.py. Battery refuses on sha mismatch
(REFUSE_MISMATCH) or clause drift (CLAUSE_DRIFT). role=probe + ledger;
symbolic identities via sympy cancel == 0 (referee: numeric spot-evaluation
of the same identities at the fresh fixtures — independent path, must agree).

## Status moves (frozen)
PBp.1 + PBp.2 PASS ⟹ direction law → **CERTIFIED (n=4 symbolic; n=5
symbolic or datum; n=6 multi-g numeric)**; CL-F5 row gains: "succeeded by
the Johnson-operator shadow law [CERTIFIED]; full bridge = shadow law +
covariant completion, completion OPEN". PBp.3(a) PASS adds the scalar's
homogeneity/symmetry as certified side-lemma. General-n symbolic proof =
separate derivation stage (no battery); CL-ENG2 stays gated.

frozen: true · author Claude-session · substrate [BOX] · S-2026-07-05b
