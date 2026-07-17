-- Stage 1: load model (runs assertions), basic dims, quintic eliminant retaining u
load "/home/wlloyd/Cella Framework/docs/horizon_wreath_inertia_model.m2";

print("codim IX = " | toString codim IX);
print("dim(S/IX) = " | toString dim(S^1/IX));

-- Step 2 of workflow: recover the quintic by eliminating only w1..w4, retaining u
massFiberIdeal = trim eliminate(IX,{w1,w2,w3,w4});
print "=== gens massFiberIdeal ===";
print toString gens massFiberIdeal;
print "=== factored generators ===";
scan(flatten entries gens massFiberIdeal, g -> print toString factor g);
