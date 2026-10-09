# Review and dependency boundary: dihedral classification

Date: 2026-10-10.

The proof is [phase5_dihedral_classification.md](phase5_dihedral_classification.md);
its exact finite-set audit is [phase5_dihedral_check.py](phase5_dihedral_check.py),
with report [phase5_dihedral_check.json](phase5_dihedral_check.json).
Run it using Python 3 and its standard library:

    python3 phase5_dihedral_check.py

It writes its report next to the script; pass --output with a scratch path to
preserve a historical report.

This is a rederivation of a published subject, not a new resolution of an open
problem. The full L109 paper has not been read: its author abstract and empty
institutional holdings were inspected. The source statement that can be compared
exactly includes L114 Theorem 5.1, which reproduces the L109 rank-two
classification, and L110 Theorem 4, printed pp.9–10, which cites L109 as [20]
and reproduces the full all-rank three-family classification and binomial
class count. The §2 subgroup definitions of RWPRI are used without adding
the locally two-transitive axiom.

## Mathematical inputs

The all-parameter proof uses only the subgroup structure of cyclic and dihedral
groups, maximal-subgroup primitivity of a coset action, the Chinese remainder
theorem, and elementary automorphisms of a dihedral group. It does not take
firmness, flag transitivity, residual connectivity, the intersection property,
or a precomputed geometry classification as an input. These are deduced.

The reusable step is the induction upgrading existential weak primitivity to
every parabolic cover being maximal in a subgroup-closed rank-two-rigid class.
The group-specific rigidity proof is supplied in full. It must not be applied
to other finite groups without verifying the rank-two hypothesis.

The count is for group–coset-system pairs modulo group automorphisms and type
permutations. Faithfulness is not required. Forgetting the specified action
can identify different counted systems; the four-cycle example explains this.
The exceptional automorphism group of the Klein four group is treated separately.

## Reviews actually performed

1. **Deriving agent (recent_conjectures):** checked cyclic and dihedral
   rank-two rigidity, all three irredundancy patterns, the left-coset congruence
   convention, CRT typed Helly, residue structure, automorphism orbit counts,
   the $n=2$ exception, and the optional locally two-transitive consequences.
2. **Independent internal agent (root):** read the complete proof and
   reported no mathematical gap in the maximality induction, cyclic/dihedral
   rigidity, irredundancy classification, CRT Helly, counts, and local-action
   boundary cases. Requested markup repairs were applied. Subsequent changes
   clarified that a cyclic intersection is contained in the rotation subgroup,
   made the nonempty index-set convention explicit, and stated the degree-two
   panel-action kernel correctly.

These are internal mathematical reviews, not external peer review.
No novelty determination is needed for the principal classification:
the 2000 primary abstract already announces it. An exact comparison against
all printed L109 theorem numbers remains unavailable.

The deriving agent subsequently read L110 Theorem 4 and compared each of its
three subgroup diagrams and its complete rank-dependent count with Theorem A
and Corollary A.1. They agree: the source's first, second, and third families
are respectively the rotation-factor, single-prime-factor, and polygon-factor
families. This independently rederives the entire published all-rank theorem
as reproduced in a primary source. It does not justify claiming every
principal result in the unavailable original twelve-page article was assessed.
The checker and historical computation report were unchanged by this source
comparison, so no further run was needed.

## Executable coverage

The checker independently generates all subgroups by adjoining elements in the
explicit multiplication table. It enumerates all irredundant families of proper
subgroups, including candidates with nonmaximal subgroups. Pruning is complete:
comparability makes a family redundant, and adding further intersections cannot
repair redundancy. It then tests the source RWPRI condition against exact
maximal-subgroup inclusions.

For every accepted family it checks the stronger all-covers-maximal property,
and it compares the accepted set with the three predicted arithmetic patterns.
Actual automorphisms and type permutations supply the orbit counts. For one
representative of every orbit it checks all typed flags for common coset
intersection, every panel for firmness, every residue of rank at least two
for connectedness, and every rank-two residue for the geometric intersection
condition.

The run passed for $n=2,\ldots,16,18,24,30$ (18 groups). No finite computation
is asserted to establish the all-$n$ result. There is no Lean formalization
of this particular classification.

## Measurement document review

The deriving agent also reviewed the public MEASUREMENT.md as requested.
No substantive metric or novelty overclaim was found in the inspected version:
source/replacement theorem sets must match; retained dependencies are charged
or declared conditional; no numerical corpus ratio and no infinity marker are
currently assigned. The infinity marker is explicitly a qualitative reporting
convention, not a mathematical description-length ratio. Internal verification
and external priority/review are kept separate.
