# difference-tower — Stage A report v2 (H1 full grid + H3 two-sided)

**Status: STAGE A CLOSED — ALL PASS at v2 under Will's ruling (b)
(brief §7A Amendment 2). v1 chain preserved verbatim as finding #1.**
**Date:** 2026-06-12. **Branch:** `campaign/difference-tower`.
**Pins:** prereg v1 `216bc623dbcbd1825e83d4725d4af87f4a692cd62b10f58dc5e9326b6f0ac21a`
(preserved: `prereg_v1.json`, `prereg_sha256_v1.pin`); prereg v2
`50dfce689a7ca3a8d8ec42f0542d1641d36fc5d693c0c120fe6928792de0af3a`.

## 1. Finding #1 — the v1 chain (preserved verbatim)

The v1 prereg's expectation "zero refusals" was unsound: its dry-run
validated lattice membership but not domain membership. One pinned cell —
(R3, x=0.5, backward, j=2, m=6), last stencil node 0.5 − 6·0.25 = **−1.0,
R3's true pole** — drew a dual matching typed refusal (lane
`div_by_zero_float`, referee `div_by_zero_true`; nothing silent). Zero ℚ
inequalities existed; K1 was never triggered; the runner's v1 headline
"K1 HALT" over-claimed (conflated refusal count with the kill
definition). v1 artifacts untouched on disk: `prediction_verdicts.json`,
`records/stage_a_h1_grid.jsonl`, `records/dp2_refusal_log.json`; surprise
ledger Entry 1; characterization per fork §1.7.

**Standing law (Amendment 2, carries ruling (a)'s semantics):** a dual
matching typed refusal at an exactly-verified domain violation is a
lawful domain event, not an H1 counterexample. Any post-v2 runtime
refusal is an anomaly → fork §1.7, route to Will.

## 2. The v2 chain — ruling (b) executed

1. **Prereg v2:** dry-run gained exact ℚ domain membership
   (`in_domain_exact`: denominator ≠ 0 at every stencil node, decided by
   the pure-ℚ referee). Excision is RULE-BASED via the single-definition
   predicate `tower.stencil_in_domain` (generator AND runner consume the
   same rule; nothing hand-enumerated). The rule excised **1 cell** —
   independently reproducing v1's refusal location, confirming the
   characterization.
2. **Runner fix:** kill headlines now derive mechanically from the kill
   definitions (K1 = ℚ inequality present), never from verdict flags;
   post-v2 refusals headline as ANOMALY and halt for Will.
3. **Re-run:** **H1 v2 PASS — 9872/9872 cells equal bit-for-bit in ℚ**
   (units: fixture × point × scheme × j × m cells); 1 cell excised by
   the domain rule; **0 anomaly refusals; 0 DP2
   below-sufficient-condition firings**. Byte-stable ×2; records sha
   `b23294c9911c27f38735164c1731609aed2c277621907c6ea6c9b2929acbc816` —
   **byte-identical to the v1 records**, since v1's records contained
   exactly the 9872 computed cells: the records themselves certify the
   rule removed precisely the refusal cell and nothing else.

## 3. H3 — stands at v1 by ruling (cells unaffected, rules unbroken)

Carried forward by citation, not re-run: **PASS two-sided** — positive
8/8 fixtures (P0–P4, P10 at d=10, R2a/R2b functional cubics; Δ^(d+1) ≡ 0
at every cell; degree exactness everywhere); negative 24/24 probe rows;
certificates exact (P0→0 … P10→10, R2a/b→3, None on every negative
fixture); **zero false positives — K2 clean**. Source:
`prediction_verdicts.json` (v1), Stage-A v1 records.

## 4. Stage-A close state

- H1: **PASS** (v2, 9872/9872 cells) — K1 never triggered in either run.
- H3: **PASS** (v1, standing) — K2 never triggered.
- v1 FAIL chain preserved verbatim as finding #1 with both pins cited.
- Full suite exit 0 after v2; registry unchanged; H4 rules untouched;
  fences (B7, R9, invariant hunt, task015) not approached.

**Stage A CLOSED. Stage B (H2 only) GO per Will's instruction — prereg
first.**

— Claire, on the bench, 2026-06-12.
