# FAITHFULNESS SEARCH REPORT — Campaign G (CL-G4)

## Outcome A — the theorem survives

**No exact-Q counterexample to T-G was found.** Across exhaustive small rational sweeps, targeted obstruction mutations, gauge-positive controls, and structured self-glue-derived families, RoleChSpec equality agreed exactly with vanishing Hessian gauge obstruction on every regular tested pair.

```
faithfulness_counterexamples (Type A: O != 0 but RoleChSpec equal): 0
gauge_invariance_counterexamples (Type B: O = 0 but RoleChSpec differ): 0
```

## The decisive test — bucket by RoleChSpec, check obstruction within each bucket

For a fixed regular `g`, every regular jet is assigned its recomputed RoleChSpec fingerprint and bucketed. Within each multi-element bucket, the obstruction rank relative to a base is computed. **A Type-A counterexample is a bucket with obstruction rank > 0** (two same-RoleChSpec jets that are not gauge-equivalent). The measured maximum obstruction rank inside *any* bucket was **0** everywhere — i.e. **every RoleChSpec bucket is exactly one same-gradient gauge orbit.**

| sweep | g | regular jets | multi-buckets | max obstruction rank in any bucket | Type-A |
|---|---|---|---|---|---|
| deep | (1,1,1), entries {-2..2} | 15 625 | 1 633 | 0 | 0 |
| broad | (1,1,1), {-1,0,1} | 729 | 171 | 0 | 0 |
| broad | (2,-1,1), {-1,0,1} | 729 | 177 | 0 | 0 |
| broad | (-1,2,1), {-1,0,1} | 729 | 177 | 0 | 0 |
| broad | (1,2,3) / (1,-2,3) / (2,3,5), {-1,0,1} | 729 each | 0 | 0 | 0 |

(The three gradients with 0 multi-buckets simply have a distinct RoleChSpec for every jet at that range — no same-RoleChSpec pair exists to test, so no counterexample is possible there.)

### Pre-check (recorded in PREREG, reproducible)

The same bucket-by-RoleChSpec test over the **three Campaign F gradients at {-2..2}** (46 875 jets, 8 584 multi-element RoleChSpec buckets) likewise found **0 Type-A failures** — a stronger, deeper coverage than the byte-stable runner's flagship deep sweep.

## Targeted adversarial constructions (CL-G4)

- **Obstruction mutations** — single off-diagonal bumps that create nonzero obstruction — always changed RoleChSpec (0 Type-A). Diagonal-only mutations likewise.
- **Gauge-positive controls** (CL-G3): `H2 = H + G_g(a)` (zero obstruction by construction) always preserved RoleChSpec — **0 Type-B** (no gauge-invariance failure; Outcome C did not occur).
- **Edge-topology + degenerate-channel families** (single edge, chain, triangle, star, B=0/A=0/C=0) across all 6 gradients: no counterexample.

`pairs_tested = 751`, `regular_pairs_tested = 19 999` (plus the pre-check's 46 875).

## Verdict

> Campaign G failed to find any exact-Q counterexample to the RoleChSpec Gauge-Obstruction Theorem. RoleChSpec equality agreed exactly with vanishing Hessian gauge obstruction on every regular tested pair.
>
> The local carrier arc now has a theorem target: **RoleChSpec is a faithful invariant of `Sym_3(Q)/Im(G_g)` on the regular active-role locus**, with the remaining work being proof of the converse outside the finite sweep.

The theorem remains **finite-tested, not globally proven.** No overclaim.
