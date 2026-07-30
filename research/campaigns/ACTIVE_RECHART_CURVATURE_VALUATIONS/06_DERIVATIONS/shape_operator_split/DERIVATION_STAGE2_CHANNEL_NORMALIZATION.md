# Stage 2 derivation — frozen invariant and channel normalization

**Proof obligations discharged:** PO-5, PO-6, PO-7, PO-8
**Falsification gate:** `05_VERIFICATION_NEW/channel_normalization/verify_sigma2_channel_split.py`
(14 checks, all exact, all passing).

---

## Part A — scoped to what the paper requires

### A.1 The invariant

`sigma_2(S) = (1/2)((tr S)^2 - tr S^2)` of the tangent shape operator `S`. Frozen facts
(gate C1, C2):

- surface in `R^3`: `sigma_2 = K_G`;
- Euclidean hypersurface of any dimension: `R = 2*sigma_2` (verified intrinsically for
  graph hypersurfaces of dimension 2 and 3 by direct Christoffel/Ricci computation).

### A.2 The channel split (PO-5)

In the distinguished role frame, `H = Hess F` splits as `H = H_c + H_s`
(`H_s = diag H`). The channel-density polynomial (bordered minors, Paper I §5.2)

```
C_hat_2(t,u) = -sum_{|I|=3} det[[0, g_I^T],[g_I, (t H_c + u H_s)_I]]
```

has coefficients `kappa_hat_{2,0}, kappa_hat_{1,1}, kappa_hat_{0,2}`; the normalized
channels are `kappa = kappa_hat / q^2`, and canonically ordered account is

```
C = (sigma_2; kappa_c, kappa_int, kappa_s),   Sigma_channel(C) = kappa_c + kappa_int + kappa_s = sigma_2.
```

Gate C1 confirms the bordered sum equals `sigma_2` of the true tangent shape operator for
ambient dimensions 3 and 4 on random exact data — the split is well-defined in arbitrary
ambient dimension, discharging PO-5 at `r = 2`; the `n=4` Gauss–Kronecker row (`r = 3`)
closes via the Newton-identity grid (gate C6).

### A.3 Exact sequence and graph section (PO-6, PO-7)

`0 -> ker(Sigma_channel) -> ChannelAccount -> IntrinsicCurvature -> 0` is exact with
`ker = {(x,y,z) : x+y+z = 0}`. A chart account is a **lift** of the invariant through the
affine fibre `Sigma_channel^{-1}(sigma_2)` — framed data, never an extra scalar invariant.

**Graph-gauge specialization (Gate 2, passed exactly):** in any graph chart of a surface,

```
kappa_c = -M^2/Q^2,   kappa_s = L N/Q^2,   kappa_int = 0,   K_G = kappa_c + kappa_s.
```

Interaction is live exactly off the graph gauge: the keystone
`F = x1^2 + x1 x2 + x3^2 - 3` at `(1,1,1)` has `(kc, kint, ks) = (-1/49, -3/49, 1/49)`
(gate C4) — a witness that no single-channel or nonnegative proxy can carry the account.

### A.4 Defining-function gauge (PO-8)

`F_tilde = mu F`, `mu(p) = 1`, `a = grad(log mu)(p)` gives the point-normalized shift

```
g_tilde = g,     H_tilde = H + g a^T + a g^T.
```

- The tangent projection kills the shift: `P (g a^T + a g^T) P = 0` — the tangent shape
  operator, hence `sigma_2` and every elementary invariant, is gauge-invariant (gate C5).
- The channel account moves **strictly inside** `ker(Sigma_channel)` (gates C5, C7), by the
  exact keystone laws of Paper I's appendix, replayed verbatim; the coupling channel is
  pinned exactly on `w(u+3v+1) + 2uv = 0`.

### A.5 Stage-2 falsification event (recorded)

The first gate run FAILED C5: the harness's grading variables `(t,u)` collided with the
gauge symbol `u`. The paper formulas were correct; the harness was wrong. Fix: grading
variables are now Dummy symbols. This is exactly the failure mode the falsification
programme exists to catch (a wrong harness silently "correcting" a right paper), and it is
kept on record rather than erased.

---

## Part B — complementary expansion (full coverage; use-case-agnostic)

### B.1 All elementary orders, all ambient dimensions

The bordered-minor density is defined for every `1 <= r <= n-1`, with normalization
`q^{(r+2)/2}` and reduction `sigma_r = C_hat_r(1,1)/q^{(r+2)/2}`. The account at order r is
the `(r+1)`-vector of bidegree coefficients `kappa_{r;p,q}`; the kernel of the reduction is
the zero-sum hyperplane of dimension r. The full channel object is the bigraded array
`{kappa_{r;p,q}}` — the "channel grid". Gate C6 verifies the `r=3` row in ambient 4 by an
independent Newton-identity route through the split shape operators `A = S[H_c]`,
`B = S[H_s]`.

### B.2 What is canonical and what is frame-relative

- Canonical given (Sigma, p): the flag `sigma_1, ..., sigma_{n-1}` (all invariants).
- Canonical given (Sigma, p, role frame): the channel grid.
- Gauge-relative inside a fixed frame: nothing — PO-8 shows defining-function gauge moves
  no invariant and no *tangent* operator, only the ambient-Hessian account coordinates
  within the kernel fibre. The gauge orbit through an account is an affine subspace of the
  fibre, of dimension <= n (the dimension of the `a`-space), with explicit rational
  parametrization (keystone laws); pinning loci of any single channel are algebraic
  hypersurfaces in gauge space.

### B.3 Use-case-agnostic reading

For any constraint among n+1 observables, the account answers "*where does the curvature
sit in the declared frame*": coupling (pure cross-sensitivities), self (pure own-
sensitivities), interaction (the part that only exists off graph presentations). The
`kint = 0` graph theorem is the agnostic statement that **choosing an output variable is
exactly the choice that kills interaction bookkeeping locally** — interaction is a property
of implicit presentations, not of the geometry.

### B.4 Curved ambient boundary (named wall)

By the Gauss equation the extrinsic term channelizes (`S ∧ S` is bilinear in the split),
the ambient tangential curvature does not — it is not a bilinear function of role data.
The account in a curved ambient is `(ambient input) + (channelized extrinsic account)`;
nothing more is claimable without a role frame for the ambient geometry itself
(kept outside the first paper; plan §4).
