# Pathfinder benchmark fixture: complete signed-contact orbit

**Benchmark ID:** `m2-all-signed-contact-walls-v2-isolated`  
**Corpus workload:** `docs/m2_out_2026-07-10/stage2_contact_walls.m2`  
**Status:** cache-isolated correctness, certificate, marginal, and cold campaigns closed

## Deliverable

Compute the base-image ideal of every signed contact component

```text
C_epsilon = IX + <u, w1-epsilon1*N1, ..., w4-epsilon4*N4>
```

for all sixteen `epsilon in {+1,-1}^4`.

The exact result family is

```text
<4*M-epsilon1*N1-epsilon2*N2-epsilon3*N3-epsilon4*N4>.
```

This is the complete recorded stage-2 deliverable, not artificial repetition.

## Compared routes

Generic baseline:

```text
apply(epsilons, eps -> projectToBase(contactIdeal eps))
```

Pathfinder structural route:

```text
derive one triangular signed-contact presentation
enumerate the complete sign orbit
transport the linear wall across the orbit
emit the sixteen wall ideals
```

Independent external replay verifies, for every sign vector,

```text
contactIdeal(eps)
  = <u,
     w1-epsilon1*N1,
     w2-epsilon2*N2,
     w3-epsilon3*N3,
     w4-epsilon4*N4,
     4*M-sum(epsiloni*Ni)>.
```

The contraction to the base ring is therefore the displayed linear wall. Pathfinder emits this route and its obligations; M2 performs execution and replay.

## Final protocol

- 30 paired trials;
- one excluded fresh-process warm-up per route;
- each route executes in a separate fresh M2 process per pair;
- baseline-first and Pathfinder-first order alternates;
- no outlier removal;
- internal M2 elapsed time measures marginal route cost;
- external process wall time and peak RSS measure cold end-to-end cost;
- Pathfinder marginal and cold totals include Python lowering, core selection, and route lifting;
- exact outputs and the independent triangular certificate must close in every trial;
- paired median differences and ratios use 10,000-sample deterministic bootstrap intervals;
- the win count uses an exact two-sided sign test.

The preliminary shared-process campaign is not used for performance claims because order-stratified results revealed cross-route cache contamination.

## Final result

```text
marginal generic median:             0.03033675 s
marginal Pathfinder median:          0.01484355 s
marginal paired speedup median:      2.04594x
marginal speedup 95% interval:       [2.02743x, 2.07586x]
marginal wins:                       30/30

cold generic median:                 3.21710469 s
cold Pathfinder median:              3.18812597 s
cold paired speedup median:          1.00969x
cold speedup 95% interval:           [1.00694x, 1.01319x]
cold wins:                           29/30
```

Exact equivalence and external certificate replay closed in every trial. Full records:

- `benchmarks/results/CONTACT_ORBIT_ISOLATED_BENCHMARK.md`
- `benchmarks/results/CONTACT_ORBIT_ISOLATED_BENCHMARK.json`
