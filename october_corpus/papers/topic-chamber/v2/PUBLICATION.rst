Chamber fibers, reflections and regular covers
==============================================

Read the six-page `common paper <umbrella.pdf>`_, the three-page application
`A two-coset criterion for chiral hypertopes <testing-chirality.pdf>`_, and
the six-page application `Chirality kernels and the smallest regular cover
<minimal-regular-covers.pdf>`_. Editable TeX, the three-page complete
`program appendix <programs.pdf>`_ and scoped Lean proofs are included.

The common arguments
--------------------

Fixing part of a flag leaves a choice of extensions. Its stabilizer acts on
those choices, and a double-coset space records the remaining orbits. In a
thin geometry the relevant panel must have exactly two extensions. The
common paper gives this exact coset statement before using finite
cardinalities to count it. It then reconstructs the geometry from chamber
adjacencies and writes the reflection explicitly on two copies of the group.
This distinguishes an action by the designated group from the full
automorphism group until the necessary argument has been proved.

For regular covers, the relation kernel and its mirror give the smallest
regular group cover. Whether that cover is a polytope is a further question.
The common intersection lemma isolates the obstruction in the actual
embedded kernels. The application identifies those local kernels and proves
the required regular-end induction before invoking the lemma.

Double-coset normalization and kernel transport are elementary group theory.
The chirality criteria and cover constructions remain attributed to their
original authors. Our contribution in this edition is a common set of
explicit proofs, complete application arguments, source qualifications and
scoped formal verification. No historical priority is claimed for this
organization. The standard geometric correspondence, Schulte–Weiss section
theorem, square-tessellation model and specified Cunningham–Pellicer
classification remain declared inputs; their expanded proof costs are unknown.

.. list-table:: Source manuscripts and recovered results
   :header-rows: 1
   :widths: 32 43 25

   * - Authors and checked edition
     - Current derivation
     - Qualification
   * - W.-J. Zhang and D. Leemans, *Testing chirality on hypertopes*,
       arXiv:2511.14562v1, November 2025; ten pages
     - Theorem 1.1: both directions of the chirality criterion, residual
       connectedness in every required rank and the full automorphism argument
     - Exact two-coset formulation for infinite groups; ancillary Magma
       implementations excluded from the principal target
   * - Gabe Cunningham, *Chiral polytopes whose smallest regular cover is
       a polytope*, author manuscript of 25 July 2023; eight pages
     - All proved conclusions: Propositions 2.2–2.4, Theorem 3.1, Remark 3.2,
       Corollaries 3.3–3.4, Example 3.5, Proposition 3.6, Corollary 3.7,
       Example 3.8, the uniqueness implication and the complete finite example
     - Retained classification and geometric inputs; nonidentity-power
       correction; publisher PDF not acquired

The second application treats the square-torus family, all five specified
atomic families and the six exact groups in the finite example. It verifies
the two distinct minimal regular polytope covers and the nonpolytopal
smallest regular group cover. The `scope record <scope.json>`_ has 27 rows
and 22 written passages. Those rows include exclusions and separate questions;
they are neither 27 manuscripts nor 27 newly solved problems.

Questions remain separate
-------------------------

The `question map <question_map.json>`_ links the earlier admitted answers
about unrestricted covers, finite rank-four covers and interval extension.
These later results are not premises of the present applications and earn
no second credit. General finite minimal-cover multiplicity in all ranks
remains unresolved. The three separate question manuscripts are not assumed
as free common theory here.

Verification and measurement
----------------------------

The `independent scientific review
<../../../audit/topic-chamber/v2/independent_review/README.rst>`_ read both
complete sources, all current proofs and all three Lean modules. It rebuilt
all eighteen current pages, recomputed the six groups from the complete GAP
program, rejected five altered code or Lean examples, and compiled fourteen
scoped declarations with standard axioms. It also checked small coset models
independently. The `root adoption
<../../../audit/topic-chamber/v2/root_adoption/README.rst>`_ records a separate
written proof review and adopts the stated source, visual and computational
evidence explicitly.

Seven new declarations in `TwoOrbitReflection.lean
<formal/TwoOrbitReflection.lean>`_ prove the actual reflection formula and
its compatibility with adjacency and translations. Seven declarations in
two reused modules remain compiled, with used and unused declarations
distinguished. Geometry reconstruction, retained classifications and the
six GAP groups are not complete Lean proofs. GAP's exact algorithms are
trusted for the finite example. The separate reflection program is
diagnostic validation; the uniform reflection theorem has a written proof.

From the repository root, check the copied bindings without redoing the
mathematical computations::

  python3 -B -O papers/topic-chamber/v2/check.py \
    --out /tmp/chamber-bindings --bindings-only

To replay the computations, scoped Lean proofs and PDFs, omit
``--bindings-only`` and add ``--render``. The exact tool versions and
path options are in the frozen `author instructions <README.rst>`_. Supply
``--study-root`` only when the already acquired private primary sources are
available. The command does not download them. The two historical runners
are preserved separately; the current runner executes the whole GAP program
directly. Frozen submission-status strings remain as provenance.

This edition adds no principal-source or solved-question credit. Complete
lengths and paired proof costs remain to be measured. The combined comparison
must pay for the whole common paper once within this topic and both complete
applications. Each conditional comparison assumes that common theory and
the declared program package already acquired. Independent topics pay their
own common theory in full.
