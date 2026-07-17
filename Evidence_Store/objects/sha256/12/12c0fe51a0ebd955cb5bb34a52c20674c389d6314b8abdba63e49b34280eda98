# Shape of the Quiet — Fixture Manifest (v1, FROZEN)

**Frozen:** YES — approved at Will's audit 2026-06-10. `sha256` pin: `9a1d7ec63e46d6418e4f8cd8992dd4b3bd7ba96df08cef760cfd7fe57772ef23` (`manifest_sha256.pin`). Audit rulings applied: F1(b) interpretation confirmed + form-borne scope note (readability of a representation-layer invariant, not emergent geometry); F2c sin control family added to the frozen sweep with per-rung argument-reduction offsets recorded; tolerances approved; F2 claim regime k ≥ 7 approved; raw per-rung errors always recorded. Any byte change to `manifest.json` from here on is refused by `require_frozen_manifest()` and requires re-audit.

This file is a *rendering* of `manifest.json` for audit. The JSON is the authoritative object; its byte-hash is what gets pinned.

---

## The ladder, in one paragraph

Each fixture walks a log proximity ladder toward its singular locus (15–16 decades). At every rung, four readings: **I1** naive float64, **I2** V3 oracle via the committed MCP stdio client (server v1.27.0, pinned binary), **I3** the V4 typed probe, **arbiter** mpmath (50 dps, raised +10 until self-consistent; referees the *exact binary* operating point, never the decimal nominal). Per rung we record value, validity self-report, and I3's raw attribution channel. "Trustworthy" = within pre-registered tol of the arbiter AND self-reports valid. Headline figure: trustworthy-depth vs proximity per instrument per fixture.

## Fixtures

| | F1 — Schwarzschild deep approach (A6) | F2 — Blowup-exponent family (A4) | F3 — Kerr extremal (A9) |
|---|---|---|---|
| Surface / loci | `1 - 2/r - z*z` (M=1), extended past the r=2.1 stop of `v3_calibration_fixtures/` | the 15 frozen zeros of ζ, J₀, Ai from `blowup_exponent_v4_audit/artifact.json` | **DEFERRED** — needs your Kerr surface form; manifest v2 re-freeze required |
| Ladder | δ = r−2, rungs 10⁰…10⁻¹⁵; r_k = fl64(2+10⁻ᵏ); effective δ recorded (exact by Sterbenz) | d = x−x₀ from above, rungs 10⁰…10⁻¹⁴; 5-point geometric window {d·2ʲ} per rung | — |
| Quantity (a) | curve curvature κ(δ), closed form from z(r) | per-rung σ1 (log-log slope over the window) | — |
| Quantity (b) | the −2 Hessian eigenvalue, M-variable surface `1 - 2*M/r - z*z` | — | — |
| tol | κ: 1e-3 relative (I3 method floor is 4.7e-4, HR129) · eig: 1e-9 absolute (truth is exactly −2) | 0.01 absolute on σ1 (method gap ≤ 0.0033, ledger retest B) | — |

## Instrument wiring (the load-bearing details)

- **I3 vocabulary = the G2 ≡ S2 jet (your ruling 1).** F1(a): κ reconstructed multivariately from (S0,S1,S2) via the Phase A `reconstruct_kappa_from_substrate`, FD steps under the Phase A operand-variation guard — guard fire ⇒ typed FD-unresolved refusal, never an estimate. F1(b): the Hessian z-block is exactly [−2] and decouples analytically, so I3 reads it with the existing `typed_finite_difference` — **no eigensolve primitive is built** (DP4 gap-stop pre-declared if full-spectrum attribution is ever needed). F2: `typed_log_log_slope` + alpha-probe companion (existing, audit-grade).
- **I2 for F2 is structurally refused.** Probed 2026-06-10: the V3 compiler allowlist accepts sqrt/sin/exp/log/arithmetic and **rejects `zeta` and `besselj0`**. Recorded per rung as `oracle_inexpressible` — a first-class result (V3's boundary on this family is expressibility, not noise). The F2 depth comparison is honestly I3-vs-I1 with the refusal stated.
- **Attribution (your ruling 2), fully pre-registered:** raw channels per rung (phenomenon / substrate / ambiguous / format_precision_pinned; glossary thresholds). Arbiter ground class per rung from the exact 1-ulp input transfer Δq_ulp: resolvable (≤ tol·|q|) / rounding-dominated (> |q|) / indeterminate. `format_precision_pinned` maps to substrate-family, recorded distinctly. Campaign verdict (incl. **contaminated**) is a mechanical rule over those sets — thresholds 0.9 / 90% frozen in the JSON. Nothing assembled post-hoc.
- **E at depth (your ruling 3):** E-unsafe flag recorded per rung; arbiter classification is authoritative in that regime.

## Questions for your audit (the manifest freezes after these)

1. **F1(b) interpretation.** I read the A6 "universal −2 eigenvalue" as the analytically-decoupled z-block Hessian eigenvalue of the constraint form (exactly −2 at every point by construction). Confirm or correct — this defines what the instruments are graded on.
2. **F2c control family (optional).** Add sin zeros at π, 2π, 3π — the one simple-zero family V3 *can* express — so F2's I2 column isn't structurally empty? 3 loci, same ladder. Your call; excluded unless approved.
3. **Tolerances** (table above) — approve or adjust.
4. **F2 claim regime** pinned at k ≥ 7 (deep half) for the campaign-verdict rule — approve or adjust.
5. **Dependency hygiene:** I3's F1 wiring imports the Phase A fd-metrology module, which is currently **untracked** in the worktree (along with the Phase A closeout + receipt). It needs to be committed before any sweep — authorize me to commit those prior-session files, or commit them yourself.

## Freeze procedure (on your approval)

1. Apply any audit edits to `manifest.json`; set `frozen: true` + `date_approved`.
2. Write `sha256(manifest.json)` to `manifest_sha256.pin` (one line).
3. `tests/test_quiet_manifest_frozen.py` goes green; the sweep gate opens.
