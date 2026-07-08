# Cella Pathfinder Route Planning Design

Date: 2026-07-08

## Goal

Build the next pathfinder layer for Cella so Claude can decide how to handle a
single expression before doing expensive symbolic or high-precision numerical
work. The first deliverable is single-expression route planning. Candidate
generation and ranking follows immediately after and consumes the route-plan
result.

This design keeps the existing `cella_residual_profile` tool. It extends the
pathfinder surface around it instead of replacing it.

## Existing Base

The current MCP surface already has:

- `cella_residual_profile`: classifies operation shape and records binary64
  residual telemetry.
- Exact-account probe samples for rational arithmetic subgraphs:
  `rounded_difference + rounding_residue == difference_exact`.
- Cleanliness tools: `cella_bacl_pair`, `cella_operand_residue_trace`,
  `cella_cleanliness_rank`, `cella_bacl_dial`, and `cella_refinery_compare`.
- A `pathfinder` MCP profile for lightweight route-selection work.

The next layer should connect these pieces into a single expression-level
decision flow.

## Phase 1: `cella_route_plan`

### Purpose

Return a compact route decision for one expression. This is the tool Claude
should call before expanding, simplifying, sampling, or raising precision.

### Inputs

- `expression`: expression string using the existing residual-profile grammar.
- `sweep`: `{variable, low, high}` or explicit positive `points`.
- `constants`: optional mapping for non-sweep symbols.
- `include_profile`: optional bool, default false. If true, include the full
  residual profile in the result.
- `include_samples`: optional bool, default false. Passed through to
  `cella_residual_profile`.

### Output

The value record should include:

- `decision`: one of:
  - `direct_ok`
  - `collapse_symbolically`
  - `rewrite_candidate_needed`
  - `rank_declared_forms`
  - `precision_budget_needed`
  - `needs_declared_constants`
  - `unsupported_shape`
- `why`: short route explanation.
- `operation_shape`: copied from the residual profile.
- `dominant_pattern`: copied from the burden vector.
- `exact_account_available`: true when at least one arithmetic probe site has
  exact Q account telemetry.
- `blocking_inputs`: missing constants or unsupported grammar reasons.
- `next_tools`: ordered tool list for Claude.
- `route_confidence`: `high`, `medium`, or `low`.
- `profile_summary`: compact site and burden summary.
- `profile`: full residual profile only when `include_profile=true`.

### Decision Rules

- No subtraction -> `direct_ok`.
- Structural self-cancellation -> `collapse_symbolically`.
- Unknown/unrecognised sites -> `needs_declared_constants` if the failure is
  missing parameter data; otherwise `unsupported_shape`.
- Catastrophic same-leading-constant cancellation -> `rewrite_candidate_needed`
  when a known rewrite family is plausible; otherwise `precision_budget_needed`.
- Benign cancellation -> `direct_ok` with BACL monitor as the next tool.
- Ordinary non-cancelling subtraction -> `direct_ok`.

The route planner must not perform aggressive symbolic algebra. It decides the
process, not the final mathematics.

## Phase 2: `cella_rewrite_candidates`

### Purpose

Generate conservative candidate forms only when the route plan says a rewrite is
useful. The generator should prefer small, inspectable algebraic moves.

### Inputs

- `expression`
- optional `route_plan`
- optional `sweep`
- optional `constants`

### Candidate Families

- Structural self collapse: `x - x -> 0`.
- Difference of squares: `a*a - b*b -> (a-b)*(a+b)`.
- Common factor extraction: `u*c - v*c -> c*(u-v)` when the parser can see the
  common factor.
- Three-term additive regrouping for pair-first absorption.
- Known conjugate templates:
  - `sqrt(1+x)-1 -> x/(sqrt(1+x)+1)`
  - `1-sqrt(1-x) -> x/(1+sqrt(1-x))`

### Output

- `original`
- `candidates`: list of `{name, expression, family, reason, risk}`
- `requires_ranking`: true when more than one candidate is emitted.
- `not_generated`: explanations for skipped families.

The generator should be conservative. It is better to emit fewer candidates than
to flood Claude with speculative forms.

## Phase 3: `cella_pathfinder_compare`

### Purpose

Rank original and candidate forms by exact-account and BACL/refinery burden over
a declared grid.

### Inputs

- `variables`
- `forms`: list of `{name, expression}`
- `grid`: `{variable: [binary64 declarations]}`
- optional `dimensions`

### Ranking Law

Use existing cleanliness machinery where possible. Rank by:

1. exact-real equivalence over the declared grid;
2. lower BACL lattice burden;
3. lower rounding residual in ulps;
4. lower final residual in ulps;
5. lower operation depth;
6. stable lexical tie-break.

### Output

- `winner`
- `ranking`
- `burden_vectors`
- `equivalence_status`
- `trace_examples`
- `decision_reason`
- `next_tools`

The comparator is a route selector, not a proof that two expressions are
globally identical. It ranks forms over the declared grid and reports that
scope explicitly.

## MCP Integration

Add these tools to the `pathfinder` profile:

- `cella_route_plan`
- `cella_rewrite_candidates`
- `cella_pathfinder_compare`

Update:

- `TOOL_NAMES`
- `TOOL_GROUPS["pathfinder"]`
- `tool_callable_map`
- `cella_help`
- router/profile gates

## Error Handling

- Missing constants produce structured `needs_declared_constants` route output
  when the expression otherwise parses.
- Unsupported grammar produces `unsupported_shape`.
- Candidate generation errors should be per-family, not whole-tool failures,
  unless the expression cannot be parsed at all.
- Ranking must refuse non-equivalent forms on the declared grid and report the
  first failing sample.

## Tests

Add focused gates proving:

- `(1 + eps) - 1` routes to `rewrite_candidate_needed`.
- `eps - eps` routes to `collapse_symbolically`.
- `(A + eps) - A` without `A` routes to `needs_declared_constants`.
- `(1 + sqrt(eps)) - 1` routes to `direct_ok` with BACL monitoring.
- `sqrt(1+eps)-1` emits the conjugate candidate.
- `((12+eps)*(12+eps))-144` emits a difference/common-structure candidate when
  representable.
- A declared candidate set ranks a cleaner form above a dirtier original using
  existing BACL/refinery dimensions.
- Router dispatch works from the `pathfinder` profile.

## Deliberate Non-Goals

- Full CAS simplification.
- Global symbolic equivalence proof for arbitrary expressions.
- Multivariate asymptotic path algebra.
- Replacing the exact symbolic arm.
- Replacing high-precision arithmetic tools.

The pathfinder decides the next process. Other Cella tools perform the deeper
work.
