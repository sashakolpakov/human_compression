# Integral homology of the Tomotope completion

Independent integer calculation for phase246, phase245, 10 October 2026.
This packet verifies the integral matrix supplied by the phase246 author.
It does not independently reconstruct that matrix from the primary
Tomotope incidence model. The group-theoretic interpretation belongs to
the phase246 argument.

## Input and result

The supplied cellular complex has 48 vertices, 768 edges and 18432 translated
square boundaries. Its integer boundary rows are stored, with all edge
endpoints, in `phase245_tomotope_complex.json`. Exact SHA256:

    79966a40e486e762f3d2997664bca7072612cf1cf49003481f6d8419dc81c8db

The independent checker selects a maximal tree with 47 edges. Projection
onto the 721 non-tree edges identifies the graph's integer cycle lattice
with Z^721. Indeed, each non-tree edge closes along a unique tree path,
giving an integral fundamental-cycle basis. The checker verifies that all
18432 supplied two-cell boundaries are integral cycles before projecting.

After duplicates and negatives are identified, the row lattice has 4608
generating rows. The calculation finds 719 unit invariant factors. The
remaining row lattice is exactly 2Z^2: every entry is even, and division by 2
followed by two further unit eliminations gives all of Z^2. Thus

    H_1(complex;Z) = Z/2Z ⊕ Z/2Z.

This determines every characteristic, not merely the primes tested in the
phase246 exploration. In the two surviving coordinates, indexed by original
edges 165 and 509, the supplied parallel-edge defect has image (1,0) modulo 2.

## Why the operations certify the integer quotient

At each pivot an entry +1 or −1 is selected and its row is normalized by a
sign. Integer row operations clear that column in every other row. Integer
column operations can then clear the remainder of the pivot row without
changing the other rows, since their entries in the pivot column are zero.
Removing the resulting unit row and column preserves the quotient by the
remaining row lattice. These are unimodular operations; there is no division
by a nonunit at this stage.

The checker records every pivot row, column and sign. It reduces the
specified cycle vector by the same pivot rows, so its final coordinates
represent its actual class in the quotient. Once only two columns remain,
all row entries are divisible by 2. Running the same unit procedure on their
halves proves that those halves generate the entire two-dimensional integer
lattice. This proves that the original residual lattice is exactly 2Z^2.

The computation uses Python integers and the standard library. It contains
no numerical approximation, probabilistic rank test or symbolic-system
Smith-form call. The invariant-factor result is an exact computational
certificate, not a Lean formalization of the cellular argument.

## Consequence when coupled to the phase246 identification

Phase246 identifies this complex's fundamental group Π with the kernel over
the actual Tomotope monodromy group G of the universal marked completion

    U = (A *_C B) / <<(s_0 s_3)^2>>,
    A=G012, B=G123, C=G12.

Any marked cover H→G whose restrictions to both end groups are isomorphisms
is a quotient of U, by the universal property of the amalgam and the string
commutation relation. Its kernel over G is therefore a quotient of Π.

The computed abelianization Π_ab=(Z/2)^2 has no quotient of order p for an
odd prime p. A nontrivial finite p-group always has a nontrivial elementary
abelian p-quotient, and hence a quotient of order p. Therefore Π has no
nontrivial finite p-group quotient when p is odd. If H→G had such a kernel,
that kernel would have to be trivial. But then H would be the non-C marked
group G. Consequently no finite C-cover of this G with odd prime-power
kernel can preserve both end groups unchanged.

This is an obstruction to that particular construction. It does not say
that odd prime-power C-covers fail to exist: the surface constructions may
and do enlarge the end groups. It does not disprove the general finite
minimal-cover conjecture.

## Replay and scope

    python3 -O phase245_tomotope_integral.py \
      --input phase245_tomotope_complex.json \
      --out /fresh/path/report.json

The author-independent matrix replay passed in 1.144 seconds, with 719 unit
factors and two factors 2. The output contains the spanning tree and complete
unit-operation witness. The file is an independent review contribution to
phase246, not a review of any later phase246 source edits or an independent
reconstruction of the primary geometry.

A second replay with Python optimization enabled passed in 1.160 seconds.
A negative control adds the actual parallel-edge defect as a new cellular
relation; the checker rejects the resulting changed invariant factors.
