# DBP Native Evaluator Release Report v1.0

**Date:** 2026-07-12  
**Verdict:** **PASS**  
**Machine record:** `DBP_NATIVE_EVALUATOR_RELEASE_REPORT_v1.0.json`

## 1. Release scope and change policy

This campaign validates the completed theorem-compiled DBP evaluator for `primary`
and `dual_cpv`. The first untouched precision matrix exposed a genuine release gate:
the frozen M1 schedule refused `dual_cpv` at 192 requested bits and both targets at
256 and 384 bits because its certified Cauchy remainder was too wide.

That failure authorized the minimum implementation change permitted by the campaign:
the frozen Pathfinder-selected panel partition, analytic radii, and algebraic kernel
forms remain fixed, while the recurrence order alone is raised deterministically from
the requested proof budget. The evaluator still re-proves every complex analytic disk
and Cauchy tail at runtime. Pathfinder remains absent from runtime and certificate
evidence.

A narrow structural certificate verifier was also added after the release campaign
showed that altered-pole and account-tampering checks were not independently callable.

## 2. Test campaign

- Initial clean-process repository suite: **37 passed, 0 failed**. The hostile
  Pathfinder benchmark passed unskipped in 95 seconds.
- Current-tree clean-process suite: **37 passed, 0 failed, 1 explicitly skipped**.
  The skip was `tests/gate_pathfinder_hostile_benchmark.py --skip-hostile`.
- DBP evaluator gate: **1,570 assertions passed**.
- Exact theorem/route verifiers: **47 + 75 + 18 assertions passed**.
- Compilation and scoped diff checks passed.

## 3. Certified dyadic brackets

Every bracket is `[lower_numerator, upper_numerator] / 2^denominator_exponent`.
The decimal column is a 60-place midpoint rendering for readability; the dyadic
endpoints and certified width are the verdict.

| Target | Requested | Certified width | Denominator | Decimal rendering |
|---|---:|---:|---:|---|
| primary | 192 | 229 bits | `2^256` | `-5.010490702660418769050021160526777648056994856721609896559050` |
| dual_cpv | 192 | 221 bits | `2^256` | `-3.988001085974558097719762257539087379694121855552360291347972` |
| primary | 256 | 295 bits | `2^320` | `-5.010490702660418769050021160526777648056994856721609896559050` |
| dual_cpv | 256 | 284 bits | `2^320` | `-3.988001085974558097719762257539087379694121855552360291347972` |
| primary | 384 | 426 bits | `2^448` | `-5.010490702660418769050021160526777648056994856721609896559050` |
| dual_cpv | 384 | 413 bits | `2^448` | `-3.988001085974558097719762257539087379694121855552360291347972` |

### Exact endpoints

**primary, 192 bits requested**

```text
lower = -580175186565198337643655937351881090836109965678107591285512890460960600493765 / 2^256
upper = -580175186565198337643655937351881090836109965678107591285512890460960514360070 / 2^256
```

**dual_cpv, 192 bits requested**

```text
lower = -461778977625679928055388951143059726456678375383303538322060207148797939478002 / 2^256
upper = -461778977625679928055388951143059726456678375383303538322060207148765110519824 / 2^256
```

**primary, 256 bits requested**

```text
lower = -10702343184484905904188000918232641530277808112391469252702947140094325597353535493293398288655109 / 2^320
upper = -10702343184484905904188000918232641530277808112391469252702947140094325597353535493293398270283446 / 2^320
```

**dual_cpv, 256 bits requested**

```text
lower = -8518318618880166845259941586258388551891836188461077743947870136405873573877307577321461131615983 / 2^320
upper = -8518318618880166845259941586258388551891836188461077743947870136405873573877307577321421074707401 / 2^320
```

**primary, 384 bits requested**

```text
lower = -3641818670416697760141711023079651972971004599583972701666492964847486286829582215705726989030275925081157669648985364229908747874628008 / 2^448
upper = -3641818670416697760141711023079651972971004599583972701666492964847486286829582215705726989030275925081157669648985364229908747872421667 / 2^448
```

**dual_cpv, 384 bits requested**

```text
lower = -2898633621819242704742764989653366270406639065874213081057645375975366262218938204938199989033773834608357799655682780499464804116267971 / 2^448
upper = -2898633621819242704742764989653366270406639065874213081057645375975366262218938204938199989033773834608357799655682780499464771327722263 / 2^448
```

## 4. Fixture digits

For all six brackets, both endpoints independently share every digit of the declared
fixture prefixes and both endpoints round identically at the fixture precision.

There is one important semantics note:

- `dual_cpv` is both a matching prefix and the correctly rounded 54-place decimal.
- The stored primary literal ending in `...72160` is correctly labeled by the contract
  as a **decimal prefix**. Conventional rounding to 50 places produces `...72161`.
  Therefore both endpoints share the stored primary prefix, but the stored literal is
  not itself the correctly rounded 50-place decimal.

## 5. Certificate replay and refusals

Two separate clean Python processes generated and structurally verified all six
certificates. Their canonical JSON bundles were byte-identical:

```text
SHA-256 = 47b82d536982fb27ff730da6311f0340e9da81ae04e3a91c3c78348d6c8cc66e
```

The refusal campaign passed **6/6**:

| Case | Result |
|---|---|
| wrong sheet | `unsupported_relative_path:path_gate` |
| wrong path | `unsupported_relative_path:path_gate` |
| missing CPV | `unsupported_relative_path:path_gate` |
| altered pole | `route_identity_failed:source_ledger` |
| account tampering | `account_not_closed:account_ledger` |
| untampered certificate | accepted |

## 6. Production dependency audit

The static production closure contains 14 reachable modules. It has zero imports or
call sites for mpmath, SymPy, SciPy, FLINT/Arb, Sage, AGM, Carlson forms, `ellipk`,
`ellipe`, `ellippi`, or another elliptic library. Only Python standard-library roots
are reachable. Arb appears solely in the external referee described below.

## 7. Benchmarks

Cold native measurements used one fresh process per target and precision. Marginal
medians are seven repeats after populating only that request's exact-integral cache.
Certificate verification medians are 100 structural verification calls. Timings are
performance evidence, not proof.

| Target | Bits | Cold native | Marginal median | Certificate verification median |
|---|---:|---:|---:|---:|
| primary | 192 | 10.020778 s | 0.001370 s | 0.000133 s |
| dual_cpv | 192 | 16.389693 s | 0.001038 s | 0.000132 s |
| primary | 256 | 18.637676 s | 0.001856 s | 0.000137 s |
| dual_cpv | 256 | 32.325893 s | 0.001492 s | 0.000133 s |
| primary | 384 | 48.895571 s | 0.002860 s | 0.000133 s |
| dual_cpv | 384 | 94.923091 s | 0.002253 s | 0.000135 s |

Pathfinder compile-time scout timing is reported separately:

- Fresh-process median over 7 trials: **0.057597 s**.
- Fresh-process range: **0.056479–0.059162 s**.
- Planning-only median over 100 warm calls: **0.0000474 s**.
- Pathfinder is not imported by native execution and contributes no certificate evidence.

## 8. External 384-bit Arb/FLINT referee

The referee used `python-flint 0.9.0`, `acb.integral`, a 512-bit context, and a
430-bit requested integration tolerance. This route is outside the certifying path.

| Target | Arb ball | Native bracket contains ball | Time |
|---|---|---:|---:|
| primary | `[-5.0104907026604187690500211605267776480569948567216098965590501968372045802270598548322437836294365391803591947103981700130038421793287266365613 +/- 5.72e-143]` | yes | 0.008867 s |
| dual_cpv | `[-3.9880010859745580977197622575390873796941218555523602913479728203743820443016200843749981845367805718259055996136404699995249347698381945162970 +/- 2.98e-143]` | yes | 0.015020 s |

Both complex integration results had imaginary balls containing zero. Both native
384-bit dyadic brackets contain the complete Arb referee ball, not merely its midpoint.

## 9. Remaining refusal boundary

- Only the two theorem-compiled DBP routes and their four target views are admitted.
- The dual execution kernel remains smooth and pole-free; no numerical CPV crossing exists.
- Pathfinder remains a compile-time scout only.
- The separate Legendre K/E realization does not route or alter DBP evaluation.

