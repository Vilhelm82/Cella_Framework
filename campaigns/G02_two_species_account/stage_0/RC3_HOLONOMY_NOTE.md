# RC-3 — route holonomy is the account gap (fresh instance)

**Certificate:** `verification/recert_holonomy.py` — 21/21, byte-stable ×2, stdout
sha16 `e4765c7ce1b89919`. Stdlib only; every EFT identity verified in ℚ in-run (H0,
18 ops), never assumed.

## The law re-certified (behind conjecture clause iii)

```
v_A - v_B  ==  rho_B - rho_A     exactly in Q
```

Two routes to the same true quantity (the mixed-difference commutator, Clairaut shape:
column-first vs row-first association over four observed nodes) may disagree at the
value level; the disagreement equals the difference of the routes' residue accounts,
exactly. Reconstruction holds per route (`v + rho == T` in ℚ); the true commutator
vanishes order-free.

## Three certified classes (one more than planned)

| fixture | holonomy | residues | reading |
|---|---|---|---|
| rounding/nonzero (pinned by deterministic search) | `−1/2⁵⁸` ≠ 0 | nonzero | the law has content — routes disagree, gap owned exactly |
| rounding/zero (the original draft fixture, kept) | 0 | **nonzero** | **zero holonomy ≠ flat** — routes can coincide bit-for-bit while every ledger is busy; the commuting class is strictly larger than the exact class |
| flat (integer lattice) | 0 | all zero | the trivially exact class |

The middle row is an RC-3 finding, not a design input: my first fixture landed there
by accident, failed the nonzero-witness check honestly, and was kept as its own class.
Clause (iii)'s "certified commuting class" must be defined by *account equality*, not
by exactness of the operations.

## Battery bites

Dropping the first nonzero op residue (deterministic choice) from its route's ledger
breaks reconstruction (`H6`); a zero-residue drop is correctly undetectable (dropping
nothing). Ledger tampering is caught by the exactness identity itself — the residue
polices its own account.

## Scope

Species M only (float rounding as the observation map; TwoSum-tracked subtractions);
one instance shape (mixed difference over 4 nodes, 3 ops per route). This certifies
the *phenomenon and its exact ownership law* for clause (iii)'s citation — the general
statement across map classes is exactly what Stage A/C must establish, not this note.
