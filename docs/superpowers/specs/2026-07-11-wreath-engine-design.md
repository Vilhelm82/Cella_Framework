# Wreath Engine — Design

**Date:** 2026-07-11
**Status:** Approved design, pre-implementation
**Mathematical basis:** `docs/galois_horizon_cover_v1_0_publication_package/` —
in particular `KUMMER_MODULE_WREATH_LIFT_THEOREM_2026-07-10.md` (the engine
theorem) and `MACAULAY2_REALIZATION_POSET_WORKFLOW_2026-07-10.md` (the
realization workflow), with `certificates/m2_out_2026-07-10/` as the reference
run the engine must be able to reproduce.

## 1. Purpose

Turn the proved theorem engine into an executable pipeline. The engine accepts:

1. a separable base cover `K/F` of degree `d` with claimed monodromy `G`
   (supplied, per the all-k interface — never recomputed);
2. `s` radical channels `r_1, …, r_s ∈ K*/K*²`;
3. candidate divisors with claimed valuation-parity rows.

It outputs: the Kummer rank `ρ = rank W`, `[H:K] = 2^ρ`, the candidate wreath
closure `C_2^s ≀ G` (under maximal rank), the colored inertia table, and
generated-and-run Macaulay2 verification tasks for the realization question.
On rank failure it returns the kernel — the square-class relation module — and
the offending divisors. Every mathematical claim is backed by a standalone,
hand-rerunnable Macaulay2 script and its verbatim output.

Primary consumer: Claude, via MCP. Secondary consumer: a human, via a small CLI.

## 2. Architecture

```
Claude ⇄ MCP (stdio) ⇄ Python server (FastMCP)
                          ├─ spec validation (JSON Schema)
                          ├─ F2 linear algebra (rank, kernel, B ⊗ I_d)   [pure Python]
                          ├─ template renderer → .m2 scripts
                          ├─ batch runner: M2 --script → parsed result block
                          ├─ persistent M2 session    [exploratory tools only]
                          └─ job manager (async long decompositions)
                                    ↓
                     m2/WreathEngine.m2  (mathematical authority)
                                    ↓
                     runs/<run-id>/  (spec, scripts, raw outputs, result.json, report.md)
```

**Division of labor.** Python does bookkeeping: F2 ranks and kernels, wreath
order arithmetic, inertia-table assembly, report formatting, job control.
Macaulay2 does every mathematical claim about the variety: primality of
divisors, unramifiedness, radicand regularity, valuation parities, and the
realization poset. A result is `"certified"` only if every mathematical gate
ran in M2 and its script+output pair is on disk.

**Execution model (hybrid).** Certified calls are stateless batch runs: render
a self-contained `.m2` script from a template, run `M2 --script`, parse the
result block. The exploratory `suggest_parity_rows` tool may use a persistent
M2 session for responsiveness; nothing from that session ever certifies
anything. Long computations (decompositions, full poset runs) go through
async job tools.

**Known M2 gotcha:** `M2 --script` cannot read process-substitution paths
(`/proc/<pid>/fd/...`); scripts are always real files under `runs/<run-id>/`.

## 3. Directory layout

```
tools/wreath_engine/
  pyproject.toml                 # uv project; dependency: mcp
  wreath_engine/
    server.py                    # FastMCP entry point; tool definitions
    spec.py                      # JSON Schema + validation → ProblemSpec
    f2.py                        # GF(2) matrices: rank, kernel, inverse, kron
    m2gen.py                     # template rendering of .m2 scripts
    m2run.py                     # batch runner + result-block parser
    m2session.py                 # persistent session (exploratory only)
    jobs.py                      # job registry: start/status/result/cancel
    inertia.py                   # colored inertia table assembly
    report.py                    # markdown certificate report
    cli.py                       # `wreath-engine run|verify <spec.json>`
  m2/
    WreathEngine.m2              # M2-side library
    templates/
      verify_divisor.m2          # per-divisor checklist gates
      poset_stage*.m2            # generalized stage1..6 pipeline
      decompose.m2               # minimalPrimes / primaryDecomposition
      slice.m2                   # exact rational slice computations
      explore_parity.m2          # exploratory valuation probe
  examples/
    horizon_static.json          # s=2, d=5 static crown (regression case)
    horizon_rotating.json        # s=3, d=5 rotating cover (acceptance case)
  runs/                          # gitignored working area
  tests/
  README.md
```

## 4. Problem specification (JSON)

One declarative document per application. The Python layer validates it
against a JSON Schema and synthesizes the M2 model (what
`horizon_wreath_inertia_model.m2` hand-codes today).

```jsonc
{
  "name": "horizon_rotating",
  "ring": {
    "variables": ["M","N1","N2","N3","N4","J","u","w1","w2","w3","w4"],
    "weights":   [1,1,1,1,1,2,2,1,1,1,1],
    "order": "GRevLex",
    "coefficients": "QQ"
  },
  "base_cover": {
    "incidence_gens": ["w1^2-u-N1^2", "w2^2-u-N2^2", "w3^2-u-N3^2",
                        "w4^2-u-N4^2", "w1+w2+w3+w4-4*M"],
    "sheet_vars": ["u","w1","w2","w3","w4"],
    "degree": 5,
    "expected_codim": 5,
    "ramification_det_identity": "8*(w1*w2*w3+w1*w2*w4+w1*w3*w4+w2*w3*w4)",
    "group": { "name": "S5", "order": 120,
               "claimed_by": "all-k symmetric monodromy theorem" }
  },
  "channels": [
    { "name": "u",     "radicand": "u" },
    { "name": "gamma", "radicand": "2*(w1*w2*w3*w4+u*(w1*w2+w1*w3+w1*w4+w2*w3+w2*w4+w3*w4)+u^2+N1*N2*N3*N4)" },
    { "name": "delta", "radicand": "gamma-4*N1*N2*N3*N4-16*J^2" }
  ],
  "divisors": [
    { "name": "even_contact",
      "gens": ["u","w1-N1","w2-N2","w3-N3","w4-N4"],
      "claimed_parity_row": [1,0,0],
      "type": "contact",
      "expected_base_image": "4*M-N1-N2-N3-N4" },
    { "name": "odd_contact",
      "gens": ["u","w1+N1","w2-N2","w3-N3","w4-N4"],
      "claimed_parity_row": [1,1,0],
      "type": "contact",
      "expected_base_image": "4*M+N1-N2-N3-N4" },
    { "name": "delta_private",
      "gens": ["gamma-4*N1*N2*N3*N4-16*J^2"],
      "claimed_parity_row": [0,0,1],
      "type": "private",
      "note": "the difference divisor IZ = IX + (delta), certified prime in the 2026-07-10 run; delta has odd (order-1) valuation, u and gamma even. Private primes must additionally be distinct across conjugate sheets (theorem report §10); the engine verifies primality and sheet separation, it does not find the divisor" }
  ],
  "generic_denominator": "2*M*N1*N2*N3*N4*(N1^2-N2^2)*(N1^2-N3^2)*(N1^2-N4^2)*(N2^2-N3^2)*(N2^2-N4^2)*(N3^2-N4^2)",
  "slices": [
    { "name": "R9", "assignments": { "N1": 4, "N2": 8, "N3": 12, "N4": 20 } }
  ],
  "base_cycle_data": []          // optional: cycle types for base-ramified divisors
}
```

Notes:

- Channel radicands may reference earlier channel names (`delta` uses `gamma`);
  the renderer expands them in order.
- `group` is accepted as claimed. The engine records `claimed_by` in every
  certificate; it never recomputes monodromy. Consistency checks only
  (`degree` matches sheet count, `order` divides `d!`).
- Polynomials are strings parsed by M2 (`value`) inside the synthesized ring;
  the Python layer checks only that they mention declared variables.
- `divisors[*].claimed_parity_row` has length `s`; exactly the theorem §5
  orbit form. The distinguished sheet is implicit in the divisor's generators
  (contact divisors pin sheets by sign pattern); `private` divisors must be
  prime upstairs and the engine verifies sheet-separation.

## 5. MCP tool surface

Registered names and semantics (envelope in §6):

| tool | semantics | M2 | status ceiling |
|---|---|---|---|
| `analyze_kummer_module(spec)` | validate spec; assemble sheet-level matrix `B` from claimed rows; rank/kernel of `B`; orbit matrix `B ⊗ I_d` rank `= d·rank B` | no | `claimed` |
| `verify_valuation_matrix(spec)` | per divisor, run the checklist gates (§7); on all-pass, promote the parity matrix to certified | batch | `certified` / `refuted` |
| `compute_wreath_lift(spec)` | if certified `B` invertible: `ρ = sd`, `[H:K] = 2^sd`, `Gal ≅ C_2^s ≀ G`, order `2^(sd)·|G|`. If deficient: kernel basis = square-class relation module, offending divisors, rank-drop report | consumes prior state | inherits |
| `classify_inertia(spec)` | colored inertia table: per certified divisor, the Kummer sign vector (parity row on distinguished sheet, theorem §7) × base cycle data (from `base_cycle_data`, else trivial) | assembly | inherits |
| `realize_branch_poset(spec, stages?)` | generate + run the generalized stage pipeline (§8); return realized poset table | batch/async | `certified` |
| `suggest_parity_rows(spec, candidate_divisors)` | exploratory valuation parities via bounded symbolic-power probe; explicitly non-certifying | session | `exploratory` |
| `inspect_certificate(run_id?)` | list runs, or return one run's artifact index + result.json | no | — |
| `start_realization(spec, stages?)` | async variant of `realize_branch_poset`; returns `job_id` | spawn | — |
| `get_job_status(job_id)` / `get_job_result(job_id)` / `cancel_job(job_id)` | job control; cancel kills the M2 subprocess | — | — |

Tools are independently callable; `compute_wreath_lift` and `classify_inertia`
look up the latest verification run for the spec (by content hash) and refuse
to report `certified` without one, returning `claimed` with a warning instead.

## 6. Result envelope

Every tool returns schema-validated `structuredContent`:

```json
{
  "status": "certified | claimed | refuted | exploratory | error",
  "run_id": "2026-07-11T.._horizon_rotating",
  "base_group": "S_5",
  "degree": 5,
  "channels": 3,
  "kummer_rank": 15,
  "maximal_rank": true,
  "index_H_over_K": "2^15",
  "closure_group": "C_2^3 wr S_5",
  "closure_order": 3932160,
  "valuation_matrix": [[1,0,0],[1,1,0],[0,0,1]],
  "orbit_matrix_rank": 15,
  "kernel_basis": [],
  "inertia_table": [ { "divisor": "even_contact", "sign_vector": [1,0,0],
                        "base_cycles": "trivial", "order": 2 } ],
  "gates": [ { "divisor": "even_contact", "gate": "prime_upstairs", "pass": true } ],
  "certificate_files": ["runs/.../verify_even_contact.m2",
                         "runs/.../verify_even_contact.out.txt"],
  "warnings": []
}
```

Fields absent from a given tool's output are omitted, not nulled. `refuted`
names the failed gate and divisor; for rank failure, `kernel_basis` is the
explicit relation module over F2 (the theorem §8 falsifier).

## 7. Verification gates (the certified core)

For each divisor `D` with claimed parity row `b`, the rendered
`verify_divisor.m2` checks, in order, printing one verdict per gate:

1. **prime_upstairs** — `D + IX` has exactly one minimal prime (and equals its
   radical along the generic open, after saturation by the spec's
   `generic_denominator` when `type` warrants it — contact divisors saturate,
   boundary studies must not; the template takes this from `type`).
2. **not_in_ramification** — the generic point of `D` is unramified in `E/F`:
   `IR ⊄ √(D + IX)` where `IR = IX + (ram det)`; concretely
   `isSubset(IR, primeOf(D))` is false.
3. **radicand_regular** — each `r_α` is neither identically zero nor infinite
   on `D` beyond its claimed order (polynomial radicands: check `r_α` not in
   the prime unless the claimed parity/valuation says so).
4. **on_sheet_parity** — for the distinguished sheet, `v_D(r_α) mod 2` equals
   `b_α`. Parity via bounded symbolic-power search (SymbolicPowers package if
   available, else saturation-based fallback): find max `n ≤ N_max` (default 8)
   with `r_α ∈ P^{(n)}`. Hitting the bound → `error`, never a silent answer.
5. **off_sheet_even** — conjugate radicands on other sheets have even
   (typically zero) valuation: membership checks `r_{α,j} ∉ P` for `j ≠ i_q`,
   with the same symbolic-power escalation if membership holds.
6. **expected_base_image** (optional, contact type) — `eliminate(D + IX,
   sheet_vars)` equals the spec's `expected_base_image` ideal.

All gates pass for all divisors → the parity matrix is certified; Theorem 5.1
plus invertible `B` then licenses `compute_wreath_lift` to promote
`C_2^s ≀ G` with status `certified`.

## 8. Realization poset pipeline (generalized stages)

Parameterized versions of the proven stage1–6 workflow, generated from the
spec instead of hand-written:

- **stage1** — synthesize model; assert `codim IX = expected_codim`; assert
  the `ramification_det_identity`; eliminant retaining the fiber coordinate.
- **stage2** — contact divisors project to `expected_base_image` walls.
- **stage3** — decompose the last channel's divisor ideal upstairs
  (`minimalPrimes`, then `primaryDecomposition`; async).
- **stage4** — incidence table: codim, degree, generic-saturation emptiness
  for the named strata lattice (`IR`, contacts, channel divisors, pairwise and
  triple sums).
- **stage4b** — minimal primes of the codim-2 strata (async).
- **stage5** — every named slice: branch image, channel images, contact ∩
  channel meets, factored generators.
- **stage6** (optional) — collision comparison: projected eliminant
  discriminant vs true branch image on a user-named collision slice.

Fast stages run synchronously in `realize_branch_poset`; stages 3/4b run under
the job manager. Output: the realized poset table (stratum, codim in X,
degree, empty-after-saturation, irreducible?) plus certificate files.

## 9. M2 output protocol

Templates are standalone: they inline the synthesized model, so each script
reruns by hand with `M2 --script`. Machine results print as a fenced block:

```
-----BEGIN WREATH RESULT-----
{ "gate": "prime_upstairs", "divisor": "even_contact", "pass": true, ... }
-----END WREATH RESULT-----
```

JSON is emitted by a small M2 formatter in `WreathEngine.m2` (use the `JSON`
package if present in 1.25.11, else a hand-rolled emitter for the flat types
we need). Everything outside the fences is human-readable audit text, saved
verbatim to `runs/<run-id>/<script>.out.txt`.

## 10. Runs, jobs, certificates

- `run_id` = timestamp + spec name + short content hash of the spec.
- `runs/<run-id>/` contains `spec.json` (frozen copy), every rendered `.m2`,
  every raw `.out.txt`, `result.json`, `report.md`.
- Job registry: `runs/jobs.json` mapping `job_id → {pid, run_id, state,
  started, script}`. States: `running | done | failed | cancelled | timeout`.
  Default timeout 1h, configurable per call. Cancel sends SIGTERM then
  SIGKILL to the M2 process group.
- `inspect_certificate` never recomputes; it only reads artifacts.

## 11. Error handling

- Spec violations → `error` with JSON-pointer paths (Python-side, no M2 run).
- M2 nonzero exit → `error` with the last 50 lines of the log and the script
  path (the script is kept for post-mortem).
- Gate failure → `refuted` with gate name, divisor, and M2 evidence excerpt.
- Symbolic-power bound hit → `error` advising a larger `N_max` or a slice.
- Persistent-session wedge (exploratory only) → session is killed and
  restarted; the tool returns `error` for that call.

## 12. Testing

- **Unit (fast, pure Python):** `f2.py` rank/kernel/inverse on known cases
  including `B_static = [[1,0],[1,1]]` and `B_rot` (both invertible, plus a
  constructed rank-deficient case whose kernel is checked exactly);
  spec validation happy/sad paths; result-block parser.
- **Integration (fast, needs M2):** static crown spec — verify two contact
  divisors end-to-end; assert `certified` envelope fields; assert a doctored
  spec (wrong parity row) yields `refuted` at `on_sheet_parity`.
- **Golden (slow, optional tier):** reproduce yesterday's certified facts on
  the rotating spec: principal irreducible quintic, all 16 walls, `IZ` prime
  of degree 64, `IR+IZ` prime of degree 192. Compared against
  `certificates/m2_out_2026-07-10/` values, not raw text.
- **MCP:** in-process client calls each tool against the static example.

## 13. Registration and CLI

- `.mcp.json` at repo root registers the server:
  `uv --directory tools/wreath_engine run wreath-engine-mcp` (stdio).
- CLI for humans: `uv run wreath-engine verify <spec.json>` (analyze + verify
  + wreath lift + inertia, writes `report.md`) and
  `uv run wreath-engine run <spec.json>` (adds the realization poset,
  running async stages to completion).

## 14. Scope fences (v1)

- Base monodromy is claimed, never computed. No group-theory census.
- Tame inertia only; residue characteristic 2 out of scope (matches paper).
- Geometric irreducibility after base extension not claimed (matches package
  scope fences).
- `suggest_parity_rows` is best-effort and clearly labeled; its output cannot
  flow into a certificate without passing `verify_valuation_matrix`.
- No parallel job scheduling beyond the OS (jobs are independent processes).
- The `J=0` split special fiber (branch-compatible component selection) is
  the user's responsibility via slices; the engine does not automate it.
