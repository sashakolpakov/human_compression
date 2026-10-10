# Independent review of the supported-kernel construction

Root review, 10 October 2026. The frozen phase129 structural theorem is
accepted at the scope below. Its author manifest has SHA-256
`6e525afd12d6c4cfe6942122d3d1618c6f73f6c1b74eab2835d77f5449f677fa`.
The new Lean source has SHA-256
`1fb99082407826a390e975432c5f12d1e665ac66af9d18fbb75532af5a57f10a`.

## Statement and written-proof correspondence

Root read the complete new Lean source, both reused local sources, the
dedicated compiler wrapper, its rejection controls and the complete U.SK
statement and proof in the bound U v2 manuscript. This is an independent
agent review, not external peer review.

The actual tuple generators are arguments of the formal theorem. Their
coordinates outside each support are one; their quotient images agree
with the corresponding deleted base coordinates. The base deletion fixes
the retained base generators. Each local marking generates its entire
local group, and its quotient has trivial kernel on every proper marked
parabolic. The supports are distinct. Base generation and base IP are
explicit assumptions.

These hypotheses follow from the written U.SK data. Regard each local
map into B_S as a map into B by inclusion, and do the same for each
deletion. Inclusion changes neither its kernel nor the marker equations.
For groups, injectivity on a subgroup implies the kernel-trivial condition
used in Lean. Finite subsets encode every subset of the finite marker set.
The type-class decidable equality assumptions add no mathematical
restriction in the classical setting used here.

The final `supported_kernel_construction` proves all of the following:

1. The tuple generators generate the full simultaneous fiber product.
2. For every label subset L, its generated subgroup contains a pure kernel
   tuple exactly when each coordinate belongs to its local kernel and
   every coordinate whose support is not contained in L is one.
3. Every pair of generated parabolics meets in the parabolic on the
   intersection of their label sets.

Neither global generation nor the kernel profile is an input. The pure
kernel induction obtains a local word from local generation, proves its
base is one using fixation, and kills coordinates outside the support
using proper-parabolic injectivity. Strict support inclusion reduces
cardinality, because supports are distinct. The finite product assembly
and the correction `y * z⁻¹` are valid for nonabelian factors: no factors
inside one coordinate are permuted. The resulting profile is supplied
to the retained image/kernel intersection theorem.

The identity describing the image of each parabolic is proved by
`marked_map`; the base projection and kernel equivalence have not been
packaged here as named equivalences. The finite order formula and the four
separately numbered U.SK corollaries are not part of this admission.
In particular, IP alone does not certify a hypertope, and the final theorem
does not assert involutory generators, typed coset Helly or any polytope
correspondence. Applications must discharge the actual local assumptions.

## Fresh execution and hypothesis challenges

The pinned author wrapper was read and then executed independently in a
fresh output directory. It rebuilt all three local Lean modules, producing
ten new substantive axiom reports and six retained reports. The compiler
was Lean 4.32.2; all nine package revisions and tracked-file cleanliness
matched the recorded dependencies. Compilation took about 10.8 seconds.
There were no errors, warnings, placeholders or native-evaluation axioms.
The reported axioms are drawn only from `propext`, `Classical.choice`
and `Quot.sound`.

All seven changed-input and occupied-output controls passed in a separate
fresh run. Those controls exercise the wrapper; they are not a substitute
for reading the Lean statement or checking its proof.

A separately written finite checker enumerates the actual generated
subgroups, all parabolics and simultaneous fibers in seven elementary
examples. One satisfies every hypothesis. Six omit exactly one of the
recorded hypotheses and make a claimed conclusion fail: distinct supports,
proper-parabolic injectivity, base fixation, trivial outside markers,
base IP, or local generation. In the first four cases the obstruction is
an actual diagonal subgroup in a product of two groups of order two.
The base-IP example has no local factors and equal nontrivial base
generators; their singleton parabolics meet nontrivially. These checks
confirm meaningful boundaries but prove no general theorem.

## Attribution and admission boundary

This certificate formalizes the support-induction argument already written
in U. It reuses `coordinate_kernel_meet` and
`intersection_of_image_and_kernel` with their original attribution; it
does not assume the older `hcoords` interface as a substitute for proving
the new kernel profile. Existing Mathlib results and the standard logical
axioms remain retained inputs. Historical priority is not established.

The installed compiler and compiled external dependency objects remain
trusted. The local proof sources were freshly compiled; the entire Mathlib
dependency tree was not rebuilt. The separate public reproduction record
binds the admitted source, reports and exact export bytes. This adds one
scoped Lean component, no newly covered source paper, no complete
conjecture solution and no compression ratio.
