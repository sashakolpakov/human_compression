# Independent presentation check of the proposed Hou–Schulte witness

10 October 2026. This private check independently confirms a counterexample
to the conclusions of Theorem 4.2(c), (d), (e) concerning its specified
subgroup C. It does not refute the separate existence of a common quotient.

The primary version checked is Hou–Schulte,
[arXiv:2605.20691v1](https://arxiv.org/html/2605.20691v1), section 4,
equations (7)–(9), Theorem 4.2 and its proof. The local extracted primary
text was read on PDF pages 5–8, and the same definitions and theorem were
independently opened in the versioned arXiv HTML. Here A_i retains every
adjacent rotation generator except that its i-th generator is squared;
C is the intersection of the Frattini subgroups of these A_i. The theorem
assumes each adjacent product has order at least four.

## Independent construction and exact checks

The script [phase12_hou_schulte_independent.g](phase12_hou_schulte_independent.g)
uses GAP's NQ package to construct the class-two nilpotent quotient of
the presentation on four involutions with distant generators commuting.
It then converts this finite group to permutations. This construction
does not use the parent's vector-space cocycle implementation.

The resulting group G has order 128 and class two. Its four marked
involutions generate it, adjacent products have orders 4,4,4, and all
256 pairs of subsets satisfy the subgroup intersection property. Thus
all source hypotheses hold with d=4, n=7.

Put sigma_i=rho_(i-1)rho_i and c_i=sigma_i^2. The checks give

    |A|=64,  |A_1|=|A_2|=|A_3|=32,
    Phi(A_1)=<c_2,c_3>,
    Phi(A_2)=<c_1,c_2,c_3>,
    Phi(A_3)=<c_1,c_2>.

In particular, their Frattini orders are 4,8,4 and their minimum
generator numbers are 3,2,3. The script separately verifies

    c_2=[sigma_1,sigma_3],
    A_2=<sigma_1,sigma_3>.

Thus the squared middle rotation generator is redundant. This directly
contradicts the claimed minimality of the defining list for every A_i
in the proof preceding the source's Frattini-order calculation.

The actual intersection is C=<c_2>, of order two. The formula in part
(c) gives order one here. The actual quotient G/C has order 64, whereas
part (d) asserts 128. Finally gamma_3(G)=1 while C is nontrivial, contrary
to part (e). These are numerical and subgroup-equality failures under
the exact stated hypotheses.

For precision, the induced quotient marking still passes all 256
intersection tests. Its type is {4,2,4}; this example does not contradict
the assertion that this particular quotient is a string C-group.
Nor does it refute the existence of a quotient isomorphic to the
specified order-128 group: G itself already supplies that quotient.

## Reproduction and scope

Run `gap -q phase12_hou_schulte_independent.g`. The clean final
[transcript](phase12_hou_schulte_independent.log) records GAP 4.15.1,
NQ 2.5.11, all checks above, and a final PASS. Earlier development runs
encountered an unavailable polycyclic intersection method and an empty-list
reporting error; neither is part of the final execution or its certificate.

This is an exact independent finite witness check and source-definition
audit. It is not a proof of a replacement universal theorem, external
peer review, a priority claim, or an assertion about an unexamined later
version of the source. No third-party full text is distributed here.
