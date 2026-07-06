# Reference_Material — currency banner (read before citing anything here)

**Standing rule (README rule 3 / BOOT mechanism section):** everything in this folder
is origin-program material. Statuses inside these documents — "proven", "certified",
"[EVAL]", "standing", "closed" — are **claims, never evidence**. Nothing here bears
load in Cella until re-proven in-repo (`verification/`, fresh code, exact ℚ,
byte-stable ×2). This folder exists to name questions and retrodiction targets, not
truths.

**Tracking policy:** the folder's contents are deliberately untracked (`.gitignore`);
only this banner travels with the repo. The canonical record never carries origin
artifacts — zero-import hygiene. If a document here is ever needed as a repo artifact,
that is an introduction from previous work and takes an ADMISSIONS record first.

## Substrate warning

`DBP STANDING RESULTS.md` marks its own certification substrates. Note carefully:
Part IV (the depth theorem), Parts V.1–V.3 (the arithmetic track), and the n=4
two-state witness (I.6, CALC-30) are **[CONTAINER]** — ephemeral scripts, never
persisted. For these there is no artifact to re-run anywhere: re-verification means
re-derivation from scratch. The dimension threshold (Part III, CALC-26/27) has no
in-repo certificate either.

The two R&D briefs (`DBP_RnD_Directions_*.md`) grade their priority boards in this
dashboard's currency ("done", "settled", "retired"). Read them for questions and
campaign shapes only; their status labels have zero evidentiary weight here.

## Known error (caught 2026-07-06 against RC-1)

`DBP_RnD_Directions_Exact_Role_Channel_Geometry.md` claims for the keystone:

```
doc:   (kappa_c, kappa_s, kappa_int) = (-1/49, +1/49, -3/49)
       "pure channels cancel; the surviving curvature is interaction curvature"
```

The in-repo certificate contradicts the labeling:

```
RC-1 (verification/recert_transport_law.py, d370daae, re-run clean 2026-07-06):
       (kappa_c, kappa_s, kappa_int) = (-1/49, -3/49, +1/49)
```

Same multiset, permuted labels. Under the certified naming, coupling + interaction
cancel and the **self** channel carries −3/49; the interaction channel is the
sign-carrying +1/49 (BOOT's "sign-carrying interaction channel"). The doc's narrative
sentence does not survive the pin. Any quotation of the keystone triple into Cella
uses RC-1's labels.

## Source-of-truth order

The dashboard's internal order ("persistent evals > dashboard > calc log") is the old
program's. Here the order is: **in-repo certificates > everything external, full stop.**
