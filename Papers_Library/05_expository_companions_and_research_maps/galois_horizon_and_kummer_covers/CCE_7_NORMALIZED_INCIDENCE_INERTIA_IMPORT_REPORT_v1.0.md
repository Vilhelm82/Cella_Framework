# CCE-7 normalized-incidence inertia import

## Outcome

`PROMOTED`: the normalized-incidence definition, true relative branch ideal,
generic inertia catalogue, and stored realization-poset theorem were already
present in the Paper-IV publication package and are now source-locked behind
a production certificate.

`ACTIVE_PROOF`: exact complex loop representatives, braid execution,
refinement independence, and compatibility with the CCE-5 route groupoid.

## Imported theorem

The normalized incidence cover is

\[
w_i^2-u-N_i^2=0\quad(1\leq i\leq4),
\qquad
\sum_iw_i=4M.
\]

Its relative Jacobian is exactly (8e_3(w)).  Consequently the projected
quintic discriminant is not accepted as the ramification divisor: at equal
squared charges it contains extra squared factors produced by unramified
sheet crossings.

Away from residue characteristic two, a Kummer inertia element flips exactly
the square roots having odd valuation.  The certified generic catalogue
contains simple mass (C_2), even/odd contact (C_2), rotating-difference
(C_2), reciprocal-sub-balance colored (C_4), and the explicitly
unramified `J=0`, generic weighted-infinity, and equal-squared-charge strata.

The stored Macaulay2 realization theorem gives the incidence degrees
(48,2,64,192,6,8,24) for the named codimension-one through
codimension-three strata.  The live model replays its core codimension and
Jacobian assertions under Macaulay2 1.25.11.  Historical stage outputs and
the theorem source are digest-bound; the producer's prose verdict is not
trusted by itself.

## Production boundary

`engine/src/cella/continuation/cce7_inertia.py` imports this exact theorem
surface and names the remaining route obligation.  It does not pretend that
an inertia permutation is already an executed geometric loop.  The
10-assertion independent gate rejects Jacobian and inertia tampering.

This changes the post-8 work estimate materially: the complex CCE-7 lane is
an adapter-and-braid campaign over an existing normalized cover, not a fresh
normalization or discriminant-classification proof.
