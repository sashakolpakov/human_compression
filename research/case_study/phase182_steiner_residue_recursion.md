# Derived designs and the residue recursion

Working extension toward the complete L092 contract. This note is not part
of the frozen correction package until it has received independent review.

Let S be a Steiner system S(t,k,v), where t≥2, k≥t+1, and
r=(v−t+1)/(k−t+1)≥3. For a point subset X of size j<t, denote by S_X
the derived system S(t−j,k−j,v−j), whose blocks are B\X for the blocks
B containing X. We write Γ(S) for literal Construction2 of L092.
Its ordinary objects are the subsets of sizes1,…,t−2; its other objects
are marked pairs (T,E), blocks B₀, and copied points z, with the six
incidence conventions used in that source. For t=2 the ordinary part is
empty, and this is Construction3 on the linear space S.

The construction is retained from L092 and its cited predecessors.
The purpose of this note is to isolate a uniform residue argument so that
an application does not pay for the same connectivity analysis at each
rank. No claim of historical novelty is made.

## The geometry and its elementary residues

**Lemma R.Firm.** Γ(S) is a firm geometry. Its panels missing an ordinary
type have size2. Panels missing the marked, block or copied-point type
have sizes k−t+2, r−1 and k−t+1 respectively.

**Proof.** Every flag's ordinary objects form a chain. If the flag
contains a marked pair (T,E), extend its ordinary chain to all subset
sizes inside T. If necessary choose a copied point in E and choose a
block through T other than T∪E. Distinct blocks through a (t−1)-set
have disjoint complements to that set, so the resulting objects form a
chamber.

Suppose instead that a block B₀ is present but a marked pair is absent.
The ordinary chain lies in B₀. Its largest member has size at most t−2,
so extend it to a (t−1)-set T⊂B₀. Use the copied point z already in the
flag, or choose z outside B₀ if none is specified. Such a point exists
because r≥3 forces v>k. The unique block B′ through T∪{z} differs from
B₀ and intersects B₀ in exactly T. The marked pair (T,B′\T), followed
by completing the ordinary chain in T, gives the required chamber.

If neither a marked pair nor a block is present, first use or choose a
copied point z outside the largest ordinary set. Extend that set to a
(t−1)-set T avoiding z. Let B′ be the block on T∪{z}, and select any
other block B₀ through T. Again complete the chain inside T. These
arguments include the empty chain when t=2, and prove the geometry axiom.

For an ordinary missing type, its immediately bounding sets differ by
two elements, and its two intermediate subsets are exactly the possible
completions. If the marked type is missing, the fixed largest ordinary
set R has size t−2, with the convention R=∅ when t=2. Its completions
are T=R∪{u}, u∈B₀\R, followed by the unique block through T∪{z}.
There are k−t+2 possibilities. The other two counts are immediate from
the r blocks through T and the k−t+1 points of E. All sizes are at least
two. ∎

For a finite set X, let B(X) be the geometry of its nonempty proper
subsets with inclusion incidence. It has rank |X|−1. We include the
empty rank-zero factor when |X|=1. A join of typed geometries means that
all objects of different factors are incident.

**Lemma R.Boolean.** B(X), and its truncation to all subset sizes1,…,h
with h<|X|, are residually connected. Rank-zero and rank-one factors
have no connectivity requirement.

**Proof.** A flag is a chain. Its residue splits into joins of subset
geometries on the successive differences between consecutive sets of
the chain, with a final truncated factor above its largest member.
In a factor of rank at least two, singleton objects are connected through
two-element objects; every object has a singleton neighbor. If the
residue has at least two nonempty positive-rank factors, their complete
cross-incidence connects it even if the factors themselves have rank one.
Thus every residue of rank at least two is connected. ∎

**Lemma R.Derive.** If X is an ordinary object of size j, then

    Γ(S)_X ≅ B(X) * Γ(S_X).

**Proof.** Objects below X are its nonempty proper subsets. An ordinary
object Y properly above X is identified with Y\X. A marked pair (T,E)
incident with X has X⊂T and is sent to (T\X,E). A block through X is
sent to its complement to X, and an incident copied point already lies
outside X. These are exactly the objects of Γ(S_X). Subtracting X from
the containment relations preserves them, and all disjointness relations
are unchanged. Every object below X is incident to every remaining
object, proving the join decomposition. ∎

## A rank-two criterion at every rank

**Theorem R.Recursion.** Under the stated parameter assumptions, Γ(S)
is residually connected if and only if Γ(S_R) is residually connected
for every (t−2)-set R of points. When t=2 the statement means the
identity criterion, with R=∅.

**Proof.** For necessity choose an ordinary chain having all subset
sizes1,…,t−2 and largest member R. Its residue is literally Γ(S_R).
Every residue of a residually connected geometry is residually connected.

For sufficiency induct on t, the case t=2 being tautological. If X is
an ordinary object of size j, then every derived (t−j−2)-set in S_X
corresponds to a (t−2)-set R containing X. The hypothesis and induction
therefore show that Γ(S_X) is residually connected. Lemmas R.Boolean
and R.Derive show that Γ(S)_X is residually connected: residues in a
join are joins of residues, and any two nonempty remaining factors have
complete cross-incidence. Thus every residue of a flag containing an
ordinary object is connected when its rank is at least two.

It remains to treat flags containing only marked pairs, blocks and
copied points. There is at most one object of each such type. A residue
of a marked pair (T,E) is the join of B(T), the r−1 alternative blocks
through T, and the k−t+1 copied points of E. The last two parts are
rank-one geometries with full cross-incidence. This join is residually
connected by Lemma R.Boolean. It deals also with flags containing the
marked pair and either or both of the other special objects.

A block B₀ and an incident copied point z leave precisely the subsets
of B₀ of sizes1,…,t−1. For the top size T, the corresponding marked
object is (T,B′\T), where B′ is the unique block through T∪{z}.
Incidence is inclusion. The residue is a truncation of B(B₀), hence
is residually connected by Lemma R.Boolean.

In the residue of a block B₀ alone, its original singleton points and
the copied points outside it form a nonempty complete bipartite graph.
Every other remaining ordinary or marked object has a singleton neighbor
inside B₀. This rank-t residue is therefore connected. In the residue
of a copied point z alone, ordinary and marked objects provide all
subsets of Ω\{z} of sizes1,…,t−1. The marked object associated to a
(t−1)-set T is again determined by the unique block through T∪{z}.
Since t≥3, singleton and two-element subsets connect this entire
skeleton. Every block avoiding z attaches to its singleton points.
Thus this residue is connected as well.

Finally, the full incidence graph contains the bipartite graph of original
singleton and copied points, with incidence x≠z. There are at least
t+2≥5 points, so this graph is connected. Every other object has a
singleton neighbor. The full geometry is connected. These cases exhaust
all flags without an ordinary object, completing the induction. ∎

## Shared applications and their remaining obligations

This theorem gives the following reductions, conditional on the displayed
classical identifications of the derived designs:

| Source family | Derived linear space | Remaining rank-three calculation |
|---|---|---|
| Points and affine planes of AG(d,2) | PG(d−1,2) | Connectivity of Γ(PG(d−1,2)) |
| Subline S(3,q+1,q^e+1) | AG(e,q) | Connectivity of Γ(AG(e,q)) |
| S(4,5,11), S(5,6,12) | AG(2,3) | Connectivity of Γ(AG(2,3)) |
| S(3,6,22), S(4,7,23), S(5,8,24) | PG(2,4) | Connectivity of Γ(PG(2,4)) |

The affine and subline identifications are elementary coordinate facts.
The Mathieu identifications are retained classical design facts and must
be named in the application ledger. The theorem does not assert flag
transitivity. That separate obligation is the source's extension-fiber
property: a group must act transitively on (ordinary chain, T, B₀), then
on the alternative blocks B′ through T, and then on B′\T. A transitive
orbit at the first stage alone does not prove the other two.

For the two small Mathieu designs, the full design group order is one
third of the chamber count (respectively7920 versus23760, and95040
versus285120). The full-group identification is a retained input; once
supplied, this immediately excludes chamber transitivity. For the three
large Mathieu designs, the common extension-fiber sizes are4 and4.
`phase182_mathieu_fibers.g` checks these actual stabilizer orbits from
native Mathieu permutation groups. Their common final chamber stabilizer
has order12. Those finite checks do not by themselves prove the design
identifications, the geometric residue theorem, or every diagram and
subgroup annotation in the source.

This is a candidate shared proof component, not a measured compression
factor or an admission of another entire source contract.
