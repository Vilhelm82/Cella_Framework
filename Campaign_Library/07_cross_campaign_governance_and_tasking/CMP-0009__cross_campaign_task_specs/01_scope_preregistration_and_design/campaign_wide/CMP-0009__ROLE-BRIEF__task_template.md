# Task Spec Template (V4 / Cella)

The single template for a Codex/agent execution spec. Tasks commit **one
at a time**; the next task's spec is re-evaluated against the evidence the
completed one produced (no forward stale drafts). Fill every section;
delete the italic guidance when instantiating.

This template folds in the rigor that used to live in a separate
"hardened" variant — the machine-checkable output contract and the
retrodiction gate are now **standard**, because the project's discipline
(prereg-freeze, content-pins, byte-stable ×2, reviewer-disposes) is the
default for every producer, trusted or not. Scale the contract down only
for a genuinely trivial mechanical task, and say so explicitly.

> **Standing law this template enforces** (CAMPAIGN_DISCIPLINE.md):
> Rule 1.2 (no substrate promotion inside a campaign — promotion is a
> separate post-closeout exercise); Rule 1.8 (graders embed their
> governing clause verbatim; the gate string-compares at runtime and
> refuses on drift); Rule 1.9 (every artifact a battery reads **or
> executes as referee** is content-pinned and gate-enforced — data and
> code alike).

---

## Mandatory pre-reads & closed-results check (do this FIRST — anti-re-derivation gate)

The dominant documented cost in this project is **re-deriving an
already-closed result**. A spec with this section blank is not ready to
commit. Per `CLAUDE.md §2`, read and record what you found:

- [ ] **`Build_Docs/Architecture/PROJECT_INDEX.md`** — the front door (what V4/Cella is, the live frontier, where things live).
- [ ] **`HISTORICAL_RECORD.md`** — confirm the result is not already PROVEN / PARTIAL / closed. Rows checked: ___ . If it overlaps, this task **extends** it (cite the row + state what is genuinely new).
- [ ] **`LIVE_CAMPAIGNS_LEDGER.md`** — confirm the work doesn't fit an **active campaign** (if it does, continue it) and doesn't match a **restart-trap alias**. Campaign(s)/aliases checked: ___ .
- [ ] **`V4_GLOSSARY.md`** — confirm no term/concept drift (esp. §13 "things commonly confused"). Terms checked: ___ .
- [ ] **`TASKS_TO_REVISIT.md`** — confirm this isn't silently re-opening a known richness-loss point.

**Closed-results verdict (tick exactly one, with a citation):**
☐ genuinely new · ☐ extension of `[HR row / report]` · ☐ continuation of campaign `[ledger entry]`.
If you cannot tick one with a citation, **stop** — not yet well-scoped.

## Binding & scope

- **Producer / reviewer:** the agent **proposes**; a human/CC reviewer **disposes**. Canonical-record writes (HR / ledger / glossary) are reviewer-only. Record integrity is evidence-gated and authorship-blind (`CLAUDE.md §3`).
- **Parent campaign:** ___ — a canonical name from `LIVE_CAMPAIGNS_LEDGER.md`. No new campaign names.
- **Workspace:** `scratch/{slug}/` or a worktree — unless this is an authorized substrate task (below). No substrate, normative-doc, or canonical-record writes from an exploratory task.
- **Substrate tasks only:** if the task edits `src/lloyd_v4/{core,primitives,projection,metrology,branch}/` or a rules/substrate doc, it runs under plan-mode + `/v4-axiom-check` first (`CLAUDE.md §6`), passes the SUBSTRATE_CONSTRUCTION §3 transplant + §4 dissection gates, and (for promotions) moves through the eval-tier registry → atomic promotion (F13). Under the **cella-as-trunk re-founding**, account-primitive work follows that charter.

## Current verified baseline

What is known-complete at task start: cite `HISTORICAL_RECORD.md` rows, test counts, and what is PROVEN vs PARTIAL vs OPEN. Do not re-derive anything closed.

## Retrodiction gate (pre-flight — passes before any new claim)

- **Reproduce first:** ___ (the known result this builds on; cite its HR row / artifact). Emit byte-stable evidence at `scratch/{slug}/retrodiction.json`. If it does not reproduce, **stop and report** — do not proceed to new work.

## Task goal

*One narrow paragraph: the question, at what scope, and why it is open per the record.*

## Design principles

*Task-specific constraints + inherited commitments. Pin precision/backends explicitly; deterministic output; exact arithmetic where the claim requires it (not float128 standing in for exact). For account-carrying work: state value + account == TRUE in ℚ as the grading identity where it applies.*

## Primitive-sufficiency gate (Axiom 12)

*Demonstrate every concept the task needs is provided by parent layers. If not, list the parent-extension tasks required first.*

## Burden of proof

- *The specific, checkable obligation (e.g. "≥2 distinct nonzero residuals per cell").*
- *The derivation that must be shown (algebraic chain / IEEE-754 reduction / exact-ℚ identity).*
- *The exact threshold/value to be located, with tolerance.*

## Required deliverables

*Files, modules, statuses, protocols, transition rules, reports. Campaign artifacts (frozen prereg, pinned manifest, byte-stable records, stage report) live under `results/{campaign}/`; exploratory artifacts under `scratch/{slug}/`.*

## Output contract (machine-checkable — reviewer validates)

Emit `result.json` matching this schema (per-claim calibration; scale down only for a trivial mechanical task, and say so):

```json
{
  "task_id": "...",
  "campaign": "...",
  "producer": "codex | claude-code | other",
  "retrodiction_gate": { "description": "...", "passed": true, "evidence_path": "..." },
  "claims": [
    {
      "claim_id": "...",
      "statement": "...",
      "kind": "measured | inferred",
      "status": "PROVEN | PARTIAL | OPEN | REFUTED | DEMONSTRATED",
      "confidence": "low | med | high",
      "value": "...",
      "generating_script": "...",
      "raw_output": "...",
      "byte_stable": true,
      "derivation": "...",
      "falsifier": "...",
      "axiom_smuggling_check": "derived from spec+axioms only | flagged: <prior>"
    }
  ],
  "scope_compliance": { "touched_substrate": false, "touched_normative_docs": false, "wrote_canonical_record": false },
  "not_established": ["honest list of what this run did NOT settle"]
}
```

## Required tests

*Test files + one-sentence descriptions. Include the controls that must FAIL (informativeness) and the dry-runs that must REFUSE, where the discipline applies.*

## Required commands

*Exact commands for the red slice, green slice, full suite, source-purity audit, and the reviewer's byte-stability re-run. Deterministic; no network; pinned env.*

## Non-goals

*What this task explicitly does not do — prevents scope creep and accidental campaign restarts.*

## Acceptance criteria (reviewer gate — every box holds)

1. `result.json` validates; **no blank fields** in any claim.
2. Retrodiction gate `passed: true` with reproducing evidence.
3. Every `measured` claim: `generating_script` + `raw_output` present, and the reviewer's independent **re-run reproduces byte-for-byte**.
4. Every claim carries a `derivation` and a `falsifier`; `axiom_smuggling_check` clean or explicitly flagged (flagged → reviewer adjudicates).
5. `scope_compliance` correct (exploratory: all-false; substrate task: the authorized edits only, gates passed).
6. `not_established` is non-empty and honest.

Fail any box → bounced back; **nothing enters the record.**

## Disposition (reviewer-only)

On full pass, the reviewer updates the canonical record per `CLAUDE.md §8` — ledger / `HISTORICAL_RECORD` / glossary — citing artifact paths, entering each claim at its **true** status (eval-tier until a substrate derivation exists). Admission is evidence-gated and authorship-blind: a measured, reproduced value stands regardless of which agent produced it.
