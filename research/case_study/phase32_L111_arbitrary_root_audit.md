# Root review of the arbitrary-rank extension

10 October 2026. **PASS for complete Theorem 4.1**, read with the source's
flag and chamber quantifiers. This extends the separate finite-rank review;
it does not turn the available indexed passages into complete-paper access.

Root independently read the primary indexed definition on page 586. Flags
are arbitrary pairwise incident sets; their ranks are cardinalities, and
every flag lies in a chamber. The proof's use of potentially infinite flags
of cotype {0,1} therefore matches the source. Connectivity always uses finite
paths, as required in both directions of the argument.

The finite note's chamber map, three residue isomorphisms, component argument
at remaining rank at least three and bipartite-double criterion at rank two
do not use finite rank. The automorphism action, rank-two classes and
disjoint-pair incidence checks likewise remain valid. This correctly
extends the residual-connectivity part without invoking the finite-rank
gallery induction.

For strong connectivity, the new proof works directly with two-type
truncations. In the forward direction, the new 01 truncation is the double
of a connected graph containing an odd cycle from a completed higher flag;
the other pairs are unchanged or copied old 0j truncations. In the reverse
direction the only missing old pair is 1j. Edges sharing a vertex are joined
inside its residue, whose strong connectivity follows from the copied-vertex
isomorphism. A finite edge path in the connected old graph then joins any
two edges, and chamber extension joins every j-object to an edge.

Applying that argument to every higher-flag residue handles infinite flags
as well. Old residues with an edge but no vertex require a separate case:
endpoint-higher truncations are complete bipartite, and higher-higher
truncations are unchanged by adjoining an endpoint. All types and residues
are covered. Passing from pair truncations to arbitrary truncations uses
chamber extension to join every additional object to one fixed retained
type; no finite-rank assumption enters.

Finally, the alternative A1/A2/A3 hypotheses imply G/E as claimed. Complete
an edge to a chamber. Endpoint containment puts every global endpoint into
that chamber's graph residue, which gives exactly two endpoints. A second
edge with those endpoints meets every higher object by A2, so simplicity in
the same graph residue identifies the edges. This supplies the required
direction of the source's hypothesis conversion without retaining its lemma
as an unproved input.

The resulting coverage is one complete numbered construction theorem,
including arbitrary rank and both input formulations. The existing general
cover theorem is used only in its stated finite-rank scope; the arbitrary-
rank result has its own path proof. No additional finite test can certify
that infinite-rank argument. Section 6 and the application tables remain
outside this review, as do any whole-paper or numerical ratio claims.
