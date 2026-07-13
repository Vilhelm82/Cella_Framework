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

Battery values `e_top(P Hc P) = -2/7`, `e_top(P H P) = -6/7`, `ratio = 1/3`, `Delta_c = 4`.

> **Correction (supersedes the earlier "name-collision" read; prior wording in git history).**
> `-2/7` and `-6/7` are the battery's **un-normalized** `e_top`, each `= q·(certified)`
> with `q=14`. The **certified** invariants are the curvature-side
> `K_G = e_top(P H P)/q = -3/49` and `kc = e_top(P Hc P)/q = -1/49`, and
> `K_G = e_top(P H P)/q` is an **identity** — verified on three distinct surfaces this
> run (keystone `-3/49`, saddle `x3-x1x2` `-1/9`, coupling+ `1/12`), cross-routed to the
> RC-1/RC-4 certified values. **Scaling weight:** under `g→tg` the raw `e_top` is
> **weight 0 (scale-invariant)**; `K_G, kc` are **weight -2** (`~1/t²`). So the battery's
> `-2/7 / -6/7` are the scale-invariant *numerators*, NOT the curvature; the
> `fixtures_eng2` `anchors` field `(-1/49, -3/49)` is the certified curvature (and was
> right). Engine consequence: the sensor picks its weight deliberately — weight-0
> `e_top` carries the claim-(iii) scale invariance; weight-2 `e_top/q` is what
> cross-routes to the certified `K_G` bank at Stage C.

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
P(g)` for all `t≠0`, so the **raw coupling numerator** `e_top(P Hc P)` (weight 0) is
scale-invariant on its own — this is exactly why no `K_G` quotient is needed. Certified:
`P(tg)==P(g)` and `e_top(P Hc P)(tg,H)==e_top(P Hc P)(g,H)` exactly at `t=2,3,5/3`, every
fixture. Contrast: the curvature-normalized channel `kc = e_top/q` is weight -2 and *does*
scale; the OG ratio `kc/K_G` cancels the two weight-2 factors to recover invariance. The
numerator reaches invariance one step earlier — no denominator at all.

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
