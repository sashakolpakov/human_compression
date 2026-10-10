# Independent mathematical audit of the small-factor cyclic-TPP theorem

10 October 2026. Internal review by recent_conjectures. **PASS: no
mathematical gap found** in the reviewed written proof, including its
final hypertope corollary. This is not external peer review and does not
establish priority.

Reviewed proof SHA256: 95642b93d361255fb0154b6f4dbd7343c7e77f36bda054c24522ba8d857795d3.
Retained primary classification PDF SHA256: 6ad3216b0cbc07088fd652787bb566917cf0c1aabbea0e1e2399c9a71ab47ac7.

I read the entire current proof, with particular scrutiny of §§3–6;
the earlier minimum-counterexample reduction in
phase3_cyclic_tpp_exploration.md; and the primary classification's
Theorem4.1 on PDFp15, Lemma2.1 on PDFp5, and its p3 restatement of the
marked metacyclic pair. The source classifies the given marked
isobicyclic pair, not merely the unmarked group. That is essential and
is correctly retained as a substantive external theorem.

The equality argument is sound. A center-avoiding cyclic subgroup has a
disjoint conjugate; both lie in any maximal subgroup containing the
first, and equality fills that maximal subgroup. The conjugator cannot
lie inside it, by normality of maximal subgroups of a finite p-group.
The right-coset action has two parts of size n. The base stabilizer acts
regularly on the opposite part; vertex-transitivity then gives
arc-transitivity, with exactly |P| arcs. Thus arc stabilizers are trivial
and the unique arc reversal is an involution. No unproved assumption
that the original conjugator is involutory or that the coset action is
faithful is needed: the trivial arc stabilizer supplies faithfulness.
Conjugating the vertex stabilizer by this reversal yields exactly the
factor-swapping marked semidirect product required by the source.

In the metacyclic branch I independently multiplied
x=a^i h^j t using h^a=h^R and a^t=ah. This gives exactly
x²=a^(2i) h^[j(R^i-1)+S_i(R)]. The bracket is odd when i is odd.
The geometric sum in x^n has valuation e-1, including R=1;
therefore x^n=h^(n/2), a nontrivial central involution. The indicated
Frattini class cannot contain a center-avoiding cyclic generator.

In the nonmetacyclic branch the source commutation rules give
x²=a^(i+j)b^(i+j) for even i,j and
x²=a^(i+j)b^-(i+j) z^[l(i+j)/2] for odd i,j.
Both possible cyclic diagonal groups have unique involution z, and
z is fixed by the swapping involution as well as central in M.
The n=4 endpoint has k=l=0 and also satisfies every step. Thus the
second Frattini class has no center-avoiding element of order>=4.

The conclusion for all TPP triples with a factor of order<=4 requires
minimum-order induction within that subclass, not just an assertion
about an unrestricted minimum counterexample. The proof does make that
distinction. Central quotients, intersections with a proper
pair-generated subgroup, and the maximal-subgroup squaring reduction
all preserve the small-factor condition. The improved inequality
alpha²<=|P|/4 yields 8alpha<=beta gamma and hence gamma>=8, excluding
a reduced counterexample in the subclass.

The hypertope corollary properly retains the earlier geometry-to-TPP
reduction, including flag-transitivity, and applies the factor-of-two
relationship between pair-product orders and square-rotation subgroup
orders. It proves the order bound whenever one pair product has order
<=8, without asserting the unrestricted conjecture.

This review is of the written uniform argument and exact source
hypotheses. It does not independently rerun the normal-form checker,
formalize the classification in Lean, or remove the published marked
isobicyclic classification from the dependency boundary.
