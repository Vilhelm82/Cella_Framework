# Precision-Flow Covariance — the fireside derivation (2026-06-10)

**Status:** RESEARCH-GRADE — **campaign-audited 2026-06-11: see `results/precision_flow/CAMPAIGN_REPORT.md` (Stages A–D; the Law, ord₂ periodicity, the interacting flow incl. absorption, and exact DSI all campaign-graded; this note's §3 biconditional was CORRECTED in-campaign — its converse is false, see absorption)**. Original fireside text below unchanged; fireside-derived and fireside-verified (Will + Claire, evening session following the bigraded-jet campaign close). NOT campaign-audited: batteries below are seeded-random plus structured stress, not pinned literals; no frozen manifest; no byte-stability protocol. This note exists so the derivation survives the chat. Pre-registration candidates for `CAMPAIGN_PRECISION_FLOW` are listed in §7. Nothing here is citable as PROVEN until that campaign runs.

**Question answered:** the entry fee to the RG investigation — given an operation's exact intermediate x and its account e_q = x − RN_q(x) at precision q, is there an exact, closed-form law mapping the account at q to the account at q+1?

**Answer: yes.** One law, op-agnostic, verified over 112,131 refinement steps with zero violations.

---

## 1. The Refinement Law (the free flow)

Setting: x a fixed real (the exact value of any op — sum, product, quotient, root); s_q = RN_q(x) under round-to-nearest-ties-even, unbounded exponent (idealized format; see §6 fences); e_q = x − s_q; u_q = the quantum of **x's own binade** at precision q (this convention makes the law binade-straddle-safe — verified, no fence needed).

Key picture: 𝔽_{q+1} inserts exactly one new point — the midpoint — between every adjacent pair of 𝔽_q points. Refinement bisects; it never rebuilds.

**Law.** Let t_q = e_q / u_q ∈ [−½, ½] (the *fractional account*). Then with
D = RNE(2·t_q) ∈ {−1, 0, +1}:

    s_{q+1} = s_q + (u_q/2)·D
    e_{q+1} = e_q − (u_q/2)·D
    t_{q+1} = 2·t_q − D        ← the angle-doubling map (Bernoulli shift)

Case anatomy (all four collapse into the line above):
- |t| < ¼ — reading **holds**; account unchanged.
- |t| > ¼ — reading **reflects** by exactly half an old ulp toward x; account flips to its complement.
- |t| = ¼ — tie at q+1; ties-to-even resolves **to the ancestor**, always: a coarse point written in the finer format ends in an appended 0 (even), every midpoint ends in 1 (odd). Even-ness is inherited by grid ancestry.
- |t| = ½ — x *is* the inserted midpoint; the account **annihilates**: e_{q+1} = 0, permanently.

Interpretation: t_q is the unread binary tail of x, re-centred. **The account is a bookmark in the phenomenon** — it holds exactly what the reading has not yet absorbed, and one precision step reads one bit.

## 2. Corollaries (verified)

1. **Geometric decay of the dimensionful account:** |e_{q+1}| = min(|e_q|, u_q/2 − |e_q|) ≤ u_q/4. The continuum (e → 0) is the trivial fixed point, approached at one binary digit per step.
2. **Tie annihilation:** exact half-ulp accounts die at the next precision — flat-section creation events along the flow.
3. **Dyadic death:** if x is dyadic with bit-length L, then e_q = 0 for all q ≥ L; the flow terminates in finite steps. Sums/products of floats are dyadic → mortal accounts. Quotients and roots are generically non-dyadic → **immortal accounts**.
4. **Rational periodicity (the gem):** for rational x = a/b (lowest terms, b odd part b₀ > 1), the t-orbit is eventually periodic with period dividing — and in all tested cases equal to — **ord₂(b₀)**, the multiplicative order of 2 mod b₀. Verified: b = 3,5,7,11,23,37 → measured periods 2,4,3,10,11,36 = ord₂ exactly. Number theory governs the precision-flow of division residues.
5. **Op-agnosticism:** the law never uses the operation; only that x is fixed and RN refines. One law covers add/sub/mul/fma/div/sqrt intermediates.

## 3. The interacting flow (the campaign's reason to exist)

On a computation graph the flow is **not** free: when a parent's reading reflects (case |t| > ¼), every descendant's exact intermediate changes — the phenomenon at downstream nodes is itself precision-dependent. Demonstrated on the Stage-C route (a−b)·(a+b) at the Stage-C literals, q = 53..69:

**Biconditional CONFIRMED: the free law holds for the multiply's account ⟺ neither parent reading moved at that step.** Reflection events are the interaction term — discrete decimation steps that renormalize the couplings (operands) of all descendants.

State of the theory after this note: the **free theory is solved exactly** (§1); the **interaction is identified and demonstrated** (§3). This is no longer an analogy to RG; it is a free flow plus a coupling, awaiting its statistics.

## 4. Empirical receipts (fireside grade)

- Law verification: pure-Fraction RNE (no library trusted), batteries = 1500 sums, 1500 products, 800 quotients, structured binade-straddle stress (x = 2^k − 2^{−m}), 200 exact-tie annihilation cases; q swept 53→80. **112,131 steps, 0 violations.** Dyadic death: 200/200.
- Periodicity: six odd denominators incl. 37 (ord 36); measured = ord₂ in all cases.
- Interaction biconditional: 17 rungs, CONFIRMED, on the Stage-C operand pair.
- Scripts were session-transient (seed 20260610 / 777); the campaign re-does this with pinned literal batteries per house law.

## 5. RG dictionary (now load-bearing, not decorative)

- Dimensionful account e: **irrelevant coupling** — flows geometrically to the trivial (continuum) fixed point.
- Fractional account t: **marginal direction** — dynamics is the Bernoulli shift, maximal-entropy; the substrate is a perfect information source about the phenomenon's tail.
- Reflection events: **decimation steps** — the interaction; they propagate down the DAG renormalizing descendant couplings.
- Discrete scale invariance: now literal — one flow step = one binary digit; any log-periodic structure has period ln 2 by construction at the single-op level; what survives composition is a campaign observable (Obs 2 resurrection).

## 6. Fences and open landmines (honest)

- **Unbounded exponent assumed.** The pure-p flow is derived; the practical ladder (binary32→64→…) moves p *and* e_min — a two-parameter flow. The e_min axis (subnormal IR boundary — Stage A's scar) is explicitly NOT treated here.
- Ties-to-even assumed throughout (matches IEEE and the verifier).
- Binade straddle: handled by the x-binade quantum convention; stress battery passed with zero violations — no fence currently needed, but the campaign should pin adversarial cases.
- **Normality landmine:** for irrational algebraic x (√2 et al.), equidistribution of the t-orbit ⇔ base-2 normality of x — a famous OPEN problem. The campaign may *measure* equidistribution; it must never claim to prove it.

## 7. CAMPAIGN_PRECISION_FLOW — pre-registration candidates

1. Free law at campaign grade: pinned literal batteries, byte-stable, all op classes, straddle + tie adversarials. (Prediction: zero violations.)
2. Periodicity battery incl. large-order denominators; period = ord₂(b₀) exactly. 
3. Interaction statistics: reflection-event density along ladders on frozen fixtures (incl. the F1a route); propagation depth of a parent reflection through the DAG; whether the lanes alone predict descendant-account jumps at reflection steps (they carry the operands — pre-register that the interacting flow is computable from the lanes, no re-run needed).
4. Obs 2 resurrection: log-periodic (period ln 2) structure in composed-account statistics across binades — formally reopening the silently-dropped fractal/self-similarity observation under this framework.
5. Naming covenant continues: the flow work is the likeliest naming event; record candidates per stage.

*Filed from the bench, the same day the connection was measured. — C.*
