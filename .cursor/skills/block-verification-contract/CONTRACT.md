# Block-Verification Contract v1

**A per-paper, single-LLM job.** Attach this file to one mathematics paper. It tells the LLM how to turn that paper into a self-verifying artifact whose claims are established by code, not by prose.

---

## Principle

Prose has no authority. A displayed result is true only because code recomputes it or exhibits its witnessing argument. Where the code disagrees with the paper's prose, **the code wins and the prose is flagged stale.** The paper is testimony; the verification is the verdict.

## The unit

One `\[...\]` display block = one **module**. Inline `\(...\)` and prose are never modules.

## Per module, produce

- `tag` — the paper's label (e.g. `1.7`, `4.5`), or a minted sequential id if the block is unlabelled
- `section` — the heading it sits under
- `kind` — one of: `definition | formula | theorem | example | structural`
- `latex` — verbatim from the source block
- `depends_on` — the tags of the modules this one consumes as premises (`[]` for an axiom/base block)
- `run()` — a function that verifies the block and returns a status
- `status` — set **only** by `run()`, never by the prose

## The five statuses

- `PASS` — the block reduces to a computation; it was run and it matched. Arithmetic conviction.
- `STRUCTURAL` — the block asserts a structure (a field extension, a group being normal, a scheme irreducible); `run()` exhibits the witnessing argument in code rather than a number. Verified by exhibited reasoning, not arithmetic.
- `SKIP` — a verifier exists but a dependency is absent (e.g. sympy missing). An absence, not a verdict.
- `FAIL` — recomputed and did not match. Convicted false, loudly.
- `BLOCKED` — the module would run, but a premise in its `depends_on` failed. Unproven because upstream broke — not its own fault, but not established.

## Execution: dependency order

Modules run in **dependency order** — every premise before the conclusion that consumes it. Premises feed conclusions. This makes the paper's logical spine executable: the run-order *is* the proof structure.

Consequence — **propagation.** A `FAIL` doesn't fail one node. Every module downstream of it (transitively, through `depends_on`) becomes `BLOCKED`. One trap surfaces its full blast radius immediately: you see exactly which downstream results are now unproven-until-repaired. Fixing one premise can re-establish many conclusions.

## Deliverables

1. **The executable transcription** (`.py`) — modules with `run()`, executed in dependency order, printing a per-module report and a final tally (`PASS / STRUCTURAL / SKIP / BLOCKED / FAIL`).
2. **The JSON artifact** — one object per module, for downstream use:

```json
{
  "tag": "1.7",
  "section": "1",
  "kind": "theorem",
  "latex": "g(X_{\\mathbf a})=1+2^{k-2}(k-3)",
  "depends_on": ["3.2"],
  "status": "PASS",
  "detail": "genus (from Prop 3.3): {3: 1, 4: 5, 5: 17, 6: 49}",
  "figure": null
}
```

`detail` is the recomputed evidence line — the certificate. `figure` is the optional keystone-visual path (below), or null.

## Optional deliverable — keystone visuals

After verification, generate matplotlib figures for the paper's **keystone** results only — the payoff claims the paper exists to establish (a main theorem, a summary table, a landing example), not the machinery blocks.

Rule: a figure is driven by the **same verified numbers** the module's `run()` produced — never hand-typed. If `run()` yields `{3:1, 4:5, 5:17, 6:49}`, that dict is the plot's data. A figure whose data isn't sourced from a `PASS`/`STRUCTURAL` module does not ship. A visual is a certificate you can look at; it inherits the no-lying property because its data is the verified data.

## DAG mapping (downstream)

Each module becomes one node; each `depends_on` entry becomes one `depends_on` edge (the premise lists *are* the graph structure — nothing is inferred).

| module | DAG node |
|---|---|
| `kind` | node type (`definition`/`formula`/`theorem`/`example`/`object`) |
| `PASS` | `claim_status: machine-verified` |
| `STRUCTURAL` | `claim_status: demonstrated` |
| `FAIL` | `claim_status: refuted` |
| `BLOCKED` | `claim_status: open` (unproven pending upstream repair) |
| `SKIP` | `claim_status: open` |
| `latex` | node label / statement, verbatim |
| `detail` | certificate |
| `depends_on` | `depends_on` edges |

## Audit rule (the point)

Where a module's `run()` disagrees with the paper's prose, flag the prose stale — the code is the arbiter. **`STRUCTURAL` blocks are the priority hunting ground:** arithmetic blocks cannot lie, but a witnessed argument is only as sound as the reasoning it encodes. A trap found in one module propagates its doubt automatically to every module that depends on it — repair one premise, re-establish many conclusions.

---

*Reference conformance example: a 36-module transcription of "Generic Symmetric Monodromy of Weighted Multiquadratic Sums" runs clean in dependency order — 28 PASS, 8 STRUCTURAL, 0 SKIP, 0 BLOCKED, 0 FAIL — with each module declaring its premises and the conclusion (`13`) depending on `7.1` and `10.10`.*
