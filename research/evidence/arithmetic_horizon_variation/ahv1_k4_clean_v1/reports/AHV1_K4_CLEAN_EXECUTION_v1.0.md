# AHV-1 at k=4: clean two-instance execution

**Version:** 1.0  
**Status:** independently rebuilt and replay-gated  
**Scope:** a k=4 falsifier/probe, not an all-k IV.3 closure

## 1. Separation of roles

This package deliberately uses two instances and does not merge their claims.

1. The **topological control** is `a=(0,2,3,7)`. It certifies the finite branch system, explicit Hurwitz transpositions, genus, integral homology, and thimble lattice. Because `a_1=0`, it is not used for the R9 contact/Kummer channel.
2. The **decoration-live instance** is `N=(1,2,4,8)`, hence `a=N^2=(1,4,16,64)`. It independently repeats the topology calculation and supplies the canonical R9 channels `r_1=u` and `r_2=gamma_R9=2(e_4(w)+u e_2(w)+u^2+P)`.

## 2. Exact eliminants and finite branching

For each instance the builder forms the full multiquadratic norm

`Phi(u,y)=prod_{epsilon in {+-1}^4}(y-sum_i epsilon_i w_i)`, with `w_i^2=u+a_i`,

inside the exact 16-dimensional group algebra. In both cases `deg_u Phi=5`, `deg_y Phi=16`, and the leading `u^5` coefficient is `-4096*y^6`. Exact resultants isolate:

- one degree-9 factor in `Res_y(Phi,Phi_u)`, occurring with exponent two;
- one square-free degree-18 factor in `Res_u(Phi,Phi_u)`, occurring with exponent one.

Thus each instance has 18 distinct finite simple branch values. Their exact coefficient lists, all resultant factor degrees, and the sparse norm are in the two certificates.

## 3. Explicit Hurwitz systems

Sheets were continued at 50-digit precision around a deterministic noncrossing star of counter-clockwise meridians. Every local permutation is a transposition. For the control instance their ordered product is `[0, 1, 2, 3, 4]`, they generate a group of order `120`, and all ten transposition pairs occur. The decoration-live instance independently gives product `[0, 1, 2, 3, 4]`, group order `120`, and again all ten pairs.

The group is therefore `S_5` in both instances. The recorded branch values, base roots, loop radii, path order, permutations, residual bound, and separation bound make the continuation auditable.

## 4. Integral topology from the computed monodromy

The matrix artifacts use a compressed lifted CW model with 5 vertices, 90 lifted branch edges, and 77 faces. It is chain-equivalent to the more heavily subdivided 95-vertex/180-edge model; no homology claim depends on that subdivision choice.

For both independently computed Hurwitz systems:

- `d_1 d_2=0`;
- `SNF(d_1)` has four nonzero invariant factors, all one;
- `SNF(d_2)` has 76 nonzero invariant factors, all one;
- `H_0=Z`, `H_1=Z^10` with no torsion, and `H_2=Z`;
- `chi=-8`, hence `g=5`, independently agreeing with Riemann--Hurwitz.

## 5. Vanishing cycles and thimbles

For each branch transposition `(a b)`, the vanishing boundary is `e_b-e_a` and the selected thimble is the lifted edge `e_(j,a)`. Exact Smith reduction gives:

- boundary SNF `(1,1,1,1)`, so the cycles integrally generate `A_4`;
- `H_1(X,F_0;Z)=C_1/im(d_2)=Z^14`;
- the augmented matrix `[d_2 | T]` has 90 invariant factors, all one, so the 18 thimbles generate the relative lattice integrally;
- the Gram matrix has nonzero SNF `(1,1,1,5)`, hence discriminant group `Z/5`;
- over `F_2`, the Gram rank is 4, its radical has dimension 14, and the relative thimble span has dimension 14.

There is no integral index defect and no hidden 2-torsion in this presentation.

## 6. Canonically normalized R9 Kummer certificate

Only the decoration-live instance is used here. With `P=64`,

Globally, `alpha=e_4(w)+u e_2(w)+u^2`, `beta=e_3(w)+u e_1(w)`, and

`gamma_R9=2(alpha+P)=2(e_4(w)+u e_2(w)+u^2+P)`.

The exact factorization `prod_i(w_i+sqrt(u))=alpha+sqrt(u) beta` gives
`alpha^2-u beta^2=P^2`, hence
`gamma_R9(gamma_R9-4P)=4u beta^2`. At a signed contact `u=0`, this global
radicand specializes to `2(P+e_4(w))`; only that specialization was used to
compute the two parity rows below.

The all-plus contact has `y=15`, reciprocal sum `15/8`, `beta=120`, and parity row `(1,0)`. The odd contact `(-,+,+,+)` has `y=13`, reciprocal sum `-1/8`, `beta=8`, and parity row `(1,1)`. Exact evaluation of the degree-18 branch polynomial at both contact values is nonzero, so these specialized contacts are away from the finite mass branch locus.

Orbit saturation under the independently certified transitive `S_5` action gives

`V=[[I_5,0],[I_5,I_5]]=B tensor I_5`, where `B=[[1,0],[1,1]]`.

Its `F_2` rank is 10. The ten conjugate square classes are independent and the k=4 static normal closure is `C_2^2 wr S_5`, of order `122880`.

## 7. What this does and does not establish

This clean run establishes the k=4 topology, integral thimble generation, and canonical two-channel R9 parity certificate on explicit good instances. It upgrades the evidence base by making every matrix and exact eliminant available for replay.

It does **not** prove the arbitrary-k relation module vanishes, identify a universal entropy-type second radicand for k other than 4, or close all of IV.3. In particular, no rank claim is made from a single unsaturated prolongation; the Kummer conclusion uses the full `S_5` orbit.

## 8. Replay

Run `python3 build_ahv1_k4_clean.py` to reconstruct the package, then `python3 verify_ahv1_k4_clean.py` or the repository gate `python3 engine/tests/gate_ahv1_k4_clean.py`.
