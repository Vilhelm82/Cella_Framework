# LEAD-7 Candidate Metric Direction

## Output-Channel Norm Inverse Metric as the Stronger Candidate

This note converts the prior review response into a Markdown handoff for Claude Code. It is focused on the mathematical direction after the initial Kerr `n = 2` pole-order checks for candidate DBP metrics.

## Executive Verdict

The initial results are not what we wanted, but they are structurally informative.

```text
Do not try to repair Candidate B as a raw pullback metric.

The pullback construction differentiates singular channel values.
That increases boundary pole order and destroys the paper's 3/4 law.

The stronger direction is to keep the paper's inverse-channel valuation mechanism,
but replace the ambiguous n=3 channel assignment by a canonical S3-equivariant
aggregation of the multiple couplings in each output chart.
```

The successful `n = 2` paper metric is not an information metric. It is an inverse channel-value metric.

```text
h = Σ_i κ_c,i dE_i ⊗ dE_i
```

```text
g_DBP = -h^(-1)
```

The observed complementarity law is specifically a curvature statement: the DBP curvature is finite on Davies and diverges on the physical boundaries, with pole order `3` generically and pole order `4` at reflection-fixed boundaries.

## Why Candidate B Failed

Candidate B was the carrier-pullback metric.

```text
g_B = (dO)^T (dO)
```

Near a role boundary, the relevant channel or carrier component typically behaves like:

```text
O_or_κ ~ t^(-2)
```

Then:

```text
dO_or_dκ ~ t^(-3)
```

So the pullback metric behaves like:

```text
g_B ~ t^(-6)
```

That is the wrong valuation class.

The paper metric instead uses inverse channel values, so the collapsing component behaves like:

```text
g_A ~ t^2
```

That difference is precisely why Candidate B gives an extremal pole order near `8` and misses the Schwarzschild pole. The pullback metric measures sensitivity of the feature map; the DBP metric measures inverse channel accessibility.

This should be banked as a lesson:

```text
Carrier faithfulness is not enough to define the DBP metric.

The metric must preserve the inverse-channel valuation law.
```

## The Stronger Candidate: Output-Channel Norm Inverse

The right direction is not to fix Candidate B. It is to generalize Candidate A directly.

For `n = 3` Kerr-Newman, each charge-output chart has three off-diagonal couplings. The canonical move is to aggregate those couplings inside each output chart by an invariant quadratic norm, then invert that scalar just as the `n = 2` metric does.

Call this Candidate D.

```text
Candidate D:
output-channel norm inverse metric
```

Let the thermodynamic graph be:

```text
M = Φ(E1, E2, E3)
```

For Kerr-Newman:

```text
(E1, E2, E3) = (S, J, Q)
```

For each charge output:

```text
Ei = f_i(M, E_j, E_k)
```

where:

```text
{i, j, k} = {1, 2, 3}
```

In that output chart, there are three input-pair couplings:

```text
Λ_i,{M,j}
Λ_i,{M,k}
Λ_i,{j,k}
```

Define the output-channel strength:

```text
C_i(t) =
[
    Λ_i,{M,j}^2
    + Λ_i,{M,k}^2
    + t * Λ_i,{j,k}^2
]
/
q_i^2
```

Here:

```text
q_i = 1 + |∇f_i|^2
```

and:

```text
t
```

is a dimensionless weight for the charge-charge input pair relative to the two mass-charge input pairs.

Then define:

```text
h_D(t) = - Σ_i C_i(t) dE_i ⊗ dE_i
```

```text
g_D(t) = -h_D(t)^(-1)
```

Equivalently, in diagonal coordinate form:

```text
g_D(t)_{ii} = 1 / C_i(t)
```

with no off-diagonal components at first pass.

This is the first candidate to push hard.

## Why Candidate D Is Better Than B

Candidate D reduces exactly to the paper's mechanism at `n = 2`.

At `n = 2`, each output chart has only one off-diagonal input pair, so:

```text
C_i = Λ_i^2 / q_i^2
```

and therefore:

```text
g_i = 1 / C_i
```

which is exactly:

```text
g_i = -1 / κ_c,i
```

So this candidate preserves the `n = 2` inverse-channel metric, not merely the complementarity pattern.

It also solves the `n = 3` coupling-arrangement problem with only one meaningful parameter:

```text
t
```

because Kerr-Newman has a distinguished graph value:

```text
M
```

and three charge roles:

```text
S, J, Q
```

For each output charge, the input-pair types split into:

```text
mass-charge pairs:
{M,j}, {M,k}
```

```text
charge-charge pair:
{j,k}
```

`S3` symmetry among the charges allows one weight for the two mass-charge pairs and one weight for the charge-charge pair. Overall scale does not matter for curvature pole sets, so the family has one real parameter.

That is the finite ambiguity we wanted: not an ad hoc zoo, but a one-parameter canonical family.

## Fully Symmetric Special Case

The simplest member is:

```text
t = 1
```

Then:

```text
C_i =
[
    Λ_i,{M,j}^2
    + Λ_i,{M,k}^2
    + Λ_i,{j,k}^2
]
/
q_i^2
```

This is the squared Frobenius norm of the off-diagonal coupling block in the output chart.

Call it:

```text
Candidate D_Frob
```

This is the first one to test.

## Why the One-Parameter Version Matters

Mass is not a charge at `n = 3`. The charge roles are symmetric under `S3`, but the graph value `M` is not in the same role class. So the most honest `S3`-equivariant quadratic aggregation is not necessarily equal-weight Frobenius.

The more honest family is:

```text
C_i(t) =
[
    mass-charge coupling energy
    + t * charge-charge coupling energy
]
/
q_i^2
```

The campaign should ask:

```text
Does the six-constraint screen select a unique value of t?
```

If yes, this gives a canonical `n = 3` metric.

If no, the ambiguity is real and theorem-worthy.

## Valuation Check

Candidate D preserves the key boundary valuation.

At a role boundary:

```text
F_i -> 0
```

the output chart becomes unsolvable. The transported couplings involving output `i` scale like:

```text
Λ_i,* ~ 1 / F_i
```

so:

```text
C_i(t) ~ 1 / F_i^2
```

and therefore:

```text
g_D(t)_{ii} ~ F_i^2
```

That is the same native-channel collapse mechanism as the paper metric. Candidate B destroyed this by differentiating the carrier.

The `n = 2` paper says the role boundaries are exactly the output-chart singularities:

```text
T = M_S = 0
Ω = M_J = 0
```

and the channels diverge when the output derivative vanishes.

The same mechanism is already identified at `n = 3` for Kerr-Newman: entropy-output channels diverge as:

```text
g1 = T -> 0
```

and that boundary is the extremal locus GTD-II misses. Candidate D is built to preserve that mechanism.

## Do Not Over-Use O Here

The faithful carrier `O` is still essential, but not as the metric pullback.

Use `O` for:

```text
1. certification that the channel data is complete;
2. gauge invariance;
3. detecting scalar aliasing;
4. proving that the metric factors through the channel account.
```

Do not use:

```text
(dO)^T(dO)
```

as the metric itself.

The `n = 3` result says the complete coupling content is the faithful carrier `O`, while `A_c` is only its lowest scalar piece. That does not imply the Riemannian metric should be the information metric of `O`. The pole-order result says exactly that.

Better statement:

```text
The metric should be channel-value inverse geometry built from the faithful carrier,
not derivative-pullback geometry of the carrier.
```

## Candidate E: Pair-Channel Tensor, If D Fails

If Candidate D is too diagonal or fails the `D3` test, the next stronger construction is a pair-channel tensor.

Instead of collapsing pair couplings into one scalar per output, build a metric directly from pair incidences:

```text
h_E =
- Σ_i Σ_{a<b in inputs(i)}
    w_type(a,b) *
    κ_i,{a,b} *
    θ_i,{a,b} ⊗ θ_i,{a,b}
```

Here:

```text
κ_i,{a,b} = -Λ_i,{a,b}^2 / q_i^2
```

and:

```text
θ_i,{a,b}
```

is the canonical one-form on the charge state associated with that pair channel.

A simple incidence choice is:

```text
θ_i,{M,j} = dE_i
```

for native output collapse. For charge-charge pairs, test:

```text
θ_i,{j,k} = dE_i
```

or an incidence form involving:

```text
dE_j - dE_k
```

This is more complicated and should only open if Candidate D(t) fails. D(t) is the clean finite family to test first.

## Candidate B Salvage, If Desired

If a corrected pullback-like object is still desired, use a log/inverse information version rather than the raw pullback.

Candidate B-log:

```text
H_log =
Σ_ρ d log |κ_ρ| ⊗ d log |κ_ρ|
```

Then use:

```text
g_log = H_log^(-1)
```

Near a boundary:

```text
κ_ρ ~ t^(-2)
```

so:

```text
d log |κ_ρ| ~ dt/t
```

and:

```text
H_log ~ t^(-2)
```

hence:

```text
g_log ~ t^2
```

This fixes the first valuation error of Candidate B.

However, keep this on the bench. It may be canonical as a Fisher/log-channel geometry, but it is less directly connected to the paper metric than Candidate D.

## Immediate Next Tests

Run these in order.

### Test 1

```text
Implement Candidate D(t) at n = 2.

Expected:
all t disappears or becomes irrelevant;
pole orders = 3 and 4;
Davies finite.
```

### Test 2

```text
Implement Candidate D_Frob at n = 3, t = 1.

Check:
positive definiteness on Kerr-Newman physical wedge;
finite on D3;
diverges on T=0, Ω=0, Φ_e=0;
Q -> 0 reduction to Kerr.
```

### Test 3

```text
Run Candidate D(t) symbolically/numerically for several t values.

Look for:
a unique t where
- Q -> 0 reduction works cleanly;
- D3 is finite;
- role-boundary pole orders are stable;
- no spurious interior singularities appear.
```

### Test 4

```text
If a unique t is found, try to derive it from an invariance principle.

Likely selectors:
- equal Frobenius weight, t = 1;
- charge/mass split weight, t = 2 or t = 1/2;
- Q -> 0 Kerr reduction;
- absence of spurious singularities.
```

### Test 5

```text
Only if D(t) fails, open Candidate E pair-channel tensor.
```

## Brief Patch Recommendation

Replace Candidate B as primary with Candidate D.

```text
CANDIDATE D — output-channel norm inverse metric [PRIMARY]

For each output charge Ei, compute all off-diagonal coupling channels in that
output chart. Aggregate their squared normalized coupling strengths into C_i(t).
Define:

g_D(t)_{ii} = 1 / C_i(t).

This is the direct n=3 generalization of the paper's inverse-channel metric.
It preserves the role-boundary valuation law and reduces exactly to the n=2
metric. The only ambiguity is the mass-charge vs charge-charge weight t.
```

Keep Candidate B as refuted for the paper lift.

```text
CANDIDATE B — carrier-pullback information metric [REFUTED for paper lift]

Fails n=2 pole-order retrodiction:
extremal order ~8, Schwarzschild no pole.

Useful as a separate sensitivity geometry, not as the DBP complementarity metric.
```

Keep Candidate C on the bench.

```text
CANDIDATE C — three-channel pullback [BENCH]

Complementary but wrong extremal order.
May be a distinct geometry, not the paper metric.
```

## Final Recommendation

The strongest immediate candidate is:

```text
Candidate D(t):
the S3-equivariant output-channel norm inverse metric.
```

It solves the right problem because it keeps the paper's actual mechanism:

```text
inverse channel values
```

and avoids the failed mechanism:

```text
derivatives of channel values
```

It also compresses the `n = 3` ambiguity into a one-parameter family:

```text
mass-charge weight vs charge-charge weight.
```

That is small enough to exhaust exactly and strong enough to become a theorem if the `D3` tests select a unique value.

The next campaign should therefore be:

```text
D(t) versus A:
does the output-channel norm inverse metric uniquely extend the n=2 complementarity law to Kerr-Newman?
```

## Banked Finding

```text
Candidate B failed for a structural reason:
carrier-pullback metrics differentiate singular channel values and therefore move into
the wrong curvature-pole valuation class.

The DBP complementarity metric must be inverse-channel geometry, not raw carrier
pullback geometry.
```
