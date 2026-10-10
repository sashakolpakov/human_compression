# Graph incidences and stabilizer orbits

This reviewed application connects faces defined by a graph to the marked
geometries studied in [Module C](MODULE_C.md). Read the [six-page manuscript](research/case_study/phase179_livingstone.pdf),
its [Markdown source](research/case_study/phase179_livingstone_manuscript.md),
and the [independent mathematical review](research/case_study/phase184_L068_independent_review.md).

The source is Hartley, Hubard and Leemans, *Regular 4-polytopes from the
Livingstone graph of Janko's first group* (2012), pp. 193–214,
[DOI 10.1007/s10801-011-0300-x](https://doi.org/10.1007/s10801-011-0300-x),
registry L068. The two intended constructions and their geometric
ingredients remain attributed to that paper and its cited predecessors.

    U + Module C + complete reconstruction of the neighbourhoods in the source
      -> literal P of type {5,6,5}, with its stabilizer lattice;
      -> explicitly corrected Q of type {5,3,5}, with its stabilizer lattice.

The reusable argument is elementary. In a transitive group action, an
invariant relation is determined by the complete neighbourhood of one
base object. If that neighbourhood equals the appropriate stabilizer
orbit, the relation is precisely coset incidence. This identifies every
flag and residue, so Module C supplies the remaining recognition theorem.
The [Lean component](research/case_study/formal/EquivariantIncidence.lean)
proves the diagonal-orbit implication and its finite-cardinality version.

The finite application reconstructs the graph's complete pentagon,
Petersen-subgraph, quadruple and local-design families. It checks all
twelve binary source relations against full stabilizer orbits. All six
relations defining P agree. The printed type-2/type-3 relation defining Q
has twelve neighbours where two are intended; ten of those flags of two objects
have no extension by an object of type 1. The manuscript gives an exact counterexample
and adds the induced-quadruple condition already motivated by the source's
Proposition 3.5. The repaired structure has the claimed polytope type and
full type-preserving automorphism group. A separate auxiliary correction
distinguishes a 40-vertex common distance-two set from its intended
10-vertex white-pentagon subset.

The [list of source results and proofs](research/case_study/phase179_source_ledger.json)
matches 17 source records to 24 passages of the proof. One main construction
is recovered as printed; the other is corrected. This counts as
**part of one source paper recovered**, with no addition to the count of
papers whose stated main results are all recovered. No open conjecture
is answered, and historical priority of the correction is unverified.

The required local proofs and programs occupy 44,524 UTF-8 bytes.
Including all the U and C text used, and the required C program, adds 135,006,
for **179,530 bytes**. The six exposition pages exclude those dependencies
and programs. There is **no matched compression ratio** for these results;
the original paper's 22 pages do not establish a 22/6 factor.

The [public check](research/case_study/phase189_root_admission.md)
reruns the earlier marking certificate, graph calculation and Lean
compilation. The independent check examines every relation as printed
and all twelve disputed neighbours. Three author-designed and
two reviewer-designed changes are rejected. Named J1 data, exact GAP
algorithms, classical graph identification and the stated results of U and C remain
inputs. Lean covers the generic implication, not the complete finite
application. See [reproduction instructions](REPRODUCING.md).
