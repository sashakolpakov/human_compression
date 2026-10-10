# What is settled in the toroidal question

For the ordered local parameters

$$
((3,0),(2,0),(1,1),(s,0)),
$$

the repository proves that finite regular hypertopes exist for every
integer $s\ge2$. It also proves that the exact universal groups are
infinite for every $s\ge6$.

These statements answer two different readings of Problem 9.2 in
Fernandes–Leemans–Ivić Weiss, *Hexagonal extensions of toroidal maps and
hypermaps* (2018). The distinction concerns whether additional global
relations are allowed.

A **universal group** imposes only the prescribed defining relations.
A **finite example** can be a quotient of that group obtained by adding
relations, while keeping the required local residues unchanged. An
infinite universal group can therefore have the required finite examples.

## The source wording and the answers

The [source reading](research/case_study/phase35_L003_problem92_scope.md)
records the exact page references. Table 8 lists finite universal
examples at $s=2,3,4,5$. The following paragraph suggests an infinite
family of finite hypertopes. The numbered problem asks for an infinite
family with the displayed parameters, without expressly requiring
universality or finiteness.

| Reading | Answer and proof |
|---|---|
| Finite examples for infinitely many parameters | Yes; the stronger all-parameter result holds. |
| A finite example for every integer $s\ge2$ | Yes; the [finite construction and geometric proof](research/case_study/phase35_L003_tensor_geometry.md), together with the retained small bases. |
| A universal regular hypertope for every integer $s\ge2$ | Yes; the [universal-object argument](research/case_study/phase35_L003_all_universal.md). These objects need not be finite. |
| Finite universal groups for every integer parameter | False; the [triangle-group quotient proof](research/case_study/phase38_L003_universal_triangle.md) proves infinitude for every $s\ge6$. |
| A complete description of the universal groups | Not established. Their full structure is a separate classification problem. |

If the family must literally contain the four original table entries,
choose those entries at $s=2,3,4,5$ and the constructed examples thereafter.
Retaining the source's computed finiteness at those four parameters gives
the exact finite-parameter set $\{2,3,4,5\}$ for the universal groups.
The new infinitude proof does not use those computations.

## Proof and attribution

The finite construction uses the earlier tensor marking and exact local
groups. The universal-object proof transports the intersection and coset
conditions through a quotient whose maximal marked parabolics inject.
The infinitude proof is independent of those geometric arguments: a
subgroup of an explicit wreath-product quotient surjects onto a triangle
group, whose real reflection representation has an infinite-order element.

Lean proves infinitude of the exact presentations for every $s\ge6$.
The final theorems assume only that numerical condition. See
[TriangleReflection.lean](research/case_study/formal/TriangleReflection.lean),
its [scope](research/case_study/formal/TriangleReflection.scope.md), and the
[independent review](research/case_study/phase42_triangle_spectral_audit.md).
The identification with regular geometries and the finite construction
remain separately reviewed written mathematics.

The source question, presentations and four small universal examples
retain their original attribution. Historical priority is unverified;
possible overlap with Zhang's 2024 *Abelian covers of regular hypertopes*
has not been resolved from its complete text. This page explains the
existing results and changes neither the question count nor the
compression accounting.
