# Lead C Theorem Brief — Role-Singularity Valuation Law

**Purpose:** Give Claude enough structure to turn Lead C into a proper theorem/campaign, without smuggling in paper-status claims as proof.

**Working title:** *Role-Singularity Valuation Law: from active-role chart failure to curvature pole order*

**Status:** theorem-shaped conjectural brief. This is **not yet a Cella-grade theorem**. It is a proof plan plus exact verification programme.

**Primary target:** strengthen LEAD-2 (“Role singularities”) from a refusal vocabulary into a stratum-reading theorem.

---

## 0. Executive instruction for Claude

Do **not** treat this as “dimension of a lost Specht module predicts a pole order.” That version is too crude.

The better target is:

> **Carrier-stratum labels identify which role-channel component collapses or becomes unreadable; valuation geometry determines the curvature pole exponent.**

Representation theory tells us *where the carrier lost information / which stratum was crossed*. The local Laurent valuation of the role derivative, transported coupling channel, metric determinant, and Brioschi numerator tells us *how hard the geometry blows up*.

---

## 1. Source anchors and trust currency

Use these as source anchors, not as proof substitutes.

1. **LEADS.md / LEAD-2** says role singularities are open: current engine can refuse at degeneracies, but cannot yet read them; the requested discriminating test is one-parameter exact-ℚ stratum crossings with channel accounts and blow-up rates.  
   Source: `LEADS.md`, 2026-07-06. fileciteturn22file0

2. **ADMISSIONS.md** says prior labels such as “PROVEN,” “CERTIFIED,” and “RATIFIED” are not evidence; load-bearing results must be re-proven inside the current repo by fresh code, fresh symbolic derivation, byte-stability ×2, or a named certificate.  
   Source: `ADMISSIONS.md`, 2026-07-06. fileciteturn22file9

3. **GTD/DBP paper** establishes the paper-level seed: the `n=2` DBP metric exists as `g_DBP = -h^{-1}`, with  
   `h = Σ κ_{c,i} dE_i ⊗ dE_i`; role boundaries occur where output charts become unsolvable and `Λ_D ∝ 1/a`, `Λ_S ∝ 1/b`; on Kerr, extremal has pole order 3, Schwarzschild has pole order 4, and Davies is finite for DBP.  
   Source: `gtd vs dbp.pdf`, 2026-06-28 paper uploaded 2026-07-06. fileciteturn22file6 fileciteturn22file11

4. **GTD/DBP paper** records the broader paper-level pattern: GTD-II curvature has order-2 poles on transition loci; DBP curvature has order-3 poles on generic role boundaries and order-4 poles at reflection-fixed role boundaries; Kerr/RN/vdW singular sets are disjoint/complementary.  
   Source: `gtd vs dbp.pdf`. fileciteturn22file13 fileciteturn22file18

5. **Review / Coverage document** says role-singularity theory remains open even though stratum-typed refusal tokens exist (`ROLE_CHART_UNAVAILABLE`, `CHANNEL_ISOTROPIC`).  
   Source: `REVIEW_Exact_Role_Channel_Geometry.md`, 2026-07-06. fileciteturn22file8

6. **A-008 admission record** says the active `n=3` role layer has been mathematically recertified for role charts, named channels, `A_c`, faithful fingerprint, and the two named degeneration strata, but engine wiring remains gated at G1.0/G1.2.  
   Source: `ADMISSIONS.md`, 2026-07-06. fileciteturn22file19

7. **RC-1 convention hazard:** never quote channel tuples without slot labels. Current case law: internal tuple order can differ from labelled `(κ_c, κ_s, κ_int)`. The stdout originally printed `(-1/49,-3/49,+1/49)` without slot labels, creating a false contradiction.  
   Source: `RC1_transport_law_stdout.txt`. fileciteturn22file2

---

## 2. The theorem target

### 2.1 Informal statement

When an active output-role chart fails — e.g. `a = f_D = 0` or `b = f_S = 0` — the failure is not merely division by zero. It is a role-singular stratum. Transported coupling channels diverge in a controlled way, the channel-inverse metric degenerates or develops component poles, and the curvature pole order is determined by the valuations of these objects.

### 2.2 Proposed theorem name

```text
Role-Singularity Valuation Law
```

### 2.3 Candidate theorem statement, v0

Let `γ(t)` be a one-parameter exact-ℚ or exact-symbolic family crossing a role stratum at `t = 0`.

Let `y(t)` be the unsolvable output derivative for that role, e.g.

```text
y(t) = a(t) = f_D(γ(t))     or     y(t) = b(t) = f_S(γ(t)).
```

Assume

```text
v_t(y) = m > 0
```

where `v_t` is the Laurent valuation at `t = 0`.

Let `Λ_i(t)` be the transported coupling channel native to the failing output role, with

```text
Λ_i(t) ~ t^{-m} · unit(t)
κ_{c,i}(t) = -Λ_i(t)^2 / q_0(t)^2
```

and let

```text
h = Σ_i κ_{c,i} dE_i ⊗ dE_i,
g_DBP = -h^{-1}.
```

Then the pole order of the scalar curvature of `g_DBP` is determined by a finite valuation ledger:

```text
PoleOrder(R[g_DBP])
=
Function(
  v_t(y),
  v_t(Λ_i),
  v_t(κ_{c,i}),
  v_t(g_DBP components),
  v_t(det g_DBP),
  v_t(Brioschi numerator),
  symmetry/fixed-locus correction
).
```

For simple `n=2` role boundaries observed so far:

```text
generic simple role boundary:          pole order 3
reflection-fixed simple role boundary: pole order 4
transition locus (Davies/spinodal):    GTD order 2, DBP finite
```

### 2.4 Stronger conjectural form

For simple role boundaries (`m = 1`):

```text
generic role boundary:
    PoleOrder(R[g_DBP]) = 3

reflection-fixed role boundary:
    PoleOrder(R[g_DBP]) = 4
```

For higher-order role derivative zeros (`m > 1`), test the provisional formulas:

```text
generic:
    PoleOrder ≈ 2m + 1

reflection-fixed:
    PoleOrder ≈ 2m + 2
```

These higher-`m` formulas are **not proven** and should be treated as conjectural until exact families are generated.

---

## 3. Definitions to pin before proof

### 3.1 Valuation

For a Laurent series

```text
f(t) = t^k u(t),   u(0) ≠ 0,
```

define

```text
v_t(f) = k.
```

Pole order is

```text
pole(f) = max(0, -v_t(f)).
```

For vectors/tensors, record valuations componentwise.

### 3.2 Role-singular stratum

At order 2 for a local graph

```text
P = f(D,S)
```

with jet

```text
(a,b,A,B,C) = (f_D, f_S, f_DD, f_DS, f_SS),
```

the active role transpositions use denominators `a` or `b`.

Define:

```text
ROLE_CHART_UNAVAILABLE_D : a = 0
ROLE_CHART_UNAVAILABLE_S : b = 0
```

The existing vocabulary token is `ROLE_CHART_UNAVAILABLE`.

### 3.3 Channel-isotropic stratum

Existing token: `CHANNEL_ISOTROPIC`.

Use it for loci such as

```text
Λ_ρ = 0
```

where the fingerprint rank drops or the role-channel orbit loses faithfulness in the certified sense.

### 3.4 Output-role channels in the `n=2` seed

From the GTD/DBP paper:

```text
Λ_P = B
Λ_D = (A b - a B) / a
Λ_S = (C a - b B) / b
κ_{c,i} = -Λ_i^2 / q_0^2
q_0 = 1 + a^2 + b^2
```

At `a = 0`, the `D`-output channel may diverge. At `b = 0`, the `S`-output channel may diverge.

### 3.5 DBP channel-inverse metric, `n=2`

Paper-level definition:

```text
h = Σ_i κ_{c,i} dE_i ⊗ dE_i
g_DBP = -h^{-1}
```

This must be re-certified before being used as load-bearing proof currency.

---

## 4. Seed evidence table

| Surface | Role boundary / transition | Known/paper-level behavior | Proposed stratum type |
|---|---|---:|---|
| Kerr | Extremal `T=M_S=0`, `S=2πJ` | `R[g_DBP] ~ (S-2πJ)^(-3)` | generic simple role boundary |
| Kerr | Schwarzschild `Ω=M_J=0`, `J=0` | `R[g_DBP] ~ J^(-4)` | reflection-fixed role boundary |
| RN | Extremal | order 3 | generic simple role boundary |
| RN | `Q=0` | order 4 | reflection-fixed role boundary |
| vdW | `P=0` boundary | order 3 | generic simple role boundary |
| Kerr/RN | Davies | GTD order 2, DBP finite | transition, not role-boundary |
| vdW | spinodal | GTD order 2, DBP finite | transition, not role-boundary |

Source: GTD/DBP paper’s complementarity and order-law table. fileciteturn22file13

---

## 5. What the theorem should *not* say

Do **not** say:

```text
pole order = dimension of lost Specht module
```

That is too simple and likely false.

Reasons:

1. The known `3 → 4` shift is caused by reflection-fixed symmetry, not by a mere change in carrier dimension.
2. The paper says the Schwarzschild pole coefficient is governed by native-channel collapse while a transverse component pole cancels out of the leading coefficient. That is valuation geometry, not dimension counting.
3. The representation-theoretic carrier identifies the collapsing/isotropic component; it does not by itself compute the Brioschi numerator valuation.

Better:

```text
Pole exponent = valuation ledger + symmetry correction.
Representation theory labels which component enters the ledger.
```

---

## 6. Local derivation scaffold

### 6.1 Generic diagonal-metric model

For a diagonal surface metric

```text
ds² = E(t,y) dt² + G(t,y) dy²
```

Gaussian curvature can be written as

```text
K = -1/(2√(E G)) [
      ∂_t( (∂_t G)/√(E G) )
    + ∂_y( (∂_y E)/√(E G) )
]
```

This formula is quoted in the GTD/DBP paper for the diagonal GTD case and is useful as a local valuation model. fileciteturn22file17

Suppose a generic role boundary has

```text
E(t,y) ~ e₂(y) t^(2m)
G(t,y) ~ g₀(y) + g_ℓ(y) t^ℓ + ...
```

with `g_ℓ ≠ 0`.

Then

```text
√(E G) ~ t^m
∂_t G ~ t^(ℓ-1)
(∂_t G)/√(E G) ~ t^(ℓ-1-m)
∂_t(...) ~ t^(ℓ-2-m)
1/√(E G) ~ t^(-m)
```

so the first term predicts

```text
K ~ t^(ℓ - 2 - 2m)
PoleOrder = 2m + 2 - ℓ.
```

For the generic first-slope case `ℓ = 1`:

```text
PoleOrder = 2m + 1.
```

For simple zeros `m = 1`:

```text
PoleOrder = 3.
```

This matches the generic role-boundary seed cases.

### 6.2 Reflection-fixed model warning

Do **not** trust a one-line diagonal metric model to prove the reflection-fixed case.

The paper says the reflection-fixed edge does something more subtle:

- at Schwarzschild `J=0`, reflection symmetry forces `M_SJ → 0`;
- the native component collapses;
- a transverse metric component carries a pole;
- that transverse pole cancels out of the leading curvature coefficient;
- the order is lifted from 3 to 4.

This must be proven by the exact Brioschi/Laurent valuation ledger, not guessed from a toy model.

Expected simple-reflection result:

```text
PoleOrder = 4
```

but the proof should compute the actual valuations of:

```text
g_DBP components
det(g_DBP)
Brioschi numerator
R[g_DBP]
```

near the fixed locus.

---

## 7. Proposed proof architecture

### Theorem 1 — Role derivative zero produces channel divergence

**Claim.** If `v_t(a)=m>0` and the numerator of `Λ_D=(Ab-aB)/a` is a unit at `t=0`, then

```text
v_t(Λ_D) = -m
v_t(κ_{c,D}) = -2m
```

Similarly for `b=0` and `Λ_S`.

**Proof method.** Direct valuation on the exact role-channel formula.

**Kill condition.** A certified family with `a=0` and unit numerator but no `Λ_D` divergence.

### Theorem 2 — Channel divergence produces inverse-metric boundary degeneration

**Claim.** If `v_t(κ_{c,i})=-2m`, then the corresponding inverse-channel metric component has

```text
v_t(g_DBP,ii) = 2m
```

unless cancelled by the surface restriction / coordinate projection.

**Proof method.** Exact inversion of diagonal `h` in the `n=2` seed; later generalize cautiously.

**Kill condition.** A verified `n=2` role boundary where the native metric component does not scale as predicted.

### Theorem 3 — Generic role-boundary pole order

**Claim.** For a simple generic role boundary (`m=1`) with a nonzero transverse first slope in the non-collapsing metric component, the curvature pole order is 3.

**Proof method.** Formal Laurent computation with the diagonal curvature formula, then confirm by exact Brioschi rational form.

**General conjecture.**

```text
PoleOrder = 2m + 1
```

if the first nonzero transverse term has `ℓ=1`.

More generally:

```text
PoleOrder = 2m + 2 - ℓ
```

for `G(t)=g₀+g_ℓ t^ℓ+...`, subject to the second curvature term not dominating.

### Theorem 4 — Reflection-fixed correction

**Claim.** For a simple reflection-fixed role boundary, the generic order-3 boundary pole is promoted to order 4.

**Proof method.**

1. Define the involution `ρ`, e.g. `J ↦ -J` or `Q ↦ -Q`.
2. Prove the fixed boundary forces an additional vanishing, e.g. `M_SJ → 0`.
3. Compute exact valuations of the metric components.
4. Compute exact valuations of the Brioschi numerator and denominator.
5. Show the transverse pole cancels from the leading coefficient.
6. Prove resulting order is 4.

**Known seed.** Kerr Schwarzschild and RN `Q=0` are order 4; vdW lacks reflection symmetry and remains order 3.

### Theorem 5 — Transition/role complementarity

**Claim.** Transition loci such as Davies/spinodal are not role-boundary strata: GTD curvature sees them with order 2, while DBP curvature is finite there. Role boundaries are seen by DBP and missed by conventional GTD-II.

**Proof method.** Exact factorization of denominators and non-divisibility checks, first for Kerr, then RN/vdW.

---

## 8. Verification campaign outline

### Campaign name

```text
RC-5 / role_singularity_valuation
```

or, if RC-5 is already assigned:

```text
LEAD2_role_singularity_valuation_v0
```

### Stage 0 — source reconstruction and schema

Inputs:

- exact formulas for Kerr, RN, vdW fundamental relations;
- exact role assignment;
- exact channel formulas;
- exact `h`, `g_DBP`, curvature formula;
- channel tuple schema with labels.

Outputs:

- a written schema file;
- refusal tokens mapped to strata;
- all formulas copied only after re-derivation.

Kill conditions:

```text
K0.1 any formula depends on undocumented tuple slot order
K0.2 any paper-status formula enters without re-derivation
K0.3 any float/tolerance lies on verdict path
```

### Stage A — recertify `n=2` GTD/DBP spine

For Kerr:

- verify GTD-II denominator has Davies² factor and no extremal factor;
- verify DBP metric definition;
- verify DBP curvature is finite on Davies;
- verify DBP pole orders 3 and 4 and leading coefficients.

For RN/vdW:

- verify order law transfer;
- classify reflection vs non-reflection boundaries.

Outputs:

```text
results/role_singularity_valuation/stage_a/*.json
verification/recert_n2_gtd_dbp_spine.py
```

### Stage B — valuation ledger engine

Build a symbolic valuation extractor that outputs, per stratum:

```text
v(a), v(b)
v(Λ_P), v(Λ_D), v(Λ_S)
v(κ_c,P), v(κ_c,D), v(κ_c,S)
v(h components)
v(g_DBP components)
v(det g_DBP)
v(Brioschi numerator)
v(R[g_DBP])
```

Each record should include:

```text
surface
stratum
parameter t
role derivative
symmetry tag
pole order
leading coefficient
proof path
```

### Stage C — theorem fitting

Try to fit:

```text
generic simple boundary -> order 3
reflection-fixed simple boundary -> order 4
higher m -> 2m+1 / 2m+2 candidates
```

If the formula fails, record the exact obstruction and revise the theorem.

### Stage D — one-parameter artificial families

Generate exact toy families with controlled `v(a)=m` or `v(b)=m` for `m=1,2,3`.

Purpose:

- separate “physics surface accident” from structural valuation law;
- test higher-order conjectures without waiting for natural examples.

### Stage E — stratum atlas integration

Integrate with LEAD-2:

- `ROLE_CHART_UNAVAILABLE`
- `CHANNEL_ISOTROPIC`
- repeated curvature / `κ_i=κ_j`
- `det S=0`
- tangent contact
- cone apex

Do not claim all are governed by the same exponent formula. The goal is a typed atlas, not a forced unification.

---

## 9. Required artifacts to verify against

Claude should explicitly locate or create these.

### Required existing or re-created artifacts

1. `verification/recert_role_channels.py` / RC-4  
   Needed for active role formulas, `Λ` channels, degeneration strata, exact-ℚ closure.

2. `verification/recert_transport_law.py` / RC-1  
   Needed for keystone and channel-label convention guard. Output must label tuple slots.

3. `gtd vs dbp.pdf` source formulas  
   Use as reference only. Re-derive before load-bearing use.

4. Exact CAS / symbolic scripts for:
   - Kerr `g_DBP`;
   - Kerr `R[g_DBP]`;
   - Kerr Laurent coefficients `C_ext`, `C_sch`;
   - RN transfer;
   - vdW transfer.

5. A new admission record:
   ```text
   A-0XX — Role-singularity valuation law
   ```
   with obligations and displacement criteria.

### If missing, create

```text
verification/recert_n2_gtd_dbp_spine.py
verification/role_singularity_valuation.py
results/role_singularity_valuation/
docs/ROLE_SINGULARITY_VALUATION_THEOREM.md
```

---

## 10. Kill conditions

Use these to keep the campaign honest.

```text
K-C1:
A re-derived Kerr DBP curvature does not have order 3 at extremal or order 4 at Schwarzschild.

K-C2:
A re-derived RN or vdW surface contradicts the claimed 3/4 order transfer.

K-C3:
A generic simple role boundary with v(a)=1 or v(b)=1 yields a pole order other than 3.

K-C4:
A reflection-fixed simple role boundary yields no order lift, or a non-reflection boundary yields order 4 without an additional mechanism.

K-C5:
The proposed exponent formula depends only on Specht-module dimension and fails on a certified counterexample.

K-C6:
Any proof uses floats/tolerances on a verdict path.

K-C7:
Any channel tuple is emitted or compared without slot labels.

K-C8:
The theorem cannot distinguish transition loci from role-boundary loci.

K-C9:
Brioschi numerator valuation cannot be made invariant under allowed coordinate changes / chart choices.
```

---

## 11. Expected theorem deliverable

A successful theorem should look something like:

```text
Theorem (Role-Singularity Valuation Law, n=2 seed).

Let F(D,S,P)=0 be a regular 3-role constraint surface away from the role
boundary, with channel-inverse metric g_DBP=-h^{-1}. Let γ(t) cross a simple
role boundary at t=0 where one output derivative vanishes to order 1.

If the boundary is not fixed by a role-reflection symmetry and the transverse
channel has nonzero first variation, then R[g_DBP] has pole order 3.

If the boundary is fixed by an involutive role-reflection symmetry forcing the
cross-coupling derivative to vanish, and the native channel collapse is simple,
then R[g_DBP] has pole order 4.

In both cases, the leading coefficient is determined by the valuation ledger of
the native role channel and the first non-cancelling Brioschi numerator term.
Transition loci such as Davies/spinodal are not role-boundary strata and are
not detected by this pole law.
```

Then add:

```text
Corollary:
For Kerr, RN, and vdW, the GTD-II and DBP curvature singular sets are
complementary: GTD-II has order-2 poles on transition loci; DBP has order-3
generic role-boundary poles and order-4 reflection-fixed role-boundary poles.
```

The corollary should remain surface-specific until more families are added.

---

## 12. Notes for the eventual `n=3` lift

The GTD/DBP paper leaves the `n=3` lift open because each output chart carries multiple off-diagonal couplings. The `h` form must be generalized before complementarity can transfer.

Lead C can support the `n=3` lift by providing:

1. a valuation-ledger method independent of the exact `h_3` choice;
2. a test for candidate `h_3` metrics:
   ```text
   Does the candidate reproduce the n=2 pole valuation law under charge suppression?
   Does it distinguish generic role boundaries from reflection-fixed boundaries?
   Does it stay finite on n=3 Davies while diverging on extremality?
   ```
3. obstruction language if no candidate survives.

Do not make Lead C depend on solving `h_3`. Let Lead C be the valuation grammar that `h_3` must obey.

---

## 13. Correction / convention guard

Use this exact rule in any theorem draft:

> **Never quote a channel tuple without slot labels.**

The certified keystone labels are:

```text
(κ_c, κ_s, κ_int) = (-1/49, +1/49, -3/49)
K_G = -3/49
κ_c + κ_s = 0
κ_int survives
```

But some internal functions may use slot order:

```text
(κ_c, κ_int, κ_s)
```

Therefore every output must say one of:

```text
channels_c_s_int = (...)
channels_c_int_s = (...)
(kc,ks,kint) = (...)
(kc,kint,ks) = (...)
```

Unlabelled `channels = (...)` is banned.

---

## 14. Suggested Claude prompt

```text
Please turn the attached Lead C theorem brief into a campaign-ready theorem plan.

Tasks:
1. Separate what is already certified in current Cella currency from what is paper-level reference.
2. Draft the formal theorem statement for the n=2 seed.
3. Identify the minimal exact symbolic derivations needed for RC-5.
4. Build the valuation ledger schema:
   v(a), v(b), v(Λ_i), v(κ_i), v(h), v(g_DBP), v(det g_DBP), v(Brioschi numerator), v(R).
5. Prove or refute:
   generic simple role boundary -> pole order 3;
   reflection-fixed simple role boundary -> pole order 4.
6. Treat the “dimension of lost Specht module predicts pole order” as a candidate to kill, not as the theorem.
7. Produce a staged prereg with kill conditions K-C1..K-C9.
8. Do not use unlabelled channel tuples.
```

---

## 15. Bottom line

Lead C is worth pursuing because it can turn:

```text
role chart failure
```

from an engineering refusal into:

```text
a typed, valuation-governed geometric stratum with predictable curvature severity.
```

That is exactly the kind of theorem LEAD-2 is missing.

The highest-value first proof is not “all singularities.” It is:

```text
generic simple role boundary = order 3
reflection-fixed simple role boundary = order 4
transition locus = not a role-boundary pole
```

Prove that cleanly for the `n=2` seed, with exact re-verification, and the rest of the atlas has somewhere solid to stand.
