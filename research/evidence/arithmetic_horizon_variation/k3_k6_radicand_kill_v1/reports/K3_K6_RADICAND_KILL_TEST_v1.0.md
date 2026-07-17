# The k=3/k=6 radicand kill test

**Version:** 1.0  
**Date:** 2026-07-18  
**Verdict:** **SURVIVES at both k=3 and k=6**

## 1. Falsifier and canonicity criterion

The question was not whether some unrelated square class could be found. That would be cheap and mathematically uninformative. The admissible candidate had to be forced by the same two axial product branches as the four-charge entropy sum.

Put

```text
A_k^+ = product_i (w_i+m),    A_k^- = product_i (w_i-m),
w_i^2 = u+N_i^2,              m^2=u,              P=product_i N_i.
```

Then `A_k^+ A_k^-=P^2`. The canonical plus-radicand is

```text
gamma_k = A_k^+ + A_k^- + 2P
        = (sqrt(A_k^+) + sqrt(A_k^-))^2.
```

It is coefficient-free, fixed by `m -> -m`, constructed functorially from the norm pair, and at `k=4` is exactly the published `gamma_R9`. The opposite cross-term

```text
gamma_k^- = A_k^+ + A_k^- - 2P
```

is not a new channel: `[gamma_k^-]=[u][gamma_k]` in the square-class group.

## 2. Identity that emerged

Writing elementary symmetric functions of the `w_i` as `e_j(w)`, define

```text
alpha_k = sum_(j congruent k mod 2)     u^((k-j)/2)   e_j(w),
beta_k  = sum_(j not congruent k mod 2) u^((k-j-1)/2)e_j(w).
```

Exact symbolic expansion gives

```text
A_k^+ = alpha_k + m beta_k,
A_k^- = alpha_k - m beta_k,
alpha_k^2-u beta_k^2=P^2,
gamma_k(gamma_k-4P)=4u beta_k^2.
```

This is the four-charge R9 identity without the restriction `k=4`. The present artifact verifies the product identities directly at `k=3` and `k=6` and records the general combinatorial formula they instantiate.

## 3. Odd probe: k=3

Here `delta_3=4` and

```text
alpha_3 = e3(w)+u*e1(w),
beta_3  = e2(w)+u,
gamma_3 = 2*(e3(w)+u*e1(w)+P).
```

The exact contact instance uses `N=(1,2,4)`, `P=8`.

- Even wall `(+,+,+)`: `4M=7`, reciprocal sum `7/4`, `beta(0)=14`, parity `(v(u),v(gamma_3))=(1,0)`.
- Odd wall `(-,+,+)`: `4M=5`, reciprocal sum `-1/4`, `beta(0)=2`, parity `(1,1)`.

For both walls the exact degree-4 mass norm has constant coefficient zero and nonzero linear coefficient, so `u=0` is a simple root. The signed sum is unique, excluding a coincident contact sheet. Thus the sheet matrix is

```text
B = [[1,0],[1,1]],  rank_F2(B)=2.
```

With the certified base group `S_4`, orbit saturation gives rank `2*4=8` and generic normal closure `C2^2 wr S4` of order `6144`.

## 4. Even probe: k=6

Here `delta_6=22` and

```text
alpha_6 = e6(w)+u*e4(w)+u^2*e2(w)+u^3,
beta_6  = e5(w)+u*e3(w)+u^2*e1(w),
gamma_6 = 2*(e6(w)+u*e4(w)+u^2*e2(w)+u^3+P).
```

The exact contact instance uses `N=(1,2,4,8,16,32)`, `P=32768`.

- Even wall `(+,+,+,+,+,+)`: `4M=63`, reciprocal sum `63/32`, `beta(0)=64512`, parity `(1,0)`.
- Odd wall `(-,+,+,+,+,+)`: `4M=61`, reciprocal sum `-1/32`, `beta(0)=1024`, parity `(1,1)`.

For both walls the exact degree-22 mass norm again has a simple root at `u=0` and a unique signed wall. The same invertible `B` therefore orbit-saturates under `S_22` to rank `44`. The generic normal closure is `C2^2 wr S22`, of order `19773629917122657266558702714880000`.

## 5. Why no hidden off-contact parity spoils the matrix

Reflection descent puts every `w_i`, hence `alpha_k`, `beta_k`, and `gamma_k`, in the mass field `K=F(u)`. At a divisor where `u` is a unit, the identity

```text
gamma_k(gamma_k-4P)=4u beta_k^2
```

forces every positive valuation of `gamma_k` to be even, because `P` is a unit and `gamma_k` and `gamma_k-4P` cannot both vanish. Odd gamma parity is therefore confined to the odd signed contacts. The chosen binary-charge walls are distinct, so the other mass sheets have `u`-valuation zero there. These are precisely the off-sheet and regularity conditions required by the conjugate Kummer-module theorem.

## 6. Evaluation

The kill test fails to kill the radicand. More strongly, the same canonical construction survives one odd and one even charge count and reaches the maximal two-channel Kummer rank in each:

```text
k=3: rank 8,  closure C2^2 wr S4;
k=6: rank 44, closure C2^2 wr S22.
```

So `gamma` is not behaving as a four-charge parity accident. The calculation also exposes the all-k identity above. This report does **not** silently promote two probes into an arbitrary-k theorem; that promotion should be a short separate proof which quantifies the generic signed-contact hypotheses and then invokes the already proved all-k base-monodromy and Kummer-wreath theorems.

## 7. Replay

Run:

```text
python3 research/evidence/arithmetic_horizon_variation/k3_k6_radicand_kill_v1/build_k3_k6_radicand_kill.py
python3 research/evidence/arithmetic_horizon_variation/k3_k6_radicand_kill_v1/verify_k3_k6_radicand_kill.py
python3 engine/tests/gate_k3_k6_radicand_kill.py
```
