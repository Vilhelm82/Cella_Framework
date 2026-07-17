# Task Spec — WARP Stage-0 Reconnaissance (read-only)

**Producer:** claude-code (CLI worker) · **Reviewer disposes:** Claire/Will.
**Parent campaign:** `the-shared-residual` — **algebra arm (WARP)**, per
`LIVE_CAMPAIGNS_LEDGER.md`. No new campaign name.
**Authority brief:** `Build_Docs/Agent_tasks/CAMPAIGN_BRIEF_algebra_arm_DRAFT.md`
(the working canon; the two superseded WARP docs are archived under
`Build_Docs/_archive/superseded_docs/`).

**Contract scale-down (declared, per TASK_TEMPLATE):** this is a **read-only
reconnaissance** task — no derivation, no battery, no new substrate claim. It
exists to convert three "to-be-confirmed-at-freeze" audit hits into verified
build-vs-consult verdicts *before* Stage 0 is written, so the freeze and Will's
§10.5 scope ruling are made on fact, not on the brief's optimism. The output
contract is scaled to a **findings report + a small `result.json`**; every finding
is evidence-backed (file path + symbol + the grep/read that found it). Scope flags
are all-false by construction.

---

## Mandatory pre-reads & closed-results check (done — recorded)

Read this session 2026-06-14: `SPINE_STATUS.md`, `WORKING_SET.md`,
`LIVE_CAMPAIGNS_LEDGER.md`, the algebra-arm brief, `TASK_TEMPLATE.md`. The Stage −1
prior-wins audit lives in the brief §1 (six hits, grep'd on-repo). This task
**re-confirms three of those hits at the source** — it does not open new ground.

**Closed-results verdict:** ☑ continuation of campaign `the-shared-residual`
(algebra arm) — Stage-0 preparation for a brief already drafted and at its §10
checkpoint. Not a new result; a confirmation pass that de-risks the freeze.

## Binding & scope

- **Producer proposes; reviewer disposes.** No canonical-record writes (HR / ledger
  / glossary). No freeze. No prereg. No manifest.
- **Workspace:** `scratch/warp_stage0_recon/` only. **Read-only against
  `src/lloyd_v4/`** — inspect, never edit. No substrate, no normative-doc, no
  results/ writes.
- **Not a substrate task.** No `/v4-axiom-check`, no plan-mode needed — nothing is
  edited. If the worker finds itself wanting to *change* a substrate file, it stops
  and reports instead.

## Task goal

Answer three build-vs-consult questions the brief's §1 audit raised but did not
resolve at the source, each of which moves Stage-0 scope or instrument cost:

1. **Does the existing `projective_ratio` L1 primitive already carry a
   `PGL₂`/Möbius (projective/fractional-linear) action**, or is that action the one
   genuinely-new micro-build for FX-W-F's keystone carrier? *(Sets §10.5 scope: is
   the ℙ¹(ℚ) carrier consult-only, or consult + one small action build?)*
2. **Can `D_static` (the factorability op-DAG walker) lift the existing
   `closure_grade` derivation-closure walk + the `AtomKind` partition**, or must it
   carry its own walker? *(Sets Stage-A instrument cost — reuse vs rebuild.)*
3. **Is the `required_precision` "decidable terminal predicate" precedent shaped
   the way the brief claims** (a static structural predicate over a restricted
   lattice, answered YES), so CL-W1's `[ANALYTIC]` leg can *cite* it rather than
   present decidability as novel?

## Design principles

Deterministic, read-only. Every answer is grounded in a named file + symbol +
the exact command that surfaced it. No claim about *factorability itself* is in
scope — only about **what substrate already exists to build on**. Where the
existing primitive is ambiguous (e.g. `projective_ratio` carries scalarization but
no transform action), say so precisely and grade it `consult + thin build`, not a
binary.

## Burden of proof (per question — the checkable obligation)

- **Q1:** locate every public symbol of the projective-ratio primitive
  (`LAYER_MANIFEST.md` "Provides" lists: `ProjectiveRatioStatus/Value/Result`,
  `PROJECTIVE_RATIO_SPACE/PROTOCOL`, `projective_ratio`, `scalarize_projective_ratio`,
  `PROJECTIVE_RATIO_SCALARIZATION_TRANSITION_RULE`). Then search the same module(s)
  for any **action / transform / Möbius / fractional-linear / PGL / matrix-acts-on-point**
  capability. Verdict: `action_present` (cite symbol) · `action_absent →
  thin eval-tier build` · `partial (what's there, what's missing)`.
- **Q2:** read `src/lloyd_v4/harness/closure_grade.py` and `core/binding.py`;
  enumerate `AtomKind` members (expect `FINITE_EXACT_ALGEBRAIC`,
  `CONSTRUCT_TO_TOLERANCE`, `NOT_ATOM`) and `LeafKind`; determine whether
  `closure_grade` exposes a **reusable static walk over an op-DAG** that `D_static`
  can call, or whether its walk is entangled with grading internals. Verdict:
  `liftable (cite the entry point)` · `partial (wrap needed)` · `rebuild`.
- **Q3:** locate the `required_precision` predicate (glossary "Required-precision
  composition floor — decidable terminal predicate"; certified-precision-spine P1,
  HR123-class). Confirm: (a) it is a **static** predicate, (b) over a **finite
  computation tree + closed-form W(k) + fixed atom-kinds + fixed format**, (c)
  recorded **decidable / answered**. Verdict: `precedent_confirmed (cite source)` ·
  `precedent_weaker_than_claimed (state the gap)`.

## Required deliverables

- `scratch/warp_stage0_recon/RECON_REPORT.md` — the three questions, each with:
  verdict, the evidence (file:symbol), the exact command(s) run, and a one-line
  **freeze implication** (what this means for Stage 0 / §10.5).
- `scratch/warp_stage0_recon/result.json` — the scaled-down contract below.
- A short **"Will's desk" block** at the end of the report: the net effect on
  §10.5 scope (does FX-W-F need a Möbius build? does Stage A reuse `closure_grade`?)
  and any newly-surfaced risk.

## Output contract (machine-checkable — scaled down, reviewer validates)

```json
{
  "task_id": "warp_stage0_recon",
  "campaign": "the-shared-residual (algebra arm / WARP)",
  "producer": "claude-code",
  "read_only": true,
  "findings": [
    {
      "id": "Q1-projective-action",
      "question": "Does projective_ratio already carry a PGL2/Mobius action?",
      "verdict": "action_present | action_absent_thin_build | partial",
      "evidence": ["file:symbol", "..."],
      "commands": ["..."],
      "freeze_implication": "...",
      "confidence": "low | med | high"
    },
    {
      "id": "Q2-dstatic-lift",
      "question": "Can D_static lift closure_grade + AtomKind?",
      "verdict": "liftable | partial_wrap | rebuild",
      "evidence": ["..."],
      "commands": ["..."],
      "freeze_implication": "...",
      "confidence": "low | med | high"
    },
    {
      "id": "Q3-decidability-precedent",
      "question": "Is required_precision the decidability precedent CL-W1 claims?",
      "verdict": "precedent_confirmed | precedent_weaker_than_claimed",
      "evidence": ["..."],
      "commands": ["..."],
      "freeze_implication": "...",
      "confidence": "low | med | high"
    }
  ],
  "scope_compliance": { "touched_substrate": false, "touched_normative_docs": false, "wrote_canonical_record": false, "froze_anything": false },
  "not_established": ["honest list — e.g. 'did not assess whether the Mobius build closes the dissection gate; that is a Stage-0 build task, not recon'"]
}
```

## Required tests

None — read-only. The acceptance gate is the reviewer's independent re-grep
reproducing each cited file:symbol.

## Required commands (deterministic; no network)

Suggested starting points (the worker may add, but records every command it runs):
```
grep -rn "projective_ratio\|ProjectiveRatio\|PROJECTIVE_RATIO" src/lloyd_v4/ Build_Docs/Architecture/LAYER_MANIFEST.md
grep -rni "mobius\|m\xf6bius\|fractional.linear\|PGL\|projective.*action\|act_on" src/lloyd_v4/
sed -n '1,200p' src/lloyd_v4/harness/closure_grade.py
grep -rn "class AtomKind\|class LeafKind\|FINITE_EXACT_ALGEBRAIC\|CONSTRUCT_TO_TOLERANCE\|NOT_ATOM" src/lloyd_v4/
grep -rn "required_precision\|Required-precision\|composition floor" src/lloyd_v4/ Build_Docs/Architecture/V4_GLOSSARY.md
```

## Non-goals

- **Does not** write fixtures, schema, manifest, prereg, or pins — that is Stage 0,
  gated on Will's §10.2/§10.5/§10.7 rulings.
- **Does not** build the Möbius action, the `D_static` walker, or the carrier
  classifier — it only reports whether they are consult, wrap, or build.
- **Does not** edit any `src/lloyd_v4/` file or any canonical-record doc.
- **Does not** make or grade any factorability / ⊕-universality claim.

## Acceptance criteria (reviewer gate)

1. `result.json` validates; every finding has a verdict, ≥1 `evidence` entry as
   `file:symbol`, and the `commands` that produced it — **no blank fields**.
2. Each cited `file:symbol` reproduces under the reviewer's independent re-grep.
3. `scope_compliance` all-false (read-only confirmed).
4. `not_established` is non-empty and honest.
5. The "Will's desk" block states the net §10.5 scope effect in one paragraph.

Fail any box → bounced back; nothing enters the record. On pass, the reviewer folds
the three verdicts into the Stage-0 freeze decision and Will's §10.5 ruling.

## Disposition (reviewer-only)

Reviewer (Claire/Will) reads the report, re-greps the citations, and carries the net
finding into: (a) §10.5 scope (FX-W-F build size), (b) the Stage-A instrument plan
(`D_static` reuse), (c) CL-W1's `[ANALYTIC]` citation. No HR/ledger/glossary write
from this recon — it is preparation, not a result.
