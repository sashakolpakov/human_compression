Forty-six chiral markings in PSU(4,2)
====================================

The two-page proof establishes at least 46 ordered chiral marking classes
of rank 3 in PSU(4,2), represented as PSp(4,3). Table 6 of Hartley, Hubard
and Leemans, Two atlases of abstract chiral polytopes for small groups,
Ars Mathematica Contemporanea 5 (2012), 371--382, prints 26. The comparison
uses the source's own convention: Section 4 classifies ordered generator
tuples, and Section 6 retains both enantiomorphic forms. Neither duals
nor mirror pairs are identified here.

This is a correction to a published finite count. It is not an answer
to an open conjecture, a claim of historical priority, or a complete
treatment of the atlas. In particular,46 is proved as a lower bound;
exhaustion of the search that supplied the tuples is not a premise.
The original source file was checked against SHA256
093b28ebbaeff1c9299d272550cc7d0e308fb34350e999155dde624888d5596c.

Verification
------------

From this directory, with an absolute fresh output directory::

    python3 validate_u42.py --out /tmp/u42-validation

The validator uses only Python's standard library and explicit finite
permutations. It reconstructs the group, verifies 92 admissible chiral
tuples, and partitions them into 46 classes. It stores 92 reflection
relations, 118 failed comparison relations and 46 successful automorphism
transports. The latter verify every edge of a 25920-vertex Cayley graph.
The two literal input files are inputs/group.json and inputs/markings.json.

The separate named-model check requires GAP::

    gap -q -b verify_model.g

It checks that the supplied generators generate exactly the same permutation
subgroup as GAP's standard PSp(4,3) constructor, not just a group of its order. The recorded execution
used GAP 4.15.1. The exceptional identification PSp(4,3)=PSU(4,2) and the
standard symplectic constructor are retained mathematical/software inputs.
A future constructor using different labels would need an explicit
isomorphism; the present script deliberately rejects a label mismatch.

Attribution and scope
---------------------

Geometric recognition is borrowed from E. Schulte and A. Ivić Weiss,
Chiral Polytopes, DIMACS Series 4 (1991), 493--516; the exact rank 3
hypotheses used here are stated in the proof. The finite traversal of a
Cayley graph is an elementary homomorphism test, not a new general
reconstruction theorem. The contribution here is the concrete family,
its relation witnesses and the correction under the source convention.

The written proof and finite checker were independently reviewed before
publication. The public proof and mathematical input files are byte-identical to that
reviewed edition. Only the two input paths in the checker have changed. The publication record identifies
the original author and review manifests and records their limited scope.
Their full historical dependency logs remain working evidence; they are
not required to run this self-contained finite permutation check. The
geometric recognition and named-model interpretation remain attributed
inputs. There is no new Lean proof or compression measurement here.
