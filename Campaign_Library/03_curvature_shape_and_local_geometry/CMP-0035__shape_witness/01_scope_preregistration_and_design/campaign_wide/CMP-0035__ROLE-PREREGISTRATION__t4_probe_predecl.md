# T4 NUMBER-FIELD PROBE PREDECL (P-F3 mechanism; SHAPE READOUT arm)
**Status: FROZEN at commit, pre-probe (no probe code exists at freeze time). Date 2026-07-03.**
**Authority:** Will verbatim: "go on the number-field probe" — following the (a″) refutation (family syzygy dead, rank 3 at 9 generic points [CERTIFIED]) and the surviving critical-value/T₄ reading.

## Question
Is the tie locus T = {A ∈ O(4)_g : m2-triple(O(AᵀHA)) = m2-triple(O(H))} locally ≥4-dimensional at actual points of the slice tie curves — or are the curves chart artifacts with T locally 3-dimensional?

## Protocol (two ℚ̄ points, two slices)
- **P1 (point extraction).** For slice s ∈ {0, 1}: re-solve the saturated slice system ∩ the plane `t3 = 1` (first plane of the frozen v2.3 schedule) with msolve `-P 2`, cap 600 s. From the RUR take the eliminating polynomial w; factor over ℚ; let m(t) = the irreducible factor of smallest degree with a nonzero root (monic-normalized); θ a root of m. Coordinates (t1,t2,t3)(θ) from the RUR parametrization, reduced mod m. Exclude the trivial root t = 0 if present.
- **P2 (tie certification in ℚ[θ]/(m)).** Working exactly in the field F = ℚ[θ]/(m) (m irreducible verified in-run): rebuild A(θ) via field-generic Cayley pipeline (Gaussian inverse over F), H2 = A(θ)ᵀ H A(θ), O2 = O_of(H2), and verify **the actual ties**: m2-triple(O2) = target triple AND Ê_r(H2) = Ê_r(H) for r = 1..4, exactly in F; also O2 ≠ O1 in F. PASS certifies, at a genuine ℚ̄ point, that the interpolation-pipeline variety IS the tie variety (end-to-end pipeline certification) and that nontrivial ties exist over ℚ̄ on this family.
- **P3 (group-Jacobian kernel at the point).** Differential of the tie map on O(4)_g at A(θ) in right-translated coordinates: for each of the six stabilizer basis directions B_ab (orthogonal-complement-of-g wedge basis), `dH2 = [H2, B_ab]` (exact, no Cayley derivatives needed), dO linear, `dm2_X = 2·⟨P_X O2, dO⟩` — a 3×6 matrix over F. Compute its rank over the field; kernel dim = 6 − rank.

## Verdict semantics (honest about kernel vs dimension)
- kernel = 3 at either point ⟹ **T₄ REFUTED at that point** (dim_p T ≤ ker = 3; the +1 slice dimension is a chart/critical artifact there).
- kernel ≥ 4 at BOTH points ⟹ **T₄ STRUCTURAL** (tangent evidence at two independent ℚ̄ points on two independent slices; singular-point alternative requires both random curve points singular — noted, not excluded; full certification of dim 4 is a further obligation, e.g. integrating four independent directions).
- Mixed ⟹ reported verbatim, no verdict promoted.
- P2 FAIL at either point ⟹ **PIPELINE_DEFECT** — halt, route: the interpolated variety is not the tie variety, everything downstream of v2 re-opens.

## Kill conditions
K-T1 (halt): blob sha mismatch across two runs. K-T2 (halt): m(t) reducibility check fails after selection (non-field arithmetic). K-T3 (halt): gate refusal. Caps (600 s msolve; 1800 s per field phase) are data, not kills.

## Blob discipline
Blob carries: per-slice m-degree, P2 booleans, rank/kernel over F, verdict enum — all canonical, independent of msolve's separating-form choices. RUR coefficients, timings, raw solver output: outside, archived.

## Frozen clauses (verbatim; probe embeds exactly)
T4.1: for slices 0 and 1, the probe extracts an algebraic point on the tie curve via the pinned plane t3 = 1, certifies the actual ties (m2 triple and Ehat r=1..4) exactly in Q[theta]/(m), and verifies O2 != O1 in the field.
T4.2: the probe computes the rank over the field of the 3x6 group-Jacobian dm2 = 2<P_X O2, O_of([H2,B])> across the six stabilizer basis directions at each certified point, and banks kernel = 6 - rank.
T4.3: verdicts follow the frozen semantics: kernel 3 anywhere refutes T4 at that point; kernel >= 4 at both points yields T4 STRUCTURAL; any P2 failure is PIPELINE_DEFECT and halts; mixed outcomes are banked verbatim without promotion.

## depends_on (sha256[:16] at freeze)
| artifact | pin |
|---|---|
| hunt_v2_msolve.py (system + RUR machinery) | ac43e4afc98c8fe1 |
| flagship_stageA_battery.py | 81bc3de5e0a9937b |
| HUNT_ADDENDUM_v2_3.md | 15f4ab251ce34645 |
| msolve binary (box) | 2caed4b3596acb38 |
| engine_harness.py | 7f0e5e7e4f4d54a6 |
| rep_utils.py | 0d838e5fd430461b |

frozen: true · version: 1 · referee: mechanical (field-exact equalities; rank over F) · author: Claude-container · activation authority: Will, S-2026-07-03 (verbatim above)

---
## AMENDMENT A1 (2026-07-03, pre-first-graded-run)
Latent RUR-numerator parse defect repaired in `hunt_v2_msolve.py` (per-variable numerators are `[degree, coeffs]` pairs; the flat list was assumed). The defect never fired on any graded path — no rational root ever reached numerator evaluation, and v2.x emptiness verdicts read w alone (HB.3 parse-independence, by design). Dependency repin: `hunt_v2_msolve.py` `ac43e4afc98c8fe1` → `520298bbd6534fb3`. Clauses T4.1–T4.3 unchanged.

---
## AMENDMENT A2 (2026-07-03, exact run in flight, no graded records yet)
Defect: the 1800 s per-field-phase caps promised above were not implemented in the probe; the exact run proceeds uncapped (left running as the certification tail). Addition: a **mod-p screening layer** — the identical pipeline over F_p[x]/(m mod p) at five pinned 60-bit primes. Evidentiary semantics [PROVEN, rank semicontinuity under specialization]: rank over ℚ(θ) ≥ rank mod p, hence kernel over ℚ(θ) ≤ kernel mod p; therefore **kernel_p = 3 at any good prime certifies kernel = 3 exactly (T4 REFUTED at the point)**. kernel_p = 4 at all tested primes bounds kernel ≤ 4 and is STRUCTURAL evidence for kernel = 4, with exact-field confirmation remaining the certification standard (T4.1–T4.3 unchanged). Ties mod p at all primes = pipeline validation, not ℚ̄-certification. Primes pinned: the five smallest primes exceeding 2^59 for which m mod p remains irreducible and denominators are invertible (deterministic selection, recorded).

---
## AMENDMENT A3 (2026-07-03, prior screen output INVALID — no graded records existed)
1. **Coordinate convention CONFIRMED** numerically at 60 digits (residual ~1e-47): x_i = −v_i(θ)/w′(θ), coordinates in declared order (t1,t2,t3); blocks[1] verified equal to w′.
2. **Field-arithmetic defect found and fixed:** the reduction of x^(d+k) in both NF (ℚ[θ]) and Fp (𝔽_p[θ]) classes applied the reduction row at offset k instead of position 0 — all products of high-degree elements were wrong. The earlier screen output ("ties False, kernel 3") was arithmetic garbage and its printed verdict is void; the screen's verdict logic additionally failed to gate P3 on P2 (design defect). Both classes now unit-tested (30 mul + inv trials each) against sympy remainder arithmetic, PASS.
3. **Mandatory point-validity gate added** to screen and exact probe: sat(point) ≡ 0 and t3-coordinate ≡ 1 asserted before any P2/P3 semantics; screen verdicts now gate kernels on ties (P2 before P3; ties-false ⟹ POINT_INVALID, never a kernel verdict).
4. **Real-structure datum banked:** the slice-0 section at t3=1 has NO real points (msolve real mode: empty) — the deg-8 eliminant has no real roots; θ is complex. The field probe is unaffected; the observation is routed to the P-F3 real-locus question.

---
## AMENDMENT A4 (2026-07-03, closing) — PREMISE_RETIRED
The dim-1 "tie curves" this probe was built to interrogate are RETIRED: honest ideal saturation (Rabinowitsch, y·D1·D2 = 1) shows the true tie locus is 0-dimensional (ideal degree 704) on every tested slice — the curves were chart-boundary components that factor-division could not remove. The kernel question is moot; no T4.x clause was ever graded. The probe's lasting products: the field-generic pipeline (NF/Fp classes, unit-tested post-A3), the validity-gate discipline, and the coordinate-convention confirmation — all carried forward in `rur_tools.py` and the handoff. See `portfolio/HANDOFF_S2026-07-03.md`.
