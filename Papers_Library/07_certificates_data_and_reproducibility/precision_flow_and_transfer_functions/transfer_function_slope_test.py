"""Test the synthesis: is the cross-fixture invariant in the SLOPE of E
versus the singular-distance coordinate, not in E's absolute value?

Per the transfer-function-exponent-family paper:
  g(f) = g0 + c·f^α·L(f)(1+r(f))   near branch point f → 0+
  → log-log slope of g vs f is α
  → log-log slope of δg/δf vs f is α-1
  → α is universal across fixtures sharing the same controlled branch form

For BOTH Schwarzschild F1 and pure_algebraic F1:
  base_operand vanishes linearly in the singular-distance coordinate
  (r-2 for Schw, 1-x for PA), so α should be 1 in both.

If the slope of E = log2|base_operand| vs log2(singular_distance) is 1
in both fixtures, the cross-fixture invariant lives in the slope.
The ~1 log2 unit cross-fixture gap should be in the INTERCEPT, not the slope.
"""
from __future__ import annotations
import json
import math
from pathlib import Path


def F1_base_schw(r):
    return 1.0 - 2.0 / r


def F1_base_pa(x):
    return 1.0 - x


def main():
    ROOT = Path("/home/william_lloydlt/projects/V4/Lloyd_Engine_V4")
    phase_1 = json.loads((ROOT / "Build_Docs/Reports/mcg_geometry_first"
                         "/phase_1_geometry_table.json").read_text())
    rows = phase_1["rows"]

    schw_rows = [r for r in rows if r.get("fixture") == "schwarzschild_four_form"
                 and r.get("principal_curvature") is not None]
    pa_rows = [r for r in rows if r.get("fixture") == "pure_algebraic_four_form"
               and r.get("principal_curvature") is not None]

    # For each fixture, build (log2(singular_distance), E = log2|base_operand|)
    def build_xy(rows_list, coord_to_base, coord_to_singular_dist):
        xs = []
        ys = []
        for row in rows_list:
            c = row["coordinate_value"]
            base = coord_to_base(c)
            sd = coord_to_singular_dist(c)
            if base > 0 and sd > 0:
                xs.append(math.log2(sd))
                ys.append(math.log2(base))
        return xs, ys

    schw_x, schw_y = build_xy(
        schw_rows,
        coord_to_base=lambda r: F1_base_schw(r),
        coord_to_singular_dist=lambda r: r - 2.0,
    )
    pa_x, pa_y = build_xy(
        pa_rows,
        coord_to_base=lambda x: F1_base_pa(x),
        coord_to_singular_dist=lambda x: 1.0 - x,
    )

    def linreg(xs, ys):
        n = len(xs)
        mx = sum(xs) / n
        my = sum(ys) / n
        num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
        den = sum((xs[i] - mx) ** 2 for i in range(n))
        slope = num / den
        intercept = my - slope * mx
        residuals = [ys[i] - (slope * xs[i] + intercept) for i in range(n)]
        ss_res = sum(r * r for r in residuals)
        ss_tot = sum((y - my) ** 2 for y in ys)
        r_sq = 1.0 - ss_res / ss_tot if ss_tot > 0 else None
        return slope, intercept, r_sq, residuals

    schw_slope, schw_int, schw_r2, schw_res = linreg(schw_x, schw_y)
    pa_slope, pa_int, pa_r2, pa_res = linreg(pa_x, pa_y)

    print("=== Log-log fit: E = log2|base_operand| vs log2(singular distance) ===\n")
    print(f"  {'Fixture':<22} {'slope (α)':>12} {'intercept':>12} {'R²':>10} {'n':>5}")
    print(f"  {'-'*22} {'-'*12} {'-'*12} {'-'*10} {'-'*5}")
    print(f"  {'Schwarzschild F1':<22} {schw_slope:>12.6f} {schw_int:>12.6f} "
          f"{schw_r2:>10.6f} {len(schw_x):>5}")
    print(f"  {'pure_algebraic F1':<22} {pa_slope:>12.6f} {pa_int:>12.6f} "
          f"{pa_r2:>10.6f} {len(pa_x):>5}")
    print()
    print("=== Cross-fixture comparison ===\n")
    slope_diff = abs(schw_slope - pa_slope)
    intercept_diff = abs(schw_int - pa_int)
    print(f"  |Δ slope|:     {slope_diff:.6e}")
    print(f"  |Δ intercept|: {intercept_diff:.6e}")
    print()
    print(f"  Slopes equal to {abs(schw_slope-pa_slope)*1e6:.3f} parts per million?")
    print(f"    {'YES' if slope_diff < 1e-3 else 'NO'}")
    print(f"  Intercepts equal?")
    print(f"    {'YES' if intercept_diff < 1e-3 else 'NO — separated by '+str(intercept_diff)+' log2 units'}")
    print()

    # Show some matched-K_G pairs and how their slopes/intercepts manifest
    print("=== Matched-K_G pair comparison: VALUE vs SLOPE space ===\n")
    schw_with_kg = [(r["coordinate_value"], r["principal_curvature"]) for r in schw_rows]
    pa_with_kg = [(r["coordinate_value"], r["principal_curvature"]) for r in pa_rows]

    matched = []
    for r_s, kg_s in schw_with_kg:
        for r_p, kg_p in pa_with_kg:
            if kg_s > 0 and kg_p > 0:
                rel = abs(kg_s - kg_p) / max(abs(kg_s), abs(kg_p))
                if rel < 0.005:
                    matched.append((r_s, kg_s, r_p, kg_p))
                    break
    matched.sort(key=lambda p: p[1])
    matched = matched[:8]

    print(f"  {'K_G':>8}  {'E_schw':>10}  {'E_pa':>10}  {'|ΔE|':>8}  "
          f"{'log2(sd_schw)':>14}  {'log2(sd_pa)':>14}")
    for r_s, kg_s, r_p, kg_p in matched:
        e_s = math.log2(F1_base_schw(r_s))
        e_p = math.log2(F1_base_pa(r_p))
        sd_s = math.log2(r_s - 2)
        sd_p = math.log2(1 - r_p)
        print(f"  {kg_s:>8.4f}  {e_s:>+10.4f}  {e_p:>+10.4f}  {abs(e_s-e_p):>8.4f}  "
              f"{sd_s:>+14.4f}  {sd_p:>+14.4f}")
    print()

    # The key test: at matched K_G, do (E - α·log2(sd)) values agree across fixtures?
    print("=== Slope-corrected reading: E - α·log2(singular_distance) ===\n")
    print("  (subtracts off the slope-1 part; what remains should be the intercept)\n")
    print(f"  {'K_G':>8}  {'schw resid':>14}  {'pa resid':>14}  {'|Δ|':>10}")
    deltas = []
    for r_s, kg_s, r_p, kg_p in matched:
        e_s = math.log2(F1_base_schw(r_s))
        e_p = math.log2(F1_base_pa(r_p))
        sd_s = math.log2(r_s - 2)
        sd_p = math.log2(1 - r_p)
        # Use the fitted slopes
        resid_s = e_s - schw_slope * sd_s
        resid_p = e_p - pa_slope * sd_p
        d = abs(resid_s - resid_p)
        deltas.append(d)
        print(f"  {kg_s:>8.4f}  {resid_s:>+14.4f}  {resid_p:>+14.4f}  {d:>10.4f}")
    print()
    print(f"  Mean |Δ| in slope-corrected residual: {sum(deltas)/len(deltas):.6f}")
    print(f"  Compare baseline |ΔE| ≈ 1.12 log2 units (Phase F amendment)")
    print()


if __name__ == "__main__":
    main()
