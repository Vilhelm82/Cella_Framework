# Retirement deletion receipt

Completed: `2026-07-15T12:34:04+10:00`

Nine ignored loose originals (35,801 bytes) were deleted only after their
byte-identical library copies, independent inodes, and lack of operational inbound
references were verified. Their original paths remain preserved in `LEDGER.json`.

| Artifact | Deleted origin | Surviving library copy | SHA-256 |
|---|---|---|---|
| PAP-0244 | `archive/Reference_Material/Theorems and Papers Library/Tier_1_Proven/T8.1_Invariant_Maximality/theorem_8_1.tex.pre_dichotomy_20260615_191620.bak` | `09_historical_and_superseded_versions/dbp_role_channel_and_orbit_geometry/theorem_8_1.tex.pre_dichotomy_20260615_191620.bak` | `d25986b2510ea35ba3f747f48adc58df601b60246578d23b9d84a9c8890738fc` |
| PAP-0245 | `archive/Reference_Material/Theorems and Papers Library/Tier_1_Proven/T8.1_Invariant_Maximality/theorem_8_1_proof.py.pre_dichotomy_20260615_191620.bak` | `09_historical_and_superseded_versions/dbp_role_channel_and_orbit_geometry/theorem_8_1_proof.py.pre_dichotomy_20260615_191620.bak` | `e8348e3c33ba3d691208d519831880ae1f288b05ecec903f239d8425b0c7e474` |
| PAP-0253 | `lead7_test8_gate_dump/Lext.txt` | `05_expository_companions_and_research_maps/local_curvature_and_black_hole_metrics/Lext.txt` | `725d706449626a474a6cdedbc60cd69bcead99ee5c5d460aead51b528425b669` |
| PAP-0258 | `lead7_test8_gate_dump/den_factor.txt` | `05_expository_companions_and_research_maps/local_curvature_and_black_hole_metrics/den_factor.txt` | `31f077dfd6a92eeb5391a4ab464d474404cb53dc2218c63b120cc9da9d820c1f` |
| PAP-0259 | `lead7_test8_gate_dump/num_factor.txt` | `05_expository_companions_and_research_maps/local_curvature_and_black_hole_metrics/num_factor.txt` | `f3ce3df5a6984e9469f0220afba1c195beadc745df9ea438ad9179e14432943b` |
| PAP-0266 | `lead7_test8_gate_dump/P_coeff_A_q2.txt` | `05_expository_companions_and_research_maps/local_curvature_and_black_hole_metrics/P_coeff_A_q2.txt` | `36abba55c2faf3fa810d6b55ada1c5830f8f7d7abbfa9c283331d54c35d51ef0` |
| PAP-0267 | `lead7_test8_gate_dump/P_coeff_B_q1.txt` | `05_expository_companions_and_research_maps/local_curvature_and_black_hole_metrics/P_coeff_B_q1.txt` | `29bb9f837961b70c435c77965ae2498c7180f099a6ba50cf64442e24cc535251` |
| PAP-0268 | `lead7_test8_gate_dump/P_coeff_C_q0.txt` | `05_expository_companions_and_research_maps/local_curvature_and_black_hole_metrics/P_coeff_C_q0.txt` | `c8c6275a065a98fe5b29db70280270d7f9d323cf6a7e9f06d17c6e5d899ba183` |
| PAP-0271 | `lead7_test8_gate_dump/positive_core_P.txt` | `05_expository_companions_and_research_maps/local_curvature_and_black_hole_metrics/positive_core_P.txt` | `dd6c6eb4783a1f4af4f0065c0ff01d490246b34c0ae1ce608f9f3a0669eb5977` |

## Explicit exclusions

- The ignored theorem PDF backup remains because `Lloyd_Engine_V4/STATE/DEDUPLICATION.json` references its exact path.
- The untracked patent PDF remains because it is part of a live patent package; an adjacent office lock also indicates current use.
- Untracked Lloyd files inside engine, research, and archive package trees remain because they are structured artifacts rather than isolated floating files.
