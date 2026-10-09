# Independent review of the Suzuki pure-subfield and mixed-center arguments

10 October 2026. **PASS**, subject to the explicit retained classical
Suzuki facts in the proof. Internal written mathematical review by the
`rank_stability` agent, not external peer review or a publication-priority
claim. This review covers Theorem A, Lemmas B/C, Theorem D, and the
literal-source boundary comparison in
[phase8_suzuki_subfields.md](phase8_suzuki_subfields.md).

## Primary-source comparison

I independently read the primary PDF page images 4, 5, 14, 15, and 18,
and the extracted text of pages 15–18 of L110. The exact source supports
the note's distinctions:

- The RWPRI definition quantifies over every proper type subset. Page 5
  explicitly requires the bottom intersection to be maximal in every
  panel stabilizer. Thus rank-one residues cannot be omitted from the
  test when the bottom subfield is Sz(2).
- The hat-dot notation denotes a nonsplit extension and E_q denotes an
  elementary abelian group of order q.
- Construction 11 writes the exponent as a product of powers of
  pairwise distinct primes and allows only rank alpha at most m−1.
  Here m counts distinct primes, not factors with multiplicity.
- Construction 10 has alpha−1 pairwise nonisomorphic maximal subfield
  groups and the mixed parabolic. The R12 discussion on pages 14–15
  gives the mixed pairwise intersection types used in Theorem D. The
  introduction to the constructions requires retention of that full
  intended intersection lattice.
- Theorem 5 literally says that the rank-at-least-four RWPRI systems
  are given by Constructions 1–11. It does not state an additional
  closure under arbitrary truncations.

The all-simple rank-four family at n=3465 has four distinct primes,
bottom exponent three, and therefore lies outside Construction 11's
literal rank range. Constructions 1–10 each have a soluble maximal
parabolic, so they do not describe this stated-action family. This is
a valid omitted boundary of the literal list. The note correctly
separates that statement from classifying all unlabelled geometries or
allowing additional truncations or a natural corrected construction.

## Pure-subfield family

Writing F=rho^e and m as the product of the selected distinct primes
places the family exactly within the previously reviewed Lang/coset
Helly theorem. Repeated prime factors inside e do not violate the
distinct relative-prime hypothesis. The common-coset property gives
both the geometry axiom and flag transitivity.

In any residue of rank at least two, the two selected subfield
parabolics have exponent greater than one, even if e=1. They are
distinct maximal subgroups and generate the ambient residue group.
Thus the residual-connectivity argument does not incorrectly apply
maximal-simple-subfield facts to Sz(2). Panel indices exceed two by
simplicity of the upper group.

For e>1 all one-step subfield inclusions are maximal. For e=1, at least
one selected relative prime is at least five. The subgroup Sz(2)=5:4
lies in the normalizer of the torus centralizing its C5. That normalizer
is strictly larger and proper, so the required rank-one maximality
fails. The exceptional prime three cannot invalidate the conclusion,
since there are at least two distinct selected primes.

## Mixed-group normal form and exact overgroups

Lemma B does not assume simultaneous subfield alignment. Place its
normal Sylow-2 subgroup inside an ambient U_q. Its elementary abelian
kernel of order q equals Z_q because all ambient involutions lie there.
This is also the full involution set of the subgroup, with the identity,
so it is characteristic and normalized by Q. The retained involution
centralizer formula gives N_G(Z_q)=N_G(U_q)=B_q explicitly.

The odd complement embeds into the unique cyclic subgroup of order
t−1 in the Borel quotient. Schur–Zassenhaus in its full preimage puts
the complement in standard position. Its action on the first unipotent
coordinate consists of all nonzero F_t scalars, so the quotient of the
2-subgroup is an F_t-line. A diagonal conjugation scales this line to
F_t while centralizing H_t. Containing the full center then forces the
entire preimage Z_q U_t. This proves the stated normal form.

For Lemma C, a non-elementary Sylow-2 subgroup has an order-four
element and hence a nonzero image in U_t/Z_t. The full odd projection
acts irreducibly on this additive F_t-line. Normality of the 2-subgroup
therefore forces surjectivity onto the entire affine quotient. Once
Q_0=Z_q H is known, the overgroup correspondence follows directly:
every element of an overgroup can be written zh, and h already belongs
to it, so z does too. The center intersections are exactly F_t-subspaces
because the scalar action is full. No additional conjugacy or arbitrary
subgroup-lattice assumption is hidden in this step.

Theorem D's order calculation gives center quotient dimension
P−P/a_i, greater than one for the admissible parameters. Thus every
prescribed mixed intersection is nonmaximal in Q_0, uniformly over all
embeddings with those intersection types. The nonsplit assumption
ensures the Sylow-2 subgroup is not elementary abelian. This proves
failure of RWPRI at the singleton mixed type; it does not prove failure
of bare embedding, geometry, or flag transitivity. The explicit standard
realization supplies the claimed bare intersection lattice.

## Independent finite rerun and limitations

I read the checker and reran an unchanged copy in a scratch directory,
preserving the author's historical output. The rerun passed:

- 28,672 actual 4-by-4 conjugation checks, 4,096 unipotent product
  checks, and 16,384 additional products involving the generating
  unipotents, over the certified field F512;
- Q=Z_512 U_8 H_8 of order 28,672 and H=U_8 H_8 of order 448;
- all nine scalar-center proper intermediate groups, each of order
  3,584, together with the two endpoint groups;
- all 16 field-degree intersections of the n=3465 example and the
  stated torus-boundary and scalar-exponent arithmetic checks.

The finite calculation verifies this scalar-module example and the
implementation. It is not an enumeration of all Suzuki subgroups and
does not independently prove the uniform normal-form or Helly results.
The written proof supplies those deductions from the retained facts.
No full replacement classification or publication priority is claimed.
Exact reviewed bytes and the separate rerun report are bound by
[phase8_suzuki_subfields_independent_audit.json](phase8_suzuki_subfields_independent_audit.json).
