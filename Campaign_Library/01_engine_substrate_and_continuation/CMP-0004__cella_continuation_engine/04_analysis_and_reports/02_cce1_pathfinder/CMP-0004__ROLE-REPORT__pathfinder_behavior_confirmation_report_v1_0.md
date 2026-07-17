# Pathfinder behavior confirmation report v1.0

**Date:** 2026-07-14  
**Verdict:** **CONFIRMED_WITH_SCOPE**

## Confirmed contract

The live typed Pathfinder core at `engine/src/cella/pathfinder/`, using only
the `dbp_native_released_evaluation` provider, satisfies:

```text
Pathfinder:
  AdmittedRequest -> ValidPlan | UnsupportedRequest

AdmittedRequest =
  exact schema-1.1 DBP native adapter identity
  x {primary, dual_cpv}
  x {192, 256, 384 requested bits}
  x exact locked family, path, selected-state and coefficient-ring manifests
```

Every admitted request produces a deterministic typed `ComputationalRoute`,
preserved verbatim as canonical JSON inside `PathfinderPlan`. Every tested
mutation outside that domain produces a typed recognition refusal and then
`UnsupportedRequest`.

The plan guarantees exact route and manifest identity, locked schedule source,
an admitted 32-panel partition, deterministic integer/rational recurrence
parameters, canonical source/route/plan digests, and explicit executor proof
obligations. The executor independently proves domain separation, analytic
disk radii, arithmetic-account closure, and the Cauchy remainder.

## Live implementation audit

The current Pathfinder package was inventoried: immutable request, route,
contract and evidence records; exact frozen-value boundary; normalized problem
lowering; native scouts; provider registry; admissibility helpers; candidate
assembly; deterministic comparison; canonical serialization; callers and
gates. After adding the DBP provider, 40 providers are registered.

CCE enables only `recognize/dbp_native.py`. It has a finite exact input domain,
no scouts, no executor invocation during planning, and two output kinds: an
admitted `RouteCandidate` or explicit `RecognitionRefusal`.

No stale or historical Pathfinder script is used by this confirmation, the CCE
runtime, or certificate evidence.

## Validity versus adequacy

Validity is enforced by typed provider guards and route constructors. Adequacy
is a separate predicate over the valid plan and `ProofBudget`. All six
recertified executions close. A deliberately smaller budget still produces the
same valid plan and is classified as inadequate rather than invalid.

## Determinism and trust boundary

- Requests, candidates, routes, and plans are frozen dataclasses.
- Binary floats are rejected at the Pathfinder IR boundary and absent from the
  DBP provider.
- The packaged schedule digest is checked before admission.
- The exact live Pathfinder source closure digest is recorded in every plan.
- The canonical `ComputationalRoute` and its digest are recorded.
- Panel order explicitly covers `0..31`.
- Randomness, clocks, locale, environment variables, network, solvers, mutable
  caches, and unordered iteration do not affect semantic output.
- The finite admitted domain is exhaustively enumerated.

Two clean process replays pass the 58-assertion PF-0 gate. Locked plan digests:

| Target | Bits | Plan digest |
|---|---:|---|
| primary | 192 | `a6d8e2cca14f78f94367f5c42cace779fa4139780d1160f5ac8ad37999f299a9` |
| dual_cpv | 192 | `4cb53a0b4820d152186e3df388ed21d4262b1870e3115b39e862de774470fac8` |
| primary | 256 | `9e4b4fe6b81e94f611ee88c63b0366290d94f1c444d2c118981d7886af20cd84` |
| dual_cpv | 256 | `ada6e19757b07a2e06b06dc5dcb71cf8cd35bfd6cd52e3f82dfb64bfe1c7669a` |
| primary | 384 | `5e7ae86cc389c908ae69bd0df70fc987a8c1ac35b1d8e0f0f325afa4fb30f45a` |
| dual_cpv | 384 | `8b662b4e984102e61c4e971ec456d851f469ca3296b0090a64a2cb5bf0f3da35` |

The combined Pathfinder source closure digest is
`0fd5afbb455fc5b142165a0f30692b54786f2f391fbc973cb1ec2cab3139bee5`.

## Imported scope

CCE imports only this six-request provider guarantee. No guarantee is imported
for arbitrary precision, arbitrary paths, or any other Pathfinder provider.

## Deliverables

- `PATHFINDER_BEHAVIOR_CONFIRMATION_REPORT_v1.0.json`
- `PATHFINDER_ADMITTED_DOMAIN_SCHEMA_v1.0.json`
- `PATHFINDER_STATE_TRANSITION_INVENTORY_v1.0.json`
- `PATHFINDER_VALIDITY_ADEQUACY_MATRIX_v1.0.json`
- `engine/tests/gate_continuation_pf0.py`
