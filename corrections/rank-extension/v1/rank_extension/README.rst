Rank and degree extension: disconnected counterexample
=====================================================

Theorem 6.4 of Cameron--Fernandes--Leemans, arXiv:2212.12723v2
(11 January 2023), allows intransitive inputs. The complete three-page proof
here gives a rank-four C-marking on nine points satisfying every printed
hypothesis, whose prescribed rank-five extension fails the intersection
property. The old group is S5 x C2 x C2; two short words on disjoint new
label pairs give the same central transposition.

The standard end-parabolic criterion is retained and attributed precisely.
The five needed subgroup descriptions and all three end intersections are
proved in the manuscript. GAP is a diagnostic, not a premise of that proof.
No Lean formalization, full L019 recovery, open-question answer, historical
priority or numerical comparison is claimed. The main transitive stability
theorem and the valid forward endpoint theorem used in L010 are not refuted.
The separate Proposition 2.4 packet remains immutable.

Replay from this packet and the existing private source PDF::

  python -B -O check.py --study-root /path/to/leemans --out /fresh/path \
    --gap /path/to/gap --render --xelatex /path/to/xelatex

The checker uses explicit exceptions, works under python -O, reruns all
256 old and 1024 new intersections and the literal source hypotheses,
rejects three damaged examples, and rebuilds all three manuscript pages.
Primary PDF/text and raster images are not exported. XeLaTeX needs
STIXGeneral and STIX Two Math. The finite diagnostic trusts installed GAP;
the complete written proof requires no finite computation.
