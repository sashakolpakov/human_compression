# Scope of CoverKernelChains.lean

Six declarations prove algebraic facts about kernels and specified
subgroups of an arbitrary group:

1. Directed unions preserve the word form of the intersection property.
2. Nonempty chains satisfy that directed-union theorem.
3. Every admissible normal kernel has a maximal admissible overgroup.
4. Uniqueness of that maximal kernel makes it greatest.
5. Two coprime powers belonging to a subgroup force the element into it.
6. The corresponding coprime-power hypotheses force the join of two
   subgroups to equal a given containing subgroup.

Admissibility includes normality, containment in a fixed target kernel,
and the actual word intersection condition. Zorn's lemma applies at
arbitrary index. There is no finiteness assumption hidden in those
declarations.

The application to covers additionally uses standard word parabolics,
nontriviality of the distinguished involutions, and the correspondence
with regular polytopes. These identifications are written mathematics.
The file does not formalize the surface, homology, source-family maps,
or the full theorem on infinitely many minimal covers.

The source is identical to the frozen phase211 file and was independently
reviewed in phase218. The fresh public compiler output is recorded in
[the report](../phase221_public_replay/author/CoverKernelChains.log).
All six declarations use only the reported standard axioms. The replay
rejects replacing coprimality by a mere inequality. The toolchain and
cached dependencies remain part of the execution trust boundary.
