Joint fixed sets and string markings
====================================

Two descriptions of one fixed set can force an entire string marking to
preserve it. The `four-page manuscript <set_gluing.pdf>`_ gives the complete
proof and a conditional application to the remaining q8 prefix of F004.
The `TeX source <set_gluing.tex>`_ and
`independent review <provenance/review.rst>`_ are included.

The theorem
-----------

Let an ambient group act on a set, and let G be a target subgroup. Suppose
``t_0,...,t_(r-1)`` satisfy the string commutation relations, with r at least
five. Put a=t_0, b=t_1 and e=t_(r-1). If

.. math::

   S=\operatorname{Fix}(a)\cap\operatorname{Fix}(e)
    =\operatorname{Fix}(a)\cap\operatorname{Fix}(b),

every mark preserves S. An element of G moving a point of S outside S
therefore proves that the marks do not generate G. Membership of the marks
in G is unnecessary for this negative conclusion.

Indeed, a,b,e fix S pointwise. The interior marks centralize a,e, and the
penultimate mark centralizes a,b. Each consequently preserves one of the
two descriptions of S. This argument needs no field, involutions,
faithfulness or intersection property.

Attribution and application status
----------------------------------

The centralizer and stabilizer facts are standard. The set-preservation
escape argument was already used in the project's earlier invariant-set
work. The additional argument combines two descriptions of the same set
with the string relations. The criterion was proposed by ``/root``;
``/root/f009_consumer_lineage`` wrote the manuscript and certificate kernel;
``/root/packing_projection_review`` independently reviewed them.
Historical priority has not been established.

The associated original is Malcolm Hoong Wai Chen, *Abstract regular
polytopes of G2(q) in even characteristic*, arXiv:2609.25004v1 (2026),
catalogue F004. Its constructions and census claims retain their attribution.
The application here concerns one prefix in the retained G2(8) model;
it does not recover the source's complete census. The earlier project
profile and literal reader below are copied unchanged, with their original
paths and whole hashes recorded in the publication record.

For original job [68,5], a guarded exploratory scan found both complete
joint fixed sets equal to ``[1,10,11,12,13,14,15,16,17]``. An earlier
acquired target-G generator lookup is ``10 -> 586``. Their use together
still requires the current original-input joins, qualified producer and
strict supplied-certificate check, independent actual review and adoption.
The theorem removes a separate prefix-membership computation from that
proof obligation; it does not remove the original target-generator premise.

The `pure certificate relation <set_certificate.py>`_,
`synthetic controls <set_controls.py>`_ and their unchanged
`profile <primitives/profile.py>`_ and
`literal-reader <primitives/model_cycles.py>`_ dependencies are supplied for
inspection. They have no standalone execution entry. The review is static:
the 22 controls have not been run, and no completed finite job is claimed
by this package. It adds no completed original, conjecture answer,
compression measurement or Lean formalization.

Build and provenance
---------------------

With pdfLaTeX installed, build from this directory into a temporary directory:

.. code-block:: sh

   hc_build_dir="$(mktemp -d)"
   pdflatex -no-shell-escape -halt-on-error -interaction=nonstopmode \
     -output-directory="$hc_build_dir" set_gluing.tex
   pdflatex -no-shell-escape -halt-on-error -interaction=nonstopmode \
     -output-directory="$hc_build_dir" set_gluing.tex

The retained PDF was built in two passes; the second had no unresolved
references or box warnings. The `build record <provenance/written_build.json>`_
retains both complete compiler returns. Temporary build outputs were removed.
PDF bytes can vary between builds because of embedded metadata.

The `publication record <provenance/publication.json>`_ pins every supplied
artifact and records the scope. Frozen review and build records retain their
original local paths as archival identifiers; the publication record maps
the included artifacts to repository-relative paths.
