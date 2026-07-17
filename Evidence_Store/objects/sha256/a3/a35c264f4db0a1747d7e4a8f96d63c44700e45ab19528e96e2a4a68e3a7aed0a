-- Stage 2 (workflow step 4): test the 16 contact images against expected walls
load "/home/wlloyd/Cella Framework/docs/horizon_wreath_inertia_model.m2";

contactImages = apply(epsilons, eps -> projectToBase(contactIdeal eps));
expectedWalls = apply(epsilons, eps -> trim ideal(wallPolynomial eps));
results = apply(16, k -> trim(contactImages#k) == expectedWalls#k);
scan(16, k -> print(toString(epsilons#k) | "  matches wall: " | toString(results#k)));
print("all 16 match: " | toString(all(results, r -> r)));
-- record actual images in case of mismatch
scan(16, k -> if not results#k then (
    print("MISMATCH at eps=" | toString(epsilons#k));
    print("  image: " | toString gens contactImages#k);
    print("  wall : " | toString gens expectedWalls#k)));
