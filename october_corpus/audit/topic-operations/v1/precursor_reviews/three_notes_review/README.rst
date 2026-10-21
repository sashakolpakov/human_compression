Independent review of three N005 notes
======================================

The root-authored free-product/converse, semidirect-join, and firm indexed
admissibility notes are accepted in their exact bound scopes. All seven
pages and the relevant primary definitions and assertions were read.
The complete arbitrary-group proofs were checked in writing; the finite
models are additional validation and cannot establish their generality.

This review does not admit a complete replacement of N005. It does not
review the separately authored S4 nonfirm counterexample, assign a ratio,
or formalize the group-theoretic arguments in Lean. The earlier compatible
tree-gluing and HNN results are retained with their exact review bindings.

Replay::

    python3 -B -O check.py --study-root /path/to/leemans --out /fresh/path

Optional fresh rendering uses ``--render --xelatex /path/to/xelatex``;
the interpreter must then provide pypdf and the TeX installation must have
STIXGeneral and STIX Two Math. Render checks compare each complete page's
extracted text with the bound author PDF and reject diagnostics. The review
does not distribute the primary PDF, its full text, or its rasters.
