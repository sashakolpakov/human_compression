# Cyclic TPP: excluding the extremal cyclic-core case

10 October 2026. Private research continuation. The unrestricted cyclic-TPP
inequality and Hou–Feng–Leemans Conjecture 3.3 remain unresolved.

## 1. Result and precise dependence

**Theorem.** Let P be a finite 2-group with P/Φ(P)≅C₂². Suppose that the
three nonzero Frattini classes contain generators of cyclic subgroups
A,B,C, each disjoint from Z(P) and each of order at least four. Then, for
each D∈{A,B,C},

    |D|² < |P|/2, and therefore |D|² ≤ |P|/4.             (1)

This theorem does not assume TPP. It strengthens the elementary bound
|D|²≤|P|/2 by ruling out equality under the three-class hypothesis.
It retains the published classification of marked isobicyclic 2-groups;
that classification is not re-proved or machine-verified here.

**Cyclic-TPP consequence.** A counterexample of minimum group order to
|A||B||C|≤|P|, for cyclic TPP triples in finite 2-groups, must have

    min(|A|,|B|,|C|) ≥ 8.

In particular the previously unresolved smallest-factor-four extremal
case is excluded uniformly, without an order cutoff. This is a reduction
of the remaining problem, not its complete solution.

## 2. Retained primary theorem, with its marking

Write n=2ᵉ≥4. An isobicyclic triple is (M,a,b) with
M=⟨a⟩⟨b⟩, |a|=|b|=n, ⟨a⟩∩⟨b⟩=1, and an automorphism
interchanging the specified generators a,b. Such an automorphism has
order two because a,b generate M.

The two retained normal forms are:

* If M is metacyclic, one may write a=gᵘ, b=gᵘh, with u odd,
  gⁿ=hⁿ=1 and hᵍ=h^(1+2ᶠ), 2≤f≤e. Consequently a,h also give
  unique coordinates M=⟨a⟩⟨h⟩ and hᵃ=hᴿ for R≡1 mod4.
  This is Theorem 1.1(1) of Du–Jones–Kwak–Nedela–Škoviera,
  [*Regular embeddings of Kₙ,ₙ where n is a power of 2. I: Metacyclic
  case*](https://doi.org/10.1016/j.ejc.2006.08.012), European Journal of
  Combinatorics 28 (2007), 1595–1609. Its exact marked statement was read
  on the primary journal page, and is restated on page 3 of the source below.
* If M is not metacyclic, the **given pair** a,b satisfies the presentation
  G₂(e;k,l) in Theorem 4.1 of the same authors,
  [*2-Groups that factorise as products of cyclic groups, and regular
  embeddings of complete bipartite graphs*](https://arxiv.org/pdf/1112.2376),
  arXiv:1112.2376v1, PDF pages 15–16. Here k,l∈{0,1}, with k=l=0 if
  n=4. We use its Lemma 2.1(i),(ii) on PDF page 5: z=a^(n/2)b^(n/2)
  is a central involution of M, ⟨a²,b²⟩ is the direct product of those
  cyclic groups, and

      bʲaⁱ = aⁱbʲ                         if i,j are even;
      bʲaⁱ = aⁱb⁻ʲ z^(lj/2)               if i odd, j even;
      bʲaⁱ = a⁻ⁱbʲ z^(li/2)               if i even, j odd;
      bʲaⁱ = a⁻ⁱb⁻ʲ z^(k+l(i+j)/2)        if i,j are odd.       (2)

We use right conjugation xʸ=y⁻¹xy. The classification of abstract groups
alone would not suffice: the markings and the specific factor-swapping
automorphism matter. Theorem 4.1 explicitly has the required marked form.

The source PDF is retained privately as phase10_isobicyclic_source.pdf;
its hash and the read locations are recorded in the certificate. It is
not part of a distributable proof/checker package.

## 3. Equality forces an involutory factor swap

Suppose a cyclic D=⟨a⟩, of order n≥4, avoids Z(P), and
|P|=2n². We first show that P is a split extension of a marked
n-isobicyclic group, without assuming a factor swap in advance.

Let u be the involution of D. It is noncentral, so choose g∈P with
uᵍ≠u. Distinct cyclic 2-subgroups intersect nontrivially only if their
involutions agree, hence D∩Dᵍ=1. Every maximal subgroup M containing D
is normal in P and contains Dᵍ. Its order is n², so

    M=DDᵍ.

In fact g∉M. Otherwise the two proper subgroups D,Dᵍ of the finite
p-group M lie in the same maximal subgroup of M (maximal subgroups are
normal), contradicting M=DDᵍ.

Consider P acting by right multiplication on its 2n right cosets of D.
The M-orbits are the two parts of size n. The stabilizer D of the base
vertex is transitive on the opposite part: the stabilizer in D of the
vertex Dg is D∩Dᵍ=1, so that orbit has n elements. Thus P acts
transitively on the oriented edges of the complete bipartite graph between
the two parts. Every such edge has trivial stabilizer, since there are
2n²=|P| oriented edges. In particular there is a unique t taking the
oriented edge (D,Dg) to (Dg,D). Its square fixes that oriented edge,
so t²=1, and t lies outside M.

Put b=aᵗ. The two vertex stabilizers ⟨a⟩ and ⟨b⟩ are disjoint,
are contained in M, and have product of size n². Therefore

    M=⟨a⟩⟨b⟩,   P=M⋊⟨t⟩,   aᵗ=b, bᵗ=a.       (3)

This establishes the full hypothesis of the marked classification.
It also gives P=⟨a,t⟩. Since P is noncyclic, aΦ(P),tΦ(P) are a
basis of P/Φ(P). In particular bΦ(P)=aΦ(P).

No assertion that the original g is involutory was used. Nor was a
general product of three subgroups assumed to be injectively parametrized.

## 4. The metacyclic isobicyclic branch

Use the marked normal form in §2 and put h=a⁻¹b. Equation (3) implies

    aᵗ=ah,   hᵗ=h⁻¹,   hᵃ=hᴿ,   R≡1 mod4.

Every x∈P\M has unique form x=aⁱhʲt, 0≤i,j<n. Because
h=a⁻¹aᵗ is a commutator, h∈Φ(P); thus the elements with i odd form
the Frattini class a t Φ(P).

For i≥0 let Sᵢ(R)=1+R+⋯+R^(i−1), with S₀=0. The split cyclic
normal form gives (ah)ⁱ=aⁱh^Sᵢ(R), hence

    x²=a^(2i)hᴷ,   K=j(Rⁱ−1)+Sᵢ(R).

If i is odd, K is odd. Consequently

    xⁿ = h^[K(1+R^(2i)+⋯+R^((n/2−1)2i))]
       = h^(n/2) ≠ 1.                                  (4)

For the last equality the geometric sum has 2-adic valuation exactly
e−1: its length is 2^(e−1) and its ratio is 1 mod4. This follows by
repeatedly factoring S_(2r)(Q)=S_r(Q)(1+Qʳ), with the second factor
2 mod4, including Q=1. The factor K is odd, so the exponent is n/2
mod n.

The involution h^(n/2) commutes with a (R is odd), h, and t (which
inverts h), hence belongs to Z(P). Equation (4) gives x order 2n and
shows that **no cyclic subgroup generated by this Frattini class avoids
the center**. This contradicts the three-class hypothesis of §1.

## 5. The nonmetacyclic isobicyclic branch

Use (2). Every x∈P\M has unique form x=aⁱbʲt. Its Frattini class
is tΦ(P) precisely when i+j is even. The central involution
z=a^(n/2)b^(n/2) of M is fixed by t, so z∈Z(P).

Set s=i+j. If i,j are both even, then

    x²=aⁱbʲbⁱaʲ=aˢbˢ ∈ ⟨a²b²⟩.

If i,j are both odd, (2) with the even exponent s gives

    x²=aⁱbˢaʲ=aˢb⁻ˢz^(ls/2) ∈ ⟨a²b⁻²⟩.       (5)

Both diagonal cyclic subgroups on the right have order n/2 and unique
involution z, because ⟨a²⟩×⟨b²⟩ is a direct product. In the second
case z itself belongs to ⟨a²b⁻²⟩, as its n/4-th power, so the last
membership in (5) includes the displayed z factor. These assertions also
hold for n=4, where k=l=0.

Thus, if x∈tΦ(P) has order greater than two, the unique involution
in ⟨x⟩ is z∈Z(P). Every cyclic subgroup from this Frattini class
that avoids the center has order at most two. This again contradicts the
three-class hypothesis, and completes the proof of the theorem. ∎

## 6. Consequence for a smallest cyclic-TPP counterexample

The earlier [minimal-counterexample argument](phase3_cyclic_tpp_exploration.md)
proves that all three cyclic factors avoid the center, generate pairwise,
and occupy the three different nonzero Frattini classes. Their violation
ratio equals two. Write α≥β≥γ for their orders; then

    |P|=αβγ/2,   α²≤|P|/2,

which already implies γ≥4. The theorem proved above therefore applies,
and improves the second inequality to α²≤|P|/4. Hence

    8α≤βγ,

and β≤α forces γ≥8. The proof is valid for a counterexample chosen of
minimum order within the subclass min(|A|,|B|,|C|)≤4 as well: central
quotients and factor intersections never increase these orders. Therefore
the cyclic-TPP inequality actually holds for **every cyclic triple with
at least one factor of order at most four** in a finite 2-group.

For the last statement, one may also phrase the induction directly:
the central-quotient and proper-pair-generated reductions preserve the
existence of a factor of order at most four; a reduced counterexample
would have γ=4 and was just excluded. This does not assume that a
hypothetical unrestricted minimum counterexample has that property.

No assertion about γ≥8 is proved here beyond the displayed necessary
inequality. In particular the next boundary γ=8, α=β, |P|=4α²
does not have the complete-bipartite equality used in §3.

**Hypertope corollary.** In the setting of Hou–Feng–Leemans
[Conjecture 3.3](https://arxiv.org/pdf/1901.09034), the order bound holds
whenever at least one of the three distinguished pair products has order
at most eight. Indeed the square-rotation subgroups in G′ form a cyclic
TPP triple and have half the corresponding pair orders; also |G:G′|=8.
Applying the small-factor theorem gives precisely the source's desired
product bound. Thus any hypertope counterexample must have all three
pair orders at least sixteen. The geometry-to-TPP reduction is retained
from [phase3_order_bound.md, §3](phase3_order_bound.md); no subgroup-IP
condition is substituted for the flag-transitivity hypothesis there.

## 7. Verification and remaining scope

The accompanying phase10_cyclic_tpp_check.py independently multiplies
normal-form coordinates in the classified semidirect products. It checks
the swap, associativity, element-power formulas and the relevant
Frattini-class central-involution obstruction for bounded parameters.
These finite checks are diagnostics, not a replacement for the uniform
proof or the retained classification. No full Lean certification or
publication-priority claim is made.

The default completed run covers e=2,…,6: 17 nonmetacyclic parameter
models and 31 metacyclic ratios R≡1 mod4, with ambient orders through
8,192. It checks 10,888 nonmetacyclic and 37,448 metacyclic forbidden-class
elements, 1,966,080 base associativity equations and 386,688 swap equations.
All base associativity triples are checked for n≤8; larger n use
generator-local equations, as explicitly recorded in the script. Each
central involution is checked against all three ambient generators.

Reproduce with Python 3 and no third-party packages:

    python3 phase10_cyclic_tpp_check.py --output phase10_cyclic_tpp_check.json

The primary search also read the statements of Berkovich's 2006
Corollary 17/Remark 18 and Sambale's Theorem 3.1 on general bicyclic
2-groups. Their broader presentations are unnecessary here: §3 supplies
the extra involutory symmetry needed for the sharper marked classification.
The 2025 paper arXiv:2505.05065 concerns when all bicyclic groups of given
factor orders are nilpotent; it does not supply this extremal argument.
