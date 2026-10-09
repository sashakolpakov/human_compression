# One affine model for all three {6,6} lattice families

9 October 2026. This note independently reconstructs the actual three presented families in Hou–Feng–Leemans, [*Regular 3-polytopes of order 2^n p*, Theorem 5.1 and Corollary 5.2](https://arxiv.org/pdf/2001.02945), using one affine model and one fixed index-48 presentation certificate. It does not derive that paper's other classification/nonexistence theorems. No claim of historical priority is made for the crystallographic model.

## Three affine transformations

Let

    a(x,y,z)=(y,x,z),
    b(x,y,z)=(1-x,z,y),
    c(x,y,z)=(-y,-x,z),

and let E be their group on R^3. Direct substitution proves

    a²=b²=c²=(ab)^6=(bc)^6=(ac)^2=(cbab)^3=1.

Their linear parts generate the signed permutation group Q of degree three, of order 48. To see this, their coordinate permutations generate S3; ac supplies a two-coordinate sign change and its conjugates supply all even sign changes; (ab)^3 supplies -I. Hence all eight sign choices occur.

**Translation lattice.** The kernel of E->Q is exactly

    L=2D3 = { (2x,2y,2z) : x+y+z is even }.

This identification has a small exact certificate. Choose one affine word for each of the 48 linear parts and form its three Schreier transitions. Every resulting translation has even coordinates and sum divisible by four. Among them occur `(-2,-2,0),(-2,0,-2),(0,-2,-2)`. Those vectors have determinant of absolute value 16, equal to the index of 2D3 in Z3. Thus they generate all of 2D3, while the containment check excludes any larger translation lattice. The [integer-only Python verifier](phase2_cubic_lattice_check.py) records all representatives' transition words and vectors in [JSON](phase2_cubic_lattice_check.json). This checks a fixed 48-state system; it is not an empirical extrapolation over m.

## Identifying the source's universal presentation

Let

    U=<a,b,c | a²,b²,c²,(ab)^6,(bc)^6,(ac)^2,(cbab)^3>.

There is a surjection U->E and the same quotient Q of order 48. An exact Reidemeister–Schreier presentation of `ker(U->Q)`, followed by Tietze simplification, has three generators and exactly the three pairwise commutator relators. Hence this kernel is Z3. The complete [GAP certificate](phase2_cubic_kernel_check.g) saves its original word generators and resulting relators in the [log](phase2_cubic_kernel_check.log).

The quotient conventions are explicit. Label the signed basis `(e1,e2,e3,-e1,-e2,-e3)` by 1,...,6. The three linear generators give precisely `(1,2)(4,5)`, `(1,4)(2,3)(5,6)`, `(1,5)(2,4)`, the permutations used in GAP. GAP composes its point permutations as a right action; the homomorphism to the usual column-matrix group sends a permutation to the inverse of its column-action matrix. Our three generators are involutions, so their images are exactly the displayed linear matrices. Thus this convention change does not alter the point-quotient kernel. The Python certificate checks the six-point image lists directly.

The induced map from this kernel onto L is a surjection between free abelian groups of rank three. Its kernel has rank zero and is torsion-free, and is therefore zero. Consequently `U is isomorphic to E` as a marked group.

This is a deliberately explicit computational proof step. The compression replaces three separate index-192/384/768 seed computations and atlas lookups by one index-48 presentation plus elementary integer coordinates. It does not pretend that the universal-presentation identification was proved without a computation.

## The source's words become three elementary lattices

In the source's notation, its three triples of translation generators evaluate as follows. Conjugation uses `x^g=g^(-1)xg`.

| Family | Translation vectors of the source's three words | Lattice Λ | Index in L |
|---|---|---|---:|
| G_m | (4,0,0), (0,-4,0), (0,0,-4) | `4Z3` | 4 |
| H_m | (4,-4,0), (4,0,-4), (-4,-4,0) | `4D3` | 8 |
| I_m | (4,-4,4), (4,-4,-4), (-4,-4,4) | `8Z3+4Z(1,1,1)` | 16 |

The determinant indices in Z3 are respectively 64,128,256, while L has index 16. All three lattices are invariant under every signed permutation, lie in L, and lie in 4Z3. Raising each word to its m-th power replaces Λ by mΛ. Thus the source's presented groups are exactly `E/(mΛ)`, and their orders are

    48 [L:mΛ] = 192m³, 384m³, 768m³.

The matrix evaluation of the actual source words, not just these determinant counts, is included in the Python certificate. This identifies the source's families rather than merely constructing groups with matching numerical parameters.

## One intersection check proves every family

The affine subgroups A=<a,b> and B=<b,c> both have order twelve and inject into their linear images. The intersection of their linear images has four elements. For two of them, namely the identity and the linear part of b, the affine translations agree. For the other two, the translations differ by `(0,2,2)`.

These four entries are explicitly listed in the certificate. Since `(0,2,2)` does not belong to 4Z3, and every mΛ is contained in 4Z3, the images satisfy

    A_bar intersect B_bar = <b_bar>

in every one of the quotients, for every m>=1. The pair orders are exactly six, since their linear images already have those orders. The endpoints commute and are distinct. Independence also follows: either endpoint lying in the other parabolic would enlarge this intersection. Thus each quotient is a rank-three string C-group of type {6,6}.

Each quotient is solvable: its translation subgroup is abelian and its point quotient `C2^3 semidirect S3` is solvable. This completes every assertion of Theorem 5.1 about the specified three families.

## The remaining order-96 case and Corollary 5.2

The tetrahedral marking of S4 is

    r0=(1,2), r1=(2,3), r2=(3,4).

Take two independent central involutions x,y and replace the marking in `S4 x <x,y>` by

    rho0=(r0,x), rho1=(r1,1), rho2=(r2,y).

The adjacent products have order six, and their cubes recover x and y separately. Thus the tuple generates the entire group of order 96. The two parabolic kernels are respectively <x> and <y>, so the kernel-intersection criterion gives IP from the tetrahedral IP. This proves the order-96 case directly, without an atlas entry.

In the three affine families set m=2^k. The orders become `3*2^(6+3k)`, `3*2^(7+3k)` and `3*2^(8+3k)`, covering every exponent n>=6. Together with the explicit order-96 example, this proves the source's complete Corollary 5.2: type {6,6} exists at order `3*2^n` for every n>=5.

The [phase-two synthesis](compression_phase2.md) combines this construction with the dihedral edge-inflation theorem. Their common feature is exact control of the kernel's coordinate lattice and the distinguished subgroup intersections. The affine lattice mechanism remains mathematically distinct from an arbitrary p-group classification.
