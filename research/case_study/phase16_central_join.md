# Central joins and an exact bounded-core classification

10 October 2026. New private followup to the frozen
[fixed-excess theorem](phase16_fixed_excess.md). This file does not
alter that proof or its finite-acceptance statement. The construction
below supplies the sufficiency that the earlier theorem deliberately
left to acceptance tests. Independent review is pending.

## 1. A marked central cocycle construction

Fix a path with vertex set V={1,...,d}. Let I be any subset, O=V\I,
and let H be a finite two-group marked by generating involutions
h_i, i in I, with actual IP and the induced-forest commutation graph.
In particular, adjacent vertices in I do not commute. The independent
Frattini classes give characters

    chi_i:H -> F2,     chi_i(h_j)=delta_(ij).

Put B=H times F2^O and extend these to coordinate characters chi_v
on B, for every vertex v. Let E_0 consist of the path edges not wholly
in I, and let Z=F2^(E_0). Orient these edges from left to right and set

    beta(b,c)_e = chi_head(e)(b) chi_tail(e)(c).

Define the group J(H,I) on B times Z by

    (b,z)(c,t) = (bc, z+t+beta(b,c)).                (1)

All characters are homomorphisms. Expanding them proves
beta(b,c)+beta(bc,a)=beta(c,a)+beta(b,ca), so (1) is associative.
The identity is (1,0), and inverses follow immediately. The Z factor
is central. This is a cocycle construction on a possibly nonabelian
base; bilinearity of the characters, rather than commutativity of B,
is what proves the cocycle identity.

Mark the group by (h_i,0) for i in I and by the corresponding outside
coordinate involutions for i in O. Each is an involution: beta is zero
on a pair with the same single vertex character. The original H
embeds, since beta restricted to H times H is zero. Every edge in E_0
has its individual central basis vector as the commutator of its two
markers. Nonedges commute, and edges inside I retain their nontrivial
H commutators. The markers generate the whole group: they generate
the base, and the edge commutators supply all of Z.

## 2. Exact parabolics and the kernel

For S contained in V the marked parabolic has the following exact
coordinate set:

    J(H,I)_S = H_(S intersect I) times F2^(S intersect O)
                 times F2^(E_0(S)),                         (2)

where E_0(S) contains the edges in E_0 with both endpoints in S.
The set on the right is a subgroup containing the indicated markers,
because the characters of absent vertices vanish. Conversely, products
of the available markers supply every base coordinate, and their edge
commutators supply every remaining central coordinate. Thus equality
holds, even though the displayed subgroup is not generally a direct
product with its written multiplication.

Taking coordinate-set intersections in (2) and using IP in H proves
the full marked IP in J(H,I). No order or genericity test is required.
Also

    |J(H,I)| = |H| 2^(|O|+|E_0|).                  (3)

Every commutator has zero vertex characters. Consequently beta
vanishes whenever either argument lies in the embedded H' or in Z.
The derived group is the direct product of H' with Z: one inclusion
comes from commutator collection, and the reverse comes from the
embedded H and the individual cross-edge commutators. It follows that

    gamma3(J(H,I)) = gamma3(H)                      (4)

inside the embedded H. Formula (2) shows that its marked support is
exactly its support in H. The construction is natural under ordered
marked isomorphisms of H, since these preserve every character chi_i.

## 3. Every compatible canonical core attaches

Fix k>=1 and d>=3. Choose a subset J of at most 3k path vertices in
at most k intervals, put I=N[J], and let H be a finite two-group marked
on I with the induced-forest IP and noncommuting edges. Require

    |gamma3(H)|=2^k,
    supp_H(gamma3(H))=J.                           (5)

These are finite core conditions. By the forest theorem,
|H|=2^(|I|+e(I)+k). Since |O|=d-|I| and
|E_0|=(d-1)-e(I), equation (3) gives

    |J(H,I)|=2^(2d-1+k).

Sections 1–2 prove that this is a nondegenerate string C-group.
Its canonical kernel has order 2^k and support exactly J, so its
closed-neighborhood core is the original H. Thus every core satisfying
(5) attaches; the order/IP acceptance checks of the earlier framework
are unnecessary for these cores.

Conversely, let G be any group in the fixed-excess theorem and extract
its canonical J and H. The cocycle group J(H,I) satisfies every relation
in that theorem's exact reconstruction presentation. The core and
string relations are immediate. The outside edge products have order
four. For an outside triple S, |S intersect J|<=1. Restriction of the
canonical kernel in H gives

    gamma3(H_(S intersect I))
       = gamma3(H) intersect H_(S intersect I) = 1,

using support J, actual IP and the trivial intersection of a cyclic
marker with H'. The version of (4) for the parabolic (2) therefore
makes every outside triple class two. Hence the reconstruction
presentation maps onto J(H,I). Both groups have the displayed order,
so it is an isomorphism.

We obtain a bijection between ordered marked groups of rank d and
excess k and their canonical pairs (J,H) satisfying (5). Marked
isomorphisms preserve the index of each marker. Necessity of the
support and size bounds is the frozen theorem; sufficiency and
uniqueness are proved here. The finite library of H has at most 5k
markers and order at most 2^(11k-1). This is an exact bounded-core
classification, with the finite library specified by effective
conditions rather than an already computed list of group names.

For k=0 use I=J empty and H=1. Construction (1) is the path-cocycle
group C_d, the unique group of excess zero.

## 4. Central edges describe the attachment

In a group extracted from the theorem, every edge not wholly in I
has a central commutator of order two. Its endpoint powers vanish at
weight three, and both containing triples are class two; all farther
markers commute with its endpoints by the string relation. Thus the
long ordinary segments interact with the core through independent
central edge coordinates. They do not carry additional higher
commutator or action parameters.

This does not say that G is a direct product of its core and its
complement. Each edge in E_0 contributes the nontrivial cocycle in (1).
It also does not imply that the subgroup generated ordinarily by the
local triple kernels is the entire kernel: the frozen order-1024
warning remains valid within a core.

## 5. Rational generating function and eventual polynomial counting

Let a_k(d) be the number of ordered marked isomorphism classes of rank
d and excess k, with d>=3. For each fixed k>=1, this number is a
polynomial in d of degree exactly k for every d>=6k-1. More precisely its generating
function is a rational function whose only possible pole is z=1,
of order at most k+1, up to a polynomial correcting d<3.

Here is an exact finite description of its coefficients. A support
pattern records:

* the t<=k positive run lengths of J, of total length at most 3k;
* each internal gap as length 1, length 2, or length at least 3;
* each end gap as length 0 or length at least 1.

There are finitely many such patterns. For a long internal gap record
the minimum length three; for a nonzero end gap record the minimum
length one. Let b be the resulting minimum total path length, and r
the number of long internal gaps plus nonzero end gaps. Then r<=t+1
and every concrete gap realization has length

    d=b+n_1+...+n_r,       each n_j>=0.              (6)

The ordered induced forest on I=N[J], together with its distinguished
J-subset, depends only on the pattern. Extra length in a long gap
adds outside vertices and never changes that bounded ordered core.
Let m be the number of core marked-isomorphism classes satisfying
(5) for this finite pattern. It is a finite nonnegative integer,
computable by the finite table enumeration of the earlier theorem.
By the bijection in section 3, the pattern contributes exactly

    m z^b/(1-z)^r                                  (7)

to the generating function, where r=0 means just m z^b. Different
patterns or different gap vectors produce different canonical J sets;
different cores produce different extracted marked groups. There is
therefore no overcounting in summing (7).

For r>=1, the coefficients are eventually
m binomial(d-b+r-1,r-1), polynomials of degree at most k. Terms with
r=0 affect only finitely many ranks. Summing finitely many terms proves
eventual polynomiality. The retained source construction, or its
independent [fiber-product rederivation](phase16_fiber_products.md),
gives a_k(d)>=binomial(d-2,k) for sufficiently large d. Thus the eventual
polynomial has degree exactly k. Finally every minimum length satisfies
b<=3k+3(k-1)+2=6k-1. When r=0 the sharper bound is b<=5k-2, so those
isolated terms have already vanished for d>=6k-1. Thus every remaining
term has its polynomial coefficient formula throughout d>=6k-1.
This is a sufficient stabilization bound, not a claim of the least
one. No claim is made here to have computed the coefficients for
arbitrary k.

## 6. Status and dependency boundary

The support bound, finite core sizes and necessary reconstruction
presentation are retained from the frozen fixed-excess theorem. The
cocycle, exact parabolic formula, automatic attachment and counting
argument are proved above. The order-k lower growth bound retains the
prescribed toroidal-section construction, now separately rederived by
the fiber-product note. No finite-group catalogue or experimental
pattern extrapolation is an input to the uniform proof.

This classification is in terms of a finite core library with exact
conditions. It is not a list of that library, a polynomial-time
algorithm or an unmarked-group classification. No publication priority,
external peer review or full Lean formalization is asserted.
