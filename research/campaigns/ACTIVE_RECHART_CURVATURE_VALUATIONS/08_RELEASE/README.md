# ACTIVE_RECHART_CURVATURE_VALUATIONS — release

**Campaign outcome (one paragraph).** The active output-role atlas, its framed
curvature-channel accounts, and the local divisor curvature valuations are assembled
into one exact local calculus. The inverse-channel metric does NOT descend: strict
descent is falsified on exact witnesses, and the defect is an exact coboundary of the
canonical pair-form family `b_{lm}` that generates every presentation
(`g^(rho) = sum of the pair forms containing rho`, obstruction class zero). Pole-order
and weight-k principal-coefficient naturality are proved on the regular role cover.
The three output-role quadruples, the diagonal order-3/order-4 laws, the master
quadric, the corner calculus, and the Kerr-Newman 3/4/4 pattern are recovered as
strict corollaries, with the global Kerr-Newman curvature never assembled.

## One-command verification

```
python3 08_RELEASE/verification/run_all.py           # full battery
python3 08_RELEASE/verification/run_all.py --quick   # skip the two slow KN certificates
```

21 new falsification gates + 7 packaged legacy certificates; exact arithmetic only;
nonzero exit on any regression.

## Contents

| item | where |
|---|---|
| main manuscript source | `07_PAPER/active_rechart_curvature_valuations.tex` |
| complementary (agnostic) paper | `07_PAPER/COMPLEMENTARY_PAPER_GENERAL_ROLE_CALCULUS.md` |
| decisive descent report | `06_DERIVATIONS/metric_descent/REPORT_01_METRIC_DESCENT_OR_OBSTRUCTION.md` |
| stage derivations (paper-scoped + expanded) | `06_DERIVATIONS/*/DERIVATION_STAGE*.md` |
| proof-obligation ledger (PO-1..27, all closed/typed) | `00_CAMPAIGN/PROOF_OBLIGATION_LEDGER.md` |
| source absorption map (no theorem 'subsumed') | `00_CAMPAIGN/SOURCE_ABSORPTION_TABLE.md` |
| falsification programme results (9/9 searches run) | `00_CAMPAIGN/FALSIFICATION_PROGRAMME_RESULTS.md` |
| notation ledger (frozen conventions) | `00_CAMPAIGN/NOTATION_LEDGER.md` |
| corpus manifest with sha256 | `00_CAMPAIGN/MANIFEST.csv` |
| authority freeze | `00_CAMPAIGN/AUTHORITY_FREEZE.json` |

## Known limits (stated by mathematical cause)

Off-diagonal codimension >= 2 (determinant/inverse control absent); r >= 3 channel
faithfulness (kernel geometry unproved beyond the n=4 grid); all-n carrier
faithfulness (rank recovery dimension-specific); char p <= r (divided powers);
curved-ambient channelization (ambient term not bilinear in role data); global
gluing/monodromy (local theory only). Four plan-named all-n scaffold scripts are
absent from the repository and recorded MISSING (OPEN_OBLIGATIONS.md).

## Build note

This environment has no TeX toolchain; the manuscript ships as source only. It is
self-contained standard LaTeX (amsart-free, article class) and compiles with any
pdflatex >= TeXLive 2020.
