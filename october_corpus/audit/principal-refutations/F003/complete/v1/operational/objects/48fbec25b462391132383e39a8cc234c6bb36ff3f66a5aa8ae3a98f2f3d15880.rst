A chiral polytope of rank four for a Suzuki group
================================================

The `five-page proof <proof/rank4_counterexample.pdf>`_ constructs a chiral
abstract polytope of type {31,31,25} with automorphism group Sz(32768).
Its two face groups are copies of Sz(32) meeting in a cyclic group of
order 31. This is a counterexample to Theorem 1.1 of Pablo Spiga,
*On the rank of Suzuki polytopes: an answer to Hubard and Leemans*,
`arXiv:2010.04080v1, 8 October 2020
<https://arxiv.org/abs/2010.04080v1>`_. The claim concerns that fixed
preprint edition.

The proof gives every matrix over an explicitly defined finite field.
A Bruhat decomposition proves the exact intersection of the two face
groups; maximal subfield structure proves generation of Sz(32768).
The cited rotation criterion gives a polytope, and odd centralizers and
the odd outer automorphism group establish chirality. The full ambient
group is not enumerated.

The source comparison identifies a specific defect in the supplied proof:
Wilson's product identity is applied to pairs outside its stated domain.
The normalized example satisfies the correct group equations but fails
source equation (13), with exact residual 28331.

The Suzuki coordinates, classical subgroup and automorphism structure,
and polytope reconstruction theorem are borrowed inputs, with attribution
in the manuscript. The explicit marking and its proof are the present
contribution. `Provenance <proof/provenance.json>`_ distinguishes the
construction from the root agent's contribution to the source diagnosis.
The `independent review <independent_review/review.rst>`_ includes a
separate GAP reconstruction of both 1,025-point face actions. Its
`second-edition addendum <v2_addendum/review.rst>`_ checks the citation
correction and the audit of earlier bounded arguments. The
`root adoption <root_adoption/adoption.json>`_ accepts that reviewed result.

Replay from the repository root, with Python and GAP installed::

  python corrections/suzuki-rank/v1/check.py --out /absolute/new/output

Add ``--render`` to rebuild the complete TeX manuscript; this also requires
pdflatex and pypdf. The replay verifies both exact arithmetic implementations,
the frozen evidence and its scope. Primary papers and their review images
remain hash-bound references; the public checker does not need private
source files. It does not rerun the discovery search.

This is a correction to a principal assertion, not a compressed proof of
that assertion. No compression ratio, new open-conjecture credit, complete
Lean verification, historical priority claim or claim about later editions
is made. Its `catalogue disposition proposal
<catalogue_disposition_proposal.json>`_ gives a separate terminal category
for a reviewed refutation; publication and catalogue registration remain
root actions.
