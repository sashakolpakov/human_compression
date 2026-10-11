Marked coordinates and chiral enumeration
=========================================

Accepted complete corrected principal recovery of L028, the revised author
manuscript of Buekenhout, Leemans and Tranchida, *A new algorithm to classify
chiral polytopes with a given automorphism group*.

Read ``phase282_marked_coordinate_umbrella.pdf`` (four pages) and
``phase282_chiral_enumeration.pdf`` (nine pages). Their full TeX sources,
three complete mathematical programs and seven Lean component proofs are
in this directory. Numbered archive names preserve exact review bindings.

The current admission is
``../../../audit/topic-chiral-enumeration/v1/admission.json``. It supersedes
the pre-review candidate status in the unchanged author packet. This adds
one original; measurement remains pending. The catalogue remains fixed
at 161 titles and all accessible originals stay in the programme.

The recovery covers connected symbols in every rank and distinguishes
oriented from unrooted isomorphism; duality is not quotiented. The source
prefix substitution and search idea are attributed to their authors.
Schulte–Weiss reconstruction and the Liebeck–Shalev bound are retained
inputs. Historical timings are not reproduced. The fourteen-page revised
author edition is the principal source; journal typesetting is unavailable.

Reproduction
------------

The public packet contains the complete author checker and package pins::

  python -B -O phase282_check.py --out /fresh/output --gap /path/to/gap \
    --lean /path/to/lean --packages /path/to/pinned/packages \
    --xelatex /path/to/xelatex

Without ``--verify-primary`` it needs no primary PDFs. Lean verifies actual
subgroup-coordinate and reflection algebra, not the full geometry or search.
The independent reviewer freshly ran all finite and formal checks and also
implemented native rotation-pair searches for three affine groups. Root
replayed that review checker with its ten controls before adopting the result.
