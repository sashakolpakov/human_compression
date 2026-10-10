# Boolean retractions and four-marker centralization

`BooleanRetractions.lean` contains two fully checked group lemmas.

* `range_intersection` derives intersection of two endomorphism images
  from the Boolean composition law e_S e_T=e_(S intersect T).
* `four_marker_centralization` derives commutation of both squared
  translation words with the fourth generator from involution and
  string commutation relations and the commutation of two edge squares.
  It holds in arbitrary groups, without a finite-order hypothesis.

The saved `.check.json` binds the source to its successful Lean 4.32.2
compilation. The printed axiom sets contain no incomplete-proof axiom;
the first theorem uses propositional extensionality, choice and quotient
soundness, and the second only propositional extensionality.

The module certifies two components of
[the fiber-product proof](../phase16_fiber_products.md). It does not
construct the toroidal seeds or their Boolean maps, identify the full
presentation, compute orders, or construct the regular, semiregular
or chiral polytopes. Those bridges and the retained geometric inputs
are explicit in the written proof. No end-to-end formalization is claimed.
