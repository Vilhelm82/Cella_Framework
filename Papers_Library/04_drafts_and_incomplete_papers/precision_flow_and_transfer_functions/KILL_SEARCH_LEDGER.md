# KILL_SEARCH_LEDGER v1 + CLAIRE REVIEW — Precision-Flow Paper (2026-06-11; migrated to repo 2026-06-12)

Companion brief: `Build_Docs/Reports/precision_flow/KILL_SEARCH_BRIEF.md`. Runner: CC with web access. Reviewer: Claire.

## PART 1 — LEDGER AS EXECUTED (verbatim)

FRONT 4 — Correct rounding / TMD (home crowd, highest collision risk)
Verdict: ADJACENT (mandatory cites, no collision).
- Ziv 1991 ("Fast evaluation of elementary mathematical functions with correctly rounded last bit", ACM TOMS): strategy of extra-precision evaluation + final rounding; about termination of an escalation loop, not a step law or residual recurrence across precisions. No iteration of the fractional-part quantity as a dynamical system; no exit-time/orbit framing of hardness.
- Lefèvre (2000/2006 papers + thesis-related work, e.g. "Worst Cases for Correct Rounding of the Elementary Functions in Double Precision" with Muller): continued fractions + three-distance theorem to find hard-to-round cases at a FIXED target precision. Purely static machinery for worst-case identification. No dynamics across p, no recurrence for the residual during escalation, no hardness as orbit exit time.
- Muller Elementary Functions ch. 12 + Handbook of FP Arithmetic correct-rounding chapters + ACM Computing Surveys correct-rounding survey (hal-04474530 / Brisebarre et al.): TMD/Ziv as static analysis or termination strategy at target p. No step-to-step residual evolution, no orbit language.
Drafted §9 differentiation sentence (SUPERSEDED — see review): "…makes that depth computable rather than exhaustively searched."
No collision on Theorems 1, 4, 6, 7, 9, or 11.

Double-rounding (part of FRONT 7 wildcard)
Verdict: ADJACENT (mandatory cite + explicit differentiation).
Figueroa (1995) "When is double rounding innocuous?" and Boldo–Melquiond ("When double rounding is odd", etc.): when rounding to an intermediate precision then final equals direct rounding (composition RN∘RN). Differentiation: our law concerns refinement RN_q(x) → RN_{q+1}(x) of the SAME exact x; double rounding concerns composition through an intermediate format. Lemma stock overlaps; objects distinct; cite and move on. No collision.

FRONT 1 — Constructive / exact real arithmetic (Boehm school)
Verdict: CLEAR on collision shape; ADJACENT on API ideas.
Boehm PLDI 2020 + related exact-real work: lazy/interval semantics, caching of decisions; incremental precision via caching/scaling, but no exact one-step state reuse via a canonical RN doubling rule, no orbit/periodicity remarks for the residual in RN terms, no round-to-nearest canonical requirement per step.
Differentiation if citing: "Exact-real APIs emphasise lazy or interval semantics with caching; our framework stays inside IEEE-754 round-to-nearest and derives an exact dynamical system on the residual under significand refinement." No collision on the Refinement Law or reconstruction.

FRONT 2 — iRRAM / computable analysis (Müller, Weihrauch TTE)
Verdict: CLEAR.
iRRAM: reiteration with increasing precision, caches discrete decisions; no exact state-reuse theorem computing the higher-precision run from the lower via the doubling map. Weihrauch TTE proves canonical binary expansions are not admissible (multiplication-by-3 pathology) — the §9 framing citation: the field proved the object "hostile" then stopped. No residual-dynamics/orbit statements under refinement in the TTE corpus.
Differentiation: "The classical admissibility results show why binary expansions are inconvenient; we turn the inconvenience into an instrument by exhibiting the exact refinement law on the residual."

FRONT 3 — Online / MSD-first arithmetic (Ercegovac school)
Verdict: CLEAR.
Online arithmetic requires redundant representations for bounded-delay MSD-first addition; non-redundant standard binary has fundamental delay issues (formally stated). No event calculus for non-redundant refinement resembling reflections/absorption. Online-delay theory is redundant-representation-only.

FRONT 5 — Adaptive / expansion arithmetic (Shewchuk, Priest, EFT)
Verdict: CLEAR on dynamics; ADJACENT on adaptive stages.
Shewchuk 1997: expansions with staged refinement for robust predicates; error bounds per stage, no residual recurrence law relating stage residuals; the expansion tail is summed, not flowed. EFT literature (Ogita–Rump–Oishi etc.): residual at fixed precision; never flowed across precisions.

FRONT 6 — Precision-driven expression DAGs (Yap CORE, LEDA::real, separation bounds)
Verdict: CLEAR.
Bounds propagation / precision requests / recomputation. No exact state reuse across levels; no node-level classification of deviate-vs-absorb under precision increase. Separation bounds static.

FRONT 7 — Wildcard sweep (Gosper, Kahan, arXiv, stochastic, Flocq)
Verdict: CLEAR on core claims; ADJACENT on double-rounding lemmas + folklore.
Gosper CF arithmetic: different object. Kahan notes: folklore, no systematic refinement dynamics. arXiv 2020–2026 sweeps: nothing matching the one-line law or graph interaction theory. Stochastic rounding: different model. Flocq: round_round / double-rounding (composition) lemmas only; no succ_prec-style refinement map for the same x.

FINAL DISPOSITION (as executed): documented silence across all seven fronts with page-level / source-level receipts (abstracts, known results, primary paper summaries, and targeted searches). No COLLISION on Theorems 1–14. The skeleton does not need repositioning. The contribution (identify the refinement object, develop its orbit + graph theory, certify exactly) stands as novel.

## PART 2 — CLAIRE REVIEW (2026-06-11)

GRADE: ACCEPTED as the search-phase verdict. No COLLISION on Theorems 1–14; novelty thesis stands; DRAFTING IS GREEN.

UNIT-DISCIPLINE ANNOTATION (binding): the disposition self-describes its receipts as "abstracts, known results, primary paper summaries, and targeted searches" — by the brief's own grammar this is SEARCH-unit, not READ-unit. Fronts 3, 5, 6 and most of 7: CLEAR at search-unit suffices. The three highest-risk corners are re-graded CLEAR-PENDING-DEEP-READ, with residues:
  R1. Lefèvre thesis chapters (continued-fraction / three-distance machinery): confirm static-in-p at page level; while there, MINE the three-distance theorem as potential toolkit for our own orbit statements.
  R2. Boehm PLDI 2020, caching/scaling sections: answer falsification question 1c at page level.
  R3. Flocq source grep (cheapest, most decisive — do first): search the .v files for any lemma relating round at precision p and p+1 of the SAME x. Source code cannot equivocate.
Residues R1–R3 are PRE-SUBMISSION obligations, not pre-drafting blockers.

DIFFERENTIATION FIX (Front 4, required — adopt verbatim in skeleton §9): "Ziv's strategy and the Lefèvre–Muller worst-case programme identify inputs whose unread tail is longest at a fixed target precision; we reframe hardness-to-round as the depth at which the exact t-orbit exits the tie neighbourhood, and supply the one-step law that governs the escalation every implementation already performs." (The executed draft's "computable rather than exhaustively searched" overclaims — it reads as obsoleting the worst-case programme; per-input exit time is comparable work to Ziv's escalation, and the global worst case still requires search.)

KEEP VERBATIM: Front 2's "we turn the inconvenience into an instrument"; Front 1 and double-rounding differentiation sentences.

NEXT ACTIONS: brief + ledger migrated (done 2026-06-12); absorb differentiation sentences into skeleton §9 (with the Front-4 replacement); R3 Flocq grep at next convenience; begin §1 prose. Drafting is GREEN.
