# RC-8 — localization support theorem, re-proven (exact-ℚ tier)

**Certificate:** `verification/recert_localization.py` — byte-stable ×2, stdout sha16
`f09444462bae1c97`, exit 0. Fresh code, zero-import, exact `Fraction`.

## Statement re-proven — PE.5 retrodiction

Triangle channels (SHADOW_LAW Lemma 3): `Delta_S = T_S · nu^T (2I−J)_S nu`, with
`nu_e = W_e·h_e`, `W_e = ∏_{k∉e} g_k`, `T_S = 1/∏_{m∉S} g_m²`. A coupling fault on edge
`e*` moves only `nu_{e*}`, hence:

```
{S : d/dt Delta_S ≠ 0 at t=0}  ==  {S : e* ⊆ S}     exactly
```

- **(⊆) structural:** `Delta_S` is free of `nu_{e*}` whenever `e* ⊄ S`, so
  `d/dt Delta_S = 0`. Exact, every fixture — the support-inclusion half is a proof,
  not a measurement.
- **(⊇) fixtures:** closed form `d/dt Delta_S = 2 T_S W_{e*} (nu_{e*} − Σ_{f⊂S, f≠e*}
  nu_f) ≠ 0` at every pinned fixture (no accidental vanishing → K-4 silent).

Two independent routes per triangle — 3-point exact interpolation of `Delta_S(t)` vs
the closed-form derivative — **agree everywhere**.

## Coverage

Fixtures e4a, e4b (n=4), e5a (n=5). `e* = (0,1)` is the PE.5 edge; the **moved-support
family** `e* ∈ {(0,1),(1,2),(0,2)}` confirms the support set tracks the fault edge
exactly. Contribution-style attribution carries no such support theorem — the dominance
clause (A-007).

## Tier & gate

`[computer-verified — exact ℚ, byte-stable ×2]` (support law + moved-support family) /
`[proven]` ((⊆) structural). **Gate K-4: NOT fired.**

## Load-bearing pins (confirmed unedited during the run)

```
verification/recert_localization.py                        581f2629f3dae3d3
old_program_sources/eng2_fault_semantics/PREREG_ENG2.md    0c11ef309a3990b5
                                 .../SHADOW_LAW_THEOREM.md  4a7da9bdb73d1b8d
                                 .../fixtures_eng2.json     8678c09570075a8b
stdout(recert_localization.py)                             f09444462bae1c97  (byte-stable ×2)
```
