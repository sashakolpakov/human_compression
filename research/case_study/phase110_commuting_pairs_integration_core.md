**(e) Finite actions, their faithful images, and extensions of configurations.** Let G be finite and let Ω be a finite G-set. Choose one representative H from each conjugacy class of subgroups. There are unique nonnegative integers m_H such that, as G-sets,

\[
 \Omega\cong\coprod_{[H]}m_H(G/H),\qquad
 |\Omega|=\sum_{[H]}m_H[G:H],\qquad
 \ker(G\curvearrowright\Omega)=\bigcap_{m_H>0}\operatorname{core}_G(H).
 \tag{Ke1}
\]

The centralizer of this action in S_Ω is

\[
 C_{S_\Omega}(G)\cong\prod_{[H]}\bigl((N_G(H)/H)\wr S_{m_H}\bigr).
 \tag{Ke2}
\]

Here the centralizer means the centralizer of the permutation image, even when the action is not faithful. For a faithful action the normalizer has the exact sequence

\[
 1\longrightarrow C_{S_\Omega}(G)\longrightarrow N_{S_\Omega}(G)
 \longrightarrow\{\alpha\in\operatorname{Aut}(G):m_{[\alpha(H)]}=m_{[H]}\text{ for every }H\}
 \longrightarrow1.
 \tag{Ke3}
\]

Thus forgetting a marking through a specified D≤Aut(G) amounts exactly to taking D-orbits of the multiplicity vectors; this is separate from arbitrary automorphisms of an ambient symmetric or alternating group.

For V=F₂^r, each subgroup is its own conjugacy class. Write ℓ_H for the nonzero linear form with kernel H when [V:H]=2. The action has image in A_Ω if and only if

\[
 \sum_{[V:H]=2}m_H\ell_H=0\quad\text{in }V^*.
 \tag{Ke4}
\]

Finally, let a finite group B act on a finite set E of configurations and on a finite set Z of allowed extensions, with an equivariant projection p:Z→E. The projection need not be onto. For representatives e of all B-orbits on E there is a bijection

\[
 B\backslash Z\cong\coprod_{e\in B\backslash E}B_e\backslash p^{-1}(e).
 \tag{Ke5}
\]

Any B-invariant test on Z can be applied before or after this enumeration. If B acts on underlying objects X and Z,E are actual tuples/subsets with fixed type tags, replacing B by its permutation image on X changes neither orbit relation nor test. In particular no faithfulness assumption on that object action is needed.

*Proof.* The orbits partition Ω. A selected point with stabilizer H gives the bijection gH↦gω, and two transitive G-sets are equivariantly isomorphic precisely when their point stabilizers are conjugate. This proves uniqueness and the size formula. Their common kernel is exactly K(c)'s intersection of cores; the faithful image is the quotient by that kernel. A G-equivariant permutation must permute isomorphic orbits. On one orbit its value at H is nH with n∈N_G(H); these choices give the group N_G(H)/H (using inverses if necessary to identify the opposite group). Independent choices on m_H copies and permutations of those copies give (Ke2). When the action is faithful, conjugation by a normalizing permutation defines an automorphism α of G with kernel the centralizer. Such a permutation exists exactly when the original action and its α-twist have the same orbit types with the same multiplicities, proving surjectivity onto the displayed stabilizer in (Ke3). This also proves the D-orbit assertion.

For V, an element v∉H acts on V/H as [V:H]/2 transpositions, and an element in H fixes it pointwise. The sign contribution can be odd only when [V:H]=2, where it is (−1)^{ℓ_H(v)}. Multiplying over all orbits proves (Ke4). For (Ke5), move the image of any z to the chosen orbit representative e. Two elements of p^{-1}(e) are B-equivalent precisely when an element of B_e carries one to the other. This proves both surjectivity and injectivity. Every configuration built from the action on X is acted on only through that image; this proves the final assertion. ∎

This finite extension of K(c) is used twice. In §21.1, take B to be a maximal subgroup acting by conjugation on its involutions, E its unordered marker subsets, and Z the subsets with an additional involution. The finite-image and invariant-test clauses justify the exact local orbit enumeration, followed by complete extension and global deduplication; the subgroup-table completeness and geometric recognition remain separately necessary. In §25, take G=V=C₂² for the all-degree multiplicity classification, then B=Aut(S₆) or Aut(A₆), E the unordered commuting endpoint pairs and Z the triples with an involutory middle. Equation (Ke5) proves completeness up to isomorphism and reversal. These are actual uses of the same action and extension interface; neither the J1 subgroup catalogue nor the exceptional symmetric-group calculation follows from linearity alone.

