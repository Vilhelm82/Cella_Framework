-- Stage 3 (workflow step 5): decompose the rotating difference divisor IZ upstairs
load "/home/wlloyd/Cella Framework/docs/horizon_wreath_inertia_model.m2";
needsPackage "PrimaryDecomposition";

print "=== minimalPrimes IZ ===";
Zmin = minimalPrimes IZ;
print("number of minimal primes: " | toString(#Zmin));
scan(#Zmin, k -> (
    print("--- prime " | toString k | " (codim " | toString codim Zmin#k
        | ", degree " | toString degree Zmin#k | ") ---");
    print toString gens Zmin#k));

print "=== primaryDecomposition IZ ===";
Zpri = primaryDecomposition IZ;
print("number of primary components: " | toString(#Zpri));
scan(#Zpri, k -> (
    print("--- primary component " | toString k | " (codim " | toString codim Zpri#k | ") ---");
    print toString gens Zpri#k));
