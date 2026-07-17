# Bigraded Jet — Stage A Report (J^(0,1): the υ-lanes alone)

**Date:** 2026-06-10 · **Branch:** `campaign/bigraded-jet` · **Manifest:** stage-a-v1, re-frozen post-amendment (current pin in `manifest_sha256.pin`; the ORIGINAL pin and its A-P1 FAIL verdict live in git history — commit "A-P1 FAIL recorded verbatim") · **Authority:** `CAMPAIGN_BIGRADED_JET.md` · **Rows:** HR131 §5 gap (driver), A4/A6 wave-two, B3/B4.

All numbers from committed byte-stable records via committed graders; measurement vs inference marked.

---

## 1. FIRST FINDING — the FAIL → amendment → outcome chain (recorded per Will's ruling 4)

**The frozen identity battery caught a misquoted theorem before the object shipped it.** The A-P1 run at the original pin FAILED (2/68): the subnormal-edge precondition for residual exactness had been transcribed into CITATIONS E3/E4/E6, the manifest, and the code as "result ≥ 2⁻¹⁰²¹" (normality of the *result*), where the cited theorems condition on representability of the *residue*, whose bits extend ~p binades below the result: `e_result ≥ e_min + p − 1 = −970`. Concretely: `sqrt(1e-300)` — a fully **normal** operand — produced a residual claimed PAIR_EXACT that is provably inexact in rationals (s² at exponent −997; the true residual needs bits at 2⁻¹¹⁰², below the 2⁻¹⁰⁷⁴ floor). Independently verified on-host by Will, including the FMA residual printing identically to the true value while differing in rationals.

Will's classification: **transcription-fidelity correction, not a retune** — prediction text unchanged, guard moved conservative (2⁻⁹⁶⁹; the (2⁻¹⁰²¹, 2⁻⁹⁶⁹) band flagged input-dependent), CITATIONS corrected **with erratum** preserving the file's own history, FAIL kept in the record.

**The amendment's two-sided grader (Will's ruling 3) immediately caught two MORE defects:** (a) BOUNDED bounds **underflowing to 0.0** for subnormal results — a wrong-ZERO **bound**, the exact anti-pattern this campaign forbids in residues, hiding in the bound channel (`0.5 × 2⁻¹⁰⁷⁴ == 0.0`); fixed with a representable-conservative `_half_ulp_bound`. (b) A grader defect: the sqrt bound check compared against `a` instead of `√a`; fixed by monotone interval squaring. One-sided grading would have passed both silently. [measured; all three defects have regression cases in the battery/tests]

## 2. Prediction verdicts (mechanical; `prediction_verdicts.json`; FAIL history preserved)

| prediction (frozen verbatim) | verdict | receipt |
|---|---|---|
| **A-P1** (kind-aware zero-gap exactness + flag totality) | **PASS** (post-amendment; original FAIL on record) | 68 cases: 62 zero-gap in exact `Fraction` arithmetic + 6 flagged-lawful (each flag verified *genuinely* below the sufficient condition, each bound verified honored); 200-bit mpmath corroboration zero-gap; zero MISSING_FLAG, zero UNLAWFUL_FLAG |
| **A-P2** (the lattice law) | **PASS** | **BACL membership 60/60** — every TwoSum subtraction residue is an exact integer multiple of ulp(b), checked in rationals; **Conjecture-C + c2 \|j\| ≤ 1: 40/40** on the boundary battery. Three months of proofs, recast as passing assertions over the υ-account. |
| **A-P3** (ORO reproduction from the lanes) | **PASS** | Lane-built Sum2/Dot2 equals 200-bit-truth-rounded-to-double on **every** battery case through cond = 1.0e16 (sum) / 2.0e16 (dot); naive error at the top of the range: 7.5% relative. Measured boundary: equality never broke anywhere in the battery's span. |

**Observation EXCEEDING the registered prediction (labeled as such per Will's ruling 5; reported, not retro-claimed):** on **all** ORO cases at **all** condition levels, `value ⊕ (sum of υ-residues)` equals the TRUE real-arithmetic result **exactly, in `Fraction` arithmetic** — not merely to double rounding. The registered A-P3 asked for truth-rounded equality in the low-cond regime; the lanes delivered identity in ℚ everywhere the coverage is EXACT. The account is complete: on this battery, floating point destroyed nothing — it relocated, and the lanes hold the relocation to the last bit.

## 3. What Stage A built [measured]

`evals/bigraded_jet.py` (placeholder name, covenant honored): typed compensated arithmetic under Amendment 1 — private `_UpsNum` algebra; unordered TwoSum default with **zero** Fast2Sum call sites (AST-enforced); FMA TwoProd; division/sqrt as exact residual pairs (ruling 2); kind taxonomy FLOAT_EXACT / PAIR_EXACT / BOUNDED / UNKNOWN with transcendentals honestly UNKNOWN (Python libm uncertified); precondition flags typed, never wrong zeros — *in residues or in bounds*; one TypedResult per evaluation; `bigraded_jet_upsilon` in the eval-tier ledger citing the brief. 12 required tests live; full suite 1125 passed, exit 0; records byte-stable on re-run.

## 4. Gaps filed

1. **Transcendental υ-coverage** [brief non-goal 2, confirmed needed]: sin/cos/exp/log carry honest UNKNOWN; a future campaign needs certified correctly-rounded transcendentals (the substrate's own typed_sin/typed_exp refine kernel is the obvious donor at promotion — noted, not pursued).
2. **The (2⁻¹⁰²¹, 2⁻⁹⁶⁹) input-dependent band**: currently flagged wholesale (honest sufficient-condition gating); a per-case exactness test (one `Fraction` check) could upgrade band entries to verified-EXACT — deferred, filed.

## 5. Names that fell out (covenant: collected, NOT adopted)

Recorded candidates the substrate suggested while the code was being written and graded — each emerged unprompted in the work, none christened:

- **"the account" / "ledger"** — appeared independently in the value-object docstrings ("the υ-account"), in A-P3's headline ("the account is complete"), and in the Option-B registry vocabulary already in the tree. The object behaves like double-entry bookkeeping for information: nothing destroyed, everything posted.
- **"residue lattice"** — A-P2's result keeps saying it: the residues *live on BACL's lattice*; the υ-lane is a lattice-valued channel.
- **"relocation"** — from the brief's own physics ("floating point relocates information"); the lanes are *where it relocates to*; "relocation account" combined the two in the A-P3 analysis.

Founder-sourced candidates, collected in-brief by Will mid-stage (commits `8713485`, `0bde698`; honestly labeled "founder, not substrate — filed, not adopted"):

- **`FocusDual`** — ADHD meta joke (dual numbers × Focalin); accidentally apt per its own filing: the ε-lane is the task, the υ-lanes are everything noticed anyway, the mixed lanes are knowing which distractions mattered.
- **`FocusDual75`** — dosage-strength variant; the 75 is the 7.5% naive-float64 error on the cond=1e16 A-P3 case the lanes treated to the last bit. (Filed post-Stage-A-stop; recorded here for completeness.)

No adoption proposed from either source. Stage B's mixed lanes may speak differently.

## 6. Stage close state

Acceptance: manifest frozen pre-implementation ✓ (amendment classified and re-pinned per ruling; FAIL preserved); predictions graded mechanically, verdicts verbatim ✓; full suite exit 0 ✓; byte-stable ✓; source audit clean (frozen-token list; AST Fast2Sum check) ✓; records under `results/bigraded_jet/stage_a/` ✓; ledger/HR updates reserved to Will per standing practice. **STOPPED at the Stage-A report as briefed — Stage B (fusion, J^(2,1)) awaits your GO.**
