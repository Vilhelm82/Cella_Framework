# PREREG_AMENDMENT_001 — Campaign A (Channel-Spectrum Carrier Atlas)

**Status:** ACCEPTED, pre-emission (recorded before any canonical output file was generated)
**Amendment type:** schema / fixture-hardening only
**Effect on mathematical claims:** NONE. CL-A1 … CL-A6 and KC-A1 … KC-A7 are unchanged.
**Recorded:** 2026-06-27, during the build phase, immediately after the exact
arithmetic core (`rational.py`, `determinants.py`) was completed and before the
carrier, serialization, fixture, or report layers were written.

This amendment is issued by Will and entered here verbatim-in-substance rather
than applied as a silent edit, per the campaign's append-only discipline.

---

## A1.1 — Canonical rational serialization

The canonical rational serialization for this campaign is the structured pair

```json
{"num": n, "den": d}
```

with `n/d` always reduced (`gcd(|n|, d) = 1`, `d > 0`).

The existing repo-style `"frac:n/d"` strings (used by `three_channel_kg` and
sibling campaigns) **may appear only as auxiliary display fields or console
text, never as a canonical value** in `records.jsonl`, `summary.json`, or any
hashed/graded artifact.

> Note on divergence: this is a deliberate, recorded divergence from the
> prevailing repo `"frac:n/d"` convention. It is confined to Campaign A and
> does not interoperate with `three_channel_kg` records.

## A1.2 — Hand-pinned independent keystone truth

The keystone fixture `n3_keystone_interaction_survives`
(`F = x₁² + x₁x₂ + x₃² − 3` at `x = (1,1,1)`, giving `g = (3,1,2)`,
`H = [[2,1,0],[1,0,0],[0,0,2]]`) MUST carry hand-pinned independent truth
values. These values are frozen **literal constants**, derived by hand
(cofactor expansion) and not produced by the channel-density implementation
under test:

| quantity | value |
|---|---|
| `q` | `14` |
| `Ĉ₁` (density coeffs) | `{(1,0): 6, (0,1): -30}` |
| `Ĉ₁(1,1)` | `-24` |
| `Ĉ₂` (density coeffs) | `{(2,0): -4, (1,1): -12, (0,2): 4}` |
| `Ĉ₂(1,1)` | `-12` |
| `kappa_c`  (r=2, normalized) | `-1/49` |
| `kappa_int`(r=2, normalized) | `-3/49` |
| `kappa_s`  (r=2, normalized) | `1/49` |
| `K_G` (r=2 reduced) | `-3/49` |

The campaign test suite asserts the implementation reproduces these literals.
A change to the implementation that fails to reproduce them is a KC-A1 kill,
not a fixture update.

## A1.3 — Named channel fields in canonical reports

Canonical reports and machine-readable artifacts MUST use **named channel
fields** — `kappa_c`, `kappa_int`, `kappa_s` (and density coefficients keyed by
their exponent pair `(p,q)`) — never bare positional tuples for the named
three-channel decomposition. Positional tuple order may appear **only** in
human-readable notes, and only when the ordering is explicitly labelled.

For `n=3`, `r=2` the canonical name map is:

| density coeff key | normalized name |
|---|---|
| `(2,0)` (pure coupling) | `kappa_c` |
| `(1,1)` (interaction)   | `kappa_int` |
| `(0,2)` (pure self)     | `kappa_s` |

## A1.4 — Predating-files disclosure / v2 rule

At the time this amendment was recorded, **no canonical output file had been
emitted**: only the package scaffold (`__init__.py`), the exact arithmetic core
(`rational.py`, `determinants.py`), and one foundation test module existed.
There are therefore **no generated `records.jsonl` / `summary.json` / report
files predating this amendment** to preserve.

If any final report had already been emitted, it would be kept and the campaign
re-run as `v2` rather than overwritten. This rule remains armed for the
remainder of the campaign: a canonical artifact, once emitted, is not silently
overwritten — it is superseded by a versioned re-run.

---

*Tracked in `MANIFEST.md`. This file is append-only; further amendments are
`PREREG_AMENDMENT_002.md`, etc.*
