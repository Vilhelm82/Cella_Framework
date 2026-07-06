# POSITIONING — what puts Cella in its own category

**Status:** PROPOSED (strategy; Will ratifies). Fresh authorship — prior work cited as
reference only, per the admission rule. **Discipline: every category claim below that
sits at a boundary carries a prior-art obligation. Prior art is an oracle, not a gate —
but no claim ships publicly before its sweep.**

## The three structural weaknesses of incumbent tools

Existing FDD stacks (single-channel thresholds, PCA/T²/SPE, DPCA, ICA, one-class SVM,
isolation forest, autoencoder residuals, spectral/envelope methods) share:

1. **No invariance guarantees.** Features shift under recalibration, unit changes, and
   preprocessing; normalization is ad hoc. None ships a theorem about what cannot move.
2. **No derived limitations.** What the method cannot detect is discovered in
   deployment. None can state its own blindness set in advance.
3. **Scores, not accounts.** A number is emitted; what was discarded to produce it is
   gone. Determinism and reproducibility are aspirations, not constructions.

## The category claim

**Sensors that come with theorems, on a substrate where every verdict is
exact-or-typed-refusal with a reconstructive account.**

Per sensor, shipped as part of the product: its invariance group (what provably cannot
move it), its blindness set (what it provably cannot see), and its completeness scope
(when the sensor set is provably sufficient — and when it provably is not). Per verdict:
the two-register certificate (CERTIFICATE_SCHEMA.md). Plus the meta-capability no
incumbent has: the **deficit audit** — hand the engine any domain's (data space, honest
symmetry group, standard summary) and it certifies what that summary is blind to and
constructs the completion.

## What we do NOT claim

- Not "beats deep models on ROC." On large noisy corpora they will often win on AUC.
  The position is: certified unique detections (the Venn quadrant), the audit
  capability, combined-AUC augmentation, and a limitation disclosure that is *derived*.
- Not "floats are banned from the product." Floats are banned from **verdict paths**;
  ingestion and display handle them through typed observation maps.
- Not "detection is exact." Computation is exact-or-refused; detection on noisy data is
  statistical and says so. One certificate never mixes the two.

## Nearest competitor concepts — named, with sweep obligations

| Adjacent concept | Where it lives | Honest differentiator | Sweep status |
|---|---|---|---|
| Structured residuals / parity relations | Classical FDI (Gertler; Frank; analytical redundancy) | They *design* fault-insensitivity into residuals of a **known plant model**. We *derive* blindness/completeness theorems for **fitted surfaces**, model-free, exactly certified. Closest concept on the board. | **OWED before any public category claim** |
| Interval / ball arithmetic, error-free transformations | Validated numerics (Rump/Ogita/Oishi; Arb) | The arithmetic is classical (KNOWN). The contribution candidate is the account discipline across a diagnostic pipeline: reconstruction (not enclosure) where possible, typed refusal where not, certificates at every exit. | OWED at claim boundary |
| Physics-based residual monitoring | Model-based FDD | Direct competitor to the equation-mode engine; our edge is exactness + invariance + no-model surface fitting mode. | OWED |
| Information geometry / thermodynamic geometry (GTD) | Mathematical physics | Different object: they study metrics on state spaces; we diagnose constraint-surface coupling with certified invariants. The double-reading of thermodynamic surfaces is our own bridge result. | partial (two-readings work) |
| Metamorphic testing | Software validation | We import the technique; our addition is that key relations are theorems (identity checks, not statistical checks). | n/a (method, not claim) |
| Contribution plots / fault isolation in PCA | Process monitoring | Known to smear across correlated variables. Support-based triangle localization has *proven* support inclusion. | OWED |

Precedent for the discipline: an earlier structure-law claim was correctly reclassified
KNOWN-adjacent after a sweep hit the minimum-rank (mr0) literature. That reclassification
is the behaviour that makes the remaining claims credible.

## The discovery loop (why this engine can surface real novelty)

The pattern behind every strong result to date: **derived impossibility + constructive
completion** (a threshold theorem plus the invariant that crosses it; a refuted law plus
the corrected invariant; a certified blindness plus its completion). The engine is
designed to mass-produce that pattern:

```
pick a domain's standard summary
→ certify its deficit (what the symmetry group says it must miss)
→ construct the completion invariants
→ test whether the completion sees something physically real
→ certificate either way
```

Run on physics domains (thermodynamic geometry first, coupled-system spectra second),
this loop is the honest mechanism for discovering new mathematics and physics with the
same machinery that diagnoses bearings. Discovery and diagnostics are the same operation
here: finding what the standard account provably cannot see, and building the thing
that sees it.
