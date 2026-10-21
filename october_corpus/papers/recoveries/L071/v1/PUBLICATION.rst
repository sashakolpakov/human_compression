Regular polytopes with a fixed automorphism group
================================================

This collection recovers the principal mathematical results of Dimitri
Leemans and Mark Mixer, *Algorithms for classifying regular polytopes
with a fixed automorphism group*, Contributions to Discrete Mathematics
7(2) (2012), 105--118. The `published source
<https://cdm.ucalgary.ca/article/download/62152/46746>`_ has fourteen
pages. Its results retain their original attribution.

The common search theorem enumerates ordered generators using stabilizers
of the generators already chosen. Its proofs explain why every permitted
extension is considered once, why the intersection test is sufficient, and
why the search terminates. The applications acquire those complete proofs
and retain the actual finite computations.

The recovered results are:

* The `criterion for permutation actions
  <compatible-actions/compatible_actions.pdf>`_ identifies exactly when
  coloured graph isomorphism detects abstract isomorphism. The normalizer
  of the chosen action must induce every automorphism of the group.
  Separate embeddings of the group and its automorphism group are
  insufficient; an explicit Klein-four example establishes the distinction.
* The `four alternating classifications
  <alternating-groups/alternating_censuses.pdf>`_ reproduce the complete
  rank tables for A11, A12, A13 and A14, including every unlisted zero.
* The `Conway-group classification <conway-group/co3_census.pdf>`_
  reproduces all 22,908 ordered classes for Co3 and all 824 printed
  table cells.
* The `remaining finite classifications
  <finite-classifications/remaining_censuses.pdf>`_ recover all twelve
  benchmark rows and the eleven ordinary sporadic groups through Held,
  with the Tits group stated separately. For H3 = A5 x C2 the unrestricted
  answer is eleven classes after identifying duals: eight connected
  rank-three classes and three disconnected rank-four classes. The
  source's eight counts precisely the connected subfamily.
* The `comparison with the original lists
  <finite-classifications/source_orbit_comparison.pdf>`_ gives explicit
  isomorphisms and conjugating permutations matching all 6,047 original
  Hartley--Hulpke markings with independently enumerated classes.

The standard polytope correspondence, classical group facts and exact GAP
operations remain stated inputs. The stabilizer method and the original
lists retain their attribution to earlier work. Our contribution here is
the explicit common correctness argument, the action qualification,
complete retained executions, and the correspondence between the actual
old and new markings. The full H3 and Suzuki predecessors are acquired
for the two reused benchmark rows.

The `source audit <../../../../audit/recoveries/L071/v1/scope_routes.json>`_
records all fifteen dispositions. Historical running times and memory
figures remain attributed observations. The general alternating-rank
conjecture and suggested future algorithms receive no new solution credit.
No compression factor or complete Lean verification is claimed here.
