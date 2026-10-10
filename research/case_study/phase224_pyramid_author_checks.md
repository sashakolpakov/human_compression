# Author checks for the toroidal pyramid application

The complete argument in phase224_pyramid_covers.md was checked against the
seven-page Monson--Schulte author text, especially Example3.7. The original
polytope, its known non-C monodromy and prior finite-cover existence are
attributed. Later classification context is attributed separately to the
relevant2022 primary section; no comprehensive priority claim is made.

The final replay is

    python3 -O phase224_pyramid_check.py --out /a/fresh/directory

It passed in3.222seconds at /private/tmp/phase224_pyramid_final_replay. The
six-file packet was copied to an otherwise independent temporary directory,
without any primary PDFs or research manifests, and the same command passed
there in3.094seconds. GAP4.15.1 and Lean4.32.2 with the pinned mathlib checkout
are external tool dependencies; their paths can be supplied as arguments.

The positive witness reconstructs all360 flags and verifies92160 component
intersections. GAP checks the actual marked homomorphism from the resulting
3,627,970,560-element monodromy group to the explicit3840-element quotient;
only permutation-group algorithms are used, not an enumeration of billions
of elements. Both end intersections and the required kernel containment are
actual subgroup comparisons. The source monodromy numbers agree, but are
not assumed by the construction.

The surface witness uses the same ten-point quotient marks printed by GAP;
the runner compares the full image lists before applying the surface program.
It constructs all3200 disks and records the exact complement components.
The all-prime result is then a deduction from the frozen211 theorem, with
homology dimension642. The pullback uses the general finite fiber-product
lemma; in particular ell=5 does not require the extension over D to split.

Two controls reject material errors: deleting one flag destroys unique
adjacency; enlarging the quotient kernel to kill an original defect produces
a top intersection of order4 versus middle intersection of order2 and fails
the pullback condition. The latter kernel has order1889568.

Nine existing Lean declarations were freshly compiled with only propext,
Classical.choice and Quot.sound. No new Lean declaration is claimed, and
neither the geometry nor GAP nor cellular homology has thereby become fully
formalized. The three formal fiber-product lemmas and six kernel-order
lemmas have exactly the scopes described in their frozen sources.

The independently readable proof and this author replay are ready for
independent mathematical review. The stronger finite theorem for arbitrary
polytopes remains unproved; exploratory224 files are not part of this freeze.
