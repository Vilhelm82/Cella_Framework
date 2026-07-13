# Essential Dimension Conjecture

**Status:** PARTIALLY PROVEN, PARTIALLY FALSIFIED — Tier 2
**Type:** Theorem ("if" direction) + qualified conjecture ("only if" direction)
**Source:** Companion paper v3, Sections 7–8; D-12 (cone counterexample)
**Dependencies:** Theorem 5 (special case for bilinear n=3)

---

## Statement (original — Conjecture 1 of companion paper v3)

For a polynomial constraint F(x₁, ..., xₙ) = 0 defining a smooth hypersurface, the Gauss-Kronecker curvature K = 0 at all generic points if and only if the essential dimension of F is strictly less than n.

## Status of Each Direction

### "If" direction: Essential dim < n → K = 0   ✅ EFFECTIVELY PROVEN

Essential dimension < n means F can be expressed in fewer variables via affine substitution. The constraint surface is a generalised cylinder with translation symmetry along (n − d) directions. At least (n − d) principal curvatures vanish identically. The Gauss-Kronecker curvature (product of all principal curvatures) is therefore zero.

This is a theorem, not a conjecture. It follows from standard differential geometry of cylinders.

### "Only if" direction: K = 0 → Essential dim < n   ❌ FALSIFIED BY CONE (D-12)

**Counterexample:** The cone x² + y² − z² = 0 has:
- K_G = 0 everywhere (it is a ruled/developable surface)
- Essential dimension 3 = n (the polynomial is algebraically irreducible — no affine substitution reduces it)

The cone is swept by straight lines through the origin. All ruled surfaces have K_G = 0 (they are developable). But ruled surfaces are NOT characterised by low essential dimension.

### Corrected conjecture (proposed restatements)

**Option 1 (exclusion):** K = 0 at generic points on a non-developable smooth hypersurface iff essential dimension < n.

**Option 2 (disjunction):** K = 0 at generic points → essential dim < n OR the surface is ruled/developable.

## Empirical Support

21/21 polynomial test surfaces consistent with the original conjecture (before cone was identified). The cone was already in the test suite as Test 1.3.1 but wasn't in the essential dimension table. Adding it: 21/22 consistent, 1 counterexample (the cone).

## Recovery of Theorem 5

For bilinear forms in three variables, essential dimension < 3 is equivalent to factorability. Theorem 5 is the special case of the (corrected) conjecture where ruled surfaces don't arise (bilinear forms with closed graph are irreducible and non-ruled).

## Action Required for Paper v4

Conjecture 1 must be restated with the ruled/developable surface exclusion. Present the cone as honest boundary-finding. The "if" direction should be presented as a theorem. The corrected "only if" as a well-supported conjecture with a known boundary condition.
