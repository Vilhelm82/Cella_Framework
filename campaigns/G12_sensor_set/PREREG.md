# G1.2 PREREG — the sensor set — predictions + falsification gates

Lean prereg. Three sensors, each a falsifiable claim with an exact retrodiction target
and a kill that ends it. Origin values are targets to reproduce in-repo, never evidence.
Do the math; a gate firing is a finding.

## P1 — Numerator tower (RC-6)

**Claim.** A numerator-only sensor `N` (no quotient) that (i) matches the ratio sensor's
coupling sensitivity, (ii) is **exactly zero** on its self-fault blindness set (not
small), (iii) is scale-invariant without the quotient.
**Target.** ENG2 fault-semantics fixtures + `SHADOW_LAW_THEOREM` (origin
`old_program_sources/eng2_fault_semantics/`, `PREREG_ENG2 0c11ef30`).
**Gates.** K-1 two-route value disagreement → pin/formula wrong. K-2 nonzero on the
blindness set → dominance case becomes a displacement candidate.

## P2 — Shape moment (RC-7)

**Claim.** The isotypic moment set captures exactly the invariant content at its degree;
scalars are insufficient at n ≥ 5 (dimension threshold).
**Target (n=4 witness, CALC-30), by two independent routes** — the `rep_utils.py`
Specht referee and an independent projector route:

```
ΔA isotypic norms:  triv 147 / std 153 / (2,2) 24 / sgn 0     Parseval  Σ = 324
```

**Gate.** K-3 n=4 witness fails to reproduce the quintuple, OR the re-derived threshold
refutes "scalars insufficient at n ≥ 5" → shape-moment dominance wrong / mis-stated.

## P3 — Localization channels (RC-8)

**Claim.** Support theorem on the covered class:

```
for F1 on edge e* = (0,1):   {S : d/dt Δ_S ≠ 0 at t=0}  ==  {S ⊇ e*}   exactly,
every fixture n ≥ 4   (Δ_S = triangle channel from the I.3b decomposition)
```

Contribution-style attribution has no support theorem.
**Target.** `PREREG_ENG2` row PE.5 (`0c11ef30`), fixtures n ≥ 4.
**Gate.** K-4 counterexample on the covered class → localization enters detection-tier
only, or not at all.

## Standing gates (all sensors)

```
K-5: CHANNEL_ISOTROPIC mistype — computes through Λ_ρ = 0, or refuses off it.
K-6: any channel tuple emitted or compared without slot labels (kc, kint, ks).
```

## Method

Fresh code, exact ℚ/ℚ(√q), no float on a verdict path. Blindness = provable exact zero.
Each sensor factors through the carrier `O` (certified G1.0), never raw `H`. Reuse the
certified bank (RC-1 keystone triple `kc=-1/49, kint=-3/49, ks=+1/49`; RC-4
`A_c=42793/1555848`, det `8·Λ_P·Λ_D·Λ_S/q0^6`; gate_11 `σ₂↔channel sums`); import
nothing else. Name collisions → consult `30_GLOSSARY_DISAMBIGUATION.md` first.

## Stage A declaration — gate_04 vocabulary 7 → 8 (P9 precedent)

Admitting `CHANNEL_ISOTROPIC` (A-010) grows the closed refusal vocabulary 7 → 8. At
Stage B the `tests/gate_04.py` count assertion updates 7 → 8 in the same commit as the
sensor wiring; its stdout pin `3775a7fb` is expected invariant (the count lives in the
assertion, not the output); the tripwire must fire pre-edit; the full Layer-0/1 suite
re-runs green ×2 at Stage C close.
