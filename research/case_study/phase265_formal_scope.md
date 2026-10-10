# Determinant-fiber formal scope

`phase265_formal/DeterminantFibers.lean` has four declarations, over arbitrary
fields and finite square matrix index sets where applicable:

- `determinant_fiber_torsor`: if A is invertible and detA=detB, there is a
  unique C with detC=1 and AC=B. Invertibility is the explicit `IsUnit A.det`
  hypothesis, and the proof constructs A⁻¹B.
- `semilinear_determinant`: the actual entrywise field-automorphism map
  followed by multiplication has determinant σ(detA)detM.
- `semilinear_fiber_transport`: after that actual semilinear matrix move,
  determinant-one right multiplication reaches exactly its determinant
  fiber, under the explicit nonzero-determinant hypothesis.
- `orbit_saturation`: when a specified subgroup acts transitively on every
  fiber of a map, its orbit relation is detected by the image of an orbit
  under that map. The fiber-transitivity hypothesis is not omitted.

There are no custom axioms, proof holes or native decision axioms. The
compiler reports only the standard axioms propext, Classical.choice and
Quot.sound (the last declaration uses only propext). The source proof is
freshly compiled. Existing cached Mathlib objects and the kernel/compiler
are part of the trust boundary, with exact dependency commits checked.

These declarations substantiate the actual determinant interface in the
common paper. The affine group adapter, contained-SL hypothesis, finite-field
classification and all incidence-geometric consequences are still written
mathematics. In particular the F9 counterexample, the reconstruction theorem,
the unital residue and the full source classification are not falsely labeled
as Lean-certified theorems. The runner deliberately changes the determinant
conclusion from1 to0 and confirms rejection; finite controls independently
show why deleting the contained-SL hypothesis invalidates the orbit criterion.
