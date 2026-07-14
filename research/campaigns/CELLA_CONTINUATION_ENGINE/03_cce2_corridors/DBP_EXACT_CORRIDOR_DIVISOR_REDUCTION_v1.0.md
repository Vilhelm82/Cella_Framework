# DBP exact corridor divisor reduction v1.0

**Scope:** curve family and relative third-kind data only  
**Surface clearance:** not certified; deferred to CCE-6

Put `rho^2=1+sigma^2` and use the continued branch of `rho`.  The complete
CCE-2 curve ledger reduces to

```text
sigma, sigma-i, sigma+i,
rho, rho-1, rho+1,
m, 1-m, 1-2m, n, 1-n, c, 1/c,
x_p, x_p-1, x_p-m, y_p^2.
```

The exact reductions in `Q(rho)` are

```text
(rho-1)(rho+1) = sigma^2
m = (rho-1)/(2rho)              1-m = (rho+1)/(2rho)
1-2m = 1/rho
n = -(rho-1)^2/(4rho)           1-n = (rho+1)^2/(4rho)
c = (rho-1)/(rho+1)
x_p = -2/(rho-1)
x_p-1 = -(rho+1)/(rho-1)
x_p-m = -(rho+1)^2/(2rho(rho-1))
y_p^2 = -(rho+1)^3/(rho(rho-1)^3).
```

Consequently the elliptic branch values `0,1,m,infinity`, marked endpoints
`Q_0,Q_m`, and the two third-kind poles remain mutually admissible whenever
`rho`, `rho-1`, and `rho+1` do not vanish.  In particular `y_p^2 != 0`
separates `P^+` from `P^-`, while `x_p`, `x_p-1`, and `x_p-m` exclude pole
collision with the finite elliptic branch points.

## Certified rational bounds

The following deliberately conservative lower bounds are replayed in exact
rational arithmetic.  They are bounds for absolute values, except for
`y_p^2`, which is already an absolute-value bound for that rational function.

| factor | route | radius-1/8 base tube pullback |
|---|---:|---:|
| `sigma` | `1/2` | `3/8` |
| near branch factor | `1/2` | `3/8` |
| far branch factor | `1` | `7/8` |
| `rho` | `1/2` | `1/2` |
| `rho-1`, `rho+1` | `1/32` | `1/64` |
| `m`, `1-m` | `1/192` | `1/512` |
| `1-2m` | `1/3` | `1/4` |
| `n`, `1-n` | `1/12288` | `1/65536` |
| `c`, `1/c` | `1/128` | `1/320` |
| `x_p` | `1/2` | `2/5` |
| `x_p-1` | `1/128` | `1/320` |
| `x_p-m` | `1/24576` | `1/163840` |
| `y_p^2` | `1/6291456` | `1/131072000` |

The tube statement concerns the regular base tube and its nonsingular
pullback double cover.  An odd-winding base tube has no global single-valued
choice of `rho`; all inequalities are sheet-independent absolute-value
statements.  No claim is made about `v=1/c`, `v=1/c^2`, a norm discriminant,
surface polar loci, or a swept surface boundary.
