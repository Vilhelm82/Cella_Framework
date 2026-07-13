# SELF-GLUE STRESS REPORT — Campaign G (CL-G6)

Structured adversarial families from the separable surface `F = D^m + D^k S + P^p − 3`, sampled at exact rational points. **No monodromy results are claimed here** — these surfaces are used only as structured adversarial *input* for the local RoleChSpec faithfulness test.

## Local 2-jet (exact)

```
g = ∇F = (m D^{m-1} + k D^{k-1} S,  D^k,  p P^{p-1})
H = Hess F, nonzero entries:
    H_DD = m(m-1) D^{m-2} + k(k-1) D^{k-2} S,  H_DS = k D^{k-1},  H_PP = p(p-1) P^{p-2}.
```

Families `(m,k,p) ∈ {(3,1,2),(4,1,2),(6,2,2),(6,3,2),(3,1,3)}` × rational points `(D,S,P) ∈ {(1,1,1),(2,1,1),(1,2,3),(2,-1,2),(3,1,2)}` — 25 structured jets. Example `(3,1,2)` at `(1,1,1)`: `g = (4,1,2)`, `H = [[6,1,0],[1,0,0],[0,0,2]]` (hand-pinned, verified).

## Result — PASS

```
self_glue_structured_stage: PASS
```

On every **regular** self-glue jet:
- gauge-positive controls (`H2 = H + G_g(a)`) preserved RoleChSpec — 0 Type-B;
- obstruction mutations (single off-diagonal bumps creating nonzero obstruction) changed RoleChSpec — 0 Type-A.

No self-glue-derived jet produced a counterexample to T-G. Non-regular self-glue jets (where a chart denominator vanishes) are typed and refused, not crashed (see `EXCEPTIONAL_LOCUS_REPORT.md`).
