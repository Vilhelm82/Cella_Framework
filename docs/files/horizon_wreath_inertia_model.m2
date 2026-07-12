-- Horizon wreath-cover incidence and inertia model
-- Macaulay2 starter file, 2026-07-10
--
-- The incidence normalization is primary.  Do not use only the quintic
-- eliminant to decide ramification: its discriminant also sees unramified
-- crossings of projected sheets.

S = QQ[
    M,N1,N2,N3,N4,J,
    u,w1,w2,w3,w4,
    Degrees => {1,1,1,1,1,2,2,1,1,1,1},
    MonomialOrder => GRevLex
    ];

P = N1*N2*N3*N4;

q1 = w1^2-u-N1^2;
q2 = w2^2-u-N2^2;
q3 = w3^2-u-N3^2;
q4 = w4^2-u-N4^2;
h  = w1+w2+w3+w4-4*M;

IX = ideal(q1,q2,q3,q4,h);
sheetVars = {u,w1,w2,w3,w4};

-- Symmetric channel functions on one normalized mass sheet.
e1w = w1+w2+w3+w4;
e2w = w1*w2+w1*w3+w1*w4+w2*w3+w2*w4+w3*w4;
e3w = w1*w2*w3+w1*w2*w4+w1*w3*w4+w2*w3*w4;
e4w = w1*w2*w3*w4;

alpha = e4w+u*e2w+u^2;
beta  = e3w+u*e1w;
gamma = 2*(alpha+P);
delta = gamma-4*P-16*J^2;

-- Relative Jacobian for X -> Spec QQ[M,N1,N2,N3,N4,J].
-- Rows are q1,q2,q3,q4,h; columns are u,w1,w2,w3,w4.
Jrel = matrix{
    {-1,2*w1,0,0,0},
    {-1,0,2*w2,0,0},
    {-1,0,0,2*w3,0},
    {-1,0,0,0,2*w4},
    { 0,1,1,1,1}
    };

ramDet = det Jrel;
IR = IX+ideal(ramDet);

-- Lightweight consistency checks.
assert(codim IX == 5);
assert((ramDet-8*e3w) % IX == 0);

-- Kummer branch candidates on one sheet.
Iu = IX+ideal(u);
Ig = IX+ideal(gamma);
IZ = IX+ideal(delta);

-- Generic-open denominator.  Do not use this saturation when studying the
-- excluded divisor that appears in the denominator itself.
collisionProduct =
    (N1^2-N2^2)*(N1^2-N3^2)*(N1^2-N4^2)*
    (N2^2-N3^2)*(N2^2-N4^2)*(N3^2-N4^2);

genericDen = 2*M*P*collisionProduct;
cleanGeneric = I -> trim saturate(I,ideal(genericDen));

-- Projection and intersection helpers.
projectToBase = I -> trim eliminate(I,sheetVars);
meetGeneric = (I,K) -> cleanGeneric(I+K);

summarizeIdeal = (label,I) -> (
    print label;
    print("  ambient codimension = " | toString(codim I));
    print("  codimension inside X = " | toString(codim I-codim IX));
    I
    );

-- Sign vectors and contact strata.
epsilons = {
    { 1, 1, 1, 1}, { 1, 1, 1,-1},
    { 1, 1,-1, 1}, { 1, 1,-1,-1},
    { 1,-1, 1, 1}, { 1,-1, 1,-1},
    { 1,-1,-1, 1}, { 1,-1,-1,-1},
    {-1, 1, 1, 1}, {-1, 1, 1,-1},
    {-1, 1,-1, 1}, {-1, 1,-1,-1},
    {-1,-1, 1, 1}, {-1,-1, 1,-1},
    {-1,-1,-1, 1}, {-1,-1,-1,-1}
    };

wallPolynomial = eps ->
    4*M-eps#0*N1-eps#1*N2-eps#2*N3-eps#3*N4;

contactIdeal = eps -> IX+ideal(
    u,
    w1-eps#0*N1,
    w2-eps#1*N2,
    w3-eps#2*N3,
    w4-eps#3*N4
    );

-- Polynomial version of P*sum(epsilon_i/N_i).
reciprocalBalance = eps ->
    eps#0*N2*N3*N4+
    eps#1*N1*N3*N4+
    eps#2*N1*N2*N4+
    eps#3*N1*N2*N3;

evenSign = {1,1,1,1};
oddSign  = {-1,1,1,1};

Ceven = contactIdeal evenSign;
Codd  = contactIdeal oddSign;

SubEven = Ceven+ideal(reciprocalBalance evenSign);
SubOdd  = Codd +ideal(reciprocalBalance oddSign);

-- The reciprocal sub-balance lies in the relative ramification locus.
assert(isSubset(IR,SubEven));
assert(isSubset(IR,SubOdd));

-- Named generic intersections on the incidence cover.
OddDelta  = meetGeneric(Codd,IZ);
EvenDelta = meetGeneric(Ceven,IZ);
RamDelta  = meetGeneric(IR,IZ);

-- Charge-zero and equal-squared-charge boundary ideals.
ChargeZero1 = IX+ideal(N1);
ChargeCollision12 = IX+ideal(N1^2-N2^2);

-- The generic charge collision is not contained in relative ramification.
CollisionRamification12 = ChargeCollision12+IR;

-- ----------------------------------------------------------------------
-- Suggested interactive commands.  They are commented out because the
-- full symbolic eliminations can be expensive.
-- ----------------------------------------------------------------------

-- 1. Recover the quintic relation while retaining u:
-- massFiberIdeal = trim eliminate(IX,{w1,w2,w3,w4});
-- gens massFiberIdeal

-- 2. Compute the true mass branch image from relative ramification:
-- massBranchBase = projectToBase IR;
-- gens massBranchBase

-- 3. Check that each contact component projects to its expected wall:
-- contactImages = apply(epsilons,eps -> projectToBase(contactIdeal eps));
-- expectedWalls = apply(epsilons,eps -> ideal(wallPolynomial eps));
-- apply(0..15,k -> trim(contactImages#k) == trim(expectedWalls#k))

-- 4. Decompose the rotating difference divisor upstairs before projecting:
-- needsPackage "PrimaryDecomposition";
-- Zminimal = minimalPrimes IZ;
-- Zprimary = primaryDecomposition IZ;

-- 5. Explore the incidence poset by sums of ideals:
-- summarizeIdeal("odd contact",Codd);
-- summarizeIdeal("difference divisor",IZ);
-- summarizeIdeal("odd contact intersect difference",OddDelta);
-- summarizeIdeal("ramification intersect difference",RamDelta);

-- 6. Project a stratum only after saturation/cleanup upstairs:
-- oddDeltaBase = projectToBase OddDelta;
-- ramDeltaBase = projectToBase RamDelta;

-- 7. Use a low-dimensional exact slice before a full elimination:
-- sliceA = ideal(N1-4,N2-8,N3-12,N4-20);
-- branchSliceA = eliminate(IR+sliceA,sheetVars);
-- deltaSliceA  = eliminate(IZ+sliceA,sheetVars);
-- gens branchSliceA
-- gens deltaSliceA

-- 8. Inspect the singular locus of the incidence model itself.  This is
-- different from the relative ramification locus of the projection.
-- X = S/IX;
-- singularLocus X

-- 9. Compare a projected polynomial discriminant with true ramification.
-- Equal-charge crossings can occur in the former without occurring in IR.
-- collisionImage = projectToBase ChargeCollision12;
-- collisionRamImage = projectToBase CollisionRamification12;

-- 10. One-sheet Kummer covers can be added after the incidence computations:
-- T = S[x,y,z,Degrees=>{1,2,2}];
-- IXT = substitute(IX,T);
-- Iaug = IXT+ideal(x^2-substitute(u,T),
--                  y^2-substitute(gamma,T),
--                  z^2-substitute(delta,T));

print "Loaded horizon wreath-cover incidence model.";
print "Core identity: relative ramification is IX + ideal(e3w).";
print "Run the commented slice computations before full symbolic elimination.";
