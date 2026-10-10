# Independent root review: the odd linear diagonal interval

10 October 2026. PASS for the uniform written proof and the exact scope
of its companion maximum-rank conclusion. This is internal review;
publication priority and external review remain unverified.

The reviewer read the complete proof. One incorrect root index in the
initial draft was corrected before the frozen version: returning from
root 24 to root 23 uses root 43. The final note lists all initial
and inductive elementary commutator chains explicitly. Every such
commutator has distinct indices, so it supplies the stated product
coefficient. The positive powers of a nonzero field generator span
the entire finite field, including one. This establishes actual
SL4 generation, rather than generation only over a proper subfield.

The triangular subgroup calculation is valid in every odd characteristic.
The three simple-root characters of the four-element diagonal subgroup
are different and nontrivial; averaging divides only by four. Its
commutator differences project onto every simple-root line. The
unitriangular abelianization has exponent p, so the Burnside-basis
application correctly gives the whole prime-field unitriangular group.
The scalar kernel is trivial because its second diagonal entry is one.

The reviewer independently derived the form-intersection equations
from rows 11, 12, 13, 14, 24, 34 and 44. They force exactly the
displayed four-sign/one-prime-field-parameter family, of size 4p.
No orthogonal subgroup classification or unspecified square-class
condition is used. Scalar projective lifts preserve the similitude
condition, so the calculation proves the projective maximal-parabolic
meet as well. Triangularity and the two distinct simple-root lines
prove both rank-three meets. The recursive criterion then applies.

The unipotent cubes handle p=3 as well as larger odd primes. The
nonzero simple-root entries force exact order p; the two signs in
the rotation give exact projective order 2p. Primitive h avoids the
single forbidden value for every q>=5, while q=3 is handled separately.
Determinant classes yield precisely the diagonal index-two subgroup.
The maximum-rank assertion additionally retains the earlier written
rank obstruction; the simple-socle existence theorem is retained only
for the complete diagonal-interval corollary.

The final exported checker was freshly executed in a scratch copy:
89 exact rational-function identities passed, with the same list as
the author report. The exported GAP checker also passed q=3,5,7,9,
all 64 marked subgroup closures and all 1,024 meets. Every reported
group order, type and parabolic order matches the author output;
only execution times differ. The companion JSON binds those runs.

This proves the proposed diagonal-interval result, conditional on its
recorded upper-bound dependency. It does not supply rank-three
representations of the extensions, unitary diagonal constructions,
field/graph extensions, or a resolution of the entire survey Problem 7.
The bounded primary-source status audit is appropriately inconclusive
about current priority. No infinity marker or new Lean claim is warranted.
