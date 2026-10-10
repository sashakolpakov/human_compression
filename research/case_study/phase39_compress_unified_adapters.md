**Corollary D1 — L032 Theorem 1.2.** For every \(d\ge3\), \(n\ge5\) and \(k_1,\ldots,k_{d-1}\ge2\) with \(\sum_i k_i\le n-1\), there is a regular rank-\(d\) polytope with automorphism group of exact order \(2^n\) and type \(\{2^{k_1},\ldots,2^{k_{d-1}}\}\).

*Proof.* Corollary Q4.1 constructs its marked string C-group using the single square seed and independent cyclic edge kernels. Apply the retained regular-polytope correspondence. ∎

**Corollary D2 — L035 Theorem 1.2.** For \(n\ge10\), \(s,t\ge2\) and \(s+t\le n-1\), there is a regular rank-three polytope of order \(2^n\) and type \(\{2^s,2^t\}\).

*Proof.* Set \(d=3\) in D1. The construction and proof are shared, with no second seed. ∎

**Corollary D3 — L035 Theorem 1.3, all three parts and eight presentations.** Let \(n\ge10\). Every marked rank-three string C-group of order \(2^n\) and type \(\{4,2^{n-s}\}\), for \(s\in\{3,4,5\}\), is exactly one of the following marked presentations. Put \(m=2^{n-s}\), \(r=bc\), \(d_0=(ab)^2\), and \(z=r^{m/2}\). All have common relations
\[
a^2=b^2=c^2=(ac)^2=(ab)^4=r^m=1.
\]
For \(s=3\), add \([d_0,c]=z^\epsilon\), with \(\epsilon=0,1\), giving \(G_1,G_2\). For \(s=4\), add \([d_0,r^2]=z^\epsilon\), with \(\epsilon=0,1\), giving \(G_3,G_4\). For \(s=5\), add
\[
[a,r^2]^2=z^\beta,\qquad [a,r^4]=z^\nu,
\]
with \((\beta,\nu)=(0,0),(1,0),(0,1),(1,1)\), giving \(G_5,G_6,G_7,G_8\), respectively. Conversely each bare presentation has the stated exact order, type and IP; the alternatives are distinct as marked string C-groups.

*Proof.* Theorem Q6.1 gives the bounded cyclic quotient. The explicit models and invariant relations in §12 construct and distinguish every listed marking. Theorem Q7.1 gives completeness, excludes the nonlifting order-256 relation patterns and identifies every bare presentation by its order bound. The complete finite relation computation and its exhaustiveness proof are in Appendix A. Thus the converse does not assume the presented group already has the desired order or IP. ∎

**Corollary D4 — F013 Theorem 1.1.** Every finite nondegenerate two-group string C-group of rank \(d\ge2\) admits a marked epimorphism onto the canonical string C-group \(G(C_d)\) of order \(2^{2d-1}\).

*Proof.* Its noncommuting diagram is a path. Theorem Q5.3 identifies its quotient by \(\gamma_3(G)\) with the explicit vertex-and-edge model. Corollary Q5.4 identifies that model with \(G(C_d)\). The Frattini/basis input is the common Theorem S, and the graded support proof is included in §11. ∎

**Corollary D5 — F013 Theorem 1.2.** Every finite nondegenerate regular rank-\(d\) polytope with two-group automorphism group, \(d\ge2\), covers \(C_d\).

*Proof.* Apply D4 and the retained marked quotient/cover correspondence. The false auxiliary source kernel is not needed; §16 proves its precise failure. ∎

**Corollary D6 — F016 Theorem 5.1(a–d).** For \(d\ge3\) and \(n_3,\ldots,n_d\ge5\), there is a finite regular rank-\(d\) polytope whose consecutive rank-three sections are exactly \(\{4,4\}_{(n_3)},\ldots,\{4,4\}_{(n_d)}\), where each square map has automorphism group of order \(2^{n_j}\). Its group has order \(2^{\sum_{j=3}^d n_j-3(d-3)}\). For \(d\ge4\) it is \((d-4,d-1)\)-flat and hence flat. It has FAP with respect to its co-\((d-4)\)-faces, co-\((d-3)\)-faces and facets, with the rank-three co-\((-1)\)-face interpreted as the whole-polytope cut.

*Proof.* The square recognition theorem and compatible product Q2.3 give the exact local sections. Equation (Q8.1) gives the order. The last product factorization gives flatness through the retained coset-face criterion, and Q2.2 supplies the actual deletion retractions and all FAP cuts. These arguments, including the rank-three convention, are all in §14. ∎

**Corollary D7 — F016 Theorem 5.3.** The automorphism group in D6 is precisely the quotient of the universal regular polytope group of generalized type \(\{\{4,4\}_{(n_3)},\ldots,\{4,4\}_{(n_d)}\}\) by
\[
[(r_ir_{i+1})^2,(r_{i+2}r_{i+3})^2]=1
\quad(0\le i\le d-4).
\]

*Proof.* Section 14 proves Boolean deletions and IP for the bare local presentation, so the universal regular polytope exists by the ordinary C-group correspondence. Lemma Q8.1 makes the third-lower-central triple kernels normal. The local lattice indices, global class-two bound and order comparison identify the quotient with the actual product construction. This retains the source's entire presentation claim and repairs the diagonal-translation order step. ∎

**Corollary D8 — F016 Theorem 6.1(a–b).** Let \(d\ge4\), \(n_3,\ldots,n_{d-1}\ge5\), and \(m_{d-1}\ge5\). There is an alternating semiregular rank-\(d\) polytope with regular facet types
\[
(n_3,\ldots,n_{d-2},n_{d-1}),\qquad
(n_3,\ldots,n_{d-2},m_{d-1}).
\]
Its full automorphism group has order
\[
2^{\sum_{j=3}^{d-2}n_j+n_{d-1}+m_{d-1}-3(d-3)}
\]
if the last parameters differ, and twice this order if they agree. At \(d=4\), the shared list is empty and the common facet of the two facets is a square. The remaining co-\((d-4)\)-section is not separately prescribed.

*Proof.* Use D6 for the two facet groups, Q2.3 for the branched compatible product, and the exact retained Monson–Schulte assembly/full-automorphism input in §15. The orders there give the displayed formula, while unequal facet orders exclude an interchange and equal marked constructions admit it. ∎

**Corollary D9 — F016 Theorem 7.1.** For a regular input polytope of rank \(d\ge3\) whose group is a finite or infinite two-group in the source's convention, its free regular extension has rank \(d+1\) and finitely generated infinite automorphism group with every finite-order element of two-power order.

*Proof.* The retained regular free-extension theorem gives the geometry and its amalgam. Lemma Q9.1 proves infinitude, finite generation and the finite-torsion assertion, including infinite input. ∎

**Corollary D10 — F016 Theorem 7.2.** For an oriented chiral input polytope of rank \(d\ge3\) with directly regular facets and finite or infinite two-group automorphism group, its free oriented chiral extension has rank \(d+1\) and a finitely generated infinite two-group in the same convention.

*Proof.* The retained Schulte–Weiss theorem gives the geometry and amalgam over the facet rotation group. That rotation group embeds in the input group; its full facet group is an index-two extension, so Lemma Q9.1 transfers the torsion property and proves the extension conclusions. No full-facet embedding in the chiral group is assumed. ∎

**Corollary D11 — F016 Theorem 7.3.** Let two regular rank-\(d\) polytopes, \(d\ge3\), have isomorphic facets and finite or infinite two-group automorphism groups. Their universal alternating semiregular extension has rank \(d+1\) and finitely generated infinite two-group automorphism group, with the additional branch swap precisely when the two facets of the extension are isomorphic.

*Proof.* The retained universal alternating-extension theorem gives the group amalgam and possible index-two extension. Lemma Q9.1 gives all three group properties in both cases. ∎

## 18. Actual proof sharing and its limit

The normal-subgroup ladder, relative-generation induction and primitive-coordinate proof occur once, before either family of applications. N008's p-group classification invokes the relative clause of Theorem S. The two-group constructions and their graded quotient invoke the same Frattini/basis theorem and its parabolic compatibility. The common kernel theorem handles both quotient-preserved coset actions and the kernel intersections needed for IP in cyclic edge extensions. The two parts of that theorem are distinct logical assertions, and their two short proofs both remain charged.

The symmetric branch cannot be reduced to the deletion construction. Adjacent tree transpositions satisfy \((\tau_e\tau_f)^3=1\). Deleting one and retaining the other would send that relation to a nontrivial transposition. Thus those markings generally admit no Boolean deletion maps. Their IP needs unique tree paths and component partitions; their flag completion needs the laminar-atom proof. B97, Whiston W1 and the stronger CFSG-dependent W2 remain necessary retained work. The sign-kernel family, module obstruction, balanced-cut overgroups and arbitrary-parabolic recovery remain fully proved in §§4–7.

The square lattice, cyclic-core descent, binary models, finite order-256 census and bare-presentation order bounds remain necessary source-specific work in §§9 and 12–13 and Appendix A. The geometric alternating-assembly and free-extension theorems remain imported in §15; a product order by itself supplies none of their geometry or universality. Gaschütz's and Archer's source-quoted earlier results remain explicit imports in §1 rather than newly proved source targets.

The separate primitive-bridge theorem also gives third-lower-central fiber formulas and all square-family face indices. Those extra consequences are not appended here: they do not discharge another required source proof in this integration. A common terminology alone is not counted as a proof saving. The accompanying before/after ledger reports exactly which old proof blocks were moved, replaced by short internal adapters, or retained, and separately charges the new common theorem and the explicit source adapters. No net shortening follows merely from the existence of a shared theorem.

The contract comprises the inherited twenty-three A/B/C adapters and eleven D adapters, not thirty-four papers or thirty-four independently new theorems. N008's unrestricted infinite converse is corrected, and its quoted Gaschütz theorem is retained; every other scope qualification remains stated at the appropriate adapter. The seven exact source versions and all retained proof/certificate costs must be independently reviewed for this new manuscript. No previous factor is transferred to it, and no seven-source length ratio or completed public release is asserted.
