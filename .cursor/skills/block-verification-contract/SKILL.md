---
name: block-verification-contract
description: Convert a mathematics paper (markdown) into a self-verifying proof-DAG per the Block-Verification Contract v1 -- one displayed-math block per module, run() recomputes or witnesses each claim, modules execute in dependency order with FAIL->BLOCKED propagation, emitting an executable .py plus a JSON artifact for Cella-DAG ingestion. Use when asked to verify, transcribe, modularize, "turn into modules", DAG-ify, or apply the block-verification contract to a math paper, or to turn its equations/theorems/examples into executable modules.
---

# Block-Verification Contract — Executable Transcription

Turn one mathematics paper into a self-verifying artifact: **prose has no authority; code is the arbiter.** Where `run()` disagrees with the paper's prose, the code wins and the prose is flagged stale.

[CONTRACT.md](CONTRACT.md) is the authoritative spec — read it. This file is the operational workflow.

## Workflow

```
- [ ] 1. Read the entire paper.
- [ ] 2. Extract modules: each \[...\] display block = one module (inline \(...\) and prose are NEVER modules).
- [ ] 3. For each module record tag, section, kind, latex (verbatim), depends_on.
- [ ] 4. Wire the dependency DAG from the paper's logical spine (premise -> conclusion).
- [ ] 5. Copy scripts/harness.py next to the paper as `harness.py`.
- [ ] 6. Write `<paper>_modules.py`: one @module per block; author run() per the status rules.
- [ ] 7. Run it; iterate until no FAIL/BLOCKED — OR a FAIL is a genuine stale-prose finding (flag it, do not fake a pass).
- [ ] 8. Confirm the JSON artifact was written.
- [ ] 9. Keystone visuals: MANDATORY interactive selection (see below).
- [ ] 10. Report the conformance tally and any stale-prose flags.
```

## Module kinds and how to author run()

`run(ctx, deps)` returns a `Result(status, value, detail)`. `value` is what downstream modules consume; `detail` is the human-readable certificate.

- **PASS** (`"OK"`): the block reduces to a computation. Recompute it and assert it equals the paper's stated value. Arithmetic conviction.
- **STRUCTURAL** (`"STRUCTURAL"`): the block asserts a *structure* (field degree, group normal/order, scheme irreducible, dimension, rank). Exhibit the witnessing argument in code (e.g. count an orbit, compute a group order, an F₂ rank) — not a bare restatement.
- **SKIP** (`"SKIP"`): a verifier exists but a library is missing (e.g. `sympy`). An absence, not a verdict. SKIP premises do NOT block dependents.
- **FAIL** (`"FAIL"`): recomputed and mismatched. Return it loudly — do not soften. This is a stale-prose finding.
- **BLOCKED**: never returned by you — the harness assigns it automatically when a `depends_on` premise did not establish.

## Dependency order and value hand-offs (the point)

Declare `deps=[...]` with the premise tags. The harness topologically sorts, runs premises first, and passes their `Result`s in as `deps`.

A conclusion must **consume** its premises' verified values, not silently recompute them:

```python
@module("4.5", "4", "Cor 4.4: ramification degree", "theorem",
        r"\deg R=2g-2+2d", deps=["3.2", "4.2", "4.4"])
def m_4_5(ctx, deps):
    g = deps["3.2"].value          # genus proven by Prop 3.3
    d = deps["4.2"].value          # degree proven by Prop 4.3
    degR = {k: 2 * g[k] - 2 + 2 * d[k] for k in g}
    ok = all(degR[k] == 2 ** (k - 1) * (k - 3) + 2 * d[k] for k in g)
    return Result("OK" if ok else "FAIL", degR, f"deg R from g[3.2],d[4.2]: {degR}")
```

A `FAIL` propagates: every transitive dependent becomes `BLOCKED`, so one trap shows its full blast radius. Fixing one premise can re-establish many conclusions.

## Keystone visuals — present options, the USER decides

**Do not auto-generate figures.** After a clean run:

1. Identify **keystone** candidates only — the payoff claims the paper exists to establish (a main theorem, a summary table, a landing example). Never machinery/lemma blocks.
2. Present them to the user with the **AskQuestion tool** as a multi-select list (`allow_multiple: true`), always including a **"None (skip visuals)"** option. Recommend the single strongest keystone first.
3. Build **only** the figures the user selects.

Each figure's data MUST come from `results[tag].value` (a `PASS`/`STRUCTURAL` module) — never hand-typed. Register with `@figure(keystone_tag, title, source_tags, filename)` and re-run with `--figures`; the harness enforces that every `source_tag` is verified before it will render, and records the path in that module's `figure` field.

```python
@figure(keystone_tag="9.table", title="Invariants k=3..6",
        source_tags=["9.1", "1.7", "1.9"], filename="invariants_table.png")
def fig_table(results, path):
    import matplotlib.pyplot as plt
    delta = results["9.1"].value; g = results["1.7"].value; degR = results["1.9"].value
    ks = sorted(delta)
    # ... plot strictly from delta/g/degR ...
    plt.savefig(path, dpi=150, bbox_inches="tight"); plt.close()
```

AskQuestion template:

```
title: "Keystone visuals"
question (allow_multiple: true):
  "Which keystone results should ship as verified figures?"
  options:
    - "<strongest keystone> (Recommended)"
    - "<second keystone>"
    - "<third keystone>"
    - "None (skip visuals)"
```

## Deliverables

1. `<paper>_modules.py` — executable transcription (imports `harness.py`).
2. `<paper>_verification.json` — one object per module: `tag, section, kind, latex, depends_on, status, claim_status, detail, figure`. Written automatically.
3. Selected keystone figures (only those the user chose), paths recorded in the JSON.

## Conformance reference

A clean run of the reference paper lives at
`Papers_Library/01_completed_papers/galois_horizon_and_kummer_covers/monodromy_modules.py`
— 36 modules: 28 PASS / 8 STRUCTURAL / 0 SKIP / 0 BLOCKED / 0 FAIL, conclusion `13` depending on `7.1` and `10.10`.
