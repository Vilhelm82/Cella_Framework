export const meta = {
  name: 'phase2-foundations',
  description: 'Build, run, and adversarially verify the three V4 Phase 2 mathematical-foundations tasks (precision-scaling boundary, subnormal topology, nested-window bias) in scratch/, then synthesize agent_sandbox_results.json + sandbox_summary_report.md. Eval-layer only, research-grade.',
  phases: [
    { title: 'Build', detail: 'one agent per task writes + runs its scratch harness' },
    { title: 'Verify', detail: 'two diverse-lens skeptics adversarially check each task' },
    { title: 'Synthesize', detail: 'merge into agent_sandbox_results.json + sandbox_summary_report.md' },
  ],
}

const SHARED = `You are an eval-layer research agent in the Lloyd V4 engine. Repo root (your cwd): /home/william_lloydlt/projects/V4/Lloyd_Engine_V4

STRICT DISCIPLINE (project CLAUDE.md + task spec):
- Eval-layer ONLY. Write ALL code and outputs under scratch/. You may IMPORT existing substrate/eval modules read-only to reuse them, but NEVER edit or promote code into src/lloyd_v4/{core,primitives,projection,metrology,branch,observers}.
- Instruments (numpy, decimal, mpmath, fractions.Fraction) are allowed in scratch as MEASUREMENT APPARATUS only; never as substrate. Do not hardcode mathematical constants as substrate truth.
- Zero-axiom tolerance: every numerical claim must be backed by reproducible IEEE 754 raw hex traces or exact mathematical reduction (fractions.Fraction or mpmath as the exact reference). No assumed float behavior.
- Observation-only: any invariant you find is a DESCRIPTIVE, research-grade observation until derived from IEEE 754 axioms. No substrate-promotion claims.
- Byte-stable outputs: after producing a JSON artifact, RE-RUN the harness and diff; report whether byte-identical. If not, make it deterministic (sorted keys, no timestamps, fixed seeds).
- Before importing any reused module, READ it to confirm real signatures (the asset map below is a guide, not authoritative).

REUSABLE ASSETS (verify by reading before use):
- Four fixtures + multi-precision eval: src/lloyd_v4/evals/precision/precision_bound_fixtures.py (canonical_grid, four_form_values, sterbenz_region, precision_battery_for_fixture)
- Theorem 3 precision-scaling fit (Task 017c): src/lloyd_v4/evals/precision/multi_precision_campaign.py (run_precision_campaign); precision/linear_fit.py (fit_linear, bootstrap_ci); precision/unit_roundoff.py (u_p, platform_float128_report, active_binary_precisions)
- Nested-window alpha machinery (Task 023b, ALREADY EXISTS): src/lloyd_v4/observers/directional_alpha_probe.py (_nested_window_evidence, AlphaWindowFit, alpha_stability_status, K_DRIFT, materiality)
- Lattice geometry: src/lloyd_v4/primitives/typed_ulp.py (typed_ulp(x, precision=...))
- Subnormal-safe exact arithmetic pattern: scratch/bacl_subnormal_audit.py (fractions.Fraction, subnormal generators)
- c2 chain reference: scratch/c2_lattice_substrate_derivation.py, scratch/c2_lattice_sharpness_audit.py

INSTRUMENT CAVEAT (verified on this machine): numpy.float128 is 80-bit x86 EXTENDED precision (eps ~ 1.08e-19, ~64-bit mantissa), NOT IEEE binary128. Treat the float128 tier as caveated; use a decimal/mpmath tier as the true high-precision anchor.

Your final message IS the structured return (schema-validated). Do the work, then return the structured object.
`;

const BUILD_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    task_id: { type: 'string' },
    ran_successfully: { type: 'boolean' },
    harness_path: { type: 'string' },
    artifact_path: { type: 'string' },
    byte_stable: { type: 'boolean' },
    headline_findings: { type: 'array', items: { type: 'string' } },
    burden_gates: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { gate: { type: 'string' }, met: { type: 'boolean' }, evidence: { type: 'string' } }, required: ['gate', 'met', 'evidence'] } },
    key_numbers: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { name: { type: 'string' }, value: { type: 'string' }, note: { type: 'string' } }, required: ['name', 'value'] } },
    caveats: { type: 'array', items: { type: 'string' } },
  },
  required: ['task_id', 'ran_successfully', 'harness_path', 'artifact_path', 'byte_stable', 'headline_findings', 'burden_gates'],
};

const VERIFY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    task_id: { type: 'string' },
    lens: { type: 'string' },
    verdict: { type: 'string', enum: ['confirmed', 'partially_confirmed', 'refuted', 'uncertain'] },
    refutation_attempts: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { claim: { type: 'string' }, method: { type: 'string' }, result: { type: 'string' } }, required: ['claim', 'method', 'result'] } },
    byte_stability_independently_checked: { type: 'boolean' },
    instrument_artifact_risk: { type: 'string' },
    recommended_caveats: { type: 'array', items: { type: 'string' } },
  },
  required: ['task_id', 'lens', 'verdict', 'refutation_attempts'],
};

const SYNTH_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    results_json_path: { type: 'string' },
    report_path: { type: 'string' },
    executive_summary: { type: 'string' },
    failed_gates: { type: 'array', items: { type: 'string' } },
    verifier_refutations: { type: 'array', items: { type: 'string' } },
  },
  required: ['results_json_path', 'report_path', 'executive_summary'],
};

const VERIFY_PREAMBLE = `You are an ADVERSARIAL verifier. Do NOT trust the build agent's claims. Independently re-derive and try to REFUTE. Read the harness scratch file and its JSON artifact, and run your own python checks. Default to skepticism; if uncertain, say uncertain.\n\n`;

const TASKS = [
  {
    id: 'A',
    name: 'precision-scaling-boundary',
    buildPrompt: `=== YOUR TASK: Phase 2 Task A — Precision-Scaling Separation Manifold Boundary Test ===

Objective: The linear precision-scaling model C_{p,k} = a + u_p * b_k (Theorem 3 / Task 017c) holds with R^2 = 1.0 in the regular region. Locate the EXACT boundary where this collapses and isolate the dominating artifact.

Steps:
1. Build a stress-test grid for the four fixtures (Schwarzschild f=1-2/r, SR f=1-beta^2, pure_algebraic f=1-x, cube_root f=1-x n=3) that intentionally drives operands OUT of the regular region and THROUGH the Sterbenz boundary (Schw r=4.0, SR beta=1/sqrt(2), PA x=0.5, cbrt x=0.5). March the operand toward the singularity (small f) at fine resolution so R^2(f) is a continuous curve. Reuse precision_bound_fixtures.canonical_grid and extend it.
2. For each cell, compute C_{p,k} across the precision ladder float32, float64, float128 (CAVEAT: 80-bit), and a decimal/mpmath true-high-precision anchor, via four_form_values + unit_roundoff.u_p; fit with linear_fit.fit_linear; record R^2 per f.
3. Find the exact f threshold where R^2 first departs from 1.0 (bracket it). At that cell, do an EXACT-arithmetic decomposition (fractions.Fraction or mpmath) of C_{p,k} into leading + sub-leading contributions to NAME the dominating term. Candidates: u_p^2 cross-term emergence; catastrophic cancellation in R^n - 1 + x_term; OR the decimal/float128 tier hitting its own floor. You MUST rule out the last (instrument) case, else the "boundary" is an artifact, not a substrate boundary.

Burden of proof (report each as a burden_gate): (i) exact f threshold where R^2 diverges from 1.0; (ii) the dominating term, shown dominant by exact decomposition; (iii) confirmed NOT merely an instrument-tier artifact.

Write harness to scratch/phase2A_precision_scaling_boundary.py and the JSON trace of exact float values at the collapse boundary to scratch/phase2A_boundary_trace.json (deterministic, sorted keys). Run it, then re-run and diff for byte-stability.`,
    lenses: [
      { label: 'A:instrument-artifact', prompt: `LENS: instrument-artifact. Determine whether the reported R^2-departure threshold is a genuine substrate boundary or an artifact of (a) the 80-bit float128 tier and/or (b) the decimal/mpmath anchor's own precision floor. Re-run the boundary measurement with the float128 tier REMOVED, and again with the decimal anchor precision raised substantially. If the threshold MOVES when you change instrument tiers, it is an instrument artifact — return refuted or partially_confirmed. Independently confirm byte-stability.` },
      { label: 'A:exact-dominance', prompt: `LENS: exact-decomposition dominance. Independently re-derive, via fractions.Fraction or mpmath, the named dominating term at the threshold cell and confirm it actually dominates the residual versus the alternative candidates (u_p^2 cross-term, catastrophic cancellation in R^n-1+x_term). Try to show a DIFFERENT term dominates. Report confirmed only if the named term is exact-arithmetically dominant.` },
    ],
  },
  {
    id: 'B',
    name: 'subnormal-topology',
    buildPrompt: `=== YOUR TASK: Phase 2 Task B — Subnormal Topology Audit (f < 2^-1022) ===

Map the breakdown of the c2 integer-lattice / Conjecture C structure when operands cross into the subnormal regime (uniform spacing 2^-1074 instead of binade-proportional).

THE USER HAS DECIDED TO DO BOTH OF THE FOLLOWING:
(a) SUBSTANTIVE AUDIT — decoupled bare-radical lattice test. The literal chain f = 1 - x_term CANNOT reach subnormals in float64 (x_term would need to be within 2^-1022 of 1.0, but the nearest float to 1 is 1 +/- 2^-53). So instead pick subnormal f DIRECTLY in [2^-1074, 2^-1022) and test the lattice property on the bare radical: R = f^(1/n), V = R^n, residual = V - f measured against ulp(f) = 2^-1074, with an EXACT fractions.Fraction reference (follow scratch/bacl_subnormal_audit.py). Do n=2 (sqrt, IEEE correctly-rounded) and n=3 (cbrt — CAVEAT: cbrt is NOT IEEE-mandated correctly-rounded; cross-check numpy.cbrt vs mpmath and report divergence).
(b) BOUNDARY NOTE — demonstrate and document the degeneracy: show numerically that f = 1 - x_term bottoms out near 2^-52 and cannot produce subnormal f in float64.

Steps:
1. Sweep subnormal f in [2^-1074, 2^-1022), log-spaced + boundary-dense near 2^-1022.
2. For n=2 and n=3, measure the residual lattice vs ulp=2^-1074 using exact Fraction. Determine: does the residual form a NEW subnormal-specific lattice, or shatter into unstructured noise?
3. Measure how the limiting log-log slope (alpha - 1) degrades as f -> 0+ in subnormals.
4. Capture raw float64 hex traces of the TRANSITION PAIRS crossing 2^-1022 (the normal->subnormal handoff), demonstrating Conjecture C breakdown.

Burden of proof (report each as a burden_gate): (i) verdict new-lattice vs noise, with exact-Fraction evidence; (ii) the (alpha-1) degradation as f->0+; (iii) hex traces of the 2^-1022-crossing pairs.

Write harness to scratch/phase2B_subnormal_topology.py and JSON (incl. hex traces) to scratch/phase2B_subnormal_trace.json (deterministic). Run, re-run, diff for byte-stability.`,
    lenses: [
      { label: 'B:exact-fraction-lattice', prompt: `LENS: exact-Fraction lattice. Independently recompute residual = V - f vs ulp=2^-1074 using fractions.Fraction for a sample of subnormal f (both n=2 and n=3) and confirm the new-lattice-vs-noise verdict. For n=3, cross-check numpy.cbrt against an mpmath correctly-rounded cbrt and report any divergence that could confound the verdict.` },
      { label: 'B:construction-and-hex', prompt: `LENS: construction-validity + hex. Independently confirm the claim that f = 1 - x_term cannot produce subnormal f in float64 (bottoms out near 2^-52). Then DECODE the reported hex traces of the 2^-1022 crossing and verify the binade-proportional -> uniform-spacing handoff is correct (ulp becomes a constant 2^-1074). Try to find an error in the hex or the boundary logic.` },
    ],
  },
  {
    id: 'C',
    name: 'nested-window-bias',
    buildPrompt: `=== YOUR TASK: Phase 2 Task C — Nested-Window Bias Harness (Task 023b Fulfillment) ===

Build a V4 typed nested-window diagnostic that separates pure algebraic branches from non-algebraic drift, so iterated-log drift is NOT misclassified as a small fractional exponent.

WHAT ALREADY EXISTS (reuse, do not rebuild): src/lloyd_v4/observers/directional_alpha_probe.py already has nested-window evidence (_nested_window_evidence, AlphaWindowFit, alpha_stability_status STABLE/UNSTABLE, K_DRIFT=2.0, materiality). READ it first. The GAP you must fill is the 3-MODEL comparison (M_A algebraic / M_L logarithmic-slow-variation / M_E essential) with an information criterion — that does NOT exist yet.

Steps:
1. Implement a nested-window processor that fits s(f) = s_inf + B * f^rho across sequential sub-windows of the h-grid (reuse the existing nested-window evidence as input where possible).
2. Implement the Automatic Stability Diagnostic: fit M_A (s converges: s_inf + B f^rho), M_L (logarithmic / slow variation), M_E (essential / iterated-log), pick the winner by AIC or BIC, and emit a TypedResult-shaped record (nested-window variance + winning IC model).
3. Define V4-NATIVE synthetic stress observables (these "Fixtures C/D/E" are NOT the four-form fixtures): Fixture C = slow algebraic drift (power law + sub-leading power correction); Fixture D = logarithmic divergence; Fixture E = iterated-log drift (the x*log(x)-style case known to recover a spurious alpha ~ 0.90). Point the harness at C, D, E.

Burden of proof (report each as a burden_gate): (i) the harness MUST classify Fixture E as non-algebraic drift, explicitly REJECTING it as a stable fractional branch; (ii) the harness MUST isolate s_inf from the finite-window bias B*f^rho in Fixture C.

Write harness to scratch/phase2C_nested_window_harness.py and the emitted TypedResult JSON to scratch/phase2C_typed_result.json (deterministic). Run, re-run, diff for byte-stability.`,
    lenses: [
      { label: 'C:false-accept', prompt: `LENS: false-accept. Independently verify the harness REJECTS Fixture E as non-algebraic (the must-pass gate). Construct one or two NEW borderline E-like observables (other iterated-log / slowly-varying forms) and check whether the harness wrongly accepts any as a stable fractional branch. Report any false-accept as a refutation.` },
      { label: 'C:overfitting-IC', prompt: `LENS: overfitting / information-criterion. Independently check the AIC/BIC comparison is not overfitting: confirm M_A wins on Fixture C and s_inf is recovered to the stated tolerance; verify the IC complexity penalty is applied correctly and the winner is robust to reasonable changes in window count / h-grid. Try to flip the winner by perturbing the window choice.` },
    ],
  },
];

phase('Build');
log('Phase 2 foundations: building + verifying 3 tasks (A precision-scaling boundary, B subnormal topology, C nested-window bias).');

const results = await pipeline(
  TASKS,
  (task) => agent(SHARED + '\n\n' + task.buildPrompt, { label: 'build:' + task.id, phase: 'Build', schema: BUILD_SCHEMA }),
  (build, task) =>
    parallel(
      task.lenses.map((lens) => () =>
        agent(
          SHARED + '\n\n' + VERIFY_PREAMBLE + 'TASK ' + task.id + ' BUILD-STAGE FINDINGS (JSON):\n' + JSON.stringify(build) + '\n\n' + lens.prompt,
          { label: lens.label, phase: 'Verify', schema: VERIFY_SCHEMA }
        )
      )
    ).then((verifies) => ({ task_id: task.id, build, verifies: verifies.filter(Boolean) }))
);

const clean = results.filter(Boolean);

phase('Synthesize');
const synthPrompt = `=== SYNTHESIS ===
You are given the build findings and adversarial-verifier verdicts for all three Phase 2 tasks (JSON below). Produce the two consolidated deliverables. Read each per-task artifact (scratch/phase2A_boundary_trace.json, scratch/phase2B_subnormal_trace.json, scratch/phase2C_typed_result.json) and harness files as needed.

1. Write scratch/agent_sandbox_results.json — a single deterministic JSON merging, for each task: the raw floating-point traces / lattice residuals / fits (embed key arrays or reference-by-path with the key arrays included), the statistical fits, and the burden-gate outcomes. Sorted keys, no timestamps.
2. Write scratch/sandbox_summary_report.md — a STRICT, zero-axiom breakdown of the mechanics discovered, with: a top header stating "RESEARCH-GRADE, pending user review; NO substrate promotion (eval-layer only)"; one section per task (A/B/C) covering the discovered mechanism, the burden-of-proof gate table (met/not-met + evidence), the adversarial-verifier verdict(s), and ALL instrument caveats (esp. float128=80-bit, cbrt non-correct-rounding); and a final "Open / not covered" section. Cite exact file paths and key numbers. Do NOT overclaim — where a verifier returned refuted/uncertain, say so plainly.

Then re-read both deliverables to confirm they were written. Return the structured object with the two paths, a 3-5 sentence executive summary, any FAILED gates, and any verifier refutations.

ALL TASK RESULTS (JSON):
` + JSON.stringify(clean);

const synth = await agent(SHARED + '\n\n' + synthPrompt, { label: 'synthesize', phase: 'Synthesize', schema: SYNTH_SCHEMA });

return { tasks: clean, synthesis: synth };
