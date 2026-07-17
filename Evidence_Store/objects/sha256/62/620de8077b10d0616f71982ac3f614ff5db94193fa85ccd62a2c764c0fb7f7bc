# WARP fixtures v1 (FX-W-A..F)

All operands pinned in `fixtures.py`. Scope cap (§2, ratified §10.5): rational-op class + the transcendental wall; carriers = free ℚ-modules (ℚ, ℚⁿ, ℚⁿˣᵐ) + the one representative quotient ℙ¹(ℚ). float64 only; no quotient atlas.

- **FXWA1** (FX-W-A): depth-2 product of sum and difference; all maps R_exact
- **FXWA2** (FX-W-A): expansion with internal cancellation; still all R_exact
- **FXWA3** (FX-W-A): division present but away from the ÷0 locus
- **FXWB1** (FX-W-B): intrinsic ÷0 token; the organ must return indeterminate
- **FXWB2** (FX-W-B): intrinsic 0^neg token; indeterminate, never a wrong factors
- **FXWC1** (FX-W-C): UNDERFLOW-WITNESS-ULP (HR138, banked): total float cancellation, factors by R_exact-by-composition
- **FXWC2** (FX-W-C): Sterbenz-protected subtraction (x/2 <= y <= 2x): float-exact
- **FXWC3** (FX-W-C): separated_coincidental cousin: two routes coincide at TRUE 0; factors (CL-M4 finite-precision cousin, reproduced not banked)
- **FXWD1** (FX-W-D): Richardson wall: D_static does_not_factor; factors only after one simplification-oracle call (CL-W3, Stage A)
- **FXWD2** (FX-W-D): Richardson wall: inverse-pair identity, oracle-recoverable
- **FXWD3** (FX-W-D): Richardson wall: on-branch inverse pair (|x| < pi/2)
- **FXWE1** (FX-W-E): scalar carrier ℚ; additive reconstruction
- **FXWE2** (FX-W-E): vector solve ℚⁿ (n=2); componentwise additive
- **FXWE3** (FX-W-E): Jacobian ℚⁿˣᵐ (2x2; Arm M reuse); entrywise additive
- **FXWF1** (FX-W-F): make-or-break Q2 edge: additive residue is representative-dependent (ill-defined on the quotient); Möbius/PGL2 is the named native reconstruction; equality by cross-multiply a·d==b·c

Recorded NON-TESTS (fence §9, carried so not silently re-added):
- FX-W-F/multiplicative_relative_error: a multiplicative-relative-error cell cannot fire the refutation kill — the exact EFT residue of any rational op is additive by construction. Recorded, not tested.
