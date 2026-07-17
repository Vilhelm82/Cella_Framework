# STAGE A PREDECL — L0 HARNESS REGRESSION GATE (campaign: THE ENGINE)
**Status: FROZEN at commit, pre-battery (no harness code exists at freeze time). Date 2026-07-03.**
**Authority:** brief §4 Stage A, activated S-2026-07-03 by Will's clearance ("Accept defaults, Go") — decision sheet v2 window closed, defaults V1–V3 stand; §8 rulings resolved on recommendations (name THE ENGINE; arms by pointer; Stage A pre-sheet YES). PA-1/2/3 (`80_PROCESS_AMENDMENTS.md`) in force. PA-3 gate: `90_HOUSEKEEPING.md` ACTIONABLE ledger EMPTY at stage start.

## 1. Object and regression law
`engine_harness.py` (E6/L0) = the factored certification scaffold: predecl-pin gate, clause-embedding gate, records-blob sha, dual-run orchestration, certificate-bundle emit — the pattern currently instantiated separately in the seven certified batteries. **Regression law (frozen in the brief, restated verbatim):** *the harness refactor must reproduce all existing certified record shas byte-identically — a refactor that moves a single verdict bit fails its own gate.*

## 2. Semantics pinned
- **"certified sha"** = the 16-hex value each battery internally computes as `sha256(blob)[:16]` over its canonical records blob and prints on the line `RECORDS_SHA256 <hex16>`. It is **NOT** the sha256 of any records file on disk (disk files are stdout captures; their file-hashes differ and are non-authoritative).
- **Invocation contract** (forced by the scripts' own code, not chosen): cwd = repo root; `python3 <script path>`; batteries self-manage `sys.path` and read their own frozen predecls by repo-root-relative paths, so their original runtime gates (predecl-pin assertions, clause-embedding assertions) fire unmodified. Harness env policy: inherit + `PYTHONHASHSEED=0` (the original ×2 certifications prove all seven outputs hash-order-independent, so this is a no-op on the seven and a determinism guarantee for future batteries).
- **Originals untouched** (inherits K-E1): the seven battery scripts are not edited, moved, or imported as modules. The harness runs them as subprocesses (the probe/referee separation is the process boundary). Factored primitives are exported for *future* batteries. [convention, recorded once]
- **Harness home:** `portfolio/campaigns/the_engine/stage_A/engine_harness.py` for the duration of the campaign. Promotion to a shared location is a post-closeout exercise (covenant #8) — "src-adjacent" in the brief is satisfied without touching `src/`.
- **PASS(B)** := run1.sha == run2.sha == certified(B), with the battery's frozen terminal verdict line printed and exit code 0 on both runs. Two runs = two independent subprocess invocations.

## 3. Frozen prediction clauses (verbatim; the harness embeds these exactly and refuses on drift)
PA.1: harness-run portfolio/campaigns/shape_witness/witness_battery.py prints RECORDS_SHA256 39bed5552c805f4d with terminal ALL_PASS and exit 0 on each of two independent runs.
PA.2: harness-run portfolio/campaigns/deficit_engine/wave0_battery.py prints RECORDS_SHA256 74720504dfd88af7 with terminal ALL_PASS and exit 0 on each of two independent runs.
PA.3: harness-run portfolio/campaigns/deficit_engine/rowb_mech_battery.py prints RECORDS_SHA256 cdee40ff26fb262c with terminal ALL_PASS and exit 0 on each of two independent runs.
PA.4: harness-run portfolio/campaigns/deficit_engine/realfiber_probe1.py prints RECORDS_SHA256 7b3b43058ffa0c7c with terminal ALL_PASS and exit 0 on each of two independent runs.
PA.5: harness-run portfolio/campaigns/deficit_engine/realfiber_probe2.py prints RECORDS_SHA256 848b8d8eca916edf with terminal line OUTCOME: INCONCLUSIVE-budget (runs at cap still descending) and exit 0 on each of two independent runs.
PA.6: harness-run portfolio/campaigns/deficit_engine/realfiber_path_cert.py prints RECORDS_SHA256 99fd1859a6e04214 with terminal ALL_PASS and exit 0 on each of two independent runs.
PA.7: harness-run portfolio/campaigns/deficit_engine/realfiber_fullfiber_cert.py prints RECORDS_SHA256 dfde6fbde06ee160 with terminal ALL_PASS and exit 0 on each of two independent runs.
PA.8: control — given expected sha 0000000000000000 for realfiber_path_cert.py, the harness verdict is REFUSE_MISMATCH and never PASS.
PA.9: control — given a predecl copy with any prediction clause byte-altered, the harness refuses with CLAUSE_DRIFT before running any battery.

Note on PA.5: probe-2's frozen grading is INCONCLUSIVE-budget per its own predecl rules; it is reproduced verbatim, never retyped (standing warning, session log S-2026-07-02 addendum 27). Its records sha carries the graded verdict inside the blob.

## 4. depends_on — content pins (Rule 1.9; sha256[:16] at freeze)
| artifact (read or graded-against at runtime) | sha256[:16] |
|---|---|
| portfolio/campaigns/shape_witness/witness_battery.py | abff00bd15d22c84 |
| evals/dbp_involution/rep_utils.py (witness import) | 0d838e5fd430461b |
| portfolio/campaigns/deficit_engine/wave0_battery.py | 4b845794e3c5ce0f |
| portfolio/campaigns/deficit_engine/rowb_mech_battery.py | de3edfe0b6162b69 |
| portfolio/campaigns/deficit_engine/realfiber_probe1.py | 7296597ea36cbddf |
| portfolio/campaigns/deficit_engine/realfiber_probe2.py | 5a8540458a7412af |
| portfolio/campaigns/deficit_engine/realfiber_path_cert.py | 18418b37ee78c949 |
| portfolio/campaigns/deficit_engine/realfiber_fullfiber_cert.py | 36601fb3abe717c2 |
| portfolio/campaigns/shape_witness/WITNESS_PREDECL.md (runtime-read) | 967c7909450ef944 |
| portfolio/campaigns/deficit_engine/WAVE0_PREDECL.md (runtime-read) | c6fd7018a4602209 |
| portfolio/campaigns/deficit_engine/ROWB_MECH_PREDECL.md (runtime-read) | 0c335fe2fa474d64 |
| portfolio/campaigns/deficit_engine/REALFIBER_PREDECL.md (runtime-read, probes 1+2) | 9f706c1a74a21317 |
| STAGEW_report.md (certified-constant provenance) | 331b4a34c2714f6f |
| WAVE0_REPORT.md (provenance) | 768de90c4a73923a |
| ROWB_MECH_REPORT.md (provenance) | 9a536866ab29a7e6 |
| REALFIBER_PROBE1_REPORT.md (provenance) | e861efa53efe9f0b |
| REALFIBER_PROBE2_REPORT.md (provenance) | 397dc9c98b19a3af |
| REALFIBER_THEOREM.md (provenance, fullfiber + path) | 9012084fb845fa70 |

Harness gate at runtime: recompute and verify every pin above before any battery runs; refuse on any mismatch (PIN_MISMATCH).

## 5. Referee
Mechanical string equality of the parsed `RECORDS_SHA256` line against the certified constants in §3. Constants' provenance = the pinned reports (§4). The harness never imports a battery as a module; truth is computed by the batteries' own frozen internal gates on an independent process path. role=probe on the harness side; the certificate bundle is the ledger.

## 6. Kill conditions (armed, typed)
- **K-A1 (halt-stage):** any of PA.1–PA.7 FAILs (sha mismatch, wrong terminal line, nonzero exit) → HALT Stage A, route to Will verbatim. The seven originals remain canonical; no engine code ships on a lossy refactor (= umbrella K-E1).
- **K-A2 (halt-stage):** run1.sha ≠ run2.sha on any battery (container nondeterminism) → HALT, diagnose before anything else runs.
- **K-A3 (halt-stage):** PA.8 or PA.9 FAILs (harness rubber-stamps a wrong sha or grades under clause drift) → HALT; the instrument is unfit regardless of PA.1–PA.7.
- No softening. A FAIL is reported verbatim; the prediction is never widened post-hoc.

## 7. Status-move rules
- PA.1–PA.9 all PASS ⟹ **CL-ENG1** (umbrella ledger) moves NOT_YET_PROBED → **CERTIFIED**, and auto-files CANONICAL iff the full PA-1 certificate class is met (predecl frozen+pinned pre-battery; clause embedding verified at runtime; controls green; byte-stable ×2; records sha banked; kills armed, un-fired).
- Any FAIL ⟹ CL-ENG1 stays NOT_YET_PROBED with the failure banked; kill chain per §6.

## 8. Economics pins
Per-battery wall-clock ceiling 20 min per run in-container (soft: breach = measure, report, route; no silent truncation). Total stage envelope: one session.

frozen: true · version: 1 · referee: mechanical (string equality vs §3 constants) · author: Claude-container · activation authority: Will, S-2026-07-03
