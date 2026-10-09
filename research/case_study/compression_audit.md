# Compact theory and a 36-paper compression audit

9 October 2026. This note measures what a compact theory actually proves. It accompanies [general_framework.md](general_framework.md), the detailed [36-paper CSV](compression_audit.csv), and the [source inventory](literature_inventory.json). The sample is deliberately varied, covering constructions, classifications, rank bounds, algorithms, hypertopes, trialities, codes and graphs. It is not a random sample of the bibliography.

A small theory does eliminate repeated proof work. The strongest verified reductions concern intersections in covers, changes of generators, rank propagation, and controlled positions of matrix subgroups. It also produces new consequences: the central cyclic lift, the exact gcd obstruction for the PSL(2) construction, and higher-dimensional intersections obtained using several independent parameters. These are substantial outputs even though most entire papers do not become corollaries.

The most useful organizational principle is **separate the finite or structural seed from the operation that propagates it**. A seed records the group, generating tuple, local subgroups, orders, and symmetry obstruction. A propagation theorem proves those properties persist for an entire parameter family. The generic proof should be done once; the seed certificate and any classification of all possible seeds must remain visible.

## 1. Five compact ingredients

The following five statements form a workable core. M1 and M2 are elementary transport principles, M3 is an established theorem of Brooksbank–Leemans, M4 is an explicit relative-position calculation developed here, and M5 is a standard character-sum method packaged for primitive elements. Publication priority is unclaimed for the elementary formulations. Their combination is a research tool, not a claim that the authors lacked a common framework.

### M1. Kernel-controlled subgroup diagrams

Let `pi:H->G` have kernel K. Let H_I be a monotone diagram of subgroups, with images G_I satisfying `G_I intersect G_J=G_(I intersect J)`. Put `K_I=K intersect H_I`. Then

    H_I intersect H_J = H_(I intersect J)(K_I intersect K_J).

Hence the upstairs intersection property is equivalent to `K_I intersect K_J=K_(I intersect J)`.

**Proof.** For h in the left intersection choose c in H_(I intersect J) with the same image. Then c^(-1)h belongs to K_I intersect K_J. The reverse containment is immediate. Intersecting with K proves necessity. ∎

This computes the remaining obstruction; it does not assume the desired upstairs intersection. In an elementary abelian kernel it reduces that obstruction to subspace intersections. Its three-subgroup form is formally checked in [LiftCertificate.lean](formal/LiftCertificate.lean).

The faithful-parabolic special case is already established: [*An exploration of locally spherical regular hypertopes*, Theorem 3.1](https://dipot.ulb.ac.be/dspace/bitstream/2013/309163/3/LSRH-revised.pdf) proves that a generator-preserving quotient onto a C-group is a C-group when it is injective on every maximal parabolic. The authors explicitly extend the McMullen–Schulte quotient criterion. M1 exposes the remaining kernel obstruction when local faithfulness is relaxed; it should not be presented as inventing the quotient method.

We also use the established recursive recognition theorem: a string-generated group is a string C-group when its two end-deleted subgroups are string C-groups and their intersection is the middle subgroup. This is a recognition criterion, not by itself a solution to any family-specific intersection problem.

### M2. Marked coordinates and symmetry stabilizers

If W is a universal marked group, D acts on W by allowed changes of marking, and W/N is a marked quotient, the changes that descend are exactly `Stab_D(N)`. If `N=MR`, with R normal and D-invariant, then

    Stab_D(M) <= Stab_D(N).

**Proof.** An automorphism fixing M and R fixes their product. ∎

An invertible word substitution is another coordinate system on the same marked group. For example,

    alpha_i = sigma_1 ... sigma_i,
    sigma_i = alpha_(i-1)^(-1) alpha_i,       alpha_0=1,

and `alpha_i^(-1)alpha_j=sigma_(i+1)...sigma_j`. The last identity gives an explicit dictionary between the subgroups occurring in the two intersection formulations. This dictionary must be supplied; saying merely that two tuples generate the same group would not suffice.

For chirality, D contains the relevant reflection of the marking. For triality without duality, the required stabilizer can be C3 inside S3. Preserving a subgroup of diagram symmetries does not automatically exclude additional geometric automorphisms.

### M3. Rank reduction

For an irreducible rank-r string C-group, r>=4, the replacement

    (rho_0,rho_1,rho_2,rho_3,...)
       -> (rho_1,rho_0 rho_2,rho_3,...)

again gives a string C-group of rank r-1 if `rho_0 in <rho_0 rho_2,rho_3>`. In particular, an odd order for rho_2 rho_3 suffices: raising rho_0 rho_2 rho_3 to that odd order recovers rho_0.

This is [Brooksbank–Leemans, Theorem 1.1 and Corollary 1.2](https://arxiv.org/pdf/1812.01055). The preservation of IP is their nontrivial contribution. Importing it into the core is useful compression for later applications, but is not an independent proof that the originating paper was unnecessary. Reversing this operation has additional hypotheses; the rank-augmentation paper supplies explicit failures of an unrestricted inverse.

### M4. Separate subgroup positions by field parameters

For subfields E,F of L, k=E intersect F, and `U(t)=I+tE_12`, direct entry comparison proves

    SL_n(E) intersect U(t)SL_n(F)U(-t)
       = C_(SL_n(k))(E_12),                       if t not in E+F.

If t=e+f with e in E and f in F, the intersection is `U(e)SL_n(k)U(-e)`. The proof and precise projective-center conditions are in [general_framework.md](general_framework.md); the entrywise equivalence is checked in [TransvectionIntersection.lean](formal/TransvectionIntersection.lean).

A useful extension replaces one shear by several. Suppose E,F are contained in K, N_1,...,N_r are square-zero matrices over k, and z has degree at least 3^r over K. Put `t_i=z^(3^(i-1))` and `U=product_i(I+t_iN_i)`. Then

    SL_n(E) intersect U SL_n(F) U^(-1)
       = C_(SL_n(k))(N_1,...,N_r).                 (*).

**Proof.** Expand U^(-1)MU as a polynomial in formal parameters T_i. Each T_i occurs once in U and once in its inverse, so its degree is at most two. Substituting the indicated powers of z sends distinct monomials to distinct powers z^j, 0<=j<3^r. These powers are linearly independent over K. If the evaluated conjugate is B over F, the constant coefficient of `U^(-1)MU-B` gives M=B, so M is over k. The coefficient of T_i gives `[M,N_i]=0`. Conversely, common centralizers are fixed by U. Square-zero matrices ensure every factor has determinant one. ∎

This is a uniform intersection theorem with an explicit extension-degree cost. It assumes neither the desired intersection nor group generation. For n=3, N_1=E_12 and N_2=E_23, the common centralizer consists of `aI+bE_13` with a^3=1. Over F3 it is exactly a cyclic group of order three. Thus two suitably positioned copies of SL_3(F3) inside SL_3(F_(3^9)) have that intersection. Whether specified generators of those copies generate an intended ambient group is a separate question.

The full statement and exact 5,616-matrix check are in [multiple_twist_theorem.md](multiple_twist_theorem.md) and [multiple_twist_check.log](multiple_twist_check.log). The extension-degree bound is sufficient; optimality is not claimed.

### M5. Primitive polynomial values

Let P be squarefree of degree D over F_Q, with P(0)!=0, Q odd. Write n=Q-1, `W(n)=2^omega(n)`, `theta(n)=phi(n)/n`, and let Z be the number of primitive roots of P. The number of primitive x for which P(x) is a nonzero square is positive whenever

    n > D W(n) sqrt(Q) + Z/theta(n).

**Proof.** Expand the primitive-element indicator in multiplicative characters. For every character psi, Weil's distinct-root bound gives

    abs(sum_(x!=0) psi(x) chi(P(x))) <= D sqrt(Q).

For a nontrivial psi, write psi=eta^j and use `eta(X^j P(X)^(n/2))`: it has D+1 distinct roots and is not an n-th power, because each root of P has multiplicity n/2. The trivial psi case follows by removing x=0 from the quadratic-character bound. Summing the squarefree-divisor weights yields error at most `theta(n)D W(n)sqrt(Q)`. Subtracting the Z primitive zeros gives the stated criterion. ∎

This invokes Weil's theorem rather than deriving it. The full norm-polynomial specialization, finite reduction and eleven witnesses are in [psl2_square_proof.md](psl2_square_proof.md). The arithmetic input is distinct from group intersection transport, and its cost is explicitly visible.

## 2. Reductions with actual hypotheses checked

### A. Endpoint twists in arbitrary rank

Let `(G;rho_0,...,rho_(r-1))` be any string C-group and c a central involution in an external C2. Replace rho_0 by `(rho_0,c)` and the other generators by `(rho_i,1)`; take the subgroup H they generate. This is again a string C-group.

**Proof.** Induct on r. For rank two, two distinct involutions give the required dihedral C-group. The end-deleted subgroup omitting rho_0 is unchanged and projects injectively; the other end-deleted subgroup is an endpoint twist in smaller rank and is a C-group by induction. Their images have the right intersection. The kernel has trivial intersection with the first subgroup, so M1 gives their correct intersection upstairs. Recursive recognition finishes the proof. ∎

Every hypothesis is checked in this argument. This recovers the endpoint sesqui-extension statement quoted as Proposition 2.2 in [Leemans–Mulpas, *Two gluing methods*](https://arxiv.org/pdf/2504.17535). It removes a recurring subsidiary proof in several construction papers. It does not prove the full gluing theorem, whose support geometry and group generation remain essential.

### B. Congruence covers of a verified lattice seed

Let W be a string group generated by involutions. Suppose `N normal in W`, `N isomorphic to Z^d`, W/N is a finite string C-group, and N intersects every proper distinguished parabolic trivially. Then for every positive integer m,

    W/mN is a string C-group of order |W/N| m^d,

with the same proper distinguished parabolics. If W/N is solvable, W/mN is solvable.

**Proof.** The subgroup mN is characteristic in N and hence normal in W. The new projection has kernel N/mN of order m^d. It is injective on every proper parabolic, so M1, or the recursive criterion with M1, establishes IP. The extension of a solvable group by an abelian group is solvable. ∎

This compresses the propagation step in [Hou–Feng–Leemans, *Regular 3-polytopes of order 2^n p*, Theorem 5.1](https://arxiv.org/pdf/2001.02945): their three index-192, index-384 and index-768 rank-three lattices give the three families with orders 192m^3, 384m^3 and 768m^3. Their generators have adjacent products of order six already in W, and the seed quotient has the same orders, verifying faithful dihedral parabolics. **The three lattice assertions and finite seed quotients are retained as the paper's certified input, not claimed to have been reconstructed from M1.** The generic m-dependent argument is eliminated; discovering the lattices is not.

### C. All symmetric-group ranks from one explicit seed

For S_n use `rho_i=(i+1,i+2)`, 0<=i<=n-2. These adjacent transpositions generate S_n; distant ones commute and adjacent products have order three. A subset of the generators gives the product of symmetric groups on the interval components of its edges in the path on n vertices. Intersecting two such groups preserves the common refinement of those interval partitions, exactly the subgroup from their common edge set. Thus IP is verified directly.

M3 now gives every rank from n-1 down to three. This is a complete short derivation of the existence part of Fernandes–Leemans' [*Polytopes of high rank for the symmetric groups*, Theorem 3](https://doi.org/10.1016/j.aim.2011.08.006), with no family-specific generation or IP assumption left unproved. Brooksbank–Leemans explicitly identify this consequence in their Section 3. It does not prove the former paper's uniqueness classifications at the top ranks; those have different content, including a subsequent corrigendum.

The 2011 paper is an additional verified consequence, outside the 36-paper primary-text sample: its exact theorem is identified in the fully read rank-reduction source, while the original publisher page and corrigendum were checked rather than a full original PDF.

### D. Characteristic-two rank intervals

The published highest-rank seeds for `O^±(2m,2^k)` and `Sp(2m,2^k)`, k>=2, have adjacent products of odd order 2^k+1. Successive M3 reductions therefore give all ranks three through 2m and 2m+1 respectively. This is exactly Brooksbank–Leemans Theorem 1.4, proved from Brooksbank–Ferrara–Leemans Corollary 1.5. It replaces separate constructions at each lower rank by one argument. Constructing the correct quadratic forms, controlling Witt type and proving that the symmetries generate the full highest-rank group remain essential seed work.

### E. Change of coordinates in the chiral enumeration algorithm

In [Buekenhout–Leemans–Tranchida, Theorem 4.3](https://arxiv.org/pdf/1912.02287), take the two substitutions displayed in M2. They are inverse by cancellation. Every product sigma_i...sigma_j is alpha_(i-1)^(-1)alpha_j. Hence its order condition is exactly the corresponding condition in the other marking, and the subgroups used in the two IP formulas are equal term by term after the index shift. Generation is preserved by the inverse word formulas. This proves the stated bijection.

This is a genuine theorem-level reduction with no unverified IP left over. The paper's algorithm and performance analysis do additional work. Counting the coordinate identity as a replacement for that entire paper would exaggerate the result.

### F. Two new outputs from the same interface

The central cyclic lift in [central_lift_proof.md](central_lift_proof.md) uses M1 to preserve the cyclic intersection and M2 to exclude an introduced reversing automorphism. The kernel is generated by a power of one marked generator, so its invariance is explicit. This fills the missing even-exponent non-tight existence range, conditional only on the source's established seed construction, whose hypotheses are checked there.

For the PSL(2) construction, M5 supplies a primitive-square parameter, and M4 computes the normalized intersection. The gcd calculation proves a structural obstruction as well: nonnested coefficient fields intersecting in F_(p^g) give a common unipotent subgroup of order p^g. The desired middle subgroup has order p, so the source construction works precisely in the coprime case. [psl2_chiral_corollary.md](psl2_chiral_corollary.md) separately checks generation using Dickson's list and chirality using the semilinear automorphism theorem and an explicit trace calculation. These dependencies are the real remaining input; none is hidden inside a claim that the marking is already polytopal.

### G. A literal torsor gives residue connectivity

A further application, outside the 36-paper sample, addresses Conjecture 1 in Leemans' 2005 Van Nypelseer construction. A block residue of the Hermitian-unital geometry has its point set identified with the norm-minus-one vectors of a Hermitian plane. SU(2,q) acts freely and transitively on that set: it is an actual torsor. In an isotropic basis, upper and lower trace-zero unipotents move each vector by an isotropic difference, which is exactly an allowed collinearity move in the residue. They generate SU(2,q), so their moves connect the torsor.

The underlying group-action fact is elementary: if a transitive group is generated by transformations carrying every vertex within its connected component, the graph is connected. The substantial application is the exact identification of the norm shell and permitted moves, rather than the word “torsor.” The [complete Hermitian proof](hermitian_unital_proof.md) also checks the other residues, firmness, and regularity on chambers under PGU(3,q). Its all-q argument has been internally reviewed and checked directly for q=2,3,4,5; external review and priority remain provisional. This supplies a further concrete geometric outcome without asserting that the five statements above alone prove every coset-geometric existence theorem.

### H. Two coset-geometry proof obligations disappear

For the standard parabolics of independent generators, thinness and residual connectedness force flag transitivity: the base-chamber orbit is closed under each unique adjacent-chamber move, and residual connectedness connects all chambers. In rank three, even the residue-connectivity hypothesis is automatic for standard pair-generated parabolics. Each singleton residue contains a connected spanning coset graph of its parabolic, since its two intersections contain the two distinguished generators. Every incident pair extends to a chamber by choosing a common coset representative.

These deductions rule out the two types of examples requested in *Highly symmetric hypertopes*, Problems 9.3 and 9.4, under that paper's standard construction. The [independent audit](hypertope_questions_independent_audit.md) gives the complete proofs and checks definitions, extra residue edges and the paper's examples. They remove genuinely redundant proof obligations; they do not assert that arbitrary C-group coset systems are thin or residually connected in higher rank. This is another application outside the fixed 36-paper sample, with historical priority still to be checked.

## 3. What the 36-paper test establishes

The CSV records exact theorem numbers when a paper uses them; otherwise it identifies the precise unnumbered proposition, census or algorithm section. The review inspected main statements and relevant proof nodes in the archived primary texts. It did not independently verify every classification table or every computational enumeration in all 36 papers. “High confidence” in the CSV refers to the dependency assessment, not to an independent reproof of each paper.

| Audit category | Papers | Meaning |
|---|---:|---|
| Fully rederived published theorem component | 1 | The chiral coordinate bijection, with relations and subgroup dictionary checked. |
| Identifiable construction tails compressed | 7 | A generic transport or rank-propagation step is reusable; substantial seed work remains. |
| Shared structure with essential separate proof | 18 | The compact core organizes the proof obligations but does not establish the selected main result. |
| Selected results outside this core | 8 | Counting, coding, metric or packing arguments need other mathematics. |
| Paper supplying a core theorem | 1 | Rank reduction is imported with credit, not counted as a consequence of itself. |
| Proposed new application to source conjectures | 1 | The PSL(2) conjectures and missing classification family; internal review, external review and novelty checks still distinguished. |

Thus there is verified compression of recurring proof components across multiple papers, plus complete short deductions for particular results. There is currently **no demonstrated reduction of dozens of entire papers to this core**. No percentage of pages “saved” is claimed: the audit did not measure line-by-line proof lengths, and a conditional reduction can conceal most of a paper if its hypotheses are allowed to include the hard result.

This distinction is constructive. It identifies the right reusable library: local subgroup diagrams, faithful-parabolic certificates, invariant kernels, seed lattices, generator substitutions, parameter-separation certificates, and primitive-value witnesses. Once a seed is certified, families can be generated and checked without repeating the transport proof. Classification and extremality require an additional completeness argument.

## 4. Essential assumptions and diagnostic counterexamples

**A quotient can create extra intersections.** In the Klein four group with independent x,y, the cyclic subgroups `<x>` and `<y>` intersect trivially. Quotient by `<xy>` identifies their images, whose intersection is then nontrivial. Thus quotienting a correct diagram need not preserve it. M1 applies in the upward direction only after the image diagram and the kernel condition are checked.

**String commutations are insufficient.** The faithful thin non-polytopal maniplex construction gives a stronger warning than a random failed tuple: even natural geometric-looking cover conditions need not guarantee polytopality. The explicit failure must be located in the intersection or flag structure.

**Generic position has a calculable residual symmetry.** A single transvection in dimension at least three leaves a substantial centralizer. M4 predicts that obstruction and the multi-parameter version removes it to a chosen common centralizer. This is a specific improvement over “choose matrices generically.”

**Rank reduction is directional.** Its word substitution can lose generation when applied without the membership condition. The rank-augmentation paper has additional orbit conditions because the inverse problem does not inherit IP for free. The A11 rank gap is another concrete warning against assuming every rank can be interpolated.

**Unitary conditions do not follow from replacing a field parameter.** The [unitary transfer obstruction](unitary_transfer_obstruction.md) gives an explicit determinant showing that the naive unit-circle substitution in the known PSL(3) triple preserves no nonzero Hermitian form in the stated range. A useful theory predicts this failure and directs a new construction, rather than relabeling it PSU(3).

**An already-solved target is not a new consequence claim.** The augmentation-module example in the framework independently reproduces a family covered by Li–Zhang's 2025 `{n,n}` theorem. Its Type (2) existence question is therefore marked resolved. The fourfold odd-entry doubling operation remains a useful transparent transport example, without a priority claim.

## 5. Next concrete deliverables

The best next step is a library of **seed certificates and transport certificates**, not a larger vocabulary. A seed certificate should include explicit generators, element orders, the proper subgroup diagram, a generation certificate and the relevant symmetry stabilizer. A transport certificate should name its map, kernel, restriction on each local subgroup, and the M1/M2 hypotheses it verifies. For matrix groups it should also record coefficient fields and projective-center conditions.

This has testable benefits: one certified Z^d seed gives all its congruence covers; one odd-order highest-rank marking gives a whole verified rank chain; a suitable power kernel propagates chirality; prescribed square-zero matrices and sufficiently independent parameters realize their common centralizer as an exact subgroup intersection. None of these operations by itself proves that every group in a classification has a suitable seed. The compact theory earns its value by making the propagation proofs reusable and the remaining hard assertions explicit.

## Paper-by-paper index

The following index gives the audited target and verdict. The CSV additionally supplies the primary URL, local text, proof reduction and indispensable remaining input for every row.

| Paper | Exact target | Assessment |
|---|---|---|
| [L007: Chiral polytopes of order 2p m](https://amc-journal.eu/index.php/amc/article/download/3716/2232) | Theorems 1.1, 1.2, 1.4 | Transport tail |
| [L008: Testing chirality on hypertopes](https://arxiv.org/pdf/2511.14562) | Theorem 1.1 | Separate essential proof |
| [L009: Geometries with trialities arising from linear spaces](https://arxiv.org/pdf/2504.06025) | Theorems 1.1, 1.2 | Separate essential proof |
| [L010: Two gluing methods for string C-group representations of the symmetric groups](https://arxiv.org/pdf/2504.17535) | Theorem 1.1; Proposition 4.8 | Separate essential proof |
| [L011: On simple groups that admit a string C-group representation](https://dipot.ulb.ac.be/dspace/bitstream/2013/397490/3/simpleGroups6.pdf) | Theorems 1.1, 2.1 | Separate essential proof |
| [L012: Regular 3-polytopes of order 2 n p](https://arxiv.org/pdf/2001.02945) | Theorems 1.2, 1.3, 5.1; Corollary 5.2 | Transport tail |
| [L013: A note on girth-diameter cages](https://arxiv.org/pdf/2401.15539) | Section 4 unnumbered Proposition; Section 2 census | Outside core |
| [L014: String C-groups of order 4p m](https://arxiv.org/pdf/2407.10388) | Theorems 1.1, 1.2, 1.3 | Separate essential proof |
| [L015: Flag transitive geometries with trialities and no dualities coming from Suzuki groups](https://arxiv.org/pdf/2311.13522) | Theorems 3.2, 3.14, 3.16 | Separate essential proof |
| [L016: Faithful and thin non-polytopal maniplexes](https://arxiv.org/pdf/2305.01372) | Theorem 1.1; Proposition 5.7 | Separate essential proof |
| [L017: On trialities and their absolute geometries](https://dipot.ulb.ac.be/dspace/bitstream/2013/375808/3/revisionAbsolute.pdf) | Theorems 3.11, 3.13 | Separate essential proof |
| [L018: There is no perfect Mondrian partition for squares of side lengths less than 1001](https://arxiv.org/pdf/2311.02385) | Title/abstract theorem; Sections 2-4 computational exclusion | Outside core |
| [L019: The number of string C-groups of high rank](https://arxiv.org/pdf/2212.12723) | Theorem 1.1 | Separate essential proof |
| [L020: A rank augmentation theorem for rank 3 string C-group representations of the symmetric groups](https://arxiv.org/pdf/2212.12563) | Theorem 4.1 | Separate essential proof |
| [L021: Maniplexes with automorphism group PSL(2,q)](https://dipot.ulb.ac.be/dspace/bitstream/2013/359689/3/projectivemaniplexes_final.pdf) | Theorems 3.10, 4.4 | Separate essential proof |
| [L023: Incidence geometries with trialities coming from maps with Wilson trialities](https://arxiv.org/pdf/2208.08215v2) | Theorems 3, 10 | Separate essential proof |
| [L024: String C-groups with real Schur index 2](https://arxiv.org/pdf/2201.01313) | Section 3 PSU(5,3) example; Theorem 4 | Outside core |
| [L025: Edge-girth-regular graphs arising from biaffine planes and Suzuki groups](https://arxiv.org/pdf/2108.06636v1) | Theorems 2.1, 3.1, 4.3 | Outside core |
| [L026: The String C-group representations of the Suzuki, Rudvalis and O'Nan sporadic groups](https://adam-journal.eu/index.php/ADAM/article/download/1405/1405) | Sections 3-4 algorithms; Section 5.3 O'Nan counts | Separate essential proof |
| [L027: On chiral polytopes having a group PSL(3,q) as automorphism group](https://dipot.ulb.ac.be/dspace/bitstream/2013/333283/3/psl3-final.pdf) | Theorems 1.1, 1.2, 1.3 | Separate essential proof |
| [L028: A new algorithm to classify chiral polytopes with a given automorphism group](https://arxiv.org/pdf/1912.02287v1) | Theorem 4.3; Sections 4.2-4.3 | Verified component |
| [L029: On residual connectedness in chiral geometries](https://arxiv.org/pdf/1911.03227v1) | Theorem 1.1 | Separate essential proof |
| [L030: An infinite family of locally X graphs based on incidence geometries](https://arxiv.org/pdf/1811.11438v1) | Theorem 4.9; Corollaries 4.10-4.11 | Outside core |
| [L031: Orthogonal groups in characteristic 2 acting on polytopes of high rank](https://arxiv.org/pdf/1709.02219) | Theorem 1.4; Corollary 1.5 | Transport tail |
| [L032: On regular polytopes of 2-power order](https://dipot.ulb.ac.be/dspace/bitstream/2013/292444/3/HRRPR-revised.pdf) | Theorem 1.2 | Transport tail |
| [L034: Existence of regular 3-hypertopes with 2 n chambers](https://arxiv.org/pdf/1901.09034v1) | Theorem 3.2; Proposition 2.1 | Transport tail |
| [L035: 2-groups behaving as automorphism groups of regular 3-polytopes](https://arxiv.org/pdf/1802.08947v2) | Theorems 1.2, 1.3 | Transport tail |
| [L037: Rank reduction of string C-group representations](https://arxiv.org/pdf/1812.01055) | Theorem 1.1; Corollaries 1.2-1.3; Theorem 1.4 | Core source |
| [L038: String C-group representations of alternating groups](https://arxiv.org/pdf/1810.12450) | Theorem 1.1; Theorem 4.1 | Transport tail |
| [L039: Groups of Ree type in characteristic 3 acting on polytopes](https://arxiv.org/pdf/1501.01125) | Theorem 1 | Separate essential proof |
| [L043: Projective linear groups as automorphism groups of chiral polytopes](https://arxiv.org/pdf/1606.08017) | Conjectures 6.1, 6.2; missing family in introduction classification | New application |
| [L044: Highest rank of a polytope for A n](https://arxiv.org/pdf/1605.09173v1) | Theorem 1.1 | Separate essential proof |
| [L050: Linear codes with complementary duals from some strongly regular subgraphs of the McLaughlin graph](https://www.mathos.unios.hr/mc/index.php/mc/article/download/1537/388) | Theorem 1; Propositions 1-5 | Outside core |
| [L063: The rank two geometries of the PSL(2,q) groups : part II](https://amc-journal.eu/index.php/amc/article/download/181/241) | Theorem 1.1; Tables 1-6 | Separate essential proof |
| [L066: On pairs of commuting involutions in Sym(n) and Alt(n)](https://math.uni.lu/kiefer/Publications/Involutions.pdf) | Theorems 1.1, 1.2 | Outside core |
| [L074: On the number of abstract regular polytopes whose automorphism group is a Suzuki simple group Sz(q)](https://math.uni.lu/kiefer/Publications/szpoly3%20r%C3%A9vis%C3%A9.pdf) | Theorems 1, 2 | Outside core |
