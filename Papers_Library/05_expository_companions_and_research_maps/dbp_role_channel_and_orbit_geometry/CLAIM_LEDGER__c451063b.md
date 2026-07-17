# CLAIM LEDGER — Campaign A: Channel-Spectrum Carrier Atlas

Eval-tier. Verdicts are graded by `run_campaign_a.py` and re-checked by `verify_campaign_a.py`.
Machine-readable mirror: `summary.json` → `claims`. Nothing here is canonical until Will signs off.

Status vocabulary: **PASS** / **FAIL** / **SCOPED-NO-WITNESS**.

| Claim | Statement | Verdict | Evidence |
|---|---|---|---|
| **CL-A1** | density reduction exact: Σ_{p+q=r} κ̂_{r;p,q} = Ĉ_r(1,1), all fixtures, all r | **PASS** | 19 fixtures; left side via Vandermonde, right side via direct (1,1) eval — independent routes agree; also checked off-axis at (3/4,-2) |
| **CL-A2** | passive covariance / triviality: reduced tower and unordered carrier fingerprint invariant under all coordinate permutations | **PASS** | all S_n permutations (n=3: 6, n=4: 24) per fixture; fingerprint and tower invariant |
| **CL-A3** | gauge zero-sum residue: H→H+ga^T+ag^T preserves reduced tower; per-r channel shifts sum to zero | **PASS** | default gauge set per fixture + keystone gauges (1,0,0),(0,1,0),(1,-2,3),(-1/2,5,1); reduced preserved, residue zero-sum, channels genuinely move |
| **CL-A4** | exactness & parity discipline: every density coefficient rational; odd-order normalized curvature marked Q(√q) unless q is a perfect square | **PASS** | no float ever emitted (canonical encoder refuses float); odd-order non-square normalizations quarantined as `Q(sqrt q)` (e.g. keystone σ₁ ∈ Q(√14)) |
| **CL-A5** | carrier separation candidates: an exact pair with same reduced tower, different channel carrier, passive-excluded | **PASS** | frozen bounds n=3, g∈{(1,1,1),(1,2,3),(2,-1,1)}, entries {-2..2}, skip H=0; **46 872 scanned, 5 298 separation groups**; gauge status **unknown** → candidates, **not** a theorem |
| **CL-A6** | n=4 interaction-order split K_{2,1} ≠ K_{1,2} | **PASS** | frozen bounds n=4, entries {-1,0,1}; witness found: g=(1,1,1,1), all-(-1) coupling incl. diagonal → K_{2,1}=12 ≠ K_{1,2}=-12; recorded as **witness**, not theorem |

## Armed kill conditions — all silent on truth, all proven to fire on mutants

| Kill | Fires when | Status this run | Mutant that fires it |
|---|---|---|---|
| KC-A1 | Σ κ̂ ≠ Ĉ_r(1,1) | silent | `mutant_channel_vector_drop_mixed` |
| KC-A2 | gauge changes Ĉ_r(1,1) | silent | (gauge invariance held on all fixtures) |
| KC-A3 | passive permutation changes fingerprint | silent | `mutant_label_sensitive_fingerprint` |
| KC-A4 | a coefficient not exactly rational | silent | `mutant_normalize_float` (refused by encoder) |
| KC-A5 | odd-order normalized emitted rational w/o square check | silent | `mutant_normalize_float` |
| KC-A6 | raw ZeroDivisionError / nan / inf in graded path | silent | (Vandermonde nodes distinct; q≠0 fixtures) |
| KC-A7 | passive permutation claimed as active recharting | silent | `mutant_label_sensitive_fingerprint` vs trivial canonical orbit |

**Kills fired this run: NONE.** Mutation controls (`tests/test_channel_spectrum_carrier_mutants.py`) prove each check is non-tautological — see `MUTATION_REPORT.md`.

## Discipline
Exact ℚ, no tolerance; stdlib only; eval-tier only; no substrate package modified; two-run byte-identical outputs (verified). **PENDING Will's sign-off.**

## Honest scope notes (do not over-read)
- CL-A5 establishes the carrier distinguishes pairs the reduced tower collapses, **passive-excluded**. It does **not** establish the carrier is a new invariant: gauge equivalence is unresolved, so some or all candidates may be gauge-residual. See `ATLAS_SUMMARY.md`.
- CL-A6 is a single witness that interaction order is asymmetric; it is not a structural theorem about K_{2,1}/K_{1,2}.
