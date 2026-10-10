# Local enumeration lemmas for the prospective application

These are author statements and proofs, not an independently admitted new module. U.Orbits and U.ExtensionOrbits are cited from the current shared theory; their proofs are not repeated. Group-specific recognition and catalogue hypotheses remain application obligations.

## E.ExactSupportOrbits

Let a finite group A act on a finite set X and on a finite poset L with greatest element 1. Let s:X→L be equivariant. Write X_l={x:s(x)≤l} and let μ be the Möbius function of L. Then the number of A-orbits of points having exact support 1 is

\[
\frac1{|A|}\sum_{a\in A}\sum_{l\in L}
\mu(l,1)\,|\operatorname{Fix}_X(a)\cap X_l|.
\tag{E1}
\]

No X_l is required to be A-invariant. The exact-top-support subset is invariant because 1 is fixed.

**Proof.** For x∈X, the defining inverse relation for the incidence-algebra Möbius function gives
\[
\sum_{s(x)\le l\le1}\mu(l,1)=
\begin{cases}1&s(x)=1,\\0&s(x)<1.\end{cases}
\]
Summing this identity over the points fixed by a gives the inner sum in (E1). On any finite A-set Y, counting pairs (a,y) with ay=y gives ∑_a|Fix_Y(a)|=∑_y|A_y|. Each orbit contributes |A|, since |orbit(y)|·|A_y|=|A|. Division by |A| therefore gives its number of orbits. Apply this to the invariant exact-support subset. ∎

For nested finite-field data, L is the divisor poset of N and X_d is the data defined over the unique subfield F_(2^d). The application must prove that these sets are exactly the support sublevel sets, rather than assuming generation follows from a coordinate count. If exact-degree data have free Frobenius orbits of length N, and an additional involution is free on those orbits, the count reduces to E(N)/(2N), where E(N)=∑_(d|N)μ(N/d)|X_d|. L074 supplies these hypotheses by normalization, the subfield-position lemma and the odd-degree inversion argument. For L066 reversal has fixed orbits, so the free-action simplification is not used: the same fixed-point identity yields (total+fixed)/2.

## E.PrimitiveTriples

Let G be a finite group, let H_1,H_2,H_3 be distinct maximal proper subgroups, and form their right-coset incidence system. Put H_ij=H_i∩H_j and B=H_1∩H_2∩H_3. For a fixed i with {i,j,k}={1,2,3}, let R_ij be the set of H_i-cosets meeting H_j. Then this incidence system is flag-transitive and residually connected if and only if

\[
|R_{ij}\cap R_{ik}|=[H_{jk}:B],
\qquad
H_i=\langle H_{ij},H_{ik}\rangle\quad(i=1,2,3).
\tag{E2}
\]

Only one chosen i is needed for the cardinality equality, whereas all three generation equalities are required. All these systems are firm. Equivalence under a specified subgroup A≤Aut(G), with arbitrary type permutation, is exactly the A-orbit relation on unordered triples of the H_i. This is the equivalence specified here, not an assertion that every abstract incidence isomorphism of arbitrary coset systems is induced by A.

**Proof.** Every incident pair of cosets has a common element, so G is transitive on flags of each two-type combination. Fix the base pair H_j,H_k. The H_i-cosets incident to both are precisely R_ij∩R_ik. Its subgroup H_jk already has an orbit of size [H_jk:B], represented by H_i. The displayed equality says this orbit is the entire set. Consequently every chamber can be moved to the base chamber, and the converse follows from chamber transitivity. This is the rank-three specialization of U.Helly, expressed without subgroup-product sets.

Under this common-chamber property, the residue at H_i identifies with the coset incidence graph of H_i on H_ij and H_ik: moving an incident chamber into H_i proves incidence in both directions. Such a bipartite coset graph is connected exactly when its two defining subgroups generate H_i. Indeed a path from a base vertex is a successive multiplication by elements of those subgroups, and conversely such a word supplies a path. The whole geometry is connected because any two distinct maximal subgroups generate G. Thus (E2) is equivalent to residual connectedness.

If a panel had a single completion, then some H_jk would equal B. In the residue at H_j, the two point stabilizers H_ij and H_jk would then generate only H_ij, which is proper in H_j since H_i and H_j are distinct maximal subgroups. This contradicts the corresponding generation equality. Hence every panel has at least two completions. Finally a marked automorphism in A sends the defining subgroup set to its image, and a type permutation merely reorders that set, proving the stated equivalence. ∎

## Exact search above a maximal pair

Let M be the finite set of all maximal subgroups of G, on which A≤Aut(G) acts. Use U.ExtensionOrbits first for ordered or unordered pairs of distinct members of M. For every unordered pair representative e, use it again with Z consisting of pairs (e,H) with H∈M\e. Every unordered triple has such a distinguished pair, so the fibers cover all triples. Enumerating the whole fiber modulo A_e, applying (E2), and finally deduplicating under A on unordered triples therefore gives a complete classification.

It is not enough merely to divide a number of pairs by |A|, or to keep one H from each conjugacy class in G without the appropriate pair stabilizer. Multiple distinguished pairs of a triple can produce duplicates; the final A-orbit test is part of the proof. If A is replaced by its actual permutation image on M, both orbit relations and all subgroup tests are unchanged, because each image element has a lifting automorphism. Faithfulness on M is unnecessary.

For L073 this gives a finite exact route to the rank-three M22 theorem. The subsequent independent-input author computation finds 431 classes and verifies their geometric shadows. It retains the complete M22 subgroup catalogue, and exact matching of the full refined source table remains open in phase164_L073_comparison_status.md. For the rank-two part, no higher typed-Helly test is required; every distinct maximal pair is connected, firm and flag-transitive. Full Aut(M22)/type equivalence still has to be computed.
