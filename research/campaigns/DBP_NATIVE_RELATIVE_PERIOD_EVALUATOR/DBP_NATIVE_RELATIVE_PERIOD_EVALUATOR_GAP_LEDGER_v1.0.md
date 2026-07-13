# DBP Native Relative-Period Evaluator

## Gap ledger, v1.0

**Date:** 2026-07-12  
**Rule:** closed mathematics, reusable code, missing code, and open theorem work are recorded separately

---

## 1. Current position

The DBP-specific route is mathematically reduced far enough to build a native
evaluator. The evaluator itself is not yet implemented.

The decisive simplification is now closed:

- the common trace differential is explicit on (E_{128});
- both relative paths are explicit;
- the dual pole and residue are exact;
- the dual CPV singularity can be subtracted with an exact zero-CPV kernel;
- after rationalization, both targets are smooth algebraic integrals on ([0,1]).

So the remaining gap is no longer "find an elliptic identity." It is:

> Build a certified native integral executor whose floating readings carry exact
> roundoff accounts, whose mathematical truncation error has an explicit proof,
> and whose first value bracket is formed only at the terminal cut.

---

## 2. Closed mathematics

| Item | Status | Authority |
|---|---|---|
| Complementary DBP parameters and involution | Closed | Landen--Trace v1.1 |
| Degree-two isogenies to (E_{128}) | Closed | Landen--Trace v1.1 |
| Common trace differential (Θ) | Closed | Landen--Trace v1.1 |
| Anti differential is exact logarithmic | Closed | Landen--Trace v1.1 |
| Primary anti-period (-4\pi) | Closed | Landen--Trace v1.1 |
| Dual CPV anti-period (0), one-sided (±4\pi i) | Closed | Landen--Trace v1.1 |
| Source pole ((-7,20i)), residue (4) for (-i\Theta) | Closed | Landen--Trace v1.1 |
| Pole point is non-torsion | Closed | Landen--Trace v1.1 |
| Primary trace path (1\to+∞) | Closed | Landen--Trace v1.1 |
| Dual trace path (1\to-∞) and sheet | Closed | Landen--Trace v1.1 |
| Primary compactification to smooth (g_+) | Closed | Native route theorem v1.0 |
| Dual exact zero-CPV polar subtraction | Closed | Native route theorem v1.0 |
| Dual cancellation to smooth (g_-) | Closed | Native route theorem v1.0 |
| Positive radicands and safe denominators | Closed conservatively | Build spec §7 |

The exact scripts verify the algebraic portion. The change-of-variable and CPV primitive
steps are displayed constructively in the theorem documents.

---

## 3. Reusable artifacts already present

### `periods.py`

Reusable:

- formal Legendre quartic records;
- exact rational third-kind residue ledgers;
- branch-jump records;
- exact (K/Π) normal forms;
- exact route comparison;
- explicit gap reporting.

Not reusable as the executor:

- it states in its module docstring that it is not a numeric period evaluator;
- it accepts rational parameters only;
- its period atoms remain formal;
- it has no (E_{128}) relative-path record;
- it emits `numeric_evaluation: None`.

Action: preserve it. Add an adapter/record type for the new (E_{128}) routes. Do not
replace its structural ownership with floating code.

### `verify_dbp_landen_trace_theorem.py`

Reusable exact field/rational-function kernel and the v1.0 trace/isogeny gates.

### `verify_dbp_landen_trace_theorem_v1_1.py`

Reusable exact anti-channel extension and endpoint normalization gates.

### `legendre_native.py` and `E_ATOM_DERIVATION.md`

Reusable as a derivation/prototype for the (K,E) connection and bilinear pinning.
They are not required by the direct (Θ) execution route and must not be imported by
the production evaluator.

---

## 4. Required implementation gaps

### G-A — typed (E_{128}) source records

Build immutable curve, differential, relative-path, sheet, pole, residue, and CPV
records. Canonical equality must be exact.

**Exit condition:** altered curve coefficients, path orientation, or sheet cannot match
the DBP route.

### G-B — exact route compiler

Implement the transformations and cancellation in the native route theorem. The dual
compiled kernel must not contain the former pole factor.

**Exit condition:** compiler output matches the contracts JSON exactly and the former
pole is an ordinary evaluable point.

### G-C — exact scalar support

Implement the proof scalars needed by the route:

- rationals/dyadics;
- (a+b\sqrt2);
- exact binary reading decode;
- exact signed residuals for the admitted arithmetic operations.

**Exit condition:** every constant and local defect has a canonical exact encoding.

### G-D — accounted floating kernel

Implement TwoSum, TwoProd/FMA, exact division numerator defects, exact square defects,
multi-limb normalization, and deterministic accumulation.

**Exit condition:** reading plus account replays every straight-line kernel node with no
unnamed loss.

### G-E — restricted composition lemma

This is the most important proof/code gap. For the fixed (g_+) and (g_-) DAGs, show
how signed local defects and nonlinear cross terms compose through reciprocal and square
root without turning every node into a ball.

Permitted v1 form:

- exact signed first-order account;
- explicitly transported quadratic cross account;
- one rigorously bounded higher-order terminal remainder.

**Exit condition:** a machine-checkable account invariant is tested at every node. If it
does not close, the evaluator refuses.

This closes only the fixed-kernel case. It is not the general generative composition
theorem.

### G-F — certified quadrature remainder

The operation account covers arithmetic error, not discretization error. Build a
separate proof that bounds the integral remainder.

The v1 choice is composite Simpson on dyadic panels plus exact fourth-derivative
majorants.

**Exit condition:** every accepted panel has a theorem-backed exact remainder budget;
nested-rule agreement alone is insufficient.

### G-G — terminal bracket

Combine the reading, operation account, nonlinear remainder, and quadrature remainder
once, at the terminal cut, into a dyadic bracket.

**Exit condition:** no production module other than `terminal.py` constructs a value
enclosure.

### G-H — certified (π) dependency

The primary formula needs (-2\pi). Connect to the existing native `pi_eval` if it is
present in the target repository. If it is absent, build a separate certified elementary
π evaluator; do not use `math.pi`.

**Exit condition:** the π bracket has an independent exact remainder proof and enters
the final account explicitly.

### G-I — certificate and replay

Canonicalize all source, route, account, panel, and bracket records and replay them
deterministically.

**Exit condition:** clean repeated runs emit byte-identical certificate records.

---

## 5. Open mathematics that is not a v1 blocker

| Open front | Why it is separate |
|---|---|
| General analytic-atom composition theorem | v1 needs only the two fixed algebraic DAGs |
| Arbitrary (K,E,Π) native evaluation | the DBP route bypasses these atoms |
| General relative homology/path comparison | v1 evaluates two declared paths independently |
| Scalar primary--dual relation | not implied by the trace theorem |
| Arbitrary rational differential reduction | v1 differential is fixed and already reduced |
| General algebraic number fields | v1 needs only (\mathbb Q(\sqrt2)) plus (i) in source records |
| Pathfinder integration | planning can consume this evaluator later |
| General Arb successor claim | requires breadth, not just the two DBP targets |

---

## 6. What is retired, and what is not

### Retired for these DBP targets

- evaluating the original (K/Π) combinations;
- crossing the dual pole numerically;
- generic CPV quadrature for the dual value;
- the incomplete-third-kind story for the anti differential;
- using AGM as the required DBP execution route;
- treating the 50-decimal pins as the last mathematical datum.

### Not retired globally

- `periods.py`;
- (K,E,Π) normal forms;
- AGM and Carlson methods for unrelated claims;
- Arb/ball arithmetic as an external referee;
- generic pole and CPV machinery;
- formal symbolic reduction;
- Pathfinder.

---

## 7. Build order

1. Exact records and route compiler.
2. Direct unaccounted kernel readings for developer diagnostics only.
3. M0 binary64 account identities.
4. Certified dyadic-panel remainder engine.
5. Terminal 40-bit brackets.
6. Multi-limb account arithmetic.
7. M1 150-bit brackets and independent pin match.
8. Certificate replay, refusal adversaries, and dependency audit.
9. Benchmarks against external referees, clearly outside the certifying path.

Do not begin with a general elliptic API. The first green milestone is the two exact DBP
routes.

