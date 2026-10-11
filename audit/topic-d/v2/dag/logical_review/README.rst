Topic D dependency review
=========================

This directory records a review of the mathematical dependency graph for
the accepted Topic D edition. It is not another independent review of that
edition's mathematics: this reviewer authored the current mathematical
papers, but did not author the graph. The separate full mathematical review
by ``enumeration_volume`` remains the basis for the mathematical admission.

The complete current common paper and three applications, all three primary
texts, all ten bound executable files, the graph builder and checker, and
every source-clause mapping have been read. The review found five errors or
omissions in graph edges and no mathematical manuscript defect. The exact
requests are preserved in ``requested_corrections.json``. The additive v2
revision resolves all five and is accepted. The original graph is immutable.

The exact comparison found seven added and three removed arrows, one more
precise node label, and two clarified edge explanations. The 45 scientific
inputs and 37 accepted records and output sets are unchanged. Fresh author
replay passed 15 controls; the separate checker passed 116 closures and 12
controls. Both final reader pages were inspected. No weights, numerical
factors, source credit or conjecture credit are assigned here.

``check_independent.py`` independently checks the bound input files, all
source mappings and recursively computed dependency closures. It imports
none of the author's implementation. Its controls test the reviewed
premises, program roles, exclusions, formal scope and unknown costs.

Run it against the immutable author revision::

  python -B -O check_independent.py --packet /study/topic_D_logical_dag_v2 \
    --study-root /study --public-root /repo --out /fresh/closures.json

Compare the immutable editions independently::

  python -B -O check_delta.py --old /study/topic_D_logical_dag \
    --new /study/topic_D_logical_dag_v2 --out /fresh/delta.json

The review reads historical arrows as documentary statements of the source
argument. It does not retroactively certify faulty arguments. The corrected
source clauses and excluded assertions remain distinct from the accepted
current proofs. Overlapping proof locators are not exclusive cost spans.
