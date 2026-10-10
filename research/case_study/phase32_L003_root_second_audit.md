# Second review of the exact translation-kernel computation

Internal mathematical and code review, 10 October 2026. The reviewed source is phase32_L003_root_check.py; the companion JSON binds its exact hash. No author or root file was edited. A fresh unchanged execution wrote phase32_L003_root_second_run.json, byte-identical to the saved root report.

**Result: PASS.** The specific certified monomial image has a translation kernel isomorphic to \(\mathbb Z^6\), with permutation quotient of order 216. This does not identify the original presented group with its image.

## Right-action and kernel checks

For pairs \((p,v)\), the program composes the first action followed by the second as
\[
(p,v)(q,w)=(q\circ p,\ v+w\circ p).
\]
The inverse is \((p^{-1},-v\circ p^{-1})\). Both formulas agree with the action \((i,n)\mapsto(p(i),n+v(i))\); the source words and the witness are evaluated with the correct convention.

The breadth-first search starts at the identity, closes under the three permutation generators, and finishes with exactly 216 permutations. Since it is a finite set of permutations closed under the generators, it is their full subgroup; inverse powers are already present. Each stored lift maps to its dictionary key. This enumeration is independent of the earlier GAP quotient or its claimed order.

Let \(t_q\) be the chosen lifted representative of a quotient element \(q\), with \(t_1=1\). For each generator \(a\), the computed element
\[
t_q\,a\,t_{q\bar a}^{-1}
\]
has trivial permutation. These are the right Schreier generators of the kernel. To see that only positive letters are needed, the loop for \(a^{-1}\) starting at \(q\) is the inverse of the loop for \(a\) starting at \(q\bar a^{-1}\). Telescoping any kernel word with the representatives therefore writes it in the 648 computed loops and their inverses. A Schreier-tree or a prefix-closed transversal is not needed for this generating argument.

The kernel is a subgroup of the additive group \(\mathbb Z^{216}\): a trivial permutation acts by its integer voltage vector, and the monomial representation is injective on these vectors because \(2^u=2^v\) implies \(u=v\). Thus no additional scalar or matrix kernel is hidden.

## Exact rank computation

The row reduction uses Fraction throughout. Its pivot positions need not increase numerically: the invariant is that each new normalized basis vector is zero at all **earlier selected** pivot positions and one at its own new pivot. Subsequent elimination preserves earlier zeros. Each accepted row therefore increases the rational rank by one.

Six original integer rows are accepted. Every one of the 648 Schreier vectors is then independently reduced to zero against the resulting basis. This proves rational rank exactly six, not merely a lower bound. A finitely generated subgroup of \(\mathbb Z^{216}\) is free abelian, and its free rank equals its rational span dimension; hence the kernel is abstractly \(\mathbb Z^6\). No saturation, lattice index, particular integral basis, splitting of the extension, or isomorphism of the whole image with a semidirect product is asserted.

## Finite quotient corollary

Let \(L\) be that translation kernel and \(H\) the certified image. For every integer \(m\geq1\), the subgroup \(mL\) is characteristic in \(L\), hence normal in \(H\). The exact sequence with permutation quotient of order 216 therefore gives
\[
 |H/mL|=216\,|L/mL|=216m^6.
\]
Every finite subgroup of \(H\) injects into every such quotient, because its intersection with the torsion-free subgroup \(mL\) is trivial. This statement concerns already established finite subgroups of the image. It neither identifies the source's prescribed local groups with subgroups of \(H\) nor proves that subgroup intersections or typed coset Helly survive the quotient.

## Execution scope

The fresh run verified all 2,160 relator-state equalities, exact parameter-word order six, the infinite translation witness, the entire finite permutation image, all 648 kernel translations and the rank-six elimination. It used the Python standard library only. This review does not establish geometric realization, exact residue preservation in finite quotients, current priority, or resolution of L003 Problem 9.2.
