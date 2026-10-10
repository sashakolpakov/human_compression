# Phase-thirteen review record

10 October 2026. This phase completes the unitary parameter construction
for every odd field size congruent to one modulo four, strengthens the
cyclic TPP bounds, and repairs the common-quotient existence argument
through nilpotency class three. The [complete root review](../research/case_study/phase13_root_review.md)
and [hash-bound record](../research/case_study/phase13_root_review.json)
state the mathematical checks and retained inputs in detail. These
reviews are internal, not external peer review.

## A complete unitary congruence class

The smooth cubic links a split-torus primitive element to a nonsplit
one through precisely the characteristic-polynomial equation needed
by the existing four-matrix template. Character sums on the punctured
genus-one curve give a uniform estimate. A primitive-character sieve
and four exact primorial bounds cover all eligible fields at least
98,660. Characteristic three uses the previous rational-curve argument.

The exact remaining intake contains 4,795 prime-power fields. The
sieve leaves 406, and the original package gives a defining polynomial
and explicit element coordinates for every one. Root wrote and freshly
executed an independent standard-library verifier, using trial arithmetic
and polynomial quotients instead of the author's GAP arithmetic and
prime-sieve implementation. It verifies all irreducibility, field,
torus-order, square-field and projective matrix-order conditions.
All 406 witnesses pass, including the distinct q=5 plus-branch case.

Root and a separate reviewer read the complete geometry and sieve
proofs. The separate reviewer reran both author Python checks; their
reports agree apart from timestamps. Generation and all intersection
properties retain the phase-eleven proofs, and maximum rank retains
the phase-nine obstruction. The result is maximum rank four for
PSU₄(q), every odd q≡1 mod 4. The construction has type {4,q²−1,2p}
for q>5, and {4,26,10} at q=5. Other odd congruence classes and general
almost-simple extensions are not settled by this construction.

The [dated status audit](../research/case_study/phase13_unitary_priority_audit.md)
records thirty searches and the precise published rank-three baseline.
It found no earlier matching uniform rank-four theorem or named unitary
conjecture. This bounded search does not establish novelty or certify
that the problem remained open. The similarly phrased named survey
conjecture concerns PSL₄ and is kept distinct.

## Stronger 2-group restrictions and order bounds

The actual highest power subgroup of the powerful core has a basis
consisting of the top involutions of the longest cyclic factors. One
or two longest factors force a marked involution to be central, using
only the one- or two-dimensional binary action. Consequently all
three cyclic orders in a minimum unrestricted counterexample are
equal, at least sixteen, and its group order is 2^(3e−1), e≥4.

The [main proof](../research/case_study/phase13_cyclic_tpp.md) separately
justifies minimum-counterexample induction within the smallest-factor
bound. Every reduction preserves a factor of order at most eight.
This gives the uniform factor-eight theorem, the bound for all
2-groups through order 1024, and the hypertope pair-order≤16 and
group-order≤2^13 consequences. The earlier order-256 finite theorem,
marked-isobicyclic classification and powerful-group results are
explicit retained inputs. No order-1024 catalogue was searched.

Root and two other agents reviewed this proof. Fresh root and independent
focused checks are byte-identical to the author report. The separate
[top-action supplement](../research/case_study/phase13_cyclic_tpp_top_action.md)
has independent reviews and fresh exact checks as well: there is one
possible marked action on the three top involutions. Its kernel is
Φ(P), its image is C₂² and its central line is the product of all
three marked involutions. This supplies a necessary condition, not
a contradiction or a full conjecture resolution.

## A canonical quotient in every rank through class three

The [common-quotient proof](../research/case_study/phase13_common_quotient_class_three.md)
uses edge supports and the original group's intersection property to
prove independence of all adjacent commutators modulo γ₃. Thus every
nondegenerate string C-group marking of class at most three maps,
with its marking, onto the path-cocycle group of order 2^(2d−1),
with kernel γ₃. The proof works for every rank d≥2 and uses no
finite-group catalogue.

Root reviewed the complete proof and freshly ran the NQ checker.
All 70 collection comparisons and 1,344 subset intersections pass.
The author's and root's transcripts agree after newline normalization;
only the first CR/LF differs. These finite diagnostics are separate
from the uniform support argument.

This repairs a structural subcase of the main existence claim in the
specified 2026 preprint. It does not repair the source's incorrect
Frattini-intersection kernel formula, and higher nilpotency classes
remain unresolved by this proof.

## Export and measurement

The [original-file manifest](phase13_original_files.json) binds the
byte-identical original artifacts. Third-party publications and the
superseded exploratory probe are excluded. Earlier proofs and all
seventeen saved Lean reports remain unchanged. No new Lean module
is added; the group and character-sum arguments remain written proofs.

The nine-work principal-result ledger and the only matched-length
ratio, 127/38≈3.34 for the specified two L066 formulas, are unchanged.
These results extend uniform theorem coverage; they do not establish
a corpus compression ratio or justify a verified-new-resolution
infinity marker in this snapshot.
