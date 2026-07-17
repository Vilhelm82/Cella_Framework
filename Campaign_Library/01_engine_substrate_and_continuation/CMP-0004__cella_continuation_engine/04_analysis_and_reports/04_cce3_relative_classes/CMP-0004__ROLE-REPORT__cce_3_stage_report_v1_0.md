# CCE-3 stage report v1.0

**Verdict:** COMPLETE  
**Date:** 2026-07-14  
**Base/current HEAD:** `50683b971399236abe413cafcf2c56c5b1b9228c`  
**Worktree:** dirty overlay on the recorded base; unrelated pre-existing
deletions and untracked paper work were preserved.

## Result

CCE-3 is the first reusable symbolic continuation release. It implements the
source-bound marked lattice `(A,B,mu,delta)`, exact boundary and compact
quotient maps, the four-ring coefficient diamond, the two certified lateral
classes, independent affine compact corrections, the selected CPV midpoint,
the transported affine midpoint, Gaussian phase separation, deterministic
certificates, and checkpoint replay.

In the endpoint basis `(A_-,B_-,mu_-,delta_-^up)`:

```text
delta_up   = (0,0,0,1),       q(delta_up)   = (0,1)
delta_down = (0,0,1,1),       q(delta_down) = (1,1)
delta_up-delta_down = -mu
delta_CPV  = (0,0,1/2,1),     q(delta_CPV)  = (1/2,1).
```

The actual transports remain

```text
G_up(delta_+)   = delta_up   + lambda_up
G_down(delta_+) = delta_down + lambda_down
```

with distinct unresolved `lambda_up,lambda_down in Z[A]+Z[B]`. Their affine
half-sum is `delta_CPV+(lambda_up+lambda_down)/2`; it is not serialized as the
selected endpoint representative.

The minimal rings replay as `Z`, `Z[1/2]`, `Z[i]`, and `Z[1/2,i]` for lateral,
CPV, phased lateral, and phased CPV classes. The obstruction certificate
derives `partial(i*delta)=i*beta`; this is outside `Z*beta`, and adding closed
cycles changes the boundary by zero. It therefore proves, rather than flags,
the impossibility of an integral replacement for `i`.

## Authorities and source events

| Authority | SHA-256 |
|---|---|
| Paper III before the authorized CCE-2 insertion | `c5d790829434f848057529ef77ff855e3bc4d9f582e1d766dc2f273b4c76aeb6` |
| Paper III after Appendix A insertion | `1fc835086c30fbae414853f186a9cab9ac8c39e6cff1ed79b7364ebb5db6d5ae` |
| Stage 3 | `bdaabb1a1015f7b6b3055321b422a3b6d84053c808d2e3669ea646ff3de82670` |
| Selected Quotient Groupoids foundation | `40461c1fbb177e0d173f0b11a5d12224dc7ce894bb7fd43c944c8fa75cdaf0d9` |
| original CCE handoff v0.2 | `001fbfb3f6a84d9ba90e843fcf10feedd33e9dba7401263e29ec2ff1fd1c12b8` |
| CCE-2 exact corridor theorem | `bfb0dc4c4678803cc46e791cbe60e87736ea41ce14db157e8fb1726e28b671fe` |

Paper III lacked the already-proved exact corridor insertion. After all CCE-2
verifiers passed, Appendix A was inserted as Lemma 7F.A. The insertion retains
both compact corrections and explicitly denies a surface-sweep conclusion. No
other theorem claim was changed.

## Certificate and dependency identity

- basis manifest digest: `5a9f9b1cdd4394d217f827e5e1f1ae94d1faea6f3f71ca5ea777dd9acda581fb`
- lateral-pair digest: `5394b4ca258c50af9369766bad940d4d9d3e1d3c3b160d9b41c072155ecadf6f`
- CCE-3 source-ledger digest: `6ef7edabf446abbddebe3de96a035ac6fc201dc8bdd1d9d087b03643ae3568f1`
- CCE-3 two-file source closure: `8c014d8ec867ff8ef7e55b0699d3569f0beb23fc8c7f393dbbeb864190e0449d`
- live 52-file Pathfinder closure: `1c887a5bfe2605e085d84176e592f0823184d70526b378fb53d05ce6fdcdc195`
- live DBP provider: `0a91a1a5e50988758c0ce7221bd285ccf047eaa3ea1e6e61027938e14efc5ced`
- PF-0 confirmation: `304fccce5ed1206f23969952634d10b250d8d4d7a7a955971afa8018c2372008`

Released certificate digests:

| Operation | Digest |
|---|---|
| lateral pair | `4e80e5df3d83aa2d774b828bd411dbf16984112e40e073139443d924a78d96ff` |
| CPV over `Z[1/2]` | `e435d40410add4233752083410fd692e6121f722b28afe55b299e82814096a99` |
| phased upper | `cb268fdc9c15206df410ac4da3e0a8f6ed7d6582352d981f668c130d86c87080` |
| phased lower | `988a54e845d2b17d54c3ea5ac586aec62b5a90ec51c13cc3bbd81de16810adc2` |
| phased CPV | `059482c34e63173f60ac60c002b25726dde55087a3b24c6990843f7b66473dcd` |
| phase obstruction | `5cf123d6410c42329e44929698a897ee4b1443ff59ff902b087aa83bfffd8257` |

The canonical six-certificate bundle is
`d7084d21cf13b069a428bd9179914e0fb6c9d565b6621a410c02a333ffb3c14f`
and reproduced identically in two clean Python processes.

The CCE-3 source closure uses only Python standard-library arithmetic and the
existing continuation records. Pathfinder is reused through the two nested
CCE-2 plans; no redundant route finder was created. No external CAS, sampled
period, floating root selection, or evaluator call enters CCE-3 evidence.

## Files changed for CCE-3

Production and theorem:

- `engine/src/cella/continuation/relative_classes.py`
- `engine/src/cella/continuation/cce3.py`
- `engine/src/cella/continuation/__init__.py`
- `research/paper/Theorems/DBP/DBP_CURVATURE_PERIODS_OF_THE_DBP_QUADRIC_v1.0.md`

Verification and campaign evidence:

- `engine/tests/gate_continuation_cce3.py`
- `research/campaigns/CELLA_CONTINUATION_ENGINE/04_cce3_relative_classes/verify_cce3_relative_class_certificates.py`
- the six required CCE-3 JSON artifacts
- this report and `CCE_3_GAP_LEDGER_v1.0.md`

## Commands, gates, and timing

Principal commands were:

```text
PYTHONPATH=engine/src python engine/tests/gate_continuation_cce3.py
python research/campaigns/CELLA_CONTINUATION_ENGINE/04_cce3_relative_classes/verify_cce3_relative_class_certificates.py
for f in engine/tests/*.py; do PYTHONPATH=engine/src python "$f"; done
PYTHONPATH=engine/src python engine/benchmarks/replay_continuation_cce1.py
```

Results:

- 38/38 engine test programs passed;
- DBP evaluator: 1,591 assertions passed;
- PF-0: 58 assertions passed;
- CCE-1: 24 assertions passed;
- CCE-2: 31 assertions passed;
- CCE-2 standalone corridor checks: 47 assertions passed;
- CCE-3 focused gate: 93 assertions passed;
- CCE-3 standalone replay: 29 assertions passed.

Diagnostic timings on this host were 1.68 seconds / 28,008 KiB maximum RSS
for the focused gate and 1.01 seconds / 24,452 KiB for standalone replay.
Timing is not theorem evidence.

Frozen compatibility locks remain:

```text
schema-1.1 evaluator bundle  aa97101da7ae03f127adf4dc7940128fbdc8ee425a21c2ef88b828c76afd2989
CCE-1 six-envelope bundle    c04ba9200de47bd5fc68e84e9c932ab63e5ea9eb41981b6bba3144272b7f84a3
CCE-2 two-route bundle       b2fc82f6705cfe25070a641f4678f2caf94c35e36a11bc1023a9fd9a4f56605c
```

## Supported scope and refusals

The public CCE-3 API admits the certified lateral pair, CPV over a ring that
inverts 2, Gaussian-phased lateral classes, phased CPV over the top ring, the
boundary-obstruction proof, and checkpoint/resume. It returns class
certificates, never numeric values.

Stable refusals distinguish `RingTooSmall`, `BoundaryObstruction`,
`AbsoluteRepresentativeUnknown`, `FullTransportMatrixUnavailable`,
`EvaluationStageRequired`, scope escalation, unsupported routes/operations,
source mismatch, certificate tampering, and checkpoint mismatch. The full
machine matrix is `CCE_3_TEST_REFUSAL_MATRIX_v1.0.json`.

The valid evaluator-campaign `pathfinder_m1_scout.py` was not read, imported,
executed, or used as evidence because CCE-3 binds the primary typed Pathfinder
under `engine/src/cella/pathfinder/`; it is not deprecated by that boundary.
No stop ceremony was performed. Open obligations are enumerated without
promotion in `CCE_3_GAP_LEDGER_v1.0.md`.
