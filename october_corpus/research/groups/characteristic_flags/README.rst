Characteristic vectors and endpoint geometry
=============================================

A string marking of rank at least five in a six-dimensional symplectic
space is reducible when both endpoint involutions have rank three after
subtracting the identity. The `complete manuscript <characteristic_flags.tex>`_
proves this through a common Lagrangian or a nonzero fixed characteristic
vector. It requires no enumeration of completions or second-generator
centralizer.

The manuscript is the exact corrected edition reviewed in the
`independent hand review <provenance/hand_review.rst>`_. Both files retain
their original bytes. The `publication record <provenance/publication.json>`_
pins them, the borrowed theory and the initial edition. This package supplies
written mathematics; no compilation or computational verification was run.

The theorem and the generation obstruction
-------------------------------------------

Let k be a **perfect** field of characteristic two, V a six-dimensional
k-space and beta a nondegenerate alternating form. Let
``t_0,...,t_(r-1)`` be k-linear symplectic involutions, where r is at least
five and nonadjacent marks commute. Put A = t_0, E = t_(r-1) and assume
rank(A-I) = rank(E-I) = 3. Set P = im(A-I) and U = im(E-I).

* If P = U, every mark preserves this common Lagrangian.
* If P differs from U, the entire marking fixes either c_A or c_E
  pointwise; both characteristic vectors are nonzero.

No intersection property is needed. For a representation of an original
group, nongeneration follows if its image escapes the resulting stabilizer.
The equal-image branch requires an ambient element moving the common
Lagrangian. The distinct-image branch requires ambient elements moving
each of c_A and c_E; these elements may differ. Faithfulness is unnecessary.

In the distinct-image branch, an ambient element D with D-I invertible
supplies both vector escapes. The diagonal matrix with field codes
``2,7,3,6,2,7`` in the existing
`ambient data <../common_commutant/data/matrices.json>`_ has this property
under the `acquired codec <../common_commutant/data/codec.json>`_, whose unit
is code 1. Its use for a proposed endpoint family still requires genuine
original ambient membership and correspondence to the same model. It does
not supply the separate Lagrangian escape in the equal-image branch.

Borrowed theory and the additional argument
--------------------------------------------

The characteristic-vector construction and coordinate formula come from
Theorem 1 of the existing project note
`Canonical fixed vectors in characteristic two
<../common_commutant/fixed_vectors.tex>`_. For a self-adjoint operator T,
its vector w(T) belongs to im T and satisfies

.. math::

   \beta(x,w(T))^2=\beta(x,Tx),\qquad
   w(T)=J^{-1}\sqrt{\operatorname{diag}(JT)}.

This is borrowed project theory, not claimed again as a new result.
Wall forms, adjoints, square-zero rank bounds and Cayley--Hamilton are
standard ingredients. The additional argument combines their geometry
with the string relations. If the second mark moves c_A, a degree-two
polynomial in AB expresses c_E using three translates of c_A. The
penultimate mark therefore fixes c_E, as do all the other marks.

The manuscript also gives a sufficient prefix criterion: if a self-adjoint
T in k[A,B] has w(T) = c_E nonzero, the entire marking fixes c_E.
In the moving branch of the main theorem, an explicit witness is

.. math::

   T_i=(AB)^i(A-I)(AB)^{-i}\quad(i=0,1,2),\qquad
   T=\frac{T_2+\tau^2T_1+T_0}{(a\tau)^2}.

The scalars a and tau are defined in the manuscript and are nonzero in
that branch. The squared coefficients and denominator are part of the
formula. One exact word expression and the stated linear identities suffice;
a failed search over an incomplete word list gives no negative conclusion.

The earlier `symplectic-flags criterion <../symplectic_flags/README.rst>`_
treats endpoint ranks two and three with zero nilpotent product. This note
treats two maximal endpoints. Its mixed-rank discussion identifies a
Lagrangian configuration but does not prove that all marks preserve it.
Neither criterion establishes its hypotheses for every remaining family.

Source attribution and the corrected edition
---------------------------------------------

The associated original is Malcolm Hoong Wai Chen, *Abstract regular
polytopes of G2(q) in even characteristic*, arXiv:2609.25004v1,
21 September 2026 (catalogue F004). The positive mixed-rank construction
uses the source's Section 3 parameter conditions and displayed matrices.
Its generation and C-string property are **imported from Theorem 1.1**,
not reproved here. Original results and model data retain their attribution;
no historical-priority claim is made for this note.

That source example uses rows in the stated six-dimensional quotient basis.
The rest of the manuscript uses columns. The conversion for an entire
representation is the contragredient ``g -> rho_row(g^-1)^T``; plain
transposition is sufficient only on the involution marks. Coordinate
subspaces must also be transported. The named group, membership and
semilinear transport premises are not supplied by a matching matrix shape.

The initial manuscript incorrectly described the fourth source generator
as antidiagonal. Edition v2 gives its correct permutation
``(1 6)(2 4)(3 5)``. It also replaces an unintended equivalence concerning
nonzero coefficients by the implication actually used. These two changes
leave the main theorem and proof unchanged. The initial manuscript and
provenance retain their separate hashes in the publication record; no Git
commit is known for that unpublished initial edition. The copied review
is bound to v2 and has not been silently rewritten.

The mathematical author is ``/root/f004_uniform_prefix_theory``, the
corrected-edition editor is ``/root``, and the independent hand reviewer is
``/root/f004_flag_proof_review``. This package adds portable organization,
not a new mathematical result or a second review.

Projective counts and application limits
-----------------------------------------

For an actual linear involution on **all** projective lines of an
n-dimensional space over an even finite field, the manuscript proves
the fixed-line formula ``(q^(n-rank(s-I))-1)/(q-1)``. In dimension six over
GF(8), it gives 73 fixed lines for rank three and 585 for rank two.
Two commuting rank-three endpoints have 73 common fixed lines when their
image Lagrangians coincide and nine when they differ. The full projective
degree is 37,449.

These are conditional mathematical values, not newly acquired counts for
remaining original families. A permutation action of degree 37,449 does not
by itself identify the action on all projective lines. Any such application
requires an explicit equivariant identification for the same original group
and representation, followed by the actual counts or endpoint matrix facts.

The original group, representation, field, form, common basis, ordered
endpoint membership and ambient escapes remain application premises.
No remaining pair ranks, point correspondences, family coverage or completed
original jobs were acquired here. This note does not finish F004 or settle
an open conjecture.

A repository checkout provides the proof, review and linked earlier theory.
The publication record uses relative paths for public files; historical
local inputs are identified by role and hash rather than broken host links.
The source path printed in the frozen bibliography is an archival identifier;
the original extracted source is not bundled in this package. Its identity
and the borrowed source claims remain explicit in the publication record.
The existing common-commutant checker does not verify this theorem.
No checker, program, test, application, guard, probe, Lean run or TeX build
was added or executed. Original, paper, conjecture, compression and Lean
counts are unchanged.
