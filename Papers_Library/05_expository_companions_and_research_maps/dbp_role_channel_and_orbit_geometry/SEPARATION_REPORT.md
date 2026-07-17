# SEPARATION REPORT — Campaign A

## CL-A5 — carrier separation (n=3)

**Frozen search bounds.** g ∈ {(1,1,1), (1,2,3), (2,-1,1)}; symmetric Hessian entries in {-2,-1,0,1,2}; the zero Hessian is skipped. Deterministic enumeration order; reproducible.

**Method.** For each g, group all Hessians by `(q, reduced_density_tower)`. A group holding two or more **distinct density fingerprints** is a separation candidate: the reduced scalar tower `(Ĉ₁(1,1), Ĉ₂(1,1))` collapses jets that the channel carrier distinguishes.

**Result.**

| quantity | value |
|---|---|
| jets scanned | 46 872 |
| distinct `(q, reduced_tower)` groups | 8 517 |
| **separation groups** (≥2 carriers per reduced class) | **5 298** |
| candidates reported (capped, deterministic) | 20 (`summary.json → separation.candidates`) |

**Verdict: PASS** — abundant exact separation candidates exist.

### What this does and does not establish

- **Passive-excluded (proven).** Two jets with different *sorted* fingerprints cannot be related by a passive coordinate permutation (CL-A2: the fingerprint forgets coordinate labels). So these candidates are **not** relabellings of one another.
- **Gauge status: unknown (not resolved).** The gauge orbit H→H+ga^T+ag^T moves channel content while fixing the reduced tower (CL-A3). Therefore some — possibly all — separation candidates could be **gauge-equivalent**, i.e. the same jet seen in different defining-function gauges. This campaign does **not** solve the gauge orbit, so every candidate carries `known_gauge_equivalent: "unknown"` and is classified `separation_candidate`, **never** `separation_theorem`.

### Representative candidates (first 3 of 20)

```
sep_n3_0000  g=(1,1,1)
  H1 = [-2,-2,-2; -2,-2,-2; -2,-2,-2]   labels: regular, rank_drop, scalar_flat_channel_active_r1, scalar_flat_channel_active_r2
  H2 = [-2,-2,-1; -2,-2,-1; -1,-1, 0]   labels: regular, rank_drop, scalar_flat_channel_active_r1, scalar_flat_channel_active_r2
  same_reduced_tower=True  same_density_carrier=False  passive_equivalent=False  known_gauge_equivalent=unknown

sep_n3_0001  g=(1,1,1)
  H1 = [-2,-2,-2; -2,-2,-2; -2,-2,-1]   labels: regular, rank_drop, channel_cancellation_present_r1, scalar_flat_channel_active_r2
  H2 = [-2,-2,-2; -2,-1,-1; -2,-1,-1]   labels: regular, rank_drop, channel_cancellation_present_r1, scalar_flat_channel_active_r2
  same_reduced_tower=True  same_density_carrier=False  passive_equivalent=False  known_gauge_equivalent=unknown

sep_n3_0002  g=(1,1,1)
  H1 = [-2,-2,-2; -2,-2,-2; -2,-2, 0]   labels: regular, rank_drop, channel_cancellation_present_r1, scalar_flat_channel_active_r2
  H2 = [-2,-2,-2; -2, 0, 0; -2, 0, 0]   labels: regular, rank_drop, channel_cancellation_present_r1
  same_reduced_tower=True  same_density_carrier=False  passive_equivalent=False  known_gauge_equivalent=unknown
```

The recurring `scalar_flat_channel_active` label is notable: many separation candidates sit at a reduced tower of `(0,0)` — scalar-flat in both elementary orders — yet carry distinct, non-zero channel content. This is the campaign's first-order answer to its own question (see `ATLAS_SUMMARY.md`).

## CL-A6 — interaction-order split (n=4)

**Frozen search bounds.** g ∈ {(1,1,1,1), (1,2,3,4), (2,-1,1,3)}; entries in {-1,0,1}; early-exit at first witness.

**Result.** Witness found on the first scanned jet:

```
g = (1,1,1,1)
H = [[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]]
r = 3:  K_{2,1} = 12,  K_{1,2} = -12   ->   K_{2,1} != K_{1,2}
```

A second, sparser witness is banked as the named fixture `n4_interaction_order_split_candidate` (g=(1,1,1,1), K₄ coupling + diag(0,0,0,1)): K₂,₁ = -3 ≠ K₁,₂ = 0.

**Verdict: PASS** — interaction order is asymmetric at r=3. Recorded as a **witness**, not a structural theorem.
