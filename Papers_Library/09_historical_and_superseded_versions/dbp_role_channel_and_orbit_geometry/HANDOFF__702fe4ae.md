# HANDOFF — GEM-0001 (Theorem 8.1 → exact-ℚ chase). For a fresh model, zero prior context.

You are picking up a **research lead**, not a finished result. The project is a typed
finite-precision math engine; a side-line called **Cella** does *exact* accounting in
rational arithmetic (ℚ) — "value + residue == TRUE in ℚ, exactly." There is a proposal
("cella-as-trunk") to re-found the engine on Cella; it is **not landed** and is fenced.

**The lead:** an external math result, **Theorem 8.1** (Lloyd's "DBP framework"), says any
role-symmetric function `φ` of a coupling `(D,S,P)` splits **uniquely** as `φ = φ_K + φ_sym`
(a coupling-structural part + a value-symmetric part), **with no third category**. The bet:
Cella can sharpen this from float to **exact ℚ**, lift it off floats, and supply a
completeness bound on coupling invariants (and show "holonomy" is one of them). It is named
the single highest-value chase to start the re-founding.

**Minimum you need to know:**
1. Read `FINDING.md` here — it is self-contained. Then `evidence/probe.py`.
2. `evidence/probe.py` is stdlib-only (Python `fractions`). Run it:
   `python3 evidence/probe.py` — you should see **ALL PASS: True** (compare to
   `evidence/probe_run_log.txt`). It demonstrates, in exact ℚ: (A) frame-dependence,
   (B) the holonomy K1-null/K3-sharp, (C) the `φ_K + φ_sym` split.
3. **The one trap that voids the chase:** read `evidence/WORKING_SET_hot_finding_excerpt.md`.
   The K_G object is actually **THREE channels** `K_G = κ_c ⊕ κ_s ⊕ κ_int`, but the draft
   brief (`evidence/CAMPAIGN_BRIEF_theorem_8_1_exact_DRAFT.md`) is written **single-channel**
   and is flagged **DO NOT FREEZE**. Do not execute that brief as-is.
4. Nothing here is canonical. No file edits, no "campaign," no freeze without the owner (Will).

**First action:** run `evidence/probe.py` to confirm ALL PASS, then read `FINDING.md` §6 and §7.
The real first experiment (§7) needs **Will's κ_c/κ_s/κ_int decomposition formula** (not in
this folder) to compute the three channels on the surface `x₁²+x₁x₂+x₃²−3` at `(1,1,1)`
(where K_G = −3/49). Until that formula exists, the chase cannot correctly begin — flag this
dependency first, do not improvise a formula.
