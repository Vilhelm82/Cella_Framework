<!--
  c001 · three_channel_kg — STAGE A ledger close block.
  The merge-packager APPENDS this to results/three_channel_kg/CLAIM_LEDGER.md
  (append-only; never rewrite a prior row). The stage-runner did NOT touch the
  shared CLAIM_LEDGER.md. Eval-tier; nothing canonical until Will signs off.
-->

## Stage A close — retrodiction spine + Stage-0 controls (2026-06-23)

**Graded against** the frozen `stage_a/prereg.json`
(pin `ecced952d202c140b54a69d9042f78120326dfbee4090dd3a17574dcb4dad628`), records
`stage_a/records.jsonl` (sha256 `53321e5c53dcd43294539120f1c5f1625b68b9e5489c023260b5b416bc917376`,
two-run byte-identical), suite exit 0. Predictions **13/13 PASS**; kills fired **NONE**; preconditions
**hold** (P-self-cert, P-frame; run not void); defect-chain count **0**.

| Claim | Statement (n=3, regular, rational `(g,H)`, declared DBP frame) | Move | Status |
|---|---|---|---|
| CL-c1 | `det(H_b)=Δ_c+Δ_s+Δ_m` ⟹ `K_G=κ_c+κ_s+κ_int`, exhaustive & disjoint | `NOT_YET_PROBED →` | **DEMONSTRATED** |
| CL-c2 | bordered-determinant channels ≡ split-shape-operator channels (κ_s non-mirror) | `NOT_YET_PROBED →` | **DEMONSTRATED** |

- **CL-c1 → DEMONSTRATED (universal warrant, R1-compliant).** Gating predictions P1, P2, P3, P11,
  P12, P13 all PASS. R1 (universal claim) satisfied via the **symbolic identity over ℚ[g,H]** (P12):
  the cofactor-expanded `det(H_b)` minus `Δ_c+Δ_s+Δ_m` is the zero polynomial (0 residual monomials;
  12 det / 12 partition monomials; pairwise-disjoint supports whose union equals the det support) —
  NOT downgraded to a finite-only warrant. Finite family (P1/P2/P3/P11/P13, exact ℚ across Paths
  A/B/B′/C, keystone F8 pinned) corroborates. K2 (partition) silent.
- **CL-c2 → DEMONSTRATED (frozen family; non-R1).** Gating predictions P1, P2, P4 all PASS. The two
  disjoint channel derivations — Path A monomial vs Path B′ split-shape-operator — agree
  channel-for-channel across the frozen family `{F1..F11}`; K3 silent; the **non-mirror** κ_s is
  established (the naive κ_s-mirror mutant is rejected by K3 on the trap set F5/F6/F8). Warrant scope:
  the frozen Stage-A family (finite, exact ℚ), NOT a symbolic-over-ℚ[g,H] universal (CL-c2 is not an
  R1 universal claim).

**Armed kills (all silent on truth; each shown to fire on a constructed mutant):**
K2 (partition) — residual `0` on all 11, Path-A det = Path-B det. K3 (two-derivation) — A==B′ on all
11; κ_s-mirror mutant differs on F5/F6/F8. K5 (wrong-sign) — true sign matches oracle on F3/F7/F8;
sign-flip inverts. K6 (rank-heuristic) — F9 developable cone exactly `0` on A/B/B′/C. K8 (√q-leak) —
all emitted values `Fraction`; float operand raises `TypeError`. K9 (tolerance-leak) — `+1/10⁹`
near-miss on F8 → row-pass FALSE (no tolerance). K11 (singular-lie) — genuine `q=0` (g=(0,0,0)) typed
REFUSED on A/B/B′; F6 single `g_i=0` (q=4) → `K_G=1` (no spurious refusal).

**Scope:** Stage A graded CL-c1, CL-c2 and armed K2/K3/K5/K6/K8/K9/K11 with P-self-cert/P-frame over
fixtures F1–F11, F13. K1/K4/K7/K10 and F12/F12a/F12b are out of Stage-A scope (other stages).

**Discipline:** exact ℚ, no tolerance; eval-tier only (geometry spine fence stays CLOSED; no substrate
promotion); proposed moves PENDING Will's sign-off — nothing canonical until then.
