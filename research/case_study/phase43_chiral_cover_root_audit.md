# Root review: kernel transport for chiral regular covers

10 October 2026. **PASS for the stated conditional author-version contract.**
The complete `phase41_chiral_cover_manuscript.md` derives the proved conclusions
in Gabe Cunningham's *Chiral polytopes whose smallest regular cover is a
polytope*, from the common kernel theorem, explicit local arguments, retained
geometric background and the charged exact finite calculation. The source
conjectures remain unresolved. This is an additional standalone source adapter;
it is not yet integrated into the reviewed seven-source manuscript, and no
length saving has been measured for it.

## Source and reading scope

The target is the eight-page author manuscript headed 25 July 2023 at the
[author's primary site](https://gabrielcunningham.com/WhichChiralPolytopes.pdf).
The published citation is JCTA Series A 204 (2024), 105839,
[DOI 10.1016/j.jcta.2023.105839](https://doi.org/10.1016/j.jcta.2023.105839).
The full publisher PDF was not acquired. The root read the complete bound
primary text and independently opened the author PDF through the web tool,
including the literal presentations in its final section. This is a text
reading, not a local PDF-byte or full visual-page verification. Mirror bars
lost in extraction and the source's nonidentity-power wording are handled
explicitly. The publisher's recorded earlier Corollary 3.3 error does not
justify claiming verification of unacquired version-of-record wording.

The root read the complete replacement, its source ledger and GAP certificate,
and the existing Lean kernel theorem. For the older atomic families, the root
read the bound Proposition 4.2 and Table 4 excerpts from Cunningham–Pellicer
arXiv:2009.04566v1. This is not a review of that entire 43-page classification.
Its existence, atomicity and prime chirality conclusions remain retained inputs.

## Proof review

The common statement K is correct for arbitrary group homomorphisms: once
the image intersection equals the image of C, the residual obstruction is
exactly the intersection with the kernel. No surjectivity or finiteness
assumption is required. Its forward transport implication matches the existing
Lean theorem `LeemansLift.intersection_of_image_and_kernel`; the converse is
immediate and written out. No new formal module is claimed.

For a marked rotation group U/N, the mirror mix has kernel N∩μ(N).
The manuscript proves its universal regular-cover property and identifies
chirality as the first-coordinate kernel. It also checks the often suppressed
local mirror convention: on the vertex subgroup, conjugating the second
coordinate by the first generator's inverse aligns the intrinsic mirror
without changing the embedded first-coordinate kernel. Thus local chirality
groups are compared inside the same ambient group, not by their abstract types.

The regular-end lemma uses rank induction and K to establish local
polytopality. The retained depth-two regular-section theorem then supplies
the prerequisites in the general case. The main cover criterion is one K
application, and the stated corollaries follow with the medial embeddings
explicit. The square-torus example has a full affine proof: linear part in
C4 kills chirality and is injective on the relevant distinguished cyclic
subgroup. Its standard square-tessellation identification remains background.

The five all-parameter atomic-family examples use the retained prime-order
global chirality theorem correctly: nontrivial local chirality subgroups
coincide with that embedded prime group. They are not inferred from a finite
sample. The older classification is neither rederived nor included as an
additional compressed source.

## Exact finite certificate and minimality

The root independently replayed the literal GAP script in a new private
directory. Its output is byte-identical to the author's bound log, with no
stderr and exit zero. The new no-clobber runner provides a reproducible public
entry point; it checks both the script hash and the complete expected output
after the same universal-newline conversion used by the historical runner.
An initial byte-only comparison correctly detected GAP's leading carriage
return; the final runner preserves raw bytes and records the explicit newline
conversion rather than silently trimming or ignoring output differences.
The historical in-place Python runner is not used or exported.

| Rotation group | Order | Facet / vertex orders | End intersection |
|---|---:|---:|---:|
| P | 324 | 54 / 54 | 9 |
| T | 324 | 162 / 18 | 9 |
| T dual | 324 | 18 / 162 | 9 |
| R = P mixed with its mirror | 972 | 162 / 162 | 27 |
| Q | 2916 | 162 / 162 | 9 |
| Q′ | 2916 | 162 / 162 | 9 |

The medial subgroup has order nine in every row. The certificate proves
actual subgroup equalities, local cyclic intersections, exact generator orders
and mirror maps; it does not rely only on matching numerical orders. P is
chiral, R is regular but fails the intersection condition, and Q,Q′ are regular
polytopes. All required marked maps are surjective with kernel order three.
The facet identification and explicit dual map are checked. The root compared
all three bare presentations with the primary source; in particular the middle
letter in the dual presentation's final relation is positive b.

The word `(b*c^-1)^2*a*c^2*a^-1` has orders one and three in Q and Q′.
Regular flag transitivity lets any rank-preserving polytope isomorphism be
adjusted to the chosen base flags, so this disproves an unbased isomorphism
as well as a marking-preserving one. It does not assert that the two are not
dual. Every regular polytope cover of P factors through R. Since each cover
Q→R has prime kernel, an intermediate proper regular quotient is R, which is
not polytopal. This proves minimality. Doubling rotation orders gives the
source's 648, 1944 and 5832 flag counts.

GAP's exact finite-presentation and permutation-group algorithms remain
trusted. The package uses no finite catalogue or RAMP and supplies no Lean
certificate for these group orders. The existing Lean K lemma verifies only
the common algebraic transport component, not the geometric correspondence.

## Admission boundary

Admit this as a reviewed principal-result adapter conditional on the ledger's
G1–G3, C1 and A1 inputs, with its exact author-version corrections. The finite
program is a required external proof component and must be included or charged
in any future integrated length denominator. This audit gives no quantitative
compression ratio, no additional membership in the seven-source assembly and
no external peer review.

The main criterion is prior mathematics: the checked 2025 F005 source already
generalizes it. Neither the general multiple-minimal-cover question nor the
five-family conjecture follows from this adapter. A bounded literature search
found no resolution, but current open status is not certified by that absence.
Any new cover-poset research has separate files and is outside this audit.
