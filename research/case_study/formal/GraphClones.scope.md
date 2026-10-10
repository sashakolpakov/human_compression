# Graph cloning: precise formal scope

`phase268_formal/GraphClones.lean` defines the actual pulled-back adjacency
relation on V×F and proves four path statements. Reachability is
`Relation.ReflTransGen`, so the conclusions supply paths, not an abstract
uninterpreted connectedness predicate.

1. A base path lifts with a fixed fiber coordinate.
2. Any two clones of a vertex with a neighbor are joined by two edges.
3. Base reachability lifts between arbitrary endpoint clones.
4. A connected symmetric relation with a neighbor at every vertex remains
   connected after cloning.

All four proofs are axiom-free under the pinned Lean 4.32.2 dependencies.
The kernel checks the complete proofs of these statements. The compiler
and cached dependency objects remain trusted.

The incidence geometry axioms, identification of every cloned residue,
firmness, chamber transitivity, affine-plane construction and the full
counterexample to the source suggestion are not formalized in this file.
The written review establishes those interfaces separately, and both
finite programs test the actual source relation. A two-clone isolated
vertex is the explicit control for the essential neighbor condition.
