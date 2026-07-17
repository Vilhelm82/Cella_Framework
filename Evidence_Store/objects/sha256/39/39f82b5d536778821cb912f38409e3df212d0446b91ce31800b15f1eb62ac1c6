-- Stage 6 (script suggested command 9, on a slice): compare projected sheet
-- crossings at a charge collision with true relative ramification.
-- Collision slice: N1 = N2 = 8, N3 = 12, N4 = 20.
load "/home/wlloyd/Cella Framework/docs/horizon_wreath_inertia_model.m2";

sliceC = ideal(N1-8, N2-8, N3-12, N4-20);

-- quintic eliminant on the collision slice, retaining u
quinticC = trim eliminate(IX + sliceC, {w1,w2,w3,w4});
print "=== quintic eliminant on collision slice (gens) ===";
print toString gens quinticC;

-- true branch image on the collision slice
branchC = trim eliminate(IR + sliceC, sheetVars);
print "=== true branch image on collision slice ===";
print toString gens branchC;
scan(flatten entries gens branchC, g -> if g != 0 then print("  factor: " | toString factor g));

-- discriminant of the quintic in u on the collision slice
Rbase = QQ[m,uu];
-- find the generator involving u
gs = select(flatten entries gens quinticC, g -> member(u, support g));
print("number of u-generators: " | toString(#gs));
if #gs > 0 then (
    q0 := gs#0;
    phi := map(Rbase, S, {m,8,8,12,20,0, uu, 0,0,0,0});
    qb := phi q0;
    print "=== quintic in uu over QQ[m] ===";
    print toString qb;
    dsc := discriminant(qb, uu);
    print "=== discriminant of quintic in uu ===";
    print toString dsc;
    print "=== factored discriminant ===";
    print toString factor dsc;
    );
