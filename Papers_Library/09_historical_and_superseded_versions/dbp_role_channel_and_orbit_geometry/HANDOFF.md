# HANDOFF — GEM-0005 (Theorem 8.1 Cella probe)

You are picking up a small, self-contained Python probe that hardens an external math result
("Theorem 8.1 — Invariant Preservation under Role Transposition") from floating-point to **exact
rational arithmetic (ℚ)**, using only the Python standard library.

**Minimum you need to know:**
1. `evidence/probe.py` is stdlib-only (`fractions.Fraction`, `itertools.permutations`). Run it with
   `python3 evidence/probe.py`. Expected: **ALL PASS** (see `evidence/probe_run_output.txt`).
2. It proves three things exactly in ℚ: (A) a role-labelled quantity `φ` is frame-dependent while the
   symmetric polynomials of `{D,S,P}` are invariant; (B) a "holonomy" = mixed second difference of a
   coupling is a hard 0 for additive `P=D+S`, exactly `h·k` for bilinear `P=D·S`, and a matching
   closed form for `P=D·S²`; (C) any role-invariant `φ` splits uniquely as `φ_K + φ_sym` (symmetric
   + structural), with no third category.
3. **What it deliberately does NOT do:** it refuses to compute the Gaussian curvature `K_G` (its
   docstring says this avoids "confabulating the K_G formula") and it flags the theorem's
   "exhaustiveness" step as a logical lemma a probe cannot discharge. This restraint is the point —
   it is the honest counterpart of a sibling brief (`evidence/CAMPAIGN_BRIEF_theorem_8_1_exact_DRAFT.md`)
   that was drafted in a flawed "single-channel" frame and is marked **DO NOT FREEZE**.
4. The live frontier (see `evidence/WORKING_SET_hot_finding_excerpt.md`): the real `K_G` is **three
   channels** `K_G = κ_c + κ_s + κ_int`; on the keystone surface `x₁²+x₁x₂+x₃²−3` at `(1,1,1)` the
   exact value is `K_G = −3/49` (κ_c=−1/49, κ_s=+1/49 cancel, κ_int=−3/49 carries it).
5. This is a **scratch probe — not canonical, no warrant**. As a result it is direction/scaffolding,
   not a graded finding.

**First action:** run `python3 evidence/probe.py`, confirm ALL PASS, then read the docstring (lines
1-28) to see exactly which legs are hardened vs fenced. The single highest-value next experiment is to
add a part (D) that computes `K_G` of the keystone surface natively in ℚ from a mixed-partial tensor
and checks it equals `−3/49` (do not import any external curvature library). Success = `−3/49`
reproduced natively; failure = the curvature leg needs the dedicated Arm-M instrument, not a probe.
