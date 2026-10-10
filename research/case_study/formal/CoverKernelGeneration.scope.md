# Scope of CoverKernelGeneration.lean

Five declarations prove:

1. Two inverse permutations supported on disjoint coordinate sets are identities when the coordinate functions separate points.
2. Injectivity of a homomorphism on the entire union of proper designated subgroups preserves the word intersection property, given the original intersection identities.
3. Normal generation and two consecutive powers in admissible kernels make the join of all admissible kernels equal the target normal subgroup.
4. Under those hypotheses, a unique maximal admissible kernel equals the target.
5. The target quotient then satisfies the word intersection property.

The file imports the actual `Admissible` and `IntersectionProperty` definitions from [CoverKernelChains.lean](CoverKernelChains.lean). In particular, admissibility includes normality, containment in the target, and an intersection witness. The final deductions explicitly assume normal generation and the supply of consecutive powers. These hypotheses are established by the separate written proofs, not by the Lean file.

The cube-complex construction, retained geometric theorems, graph comparison, projection bounds, interval extension, and complete group–polytope correspondence are not formalized here. No new axiom represents them.

The source agrees byte for byte with the frozen author file. The [compiler record](CoverKernelGeneration.check.json) and [fresh public log](../phase223_public_replay/author/CoverKernelGeneration.log) report all five declarations with standard axioms only. The replay also compiles the six retained dependency declarations and rejects three hypothesis weakenings. The compiler and cached dependency objects remain part of the execution trust boundary.
