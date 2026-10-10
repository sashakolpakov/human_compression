# Dihedral centralizers and polytopes over a projective line

One common argument recovers the two specified principal classifications
of regular polytopes with automorphism group PSL₂(q) or PGL₂(q), in every
rank at least four. The complete proof is available as a
[manuscript](research/case_study/phase230_rank_one_classification.md) and
[nine-page PDF](research/case_study/phase230_rank_one_classification.pdf),
with an [independent review](research/case_study/phase234_review.md).

| Intake | Main results recovered | Exclusions |
|---|---|---|
| L083: Leemans and Schulte, *Groups of type L₂(q) acting on polytopes*, retained arXiv math/0606660v1 PDF | Rank restriction, Theorems 1, 3 and 4, the full ten-row table, uniqueness and the stated geometric properties of the 11-cell and 57-cell | Introductory results about other presentations and chiral constructions remain cited background. The bound PDF also has an August 2018 typesetting date; no later edition is inferred. |
| L079: Leemans and Schulte, *Polytopes with groups of type PGL₂(q)*, arXiv:0909.1991v1 | Rank restriction and Theorem 10: the unique example in rank at least four is the 4-simplex with PGL₂(5) | The additional seventeen-case PΣL₂(25) census and Conjecture 11 remain outside this recovery. |

Thus the matched implication is

```text
common centralizer proof + local markings + ten universal presentations
    → L083's stated principal classification
    → L079's stated principal classification.
```

The split into a complete topic umbrella U_E and two complete application
papers is in progress. The reviewed combined proof supplies their
mathematical content. Neither the nine-page rendering nor the two-source
count establishes a compression factor: matched source spans and all
required computational content still need to be measured.

## The common argument

In odd characteristic, the centralizer of a dihedral subgroup generated
by two involutions whose product has order greater than two descends to
the field of those involutions. For a semisimple product represented by
A, its only possible nonidentity centralizing projectivity is represented
by A − tr(A)I/2. For a unipotent product, the centralizer is trivial.

Together with elementary rank bounds and Dickson's subgroup types, this
excludes subfield facets uniformly. A PGL₂ facet would already contain the
fourth generator. A PSL₂ facet would be normalized by it; the odd adjacent
order then forces that generator into the facet too. Both conclusions
contradict independence. Only S₄ and A₅ facets remain.

The exact finite calculation gives six local marking classes and ten
universal presentations, up to duality. Their orders, quotient exclusions
and marked intersections leave precisely the 11-cell, 57-cell and
4-simplex. The proof includes uniqueness, the specified face counts,
self-duality, local projectivity and covering universality.

## Attribution and verification

The classifications retain their attribution to Leemans and Schulte; the
11-cell and 57-cell retain their attribution to Grünbaum and Coxeter.
Dickson's subgroup classification and the group–polytope correspondence
are retained inputs. The contribution here is a common centralizer
argument and the explicit route from six local markings to both complete
principal classifications. No historical priority claim is made for the
centralizer calculation.

The independent review checks every row of the historical table and all
nine pages of the replacement. Fresh public execution reproduces all ten
universal group orders, the marked intersection tests and four controls
that reject altered claims. Separate field computations check the
centralizer calculation on 384 semisimple and 144 unipotent pairs.

[DihedralFacetObstruction.lean](research/case_study/formal/DihedralFacetObstruction.lean)
verifies five general steps in the facet-normalizer obstruction, using
only Lean's standard axioms. The matrix calculation, classical inputs,
finite group computations and complete classification remain outside
that formal proof. GAP's exact algorithms are part of the trust boundary.

Use a new output directory:

```sh
python3 -B -O research/case_study/phase234_check.py --out /tmp/NEW-projective-line --lean LEAN --packages PACKAGES --gap GAP
```

The [replay guide](research/case_study/phase234_replay.md) specifies the
versions and optional primary-source checks. The
[publication record](provenance/phase121_review.md) and
[registry addition](research/case_study/phase235_projective_line_overlay.json)
admit two principal source results, bringing that count to 23. This
recovers known theorems and adds no solved-question entry.
