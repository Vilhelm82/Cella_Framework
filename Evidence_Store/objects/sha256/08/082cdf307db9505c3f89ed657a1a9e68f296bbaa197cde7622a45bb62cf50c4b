# EXCEPTIONAL LOCUS REPORT — Campaign G (CL-G5)

Every sampled jet is typed before any comparison; singularities are **refused, never faked or crashed** (K-G4). No raw `ZeroDivisionError` occurs in any chart or verdict path.

## Typed strata

| status | condition | handling |
|---|---|---|
| `REGULAR` | `g_i ≠ 0` for all i; all three active output charts available | RoleChSpec recomputed and compared |
| `ROLE_CHART_UNAVAILABLE` | some `g_i = 0` (a chart denominator vanishes) | refused; comparison returns "not comparable" (None) |
| `SINGULAR_GRADIENT` | `g = 0` (no normal direction) | refused |
| `OUT_OF_SCOPE` | non-exact entry (float) or unsupported construction | refused |

## In this run

The theorem T-G is stated on the **regular** active-role locus (`g_1 g_2 g_3 ≠ 0`). All faithfulness sweeps and targeted constructions filter to `REGULAR` jets; non-regular jets are typed and skipped. The six attack gradients are all regular, so their full Hessian sweeps are regular. Among the self-glue families, jets at points with a vanishing required partial are typed `ROLE_CHART_UNAVAILABLE`/`SINGULAR_GRADIENT` and excluded from the faithfulness comparison (the regular ones are stressed; see `SELF_GLUE_STRESS_REPORT.md`).

No faithfulness failure or undefined-RoleChSpec event was observed *on* a typed exceptional stratum — i.e. there is no exceptional-locus counterexample (Outcome D did not occur). The exact-Q discipline (no float / no tolerance in any decision) means every refusal is a typed status, not an approximate judgement.
