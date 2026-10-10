# The universal label-four presentation is unitriangular

10 October2026. Additive author argument; the frozen finite-existence package is unchanged. The stronger conclusion here follows from an explicitly retained theorem of Biss–Dasgupta, rather than from the existence of a finite matrix image.

**Theorem.** Let U_d be the group on d involutions r_0,…,r_(d−1), with distant generators commuting, adjacent products of fourth power one, and

\[
\big((r_{i+1}r_{i+2})^k(r_ir_{i+1})^k\big)^2=1
\quad(0\le i\le d-3,\ k=1,2,3).
\]

Then the marking-preserving map

\[
U_d\longrightarrow\operatorname{UT}_{d+1}(\mathbb F_2),
\qquad r_i\longmapsto I+E_{i,i+1},
\]

is an isomorphism. Consequently U_d has order2^{d(d+1)/2}, has exact type{4,…,4}, and has the full standard-parabolic intersection property.

We use the commutator convention [x,y]=xyx^{-1}y^{-1} throughout this adapter; the identity of the generators with their inverses makes this agree with the needed adjacent commutators in the earlier matrix note.

**Retained presentation theorem.** Biss and Dasgupta, *A Presentation for the Unipotent Group over Rings with Identity*, Journal of Algebra237(2001),691–707, Theorem1 on printedp692, give UT_(d+1)(Z/mZ) on the elementary consecutive generators s_i, with relations

\[
s_i^m=1,\quad [s_i,s_j]=1\ (|i-j|>1),
\]
\[
[s_i,[s_i,s_{i+1}]]=[s_{i+1},[s_i,s_{i+1}]]=1,
\]
\[
[[s_i,s_{i+1}],[s_{i+1},s_{i+2}]]=1.
\]

The last family is needed for even m. We use precisely m=2. The source credits the binary presentation to Biss's1998 paper; neither that presentation nor its proof is a new result here. The exact source is the [author-hosted published PDF](https://sites.math.duke.edu/~dasgupta/papers/Unipotent.pdf), DOI10.1006/jabr.2000.8604.

**Proof of the adapter.** Suppose a²=b²=1 and put A=ab, u=[a,b]=A². Then

\[
aua=u^{-1},\qquad bub=u^{-1},
\qquad [a,u]=[b,u]=u^{-2}.
\]

It follows that the two nested commutator relations are equivalent to A⁴=1. In particular, u is then an involution or the identity. Thus the adjacent fourth-power relations are exactly the Biss–Dasgupta adjacent relations at m=2, in both directions.

For a consecutive triple a,b,c, put A=ab, B=bc. After imposing the adjacent fourth-power relations, the elements u=A² and v=B² are involutions. Therefore

\[
[[a,b],[b,c]]=1
\quad\Longleftrightarrow\quad uv=vu
\quad\Longleftrightarrow\quad (vu)^2=1,
\]

and the last equation is precisely the k=2 extra relator of U_d. Finally ac=ca implies (BA)²=1, since BA=b(ac)b. Also B³A³=B^{-1}A^{-1}=(AB)^{-1}=(ac)^{-1}, whose square is one. Thus the k=1 and k=3 relators add nothing. This proves that the two presentations have identical normal closures of their defining relators, under the identity on generators. The retained presentation theorem identifies U_d with the stated matrix group.

The complete matrix-parabolic argument in phase124_equal_label_partial.md now applies to this group itself: each standard parabolic consists of unitriangular blocks on the intervals of its retained path edges; a matrix entry (a,b) is allowed precisely when every intervening edge is retained. Intersecting these coordinate conditions gives U_J∩U_K=U_(J∩K). Adjacent products have exact order4. This proves every conclusion. ∎

This establishes the universal-presentation strengthening for n=4 in every rank, in addition to the classical n=3 strengthening. It does not identify the universal group for other labels, and it does not solve the all-label conjecture. The exact presentation equivalence and matrix IP proof are written, not presently an end-to-end Lean theorem. Historical novelty of this application to Li–Zhang Conjecture3.7 has not been checked.

## Primary-source access boundary

The author-hosted17-page PDF was opened through the web tool; its first eight extracted pages, including the complete Theorem1 statement, conventions and the even-m proof, were read. Direct local download failed DNS, and the screenshot interface did not expose a viewable image in this session. No local PDF hash, fresh PDF rendering or visual formula inspection is claimed. The readable extracted source identifies the exact nested commutator formulas; an independent reviewer should confirm their printed typography before final admission. The general-ring and minimality sections were not read and are unused.
