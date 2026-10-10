# Root review: every odd diagonal unitary index-two extension

10 October 2026. **PASS for the stated theorem**, with the q=3 finite
base distinguished from the uniform q>=5 proof. The exact final proof
hash and check artifacts are bound by the accompanying JSON. This is
an internal review, not external peer review or a priority claim.

The new endpoint is an anti-isometry multiplied by a scalar of norm
minus one. It is genuinely unitary, squares to a norm-one scalar and
therefore gives a projective involution. Its determinant has exponent
two in the norm-one group. Together with the reflection determinant,
this supplies the diagonal index-two coset in every odd congruence
class, including q=7 mod8 missed by the previous template.

Root read the standalone generation argument in full. A primitive t
has full-field square; the opposite unipotents on the isotropic plane
therefore generate SL2(E), with the retained Dickson exclusions checked
in characteristics three and five. The pointwise kernel in the full
unitary group is the same radical R as before. The inverse image of
SL2(E) lies in SU4 because the determinant of a unitary lift is
det(g)/conjugate(det(g)). This is the necessary adjustment when the
whole generated plane stabilizer is not special unitary.

The torus-weight contradiction, additive radical irreducibility and
opposite-root extraction then apply with the displayed new matrices.
In particular h(m,Bm)=t*conjugate(t) is always nonzero. The proof supplies
these steps explicitly, retaining only the stated elementary unitary
generation theorem. Root also checked projective nondegeneracy and
the full same-marking dihedral intersection argument. The latter
excludes both common rotations and mixed rotation/reflection cases.

The q=3 base was independently implemented by root from the literal
polynomial coordinates, without importing GAP, author code, a supplied
plane list or group-recognition data. The checker enumerates all 280
isotropic projective points and all 112 isotropic planes over
F3[t]/(t^2-t-1), verifies the unitary identities, and constructs the
three plane permutations. SymPy 1.14.0 Schreier-Sims gives order
6,531,840. Exact unitary containment and the classical target order
give the projective order sandwich. All seven proper marked subgroups
are enumerated directly: their orders are 1,2,2,16,2,4,12 by mask.
The 49 proper-subgroup meets and 15 meets involving the whole group
give all 64 IP checks. This fresh run passed. The survey agent's
separate polynomial-coordinate implementation also passed; these
remain two checks of the same finite base, not extra parameter cases.

Root also freshly reran all 31 identities in the frozen symbolic checker,
from a scratch copy that preserves the historical report. They pass.

The earlier upper bound and rank-four constructions imply rank set
{3,4} for U2(q) for every odd q>=3. This concerns the diagonal extension,
not the simple PSU4(3), which remains the known exception. The linear
proper index-two family, field/graph extensions and all other almost-simple
groups are outside this theorem. The new primary-literature records
must be consulted before attributing novelty: a source with an open
general classification does not certify that this family was unsolved.

No Lean formalization of unitary generation or finite-group order is
claimed. SymPy's permutation-group implementation and the classical
unitary order formula are retained inputs to the finite base. The
all-field proof and its source status remain separately reviewable.
