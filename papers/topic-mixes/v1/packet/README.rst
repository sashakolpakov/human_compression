F005: Intersections, mixes and regular covers
===========================================

Complete private author edition, pending distinct review. No public admission, source count or numerical factor
is claimed. This is one original in the fixed 161-paper register, not new intake.
The exact membership and primary-byte bindings are in initial_bindings.json.

Read fiber_intersections.tex first, then mix_applications.tex. The latter inputs
single_base_obstruction.tex and rooted_two_orbit_tests.tex. All common theory is
part of the eventual topic cost; earlier projective or covering papers are not
unpriced premises. The classical path characterization, symmetric-group Coxeter
presentations and cubic-toroid quotient fact are retained at their points of use.

Two corrections have complete written proofs for distinct review:

* The six-coordinate construction gives two 360-flag polytopes whose 1080-flag
  mix passes the source's single-base tests and fails elsewhere. The proof gives
  generation, local kernels, all input polytopality, symmetry, uniform local
  types, and explicit witness words. It directly treats Corollary 6.4 and
  Theorem 6.7; Corollary 6.6 and Proposition 6.8 use the source's operational,
  standard meaning of medial-section transitivity, correcting its contradictory
  parenthetical chain type.
* The eleven-cell and the four-simplex contradict the literal Proposition 6.9.
  Both-factor orientability, or the stated weaker first-end condition, gives a
  valid positive criterion.

The exceptional two-orbit table uses the actual embedded groups at its two
roots. Its last two rows match Corollaries 6.11 and 6.12. For Corollary 6.10 the
extra identification of the vertex variance groups is not assumed merely from
isomorphic section types. The root-explicit criterion is proved, while the
additional untransported equality is neither asserted nor declared disproved.
The smallest regular premaniplex cover of a two-orbit polytope is itself regular,
so a single correctly embedded base test supplies the full regular-cover
criterion in every class. All source correspondence qualifications are explicit.

Programs and formal scope
-------------------------

check_coprime.g is the complete required finite certificate for the two literal
regular input markings and their failed mixed intersection. GAP's subgroup
arithmetic is trusted here. The group-product argument after those inputs is
written in full.

check_single_base.py is a complete bounded validation of the written
six-coordinate proof, including every input subset intersection, all mixed-end
intersections and the displayed actual automorphisms. It is not used to
extrapolate a uniform theorem.

FiberIntersections.lean proves the actual arbitrary-group-action fiber theorem
and its equivalence in two declarations. It does not formalize polytopality,
normalizer identifications, the finite constructions or all source hypotheses.
No end-to-end formal verification is claimed.

The explore_*.py/.g files are private discovery scratch work. They are not final
proof dependencies and will not be exported as required code. In particular the
regular twelve-flag diagnostic is not a claimed literal Corollary 6.10
counterexample. The three final source problems remain outside this recovery.

Replay and complete boundary
----------------------------

Run from this directory with an unused output directory::

  /Users/sasha/.venvs/global/bin/python -B -O check.py --study-root /Users/sasha/medusa/research/leemans --out /private/tmp/F005_fresh --render

The packet is copyable without discovery files. Supply the two external primary
files at their relative paths under --study-root and the pinned Lean packages;
--gap, --xelatex, --lean and --packages permit explicit tool locations. No primary
text or font is exported. check_integrity.py supplies three separate corruption
controls against a frozen copy. Both drivers are operational files, distinct
from the one required GAP certificate and the complete Python validation file.

The written boundary is the entire five-page common paper and eight-page
application, with the complete four-page code appendix as a separate executable
representation. These are page counts, not measured proof costs or ratios.
scope.json has 35 result/background rows and three separately excluded problems,
with 15 exact proof contexts. Those contexts are evidence locators, not exclusive
weighted cost ownership. The initial corpus-pointer hashes are historical
observations; no claim is made that a moving public pointer remains unchanged.
