# Suzuki graph pentagons from a four-parameter matrix word

9 October 2026. Proposed proof of Conjecture 3.2 in Araujo-Pardo–Leemans,
[*Edge-girth-regular graphs arising from biaffine planes and Suzuki groups*](https://arxiv.org/abs/2108.06636),
published in Discrete Mathematics 345 (2022), 112991. The proof is a uniform
matrix calculation; finite examples are checks, not its justification.
External review and publication priority remain outstanding.

## Statement and exact source identification

For q=2^(2e+1), e≥1, the source constructs a graph on cosets of a subgroup
H≅E_q:C_(q−1) of G=Sz(q), with edge stabilizer D_(2(q−1)). It proves girth
five and conjectures that each edge belongs to exactly q−1 pentagons.

**Theorem.** Its graph is edge-girth-regular with parameters

    (number of vertices, degree, girth, cycles per edge)
       = (q(q²+1), q, 5, q−1).

Use the standard Suzuki matrices from Bray–Bäärnhielm,
[*A new method for recognising Suzuki groups*, equations (1)–(5)](https://arxiv.org/abs/1706.05697).
Write θ=2^(e+1), so (x^θ)^θ=x² in F_q, and put

    z(a) = [[1,0,0,0], [0,1,0,0], [a,0,1,0], [a^θ,a,0,1]],
    t(λ) = diag(λ^(1+θ), λ, λ^(-1), λ^(-1-θ)),
    w = antidiag(1,1,1,1),
    Z = {z(a): a in F_q},  T = {t(λ): λ in F_q*},  H=ZT.

Here Z is the center of the standard Sylow 2-subgroup U. The subgroup H has
order q(q−1); w normalizes T by inversion; H∩wHw=T. These facts follow from
the displayed triangular matrices and their diagonal entries. In particular
z(a)z(b)=z(a+b), and every z(a) is an involution or the identity.

This is the exact source subgroup pair, up to conjugacy. Move its ordered
nucleus/point pair (n,p) to the standard ordered ovoid pair (infinity,zero).
Its order-q elementary abelian subgroup consists of all involutions in the
Sylow 2-subgroup fixing infinity, hence is Z. Its common order-(q−1)
stabilizer fixes both infinity and zero, hence is T. Its edge stabilizer is
N_G(T)=<T,w>. Thus its vertex stabilizer is ZT and its edge stabilizer is
<T,w>, as above. Passing from the source's right cosets to left cosets by
inversion gives the same undirected graph.

## A unique coordinate for each next step

Use left cosets gH as vertices. The neighbors of gH are exactly

    g z(a) w H,       a in F_q.

These q vertices are distinct, since z(b)^(-1)z(a) belongs to H∩wHw only
when a=b. The matrix w does not belong to H, so there are no loops. Since
w²=1 the graph is undirected. The group G is vertex transitive and H is
transitive on its q neighbors, so G is arc transitive. The group order
|G|=q²(q²+1)(q−1) gives q(q²+1) vertices.

After a step represented by w, choosing parameter zero for the next step
backtracks, since w z(0) w=1. It is the unique backtracking choice, by the
uniqueness of the neighbor coordinates. Consequently walks of length five
starting with the fixed oriented edge H,wH are parametrized uniquely by

    (a,b,c,d) in F_q^4,

and their terminal vertex is W(a,b,c,d)H, where

    W(a,b,c,d)=w z(a) w z(b) w z(c) w z(d) w.

Such a walk closes if and only if W belongs to H. Nonbacktracking means
a,b,c,d are nonzero. There is no division by two in counting cycles through
the fixed oriented edge: each undirected pentagon has exactly one traversal
that starts with that directed edge.

## Three entries solve the entire closing equation

Write A=a^θ, B=b^θ, C=c^θ, D=d^θ. Direct multiplication, over a field of
characteristic two, gives the following three entries (indices start at one):

    W_32 = bc+1,
    W_12 = ABc+abc+a+c,
    W_43 = BCd+bcd+b+d.

Every matrix in H has these entries zero. The first equation gives bc=1.
The second then reduces to (AB+1)c=0, so AB=1. Frobenius is injective;
therefore ab=1. Thus c=a and b=a^(-1). The third equation now reduces to
b+d=0, hence d=b=a^(-1). We have proved that closure forces

    (a,b,c,d)=(a,a^(-1),a,a^(-1)),     a≠0.             (1)

Conversely, full matrix multiplication gives

    W(a,a^(-1),a,a^(-1))
       = [[A,0,0,0], [0,a²/A,0,0],
          [A/a,0,A/a²,0], [1,a/A,0,1/A]]
       = z(a^(-1)) t(a^(2−θ)).                       (2)

For the diagonal identity, (a^(2−θ))^(1+θ)=a^θ because θ² acts as
squaring. The lower entries agree with z(a^(-1)) because (a^(-1))^θ=A^(-1).
Thus (2) belongs to H. Equations (1)–(2) classify **all** closing walks,
uniformly in q, and there are exactly q−1 of them.

## Girth, without the source's incidence-graph argument

No length-three closed walk starts with the fixed arc: the (3,2) entry of
`w z(a) w z(b) w` is 1, whereas all H matrices have that entry zero.

For a length-four walk the (1,2) entry of
`w z(a) w z(b) w z(c) w` is a^θ b. Membership in H forces this entry to
vanish. A nonbacktracking walk has a,b≠0, so this is impossible.

The walks in (1) do not backtrack. A closed nonbacktracking walk of length
five in a simple graph with no triangles or four-cycles is a pentagon.
Therefore the girth is five, and every edge belongs to exactly q−1
pentagons. This proves the theorem. ∎

Connectivity, already established for the source family, also follows from
the standard maximality of N_G(T) in Sz(q): <H,w> contains N_G(T) properly
and hence equals G. This structural fact is not needed for the pentagon count.

## Relation to the common theory and verification scope

This is a normal-form solution of a coset-walk equation. The torsor formulation
turns closed paths into subgroup membership; the faithful four-dimensional
representation reduces membership to three forced zero entries. The remaining
parameter is a single point of F_q*, giving the exact answer q−1. Merely
recognizing that a permutation representation exists would not provide (1).

The [independent GAP coset-graph calculation](phase3_suzuki_probe.g) at q=8
gives 520 vertices, degree 8, no triangles or squares through the base edge,
and seven pentagons; its [transcript](suzuki_coset_check.log) passes. It
constructs the graph from a permutation group and subgroup cosets, independently
of the displayed four-dimensional matrices.

The [symbolic checker](suzuki_cycle_check.py) verifies the short-walk
obstructions, the three forced entries, and all sixteen entries of (2) over
the Laurent-polynomial ring in characteristic two. Its [report](suzuki_cycle_check.json)
passes without specializing to sample field values.

The [Lean certificate](formal/SuzukiPentagons.lean), checked with the pinned
toolchain in [formal/README.md](formal/README.md), proves the complete
equivalence `W(a,b,c,d) in H` if and only if (1), assuming a characteristic-two
field with a field automorphism θ satisfying θ²(x)=x². It also checks the
short-walk matrix entries. The [compiler report](formal/SuzukiPentagons.check.json)
has exit code zero and only the standard axioms `propext`, `Classical.choice`
and `Quot.sound`, with no `sorryAx`. The Lean predicate named `BorelPart`
means precisely the displayed set ZT, not the full Suzuki Borel subgroup UT.

The finite-field instantiation, identification of the source subgroup pair,
and bijection from the matrix solutions to graph pentagons are written
mathematics, not parts of this Lean certificate. The
[independent audit](phase3_suzuki_audit.md) checked those interfaces, including
simplicity of the source graph and the absence of a cycle-counting factor.
External review remains outstanding. The
[combined certificate](suzuki_cycle_certificate.json) records sources,
verification scope and artifact hashes.

A targeted literature search on 9 October 2026 found the original conjecture
and later work disproving a separate extremality conjecture, but no resolution
of this pentagon-count conjecture. The 2025 Glinskikh–Tsiovkina graph family
has different parameters q²(q²+1), q−1 and a torus vertex stabilizer; it is
not this family. Absence from these searches does not establish priority.
