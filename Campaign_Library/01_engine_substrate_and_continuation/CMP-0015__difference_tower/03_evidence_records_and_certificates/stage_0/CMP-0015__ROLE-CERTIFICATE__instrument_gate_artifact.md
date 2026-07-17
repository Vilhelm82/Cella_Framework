# difference-tower — Stage-0 instrument-gate artifact (SIGNED)

**Sign-off:** Will, 2026-06-12 — Stage-0 rulings DP1–DP4 recorded as brief
§7A Amendment 1; manifest freeze mechanically delegated and executed.
**Executed by:** Claire (Claude), 2026-06-12, branch
`campaign/difference-tower`.
**Authority:** `Build_Docs/Agent_tasks/CAMPAIGN_DIFFERENCE_TOWER.md`
(GO 2026-06-12 + Amendment 1).

## Freeze record

- `manifest.json` v1: `"frozen": true` set by delegation; sha256 pin
  `85ae1400c2ac1d8e36bd6a70b2b2ce23651b309314282c08f497fe225033a029`
  recorded in `manifest_sha256.pin`.
- Generator (`make_manifest.py`) intentionally still emits
  `frozen: false` — the freeze flag is Will's, never the generator's;
  the determinism test compares content with the flag normalized out.

## Frozen gate run (×2, byte-stable)

| Check | Result |
|---|---|
| H1 dual-path exactness gate | **PASS — 1329/1329 cells equal bit-for-bit in ℚ** (units: fixture × point × scheme × j × m cells) |
| Realizability refusal demo | refused as expected (`stencil_not_realizable`) |
| Annex lane refusal demo | refused as expected (`annex_not_q_exact`) |
| Arbiter coherence | PASS — 8/8 overlap rows, every gap 0.0 (≤ 1e-25) |
| Records sha256 (×2 identical) | `caee20dcfc3d750d353bf777f4f62f11b13f239449dc60f8e3ddde320a2e49ac` |
| Stable summary sha256 (×2 identical) | `4d31be959a27aadad4b969cd15359dbd888fea0474abc3579fea8038f5d0155f` |

Records sha is byte-identical to the PREFREEZE-BENCH run — the freeze
changed flags and pins, not content.

## Standing rules now in force (Amendment 1)

- DP1: C1/C2 `true_class: annex`; H5's ℚ-identity leg narrowed to
  polynomial/rational-class route pairs.
- DP2: refuse-over-degrade below RESIDUAL_FLOOR; every BOUNDED /
  below-sufficient-condition firing location logged in stage records;
  any such firing on a rational-class fixture → surprise ledger
  immediately.
- DP3: one-sided abs rule + `jet_at_kink` refusal stand at evaluation
  level; H4 verdict rules untouched, reserved to Will (pre-Stage-D gate).
- DP4: per-point j-ladder disclosure accepted; closed.

**Stage 0 CLOSED.** Stage A authorized (H1 full grid + H3 two-sided),
prereg-first.
