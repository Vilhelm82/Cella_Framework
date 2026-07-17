# R3 AC-fold hostile fixture precommitment

**Status:** frozen before the R3 implementation comparison

The independent lossless two-bus AC-fold realization is to be tested at

\[
(P,Q,X,E)=(1,0,1,2).
\]

The implementation has not been given a decimal target.  The prediction is
fixed from the native equation alone:

\[
v^2-4v+1=0,
\qquad
\Delta=12,
\qquad
v_{\rm high}=2+\sqrt3\in(3,4),
\qquad
v_{\rm low}=2-\sqrt3\in(0,1).
\]

The sealed comparison must additionally show:

1. both isolating intervals have rational endpoints and are disjoint;
2. one positive discriminant loop swaps the two sheets and two loops act as
   the identity;
3. route reversal negates winding and inverts the native morphism;
4. mutation of a parameter, selected sheet, winding, source digest, or root
   interval invalidates replay; and
5. the R3 verifier imports no CCE-5, CCE-7, CCE-8, DBP-native, or horizon
   executor as an oracle.

The fixture tests a voltage-sheet prediction that is not an axiom of the
selected-skeleton adapter.  Its exact result may be compared only after the
native realization and verifier are sealed.
