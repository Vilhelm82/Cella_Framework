# c001 · three_channel_kg — STAGE A REPORT

**Stage A — the retrodiction spine + Stage-0 controls (the campaign's gating stage).**
One scored battery, run end to end under the covenant.

- **Date:** 2026-06-23 (machine date).
- **Authority (binding, read first):** the frozen objects under `results/three_channel_kg/`
  (`manifest_v1.json`, `SCHEMA.md`, `FIXTURES.md`, `CLAIM_LEDGER.md`) — the three pinned objects
  verified byte-for-byte against `freeze_pins_sha256.json` (CLAIM_LEDGER intentionally unpinned, not
  expected in the pin file); the built+frozen bench under `src/lloyd_v4/evals/three_channel_kg/`
  (`schema`, `fixtures`, `probe`, `referee_total`, `referee_channel`, `oracle`) IMPORTED READ-ONLY by
  exact pinned file path and pinned in the prereg `depends_on`; the covenant embedded in the
  stage-runner's own agent definition; reserved-ruling dispositions R1/R2/R3. The
  `v4-campaign-discipline` skill was NOT loaded (orchestrator override; unavailable this session) —
  the frozen objects + covenant are the sole binding authority.
- **Scope (exactly this):** claims **CL-c1**, **CL-c2**; armed kills **K2, K3, K5, K6, K8, K9, K11**;
  preconditions **P-self-cert, P-frame**; fixtures **F1–F11, F13**. (NOT F12/F12a/F12b — Stage D.
  K1/K4/K7/K10 — other stages.)

## Pins & reproducibility

- **prereg pin** (`prereg_sha256.pin` = sha256 of the frozen `prereg.json`):
  `ecced952d202c140b54a69d9042f78120326dfbee4090dd3a17574dcb4dad628`
- **records sha256** (`records.jsonl`, 53 records):
  `53321e5c53dcd43294539120f1c5f1625b68b9e5489c023260b5b416bc917376`
- **Byte-stability:** the battery was run TWICE to `records.jsonl` and `records_run2.jsonl`; the two
  files are **byte-identical** (`cmp` exit 0; identical sha256). Records are deterministic sorted-keys
  JSON, exact-ℚ `frac:n/d` strings, no float/time/random.
- **Suite:** `pytest results/three_channel_kg/stage_a/test_stage_a.py` → **17 passed, exit code 0**.
  The suite proves the gates BITE (clause-drift, bench-pin-drift, prereg-pin-mismatch all refuse) and
  carries mutation guards that prove a lying engine would be caught (wrong tuple fails P1; broken
  partition fails P3/K2; a non-flipping mutant is not falsely flagged as inverting in P5; nonzero on
  F9 fails P6; a near-miss is rejected by exact equality while a 1e-6 tolerance band would wrongly
  pass it, P8; a numeric-0-on-q=0 lie is caught by P9; a corrupted partition formula leaves nonzero
  residual, P12).

### Pin verification (frozen authority + bench)

| Object | sha256 | matches |
|---|---|---|
| `manifest_v1.json` | `a28042d9…` | freeze_pins ✓ |
| `SCHEMA.md` | `fe0eb353…` | freeze_pins ✓ |
| `FIXTURES.md` | `3d933e39…` | freeze_pins ✓ |
| `probe.py` | `1f999658…` | known-good ✓ |
| `schema.py` | `40335dc1…` | known-good ✓ |
| `fixtures.py` | `3d415011…` | known-good ✓ |
| `referee_total.py` | `993ffd21…` | known-good ✓ |
| `referee_channel.py` | `28eff76c…` | known-good ✓ |
| `oracle.py` | `b8af9397…` | known-good ✓ |

No pin mismatch on any pinned object.

## Verdicts table (13 predictions, exact ℚ, no tolerance)

| ID | Prediction (claim / kill) | Units | Result |
|---|---|---|---|
| P1 | All `{F1..F11}` rows pass all 5 closure identities (CL-c1, CL-c2; K2/K3/K5) | rows passing /11 | **PASS** (11/11) |
| P2 | Keystone F8: `q=14`, `det(H_b)=12`, tuple `(−3/49,−1/49,1/49,−3/49)` on A/B/B′/C; `K_G<0` (CL-c1, CL-c2) | exact ℚ per component | **PASS** |
| P3 | K2 partition silent: `det(H_b)−(Δ_c+Δ_s+Δ_m)=0` on Path A all 11; Path-A det = Path-B det (CL-c1; K2) | exact ℚ residual = 0/1 | **PASS** |
| P4 | K3 two-derivation: Path-A channels = Path-B′ channels all 11; κ_s-mirror mutant DIFFERS from truth on trap F5/F6/F8 (CL-c2; K3) | exact ℚ; A==B′ + mutant≠truth | **PASS** |
| P5 | K5 wrong-sign: true K_G sign matches oracle on F3/F7/F8; sign-flip mutant inverts the sign (object integrity; K5) | exact ℚ sign | **PASS** |
| P6 | K6 rank-heuristic: F9 developable cone `K_G=0` exactly on A/B/B′/C, never nonzero (CL-c1, CL-c2; K6) | exact ℚ = 0/1 | **PASS** |
| P7 | K8 √q-leak: all emitted values are `Fraction` on all 11; a float operand at the door raises `TypeError` (type gate; K8) | isinstance Fraction; refusal-on-float | **PASS** |
| P8 | K9 tolerance-leak: an injected `+1/10⁹` near-miss on F8 makes row-pass FALSE (no tolerance band) (type gate; K9) | boolean (must be FALSE) | **PASS** |
| P9 | K11 singular-lie: genuine `q=0` (g=(0,0,0)) → typed REFUSED on A/B/B′; F6 single `g_i=0` (q=4) → `K_G=1`, no refusal (refuse-not-lie; K11) | typed-exception predicate | **PASS** |
| P10 | Preconditions: P-self-cert (oracle imports none of A/B/B′/fixtures, and vice-versa) + P-frame (every channel fixture carries a frame) | boolean | **PASS** |
| P11 | Both-sign witnesses: F6 `K_G=+1>0`, F8 `K_G=−3/49<0`, F10 `κ_int=−1/9<0`, F11 `κ_int=+2/9>0` (CL-c1 signed) | exact ℚ sign | **PASS** |
| P12 | CL-c1 **universal** warrant (R1): `det(H_b)−(Δ_c+Δ_s+Δ_m)=0` as a polynomial in ℚ[g,H] (0 residual monomials; 12 det / 12 partition monomials; pairwise-disjoint supports whose union = det support) | residual-monomial count = 0; etc. | **PASS** |
| P13 | F13 parity contrast: `σ₂=−3/49` (=F8 K_G), `Ĉ₁=−24` exact-ℚ; `σ₁∈ℚ(√14)` NOT emitted numerically (CL-c1) | exact ℚ + field-label | **PASS** |

**Predictions: 13/13 PASS. Kills fired: NONE. Preconditions: hold (run NOT void).**

## Headline

The signed three-channel `K_G = κ_c + κ_s + κ_int` retrodicts the entire frozen Stage-A family
exact-ℚ across four code-disjoint paths (Path A monomial read-off, Path B `−det(H_b)/q²` Bareiss
total, Path B′ split-shape-operator channels, Path C frozen external oracle) with the keystone
F8 pinned (`q=14`, `det(H_b)=12`, `(−3/49,−1/49,1/49,−3/49)`), the sphere F6 at `+1`, the developable
cone F9 at exactly `0`, both signs of `κ_int` witnessed (F10/F11), and — decisively for the CL-c1
universal warrant under R1 — the partition identity established as a **symbolic polynomial identity
over ℚ[g,H]** (the cofactor-expanded `det(H_b)` minus `Δ_c+Δ_s+Δ_m` is the zero polynomial;
exhaustive & disjoint monomial supports), not finite agreement alone. Every armed kill stayed silent
on truth and was shown to fire on a constructed mutant (κ_s-mirror → K3; sign-flip → K5;
near-miss → K9; numeric-0-on-q=0 → K11). Zero defect chains.

## Proposed status moves (eval-tier; nothing canonical until Will signs off)

- **CL-c1: `NOT_YET_PROBED → DEMONSTRATED`.** Gating predictions P1, P2, P3, P11, P12, P13 all PASS.
  R1 is satisfied as a **universal** warrant: the symbolic identity over ℚ[g,H] (P12) is established
  rigorously — NOT downgraded to a finite-only warrant — with the finite family (P1/P2/P3/P11/P13) as
  corroboration. Warrant scope: `det(H_b)=Δ_c+Δ_s+Δ_m ⟹ K_G=κ_c+κ_s+κ_int`, exhaustive & disjoint,
  for every regular jet (q≠0). Eval-tier; no substrate promotion.
- **CL-c2: `NOT_YET_PROBED → DEMONSTRATED`.** Gating predictions P1, P2, P4 all PASS. CL-c2 is NOT an
  R1 universal claim; it is graded per its ledger statement — the two disjoint channel derivations
  (Path A monomial vs Path B′ split-shape-operator) agree channel-for-channel across the frozen
  Stage-A family `{F1..F11}`, K3 silent, and the **non-mirror** κ_s is established (the naive κ_s-mirror
  mutant is rejected by K3 on the trap set F5/F6/F8). Warrant scope: the frozen family (finite, exact
  ℚ), NOT a symbolic-over-ℚ[g,H] universal. Eval-tier; no substrate promotion.

These are PROPOSED moves for Will/the merge-packager. The shared `CLAIM_LEDGER.md` was NOT touched;
the ledger close block is in `stage_a/ledger_close_block.md` for the merge-packager to append.

## Defect-chain count

**0 (NONE).** No prediction FAILed; no kill fired; no HALT; preconditions hold (run not void). The
records, the suite, and the two-run byte-stability are all clean.

## Will's desk

- **The CL-c1 universal warrant is real, not asserted.** P12 is a deterministic, complete
  polynomial-identity proof over ℚ[g₁,g₂,g₃,h₁₁,…,h₃₃] (the residual is the empty polynomial — 0
  monomials), built by the battery's own exact-ℚ multivariate engine re-deriving the probe's
  partition formulas. It is NOT Schwartz–Zippel sampling and NOT finite-fixture agreement. If you want
  the warrant phrased more conservatively (e.g. "DEMONSTRATED on the family + symbolic identity over
  ℚ[g,H]" rather than a bare universal), the move text is yours to set — the evidence supports the
  universal reading under R1 as written.
- **K11 frozen-spec tension was acted upon, as instructed — flagging for your awareness, not as a
  defect.** The manifest `stage0_controls.singular_refusal` and `SCHEMA.md` list "`g_i=0`" among
  singular strata, yet frozen fixture **F6** (sphere at `(3/5,4/5,0)`, `g=(6/5,8/5,0)`, `g₃=0`, `q=4≠0`)
  is a `+`-sign witness that MUST give `K_G=1`. The probe's forced reading (genuine stratum = `q=gᵀg=0`;
  a single zero gradient component at a regular point computes normally) was honored: K11 is exercised
  with a genuine `q=0` jet `g=(0,0,0)` (typed REFUSED on all three paths), and F6 evaluates to `K_G=1`
  with no refusal. No spurious K11 FAIL. If you ever want the manifest text tightened to read
  "`q=gᵀg=0` / cone apex" instead of "`g_i=0`", that is a frozen-spec edit for Records, out of stage
  scope.
- **One out-of-scope arithmetic note (NOT graded; NOT a halt) — to be PINNED in the Stage-B/K1 prereg.**
  The manifest `stage0_controls` K1-proxy annotation says `kappa^2=9/2401`. Resolved: **`9/2401` is
  `K_G² = (−3/49)²`** — the squared *total*, a legitimate sign-blind proxy. It is **NOT** the
  channel-norm `κ_c²+κ_s²+κ_int² = ((−1)²+1²+(−3)²)/49² = 11/2401`. Those are two *different*
  sign-blind proxies; the manifest's value is the squared total, not the channel-norm. K1 and its
  proxies are **out of Stage-A scope** (K1 belongs to Stage B), so this touches no graded Stage-A
  prediction — surfaced (and to be pinned as a note in the Stage-B prereg) so the K1 stage-runner does
  **not** transcribe `9/2401` as a channel-norm. Either way the K1 *intent* holds: each such proxy is
  `≥0` and differs from the signed `K_G=−3/49`, so none can represent the signed object.
- **Worktree/bench topology note — RESOLVED by the post-gate reproducibility retrofit.** This stage
  ran in worktree `agent-a327d51553a3e8a26`, whose tree predates the bench integration; the bench is
  committed+frozen on `main` with the exact known-good shas, imported READ-ONLY by exact file path
  (shadow-proof against the worktree's own bench-less `src/lloyd_v4`) and sha-pinned in `depends_on`.
  The first cut of `battery.py` baked the ephemeral worktree path into its prereg/results constants;
  **post-gate, `battery.py` was retrofitted to derive ALL paths from `__file__`** (STAGE = its own
  directory; repo root three levels up; bench under the repo's `src/`). The grader now re-runs from
  `main` with no worktree dependency — re-verified on `main`: same `records sha256` `53321e5c…`,
  **13/13 PASS**, suite **17 passed, exit 0**, all three gates (prereg-pin, clause, bench-pin) green.
  The retrofit is **path-only** (records content is path-independent), so the frozen `prereg.json`
  (pin `ecced952…`) and the `depends_on` bench shas are untouched. All Stage-A outputs remain only
  inside `results/three_channel_kg/stage_a/`. The merge-packager consolidates.

---

*Stage A graded against the frozen `prereg.json` (pin `ecced952…`). Exact ℚ, no tolerance. Eval-tier
only; geometry spine fence stays CLOSED; no substrate promotion; nothing canonical until Will signs
off.*
