-- Stage 4b (workflow section 10): minimal primes of IR+IZ, SubEven, SubOdd
load "/home/wlloyd/Cella Framework/docs/horizon_wreath_inertia_model.m2";

reportPrimes = (lbl, I) -> (
    print("=== minimalPrimes " | lbl | " ===");
    ps := minimalPrimes I;
    print("number of minimal primes: " | toString(#ps));
    scan(#ps, k -> (
        print("--- prime " | toString k | " (codim " | toString codim ps#k
            | ", degree " | toString degree ps#k | ") ---");
        print toString gens ps#k));
    );

reportPrimes("SubEven", SubEven);
reportPrimes("SubOdd", SubOdd);
reportPrimes("IR+IZ", IR+IZ);
