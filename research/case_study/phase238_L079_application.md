# The simplex as the unique higher-rank projective general linear polytope

## Abstract

We apply the common projective-line reduction to all regular polytopes of
rank at least four with full automorphism group $\operatorname{PGL}_2(q)$. The unique example
is the 4-simplex, with $\operatorname{PGL}_2(5)$≅$S_5$. The proof includes all possible quotients
of the finite universal groups and uniqueness of the distinguished marking.
This is the classification of Leemans and Schulte, obtained here as a second
complete application of the same centralizer and finite-amalgam theory.

## 1. Statement and shared hypotheses

We use the marked string C-group convention of [E], and the standard
correspondence with regular abstract polytopes [MS]. In particular an
isomorphism must preserve the ordered distinguished generators, not merely
the abstract automorphism group. A regular polytope's full automorphism
group acts regularly on its flags.

**Theorem 1 (Leemans–Schulte).** Let q be a prime power. If a regular abstract
polytope P of rank $n\ge 4$ has full automorphism group isomorphic to $\operatorname{PGL}_2(q)$,
then $n=4$, $q=5$, and P is the 4-simplex. Its distinguished marking is the
standard adjacent-transposition marking of $S_5$, of type {3, 3, 3}. Conversely
that marking gives the required polytope.

By [E, Theorem 1], the hypotheses already force odd q and rank four. Both
end parabolics are proper and have groups $S_4$ or $A_5$. All their ordered
rank-three markings and compatible pairs are included in [E, Lemmas 10–11].
Consequently the desired group is a marked quotient of one of ten explicit
universal groups. The common reduction includes the cases of subfield
$\operatorname{PSL}_2$ groups, subfield $\operatorname{PGL}_2$ groups, affine groups and unipotent dihedral
subgroups; none has been omitted as a small-field exception.

## 2. Elimination of every other quotient

Four universal groups in the table are trivial. In the rows of orders 60
and 24, an end parabolic equals the entire universal group. Passing to a
quotient preserves this generator dependence, contradicting the marked
intersection property. These six rows cannot produce a polytope in the
statement.

The two universal groups $\operatorname{PSL}_2(11)$ and $\operatorname{PSL}_2(19)$ are nonabelian simple, so their
only nontrivial quotients are themselves. For odd q the determinant modulo
squares gives $\operatorname{PGL}_2(q)$ a quotient of order two. It cannot be either of those
simple groups. This eliminates the two locally projective rows without
comparing orders or silently replacing $\operatorname{PGL}_2(q)$ by $\operatorname{PSL}_2(q)$.

The universal group in the remaining row of order 96 can map onto $\operatorname{PGL}_2(q)$
only if $q(q^2-1)$ divides 96. For odd $q\ge 5$ the order is at least 120; thus the
only possibility is $q=3$. But $\operatorname{PGL}_2(3)$≅$S_4$ cannot contain the required $S_4$ or
$A_5$ facet as a proper subgroup. Hence that row also gives nothing.

The final universal group is $S_5$, of order 120. Its normal subgroups are
1, $A_5$, $S_5$, so the only nontrivial quotient groups are $S_5$ and $C_2$. The order
of $\operatorname{PGL}_2(q)$ for odd $q\ge 3$ is at least 24, excluding $C_2$. Its order $q(q^2-1)$ is
strictly increasing in positive q, and equals 120 precisely at $q=5$. The
remaining group is therefore $\operatorname{PGL}_2(5)$≅$S_5$. This proves exhaustion for every
prime power, including the small cases excluded by the common rank theorem.

## 3. The marking, existence and uniqueness

The successful local pair has both facet and vertex figure the tetrahedron,
with presentation [3, 3]₄ in [E]. Its four-generator universal presentation is

\[
\begin{split}
\langle r_0, r_1, r_2, r_3\mid {}&r_i^2=1,\ (r_ir_j)^2=1\quad(j-i>1),\\
 &(r_0r_1)^3=(r_1r_2)^3=(r_2r_3)^3=1,\\
 &(r_0r_1r_2)^4=(r_1r_2r_3)^4=1\rangle.
\end{split}
\tag{2}
\]

The shared exact computation proves that this is $S_5$ with its specified
string C-marking. There is also an explicit geometric identification. Send
the generators in order to (12),(23),(34),(45). These adjacent transpositions
generate $S_5$; they satisfy all of (2), including the two 4-cycle relations.
The resulting epimorphism from the universal group is an isomorphism because
both groups have order 120. Thus its marking is precisely the familiar
simplex marking, not merely a group of the same order as the simplex.
By [MS] this gives the 4-simplex, and hence existence in Theorem 1.

Every possible local marking is covered by the common six-class enumeration.
For each compatible pair, its literal universal presentation supplies the
marked epimorphism to the group under consideration. Section 2 eliminates
all pairs except the tetrahedral pair, and eliminates every proper nontrivial
quotient of its universal group. Any surviving epimorphism is therefore an
isomorphism preserving the four distinguished generators. This proves
uniqueness of the marked group and of the polytope. Reversing the four
adjacent transpositions is also an automorphism, by conjugation with the
permutation reversing 1, 2, 3, 4, 5, so the usual self-duality is recovered.
Theorem 1 follows. ∎

## 4. Source scope, attribution and proof dependencies

This is the complete principal contract of [LS, Theorem 10], together with
its rank restriction and introductory rank-at-least-four formulation. The
classification is attributed to Leemans and Schulte. The projective-line
centralizer descent and the odd-order normalizer obstruction are supplied
by the common paper [E]; its single finite program supplies all six local
classes and ten universal amalgams. The $\operatorname{PSL}_2$ application is a separate
consequence of the same common paper, not an additional unproved premise
of the argument here.

Dickson's subgroup types and their standard embeddings, elementary projective
group structure and the marked group/polytope correspondence remain retained
classical inputs. The shared finite-presentation calculations use GAP's exact
algorithms. Its Lean component proves only the abstract normalizer obstruction;
there is no end-to-end Lean proof of this application at this stage. No
historical priority or new-conjecture claim is made.

The final part of [LS] also prints a seventeen-case census for $P\Sigma L_2(25)$,
recalls other almost-simple and chiral constructions, and states Conjecture 11
about extensions at odd square q. Those are separate assertions. They are
neither premises nor conclusions here, and their current status is not
inferred from the projective general linear classification. The separate
historical-status audit records the later answer to Conjecture 11; this
application does not claim that answer. In particular
the present paper is not a replacement for all statements in that source.

## References

[E] *Centralizers, facets and finite amalgams on the projective line*, companion
umbrella paper, especially Theorem 1 and Lemmas 10–11.

[LS] D. Leemans and E. Schulte, *Polytopes with groups of type $\operatorname{PGL}_2(q)$*,
retained arXiv:0909.1991v1, 9 physical pages, Theorem 10 on page 7.

[MS] P. McMullen and E. Schulte, *Abstract Regular Polytopes*, Cambridge
University Press, 2002, especially the string C-group correspondence.
