# Distinct kernel characters separate marked covers

10 October 2026. This certificate formalizes one algebraic step in the
[odd-prime family proof](../phase49_cover_family_theorem.md).

Let π:H→G and π′:H′→G be group homomorphisms, and let a and a′ be specified
elements. Suppose z∈ker π is not equal to its inverse, conjugation by a
inverts z, and conjugation by a′ fixes every element of ker π′. Then there
is no group isomorphism e:H≃H′ with e(a)=a′ and π′∘e=π. No finiteness or
surjectivity hypothesis is needed. An additional lemma shows that an
element of odd prime order is not self-inverse, giving that specialization.

The declarations in namespace `MathCompression.CoverCharacterSeparation` are
`no_marked_cover_iso`, `ne_inv_of_odd_prime_order`, and
`no_marked_cover_iso_of_odd_prime_order`. The proof transports z and its
conjugation equation through the proposed isomorphism and uses injectivity.
The order lemma uses mathlib's element-order divisibility theorem.

In the written family theorem, Q and its dual have kernel characters
(-,+,+) and (+,+,-) on their corresponding marked generators. Their kernels
have order p. These independently reviewed written facts supply the formal
theorem's premises. The source file does not construct those groups or
verify their action tables, polytopality or minimality. It distinguishes
marked covers over the common base; it does not exclude an abstract group
isomorphism or a rank-reversing duality.

The [saved build](CoverCharacterSeparation.check.json) uses Lean 4.32.2 and
the pinned dependencies. The first declaration uses `propext` and
`Quot.sound`; the other two also use `Classical.choice`. There are no
unproved placeholders or native-evaluation axioms. Pinned dependency
revisions and tracked cleanliness are checked; existing compiled dependency
objects remain trusted build inputs.

With dependencies installed as in the [formal instructions](README.md), run:

```sh
python3 research/case_study/formal/verify_lean.py CoverCharacterSeparation.lean
```

This component adds no manuscript, length ratio or historical-novelty claim.
