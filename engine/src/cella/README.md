# `cella` package inventory

This directory contains the Python implementation of the Cella Framework. The package combines exact arithmetic and geometry primitives, typed numerical diagnostics, proof helpers, route planning, and the MCP adapter that exposes those capabilities.

| Item | Short specification |
|---|---|
| `README.md` | This inventory of the package contents. |
| `__init__.py` | Declares the `cella` package and its version, and documents the Layer 0 contract and core primitives. |
| `arithmetic.py` | Certification helpers for precision refinement, elliptic-period transformations, branch and residue checks, independent-route comparison, field recognition, and constant pinning. |
| `campaign.py` | Exact, formula-level tools for local metric-germ classification, divisor and corner analysis, positivity certificates, metric candidate selection, metric construction, and implicit Gaussian curvature. |
| `carrier.py` | Extracts the gauge-invariant Hessian carrier, constructs its normal form, and provides the labelled three-channel cross-check for three-dimensional inputs. |
| `cell.py` | Defines the immutable `Cell(value, residue)` result type, including exact reconstruction and first-class refusal handling. |
| `certificate.py` | Builds deterministic two-register result certificates, canonicalizes exact values, and verifies repeatability by double-running computations before emission. |
| `cleanliness.py` | Diagnoses binary floating-point algebra using BACL lattice checks, exact operand-residue traces, refinery comparisons, cleanliness rankings, and parameter-grid sweeps. |
| `hostile_benchmark.py` | Runs the internal Pathfinder hostile benchmark against direct Cella and conventional symbolic/numerical baselines using a frozen manifest. |
| `jet.py` | Defines immutable, validated exact order-2 jets and constraint blocks used as geometry inputs. |
| `mcp_server.py` | Adapts Cella operations to MCP: validates and serializes inputs, selects tool profiles, dispatches tool calls, emits telemetry, and runs the stdio server/router. Its arithmetic profile includes native DBP evaluation/replay, native Legendre K/E and pinning, the clean-process Landen trace audit, and a hash-pinned release receipt. |
| `neutral_sweep.py` | Runs a declarative, engine-neutral benchmark corpus with per-engine time limits and native adapters for each comparison engine. |
| `observation.py` | Defines lossy observation maps that produce measurement residues or typed refusals while keeping representation changes separate. |
| `pathfinder/` | Typed route-discovery kernel: canonical task IR with stable hashing, structural fingerprint engine, native scout engine, a registry of 39 route-family providers with admissibility-first Pareto selection and recorded loser evidence, and canonical route serialization. Returns typed `ComputationalRoute` instructions only — never the final mathematical result. |
| `_legacy_pathfinder.py` | Frozen early-prototype behavior (residual-fingerprint route planning, conservative rewrites, burden comparison) preserved behind `pathfinder.compat`; characterization and MCP gates close through it. |
| `periods.py` | Records exact structural data for elliptic quartic periods, third-kind residues, branch jumps, K/Pi normal forms, route comparisons, and known capability gaps. |
| `probe_observers.py` | Provides finite-difference, sweep-signature, directional-alpha, and jet observers with measured floating telemetry and typed fit diagnostics. |
| `proofs.py` | Implements narrow exact-rational proof primitives for pole laws, Newton corners, rational surface jets, shifted polynomial positivity, and Sturm positivity. |
| `qsqrt.py` | Implements exact arithmetic in a fixed quadratic extension, representing values of the form `a + b*sqrt(r)`. |
| `reference_lift.py` | Reconstructs selected reference-material results as exact local tools for channel transport, role orbits, curvature spectra, shadow laws, and wreath laws. |
| `refusal.py` | Defines the closed vocabulary and immutable type for stratum-specific non-recovery results, including plain-language rendering. |
| `residual_profile.py` | Parses a restricted arithmetic expression graph and profiles cancellation sites, residual orders, sweep behavior, and likely operational burden. |
| `residue.py` | Implements the exact two-species residue algebra and its `Account` ledger for measurement and representation defects. |
| `sensors.py` | Computes invariant geometry sensors: numerator towers, shape moments, localization channels/support, and combined fingerprints. |
| `slope_flow.py` | Compares local log-magnitude slope segments with declared models to classify residual-order behavior without relying only on a global fit. |
| `symbolic.py` | Supplies a restricted exact rational-function engine over sparse multivariate polynomials, including equality, valuation, pole-law, carrier, and channel calculations. |
| `tower.py` | Computes the exact invariant tower of elementary symmetric principal-curvature functions, with rational or quadratic-extension output fixed by parity. |
| `typed_elementary.py` | Constructively evaluates elementary functions using exact rational enclosures, domain-specific refusals, and precision refinement without external numerical libraries. |
| `typed_log_log_slope.py` | Fits typed log-log power laws with degeneracy handling, diagnostics, and signed coefficient recovery. |
| `typed_ulp.py` | Computes canonical IEEE 754 spacing and exact ULP records for binary32 and binary64 values. |
| `__pycache__/` | Generated Python bytecode cache; it is runtime output, not authored source, and can be recreated automatically. |

## Mathematical primitives and operations

The notes below describe the mathematical objects each module owns and the operations it actually performs. They also distinguish exact verdict-bearing operations from floating-point observations and orchestration code.

Notation used below:

- `Q` is the rational field and `Q(sqrt(r))` is a fixed quadratic extension.
- `g` is a constraint gradient, `H` its Hessian, and `q = g dot g`.
- `P = I - g g^T/q` projects onto the tangent space of a regular level set.
- `Cell(v, rho)` means a represented value `v` plus an exact residue `rho`; reconstruction is `v + rho`.
- A *refusal* is a typed statement that an operation is outside its certified domain, not a numeric result.

### `README.md`

- **Primitives:** Documentation only.
- **Operations:** None. It inventories the package and records the contracts below.

### `__init__.py`

- **Primitives:** The Layer 0 concepts `Cell`, `ObservationMap`, `Residue`, `Refusal`, `QSqrt`, and `Certificate` are named here, although their implementations live in separate modules.
- **Operations:** No mathematical computation; it declares the package version and the rule that higher layers must not emit uncertified bare numbers.

### `arithmetic.py`

- **Primitives:** Rational enclosures, binary precision budgets, Legendre elliptic parameters, complete elliptic-integral routes, algebraic-field bases, and route-comparison records.
- **Exact operations:** Rounds rationals to `p` binary significant bits using round-to-nearest/ties-to-even; accepts an enclosure `[lo, hi]` only when both endpoints round to the same value; and computes a required precision floor `output_bits + sum(path_losses)`.
- **Elliptic operations:** Applies Legendre/third-kind parameter reductions, branch and residue gates, Cauchy-principal-value bookkeeping, Carlson-form comparison routes, and elliptic-curve invariants such as cross-ratio and `j`-invariant checks.
- **Recognition and comparison:** Compares two numerical routes by their absolute difference and supported decimal digits; uses PSLQ against a declared basis; and pins a proposed constant only when the recognition, route-agreement, branch, and precision gates close.
- **Boundary:** This is a certification harness around SymPy/mpmath computations, not the Cella-native exact period kernel; the native structural subset is in `periods.py`.

### `campaign.py`

- **Primitives:** Local diagonal metric germs, divisor pole signatures, Newton/support vertices, positivity obligations, metric candidates, Kerr-Newman role metrics, and implicit surfaces in `R^3`.
- **Local pole classification:** Recognizes the parity-fixed law `R = -m(m+5) x^-4/B + O(x^-2)` and the generic quadratic law `R = (1/A) sum(P_a1/P_a0) x^-3 + O(x^-2)`. It also rejects the false inference that a lone `B x^2 dx^2` collapse with flat transverse channels must create a curvature pole.
- **Corner operations:** Builds exponent vertices, removes vertices whose coefficients cancel, evaluates a path support order `max[-(u ax + v ay)]`, and identifies the active front face and balanced ray.
- **Proof composition:** Combines shifted-coefficient and Sturm certificates factor by factor, and accepts a product as positive only when every factor is certified positive.
- **Geometry operations:** Selects metric candidates by declared gates, constructs the graph-normalized Kerr-Newman role-metric specification, and computes implicit Gaussian curvature from the bordered Hessian: `K_G = -det([[H,g],[g^T,0]]) / q^2`.

### `carrier.py`

- **Primitives:** A regular codimension-one order-2 jet, the gauge action `H -> H + g a^T + a g^T`, the carrier `O`, its zero-diagonal normal form `H_perp`, and the labelled three-channel tuple `(kc, kint, ks)`.
- **Carrier extraction:** For every `i < j`, computes `O_ij = H_ij - g_i H_jj/(2 g_j) - g_j H_ii/(2 g_i)`. This removes Hessian directions generated by the gauge action while retaining the complete same-gradient invariant on the supported chart.
- **Normal form:** Places `O_ij` in the off-diagonal entries of a symmetric matrix and sets its diagonal to zero.
- **Three-dimensional cross-check:** Samples a bordered-Hessian density at interpolation points in `(t,u)`, recovers its `t^2`, `tu`, and `u^2` coefficients by finite differences, divides them by `q^2`, and reports `K_G = kc + kint + ks`.
- **Boundary:** Carrier division requires every gradient component to be nonzero; higher codimension and singular/chart-degenerate inputs return typed refusals.

### `cell.py`

- **Primitives:** The immutable pair `Cell(value, residue)` and refusal cells `Cell(None, Refusal)`.
- **Operations:** Validates exact-tower payloads, tests whether a cell is a refusal, and reconstructs the represented object with exact module addition: `true_object = value + residue`.
- **Boundary:** It performs no approximation, uncertainty propagation, or interval arithmetic. A refusal is returned as-is rather than coerced into `NaN` or a guessed value.

### `certificate.py`

- **Primitives:** Canonical exact records, SHA-256-derived digests, and immutable two-register certificates with machine and plain-language views.
- **Operations:** Canonicalizes rationals, quadratic numbers, tuples, dictionaries, and refusals; hashes their canonical JSON form; executes a computation twice; and emits a certificate only if the two canonical results agree bit-for-bit.
- **Boundary:** The digest certifies deterministic reproduction of the computation and account. It does not prove that an external physical state is correct.

### `cleanliness.py`

- **Primitives:** Exact rational representations of binary64 operands, ULP lattices, BACL pair records, operation-residue traces, burden vectors, and Pareto rankings.
- **BACL operation:** For an additive/subtractive pair, measures the exact separation on the coarser operand's ULP lattice, finds the nearest integer lattice index, and records the non-integer residual. An integer index under the theorem hypothesis marks a protected lattice relation.
- **Operation tracing:** Evaluates restricted `+`, `-`, `*`, `/`, and integer-power expression trees in binary64 while simultaneously evaluating the same operations on the exact rational values of those binary64 operands. At each node it computes `rounding_residue = exact_result - rounded_result` and expresses it in result ULPs.
- **Form comparison:** Requires candidate forms to agree exactly on the declared sample grid, then compares lattice class, maximum lattice residual, rounding error in ULPs, and operation depth componentwise. It returns a Pareto frontier rather than claiming global symbolic equivalence.
- **BACL dial:** Enumerates regroupings of a three-term sum and ranks their operational cleanliness across a declared grid.

### `hostile_benchmark.py`

- **Primitives:** A frozen benchmark manifest, test cases, engine adapters, timing records, and expected route/verdict records.
- **Operations:** Runs the same hostile cases through Pathfinder, direct Cella routines, SymPy, mpmath, and optional FLINT/Arb adapters; compares outputs to manifest expectations; and aggregates correctness and timing counts.
- **Boundary:** It is experimental comparison infrastructure, not a proof primitive and not an exposed MCP tool.

### `jet.py`

- **Primitives:** `Jet2(point, g, H)`, representing the order-2 jet of a scalar constraint, and `ConstraintBlock`, representing one or more constraints at a common point.
- **Operations:** Validates exact coordinates, matching dimensions, an `n x n` Hessian, Hessian symmetry, and consistency of all jets in a block.
- **Boundary:** The module stores differential data but does not differentiate expressions or calculate invariants itself.

### `mcp_server.py`

- **Primitives:** JSON encodings of exact scalars and proof records, tool profiles, tool schemas, routing records, and MCP server objects.
- **Operations:** Converts JSON values to and from Cella exact types, constructs jets and constraint blocks, dispatches calls into the mathematical modules, serializes proofs/refusals/telemetry, and selects the permitted tool surface for each profile.
- **Boundary:** It deliberately contains almost no mathematics of its own; it is the protocol and validation layer around the kernels listed here.

### `neutral_sweep.py`

- **Primitives:** A declarative benchmark corpus, per-engine adapters, subprocess results, time caps, and normalized comparison records.
- **Operations:** Gives each engine the same mathematical task, chooses that engine's ordinary native route, enforces the declared time cap, and aggregates success, failure, timeout, and timing statistics.
- **Boundary:** Results are empirical and engine/version dependent. They are not mathematical certificates.

### `observation.py`

- **Primitives:** `ObservationMap`, a named lossy map from a true object to either `(value, measurement_residue)` or a refusal.
- **Operations:** Applies an observation and wraps its result in a `Cell`. Composition `A.then(B)` applies `A` then `B` and adds their measurement residues exactly: `rho_total = rho_A + rho_B`.
- **Boundary:** Observation maps create measurement (`M`) residues only. Representation (`R`) changes belong to the account algebra and are not treated as observations.

### `pathfinder.py`

- **Primitives:** Route plans, residual fingerprints, rewrite candidates, engine-stack provenance, burden rankings, and declared-grid comparison results.
- **Route planning:** Converts a residual profile into a route decision such as direct evaluation, exact collapse, algebraic rewrite, precision escalation, or refusal. The primary key is the residual fingerprint—local shape, residual order/scale, account closure, domain stratum, and burden—not the source string alone.
- **Algebraic rewrites:** Detects and proposes exact structural transformations including `x-x -> 0`, `(c+x)-c -> x`, scaled constant collapse, `a^2-b^2 -> (a-b)(a+b)`, square-root conjugation, common-factor extraction, and alternative three-term groupings.
- **Candidate comparison:** Uses `cleanliness.py` to verify exact-real equality on a declared grid and rank candidates by BACL/rounding burden. This establishes a grid-scoped operational preference, not universal symbolic identity.

### `periods.py`

- **Primitives:** The Legendre even quartic `y^2 = (1-x^2)(1-m x^2)`, exact rational/quadratic residues, formal period atoms `K(m)` and `Pi(n;m)`, branch-jump ledgers, and exact linear normal forms over those atoms.
- **Curve operations:** Computes the branch square `1/m` and `j = 256(1-m+m^2)^3 / [m^2(1-m)^2]` for a nondegenerate rational parameter `m`.
- **Residue operations:** For the differential `p dx / [(1-n x^2)y]`, computes the pole locations through `x0^2 = 1/n`, `y0^2 = (1-x0^2)(1-m x0^2)`, and the exact squared residue `p^2 n / [4(n-1)(n-m)]`; the square root is retained in `Q(sqrt(r))` when irrational.
- **Period reduction:** Records `CPV Pi(n;m) = K(m) - Pi(m/n;m)` when `n > 1`, combines rational coefficients of formal `K`/`Pi` atoms, and compares two routes by exact coefficient subtraction plus equality of their residue-jump ledgers.
- **Boundary:** Period atoms are structural symbols here; this module does not yet enclose or numerically evaluate complete elliptic integrals.

### `probe_observers.py`

- **Primitives:** Forward-difference transfers, scale sweeps, declared power-law models, alpha estimates, local jet probes, fit diagnostics, and cancellation classifications.
- **Finite differences:** Computes `[g(f + delta_f) - g(f)] / delta_f` and a cancellation ratio `abs(delta_g) / max(abs(g(f)), abs(g(f+delta_f)))`.
- **Sweep and alpha operations:** Uses `delta_f = eta f`, fits `log(abs(transfer))` against `log(f)`, and interprets a fitted derivative slope `s` as an original power `alpha = s + 1`. Nested windows test whether the estimate is stable as the sampled scale shrinks.
- **Jet probes:** For a regular point, analyzes `f(x0+h)-f(x0)`; for a singular model, analyzes `f(x0+h)` directly. It also reports a usable numerical derivative when one survives the cancellation checks.
- **Boundary:** These are floating observations with explicit status and residual diagnostics, not exact proofs of asymptotic order.

### `proofs.py`

- **Primitives:** Sparse exact polynomials, Sturm sequences, local metric exponent vectors, rational surface jets, and Newton/support records.
- **Pole laws:** For `g_xx = B x^p0` and transverse `g_aa = A_a x^pa`, computes `R = C(p) x^-(p0+2)/B`, where `C(p)` is an exact quadratic expression in the exponents. Specialized routines return the parity-fixed and generic quadratic laws used by `campaign.py`.
- **Surface jets:** Parses a restricted exact expression, differentiates it symbolically, and evaluates its value, gradient, and Hessian at a rational point.
- **Corner valuation:** Computes exact exponent vertices and the dominant support along a declared path.
- **Positivity:** After shifting variables, coefficient positivity certifies a polynomial on a positive orthant. For a univariate polynomial, a Sturm chain counts real roots on an open ray and combines the zero-root count with a positive sample to certify positivity.
- **Boundary:** This is a deliberately narrow rational proof kernel, not a general computer algebra system.

### `qsqrt.py`

- **Primitives:** Exact values `a + b sqrt(r)` with `a,b,r in Q`, `r > 0`, and `r` a nonsquare rational.
- **Field operations:** Adds and subtracts coefficients componentwise; multiplies by `(a+b sqrt(r))(c+d sqrt(r)) = (ac+bdr) + (ad+bc)sqrt(r)`; and divides using conjugation and the norm `N(a+b sqrt(r)) = a^2-b^2 r`.
- **Boundary:** Arithmetic is closed only for a fixed radicand. Mixing quadratic fields is rejected, and conversion to float is explicitly display-only.

### `reference_lift.py`

- **Primitives:** Exact three-channel densities, gauge transports, role-jet group orbits, curvature spectra, role-channel signatures, loss diagnostics, shadow laws, and wreath-product combinatorics.
- **Linear-algebra operations:** Reconstructs labelled channel components from exact gradients/Hessians, transports them under Hessian gauge changes, solves small rational systems, and checks determinant/rank conditions.
- **Group-action operations:** Generates exponent/role orbits under permutations and projective transformations, computes first projective invariants, and reduces graph jets into curvature-orbit spectra.
- **Role analysis:** Compares full role-channel information with pairwise/scalar reductions, reports information lost as dimension grows, and constructs shadow/wreath-law records from exact combinatorial counts.
- **Boundary:** These are local exact reconstructions of selected reference results; they are not imports of or calls back into the reference scripts.

### `refusal.py`

- **Primitives:** A closed set of refusal tokens, their strata, technical details, and plain-language renderings.
- **Operations:** Validates that a refusal token belongs to the admitted vocabulary, attaches its domain/degeneracy stratum, and renders it for machine or human consumption.
- **Boundary:** No arithmetic is performed. A refusal records why arithmetic or recovery is invalid on a particular stratum.

### `residual_profile.py`

- **Primitives:** A restricted expression tree, scale sweeps, subtraction sites, local residual orders, cancellation classes, burden vectors, and exact sample accounts where available.
- **Expression operations:** Parses constants, variables, selected unary functions, and binary arithmetic; evaluates branches over a log-spaced sweep; and locates subtraction nodes where two large branches may leave a small residual.
- **Asymptotic operations:** Fits branch and residual magnitudes to power laws, estimates the first surviving residual order, identifies same-leading-constant cancellation, checks Sterbenz windows, and estimates when a residual crosses machine epsilon.
- **Exact-account operation:** Where the expression subset permits, reevaluates binary64 inputs and intermediates as exact rationals to separate representational rounding from mathematical cancellation.
- **Routing output:** Aggregates site severity, residual order, scale class, missing parameters, exact-account coverage, and predicted burden. It diagnoses an expression; it does not rewrite it.

### `residue.py`

- **Primitives:** The exact scalar tower, shape-preserving module addition/subtraction, measurement residues `M`, representation residues `R`, and a two-ledger `Account`.
- **Module operations:** `madd` and `msub` operate exactly on rationals, fixed-radicand quadratic values, or equally shaped nested tuples. `is_zero` recursively tests the additive identity.
- **Residue composition:** `M` residues add in the defect module. `R` residues add only when they act at the same gradient base; a base change starts a new account epoch.
- **Account operations:** Absorbs residues without mixing the `M` and `R` ledgers, folds a geometry-computed cross-term into `M`, and defines the owned holonomy gap between comparable accounts as their exact `M`-ledger difference.

### `sensors.py`

- **Primitives:** Four invariant sensor families: the numerator tower, carrier isotypic shape moments, triangle localization channels, and an `n=3` role fingerprint.
- **Numerator tower:** Forms the off-diagonal Hessian `Hc`, projects with `P`, and computes elementary symmetric principal-minor sums of `P Hc P`, normalized by powers of `q`; parity determines rational versus `Q(sqrt(q))` output.
- **Shape moments:** Treats carrier entries as the edge/pair representation of the symmetric group `S_n`; constructs character projectors using Murnaghan-Nakayama characters; and returns exact squared norms of the trivial, standard, and `(n-2,2)` shape components.
- **Localization:** For each triangle `S`, weights off-diagonal entries by products of the other gradient components and computes a quadratic contrast `Delta_S`. Its derivative support identifies which triangles respond to a fault on a selected edge.
- **Role fingerprint:** Converts an `n=3` implicit jet to graph derivatives `(a,b,A,B,C)`, forms channel amplitudes `Lambda_P`, `Lambda_D`, `Lambda_S`, channel curvatures `k_i = -Lambda_i^2/q0^2`, anisotropy `A_c = sum_pairwise(k_i-k_j)^2`, and faithfulness determinant `8 Lambda_P Lambda_D Lambda_S/q0^6`.

### `slope_flow.py`

- **Primitives:** Positive control/observable samples, declared constant-slope models, adjacent log-log segments, model residuals, and order-stability classifications.
- **Segment operation:** For adjacent samples, computes `s = Delta log(abs(observable)) / Delta log(control)`.
- **Model comparison:** Compares every segment slope with each declared model, calculates residual summaries, selects a unique model only when it lies within the declared band, and reports ambiguity or no match otherwise.
- **Residual-order interpretation:** For direct residuals `C x^p`, slope `p` estimates the order. For finite-difference sweep transfers, expected slope is `p-1`, so the module maps the selected derivative model back to residual order `p`.

### `symbolic.py`

- **Primitives:** Sparse multivariate polynomials over `Q`, rational functions `P/Q`, a restricted infix parser, exact valuations, and symbolic carrier/channel records.
- **Polynomial operations:** Canonical term collection, exact addition/subtraction, convolution multiplication, integer powers by repeated squaring, scaling, and leading/content normalization.
- **Rational-function operations:** Exact `+`, `-`, `*`, `/`, inversion, and signed integer powers. Equality is decided by the zero cross-difference `P1 Q2 - P2 Q1`, not by sampled numerical agreement.
- **Geometry operations:** Evaluates the same carrier formula as `carrier.py` over a rational-function field, sums labelled symbolic channels, and builds symbolic versions of the supported pole laws.
- **Valuation operations:** Associates monomial exponent vectors with rational-function coefficients, computes path support orders, and reports coefficient-zero deletion walls and denominator domain walls.
- **Boundary:** It accepts rational arithmetic and integer powers only; transcendental functions, decimal literals, general factorization, and unrestricted simplification are outside this arm.

### `tower.py`

- **Primitives:** Tangent projector `P`, projected Hessian `A = P H P`, principal-minor sums `c_r = e_r(A)`, and invariant tower entries `sigma_r` for `r = 1,...,n-1`.
- **Operations:** Computes determinants and sums all `r x r` principal minors, then applies `sigma_r = (-1)^r c_r / q^(r/2)`. Even orders are rational; odd orders are represented in `Q(sqrt(q))` unless `q` is a rational square or the coefficient vanishes.
- **Invariance:** Because `P g = 0`, the projected matrix annihilates additions of the form `g a^T + a g^T`, so the tower is exactly gauge invariant.
- **Boundary:** It requires only `g != 0`, not a chart with every gradient component nonzero; higher-codimension blocks still refuse.

### `typed_elementary.py`

- **Primitives:** Rational enclosures `[lo, hi]`, domain-specific evaluation refusals, a refinement state machine, and correctly rounded elementary-function records.
- **Refinement:** Increases working precision until the lower and upper rational bounds round to the same requested `p`-bit value, or until the constructive precision ceiling is reached.
- **Constructive operations:** Builds enclosures for `log`, `exp`, `pi`, `sin`, `cos`, `asin`, `acos`, `atan`, `tan`, `log2`, and real powers using exact range reduction, rational series bounds, algebraic identities, and endpoint rounding. It does not call libm, mpmath, or SymPy for the verdict.
- **Domain handling:** Separately refuses invalid logarithm arguments, inverse-trigonometric arguments, real-power domains, and tangent poles instead of returning non-finite floats.

### `typed_log_log_slope.py`

- **Primitives:** Positive log-log observations, ordinary least-squares coefficients, residual diagnostics, snapped rational exponents, and signed power-law coefficients.
- **Fit operation:** For `x_i = log(f_i)` and `y_i = log(abs(t_i))`, computes the OLS slope, intercept, `R^2`, standard error, RMS residual, maximum residual, and relative RMS residual.
- **Power-law recovery:** Interprets `y = alpha + p x` as `abs(t) = exp(alpha) f^p`, recovers the coefficient sign from the observations, and reports `t approximately C f^p`. Exact-zero observations receive a separate zero-power status rather than being logged.
- **Boundary:** Fits are measured floating evidence; exponent snapping is a classification aid, not an exact identity proof.

### `typed_ulp.py`

- **Primitives:** IEEE 754 binary32/binary64 bit patterns, sign/exponent/fraction fields, adjacent representable values, exact rational spacings, and value-class records.
- **Operations:** Rounds inputs to the requested format, decodes their bit representation, finds the next representable value above the positive magnitude, and returns `ULP(x)` both as a float and an exact rational difference.
- **Special cases:** Handles zero/subnormals, normals, infinities, and NaNs explicitly; only finite lattice spacings are usable in exact burden calculations.

### `__pycache__/`

- **Primitives:** None; it contains interpreter-generated bytecode files.
- **Operations:** None at the source level. Python may create or replace these files when modules are imported or compiled.
