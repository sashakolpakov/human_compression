Symplectic flags in string generating sets
==========================================

One endpoint criterion excludes every string generating set of rank at
least five with a specified pair of endpoints. The argument uses invariant
subspaces in a six-dimensional symplectic representation. It replaces a
separate centralizer or commutant calculation for each second generator
when its endpoint hypotheses hold.

The complete `manuscript <endpoint_images.tex>`_ and
`independent hand review <provenance/hand_review.rst>`_ are exact copies of
their frozen sources. The `publication record <provenance/publication.json>`_
records their hashes, the origin of the supplied matrices and the precise
limits of this written-theory package. The manuscript has not been compiled
for this publication; no PDF or machine verification is supplied here.

The mathematical statement
--------------------------

Let V be six-dimensional over a field of characteristic two, with a
nondegenerate alternating form. Let A and E be symplectic involutions and put

.. math::

   N=A-I,\qquad M=E-I,\qquad P=\operatorname{im}N,
   \qquad U=\ker M.

Assume that rank N = 2, rank M = 3 and NM = 0. Every string marking
``t_0,...,t_(r-1)`` with r at least five, first mark A and last mark E,
generates a subgroup stabilizing P or U. Here a string marking consists of
involutions whose nonadjacent terms commute; the intersection property is
not required.

Consequently, if a representation of an original group has these endpoint
images, and its image contains an element escaping P and an element escaping
U, no such marking generates the original group. The two escaping elements
may be the same. Faithfulness is unnecessary. Escape from both alternatives
is essential: escape from only one space does not suffice.

The key step concerns the second mark B. If B preserves P, every mark does.
Otherwise the restriction of B-I to the three-dimensional Lagrangian U has
rank one. The joint fixed plane of A and B then spans U together with P.
The penultimate mark preserves these two planes, while the other marks
preserve U by their string relations. This proves the second alternative.

The manuscript also describes a conditional extension in dimension 2m.
As the independent reviewer notes, take m at least two when P is required
to be proper and nonzero; the additional rank bound on the restriction of
B-I must be assumed there. The six-dimensional theorem needs neither
qualification beyond its stated hypotheses.

The retained example and its premises
--------------------------------------

The `endpoint data <data/endpoints.json>`_ contains the exact matrices A and
E for retained family 4. In the acquired GF(8) exponent codec, code 0 means
zero, code 1 means one and code i means zeta raised to i-1 for 1 <= i <= 7.
Thus code 2 is not the integer scalar two. The form has antidiagonal Gram
matrix J; vectors are columns.

The field is reused from `common_commutant/data/codec.json
<../common_commutant/data/codec.json>`_. Its two ambient matrices D,C are
reused from `common_commutant/data/matrices.json
<../common_commutant/data/matrices.json>`_. Static comparison found these
entire JSON values equal to the corresponding values in the retained
family-4 member certificate. The endpoint values in that public file belong
to branch 621 and are different: they must not be substituted for the pair
in this package.

For the supplied family-4 pair, the manuscript proves symbolically that
P = span(e1,e2), U = span(e1,e2,e3), the endpoint ranks are two and three,
and NM = MN = 0. It also proves that D and C preserve J, and that
C e2 = e3+e4 lies outside both P and U. These are written identities,
not results of a new finite-field computation during publication.

The finite application retains the following original premises:

* the named original group and its well-defined representation in this
  acquired field and common basis;
* genuine original membership and transport of the two endpoints to A,E;
* genuine original ambient generators whose images are D,C and generate
  the entire represented image;
* for a catalogue application, the exact mapping of each original job to
  this first/last pair, including any whole-marking automorphism transport.

The theorem does not require a linear representation of the full
automorphism group. A group automorphism may first transport the whole
marking; generation and string relations are preserved. Columns in this
argument are not being identified with points of an original permutation
action. The historical group model, membership and transport protocols
have not been rerun or reproduced by this package.

Attribution and relation to earlier work
----------------------------------------

The associated original is Malcolm Hoong Wai Chen, *Abstract regular
polytopes of G2(q) in even characteristic*, arXiv:2609.25004v1 (2026),
catalogue identifier F004. Its original results, enumeration and group
data retain their attribution. This note does not reprove the entire paper.

Adjoints of isometries, orthogonal complements, rank-nullity for square-zero
maps, and invariance of images and joint kernels under commuting maps are
standard linear algebra. The project's contribution here is their combination
into the P-or-U endpoint criterion and its application to the retained pair.
No historical-priority claim is made. The frozen manuscript was authored by
``/root/f004_uniform_prefix_theory`` and independently reviewed by
``/root/f004_flag_proof_review``. This publication adds organization and
portable references; it adds no new mathematics.

The `common commutant method <../common_commutant/README.rst>`_ and
`canonical fixed-vector theorem <../common_commutant/fixed_vectors.tex>`_
give related obstructions. They remain useful when these endpoint rank
conditions fail. The fixed-vector theorem is not needed in this proof;
the manuscript includes its own elementary lemmas. No extra shared theory
or computation is charged or credited by publishing these links.

Review and replication boundary
-------------------------------

The copied review supports the abstract theorem and its conditional matrix
application. It is an independent hand review, not Lean formalization or
an executed application certificate. Its ten eligible rank-five jobs are
a historical snapshot, distinct from twenty original pair rows and seventeen
active acquired rows. Those statements are preserved as history, not asserted
as today's pending count. This publication changes no ledger or acceptance.

A reader can inspect the complete proof, its review, the supplied endpoint
values and the linked field and ambient values without the private study
tree. The publication record uses paths relative to this package and pins
their exact bytes. Unbundled historical model and acceptance records are
identified by role and hash as imported premises, not presented as working
local links or as freshly reproducible acquisitions. To retain all linked
public material, use the repository checkout or keep both sibling directories
``symplectic_flags`` and ``common_commutant`` together.

The existing common-commutant checker concerns its earlier numerical example.
It does not verify this endpoint theorem or accept this family-4 application.
No checker, group operation, application, control suite, guard, probe, test,
Lean run or TeX compilation was executed or added for this publication.
Paper, original, conjecture, compression and Lean counts remain unchanged.
The result does not settle Question 4.1, cover all endpoint types or complete
F004, and no whole-manuscript compression ratio is claimed.
