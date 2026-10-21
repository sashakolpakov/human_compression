Written mathematical review
===========================

External paths and first-shell disjointness
------------------------------------------

For a simple external path between distinct cycle vertices, one cycle arc has
parity opposite to its length. Its union with the path is a simple odd cycle.
Minimality makes that arc at least ell-r long; the complementary arc therefore
has length at most r and the same parity as r. Chords contradict odd minimality.
A vertex outside C joined to two cycle vertices gives an external path of length
two, hence a two-edge cycle arc and a quadrilateral, contradicting girth at least
six. Thus the ell first-shell sets are disjoint and each has k-2 elements.

First-shell matching
--------------------

An edge between S_i and S_j supplies an external three-edge path. The short odd
arc has length one or three; length one gives a quadrilateral. Thus j-i is plus
or minus three. Two neighbors in one such set give another quadrilateral. If a
vertex in S_i has one neighbor in each of S_(i-3),S_(i+3), these three shell
vertices form a four-edge external path between c_(i-3) and c_(i+3). The cycle
arc complementary to the six consecutive edges has length ell-6, positive and
odd even at ell=7. The union is simple and has odd length ell-2. This contradicts
minimality. Every shell vertex therefore has at most one shell neighbor.
It has one cycle neighbor, so at least k-2 neighbors in the remaining set R.

Second-shell capacity
---------------------

A vertex in R cannot meet one S_i twice, since that gives a quadrilateral. Two
of its shell neighbors yield an external path of length four. The corresponding
short even cycle arc has length two or four, giving differences plus/minus two
or four. Multiplication by the inverse of two modulo odd ell identifies the
root-index graph with the square of a cycle. In a clique containing zero, the
other vertices belong to {-2,-1,1,2}. The three forbidden pairs listed in the
proof are nonedges for every ell>=7, and every three-element subset of these
four contains a forbidden pair. Thus the clique size is at most three. The bound
is sharp since {0,1,2} is a clique. This proof includes ell=7 and requires the
explicit ell>=7 hypothesis; the square of the five-cycle is complete.

Summation and scope
-------------------

There are at least ell*(k-2)^2 edges from S to R, and each R vertex receives at
most three. Adding ell cycle vertices and ell*(k-2) shell vertices proves
ell*(k-1)+ceil(ell*(k-2)^2/3)=ceil(ell*(k^2-k+1)/3). All counts remain valid
for k=2. For disconnected graphs use a component with a shortest odd cycle;
its degree is still k and extra components only increase the order.

Biaffine interface
------------------

Substituting lambda=(q-1)^2*(q-2) into the separately declared Moore-tree
interfaces gives D=(q-1)^2, general lower bound 2q^2-1 and bipartite bound 2q^2.
The complete biaffine construction at 2q^2 is another explicit parent interface.
For odd q, the handshaking identity excludes the odd smaller order. For even
prime-power q>=8, a competitor at the smaller order would be nonbipartite and
have ell>=7. The difference of three times the competing bounds is
7*(q^2-q+1)-3*(2q^2-1)=(q-5)*(q-2)>0. Thus it cannot exist. At q=4 the
shell inequality only gives 31 and does not prove the needed exclusion.

The actual F012 Table 2 row has literature lower 31, new lower 32, new upper 32
and one graph at the upper bound. Only the lower bound 32 is used. The census
completeness is retained as an external finite premise; uniqueness is not used.
The only even prime power between 3 and 8 is 4. Consequently the combined
result covers every q>=3, subject to the two parent interfaces and this retained
census. Source Theorems 4.1--4.2 print an incorrect even-girth exponent; this
companion explicitly uses the parent's corrected expressions rather than that
literal formula. No uniform conclusion is inferred from the small diagnostics.

No requested correction
-----------------------

Every argument above is present in the frozen text. No additional hypothesis,
new mathematical repair or author-file change is requested. The separate full
parent review must assess the remaining source clauses, constructors, small
graph certificates, corrected bounds, Suzuki proof and all retained dependencies.
