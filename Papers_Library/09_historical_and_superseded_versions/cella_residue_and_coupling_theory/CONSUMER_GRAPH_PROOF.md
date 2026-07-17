# CONSUMER GRAPH PROOF — which of the four probes actually have a live src consumer
# Generated 2026-06-18 by ORPHAN-0003 dossier builder. Reproduce with the grep commands shown.

## Method
For each probe module, search src/lloyd_v4/ for imports/references OUTSIDE its own file
and outside the observers/__init__.py re-export. A hit in src/ = a live src consumer.

    for mod in directional_alpha_probe scalar_alpha_jet_bundle singular_alpha_jet_bundle sweep_signature_probe; do
      grep -rln "$mod" --include="*.py" src/lloyd_v4 | grep -v __pycache__ \
        | grep -v "observers/$mod.py" | grep -v "observers/__init__.py"
    done

## Result (live, regenerated at dossier-build time)

### directional_alpha_probe
  consumer: src/lloyd_v4/evals/difference_tower/make_prereg_b.py
  consumer: src/lloyd_v4/evals/difference_tower/run_stage_b.py
  consumer: src/lloyd_v4/observers/scalar_alpha_jet_bundle.py
  consumer: src/lloyd_v4/observers/singular_alpha_jet_bundle.py

### scalar_alpha_jet_bundle
  TRUE ORPHAN — no src consumer (only tests reference it).

### singular_alpha_jet_bundle
  TRUE ORPHAN — no src consumer (only tests reference it).

### sweep_signature_probe
  consumer: src/lloyd_v4/observers/directional_alpha_probe.py

## Interpretation
- directional_alpha_probe: NOT an orphan. Live consumer = evals/difference_tower/run_stage_b.py + make_prereg_b.py
  (the HR134 difference-tower Cella instrument; live tests test_dt_*; frozen results results/difference_tower/).
  Also imported by both jet bundles (which delegate to it) and imports sweep_signature_probe as companion.
- sweep_signature_probe: NOT an orphan. Consumed by directional_alpha_probe (companion, Task036/HR102),
  hence transitively reachable in the live difference-tower chain. Ledger line 94: 'in production'.
- scalar_alpha_jet_bundle: TRUE ORPHAN (no src consumer; delegates to directional; only tests reference it).
- singular_alpha_jet_bundle: TRUE ORPHAN (no src consumer; delegates to directional; only tests reference it).

## Prune-exemption check (regenerated)
Deliberate-prune commit 6a9f64b touched observers/ ?
ANSWER: NO — 0 observers/ files in commit 6a9f64b (the 102-module/640-test prune).
These four probes were NEVER in the deliberate prune; they survived by being substrate (observers/), not eval.
