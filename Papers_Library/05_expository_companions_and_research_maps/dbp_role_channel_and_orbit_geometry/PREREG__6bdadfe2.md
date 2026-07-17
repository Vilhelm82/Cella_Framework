# PREREG — Campaign G: RoleChSpec Gauge-Obstruction Faithfulness

**Status:** pre-registration, recorded **before** any generated report.
**Tier:** eval-tier only. No substrate promotion. Does not change Campaign A/D/E/F artifacts. Campaign type: **adversarial theorem test**.
**Discipline:** exact `fractions.Fraction`; stdlib only; no float / no NumPy / no tolerance in any verdict path; canonical `{"num": n, "den": d}`; deterministic, two-run byte-identical.

## Theorem under attack (T-G)

For `g ∈ Q^3` with `g1·g2·g3 ≠ 0` and `H1, H2 ∈ Sym_3(Q)`, with the same-gradient gauge map `G_g(a) = g a^T + a g^T` and the obstruction `O_g(ΔH) = (O_12, O_13, O_23)`,

```
O_ij(ΔH; g) = ΔH_ij − g_i·ΔH_jj/(2 g_j) − g_j·ΔH_ii/(2 g_i)
O_g(ΔH) = 0  ⟺  ΔH ∈ Im(G_g)        (exact gauge-image lemma)
```

> **T-G:** on the regular n=3 active-role locus, `RoleChSpec_g(H1) = RoleChSpec_g(H2)  ⟺  O_g(H2 − H1) = 0`.

## The two attack directions

- **Type A — faithfulness failure:** regular `g, H1, H2` with `O_g(H2−H1) ≠ 0` **but** `RoleChSpec_g(H1) = RoleChSpec_g(H2)`. Would show RoleChSpec is *coarser* than the obstruction quotient `Sym_3(Q)/Im(G_g)` (Campaign F finite-atlas exact but not global).
- **Type B — gauge-invariance failure:** regular `g, H1, H2` with `O_g(H2−H1) = 0` **but** `RoleChSpec_g(H1) ≠ RoleChSpec_g(H2)`. Would contradict Campaign D's proven gauge-invariance — a serious defect (Outcome C; stop).

## Pre-check result (recorded; the registered expectation)

Bucketing all jets by RoleChSpec and checking the obstruction rank **within each bucket** (a stronger test than Campaign F's reduced-tower grouping), over the 3 frozen gradients × entries {-2..2} (46,875 jets, 8,584 multi-element RoleChSpec buckets): **0 Type-A failures, 0 Type-B failures.** Every RoleChSpec bucket is exactly one gauge orbit. Expected campaign outcome: **A — theorem survives the adversarial sweep, not globally proven.** The campaign attacks harder (6 gradients, targeted constructions, self-glue families); if any counterexample appears, it becomes the result.

## Non-tautology (CL-G7)

The verdict path must not use Campaign D survival labels, the Campaign F obstruction verdict, or cached RoleChSpec records as a shortcut; RoleChSpec is **recomputed** from `(g,H)`. No floats/tolerances for exact decisions. Singularities are typed (REGULAR / ROLE_CHART_UNAVAILABLE / SINGULAR_GRADIENT / CHANNEL_DEGENERATE / OUT_OF_SCOPE) — never a raw `ZeroDivisionError`.

## Claims

- **CL-G1** gauge-obstruction formula: `ker(O_g) = Im(G_g)` by exact construction (gauge diffs → O=0; mutations → O≠0).
- **CL-G2** Campaign F retrodiction: obstruction_rank 0→0/1917, 1→2549/0, 2→832/0.
- **CL-G3** gauge-invariance stress: `O=0 ⟹ RoleChSpec equal` (any counterexample is a kill — K-G2).
- **CL-G4** faithfulness attack: search for `O≠0 ∧ RoleChSpec equal`; report exact counterexamples or the searched count.
- **CL-G5** exceptional-locus typing: all refusals typed, no raw exceptions.
- **CL-G6** self-glue structured stress: exact local jets from `F = D^m + D^k S + P^p − 3`.
- **CL-G7** non-tautology: no forbidden labels/shortcuts/floats.
- **CL-G8** mutation controls: 10 mutants caught.

## Search families (§7)

6 gradients {(1,1,1),(1,2,3),(2,-1,1),(1,-2,3),(2,3,5),(-1,2,1)}; bucket-by-RoleChSpec sweep; gauge-positive controls; obstruction mutations; diagonal-only mutations; single-edge / chain / triangle / star / complete coupling families; degenerate-channel targets; self-glue `(m,k,p)` ∈ {(3,1,2),(4,1,2),(6,2,2),(6,3,2),(3,1,3)}.

## Kill conditions
K-G1 obstruction formula broken · K-G2 gauge invariance broken · K-G3 faithfulness broken · K-G4 raw singular crash · K-G5 float leakage · K-G6 cached-label leakage. A counterexample is **preserved and made the result**, not hidden.

## Non-goals
n ≥ 4; substrate promotion; monodromy claims from the self-glue families (used only as structured adversarial input); a global proof of the converse (the remaining work after a successful sweep).
