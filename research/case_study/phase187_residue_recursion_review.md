# Independent assessment: reduction to derived rank-three geometries

Phase187. This is an independent mathematical assessment of the proposed
general residue reduction for L092 Construction2. It is separate from the
frozen phase183 subline review and from phase186's full source expansion.
No additional source or conjecture credit is attached to this note.

The proposal is correct under the firm parameters below. Necessity needs
one precise qualification: the residue at a single ordinary object R is
a join. Connectedness of that join alone does not imply connectedness of
the factor of interest. Taking a complete ordinary chain ending in R
removes the other factor and gives the required implication.

## Statement

Let S be an S(t,k,v), with t≥3, k≥t+1 and

    r=(v−t+1)/(k−t+1)≥3.

For X⊆Ω, |X|≤t−2, let S_X be the derived Steiner system on Ω\X, whose
blocks are B\X for the blocks B containing X. It has parameters
S(t−|X|,k−|X|,v−|X|). Let Γ denote literal Construction2, including the
rank-three instance when the first parameter is two. Then

    Γ(S) is residually connected
      iff Γ(S_R) is residually connected for every |R|=t−2.

No transitivity assumption is needed. No identification of a derived
design with a classical plane or a Mathieu design is built into this
statement. Those are separate inputs in applications.

## The construction and firmness

Use source types 1,…,t+1. The ordinary objects of type j, 1≤j≤t−2,
are j-subsets. The marked objects are m=(T,E), where |T|=t−1,
|E|=k−t+1, T∩E=∅ and T∪E is a block. The remaining types are blocks
B₀ and copied points z. Ordinary objects form inclusion chains, and
X is incident with m,B₀,z precisely when X⊆T, X⊆B₀, z∉X,
respectively. The three exceptional incidences are

    m∼B₀ iff B₀∩(T∪E)=T;
    m∼z iff z∈E;
    B₀∼z iff z∉B₀.

The first equivalence uses the Steiner property: distinct blocks through
T have intersection exactly T. The blocks through T partition Ω\T by
their tails, giving exactly r such blocks. All derived designs in the
statement retain the same values of k−t+1 and r, hence the firm parameter
conditions are inherited.

Here is a direct flag-extension check, avoiding any dependence on an
unstated geometry axiom. Let A be the largest ordinary member of a flag,
or the empty set when there is none. If a marked object is present, its
set T contains the whole ordinary chain. Choose a missing block among
the r−1 alternatives through T, and a missing copied point in E; these
choices meet any already fixed block or copied point. If a block B₀ is
present but no marked object, extend A to a (t−1)-subset T of B₀ and
choose a copied point z outside B₀ if it is not already prescribed. The
unique block through T∪{z} supplies the marked object. If only a copied
point is prescribed, extend A to T⊆Ω\{z}, take the unique block through
T∪{z}, and select an alternative block through T. If none of the three
exceptional objects is present, first choose T containing A, then a block
through T, a point in its tail, and an alternative block through T.
In each case complete the original inclusion chain to all subset sizes
1,…,t−2 inside T. Thus every flag extends to a chamber.

The panels missing an ordinary type have two completions. The other
three panel sizes, in marked/block/copied-point order, are

    k−t+2, r−1, k−t+1.

For the marked panel, its largest ordinary set R has size t−2; choose
the additional point of T in B₀\R and use the unique block through
T∪{z}. The other counts follow directly from the tails through T. All
these sizes are at least two. This recovers the sufficient direction of
the source's firmness lemma in explicit form; it is not a new claim of
priority for that lemma.

## Exact residue at an ordinary object

Let X_j be an ordinary object. Its residue is the join

    BooleanProper(X_j) * Γ(S_Xj).

The first factor consists of the nonempty proper subsets of X_j, with
their original ranks. The second factor has the following explicit map:

| Object in the residue above X_j | Object in Γ(S_Xj) |
|---|---|
| Ordinary Y⊃X_j | Y\X_j |
| Marked (T,E), T⊃X_j | (T\X_j,E) |
| Block B₀⊃X_j | B₀\X_j |
| Copied point z∉X_j | z |

All six kinds of inclusion or exceptional incidence are preserved by
these maps. Every object of the first factor is incident with every
object of the second. In particular it is incident with every copied
point because those points lie outside X_j. The displayed decomposition
is an isomorphism of typed incidence structures, not merely a numerical
description of a residue.

The Boolean factor is residually connected. A flag divides its residue
into joins of proper-subset geometries on the intervals between successive
fixed sets. An interval of rank at least two is connected through its
singletons and two-subsets; its remaining objects attach to singletons.
Two nonempty intervals are completely cross-incident. Rank-zero factors
are harmless, and a rank-one factor has no residual-connectivity condition
on its own. The same observation proves that a join of residually
connected geometries is residually connected.

## Necessity and the induction for ordinary flags

Fix R of size t−2 and choose a complete chain

    X₁⊂X₂⊂⋯⊂X_(t−2)=R, with |X_j|=j.

Its residue has exactly the marked, block and copied-point types. The
previous map identifies it with Γ(S_R). A residue of a residually
connected geometry is residually connected, since its flag residues are
also flag residues of the original geometry. This proves necessity.

For sufficiency, induct on t, taking t=2 as the tautological starting
case. At X_j the derived system has strength t−j<t. Its final two-design
derivatives are precisely S_R for the sets R⊇X_j of size t−2. By the
induction hypothesis Γ(S_Xj) is residually connected. The Boolean join
therefore is residually connected. It follows that the residue of every
flag containing an ordinary object is connected whenever its rank is
at least two. This handles flags containing several ordinary objects
and any additional exceptional objects at once.

## Flags containing only exceptional objects

There remain just the following cases; no orbit reduction is used.

**A marked object m=(T,E) is fixed.** Its residue is the join of the
proper-subset geometry on T, the discrete set of r−1 alternative blocks
through T, and the discrete set E of copied points. All cross-incidences
are present by the Steiner property. Fixing an additional block or copied
point deletes the corresponding discrete factor. The remaining residue
is connected whenever it has rank at least two. In the boundary case
t=3 with both additional objects fixed the residue has rank one, so no
connectivity claim is required.

**A block B₀ and a copied point z are fixed.** Here z∉B₀. Each marked
object is uniquely specified by its (t−1)-subset T of B₀: use the unique
block through T∪{z}. Consequently the residue is the inclusion geometry
of all subsets of B₀ of sizes 1,…,t−1. As t≥3 it includes points and
two-subsets, which give a connected graph; every remaining object has
a point neighbor.

**Only a block B₀ is fixed.** The original points in B₀ and copied
points outside B₀ form a nonempty complete bipartite subgraph. Other
ordinary subsets of B₀ attach to copied points. Marked objects attach
to the original points of T⊆B₀. The residue is connected.

**Only a copied point z is fixed.** The ordinary objects are all subsets
of Ω\{z} of sizes 1,…,t−2, and the marked objects are in bijection with
all (t−1)-subsets T of Ω\{z}, through the unique block T∪{z} determines.
Together these form the subset inclusion geometry on sizes 1,…,t−1,
which is connected through points and two-subsets. Every block avoiding
z has an original-point neighbor and attaches to this graph.

**The empty flag.** Original and copied points form K_(v,v) with its
matching removed, connected since v≥3. Every block and every marked
object has an original-point neighbor. Every ordinary object of size
at least two has such a neighbor as well. Thus the full graph is connected.

These cases exhaust the eight possible subsets of the three exceptional
types. Together with the induction they prove sufficiency.

## Attribution and review boundary

Construction2 and its firmness criterion are retained from the primary
L092 body. The source already uses derived geometries in its individual
family arguments. The present assessment verifies the precise general
equivalence and records all remaining flag cases; it does not assert
that the underlying induction is historically new.

The equivalence is a reusable reduction. It does not by itself classify
which rank-three geometries are residually connected, establish flag
transitivity, or identify a derived design with a named classical design.
Those contracts must be discharged independently before applying it to
the affine, inversive or Mathieu branches. There is no Lean certificate
for the statement in this note. A general source-count or compression
claim is therefore not inferred from it.
