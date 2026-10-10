# Scope of CompactAffineData.lean

The four explicit affine maps in six integer coordinates are written as
homogeneous7x7 integer matrices. Four theorem blocks are kernel-checked:

- Each mark squares to identity.
- The nine fixed source rotational words evaluate to identity.
- T² and its specified conjugate are translations-2e1 and-2e2.
- The six exact Schreier basis words translate by2e1,...,2e6.

Every finite identity uses decide +kernel. All printed axiom sets are the
standard propext, Classical.choice and Quot.sound, with no native-evaluation
axiom or unproved placeholder. The first staged pinned Lean4.32.2 run passed.
An independent reader compared all homogeneous marks, source words and
the six basis words against the standalone affine certificate; all matched.

This module does not enumerate the linear quotient, prove its reduction
faithful, span the entire Schreier kernel, count coset flags, or identify
source toroidal residues. It does not construct the presented-group map
or the hypertope inside Lean. Those connections remain in the separately
reviewed computation and written proof. The old/new affine intertwiner
and current-literature status are also outside this formal certificate.
