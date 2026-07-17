"""Stage-B prereg generator (H2 ONLY — convergence law + self-pricing).
Deterministic; pinned literals; zero RNG. Frozen before execution per
Will's Stage-B GO (2026-06-12).

Grading seam (brief §0 rule 1, GO verbatim):
  EXACT side (zero band tests): the d ≤ 4 self-pricing identity and the
  Newton falling-factorial inversion, both bit-for-bit in Q.
  ARBITER side (bands lawful): Taylor-order slopes measured by the
  CONSUMED chain typed_finite_difference → typed_collection →
  typed_log_log_slope (never re-derived), and the analytic next-term
  band rules with mpmath-arbiter coefficients.

The freeze dry-run is referee-class and refuses to pin an unsound
prereg: it verifies f″ ≠ 0 and f‴ ≠ 0 EXACTLY at every lane
slope-battery point (a vanishing leading coefficient would change the
predicted order — the slope leg must be falsifiable, HR129), checks the
annex battery the same way through the mp arbiter, and self-checks the
Newton inversion identity on one pinned case (the bigraded Stage-A
misquoted-theorem lesson: verify the cited identity before freezing it).

Math cited, never re-derived: forward Taylor pricing
Δ¹/h − f′ = Σ_{k=2..d} h^(k−1)/k!·f⁽ᵏ⁾ (Taylor with exact terminating
sum on polynomials); derivative-from-differences inversion
hD = ln(1+Δ) ⇒ f⁽ᵏ⁾ = (k!/h^k)·Σ_{i=k..d} s(i,k)/i!·Δ̃^i with s(i,k)
the SIGNED Stirling numbers of the first kind (Jordan, Calculus of
Finite Differences, the classical operator identity; finite on
degree-d polynomials since Δ̃^i ≡ 0 for i > d).

Run: ``python -m lloyd_v4.evals.difference_tower.make_prereg_b``
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

STAGE_B_DIR = (Path(__file__).resolve().parents[3].parent
               / "results" / "difference_tower" / "stage_b")

# --- exact legs: fixtures of functional degree d <= 4 ----------------------
IDENTITY_FIXTURES = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "P4": 4,
                     "R2a": 3, "R2b": 3}
IDENTITY_J = [2, 5, 9, 14, 20]          # wide dyadic points
IDENTITY_J_TIGHT = [8, 10, 12]          # the RN(1/10) point (P2)

# --- arbiter leg 1: lane slope battery (Q-exact deviations, measured
# through the consumed float-domain instruments) ----------------------------
LANE_SLOPE_BATTERY = [
    ["P3", "0x1.0000000000000p-1"], ["P3", "0x1.4000000000000p+1"],
    ["P4", "0x1.8000000000000p-1"], ["P4", "-0x1.8000000000000p+0"],
    ["R1a", "0x1.8000000000000p-1"], ["R1a", "0x1.4000000000000p+1"],
    ["R3", "0x1.0000000000000p-1"], ["R3", "0x1.4000000000000p+1"],
]
LANE_SLOPE_J_WINDOW = list(range(6, 17))   # h = 2^-j, 11 ladder points

# --- arbiter leg 2: annex (raw towers vs mp arbiter) ------------------------
ANNEX_SLOPE_BATTERY = [
    ["T1", "0x1.0000000000000p-1"], ["T1", "0x1.4000000000000p+0"],
    ["T2", "0x1.0000000000000p-1"], ["T2", "-0x1.8000000000000p+0"],
    ["T3", "0x1.0000000000000p-1"], ["T3", "0x1.4000000000000p+1"],
]
ANNEX_SLOPE_J_WINDOW = list(range(2, 11))  # truncation >> float noise here

PREREG = {
    "campaign": "difference_tower",
    "stage": "B",
    "version": 2,
    "frozen": False,
    "date": "2026-06-12",
    "v1_pin_preserved": "dca8eb406211b51485f2eb53bb15abe5193fe494de86fb174144668ddbf56b07",
    "amendment_3": "Will's ruling (a) 2026-06-12 (brief 7A Amendment 3): "
                   "v1 B-P3/B-P4 FAIL chain preserved verbatim as Stage B "
                   "finding #1 (r2 definitionally uninformative on the "
                   "near-zero transfer slope of a forward alpha=1 law; "
                   "second documented envelope-category-error instance). "
                   "r2 REMOVED uniformly across schemes. v2 re-runs the "
                   "slope legs ONLY; B-P1 (73/73) and B-P2 (166/166) "
                   "exact-leg verdicts STAND, carried by citation.",
    "v2_slope_acceptance_two_leg": {
        "consumption": "directional_alpha_probe (the SAME chain "
                       "typed_finite_difference -> typed_collection -> "
                       "typed_log_log_slope, now consumed through the "
                       "instrument that carries the declared-uncertainty "
                       "calculus: observed_alpha = slope + 1, "
                       "propagated_window_error, alpha_stability_status, "
                       "declared-model classification). eta = 1e-6 (= v1 "
                       "delta_ratio): measurements identical to v1 by "
                       "construction - acceptance changed, data did not.",
        "leg_i_correctness": "one DeclaredAlphaModel per (scheme): "
                             "alpha = alpha_pred, band = pinned tol (lane "
                             "0.05 / annex 0.10, as registered in v1). "
                             "PASS iff the chain selects the declared "
                             "model (selected_alpha_model == declared name; for "
                             "integer alphas the chain's consistent "
                             "outcome status is alpha_regular_integer). "
                             "Equivalent to |alpha - alpha_pred| <= tol.",
        "leg_ii_trust": "CAMPAIGN_DISCIPLINE section 4 calculus: the "
                        "chain PROVIDES propagated_window_error (V4's "
                        "honest declared uncertainty; standard_error "
                        "fallback NOT needed - field present), plus the "
                        "stability stratum. PASS iff "
                        "alpha_stability_status == stable AND "
                        "propagated_window_error <= tol (the declared "
                        "uncertainty must support the tolerance at which "
                        "leg i is claimed - a verdict claimed at tol with "
                        "declared uncertainty > tol would be a "
                        "wrong-clean-emit shape). NOTE: alpha_pred-inside-"
                        "propagated-error is deliberately NOT the test: "
                        "the prediction is asymptotic, the measurement is "
                        "window-local (higher-order Taylor bias is real "
                        "and budgeted by leg i's tol).",
        "r2": "REMOVED uniformly (Amendment 3): a statistic valid only "
              "conditionally on the law under test is unsound as a "
              "frozen criterion.",
    },
    "scope": "H2 ONLY (Will's Stage-B GO): convergence law + "
             "self-pricing. H1/H3 closed at Stage A v2.",
    "authority": "Build_Docs/Agent_tasks/CAMPAIGN_DIFFERENCE_TOWER.md "
                 "section 7 H2 + 7A Amendments 1-2; Will's Stage-B GO "
                 "2026-06-12 (prereg first; seam holds; BOUNDED firings "
                 "logged; STOP at the Stage-B report)",
    "depends_on": {
        "stage0_manifest_sha256_pin":
            "85ae1400c2ac1d8e36bd6a70b2b2ce23651b309314282c08f497fe225033a029",
        "stage_a_prereg_v2_sha256_pin":
            "50dfce689a7ca3a8d8ec42f0542d1641d36fc5d693c0c120fe6928792de0af3a",
    },
    # ---------------- EXACT legs (zero band tests) ------------------------
    "b_p1_identity": {
        "fixtures_with_degree": IDENTITY_FIXTURES,
        "grid": "fixture's frozen Stage-0 gate points x forward scheme x "
                "j in identity_j (tight ladder for the RN(1/10) point)",
        "identity_j": IDENTITY_J,
        "identity_j_tight": IDENTITY_J_TIGHT,
        "rule": "lane_cell(m=1, forward) - f'(x) == "
                "Sum_{k=2..d} h^(k-1)/k! * f_k(x), bit-for-bit in Q, "
                "with f_k from the exact symbolic-Q arbiter "
                "(nth_derivative_at); h = 2^-j exactly. EVERY cell. "
                "Units: (fixture, point, j) cells.",
        "citation": "Taylor's theorem with terminating exact sum on "
                    "polynomials (degree d): brief section 7 H2 verbatim.",
    },
    "b_p2_newton_inversion": {
        "fixtures_with_degree": {k: v for k, v in IDENTITY_FIXTURES.items()
                                 if v >= 1},
        "grid": "same points; forward scheme; same j ladders; tower "
                "levels m = 1..d from the lane tower",
        "rule": "for every k in 1..d: "
                "k! * Sum_{i=k..d} s(i,k)/i! * lane_cell(m=i) * h^(i-k) "
                "== f_k(x) from the exact arbiter, bit-for-bit in Q. "
                "s(i,k) = SIGNED Stirling numbers of the first kind via "
                "the recurrence s(i+1,k) = s(i,k-1) - i*s(i,k), exact "
                "integers. Units: (fixture, point, j, k) reconstructions.",
        "citation": "hD = ln(1+Delta) (Jordan, Calculus of Finite "
                    "Differences); finite truncation exact on degree-d "
                    "polynomials (Delta^i = 0 for i > d, certified by "
                    "Stage-A H3).",
        "meaning": "levels k..d price level k's truncation exactly - "
                   "the self-pricing claim at full strength.",
    },
    # ---------------- ARBITER legs (bands lawful) -------------------------
    "b_p3_lane_slopes": {
        "battery": LANE_SLOPE_BATTERY,
        "j_window": LANE_SLOPE_J_WINDOW,
        "schemes_with_predicted_alpha": {"forward": 1, "centered": 2},
        "observable": "dev(h): node = RN(x+h); h_real = Q(node) - Q(x) "
                      "(exact); forward: |(TRUE(node)-TRUE(x))/h_real - "
                      "f'(x)| as float; centered: both nodes, quotient "
                      "over (h+ + h-); TRUE and f' exact (lane + "
                      "symbolic arbiter), floatified ONLY for the "
                      "instrument. Well-defined off-lattice via the "
                      "realized step - no lattice-realizability needed.",
        "consumption_chain": "typed_finite_difference(observable, h, "
                             "1e-6*h) per h = 2^-j over the window -> "
                             "typed_collection -> typed_log_log_slope; "
                             "measured alpha = value.slope + 1 (the "
                             "chain measures the transfer of T, which "
                             "scales as h^(alpha-1)).",
        "acceptance": "SLOPE_OBSERVED status AND r_squared >= 0.999 AND "
                      "|alpha_measured - alpha_predicted| <= 0.05. "
                      "Arbiter-graded side: band lawful. Units: "
                      "(fixture, point, scheme) slope fits.",
        "delta_ratio": 1e-6,
    },
    "b_p4_annex_slopes_and_band": {
        "battery": ANNEX_SLOPE_BATTERY,
        "j_window": ANNEX_SLOPE_J_WINDOW,
        "schemes_with_predicted_alpha": {"forward": 1, "centered": 2},
        "observable": "raw float64 path (eval_raw) at RN nodes; realized "
                      "float step (exact by Sterbenz for h <= x/2, and "
                      "measured exactly in Q regardless); deviation vs "
                      "the mp arbiter f'(x) (240 dps, pinned escalation "
                      "rule from Stage 0).",
        "slope_acceptance": "SLOPE_OBSERVED AND r_squared >= 0.99 AND "
                            "|alpha_measured - alpha_predicted| <= 0.10. "
                            "Units: (fixture, point, scheme) slope fits.",
        "next_term_band_rule": "forward scheme, every (fixture, point, "
                               "j) cell on the window: "
                               "|dev_signed - (h_real/2)*f''(x)| <= "
                               "2*(h_real^2/6)*|f'''(x)| + "
                               "8*2^-53*M/h_real, with f'', f''' from "
                               "the mp arbiter (240 dps) and M = "
                               "max(|f(x)|, |f(node)|, 1). Slack factor "
                               "2 covers |f'''| variation over [x, x+h] "
                               "(< 2x on this battery/window, verified "
                               "at freeze); the M-term is the float-eval "
                               "noise allowance (4 ulp per evaluation, "
                               "two evaluations, amplified by 1/h). "
                               "Units: (fixture, point, j) band cells.",
        "delta_ratio": 1e-6,
    },
    "dp2_logging": "Amendment 1 standing instruction: BOUNDED / "
                   "below_sufficient_condition firings logged with "
                   "location; rational-class firing -> surprise ledger "
                   "immediately. Expected on this grid: 0 firings.",
    "domain_rule": "Amendment 2 standing law applies: stencil/node "
                   "domain membership checked exactly where lane TRUE "
                   "is evaluated; the identity/inversion grids contain "
                   "no division-by-zero nodes (verified at freeze).",
    "determinism": "byte-stable re-run x2 (sha256 over records) required "
                   "before the report; records sha-pinned in verdicts; "
                   "zero RNG.",
}


def main() -> None:
    from lloyd_v4.evals.difference_tower.arbiter import (
        mp_derivative, nth_derivative_at)
    from lloyd_v4.evals.difference_tower.eft_eval import in_domain_exact
    from lloyd_v4.evals.difference_tower.manifest import (
        fixture_exprs, require_stage0)
    from lloyd_v4.evals.difference_tower.tower import lane_tower_cell

    manifest = require_stage0()
    exprs = fixture_exprs(manifest)
    by_id = {f["fixture_id"]: f for f in manifest["fixtures"]}

    # dry-run 1: lane slope battery — leading coefficients nonzero, EXACT
    for fid, point_hex in LANE_SLOPE_BATTERY:
        x = Fraction(float.fromhex(point_hex))
        assert nth_derivative_at(exprs[fid], x, 2) != 0, (fid, "f'' == 0")
        assert nth_derivative_at(exprs[fid], x, 3) != 0, (fid, "f''' == 0")
    # dry-run 2: annex battery — mp arbiter accepts and coefficients
    # bounded away from zero at working precision
    for fid, point_hex in ANNEX_SLOPE_BATTERY:
        x = Fraction(float.fromhex(point_hex))
        for order in (1, 2, 3):
            val = mp_derivative(exprs[fid], x, order)
            assert val is not None and abs(val) > 1e-6, (fid, order)
    # dry-run 3: identity grids in-domain at every node (forward, max j)
    for fid in IDENTITY_FIXTURES:
        for g in by_id[fid]["gate_grid"]:
            x_q = Fraction(float.fromhex(g["point"]))
            ladder = (IDENTITY_J_TIGHT
                      if g["point"] == "0x1.999999999999ap-4"
                      else IDENTITY_J)
            for j in ladder:
                for k in range(0, max(IDENTITY_FIXTURES[fid], 1) + 1):
                    assert in_domain_exact(
                        exprs[fid], x_q + k * Fraction(1, 2 ** j)), (fid, j)
    # dry-run 4: Newton-inversion self-check on ONE pinned case (P3 at
    # x = 0.5, j = 5, d = 3) — the cited identity must hold before it is
    # frozen (bigraded misquote lesson)
    s = {(0, 0): 1}
    for i in range(0, 4):
        for k in range(0, i + 2):
            s[(i + 1, k)] = (s.get((i, k - 1), 0) - i * s.get((i, k), 0))
    x, j, d, fid = 0.5, 5, 3, "P3"
    h = Fraction(1, 2 ** j)
    cells = {m: lane_tower_cell(exprs[fid], x, j, m, "forward")
             for m in range(1, d + 1)}
    for k in range(1, d + 1):
        fact_k = 1
        for t in range(2, k + 1):
            fact_k *= t
        acc = Fraction(0)
        for i in range(k, d + 1):
            fact_i = 1
            for t in range(2, i + 1):
                fact_i *= t
            acc += Fraction(s[(i, k)], fact_i) * cells[i] * h ** (i - k)
        assert fact_k * acc == nth_derivative_at(
            exprs[fid], Fraction(x), k), f"Newton self-check failed k={k}"
    # informativeness under the predicted law (Amendment 3 standing law,
    # applied here one stage early by choice): synthetic predicted-law
    # case per criterion + wrong-law negative control
    from lloyd_v4.observers.directional_alpha_probe import (
        DeclaredAlphaModel, directional_alpha_probe)
    h_window = [2.0 ** -j for j in LANE_SLOPE_J_WINDOW]
    model = [DeclaredAlphaModel("synthetic_taylor", 1.0, 0.05)]
    res = directional_alpha_probe(lambda h: 3.7 * h + 0.9 * h * h, h_window,
                                  probe_id="dryrun_alpha1",
                                  function_label="synthetic_law",
                                  declared_alpha_models=model)
    v = res.value
    assert v.selected_alpha_model == "synthetic_taylor", res.status
    assert v.alpha_stability_status.value == "stable"
    assert v.propagated_window_error is not None
    assert v.propagated_window_error <= 0.05
    res_bad = directional_alpha_probe(lambda h: 2.2 * h ** 1.5, h_window,
                                      probe_id="dryrun_wronglaw",
                                      function_label="wrong_law",
                                      declared_alpha_models=model)
    assert res_bad.value.selected_alpha_model is None  # criterion CAN fail
    print("informativeness dry-run: synthetic predicted-law case passes "
          "both legs; wrong-law control fails leg i - criteria "
          "informative under the law")
    print("dry-run: lane battery coefficients nonzero (exact); annex "
          "battery mp-accepted; identity grids in-domain; Newton "
          "inversion self-check PASS (P3, x=0.5, j=5, k=1..3)")

    STAGE_B_DIR.mkdir(parents=True, exist_ok=True)
    path = STAGE_B_DIR / "prereg.json"
    path.write_text(json.dumps(PREREG, sort_keys=True, indent=1) + "\n",
                    encoding="utf-8")
    print(f"prereg (frozen={PREREG['frozen']}) -> {path}")
    print(f"sha256: {hashlib.sha256(path.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
