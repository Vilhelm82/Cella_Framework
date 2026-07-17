# RULE LEDGER — Campaign E

Reported confirmed rules (25 survive-direction + 15 collapse-direction). Full machine-readable set: `summary.json → rules`. Every predictor is §7 Hessian-structural (`forbidden_field_check_passed = true` for all).

Confirmed total: **2563** · held-out validated: **1759** · train-only: **804** · rejected: **0** · min-support 10, max-depth 3.

| rule_id | outcome | support | violations | held-out status | predicate |
|---|---|---|---|---|---|
| E-RULE-0001 | SURVIVES | 273 | 0 | VALIDATED_HELDOUT | `any_rank_drop is_false` AND `channel_zero_pattern_set_size_r2 le 4` AND `diag_support_set_size ge 4` |
| E-RULE-0002 | SURVIVES | 239 | 0 | VALIDATED_HELDOUT | `any_rank_drop is_false` AND `channel_zero_pattern_set_size_r2 le 3` AND `diag_support_set_size ge 4` |
| E-RULE-0003 | SURVIVES | 236 | 0 | VALIDATED_HELDOUT | `any_channel_cancellation_r1 is_true` AND `any_rank_drop is_false` AND `diag_support_set_size ge 4` |
| E-RULE-0004 | SURVIVES | 232 | 0 | VALIDATED_HELDOUT | `any_rank_drop is_false` AND `channel_sign_pattern_set_size_r2 le 6` AND `diag_support_set_size ge 4` |
| E-RULE-0005 | SURVIVES | 232 | 0 | VALIDATED_HELDOUT | `channel_zero_pattern_set_size_r2 le 4` AND `diag_support_set_size ge 4` AND `offdiag_support_set_size le 3` |
| E-RULE-0006 | SURVIVES | 229 | 0 | VALIDATED_HELDOUT | `any_rank_drop is_false` AND `channel_zero_pattern_set_size_r2 le 4` AND `diag_support_set_size eq 4` |
| E-RULE-0007 | SURVIVES | 225 | 0 | VALIDATED_HELDOUT | `diag_support_set_size ge 4` AND `graph_family_count le 2` AND `graph_family_set contains triangle` |
| E-RULE-0008 | SURVIVES | 216 | 0 | VALIDATED_HELDOUT | `channel_zero_pattern_set_size_r2 le 4` AND `diag_support_set_size eq 4` AND `offdiag_support_set_size le 3` |
| E-RULE-0009 | SURVIVES | 216 | 0 | VALIDATED_HELDOUT | `diag_support_set_size ge 4` AND `graph_family_count eq 2` AND `graph_family_set contains triangle` |
| E-RULE-0010 | SURVIVES | 214 | 0 | VALIDATED_HELDOUT | `channel_sign_pattern_set_size_r2 le 6` AND `diag_support_set_size ge 4` AND `offdiag_support_set_size le 3` |
| E-RULE-0011 | SURVIVES | 214 | 0 | VALIDATED_HELDOUT | `channel_zero_pattern_set_size_r2 le 3` AND `diag_support_set_size ge 4` AND `graph_family_count le 2` |
| E-RULE-0012 | SURVIVES | 211 | 0 | VALIDATED_HELDOUT | `any_rank_drop is_false` AND `channel_sign_pattern_set_size_r2 le 5` AND `diag_support_set_size ge 4` |
| E-RULE-0013 | SURVIVES | 209 | 0 | VALIDATED_HELDOUT | `any_rank_drop is_false` AND `channel_zero_pattern_set_size_r2 le 3` AND `diag_support_set_size eq 4` |
| E-RULE-0014 | SURVIVES | 208 | 0 | VALIDATED_HELDOUT | `channel_zero_pattern_set_size_r2 le 3` AND `diag_support_set_size ge 4` AND `offdiag_support_set_size le 3` |
| E-RULE-0015 | SURVIVES | 205 | 0 | VALIDATED_HELDOUT | `channel_zero_pattern_set_size_r2 le 3` AND `diag_support_set_size ge 4` AND `graph_family_count eq 2` |
| E-RULE-0016 | SURVIVES | 204 | 0 | VALIDATED_HELDOUT | `any_rank_drop is_false` AND `channel_sign_pattern_set_size_r2 le 6` AND `diag_support_set_size eq 4` |
| E-RULE-0017 | SURVIVES | 203 | 0 | VALIDATED_HELDOUT | `channel_sign_pattern_set_size_r2 le 5` AND `diag_support_set_size ge 4` AND `offdiag_support_set_size le 3` |
| E-RULE-0018 | SURVIVES | 201 | 0 | VALIDATED_HELDOUT | `diag_support_set_size ge 4` AND `graph_family_set eq ['open_chain', 'triangle']` |
| E-RULE-0019 | SURVIVES | 200 | 0 | VALIDATED_HELDOUT | `channel_sign_pattern_set_size_r2 le 6` AND `diag_support_set_size eq 4` AND `offdiag_support_set_size le 3` |
| E-RULE-0020 | SURVIVES | 198 | 0 | VALIDATED_HELDOUT | `channel_zero_pattern_set_size_r2 le 3` AND `diag_support_set_size eq 4` AND `support_mask_set_size ge 6` |
| E-RULE-0021 | SURVIVES | 197 | 0 | VALIDATED_HELDOUT | `any_channel_cancellation_r1 is_true` AND `any_rank_drop is_false` AND `diag_support_set_size eq 4` |
| E-RULE-0022 | SURVIVES | 195 | 0 | VALIDATED_HELDOUT | `any_channel_cancellation_r1 is_true` AND `diag_support_set_size ge 4` AND `offdiag_support_set_size le 3` |
| E-RULE-0023 | SURVIVES | 195 | 0 | VALIDATED_HELDOUT | `channel_zero_pattern_set_size_r2 le 3` AND `diag_support_set_size eq 4` AND `offdiag_support_set_size le 3` |
| E-RULE-0024 | SURVIVES | 192 | 0 | VALIDATED_HELDOUT | `channel_zero_pattern_set_size_r2 eq 3` AND `diag_support_set_size ge 4` AND `rank_min ge 2` |
| E-RULE-0025 | SURVIVES | 190 | 0 | VALIDATED_HELDOUT | `any_channel_cancellation_r2 is_true` AND `diag_support_set_size ge 4` AND `support_mask_set_size ge 9` |
| E-RULE-0026 | COLLAPSES | 30 | 0 | TRAIN_ONLY | `all_channel_cancellation_r1 is_true` AND `channel_sign_pattern_set_size_r2 le 2` AND `graph_family_set eq ['open_chain', 'single_edge']` |
| E-RULE-0027 | COLLAPSES | 24 | 0 | TRAIN_ONLY | `all_channel_cancellation_r1 is_true` AND `all_channel_cancellation_r2 is_true` AND `graph_family_set eq ['open_chain', 'single_edge']` |
| E-RULE-0028 | COLLAPSES | 24 | 0 | TRAIN_ONLY | `all_channel_cancellation_r1 is_true` AND `channel_sign_pattern_set_size_r2 eq 2` AND `graph_family_set eq ['open_chain', 'single_edge']` |
| E-RULE-0029 | COLLAPSES | 24 | 0 | TRAIN_ONLY | `channel_sign_pattern_set_size_r2 eq 1` AND `diag_support_set_size eq 1` AND `graph_family_set eq ['single_edge', 'triangle']` |
| E-RULE-0030 | COLLAPSES | 20 | 0 | TRAIN_ONLY | `all_channel_cancellation_r1 is_true` AND `diag_support_set_size eq 1` AND `graph_family_set eq ['open_chain', 'single_edge']` |
| E-RULE-0031 | COLLAPSES | 16 | 0 | TRAIN_ONLY | `all_channel_cancellation_r1 is_true` AND `all_channel_cancellation_r2 is_true` AND `graph_family_set eq ['single_edge', 'triangle']` |
| E-RULE-0032 | COLLAPSES | 16 | 0 | TRAIN_ONLY | `diag_support_set_size eq 1` AND `graph_family_set contains empty` AND `graph_family_set contains triangle` |
| E-RULE-0033 | COLLAPSES | 15 | 0 | TRAIN_ONLY | `any_rank_drop is_false` AND `channel_sign_pattern_set_size_r2 le 3` AND `graph_family_set eq ['empty', 'triangle']` |
| E-RULE-0034 | COLLAPSES | 14 | 0 | TRAIN_ONLY | `diag_support_set_size eq 1` AND `graph_family_set eq ['empty', 'triangle']` |
| E-RULE-0035 | COLLAPSES | 14 | 0 | TRAIN_ONLY | `all_rank_drop is_false` AND `diag_support_set_size eq 1` AND `graph_family_set contains empty` |
| E-RULE-0036 | COLLAPSES | 14 | 0 | TRAIN_ONLY | `channel_sign_pattern_set_size_r2 eq 2` AND `graph_family_set eq ['open_chain', 'single_edge']` AND `support_mask_set_size eq 3` |
| E-RULE-0037 | COLLAPSES | 14 | 0 | VALIDATED_HELDOUT | `diag_support_set_size eq 1` AND `graph_family_set eq ['single_edge', 'triangle']` AND `rank_set eq [2, 3]` |
| E-RULE-0038 | COLLAPSES | 13 | 0 | TRAIN_ONLY | `any_rank_drop is_false` AND `channel_zero_pattern_set_size_r2 eq 2` AND `graph_family_set eq ['empty', 'triangle']` |
| E-RULE-0039 | COLLAPSES | 11 | 0 | TRAIN_ONLY | `any_channel_cancellation_r2 is_false` AND `any_rank_drop is_false` AND `graph_family_set contains empty` |
| E-RULE-0040 | COLLAPSES | 11 | 0 | TRAIN_ONLY | `any_rank_drop is_false` AND `diag_support_set_size eq 1` AND `graph_family_set contains empty` |
