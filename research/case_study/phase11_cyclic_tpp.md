# Cyclic TPP: the smallest-factor-eight boundary

10 October 2026. Private continuation. Phase 10 is unchanged. The unrestricted
cyclic-TPP inequality and the complete smallest-factor-eight case remain open.

## 1. The precise remaining boundary

For a minimum-order cyclic-TPP counterexample, the previous reductions give
three center-free cyclic subgroups A=⟨a⟩, B=⟨b⟩, C=⟨c⟩ in the three
nonzero Frattini classes, any two generating P, with violation ratio two.
By [phase 10](phase10_cyclic_tpp.md), if the smallest factor has order eight,
then necessarily

    |A|=|B|=n,  |C|=8,  |P|=4n².                        (1)

Here n is a power of two. The existing certificate through order 512
excludes n=8, so a remaining case has n≥16. No order-1024 catalogue is
assumed or searched here.

The following structural conclusions are proved below:

* The involution u of A is central in the maximal subgroup M_A containing A;
  likewise the involution v of B is central in M_B.
* Z(P) is cyclic. If z is its unique involution, then
  [u,b]=[v,a]=z.
* E=⟨u,v,z⟩≅C₂³ is normal in P and contained in Z(Φ(P)). The action of
  P/Φ(P) on E is the pair of transvections displayed in §4.
* Φ(P) is nonabelian.

These statements use the retained marked isobicyclic classification already
recorded in phase 10. They do not classify or exclude every remaining P.

## 2. A further consequence of the extremal classification

**Lemma.** Suppose R is a finite 2-group of order 2n², n≥8 a power of two,
with a center-free cyclic subgroup D of order n. Exactly one of the three
nonzero classes in R/Φ(R) can contain a center-free cyclic generator of
order greater than four; it is the class of D.

The word "exactly" refers to the supporting class: D itself has order n>4.
It does not assert that all elements of that class are center-free.

**Proof.** Phase 10, §3 gives

    R=H⋊⟨t⟩, H=⟨a⟩⟨b⟩, b=aᵗ, t²=1, |a|=|b|=n,

with the specified marked isobicyclic pair. The images of a,t form a
Frattini basis. The two other nonzero classes lie outside H.

In the nonmetacyclic normal form put z₀=a^(n/2)b^(n/2), central in R.
For x=aⁱbʲt with i+j even, phase 10 proves that every nontrivial square
has unique involution z₀. Hence a center-free x in that class has order≤2.
If i+j is odd, the square x² has normal form aʳbˢz₀ᵈ with r,s odd:
this follows directly from Lemma 2.1(ii) of the retained source. Applying
the odd-odd multiplication rule once more gives

    x⁴∈⟨z₀⟩.

Thus x has order at most eight; if it has order eight, its unique involution
is central. Every center-free x outside H therefore has order at most four.

In the metacyclic normal form use H=⟨a⟩⟨h⟩, hᵃ=hᴿ⁰, R₀≡1 mod4,
aᵗ=ah and hᵗ=h⁻¹. Every outside element is x=aⁱhʲt. For i=0 it is
an involution. For 0<i<n put w=v₂(i). The square calculation from phase 10 is

    x²=a^(2i)hᴷ,
    K=j(R₀ⁱ−1)+Sᵢ(R₀),  Sᵢ(R₀)=Σ_(r=0)^(i−1)R₀ʳ.

Here v₂(K)=w: the sum has valuation w, while R₀ⁱ−1 is divisible by
2^(w+2). Applying the same geometric-sum valuation to this square gives

    x^(2^(e−w))=h^(n/2)≠1,   n=2ᵉ.

The right side is a central involution of R. Hence every outside element
of order greater than two has a central involution. This proves the lemma.
The valuation assertions also include R₀=1 by their direct sum formulas. ∎

Primary input: Du–Jones–Kwak–Nedela–Škoviera,
[arXiv:1112.2376v1](https://arxiv.org/pdf/1112.2376), marked Theorem 4.1
and Lemma 2.1, together with the marked metacyclic normal form in their
[2007 Theorem 1.1(1)](https://doi.org/10.1016/j.ejc.2006.08.012).
The input scope and private source hash remain those of phase 10.

## 3. The large cyclic factors centralize their own involutions locally

The next conclusions only require that P=⟨a,b⟩ has order 4n², that
|a|=|b|=n≥16, and that both cyclic subgroups avoid Z(P). They do not
use C or TPP.

Let M_A be the maximal subgroup corresponding to aΦ(P), and put
u=a^(n/2), v=b^(n/2). Suppose u is noncentral in M_A. Then A is
center-free in M_A, and |M_A|=2n², so §2 applies to M_A.

Conjugation by b is an automorphism of M_A. It maps a to another
center-free element of order n, so it preserves the unique nonzero
Frattini class supporting such an element. Thus

    aᵇΦ(M_A)=aΦ(M_A).

Schreier generators for the index-two subgroup give

    M_A=⟨a,aᵇ,b²⟩.

Since M_A/Φ(M_A) has rank two by §2, the element b² must have the
other independent nonzero image; equivalently a,b² generate M_A.
The subgroup B² is center-free in M_A: if its involution v were central
there, it would commute with b as well, hence with P=⟨M_A,b⟩. This
would contradict B∩Z(P)=1. But |B²|=n/2>4, contradicting §2.

Therefore u∈Z(M_A). Interchanging a,b gives v∈Z(M_B).

Neither u nor v is central in P. As b²∈M_A and u is central in M_A,
conjugation by b swaps the two distinct commuting involutions u,uᵇ.
Their product

    z_A=[u,b]=u uᵇ

is a nontrivial involution fixed by M_A and by b, hence central in P.
Similarly z_B=[v,a] is a nontrivial central involution. Thus

    [u,P]=⟨z_A⟩,  [v,P]=⟨z_B⟩.                      (2)

## 4. Cyclic center and a forced normal elementary-abelian subgroup

Suppose Z(P) had more than one involution. Its involutions would then
contain a Klein four group. Choose a central subgroup N of order two
different from both ⟨z_A⟩ and ⟨z_B⟩: there are at least three central
subgroups of order two in total, so at least one remains after these exclusions.

A and B intersect N trivially, so both retain order n in P/N. Their
involutions are noncentral in the quotient by (2), so their images are
center-free. Also Z(P)≤Φ(P): otherwise a central element outside Φ(P),
together with one other basis lift, would generate P, making P abelian.
Consequently P/N has the same rank-two Frattini quotient, and the images
of a,b remain in different nonzero classes.

Now |P/N|=2n². Lemma §2 applied to the image of A says that only one
nonzero Frattini class can support a center-free cyclic subgroup of
order n>4. The image of B contradicts this. Thus Z(P) has a unique
involution z and is cyclic, and (2) becomes

    [u,b]=[v,a]=z.                                      (3)

The involutions u,v,z are independent. First u and v commute: both lie
in Φ(P), and u is central in M_A while Φ(P)≤M_A. If a product
uⁱvʲzᵏ were one, commuting it with a gives zʲ=1 and commuting with b
gives zⁱ=1; then k=0 as well. Hence

    E=⟨u,v,z⟩≅C₂³.

It is normal, contained in Z(Φ(P)), and has the following action:

| Generator | u | v | z |
|---|---|---|---|
| a | u | vz | z |
| b | uz | v | z |

The two actions are independent commuting involutions. Their common kernel
in P is Φ(P), so C_P(E)=Φ(P). This describes a necessary normal
subgroup and action, not the entire group P.

## 5. The Frattini subgroup cannot be abelian

Continue under the hypotheses of §3. Suppose Φ(P) were abelian. Put

    x=a², y=b², d=[a²,b].

Because x and xᵇ belong to the abelian Φ(P), equation (3) gives

    d^(n/4)=[a^(n/2),b]=z.

Therefore d has order n/2 and unique involution z. The cyclic groups
⟨x⟩,⟨y⟩,⟨d⟩ all have order n/2, and their respective involutions
are the independent u,v,z. Their product inside the abelian Φ(P) is
direct: any nontrivial kernel in the map from C_(n/2)³ would contain
an involution, whereas the map is injective on its involutions.

This forces

    |Φ(P)|≥(n/2)³.

But |Φ(P)|=n², so n≤8, contrary to n≥16. Thus Φ(P) is nonabelian. ∎

In particular the boundary (1) is excluded for every group with abelian
Frattini subgroup. This statement does not assert cyclic TPP for all such
groups at larger values of the smallest cyclic factor.

## 6. What the coset graph does and does not supply

The action on the cosets of A has 4n vertices. The M_A-orbits form two
parts of size 2n. By §3, every g outside M_A sends u to uz≠u, so
A∩Aᵍ=1. Consequently A has exactly two regular orbits, each of size n,
on the opposite part. There are exactly two P-orbits on oriented edges
between the two parts, each with trivial stabilizer and size |P|.

Reversal either fixes both such orbits, or interchanges them. In the first
case either orbit gives an undirected bipartite graph of degree n on 4n
vertices; in the second they give the two orientations of a bipartite
tournament. A self-paired orbit has a unique involution reversing a chosen
arc, by the same free-action argument as phase 10. However neither
self-pairing nor connectedness of an individual orbit graph follows from
the current hypotheses. In particular an involutory factor swap or a
complete-bipartite graph must not be assumed at this stage.

The remaining group must therefore realize (3), the normal E₈ action,
a cyclic center and a nonabelian Φ(P), together with the additional
order-eight cyclic subgroup C and TPP. No such realization or contradiction
is established here. These restrictions are candidates for a smaller
structural classification, not a complete proof for γ=8.

## 7. Evidence and limits

The written reductions are separate from the existing finite certificate.
Only that certificate excludes the initial n=8 case in (1). No new broad
SmallGroups enumeration is used. The new phase11_cyclic_tpp_check.py checks
the additional outside-element order assertion from §2 in the frozen
phase10 normal forms; its finite scope is separate from the uniform proof.

There is a concrete obstruction to an appealing alternative argument.
In SmallGroup(32,5), with the standard GAP pc generators f₁,…,f₅, take

    A=⟨f₂⟩, B=⟨f₁⟩, C=⟨f₂f₃⟩.

These cyclic groups have orders 2,8,2, with A∩B=1 and AB∩C=1, so
they have TPP. Their order product equals |P|=32, yet |ABC|=24.
The ambient group is (C₈×C₂):C₂ and even has nilpotency class two.
Thus numerical equality in the cyclic-TPP bound does not imply global
injectivity. The standalone phase11_tpp_equality_witness.g checks this
single example; phase11_tpp_equality_probe.g records its bounded discovery
and a separate S₄ example. Neither example contradicts the inequality.

Reproduce the diagnostics using Python 3 and GAP with SmallGrp:

    python3 phase11_cyclic_tpp_check.py --output phase11_cyclic_tpp_check.json
    gap -q phase11_tpp_equality_witness.g

Targeted primary searches included Lucchini's 1998 bound for transitive
groups with cyclic point stabilizer and the published work on nilpotent
regular maps. No classification or theorem from those papers is imported
into §§2–6. The only retained classification is the marked isobicyclic
one already audited in phase 10.
