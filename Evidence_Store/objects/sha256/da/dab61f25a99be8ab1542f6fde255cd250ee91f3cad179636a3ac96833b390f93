# CCE-0 evaluator recertification report v1.1

**Date:** 2026-07-14  
**Verdict:** **PASS — schema-1.1 baseline recertified**

## Baseline transition event

The continuation handoff initially named the schema-1.0 evaluator byte lock:
1,570 DBP assertions, six schema-1.0 certificate digests, and bundle digest
`47b82d…c66e`. The live repository contains the later required edit
`2a2fdc75e0cc52aa5e8d6096873a4ae9992736aa`, which changed the transport
encoding to canonical hexadecimal numerators, advanced the certificate schema
to 1.1, and added G9 transport-safety gates.

The user authorized this shift as the new baseline and requested
recertification rather than rollback. No evaluator production source was
changed during recertification.

## Recertified result

- All 34 currently present `engine/tests/*.py` programs passed in clean
  processes.
- The live DBP gate passed **1,591 assertions**.
- Exact theorem/route verifiers passed **47 + 75 + 18** assertions.
- Two independent clean Python processes each generated and verified all six
  certificates.
- Every individual digest was identical across the two processes.
- Both canonical six-record bundles hashed to:

```text
aa97101da7ae03f127adf4dc7940128fbdc8ee425a21c2ef88b828c76afd2989
```

| Target | Bits | Recertified schema-1.1 digest |
|---|---:|---|
| primary | 192 | `a2ee898068f07889de338866a97d86d221758f40dbaf80cebeaa8b7ad83fadde` |
| dual_cpv | 192 | `b0af49eed283d049f16d8ca13d11532f59975ffc716405387ef6f55ce3104ed3` |
| primary | 256 | `60d584a33bbde31c4e2a0126f63165e34cccb75f4e991b99be004cf90a36fb0b` |
| dual_cpv | 256 | `484a56c34282b1a44deb9292040ffbed1325a6e8b8f0cb4ff0c9224852427c5f` |
| primary | 384 | `56b1e74f5a8a2b2a3e53153e2bfe1c83758483ee84e83337e7e6fa2db803b59d` |
| dual_cpv | 384 | `588be2cd98bb977a601d21f4d4a55401a8eda983ea5ed752ea59a1576c616c69` |

The canonicalization is UTF-8 JSON of the ordered six-record array with
sorted keys and compact separators.

## Compatibility meaning

Schema 1.0 remains a historical release receipt. For this continuation
campaign, "legacy byte-identical" now means byte-identical to the recertified
schema-1.1 lock above. The mathematical target set, exact dyadic enclosures,
native proof kernel, refusal semantics, and no-external-library boundary were
not broadened by this event.

## Worktree discipline

The pre-existing unrelated deletions and untracked DBP theorem sources were
preserved. No theorem paper and no `native_periods` production source was
edited.

Machine-readable evidence: `CCE_0_BASELINE_LOCK_v1.1.json`.
