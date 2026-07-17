# Stage A — numerator-tower normalization (pinned, falsification-gated)

**Script:** `campaigns/G12_sensor_set/stage_a/normalization_pin.py` — byte-stable ×2,
stdout sha16 `7bf1b0c90d26cdb4`, exit 0, exact `Fraction`.

## Result

The numerator-tower channel is

```
kappa_r = e_r(P Hc P) / q^(r/2),    r = 2 .. n-1,   q = g.g,   Hc = offdiag(H)
```

It is the invariant of the surface under the physical recalibration `F -> t*F`, which
scales both `g = grad F -> t g` and `H = Hess F -> t H`: `e_r` scales as `t^r`, `q` as
`t^2`, so `q^(r/2)` scales as `t^r` and cancels. Confirmed n = 3, 4, 5.

## Gates (each fires if the underlying math is wrong)

- **G1 — F->tF invariance.** `e_r((tH)c) == t^r * e_r(Hc)` and `q(tg) == t^2 * q`
  exactly, `t = 2,3`, every fixture. => `kappa_r` invariant for all n, r. **PASS.**
- **G2 — cross-route to the certified bank.** keystone `kappa_2 = e_2/q = -1/49`
  (= certified `kc`, RC-4) and `K = e_2(P H P)/q = -3/49` (= certified `K_G`, RC-1).
  **PASS.**
- **G3 — parity-law consistency.** `kappa_r in Q` iff `r` even; `r` odd lands in
  `Q(sqrt q)` (q nonsquare). n=5: `r=2,4` rational, `r=3` carries `sqrt q` — matches
  the certified tower parity (A-003, even Q / odd Q(sqrt q)), falling out of the
  normalization rather than imposed. **PASS.**
- **G4 — control (must fire).** the naive `e_r/q` is `F->tF`-invariant only at `r=2`;
  at `n=4, r=3` it moves under scaling (ratio `t`). Confirms `/q` wholesale is wrong for
  `r != 2` and the gate catches it. **PASS (control behaves as designed).**

## Resolution of the -2/7 question

`-2/7` was `e_2(P Hc P)` with no normalization. The certified channel is
`kappa_2 = e_2/q = -1/49`. The general rule is `/q^(r/2)`, not `/q` — the earlier `/q`
was right only because `r=2` gives `r/2 = 1`. Parity is a consequence: odd rungs carry
`sqrt q`, even rungs are rational — the certified tower's split.

## Consequence for Stage B

The engine ships `kappa_r = e_r(P Hc P)/q^(r/2)`. Self-fault blindness (RC-6) and
coupling sensitivity are normalization-independent (properties of `P Hc P`), so they
carry over unchanged. Scale invariance is now correctly the `F->tF` invariance of
`kappa_r` — not the g-only invariance of raw `e_top`. Odd rungs live in `Q(sqrt q)`, so
the sensor tower uses the certified number tower (G0.3), already in place.

## Pins

```
campaigns/G12_sensor_set/stage_a/normalization_pin.py   f405524fe75ee2c2
stdout                                                  7bf1b0c90d26cdb4  (byte-stable x2)
certified cross-route: kc=-1/49, K_G=-3/49 (RC-1/RC-4)
```
