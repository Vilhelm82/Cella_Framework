# NOTATION LEDGER — frozen conventions for the Active Rechart / Curvature Valuation campaign

**Status:** FROZEN at Stage 0 (2026-07-30). Any later change requires a new ledger version and
a regression run of every gate verifier.

## 1. Curvature invariant and normalization

- Generalized invariant: the second elementary symmetric curvature of the shape operator
  `sigma_2(S) = (1/2)((tr S)^2 - tr(S^2))`.
- Surface dimension 2: `sigma_2(S) = K_G` (Gaussian curvature).
- Euclidean hypersurface, any dimension: scalar curvature `R = 2*sigma_2(S)`.
- Scalar-curvature sign convention: the round unit two-sphere has `R = +2`
  (inherited from LOCAL_CURVATURE_CALCULUS_COMPLETE_v1.0, kept unchanged).

## 2. Channel order (canonical, this campaign)

- Canonical channel account: `(sigma_2; kappa_c, kappa_int, kappa_s)` — coupling, interaction, self.
- LEGACY order used by Paper I / Theorem 8.1 correction / role_channel_anisotropy:
  `(K_G, kappa_c, kappa_s, kappa_int)`.
- One-line conversion: `(K, c, s, i)_legacy  ->  (sigma_2=K; c, i, s)_canonical`
  (swap the last two entries, rename K_G to sigma_2).

## 3. Jet notation (three-role case)

- Graph chart `P = f(D,S)`: `(a,b,A,B,C) = (f_D, f_S, f_DD, f_DS, f_SS)`, `q_0 = 1 + a^2 + b^2`.
- Active transposition `t = (D P)`: `t(a,b,A,B,C) = (1/a, -b/a, -A/a^3, (Ab-aB)/a^3, (-Ab^2+2abB-a^2C)/a^3)`.
- Input swap `s = (D S)`: `s(a,b,A,B,C) = (b,a,C,B,A)`.
- Coupling numerators: `Lambda_P = B`, `Lambda_D = (Ab-aB)/a`, `Lambda_S = (Ca-bB)/b`.
- Transverse quadratic: `R_trans = a^2*C - 2abB + b^2*A = (b,-a) Hess (b,-a)^T`.

## 4. Implicit (use-case-agnostic) notation

- Constraint hypersurface `Sigma = {F(x_0,...,x_n) = 0}`; regular role locus
  `Omega_role = {F = 0, prod_i F_i != 0}` with `F_i = dF/dx_i`.
- `g = grad F`, `H = Hess F`, `q = g^T g`. Frame split `H = H_c + H_s`,
  `H_s = diag(H)`, `H_c = H - H_s` (in the distinguished role frame).
- Channel-density polynomial (bordered minors, Paper I §5.2):
  `C_hat_r(t,u) = (-1)^{r+1} sum_{|I|=r+1} det[[0, g_I^T],[g_I, (t H_c + u H_s)_I]]`,
  normalized channels `kappa_{r;p,q} = kappa_hat_{r;p,q} / q^{(r+2)/2}`, invariant
  `sigma_r = sum_{p+q=r} kappa_{r;p,q}`.
- Implicit first partials of the i-output chart: `d x_i / d x_k = -F_k / F_i` on `F_i != 0`.

## 5. The inverse-channel metric assignment (the Stage 3 test object)

- Presentation `rho`: role `x_rho` is the graph value; state coordinates `{x_j : j != rho}`.
- Mixed coupling numerator of the i-output chart against pair `{rho, m}`:
  `Lambda_{i,{rho,m}} = d^2 x_i / (d x_rho d x_m)` (chart mixed partial).
- Chart norm: `q_i = 1 + |grad f_i|^2`.
- Metric assignment (KN-selected u=0 rule, generalized):
  `g_rho = sum_{i != rho} G_i^{(rho)} (dx_i)^2`,
  `G_i^{(rho)} = q_i^2 * sum_{m != i, rho} Lambda_{i,{rho,m}}^{-2}`.
- n=2 reduction: single pair, `G_i^{(rho)} = q_i^2 / Lambda_i^2 = -1/kappa_c^{(i)}`.
- Rechart defect: `D_(rho,sigma) = g_rho - phi_(rho,sigma)^*(g_sigma)`, with
  `phi_(rho,sigma)` the identity map of `Sigma` expressed between the two state charts.

## 6. Divisor and valuation notation

- Divisor order `ord_{D_a}(f) = lambda` when `f = z_a^lambda u`, `u|_{D_a} != 0`;
  signed blow-up order `kappa_{D_a}(f) = -ord_{D_a}(f)`.
- Metric valuation matrix `P = (p_{ia})`; base vertices `V_a = -P_a - 2 e_a` (normal),
  `V_mu = -P_mu` (tangential).
- Master quadric (one face, normal exponent p_0, transverse p_1..p_m):
  `C(p) = -(1/2)[ sum p_alpha^2 + sum_{alpha<beta} p_alpha p_beta - (p_0+2) sum p_alpha ]`.
- Off-diagonal germ class (Stage 5): `g = E^T diag(z^{p_i} h_i) E`, `E` smooth invertible up to
  the divisor, `h_i` smooth nonvanishing.
- Principal coefficient weight law: for `z' = u(y) z + O(z^2)`, `u|_D != 0`, and
  `R[g] = c(y) z^{-k} + O(z^{-k+1})`: `c'(y) = u(y)^k c(y)` — the principal coefficient is a
  section of the k-th power of the conormal-line dual (normal-line-valued datum), not a scalar.

## 7. Words that are never conflated

- **active rechart** = re-solving the relation with a different output role (changes the jet).
- **passive relabelling** = permuting coordinate labels (never changes any spectrum).
- **channel account** = a lift of the invariant through the affine fibre `Sigma_channel^{-1}(sigma_2)`;
  it is framed data, NOT an additional scalar invariant.
- **finite-tower naturality** (CCE-8) = truncation-compatibility of the active action at every
  finite order. It is NOT an analytic convergence statement and must never be cited as one.
