# Review and completion of the cyclic-index bridge

The mathematical shortcut in the root-authored phase165 note passes independent
review. Its citation to a class-two recognition theorem in U needs correction:
the exact result is **A2.3/A2.4 in the second edition of Construction and
classification of two-group polytopes and hypertopes**. U.Nilpotent deliberately
assumes that recognition. The separately bound completion note makes this
correction and supplies the previously missing source-presentation, abstract
nonisomorphism and product-decomposition arguments.

The completed all-parameter argument recovers Loyola's Theorem4.1 with an
explicit correction to its final semidirect-product parameter assignment, and
the structural content of Proposition4.2. This is not a replacement for the
whole 31-page paper. Its separate abstract-group catalogues and involution
tables are not proved here. No new source count, whole-paper compression ratio,
open-conjecture answer, historical novelty or whole-theorem Lean certification
is claimed by this package.

There are two distinct roles in this package. The review of the root-authored
phase165 proof is independent of its author. The new missing arguments in
`phase169_cyclic_index_completion.md` are authored by this reviewer and still
require a separate root or other independent review before admission. A frozen
author-complete extension is not thereby an independently admitted extension.

## Source and existing-theory reading

The source is Mark L. Loyola, *String C-groups from groups of order 2^m and
exponent at least 2^(m−3)*, arXiv:1607.01457v1, 6 July 2016. Its full 31-page
PDF has SHA-256
`74b2a1b49e81aa30fd2fa067660a7dc402607707a4a83f618900edff06c53477`.
The complete saved extraction was freshly read, including the introductory
scope, all presentation families, the principal proof and all appended tables
and references. This does not mean that every classification-table entry was
independently verified. The relevant printed pages11–14 were freshly rasterized
and individually displayed to check the theorem, original presentation,
parameter convention and product proof. Remaining PDF pages were read through
their full extraction, not individually visually inspected.

The exact root working note reviewed is SHA-256
`af820259b49248650e6a91ec6958545c1351649967b7bb83bdfc244649afacb2`.
The existing A second edition is SHA-256
`0304c85d3ea6592a3778c380dfbb60e3dc842fa38f5b6151a40a9eeab057a47e`.
Its full A2.1–A2.4 recognition argument and s=3 model/interface in §5 were
reread, together with the relevant square-group presentation in §3. The exact
U3 statement distinguishing assumed quotient recognition from U.Nilpotent's
search conclusion was checked. No source-access search or later-edition claim
is implied by this review.

## Independent findings on phase165

The quotient has order 2^(2d−1) and exponent four for a connected rank-d
finite two-group string C-group. A cyclic image has order at most four, giving
the index bound immediately. Equality in rank three forces the third
lower-central subgroup into the maximal cyclic subgroup; its order is exactly
M/4. This conclusion concerns an actual canonical quotient recognized using
IP, rather than an assumed IP property of an arbitrary quotient.

When that third term is cyclic, two adjacent orders at least eight would give
a common nontrivial half-rotation. The original intersection property excludes
it, so one adjacent order is four. The proof that K=<r^4,h> is sound: its
right side is characteristic in cyclic K, and the quotient is demonstrably
class two. Conjugation on a cyclic group has abelian image, so the commutator
x centralizes h; inversion by x then makes h have order at most two.

For M≥16 this forces r^4 to generate K. The M=8 argument is also valid:
centrality of K gives gamma4=1, hence an abelian derived group; if both adjacent
orders were four, its generating conjugates would be involutions, making the
whole group exponent at most four. The M=4 case is exactly the order32
class-two model. These are uniform arguments, not an inference from a few
small-group identifications.

The central-product model and its commuting involutory actions work at all
stated parameters. The M=4,epsilon1 action fails to preserve the identified
half-rotation and is correctly excluded. The coset-square calculation proves
the exponent, and the parabolic intersection argument proves IP. The
disconnected-component reduction is also correct; the completion spells out
the final short enumeration rather than leaving it implicit.

The root note itself explicitly left unmarked distinctness, the literal
presentation bridge and named semidirect products unfinished. Those were real
remaining obligations. The new completion supplies them as follows.

## Newly supplied completion

For M≥8 the centers of the two models have orders four and two. An element
in an a-coset cannot centralize r because conjugation introduces an x
coordinate. In a c-coset it would force r² to equal a half-rotation of order
at most two. The center therefore lies in the collected normal subgroup,
where its exact description is elementary. This establishes unmarked
nonisomorphism, stronger than a differing word in a fixed marking.

The universal word identity h^b=(abcb)² is proved using only the common
involution, distant-commutation and order-four relations. It converts Loyola's
extra Coxeter relator exactly to h=z^epsilon. Those same relations make z
central and collect every word to one of at most8M forms. The explicit model
attains this bound. Thus the literal presentation defines the model, rather
than merely mapping onto it. Inverse generator substitutions are written for
the older p,q,r presentation too; all seven defining relations are accounted
for in both directions.

The factors L=<c,r²> and H=<a,x> have trivial intersection and orders M and
four. Their complete conjugation actions are supplied, as is the outer
involution b. The inner action is trivial for epsilon0 and nontrivial for
epsilon1. This agrees with Proposition4.2 and the source conclusion, while
the final sentence of Theorem4.1 on p.11 assigns the parameters in the
opposite order. The completion states the correction rather than silently
relabeling the source. It does not claim discovery priority for that correction.

Smoothness follows from the exact adjacent orders. Infinitude of the ambient
[4,M] is supplied by its epimorphism onto the affine [4,4] model already
proved in A §3. Finally, the direct-product component argument supplies all
four nonconnected/low-rank clauses with their elementary-abelian boundaries.

## Computation and practical limits

The pure-Python checker implements the collected group law independently of
GAP. It checks all11 permitted cases at M=4,8,16,32,64,128. It verifies the
two normal-subgroup actions on every pair of elements, their commuting
involutory property, generation, every element's exponent, all64 marked
subset intersections per group, both presentations and inverse substitutions,
the exact center, and every stated factor/action assertion. The total is704
IP checks. The smallest normal subgroup additionally has every associativity
triple checked. Associativity and all-parameter validity come from the written
central-product/semidirect-product construction, not the finite sample.

A separate GAP4.15.1 program begins with the two literal finitely presented
groups. For M=4,8,16,32 it checks all seven permitted parameter cases, exact
orders, exponents and centers, and both generator maps and their inverses.
It uses no source abstract-group catalogue or SmallGroups identifiers. Its
negative boundary proves that the excluded M=4,epsilon1 presentation has
order16 and right adjacent order2, so it is not a second order32 case.
The final exact run took about3.16 seconds for these literal-presentation
checks and0.35 seconds for the coordinate checks.

An earlier unfrozen exploratory GAP run reached the generic coset enumerator's
4096000-coset limit at M=64,epsilon1. That attempt is not counted as a passed
larger-presentation check. The final executable deliberately declares the
smaller range above; the independent coordinate check reaches M=128 and the
written collecting proof covers every power-of-two parameter. No inference of
failure of the mathematical presentation was drawn from the computation limit.

The standalone wrapper binds both exact programs, rejects existing outputs and
changed inputs, checks completion markers even when GAP returns zero after an
error, and records all runtime hashes. An isolated run with only its three
public arithmetic files passes. Nine controls cover this positive portable
replay, two program mutations and preservation of existing files, directories
and dangling symlinks by both the runner and coordinate checker. The root
manuscript, shared theory and private source files are not runtime inputs to
this finite replay.

The arithmetic can be repeated with:

```sh
python3 -B -O phase169_cyclic_index_verify.py --output-dir /private/tmp/NEW-cyclic-index
```

Add `--gap /path/to/gap` if GAP is not on PATH. The full mathematical proof
still requires the explicitly cited A recognition theorem. No new Lean file
or full written-proof/formal-statement certificate is claimed.

## Scope of a future attachment

The frozen ledger separates the fully derived Theorem4.1/Proposition4.2
contract from the unclaimed abstract-group catalogues, table completeness and
individual catalogue exclusion statements. The source's146 candidates include
the separate nine higher-exponent groups as well as its123+14 enumeration;
none of that general catalogue completeness is imported or newly credited.
The shared proof interface is A's canonical quotient, and the new local cost
is the full cyclic-third-term/model/presentation argument, including all small
boundaries and unmarked distinctions. No matched source-length measurement
was performed, and no numerical or whole-paper compression factor follows.

All new proof, check, log and review files have an exact manifest allowlist.
The original phase165 note, existing U/A files and public tree were not edited.
