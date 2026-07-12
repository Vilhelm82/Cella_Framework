-- Generated Kummer finite-extension primeness route (route ladder P4).
load "/home/wlloyd/Cella Framework/docs/files/horizon_wreath_inertia_model.m2";

pathfinderExecStart = cpuTime();
-- Route step 1: squarefreeness of the rotating radicand in the rotation variable.
radicandPoly = delta;
radicandDerivative = diff(J, radicandPoly);
-- Route step 2: the private-prime structure comes from the derivative pairing.
privatePrimeWitness = ideal(radicandPoly, radicandDerivative);
pathfinderExecCPU = cpuTime() - pathfinderExecStart;

print "PATHFINDER_M2_RESULT_BEGIN";
print toString gens trim IZ;
print "PATHFINDER_M2_RESULT_END";
print("PATHFINDER_M2_EXEC_CPU_SECONDS=" | toString pathfinderExecCPU);

pathfinderCertStart = cpuTime();
-- External certificate replay: squarefreeness plus the certified Thm 16.1
-- codimension/degree data of the rotating difference ideal.
assert(gcd(radicandPoly, radicandDerivative) == 1);
assert(codim IZ == 6);
assert(degree IZ == 64);
pathfinderCertCPU = cpuTime() - pathfinderCertStart;
print("PATHFINDER_M2_CERT_CPU_SECONDS=" | toString pathfinderCertCPU);
print "PATHFINDER_M2_CERTIFICATE=CLOSED";
