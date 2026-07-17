# CALC-LOG ↔ EVALS DRIFT LEDGER

**Date:** 2026-07-01 · **Author:** reconciliation sweep (this session) · **Status:** proposal-grade audit artifact. Nothing canonical was edited.

## Purpose
The calc log (`dbp_four_role_calc_log_v*.md`) is a **diary** — a chronological record of what each session did, *including sessions that re-opened already-settled questions*. The **evals** (`evals/**`) plus their `rec.record(tier=…)` standing conclusions are the **dashboard** — the certified state. Nothing keeps the diary's `[open]`/`[conjecture]` markers in sync with the evals that close them, so **"open in the log" ≠ "open in reality."** This ledger records where they have drifted apart.

**Source-of-truth order:** evals + standing conclusions (state) **>** calc log (history). A log `[open]` marker means "open when written," not "open now."

## CERTIFIED DRIFT

### DRIFT-1 — "same S₃?" (role S₃ vs monodromy within-block S₃)
- **Log says open:** `dbp_four_role_calc_log_v7.md` L797/799 — "live frontier … `[conjecture]` (same S₃)".
- **Actually closed by (runnable eval, on disk):** `evals/dbp_involution/stageE_monodromy_alt_probe.py` — P-E3 / E_VERDICT: `canonical_map_exists = False`, verdict `no_canonical_comparison_map`, tier `[computer-verified group theory; canonicity is a structural fact]`, citing **CALC-10** as the standing conclusion. Corroborated by `stageA_sym_wedge_split.py` (carrier = symmetric half, `[proven]`) and `stageB_O_parity_vs_tau.py` (alternating half = `∧²(std₃)=sign`, untouched by the carrier O).
- **Answer:** the two S₃'s are **distinct** — the 3 monodromy blocks are root-sheets of the stage-2 trinomial, not the 3 roles; no role-canonical bijection. Settled at **CALC-10**, i.e. long before this session.
- **Re-derived (wastefully) as:** **CALC-36** (this session), via a weaker Jacobian-rank functional-independence check. CALC-36 should be marked **superseded / reconciled-known** — it adds nothing the eval didn't already hold, more rigorously.
- **Grade:** CERTIFIED drift.

### DRIFT-2 — self-glue monodromy wreath structure (CALC-25 group-theoretic opens)
- **Log says open:** `v7` CALC-25 "Open/next" (2) C₄-vs-D₄ on directive cover, (3) full certified continuation; and the original monodromy paper §10 `[conjecture]` items ("beyond mP=2 — does the product side climb to S₃≀S₃?", "fullness of the wreath for all mD").
- **Actually closed by (paper on disk, proven / computer-verified):** `tmp/pdfs/constant_hunt/self_glue_monodromy.txt` —
  - Lemma B′ (coprime trinomial ⇒ Sₘ, all k) `[proven]`;
  - Lemma C (gcd law: cover = `C_d ≀ S_{m/d}`, d = gcd(m,k)) `[proven]`;
  - certified continuation (3,2)(4,3)(6,5)→S₃,S₄,S₆ and (4,2)(6,2)(6,3)(9,3)→C₂≀S₂,C₂≀S₃,C₃≀S₂,C₃≀S₃ `[computer-verified]`;
  - product cover = `C_mP ≀ C_mP` cyclic wreath `[proven]` / `[cv @ mP=2,3,4]` — which **answers "climb to S₃≀S₃": NO** (cyclic, not symmetric) and **corrects the original paper's `Sym(mP)≀Sym(mP)` claim.**
- **Grade:** CERTIFIED-as-documented drift (closure is a proven/computer-verified paper on disk; the certifying continuation script may be ephemeral — no persistent runnable eval for the monodromy covers was located under `evals/`).
- **Still open (NOT closed):** CALC-25 open (4) — promote (omega-multiplicity, signature) to a *defined diagnostic coordinate* and retrodict the curvature ladder. Genuinely open.

## GENUINELY OPEN (checked, no eval closure found — NOT drift)
- CALC-35 opens: mixed bidegrees `κ_{r;p,q}` (minimal p for depth r), other depth-r irreps (alternating `S^(n−r,1^r)`, three-row), full-density surjectivity onto `M_flags^(r)`.
- Finite two-state witness against the (2,2) shape invariant (v7 L322).
- CALC-25 open (4) (see DRIFT-2 caveat).

## STRUCTURAL DIAGNOSIS (the actual finding)
The drift is not incidental — it is the **default behavior** of a diary-plus-evals setup with no reconciliation mechanism. A fresh session reads a frozen `[open]` marker, trusts it, and re-derives work the evals already closed. This session did exactly that with DRIFT-1 (CALC-36 re-deriving the CALC-10 standing conclusion). This is the concrete, on-disk demonstration of the context problem the retrieval-index proposal was reaching for.

## RECOMMENDATION
Index contract: **"is question X open?" resolves to the eval / standing conclusion that closed it, not to a calc-log line.** Corpus = `evals/**` + their `rec.record(tier=…)` conclusions (+ the proven papers under `tmp/pdfs/`). Keys = exact identifiers (CALC-NN, stage names, S₃, wreath, `κ_{r;p,q}`) + a thin semantic layer. The calc log stays a diary; this ledger and such an index are the dashboard it was never meant to be.

## IMMEDIATE CLEANUP (proposed, NOT executed — awaiting sign-off)
1. Mark CALC-36 in the working calc log as **superseded / reconciled-known** (re-derivation of the CALC-10 standing conclusion; closure in `stageE_monodromy_alt_probe.py`).
2. Append a dated note at the v7 L797 frontier pointing to `stageE_monodromy_alt_probe.py` (append to the diary; do not rewrite history).
3. Optionally annotate CALC-25 opens (2)(3) as closed by `constant_hunt/self_glue_monodromy.txt`; leave (4) open.
