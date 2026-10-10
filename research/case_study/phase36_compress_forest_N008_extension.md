# A Frattini extension of Compress_A: kernel reduction and coordinate geometries

Private candidate third-paper chapter and full source inventory, 10 October 2026. **This file does not change the reviewed two-paper manuscript.** It develops an actual extension for Archer–Cara–Krempa (2005), catalogue N008, with complete proofs of its scoped new results. It is not yet an independently accepted three-paper intake or a measured three-paper compression claim.

## 1. Exact source, scope and the point of reuse

The primary is Claude Archer, Philippe Cara and Jan Krempa, *Using the Frattini Subgroup and Independent Generating Sets to Study RWPRI Geometries*, Beiträge zur Algebra und Geometrie **46**(1) (2005), 169–177. Two recorded primary mirrors returned the same complete nine-page PDF:

* <https://ftp.gwdg.de/pub/EMIS/journals/BAG/vol.46/no.1/b46h1car.pdf>
* <https://emis.muni.cz/journals/BAG/vol.46/no.1/b46h1car.pdf>

The existing private PDF is `sources/phase16_frattini_geometries.pdf`, SHA-256 `cfbd53bc367ecaea644214eb0f64fc5db0c20d63096fdc239cf5d61c3f72c5c9`. Its complete page-marked extraction is `sources/phase16_frattini_geometries.txt`, SHA-256 `056823e93c4da84e0fb8f9425ebb2a1f27efc78b7ce6bb18a69b09c0b102f128`. Every page, definition, numbered statement, proof, computational remark and reference in that extraction was read for this extension. No new PDF extraction or independent visual reconstruction of its formula layout was performed. Exact source anchors are supplied by the companion intake JSON; these are scope bindings, not length selections. The primary files remain unchanged and private.

The proposed new target set contains Theorem 2.1 in finite-group scope; Theorem 3.1 including its explicitly advertised infinite-group scope; Proposition 3.2, Corollary 3.3 and Theorem 3.4; the finite-p-group conclusions Proposition 3.7 and Theorem 3.8; and the necessary residue test of §4.2. We also prove subsidiary Proposition 3.5 and Lemma 3.6 and the action-kernel conclusion of §4.3. Theorem 4.1 is an explicitly quoted theorem of Gaschütz, rather than a new result of N008, and is retained separately. The complete inventory below records the unnumbered discussions and exclusions as well.

The common interface is **Theorem R(b) of Compress_A**: for a firm RWPRI coset geometry with Borel subgroup \(B\), panel choices \(s_i\) satisfy
\[
H_J=\langle B,s_i:i\notin J\rangle.\tag{R}
\]
The N003 rank bound and strong-independence theorem are thus reused in a further paper, not merely cited as a related subject. After a Frattini quotient, (R) directly gives a coordinate basis and all p-group parabolics. There is no need to import a separate p-group geometry classification or to repeat the source's recursive maximal-subspace argument.

For a standalone reading, the short proof of (R) and the required conventions are given below. In an integrated third-paper manuscript that duplicate proof would be replaced by the existing Theorem R; all genuinely new arguments here would remain charged. This extension does not assume B97, W1, W2, Cayley's formula, or a finite-group census.

## 2. Finite rank, relative generation and maximal overgroups

Here \(I\) is a finite nonempty type set, but \(G\) may be infinite unless finiteness is stated. Write \(H_J=\bigcap_{j\in J}H_j\), \(H_\varnothing=G\), and \(B=H_I\). Use left cosets, with incidence given by intersection. A geometry requires that every flag extend to a chamber. Firmness means at least two chamber extensions of a nonchamber flag. A residue is WPRI when its stabilizer acts primitively on at least one remaining type, and RWPRI requires this in every nonempty-rank residue, including the geometry itself. Taking the induced action, rather than a possibly unfaithful stabilizer action, leaves primitivity unchanged.

**Lemma E0 (the source's flag-transitivity convention is automatic here).** A finite-rank geometry on which a group acts residually weakly primitively is flag-transitive.

*Proof.* Fix a chamber. Starting with its empty flag, choose a remaining type on which that flag's stabilizer acts primitively, hence transitively. Given any second chamber containing the chosen flag, use that stabilizer to match its element of the chosen type to the fixed chamber's element. Repeat in the residue. At most \(|I|\) steps match any chamber to the fixed chamber. Thus the group is chamber-transitive. Every flag extends to a chamber, so it is transitive on flags of each fixed type. The fixed chamber's element stabilizers then give the usual coset representation: the typewise coset bijections preserve incidence because transitivity on incident pairs supplies a common representative. ∎

This justifies the source's subgroup translation without inserting an unprinted flag-transitivity hypothesis into its firm-RWPRI conclusions. For a flag-transitive coset geometry, firmness gives distinct \(H_J\), and RWPRI gives a maximal next intersection at every proper \(J\). To see distinctness explicitly, firmness gives \(H_{I\setminus\{i\}}>B\); choose \(s_i\) in this difference. For \(J\ne K\), a type in one of their differences supplies an \(s_i\) that lies in one intersection and not the other.

The same choices are independent relative to \(B\), because all other \(s_j\) lie in \(H_i\), while \(s_i\) does not. Prove (R) by downward induction on \(J\). It is true for \(J=I\). Choose \(k\notin J\) with \(H_{J\cup\{k\}}\) maximal in \(H_J\). By induction that maximal subgroup is generated by \(B\) and the other remaining panel choices, and \(s_k\) lies outside it but inside \(H_J\). Hence those generators together generate \(H_J\). No finiteness of \(G\) is used. Intersecting the resulting equalities gives strong relative independence as in Compress_A.

**Lemma E1 (relative finite generation supplies maximal overgroups).** Suppose \(G=\langle B,t_1,\ldots,t_r\rangle\) with finite \(r\). Every proper subgroup \(H\geq B\) is contained in a maximal subgroup of \(G\).

*Proof.* Order the proper overgroups of \(H\) by inclusion. The union of a chain is a subgroup; if that union were \(G\), a single member would contain the finitely many \(t_j\), and hence all of \(G\), a contradiction. Every chain therefore has a proper upper bound, and Zorn's lemma gives a maximal element. ∎

Let \(\Phi(G)\) denote the intersection of all maximal subgroups of \(G\), with the intersection equal to \(G\) if there are none. It is characteristic and hence normal. If every proper overgroup of \(B\) lies in a maximal subgroup, then
\[
\Phi(G)H=G,\ H\geq B\quad\Longrightarrow\quad H=G.\tag{2.1}
\]
Indeed a maximal subgroup containing a proper \(H\) also contains \(\Phi(G)\). This hypothesis holds for finite \(G\), and more generally under Lemma E1. It is important to supply it when \(G\) is infinite.

## 3. The new common theorem: Frattini containment and exact kernel transport

**Theorem E2 (normal-subgroup ladder).** Suppose all intersections \(H_J\), \(J\subseteq I\), are distinct and that some ordering of the types gives a maximal subgroup chain
\[
G=K_0>K_1>\cdots>K_r=B,\qquad K_j=H_{\{1,\ldots,j\}}.
\tag{3.1}
\]
If \(N\unlhd G\) lies in every maximal subgroup of \(G\), then \(N\leq B\). The group may be infinite.

*Proof.* Choose \(t_j\in K_{j-1}\setminus K_j\). Each maximal inclusion gives \(K_{j-1}=\langle K_j,t_j\rangle\), so backwards induction gives \(G=\langle B,t_1,\ldots,t_r\rangle\). Lemma E1 implies that \(NH_i=G\) is impossible for a proper \(H_i\): a maximal overgroup of \(H_i\) would contain both factors.

Suppose \(N\not\leq B\), and let \(k\) be the first index with \(N\not\leq K_k\). Then \(N\leq K_{k-1}\), and normality and maximality give
\[
K_{k-1}=N(K_{k-1}\cap H_k).
\]
Suppose, in an upward step with \(1\leq j<k\), that \(K_j=N(K_j\cap H_k)\). Since \(N\leq K_{j-1}\),
\[
K_j\leq N(K_{j-1}\cap H_k)\leq K_{j-1}.
\]
Maximality permits only the endpoints. Equality with the lower endpoint would imply \(K_{j-1}\cap H_k\leq K_j\), and consequently
\[
K_{j-1}\cap H_k=K_j\cap H_k.
\]
These are different indexed intersections, because \(j<k\), contradicting distinctness. Thus equality with the upper endpoint holds. Repeating this step reaches \(G=NH_k\), the contradiction established in the first paragraph. ∎

RWPRI supplies (3.1) by choosing a maximal next intersection repeatedly. Lemma E0 and firmness supply distinctness. With \(N=\Phi(G)\), Theorem E2 proves \(\Phi(G)\leq B\) for every finite-rank firm RWPRI geometry, including infinite \(G\). Its infinite proof does not assume that the whole Frattini subgroup is always superfluous.

**Theorem E3 (exact coset-kernel transport).** If \(N\unlhd G\) and \(N\leq B\), the quotient map induces an isomorphism of typed pregeometries
\[
 gH_i\longmapsto (gN)(H_i/N)
\tag{3.2}
\]
between the families in \(G\) and \(G/N\). It preserves all coset intersections, flags, chambers, residues, common-point witnesses, firmness, residual connectedness, flag-transitivity, RWPRI and RPRI. Subgroup families containing \(N\) correspond bijectively to quotient subgroup families.

*Proof.* For the quotient homomorphism \(\pi\),
\[
\pi^{-1}\bigl(\pi(g)(H_i/N)\bigr)=gH_i.
\]
Thus corresponding cosets are in bijection and every intersection pattern is preserved, including common points of any family. This proves the incidence and flag claims, also for pregeometries lacking flag-transitivity. The acting groups have the same permutation image on the corresponding cosets. Subgroup correspondence preserves maximality in each interval above \(N\), including all residue intervals, which proves the primitive properties. The usual subgroup correspondence gives the final assertion. ∎

The quotient by \(\Phi(G)\) is Frattini free: its maximal subgroups correspond to the maximal subgroups of \(G\), whose intersection is \(\Phi(G)\). If \(G\) has no maximal subgroups, then \(\Phi(G)=G\) and the quotient is trivial, giving the same conclusion. Moreover the kernel of the action on all typed cosets is
\[
\bigcap_i\operatorname{core}_G(H_i)
 =\operatorname{core}_G(B).
\tag{3.3}
\]
It is the largest normal subgroup of \(G\) contained in \(B\); transport through that kernel yields the faithful action. Theorem E2 puts \(\Phi(G)\) inside this kernel.

The bijection here concerns indexed subgroup families with the quotient map fixed. It is not a claim that all automorphisms of \(G/\Phi(G)\) lift to \(G\), or that their respective automorphism orbits have equal counts. The source's stated incidence isomorphisms and its quotient-family correspondence are fully recovered without that extra assertion.

## 4. Relative generating families and the infinite correction

**Theorem E4 (Frattini transport of relative generators).** Suppose every proper subgroup containing \(B\) is contained in a maximal subgroup of \(G\). For a finite indexed family \((s_i)\), it is an independent generating family of \(G\) relative to \(B\) if and only if its image is an independent generating family of \(G/\Phi(G)\) relative to \(B\Phi(G)/\Phi(G)\). In particular this holds for finite groups and for groups finitely generated relative to \(B\).

*Proof.* For \(H=\langle B,s_i:i\in I\rangle\), generation in the quotient means \(\Phi(G)H=G\), equivalent to \(H=G\) by (2.1). Under generation, independence means that every deletion subgroup \(H_i'=\langle B,s_j:j\ne i\rangle\) is proper. Apply the same equivalence to each \(H_i'\): it is proper precisely when its image is proper in the quotient. This is exactly quotient independence. ∎

The unqualified printed infinite converse of N008 Theorem 2.1 is false. Let \(D=C_{p^\infty}\) be a Prüfer group and \(G=D\times C_2\). Every maximal subgroup of this abelian group has a cyclic prime-order quotient. Divisibility forces every homomorphism from \(D\) to such a quotient to be trivial. Hence \(D\times1\) is the unique maximal subgroup and equals \(\Phi(G)\). The one element generating the second factor generates \(G/\Phi(G)\), but does not generate \(G\). Taking \(B=1\) gives the advertised failure even for a one-element family.

This is a source-scope correction, not a new-priority claim. Theorem E4 gives the required finite version and a precise sufficient infinite hypothesis. If a finite family is already known to generate \(G\) relative to \(B\), Lemma E1 supplies the maximal-overgroup hypothesis, so its independence equivalence also survives for infinite \(G\). The independent proof of Theorem E2 remains valid in full infinite geometric scope.

## 5. Coordinate geometry as a direct corollary of the existing relative core

The only new group-theoretic background needed here is the standard finite-p-group Frattini fact:
\[
P/\Phi(P)\text{ is an elementary abelian }p\text{-group}.
\tag{PΦ}
\]
It is retained unexpanded, rather than charged as a classification of p-groups. Elementary vector-space dimension facts are also used. Zorn's lemma is needed only for the stated infinite conclusions above.

**Theorem E5 (the coordinate specialization of (R)).** Let \(P\) be a finite p-group and let a firm RWPRI coset geometry for \(P\) have rank \(r\) and Borel \(B\). Then \(B\unlhd P\), \(P/B\cong\mathbb F_p^r\), and in a suitable basis \((v_i)\) of \(P/B\),
\[
H_J/B=\operatorname{span}\{v_i:i\notin J\}
\qquad(J\subseteq I).
\tag{5.1}
\]
Consequently every type has \(p\) elements, every choice of one element of each type is a chamber, the geometry is RPRI, and it is the direct sum of \(r\) primitive rank-one geometries. Its faithful group \(P/B\) acts regularly on chambers.

*Proof.* Theorem E2 gives \(\Phi(P)\leq B\). By (PΦ), \(P/\Phi(P)\) is a vector space, so its subgroup \(B/\Phi(P)\) is normal and \(P/B\) is a vector space over \(\mathbb F_p\). Apply the existing formula (R). The images \(v_i=s_iB\) span \(P/B\). They are linearly independent: a nontrivial relation would express one \(s_i\) modulo \(B\) in terms of the other generators, contrary to relative independence. Thus they form a basis, and (R) becomes (5.1).

The type-\(i\) cosets are the \(p\) values of the \(i\)-th coordinate. Assignments to any distinct coordinates have a common vector, hence a common coset representative. Every selection of one element of each type is therefore a chamber. In a residue, fixing another coordinate is an index-\(p\) subgroup inclusion, which is maximal. Thus the geometry is RPRI. Each type is a primitive rank-one \(p\)-point geometry and all distinct types are completely incident, proving the direct-sum assertion. Its kernel is \(B\) by normality and (3.3), and the coordinate translations act regularly on complete coordinate assignments. ∎

Conversely, writing \(d=\dim P/\Phi(P)\), any \(r\) independent linear functionals on that vector space, each considered up to nonzero scalar, give the full collection of examples of rank \(1\leq r\leq d\) by pulling back their kernels. Indeed a basis of \(P/B\) in E5 supplies exactly those quotient coordinate functionals. Every resulting family is firm, flag-transitive, residually connected and RPRI by coordinate assignments. For clarity this also gives the exact number of **indexed subgroup families**, not automorphism orbits:
\[
\frac{\prod_{j=0}^{r-1}(p^d-p^j)}{(p-1)^r}.
\tag{5.2}
\]
The numerator chooses independent ordered functionals; independent rescaling does not change their kernels. This converse and count are useful extra consequences of the common theory, not extra source targets or an asserted new result.

Two subsidiary source statements need only elementary arguments. For two subgroups \(H_1,H_2\), every left coset of one intersects every left coset of the other exactly when \(H_1H_2=G\), since \(gH_1\cap hH_2\ne\varnothing\) is equivalent to \(g^{-1}h\in H_1H_2\). This is the rank-two direct-sum criterion. If \(U,W<V=\mathbb F_p^k\), with \(U\) a hyperplane, \(U\cap W\) a hyperplane of \(U\), and \(W\not\subseteq U\), then the image of \(W\) in \(V/U\) is one-dimensional. Therefore \(\dim W=(k-2)+1=k-1\), giving the source's maximal-subspace lemma.

## 6. Residual Frattini tests and explicit source corollaries

For every proper \(J\subsetneq I\), apply E2 inside the residue group \(H_J\). The Borel of that residue is still \(B\), since
\[
\bigcap_{i\notin J}(H_J\cap H_i)=B.
\]
Thus every firm RWPRI geometry satisfies
\[
\Phi(H_J)\leq B\leq H_{J\cup\{i\}}
\qquad(i\notin J).
\tag{6.1}
\]
This is a necessary rejection test on candidate residue groups. It neither asserts sufficiency nor assumes \(\Phi(H_J)\leq\Phi(G)\). No runtime improvement for a particular enumeration follows from the proof alone.

The following corollaries constitute the proposed third-paper recovery, with complete formulations in the source inventory immediately below.

**C1 — N008 Theorem 2.1, finite scope.** Relative independent generating families in a finite group descend to and lift from its Frattini quotient, relative to the image of \(B\). This is E4. Its printed unrestricted infinite converse is replaced by E4's explicit additional hypothesis and the preceding counterexample.

**C2 — N008 Theorem 3.1.** In any finite-rank firm RWPRI coset geometry, \(\Phi(G)\leq H_i\) for every type, including infinite groups. Lemma E0 and firmness give the lattice hypotheses, and E2 yields the stronger \(\Phi(G)\leq B\).

**C3 — N008 Proposition 3.2.** A coset pregeometry whose type subgroups contain \(N\unlhd G\) is isomorphic to the pregeometry of their images in \(G/N\). This is E3 without any flag-transitivity assumption.

**C4 — N008 Corollary 3.3.** Every firm RWPRI coset geometry is isomorphic to its Frattini-quotient coset geometry. Combine C2 with E3.

**C5 — N008 Theorem 3.4.** Every firm RWPRI geometry is isomorphic to one for a Frattini-free group. Apply C4 and the maximal-subgroup correspondence following E3. Quotient and pullback give the fixed-indexed-family bijection motivating the paper.

**C6 — N008 Proposition 3.5.** A rank-two coset pregeometry is a direct sum exactly when \(H_1H_2=G\). This is the coset-product calculation after E5, with no finiteness or normality assumption.

**C7 — N008 Lemma 3.6.** If \(U,W<\mathbb F_p^k\), \(W\not\subseteq U\), \(U\) is maximal and \(U\cap W\) is maximal in \(U\), then \(W\) is maximal in \(\mathbb F_p^k\). This is the dimension calculation after E5.

**C8 — N008 Proposition 3.7.** A firm coset geometry of a finite p-group is RWPRI if and only if it is RPRI. E5 proves the nontrivial implication; the converse is immediate from the definitions.

**C9 — N008 Theorem 3.8, finite-p-group context.** Every firm RWPRI coset geometry of a finite p-group is a direct sum of primitive geometries of rank one. This is E5; each summand has exactly \(p\) points.

**C10 — N008 §4.2.** For each standard flag of type \(J\), \(\Phi(H_J)\) must lie in every \(H_J\cap H_i\), \(i\notin J\). This is (6.1), derived by applying E2 in each residue.

**C11 — N008 §4.3, action-kernel assertion.** The largest normal subgroup of \(G\) contained in the Borel is \(\operatorname{core}_G(B)=\bigcap_i\operatorname{core}_G(H_i)\). Quotienting by it preserves the geometry and makes the action faithful; for firm RWPRI geometries it contains \(\Phi(G)\). This is (3.3), E3 and E2.

## 7. Complete numbered inventory and main-result mapping

The formulations in this ledger preserve all mathematical clauses while normalizing notation. Locations refer to the journal's printed pages; subtract 168 to obtain the one-based physical PDF page number. An indexed family and its specified action are retained throughout; no additional automorphism-orbit equivalence is silently imposed.

| Item | Full source formulation and scope | Recovery and status |
|---|---|---|
| Theorem 2.1, 171–172 | For \(B\leq G\), \(\Phi=\Phi(G)\), a family \((s_i)\) is an independent generating family relative to \(B\) iff \((\Phi s_i)\) is one for \(G/\Phi\) relative to \(\Phi B/\Phi\). The printed statement says an arbitrary group. | C1/E4 prove the finite specialization and a stated infinite correction. The unrestricted converse is not recovered and has an explicit counterexample. |
| Theorem 3.1, 173 | For a firm RWPRI coset geometry \(\Gamma(G,(H_i))\), \(\Phi(G)\leq H_i\) for all \(i\); the paragraph before the theorem explicitly allows infinite \(G\). | C2/E0/E2 prove the full finite-rank geometric claim, including infinite \(G\). |
| Proposition 3.2, 174 | If \(N\unlhd G\) lies in every type subgroup of a coset pregeometry, then \(\Gamma(G,(H_i))\cong\Gamma(G/N,(H_i/N))\). It is attributed to earlier background [2] in the source. | Reproved as C3/E3 for all groups and pregeometries; not retained as a black box. |
| Corollary 3.3, 174 | A firm RWPRI coset geometry is isomorphic to \(\Gamma(G/\Phi(G),(H_i/\Phi(G)))\). | C4; also preserves firmness and RWPRI in both directions. |
| Theorem 3.4, 174 | Every firm RWPRI geometry is isomorphic to a firm RWPRI geometry for a Frattini-free group. | C5 and the explicit \(\Phi(G/\Phi(G))=1\) argument. |
| Proposition 3.5, 174 | The rank-two pregeometry \(\Gamma(G,(H_1,H_2))\) is a direct sum iff \(H_1H_2=G\). The source attributes it to earlier work. | Reproved as C6 by exact coset intersections. |
| Lemma 3.6, 174 | For proper \(U,W<\mathbb F_p^k\), if \(W\not\subseteq U\), \(U\) is maximal, and \(U\cap W\) is maximal in \(U\), then \(W\) is maximal in \(\mathbb F_p^k\). | C7, a complete dimension proof. |
| Proposition 3.7, 174–175 | For a finite p-group, a firm coset geometry is RWPRI iff it is RPRI. | C8/E5, reusing (R) from the N003 branch. |
| Theorem 3.8, 175 | A firm RWPRI coset geometry for a p-group is a direct sum of primitive rank-one geometries. The theorem omits “finite”, but §3.2.2 begins with a finite p-group and uses its finite-dimensional elementary abelian Frattini quotient. | C9 in that finite-p-group context; no unrestricted infinite-p-group extension is claimed. |
| Theorem 4.1, 175 | If a finite Frattini-free group \(F\) has socle \(S=A\times D\), with \(A\) a product of abelian simple groups and \(D\) a product of nonabelian simple groups, then \(F=A\rtimes K\), where \(K\leq\operatorname{Aut}(S)=\operatorname{Aut}(A)\times\operatorname{Aut}(D)\) contains \(D=\operatorname{Inn}(S)\) and acts semisimply on \(A\). Here semisimple means that the maximal \(K\)-invariant subgroups of \(A\) have trivial intersection. | Explicit retained theorem of Gaschütz (1953), as the source itself identifies. Not reproved or needed by E0–E5. It must remain an imported theorem if the integrated manuscript includes this structural description. |

Additional source content, fully inventoried:

| Source passage | Treatment |
|---|---|
| §1, 170–171, incidence definitions and subgroup translations | Shared with Compress_A. E0 supplies the flag-transitivity bridge for the unqualified RWPRI geometric statements; general correspondence conventions remain stated. |
| §2.2, 171, claim that adjoining the whole Frattini subgroup never changes generation | Valid in the finite setting; the unrestricted assertion is corrected by (2.1), E4 and the Prüfer-product counterexample. Individual nongenerator statements are not confused with simultaneous removal of an infinite subgroup. |
| §2.3, 172, relative generators and strong independence from Cameron–Cara | Already proved as Compress_A Theorem R. Its elementary induction is repeated only to make this draft extension readable alone and to state the finite-rank infinite-group form. |
| §3.1 opening and abstract, quotient-family bijection | E2/E3 prove exact fixed-indexed-family lift/descent and incidence isomorphism. No automorphism-lifting claim is added. |
| §3.2.1, 174, flags/chambers/residues of direct sums | In the coordinate application this is explicit: a chamber assigns every coordinate, and a residue fixes some coordinates and retains the rest. No independent direct-sum classification is imported. |
| §4.1.1, 175–176, historical SmallGroups counts and scarcity discussion | Excluded historical computation, not a new geometric theorem. The counts are neither rerun nor silently updated; their database/version cost would be additional work if admitted. The suggested asymptotic predominance of p-groups is not proved. |
| §4.2, 176, the residue Frattini test | Main unnumbered consequence C10; necessary only, with complete proof and no runtime assertion. |
| §4.2.1, 176, algorithms for computing \(\Phi\) | Source references Eick's soluble-group methods and a Fitting-subgroup approach. These algorithms are not new source theorems and are not reimplemented or benchmarked here. |
| §4.3, 176, largest normal kernel and faithful quotient | C11; exact full assertion proved. The illustrative case \(\Phi(G)=\operatorname{core}_G(B)\) when \(G/\Phi(G)\) is simple follows because a proper Borel cannot contain that nontrivial simple quotient as a normal subgroup. |
| §4.3 final paragraph, reduction of non-direct-sum RPRI geometries to primitive groups | Explicitly cited prior result of Archer, *Direct sum decomposition of geometries based on maximal subgroups*, J. Geometry 79 (2004), 12–18. Retained/excluded earlier classification, not a newly proved N008 result. No claim that E0–E5 recover that earlier paper. |

## 8. Dependency cost and conditions for admission as a third manuscript

The substantive additions to Compress_A are E1/E2 (relative maximal-overgroup existence and the normal-subgroup ladder), E3 (exact coset-kernel transport), E4 (Frattini transport of relative generation and its scope correction), and the short coordinate specialization E5. E0 closes the source convention about flag transitivity. The existing relative parabolic-generation formula pays for the coordinate basis and all residue subspaces. The kernel argument is useful at the level of actual incidence, preserving flags and residues rather than merely replacing a group by a linear representation.

The retained common inputs for the newly recovered results are elementary subgroup correspondence, finite-dimensional linear algebra, (PΦ), and Zorn's lemma where infinite groups are claimed. Gaschütz's structural theorem and Archer's earlier primitive-group reduction are separately identified source imports; neither is needed for the new core. No Whiston or CFSG input is added to the N008 branch. Historical enumerations and computation methods remain excluded with their costs visible.

This chapter supplies a genuine candidate third-manuscript derivation for the declared main-result set, but it cannot recover the source literally in unrestricted infinite scope because Theorem 2.1's converse fails. A three-paper intake must accept the finite specialization/corrected statement explicitly. Before admission it needs independent mathematical review of this new assembled proof, a source-scope review of the complete inventory (especially the finite context of Theorem 3.8 and the retained Theorem 4.1), and final approval of the corrected main-result contract. No numerical gain is inferred from adding one paper to the coverage count.

Once accepted, integration would share the existing definitions and Theorem R and insert the new chapter before the source-corollary collection. Its entire proof cost, including the infinite-scope correction and necessary background exposition, must enter the three-paper denominator. The N008 full main-body source length could then enter the numerator under the same normalization as N001 and N003. This file deliberately makes no such measurement and leaves the independently reviewed two-paper manuscript untouched.
