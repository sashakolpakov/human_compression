# Finite covers preserving the end subgroups

The [six-page paper](research/case_study/phase246_locally_faithful_covers.pdf)
gives an exact criterion for finite abelian covers that preserve both end
subgroups. It applies in every finite rank at least three, provided those
end subgroups already satisfy the intersection property. The
[independent agent review](research/case_study/phase255_locally_faithful_review.md)
accepts the written proof and its computational application. This is internal
review; no external peer review or historical priority is claimed.

## The reusable criterion

Let the marked end subgroups be A and B, their shared marked subgroup C,
and their actual intersection D. Glue A and B along C and impose the
commutation of the two extreme generators. The kernel of the resulting
map onto the base group is the fundamental group of an explicit finite
complex X. Each element of D outside C determines a discrepancy class in
the first homology of X.

| Conclusion | Exact condition |
|---|---|
| A finite abelian cover preserving both ends exists and satisfies all marked intersections | Every discrepancy is nonzero in integral first homology |
| Such a cover exists with an elementary abelian p-kernel | Every discrepancy survives modulo p |
| No cover preserving both ends has a nontrivial p-group kernel | First homology modulo p vanishes |
| A non-C base has infinitely many finite minimal regular covers | Every discrepancy survives in rational first homology; this is a sufficient condition |

The proof includes the construction of the kernel, identification of the
actual discrepancies, and both directions of the abelian criterion. The
last row supplies a route to multiplicity, not a claim that its hypothesis
always holds. The [full text](research/case_study/phase246_locally_faithful_covers.md)
and [source ledger](research/case_study/phase246_source_ledger.json) give the
statements, proofs and retained classical inputs.

## Complete application within the stated class

For the Tomotope, the complex has 48 vertices, 768 edges and 18,432 translated
square cells. Exact integer reduction gives first homology C₂ × C₂, with
nonzero discrepancy. There are precisely two covers preserving both ends
with abelian kernel, of orders **73,728 and 36,864**. The latter is minimal.
There is no such cover with a nontrivial odd-prime-power kernel, including
nonabelian kernels.

The smaller cover is identified with the earlier cover in
Monson–Pellicer–Williams, Proposition 4.5, using its marked map and end orders.
Their prior cover constructions and infinite multiplicity theorem keep
their attribution. This application claims a classification within the
specified class, not new existence merely from producing those orders.

## Verification and remaining problem

Independent GAP code reconstructs the complex using different coset
numbering and computes the action on the actual kernel. The public replay
checks the integral reduction, the generated covers, all 256 marked
subgroup intersections and deliberate false inputs.

Three [Lean proofs](research/case_study/formal/LocallyFaithfulIntersection.lean)
verify the quotient-intersection equivalence, faithfulness on an end and
kernel containment. The topology, integer computation and full cover
theorems remain outside Lean. See the
[formal scope](research/case_study/formal/LocallyFaithfulIntersection.scope.md)
and [publication record](provenance/phase130_review.md).

The **general finite minimal-cover multiplicity question remains open**.
The Tomotope obstruction shows that restricting attention to covers
preserving both ends cannot provide a uniform odd-prime construction.
The separate [surface method](INFINITE_MINIMAL_COVERS.md) enlarges the ends.
This packet adds no principal-source count, complete conjecture answer or
compression ratio.

With the pinned dependencies, use a new output directory:

```sh
python3 -B -O research/case_study/phase260_check.py --out /tmp/NEW-local-covers --gap GAP --lean LEAN --packages PACKAGES
```
