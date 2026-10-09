# A uniform obstruction for two tensor configurations in PSL(4,q)

Date: 2026-10-09. Working proof notes, not a proof of Leemans's full PSL(4,q) rank conjecture. The lemmas below are independently derived here; novelty has not been established.

Work over an algebraically closed field k of characteristic different from 2. A projective involution can be represented by a matrix squaring to I after scaling. Matrices representing commuting projective involutions commute or anticommute: if XY=cYX and X²=Y²=I, conjugating twice shows c²=1.

For a candidate rank-five string C-group write its normalized lifts as T_0,...,T_4. The projective subgroup E=<[T_0],[T_2],[T_4]> must be elementary abelian of rank three. In particular, [T_2] is not in <[T_0],[T_4]>. Adjacent generators must not commute projectively when the whole group is nonabelian simple: otherwise the string splits as a direct product of its two sides by the intersection property.

## Lemma 1: untwisted tensor configuration

Suppose V=U⊗W with dim U=dim W=2 and

    T_0=L_0⊗I,  T_1=L_1⊗I,
    T_3=I⊗R_3,  T_4=I⊗R_4,

where each L_i and R_i is a nonscalar involution. Suppose T_2 is a projective involution commuting projectively with T_0 and T_4. Then all five matrices preserve a common nonzero bilinear form up to individual scalar multipliers. The form may be degenerate.

### Proof

Choose bases in U and W so L_0=R_4=Z=diag(1,-1). Write

    L_1=[[a,b],[c,-a]],   a²+bc=1,
    R_3=[[d,e],[f,-d]],   d²+ef=1.

Set Q_L=diag(c,b), Q_R=diag(f,e), and J=[[0,1],[-1,0]]. Direct multiplication gives

    L_i^T Q_L L_i=Q_L,   R_i^T Q_R R_i=Q_R,
    M^T J M=det(M)J for every 2×2 matrix M.

Since adjacent projective generators do not commute, (b,c) and (e,f) are nonzero pairs, so Q_L and Q_R are nonzero. They can have rank one, which causes no difficulty.

Write T_2 T_0=(-1)^α T_0 T_2 and T_2 T_4=(-1)^β T_4 T_2, α,β∈{0,1}. The four simultaneous eigenspaces of T_0,T_4 are one-dimensional. Thus T_2 is a monomial matrix whose permutation flips the first coordinate if α=1 and the second if β=1. Since T_2²=I, the products of its paired coefficients are 1; in the diagonal case every diagonal coefficient squares to 1.

The following form is preserved up to a scalar by T_2, by direct substitution of these coefficients:

| α | β | Form B |
|---|---|---|
| 0 | 0 | Q_L⊗Q_R |
| 1 | 0 | J⊗Q_R |
| 0 | 1 | Q_L⊗J |
| 1 | 1 | J⊗J |

For the last row, J⊗J pairs each of the four basis vectors with its opposite vertex in the square, and the two coefficients in each such pair multiply to 1. For the middle rows, J pairs the flipped coordinate while the other factor is diagonal. For the first row the form is diagonal. This verifies each row even when one of the Q's is degenerate.

The four endpoint matrices preserve B up to scalar, by the displayed identities. B is nonzero since each tensor factor is nonzero. This proves the lemma.

## Lemma 2: tensor configuration with four anticommuting cross pairs

Suppose

    T_0=L_0⊗I,  T_1=L_1⊗I,
    T_3=K⊗R_3,  T_4=K⊗R_4,

where L_0,L_1,R_3,R_4,K are nonscalar invertible 2×2 matrices, all relevant tensor generators are involutions, and K anticommutes with both L_0 and L_1. Suppose adjacent generators do not commute projectively, and [T_0],[T_2],[T_4] are independent commuting projective involutions. Then all five matrices preserve one nondegenerate alternating form up to scalar.

### Proof

Scale K so K²=I, and the R_i accordingly so R_i²=I. An anticommuting pair of nonscalar 2×2 involutions can be put in the form L_0=Z, K=X=[[0,1],[1,0]]. The condition KL_1=-L_1K gives

    L_1=[[a,b],[-b,-a]],    a²-b²=1.

Choose the basis in W so R_4=Z. The form

    F=Z⊗J=diag(J,-J)

is nondegenerate and alternating. We have L_i^T Z L_i=Z, K^T Z K=-Z, and R_i^T J R_i=det(R_i)J=-J. Thus the four endpoint matrices preserve F.

It remains to treat T_2. Write

    T_2 (Z⊗I)=ε (Z⊗I) T_2,
    T_2 (X⊗Z)=δ (X⊗Z) T_2,

with ε,δ∈{1,-1}.

If ε=1, then T_2=diag(B,C) and C=δ ZBZ. Since T_2²=I, B²=I. If B is scalar, [T_2] is either the identity or [T_0], violating independence. Therefore B is traceless with det(B)=-1, as is C. Consequently

    T_2^T F T_2=diag(-J,J)=-F.

If ε=-1, write T_2=[[0,B],[C,0]]. The second commutation relation gives C=δ ZBZ. The involution relation is equivalent to (BZ)²=δ I. Put D=BZ. If D is scalar, [T_2] equals [T_4] or [T_0T_4], again violating independence. Otherwise D is traceless, with det D=-δ. Therefore det B=det C=δ, and

    T_2^T F T_2=diag(-δJ,δJ)=-δF.

This proves the lemma.

## Consequence for PSL(4,q)

For odd q, neither configuration can generate the natural projective group PSL(4,q). If B is degenerate, its nonzero proper radical is invariant. If B is nondegenerate, a common projective similarity form would give the full PSL(4,q) a self-dual natural projective representation. This is impossible for its natural four-dimensional module; it can also be checked directly with elementary transvections.

Here is a direct check avoiding any classification. Pull back the alleged form to SL_4(q). The scalar multiplier is a homomorphism SL_4(q)→k*, hence trivial because SL_4(q) is perfect. Thus all transvections I+tE_ij preserve B. Choose t=1,-1. Expanding and subtracting gives E_ji B+B E_ij=0 and E_ji B E_ij=0. The latter forces B_ii=0. The former, varying i,j, forces all entries in row i outside column j, and all entries in column i outside row j, to vanish. Since dimension is at least three and j can vary, B=0, a contradiction.

These lemmas give a uniform exclusion, valid in every odd characteristic and without assuming semisimplicity of the two-dimensional dihedral modules. They improve on checking extensions of one existing rank-four construction. They do **not** yet classify every four-dimensional projective representation of the two commuting endpoint dihedrals.

## Outstanding configurations

The genuine remaining work is to prove the endpoint action falls into these tensor cases, or to handle the other cases explicitly. In particular:

1. The four cross commutators between {T_0,T_1} and {T_3,T_4} may have mixed signs.
2. The representation of the two endpoint dihedrals can have invariant summands, extensions, or imprimitivity that are destroyed after adding T_2.
3. Projective involutions of 1+3 eigenspace type, available inside PSL(4,q) when q≡1 mod 8, allow diagonal elementary-abelian configurations absent in other odd q.
4. Excluding rank-five representations alone does not automatically exclude higher rank, because the known rank-reduction theorem has hypotheses and rank-five parabolics in a higher-rank representation are proper subgroups.

No statement here removes these remaining cases.
