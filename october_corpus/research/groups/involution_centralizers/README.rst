Subgroups avoiding the central involution
=========================================

The manuscript ``subgroups.tex`` proves an elementary order bound. Put

  C = {(X,Y) in GL2(11)^2 : det X = det Y} / {(sI,sI) : s in F11*}.

If H is a subgroup of C containing a Klein four and avoiding the central
involution z = [I,-I], then |H| <= 1320. The proof uses the two projective
projections, Sylow theory and explicit projective stabilizers. It does not
use a classification of all subgroups of PGL2(11).

An independent agent reviewed the exact manuscript in
``subgroups_review.rst``. The draft predates that review; the review records
its whole-file hash and two optional explanatory expansions. No blocking
omission was found. This is a written mathematical review, not a Lean proof.

Application to a marking
------------------------

For a string marking (a,b,c,d,e), suppose the actual centralizer of e is
identified with C, carrying e to z. The intersection property then requires
|<a,b,c>| <= 1320. Thus 1321 pairwise distinct matrix word images obstruct
the intersection property. This lower bound needs only a genuine
homomorphism, since distinct images imply distinct original elements.

A direct word equal to e gives another obstruction. Equality of matrix
images alone lifts to that group equality only under a suitable faithful
representation or a separate original-group equality proof. The manuscript
keeps these two certificate interfaces separate.

The centralizer identification is an explicit hypothesis of the marking
application. This package proves the group-theoretic bound, not that model
identification for an arbitrary supplied group. It contains no newly run
candidate census, completed source manuscript, conjecture resolution,
compression measurement or Lean formalization.

Read and build
--------------

Read ``subgroups.tex`` and the independent review. ``manifest.json`` records
their exact bytes. The proof is self-contained for the defined group C.
To typeset it, use a LaTeX installation with amsmath, amssymb, amsthm and
geometry, keeping build files outside the checkout::

  build_dir=$(mktemp -d)
  pdflatex -halt-on-error -interaction=nonstopmode -output-directory "$build_dir" subgroups.tex

No PDF build is asserted by this publication. The title page retains the
author's draft date; the independent review is the current proof assessment.
