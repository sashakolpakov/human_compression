# Two retained classification inputs for the Steiner module

The reductions in this module use two classification theorems. Their proofs and their dependence on finite-group classification remain credited to the original authors. Neither theorem is claimed as a consequence of the elementary residue recursion.

## Locally two-transitive linear spaces

The primary source is F. Buekenhout, P.-O. Dehaye and D. Leemans, *RWPRI and (2T)₁ Flag-transitive Linear Spaces*, Beiträge zur Algebra und Geometrie **44** (2003), 25–46. The retained PDF is sources/older_L102_gwdg.pdf, SHA256 94cc12d9f5ab55f087c596095b87c1a326b4858ba5e1c611d2f07749fdee1ad6.

The exact input is **Theorem6.2, pp42–43**, under the hypotheses that the linear space is finite and the group acts faithfully and flag-transitively, and that each point and line stabilizer acts doubly transitively on its incident objects. Its six numbered possibilities consist of:

1. AG(2,4) with AΓL(1,16);
2. PG(n,q), n≥2, with PSL(n+1,q)≤G≤PΓL(n+1,q);
3. PG(3,2) with the exceptional A₇ action;
4. AG(n,q), n≥2 and q≥3, with its translation group and a linear stabilizer containing SL(n,q);
5. a Hermitian unital UH(q), with PSU(3,q)≤G≤PΓU(3,q);
6. a circle, meaning that every line has exactly two points, with one of the specified triply transitive point actions.

For the **thick** linear spaces in L092 Theorem2, the last possibility is excluded. The first five cases and their ranges agree exactly with the five clauses in L092. Some cases overlap at small parameters; the primary theorem explicitly permits this. In particular UH(2) and AG(2,3) must not be counted as disjoint families.

The proof on p43 reduces the list to Theorem6.1 and the earlier case analyses, citing Propositions5.6,3.3,3.6,3.8 and the unital discussion. The theorem is used as a retained classification, rather than charged as an additional result of the present manuscript. The elementary proofs B.ProjectivePlane, B.AffinePlane, B.SemilinearSixteen and B.SpaceObstruction then pay the construction-specific consequences of the projective and affine cases. The Hermitian case belongs to the separately audited unital work.

## Highly transitive Steiner systems

The primary source is W. M. Kantor, *Homogeneous Designs and Geometric Lattices*, Journal of Combinatorial Theory, Series A **38** (1985), 66–74. The author's [primary PDF](https://pages.uoregon.edu/kantor/PAPERS/homogeneousdes.pdf) is retained as sources/phase183_kantor_homogeneousdes.pdf, SHA256 36532c56e2af68c0b043c3b21818dbc71fe5ce250e9f380315e122842de308a2.

The exact input is **Theorem3 and its proof, p73**, with λ=1 understood from the design convention of the article, k≥t+1≥4, and a t-transitive group of automorphisms. Its three possibilities are the affine binary plane designs, projective subline designs, and the five Mathieu Steiner systems. L092 Theorem10 reproduces these possibilities. In the affine case the specified actions are 2ᵈ:GL(d,2) and, when d=4, 2⁴:A₇. The subline case has blocks the PGL(2,qᵉ)-images of GF(q)∪{∞}, e≥2, with a group containing PSL(2,qᵉ). The Mathieu parameters are (4,5,11), (5,6,12), (3,6,22), (4,7,23), and (5,8,24), with the indicated native Mathieu subgroup.

The proof supplies a useful extra restriction: the subline action is contained in PΓL(2,qᵉ). This follows from the complete list of triply transitive groups used there, and must be retained when bounding the fiber action. Merely retaining the displayed lower bound PSL≤G would not exclude other abstract overgroups. The complete finite-group classification in Section2 and the rank-two design classification in Theorem1 are part of this borrowed input.

Our finite Witt computations concern the standard permutation actions of the five named Mathieu groups. Their application to the classification is not an inference from design parameters alone. For the three large actions, the stabilizer of an ordered t-tuple has exactly one invariant subset of size k−t in its remaining point set: it is its unique orbit of that size, and every other orbit is larger. The unique block through that tuple is therefore forced. Since the group is t-transitive, its full block system is forced. For M₁₁ and M₁₂, enumeration of the k-subset orbits gives exactly one orbit of the requisite block count and no smaller orbits; a group-invariant block system of that size is again forced. These arguments identify the native block models within the retained permutation actions before any full automorphism or derived-plane computation is used.

The identification of the named Mathieu permutation actions in GAP with the classical actions in Kantor's theorem remains a library and classical-group input. The subsequent incidence checks, full design automorphism computations, and explicit PG(2,4) maps are separately reported finite computations. None is represented as a Lean proof or as a new classification of the Mathieu groups.
