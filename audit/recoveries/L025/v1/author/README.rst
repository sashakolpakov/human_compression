L025: cycles in incidence graphs
================================

This is a complete principal-recovery candidate for the fixed seventeen-page
edition arXiv:2108.06636v1 by Gabriela Araujo-Pardo and Dimitri Leemans.
Independent scientific acceptance is a separate record. No original is
credited by this author packet.

Read cycles_in_incidence_graphs.pdf (seven pages), the whole retained common
paper retained/common/cages_and_planes.pdf (five pages), and the whole
retained/odd_cycle/odd_cycle_bound.pdf (three pages). The source_map.json
gives 41 dispositions, including explicit corrections, retained background,
and the three separate question records. The source's auxiliary rank-three
geometry is replaced as a proof device; this packet does not recover its
classification as a further principal result.

The source constructions and hexagon argument retain their attribution.
The shared incidence theory is reused from the accepted L013 work. The
Suzuki matrix proof, audit and partial Lean certificate are earlier project
work, retained exactly and reorganized into a complete written argument.
The uniform matching count is written here. The odd-cycle bound is joint
work: rewrite_termination developed the shell argument and root supplied
the decisive first-shell matching step. Its distinct review is required.
No priority claim is made.

The graph Bq is extremal among all competitors: odd q uses parity, even
q>=8 uses the odd-cycle bound, and q=4 explicitly borrows the finite lower
bound in Goedgebeur--Jooken Table2. The q=2 endpoint is separately C8.
The two 32-vertex graphs in the fixed preprint are different. Their full
automorphism orders are 1920 and 48, respectively. The published edition
already describes two graphs; the preprint identification is not attributed
to that edition. The displayed duality of the coordinate graph needs the
field squaring written in the recovery. The appendix's general routine
needs zero-cycle edges included: K4 disjoint the cube is a counterexample
to its printed positive-only test.

Finite verification is exact: six supplied graphs, all edge cycle counts,
six uncached full automorphism searches, literal E16:C3 structure for G,
corrected coordinate automorphisms, a complete H-to-G search, and positive
and negative controls. The algorithm proofs are in the paper. The whole
accepted L013 direct_graphs.py is reused. No external graph library is
needed. The four-cage completeness theorem and the F012 degree-four
exclusion remain named external premises. Neither is rerun or claimed
independently certified here; their unrecorded costs are unknown, not zero.

Portable replay from an export-only copy::

  python -B -O check.py --out FRESH --render

The rendering option requires pdflatex and pypdf. Override --pdflatex if
needed. Add --study-root /Users/sasha/medusa/research/leemans to verify the
private source PDF hashes and the exact adjacency transcription. No whole
primary source is included in the public payload. All declared exports
are needed for exact packet integrity; source PDFs stay private.

This is unmeasured. Any later manuscript comparison charges the complete
common material and companion note in the applicable block. Validation
programs must be excluded on both sides or included on both sides under
the user's symmetric policy. Existing partial Lean proves the matrix core,
not the complete finite-field/coset/graph interface. There is no new Lean
work, source-count credit, conjecture credit or compression ratio here.
