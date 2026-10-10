# Hermitian unitals in the Van Nypelseer construction

**Proposed theorem, with a complete elementary argument below.** For every prime
power (q>2), the geometry Γ(U_H(q)) in Leemans's Conjecture 1 is firm,
residually connected and flag-transitive. In fact PGU(3,q) acts regularly on its
chambers. The argument also works for q=2.

This answers the mathematical statement of Conjecture 1 in Dimitri Leemans,
*A generalization of a construction due to Van Nypelseer*, Beiträge zur Algebra
und Geometrie 46 (2005), 561–574, §4.6, p.569. The exact construction is
Construction 3 on p.565, equivalent to Construction 2 when t=2. The source
reports computations for q≤16. [Primary article PDF](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.46/no.2/b46h2lee.pdf).
The proof has been produced in this workspace; independent external review and
priority verification remain necessary before calling it a new published result.

## The geometry and its panels

Let K=F_(q²), with involution a↦a^q, and let V be a nondegenerate three-dimensional
Hermitian space over K. The classical Hermitian unital has points P equal to the
isotropic one-spaces of V, and blocks B equal to the intersections of P with
projective secant lines. It is a 2-(q³+1,q+1,1) design: each point is on q² blocks.

The three types of Γ are points Q, blocks L, and original flags (p,M), where
p∈M. Its incidences are

* Q incident with L exactly when Q∉L;
* Q incident with (p,M) exactly when Q∈M\{p};
* L incident with (p,M) exactly when M∩L={p}.

The last condition is equivalent to p∈L and L≠M. A chamber is therefore
(Q,L,(p,M)) with distinct p,Q∈M and p∈L≠M.

Every incident pair extends to a chamber. The numbers of completions of a
point–block, point–flag, and block–flag pair are respectively q+1, q²−1, and q.
For example, if Q∉L, each p∈L gives the unique completion (p,pQ). These numbers
are all at least two. Every single element lies in such a pair, so Γ is a firm
rank-three geometry. This also verifies the hypotheses of the source's Lemma 1
without relying on any ambiguity in its type indexing.

## Two easy residues and global connectedness

Fix an original flag (p,M). Its residue consists of Q∈M\{p} and blocks L through
p other than M. Every such Q is outside every such L, so the residue is the
complete bipartite graph K_(q,q²−1).

Fix a point Q. The flag-type elements of its residue are precisely (p,Qp), one
for each p≠Q. The block-type elements are blocks L avoiding Q, and incidence is
exactly p∈L. If p,r≠Q are on distinct blocks through Q, their joining block pr
avoids Q and connects them. If Q,p,r are collinear, choose s outside their common
block; the blocks ps and sr avoid Q, giving a path from p to r. Every block
avoiding Q contains a point p≠Q. Thus this residue is connected.

The whole incidence graph is connected as well. For two distinct point-type
elements Q,R, choose p outside QR. Of the q² blocks through p, at most two contain
Q or R. A remaining block is incident in Γ with both Q and R. Every block has
an outside point, and every original flag (p,M) is incident with a point of
M\{p}. Hence all three types lie in the same component.

It remains to prove connectivity of the residue of a block. This is the part
that uses the Hermitian geometry.

## A reusable connectivity observation

Suppose a group H acts transitively on a set X. Let a graph on X have the
property that, for each x∈X and each element h in a generating subset of H,
x and hx are in the same connected component. Then the graph is connected:
write an element carrying x to y as a product of generators and follow the
successive component-preserving moves.

The same argument applies to the point collinearity graph of a bipartite
incidence graph, provided every vertex of the other type has a neighbor.
When H acts regularly, the first graph is a Cayley graph or contains the
necessary Cayley edges. This observation is standard; the useful step here is
identifying the particular Hermitian residue and its generating moves.

## The block residue as a Hermitian norm shell

Fix a block L. Its projective line is a nondegenerate Hermitian two-space W:
a degenerate two-space in V would have a one-dimensional radical and exactly
one isotropic projective point, whereas a secant has q+1 such points.
Write V=W⊥Kz and scale the form or z so that h(z,z)=1. Every unital point outside
L has a unique representative v+z with v∈W and

    h(v,v)=−1.

Thus the point-type part of the block residue identifies with
X={v∈W : h(v,v)=−1}.

Two different elements v,w∈X are joined through a flag-type element of the
block residue whenever h(v−w,v−w)=0. Indeed the secant through the isotropic
points ⟨v+z⟩ and ⟨w+z⟩ meets W in ⟨v−w⟩. If this difference is isotropic, that
intersection is a point p of the block L; the original flag (p,M), where M is
the joining secant, lies in the residue and is incident with both points.
Conversely, a common flag implies exactly this condition.

Every flag-type element (p,M) of this residue has q neighboring points, namely
the q points of M other than p. It therefore suffices to connect X by isotropic
difference moves.

## A self-contained SU(2,q) calculation

A nondegenerate Hermitian plane over a finite field has an isotropic basis
e,f with h(e,e)=h(f,f)=0 and h(e,f)=1. In this basis its Gram matrix is
J=[[0,1],[1,0]]. Choose nonzero δ∈K with δ^q=−δ; such a δ exists because the
trace map K→F_q has a one-dimensional kernel. This works in characteristic two
as well, when the trace kernel is F_q.

For a matrix A=[[a,b],[c,d]] of determinant one, the unitary equation is

    A^(-1) = J A^(q,T) J.

Comparison of entries shows that a,d∈F_q and b,c∈δF_q. Conversely these
conditions together with determinant one imply the unitary equation.
Conjugation by diag(δ,1) therefore identifies SU(W) with SL(2,q), since
δ²∈F_q^*. In particular |SU(W)|=q(q²−1), and it is generated by the two
families

    U_t=[[1,t],[0,1]],  V_t=[[1,0],[t,1]],   t∈δF_q.

The generation assertion follows directly from Gaussian elimination in
SL(2,q): elementary upper and lower matrices generate it. Diagonal determinant
one matrices are also products of these elementary matrices, so there is no
remaining diagonal factor.

The group SU(W) acts freely on X. An element fixing a vector v of nonzero norm
preserves the decomposition W=Kv⊥v^⊥. It is the identity on Kv and acts by a
scalar on the one-dimensional orthogonal complement. Determinant one forces
that scalar to be one.

It also acts transitively. To see this without invoking Witt's theorem, count
X in an orthonormal basis. For any c∈F_q^*, the equation

    x^(q+1)+y^(q+1)=c

has 2(q+1)+(q−2)(q+1)²=q(q²−1) solutions: the norm fiber over zero has one
element, and each nonzero norm fiber has q+1 elements. Hence |X|=|SU(W)|, and
the free action has a single orbit.

Finally, U_t(v)−v is a multiple of e, and V_t(v)−v is a multiple of f. Both
differences are isotropic. When t≠0 the difference is nonzero for every v∈X:
a vector in either isotropic coordinate axis cannot have norm −1. Thus every
nonidentity elementary generator gives a permitted edge in the point
collinearity graph of the block residue. The connectivity observation proves
that graph, and hence the entire block residue, connected.

All residues of rank at least two are now connected: for a rank-three geometry
these are exactly the whole geometry and the residues of single elements.
Therefore Γ is residually connected.

## Chamber transitivity, in fact regularity

The projective unitary group PGU(3,q) acts on the construction because it
preserves points, blocks, and the displayed incidences. It is transitive on
ordered pairs of distinct isotropic points: choose representatives e,f of a
pair, rescale so that h(e,f)=1, and complete them by a vector of norm one
orthogonal to both. Mapping one such hyperbolic basis to another is a unitary
isometry.

Fix an ordered pair p=⟨e_1⟩ and Q=⟨e_3⟩, with Hermitian form

    h(x,x)=x_1 x_3^q + x_1^q x_3 + x_2^(q+1).

The block M=pQ is fixed. A projective line through p other than M has the form

    L_t=⟨e_1,e_2+t e_3⟩,  t∈K.

L_0 is tangent to the unital at p. For t≠0 the equation
x t^q+x^q t+1=0 has q solutions x, so L_t is a secant with q+1 unital points.
Thus the possible blocks L≠M through p are exactly the L_t with t∈K^*.

The projective unitary stabilizer of the ordered pair contains

    D_a=diag(a,1,a^(−q)),  a∈K^*,

which sends L_t to L_(t a^(−q)). This is transitive on K^*, proving chamber
transitivity. As every flag extends to a chamber, the action is flag-transitive.

Moreover this ordered-pair stabilizer is precisely the displayed torus:
a unitary map preserving the two isotropic one-spaces also preserves their
one-dimensional orthogonal complement, and normalizing the middle entry by a
central norm-one scalar gives exactly D_a. Its action on K^* is free. Therefore
the stabilizer of a chamber is trivial, and PGU(3,q) acts regularly on chambers.
The chamber count is (q³+1)q²q(q²−1)=q³(q³+1)(q²−1), in agreement with its order.

## Audit limits and priority search

The independent exact GAP script [hermitian_unital_check.g](hermitian_unital_check.g)
constructs the projective isotropic points and every secant directly in a
diagonal Hermitian form, rather than taking the norm-shell description as the
definition. It verifies design sizes and pair uniqueness, representative
residues of all three types, global point–block anti-incidence connectivity,
and a separate root-group/norm-shell orbit calculation. All checks passed:

| q | Unital points | Blocks | Block-residue vertices | Block-residue edges | SU(2,q) orbit |
|---|---:|---:|---:|---:|---:|
| 2 | 9 | 12 | 15 | 18 | 6 |
| 3 | 28 | 63 | 56 | 96 | 24 |
| 4 | 65 | 208 | 135 | 300 | 60 |
| 5 | 126 | 525 | 264 | 720 | 120 |

The complete output is [hermitian_unital_check.log](hermitian_unital_check.log).
These are representative residues; the proof's unitary transitivity supplies
their equivalence for other elements of the same type. The script itself does
not enumerate the full chamber action of PGU(3,q).

The only finite-field ingredients are the trace/norm fiber sizes and elementary
Hermitian linear algebra; generation and orbit size were proved above. There
is no enumeration-dependent step in the all-q proof. Small-field computation
is a separate implementation check, not an infinite-family proof.

Two independent exact-title searches, and searches combining “Leemans”, “Van Nypelseer”,
“Hermitian”, “unital”, and “conjecture”, located the original primary article
and bibliographic references, but no later resolution. The indexed OpenAlex
citing-paper query for work W1593999718 returned no records; its response is
saved as [van_nypelseer_forward_openalex.json](sources/van_nypelseer_forward_openalex.json).
This is weak negative evidence, since that index may omit citations. The 2026
linear-space triality paper studies a different construction, called Δ, and
does not provide a resolution of this Γ conjecture. This is not a complete
citing-paper/priority audit. Accordingly the safe claim is that the above is a
proposed proof of the published conjectural statement, not a verified priority
claim about an open problem as of 2026.
