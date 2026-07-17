"""Local slope field — no averages. Compute the log-log slope of E vs
singular_distance AT EACH PROBE using a small adjacent-probe window.

The transfer-function law: g(f) ~ c·f^α as f → 0+, so log-log slope → α
asymptotically. Test: as we approach the branch point in EACH fixture,
does the local slope converge to a common value?

If yes: the cross-fixture invariant is asymptotic, not global.
If no: the threads don't tie this way.
"""
from __future__ import annotations
import json
import math
from pathlib import Path


def main():
    ROOT = Path("/home/william_lloydlt/projects/V4/Lloyd_Engine_V4")
    phase_1 = json.loads((ROOT / "Build_Docs/Reports/mcg_geometry_first"
                         "/phase_1_geometry_table.json").read_text())
    rows = phase_1["rows"]

    def build_image(fixture, base_fn, sd_fn):
        fx = [r for r in rows if r.get("fixture") == fixture
              and r.get("principal_curvature") is not None]
        fx.sort(key=lambda r: r["coordinate_value"])
        image = []
        for row in fx:
            c = row["coordinate_value"]
            b = base_fn(c)
            sd = sd_fn(c)
            if b > 0 and sd > 0:
                image.append({
                    "coord": c,
                    "log2_sd": math.log2(sd),
                    "E": math.log2(b),
                    "K_G": row["principal_curvature"],
                })
        return image

    schw = build_image(
        "schwarzschild_four_form",
        base_fn=lambda r: 1.0 - 2.0 / r,
        sd_fn=lambda r: r - 2.0)
    pa = build_image(
        "pure_algebraic_four_form",
        base_fn=lambda x: 1.0 - x,
        sd_fn=lambda x: 1.0 - x)

    # Sort by singular distance ascending (closest to branch first)
    schw.sort(key=lambda p: p["log2_sd"])
    pa.sort(key=lambda p: p["log2_sd"])

    # Local slope at each probe via central difference on adjacent probes
    def local_slopes(image):
        slopes = []
        for i in range(len(image)):
            if 0 < i < len(image) - 1:
                # central difference
                dE = image[i+1]["E"] - image[i-1]["E"]
                dSD = image[i+1]["log2_sd"] - image[i-1]["log2_sd"]
                s = dE / dSD if dSD != 0 else None
            elif i == 0:
                dE = image[1]["E"] - image[0]["E"]
                dSD = image[1]["log2_sd"] - image[0]["log2_sd"]
                s = dE / dSD if dSD != 0 else None
            else:
                dE = image[-1]["E"] - image[-2]["E"]
                dSD = image[-1]["log2_sd"] - image[-2]["log2_sd"]
                s = dE / dSD if dSD != 0 else None
            slopes.append(s)
        return slopes

    schw_slopes = local_slopes(schw)
    pa_slopes = local_slopes(pa)

    # Print slope field sorted by singular distance (asymptotic first)
    print("=== Local log-log slope of E vs log2(singular_distance) ===\n")
    print("Sorted closest-to-branch first. Asymptotic limit is the first row.\n")
    print(f"{'log2(sd)':>12}  {'Schw slope':>12}  {'log2(sd)':>12}  {'PA slope':>12}")
    print("-" * 60)
    # Show first 10, middle 5, last 5
    schw_sorted = list(zip(schw, schw_slopes))
    pa_sorted = list(zip(pa, pa_slopes))
    for i, (s_pair, p_pair) in enumerate(zip(schw_sorted, pa_sorted)):
        s_pix, s_slope = s_pair
        p_pix, p_slope = p_pair
        if i < 15 or i > len(schw_sorted) - 6 or (50 < i < 60):
            s_sl = f"{s_slope:+.4f}" if s_slope is not None else "N/A"
            p_sl = f"{p_slope:+.4f}" if p_slope is not None else "N/A"
            print(f"{s_pix['log2_sd']:>+12.4f}  {s_sl:>12}  "
                  f"{p_pix['log2_sd']:>+12.4f}  {p_sl:>12}")
        elif i == 15:
            print("    ...")
    print()

    # Check convergence: average of first N slopes vs threshold
    print("=== Asymptotic convergence check ===\n")
    print("Mean local slope over closest-N probes (excluding edge points):\n")
    for N in (5, 10, 20, 50, 100, len(schw)-1):
        # Use only interior probes (not edge i=0 or i=last)
        sl_s = [s for s in schw_slopes[1:N+1] if s is not None]
        sl_p = [s for s in pa_slopes[1:N+1] if s is not None]
        ms = sum(sl_s) / len(sl_s) if sl_s else None
        mp = sum(sl_p) / len(sl_p) if sl_p else None
        print(f"  N={N:>4}:  Schw mean slope = {ms:+.4f}   PA mean slope = {mp:+.4f}   "
              f"|Δ| = {abs(ms-mp):.4f}")
    print()

    # Show the actual asymptotic limit at the very closest probes
    print("=== Slope at the 3 probes nearest each branch ===\n")
    print("Schwarzschild:")
    for i in range(3):
        p = schw[i]
        s = schw_slopes[i]
        print(f"  r={p['coord']:.4f}  (r-2)={p['coord']-2:.6f}  E={p['E']:+.4f}  "
              f"local slope={s:+.4f}")
    print()
    print("pure_algebraic:")
    for i in range(3):
        p = pa[i]
        s = pa_slopes[i]
        print(f"  x={p['coord']:.4f}  (1-x)={1-p['coord']:.6f}  E={p['E']:+.4f}  "
              f"local slope={s:+.4f}")
    print()


if __name__ == "__main__":
    main()
