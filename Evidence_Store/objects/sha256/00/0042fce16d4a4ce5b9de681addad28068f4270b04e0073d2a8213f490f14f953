# Independent R3 realization: lossless two-bus AC fold

**Outcome:** `PROMOTED` for the native realization and its own selected
skeleton image; three-way coherence with the DBP arms remains `ACTIVE_PROOF`.

## 1. Native cover

For exact rational parameters (P,Q,X,E), with (X,E>0), define

\[
F(v)=v^2+(2QX-E^2)v+X^2(P^2+Q^2)
\]

and

\[
\Delta=E^4-4E^2QX-4P^2X^2.
\]

On the strict real chamber (Delta>0), the normalized cover has two sheets

\[
v_\pm=\frac{E^2-2QX\pm\sqrt\Delta}{2}.
\]

Objects are exact parameter tuples with a selected `high` or `low` sheet.
A native morphism has an integer winding about the discriminant.  Its target
sheet is exchanged exactly when the winding is odd.  Composition adds
winding; reversal negates it.  This is a genuine groupoid before any adapter
is introduced.

The physical section is the high-voltage sheet selected at no load:
((P,Q)=(0,0)) gives (v=E^2,0).  The wall (Delta=0) is a square-root
saddle-node fold.  The current release certifies the regular chamber and
returns a typed refusal on or beyond this wall; it does not fake wall
crossing as regular continuation.

## 2. Exact certificate

The certificate binds the native equation, exact discriminant, rational
isolating intervals for both algebraic roots, selected sheet, winding,
source and target objects, (C_2) action, skeleton image, theorem IDs,
dependency ledger, and deterministic digest.  Replay recomputes every field
and rejects parameter, route, sheet, interval, discriminant, or dependency
mutation.

The precommitted hostile fixture

\[
(P,Q,X,E)=(1,0,1,2)
\]

produces (F(v)=v^2-4v+1), (Delta=12), and independently isolates
(v_{\rm high}=2+\sqrt3\) in ((3,4)) and
(v_{\rm low}=2-\sqrt3\) in ((0,1)).  One loop swaps them; two loops fix
them.  All 29 native, functorial, hostile, and oracle-separation assertions
pass.

## 3. Reduction and exact functor properties

The reduction retains the selected discriminant divisor, strict-chamber
stratum, sheet, rational quadratic coefficient domain with chosen real
embedding, orientation, and local (C_2) parity.  On morphisms it is

\[
\mathbb Z\longrightarrow C_2,\qquad k\longmapsto k\bmod2.
\]

It preserves identities and composition.  Componentwise:

| property | result |
| --- | --- |
| well-defined | `PROMOTED` |
| full onto the native (C_2) parity image | `PROMOTED` |
| faithful | `REFUTED`; kernel (2\mathbb Z) |
| essentially surjective onto its declared two-sheet image | `PROMOTED` |
| full-carrier equivalence to a DBP arm | not claimed |

The loss of even winding is explicit rather than smuggled into a false
equivalence.

## 4. Independence audit

- The source equation and no-load voltage selection are native AC
  power-flow data, not a base change, quotient, isogeny, or reparameterized
  DBP equation.
- The (C_2) wall and monodromy are derived from this quadratic
  discriminant.
- The implementation imports no CCE-5, CCE-7, CCE-8, native-period, or
  horizon executor, and its verifier calls none as an oracle.
- The precommitted voltage-root interval is a native prediction not inserted
  into the skeleton adapter.

This closes the construction and separation portion of R3.  It does not by
itself prove a three-way natural isomorphism: the two DBP reduction functors
have not yet been constructed on a common object domain.  The exact next
object is a pair of DBP-arm functors into the same typed skeleton followed by
componentwise coherence diagrams.

Production source: `engine/src/cella/continuation/r3_ac_fold.py` and
`engine/src/cella/continuation/selected_skeleton.py`.  Gate:
`engine/tests/gate_continuation_r3_ac_fold.py`.
