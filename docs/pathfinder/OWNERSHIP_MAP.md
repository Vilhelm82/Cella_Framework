# Pathfinder ownership map

**Authority:** `campaigns/CODEX_HANDOFF_PATHFINDER_BUILD.md`  
**Target core:** `src/cella/pathfinder/`  
**Legacy compatibility source:** `src/cella/_legacy_pathfinder.py`  
**Status:** Phase 0 source and ownership audit, 2026-07-11

## Boundary

Pathfinder receives a wrapper-lowered mathematical task, performs bounded internal structural analysis, constructs admissible computational routes, compares their evidenced burdens, and returns one typed route. It stops there.

```text
host task
  -> separate host wrapper
  -> Pathfinder request/IR
  -> internal scouts and recognizers
  -> admissible route candidates
  -> Pareto/burden selection
  -> ComputationalRoute
  -> host execution and certificate modules
```

| Pathfinder owns | Pathfinder references but does not own |
|---|---|
| Wrapper-neutral request and problem IR | Host mathematical object identity and semantics |
| Bounded internal exact/scout shadows used for route discovery | General arithmetic, polynomial, Gröbner, ideal, factorization, cover, Kummer, real, or geometry services |
| Residual and structural fingerprints | Execution of the selected mathematical route |
| Route-family recognizers and conservative transformation candidates | CRT/rational reconstruction as public services |
| Route contracts, hypotheses, evidence requirements, and exceptional branches | Final result reconstruction |
| Admissibility and already-discharged-obligation tracking | Mathematical certificate construction, replay, or sealing |
| Burden vectors, Pareto comparison, and stable tie-breaking | Artifact persistence for executed mathematics |
| Route assembly and canonical route serialization | Final mathematical result emission |

Internal scouts are non-verdict-bearing and replaceable. No Pathfinder public field is a fabricated wall-clock prediction, and Pathfinder never returns the requested mathematical answer.

## Package map

```text
src/cella/pathfinder/
  api/          request, route, wrapper-neutral contracts
  ir/           normalized problem, scope, obligation, fingerprint, burden
  scout/        bounded route-discovery evidence only
  recognize/    route-family recognizers and hypothesis emitters
  plan/         registry, admissibility, comparison, assembly, selection
  compat/       legacy encoding and behavior bridge
  serialize/    canonical route serialization
```

The former `src/cella/pathfinder.py` implementation remains the behavioral reference at `src/cella/_legacy_pathfinder.py`. The package `__init__.py` re-exports `route_plan`, `rewrite_candidates`, and `pathfinder_compare`; characterization and MCP gates close through that compatibility facade. The temporary sibling location avoids changing the implementation's relative imports and can move into `compat/` when those imports are retired.

Host adapters are separate distributions/packages. M2 syntax, process control, mathematical execution, and certificate logic must not appear under `src/cella/pathfinder/`.

## Existing-code disposition

| Current source | Disposition |
|---|---|
| `src/cella/_legacy_pathfinder.py` | Frozen former `pathfinder.py` behavior behind the package facade; later replace with a typed legacy encoder. |
| `src/cella/residual_profile.py` | Internal residual scout/fingerprint input; never a public mathematical verdict. |
| `src/cella/cleanliness.py` | Preserve declared-grid equivalence and BACL/Pareto burden comparison as planning evidence. |
| `src/cella/probe_observers.py` | Internal measured scout evidence only. |
| `src/cella/typed_log_log_slope.py`, `src/cella/slope_flow.py`, `src/cella/typed_ulp.py` | Internal route-analysis support; their floating telemetry cannot discharge exact obligations. |
| `src/cella/symbolic.py` | May support bounded internal shadows; it remains a general Cella mathematical module, not Pathfinder-owned public algebra. |
| `src/cella/campaign.py`, `carrier.py`, `tower.py`, `sensors.py`, `reference_lift.py`, `periods.py` | External execution/client modules and theorem sources. Pathfinder may recognize their routes but does not execute their deliverables. |
| `src/cella/certificate.py` | Outside Pathfinder route ownership; current digest is reproducibility metadata, not an answer certificate. |
| `src/cella/mcp_server.py` | Existing transport surface; not the new Pathfinder core boundary. |
| `tools/wreath_engine/` | External mathematical executor/candidate source for later wrapper work; no dependency from Pathfinder core. |

## Source audit

The handoff requires missing sources to be named rather than silently substituted.

| Requested source | Audit result |
|---|---|
| `upload/pathfinder(1).py` | **Missing.** The earliest committed prototype was recovered from Git commit `a0beee8` at `src/cella/pathfinder.py`; it contains `route_plan` but not the later rewrite/comparison surface. The live module and current gates are the closest behavioral continuation, not claimed identity with the missing upload. |
| `CELLA_ARCHITECTURE_v1.3.md` | Found at repository root and read as the full-terrain inventory. The handoff overrides its over-scoped Build-P ownership of reconstruction, proof construction/replay, and artifact storage. |
| `CELLA_PATHFINDER_MODULE_SPEC_v1.0.md` | The exact filename is absent. The user supplied repository-root `CELLA_PATHFINDER_KERNEL_ARCHITECTURE_v1.0.md` as the intended v1.0 source; it is used for inventory only and its claim-compiler/execution/certificate ownership is overridden by the handoff. |
| `CELLA_PATHFINDER_MODULE_SPEC_v1.1.md` | **Missing.** Nearby kernel-architecture v1.1 is present but is not authority; the handoff independently prohibits the minimum-duration design. |
| `project_sources/` directory | **Missing as named.** Current or historical in-repo counterparts are mapped below. |

### Project-source counterparts

| Named handoff source | Located counterpart |
|---|---|
| `01-DBP_Curvature_Role_Reduction.md` | `Reference_Material/papers/current/DBP_Curvature_Role_Reduction.md` |
| `02-Canonical_Invariant_Reduction_Theorem.md` | `Reference_Material/papers/current/Canonical_Invariant_Reduction_Theorem.md` |
| `03-Theorem_8_1_New_Math_Extension.md` | `Reference_Material/archive/older_versions/Theorem_8_1_New_Math_Extension.md` — historical only |
| `04-Theorem_8_1_Curvature_Orbit_Correction.md` | `Reference_Material/papers/current/Theorem_8_1_Curvature_Orbit_Correction.md` |
| `05-Gauge_Channel_Transport_Law.md` | `Reference_Material/papers/current/Gauge_Channel_Transport_Law.md` |
| `06-Three_Channel_KG_Strong_Spec.md` | `Reference_Material/papers/current/Three_Channel_KG_Strong_Spec.md` |
| `07-Three_Channel_KG_New_Math_Extension.md` | `Reference_Material/papers/current/Three_Channel_KG_New_Math_Extension.md` |
| `12-lead7_kn_n3_dbp_metric.tex` | `paper/lead7_kn_n3_dbp_metric.tex` |
| `13-pfc_normal_forms.tex` | `paper/pfc_normal_forms.tex` |
| `14-self_glue_monodromy.txt` | `Reference_Material/papers/current/self_glue_monodromy.txt` |
| `15-dbp_orbit_calculus.tex` | `Reference_Material/papers/current/dbp_orbit_calculus.tex` |
| `16-DBP_Curvature_Constants_Corrected_Formulation.md` | `Reference_Material/papers/current/DBP_Curvature_Constants_Corrected_Formulation.md` |

All nine newer Galois/Kummer/realization sources named by the handoff were found under `docs/files/` and/or the self-contained publication package. Duplicate publication copies are one source family, not independent evidence.

## First-build dependency law

```text
wrapper -> Pathfinder core
execution module -> returned route
certificate module -> execution artifacts

Pathfinder core -/-> wrapper implementation
Pathfinder core -/-> M2
Pathfinder core -/-> downstream execution module
Pathfinder core -/-> certificate construction/replay
```

The release optimization target is total wrapped pipeline time, including lowering, Pathfinder analysis, selected-route execution, external certificate work, and lifting. Scout burden determines route comparison; measured end-to-end time determines release success.
