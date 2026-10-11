Independent review of Topic B
=============================

Accepted for the thirty declared source clauses, with the additive C10/C11
proof-map correction. The original author packet remains unchanged. This is a
review of the complete common paper and four applications, not a claim that
every statement in their four historical sources has been replaced.

The review read the complete five scientific TeX papers, their scope reader,
the actual Lean module and runner, and all available mathematical source text.
N003, N008 and the revised L030 edition were read in full. N001 was read from
its bound authored browser rendering; its original PDF remains unavailable.
Selected mathematical source pages and all twenty-four final own-PDF pages
were also inspected visually. The full source contracts and their retained
inputs are preserved, including the 1997 foundational classification and the
two distinct Whiston inputs.

The common proofs establish coset flag completion, relative generation by
residual maximality, the full intersection formula, and the weighted-forest
construction. The applications supply their own remaining arguments. In
particular, the symmetric-group classification retains its n >= 7 range and
all three counting conventions; the infinite-group Frattini argument proves
the needed relative finite-generation step; and the disjoint-subset paper
proves the uncolored graph automorphism assertion by its eigenvalue argument.
There is no unpriced reference to an archived manuscript written by this
project as a substitute for one of these proofs.

The six Lean declarations prove the actual subgroup induction, its
intersection consequences and independence. Finite type indexing is made
explicit for total generation. They do not formalize the incidence geometry,
forest construction, Frattini application, spectral argument, or any complete
source application. A fresh compilation passed with only propext,
Classical.choice and Quot.sound reported. Imported compiled dependencies are
trusted; they were not rebuilt in this review. The three weakened-hypothesis
edits were rejected, and the corresponding finite countermodels show that
the hypotheses matter mathematically.

A fresh complete replay verified the bound sources, all thirty source rows
and twenty-nine complete proof spans, and reproduced every page's extracted
text in all six PDFs. Independent finite checks used an independently built
S3 subgroup lattice and an odd-prime example with nontrivial Borel subgroup;
they corroborate the stated subgroup interface, rather than proving the
uniform theorem. All own PDFs have clean extraction with no C0 control glyph,
replacement character or private-use character. A detached proof-end square
at the start of umbrella page 4 is a minor presentational issue and does not
require a change to the frozen edition.

The author identified and preserved an additive documentary correction:
C10, the residue Frattini test, uses B3.Coordinates and B3.Ladder; C11, the
action-kernel result, uses B3.Frattini and B3.Quotient. The independent check
confirms that only these four new-owner/span fields changed. All source
statements, mathematical TeX, PDFs and Lean bytes are unchanged. The obsolete
swapped map is rejected by the added binding control.

Existing qualifications remain essential. N008's unrestricted
generating-set converse is corrected, while its geometric theorem retains
the declared infinite-group scope. L030 is the fixed revised institutional
edition. Its panel parameter, thin boundary and displayed 63-vertex example
have the already-recorded corrections. Correcting the full automorphism
group of that example does not disprove the existence of a different locally
Desargues graph with the source's stated group. The separately cited
Gaschütz and Archer classifications are neither re-proved nor required by
these applications. The historical C11 wording about Archer is a preserved
source-scope note, not a hidden premise of the new proof.

No new source, conjecture or principal-result credit, historical-priority
claim, or compression factor is assigned by this review. N001's missing PDF
cost remains unknown.

Reproduction
------------

Run the author replay with explicit tool locations and a fresh output path::

  python topic_B_volume/check.py --verify-primary --sources-root RESEARCH_ROOT \
    --lean LEAN --packages PACKAGES --render --xelatex XELATEX --out FRESH_DIR

Run the independent interface and binding checks separately::

  python -B -O topic_B_independent_review/finite_interfaces.py --out FRESH_JSON
  python -B -O topic_B_independent_review/check_bindings.py \
    --research-root RESEARCH_ROOT --out OTHER_FRESH_JSON

The primary documents remain private. Binding verification alone does not
replace this independent written mathematical review.
