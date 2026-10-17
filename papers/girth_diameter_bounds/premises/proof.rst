Boolean certificates for six consecutive layers
===============================================

Status: proposed method, requiring distinct review and actual certificates.
No graph exclusion is obtained from this document alone.

Consider a simple graph of degree four and girth at least five. Let six
consecutive nonsingleton BFS layers, beginning after the root layer, have
total size 21. Choose consecutive vertices u,v in their middle layers on
a geodesic crossing the interval. The previously accepted adjacent-ball
argument labels their other neighbors A1,A2,A3 and B1,B2,B3. Each of the
nine positions ij contains at most one common second neighbor Cij. If
position ij is missing, use a private neighbor Uij of Ai and a private
neighbor Vij of Bj. These names denote distinct vertices. The union of
the two balls has 26-m vertices when m positions are occupied.

This method treats only m=5 or m=6. In the latter case one additional
vertex X completes the section; in the former there are no extras. The
geodesic can be labelled U11,A1,u,v,B1,V11 at layers 0,1,2,3,4,5. Cell 11
is missing because A1 and B1 differ by three BFS indices. Private names
within each parent group are arbitrary, so choosing U11,V11 for these
two geodesic vertices loses no graph. The remaining holes must be specified
in each request. One fixed pattern never excludes all other patterns.

Encoding
--------

For every vertex v, six Boolean variables H(v,h) describe its unique layer.
For each unordered pair not incident to the eight saturated centres and
parents, a Boolean variable describes an edge. Prescribed edges are the
constant true; other edges incident to those eight vertices are false.
The constants are necessary because their four prescribed neighbors are
already distinct. There is no restriction on edges among remaining vertices
beyond the following necessary conditions.

The layer variables have exactly one true entry. The six geodesic anchors
are fixed as above. Every layer contains at least two vertices. An edge
can only join indices differing by at most one. Every internal vertex has
four neighbors in the section; all vertices have at most four. A vertex
at local index zero has at most three neighbors here, since its original
nonroot BFS layer supplies a predecessor outside the section. It may have
zero neighbors here: in particular no unjustified positive-degree condition
is imposed on an extra vertex at this boundary. Each vertex at index h>0
has a neighbor at h-1. There is no condition requiring a successor.

For each pair a,b, at most one vertex is adjacent to both; this is exactly
the absence of a cycle of length four in a simple graph. If a,b themselves
are adjacent, they have no common neighbor, excluding triangles. Cycles of
length five are allowed. We reuse the Boolean Formula gates and cardinality
encoding from the acquired F012 certificate method, but do not call its
graph builder: that builder also excludes five-cycles and would be wrong
for the present problem.

The threshold recurrence is s(0)=true, s(j)=false initially for j>0, and
s_new(j)=s(j) or (x and s(j-1)) when one new literal x is read. By induction
it says that at least j of the literals read so far hold. Degree bounds use
thresholds four and five, and nonsingleton layers use threshold two. Every
auxiliary OR/AND variable is defined by equivalence clauses from the retained
Formula implementation. Thus any actual section extends to a satisfying
assignment by its literal adjacency, layer indices and gate evaluations.

Certificate and limits
----------------------

For an exact requested hole pattern, the builder emits deterministic DIMACS
clauses and a map of primary variables. A solver's UNSAT answer alone is
insufficient. The proposed route retains its proof stream, checks every
addition by the already reviewed reverse-unit-propagation reader, and requires
a checked empty clause. Deletions can be ignored soundly: retaining more
previously justified clauses cannot invalidate their consequences. A second
read must reconstruct the exact DIMACS file and verify the actual proof
against it before a local exclusion is adopted. The graph-to-clause argument
also needs distinct mathematical review. This is an ordinary computational
certificate, not a Lean proof or a complete F009 result.

A satisfying assignment is only a candidate local fragment. A timeout or
incomplete proof excludes nothing. Covering all hole patterns requires a
separate, explicit finite coverage argument. Neither an automatic sequence
of calls nor an extension of the existing resource bounds follows from this
method proposal. The Moore bound, adjacent-ball argument and BFS framework
retain their existing source attribution.
