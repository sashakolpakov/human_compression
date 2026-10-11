Lean verification of support counting
====================================

The `two Lean modules <../../../../papers/topic-d/v2/support-formal>`_
verify the global orbit decomposition and both generic support-counting
statements in Topic D's `common paper
<../../../../papers/topic-d/v2/umbrella.pdf>`_. They construct the actual
actions, fixed-point sets and orbit quotients. The counting conclusion
is not an assumed hypothesis.

An equivariant base map first reduces an ambient orbit to an orbit under
the stabilizer of its base. Choosing one representative of each base orbit
gives an equivalence with the disjoint union of those fiber quotients.
Möbius inversion detects exact support. Burnside counting then yields
the full sum in UD.AdmissibleExtensions; UD.ExactSupportOrbits is verified
as well. Only the exact-top subset must be invariant. Individual support
sublevel sets need not be invariant.

The `independent review <independent_review/review.json>`_ read both complete
Lean modules, inspected six actual exported signatures and freshly compiled
all 28 declaration reports. These include equivalences and adapter
definitions, not 28 independent mathematical results. Seven altered proofs
were rejected and ten finite validations passed. All reported axioms are
among ``propext``, ``Classical.choice`` and ``Quot.sound``.

The invariant admissible subset R is represented by the acted-on type X.
Concrete applications must still construct it and prove their admissibility,
generation, support and geometry hypotheses. The divisor-poset interpretation,
least-field arguments, source classifications and finite censuses remain
outside this supplement. The normalizer theorem in UD.Orbits is also outside
its scope. This is not an end-to-end formalization of a source manuscript.

The classical incidence inverse identity and Burnside theorem come from
the pinned mathlib library and retain that attribution. The verified work
here composes them with the explicit action and fiber constructions. No
historical priority, new source result, solved conjecture or compression
factor is claimed.

Run from the repository root::

  python3 -B -O papers/topic-d/v2/support-formal/check.py \
    --out FRESH_DIRECTORY --lean PATH_TO_LEAN --packages PATH_TO_PINNED_PACKAGES

Use Lean 4.32.2 and the package revisions in
`dependency_manifest.json <../../../../papers/topic-d/v2/support-formal/dependency_manifest.json>`_.
The local modules and missing dependency objects are compiled in a fresh
private overlay. Existing pinned dependency objects remain trusted; this
is not a complete mathlib rebuild. The `actual type transcript
<independent_review/actual_types.txt>`_ records the inspected signatures.

This is an additive formal admission. It supersedes the earlier pending
status of this supplement in the frozen Topic D publication guide. The
original ten scoped declarations and mathematical admission remain
unchanged. The first twelve-declaration supplement is preserved under
``first_supplement/``; its complete first module is byte-identical to the
one in the current twenty-eight-declaration edition, and is not counted
again. The manuscript text and measured program boundary are unchanged.
