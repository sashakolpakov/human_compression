# Independent audit of the transvection/subfield intersection theorem

Let E,F be subfields of a field L, put k=E∩F, and let n≥2. Write N=E_(12) and U(t)=I+tN. The proposed general theorem is correct:

    SL_n(E) ∩ U(t) SL_n(F) U(−t) = C_(SL_n(k))(N), if t∉E+F.

The same theorem holds for GL_n. In fact it holds before imposing any determinant or invertibility condition:

    M_n(E) ∩ U(t) M_n(F) U(−t) = C_(M_n(k))(N).

Here the centralizer on the right consists of matrices commuting with the nilpotent matrix N. There is no finite-field hypothesis and no restriction on characteristic. This is an audited generalization of the matrix intersection mechanism used in the proposed proof of the 2017 Conjecture 6.2. Novelty outside the Leemans setting has not been established.

For M=(m_ij), the conjugate M'=U(−t)MU(t) has entries

    m'_ij = m_ij + t m_i1 δ_j2 − t δ_i1 m_2j − t² δ_i1 m_21 δ_j2.

Suppose M is over E and M' is over F. The entry m_21 is unchanged, so it belongs to k. The equation m'_11=m_11−t m_21 shows m_21=0: otherwise t is a sum of an element of E and one of F.

For i≠1, the unchanged m_i1 belongs to k, and m'_i2=m_i2+t m_i1 forces m_i1=0. Similarly, for j≠2, the unchanged m_2j belongs to k, and m'_1j=m_1j−t m_2j forces m_2j=0. The diagonal entries now belong to k. Finally m'_12=m_12+t(m_11−m_22) forces m_11=m_22. All entries are now unchanged by conjugation, so they lie in k. The vanishing row and column entries together with m_11=m_22 are exactly the conditions MN=NM. The reverse containment is immediate.

If t is in the additive sum, write t=e+f with e∈E,f∈F. Since the U parameters add and U(f) normalizes SL_n(F),

    SL_n(E) ∩ U(t) SL_n(F) U(−t)
      = U(e) SL_n(k) U(−e).

The same argument applies to GL_n and the full matrix algebra. Thus the additive sum is the precise boundary between these two intersection types. Choosing a different decomposition t=e'+f' changes e by an element of k and leaves this subgroup unchanged.

## Formal certificate

[formal/TransvectionIntersection.lean](formal/TransvectionIntersection.lean) proves the entrywise statement in arbitrary dimension, with the displayed conjugation expression made explicit. It uses an arbitrary index type with two distinct distinguished indices, so it does not even require finiteness of the matrix index set.

The theorem `transvection_intersection_iff` proves both directions: the conjugated entries belong to F exactly when the original entries belong to E∩F and the entries of MN and NM agree. Neither determinant nor invertibility is assumed. The actual finite matrix multiplication identity and the packaging into SL_n/GL_n are the elementary steps outside this certificate.

The file compiles with the pinned Lean/mathlib environment, has no `sorryAx` dependency, and uses only the usual `propext`, `Classical.choice`, and `Quot.sound` axioms. The hash-bearing build record is [formal/TransvectionIntersection.check.json](formal/TransvectionIntersection.check.json). Reproduce with:

    python3 research/leemans/formal/verify_lean.py TransvectionIntersection.lean

## Why coprime degrees are necessary for the PSL(2) construction

The primitive parameters in the proposed square theorem exist for every pair of odd degrees e_1,e_2>1. This does not mean that all degree pairs produce rank-four chiral polytopes.

Let g=gcd(e_1,e_2), F_i=F_(p^e_i), k=F_(p^g), and L their compositum. For the source's matrices, the adjacent generated subgroups are the full conjugate subfield groups PSL(2,F_i); this follows from the Dickson generation argument in [psl2_chiral_corollary.md](psl2_chiral_corollary.md).

If neither degree divides the other, the field argument from the intersection proof works with base field k instead of F_p. Both u² and v² lie outside k, since they generate their respective fields. It follows that the shear parameter t is outside F_1+F_2. The actual adjacent-subgroup intersection is therefore U(k), of order p^g. The shared generator β still has order p. Consequently the required intersection property holds precisely when g=1.

If e_1 divides e_2, then L=F_2 and t∈F_2. The normalized second subgroup is the whole PSL(2,F_2), while the first is PSL(2,F_1); their intersection is the full smaller subgroup. The reversed nesting case is identical after conjugating by U(t). In particular the intersection property fails for every nested pair.

This gives a structural explanation for the source's coprime factorization d=e_1e_2. The distinction between the full primitive-square conjecture and the narrower parameters needed for the chiral construction is essential.
