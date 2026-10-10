# Scope of SplitLatticeReduction.lean

The generic theorem takes additive homomorphisms f:A→B and p:B→A, between
arbitrary abelian groups, with p(f(a))=a. For every natural modulus m,
f(a) is an m-multiple in B exactly when a is an m-multiple in A. A second
statement applies this to differences, giving the induced injectivity
after reduction. The modulus-zero case is included without restriction.

The module also kernel-checks both products of the literal six-by-six
integer coordinate minor and its stated integer inverse. These are the
matrices in the phase34 even-family lattice certificate. This exact finite
calculation uses decide +kernel, with no native-evaluation axiom.

The hypothesis supplying an additive left inverse is explicit. The source
does not contain the1296-coordinate basis, Schreier enumeration, group
extension, finite cardinality argument or geometric/source adapter.
Those are connected to the generic theorem in the written lattice proof.
Thus this is a component certificate, not a formalization of the whole
hypertope family or of its source-problem status.

The first pinned staged compilation passed with Lean4.32.2. The printed
axioms are propext for modulus_membership and the standard propext,
Classical.choice and Quot.sound for the other two statements. There are
no unproved placeholders or native-evaluation axioms. The saved report
records all nine pinned package revisions and their tracked-file checks.
