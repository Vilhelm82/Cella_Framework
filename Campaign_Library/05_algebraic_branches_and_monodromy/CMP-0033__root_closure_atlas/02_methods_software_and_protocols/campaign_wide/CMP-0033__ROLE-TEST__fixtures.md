# root-closure-atlas — fixture taxonomy v1 (D4; FREEZE GATES ON WILL)

**Status: FROZEN v1 — Will's sign-off 2026-06-11 (machine date), both
deviations blessed; FXB4 added at freeze.** Source of truth: `manifest_v1.json` (sexprs, brackets, ℚ
roots, pathology annotations, facet tags, I2 encoding pins, PROBED lv3
expressibility — 32/32 graph lifts accepted live). Every constructed ℚ
root verified `f(x*) == 0` exactly in tests; every bracket's wall signs
verified exact pre-freeze. 32 pinned instances.

| Class | Instances | What it stresses | §17 hooks |
|---|---|---|---|
| FX-A simple | FXA1 (root 1/3 — non-representable), FXA2 (√2 — cell-only) | terminal cells non-trivial by construction | S1 lift validated |
| FX-B multiple | FXB2 (m=2, no sign change), FXB3 (m=3, 1/3), FXB4 (m=4, 1/3 — even × NON-dyadic: no crossing AND no float carries the zero; certificate `none`), FXB5 (m=5, dyadic) | even-m has NO crossing; Newton degrades | S2 dual-encoding pins on all four |
| FX-C clusters + Kerr | ε ladder 2⁻¹⁰…2⁻⁵² (3-root); Kerr Δ a→M: 2 resolved + extremal | A9 head-on; cluster-vs-multiple | S6 explicit-branch dual form; S8 grids |
| FX-D dyadic-exact | FXD1 (root = float), FXD3 (root at binade edge 2.0) | exact_zero certificates; cell degeneracy | — |
| FX-E ghosts | FXE1 ((x−1)²+2⁻²⁰⁰, expanded route), FXE2 (identity ghost, S10 regime ≥1.1e8) | exact f > 0; float "convergence" is a lie | S4/S10 pins |
| FX-F poles | FXF1 (root/pole interlace), FXF2 (POLE-ONLY sign change in bracket) | refusal certificates; bisection's classic lie | S4 |
| FX-G kinks | FXG1 (roots flank kink; bracket crosses it), FXG2 (tangency: exact zero, no crossing) | kink honesty | S5 contrast |
| FX-H Wilkinson | FXH1 (W20 ROUNDED coeffs, cell near 13), FXH2 (c₁₉+2⁻²³, surviving real cell near 8.9) | the honest machine question; backward error explicit | S7 |
| FX-I Newton pathology | FXI1 (2-cycle trap start pinned FIRST), FXI2 (basin boundary 1/√5 starts) | landing variability; S9 contrast row guaranteed | S9 |
| FX-J transcendental | sin(x)−x/2, exp(−x)−x, log(x)−1/2 | Arbiter-M territory; budget-relative later | — |
| FX-K route pairs | K1 expanded/factored (root 1/3); K3 c1/c2 sqrt-square chains | route fingerprints at the root level | B3/B4/B5 leverage |

**Certificates exercised by the taxonomy:** `sign_change_cell` (most),
`exact_zero` (FXD1, FXG2, FXC_kerr2 — the extremal Kerr merger point at
a = 1.0 exactly is an exact ℚ zero at the float 1.0), `refusal` (FXF2's
pole-borne crossing), `none` (FXE ghosts, FXB2's even multiplicity).

## Deviation from the brief (blessed at freeze, Will 2026-06-11)

The brief's FX-D lists three items; v1 carries two (**FXD1, FXD3** — the
numbering gap is deliberate). Item (b), "root engineered at a cell
wall", is the SAME predicate as item (a), "root exactly a float": a
terminal cell is an adjacent-float pair, so its walls ARE the floats —
any root at a wall is a root at a float, certified `exact_zero`. A
second instance would be a fixture that cannot distinguish anything
(HR129). Cut stands by ruling; the FXD2 slot stays reserved.

**Deferred to manifest v2 (noted, not smuggled):** complex-plane FX-I
fixtures; additional FX-H bracket cells (only the near-13 and near-8.9
cells are pinned in v1); **a subnormal regime-wall fixture** (the
genuinely distinct FX-D variant — cells in the subnormal range where
lattice spacing goes uniform; recorded as the v2 candidate at the FXD2
freeze ruling).
