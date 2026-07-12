-- Exact equivalence gate for m2-even-contact-delta-slice-a-v1.
-- Execution and verification live outside Pathfinder core.

load "/home/wlloyd/Cella Framework/docs/files/horizon_wreath_inertia_model.m2";

sliceA = ideal(N1-4, N2-8, N3-12, N4-20);

baseline = trim eliminate(
    saturate(Ceven + IZ + sliceA, ideal(M)),
    sheetVars
    );

-- The recognizer's exact structural witnesses.
assert((delta + 16*J^2) % Ceven == 0);

structuralUpstairs = ideal(
    N1-4, N2-8, N3-12, N4-20,
    u,
    w1-4, w2-8, w3-12, w4-20,
    M-11,
    J^2
    );
assert(trim(Ceven + IZ + sliceA) == trim structuralUpstairs);

structuralBase = ideal(N1-4, N2-8, N3-12, N4-20, M-11, J^2);
assert(baseline == structuralBase);

print "GATE PATHFINDER M2 EVEN CONTACT EQUIVALENCE: CLOSED";
