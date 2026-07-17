# CCE-1 compatibility facade and certificate-envelope report v1.0

**Date:** 2026-07-14  
**Worktree base:** `50683b971399236abe413cafcf2c56c5b1b9228c` on `main`, with preserved pre-existing unrelated changes  
**Verdict:** **PASS within PF-0's enumerated six-request scope**

## Implemented scope

`continue_certified` accepts immutable typed requests, invokes the confirmed
live `cella.pathfinder.plan_request` route constructor, separates plan validity
from budget adequacy, delegates execution to the untouched schema-1.1 DBP
native evaluator, and emits linked route/evaluation certificates. Verification
reconstructs the live plan, replays the nested legacy certificate, checks all
manifest and digest links, and checks achieved width.

The imported Pathfinder guarantee is exactly:

```text
six requests = {primary, dual_cpv} x {192, 256, 384}
AdmittedRequest -> ValidPlan | UnsupportedRequest
```

Its PF-0 verdict is `CONFIRMED_WITH_SCOPE`. Other Pathfinder providers,
unreleased precisions, and arbitrary continuation paths are excluded. No
external referee output is certificate evidence.

## Changed files

- `engine/src/cella/continuation/`: immutable model, adapter protocol,
  DBP delegate, public facade, canonicalization, checkpoints, certificates,
  live-Pathfinder bridge, and verifier;
- `engine/src/cella/pathfinder/recognize/dbp_native.py` and provider registry;
- `engine/tests/gate_continuation_pf0.py` and
  `engine/tests/gate_continuation_cce1.py`;
- `engine/benchmarks/benchmark_continuation_cce1.py` and
  `engine/benchmarks/replay_continuation_cce1.py`;
- campaign schemas and reports in this directory.

No `cella.native_periods` production file and no theorem paper was modified.
Pre-existing unrelated worktree changes were preserved.

## Deterministic certificate inventory

Two independent clean processes produced the same canonical six-envelope
bundle digest:

```text
c04ba9200de47bd5fc68e84e9c932ab63e5ea9eb41981b6bba3144272b7f84a3
```

| Target | Bits | Plan digest | Route digest | Evaluation digest |
|---|---:|---|---|---|
| primary | 192 | `a6d8e2cca14f78f94367f5c42cace779fa4139780d1160f5ac8ad37999f299a9` | `ac158caa9e3d31614f28275dc168f732abba2829d5af3409fce7c8c626d61616` | `2b068ba7d73cc3d0ef588ff293c74d6d59232f9bc7015f2244291f767f096732` |
| dual_cpv | 192 | `4cb53a0b4820d152186e3df388ed21d4262b1870e3115b39e862de774470fac8` | `1145130915228647b881cd46b0cc38937d761424e6cc5f6ea3175b94933973db` | `f8b49fe5e10e06d55d9f7b3c9011f12345324d42b02d7c7464a6e68d000b547b` |
| primary | 256 | `9e4b4fe6b81e94f611ee88c63b0366290d94f1c444d2c118981d7886af20cd84` | `e019fa2246e13f432a01433fd9b2577683909f656a727bfb051fee5d39ba43f9` | `74ee5fdf9b73c0cd09c9c7820adf3bfd182de9b68fce2a4b2722ec7ae0465c0a` |
| dual_cpv | 256 | `ada6e19757b07a2e06b06dc5dcb71cf8cd35bfd6cd52e3f82dfb64bfe1c7669a` | `7c6372a2fd7b4e432e44ae8b17a0c04ae0cc6301e08bd9e3573cf404c0765e1c` | `7f006c0d39e36338e78fc7865308383e79b85f93cf736f749d20f4be725a9b3e` |
| primary | 384 | `5e7ae86cc389c908ae69bd0df70fc987a8c1ac35b1d8e0f0f325afa4fb30f45a` | `8eff4aef5e94b39eec1e67a4c711add53a465620f4d167ef1a8ef7f6ea3963d0` | `95f92bacaea0c138ea0f14617d27e589bde0c7878f52a74ede8310a76dd10001` |
| dual_cpv | 384 | `8b662b4e984102e61c4e971ec456d851f469ca3296b0090a64a2cb5bf0f3da35` | `51502d5701725a9c613838f28c3f9298740143d034f9e22ebcba769e50fd897f` | `73d7d18a57e2ce2edce2e7a7adc4d68875b27d19f02f0b94114ebe911c908365` |

The nested legacy digests are exactly the six schema-1.1 digests in
`CCE_0_BASELINE_LOCK_v1.1.json`; its bundle digest remains
`aa97101da7ae03f127adf4dc7940128fbdc8ee425a21c2ef88b828c76afd2989`.

## Commands and gates

- all 36 `engine/tests/*.py` programs: passed, zero failed;
- DBP native evaluator: 1,591 assertions passed;
- PF-0 focused gate: 58 assertions, repeated in two clean processes;
- CCE-1 focused gate: 24 assertions;
- PF-0 and CCE-1 gates under `python -S`: 58 + 24 passed;
- two clean six-envelope generations: byte-identical;
- `compileall`, JSON parsing, stale-file exclusion grep, and source-level
  dependency audit: passed.

## Mathematical and coefficient scope

CCE-1 wraps fixed terminal evaluation routes; it does not yet transport an
arbitrary exact path or a relative-homology class. The primary target is typed
over `Z`; the released dual CPV target retains `Z[1/2,i]` in its request
manifest. That is compatibility typing, not a new derivation of CPV or a claim
that quotient data determines an absolute scalar.

Route composition and reversal deliberately return typed refusals. The first
unclosed proof obligation is the exact `ell_up`/`ell_down` route and clearance
lemma recorded by `CCE_2_ROUTE_SPECIFICATION_GAP_v1.0`.
