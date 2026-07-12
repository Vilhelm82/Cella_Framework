# Cella-Native Ideal Decomposition

**Date:** 2026-07-11  
**Status:** Derived design; implementation not started  
**Scope:** Exact ideals in `Q[x_1,...,x_n]`, with an optional declared localization. This document concerns ideal decomposition only.

## 1. Decision

Cella should not begin by cloning a general-purpose `primaryDecomposition` command. The first native method should be a **certificate-first structured decomposition** for the ideals already occurring in the repository:

1. exact incidence and constraint ideals;
2. complete intersections obtained by adjoining named channel or stratum equations;
3. ideals localized away from a declared exceptional boundary;
4. components supplied by geometry, factorization, or an eliminant and then verified natively.

The native method has two outputs:

- a certified **minimal-prime/radical decomposition** when the complete-intersection certificate closes;
- a typed `INDETERMINATE` result when nilpotent or embedded structure remains and a full primary decomposition has not been certified.

Full arbitrary primary decomposition is a later layer built on the same ideal kernel using GTZ or Shimoyama-Yokoyama localization. It must not be faked by relabelling minimal primes as primary components.

## 2. What already exists

### Reusable Cella primitives

`src/cella/symbolic.py` already provides:

- exact sparse polynomials over `Q`;
- canonical term collection;
- exact addition, subtraction, multiplication, scaling, and integer powers;
- exact rational functions over a fixed polynomial ring;
- a restricted exact parser;
- exact cross-multiplication equality for rational functions.

`src/cella/certificate.py` already provides:

- canonical serialization;
- deterministic digests;
- double-run agreement before certificate emission.

`src/cella/refusal.py` already provides a usable refusal for unsupported cases:

```text
INDETERMINATE
```

The refusal stratum should state the precise failed decomposition gate, such as `non_complete_intersection`, `nonreduced_generic_component`, `prime_certificate_missing`, or `degree_balance_failed`.

### Current non-native authority

`tools/wreath_engine` currently generates Macaulay2 calls to:

```text
minimalPrimes
primaryDecomposition
saturate
eliminate
```

Those runs are valuable regression oracles, but they are not native primitives. The current decomposition output also proves less than the desired Cella record: it reports component counts and generators, but does not emit a complete independently checkable equality/intersection certificate.

## 3. The missing irreducible kernel

The existing `Poly` type is not yet an ideal engine. These operations are genuinely new and cannot be derived from addition/multiplication alone:

1. selectable monomial orders (`Lex`, `GRevLex`, and block elimination order);
2. leading monomial and leading term;
3. monomial divisibility, least common multiple, and quotient;
4. multivariate polynomial division and normal form;
5. S-polynomials and a deterministic Buchberger algorithm;
6. reduced/interreduced Gröbner bases;
7. ideal membership and equality;
8. ideal sum, product, power, intersection, and saturation;
9. elimination ideals;
10. dimension and degree from the leading-monomial ideal/Hilbert data;
11. Jacobian matrices and minors;
12. exact univariate square-free factorization and factor certificates.

Everything above can use the existing exact `Fraction` coefficients and sparse exponent tuples. No floating arithmetic belongs on this path.

## 4. Native ideal identities

Let `R = Q[x_1,...,x_n]` and let `I,J` be ideals of `R`.

The initial kernel needs only a small set of exact constructions.

### Membership and equality

For a Gröbner basis `G` of `I`,

```text
f in I  iff  NF_G(f) = 0.
```

Ideal equality is mutual generator containment:

```text
I = J  iff  every generator of I reduces to zero modulo G_J
             and every generator of J reduces to zero modulo G_I.
```

### Elimination

With a block order placing eliminated variables above retained variables, the elements of a Gröbner basis that contain only retained variables generate the contraction to the retained polynomial ring.

### Intersection

Introduce a new variable `t`. Then

```text
I intersect J = (t I + (1-t) J) intersect R.
```

The final contraction is an elimination ideal. Repeating this construction gives the intersection of any finite component list.

### Saturation

For a polynomial `d`, introduce a new variable `t`. Then

```text
I : d^infinity = (I + <1-t d>) intersect R.
```

This is the required operation for a declared generic-open denominator. It must be performed before decomposition, and the denominator must be recorded in the certificate.

### Projection rule

Decompose upstairs before eliminating sheet or auxiliary variables. Contraction distributes over a finite intersection:

```text
(intersection_i Q_i) intersect S = intersection_i (Q_i intersect S)
```

for a polynomial subring `S`. Projected components may become equal and must be canonicalized and merged. A slice is a new ideal and must be decomposed again; generic components cannot simply be substituted and assumed to remain complete.

## 5. Core decomposition theorem

The main native fast path is a complete-intersection certificate.

### Theorem: certified radical decomposition of a complete intersection

Let

```text
R = Q[x_1,...,x_n],
I = <f_1,...,f_c>,
height(I) = c.
```

Let `P_1,...,P_r` be distinct candidate ideals. Suppose Cella certifies:

1. `I subset P_i` for every `i`;
2. every `P_i` is prime;
3. `height(P_i) = c` for every `i`;
4. for every `i`, some `c x c` minor of the Jacobian of `(f_1,...,f_c)` is nonzero modulo `P_i`;
5. the degree balance

   ```text
   degree(I) = sum_i degree(P_i)
   ```

   holds exactly.

Then

```text
I = intersection_i P_i,
```

and `I` is radical. Consequently this is both the minimal-prime decomposition and a primary decomposition whose components are prime.

### Why the theorem works

`height(I)=c` makes the generators a regular sequence in the polynomial ring, so `R/I` is a complete intersection and therefore Cohen-Macaulay. A Cohen-Macaulay quotient has no embedded associated primes.

The nonzero Jacobian minor makes each candidate component generically reduced. The degree formula for an unmixed ideal is a positive sum over all minimal primes, weighted by their generic lengths. Exact degree balance therefore proves simultaneously that:

- no candidate component is missing;
- no additional minimal component exists;
- every generic length is one.

Thus `R/I` satisfies generic reducedness plus the no-embedded-prime condition, so it is reduced. Its defining ideal is the intersection of exactly the certified primes.

This route is much smaller than generic primary decomposition and matches the structure of the repository's incidence and stratum ideals.

## 6. Localized decomposition theorem

Let `d` be the explicitly declared product of boundaries excluded from the current calculation. First compute

```text
I_open = I : d^infinity.
```

Apply the complete-intersection theorem to `I_open`, not to `I`.

If a radical decomposition of `I` is already known,

```text
I = intersection_i P_i,
```

then saturation keeps exactly the components on which `d` is not identically zero:

```text
I : d^infinity = intersection_(d notin P_i) P_i.
```

The output must record removed components. They are excluded by the declared chart; they are not algebraically nonexistent.

## 7. Candidate-prime certificates

The method separates **finding** a candidate from **proving** it prime. Candidate discovery may use known geometry, exact factorization, a declared contact sign, or an eliminant. Certification must use one of the following native proof routes.

### P1: linear elimination certificate

If a Gröbner basis solves some variables by monic linear equations and leaves a polynomial ring in the remaining variables, the quotient is a polynomial ring and hence a domain. The ideal is prime.

This is the preferred route for signed contact components and graph-like incidence components.

### P2: triangular field/domain tower

After a variable ordering, suppose a triangular basis is monic successively and each new univariate polynomial is certified irreducible over the fraction field of the preceding domain. Then the quotient is an iterated domain extension, so the ideal is prime.

This route requires exact univariate factorization over `Q` first. Factorization over algebraic or rational-function extensions is a later extension.

### P3: explicit inverse maps

If the component has an explicit parametrization and inverse, verify both compositions by ideal normal forms. An isomorphism to a polynomial ring or a previously certified domain proves primality.

### Refusal boundary

If none of P1-P3 closes, return:

```text
Refusal(
  "INDETERMINATE",
  stratum="prime_certificate_missing:<component>",
  detail="candidate component found but primality was not certified natively"
)
```

Do not promote a probable or externally reported prime.

## 8. Decomposition algorithm

### Inputs

```text
ring:
  variables
  monomial_order
ideal_generators
localization_denominator        # optional; default 1
candidate_components            # optional but expected in MVP
prime_certificate_hints         # linear, triangular, or explicit map
```

### Procedure

1. **Parse and canonicalize.** Convert every generator to an exact sparse polynomial. Reject rational-function denominators and decimal coefficients.
2. **Canonical ideal basis.** Compute a deterministic reduced Gröbner basis for the input ideal.
3. **Localize.** If `d != 1`, compute `I_open = I:d^infinity` with the Rabinowitsch construction.
4. **Reject the empty chart.** If `I_open=<1>`, return a certified empty-locus result.
5. **Compute invariants.** Record dimension, codimension, degree, leading ideal, and Gröbner digest.
6. **Check complete intersection.** Reduce the input to a minimal generator set where supported and require `generator_count = codimension`. If this cannot be certified, refuse the fast path.
7. **Obtain candidates.** Use supplied geometric candidates or exact factors of a supported eliminant. Candidate discovery is `exploratory` until the remaining gates close.
8. **Normalize candidates.** Saturate each candidate by the same `d`, discard `<1>`, compute reduced Gröbner bases, and merge equal ideals.
9. **Containment.** Reduce every generator of `I_open` modulo every candidate basis.
10. **Prime gates.** Certify every candidate by P1, P2, or P3.
11. **Height and distinctness.** Require equal height and pairwise unequal reduced bases.
12. **Jacobian gates.** Find a full-rank Jacobian minor whose normal form modulo each candidate is nonzero.
13. **Degree balance.** Require exact equality between `degree(I_open)` and the sum of candidate degrees.
14. **Intersection replay.** Independently construct `J=intersection_i P_i` using auxiliary-variable elimination and certify `J=I_open` by mutual normal-form containment.
15. **Emit.** Return the ordered component list, proof route for every prime, invariant table, intersection replay, dependencies, and rerun digest.

Step 14 is deliberately redundant. The theorem already closes at Step 13, but explicit intersection replay is cheap enough for the supported scale and catches implementation errors in dimension, degree, or candidate handling.

## 9. Nonreduced and embedded cases

The radical fast path must detect rather than hide scheme structure.

### Nonreduced signal

If a candidate has the right support but its Jacobian rank drops generically or

```text
degree(I) > sum_i degree(P_i),
```

then at least one generic multiplicity exceeds one or a component is missing. Return the component supports and measured degree deficit as `exploratory`, followed by an `INDETERMINATE` refusal for primary decomposition.

### Embedded signal

If `generator_count != codimension`, the complete-intersection/no-embedded-prime theorem is unavailable. An example is

```text
I = <x^2, x y>.
```

Its radical support is `<x>`, but it also has embedded structure. Returning only `<x>` would lose part of the ideal.

### Later full-primary route

The later general algorithm should be Shimoyama-Yokoyama or GTZ:

1. compute minimal associated primes;
2. localize using maximal independent variable sets;
3. reduce to zero-dimensional decomposition over rational-function coefficient fields;
4. extract and contract isolated primary components by saturation;
5. form the residual ideal quotient and recurse for embedded components;
6. verify the final intersection exactly.

That route requires factorization over finitely generated fields and generalized coefficient domains. It is not a sensible MVP dependency for the structured Wreath ideals.

## 10. Proposed module boundary

```text
src/cella/monomial.py
    MonomialOrder
    monomial_divides
    monomial_lcm

src/cella/groebner.py
    divide
    normal_form
    s_polynomial
    buchberger
    reduced_basis

src/cella/ideal.py
    Ideal
    contains
    equals
    sum
    product
    power
    intersect
    saturate
    eliminate
    dimension_degree

src/cella/ideal_decomposition.py
    PrimeCandidate
    PrimeCertificate
    DecompositionCertificate
    decompose_complete_intersection
    verify_decomposition
```

`symbolic.py` remains the scalar polynomial/rational-function layer. It should not absorb ideal algorithms and become another monolith.

## 11. Certificate shape

```json
{
  "status": "certified",
  "kind": "radical_complete_intersection_decomposition",
  "ring": {
    "coefficients": "Q",
    "variables": ["x", "y"],
    "order": "GRevLex"
  },
  "input_basis": ["x*y"],
  "localization_denominator": "1",
  "dimension": 1,
  "codimension": 1,
  "degree": 2,
  "complete_intersection": true,
  "components": [
    {
      "basis": ["x"],
      "prime": true,
      "prime_proof": "linear_elimination",
      "dimension": 1,
      "degree": 1,
      "jacobian_witness": "y"
    },
    {
      "basis": ["y"],
      "prime": true,
      "prime_proof": "linear_elimination",
      "dimension": 1,
      "degree": 1,
      "jacobian_witness": "x"
    }
  ],
  "degree_balance": "2 = 1 + 1",
  "intersection_replay": true,
  "removed_by_localization": [],
  "certificate_digest": "..."
}
```

## 12. Mandatory falsification fixtures

The gate must include at least these exact cases.

| Ideal | Expected result |
|---|---|
| `<x*y>` | Certified `<x> intersect <y>`. |
| `<x^2-y^2>` | Certified `<x-y> intersect <x+y>` over `Q`. |
| `<x^2,y>` | Refuse radical decomposition: one support `<x,y>` with generic multiplicity 2. |
| `<x^2,x*y>` | Refuse complete-intersection route: embedded structure is possible/present. |
| `<x*y> : x^infinity` | Certified localized result `<y>` and record `<x>` as removed. |
| `<w^2-u-N^2,u>` localized by `2N` | Certified two contact components `<u,w-N>` and `<u,w+N>`. |
| `<x^2-a,x-1>` | Certified prime `<x-1,a-1>` by linear elimination. |
| a slice causing two generic components to merge | Recompute and report the merged/special multiplicity; never substitute the generic answer unchanged. |

Mutation catchers must fail if:

- degree balance is ignored;
- a Jacobian witness reduces to zero on a component;
- saturation silently deletes an undeclared boundary;
- projected equal components are counted twice;
- a radical support list is labelled a primary decomposition;
- an external Macaulay2 claim is accepted without native replay.

## 13. Implementation order

1. monomial order and multivariate normal form;
2. deterministic Buchberger and reduced bases;
3. membership/equality, intersection, saturation, and elimination;
4. dimension/degree and Jacobian witnesses;
5. P1 linear prime certificates;
6. complete-intersection decomposition theorem and fixtures;
7. P2 univariate/triangular prime certificates;
8. optional candidate finder from supported eliminant factorization;
9. only then investigate the full SY/GTZ primary layer.

The first useful milestone is Steps 1-6. It already replaces the decomposition calls needed for split reduced channel/contact ideals and gives a mathematically honest refusal on the difficult cases.

## 14. References used for the derivation

- Gianni, Trager, and Zacharias, *Gröbner Bases and Primary Decomposition of Polynomial Ideals*, Journal of Symbolic Computation 6 (1988), 149-167, DOI `10.1016/S0747-7171(88)80040-3`.
- Shimoyama and Yokoyama, *Localization and Primary Decomposition of Polynomial Ideals*, Journal of Symbolic Computation 22 (1996), 247-277, DOI `10.1006/jsco.1996.0052`.
- The Stacks Project, tags `00N6` (regular sequences in Cohen-Macaulay modules), `00N2` (Cohen-Macaulay modules have no embedded associated primes), `00SB` (local complete intersections are Cohen-Macaulay), and `031R` (reduced equals `R_0 + S_1` for Noetherian rings).

