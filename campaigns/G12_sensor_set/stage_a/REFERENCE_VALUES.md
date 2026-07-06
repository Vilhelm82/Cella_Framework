# Stage A — per-sensor reference values (n=3 corpus, gated)

**Script:** `campaigns/G12_sensor_set/stage_a/reference_values.py` — byte-stable ×2,
stdout sha16 `d3e9e1ed1b5caf29`, exit 0, exact `Fraction`.

Scope (Will's call): keystone + one representative of each type — sphere, saddle,
cylinder. All four are n=3, where the shape doublet `S^(n−2,2)` and multi-triangle
localization do not yet exist, so at n=3 the sensor set reduces to the **numerator
channel**.

## Numerator channel and curvature, cross-routed to the certified bank

`kappa_2 = e_2(P Hc P)/q` (`Hc = offdiag H`) is the coupling channel; `sigma_2 =
e_2(P H P)/q` is the curvature `K_G`.

| surface  | κ₂ = e₂(P·Hc·P)/q | cert kc  | σ₂ = e₂(P·H·P)/q | cert K_G | kc+kint+ks |
|----------|-------------------|----------|------------------|----------|------------|
| keystone | −1/49             | −1/49    | −3/49            | −3/49    | −3/49      |
| sphere3  | 0                 | 0        | 1/14             | 1/14     | 1/14       |
| saddle   | −1/9              | −1/9     | −1/9             | −1/9     | −1/9       |
| cylinder | 0 (P-route)       | (refuse) | 0                | 0        | (refuse)   |

**Finding.** `κ_2 == kc` on every regular surface — the numerator channel *is* the
certified coupling channel, confirmed as an identity, not a keystone coincidence.
`σ_2 == K_G` and the cross-route `kc+kint+ks == σ_2` hold. Saddle is pure coupling
(`Hc = H`, zero diagonal) so `κ_2 = σ_2 = −1/9`; sphere is pure self (`Hc = 0`) so
`κ_2 = 0` while `σ_2 = 1/14`.

## Gates (each fires if the underlying math is wrong)

- **A** — `κ_2 == certified kc` (keystone −1/49, sphere 0, saddle −1/9). **PASS.**
- **B** — `σ_2 == certified K_G` (keystone −3/49, sphere 1/14, saddle −1/9, cylinder 0). **PASS.**
- **C** — cross-route `kc+kint+ks == σ_2` (gate_11 P3). **PASS.**
- **D — control (must distinguish).** the full-H numerator returns `σ_2 = −3/49` (= K_G)
  ≠ `kc = −1/49` at the keystone — the off-diagonal `Hc` restriction is load-bearing, so
  mistaking `Hc` for `H` is caught. **PASS.**

## Cylinder — the chart/regularity asymmetry (gate)

Cylinder has `g = (2,4,0)` (a zero gradient component). The numerator channel computes
via `P Hc P` (needs only `q = 20 ≠ 0`) and returns `0`; the carrier/fingerprint route,
which forms `O` by dividing by individual `g_i`, refuses `ROLE_CHART_UNAVAILABLE`. Same
asymmetry gate_11 P3 pins for the σ tower vs the carrier — the numerator tower is P-route
(computes), the fingerprint is O-route (refuses). This is where `CHANNEL_ISOTROPIC`
(A-010) / `ROLE_CHART_UNAVAILABLE` (A-009) get exercised at Stage C.

## Sensors that are n≥4 structures (absent/trivial at n=3; anchored elsewhere)

- **Shape moment.** `dim S^(n−2,2) = n(n−3)/2 = 0` at n=3 — no shape row on this corpus.
  Anchor: the RC-7 n=4 witness (isotypic quintuple 147/153/24/0, Σ=324).
- **Localization.** a single triangle at n=3 — the support theorem is trivial. Anchor:
  RC-8 (`{S : dΔ_S/dt≠0} = {S⊇e*}`, n≥4).
- **Fingerprint anisotropy.** keystone `A_c = 42793/1555848` [certified RC-4] — cited,
  not re-derived; the faithfulness det `8·Λ_P·Λ_D·Λ_S/q0⁶` and the `Λ_ρ=0` stratum
  (A-010) are Stage B/C.

## Pins

```
campaigns/G12_sensor_set/stage_a/reference_values.py   bc5db2c38b635f19
stdout                                                 d3e9e1ed1b5caf29  (byte-stable x2)
certified cross-route: gate_11 P3 triples + K_G;  A_c = 42793/1555848 (RC-4)
```
