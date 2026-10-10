# Formal scope and controls

The three declarations in `phase258_formal/StringCentralizerBridge.lean`
prove the actual abstract interface used in the application. Commutation
with each generator implies commutation with the whole group. In a
centre-free string-generated group, the first adjacent markers cannot
commute. If each noncommuting involution pair has at most one nonidentity
common centralizer element, an injective marking has rank at most four.
The theorem quantifies over every rank, with no finiteness, simplicity,
projective-group or intersection-property hypothesis.

The common-centralizer condition is an explicit hypothesis. Its matrix
proof and passage to PGL are not hidden axioms: they are the written
umbrella dependency. Frozen237 proves the actual normal-form matrix
calculations, but its algebraic-closure conjugacy, basis-change and
projective descent remain written. The reused file
`formal/InvolutionCentralizers.lean` proves the general characteristic-two
and Suzuki-style rank-three obstruction from its stated abstract
centralizer condition; its two declarations are replayed separately and
are not counted as new theorems.

The new formal proof uses only standard Lean axioms. The driver compiles
two deliberately false weakenings and requires both to fail: removing
the string commutation condition, and allowing identity markers. The
first fails mathematically in A5 with five distinct involutory generators,
although the common-centralizer and centre-free conditions hold. The
second fails by adjoining an identity fifth marker to the literal rank-four
PSL13 example; all other marking conditions in the theorem hold. The
finite checker verifies the corresponding countermodels.

Lean does not certify the complete classification, Dickson's theorem,
torus normalizers, Dirichlet's theorem, exact finite universal orders,
source matrix conjugacy or the whole infinite-family constructions.
Those remain written or exact GAP computations. The pinned source
checkout, cached dependency objects and compiler are trusted inputs.
