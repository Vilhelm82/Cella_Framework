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

The first surface is still the lightweight arithmetic planner. The final source
pass adds a DBP/geometry overlay: when an expression is known to come from the
DBP role-channel or inverse-channel metric setting, Pathfinder should classify
the channel and local germ before attempting any global symbolic expansion.

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

## Authority Hierarchy

For DBP/geometry routing, use this source order when records conflict:

1. `Project Management/roles/field-specialists/engineer/archieve/c001__THREE_CHANNEL_KG_CAMPAIGN_RESULTS__dev-role-manager-to-records-and-field-specialists.md`
   supersedes WARP-style or older portfolio framing for the three-channel KG
   campaign. These moves remain eval-tier until final sign-off, so route output
   should expose that status.
2. `portfolio/10_DBP_STANDING_RESULTS.md` governs standing DBP carrier,
   shape-resolution, modular, and supersession claims.
3. `paper/lead7_kn_n3_dbp_metric.tex` and `paper/pfc_normal_forms.tex` govern
   the inverse-channel metric selection rule and local curvature normal forms.
4. Older WARP/residual-path ideas remain available only as generic arithmetic
   Pathfinder machinery unless they agree with the three authorities above.

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
- Constant-offset collapse: `(c+x)-c -> x` and `(x+c)-c -> x`.
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
- `requires_ranking`: true when a nontrivial operational candidate should be
  compared against the original form before use. Structural self-collapse does
  not require ranking.
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

## DBP Geometry Overlay

### Purpose

Route DBP role-channel and inverse-channel metric work by structural metadata
before invoking broad CAS simplification. The overlay should decide whether the
right next move is channel evaluation, carrier decomposition, local germ
valuation, corner Newton analysis, or refusal due to a true singular locus.

### Route State

The overlay should add a compact geometry record when `domain="dbp"` or
`domain="inverse_channel_metric"` is declared:

- `authority`: `c001_eval`, `dbp_standing_results`, `lead7_kn`, `pfc_normal_forms`,
  or `generic_pathfinder`.
- `channel_predicate`: for example `delta_kappa_c`, `sigma_r`,
  `mass_role_lambda`, or `role_role_lambda`.
- `regularity_status`: `regular`, `q_zero_singular`, `role_divisor`,
  `channel_isotropy`, `chart_degenerate`, or `unknown`.
- `local_germ_kind`: `generic_quadratic`, `parity_fixed`, `corner_newton_wedge`,
  `carrier_shape`, or `unknown`.
- `shape_resolution`: `scalar_spectrum_sufficient`, `carrier_required`, or
  `not_applicable`.
- `route_status`: `eval_tier`, `standing_canonical`, `paper_local_form`, or
  `open_successor`.

### DBP Channel Rules

- Pin/move predicates are channel-level predicates. Stage C is keyed to
  `delta_kappa_c`, not to whole-vector equality of the channel tuple.
- Refuse only at the true singular locus `q = g^T g = 0`. A single coordinate
  condition such as `g_i = 0` is a chart/stratum fact, not automatic refusal.
- Distinguish squared total curvature from channel norm:
  `squared_total_KG = K_G^2` is not the same quantity as
  `channel_norm_sq = kappa_c^2 + kappa_s^2 + kappa_int^2`.
- For DBP carrier routing, default to the role-pair carrier
  `M^(n-2,2) = C[C(n,2)]`. The loss shape is `S^(n-2,2)`.
- The full scalar `sigma_r` spectrum resolves shape only for `n <= 4`.
  For `n >= 5`, route to carrier/witness machinery rather than trusting a
  scalar signature.
- Pure-coupling order `r` targets `S^(n-r,r)` when `n >= 2r`; mixed bidegrees
  and full density remain successor territory.
- Record prime-2/characteristic metadata explicitly. In characteristic 2,
  orientation and magnitude can collide, so parity and alternating-companion
  data should not be discarded.
- Keep role symmetry and monodromy symmetry separate. Do not identify role
  `S_3` with self-glue or product-cover monodromy unless a comparison map is
  explicitly supplied.

### Inverse-Channel Metric Rules

- For the Kerr-Newman n=3 metric, assemble by inverting each mass-role channel
  before summing. The selected metric uses `u=0`: role-role channels are omitted
  from the metric and treated as interior channel-isotropy diagnostics.
- Route by local valuation data, not by expanding the global scalar curvature.
  The global rational expression is a last-resort diagnostic, not the primary
  computation.
- Generic quadratic collapse with finite transverse channels routes to an
  order-3 pole. The leading coefficient is the transverse first log-drift,
  `A^{-1} sum_alpha d_x log(P_alpha)|_0`.
- Parity-fixed inverse-channel collapse routes to an order-4 pole with
  universal coefficient `-m(m+5)/B`. In the three-dimensional state-space case
  `m=2`, this is `-14/B`.
- Double reflection corners route to Newton-wedge analysis. Leading order is a
  support function of the polar vertices; it is not a sum of the two single-face
  laws. Vertex disappearance is decided by exact coefficient cancellation.
- Preserve graph-normalization data. In the KN chart, `q_i = 1 + |grad f_i|^2`
  and the `+U_i^2` contribution are structural, not optional simplifications.

### Overlay Tests

Add gates, when this overlay is implemented, for:

- Stage C pin/move uses `delta_kappa_c` and rejects a whole-vector substitute.
- `g_i = 0, q != 0` is not refused as singular.
- `K_G^2` and channel-norm square are reported as distinct quantities.
- KN reflection faces classify as `parity_fixed` and return `-14/B` for `m=2`.
- The extremal face classifies as `generic_quadratic` and returns order 3.
- A double reflection corner returns a Newton wedge, not a superposed face law.
- For `n=5`, scalar spectrum routing reports `carrier_required`.

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
  when the expression otherwise parses. Residual-profile site records should
  expose `unknown_parameters` structurally; route planning may retain a fallback
  parser for older profile records.
- Unsupported grammar produces `unsupported_shape`.
- Candidate generation errors should be per-family, not whole-tool failures,
  unless the expression cannot be parsed at all.
- Ranking must refuse non-equivalent forms on the declared grid and report the
  first failing sample.

## Tests

Add focused gates proving:

- `(1 + eps) - 1` routes to `rewrite_candidate_needed`.
- `cos(eps)-1` routes to `precision_budget_needed`.
- `(cos(eps)-1)+((1+eps)-1)` routes to `precision_budget_needed` because not
  every catastrophic site has a known rewrite.
- `eps - eps` routes to `collapse_symbolically`.
- `(A + eps) - A` without `A` routes to `needs_declared_constants`.
- `(1 + sqrt(eps)) - 1` routes to `direct_ok` with BACL monitoring.
- `sqrt(1+eps)-1` emits the conjugate candidate.
- `(1+eps)-1` emits a `constant_offset_collapse` candidate `eps`.
- `(a*a)-(b*b)` emits a general symbolic difference-of-squares candidate.
- `sqrt(1+eps+eps^2)-1` routes to rewrite and emits a matching generic
  conjugate candidate.
- `1-sqrt(1-eps)` routes to rewrite and emits the reverse conjugate candidate.
- Non-equivalent declared forms return a refusal-shaped compare result instead
  of leaking an exception.
- `((12+eps)*(12+eps))-144` emits a difference/common-structure candidate when
  representable.
- A declared candidate set ranks a cleaner form above a dirtier original using
  existing BACL/refinery dimensions.
- Router dispatch works from the `pathfinder` profile.

## Deliberate Non-Goals

- Full CAS simplification.
- Global symbolic equivalence proof for arbitrary expressions.
- General multivariate asymptotic path algebra outside declared local normal
  form families.
- Replacing the exact symbolic arm.
- Replacing high-precision arithmetic tools.

The pathfinder decides the next process. Other Cella tools perform the deeper
work.
