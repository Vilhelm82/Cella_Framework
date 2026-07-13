# State Canon & Repository Reorganization — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the repo into five epistemically-distinct regions (STATE/engine/research/docs/archive), scaffold the schema-bound STATE/ canon, and install the session/derivation protocols — without breaking the gate suite or either MCP server.

**Architecture:** Purely additive-then-move migration executed in ordered phases, each ending with the full gate suite green and both MCP servers importable. Moves use `git mv` to preserve history. The program (`src`, `tests`, `tools`) moves *together* under `engine/` so the tests' `parent.parent / "src"` import geometry is preserved with zero test edits; only three genuine path couplings are hand-fixed. The canon (`STATE/`) is created as empty-but-schema-valid files plus a bootstrapped `CURRENT.md`; interactive population of load-bearing results is explicitly deferred (requires user ratification).

**Tech Stack:** Python 3 (stdlib only for the gate harness), git, Desktop Commander (filesystem access from claude.ai). Gates are standalone `__main__` scripts run as `PYTHONPATH=<src> python3 <gate>.py`, exit 0 = pass. No pytest.

## Global Constraints

- **Never leave the repo broken between tasks.** Every task ends with the gate suite showing the *same passing set* as the captured baseline (Task 1) — no new failures.
- **All moves via `git mv`** — preserve history; never delete-and-recreate a tracked file.
- **`PYTHONPATH` stays the primary run mechanism.** `pyproject.toml` is added for identity/installability but the MCP server and gates must keep working via `PYTHONPATH` with no venv/install step (Desktop Commander sessions have no install).
- **Reference_Material stays tracked** (README rule; `.gitignore` note). Moving it under `archive/` must not un-track it; only its transient-junk ignore paths get repointed.
- **Canon schemas are law.** Any `STATE/` file created here must conform to the schemas in the spec §4 — mandatory `scope`/`not-scope`/`displaced-by` on constraints; no bare slogans.
- **Spec:** `docs/superpowers/specs/2026-07-13-state-canon-reorg-design.md` is the source of truth for schemas, region status, and protocol text.

---

## File Structure

**Reusable verify snippet** (referenced as **[GATE-CHECK]** throughout). Run from repo root; `SRC` and `TESTS` differ by phase:

```bash
# Before Phase 1:  SRC=src        TESTS=tests
# After  Phase 1:  SRC=engine/src TESTS=engine/tests
SRC=engine/src; TESTS=engine/tests
for f in "$TESTS"/gate_*.py; do
  if PYTHONPATH="$SRC" python3 "$f" >/dev/null 2>&1; then echo "PASS $(basename "$f")"
  else echo "FAIL $(basename "$f")"; fi
done | sort > /tmp/claude-1000/-home-wlloyd-Cella-Framework/74da3a5b-08de-4170-be82-7db1faef94dc/scratchpad/gates_now.txt
diff /tmp/claude-1000/-home-wlloyd-Cella-Framework/74da3a5b-08de-4170-be82-7db1faef94dc/scratchpad/gates_baseline.txt \
     /tmp/claude-1000/-home-wlloyd-Cella-Framework/74da3a5b-08de-4170-be82-7db1faef94dc/scratchpad/gates_now.txt \
  && echo "GATE SET UNCHANGED ✓" || echo "GATE SET CHANGED ✗ — investigate before proceeding"
```

**MCP smoke** (referenced as **[MCP-CHECK]**):

```bash
# After Phase 1, paths are engine/src and engine/tools/wreath_engine
PYTHONPATH=engine/src python3 -m cella.mcp_server --help >/dev/null 2>&1 && echo "cella MCP imports ✓" || echo "cella MCP BROKEN ✗"
```

Files touched by hand (everything else moves untouched):

| File | Change | Task |
|------|--------|------|
| `.mcp.json` | `PYTHONPATH: src`→`engine/src`; wreath `--directory tools/...`→`engine/tools/...` | 2 |
| `engine/pyproject.toml` | **create** — src-layout package identity | 2 |
| `engine/tests/gate_dbp_native_relative_periods.py` | `parents[1]`→`parents[2]`; `campaigns/`→`research/campaigns/` | 3 |
| `engine/src/cella/hostile_benchmark.py:483` | `--output` default `reports/`→`research/reports/` | 3 |
| provenance citation strings in `engine/src/cella/**` | `"campaigns/…`/`"paper/…`/`"reports/…` → `"research/…` | 3 |
| `.gitignore` | repoint `Reference_Material/**` ignores → `archive/Reference_Material/**`; add `tmp/` | 4 |
| `README.md` | rewrite to ~1 screen pointing at `STATE/CURRENT.md` | 5 |

---

### Task 1: Capture baseline (no regression can be proven without it)

**Files:**
- Create: `scratchpad/gates_baseline.txt` (scratch, not committed)
- Create: `scratchpad/tree_baseline.txt` (scratch)

**Interfaces:**
- Produces: `gates_baseline.txt` — the authoritative "passing set" every later task diffs against via **[GATE-CHECK]**.

- [ ] **Step 1: Record the current passing gate set**

```bash
cd "/home/wlloyd/Cella Framework"
SB=/tmp/claude-1000/-home-wlloyd-Cella-Framework/74da3a5b-08de-4170-be82-7db1faef94dc/scratchpad
for f in tests/gate_*.py; do
  if PYTHONPATH=src python3 "$f" >/dev/null 2>&1; then echo "PASS $(basename "$f")"
  else echo "FAIL $(basename "$f")"; fi
done | sort > "$SB/gates_baseline.txt"
cat "$SB/gates_baseline.txt"
```

Expected: a list of `PASS gate_*.py` / `FAIL gate_*.py` lines. **Some gates may already be FAIL (later-layer gates are open) — that is fine.** The invariant is that this exact set is preserved, not that all pass.

- [ ] **Step 2: Snapshot the tracked tree**

```bash
cd "/home/wlloyd/Cella Framework"
git ls-files > "$SB/tree_baseline.txt"; wc -l "$SB/tree_baseline.txt"
```

Expected: ~681 files.

- [ ] **Step 3: Confirm clean-ish working tree**

```bash
cd "/home/wlloyd/Cella Framework" && git status --short | grep -v '^ M src/cella/native_periods/' || echo "only known pre-existing edits present"
```

Expected: only the three pre-existing `native_periods` modifications from session start (leave them; not our concern). No commit in this task.

---

### Task 2: Phase 1 — move the program into `engine/`

**Files:**
- Move: `src/ tests/ tools/` → `engine/`
- Modify: `.mcp.json`
- Create: `engine/pyproject.toml`

**Interfaces:**
- Consumes: `gates_baseline.txt` (Task 1).
- Produces: program rooted at `engine/`; gates run with `PYTHONPATH=engine/src`, MCP with `PYTHONPATH=engine/src python3 -m cella.mcp_server`.

- [ ] **Step 1: Move the three program dirs together (preserves test import geometry)**

```bash
cd "/home/wlloyd/Cella Framework"
mkdir -p engine
git mv src engine/src
git mv tests engine/tests
git mv tools engine/tools
```

- [ ] **Step 2: Verify the sys.path geometry survived — run [GATE-CHECK] with new paths**

```bash
cd "/home/wlloyd/Cella Framework"
SB=/tmp/claude-1000/-home-wlloyd-Cella-Framework/74da3a5b-08de-4170-be82-7db1faef94dc/scratchpad
for f in engine/tests/gate_*.py; do
  if PYTHONPATH=engine/src python3 "$f" >/dev/null 2>&1; then echo "PASS $(basename "$f")"
  else echo "FAIL $(basename "$f")"; fi
done | sort > "$SB/gates_now.txt"
diff "$SB/gates_baseline.txt" "$SB/gates_now.txt" && echo "GATE SET UNCHANGED ✓" || echo "CHANGED ✗"
```

Expected: `GATE SET UNCHANGED ✓`. (The 33 `parent.parent / "src"` and the `ROOT / "tools" / "pathfinder_m2"` tests now resolve to `engine/src` and `engine/tools/pathfinder_m2` — both correct because all three moved together.)

> If any gate that read `campaigns/…` via a repo-root path FAILs here, it is `gate_dbp_native_relative_periods.py` — it is fixed in Task 3. If it was PASSing at baseline it will still PASS now (campaigns hasn't moved yet); it only breaks in Task 3, where its fix lives.

- [ ] **Step 3: Update `.mcp.json` paths**

Change `PYTHONPATH` and the wreath `--directory`:

```json
{
  "mcpServers": {
    "cella": {
      "type": "stdio",
      "command": "python3",
      "args": ["-m", "cella.mcp_server", "--router", "--profile", "core"],
      "env": { "PYTHONPATH": "engine/src" }
    },
    "wreath-engine": {
      "type": "stdio",
      "command": "uv",
      "args": ["--directory", "engine/tools/wreath_engine", "run", "wreath-engine-mcp"]
    }
  }
}
```

- [ ] **Step 4: Create `engine/pyproject.toml` (identity only; PYTHONPATH stays primary)**

```toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "cella"
version = "0.1.0"
description = "Cella Framework — exact residue accounting engine"
requires-python = ">=3.10"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
cella = ["*.md", "*.json"]
```

- [ ] **Step 5: Run [MCP-CHECK]**

```bash
cd "/home/wlloyd/Cella Framework"
PYTHONPATH=engine/src python3 -m cella.mcp_server --help >/dev/null 2>&1 && echo "cella MCP imports ✓" || echo "cella MCP BROKEN ✗"
```

Expected: `cella MCP imports ✓`.

- [ ] **Step 6: Commit**

```bash
cd "/home/wlloyd/Cella Framework"
git add -A
git commit -m "reorg(phase 1): move program (src/tests/tools) under engine/ + pyproject

$(printf 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_016rVCVapxwgHqwKmyeKDTt8')"
```

---

### Task 3: Phase 2 — move research into `research/` and fix the two functional couplings

**Files:**
- Move: `campaigns/ verification/ benchmarks/ reports/ paper/` → `research/`
- Create: `research/derivations/` (+ move `legendre_native.py` into it)
- Modify: `engine/tests/gate_dbp_native_relative_periods.py`
- Modify: `engine/src/cella/hostile_benchmark.py` (line ~483)
- Modify: provenance citation strings across `engine/src/cella/**`

**Interfaces:**
- Consumes: Phase 1 layout.
- Produces: research rooted at `research/`; the DBP gate and hostile-benchmark output path repointed; citation strings accurate.

- [ ] **Step 1: Move the research dirs**

```bash
cd "/home/wlloyd/Cella Framework"
mkdir -p research
for d in campaigns verification benchmarks reports paper; do git mv "$d" "research/$d"; done
mkdir -p research/derivations
git mv legendre_native.py research/derivations/legendre_native.py
```

> `legendre_native.py` imports `verify_local_curvature_calculus` from `/mnt/user-data/uploads` (a claude.ai upload dir) — it is a non-portable session artifact, archived as the seed of the derivations trail. Do **not** try to make it runnable; its dependency is not in the repo.

- [ ] **Step 2: Fix the DBP gate — depth AND prefix (write the change)**

`engine/tests/gate_dbp_native_relative_periods.py` line 34-35. Under the new layout the test sits at `engine/tests/`, so `parents[1]` is now `engine/` (was repo root); campaigns now lives at `research/campaigns`. Change both:

```python
# line 34 — was: root = Path(__file__).resolve().parents[1]
root = Path(__file__).resolve().parents[2]
# line 35 — was: ...(root/"campaigns/DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR/DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR_CONTRACTS_v1.0.json")
contracts = json.loads((root/"research/campaigns/DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR/DBP_NATIVE_RELATIVE_PERIOD_EVALUATOR_CONTRACTS_v1.0.json").read_text())
```

- [ ] **Step 3: Verify the DBP gate specifically passes**

```bash
cd "/home/wlloyd/Cella Framework"
PYTHONPATH=engine/src python3 engine/tests/gate_dbp_native_relative_periods.py >/dev/null 2>&1 && echo "DBP gate ✓" || echo "DBP gate ✗"
```

Expected: `DBP gate ✓` (if it was PASS at baseline). If it was FAIL at baseline for unrelated reasons, confirm it is not failing on a `FileNotFoundError` for the contracts path:

```bash
PYTHONPATH=engine/src python3 engine/tests/gate_dbp_native_relative_periods.py 2>&1 | grep -i "no such file\|FileNotFound" && echo "PATH STILL BROKEN ✗" || echo "no path error ✓"
```

Expected: `no path error ✓`.

- [ ] **Step 4: Fix the functional `--output` default in hostile_benchmark.py**

`engine/src/cella/hostile_benchmark.py` ~line 483:

```python
# was: parser.add_argument("--output", default="reports/pathfinder_hostile/mvp-report.json")
    parser.add_argument("--output", default="research/reports/pathfinder_hostile/mvp-report.json")
```

- [ ] **Step 5: Repoint provenance citation strings (mechanical, accuracy fix)**

These are citation metadata (not file reads except the DBP one already fixed). No test asserts them (verified: only the DBP gate read a research file). Update prefixes so pointers stay valid:

```bash
cd "/home/wlloyd/Cella Framework"
grep -rl '"campaigns/\|"paper/\|"reports/' engine/src/cella --include='*.py' | grep -v __pycache__ | while read -r f; do
  sed -i 's#"campaigns/#"research/campaigns/#g; s#"paper/#"research/paper/#g; s#"reports/#"research/reports/#g' "$f"
done
# verify none remain that point outside research/
grep -rn '"campaigns/\|"paper/\|"reports/' engine/src/cella --include='*.py' | grep -v __pycache__ | grep -v '"research/' && echo "STRAGGLERS ✗" || echo "all citations repointed ✓"
```

Expected: `all citations repointed ✓`.

- [ ] **Step 6: Full [GATE-CHECK] — no regression**

```bash
cd "/home/wlloyd/Cella Framework"
SB=/tmp/claude-1000/-home-wlloyd-Cella-Framework/74da3a5b-08de-4170-be82-7db1faef94dc/scratchpad
for f in engine/tests/gate_*.py; do
  if PYTHONPATH=engine/src python3 "$f" >/dev/null 2>&1; then echo "PASS $(basename "$f")"
  else echo "FAIL $(basename "$f")"; fi
done | sort > "$SB/gates_now.txt"
diff "$SB/gates_baseline.txt" "$SB/gates_now.txt" && echo "GATE SET UNCHANGED ✓" || echo "CHANGED ✗"
```

Expected: `GATE SET UNCHANGED ✓`.

- [ ] **Step 7: Commit**

```bash
cd "/home/wlloyd/Cella Framework"
git add -A
git commit -m "reorg(phase 2): move research under research/; fix DBP gate + hostile output + citations

$(printf 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_016rVCVapxwgHqwKmyeKDTt8')"
```

---

### Task 4: Phase 3 — docs, archive, and junk

**Files:**
- Create: `docs/architecture/`, `archive/handoffs/`, `archive/packages/`
- Move: architecture docs, governance docs, handoffs, Reference_Material, zips
- Modify: `.gitignore`
- Untrack: `tmp/`, `lead7_test8_gate_dump/`

**Interfaces:**
- Consumes: Phase 1–2 layout.
- Produces: five clean top-level regions; sediment quarantined; canon slot (`STATE/`) still empty (Task 5).

- [ ] **Step 1: Architecture + governance docs into `docs/`**

```bash
cd "/home/wlloyd/Cella Framework"
mkdir -p docs/architecture
git mv CELLA_ARCHITECTURE_v1.3.md docs/architecture/
git mv CELLA_PATHFINDER_KERNEL_ARCHITECTURE_v1.0.md docs/architecture/
# delta versions already under docs/ — group them too
for f in docs/CELLA_PATHFINDER_KERNEL_ARCHITECTURE_v1_2*_DELTA.md; do git mv "$f" docs/architecture/; done
git mv ADMISSIONS.md ROADMAP.md CERTIFICATE_SCHEMA.md POSITIONING.md docs/
```

- [ ] **Step 2: Handoffs + sediment into `archive/`**

```bash
cd "/home/wlloyd/Cella Framework"
mkdir -p archive/handoffs archive/packages
git mv BOOT.md CELLA_SESSION_HANDOFF.md HANDOFF_2026-07-09.md archive/handoffs/
git mv Reference_Material archive/Reference_Material
# zip artifacts
git mv research/campaigns/CV_curvature_valence.zip archive/packages/ 2>/dev/null || true
git mv docs/galois_horizon_cover_v1_0_publication_package.zip archive/packages/ 2>/dev/null || true
```

> `LEADS.md`, `LEVER_AUDIT.md`, `E_ATOM_DERIVATION.md` are **left at root for now** — they are canon-extraction *sources* consumed in Task 5, which moves them to `archive/` after mining. Moving them here would scatter that step.

- [ ] **Step 3: Untrack transient junk and repoint `.gitignore`**

```bash
cd "/home/wlloyd/Cella Framework"
git rm -r --cached tmp lead7_test8_gate_dump 2>/dev/null || true
```

Then edit `.gitignore`: change the two `Reference_Material/**` lines to `archive/Reference_Material/**`, and add `tmp/`:

```
# was: Reference_Material/**/__pycache__/  and  Reference_Material/**/*.pyc
archive/Reference_Material/**/__pycache__/
archive/Reference_Material/**/*.pyc
tmp/
```

(The existing `lead7_test8_gate_dump/` ignore line stays.)

- [ ] **Step 4: Verify Reference_Material is still tracked (not accidentally ignored)**

```bash
cd "/home/wlloyd/Cella Framework"
git ls-files archive/Reference_Material | wc -l
```

Expected: ~91 (same as before the move). If 0, the `.gitignore` repoint over-matched — fix before committing.

- [ ] **Step 5: Verify the tree invariant — nothing outside the five regions**

```bash
cd "/home/wlloyd/Cella Framework"
git ls-files | awk -F/ '{print $1}' | sort -u
```

Expected: only `.github`, `.gitignore`, `.mcp.json`, `README.md`, `E_ATOM_DERIVATION.md`, `LEADS.md`, `LEVER_AUDIT.md` (the three canon-sources, gone after Task 5), and the five region dirs `STATE`(after Task 5) `archive docs engine research`. No stray `benchmarks/`, `campaigns/`, `tmp/`, etc.

- [ ] **Step 6: [GATE-CHECK] — moving docs must not touch gates**

```bash
cd "/home/wlloyd/Cella Framework"
SB=/tmp/claude-1000/-home-wlloyd-Cella-Framework/74da3a5b-08de-4170-be82-7db1faef94dc/scratchpad
for f in engine/tests/gate_*.py; do
  if PYTHONPATH=engine/src python3 "$f" >/dev/null 2>&1; then echo "PASS $(basename "$f")"
  else echo "FAIL $(basename "$f")"; fi
done | sort > "$SB/gates_now.txt"
diff "$SB/gates_baseline.txt" "$SB/gates_now.txt" && echo "GATE SET UNCHANGED ✓" || echo "CHANGED ✗"
```

Expected: `GATE SET UNCHANGED ✓`.

- [ ] **Step 7: Commit**

```bash
cd "/home/wlloyd/Cella Framework"
git add -A
git commit -m "reorg(phase 3): docs/ governance, archive/ sediment, untrack tmp

$(printf 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_016rVCVapxwgHqwKmyeKDTt8')"
```

---

### Task 5: Phase 4-scaffold — create the STATE/ canon (schema-valid, bootstrapped)

**Files:**
- Create: `STATE/CURRENT.md`, `STATE/RESULTS.md`, `STATE/CONSTRAINTS.md`, `STATE/DEFINITIONS.md`, `STATE/GAPS.md`, `STATE/sessions/.gitkeep`
- Modify: `README.md` (rewrite to ~1 screen)
- Move (after mining): `LEADS.md`, `LEVER_AUDIT.md`, `E_ATOM_DERIVATION.md` → `archive/`

**Interfaces:**
- Consumes: README (three standing rules), ROADMAP (layer/gate status), the three root source docs.
- Produces: a schema-valid canon. **RESULTS/DEFINITIONS ship with `C-`/example entries and a `pending` marker — full population is deferred (needs user ratification, spec §8 Phase 4).**

- [ ] **Step 1: Create `STATE/CONSTRAINTS.md` with the three standing rules as real entries**

Populate from README's three rules, in the spec §4.3 schema. Full file:

```markdown
# CONSTRAINTS — the constraint register

**Rule zero: if it is not in this register, it is not a constraint.** Prose
elsewhere (docs, reports, code comments, git history) is context, never a rule.

## C-001 standalone-zero-import
rule:        No code, design, doc, or corpus is imported wholesale from prior
             work; everything is built and certified in-repo.
scope:       All of engine/ and any result entering RESULTS.md.
not-scope:   Reading prior work in archive/ for context or comparison; the
             admission path (C-002) is how external material legally enters.
why:         The repo's value is that every capability was derived here.
displaced-by: An ADMISSIONS.md case that closes (see C-002).

## C-002 admission-rule
rule:        Anything from prior work enters only via an ADMISSIONS.md record
             that closes: why needed, why nothing derivable beats it, what
             would displace it.
scope:       Introduction of any external design/formula/doc/corpus.
not-scope:   In-repo derivation from admitted building blocks (that is the norm,
             not an admission).
why:         Keeps the corpus auditable and displacement-by-evidence honest.
displaced-by: Revision of the admission ledger itself.
source:      docs/ADMISSIONS.md

## C-003 re-verification-rule
rule:        No prior result is trusted on documentary status. Every
             mathematical input is re-proven in-repo (fresh code, byte-stable
             ×2, under research/verification/) before it bears load.
scope:       Any result gaining status: current in RESULTS.md.
not-scope:   Exploratory scouting and hypothesis testing (results there are not
             load-bearing until certified).
why:         Trust attaches to re-runnable certificates, never to labels.
displaced-by: A stronger certification standard.
```

- [ ] **Step 2: Create `STATE/RESULTS.md` and `STATE/DEFINITIONS.md` (schema headers + deferred-population marker)**

`STATE/RESULTS.md`:

```markdown
# RESULTS — ledger of load-bearing results

Schema per entry: `## R-NNN <slug>` then fields `claim / status / scope /
certificate / depends-on`. Supersession edits the old entry's `status` in
place. A result with no certificate pointer may not be `status: current`.

> **POPULATION PENDING.** Load-bearing results are migrated from LEADS.md,
> reports/, and verification/ interactively, each ratified by the maintainer
> before gaining `status: current` (spec §8 Phase 4). Until then this ledger is
> empty by design — absence here means "not yet migrated", not "no results".

<!-- template:
## R-001 <slug>
claim:       <one precise declarative sentence, no adjectives>
status:      current
scope:       <where it holds; where it does not>
certificate: research/verification/<file>.py  (byte-stable ×2)
depends-on:  <R-/D- ids>
-->
```

`STATE/DEFINITIONS.md`:

```markdown
# DEFINITIONS — canonical objects & notation

Schema per entry: `## D-NNN <slug>` then `object / domain / source / used-by`.
Check here before deriving any quantity (anti-rederivation).

> **POPULATION PENDING** — same ratified-migration process as RESULTS.md.

<!-- template:
## D-001 <slug>
object:      <formula / definition, canonical form>
domain:      <where defined>
source:      derived research/derivations/<file>.md | admitted docs/ADMISSIONS.md §…
used-by:     <R- ids>
-->
```

- [ ] **Step 3: Create `STATE/GAPS.md`, seeded from known open items**

Seed from ROADMAP open layers + the three root source docs (LEADS/LEVER_AUDIT). Keep entries honest — mark them `open`, fill `blocks` only where you can name real corpus objects, else leave a note:

```markdown
# GAPS — open holes, cumulative across sessions

Schema per entry: `## G-NNN <slug>` then `gap / blocks / attempted /
known-echo / status`. Gap work resumes from here; do not restart from blank.

> **SEEDING PASS.** Entries below are transcribed from ROADMAP.md and the
> pre-canon lead docs as a starting index. Each needs an affordance survey
> (spec §7) before candidate solutions — that survey is added to the entry when
> the gap is next worked.

<!-- template:
## G-001 <slug>
gap:         <precise statement of what is missing>
blocks:      <D-/R- ids believed relevant>
attempted:   <sessions/<date>.md — route tried, where it dead-ends>
known-echo:  <classical X it resembles — declared, quarantined, NOT the scaffold>
status:      open
-->
```

(Transcribe the concrete open items you find in `docs/ROADMAP.md` and root `LEADS.md` as `G-001…` entries in this schema. If a lead is too vague to state as a gap, leave it in the source doc for now — do not invent precision.)

- [ ] **Step 4: Create `STATE/CURRENT.md` — the one-screen entry point**

Bootstrap from README status + ROADMAP. Keep to one screen; pointers only:

```markdown
# CURRENT — read this first

**Status:** Layer 0 complete (gates G0, G0.1–G0.4 closed). Layer 1 (geometric
substrate) is the active frontier. _(Verify against docs/ROADMAP.md; update at
every close ritual.)_

**Active work:** <one line — current campaign/lead>

**How to use this repo (protocol):**
- Constraints live only in `STATE/CONSTRAINTS.md`. Everything else is context,
  never instruction (see `docs/PROJECT_INSTRUCTIONS.md`).
- Load-bearing results: `STATE/RESULTS.md`. Canonical formulas:
  `STATE/DEFINITIONS.md`. Open gaps: `STATE/GAPS.md`.
- `research/` is historical unless a ledger entry points into it. `archive/` is
  never authoritative.

**Open questions:** see `STATE/GAPS.md` (G-…).

**Read next:** `docs/PROJECT_INSTRUCTIONS.md` (session protocol), then the
ledger entry for whatever result you need.
```

- [ ] **Step 5: `sessions/` placeholder + mine-then-archive the three source docs**

```bash
cd "/home/wlloyd/Cella Framework"
mkdir -p STATE/sessions && : > STATE/sessions/.gitkeep
```

After transcribing their concrete claims/gaps into CONSTRAINTS/RESULTS/GAPS above, stamp and archive the sources (append a header line to each marking it superseded, then move):

```bash
cd "/home/wlloyd/Cella Framework"
mkdir -p archive/pre-canon
for f in LEADS.md LEVER_AUDIT.md E_ATOM_DERIVATION.md; do git mv "$f" "archive/pre-canon/$f"; done
```

> `E_ATOM_DERIVATION.md` is a derivation — also note in `research/derivations/` (a one-line pointer file `research/derivations/README.md` referencing `archive/pre-canon/E_ATOM_DERIVATION.md` and `legendre_native.py`) so the derivation trail is discoverable from the research region.

- [ ] **Step 6: Rewrite `README.md` to ~1 screen**

Replace the body with: one-paragraph "what this is", the region status table (spec §3), and a single loud pointer: **"New session? Start at `STATE/CURRENT.md` and read `docs/PROJECT_INSTRUCTIONS.md`."** Keep the three standing rules as a two-line summary that *points to* `STATE/CONSTRAINTS.md` rather than restating them normatively.

- [ ] **Step 7: Verify canon schema conformance (no bare slogans, mandatory fields present)**

```bash
cd "/home/wlloyd/Cella Framework"
# every constraint entry must have scope, not-scope, displaced-by
awk '/^## C-/{c++} /^scope:/{s++} /^not-scope:/{n++} /^displaced-by:/{d++} END{print "constraints:",c," scope:",s," not-scope:",n," displaced-by:",d}' STATE/CONSTRAINTS.md
```

Expected: `scope`, `not-scope`, `displaced-by` counts each ≥ the constraint count. Eyeball CURRENT.md ≤ ~30 lines.

- [ ] **Step 8: Commit**

```bash
cd "/home/wlloyd/Cella Framework"
git add -A
git commit -m "reorg(phase 4): scaffold STATE/ canon + rewrite README; archive pre-canon sources

$(printf 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_016rVCVapxwgHqwKmyeKDTt8')"
```

---

### Task 6: Phase 5 — the protocol document + whole-repo verification

**Files:**
- Create: `docs/PROJECT_INSTRUCTIONS.md`
- (final verification only)

**Interfaces:**
- Consumes: the full new layout + canon.
- Produces: the paste-into-claude.ai-Project instruction text; a green whole-repo verification.

- [ ] **Step 1: Write `docs/PROJECT_INSTRUCTIONS.md`**

Assemble verbatim from spec §6–§7. Sections, in order: **Region status table** (§3); **Boot ritual** (§6.1); **Openness protocol** (§6.2, the blockquote); **Derivation-first protocol** (§7: affordance survey → declaration rule → dead-end escalation); **Close ritual** (§6.3, triggered by "wrap up", including the laundering audit and style-law sweep). End with: "This file is the versioned source of the claude.ai Project custom-instructions; paste its contents there."

- [ ] **Step 2: Whole-repo tree invariant**

```bash
cd "/home/wlloyd/Cella Framework"
git ls-files | awk -F/ '{print $1}' | sort -u
```

Expected exactly: `.github .gitignore .mcp.json README.md STATE archive docs engine research`. No `LEADS.md`/`LEVER_AUDIT.md`/`E_ATOM_DERIVATION.md` at root (archived in Task 5), no stray region dirs.

- [ ] **Step 3: Final [GATE-CHECK] + [MCP-CHECK]**

```bash
cd "/home/wlloyd/Cella Framework"
SB=/tmp/claude-1000/-home-wlloyd-Cella-Framework/74da3a5b-08de-4170-be82-7db1faef94dc/scratchpad
for f in engine/tests/gate_*.py; do
  if PYTHONPATH=engine/src python3 "$f" >/dev/null 2>&1; then echo "PASS $(basename "$f")"
  else echo "FAIL $(basename "$f")"; fi
done | sort > "$SB/gates_now.txt"
diff "$SB/gates_baseline.txt" "$SB/gates_now.txt" && echo "GATE SET UNCHANGED ✓" || echo "CHANGED ✗"
PYTHONPATH=engine/src python3 -m cella.mcp_server --help >/dev/null 2>&1 && echo "cella MCP ✓" || echo "cella MCP ✗"
```

Expected: `GATE SET UNCHANGED ✓` and `cella MCP ✓`.

- [ ] **Step 4: The "float litmus" sanity read (spec §10 success criterion 3)**

Confirm the mechanism exists: `C-003`-style exactness rule in `STATE/CONSTRAINTS.md` carries a `not-scope` that explicitly frees research-side numeric work. (This is a read, not a command — the exactness constraint may be authored during interactive population; if RESULTS/DEFINITIONS are still pending, verify at least that `CONSTRAINTS.md` demonstrates the `not-scope` pattern via C-001..C-003.)

```bash
cd "/home/wlloyd/Cella Framework"
grep -A1 "^not-scope:" STATE/CONSTRAINTS.md | head
```

Expected: `not-scope` lines that carve out exploratory/research use — the anti-over-pruning surface is present.

- [ ] **Step 5: Commit**

```bash
cd "/home/wlloyd/Cella Framework"
git add -A
git commit -m "reorg(phase 5): project instructions (boot/openness/derivation/close protocol)

$(printf 'Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_016rVCVapxwgHqwKmyeKDTt8')"
```

---

## Deferred (not in this plan — interactive follow-on)

- **Canon population (spec §8 Phase 4, full):** migrating individual load-bearing results/definitions from `reports/`, `research/verification/`, and the archived lead docs into `RESULTS.md`/`DEFINITIONS.md`, each ratified by the maintainer. Cannot be scripted — it is per-claim math review. The scaffolding (Task 5) makes this a fill-in-the-schema exercise.
- **MCP read-only state layer (spec §9):** `current_state()`/`lookup_result(id)` as thin views over `STATE/` files, only after the ledger format proves out in real sessions.
- **Style-law linter + CI certificate-path check (spec §9).**

## Self-review notes

- **Spec coverage:** layout §3 → Tasks 2–4; canon schemas §4 → Task 5; style law §5 → Task 5 Step 7; session protocol §6 + derivation §7 → Task 6 Step 1; migration §8 phases 1–3 → Tasks 2–4, phase 4-scaffold → Task 5, phase 5 → Task 6; success criteria §10 → Task 6 Steps 2–4. Full canon *population* (§8 phase 4 interactive) is explicitly deferred, not dropped.
- **The three real functional couplings** (DBP gate path+depth, hostile `--output`, `.mcp.json`) each have a dedicated fix step with before/after code and a targeted verify.
- **No-regression** is enforced by a captured baseline (Task 1) diffed after every phase, tolerating pre-existing open gates.
