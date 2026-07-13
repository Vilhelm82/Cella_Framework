# GAPS — open holes, cumulative across sessions

Schema per entry: `## G-NNN <slug>` then `gap / blocks / attempted / known-echo /
status`. Gap work resumes from here — do not restart from a blank stare. Before
proposing candidate solutions, write an **affordance survey** into the entry:
enumerate the corpus blocks (D-/R- ids) and the moves they afford. Candidates
must trace back to that survey. If a gap resembles a known external design, name
it in `known-echo` and quarantine it as a comparison object — using it as the
scaffold (directly, or by rebuilding it from blocks) is import laundering. If
corpus blocks provably cannot reach the gap, record the obstruction and escalate
through docs/ADMISSIONS.md — the only legal import path.

## G-001 pathfinder-self-containment
gap:         The typed pathfinder package's three public entry points —
             `route_plan`, `rewrite_candidates`, `pathfinder_compare` — are not
             natively implemented. `pathfinder/__init__.py` re-exports them from
             `pathfinder/compat/`, which imports them from the frozen
             `engine/src/cella/_legacy_pathfinder.py`. The package presents a
             typed-native facade while the behavior is still the legacy prototype.
blocks:      Partial native machinery exists (~9.7k lines in the typed package)
             but it is NOT a drop-in for the legacy trio:
             - `plan/select.py::plan_request` and `plan/compare.py::compare_candidates`
               exist but consume a typed IR (`PathfinderRequest` / `RouteCandidate`,
               `pathfinder/api/route.py` + `ir/`), where the legacy `route_plan` /
               `pathfinder_compare` take raw strings / untyped dicts — closing these
               needs typed-IR adapters, not a re-point.
             - `rewrite_candidates` (candidate enumeration for host ranking) has NO
               native equivalent. The nearest, `recognize/rewrite.py::recognize_symbolic_collapse_rewrite`,
               admits/refuses one route family and returns an executor instruction —
               a different output contract. This third function needs new native
               design, not wiring.
attempted:   None recorded. `engine/tests/gate_pathfinder_prototype_characterization.py`
             is the seam that pins native-vs-legacy behavioral equivalence and
             must stay green through any change here.
known-echo:  n/a — this is a native-completion gap, not an external design.
status:      open — deferred pending the MCP tool-list rebuild (see CURRENT.md
             active work). To close: design a native `rewrite_candidates`; adapt
             the typed api/plan layer to the legacy input/output contracts;
             satisfy the characterization gate; then delete pathfinder/compat/ and
             _legacy_pathfinder.py.

---

> **DISCOVERY-QUEUE SEEDING PENDING.** The research discovery queue (LEAD-1 …
> LEAD-9 — role-channel curvature, stratum classification, channel topology, the
> odd √q sector, order-3 transport, D_static, the n=3 DBP metric, higher
> Cohn-Vossen, the PFC calculus) lives at `archive/pre-canon/LEADS.md`. Migrating
> each open lead into a `G-` entry (with its affordance survey) is ratified work,
> not auto-transcription — a lead's precise mathematical statement is the
> maintainer's to canonicalize. Until migrated, treat `archive/pre-canon/LEADS.md`
> as the authoritative open-work list and this ledger as the destination.
> Roadmap-level future layers (Layer 2 time-series bridge, Layer 3 diagnostic
> surface) are tracked in `docs/ROADMAP.md`, not here.

<!-- template — copy, do not delete:
## G-NNN <slug>
gap:         <precise statement of what is missing>
blocks:      <D-/R- ids believed relevant>
attempted:   <sessions/<date>.md — route tried, where it dead-ends>
known-echo:  <classical X it resembles — declared, quarantined, NOT the scaffold>
status:      open
-->
