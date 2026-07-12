-- Generated signed-contact orbit route.
load "/home/wlloyd/Cella Framework/docs/files/horizon_wreath_inertia_model.m2";

pathfinderExecTimed = elapsedTiming apply(epsilons, eps ->
    trim ideal(wallPolynomial eps)
    );
pathfinderContactImages = pathfinderExecTimed#1;

print "PATHFINDER_M2_RESULT_BEGIN";
scan(pathfinderContactImages, image -> print toString gens image);
print "PATHFINDER_M2_RESULT_END";
print("PATHFINDER_M2_EXEC_ELAPSED_SECONDS=" | toString(pathfinderExecTimed#0));

pathfinderCertTimed = elapsedTiming all(epsilons, eps ->
    trim(contactIdeal eps) == trim ideal(
        u,
        w1-eps#0*N1,
        w2-eps#1*N2,
        w3-eps#2*N3,
        w4-eps#3*N4,
        wallPolynomial eps
        )
    );
assert(pathfinderCertTimed#1);
print("PATHFINDER_M2_CERT_ELAPSED_SECONDS=" | toString(pathfinderCertTimed#0));
print "PATHFINDER_M2_CERTIFICATE=CLOSED";
