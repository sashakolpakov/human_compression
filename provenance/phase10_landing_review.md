# Independent phase-ten landing-document review

10 October 2026. **PASS after the wording corrections below.** This is an
internal review of the new phase-ten summaries against the frozen proofs,
source-scope records and executed certificates. It is not a new full proof
audit of every older section, an external review, or a fresh Lean compilation.

Reviewed the phase-ten changes in README, the unitary paragraph and sections
12–13 of INTRODUCTION, REPRODUCING, MEASUREMENT and
research/case_study/torsor_compression_overview.md. The later
[phase-ten review record](phase10_review.md) was also read. No unresolved
mathematical-scope or numerical mismatch was found in these changes.

## Exact scopes checked

* **Suzuki reduction:** both L074 principal counts are recovered with their
  all-parameter equivalence, while L085 is matched through its exact primary
  restatement. The original L085 article body remains unavailable. Classical
  group structure is retained. The four sample counts 7,93,14476,35788085,
  49 odd-degree formula comparisons, fields of sizes 8,32,512, and the
  42 matrix triples / 2688 subgroup intersections / 42 duality identities
  agree with the proof and recorded checks. None is presented as proving
  a uniform theorem by finite sampling.
* **Cyclic TPP:** the new theorem covers every finite 2-group triple with a
  cyclic factor of order at most four. The square-rotation factors have
  half the distinguished pair-product orders; with |G:G'|=8, their product
  bound gives precisely the hypertope bound for one pair order at most
  eight. Because the orders are powers of two, remaining counterexamples
  have all pair orders at least sixteen. The marked isobicyclic
  classification remains an explicit input. The 48 models, 48336 relevant
  elements, 386688 swap equations and 1966080 associativity equations match
  the saved report. Ambient order8192 is the largest model, not a census
  cutoff; only n<=8 models exhaust every associativity triple.
* **PSU4(5):** the four matrices preserve the stated Hermitian form over
  GF(25) and have determinant one. Their projective plane-action order is
  14742000000 on 756 planes. Containment and equality of orders identify
  PSU4(5) without a faithfulness assumption or finite-simple-group
  recognition. The sixteen subset groups and all256 intersections give
  type{4,26,10}. Maximum rank four uses the separate phase-nine upper
  bound. The statement remains finite; general odd-field existence and
  historical priority are not asserted.
* **Measurement:** the existing 3.34 ratio is unchanged and remains confined
  to its two matched L066 formulas. No new ratio, whole-corpus extrapolation
  or infinity marker appears. The tree scope audit correctly withholds a
  cross-paper numerator because complete1998 source spans were not recovered.

## Actual Lean statement

I read the complete new InvolutionCentralizers.lean source and its two
statements. The centralizer condition is universally quantified over
nonidentity involutions a,b,c: if b and c commute with a, they commute
with one another. The other assumptions are trivial center, nonidentity
involutory generators indexed by Fin n, distant string commutations, and
Subgroup.closure(Set.range rho)=top. The conclusion is n<=3.

The proof shows that rho3 commutes with every generator and then uses
subgroup-closure induction to prove that it commutes with every group
element. It does not assume the conclusion through a generation predicate.
There is no finiteness hypothesis on the group, no pairwise-distinctness
hypothesis and no subgroup intersection property. Fin n specifies the
length of the proposed generating string, not finiteness of the group.
The second statement merely expresses trivial center as center(G)=bottom.

The saved successful report matches the source hash
`cd7c62c97fd09f9c14f4cf6bcb9c5ab972cd40e1fa6a30585fabd580b8e47072`.
It records only propext, Classical.choice and Quot.sound, with no sorryAx.
This review checked that binding and read the actual formal proof; the
separate compiler execution is recorded by the author/root. Neither the
module nor these summaries claim to formalize Suzuki centralizers,
subfield generation, counting, or rank-three existence.

## Corrections completed during review

README now says the **projective images** of the four unitary matrices form
the string C-group: two matrix lifts square to minus the identity.
INTRODUCTION now says nonzero Frattini classes contain **generators of**
cyclic subgroups, and that the centralizer hypothesis concerns **any**
nonidentity involution. The incidental Suzuki intake author initial was
corrected to A.Kiefer. These changes repair precision without altering
any frozen mathematical argument or computational input.

The reproduction commands distinguish saved hashes from fresh calculations,
use fresh output paths where needed, and state the artifact-directory
requirement for the matrix witness. The sixteen-module count agrees with
the formal inventory. This review does not claim that all sixteen modules
were freshly compiled during phase ten.
