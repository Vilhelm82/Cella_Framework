# PFC — Parity-Fixed inverse-channel local Calculus

**Opened 2026-07-07.** A separate-but-related project extracted from LEAD-7. The strategic
shift: stop treating `C = −14/B` as a Kerr-Newman fact, and lift it to a **dimension-general
local curvature calculus** for parity-fixed inverse-channel geometry. Kerr-Newman, RN-AdS,
Kerr-AdS, cavity ensembles, … then become *applications* of one local classification, instead
of a sprawl of case studies.

## The core object

One collapsing coordinate `x` against an `m`-dimensional flat transverse fibre `y_1..y_m`
(`m` = transverse fibre dimension = state-space dimension − 1). Three local types:

| type | metric germ (near `x=0`) | order | leading coefficient |
|---|---|---|---|
| **generic collapse** | `g_xx = A x² + O(x³)`, `g_αα = P_{α0}+P_{α1}x+O(x²)` (finite, NOT even) | **3** | `(1/A) Σ_α P_{α1}/P_{α0} = (1/A) Σ_α ∂_x log P_α\|_0` |
| **parity-fixed reflection** (asymptotic) | `g_xx = B(y)x²+O(x⁴)`, `g_αα = A_α(y)x⁻²+O(1)`, even in `x` | **4** | `−m(m+5)/B(y)` (amplitudes `A_α` forgotten) |
| **pure parity-fixed** (exact model) | `ds² = B x² dx² + x⁻² Σ_α A_α dy_α²` | **4** | `R = −m(m+5)/(B x⁴)` exactly |
| **higher-codim corner** | several parity variables vanish together | wedge | projective front-face coefficients (Newton polygon) |

`m(m+5) = 6m + m(m−1)` = radial focusing + transverse fibre shear. The odd order (3) of the
generic face comes from the parity-**breaking** linear drift `P_{α1}`; the even parity-fixed
face has `R` even in `x`, killing `x⁻³` and forcing order 4.

## Campaign structure

- **PFC-1 — Pure warped-product theorem.** `ds²=Bx²dx²+x⁻²ΣA_α dy_α² ⇒ R=−m(m+5)/(Bx⁴)`.
  **DONE** (`verification/pfc_test1_local_normal_forms.py`, byte-stable ×2): first-principles
  Ricci `m=1..4` → `6,14,24,36`, amplitude-independent; symbolic-in-`m` warped reduction
  `r=√B x²/2`, `w∝r^{−1/2}`, `R=−2m w''/w−m(m−1)(w'/w)²=−m(m+5)/(4r²)` for ALL `m`.
- **PFC-2 — Asymptotic parity theorem.** `g_xx=B(y)x²+O(x⁴)`, `g_αα=A_α(y)x⁻²+O(1)`, even in
  `x` ⇒ `R=−m(m+5)/B(y)x⁻⁴+O(x⁻²)`. **DONE** (`pfc_test1`, `m=2,3`): parity (`R(−x)=R`) kills
  `x⁻³`; leading coeff `−m(m+5)/B(y)` independent of amplitudes and even subleading data.
- **PFC-3 — Generic collapse comparison.** `g_xx=Ax²+O(x³)`, `g_αα=P_{α0}+P_{α1}x+O(x²)` ⇒
  `R=(1/A)Σ_α(P_{α1}/P_{α0})x⁻³+O(x⁻²)`. **DONE** (`pfc_test1`, `m=2,3`): order 3, coeff from
  the transverse first drift, independent of `A₃,A₄,P_{α2}`. Explains why generic faces are
  order 3 and parity-fixed faces order 4 — it is exactly parity.
- **PFC-4 — Corner blow-up theory.** *(OPENED 2026-07-07; opening result DONE, general proof
  OPEN.)* PREREG `PREREG_PFC4_corner.md`. **Codim-2 corner-valuation theorem:** two faces with
  single-face orders `p_x,p_y` and corner-residue weights `r_x,r_y` give a polar Newton polytope
  with vertices `v_x=(−p_x,r_y)`, `v_y=(r_x,−p_y)`, and the order along `x=ρε^{a_x}, y=ε^{a_y}`
  is the **support function** `m(a)=max(p_x a_x−r_y a_y, p_y a_y−r_x a_x)`. **DONE**
  (`verification/pfc_test2_corner_valuation.py`, byte-stable ×2): KN corner from CERTIFIED face
  data (`C_Ω~Q²`, `C_Φ~J²`, order 4) reproduces the `lead7_test9` wedge `max(4a−2,4−2a)`;
  synthetic `(4,4)` and `(4,3)` corners validated by direct curvature (rule is NOT KN-specific);
  corner order DROPS below both faces; at the balanced (facet-parallel) direction the whole
  facet is optimal, so the leading coefficient is a facet sum — the KN mixed term `M` explained
  as the front-face coefficient. **Key subtlety:** the correct input is FACE data, not raw metric
  monomial weights — a pure single-monomial ("toric") metric is non-generic and gives a milder
  (wrong) wedge. **OPEN body:** general proof of the vertex rule with the cancellation condition;
  codimension ≥3; the front-face coefficient classification.

## Kerr-Newman as the m=2 application (the dictionary)

| KN divisor | PFC local type | order | coefficient |
|---|---|---|---|
| `T=0` (extremal) | generic quadratic collapse (PFC-3) | 3 | `C_ext=A₂⁻¹∂_S log(G_JG_Q)\|_ext<0` |
| `Ω=0` (spin) | parity-fixed reflection (PFC-2) | 4 | `C_Ω=−14/B_J` |
| `Φ_e=0` (charge) | parity-fixed reflection (PFC-2) | 4 | `C_Φ=−14/B_Q` |
| `Ω=Φ_e=0` (Schwarzschild corner) | double-reflection corner (PFC-4) | wedge, min 2 | mixed stratum |

## Deliverables

- **Certificate:** `verification/pfc_test1_local_normal_forms.py` (PFC-1/2/3, general `m`).
- **Note (short, surgical):** `paper/pfc_normal_forms.tex` — *Parity-fixed inverse-channel
  normal forms and universal curvature blow-up*. The classification theorem + the KN
  application table. Kept deliberately minimal; the KN paper cites it, not vice versa.
- **Open:** PFC-4 corner-valuation theorem (its own campaign when taken up).

## Why this matters (the DBP-legs test)

If the same local laws recur across black-hole chemistry (RN-AdS, Kerr-AdS), cavity ensembles,
ordinary thermodynamic systems, and even non-thermodynamic implicit surfaces, then DBP is a
**normal-form calculus**, not "a metric that worked once." The pattern to watch:

- **Physical role divisors** (mass-role channels vanish): local type generic or parity-fixed;
  curvature pole follows the PFC law.
- **Interior channel-isotropy strata** (role-role channels vanish, excluded at `u=0`):
  diagnostic, not a physical role-boundary pole.
- **Critical / phase loci:** finite, pole, or sign-change according to whether they are
  role-divisors, response degeneracies, or channel-isotropy surfaces.

The frontier is separating kinds of thermodynamic *specialness* by local channel geometry.
