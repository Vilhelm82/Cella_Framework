# difference-tower — Stage E report (H7 duality + transcendental annex)

**Status: STAGE E COMPLETE — exploratory, no kill attached, all findings
positive. E-P1 7/7 battery points within declared floors; E-P2 216/216
nodes within the exposure bound, zero zero-exposure damage; E-P3 12/12
enclosure cells contained. STOPPED at this report per the GO.**
**Date:** 2026-06-12. **Prereg:** frozen first (informativeness law run),
pin `85ec8e27…849c2b`. **Records:** sha256 `2e671390…61abbe`,
byte-stable ×2. Suite exit 0.

## 1. E-P1 — jet–tower duality: **7/7 within declared floors**

The HR131 jet's derivative value and the tower's law-extrapolated limit
agree at every smooth battery point, within class-derived floors:
polynomials via the exact Newton-inversion limit (floor = jet float
headroom only, ~1e-15 — and the gap fit inside it); rationals via the
deep lane centered cell (j = 40); annex via the Stage-D Tier-2 estimate
(floors ~1e-8, gaps inside). Two instruments, two architectures —
forward-mode AD on the float path vs exact finite differences on the
lattice — auditing each other and agreeing to their joint precision.
H7's first leg: each instrument audits the other, and both pass.

## 2. E-P2 — EXPOSURE/damage correspondence (recorded): clean

On the R2 pair grid: realized node deviation |δ| sat within the
account's exposure bound at **216/216 nodes** (max ratio 0.827 — the
bound is tight but never violated), and **zero cells with
zero-exposure stencils showed damage** — where the account says nothing
happened, nothing happened. The jet/lane exposure account is a sound
damage predictor on this grid.

## 3. E-P3 — annex enclosures via the certified elementary set: **12/12 contained**

TRUE(node) enclosed by the V4-native certified instruments (typed_sin /
typed_exp / typed_log over typed_refine, HR123–128 — consumed, not
re-derived) at 120 bits; cell enclosures by exact-ℚ interval
differencing. Every refined cell's enclosure contained the mp 240-dps
value; zero refusals; widths ~1e-30 at the worst (j=9, m=2) cells. The
transcendental annex now has a certified-enclosure story for tower
cells, ready for the atlas seam.

## 4. Disclosures (implementation defects, fixed pre-report)

1. **E-P3 scaling bug:** first run divided the mp comparison value by h
   once instead of h^m — exactly the m=2 cells failed containment
   (6/12). Fixed; 12/12.
2. **Jet value-column field name:** `jet_column` read a nonexistent
   `.g` attribute (the field is `.gradient`), so E-P1's first run had
   no jet values — and **the Stage-D head-to-head records carry the
   same defect**: their `g` column is None everywhere. ERRATUM, not a
   re-grade: the head-to-head was recorded-not-graded, the jet STATUS
   column (the dead-mode contrast) was correct throughout, and the
   kink-row g=None entries are genuinely dead. The committed Stage-D
   records stand verbatim; corrected jet values for the smooth controls
   are in this stage's E-P1 records.
3. E-P2's exposure bound includes the exact deviation term alongside
   the per-entry residues (conservative by construction); recorded as
   the bound's definition, max ratio 0.827 measured against it.

## 5. Stage-E close state

All seven hypotheses have now been executed: H1/H3 (Stage A v2), H2
(Stage B v2, closed scoped), H6 (Stage C, all-pass — the inversion),
H4/H5 (Stage D + Amendment-6 leg — zero wrong clean emits; conditional
law two-sided), H7 (this stage — positive findings, no kill). The
campaign's Close stage (discipline §3 synthesis, successor doors,
ledger close-text) awaits Will's word per §9 — not entered here.

— Claire, on the bench. STOPPED at the Stage-E report per the GO.
