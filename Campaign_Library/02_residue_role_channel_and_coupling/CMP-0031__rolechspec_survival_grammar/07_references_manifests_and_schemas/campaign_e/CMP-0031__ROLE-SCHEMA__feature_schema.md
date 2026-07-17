# FEATURE SCHEMA — Campaign E

Every quantity, classified by how the rule miner is allowed to use it. The
`predictor_allowed` set is exactly the §7 Hessian-structural feature schema; the
miner uses nothing else. `features.py` is architecturally barred from importing
the RoleChSpec / gauge engine, so a target field cannot reach a predictor.

## predictor_allowed (mineable structural features)

Computed per class from its representative Hessians + `g` + reduced tower, via Campaign A structure only (rank, coupling graph, channel patterns, strata).

| feature | type |
|---|---|
| `rank_min`, `rank_max`, `rank_span` | int |
| `rank_set` | tuple<int> |
| `all_rank_drop`, `any_rank_drop` | bool |
| `graph_family_set` | tuple<str> |
| `graph_family_count` | int |
| `all_same_graph_family` | bool |
| `diag_support_set_size` | int |
| `offdiag_support_set_size` | int |
| `support_mask_set_size` | int |
| `channel_zero_pattern_set_size_r2` | int |
| `channel_sign_pattern_set_size_r2` | int |
| `all_scalar_flat_r1`, `any_scalar_flat_r1` | bool |
| `all_scalar_flat_r2`, `any_scalar_flat_r2` | bool |
| `all_channel_cancellation_r1`, `any_channel_cancellation_r1` | bool |
| `all_channel_cancellation_r2`, `any_channel_cancellation_r2` | bool |
| `reduced_tower_r1_zero`, `reduced_tower_r2_zero`, `reduced_tower_is_zero` | bool |

## target_only (graded against, never a predictor)

| field | why |
|---|---|
| `survival_label` | the target itself |
| `n_rolechspec_carriers` | distinct RoleChSpec count — directly determines the label |

## debug_only (record metadata, excluded from mining)

| field | why |
|---|---|
| `n_direct_carriers`, `n_representatives` | counts of distinct direct carriers; §7 marks the direct-carrier fingerprint debug-only, so its count is kept out of the mineable schema to stay clear of any tautology (it predicts survival, but is reported only as an observation — see `SURVIVAL_GRAMMAR.md`) |
| `q`, `reduced_tower`, `g`, `class_id` | class identity / provenance |

## forbidden_for_rule_mining (would be tautological — KC-E2 / KC-E9)

`rolechspec_fingerprint`, `rolechspec_equal`, `gauge_status` / `gauge_verdict` / `gauge_equivalent`, `direct_carrier_fingerprint`, `candidate_id`, and any `summary.json` verdict field. `features.assert_no_forbidden` raises if any of these appears among the predictor features, and `run_campaign_e` checks every reported rule's predicates against this set (`forbidden_field_check_passed`).
