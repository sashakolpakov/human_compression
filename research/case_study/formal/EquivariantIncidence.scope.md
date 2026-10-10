# Equivariant incidence reconstruction: formal scope

The unchanged source [EquivariantIncidence.lean](EquivariantIncidence.lean)
is also distributed at the frozen author's path
`phase179_formal/EquivariantIncidence.lean`. The portable runner compiles
that exact source. The [fresh report](EquivariantIncidence.check.json)
records the identical canonical-source hash.

For a group acting on X and Y, `reconstruction` proves that an invariant
relation containing a selected pair is its diagonal orbit when X is
transitive and the entire base neighbourhood is the stabilizer orbit in Y.
`localOrbit_subset` proves the inclusion supplied by invariance and the
base relation. `reconstruction_of_card` derives equality from that inclusion
and equality of finite cardinalities. The theorem does not assume the
group is finite; the cardinality form assumes Y is finite.

All three declarations compiled with Lean 4.32.2 and the pinned
[dependencies](dependency_manifest.json). The first uses `propext`; the
other two use `propext`, `Classical.choice` and `Quot.sound`. No native
evaluation axiom, placeholder or admitted theorem occurs. Compiled
dependency objects remain trusted inputs.

The [written application](../phase179_livingstone_manuscript.md) passes
from left to right actions by inverse coordinates and proves the coset
identification. Neither quotient-set construction nor the named J1 data,
graph families, literal source incidences, GAP computations, or either
complete polytope theorem is formalized by these three declarations.
The [independent review](../phase184_L068_independent_review.md) and
[root admission](../phase189_root_admission.md) preserve those boundaries.
