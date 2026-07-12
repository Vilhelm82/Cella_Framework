# DBP native relative periods

This package certifies exactly four views of two fixed relative periods on
`E128`: `trace_primary`, `primary`, `trace_dual_real_cpv`, and `dual_cpv`.
It is not a general elliptic evaluator and has no runtime CPV crossing.

The exact route compiler first removes the dual source pole.  The executor then
uses a frozen, compile-time-scouted schedule of fixed algebraic Taylor
recurrences.  At runtime it independently checks complex analytic separation,
coefficient-account closure, and a Cauchy tail bound on every panel.  The scout
and decimal regression pins are absent from the production dependency graph and
certificate evidence.

Unsupported curves, differentials, paths, sheets, prescriptions, and precision
requests return typed `PeriodRefusal` records; there is no numerical fallback.

`legendre_ke.py` is a separate numerical realization for the classical
Legendre `K` and `E` atoms on `0 <= m < 1`.  It accepts exact `Fraction` and
fixed-radicand `QSqrt` parameters, keeps series partial sums in that field,
uses `typed_elementary.pi_eval` for `W0 = pi/2`, and carries the complementary
Legendre pinning identity as a certificate register.  It is not used by the
DBP evaluator and does not implement `Pi`, Landen descent, or general field
normalization.
