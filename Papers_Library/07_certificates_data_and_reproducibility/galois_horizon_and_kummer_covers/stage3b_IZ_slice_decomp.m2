-- Stage 3b: decompose IZ upstairs restricted to the exact slice N=(4,8,12,20).
-- Cheaper probe of whether the rotating difference divisor splits on the cover.
load "/home/wlloyd/Cella Framework/docs/horizon_wreath_inertia_model.m2";

sliceA = ideal(N1-4, N2-8, N3-12, N4-20);
IZslice = IZ + sliceA;

print "=== minimalPrimes (IZ + sliceA) upstairs ===";
Zmin = minimalPrimes IZslice;
print("number of minimal primes: " | toString(#Zmin));
scan(#Zmin, k -> (
    print("--- prime " | toString k | " (codim " | toString codim Zmin#k
        | ", degree " | toString degree Zmin#k | ") ---");
    print toString gens Zmin#k));
