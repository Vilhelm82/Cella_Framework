# Precision Flow — Stage B Report (arithmetic of the orbit)

**Date:** 2026-06-11 · **Manifest:** frozen pre-implementation, pinned; batteries literal (132 rational cases over 15 denominators incl. 907/941/946-order monsters; 110 sqrt non-squares); transients DERIVED at freeze (odd denominator ⇒ pre-period 0; no free parameter) · **Verdicts (mechanical, byte-stable):** B-P1 **PASS** · B-P2 **PASS** · B-P3 **PASS** · full suite green, exit 0.

## Results

- **B-P1 (periodicity = ord₂):** 132/132 — every rational case's measured minimal t-orbit period EQUALS the frozen ord₂(b₀), including ord 906 (b₀=907), 940 (941), 946 (947) over ~1950-step windows. Equality graded by exhaustive smaller-P refutation: any P < ord passing would have failed the case. Number theory governs the precision-flow of division residues — now campaign fact, not fireside observation.
- **B-P2 (the bookmark identity):** **141,766 checks, zero failures** — t_q equals the re-centered fractional part of x/u_q exactly in ℚ, across the Stage-B rationals AND all seven re-swept Stage-A batteries (under their pins), with the sqrt classes graded in the manifest's comparison form (independent floor + midpoint comparisons vs the referee's choice). The account IS the unread tail — a theorem-level identity, graded.
- **B-P3 (distinctness lemma, adopted form):** 110/110 sqrt cases — all 28 window t-values pairwise distinct by exact comparison (the t_q1 = t_q2 rational-comparison criterion derived in the manifest). **Zero periodicity detections**: the orbit machinery is clean, per PF-2 any detection would have been an instrument defect and stopped the stage.

## Observational deliverable (NO VERDICT)

`observational_t_distributions.json` — empirical t-histograms per battery class, labeled OBSERVATIONAL, the normality fence (PF-4, Borel, OPEN) cited inline. The word "equidistributed" appears in no verdict.

## Names that fell out (collected, NOT adopted)

- **"the metronome"** — the large-order cases ticking through periods 906/940/946 with the regularity of clockwork; the orbit extractor's window logic kept reading as beat-counting.
- Standing candidates carried; the bookmark/unread-tail pair from Stage A grew stronger — B-P2 made the bookmark literal.

## State

Stage B closed pending Will's review. Stage C (the interacting flow on graphs — the campaign's crown) awaits GO.
