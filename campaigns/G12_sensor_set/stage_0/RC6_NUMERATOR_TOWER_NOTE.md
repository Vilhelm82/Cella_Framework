# RC-6 — the numerator tower (fault-semantics sensor), re-proven (exact-ℚ tier)

**Certificate:** `verification/recert_numerator_tower.py` — byte-stable ×2, stdout sha16
`3f14785933bed576`, exit 0. Fresh code, zero-import, exact `Fraction` on every path.

## Sensors

```
numerator tower   kc_r = e_r(P Hc P),  Hc = offdiag(H),  r = 2..n-1
  top rung        kappa_c = e_{n-1}(P Hc P)
  coupling form   Delta_c = -q * e_2(P Hc P)
OG-ratio denom    Kh = e_{n-1}(P H P)   (full Hessian)
P = I - g g^T / q,   q = g.g
```

## PE.0 keystone retrodiction  (n=3, g=(3,1,2), H=[[2,1,0],[1,0,0],[0,0,2]])

`kappa_c = -2/7`, `Kh = -6/7`, `ratio = 1/3`, `Delta_c = 4`. Independent route:
SHADOW_LAW keystone `q=14, |Mg|^2=10 ⟹ Delta_c = 14-10 = 4 ⟹ kappa_c = 4/(-14) = -2/7`.

> **Name-collision flag (brief caution).** The fixture's `anchors` field
> `kappa_c=-1/49, K_G=-3/49` is the ν/W-prod **channel** normalization (RC-4 keystone
> triple), a *different coordinate* from the raw `e_top(P Hc P) = -2/7` the battery
> asserts. Retrodicted the battery's raw value; the ν-channel is flagged, not conflated.

## Dominance over the OG ratio — three clauses

**(ii) EXACT self-fault blindness [PROVEN, all n].** `kappa_c` and `Delta_c` factor
through `Hc = offdiag(H)`. Self-faults `S1 (H00 += t)`, `S2 (H_diag += t·d_s)` act only
on the diagonal, so `offdiag(H + D) = offdiag(H)` for **every** diagonal `D` — the whole
tower is identically unchanged. Exact zero response, not small. Certified two ways:
(a) **identity** — `kc, Delta_c` invariant under random diagonal perturbations at every
fixture; (b) **fixtures** — `kc(t), Delta_c(t)` are degree-0 (constant) polynomials
under S1, S2. The ratio `kappa_c/Kh` **fails** blindness: `Kh` reads the diagonal, so
`d/dt[kappa_c/Kh] ≠ 0` under self-faults — the literal OG clause "self-faults preserve
the ratio" is false (PE.4); the corrected invariant is the numerator.

**(iii) Scale invariance without the quotient [PROVEN].** `P(tg) = I − t²gg^T/(t²q) =
P(g)` for all `t≠0`, so `kappa_c = e_top(P Hc P)` is scale-invariant on its own.
Certified: `P(tg)==P(g)` and `kappa_c(tg,H)==kappa_c(g,H)` exactly at `t=2,3,5/3`, every
fixture. The OG got scale invariance only via the ratio; the numerator needs no denominator.

**(i) Coupling sensitivity [demonstrated].** Under `F1 (H01 += t)` and `F2` (generic
coupling), `kappa_c` is non-constant and `d/dt[kappa_c/Kh] ≠ 0` at every fixture — same
coupling sensitivity as the ratio.

## Fixtures & tier

e3key (n=3), e4a/e4b (n=4), e5a (n=5); fault families F1/F2 (coupling) + S1/S2 (self),
exact ℚ. `[computer-verified — exact ℚ, byte-stable ×2]` (PE.0 retrodiction, fixture
demonstrations) / `[proven]` (blindness by factor-through-Hc; scaling by `P(tg)=P(g)`).
**Gates K-1, K-2: NOT fired.**

## Load-bearing pins (confirmed unedited during the run)

```
verification/recert_numerator_tower.py                     a68a1f3378869882
old_program_sources/eng2_fault_semantics/PREREG_ENG2.md    0c11ef309a3990b5
                                 .../SHADOW_LAW_THEOREM.md  4a7da9bdb73d1b8d
                                 .../fixtures_eng2.json     8678c09570075a8b
                                 .../eng2_battery.py        07f95d0efff58553
stdout(recert_numerator_tower.py)                          3f14785933bed576  (byte-stable ×2)
```
