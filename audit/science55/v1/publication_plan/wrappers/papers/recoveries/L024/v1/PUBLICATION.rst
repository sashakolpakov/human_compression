Real Schur index two: corrected principal recovery
=================================================

The complete `five-page paper <schur_characters.pdf>`_ and its
`native TeX <schur_characters.tex>`_ recover the principal existence results of
P. J. Cameron, A. Herman and D. Leemans, *String C-groups with real Schur index 2*,
arXiv:2201.01313v1 (six pages).

An explicit marking of PSU(5,3) gives a string C-group whose vertex permutation
character contains every nontrivial irreducible constituent, including five
with Frobenius--Schur indicator minus one. The intersection property is proved
in writing from the adjacent dihedral groups, product orders and full
generation. Standard character orthogonality bounds reduce positivity to a
short table. A separate argument gives the corrected infinite-family statement:
the source's dimension-three case is false, the dimension-six existence is a
retained classification input, and the stated higher-dimensional theorem is
used only in its valid range.

The `13-route source map
<../../../../audit/recoveries/L024/v1/author/source_map.json>`_ explicitly retains
three limits. The unspecified historical run producing 36 markings is not
reproduced; the introductory global-minimality wording is not proved; and the
informal suggestion of polytopality throughout the infinite family remains
unproved. These limits do not erase the principal existence conclusions. This
is a corrected principal recovery, not an assertion that the original and
replacement theorem sets are equivalent.

The `scientific admission <../../../../audit/recoveries/L024/v1/admission.json>`_
links root's author packet, enumeration_volume's distinct mathematical review
and root's adoption. The full
`GAP program <../../../../audit/recoveries/L024/v1/author/verify_schur_example.g>`_
is required for group generation and character calculations. Its 64 intersection
checks corroborate the written proof; the whole program remains included in the
inventory. The `saved output
<../../../../audit/recoveries/L024/v1/author/schur_example_report.txt>`_ and
`retained-input record <../../../../audit/recoveries/L024/v1/author/dependencies.json>`_
state the GAP/character-table versions and trust boundary. There is no generator
search. Permutation stabilizer chains use the explicitly asserted option
``random=1000``, which requires exact verification while allowing internal
random construction.

This recovery is unmeasured and creates no comparison topic. Literal GAP
commands in the source must be addressed symmetrically in any later input
audit. Historical software and external proof costs are unknown, not zero.
There is no new source-question answer, historical-priority claim or Lean claim.

Publication bindings and the complete frozen packets can be reconstructed
without a new finite computation::

    python3 audit/science55/v1/publication_plan/replay.py --repo . --out /tmp/science55-replay

The ``--render`` option rebuilds the accepted native papers. No source PDF or
third-party source text is redistributed. The separate distinct-review code is
preserved for an explicitly requested mathematical replay; it is not silently
run by this publication check.
