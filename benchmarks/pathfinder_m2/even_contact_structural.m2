-- Structural route for m2-even-contact-delta-slice-a-v1.
-- This is an execution/certificate fixture outside Pathfinder core.

load "/home/wlloyd/Cella Framework/docs/files/horizon_wreath_inertia_model.m2";

sliceA = ideal(N1-4, N2-8, N3-12, N4-20);

-- Exact contact-restriction witness.
assert((delta + 16*J^2) % Ceven == 0);

-- Direct structural presentation upstairs on the slice.  Keep J^2: this is
-- a doubled scheme node, not merely its reduced support J=0.
structuralUpstairs = ideal(
    N1-4, N2-8, N3-12, N4-20,
    u,
    w1-4, w2-8, w3-12, w4-20,
    M-11,
    J^2
    );

assert(trim(Ceven + IZ + sliceA) == trim structuralUpstairs);

structuralBase = ideal(N1-4, N2-8, N3-12, N4-20, M-11, J^2);

print "PATHFINDER_M2_STRUCTURAL_BEGIN";
print toString gens structuralBase;
print "PATHFINDER_M2_STRUCTURAL_END";

