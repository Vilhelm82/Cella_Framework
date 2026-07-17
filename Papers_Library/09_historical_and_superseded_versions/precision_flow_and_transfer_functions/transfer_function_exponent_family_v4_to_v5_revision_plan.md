# Transfer Function Exponent Family — v4 to v5 Revision Plan

**Status**: Draft for review (before any edits to the .tex or creation of v5.tex)  
**Date**: 2026-05-30  
**Controlling documents**:
- `transfer_function_exponent_family_v4_to_v5_artifact_mapping.md` (accepted by user 2026-05-30)
- `HISTORICAL_RECORD.md` (Superseded section + paper-hardening entries)
- Original paper: `transfer_function_exponent_family_v4.tex` (2026-05-14)

**Scope decisions (confirmed 2026-05-30)**:
- GR critical exponents whitepaper + 45/16 derivation + ISCO/Kerr recoveries: **no-go**. Do not add as new content or cite in v5.
- Focus: Corrective reframing of superseded claims + citation of existing dedicated artifacts for the lattice derivation, precision-scaling partial, cross-fixture per-fixture reports, etc.
- Two real gaps remain open and correctly flagged: finite-window-bias V4 harness (Open Challenge #6) and non-algebraic/iterated-log V4 retest (Open Challenge #5, only V3 task023 material exists).

**Principles for the revision**:
- Cite existing artifacts only (never claim new work).
- Corrective credibility work first (the three HISTORICAL_RECORD-superseded items).
- Preserve honest partial status (especially theorem2_partial / task017c).
- Relabel or re-scope empirical observations that were presented as derived theorems.
- Add one modest new subsection for the BACL + c2 substrate derivation (the thing that was explicitly a forward task in v4).
- Keep the paper a "note" — no structural expansion beyond what is required for accuracy.
- Every changed claim gets a precise pointer to report directory + closeout/summary.
- Anti-drift: v5 must include a short provenance appendix or note that points back to the mapping document.

---

## 1. Overall Structure of Changes (High Level)

| Priority | Category | Sections Affected | Effort |
|----------|----------|-------------------|--------|
| 1 (Critical) | Corrective reframing | Abstract (esp. ¶40-42), Thm 3 + Status (L388-417), Revised empirical framing (L560-574), Open challenges #2 (L595), Notes on Scope (L605-614), Recommended manuscript changes | High |
| 2 | New derivation content | Insert one short subsection after current §6 or in §7 (after cross-fixture) describing the BACL+c2 substrate derivation of the lattice structure | Medium |
| 3 | Citation hygiene | Throughout (especially validation sections, Sterbenz, refinery, path-basis) + per the mapping document | Medium |
| 4 | Open challenges refresh | L593-601 (update #2 as now closed via derivation; keep #5 and #6 explicitly as "no V4 artifact yet"; note progress on others) | Low |
| 5 | Frontmatter + versioning | Title, date, abstract lead sentence, new "Changes since v4" note or short appendix | Low |
| 6 | Artifact hygiene (outside .tex) | Broken test path, GLOSSARY cross-refs, LIVE_CAMPAIGNS_LEDGER, any audit reports that hard-link to v4 claims | Low |

---

## 2. Detailed Section-by-Section Plan

### 2.1 Title / Date / Author block (L18-22)

**Current**:
```
\title{The Transfer-Function Exponent Family at Algebraic Branch Points\\
\large A Sharpened Structural Law, Cross-Fixture Substrate Validation,\\
and an Identified Mechanism for Arithmetic-Path Conditioning}
\author{William Lloyd\\\small Lloyd Geometric Diagnostics Pty Ltd}
\date{May 2026 (V4 typed-substrate revision, post-031 hardening)}
```

**Proposed**:
- Keep title (or minor tweak if desired).
- Change date to: `May 2026 (V5 substrate-derivation revision)`
- Add a one-line provenance note in the date or a new `\thanks{}`: "All cross-fixture and lattice claims now trace to dedicated V4 campaign artifacts; see `transfer_function_exponent_family_v4_to_v5_artifact_mapping.md` for the complete provenance table."

**Rationale**: Signals that this is the grounded version.

---

### 2.2 Abstract (L27-45) — Highest priority corrective text

**Problematic paragraphs** (L40-42):
- "Cross-fixture campaigns ... find five substrate invariants ... The cross-fixture invariants extend to controlled-branch radical chains beyond the original square-root case."
- "The precision-scaling separation theorem has been empirically validated: a linear-in-$u_p$ model fits ... at $R^2 = 1.0$ across all four fixtures."

**Proposed rewrite** (keep the math description of Thm 1 unchanged; rewrite the empirical summary):

V4 typed primitives validate the transfer law directly via `typed_finite_difference` and `typed_log_log_slope`. Cross-fixture campaigns across four fixtures spanning two radical degrees (Schwarzschild, special-relativistic time dilation, physics-stripped pure-algebraic control, and cube-root control; see per-fixture reports task024b, task027, task028, task029c and synthesis in _audit/03) establish five classification-level invariants in the arithmetic-path residuals of algebraically equivalent routings. The lattice structure underlying the 0.5/0.25 grain pattern and integer vs non-integer distinction is now derived from IEEE 754 + Sterbenz + the BACL invariant (Reports/bacl_invariant_audit/, c2_lattice_substrate_derivation/, c2_theorem_scope_gate/, with route-dependent rank for n=3).

The precision-scaling separation (Theorem 2) has a validated core: the regular-region linear-in-$u_p$ model for $C_{p,k}$ fits at $R^2 = 1.0$ across all four fixtures and load-bearing paths (task017c). Three sub-claims remain partial (detailed in §self-reference and task017c headline classification).

The Sterbenz boundary is confirmed as one concrete, fixture-shifted mechanism contributing to the path-conditioning amplitude $b_k$ (task031). A six-candidate refinery audit identifies sub-lattice alignment as a separate optimization criterion from operation-level exactness (task030, task032_cross_fixture_refinery_audit).

(Keep the final sentence on the diagnostic-vs-evaluation tension almost verbatim.)

**Rationale**: Directly implements the user's mapping + HISTORICAL_RECORD supersession flags. Removes "in general" over-reach and "empirically validated" for the whole theorem.

---

### 2.3 Theorem 3 (Cross-fixture invariance) + immediate Status paragraph (L388-417)

**Current label + statement**:
`\begin{theorem}[Cross-fixture invariance, classification level]\label{thm:cross-fixture}` + the five-item list + table + Status sentence that says it "strengthens ... to controlled-branch radical chains in general" + "Operation-level Sterbenz annotation ... remains a forward task".

**Proposed**:
- Change environment to `\begin{observation}` (or keep theorem environment but change title to "Cross-fixture classification invariants (observed)").
- Keep the five-item empirical list and table exactly (they are still true observations).
- Replace the Status paragraph (L415-417) with:

**Status.** This is a classification-level empirical regularity observed across the four fixtures (task024b_schwarzschild_four_form, task027_sr_four_form_cross_fixture, task028_conditional_masks_joint_lattice_pure_algebraic, task029c_cbrt_four_form_battery; synthesis in _audit/03_four-form-battery-cross-fixture-invariance.md). The 0.5/0.25 grain values and integer vs non-integer lattice distinction are properties of the two rounding grids (F1/F2 families), not a deep substrate universal. The underlying c2 integer-lattice structure is now a substrate-derived theorem (see new §"Substrate derivation of the c2 lattice invariants" below). Mechanism-specificity predictions (P_distrib_sqrt_mul absent in cube-root) from the path-basis work (task029c) continue to hold.

The forward task of full operation-graph annotation deriving the five invariants from per-operation rounding propagation remains open.

**Rationale**: Exactly matches HISTORICAL_RECORD supersession entry for this item + the user's mapping. Removes the "Theorem 3" over-claim while preserving all the actual observed data.

---

### 2.4 Precision-scaling section Status (L307-333) — mostly already good

The existing text already calls out the three sub-claims and the inverted Sterbenz-region observation. Minor tightening only:

- Change opening "Theorem \ref{thm:precision-separation} is empirically validated at the regular-region level" → "The regular-region core of Theorem \ref{thm:precision-separation} is empirically instantiated at R² = 1.0 (task017c_multi_precision_theorem2 + task017c_summary.md)."
- Add one sentence: "See task017c headline classification.md for the precise partial status."
- Keep the table and the mechanistic discussion of why the Sterbenz region behaves differently.

**Rationale**: The body text is already more honest than the abstract and revised framing. The flag in HISTORICAL_RECORD is mostly about the surrounding presentation.

---

### 2.5 Insert new short subsection: "Substrate derivation of the c2 lattice invariants" (new content, highest-value addition)

**Location suggestion**: After current §6 (cross-fixture) and before §7 (Sterbenz), or as a new §6.1.

**Proposed content outline** (≈ 12-18 lines):

The lattice grain pattern observed in the four fixtures (0.5 in transformed-operand fixtures, 0.25 in identity-operand fixtures) is not merely an empirical regularity. It is a direct consequence of three substrate facts now established in V4:

1. BACL invariant (Reports/bacl_invariant_audit/closeout.md + bacl_multi_format + bacl_subnormal): for floats a, b with ulp(a) ≥ ulp(b), a − b = j · ulp(b) for integer j. Proven across normal + subnormal ranges and multiple formats.
2. Sterbenz exact subtraction for the first R^n − 1 step inside the applicable half-space.
3. Conjecture C (Reports/conjecture_c_proof_audit/closeout.md): correctly-rounded square root preserves binade floor under canonical squaring (required for the n=2 clean case).

These combine into the c2 integer-lattice theorem (Reports/c2_lattice_substrate_derivation/closeout.md): c2 = round(V_n + (x_term − 1)) lands on an integer multiple of ulp(f). Scope is explicit (normal range, f_float ≥ 2^{-1021}). For n=2 the bound is tight (|j| ≤ 1); for n=3 the observed rank is route-dependent (np.cbrt max |j|=7 vs pow(1/3) max=2); higher n requires further C_n results (c2_theorem_scope_gate).

The 0.5/0.25 distinction and the integer vs non-integer classification are therefore now derived (with clear scope gates) rather than purely cross-fixture observations. The original empirical campaigns (task024b/027/028/029c) supplied the discovery data and the mechanism-specificity tests; the later BACL + c2 work supplied the derivation.

**Rationale**: This is the single most important strengthening. It directly closes what v4 called a forward task (operation-level mechanism for the cross-fixture lattice behaviour).

---

### 2.6 Revised empirical framing section (L556-574)

**Problematic long quote (L562-564)** and the numbered list of six claims (L566-574).

**Proposed**:
- Rewrite the long quote to match the new abstract language (reference the per-fixture reports for the invariants; reference the new derivation subsection for the lattice structure; qualify the precision-scaling claim as "regular-region core ... R²=1.0 (task017c)").
- In the numbered list:
  - Item 3 (cross-fixture): change "Theorem \ref{thm:cross-fixture}" → "the cross-fixture classification invariants (observed across four fixtures...)"
  - Item 5 (precision): qualify as "the regular-region core of the IEEE 754 amplitude-scaling law... instantiated at R²=1.0 (task017c)"
- Add a 7th item or a note: "the substrate derivation of the c2 lattice structure (BACL + Conjecture C + c2 theorem, Reports/...)".

**Rationale**: The "sharper empirical conjecture" paragraph is one of the places reviewers will read first for over-claim.

---

### 2.7 Open Challenges section (L593-601)

**Specific updates**:

- Challenge #2 ("Operation-level mechanism for Theorem \ref{thm:cross-fixture}"): Mark as **closed for the lattice structure** via the BACL + c2 derivation (cite the closeouts). Retain a narrower forward task for full per-operation graph annotation deriving all five invariants (including polarity coupling and Sterbenz bias).
- Challenge #5 (Non-algebraic discrimination retest): Keep verbatim + add "Only the V3 discovery (task023_iterated_logarithm_discovery/) exists; no V4 retest under the automatic diagnostic rule has been executed."
- Challenge #6 (Family-dependence / finite-window bias harness): Keep verbatim + add "No V4 typed fitting harness applying the bias model of Proposition finite-window-bias across nested typed transfer observations has been built."
- Other challenges: Light updates citing task032 (multi-fixture refinery), task029b (path-basis), etc.

**Rationale**: Directly implements the user's explicit statement that these two are the real remaining gaps with no artifacts.

---

### 2.8 Notes on Scope (L603-614)

Update the enumerated list of "novelty of the framework" to reflect the new derivation status for the lattice invariants and the qualified status of the precision-scaling claim. Remove or qualify any language that still reads as pure empiricism for items now derived.

---

### 2.9 Recommended manuscript changes (L576-589)

This section can mostly stay (it was already good forward guidance). Add one new item at the top:

"0. Reframe all cross-fixture universality and lattice claims in light of the BACL + c2 substrate derivations (see artifact mapping document). Relabel Theorem 3 as an observation or derived corollary where appropriate."

---

## 3. Frontmatter + Versioning + Anti-Drift

- Title block: as in 2.1.
- Add a new short unnumbered section or appendix "Provenance and changes since v4" (1 page max) that:
  - Points to the artifact mapping document as the complete table.
  - Lists the three major corrective changes (cross-fixture reframing, addition of substrate derivation subsection, precision-scaling qualification).
  - States the scope decision (GR work excluded from this revision).
  - Lists the two items that remain correctly open.

This satisfies the anti-drift requirement from the audits.

---

## 4. Artifact Hygiene Checklist (do in parallel with .tex work)

- Fix `tests/test_task017c_multi_precision_theorem2.py` (hardcoded old v3.tex path outside tree).
- Audit and update `V4_GLOSSARY.md` entries that point to the paper.
- Audit `LIVE_CAMPAIGNS_LEDGER.md` "maintain the paper" campaign entry.
- Any _audit/ reports that quote the old "Theorem 3" language can be left as historical or lightly annotated.
- Consider whether the mapping document itself should live in `Reports/` or stay in `Build_Docs/`.

---

## 5. Proposed v5 Deliverables (after plan approval)

1. Updated `transfer_function_exponent_family_v5.tex` (or in-place v5 revision of the existing file).
2. The mapping document (already written) and this plan (as appendices or separate references in the paper).
3. Possibly a one-page "v4 → v5 delta" summary for reviewers.
4. Updated HISTORICAL_RECORD entry noting that the paper claims have been reconciled to the post-May-18 substrate derivations.

---

## 6. Risk / Review Notes

- The corrective reframing (priority 1) is the only high-credibility-risk part. Everything else is additive citation or honest gap documentation.
- No new numerical results are claimed.
- The inserted derivation subsection must be written in the same tone as the rest of the paper (substrate reveals; short, precise, citation-heavy).
- After the plan is approved, the actual .tex edits can be done in small, reviewable chunks (one section at a time).

---

**Next action**: User review of this plan. When approved (with any adjustments), I will produce the actual edited v5.tex (or a set of precise search/replace patches) plus any small supporting updates. No .tex changes will be made until sign-off.

This plan is deliberately conservative and traceable. It turns the May 14 empirical draft into the properly grounded post-derivation version using only artifacts that already exist.