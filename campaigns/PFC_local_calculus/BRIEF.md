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
- **PFC-4 — Corner blow-up theory.** *(OPENED 2026-07-07; opening result + general vertex-rule
  proof DONE; codim ≥3 OPEN.)* PREREG `PREREG_PFC4_corner.md`. **Codim-2 corner-valuation
  theorem:** two faces with single-face orders `p_x,p_y` and corner-residue weights `r_x,r_y`
  give a polar Newton polytope with vertices `v_x=(−p_x,r_y)`, `v_y=(r_x,−p_y)`, and the order
  along `x=ρε^{a_x}, y=ε^{a_y}` is the **support function** `m(a)=max(p_x a_x−r_y a_y,
  p_y a_y−r_x a_x)`. Opening result `verification/pfc_test2_corner_valuation.py` (×2): KN from
  CERTIFIED face data → `lead7_test9` wedge; synthetic (4,4),(4,3) by direct curvature; corner
  drops below both faces; balanced facet ⟹ front-face coefficient (the KN mixed term `M`).
  **GENERAL VERTEX RULE PROVEN** (`verification/pfc_test3_vertex_rule.py`, ×2) as a closed
  symbolic identity: for `g_i=h_i(s)x^{p_i}y^{q_i}u_i`, the polar part of R is supported on
  exactly `V_1=(−(p_1+2),−q_1)`, `V_2=(−p_2,−(q_2+2))`, `V_0=(−p_0,−q_0)` with EXPLICIT
  coefficients `A(p_0,p_1,p_2)/(2h_1)`, `B(q_0,q_1,q_2)/(2h_2)`, and an s-jet `C_0`;
  `A=−p_0²+p_0p_1−p_0p_2+2p_0+p_1p_2−p_2²+2p_2`. Face data and raw weights are EQUIVALENT
  (`p_x=p_1+2`, `r_y=−q_1`, …). **Cancellation condition:** a vertex disappears iff its
  coefficient vanishes (`A=0`, `B=0`, or degenerate s-jet); the spectator vertex `V_0`
  contributes only when polar (`p_0>0` or `q_0>0`). Unit factors leave the vertices/order fixed
  (generic germs, not just monomials). **CORRECTION:** an earlier `pfc_test2` check swapped the
  x,y weights and wrongly claimed the single-monomial ("toric") germ was non-generic — with the
  correct weights it realises the polytope; fixed in ink. **OPEN body:** codimension ≥3 (Newton
  polytope in ℝ^k); the front-face coefficient classification.

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
