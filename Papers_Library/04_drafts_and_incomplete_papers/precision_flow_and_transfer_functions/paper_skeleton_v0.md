<!-- NAMING (2026-06-11, Will): THE OBJECT is named **Cella** — the lane-carried exact account (value + account == TRUE in Q). Section-1 prose names her at first use; 'the account' remains the common-noun form thereafter. Glossary section 9 entry is canonical. -->
# PAPER SKELETON v0 — "The Precision Flow of Rounding Error"

**Status:** working skeleton (Claire draft, 2026-06-11, post campaign close). Not a manuscript. Every theorem below is already proved and/or campaign-graded; pointers map each claim to the artifact that owns it. Pre-submission checklist at the bottom is binding before anything leaves the building.

**Target:** research paper for the computer-arithmetic community (ARITH / IEEE TC class), with an arXiv preprint. The expository number-theory piece (Monthly-class) is PAPER 2, parked — see §10.

---

## 0. Title candidates (pick one, Will)

1. *The Precision Flow of Rounding Error: An Exact Dynamics for Round-off under Significand Refinement*
2. *Exact Dynamics of the Rounding Residual under Precision Refinement, with Applications to Computation Graphs*
3. *Reading One Bit at a Time: Refinement Dynamics of Round-to-Nearest* (warmer; better for the preprint title than the venue submission)

Recommendation: (1) for submission; the phrase "precision flow" is ours and should appear in the title we want cited.

## 1. Abstract (draft, ~190 words — tighten at submission)

> Fix a real number x and consider its round-to-nearest readings s_q = RN_q(x) as the significand precision q increases by one bit at a time. We show the rounding residual e_q = x − s_q obeys an exact one-line recurrence: in the normalized coordinate t_q = e_q/ulp_q, refinement acts as the re-centered angle-doubling map t_{q+1} = 2t_q − RNE(2t_q). Precision refinement reads the binary tail of x one bit per step; the residual is, exactly, the unread tail. Consequences follow at three levels. Free flow: ties resolve to grid ancestors; dyadic residuals die at finite precision, sharply; residuals of rational values are eventually periodic with minimal period equal to the multiplicative order of 2 modulo the odd denominator; irrational residual orbits have pairwise-distinct normalized values. Interacting flow: on computation graphs, where each node's exact intermediate is built from rounded parents, we prove a commutation criterion classifying exactly when a parent's reading shift is absorbed by the finer grid versus when the residual deviates, and a reconstruction theorem computing the entire refined graph state from carried state with zero re-execution. Scale structure: an exact ×2 discrete scale invariance with a complete homogeneity calculus and localized breaking. All claims are exact in ℚ; an exhaustive, byte-stable machine verification (several hundred thousand exact checks; zero tolerance parameters anywhere) accompanies the paper. We close by re-reading Ziv's strategy and the Table Maker's Dilemma as statements about the orbit.

## 2. Section map

**§1 Introduction.** The question (what happens to round-off when precision increases), why nobody has written the step law down (the field studies fixed-precision worst cases, not refinement dynamics), the three-level structure (free / arithmetic / interacting), and the verification philosophy (every claim exact in ℚ; no thresholds, no bands; receipts byte-stable). **Positioning thesis (Will, 2026-06-11, verbatim — the paper's spine):** "The refinement law itself is elementary once the precision ladder is made the object of study; the contribution is to identify that object, develop its orbit and graph interaction theory, and certify the resulting calculus exactly." The three verbs are the architecture: *identify* = §§2–3, *develop* = §§4–6, *certify* = §8. Lineage note — **manuscript wording (Will, 2026-06-11, verbatim):** "The move is analogous in spirit to Wilkinson's reframing in backward error analysis: the arithmetic is elementary once the right object is named. Here the object is not the fixed-precision residual, but its trajectory under significand refinement." The second sentence doubles as the EFT differentiation pivot in §9 and is the leading candidate for the abstract's compressed-thesis echo. (The earlier grander phrasing — "this is Wilkinson's move" — is retired to talks and firesides: this version claims kinship of method, not stature.) Echo a compressed form of the thesis in the abstract's final pass.

**§2 Setting and conventions.** 𝔽_q with q-bit significand, unbounded exponent (the e_min fence stated up front; two-parameter (q, e_min) flow declared future work). RNE. The quantum convention: u_q taken at **x's own binade** — state as a definition, prove straddle-safety as a lemma (receipt: Stage-A straddle battery, zero violations, no special-casing). t_q ∈ [−½, ½]. Notation table.

**§3 The Refinement Law (free flow).**
- **Theorem 1 (Refinement Law).** With D = RNE(2t_q) ∈ {−1,0,+1}: s_{q+1} = s_q + (u_q/2)·D, e_{q+1} = e_q − (u_q/2)·D, t_{q+1} = 2t_q − D. *Proof:* midpoint-insertion picture; four cases (hold / reflect / tie-to-ancestor / annihilate). Owned: covariance note §1; campaign Stage A (120,096 steps, 7 battery classes, zero violations).
- **Lemma 2 (Tie inheritance).** Refinement ties resolve to the coarse ancestor: a q-grid point written in q+1 bits ends in 0 (even); every midpoint ends in 1. Even-ness is inherited by grid ancestry.
- **Lemma 3 (Annihilation).** |t_q| = ½ ⟹ e_{q+1} = 0, permanently.
- **Corollary 4 (Bookmark identity).** t_q equals the re-centered fractional part of x/u_q: the residual is exactly the unread binary tail of the phenomenon. Remark: the doubling map's Kolmogorov–Sinai entropy log 2 is realized literally — one bit read per step. Owned: Stage B (141,766 exact identity checks across all battery classes incl. sqrt via algebraic comparison).
- **Corollary 5 (Dyadic death, sharp).** x dyadic of bit-length L ⟹ (e_q = 0 ⟺ q ≥ L). Owned: Stage A, both directions, 200/200.

**§4 Arithmetic of the orbit.**
- **Theorem 6 (Rational periodicity).** For rational x with odd denominator part b₀ > 1, the t-orbit is (purely, under §2 conventions) periodic with minimal period **ord₂(b₀)**. The doubling map restricted to denominator-b₀ rationals *is* multiplication by 2 on (ℤ/b₀ℤ)×; full-period orbits at primes with 2 a primitive root are complete tours (m-sequences). Cites the classical expansion theorem (Hardy & Wright ch. IX); the contribution is the corollary that **division residuals flow periodically in precision**. Owned: Stage B, 132/132 cases, equality not divisibility, orders to 946.
- **Theorem 7 (Irrational distinctness).** x irrational ⟹ the t_q are pairwise distinct (two-line proof: equal t's at distinct q force x rational via the strictly decreasing quantum). Strictly stronger than aperiodicity; makes the instrument self-policing. Owned: Stage B, 110/110, zero detections.
- **Remarks, carefully fenced:** equidistribution of irrational orbits ⟺ base-2 normality (Borel 1909 framework; the 1950 conjecture for algebraics) — OPEN, we claim nothing; Artin's conjecture adjacency for full-period primes — cited, not leaned on.

**§5 The interacting flow on computation graphs.** (The headline section.)
Setup: DAG; node phenomenon x_n(q) = op(parent **readings** at q); REFLECTS ⟺ own D ≠ 0; propagated shift δ_n = x_n′ − x_n, exactly computable from carried state.
- **Proposition 8 (Ancestry).** Residual deviation from the free law ⟹ some ancestor reflected. Owned: Stage C C-P1′, zero violations, all fixtures.
- **Theorem 9 (Commutation criterion / exact classification).** A node deviates at a refinement step **iff** x′ ≠ x and RN_{q+1}(x′) − RN_{q+1}(x) ≠ x′ − x. Equivalently: the deviating set equals the non-commuting subset of the reflectors' descendant closure — set equality, both inclusions. Owned: Stage C v2 C-P2′, zero violations.
- **Proposition 10 (Absorption characterizations).** (a) *Lattice equivariance:* shifts that are integer multiples of the (q+1)-quantum commute with RN (tie parity noted; the criterion form is tie-safe because it tests the fact). (b) *Additive edges:* δ/u′ = 2^(E_parent − E_child) — absorption whenever E_p ≥ E_c, i.e. **every cancellation edge absorbs**. (c) *Multiplicative edges:* absorption iff the co-operand reading is a power of two. Owned: Amendment-2 derivations + Stage C observational split (525 absorptions: 403 additive / 122 multiplicative) + Stage D ÷7 witness.
- **Theorem 11 (Reconstruction without re-execution).** The full (q+1)-state of the graph is exactly computable from the q-state, the Law, and reference rounding of the exactly-shifted intermediates — zero re-execution. Owned: Stage C C-P3, zero violations. (This is the result with algorithmic legs: a precision-sensitivity oracle at the cost of bookkeeping.)
- **Proposition 12 (Two deviation notions bifurcate).** Reading-deviation and residual-deviation coincide for fixed phenomena and bifurcate on shifted ones, with the exact identity **e_dev = δ − s_dev**; absorbed nodes are precisely reading-deviating and residual-serene. Include as a structural caution for implementers — this cost us a stage and will cost any reader who skips it. Owned: Stage C v1 finding + divergence identity, recount-verified.

**§6 Exact discrete scale invariance.**
- **Proposition 13 (Binade covariance, folklore formalized).** t invariant under x ↦ 2^k x.
- **Theorem 14 (Homogeneity calculus and localized breaking).** Weight calculus: leaves 1; constants 0; ± requires equal weights; × adds; ÷ subtracts; √ halves. Covariant ⟺ integer weight ⟹ t invariant under global leaf ×2^j. Multiplicative/divisive constants never break; breaking requires pinning an absolute scale (additive constants — "a mass term" — mixed-weight sums, odd-weight roots), and the broken set is contained in the breaker's descendant closure. Owned: Stage D, 35/35 pairs all j all q; containment 35/35; equality 32/35 observational.

**§7 Applications and discussion.**
- **TMD/Ziv in orbit language.** Hardness-to-round of f(x) at precision p = the depth at which the exact value's t-orbit exits the tie neighborhood; Ziv termination = first exit time; Lefèvre–Muller worst cases = inputs whose unread tail opens with the longest runs. One fully worked example re-deriving a known statement (the p + p′ accuracy condition) as an orbit statement.
- **Mixed precision.** "Will bumping precision change my downstream result?" — absorption is the exact selection rule; Theorem 11 is the cheap oracle. Sketch the procedure; defer empirical benchmarking to follow-up.
- **One contained paragraph:** the statistical-mechanics reading (dimensionful e irrelevant, t marginal, reflections as decimation events, DSI with literal period ln 2) — framed explicitly as a remark, not a claim. Keep the word *renormalisation* out of the title and abstract.
- **Limitations:** unbounded exponent (e_min axis = declared successor); rational-core + sqrt scope (certified-transcendental flow = successor); RNE only (other rounding modes conjectured analogous, untested).

**§8 Machine verification and reproducibility.** The methodology section the venue won't expect and should love: all-exact grading (zero band tests, zero thresholds, zero statistical verdicts), pinned literal batteries with hashes, frozen pre-registered predictions, byte-stable re-runs, counting-unit discipline. Counts table: 120,096 / 400 / 132 / 141,766 / 110 / Stage-C closures / Stage-D cells. Artifact availability statement (repo subset or archived bundle — decide at submission).

**§9 Related work.** See kill-list in §11; written as honest positioning, with Lefèvre's continued-fraction worst-case machinery called out as the closest prior *thinking* and differentiated cleanly (static inequality at fixed p vs. dynamics across p).

**§10 PAPER 2 (parked).** *Gauss in the Machine: the Number Theory of Rounding Errors* — Monthly-class expository: doubling map, ord₂ periods, full-period primes and m-sequences, the Borel–Artin corridor. Write after Paper 1 exists to cite.

---

## 11. Pre-submission checklist (binding)

1. **Kill-search, adversarial:** read Muller, *Elementary Functions* ch. 12; *Handbook of Floating-Point Arithmetic* (refinement/precision chapters); Lefèvre's thesis (continued-fraction fractional-part machinery — closest prior thinking, must cite and differentiate); the ACM Computing Surveys correct-rounding survey (hal-04474530) as the field map; targeted searches: "monotone with precision", "rounding error refinement", "residual orbit", EFT literature (Ogita–Rump–Oishi — their error term IS our residual; they never flow it). Any collision found ⟹ reposition honestly before drafting prose.
2. **IP review BEFORE preprint:** if reconstruction-without-re-execution or absorption-aware precision validation belongs in the patent family, a provisional goes in first. Publication is prior art against future claims; the 2027 conversions cover only what is already filed. One conversation with the attorney.
3. **Authorship & disclosure:** sole author W. Lloyd (Lloyd Geometric Diagnostics Pty Ltd). Decide the AI-assistance disclosure line (most venues now require one); draft: "Theorem statements and proofs were developed and verified by the author; an AI assistant was used for derivation checking, literature triage, and drafting support." Adjust to taste and venue policy.
4. **arXiv path:** cs.NA (primary) / math.NA; endorsement may be needed — identify an endorser or use the venue submission first.
5. **Venue timing:** check the current ARITH CFP (do not trust memory for dates); fallback/journal: IEEE Transactions on Computers or ACM TOMS. Preprint goes up regardless, after item 2 clears.
6. **Figures (draft list):** the midpoint-insertion four-case picture; a t-orbit cobweb (rational, period visible); the absorption anatomy (reading shift vs phenomenon shift); one graph timeline (reflections, absorptions, deviations across q); the DSI invariance table with the mass-term break.
7. **Scope sentences locked:** e_min fence; normality fence (with both Borel citations); ties-to-even assumption; RNE-only.

## 12. Open questions the paper may pose (and not answer)

- The two-parameter (q, e_min) flow across the subnormal boundary.
- Other rounding modes (directed rounding: the law's analogue is a pure shift map — conjecture, untested).
- Statistics of reflection/absorption events on random DAGs (the interacting flow's "thermodynamics").
- Formalization target: the Law and Theorems 9/11 look Coq/Flocq-sized (Boldo–Melquiond school) — a verified-arithmetic collaboration hook.
