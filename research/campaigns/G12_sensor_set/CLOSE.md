# G1.2 — the sensor set — CLOSED

**`tests/gate_12.py`: CLOSED, byte-stable ×2 (stdout `adf6316f`); full Layer-0/1
suite (gate_zero..04, 10, 11, 12) green ×2.** Delivered `src/cella/sensors.py` — four
sensors, generic-n where scoped, certified against the Stage-0 recerts and Stage-A pins.

## What closed

- **Numerator tower** `kappa_r = e_r(P Hc P)/q^(r/2)`, r=2..n-1, parity-typed (even ℚ,
  odd ℚ(√q)): `kappa_2 == certified kc` (an identity, holds even under gauge); exact
  self-fault blindness (factor-through-Hc); F→tF scale-invariant (even rungs exact, odd
  rungs at value level b²·r); computes on component-zero gradients (P-route).
- **Shape moment**: S_n-isotypic norms of the carrier O; the `(n-2,2)` shape component
  is absent at n=3 (0) and present at n=4; O-based, so it inherits the chart refusal.
- **Localization**: triangle channels + support theorem `{S: dDelta_S≠0} == {S ⊇ e*}`
  exact, with the moved-support family tracking the fault edge.
- **Fingerprint** (n=3-fenced, A-008): `A_c(keystone) = 42793/1555848`, faithfulness
  `det = 8·L_P·L_D·L_S/q0⁶`; both strata — `CHANNEL_ISOTROPIC` (a Λ=0, names the channel)
  and `ROLE_CHART_UNAVAILABLE` (component-zero gradient); `n != 3` is an API-contract
  ValueError.
- **`CHANNEL_ISOTROPIC` admitted (A-010)**: closed vocabulary 7 → 8; `gate_04` count
  assertion updated, its stdout pin `3775a7fb` **invariant** (count lives in the
  assertion — P9); `gate_10` count assertion updated (re-pinned `372a7f54`, message-only).
- **Four mutants bite**: ratio-sensor reimplementation (numerator self-fault dominance),
  label-swap (slot-label case law), single-scalar flatten (the Goldman guard), isotropic
  mistype (fingerprint refuses where a computing mutant would return a value).

## Correction banked (kept in the record)

The numerator tower is the **coupling channel kc**: self-fault-blind and F→tF
scale-invariant, but **gauge-covariant** (a chart-dependent channel — the gauge-invariants
are `A_c` and `K_G`, not individual `kc`). A first gate_12 draft wrongly tested the
numerator for gauge *invariance*; corrected to the coupling-channel identity `kappa_2 ==
kc` (which the data shows holds identically, including under gauge — so the Stage-A
identity was right, not representative luck). The brief's numerator claims (coupling
sensitivity, self-fault blindness, scale invariance) never included gauge invariance.

## Status moves

- **A-007** G1.2 obligation (each sensor enters with reference values + blindness) —
  DISCHARGED. **A-008** G1.2 fingerprint obligation — DISCHARGED. **A-010** — ESTABLISHED,
  wiring certified.
- Scope, stated exactly: mathematical dominance on the regular locus at declared
  order/degree per sensor. Empirical dominance (G3.1/G3.2) and global completeness
  (A-007 successor) remain OPEN.

## Pins

```
src/cella/sensors.py  ·  tests/gate_12.py  (stdout adf6316f, byte-stable x2)
suite gate_zero..04,10,11,12 green x2   ·   gate_04 3775a7fb (invariant)  ·  gate_10 372a7f54
```
