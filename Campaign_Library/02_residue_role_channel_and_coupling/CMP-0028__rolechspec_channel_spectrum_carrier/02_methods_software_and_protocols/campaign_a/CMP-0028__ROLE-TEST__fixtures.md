# FIXTURES — Campaign A

Exact-Q hand-curated catalogue (`src/lloyd_v4/evals/channel_spectrum_carrier/fixtures.py`).
All `g` rational, all `H` symmetric rational. `q = g·g`.

## n = 3

| id | g | H (rows) | role |
|---|---|---|---|
| `n3_flat_zero_hessian` | (1,2,3) | 0 | every channel vanishes |
| `n3_pure_self_positive` | (1,1,1) | diag(2,3,1) | pure self, no coupling |
| `n3_pure_coupling_single_edge` | (1,1,1) | edge (0,1)=1 | single coupling edge |
| `n3_pure_coupling_open_chain` | (1,1,1) | edges (0,1),(1,2)=1 | open chain (path) |
| `n3_pure_coupling_triangle` | (1,1,1) | edges (0,1),(0,2),(1,2)=1 | triangle |
| `n3_saddle_graph_z_minus_xy` | (-1,-1,1) | edge (0,1)=-1 | graph saddle z=xy; pure coupling **negative** |
| `n3_keystone_interaction_survives` | (3,1,2) | [[2,1,0],[1,0,0],[0,0,2]] | **keystone** (hand-pinned truth) |
| `n3_scalar_flat_channel_active` | (1,1,1) | [[-2,-1,-1],[-1,-2,2],[-1,2,-2]] | ΣĈ₂=0 but Ĉ₂≠0 (full rank) |
| `n3_gauge_transport_keystone` | (3,1,2) | keystone H | + gauges a=(1,0,0),(0,1,0),(1,-2,3),(-1/2,5,1) |

### Keystone — hand-pinned literal truth (PREREG_AMENDMENT_001 A1.2)

Derived by hand (cofactor expansion), **not** by the implementation under test; the suite asserts the engine reproduces them.

| quantity | value |
|---|---|
| q | 14 |
| Ĉ₁ | {(1,0): 6, (0,1): -30} |
| Ĉ₁(1,1) | -24 |
| Ĉ₂ | {(2,0): -4, (1,1): -12, (0,2): 4} |
| Ĉ₂(1,1) | -12 |
| κ_c, κ_int, κ_s (r=2, normalized by q²) | -1/49, -3/49, 1/49 |
| K_G | -3/49 |

Parity: r=1 is odd and q=14 is not a perfect square, so the normalized σ₁ lives in **Q(√14)** and is reported as `Q(sqrt q)`-class — never as a false rational. The density coefficients (6, -30, -24) remain exactly rational.

## n = 4

| id | g | coupling | role |
|---|---|---|---|
| `n4_flat_zero_hessian` | (1,2,3,4) | — | flat |
| `n4_pure_self_diagonal_generic` | (1,2,3,4) | diag(1,-2,3,1) | pure self |
| `n4_single_coupling_edge` | (1,2,3,4) | (0,1) | single edge |
| `n4_path_graph_coupling` | (1,2,3,4) | (0,1),(1,2),(2,3) | open chain |
| `n4_star_graph_coupling` | (1,2,3,4) | (0,1),(0,2),(0,3) | star |
| `n4_triangle_plus_isolated` | (1,2,3,4) | (0,1),(0,2),(1,2) | triangle + isolated vertex |
| `n4_complete_graph_coupling` | (1,2,3,4) | all 6 | complete K₄ |
| `n4_mixed_self_coupling_sparse` | (1,2,3,4) | diag(1,0,0,2)+ (0,1) | sparse mix |
| `n4_mixed_self_coupling_dense` | (1,2,3,4) | diag(1,-1,2,1)+4 edges | dense mix |
| `n4_interaction_order_split_candidate` | (1,1,1,1) | K₄ coupling + diag(0,0,0,1) | **K₂,₁ ≠ K₁,₂ witness** (r=3) |

For n=4 the campaign reports the r=3 density pieces K₃,₀, K₂,₁, K₁,₂, K₀,₃ in `records.jsonl` (`channel_vectors["3"]`).
The split fixture has K₂,₁ = -3 ≠ K₁,₂ = 0 — a witness, not a theorem.

Scope: n=3,4 regular rational jets (q ≠ 0); even-order normalized curvature is exact-Q, odd-order is Q(√q)-class. Singular strata (q=0) are out of scope for this campaign.
