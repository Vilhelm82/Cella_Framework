# root-closure-atlas — record schema (D1; FREEZE GATES ON WILL)

**Status: FROZEN v1 — Will's sign-off 2026-06-11 (machine date), both
deviations blessed.** Implementation: `src/lloyd_v4/evals/root_closure_atlas/schema.py`
(`AtlasRecord`, slotted dataclass; JSON-serialized one record per line).
After freeze, changes land only as versioned schema amendments pinned
pre-execution — never silent field additions (Design Principle 3).

## Fields (schema_version = 1)

| Field | Type | Semantics |
|---|---|---|
| `campaign_id` | str | literal `root_closure_atlas` (neutral path token; covenant: no name in schemas) |
| `schema_version` | int | 1 |
| `stage` | str | `"0"`, `"A"`, … |
| `fixture_id` / `fixture_class` / `fixture_params` | str / str / dict | manifest keys; params echo the pinned instance |
| `route_id` | str | the expression ROUTE (sexpr identity) — route-variant pairs differ here |
| `instrument_id` | str | e.g. `I1a_bisection`, `I2_multi_start`, `I3_probe_v0_stub`; judge and navigator IDs never shared |
| `role` | enum | `judge` \| `oracle` \| `probe` \| `navigator` |
| `start_or_seed` | any | pinned start (hex) / seed grid id / null |
| `returned_values` | tuple[float] | what the instrument returned (possibly empty) |
| `instrument_claim` | enum | `converged` \| `refused` \| `diverged` \| `max_iter` \| `not_applicable` |
| `instrument_declared_tol` | dict\|null | the registered stopping rule, echoed verbatim |
| `certificate` | enum | `none` \| `sign_change_cell` \| `exact_zero` \| `refusal` \| `enclosure` |
| `terminal_cell` | {lo,hi}\|null | hex-float adjacent pair (the campaign's ground-truth object) |
| `verdict_vs_own_promise` | enum | `kept` \| `broken` \| `na` — column 1 of two-column honesty |
| `verdict_vs_certified_cell` | enum | `inside` \| `outside_by_k_ulps` \| `missed_root` \| `ghost_accepted` \| `na` — column 2 |
| `outside_by_k_ulps` | int\|null | present iff verdict is `outside_by_k_ulps` |
| `account` | dict\|null | I3-era lanes (cancellation_binades, exposure, realized, div_amplification, refusals); null for I1/I2 |
| `arbiter` | dict\|null | {ground_truth_ref, certified_cell, dual_arbiter_agreement} |
| `telemetry` | dict | n_evals / n_iters / wall_ms — **permanently non-verdict-bearing** (covenant 3) |
| `v3_status_bucket` | str\|null | verbatim oracle vocabulary bucket (§17 (v); S3 collapse stays queryable) |
| `byte_hash` | str | sha256 of the canonical record sans hash |
| `notes` | str | free text, never graded |

## Deviation from the brief (blessed at freeze, Will 2026-06-11)

The brief's D1 pins `certificate {none|sign_change_cell|refusal|enclosure}`
(four values). The implemented vocabulary adds a fifth: **`exact_zero`** —
a root exactly at a float64 lattice point. The degenerate-cell argument:
a terminal cell is an adjacent-float pair, so a root AT a float collapses
the cell to a point; forcing it into `sign_change_cell` would falsify the
cell's one-lattice-step invariant, and `none` would erase a certified
zero. The axiom argument: **Axiom 6** (zero is measured or proven —
`identity_zero` is a distinct epistemic state, and `exact_zero` is
exactly its certificate at the root level) and **Axiom 9** (type-system
failures are real failures — a false `sign_change_cell` sticker on a
degenerate cell is worse than an honest fifth value). Pinned in the
manifest `freeze_note` as the P0.5 pre-execution amendment.

## Enforced invariants (tests, not convention)

1. **Role gate (P0.6):** a `navigator` record carrying any verdict
   content (`instrument_claim` ≠ `not_applicable`, any certificate,
   any cell, any non-`na` verdict) is REJECTED by `validate`.
2. **Ad-hoc fields (P0.5):** `from_json` rejects unknown keys and
   missing fields. The dataclass is slotted.
3. `outside_by_k_ulps` presence ⟺ the cell-verdict says so.
4. Two-column honesty: both verdict columns present on every judge
   record; neither substitutes for the other (Design Principle 2).
