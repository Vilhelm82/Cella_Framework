# Agent Race Problem Paper 001

Each solver receives this paper and must produce a JSON report. The paper is intentionally engine-neutral. Use any mathematically valid route allowed by the separate engine brief.

For every case, return one answer string. Exact cases must return an exact expression or exact rational value. Numeric cases must return enough digits to satisfy the stated absolute tolerance.

## Required Report Shape

```json
{
  "engine": "engine-name",
  "cases": [
    {
      "case_id": "P001",
      "status": "pass",
      "answer": "answer string",
      "elapsed_ms": 0.0,
      "native_ms": 0.0,
      "filler_ms": 0.0,
      "native_steps": ["engine-native operations used"],
      "filler_steps": ["basic Python filler operations used"],
      "method": "short description",
      "working_precision": "optional string"
    }
  ]
}
```

Allowed `status` values are `pass`, `fail`, `timeout`, and `unsupported`. Only `pass` answers are judged for correctness.

Every solver may use basic Python filler for parsing, orchestration, exact string formatting, timing, simple arithmetic glue, and small missing primitives. The report must split each case's wall-clock time into:

- `native_ms`: time spent inside the engine-native route or allowed native library calls.
- `filler_ms`: time spent in Python filler, glue, or hand-coded replacement logic.
- `native_steps`: short labels for the native route pieces.
- `filler_steps`: short labels for Python filler pieces.

The filler split is not an automatic failure. It is measurement data: high filler percentage identifies primitive gaps or places where a solver had to leave its native substrate.

## Cases

### P001: Rational Collapse

Simplify the rational expression

```text
((S + Q)^2 - S^2)/(Q*(2*S + Q))
```

Return the exact simplified value. Assume denominators are nonzero.

Comparison: exact.

### P002: Polynomial Identity Defect

Compute the exact polynomial defect

```text
x^4 + 4*y^4 - (x^2 - 2*x*y + 2*y^2)*(x^2 + 2*x*y + 2*y^2)
```

Return the exact simplified polynomial.

Comparison: exact.

### P003: Hilbert Determinant

Let `H` be the `7 by 7` matrix with entries

```text
H[i,j] = 1/(i + j + 1),  0 <= i,j < 7
```

Return `det(H)` exactly as a rational number.

Comparison: exact rational.

### P004: Tiny Square-Root Difference

Evaluate

```text
sqrt(1 + 10^-50) - 1
```

Return a decimal value with absolute error at most `1e-80`.

Comparison: decimal absolute tolerance `1e-80`.

### P005: Principal Complex Branch

Evaluate the principal value of

```text
log(exp(i*pi))
```

Return the complex value as `real+imag i` with absolute error at most `1e-70` in both components.

Comparison: complex rectangular absolute tolerance `1e-70`.

### P006: Local Diagonal Metric Pole

For the diagonal metric germ

```text
g_xx = B*x^2
g_yy = A*x^-2
g_zz = C*x^-2
```

with nonzero leading units `A`, `B`, and `C`, compute the coefficient of the leading scalar-curvature term multiplying `x^-4`.

Return the coefficient as an exact symbolic expression in `B`.

Comparison: exact symbolic string after whitespace removal.

### P007: Master Exponent Pole

For a diagonal metric germ with radial exponent `p0=2` and transverse exponents `p1=-1`, `p2=-3`, scalar curvature has leading form

```text
R = C/B * x^-(p0 + 2)
```

Compute `C/B`.

Comparison: exact rational expression.

### P008: Clustered Root Gap

The polynomial

```text
(x - 1)^2 * (x - (1 + 10^-30))
```

has two distinct real root locations. Return the positive distance between the two distinct root locations.

Comparison: decimal absolute tolerance `1e-60`.

### P009: Residue Contour Integral

Let `gamma(t)=2*exp(i*t)` for `0 <= t <= 2*pi`. Compute

```text
integral_gamma dz/(z - 1/3)
```

Return the complex value as `real+imag i` with absolute error at most `1e-70` in both components.

Comparison: complex rectangular absolute tolerance `1e-70`.

### P010: First Asymptotic Coefficient

Compute

```text
lim_{eps -> 0} (sqrt(1 + eps) - 1)/eps
```

Return the exact value.

Comparison: exact rational.
