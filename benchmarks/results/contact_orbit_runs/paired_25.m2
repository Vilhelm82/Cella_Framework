-- Paired 16-contact benchmark; model startup is outside marginal timings.
load "/home/wlloyd/Cella Framework/docs/files/horizon_wreath_inertia_model.m2";
baselineTimed = elapsedTiming apply(epsilons, eps ->
    projectToBase(contactIdeal eps + ideal(0_S))
    );
baselineImages = baselineTimed#1;
structuralTimed = elapsedTiming apply(epsilons, eps ->
    trim ideal(wallPolynomial eps)
    );
structuralImages = structuralTimed#1;

certificateTimed = elapsedTiming all(epsilons, eps ->
    trim(contactIdeal eps + ideal(0_S)) == trim ideal(
        u,
        w1-eps#0*N1,
        w2-eps#1*N2,
        w3-eps#2*N3,
        w4-eps#3*N4,
        wallPolynomial eps
        )
    );
assert(certificateTimed#1);

assert(all(16, k -> trim(baselineImages#k) == trim(structuralImages#k)));
assert(#structuralImages == 16);
print("CONTACT_BASELINE_ELAPSED_SECONDS=" | toString(baselineTimed#0));
print("CONTACT_STRUCTURAL_ELAPSED_SECONDS=" | toString(structuralTimed#0));
print("CONTACT_CERTIFICATE_ELAPSED_SECONDS=" | toString(certificateTimed#0));
print "CONTACT_EQUIVALENCE=CLOSED";
