# Scope of the odd-cover separation certificate

This certificate proves six general algebra/order statements. It is an
author package pending independent review and public admission.

Let π:H→G and σ:J→G be group homomorphisms and let q:H→J be a surjective
homomorphism with σq=π. Then the induced map ker π→ker σ is surjective,
so |ker σ| divides |ker π|. An odd covering-kernel order therefore stays
odd under every quotient over G. In particular an odd-degree cover cannot
map onto an even-degree cover, including a double cover, over the same base.

No surjectivity of π or σ is needed for these statements. The kernel
cardinalities use `Nat.card`; assuming one is odd entails that it is nonzero.
The source kernels need not be abelian or elementary abelian.

The sixth theorem assumes H finite and takes an explicit arbitrary predicate
`admissible : Subgroup H → Prop`, with `admissible ⊥`. It produces an
admissible normal subgroup N≤ker π maximal among all subgroups satisfying
those three conditions. The predicate is not hidden mathematical content:
no string C-group or polytope predicate is defined or established here.

## Relation to minimal covers

For a finite polytopal marked cover H→G, the intended predicate says that
the marked quotient H/N remains polytopal. The trivial subgroup is then
admissible. Under the standard cover/quotient correspondence, a maximal
admissible N gives a minimal polytopal descendant: any further polytopal
quotient would correspond to a larger admissible normal subgroup of H.
This interpretation uses that correspondence as a written input; it is
not a formalization of the correspondence itself.

If H→G has odd degree, every such descendant still has odd degree and
cannot factor onto a known double cover of G. Hence it differs from that
cover. To conclude a second minimal cover for a particular chiral polytope
also requires the written relation between that source and its smallest
regular maniplex. The candidate enlarged-end construction is a separate
package and is not an input or a theorem of this certificate.

## Attribution and trust

The arguments are standard group theory and finite-order reasoning.
Mathlib supplies Lagrange's cardinality divisibility and existence of a
maximal element in a finite set. The repository supplies the commuting
kernel map, its surjectivity proof and the exact scoped Lean statements.
There is no historical novelty or open-problem resolution claim.

`phase105_odd_cover_separation_check.py` compiles the exact hash-bound
source under Lean 4.32.2 and the recorded dependency revisions. Its six
axiom reports permit only `propext`, `Classical.choice` and `Quot.sound`.
There are no unproved placeholders or native-evaluation axioms. Existing
compiled mathlib objects remain trusted build inputs. The interface is
adapted from the previously reviewed phase68 compiler wrapper; it is not
a new mathematical proof ingredient.

From the study directory, choose a new output directory:

```sh
python3 -O phase105_odd_cover_separation_check.py \
  --packages /path/to/pinned/packages --lean /path/to/lean-4.32.2 \
  --output-dir /tmp/odd-cover-separation-new
```

This standalone formalization adds no source manuscript or compression
factor, and proves neither existence nor intersection recognition for a
proposed cover. The entire proposed construction still needs its own
mathematical and computational review.
