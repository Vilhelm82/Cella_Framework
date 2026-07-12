# First Pathfinder-to-M2 vertical-slice fixture

**Benchmark ID:** `m2-even-contact-delta-slice-a-v1`  
**Status:** Boundary/equivalence fixture closed; release timing gate open  
**Host:** Macaulay2 1.25.11  
**Source model:** `docs/files/horizon_wreath_inertia_model.m2`

## Mathematical target

Compute the base-image ideal of the even signed contact component intersected with the rotating difference divisor on the exact charge slice

```text
N1=4, N2=8, N3=12, N4=20,
```

retaining `M` and `J`.

The required exact deliverable is

```text
<N1-4, N2-8, N3-12, N4-20, M-11, J^2>.
```

The `J^2` generator is scheme data. It must not be reduced to `J`, because the even contact/difference node has multiplicity two.

## Exact M2 input

The common incidence model is

```text
S = QQ[M,N1,N2,N3,N4,J,u,w1,w2,w3,w4,
       Degrees=>{1,1,1,1,1,2,2,1,1,1,1},
       MonomialOrder=>GRevLex];

IX = <w1^2-u-N1^2,
      w2^2-u-N2^2,
      w3^2-u-N3^2,
      w4^2-u-N4^2,
      w1+w2+w3+w4-4M>;

gamma = 2*(w1*w2*w3*w4
           +u*(w1*w2+w1*w3+w1*w4+w2*w3+w2*w4+w3*w4)
           +u^2+N1*N2*N3*N4);
delta = gamma-4*N1*N2*N3*N4-16J^2;
IZ = IX+<delta>;

Ceven = IX+<u,w1-N1,w2-N2,w3-N3,w4-N4>;
sliceA = <N1-4,N2-8,N3-12,N4-20>;
```

## Baseline route

The historical stage-5 route performs saturation and elimination:

```text
baseline = trim eliminate(
    saturate(Ceven+IZ+sliceA, ideal(M)),
    {u,w1,w2,w3,w4}
    );
```

Reference output from `docs/m2_out_2026-07-10/stage5_slice.out.txt`:

```text
matrix {{N4-20, N3-12, N2-8, N1-4, M-11, J^2}}
```

Runnable baseline: `benchmarks/pathfinder_m2/even_contact_baseline.m2`.

## Candidate route families

| Route family | Admissibility |
|---|---|
| Generic saturation plus elimination | Always available in the M2 baseline; structurally excessive for this fixture. |
| Direct contact substitution | Admissible because the even contact equations explicitly set `u=0` and `w_i=N_i`. |
| Complete-intersection degree route | Useful for codimension/degree claims but unnecessary for this projection. |
| Kummer finite-extension route | Not required; the target is a contact restriction, not global primeness of `IZ`. |

## Selected structural route

On an even signed contact, `product(epsilon_i)=+1`. Direct substitution gives

```text
delta restricted to Ceven = -16 J^2.
```

Therefore

```text
Ceven + IZ = Ceven + <J^2>.
```

On slice A, the contact wall is

```text
4M-(4+8+12+20)=0,
```

so `M=11`. The base image is read directly without saturation or elimination:

```text
<N1-4,N2-8,N3-12,N4-20,M-11,J^2>.
```

Source theorem/derivation:

- `CELLA_PATHFINDER_KERNEL_ARCHITECTURE_v1.0.md`, section 12.1;
- `CELLA_ARCHITECTURE_v1.3.md`, structure-first contact restriction;
- `docs/files/WREATH_COVER_INERTIA_BRANCH_STRATIFICATION_v1_1_2026-07-11.md`, equation (16.3).

## Returned route contract

Pathfinder returns, but does not execute:

```text
route_family: contact_restriction
ordered_steps:
  1. apply signed-contact substitutions u=0, w_i=N_i
  2. reduce delta to -16*J^2
  3. preserve multiplicity and replace the restricted generator by J^2
  4. apply exact slice assignments
  5. solve the linear contact wall for M
  6. emit the base ideal in host variable identities
required_hypotheses:
  - sign_product = +1
  - characteristic != 2
  - exact slice assignments are those declared by the wrapper
certificate_obligations:
  - contact substitutions satisfy the incidence generators
  - delta + 16*J^2 vanishes modulo Ceven
  - the unsaturated upstairs ideal equals the structural upstairs ideal
  - J^2 multiplicity is retained
completion_condition:
  - host executor returns the declared base ideal
```

## Ownership of execution and certification

| Work | Owner |
|---|---|
| Lower M2 objects and preserve variable bindings | Separate M2 wrapper |
| Recognize and select `contact_restriction` | Pathfinder core |
| Apply route steps and construct the output ideal | M2 execution adapter |
| Verify polynomial/ideal identities and multiplicity obligation | External mathematical certificate adapter; never Pathfinder |
| Compare final deliverable with baseline for the release fixture | Benchmark harness |

Runnable structural execution/check: `benchmarks/pathfinder_m2/even_contact_structural.m2`.

## Measurement protocol

Measure the complete wrapped pipeline, not isolated Pathfinder analysis:

```text
T_total = T_wrapper_lowering
        + T_pathfinder_analysis
        + T_selected_route_execution
        + T_certificate_construction_replay
        + T_wrapper_lifting.
```

Baseline and selected-route trials use:

- the same host and M2 version;
- the same exact model and slice;
- separate cold M2 processes;
- one warm-up excluded from statistics;
- at least seven measured trials per route;
- median, minimum, maximum, and peak RSS;
- byte-canonicalized generator comparison;
- explicit confirmation that `J^2`, not `J`, is returned.

No speedup is claimed until the wrapper, Pathfinder, execution, and external certificate overheads are included and the median `T_total` is below the baseline median.

## Measured campaign result

The first completed campaign used one excluded warm-up and seven measured cold M2 processes per route. Full reports are:

- `benchmarks/results/FIRST_M2_REPORT.md`
- `benchmarks/results/FIRST_M2_REPORT.json`

Measured medians:

```text
generic baseline:               3.221196313 s
wrapped Pathfinder route:       3.236630539 s
T_baseline / T_pathfinder:      0.9952313909
```

Exact generator equivalence and external certificate replay both closed. The timing gate did not: Pathfinder was not faster on the measured median, so no speedup is claimed.

The recorded M2 structural execution and certificate work are millisecond-scale while a cold M2 process/model load is approximately 3.2 seconds. This fixture therefore proves the wrapper/core/executor/certificate boundary but does not provide enough generic-search burden to discriminate route performance from cold-start variation. It must not be rerun selectively until noise produces a favorable median.
