Common commutants: one witness for an entire prefix
=================================================

A matrix X commuting with every candidate generator, but not with one known
ambient generator, proves that the candidates generate a proper subgroup.
This package gives the complete argument and the actual branch 621 witness,
using only Python's standard library. See THEORY.rst for the general lemma,
the subgroup version, the structural center argument and precise attribution.

The numerical package contains the actual GF(8) codec, 21 ordered 6x6 member
images, two original ambient images, two complete K/H tables of 512 elements,
and the supplied X with a nonzero ambient commutator entry. The checker
verifies the 12 original synthetic controls, all field axioms, complete
finite image groups and involutions, all 21 commutations and the
original-generator escape. It uses exact borrowed definitions, with explicit
source spans and hashes. Only Python's standard library is required.

`Commutation constraints and affine matrix witnesses <COMMUTATION_CONSTRAINTS.rst>`_
gives a further general theorem. It replaces full group centralizers with
matrix double commutants, applies to fixed triples in every string rank at
least five, and makes the normalized witness spaces additive torsors. Its
`written review <provenance/commutation_constraints_review.rst>`_ records the
precise scope. The numerical example here uses the earlier K/H method.

`Canonical fixed vectors in characteristic two <fixed_vectors.pdf>`_
(`TeX source <fixed_vectors.tex>`_) gives another criterion. A self-adjoint
operator determines a canonical vector fixed by every linear isometry
commuting with it. This can replace both a centralizer-order calculation
and a rank-one search with linear equations. The complete proof and
`independent written review <provenance/fixed_vectors_review.rst>`_ state
the required form, original-group correspondences and moved-vector test.
This is a conditional theory: no additional corpus instance, completed
original or compression measurement is claimed by the note.

To compile the note, run ``pdflatex -no-shell-escape -halt-on-error`` on
``fixed_vectors.tex``, with the output directory outside this package.

Reproduce from an isolated copy
-------------------------------

Use Python 3.9 or newer. Copy this directory by itself, or clone the repository,
and run the following from this directory. Results must be outside the
package; the entrypoint refuses to overwrite files or write into the package.

.. code-block:: sh

   package_dir="$(pwd -P)"
   result_dir="$(mktemp -d "${TMPDIR:-/tmp}/common-commutant.XXXXXX")"
   result_dir="$(cd "$result_dir" && pwd -P)"
   python3 -I -B -S "$package_dir/check.py" --out "$result_dir/result.json"

A successful check reports 12 controls, field order 8, 21 member images,
group orders [512,512], nonidentity involution counts [511,119],
60,809 raw image pairs and a verified escape. The actual escape is at
generator 2, entry (row 1, column 4), with field codes 3 and 0.

To run only the real retained synthetic controls:

.. code-block:: sh

   python3 -I -B -S "$package_dir/check.py" --controls-only \
     --out "$result_dir/controls.json"

Both commands passed from an isolated copy under the existing resource
guard. The full check took about 0.20 seconds and peaked below 28 MiB RAM.
The `verification record <provenance/verification.json>`_ gives the tested
snapshot and hashes of the unchanged checker and data. The later additions
are written theory, reviews and documentation.

Scope and retained premises
----------------------------

The checker proves finite field/matrix/table/witness facts about the INCLUDED
data. The original representation and generator correspondence, and equality
of the original K/H bases with FULL original centralizers, remain explicitly
retained premises. No small arithmetic package can establish these merely
by checking matrices. The package therefore does not reproduce a named G2(8)
acquisition or the full original manuscript. See
provenance/retained_premises.json and THEORY.rst.

Under those retained correspondences, the common witness excludes ALL
completions of the original prefix 621. The 60,809 raw involution pairs are a
complete superset of the candidates. The method avoids checking
the pairs separately; it does not claim a measured manuscript compression
ratio, an open-conjecture solution, historical novelty or Lean verification.

Attribution and contents
-------------------------

The associated original manuscript is Malcolm Hoong Wai Chen, Abstract
regular polytopes of G2(q) in even characteristic, arXiv:2609.25004v1 (2026).
Its results and enumeration are credited to their original author. The
elementary commutant/center lemmas are standard; the project's specific
uniform application and its borrowed implementation are distinguished in
THEORY.rst and provenance/origins.json.

arithmetic.py, commutant.py and controls.py contain ONLY the selected used
definitions from the genuine project Sources. The small nonexecuted whole
Source text archive in provenance/source_derivation.json makes their origin
hashes and extraction spans independently checkable. The new check.py and
the explanatory manuscript are the portable additions. data/ has only the
necessary field, matrices, finite tables and actual witness. SourceManifest.json
checks the local file set and hashes; it is consistency evidence, not a
signature proving an original-group acquisition. Historical proof hash
references remain provenance and are not portable execution receipts.
