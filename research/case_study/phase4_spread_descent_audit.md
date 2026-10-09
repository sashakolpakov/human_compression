# Review record: the 2003 semilinear spread-space question

Date: 9 October 2026. The proof was authored in the `recent_conjectures`
agent track and independently reviewed by the root agent. This records
an internal agent review, not external peer review or a priority claim.

**Verdict: PASS for Theorem A under its stated hypotheses.** The root
agent read Lemmas A1–A3 and checked the primary paper's definitions and
one-dimensional spread reduction in Sections 2.2 and 5.1–5.2. No gap was
found in the prime-degree argument, the arithmetic, or the semilinear
rigidity step.

Reviewed proof: [phase4_old_problem_audit.md](phase4_old_problem_audit.md),
Section 1. SHA-256: `f3ec2ff001fd4271a73c6a5f113db824e275a326f940df516b58ba701bf38882`.

## Precise theorem and dependency boundary

The theorem concerns a spread S of l-dimensional F_p-subspaces of
F_(p^d), with a group H contained in GammaL1(F_(p^d)). H must act
transitively and primitively on S, and each H_U must act irreducibly on
its spread member U over F_p. It concludes that S is the full set of
one-dimensional F_(p^l)-subspaces. For the 2003 geometric question,
source Proposition 5.2 supplies the translation/spread reduction, and
affine blocks correspond to invariant additive subspaces.

No classification of finite simple groups is used inside the descent
argument. No claim is made to reprove the complete classification of
flag-transitive linear spaces or the reduction of every affine action
to the source's case list. The external input is explicitly the
translation/spread description for the one-dimensional case already
established in the primary source.

## Points reviewed

* A primitive permutation action of a group with cyclic normal subgroup
  and cyclic quotient has prime degree. Taking the induced faithful
  action handles a scalar kernel.
* Prime spread size forces d/l=u prime and l=u^e by proper geometric-sum
  or cyclotomic divisors. It also excludes p congruent to 1 modulo u.
* The group acting on a line is taken to be its faithful image J.
  The ambient stabilizer can have a nontrivial restriction kernel;
  the proof does not silently discard it. The scalar subgroup still
  embeds faithfully, and J/C remains a cyclic u-group.
* K=F_p[C] is a field because C consists of genuine ambient-field
  multipliers. Its degree divides the line dimension. Normalization
  of K and the semilinear action follow from the ambient GammaL1 action.
* A suitable u-element y generates J together with C. If m is its
  induced field-automorphism order, y^m centralizes J. Irreducibility
  makes F_p[y^m] a finite field of degree dividing u^e. Its nonzero
  elements have order coprime to u, forcing y^m=1.
* The fixed-vector argument uses independence of field automorphisms,
  not division by the Galois-group order. It therefore includes the
  case u=p. A nonzero fixed vector produces a J-invariant K-line,
  and irreducibility identifies the whole line with that K-line.
* Other spread members are scalar-Frobenius images of this line.
  Uniqueness of the subfield and the spread count give the entire
  Desarguesian spread, rather than just one subfield-like member.

## Evidence and remaining limits

The separate Python certificate exhausts normalized subspaces over F2
in ambient/line dimensions (4,2), (8,4), and the boundary case (6,2).
The first two have only the subfield orbit with irreducible full
semilinear stabilizer. The third has an additional non-subfield orbit,
which demonstrates that the arithmetic hypotheses cannot simply be
removed. These bounded checks are implementation evidence, not the
all-parameter proof.

The proof is not currently a Lean formalization. Targeted later-source
searches found no explicit external resolution of the narrow 2003
RWPRI question, but this does not establish novelty. Later cyclic-spread
constructions lacking local primitivity are outside the theorem's scope.

## Second independent internal review

On 9 October 2026, the separate `survey_audit` agent independently
reviewed Lemma A3 and reported no gap. That review explicitly checked:

* The prime-to-u component of a lift of the cyclic quotient generator
  lies in C, giving J=C⟨y⟩ for its u-primary component.
* The power y^m centralizes K and y, hence J. The finite-field argument
  for F_p[y^m], the divisibility of its degree by the module dimension,
  and absence of u-torsion give y^m=1.
* Applying a K-linear functional nonzero on v to the semilinear sum
  gives a nonzero coefficient at the identity automorphism. Independence
  of the field automorphisms therefore gives a nonzero fixed vector,
  including in characteristic u. Its K-line is J-invariant.
* The faithful-image passage from H_U and the genuine ambient scalar
  subfield K in the theorem application are valid.

This second internal mathematical review does not determine current
literature status or publication priority, replace the written proof,
or extend the theorem beyond its stated hypotheses.

## Existence converse added after the descent review

The root agent proposed, and the `recent_conjectures` agent independently
checked, the explicit converse now recorded after Theorem A. On the
Desarguesian K-lines of F, the designated group T_F⋊F* is already a
one-dimensional affine group. Its pencil action is regular cyclic of
order |F*|/|K*|, so is primitive when that ratio is prime. Its line
stabilizer T_K⋊K* is sharply 2-transitive, as is its global action on
F. This proves the exact existence-and-uniqueness corollary under the
stated parameter conditions, without an appeal to the full affine-space
automorphism group. It does not classify all possible acting subgroups.
