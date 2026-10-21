Recognizable extensions and finite normal pairs
===============================================

Read the five-page `common theory <umbrella.pdf>`_ and the five-page
application `Finite normal pairs as incidence geometries
<finite-normal-pairs.pdf>`_. Their editable sources are TeX. The separate
four-page `validation appendix <program-appendix.pdf>`_ prints both complete
programs; the Lean files and their exact scope are included.

The source is Antonio Díaz Ramos, Rémi Molinier and Antonio Viruel,
*Every finite group is represented by a finite incidence geometry*,
`arXiv:2511.02410v2 <https://arxiv.org/abs/2511.02410v2>`_, 16 December 2025,
thirteen pages. It entered the existing corpus as an independent followup
source. Its authorship is not attributed to another research group.

The mathematical idea
---------------------

Extending the symmetries of a graph does not by itself determine the full
symmetry group of the extension. We first recognize the old vertices inside
the new graph. Restriction then gives an actual homomorphism between the
permutation groups. If fixing the old vertices fixes the whole extension,
restriction is injective. If every old symmetry has an extension, it is
surjective. A compatibility condition identifies the distinguished subgroup
of automorphisms that preserve each color.

The common paper proves these statements and a criterion that recognizes
components from their boundary vertices. It supplies complete proofs of
the source's chamber completion and cleaning constructions. The application
then pays for the explicit encoding of a finite normal pair, its graph
recognition, and every step of the recursive symmetric-group example.

The source constructions, representation theorem and symmetric family
remain attributed to Díaz Ramos, Molinier and Viruel. The restriction
principle is elementary group theory. Our contribution here is the common
proof organization, complete local arguments, explicit corrections and
scoped formal verification. This edition reuses earlier accepted project
proofs without claiming them again as new mathematics. Frucht and König
are historical antecedents; no external representation theorem is left
as an unproved premise.

.. list-table:: Exact source contract and current proofs
   :header-rows: 1
   :widths: 20 53 27

   * - Source result
     - Current derivation
     - Qualification
   * - Theorem 3.1
     - Ordered-pair graph; recognition of its vertices and directed labels;
       right translations; exact correlation and color-preserving groups
     - Finite group and normal subgroup; all construction hypotheses checked
   * - Theorem 4.1
     - Every clique extends to a chamber; old vertices are recognized by
       degrees; restriction and unique extension preserve the group pair
     - Correct degrees are r-1 and d(v)(r-1)
   * - Theorem 4.2
     - The full cleaning gadget, palette recognition, local rigidity and
       extension; triangle-freeness and minimum degree
     - Includes isolated vertices and the smallest gadget; cleaning
       preserves components rather than creating connectedness
   * - Theorem A
     - Apply chamber completion to the explicit encoding; prove
       connectedness and rank, with the trivial group treated separately
     - Nontrivial rank [G:H]+3; no universal rank-two assertion
   * - Example 5.1
     - Compute both full hexagon symmetry pairs and exhibit the reflection
     - Completed pair is (D12,S3), where D12 has order twelve
   * - Example 5.2
     - Full recursive construction; genuine symmetric-group action;
       palette sizes, recognition of the top class and faithfulness
     - Minimum degree two starts at n=3; the n=2 path has leaves

These six blocks are mapped to thirteen written proof or scope passages
in `scope.json <scope.json>`_. The source's Question 2.4 was answered by
its own Theorem A and earns no new solved-question credit here. Claims of
optimal graph size, optimality of every completion hypothesis, and a
universal identification with (Aut(A_n),Inn(A_n)) are excluded.

Verification and costs
----------------------

The `independent review <../../../audit/topic-representation/v2/independent_review/README.rst>`_
read the complete source and both current papers. It checked the two whole
programs, actual Lean statements and all fourteen rendered pages. A separate
small graph enumerator checked both hexagon pairs and the delicate isolated
vertex and recursive base cases. These finite checks support the review;
the uniform theorems have written proofs independent of those samples.

`RecognizableRestriction.lean <formal/RecognizableRestriction.lean>`_ has
eight new generic declarations. It derives the restriction homomorphism
from an injective embedding and action compatibility, proves the kernel
and extension criteria, and transports the distinguished subgroup.
`CompletedHexagonCounterexample.lean <formal/CompletedHexagonCounterexample.lean>`_
retains four previously verified local facts about the reflection and C3.
All twelve declarations were freshly compiled with standard Lean axioms.
The concrete graph hypotheses, chamber and cleaning constructions,
component lemma, recursive induction, full hexagon group orders and
universal finite-pair theorem remain written mathematics.

The `root acceptance <../../../audit/topic-representation/v2/root_adoption/README.rst>`_
adopts that review and records a fresh bounded replay. The original review
and a separate correction of its agent-author label are both preserved;
the correction changes no mathematics or verdict. Frozen candidate-status
strings describe the original submissions, not the current acceptance.

For a fresh binding and rendering check, from the repository root::

  python3 -B -O papers/topic-representation/v2/check.py \
    --out /tmp/representation-render --render --xelatex /path/to/xelatex

Add --programs and --formal to rerun the bounded GAP validations and local
Lean compilation. Tool versions and --lean/--packages options are specified
in the frozen `author instructions <README.rst>`_. Two historical drivers
are supplied separately; their joint historical bindings are not required
by the current portable command.

The complete common paper, application and both full programs remain
available for measurement. Each independent topic pays its own whole common
theory. This publication admits no compression ratio; the combined and
individual comparisons require a separate length audit. It adds no source
or solved-question credit to the fixed corpus.
