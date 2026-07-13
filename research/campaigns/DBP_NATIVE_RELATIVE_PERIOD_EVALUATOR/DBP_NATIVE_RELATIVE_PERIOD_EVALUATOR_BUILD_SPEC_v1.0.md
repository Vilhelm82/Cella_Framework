# DBP Native Relative-Period Evaluator

## Build specification, v1.0

**Date:** 2026-07-12  
**Mathematical authority:** `DBP_LANDEN_TRACE_THEOREM_COMPLETE_v1.1.md` and `DBP_NATIVE_RELATIVE_PERIOD_ROUTE_THEOREM_v1.0.md`  
**Product boundary:** a native certified evaluator for the two fixed DBP relative periods on (E_{128})  
**Explicitly separate from:** Pathfinder route discovery and general elliptic-function evaluation

---

## 1. Product definition

Build a native module that returns certified dyadic brackets for

\[
I_{\rm primary}
=
\frac12\int_0^1g_+(t)\,dt-2\pi
\]

and

\[
I_{\rm dual,CPV}
=
\frac12\int_0^1g_-(t)\,dt,
\]

where (g_+) and (g_-) are the smooth algebraic kernels in the route theorem.

The module must certify its own answer. A decimal approximation, agreement with a
library, or agreement with the stored pins is not a certificate.

The central execution rule is:

> Apply the theorem-directed exact reduction first; execute only the resulting
> smooth finite-interval route; carry floating roundoff as measured account data;
> materialize the enclosing bracket only at the terminal cut.

---

## 2. What v1 owns

The v1 evaluator owns exactly four public targets:

| Target | Meaning | Final formula |
|---|---|---|
| `trace_primary` | (J_+=\int_{\Gamma_+}\Theta) | (\int_0^1g_+(t)dt) |
| `primary` | DBP primary constant | (J_+/2-2\pi) |
| `trace_dual_real_cpv` | (H_-=-i\,\mathrm{CPV}\int_{\Gamma_-}\Theta) | (\int_0^1g_-(t)dt) |
| `dual_cpv` | DBP dual CPV constant | (H_-/2) |

The dual execution kernel is an ordinary smooth integral. The certificate must still
record the source pole (X=-7), residue (4), physical sheet, polar subtraction, and
the proof that the subtracted kernel has zero CPV.

---

## 3. Non-goals and mandatory refusals

The following are not part of v1:

- arbitrary (K(m)), (E(m)), or (Π(n;m)) evaluation;
- AGM, Carlson-form, or generic elliptic evaluation;
- arbitrary elliptic curves, rational differentials, or relative paths;
- discovery of the Landen--Trace route;
- a scalar relation between the primary and dual path values;
- one-sided dual continuation unless the caller supplies an explicit side and branch;
- a general proof of the proposed analytic-atom composition theorem;
- Pathfinder integration.

Unsupported input must return a typed refusal. It must never fall back silently to
mpmath, SymPy, SciPy, FLINT/Arb, a system elliptic routine, or a decimal pin.

Required refusal tokens:

- `unsupported_curve`
- `unsupported_differential`
- `unsupported_relative_path`
- `sheet_not_declared`
- `cpv_side_not_declared`
- `route_identity_failed`
- `domain_separation_failed`
- `account_not_closed`
- `remainder_bound_failed`
- `precision_budget_exhausted`
- `oracle_dependency_detected`

---

## 4. Authoritative exact data

The recognized source record is

\[
E_{128}:Y^2=X^3-X^2+X-1=(X-1)(X^2+1),
\]

\[
\Theta=8\frac{X-3}{X+7}\frac{dX}{Y}.
\]

The two path records are:

### Primary

- start: (X=1), branch point;
- end: (+∞);
- sheet: (Y>0) for (X>1);
- pole crossings: none.

### Dual CPV

- start: (X=1), branch point;
- end: (-∞);
- sheet: (Y=+i\sqrt{-(X-1)(X^2+1)}) for (X<1);
- source pole: (X=-7), (Y=20i);
- residue of (-i\Theta): (4);
- prescription: real Cauchy principal value.

The execution kernels are copied verbatim from the route theorem. Put (w=1-t),
(s=\sqrt2):

\[
P_+=t^4+2t^2w^2+2w^4,
\]

\[
g_+=16\frac{t^2-2w^2}{t^2+8w^2}\frac1{\sqrt{P_+}},
\]

\[
P_-=(t^2-w^2)^2+w^4,
\]

\[
g_-=-\frac{16t^2}{\sqrt{P_-}(t^2+2w^2+s\sqrt{P_-})}.
\]

No runtime denominator (t^2-8w^2) is permitted in the dual kernel. Its presence
means the exact cancellation was not compiled and is a build failure.

---

## 5. Module layout

The names may be adapted to the repository, but ownership must remain separated:

```text
native_periods/
  __init__.py
  exact_scalar.py          # dyadics and Q(sqrt(2)) proof scalars
  records.py               # curve, differential, path, pole, branch records
  dbp_theta_route.py       # exact matcher and theorem-directed compiler
  dbp_theta_kernels.py     # fixed straight-line g_plus / g_minus kernels
  eft.py                   # TwoSum, FastTwoSum, TwoProd/FMA, renormalization
  account.py               # operation defects and sensitivity/remainder account
  sqrt_account.py          # sqrt reading, exact square defect, terminal bound
  quadrature.py            # deterministic dyadic-panel certified integrator
  jet_bound4.py            # proof-only fourth-derivative panel majorants
  terminal.py              # one terminal conversion to a dyadic bracket
  certificate.py           # canonical replay record and digest
  api.py                   # four public targets and typed refusals
tests/
  test_dbp_route_exact.py
  test_dbp_native_vectors.py
  test_dbp_branch_refusals.py
  test_account_identities.py
  test_bracket_nesting.py
  test_no_oracle_imports.py
```

`periods.py` remains the owner of formal Legendre period normal forms and residue
ledgers. Add an adapter for the (E_{128}) relative-path records; do not turn
`periods.py` itself into a floating evaluator.

---

## 6. Exact route compiler

`dbp_theta_route.py` must accept a typed source record and emit one of the two fixed
kernel records only after exact gates close.

Required gates:

1. curve coefficients equal ((a_1,a_2,a_3,a_4,a_6)=(0,-1,0,1,-1));
2. cubic factorization equals ((X-1)(X^2+1));
3. differential coefficient equals (8(X-3)/(X+7));
4. path endpoint, orientation, and sheet equal one of the two admitted records;
5. dual pole image is ((-7,20i));
6. dual residue of (-i\Theta) is (4);
7. the exact polar kernel is (16\sqrt2/(z^2-8));
8. its logarithmic primitive has equal endpoint limits and hence zero CPV;
9. the rationalizing identity (A^2-2P_-=-t^2D) closes;
10. the compiled radicand and denominator positivity witnesses are attached.

The compiler output is immutable and includes the source theorem/version identifiers.

---

## 7. Domain witnesses

The executor must not infer safety from sampled values. It consumes exact global
witnesses from the compiler.

Useful conservative witnesses on (0\le t\le1), (w=1-t), are:

\[
t^2+8w^2\ge\frac89,
\]

\[
P_+\ge t^4+w^4\ge\frac18,
\]

\[
P_-=(2t-1)^2+w^4\ge\frac1{64},
\]

and

\[
t^2+2w^2\ge\frac23.
\]

The (P_-) bound may be proved by splitting (t\le1/2),
(1/2<t<5/8), and (t\ge5/8). These bounds are intentionally conservative;
tighter exact bounds may be substituted if their proof is recorded.

---

## 8. Reading-and-account arithmetic

### 8.1 Reading

Every runtime numeric object has a first-class reading:

```text
BinaryReading {
  format,
  sign,
  exponent,
  significand,
  raw_bits
}
```

The exact dyadic value represented by the bits is recoverable without calling a
decimal parser.

### 8.2 Local operation defects

For each operation, record an identity, not an error estimate:

- addition/subtraction: `TwoSum` gives (s+e=a+b) exactly;
- multiplication: `TwoProd` (prefer FMA) gives (p+e=ab) exactly;
- division: for (q=\mathrm{fl}(a/b)), carry the exact numerator defect
  (r=a-qb), so (a/b=q+r/b);
- square root: for (q=\mathrm{fl}(\sqrt a)), carry the exact square defect
  (d=a-q^2), together with the identity
  \[
  \sqrt a-q=\frac{d}{\sqrt a+q};
  \]
- fused accumulation: record every discarded expansion component exactly.

The account must preserve signs. Replacing signed defects by absolute radii at every
node is an interval implementation and does not satisfy the target architecture.

### 8.3 Restricted composition obligation

The full general analytic-atom composition theorem is not assumed complete. For v1,
prove and implement only the restricted composition lemma for the two fixed
straight-line kernels.

The lemma must show that:

1. every local exact defect enters a transported signed account;
2. all nonlinear cross terms generated by reciprocal and square-root nodes are either
   carried explicitly or covered by a separately named remainder account;
3. the account plus the reading reconstructs the exact node value up to the named
   terminal remainder;
4. no unowned term is discarded;
5. a bracket is formed only in `terminal.py`.

If this lemma is not implemented, return `account_not_closed`. Do not label an
ordinary floating result certified.

### 8.4 Precision tiers

- **M0:** binary64 reading, at least a 40-bit certified final bracket;
- **M1:** a normalized multi-limb binary64 expansion, at least a 150-bit certified
  final bracket, sufficient to contain and reproduce the supplied 50-decimal pins;
- **M2:** adaptive limb count requested by `target_bits`.

The M0 milestone validates the architecture. The build is not complete until M1 passes.

---

## 9. Certified integration

Use a deterministic composite Simpson executor on dyadic panels for v1. This keeps all
abscissas and weights exact dyadics and avoids a second transcendental node generator.

For a panel ([a,b]), Simpson's mathematical remainder is bounded by

\[
\frac{(b-a)^5}{2880}\sup_{t\in[a,b]}|g^{(4)}(t)|.
\]

Requirements:

1. evaluate the three Simpson readings with the accounted kernels;
2. accumulate the weighted readings with EFT expansions;
3. transport the signed roundoff account separately from the quadrature remainder;
4. obtain the fourth-derivative majorant from `jet_bound4.py` using exact rational or
   (\mathbb Q(\sqrt2)) bounds;
5. bisect a panel when its exact remainder budget is too large;
6. use a deterministic priority rule so replay is bit-for-bit stable;
7. sum panel remainder budgets exactly;
8. combine reading, roundoff account, and quadrature remainder only at the terminal cut.

`jet_bound4.py` is proof infrastructure, not a moving value-ball evaluator. It may use
exact interval bounds for derivatives. The primary numeric value must still travel as a
reading plus account, not as an interval at every operation.

The implementation may later replace Simpson with a faster certified rule, but only if
the new rule has an explicit truncation theorem and deterministic exact remainder
ledger. Agreement between nested rules is evidence, not a remainder proof.

---

## 10. Terminal bracket

`terminal.py` is the only module allowed to return an enclosure.

Input:

- accumulated reading expansion;
- exact signed operation-defect account;
- exact bound for the unmaterialized nonlinear remainder;
- exact quadrature remainder bound;
- requested output precision.

Output:

```text
DyadicBracket {
  lower_numerator,
  upper_numerator,
  denominator_power_of_two,
  width_bits,
  rounded_value_bits
}
```

For `primary`, the terminal stage also consumes a certified (π) bracket from the
existing native elementary kernel. If that kernel is unavailable or cannot meet the
budget, return a refusal. Do not use `math.pi` in the certifying path.

---

## 11. Certificate record

Every successful result must include:

- theorem and route versions;
- canonical source curve/differential/path records;
- exact transformation ledger;
- source pole/residue/branch ledger;
- compiled kernel identifier;
- arithmetic format and limb count;
- panel tree and exact Simpson weights;
- operation-defect account digest;
- derivative/remainder witness digest;
- terminal dyadic bracket;
- deterministic replay digest;
- explicit list of unused oracle pins.

The digest proves deterministic replay of the record; it is not a substitute for the
mathematical gates.

---

## 12. Acceptance gates

### G0 — existing theorem gates

```bash
python verify_dbp_landen_trace_theorem.py
python verify_dbp_landen_trace_theorem_v1_1.py
python verify_dbp_native_relative_period_route.py
```

All must pass.

### G1 — exact route identity

The compiler must reproduce the exact (g_+) and (g_-) records in the contracts file.

### G2 — account identities

Random and adversarial tests must verify the exact TwoSum/TwoProd identities, division
residual identity, square-defect identity, expansion normalization, and account replay.

### G3 — certified convergence

At increasing target bits, brackets must be nested or overlap consistently, widths must
meet the requested budget, and the 150-bit brackets must independently round to the
stored regression prefixes.

### G4 — branch adversaries

Wrong dual sheet, missing CPV declaration, reversed path without sign update, altered
pole, and one-sided continuation without side declaration must refuse.

### G5 — no singular execution

The dual compiled kernel must contain no division by (t^2-8(1-t)^2) and must evaluate
normally at the former pole.

### G6 — no production oracle

Production modules must not import or call mpmath, SymPy, SciPy, FLINT/Arb, Sage,
Mathematica, `ellipk`, `ellipe`, `ellippi`, Carlson forms, or an AGM evaluator.

### G7 — pin independence

Deleting the decimal pins must not change the returned bracket or certificate.

### G8 — reproducibility

Two clean runs with the same target bits must emit byte-identical canonical certificate
records.

---

## 13. What this build retires

For the two DBP targets only, the completed build retires these execution routes:

- generic (K/Π) evaluation of the original formulas;
- runtime CPV quadrature across the dual pole;
- arbitrary third-kind reduction for the anti sector;
- the discarded incomplete-Π interpretation;
- numerical cancellation between large complete-period terms.

It does not retire:

- `periods.py` as the exact structural period/residue ledger;
- (K,E,Π), AGM, Carlson, or Arb for unrelated claims;
- a future general relative-period evaluator;
- a future general composition theorem;
- Pathfinder as a separate route planner.

---

## 14. Definition of done

The evaluator is done when:

1. all G0--G8 gates pass;
2. both DBP constants have at least 150-bit certified dyadic brackets;
3. the brackets reproduce the independent decimal pins without using them;
4. the dual execution trace contains no pole or CPV numerical operation;
5. the certificate fully records the source pole and its exact removal;
6. no external numerical oracle occurs in the production dependency graph;
7. the README states the exact scope and refuses broader claims;
8. a clean build and test command is recorded in the handoff.

