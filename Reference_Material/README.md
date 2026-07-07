# Reference_Material — currency banner (read before citing anything here)

**Standing rule (README rule 3 / BOOT mechanism section):** everything in this folder
is origin-program material. Statuses inside these documents — "proven", "certified",
"[EVAL]", "standing", "closed" — are **claims, never evidence**. Nothing here bears
load in Cella until re-proven in-repo (`verification/`, fresh code, exact ℚ,
byte-stable ×2). This folder exists to name questions and retrodiction targets, not
truths.

**Tracking policy (CORRECTED — Will, 2026-07-07; supersedes "deliberately untracked"):**
the folder's contents ARE tracked. Reference docs must persist across ephemeral
container resets — the old "untracked for zero-import hygiene" policy conflated two
different things and cost real work: it lost the docs on every reset and stalled
sessions waiting for manual re-uploads. **Zero-import (README rule 1) governs the
BUILD** (`src/`, `tests/`, `verification/` must be standalone, must not copy origin
code/results). It does NOT govern *storing reference material* — the papers you
re-verify *against*. What fences these as "claims, not evidence" is **this banner + the
re-verification rule (rule 3)**, not their absence from git. Committing a reference PDF
imports nothing into the build. Do NOT re-gitignore this folder. (An ADMISSIONS record
is still required to introduce something into the BUILD as a dependency — that is a
separate act from tracking a doc for reference.)

**Currently tracked (surfaced by Will):** `gtd_vs_dbp.pdf` (GTD-vs-DBP paper, RC-5/LEAD-7
source), `dbp_four_role_calc_log_v8.md` (the diary, latest; absent from V4),
`DBP_STANDING_RESULTS_v1.1.md` (CANONICAL; the once-uploaded v1.0 is stale),
`DBP_Curvature_Constants_Corrected_Formulation.md` (arithmetic-track, n=3 elliptic).

## Substrate warning

`DBP STANDING RESULTS.md` marks its own certification substrates. Note carefully:
Part IV (the depth theorem), Parts V.1–V.3 (the arithmetic track), and the n=4
two-state witness (I.6, CALC-30) are **[CONTAINER]** — ephemeral scripts, never
persisted. For these there is no artifact to re-run anywhere: re-verification means
re-derivation from scratch. The dimension threshold (Part III, CALC-26/27) has no
in-repo certificate either.

The two R&D briefs (`DBP_RnD_Directions_*.md`) grade their priority boards in this
dashboard's currency ("done", "settled", "retired"). Read them for questions and
campaign shapes only; their status labels have zero evidentiary weight here.

## Artifact audit against the FULL Lloyd_Engine_V4 tree (2026-07-06, late)

The V4 root became reachable only at the end of 2026-07-06 (mount was nested at
`DBP Engine Dev` all day — see BOOT runbook). Full-tree audit of the substrate
claims, so nothing above rests on an unchecked map:

- **CONFIRMED ABSENT (re-derivation, not re-run):** depth-theorem scripts
  (`f1_*.py`, CALC-31..35), arithmetic-landscape scripts (`ladder.py`,
  `h2_walls.py`, `mono_galois.py`, `trap_*.py`), the CALC-30 two-state witness
  script, any CALC-26/27 (dimension threshold) script, and the
  `dbp_four_role_calc_log` diary itself (only its drift ledger survives, in
  `_audit/`). Searched: tree + `_attic/*.zip` + `scratch/`.
- **DEGRADED (worse than the map claimed):** `evals/constant_hunt/` — the
  substrate map's [EVAL] tier for the total-curvature constant — now holds
  BYTECODE ONLY (`__pycache__/*.cpython-314.pyc`; sources gone). Even the
  "persistent evals" tier rots. The constant itself is unaffected here: it is
  independently certified in-repo (closed-form retrodiction + the Cohn-Vossen
  −2L route, `reports/arithmetic_track/`).
- **CONFIRMED PRESENT (retrodiction-grade, copied to `old_program_sources/`):**
  `evals/dbp_involution/` with sources incl. the independent Specht referee
  (`rep_utils.py`); the ENG2 fault-semantics campaign (numerator tower +
  triangle localization, with frozen fixtures and sha pins); the shape_witness
  campaign records; `portfolio/10_DBP_STANDING_RESULTS.md` (diff against this
  folder's copy before first citation — possibly newer).
- **NAME-COLLISION WARNING:** V4 reuses names across program eras —
  `f1_f2_natural_phase` (float formats) is NOT the depth-theorem `f1_*`;
  `results/bigraded_jet` (rounding jets) is NOT the κ bigraded grid. Use
  `old_program_sources/30_GLOSSARY_DISAMBIGUATION.md` before trusting any name.

### constant_hunt forensics (2026-07-06, late — "what happened to the work")

Cause established: the constant_hunt sources were **never committed** (unlike
`dbp_involution`, which was — commit `c31c8a9`); they lived untracked and were
deleted 2026-07-02 ~21:28 during the `Build_Docs/reference` reorganization sweep
(directory mtime; not moved — full-tree name search empty; `__pycache__` left
behind). The old program's own history thus contains the bank-everything lesson:
untracked working files do not survive reorganizations.

Content recovered from bytecode (unmarshalled, not executed; copies in
`old_program_sources/constant_hunt_bytecode/`):

- `dbp_total_curvature`: **the origin program had the boundary route** —
  `compute_gauss_curve_certificate`, "the boundary Gauss-curve geodesic
  curvature certificate" for the asymptotic-cone normal curve
  `C_+(φ) = (2cosφ, cosφ−1, 2sinφ)/L, L² = cos²φ − 2cosφ + 5`, in the same
  (1±√2)/2 eigenframe. This independently CORROBORATES the −2L Cohn-Vossen
  reduction found blind in `reports/arithmetic_track/ADDENDUM_2026-07-06`
  and likely names the third of [SR]'s "three independent routes."
  **ARITH-I Stage A gains an origin retrodiction target** (the C_+ curve pins).
- `alt_scalar`: the Stage-A flag ladder — per-flag r=2 coupling-density
  numerator `−Λ_{k,{i,j}}²`, `Λ = (−x_ij + x_ik + x_jk)/2` on pair carriers.
- `run_constant_hunt`: prereg-generating runner ("NO-DECIMAL-WORSHIP" bench);
  note its `elliptic_modulus_probe` used m = (√2−1)² = 3−2√2 as a
  "provisional, user-supplied lead" — NOT the certified modulus (2−√2)/4.
  Treat any m = 3−2√2 residue in origin notes as the provisional lead, not
  the identification.

Also recovered from the same July-2 sweep's destination:
`old_program_sources/{gauge_channel_transport_probe, theorem_8_1_curvature_
orbit_probe, theorem_8_1_role_jet_probe}.py` — runnable origin probes that
never made it into this folder's original doc copies.

### Full-tree loss audit (2026-07-06, final tally)

Method: pycache-orphan sweep (67 orphans) classified against git history
(incl. `--all` and 6 dangling commits), tree duplicates, and `_attic` zip
indexes. Basename-level matching — a "recoverable" copy is not guaranteed
byte-identical to what was deleted.

- **Committed git history: fully intact.** Nothing was ever lost FROM git.
  Six dangling commits exist (five c001-era WIP stashes of June 23, one
  pre-sync backup of 2026-07-02 21:28 that captured tracked files only).
- **58 of 67 orphans recoverable** (tracked deletions, duplicate dirs, or
  `_attic` zips).
- **9 files TRULY LOST from the untracked layer** — all with surviving
  bytecode (that is how they were detected): the constant_hunt trio + its two
  tests, and four task003/task009a projection-protocol tests. Content-level
  recovery of the constant_hunt trio is above; full decompile-grade
  reconstruction is possible from the `.pyc` copies banked in
  `old_program_sources/constant_hunt_bytecode/`.
- **Invisible-loss floor:** this method only sees Python that was once
  imported. The [CONTAINER]-tier scripts (f1_*, trap_*, ladder, h2_walls,
  mono_galois) were never on this machine at all — ephemeral-container
  casualties, not repo losses.
- **CALC-LOG DIARY RECOVERED (2026-07-06, Will's external copies):**
  `old_program_sources/Calc_logs/` — four cumulative snapshots; **v8 is the
  complete diary, all 36 entries CALC-01..CALC-36** (~152KB of derivation
  history vs the dashboard's ~16KB of state). The dashboard does NOT subsume
  it: per its own header it is "STATE, not history" — the diary carries the
  derivations (CALC-26 dimension threshold: ~156 lines vs a 4-line [SR] row),
  first-form definitions (the anti-reconstruction-drift record for G1.2),
  dead branches and re-openings (what NOT to re-run), the CALC-31..35 depth
  entries (partial substitute for the lost [CONTAINER] scripts), and the
  CALC-23/24/25 arithmetic entries (extra ARITH-I retrodiction targets).
  The earlier snapshots (v1/v2/v3) enable revision-diffing against v8 —
  the drift ledger documented that entries were sometimes silently revised,
  and the snapshot series is how to catch it.
- **Standing fix (Will's rule, generalized):** V4 is a frozen reference repo —
  one `git add -A` preservation commit there would make the entire surviving
  untracked layer permanent and end this loss class outright.

## Label-convention case law (2026-07-06 — RETRACTION of the "Known error" section
## that briefly stood here, commit 2ed5142)

An earlier revision of this banner claimed doc 1's keystone triple was mislabeled.
**That note was itself the error and is retracted.** Resolution from source
(`verification/recert_transport_law.py`) plus fresh structural discriminators
(hollow Hessian ⟹ all curvature lands in the coupling slot; diagonal Hessian ⟹ all
in the self slot):

```
channels() returns (kappa_c, kappa_INT, kappa_s) — interaction in the MIDDLE slot.
Keystone, certified labels:
    kappa_c   = -1/49
    kappa_int = -3/49
    kappa_s   = +1/49
kappa_c + kappa_s = 0 ;  K_G = kappa_int = -3/49
```

Doc 1's statement — "pure channels cancel; the surviving curvature is interaction
curvature" — is **CONFIRMED** under the certified naming (consistent with BOOT's
standing "sign-carrying interaction channel"). The retracted note had read RC-1's
then-unlabeled T1 stdout line positionally as (c, s, int); T4's labeled rows were
always correct in (kc, ks, kint) order, deliberately reordered in the source.

Standing rule from this incident: **never quote a channel tuple without slot
labels.** RC-1's stdout was hardened in ink the same day (T1/T6 lines now carry
labels; pin re-based `d370daae` → `4ad5a6eb`, 71/71 ×2, all values unchanged).
The collision was flagged for source-level re-check by external review before the
mislabeling propagated further.

## Source-of-truth order

The dashboard's internal order ("persistent evals > dashboard > calc log") is the old
program's. Here the order is: **in-repo certificates > everything external, full stop.**
