# Quotient transport with one exceptional maximal parabolic

Date: 2026-10-10. Separate extension of the frozen phase32 transport lemma.

Let a group homomorphism \(f:G\to\bar G\) preserve a marked subgroup family
\(G_A\), indexed by arbitrary subsets of a type set \(I\). Assume that this
family is monotone, \(G_I=G\), and its exact image family has the full
intersection property. Choose one type \(e\in I\). Suppose \(f\) is injective
on \(P_i=G_{I\setminus\{i\}}\) for every \(i\ne e\). No injectivity hypothesis
is imposed on \(P_e\).

**Theorem.** The original marked family has the full intersection property.
If the maximal image parabolics have typed right-coset Helly, so do the original
maximal parabolics. The groups and type set may be infinite; global surjectivity
of \(f\) and centrality of its kernel are unnecessary.

Here typed Helly means that every pairwise-intersecting family of right cosets,
with at most one coset per type, has a common point. It includes arbitrary
selected type subsets, not just finite ones.

For the subgroup assertion, a proper generator subset \(A\) lies in an
injective maximal parabolic unless \(A=I\setminus\{e\}\). Indeed, absence of
an omitted type other than \(e\) forces precisely that equality. Given two
distinct proper subsets, at least one is therefore protected by injectivity.
If \(x\in G_A\cap G_B\), image IP supplies \(y\in G_{A\cap B}\) with
\(f(y)=f(x)\). Both lie in the protected subgroup, so \(x=y\).
Equal subsets and any full subset give tautological intersections.

For the coset assertion, image IP and the newly proved original IP give
\(f(P_i\cap P_j)=f(P_i)\cap f(P_j)\). Empty or singleton selected families
have an immediate common point. Any other selected family has a type
\(k\ne e\), which can anchor the lift. Take a common image point supplied by
downstairs Helly and lift it through the selected \(P_k\)-coset. For every
other type \(i\), choose an old pairwise intersection point with that anchor.
The difference from the proposed lift lies in \(P_k\) and its image lies in
\(f(P_i)\cap f(P_k)\). The exact image-meet equality supplies a matching
element of \(P_i\cap P_k\); injectivity on \(P_k\) identifies the two. Thus
the proposed lift belongs to every selected coset.

This last argument also proves a standalone form: for an arbitrary family
\(P_i\), exact mapped pair intersections, downstairs typed Helly, and
injectivity on all but one family member imply upstairs typed Helly. No
generator-subset indexing is needed for that standalone statement.

[OneExceptionalParabolic.lean](formal/OneExceptionalParabolic.lean) formalizes
the standalone and combined statements, importing the unchanged definition
from [ParabolicQuotientTransport.lean](formal/ParabolicQuotientTransport.lean).
The successful Lean report contains only the standard axioms `propext`,
`Classical.choice`, and `Quot.sound`; it contains no `sorry` or native evaluation
axioms. The finite groups, presentation words, and incidence-geometric adapter
needed for any application remain outside this module. In particular, this
general result alone makes no claim about a varying toroidal parameter or an
infinite family of source geometries.
