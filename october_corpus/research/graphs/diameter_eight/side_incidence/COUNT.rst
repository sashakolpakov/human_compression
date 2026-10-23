An analytic count of the six-column incidence types
===================================================

The complement encoding developed in the preceding incidence argument
turns the six-column case into a loopless multigraph on six vertices,
with exactly five edges counted with multiplicity and maximum degree at
most four. This note proves that there are exactly 45 isomorphism types
without assuming the output of the finite catalogue. The catalogue is
still needed when explicit representatives and transporters are wanted.

The proof uses the standard orbit-counting formula of Burnside. The
application and the calculations below were developed by the Root agent.
They do not assert a new general counting principle or historical priority.

1. Counting all five-edge multigraphs
------------------------------------

Let V be a set of six vertices, and let E be its fifteen unordered pairs.
A loopless multigraph of total edge multiplicity five is a function
w:E -> {0,1,2,...} with sum w(e)=5. The symmetric group S6 acts by
permuting V and hence E. Its orbits are precisely graph isomorphism types,
including isolated vertices and allowing parallel edges.

For a vertex permutation g, let m_j(g) be the number of cycles of length
j in its action on E. A multiplicity function is fixed by g if and only
if it is constant on each such cycle. A cycle of length j, assigned
multiplicity r, contributes jr to the total edge count. Consequently

  Fix_5(g) = [t^5] product_j (1-t^j)^(-m_j(g)).                 (1)

For completeness, the orbit-counting formula follows by counting pairs
(g,w) with g.w=w. In an orbit O, every w has stabilizer of size
720/|O|, so summing stabilizer sizes over O gives 720. Hence the number
of orbits is (1/720) sum_g Fix_5(g).

The following table lists every cycle type on six vertices. The third
column gives the cycles on the fifteen unordered pairs. Exponents denote
numbers of cycles, not vertex degrees.

=================  ==========  =================  ========
Vertex cycle type  Class size  Pair cycle type     Fix_5
=================  ==========  =================  ========
1^6                         1  1^15                  11628
2 1^4                      15  1^7 2^4                 868
2^2 1^2                    45  1^3 2^6                 144
2^3                        15  1^3 2^6                 144
3 1^3                      40  1^3 3^4                  45
3 2 1                     120  1 2 3^2 6                 7
3^2                        40  3^5                       0
4 1^2                      90  1 2 4^3                   6
4 2                        90  1 2 4^3                   6
5 1                       144  5^3                       3
6                         120  3 6^2                     0
=================  ==========  =================  ========

Here are explicit ways to verify all the table entries. A vertex cycle
of odd length r contributes (r-1)/2 pair cycles of length r internally.
A cycle of even length r contributes r/2-1 cycles of length r and one
cycle of length r/2 consisting of opposite pairs. Between two distinct
vertex cycles of lengths a and b there are gcd(a,b) pair cycles, each
of length lcm(a,b). These rules also cover fixed points. They follow by
following an unordered pair around its vertex cycles; an earlier return
inside one cycle is possible only for opposite vertices. They give the
third column directly, and its weighted cycle lengths sum to fifteen
in every row.

If the vertex cycle type has a_r cycles of length r, its class size is
720 / product_r (r^(a_r) a_r!). Indeed, writing the cycles as ordered
lists overcounts by each cyclic rotation and by permutations of equal
length cycles. This gives the second column, whose entries sum to 720.

Finally, expanding (1-t^j)^(-m) gives coefficient
binomial(m+r-1,r) at t^(jr). The nonzero coefficient calculations in
the fourth column are

* 1^15: binomial(19,5)=11628;
* 1^7 2^4: 462 + 4*84 + 10*7 = 868;
* 1^3 2^6: 21 + 6*10 + 21*3 = 144;
* 1^3 3^4: 21 + 4*6 = 45;
* 1 2 3^2 6: 3 + 2*2 = 7;
* 1 2 4^3: 3 + 3 = 6;
* 5^3: 3.

The two remaining pair cycle types have all lengths divisible by three,
so their degree-five coefficient vanishes. The weighted sum is

  11628 + 15*868 + (45+15)*144 + 40*45
        + 120*7 + (90+90)*6 + 144*3 = 37440.

It follows that all five-edge multigraphs on six vertices have exactly
37440/720 = 52 isomorphism types.

2. Removing the excessive-degree types
--------------------------------------

A vertex of degree at least five in a five-edge loopless multigraph
must have degree exactly five, and every edge is incident with it.
Thus every forbidden graph is a multistar. List the positive edge
multiplicities at its centre; they form a partition of five. Conversely
every partition of five gives such a graph on six vertices, padding with
isolated vertices when necessary. The seven partitions are

  (5), (4,1), (3,2), (3,1,1), (2,2,1), (2,1,1,1), (1,1,1,1,1).

The partition determines the graph up to isomorphism. If two distinct
vertices both have degree five, every edge must join those two vertices,
so the graph is the five-parallel-edge graph. Its two possible centres
both give partition (5), and it is counted once. All other forbidden
graphs have a unique degree-five centre. Thus precisely seven of the
52 types are forbidden, leaving 52-7 = 45 admissible types.

There is also a direct labelled check. For a fixed vertex, its five
incident possible pairs have multiplicities summing to five, giving
binomial(9,5)=126 choices. For two fixed distinct vertices, the two
degree-five conditions hold together only for the five-parallel-edge
graph on their pair. No three vertices can all have degree five.
Inclusion-exclusion therefore gives exactly

  6*binomial(9,5) - binomial(6,2) = 756-15 = 741

forbidden labelled multigraphs, and 11628-741 = 10887 admissible ones.

3. Scope
---------

The result counts bare six-column incidence types. Together with the
six five-column partition types and the independently reviewed parity
argument, it supplies the count of 51 possible unmarked incidence types
on one side of a target. It does not count complete side graphs, ports,
marked lifts or full graphs. The supplied finite catalogue additionally
provides representatives, degree data and carrying permutations; those
are separate computational claims. No graph census, manuscript treatment,
Lean formalization or compression measurement is completed by this note.
