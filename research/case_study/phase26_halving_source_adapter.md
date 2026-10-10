# Existing geometric halving and the abstract support test

Private source-bound adapter, 10 October 2026. This note attributes the existing geometric results precisely and diagnoses the scope of the new abstract criterion. It does not claim a new solution or rederive an entire cited paper. Source access is recorded in [phase26_access.md](phase26_access.md).

## 1. Exact attribution and hypotheses

The source is C. A. Piedade and P. Tranchida, *Constructing new geometries: a generalized approach to halving for hypertopes*, [arXiv 2405.19050v1](https://arxiv.org/abs/2405.19050v1), 29 May 2024. The cached PDF is `sources/halving_hypertopes2025.pdf`; the basename is not its version date.

For a regular hypertope with a $(0,1)$ leaf, write $a=\rho_0$, $b=\rho_1$, $R=\langle\rho_i:i\ge2\rangle$ and $P=\langle b,R\rangle$. The leaf assumption gives $[a,R]=1$. The source imposes:

- **B1:** its vertex-edge truncation is a simple graph;
- **B2:** an edge is incident with a higher-type object exactly when both its endpoints lie in that object's vertex shadow.

Lemma 4.5 (pp.14–15) proves B1 equivalent to $P\cap P^a=R$. Proposition 4.7 (p.15) obtains failure of the new C-group property when B1 fails. Theorem 4.4 (p.14) identifies the halving coset system with a regular hypertope under **both B1 and B2 and the original regular-hypertope hypothesis**. The construction separates the bipartite and nonbipartite cases. These are existing primary-source geometric results; the overlap identity is not newly attributed to this project.

Selected reading includes the definitions and geometric constructions in §§1,3, Theorem 4.1 and its retained-source explanation, the full proof of Theorem 4.4, and §4.2 through Proposition 4.7 and Examples 4.8–4.9. The 2000 original remains only partially accessible; its numbering is reported through this primary follow-up rather than promoted to an original full reading.

## 2. What the support filter adds outside those hypotheses

For the abstract old C-group define, for a subset $J$ of the remaining labels,

$$U_J=\langle a,b,R_J\rangle,\qquad H_J=\langle aba,b,R_J\rangle,$$
$$\mathcal F=\{J:a\in H_J\}.$$

The abstract [halving criterion](phase26_halving_core.md) states that the new marking is a C-group exactly when the overlap identity holds and $\mathcal F$ is intersection closed. It assumes the old subgroup intersection property and $[a,R]=1$, but no underlying flag-transitive geometry. Its second test is therefore a statement about information that a general C-group marking may lose.

The cited paper does **not** state this filter criterion. Its joint geometric hypotheses nevertheless imply it: Theorem 4.4 gives a regular hypertope for the new marking, so the new marking has the subgroup intersection property. In particular,

$$H_I\cap H_J=H_{I\cap J}.$$

If $a$ belongs to both groups on the left, it belongs to the group on the right. Hence $\mathcal F$ is intersection closed. This implication uses the cited conclusion, not an unproved identification of B2 with the filter. It neither shows that B2 is necessary nor that the original geometric hypothesis may be omitted.

The source itself gives a hemicube example where B2 fails but halving still works. Thus B2 is a sufficient geometric condition in this theorem, while the abstract filter is an exact algebraic condition paired with the overlap identity. The two should not be presented as equivalent.

## 3. Exact separation supplied by the six-point example

Consider

$$a=(12),\quad b=(13)(24)(56),\quad c=(45),\quad d=(46)$$

in $S_6$. The original marking has the full subgroup intersection property; its overlap is $P\cap P^a=\langle c,d\rangle$. Yet

$$\mathcal F=\{\{c\},\{d\},\{c,d\}\}$$

fails intersection closure. The abstract note gives the resulting failure of new marked intersections. The additional question is whether this example satisfies the hypotheses of the published geometric theorem.

The standalone [coset checker](phase26_s6_geometry_check.py) answers this without assuming a geometry. It constructs all typed left cosets of the old maximal parabolics and checks every pairwise-incident family, all possible chamber extensions, and both local graph conditions. The [exact report](phase26_s6_geometry_check.json) gives:

| Quantity | Exact result |
|---|---:|
| Old group order |720|
| Old subgroup-IP meets checked |256|
| Maximal parabolic orders |48,12,72,72|
| Type-set sizes |15,60,10,10|
| Full chambers |720|
| Pairwise-incident flags with no common group element |90|
| Flags not contained in any chamber |90|
| Types of every such flag |$\{0,2,3\}$|
| B1 and B2 |both true|

All other typed flags have a common group element. The full chambers form the usual 720-element orbit, but the extra 90 rank-three flags have no completion. Therefore the old coset incidence is **not a geometry**, and it is not a regular hypertope. Chamber transitivity on the full chambers does not fix the missing-completion problem.

This example does not contradict Theorem 4.4. It shows why its original geometric hypothesis matters: even B1, B2, and the old subgroup-IP do not imply the abstract support test. No conclusion is drawn here about whether some weaker geometric hypothesis would already force the filter.

There is also a direct combinatorial description, independently identified during the rank review. Type 0 objects are the two-element subsets of six points, and type 1 objects are the edges of the Johnson graph $J(6,2)$. Types 2 and 3 are two copies of the unordered $3+3$ partitions. A vertex is incident with a partition when its two points lie in opposite parts; an edge is incident when both its vertices are; partitions of different types are incident exactly when distinct. For the base flag, the four stabilizers fix respectively $\{1,3\}$, the Johnson edge $\{\{1,3\},\{2,3\}\}$, the partition $125\mid346$, and the partition $126\mid345$. Their orders agree with the full stabilizers, identifying this model with the coset incidence.

Now take the vertex $\{5,6\}$ and the two partitions $126\mid345$ and $125\mid346$. This is a flag. The vertices crossing both partitions are precisely $\{i,j\}$ with $i\in\{1,2\}$ and $j\in\{3,4\}$, together with $\{5,6\}$. The last vertex is isolated in the induced Johnson graph. Thus no incident type 1 object completes this flag. This explains the failed geometry axiom without relying on the numerical count.

Reproduce the diagnostic with `python3 phase26_s6_geometry_check.py --output /tmp/S6-halving-geometry.json`, using a new output path. It uses only standard-library permutation arithmetic, no group catalogue or external geometry package. The explicit first failing coset family is retained in the JSON. This is one exact example, not a classification or proof of the general criterion.

## 4. The lattice and matching-diagram bridges

Montero–Weiss, [arXiv 2001.11082v1](https://arxiv.org/abs/2001.11082v1), §3, assumes a regular polytope whose face poset is a lattice. Reverse their generator order to compare with $a\mapsto aba$. The special endpoint-parabolic meet in Theorem 3.1 is precisely the overlap above: an automorphism fixing two adjacent facets fixes their unique common ridge. The lattice condition supplies that unique ridge. Their other meets are handled by the old string subgroup-IP, direct products, and induction through sections. Proposition 3.2 supplies flag transitivity separately, using the cited tail-triangle semiregular-polytope result. The current algebraic overlap proof does not eliminate that retained geometric input merely by changing notation.

Piedade's [2023 paper](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v30i2p20/pdf/), §§2.3–2.4, combines this halving theorem with a matching diagram on the antipodal vertex pairs of a centrally symmetric polytope $\mathcal P$. For the following order calculation, assume a finite centrally symmetric regular polytope $\mathcal P$ and an integer $2\le s<\infty$, as in the cited finite families. The diagram group has one dihedral factor of order $2s$ per antipodal pair. With $m=|V(\mathcal P)|/2$, the extended group is

$$D_{2s}^{\,m}\rtimes\operatorname{Aut}(\mathcal P).$$

Consequently its order is $(2s)^m|\operatorname{Aut}(\mathcal P)|$. The halving subgroup has half this order in the paper's families, because the presentations preserve the parity of the added endpoint generator. This is the coordinate-product and index-two portion that the common marked-action machinery immediately explains.

For example, the $n$-orthoplex has $2n$ vertices and automorphism-group order $2^nn!$. The extended order is $(4s)^nn!$ and the halved order is $(4s)^nn!/2$, agreeing with Proposition 13's order formula. The asserted geometry, explicit relator reductions, local residue types, and other families still require their stated construction inputs and source-specific verifications. This intake does not assign a whole-paper reduction on the strength of the order calculation.

## 5. Distinguish three operations

The geometric Petrial in the 2001 paper replaces faces by sets traversed by a chamber walk; the action can acquire a kernel when the result is not thin. Endpoint halving replaces one involution by the conjugate of its neighbour and may change the ambient group by index two. The higher-rank Petrie-like/rank-reduction operation attributed to the 2008 paper can remove a generator by a commuting product. Similar terminology does not identify these operations or transfer their hypotheses. The retained marking, the actual subgroup intersections, and the existence of all geometric flag completions must each be checked.
