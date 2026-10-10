# Formal scope of the four-family construction

`phase257_formal/FourProjectiveMarks.lean` proves eleven declarations
about the actual matrices in the manuscript. It has no placeholders,
new axioms or native-evaluation declarations. The compiler reports only
`propext`, `Classical.choice` and `Quot.sound`.

Over a commutative ring, it verifies the four squares, the three distant
anticommutations, all determinants, the two adjacent product formulas,
addition and natural powers of lower unipotents, and the criterion for
a lower unipotent to be scalar. Over a field of characteristic different
from two it proves that each mark is nonscalar and that all six pairs
are nonproportional. Over `ZMod p` it proves that the nth power of the
lower unipotent is scalar exactly when p divides n. For nonzero p it
also proves that every lower unipotent is a power with exponent below p.
The latter two ring statements do not need primality; the written
application uses prime p to identify `ZMod p` with the prime field.

The squares and determinants establish the matrix inputs; passing from
invertible matrices to PGL classes remains written. No declaration here
proves the complete four-family theorem, the two-root generation lemma,
the finite subgroup classification, split/nonsplit torus descent,
Dirichlet's theorem or the correspondence with regular maniplexes.
The common centralizer theorem also retains its previously recorded
partial formal scope. These eleven declarations must not be represented
as a full Lean certificate for the conjecture.

The replay verifies Lean 4.32.2 and the pinned dependency revisions,
requires clean tracked dependency sources, and compiles in a fresh output
directory. Cached compiled dependencies remain trusted. A changed
projective-period conclusion, p dividing n+1 rather than n, fails to
compile with the proof. Two separate GAP controls change an actual
matrix and collapse two markers; both must be rejected. These controls
test the checker and do not substitute for independent proof review.
