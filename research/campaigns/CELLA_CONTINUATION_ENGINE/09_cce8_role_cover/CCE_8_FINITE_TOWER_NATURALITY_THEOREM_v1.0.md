# CCE-8 finite-tower naturality theorem

**Outcome:** `PROMOTED`

Let (J_N=mathbb Q[D,S]_{geq1}/(D,S)^{N+1}) and let
(	au_{N,r}:J_N	o J_r), (2leq rleq N), be truncation.  On the regular
active-role locus, the exact role generators (s,t) implemented by CCE-8
satisfy

\[
\tau_{N,r}(s f)=s\tau_{N,r}(f),
\qquad
\tau_{N,r}(t f)=t\tau_{N,r}(f).
\]

Consequently, for every finite word (w\in\langle s,t\rangle),

\[
\boxed{\tau_{N,r}(w f)=w\tau_{N,r}(f).}
\]

## Proof

The generator (s) exchanges the two variables and therefore preserves the
total-degree filtration.  The generator (t) is the recursively unique
formal inverse (D=g(P,S)).  Its coefficient in total degree (d) is
obtained by cancelling the degree-(d) coefficient of (f(g(P,S),S)), after
the inverse coefficients in degrees below (d) have been fixed.  It depends
only on the input and inverse coefficients through degree (d).  Terms of
degree greater than (r) therefore cannot affect the inverse modulo
((P,S)^{r+1}).  This proves generator naturality; induction on word length
proves the displayed identity.

The implementation independently replays the commuting square
coefficient-by-coefficient.  `FiniteTowerNaturalityWitness` binds both path
digests, the two orders, the operation word, and the recurrence argument.

## Certified surface and boundary

- Every finite (N\geq r\geq2) and every finite word in `s,t` is covered.
- The regular-chart nonvanishing hypotheses required by formal inversion are
  retained.
- This is a projective-system theorem.  It does not assert convergence of an
  analytic infinite germ.
- The order-7 hostile fixture replays truncations to orders 2 through 6 and
  rejects a mutated target order.

The production implementation is
`engine/src/cella/continuation/cce8.py`; the independent gate is
`engine/tests/gate_continuation_cce8.py`.
