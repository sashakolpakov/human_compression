Explicit Suzuki rank-four construction
======================================

This author packet gives a complete proposed counterexample to Theorem 1.1
of Spiga, arXiv:2010.04080v1 (8 October 2020): a chiral polytope of type
{31,31,25} with automorphism group Sz(32768). It awaits distinct review.
No original, conjecture, Lean or measurement credit is granted by this packet.

Read rank4_counterexample.pdf in full. The subgroup classification, standard
Suzuki coordinates and Schulte--Weiss reconstruction theorem are retained
inputs. Their roles and exact supplied editions are identified in the paper
and dependencies.json. The explicit rotations, field arithmetic, two-face
intersection argument and source comparison are the present contribution.

Replay using the project's Python environment::

  /Users/sasha/.venvs/global/bin/python check.py \
    --study-root /Users/sasha/medusa/research/leemans \
    --out /absolute/path/to/a/new/replay/directory --render

The arithmetic program reconstructs the field and every matrix from the
printed formulas, without using discovery output, a torus enumeration,
GAP, or a precomputed group. It also reconstructs a conjugator taking abc
to J and changes to the Wilson basis used in the source. The resulting
symmetric matrix satisfies the correct Suzuki equations but violates the
source's equation (13), which arose from an inadmissible pair of vectors.

The diagnostic that found the example is retained separately under
reboot_20261013/f003/equal_face32_full_probe.*. It considered one finite
ambient field and a fixed split middle element. Its completeness is not a
premise of this packet. Previous attempts at a uniform two-trace descent
lemma are superseded: the explicit example falsifies that proposed lemma.
All older bounded accepted packets remain unchanged.
