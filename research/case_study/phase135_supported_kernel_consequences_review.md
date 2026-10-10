# Independent formal review: supported-kernel consequences

10 October 2026. Root admits `SupportedKernelConsequences.lean`, SHA-256
`12f45316150aeaa73b3de38ea1338daa5d23dfa678bebf0f07504fac9adf5083`,
with the exact scope of its frozen author manifest. Root read every
definition and proof, the scope document and the verification/control
programs, and compared the conclusions to frozen U version 2.

## Statement and proof correspondence

The cardinality theorem takes the actual supported-kernel construction
hypotheses and calls the reviewed profile theorem. Its helper coordinate
equivalence has a profile premise, but that premise is discharged in
the final construction theorem. Both directions of the equivalence are
proved. The order identity follows from the projection range, kernel
index and dependent product. Nat.card is zero on infinite types; the
statement's finite specialization is the ordinary group-order formula.
It does not assert infinite cardinal multiplication or a finiteness bound.

Local recognition proves both injectivity and surjectivity of the actual
coordinate homomorphism. The antichain condition removes every possible
other supported kernel coordinate. No order equality is substituted for
an injection argument. This specializes exactly to U.SK.Local.

Separator factorization lifts a base product and splits the residual
kernel by supports. The proof shows that a^(-1)n_M a remains in the M
parabolic, using normality of each local quotient kernel and the exact
profile. It neither assumes that the whole M parabolic is normal nor
commutes elements within a nonabelian kernel. It proves U.SK.Separator
and its all-parabolic version.

For the lower-central statement, local kernel elements lift into the
required lower-central subgroup. The same support induction as the
construction removes unwanted smaller coordinates inside that subgroup.
Functoriality and the vanishing base term prove the converse inclusion.
The profile, pure-kernel membership and final equality are conclusions,
not assumptions. Mathlib index n is conventional gamma_(n+1), so the
written U.SK.Central uses n=c-1. The written local equality implies the
formal theorem's weaker local inclusion hypothesis.

The formal parameterization uses a quotient E_j→B and a base endomorphism
p_j. A written quotient E_S→B_S is composed with B_S→B, and the specified
base deletion supplies p_j. Supports are finite and distinct, local
markers vanish outside them, each local marking generates, and every
proper local parabolic has trivial quotient kernel. These are substantive
application obligations; no certificate removes them.

## Fresh checks and trust

The dedicated pinned runner compiled all four local modules and two
specified Mathlib modules in a new isolated output directory. All seven
new and sixteen retained printed declarations report only propext,
Classical.choice and Quot.sound; no placeholder, warning or native
evaluation axiom was accepted. The fresh compilation took approximately
21.2 seconds. Eight rejection controls also passed, preserving altered
test inputs and occupied output paths as specified.

The compiler and all other cached package objects remain trusted. Package
revisions and tracked cleanliness were checked. The private Mathlib
overlay excludes every target module stem before compilation, protecting
the installed cache. The author source, checkpoints and older construction
certificate are preserved unchanged. A fresh public generic-runner result
is recorded separately on publication.

This certifies the U.SK order formula, local recognition, separator
factorization and lower-central consequence. Boolean deletions, typed
Helly, complete geometry recognition and source applications are not
proved by this particular module. Their separate certificates or written
arguments must not be folded into its scope. No source-compression ratio,
historical-priority clearance or new conjecture solution is claimed.
