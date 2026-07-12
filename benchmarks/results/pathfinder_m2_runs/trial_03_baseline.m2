-- Historical generic baseline for m2-even-contact-delta-slice-a-v1.
load "/home/wlloyd/Cella Framework/docs/files/horizon_wreath_inertia_model.m2";
sliceA = ideal(N1-4, N2-8, N3-12, N4-20);
baseline = trim eliminate(
    saturate(Ceven + IZ + sliceA, ideal(M)),
    sheetVars
    );
print "PATHFINDER_M2_BASELINE_BEGIN";
print toString gens baseline;
print "PATHFINDER_M2_BASELINE_END";
