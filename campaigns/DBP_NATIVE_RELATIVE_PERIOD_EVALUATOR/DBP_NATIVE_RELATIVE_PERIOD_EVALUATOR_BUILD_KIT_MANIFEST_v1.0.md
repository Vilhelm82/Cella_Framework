# DBP Native Relative-Period Evaluator Build Kit

## Manifest, v1.0

**Date:** 2026-07-12  
**Purpose:** self-contained handoff material for implementing the two fixed DBP native
relative-period routes

---

## Start here

Give Codex the ZIP and this instruction:

> Open `CODEX_HANDOFF_BUILD_DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR.md`, follow it in full,
> preserve the existing repository, and do not stop at scaffolding or an unaccounted
> floating result.

---

## Required build documents

| File | Role |
|---|---|
| `CODEX_HANDOFF_BUILD_DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR.md` | finish-to-green implementation directive |
| `DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR_BUILD_SPEC_v1.0.md` | product, architecture, arithmetic, integration, and acceptance spec |
| `DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR_CONTRACTS_v1.0.json` | machine-readable routes, records, API, fixtures, and refusals |
| `DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR_GAP_LEDGER_v1.0.md` | closed/reusable/missing/open separation |
| `DBP_NATIVE_RELATIVE_PERIOD_ROUTE_THEOREM_v1.0.md` | exact compilation to smooth (g_+) and (g_-) kernels |

## Authoritative mathematical inputs

| File | Role |
|---|---|
| `DBP_LANDEN_TRACE_THEOREM_COMPLETE_v1.1.md` | corrected completed trace and splitting theorem |
| `DBP_Curvature_Constants_Corrected_Formulation.md` | corrected source constants, branch ledger, and independent pins |

## Exact verifiers

| File | Role |
|---|---|
| `verify_dbp_landen_trace_theorem.py` | base exact isogeny/trace/pole/non-torsion gates |
| `verify_dbp_landen_trace_theorem_v1_1.py` | exact anti-channel and logarithmic closure gates |
| `verify_dbp_native_relative_period_route.py` | exact finite-interval/pole-removal route gates |

## Existing structural kernel

| File | Role |
|---|---|
| `periods.py` | formal Legendre quartic, residue, branch-jump, and period-normal-form owner; not a numeric evaluator |

`periods.py` expects the target repository's `qsqrt.py` and package context. It is
included for integration, not as a standalone script.

---

## Verification commands

From the directory containing the three verifier scripts:

```bash
python verify_dbp_landen_trace_theorem.py
python verify_dbp_landen_trace_theorem_v1_1.py
python verify_dbp_native_relative_period_route.py
python -m json.tool DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR_CONTRACTS_v1.0.json
```

Expected pre-build result:

- the exact theorem verifiers pass;
- the contracts JSON parses;
- no native numerical bracket is expected yet.

The package is a complete build specification and mathematical route certificate. It
does not mislabel the still-unimplemented numerical executor as finished.

---

## Scope warning

The ZIP is deliberately narrow. It does not contain Pathfinder, generic route families,
an AGM evaluator, or a general (K/E/Π) implementation. The direct DBP route does not
need them.

The broader E-atom and calculus artifacts remain preserved in the source workspace but
are not required to build this evaluator.

