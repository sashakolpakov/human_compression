# Independent review of the marked parity-mix formal proof

**PASS. No mathematical, formal-statement or executable correction is required.**
This review admits the precise general group construction stated below, not the
whole finite-field application or a complete answer to the equal-label conjecture.

The exact author freeze is `phase146_parity_mix_manifest.json`, SHA-256
`ed486ab555336588356b93622fa1cb769d7fbc8a09543dab53c9f99ba10410e0`.
The principal source `formal/ParityMixTheorem.lean` has SHA-256
`9927c96f935d5b1739f7d21a7685117d18f8217399e7ac06921388d46abd86ed`.
All twenty author artifact bindings and twelve retained-input bindings were
checked before and after review. Frozen sources and the public tree were not
edited. Historical author-pending or mutable-development comments in frozen
source files are documentary labels, not further hypotheses of the theorem.

## Exact admitted statement

Let `e : Fin n → E` and `g : Fin n → G` be markings of groups, and let `A` be a
commutative group. Assume:

- every element of `E` has order dividing some power of two (`IsPGroup 2 E`);
- every input marker squares to one;
- actual homomorphisms `ε : E →* A` and `δ : G →* A` send every marker to the same
  specified `t ≠ 1`;
- each consecutive product in the `G` marking has finite odd order;
- both markings have string commutation and the full intersection property.

Then the **literal generated subgroups** of `E × G` on paired markers satisfy

\[
 \langle(e_i,g_i):i\in S\rangle\cap
 \langle(e_i,g_i):i\in T\rangle
 =\langle(e_i,g_i):i\in S\cap T\rangle
\]

for all finite supports. The same equality is proved inside the actual generated
mix, using its injective subtype map. Its intrinsic paired markers generate that
group, are nonidentity involutions, and satisfy the string relations. These are
actual group-theoretic conclusions, not properties of an assumed abstract mix.

There is no hidden finiteness or ambient-generation hypothesis in the final
intersection statements. The two-primary predicate is pointwise: its exponent
may depend on the element. Oddness of `orderOf` excludes infinite-order adjacent
products, since their Mathlib order is zero. Nonidentity of the markers follows
from the genuine character, rather than from their squares alone. The formal
types allow `n = 0`, empty supports and empty component types. At rank zero the
marker assertions are correctly vacuous. The final theorem does not assume a
mixed intersection property, common-quotient classification, component profile,
row/column character identity or interval-forest claim.

## Proof and consumer-interface review

I read every line of all twelve new Lean files, the complete scope document, the
dependency map, checkpoint, compiler wrapper and control program. I reread §1 of
the exact retained `phase124_even_label_mix.md` and the definitions and interfaces
actually imported from the retained files. The mathematical arguments and their
formal use agree as follows.

| Proof portion | Checked mathematical content |
|---|---|
| `ParityMix` | Taking a two-power kills the first coordinate; a coprime power recovers an odd-order second coordinate. Products along actual paths telescope. Closure induction gives a companion equal to one or a fixed involution. Character compatibility isolates the character kernel, and surjective first projection then proves the whole connected fiber. |
| `ParityMixLocal`, `ParityMixFiniteProfile` | The local markers generate the actual parabolics by definition. The first local group inherits the two-primary property. Order is preserved under subtype inclusion; reversed adjacent products have the same odd order. Genuine interval paths discharge connectivity. The empty-support case is separate and correct. |
| `ParitySupportIntervals` | Components are the actual finite order-connected components. Their coverage, nonemptiness, disjointness, interval paths and separation are proved, rather than supplied as graph assumptions. Distinct canonical components really have a missing marker between them. |
| `ParityMixComponents`, `ParityMixProfile` | String relations extend from markers to commuting subgroups. Factor IP gives each component trivial intersection with the subgroup on **all other components**, sufficient for product injectivity. Pairwise trivial intersection alone is not substituted. The mixed assembly is onto by generation; the two factor assemblies are injective, giving the exact mixed component profile without using mixed IP. |
| `ParityComponentCoordinates`, `ParityMixCoordinateProfile` | Coordinates are homomorphisms obtained by inverting proved assembly equivalences. A tuple supported on one component has its actual group value there and identity elsewhere. The refinement character product is proved by the restrictions of a homomorphism to the direct-product factors. The codomain's commutativity is used explicitly; the factor groups may remain noncommutative. |
| `ParityOverlapGrid`, `ParityRefinementCharacters` | All pairwise intersections of the two support-component families cover the support intersection, are intervals and are disjoint. Empty intersections are allowed. Actual membership in each original mixed subgroup yields the corresponding coarse character equalities, and refinement derives both the row and column equations. |
| `ParityMixIntersections`, `ParityMixTheorem` | Projection plus the two input IP statements places both coordinates on the support intersection. The actual fine coordinates define additive character defects. Empty overlaps give zero defects; the proved interval theorem kills all remaining defects. Exact interval fibers and mixed assembly then prove membership in the intersection parabolic. Monotonicity supplies the reverse containment, and the subtype transport gives intrinsic IP. |

The key retained invocation is `fin_weights_eq_zero`. Its actual arguments are the
two canonical interval families, their proved disjointness and order-connectedness,
the genuine character defects, the derived row/column equations, and the proved
zero values on empty overlaps. None is silently inferred from the desired mixed
intersection conclusion. The theorem does not require the fine overlaps to be
pre-labelled canonical components; their proved interval structure, coverage and
disjointness suffice.

I also reread the exact interval sources. Their hereditary leaf argument chooses
a nonzero edge with least incident right endpoint; all its nonzero neighbors must
contain that endpoint. Opposite-family disjointness leaves one neighbor, so its
row or column sum forces the edge to vanish. It uses neither an assumed forest nor
additive cancellation. The `Fin n` adapter proves that `Fin.val` preserves the
needed convexity and disjointness, including empty cases. **I authored these two
retained interval files in phases149 and154.** Their own mathematical review was
performed by root in phase155. My independent role here concerns the newly
authored group proof, its actual consumer bindings and the complete final scope;
it is not presented as independent authorship of every retained proof leg.

The connected-fiber Lean proof uses direct coprime isolation instead of the
written finite Goursat argument. This is a valid proof of the same construction,
under the weaker pointwise two-primary condition in place of a finite two-group
premise.
The canonical profile and intersection stages follow the written component and
overlap proof. The result therefore formalizes the central group-theoretic claim
of the written §1, rather than only a conditional helper whose desired conclusion
has been assumed. It does not formalize every conclusion or application in that
note.

## Fresh verification and portable execution

The exact compiler was Lean 4.32.2, release commit
`f3b06c705e6c85f5314019d5d3baab0fec5b580c`. The pinned Mathlib revision is
`905b95818eb32af7874a58b427f50c1711a5e96c`. All nine package revisions and tracked
cleanliness checks passed. I freshly compiled all eighteen local sources in a new
directory: **PASS, 45.105185791 seconds** of recorded compiler time.

All **75 requested axiom reports** were present: fifty from the twelve new modules
and twenty-five from six retained modules. Seventy-one report exactly
`Classical.choice`, `Quot.sound`, and `propext`; four report only `Quot.sound` and
`propext`. The latter are `interval_forward_path`, `interval_path`,
`overlapScope_ordConnected`, and `character_defect_sum`. There were no compiler
warnings, errors, `sorryAx`, `native_decide` dependencies or new axioms. The fresh
report preserves every declaration's actual axiom list and every source/object/log
hash; a module count is not a count of new mathematical discoveries.

My separate `phase157_parity_mix_interface_checks.py` copied only the declared
twenty-one replay files into an isolated public-style tree: the two wrappers,
eighteen Lean sources and dependency manifest. No source PDFs, manuscript,
registry, historical source bank or methodology document was present there. I
deliberately supplied a nonexistent inherited `LEAN_PATH`; the exact wrapper
correctly replaced it with the fresh output and pinned package libraries. This
second full compile passed in **53.264771790 seconds**, again with all seventy-five
reports.

The independent interface suite passed **twelve cases**: that isolated positive
compile; mutations of the final theorem, retained finite-interval adapter and
dependency manifest; and four occupied path forms for each of the two wrappers.
The occupied forms were a regular file, directory with nested contents, live
symlink and dangling symlink. Full snapshots establish preservation, every
mutation was restored, and rejected source mutations created no proposed output.
This suite uses explicit checks under optimized Python; it does not import author
control helpers. A fresh replay of the author's separate **23 rejection controls**
also passed. These controls verify executable integrity and refusal behavior;
they are not substitutes for Lean's proof checking.

The wrapper verifies exact source and dependency-manifest hashes before creating
output, compiles in dependency order into a new directory, validates the complete
expected axiom-name sets, and rechecks source hashes afterward. The outer frozen
manifest binds the wrapper and its prose evidence; it was independently checked.
The pinned compiled package cache and installed compiler remain trusted. This is
not a from-source rebuild of all Mathlib or a proof that the compiler implementation
is correct. No network access or private study material is needed for the declared
formal replay.

## Scope, attribution and charged costs

The certificate stops before the finite parabolic cardinality formula
`|H_S| = |E_S| |G_S| / 2^c(S)` and before exact adjacent least-common-multiple
orders. The profile needed for those deductions is formalized; the numerical
deductions themselves are not advertised as Lean theorems here.

Concrete finite-field groups and allowed parameters, their BFL generation and IP,
the existence and marker values of a Dickson or matrix parity homomorphism, and
the group-to-polytope correspondence remain explicit application inputs. This
package neither proves the full equal-label conjecture nor establishes historical
novelty, current openness, a new source-level compression ratio or another whole
paper replacement. The classical coprime-power/subdirect-product reasoning,
commuting subgroup decomposition and Mathlib order-component machinery are
retained and attributed; compiler success is not a priority determination.

I independently checked all recorded local import lists, source hashes, sizes and
plain NFC whitespace counts. The twelve new formal bodies contain **59,591 UTF-8
bytes / 10,567 tokens**. The six retained local files cost **37,019 bytes / 6,739
tokens**, yielding **96,610 bytes / 17,306 tokens** in the full local formal closure.
The directly used old interfaces are the fiber-product definition, the marked
subgroup definition and monotonicity/map lemmas, and interval cancellation. The
larger imported proof files are nevertheless charged and recompiled in full. The
new proof invokes neither the old coprime-kernel theorem nor the supported-kernel
construction theorem. Standard-library transitive costs are not measured here.

There is no matched alternative formal proof and no previously frozen version of
these twelve new bodies. Accordingly measured duplicate removal, payback and a
sawtooth saving trend remain unknown. The reported body acquisition is a cost,
not evidence of such a saving. The package's methodological GKM attribution is
separate from the mathematical hypotheses and was not used as proof evidence.
