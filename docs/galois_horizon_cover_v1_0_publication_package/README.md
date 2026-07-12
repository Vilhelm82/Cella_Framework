# Galois Theory of the Horizon Cover — v1.0 package

Date: 2026-07-11

## Primary deliverables

- `galois_horizon_cover_v1_0.tex` — integrated LaTeX source.
- `galois_horizon_cover_v1_0.pdf` — verified 14-page build.

Build command:

```sh
pdflatex -interaction=nonstopmode -halt-on-error galois_horizon_cover_v1_0.tex
pdflatex -interaction=nonstopmode -halt-on-error galois_horizon_cover_v1_0.tex
```

Final build status: no undefined references, LaTeX warnings, overfull boxes, or
fatal errors. All pages were rendered to PNG and visually inspected.

## Integrated mathematical results

1. The four-charge mass fiber is a quintic with generic group `S_5`.
2. The static ordered-horizon field has degree 20.
3. Its normal closure has group `C_2^2 wr S_5`, order 122880.
4. The generic rotating ordered-horizon field still has degree 20 and the same
   abstract normal-closure group.
5. The augmented axial–horizon field has degree 40 and normal closure
   `C_2^3 wr S_5`, order 3932160.
6. The tame inertia classes are determined by colored cycle data and parity
   rows of divisorial valuations.
7. The Macaulay2 realization calculation verifies every named generic-open
   stratum; the rotating difference ideal is prime, reduced, and irreducible
   over `QQ` on the incidence cover.

## Audit trail

- `supporting_reports/` contains the proof dossiers used to build the new
  theorem sections.
- `certificates/horizon_wreath_inertia_model.m2` is the master Macaulay2 model.
- `certificates/m2_out_2026-07-10/` contains the workflow scripts, verbatim raw
  outputs, and the realization-poset run report.

SHA-256:

```text
777daf7b60d337709587606f0974f8d4c8ff9c79473b609aadd54827223613ce  galois_horizon_cover_v1_0.tex
c0a6c24cad8b33b2b7fbae12ce48fae4f436e93a75b1a2cd8b78d42b750429fe  galois_horizon_cover_v1_0.pdf
d7940c05f9021b211fad4bb0546504ee91b7e9135c28ef1ba9fcd6a1d3199d46  certificates/horizon_wreath_inertia_model.m2
```

## Scope fences

- `J` is treated generically/transcendentally in the rotating theorems.
- At `J=0`, the augmented Kummer algebra has a split special fiber; one must
  select a branch-compatible component before identifying the static crown.
- “Prime and irreducible” for the difference ideal is the exact Macaulay2
  result over `QQ`; geometric irreducibility after arbitrary base extension is
  not claimed.
- The paper is technically compiled and internally certificate-backed, but a
  specialist counter-audit and final prior-art review remain advisable before
  submission.
