# Independent audit: odd-order nilpotent cyclic TPP

10 October 2026. Private internal review by the survey-audit agent.
**PASS: no mathematical gap found** in
[phase11_odd_nilpotent.md](phase11_odd_nilpotent.md). The earlier
[class-three consequence](phase11_odd_class_three.md) also passes, with
its separate verification recorded below. Exact proof hashes are bound
in the accompanying JSON. No publication-priority determination or external
peer review is claimed.

## Short proof for all odd primes

The minimum-counterexample proof is valid without any central quotient
or center-free reduction. A trivial cyclic factor leaves the product of
two disjoint subgroups, whose cardinality cannot exceed the group order.
An abelian group likewise cannot be a counterexample. For a proper
pair-generated subgroup H, the TPP triple restricts to A,B,C∩H, and
the injection of C-cosets into the cosets of H supplies the index bound.
No normality of H is assumed. Permutation symmetry of TPP justifies all
three pair-generation conclusions.

Two-generation and noncyclicity then give Frattini index p². Minimality
inside the proper subgroup K=Φ(P) bounds the product of the three cyclic
p-th-power factors, so the violation ratio is at most p. Their original
nontriviality justifies dividing each order by p, even if a resulting
power subgroup is trivial. The violating ratio is a positive power of p,
so it equals p and the powered triple has order product exactly |K|.

If those factors generated a proper subgroup of K, that subgroup would
itself be a smaller counterexample. Consequently

    Φ(P)=⟨a^p,b^p,c^p⟩≤P^p≤Φ(P).

For odd p this makes P powerful, because P′≤Φ(P)=P^p. I independently
checked the precise retained input in Lubotzky–Mann's
[primary author-uploaded text](https://www.researchgate.net/publication/265533173_Powerful_p-groups_I_Finite_groups),
Theorem 1.11 and its forward proof on printed pages 489–490. It applies
to the given arbitrary generating list, so P=⟨a,b⟩ implies P=AB as an
ordered product. Any nonidentity element of C then supplies a forbidden
TPP relation. Merely knowing that some other cyclic factorization exists
would not have sufficed; the retained source has the required marking.

This use of equality establishes generation by minimality. It does not
infer injectivity of A×B×C or of the powered triple's multiplication map.
The proof does not need the dimension-three action lemmas, the powerful-
Frattini obstruction, or Lubotzky–Mann Proposition 1.13.

The passage to finite nilpotent groups of odd order is valid: decompose
the group and each cyclic factor into Sylow components, restrict TPP,
apply the prime-power assertion, and multiply. The proof makes no claim
for arbitrary groups of odd order. Its exact obstruction at p=2 is also
correct: Φ(P)=P² does not imply P′≤P⁴, the powerfulness condition there.

## Earlier odd-prime class-three proof

That proof is independently correct, although the new theorem has wider
scope. For every subgroup H of a class-three group, work modulo Φ(H)^p.
The image of H′ is abelian and has exponent dividing p, and its third
lower-central subgroup is central. The class-three collection identity

    [a^p,b]=[a,b]^p [a,b,a]^(p(p−1)/2)

follows by induction with right conjugation. Both terms vanish for odd p,
including p=3. Hence H^p is central in the quotient, and Φ(H)=H^pH′
has abelian image. This gives [Φ(H),Φ(H)]≤Φ(H)^p for every H, precisely
the hereditary hypothesis of the separately reviewed powerful-Frattini
theorem. The same Sylow-product step is legitimate.

## Added odd-order boundary witness

The final scope paragraph adds SmallGroup(21,1) and does not change the
proof. I read the standalone script and freshly reran it with GAP 4.15.1
and SmallGrp 1.5.4. The three cyclic groups have order three, A∩B=1 and
AB∩C=1, while their order product is 27>21. The ambient group is
nonnilpotent. This is an exact counterexample to dropping nilpotence from
the odd-order statement, not a counterexample to the theorem. The fresh
output is saved separately and the final proof bytes are rebound in JSON.

## Evidence boundary

These are audits of the uniform written arguments and the exact retained
source statement. No new finite census or Lean execution is needed or
claimed. The retained powerful-group theorem has not been re-proved here.
The source was read as rendered primary author text; no local PDF hash
is fabricated. The unresolved 2-group inequality and the full hypertope
conjecture remain outside the all-odd-prime theorem.
