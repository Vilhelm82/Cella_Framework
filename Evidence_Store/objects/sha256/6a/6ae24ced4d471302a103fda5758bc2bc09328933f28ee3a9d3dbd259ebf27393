# Pre-registration — DBP 2-Primary Involution Campaign

**Bench names:** PAIR-SPLIT · Sym/Wedge Boundary · The Alternating Half Hunt
**Task brief:** `Build_Docs/Agent_tasks/DBP_2-Primary_Involution_Campaign.md`
**Workstream:** `evals/dbp_involution/` · `results/dbp_involution/`

## Thesis under test

The repeated appearances of the prime `2` in DBP role-coupling are all manifestations of one
linear-algebraic fact, `std ⊗ std = Sym²(std) ⊕ ∧²(std)` over rings where `2` is invertible:

1. local DBP coupling lives in the symmetric half `Sym²(std)`;
2. the recurring prime-2 defects come from the failure of the `Sym²/∧²` eigenspace split when `2` is not invertible;
3. the missing alternating half `∧²(std)` may live in the global transport / monodromy side;
4. Campaign H's `O`-parity, the char-2 phantom, the `V₄` quotient at n=4, the `32 = 2⁵` constant, and even/odd field parity should be projections of this split.

## Discipline (committed before running)

- **Exact arithmetic only.** `sympy.Rational` / integer matrices / explicit mod-p Gaussian
  elimination / integer Smith normal form. No float reaches any graded verdict.
- **Independent referee.** `rep_utils.py` re-implements S_n representation theory from scratch
  (Murnaghan–Nakayama on beta-sets, character inner products, integral `std_n` matrices). It
  shares no code with the DBP engine. The engine (`dbp_carrier.py`) computes characters as
  traces of explicit matrices; a claim passes only when engine and referee agree.
- **No tautology.** Every decomposition is checked by character/rank/projector evidence; the
  referee is unit-tested against known S_3/S_4 character tables and character orthogonality.
- **Independence from the parallel campaign.** A separate campaign
  (`codex_task_dbp_prime2_structure.md`) attacks the same questions. No banked values, gate
  numbers, conventions, or results are lifted from it; every number here is recomputed by this
  workstream's own machinery. Overlapping outcomes are independent corroboration only.
- **Campaign H is reproduced, not cited.** The n=3 O-space, O-parity, and char-2 phantom (CL-H10)
  are recomputed / cross-checked against the Campaign H engine in `src/` (sanctioned by the brief).
- **Verdict vocabulary:** PROVEN / COMPUTER_VERIFIED / REFUTED / BRANCHED / OPEN.

## Pre-registered predictions and gates

| Stage | Prediction | STOP gate |
|---|---|---|
| **0** P0.1 | `rank L = C(n,2)`, `χ_Im(L) = C(fix,2)+#2cycles`, n=3..8 | yes |
| **0** P0.2 | `Im(L)=triv⊕std⊕S^(n-2,2)`, `dim loss = n(n-3)/2` | — |
| **0** P0.3 | n=4 kernel `V₄` margin 0; n≥5 kernel trivial margin `2(n-3)`, n=4..12 | yes |
| **A** P-A1/2 | `std⊗std=Sym²⊕∧²`; `Sym²=triv⊕std⊕S^(n-2,2)`, `∧²=S^(n-2,1,1)` | — |
| **A** P-A3 | `P_-(Im L)=0`, `P_+(Im L)=Im L` (else BRANCH) | branch |
| **B** | reproduce r=1 odd / r=2 even; classify `tau_O` ∈ {−I, +I, other} | — |
| **C** P-C1/2/3 | torsion exactly 2-primary; vanishes over `ℤ[1/2]`; locate the seam | branch on odd torsion |
| **D** P-D1/2/3 | ker(channel mod p)=gauge; GF(2) gauge rank n−1, kernel ⟨g⟩, `ggᵀ∉`im; ker(mod 2)=gauge⊕⟨ggᵀ⟩ | — |
| **E** | rebuild monodromy groups; hunt `∧²(std)`; classify found/absent/no-map | — |

Outcomes of stages B and E are **not** assumed; both possible results are findings. A failed
prediction is not a failed campaign if the failure is exact, recorded, and interpreted.

## Reproduce

```
cd evals/dbp_involution
python3 rep_utils.py            # referee self-test
python3 run_all.py             # full campaign -> results/dbp_involution/{records.jsonl, prediction_verdicts.json}
```
