# Primitive elements giving a nonzero square

For every odd prime p and odd integers e₁,e₂ greater than one, there are
primitive elements jᵢ in F_(p^eᵢ) for which

```math
(j_1+j_1^{-1})^2(j_2+j_2^{-1})^2
-4\bigl((j_1+j_1^{-1})^2+(j_2+j_2^{-1})^2\bigr)
```

is a nonzero square in the compositum. Equal and nested fields are included.
This answers Conjecture 6.1 in the bound June 2016 author edition of
Leemans, Moerenhout and O'Reilly-Regueiro, *Projective linear groups as
automorphism groups of chiral polytopes* (arXiv:1606.08017v1).
A separate collation with the 2017 journal edition and historical priority
have not been established.

The [complete proof](research/case_study/psl2_square_proof.md) now has a
[detailed independent arithmetic review](research/case_study/phase267_review.md).
The review accepts the whole stated range without a mathematical amendment.
It checks the quartic and its coefficient norm, all field configurations,
the primitive-character estimate, the strict bounds and every remaining
finite case. Finite-field theory, character orthogonality and the Weil
bound are retained mathematics. The proof contributes their particular
norm construction and complete reduction for this expression.

The independent replay checks all eleven exceptional witnesses, reconstructs
214,132 primitive pairs across five exceptional equal fields, and tests
actual compositum norms in four cases. Four corrupted certificates are
rejected. These computations complement the uniform written proof.

[Six Lean declarations](research/case_study/formal/PrimitiveSquarePolynomial.lean)
verify the actual quartic, derivative, trace identity, polynomial identity
and separation of roots. Their [scope](research/case_study/phase266_formal_scope.md)
excludes the character-sum argument and the full conjecture. The fresh public
replay passed under pinned Lean 4.32.2 and Mathlib dependencies.

```sh
python3 -B -O research/case_study/phase269_check.py \
  --out /tmp/NEW-primitive-square-review \
  --gap GAP --lean LEAN --packages PACKAGES
```

No primary full text is distributed or needed by this command. See the
[publication record](provenance/phase131_review.md) for the exact frozen
bindings and replay. This strengthens the evidence for an existing question
entry; it adds no new question, principal-source credit or compression rate.
