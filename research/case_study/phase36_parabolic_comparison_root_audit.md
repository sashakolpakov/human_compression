# Root review and fresh formal verification of the comparison theorem

Date: 2026-10-10. PASS for the written theorem and the stated Lean interface.

The written theorem compares full marked subgroup intersections and typed
coset Helly under injectivity on products of protected parabolics and exact
exceptional membership on that set. I read the full proof and the separate
reviewer's indexed-exception correction. Redundant markings are correctly
handled by omitting only the tautological index pair E,E.

I also read the entire Lean source and checked its interfaces against the
written assumptions. Protected membership reflection and image meets use
no IP hypothesis. Product comparison handles the protected/protected and
both exceptional-factor orientations. The right-coset difference order is
correct. A protected anchor and simultaneous representative choice prove
the complete source-to-image Helly direction for arbitrary type sets;
the retained one-exceptional theorem proves the reverse direction.

The formal conclusion therefore holds for arbitrary groups and type sets
and requires no global surjectivity. It proves actual common-point existence
for every selected pairwise-incident family, including infinite families.
The full marked-IP equivalence and the specific matrix/geometric applications
remain written arguments; they are not implicitly included in this Lean claim.

A fresh public-run compilation checked both unchanged dependency modules
and the new module, in a clean scratch output directory with pinned Lean and
all nine recorded package revisions. All three passed. The new six printed
theorem axiom lists use only propext, Classical.choice and Quot.sound; there
is no sorry or native-evaluation axiom.

The public runner now computes transitive local import closure. This is
needed because the new source imports OneExceptionalParabolic, which in
turn imports ParabolicQuotientTransport. The fresh three-module run verifies
that the dependency closure is actually selected and compiled. The Lake
root list is synchronized with all35 certificate names; its former shorter
list did not match the documented full-build scope.

These are internal mathematical/interface reviews and actual kernel runs,
not external peer review, a historical-priority judgement or a new paper's
main-result coverage claim. Earlier pending status strings remain historical.
