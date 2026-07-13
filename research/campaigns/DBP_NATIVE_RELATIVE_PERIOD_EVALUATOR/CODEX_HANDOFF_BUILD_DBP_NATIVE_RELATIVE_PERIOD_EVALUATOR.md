# Codex handoff: build the DBP native relative-period evaluator

## Mission

Implement and finish the certified native evaluator specified in this kit. The target is
bounded: evaluate the two corrected DBP relative periods through the fixed smooth
(E_{128}) route. Do not expand the job into Pathfinder, a general elliptic library, or
route-family coverage work.

The product claim is:

> The corrected DBP relative-period problem was theoremically compiled to one of two
> smooth algebraic integrals on ([0,1]), and the native executor evaluated only that
> route while carrying roundoff as account data and forming a certified dyadic bracket
> at the terminal cut.

---

## Read first, in this order

1. `DBP_LANDEN_TRACE_THEOREM_COMPLETE_v1.1.md`
2. `DBP_NATIVE_RELATIVE_PERIOD_ROUTE_THEOREM_v1.0.md`
3. `DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR_BUILD_SPEC_v1.0.md`
4. `DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR_CONTRACTS_v1.0.json`
5. `DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR_GAP_LEDGER_v1.0.md`
6. `periods.py`
7. `verify_dbp_landen_trace_theorem.py`
8. `verify_dbp_landen_trace_theorem_v1_1.py`
9. `verify_dbp_native_relative_period_route.py`

`E_ATOM_DERIVATION.md` and `legendre_native.py` are context/reference artifacts. They
are not production dependencies of this direct route.

---

## Preserve and reuse

- Do not delete or rewrite the theorem sources or existing verifiers.
- Do not replace `periods.py`. Preserve its structural period/residue ownership and add
  a narrow (E_{128}) relative-path adapter beside it.
- Reuse existing repository exact scalars, refusals, certificates, EFT primitives, and
  native `pi_eval` when their semantics satisfy the contracts.
- Audit before adding a duplicate primitive. If an existing primitive is partial, extend
  it in place with tests when safe.
- Preserve unrelated user changes in the worktree.

---

## Exact execution route

Implement these kernels exactly, with (w=1-t):

```text
P_plus  = t^4 + 2*t^2*w^2 + 2*w^4
g_plus  = 16*(t^2 - 2*w^2)/(t^2 + 8*w^2)/sqrt(P_plus)

P_minus = (t^2 - w^2)^2 + w^4
g_minus = -16*t^2 /
          (sqrt(P_minus)*(t^2 + 2*w^2 + sqrt(2)*sqrt(P_minus)))
```

Then

```text
J_plus        = integral_0^1 g_plus(t) dt
I_primary     = J_plus/2 - 2*pi
H_minus       = integral_0^1 g_minus(t) dt
I_dual_CPV    = H_minus/2
```

The dual runtime kernel must not contain `t^2 - 8*w^2`, a pole check, or a CPV split.
Those belong only to the source certificate ledger. If the former pole survives into
execution, the route compiler is wrong.

---

## Implementation sequence

### 1. Establish the repository baseline

- Locate the existing Cella package, test runner, exact scalar types, refusal types,
  certificate serializer, EFT code, and `typed_elementary.pi_eval`.
- Run the existing tests before editing.
- Run all three exact DBP verifiers supplied in this kit.
- Record the clean baseline and any pre-existing failures.

### 2. Add typed source records and the exact route compiler

Implement immutable records for:

- (E_{128});
- (Θ);
- primary and dual relative paths;
- sheet/orientation;
- pole/residue/CPV ledger;
- compiled kernel and domain witnesses.

Match exact content, not names or decimal samples. Implement every compiler gate in the
build spec. Return typed refusals on mismatch.

### 3. Add straight-line accounted kernels

Implement `g_plus` and `g_minus` as fixed straight-line programs. Do not build a general
expression AST for this milestone.

Each arithmetic operation must emit a reading and exact local defect:

- TwoSum for add/subtract;
- TwoProd/FMA for multiply;
- exact numerator defect for divide;
- exact square defect for square root;
- deterministic expansion normalization and accumulation.

Keep signs. Do not replace each local defect with an interval radius.

### 4. Close the restricted composition account

For these two fixed DAGs, implement a machine-checkable invariant showing how local
defects and nonlinear cross terms travel to the output. Carry cross terms explicitly or
place them in a named rigorously bounded terminal remainder. No term may disappear.

If the invariant cannot be proved for an operation, return `account_not_closed`.

Do not claim that this proves the general analytic-atom composition theorem.

### 5. Add certified dyadic-panel integration

Implement deterministic composite Simpson integration on dyadic panels. Use the exact
fourth-derivative remainder bound from the build spec. Generate or hard-code derivative
jets for the two kernels; do not add a general symbolic differentiator unless one already
exists and is clearly the repository owner.

Keep separate ledgers for:

- operation defects;
- nonlinear account remainder;
- quadrature remainder.

Agreement between nested meshes is a diagnostic only, never the proof of the remainder.

### 6. Materialize only the terminal bracket

`terminal.py` is the only value-enclosure boundary. It combines the reading expansion,
signed operation account, nonlinear remainder, quadrature remainder, and (for the
primary target) the certified π bracket.

Emit a canonical dyadic bracket and deterministic replay certificate.

### 7. Finish both precision milestones

- M0: binary64 reading with a certified bracket of at least 40 bits.
- M1: multi-limb binary64 expansion with a certified bracket of at least 150 bits.

The work is not done at an unaccounted float result, a route plan, a scaffold, or M0
alone.

---

## Required tests

Implement all of the following:

1. existing v1.0 and v1.1 theorem verifiers pass;
2. native route verifier passes;
3. exact compiler output equals the contracts JSON;
4. EFT identities pass adversarial and randomized bit-pattern tests;
5. division and square-root defect identities replay exactly;
6. account invariant closes at every node of both kernels;
7. domain witnesses hold without sampling;
8. dual former-pole point evaluates as an ordinary finite point;
9. production dual kernel contains no former-pole denominator;
10. wrong curve, differential, orientation, sheet, and prescription refuse;
11. final brackets meet requested width and are stable under precision escalation;
12. 150-bit brackets independently round to the supplied decimal prefixes;
13. deleting the pins does not change computation or certificates;
14. clean duplicate runs emit byte-identical certificate records;
15. production dependency audit finds no mpmath, SymPy, SciPy, FLINT/Arb, Sage,
    elliptic-library, Carlson, or AGM call.

Use external libraries only in optional referee tests that cannot enter the production
dependency graph or certificate.

---

## Required public API

```text
evaluate_dbp_relative_period(
    target: one of {
      trace_primary,
      primary,
      trace_dual_real_cpv,
      dual_cpv
    },
    target_bits: positive integer,
    certificate: bool = true
) -> CertifiedPeriodResult | Refusal
```

The result and refusal records must conform to the contracts JSON.

---

## Non-negotiable boundaries

- No Pathfinder work in this build.
- No route-family prioritization question; there are exactly two admitted kernels.
- No (K,E,Π), AGM, Carlson, or Arb execution path.
- No runtime numerical CPV crossing.
- No incomplete-third-kind claim.
- No direct primary--dual scalar identity claim.
- No hidden use of decimal pins.
- No false precision.
- No certification from route agreement alone.
- No deletion of valuable existing work.

---

## Definition of done

Do not stop until all acceptance gates G0--G8 in the build spec pass, both 150-bit
brackets are emitted, and the clean test command succeeds.

At handoff, report only:

1. files added/changed;
2. exact test command and result counts;
3. certified dyadic brackets and widths;
4. decimal renderings for readability;
5. benchmark timings, clearly separated from proof;
6. any remaining refusal boundary.

If a genuine mathematical blocker remains after exhausting the fixed route, name the
first unclosed invariant precisely and leave the build honestly non-green. Do not replace
it with a generic elliptic call.

