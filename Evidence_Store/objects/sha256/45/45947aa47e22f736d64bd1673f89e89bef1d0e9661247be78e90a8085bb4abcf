# G1.0 PREREG — frozen before implementation

All pins below were hand-derived from the RC-2 formula and independently verified by
a one-off direct evaluation (session log 2026-07-06) BEFORE any implementation code
existed. The gate battery retrodicts them through the API. Pins are immutable; a
failed pin is a finding (triage: implementation bug vs kill condition), never an
edit target mid-run. ("In-ink" correction of a demonstrated prereg arithmetic error
follows the G0.3 precedent: correct, re-freeze, record — never silently.)

## Conventions

- O components in lexicographic pair order: n=3 → (01,02,12); n=4 → (01,02,03,12,13,23);
  n=5 → (01,02,03,04,12,13,14,23,24,34).
- Channel triples ALWAYS labeled (kc, kint, ks) or as a keyed record — never
  positional (label-convention case law, 2026-07-06).
- Gauge action at jet level: H -> H + g a^T + a g^T, g fixed.

## P1 — carrier pins (retrodicted through the API)

Keystone n=3: g = (3, 1, 2); H = [[2,1,0],[1,0,0],[0,0,2]]
```
O = (2/3, -13/6, -1/2)
```

n=4 fixture: g = (1, 2, 3, 5)
H = [[2,1,-1,3],[1,4,2,-2],[-1,2,6,1],[3,-2,1,-4]]
```
O = (-2, -5, -8/5, -3, -31/5, -14/5)
```

n=5 fixture: g = (2, 1, 3, 7, 5)
H = [[4,1,-2,3,-1],[1,2,5,-3,2],[-2,5,-6,1,-4],[3,-3,1,10,6],[-1,2,-4,6,8]]
```
O = (-2, -3, -38/7, -38/5, 3, -75/7, -19/5, 41/7, -7/5, -111/35)
```

Sample hand derivation (n=5, last component, shown so the pin's independence is
auditable):
```
O_34 = H_34 - g_3*H_44/(2*g_4) - g_4*H_33/(2*g_3)
     = 6 - 7*8/10 - 5*10/14 = 6 - 28/5 - 25/7 = (210 - 196 - 125)/35 = -111/35
```

## P2 — gauge-invariance sweep (through the API)

For every fixture above and every gauge row a in:
```
n=3: (1,0,0), (0,1,0), (1,-2,3), (-1/2,5,1), (2,3,-1)
n=4: (1,0,0,0), (0,-1,2,0), (1/3,-2,5,7), (2,2,-3,-1/2)
n=5: (1,0,0,0,0), (0,2,-1,3,0), (-1/2,1,7,-2,1/3)
```
carrier(gauged jet) == carrier(jet), componentwise exact. ANY failure at n=4,5 fires
K-1; at n=3 it is an implementation bug (RC-1 certifies n=3 invariance).

## P3 — normal form canonicality

For every fixture and every gauge row: H_perp(gauged) == H_perp(base); H_perp has
zero diagonal and off-diagonal equal to O; and the decomposition witness holds:
```
D := H - H_perp ;  a_i := D_ii / (2*g_i)  ==>  D_ij == g_i*a_j + a_i*g_j  for all i,j
```
Failure fires K-3.

## P4 — the n=3 channel cross-check (labeled)

Keystone through the cross-check function:
```
kc = -1/49 ; kint = -3/49 ; ks = +1/49 ; K_G = -3/49
```
(RC-1 `4ad5a6eb`, RC-4 `3d7ed1bf` values.) Disagreement between the carrier-path jet
and this cross-check fires K-2. The function is n=3-ONLY: calling it at n != 3 is an
API-contract ValueError (freeze rule 3 — the channel route is not the pathway).

## P5 — refusal rows (data conditions refuse; misuse raises)

```
R1  block of length 2 (valid jets)            -> CODIM_UNSUPPORTED refusal cell
R2  g = (0,0,0), n=3                          -> SINGULAR_GRADIENT refusal cell
R3  g = (3,1,0), n=3                          -> ROLE_CHART_UNAVAILABLE, stratum
                                                 names component index {2}
R4  g = (0,2,0,1), n=4                        -> ROLE_CHART_UNAVAILABLE, stratum
                                                 names {0, 2}
R5  refusal cells flow into certificates; plain register renders the reason,
    no raw token, no exception
R6  float anywhere in g/H/point               -> TypeError (not a refusal)
```
Precedence pin: R-precedence is CODIM_UNSUPPORTED (block shape) before gradient
strata; all-zero gradient is SINGULAR_GRADIENT (no direction), not
ROLE_CHART_UNAVAILABLE.

## P6 — purity wiring (the two-species account meets the carrier)

```
U1  R-motion: absorbing an R-epoch (base g, parameter a) leaves carrier O of the
    gauged H equal to O of H  (purity, T-A; operationally P2)
U2  M-defect: H' = H + E with E a nonzero symmetric M-residue moves O in general;
    witness pinned: keystone with E = E_01 = E_10 = 1 (else 0) gives
    O' = (5/3, -13/6, -1/2)  (only the 01 component moves, by +1)
U3  M-correction: reconstructing truth H from (H', residue E) and extracting O
    recovers the base pin exactly
```

## P7 — certificates

```
C1  value path: certificate emits with tier language in `what`
    ("tier: local; codim-1; order 2; jets over Q") and 16-hex rerun digest
C2  refusal path (R1): schema-conformant certificate, plain names the reason
C3  double-run law: a nondeterministic carrier compute cannot emit
```

## P8 — mutants (each MUST FAIL its target row; a passing mutant fails the gate)

```
M1  GOLDMAN-FLATTEN: replace every O component by the mean of the components
    (preserves a scalar aggregate, destroys channel content).
    Must FAIL P1 pins and P4 cross-check. Guards: totals never certify alone.
M2  DROPPED-TERM: O_ij = H_ij - g_i*H_jj/(2*g_j)  (third term omitted).
    Must FAIL the P2 gauge sweep (the dropped term is what kills the gauge).
M3  LABEL-SWAP: cross-check returns kint and ks exchanged.
    Must FAIL P4 (the label-convention case law, permanently armed in the battery).
```

## P9 — declared side effect (before the battery, not after)

Admitting A-009's two tokens grows the closed vocabulary 5 → 7. `tests/gate_04.py`
pins the count at 5 (its tripwire for exactly this event). DECLARED NOW: gate_04's
count updates to 7 in the same commit as the vocabulary change; gate_04 re-pins;
old pin `3775a7fb` superseded; all other gate_04 rows unchanged. Full Layer-0 suite
re-runs ×2 at close and all five gates must remain green.

## Verdict rule

Gate closes only if: every P1-P7 row passes, every P8 mutant fails its target,
P9's suite is green ×2, and gate_10 stdout is byte-stable ×2. Any kill fires:
HALT, bank, no close.
