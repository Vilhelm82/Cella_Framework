-- Cache-isolated generic route for all sixteen contact images.
load "/home/wlloyd/Cella Framework/docs/files/horizon_wreath_inertia_model.m2";
baselineTimed = elapsedTiming apply(epsilons, eps ->
    projectToBase(contactIdeal eps + ideal(0_S))
    );
baselineImages = baselineTimed#1;
expectedWalls = apply(epsilons, eps -> trim ideal(wallPolynomial eps));
assert(#baselineImages == 16);
assert(all(16, k -> trim(baselineImages#k) == trim(expectedWalls#k)));
print("CONTACT_BASELINE_ELAPSED_SECONDS=" | toString(baselineTimed#0));
print "CONTACT_BASELINE_EXACTNESS=CLOSED";
