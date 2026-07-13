# Wreath Engine

Executable pipeline for the **conjugate Kummer wreath-lift theorem**
(`docs/galois_horizon_cover_v1_0_publication_package/supporting_reports/KUMMER_MODULE_WREATH_LIFT_THEOREM_2026-07-10.md`).

Supply a separable base cover of degree `d` with claimed monodromy `G`, the
radical channels `r_1..r_s`, and candidate divisors with claimed
valuation-parity rows. The engine returns the Kummer rank, `[H:K]`, the
wreath closure `C_2^s ≀ G` (under certified maximal rank), the colored
inertia table, and the Macaulay2 realization poset — every mathematical claim
backed by a standalone, hand-rerunnable `.m2` script and its verbatim output
under `runs/<run-id>/`. On rank failure the kernel (the square-class relation
module) is returned explicitly.

**Division of labor.** Python does bookkeeping: F2 linear algebra, wreath
order arithmetic, inertia tables, reports, jobs. Macaulay2 (1.25+) is the
mathematical authority: primality, unramifiedness, valuation parities,
decompositions. A result is `"certified"` only when every gate ran in M2.

## Quick start

```sh
cd tools/wreath_engine
uv sync
uv run pytest                       # 22 tests; M2 integration included
uv run wreath-engine verify examples/horizon_static.json
uv run wreath-engine report examples/horizon_static.json
```

The static example certifies in seconds and reproduces the audited R9
theorem: `Gal = C_2^2 ≀ S_5`, order 122880.

## MCP server

Registered in the repo root `.mcp.json` as `wreath-engine`. Tools:

- `analyze_kummer_module` — F2 facts from claimed rows (status `claimed`)
- `verify_valuation_matrix` — the certified checklist (M2): prime upstairs,
  not in ramification, not in singular locus, on-sheet parity via bounded
  symbolic powers, off-sheet evenness via norm valuation, expected wall image
- `compute_wreath_lift` — certified rank ⇒ `C_2^s ≀ G`; deficient ⇒ kernel
- `classify_inertia` — colored inertia table (sign vectors × base cycles)
- `realize_branch_poset` — walls, incidence table, slices; optional
  decompositions
- `suggest_parity_rows` — exploratory probe (never certifies)
- `start_verification` / `start_realization` + `get_job_status` /
  `get_job_result` / `cancel_job` / `list_jobs` — async jobs
- `inspect_certificate`, `render_report`

Result envelopes carry `status` ∈ `certified | claimed | refuted |
exploratory | error`; `refuted` names the failed gates and, for rank
failures, the relation module.

## Problem specs

Declarative JSON (see `examples/`): ring + weights, incidence generators,
sheet variables, claimed `d` and `G` (accepted, never recomputed — the all-k
interface), channels, divisors with claimed parity rows, generic denominator,
slices. Channel radicands may reference earlier channels; the generator
expands everything to ring variables before M2 sees it.

## Mathematical notes

- **On-sheet parity** is the symbolic-power order of the radicand along the
  divisor's prime upstairs (bounded search; hitting the bound is an error,
  never an answer).
- **Off-sheet evenness** uses the norm argument: with the divisor unramified
  in the closure and radicands regular, `v_base(Norm(r)) = Σ_sheets v(r)`;
  equality with the on-sheet order forces all off-sheet valuations to zero.
  The norm is read off the channel's characteristic polynomial over the base
  (elimination), and base multiplicities are exact UFD divisions.
- **Cover integrity** is certified per run: codimension, the ramification
  determinant identity, primitive-element degree `= d`, and irreducibility
  of its characteristic polynomial (so the generic fiber algebra is a field).
- Design doc: `docs/superpowers/specs/2026-07-11-wreath-engine-design.md`.
  Deviation from the doc: M2 scripts are generated programmatically in
  `m2gen.py` on top of the `m2/WreathEngine.m2` library rather than from
  template files; scripts remain standalone and hand-rerunnable.
