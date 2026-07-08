# c001 · three_channel_kg — FIXTURES (FROZEN)

Campaign `three_channel_kg` (cycle `c001`). Frozen Stage-0 fixtures, transcribed verbatim from
the ratified merged committed spec §5; **F12 pinned** from the Mathematician's F12 fixture pin
(reserved ruling R3 — CLOSED). All operands and expectations are **exact ℚ**. The bench
`fixtures.py` (built by Dev/CLI against this freeze) must reproduce every value exactly at
generation (a Stage-0 control). Frozen — no fixture changes without a versioned manifest bump.

## Retrodiction family (all values exact ℚ, declared DBP frame)

| ID | Surface / jet | Point | K_G | κ_c | κ_s | κ_int | Role |
|---|---|---|---|---|---|---|---|
| F1 | `x₁+x₂+x₃−3` | (1,1,1) | 0 | 0 | 0 | 0 | flat sanity |
| F2 | `x₁x₂+x₂x₃−2` | (1,1,1) | 0 | 0 | 0 | 0 | coupling yet developable |
| F3 | `x₁x₂+x₂x₃+x₃x₁−3` | (1,1,1) | 1/12 | 1/12 | 0 | 0 | pure-coupling positive |
| F4 | `x₁x₂x₃−1` | (1,1,1) | 1/3 | 1/3 | 0 | 0 | multilinear pure-coupling |
| F5 | `x₃−x₁²−x₂²` | (1,1,2) | 4/81 | 0 | 4/81 | 0 | pure-self; κ_s trap |
| F6 | `x₁²+x₂²+x₃²−1` | (3/5,4/5,0) | 1 | 0 | 1 | 0 | sphere, rational point (+sign witness) |
| F7 | `x₃−x₁x₂` | (1,1,1) | −1/9 | −1/9 | 0 | 0 | pure-coupling negative |
| **F8** | **`x₁²+x₁x₂+x₃²−3`** | (1,1,1) | **−3/49** | −1/49 | 1/49 | **−3/49** | **sign-collapse catcher (keystone)** |
| F9 | `x₁²+x₂²−x₃²` | (3,4,5) | 0 | 0 | 0 | 0 | indefinite Hessian, developable; rank-heuristic kill |
| F10 | `g=(2,1,1), H=[[2,2,2],[2,0,1],[2,1,0]]` | (1,1,1) | 2/9 | 1/3 | 0 | −1/9 | interaction decoupled (κ_int≠K_G) |
| F11 | `g=(2,1,1), H=[[1,2,0],[2,1,0],[0,0,−1]]` | jet | 0 | −1/9 | −1/9 | +2/9 | **positive** interaction |
| F13 | keystone, rungs r=1,2 | (1,1,1) | `σ₂=−3/49∈ℚ`; `Ĉ₁=−24∈ℚ`, `σ₁∈ℚ(√14)` | — | — | — | parity contrast |

## F12 — frame-relativity (R3 pinned, exact ℚ)

Rotation `R = (1/5)·[[3,−4,0],[4,3,0],[0,0,5]] ∈ SO(3)` (`RᵀR=I`, `det R=+1`, verified in ℚ).
Base jet (keystone F8, declared frame): `g=(3,1,2)`, `H=[[2,1,0],[1,0,0],[0,0,2]]`, `q=14`.

- **F12a** generic rotation (convention `x=Ry`, `g'=Rᵀg`, `H'=RᵀHR`):
  `g'=(13/5,−9/5,2)`, `H'=[[42/25,−31/25,0],[−31/25,8/25,0],[0,0,2]]`, `q'=14`.
  `(K_G, κ_c, κ_s, κ_int) = (−3/49, −961/30625, 2713/30625, −3627/30625)` — channels **MOVE**, K_G invariant.
- **F12b** signed permutation (swap axes 1↔2; `P=[[0,1,0],[1,0,0],[0,0,1]]`):
  `(K_G, κ_c, κ_s, κ_int) = (−3/49, −1/49, 1/49, −3/49)` — channels **FIXED**, K_G invariant.

Role: CL-c7 frame-honesty (channels frame-relative under generic rotation; S₃⋉{±}-invariant under signed permutation; K_G invariant under both).

## Derivation fixtures (named sets)

- **BOTH_SIGN_WITNESSES** — sphere `+1`, keystone `−3/49`, F10/F11 (both signs of κ_int).
- **KAPPA_S_TRAP** — F5/F6/F8 (the naive mirror κ_s ≠ the correct split-shape-operator κ_s).
- **GAUGE_SINGLE_EDGE** — keystone under `t·e₁, e₂, e₃` (e₁/e₂ pin; e₃ moves `6/49`).
- **ROTATION_WITNESS** — the CL-c7 self-refute surface (= F12).

## Scope cap

n=3 regular rational jets; even-order exact-ℚ; singular strata (`q=0` / cone-apex / `gᵢ=0`) appear
**only as typed `REFUSED`**, never as a numeric value.

Operands are pinned exactly in `src/lloyd_v4/evals/three_channel_kg/fixtures.py` (built by Dev/CLI to
this freeze); expectations are verified by exact arithmetic at generation (Stage-0 controls).
