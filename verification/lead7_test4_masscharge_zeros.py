"""
LEAD-7 TEST 4 — THEOREM: the mass-charge coupling zeros are exactly the role divisors.
FRESH, zero-import. sympy + mpmath (declared). SYMBOLIC (exact identities) + a numeric
cross-check. Byte-stable.

Upgrades the interior-cleanliness of the Candidate-F(u=0) metric (Test 3,
reports/LEAD7_test3_candF_n3.md) from a finite numerical scan to a THEOREM: the
mass-charge inverse-channel metric g_F(u=0) has NO interior curvature singularity because
its mass-charge couplings have no interior zeros -- they vanish exactly on the physical
role divisors T=0 (extremal), Omega=0 (J=0), Phi_e=0 (Q=0).

SET-UP. Kerr-Newman graph M^2 = U(S,J,Q),  U = S/(4pi) + pi J^2/S + Q^2/2 + pi Q^4/(4S),
charges E=(S,J,Q). Each output chart E_i = f_i(M, E_j, E_k) solves M^2=U for E_i. Its
mass-charge couplings are the mixed second partials Lambda_{i,{M,j}} = d^2 E_i/dM dE_j.

UNIFORM FORMULA (implicit differentiation of M^2=U; chart-independent):
    E_{i,M}   = 2M / U_i                         (diverges on the NATIVE role divisor U_i=0)
    Lambda_{i,{M,j}} = E_{i,Mj} = 2M (U_ii U_j - U_i U_ij) / U_i^3 .
So the coupling's pole is the native divisor U_i=0; its ZERO is the numerator
    N_{ij} = U_ii U_j - U_i U_ij = 0.

THEOREM (this file certifies the pieces). On the physical wedge
W = {S,J,Q > 0, disc = M^4 - M^2 Q^2 - J^2 > 0} (equivalently U_S > 0):
  (a) [uniform formula] Lambda_{i,{M,j}} from the implicit formula equals the explicit
      chart differentiation of f_i  (numeric, all three charts).
  (b) [factorization] each of the six numerators N_{ij} factors as
          N_{ij} = (charge factor: J or Q, or a U_S-term) x (manifestly POSITIVE bracket),
      an exact symbolic identity.
  (c) [positivity of U_S] U_S = sqrt(disc)/S_+ >= 0 on the outer branch, = 0 iff disc=0
      (extremal), via the horizon Vieta relations S_+ S_- = pi^2(4J^2+Q^4), S_+ - S_- =
      4 pi sqrt(disc).
  (d) [all-positive coefficients] each bracket, with U_S replaced by a nonnegative
      placeholder, is a polynomial in the POSITIVE variables (S,J,Q,U_S,pi) with all
      coefficients >= 0.
Hence in the OPEN interior (J,Q>0, U_S>0) every N_{ij} > 0: the mass-charge couplings are
finite and nonzero there. Their zero loci in the closure lie in {J=0} u {Q=0} u {U_S=0},
i.e. EXACTLY the role divisors Omega=0, Phi_e=0, T=0.

CONSEQUENCE. g_F(u=0)_{ii} = q_i^2 * sum_{mass-charge j} 1/Lambda_{i,{M,j}}^2 is finite,
smooth and positive-definite on the interior (no 1/Lambda^2 pole), so its curvature is
finite there. All curvature divergences of g_F(u=0) sit on the role boundaries -- the
interior-cleanliness of Test 3 is now a theorem, not a scan.
"""
import sympy as sp
import mpmath as mp

FAILS = []
def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)

M, S, J, Q, pi, us = sp.symbols('M S J Q pi u_S', positive=True)
U = S/(4*pi) + pi*J**2/S + Q**2/2 + pi*Q**4/(4*S)
Us, Uj, Uq = sp.diff(U, S), sp.diff(U, J), sp.diff(U, Q)
Uss, Ujj, Uqq = sp.diff(U, S, 2), sp.diff(U, J, 2), sp.diff(U, Q, 2)
Usj, Usq, Ujq = sp.diff(U, S, J), sp.diff(U, S, Q), sp.diff(U, J, Q)

# six mass-charge numerators N_{i,j} = U_ii U_j - U_i U_ij  (output i, other charge j)
N = {'S,J': Uss*Uj - Us*Usj, 'S,Q': Uss*Uq - Us*Usq,
     'J,S': Ujj*Us - Uj*Usj, 'J,Q': Ujj*Uq - Uj*Ujq,
     'Q,S': Uqq*Us - Uq*Usq, 'Q,J': Uqq*Uj - Uq*Ujq}

# ---- (b) factorizations: N = (charge/U_S factor) x (positive bracket) ----
# brackets written with the SYMBOL us in place of U_S (nonneg); charge factor explicit.
Fac = {
    'S,J': (J/(2*S**2)) * (pi**2*(4*J**2 + Q**4)/S**2 + 1),
    'S,Q': (pi*Q/S**2) * ((4*J**2 + Q**4)*(1 + pi*Q**2/S)/(2*S) + Q**2*us),
    'J,S': (2*pi/S)*us + 4*pi**2*J**2/S**3,
    'J,Q': (2*pi/S)*Q*(1 + pi*Q**2/S),
    'Q,S': (1 + 3*pi*Q**2/S)*us + pi*Q**4*(1 + pi*Q**2/S)/S**2,
    'Q,J': (2*pi*J/S)*(1 + 3*pi*Q**2/S),
}
for k in N:
    identity = sp.simplify(N[k] - Fac[k].subs(us, Us)) == 0
    check(f"T4-b.factor[{k}]", identity, f"N_[{k}] = documented factorization")

# ---- (a) uniform implicit formula == explicit chart differentiation (all 3 charts) ----
disc = M**4 - M**2*Q**2 - J**2
fS = pi*(2*M**2 - Q**2 + 2*sp.sqrt(disc))
wv = S/(2*pi) - M**2 + Q**2/2
fJ = sp.sqrt(M**4 - M**2*Q**2 - wv**2)
fQ = sp.sqrt(-S/pi + (2/pi)*sp.sqrt(pi*S*M**2 - pi**2*J**2))
Mval = sp.sqrt(U)
def Limp(i_sym, j_sym):
    Ui = sp.diff(U, i_sym); Uii = sp.diff(U, i_sym, 2); Uij = sp.diff(U, i_sym, j_sym)
    Uj = sp.diff(U, j_sym)
    return 2*Mval*(Uii*Uj - Ui*Uij)/Ui**3
mp.mp.dps = 40
fS_n = sp.lambdify((M, J, Q, pi), fS, 'mpmath')
# explicit couplings per chart (mixed partials of the chart function wrt M and the other charge)
expl = {
    ('S', 'J'): sp.lambdify((M, J, Q, pi), sp.diff(fS, M, J), 'mpmath'),
    ('S', 'Q'): sp.lambdify((M, J, Q, pi), sp.diff(fS, M, Q), 'mpmath'),
    ('J', 'S'): sp.lambdify((M, S, Q, pi), sp.diff(fJ, M, S), 'mpmath'),
    ('J', 'Q'): sp.lambdify((M, S, Q, pi), sp.diff(fJ, M, Q), 'mpmath'),
    ('Q', 'S'): sp.lambdify((M, S, J, pi), sp.diff(fQ, M, S), 'mpmath'),
    ('Q', 'J'): sp.lambdify((M, S, J, pi), sp.diff(fQ, M, J), 'mpmath'),
}
imp = {(str(i), str(j)): sp.lambdify((M, S, J, Q, pi), Limp(i, j), 'mpmath')
       for (i, j) in [(S, J), (S, Q), (J, S), (J, Q), (Q, S), (Q, J)]}
pts = [(mp.mpf(2), mp.mpf(1), mp.mpf('0.5')), (mp.mpf(3), mp.mpf('1.5'), mp.mpf(1))]
def arg(i, j, m, s, jj, q):
    if i == 'S': return (m, jj, q, mp.pi)
    if i == 'J': return (m, s, q, mp.pi)
    return (m, s, jj, mp.pi)
max_mismatch = mp.mpf(0)
for (m, jj, q) in pts:
    s = fS_n(m, jj, q, mp.pi)
    for (i, j) in expl:
        e = expl[(i, j)](*arg(i, j, m, s, jj, q))
        im = imp[(i, j)](m, s, jj, q, mp.pi)
        max_mismatch = max(max_mismatch, abs(e - im))
check("T4-a.uniform_formula", max_mismatch < mp.mpf('1e-30'),
      f"implicit formula = explicit chart couplings, all 3 charts (max mismatch {mp.nstr(max_mismatch,3)})")

# ---- (c) U_S = sqrt(disc)/S_+ >= 0, zero iff extremal (Vieta) ----
Sp = pi*(2*M**2 - Q**2 + 2*sp.sqrt(disc)); Sm = pi*(2*M**2 - Q**2 - 2*sp.sqrt(disc))
vieta = (sp.simplify(Sp*Sm - pi**2*(4*J**2 + Q**4)) == 0 and
         sp.simplify(Sp - Sm - 4*pi*sp.sqrt(disc)) == 0)
Us_closed = sp.simplify(Us - (S**2 - pi**2*(4*J**2 + Q**4))/(4*pi*S**2)) == 0
Us_at_Sp = sp.simplify(((Sp**2 - pi**2*(4*J**2 + Q**4))/(4*pi*Sp**2)) - sp.sqrt(disc)/Sp) == 0
check("T4-c.U_S_nonneg", vieta and Us_closed and Us_at_Sp,
      "U_S = sqrt(disc)/S_+ >= 0 (Vieta: S_+ S_- = pi^2(4J^2+Q^4), S_+ - S_- = 4pi sqrt(disc)); =0 iff extremal")

# ---- (d) each bracket has all-nonnegative coefficients over positive vars (S,J,Q,us,pi) ----
# strip the leading charge factor, clear the S-denominator, expand -> Poly; all coeffs >= 0.
brackets = {
    'S,J': (pi**2*(4*J**2 + Q**4)/S**2 + 1),                                   # x J/(2S^2)
    'S,Q': ((4*J**2 + Q**4)*(1 + pi*Q**2/S)/(2*S) + Q**2*us),                  # x pi Q/S^2
    'J,S': (2*pi/S)*us + 4*pi**2*J**2/S**3,                                    # x 1
    'J,Q': (1 + pi*Q**2/S),                                                    # x 2pi Q/S
    'Q,S': (1 + 3*pi*Q**2/S)*us + pi*Q**4*(1 + pi*Q**2/S)/S**2,                # x 1
    'Q,J': (1 + 3*pi*Q**2/S),                                                  # x 2pi J/S
}
allpos = True
for k, b in brackets.items():
    num = sp.numer(sp.together(sp.expand(b)))          # clear S-denominator
    poly = sp.Poly(sp.expand(num), S, J, Q, us, pi)
    if any(c < 0 for c in poly.coeffs()):
        allpos = False
check("T4-d.brackets_positive", allpos,
      "every bracket = sum of positive-coefficient monomials in (S,J,Q,U_S,pi) => bracket > 0 in the wedge")

# ---- conclusion: interior zero-locus is exactly the role divisors ----
# N_{S,J},N_{Q,J} ~ J*(+)  -> zero iff J=0 (Omega=0);
# N_{S,Q},N_{J,Q} ~ Q*(+)  -> zero iff Q=0 (Phi_e=0);
# N_{J,S}=(2pi/S)U_S+4pi^2 J^2/S^3, N_{Q,S}=(..)U_S+(+)Q^4  -> zero iff U_S=0 AND J(or Q)=0.
# With U_S>0, J,Q>0 in the open interior, ALL six N_{ij} > 0: no interior zeros.
zero_loci_ok = (FAILS == [])   # the four verified pieces (a)-(d) establish it
check("T4.theorem", zero_loci_ok,
      "THEOREM: mass-charge coupling zeros = role divisors {J=0}u{Q=0}u{extremal}; "
      "no interior zeros => g_F(u=0) has no interior curvature singularity")

# ---- verdict ----
ntot = 6 + 1 + 1 + 1 + 1  # 6 factorizations + a + c + d + theorem
if FAILS:
    print(f"VERDICT: FAIL ({len(FAILS)}): {', '.join(FAILS)}")
    raise SystemExit(1)
print(f"VERDICT: LEAD-7 TEST 4 CLEAN -- {ntot}/{ntot}. THEOREM (symbolic): the six "
      f"mass-charge couplings Lambda_{{i,{{M,j}}}} = 2M(U_ii U_j - U_i U_ij)/U_i^3 have "
      f"numerators that factor as (charge/U_S factor) x (positive bracket); with "
      f"U_S = sqrt(disc)/S_+ > 0 in the open wedge, every numerator is strictly positive "
      f"there. Hence the mass-charge coupling zeros are EXACTLY the role divisors "
      f"Omega=0 (J=0), Phi_e=0 (Q=0), T=0 (extremal, as the native pole) -- no interior "
      f"zeros. The Candidate-F(u=0) metric therefore has NO interior curvature "
      f"singularity: Test 3's interior-cleanliness is upgraded from a finite scan to a "
      f"theorem. Remaining for full certification: exact pole-coefficient retrodiction "
      f"(KN analogue of the n=2 RC-5 tier).")
