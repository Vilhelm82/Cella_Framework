# KILL_SEARCH_BRIEF — Precision-Flow Paper (v1)

**Status:** authored by Claire, 2026-06-11, in a session without web tools (toolkit rotation); MIGRATED to repo 2026-06-12. Executed 2026-06-11/12 by CC (web-enabled) — see `results/precision_flow/paper/KILL_SEARCH_LEDGER.md` for the executed ledger + review. This document operationalizes paper-skeleton §11 item 1.

## THE COVENANT
This is an ADVERSARIAL search: we are trying to FIND our own results in the literature, not to confirm their absence. Success is either (a) a verified collision, recorded verbatim, with the skeleton repositioned honestly, or (b) documented silence across all fronts WITH RECEIPTS — queries run, sources read, sections cited. "To our knowledge" is earned, never asserted. The FAIL ledger and the discovery ledger are the same document; that rule applies to related work too.

## VERDICT GRAMMAR (one block per front, no exceptions)
- COLLISION: a found statement subsumes one of Theorems 1–14. Record: verbatim quote, full citation, page/section, which theorem(s) it kills or wounds. Stop that front immediately; continue the others; flag the skeleton.
- ADJACENT: related machinery that must be cited. Record: citation + a drafted one-sentence differentiation for §9.
- CLEAR: every falsification question answered negative, with page-level receipts (chapter/section read, not just searched).
Every verdict names its evidence. Counting-unit discipline applies: "searched" ≠ "read".

## PRELIMINARY RECEIPTS (run in-session, 2026-06-11)
- Probe 1: dynamics-of-floating-point literature — studies FP corrupting chaotic orbits (Hénon reversibility, logistic degradation); opposite arrow; no residual-flow formulation found. PRELIMINARY CLEAR, does not discharge Fronts 1–6.
- Probe 2: TMD/Ziv corridor — hard-to-round condition is the fractional part 2^p·m(f(x)) mod 1 used as a STATIC inequality at fixed p; Ziv analyzed for termination, not step law. PRELIMINARY ADJACENT (mandatory cites), does not discharge Front 4's thesis-level questions.

## FRONT 1 — Constructive / exact real arithmetic (Boehm school)
Sources: Boehm, "Towards an API for the Real Numbers" (PLDI 2020); Boehm–Cartwright "Exact Real Arithmetic: A Case Study in Higher Order Programming"; CRCalc / Android calculator notes.
Falsification questions:
  1a. Is appr(p) anywhere REQUIRED to be round-to-nearest (canonical), or only modulus-bounded (any integer within an ulp)?
  1b. Any stated one-step relation between appr(p) and appr(p+1)?
  1c. Does incremental evaluation ever reuse lower-precision state EXACTLY, or always re-evaluate under bounds? (Read the caching/scaling sections of PLDI 2020 closely — this is the reconstruction-collision surface.)
  1d. Any orbit/periodicity remark for rational values?
Search strings: Boehm recursive real arithmetic incremental precision; "towards an API for the real numbers" caching reuse; constructive real arithmetic "one more bit".
Collision shape: a lemma relating successive canonical approximations by a shift/doubling rule, or exact state reuse across precision.

## FRONT 2 — iRRAM / computable analysis (Müller; Weihrauch TTE)
Sources: Müller, iRRAM documentation + "The iRRAM: Exact Arithmetic in C++"; precision/reiteration policy notes; Weihrauch, "Computable Analysis" (TTE); Brattka–Hertling–Weihrauch survey.
Falsification questions:
  2a. Any state-reuse result across reiterations beyond caching of discrete decisions?
  2b. Obtain the exact theorem + citation for the canonical-binary pathology (multiplication by 3 not computable on binary expansions; admissibility of representations) — this is §9's framing citation: the field PROVED our object hostile, then nobody mapped it.
  2c. Any residual-dynamics statement anywhere in TTE literature (orbits of approximation error under refinement)?
Search strings: iRRAM reiteration precision policy state reuse; Weihrauch admissible representation binary expansion not computable multiplication.
Collision shape: a reiteration theorem computing the higher-precision run's state from the lower one.

## FRONT 3 — Online / MSD-first arithmetic (Ercegovac school; digit streams)
Sources: Ercegovac & Lang, "Digital Arithmetic" (online arithmetic chapter); Trivedi–Ercegovac 1977; Avizienis 1961 (signed digits); Edalat–Potts LFT exact arithmetic; Escardó digit-stream papers.
Falsification questions:
  3a. Is the non-redundant impossibility (no bounded-delay MSD-first addition in standard binary) stated FORMALLY anywhere? Obtain the citable form.
  3b. Any treatment — even informal — of the EVENT structure of non-redundant refinement (which outputs move when an input digit arrives; anything resembling reflections/absorption)?
  3c. Confirm online-delay theory is redundant-representation-only.
Search strings: online arithmetic bounded delay redundancy necessity; most significant digit first standard binary impossible; signed digit online delay addition.
Collision shape: an event calculus for non-redundant streams.

## FRONT 4 — Correct rounding / TMD (the home crowd)
Sources: Ziv 1991 ("Fast evaluation of elementary functions..."); Lefèvre's thesis (READ the continued-fraction / three-distance machinery chapters); Lefèvre–Muller worst-case papers; Muller, "Elementary Functions" ch. 12; "Handbook of Floating-Point Arithmetic" correct-rounding chapters; ACM Computing Surveys correct-rounding survey (hal-04474530); SLZ algorithm papers.
Falsification questions:
  4a. Does ANY source iterate the fractional-part quantity ACROSS precisions (a recurrence), versus bounding it at one fixed p?
  4b. Does any Ziv analysis characterize step-to-step evolution of the residual during escalation (not just termination/expected iterations)?
  4c. Lefèvre's machinery: static at target precision, or dynamic in p?
  4d. Is hardness-to-round anywhere defined as an exit-time / orbit statement?
Search strings: Lefèvre worst cases fractional part successive precisions; Ziv strategy residual recurrence; correctly rounded "increasing the working precision" analysis.
Collision shape: t_{p+1} = 2t_p − D in any notation; an exit-time formulation of TMD.

## FRONT 5 — Adaptive / expansion arithmetic (Shewchuk; Priest; EFT school)
Sources: Shewchuk 1997 ("Adaptive Precision Floating-Point Arithmetic and Fast Robust Geometric Predicates"); Priest 1991; Dekker 1971; Ogita–Rump–Oishi 2005.
Falsification questions:
  5a. Shewchuk's staged refinement: any step LAW relating stage residuals, or only per-stage error bounds?
  5b. Expansions literature: any statement that the expansion tail evolves under a dynamics (vs is merely summed)?
  5c. EFT literature: any precision-VARYING treatment at all (their residual is ours at fixed p; do they ever flow it)?
Search strings: Shewchuk adaptive stages error bound residual; floating point expansion tail refinement dynamics.
Collision shape: a stage-to-stage residual recurrence.

## FRONT 6 — Precision-driven expression DAGs (Yap's CORE; LEDA::real; separation bounds)
Sources: Yap et al., CORE library papers ("A Core Library for Robust Numeric and Geometric Computation"); LEDA::real documentation/papers; BFMSS separation-bound papers.
Falsification questions:
  6a. Does Expr propagate anything across precision levels other than bounds and precision REQUESTS — any exact state reuse?
  6b. Any classification of WHICH DAG nodes' values change when precision increases (deviation/absorption shape)?
  6c. Separation-bound machinery: purely static, correct?
Search strings: CORE library precision driven expression DAG recompute; LEDA real precision propagation; exact geometric computation precision demand.
Collision shape: node-level change classification under precision increase.

## FRONT 7 — Wildcard sweep
- Gosper continued-fraction arithmetic (HAKMEM item 101) — incremental refinement in CF representation.
- Kahan's web notes/lectures — folklore hides there; strings: Kahan precision refinement remark; Kahan "one more bit".
- Recent arXiv sweep 2020–2026: "rounding error" + "precision refinement"; "round-to-nearest" recurrence precision; "doubling map" floating point; residual orbit precision; Bernoulli shift rounding.
- Stochastic-rounding surveys (contrast only; confirm no refinement-dynamics section).
- Formal-proof corpus: Flocq/Boldo–Melquiond — any lemma family about RN at two precisions (succ_prec style lemmas)? Sleeper collision surface: proof libraries state small exact lemmas nobody publishes. NOTE: "double rounding" literature (rounding twice through an intermediate precision) is ADJACENT-at-minimum and must be read: Figueroa, Boldo–Melquiond. Our law concerns RN_q vs RN_{q+1} of the SAME x (refinement), not RN∘RN composition (double rounding) — but the lemma stock overlaps. Obtain and differentiate explicitly.

## EXECUTION PROTOCOL
1. One focused session. Fronts in order 4, 7(double-rounding), 1, 6, 2, 3, 5 (highest collision risk first).
2. For each front: run strings, FETCH AND READ the named primary sources at the cited chapters, answer every falsification question with page/section receipts, write the verdict block.
3. Output: KILL_SEARCH_LEDGER.md (results/precision_flow/paper/): one verdict block per front, preliminary receipts incorporated, drafted differentiation sentence per ADJACENT, and a final one-paragraph disposition.
4. Any COLLISION: stop that front, record verbatim, finish remaining fronts, flag paper_skeleton_v0.md §1/§9 for repositioning. Do not soften. A collision found by us is a citation; a collision found by a referee is a rejection.
5. STOP at the ledger. Skeleton edits are a separate approved step.
