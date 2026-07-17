-- Stage 5 (workflow steps 7-8, section 8): exact rational slice N=(4,8,12,20), M,J symbolic
load "/home/wlloyd/Cella Framework/docs/horizon_wreath_inertia_model.m2";

sliceA = ideal(N1-4, N2-8, N3-12, N4-20);

reportSlice = (lbl, I) -> (
    print("=== " | lbl | " ===");
    E := trim eliminate(I + sliceA, sheetVars);
    print toString gens E;
    scan(flatten entries gens E, g -> if g != 0 then print("  factor: " | toString factor g));
    E);

-- mass branch image on the slice
branchSliceA = reportSlice("branchSliceA = eliminate(IR+sliceA, sheetVars)", IR);

-- rotating difference image on the slice
deltaSliceA = reportSlice("deltaSliceA = eliminate(IZ+sliceA, sheetVars)", IZ);

-- odd/even contact intersect delta=0 on the slice
-- (no generic saturation needed: charges are fixed distinct nonzero values,
--  so genericDen restricts to a nonzero multiple of M; saturate by M only)
satM = I -> saturate(I, ideal(M));
oddDeltaSlice = reportSlice("oddDeltaSlice = eliminate(sat_M(Codd+IZ)+sliceA, sheetVars)", satM(Codd+IZ+sliceA));
evenDeltaSlice = reportSlice("evenDeltaSlice = eliminate(sat_M(Ceven+IZ)+sliceA, sheetVars)", satM(Ceven+IZ+sliceA));

-- ramification intersect difference on the slice
ramDeltaSlice = reportSlice("ramDeltaSlice = eliminate(sat_M(IR+IZ)+sliceA, sheetVars)", satM(IR+IZ+sliceA));
