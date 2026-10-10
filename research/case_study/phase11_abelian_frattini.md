# Cyclic TPP in finite 2-groups with abelian Frattini subgroup

10 October 2026. Private research proof. This result is separate from the
phase11 smallest-factor-eight restrictions and does not retain the
isobicyclic classification used there.

## 1. Uniform theorem

**Theorem.** Let P be a finite 2-group with abelian Frattini subgroup Φ(P).
If A,B,C are cyclic subgroups with the triple product property

    abc=1, a∈A, b∈B, c∈C  ⇒  a=b=c=1,

then |A||B||C|≤|P|.

The theorem assumes cyclicity. It does not claim the
same bound for arbitrary subgroup TPP triples, nor does it settle the
cyclic-TPP problem for all 2-groups.

The retained group-theoretic background consists of the elementary
Frattini formulas for finite p-groups, Burnside's basis theorem and
orbit/product formulas. The proof includes its reductions. Its only
additional finite-dimensional ingredient is the binary linear lemma
proved in §3; no group classification or subgroup catalogue is used.

## 2. A minimum counterexample forces a direct Frattini decomposition

Suppose the theorem fails, and take a counterexample of minimum |P|
within this class. The class is closed under subgroups and quotients:
Φ(H)=H²[H,H]≤P²[P,P]=Φ(P), and Φ(P/N)=Φ(P)N/N.
Thus both are abelian whenever Φ(P) is abelian.

First A∩Z(P)=B∩Z(P)=C∩Z(P)=1. Otherwise quotient by a nontrivial
central subgroup D of one factor, say A. A relation abc∈D is absorbed
into a, so the quotient triple has TPP. The other two factors meet D
trivially, and the factor-order product divided by the group order is
unchanged. This contradicts minimum order.

Second every pair generates P. If H=⟨A,B⟩<P, the smaller triple
A,B,C∩H has TPP. Its inequality, multiplied by
|C:C∩H|≤|P:H|, proves the original inequality. The other pairs follow
because subgroup TPP is invariant under permutations: cyclically rotate
the defining equation and take inverses.

Hence P is noncyclic, P/Φ(P)≅C₂², and generators of A,B,C lie in its
three different nonzero classes. If the violation ratio

    r=|A||B||C|/|P|

were at least four, take the maximal subgroup M corresponding to A's
Frattini class. The triple A,B²,C² lies in M, retains TPP, and has
violation ratio r/2≥2. Minimum order forbids this. Since r is a power of
two greater than one, it equals two.

All three cyclic factors have order at least four. Indeed, write their
orders α≥β≥γ. If u is the involution of A, choose g with uᵍ≠u,
possible because A avoids the center. Then A∩Aᵍ=1. A maximal subgroup
containing A is normal and contains Aᵍ, so α²≤|P|/2. Combining this
with |P|=αβγ/2 gives 4α≤βγ; since β≤α, it follows that γ≥4.
This step is elementary and does not use phase10's stronger bound.

Put K=Φ(P). The subgroups A²,B²,C² lie in K and still have TPP.
Since K is abelian, their multiplication map is a homomorphism with
trivial kernel. Therefore their product is an internal direct product.
Its order is

    |A²||B²||C²|=|A||B||C|/8=|P|/4=|K|.

Choose generators a,b,c of A,B,C, and put x=a²,y=b²,z=c². We have

    K=⟨x⟩×⟨y⟩×⟨z⟩,                                (1)

with each factor nontrivial. Thus the images of x,y,z form a basis of
V=K/2K≅F₂³, where K is written additively.

The inference of a direct product here uses the actual abelianness of K.
Numerical equality plus cyclic TPP alone would be insufficient, as the
separate order-32 witness in phase11 demonstrates.

## 3. The binary square-action lemma

**Lemma.** Let x,y,z be a basis of a three-dimensional F₂-space V.
Let S,T be commuting involutory linear maps, and let d,f∈V satisfy

    Sx=x,             Ty=y,
    Tx=x+(I+S)d,      Sy=y+(I+T)d,
    z=x+y+Td+(I+ST)f.                                  (2)

Then either S=T=I, or

    im(S−I)=im(T−I)=L,

where L is one of the three coordinate lines ⟨x⟩,⟨y⟩,⟨z⟩ and
both maps fix L pointwise.

**Proof.** If S=I, equations (2) give Tx=x, Ty=y and Td=d. Applying
T to the last equation gives Tz=z, so T=I. The case T=I is symmetric.
If S=T, the first two equations fix x,y; the third fixes d; and then
the last fixes z. Thus again S=T=I.

Otherwise N=S−I and M=T−I are distinct, nonzero, square-zero maps
on V. Each has rank one, because im N≤ker N in dimension three, and
similarly for M. Also NM=MN=0. For if their common product were
nonzero, its image would force im N=im M; each map kills this common
line, which instead makes the product zero.

If im N and im M were different, their span would be both kernels:
NM=MN=0 and square-zero imply that both image lines lie in each
two-dimensional kernel. Call the common kernel W. The equations
Nx=0, My=0 put x,y in W. The next two equations give Nd=Md=0,
so d∈W. But then Td∈W and (I+ST)f=(N+M)f∈W; the last
equation in (2) puts z in W too, a contradiction.

Consequently im N=im M=⟨u⟩. Write N=uφ and M=uψ, where φ,ψ
are distinct nonzero linear functionals. They are independent over F₂
and annihilate u. Set

    r=ψ(x)=φ(d),   s=φ(y)=ψ(d).

Equations (2) give the following images under (φ,ψ):

    x↦(0,r),  y↦(s,0),  z↦(r+s,r+s).                  (3)

Since φ,ψ are independent and x,y,z are a basis, (r,s) cannot be
(0,0). The three other cases in (3) have kernel ⟨z⟩, ⟨y⟩, ⟨x⟩,
respectively. This kernel is the common line ⟨u⟩. It is therefore a
coordinate line and is fixed by both maps, as required. ∎

The standalone checker phase11_binary_action_check.py exhausts all
linear maps on F₂³ satisfying the hypotheses. It is an exact finite
cross-check of this lemma; the displayed argument proves it directly.

## 4. Why conjugation satisfies the lemma

Use right conjugation vᵃ=a⁻¹va. Let S,T denote conjugation by a,b on
the abelian group K, and also their induced maps on V=K/2K. These
actions commute and have square I: a²,b² and [a,b] lie in K, whose
inner action on itself is trivial. Also Sx=x and Ty=y.

Put d=[b,a]=b⁻¹a⁻¹ba∈K. Then bᵃ=bd and aᵇ=ad⁻¹. The
square calculations, first in additive K, are

    Tx=x−Sd−d,       Sy=y+Td+d.                        (4)

Since c lies in the third Frattini class, write c=abf with f∈K.
Computing its square gives

    z=c²=x+y+Td+(I+ST)f.                               (5)

For example (ab)²=a²b²dᵇ, which proves the first three terms in (5).
Reducing (4),(5) modulo 2K yields exactly (2). Thus the lemma applies
to the actions on the distinguished direct factors in (1).

## 5. Lifting to a central involution

Write the orders of the three factors in (1) as 2ʳˣ,2ʳʸ,2ʳᶻ, with
rₓ,rᵧ,r_z≥1, and let r be their maximum. For any automorphism of K,
the image of the involution 2^(r−1)w in a factor of order 2ʳ depends
only on the reduction modulo two of its coefficients in the factors of
that same maximal order. Contributions in shorter factors vanish when
multiplied by 2^(r−1); even coefficients in maximal factors vanish too.

If the actions on V are both trivial, any maximal-order factor therefore
has its involution fixed by both S and T. Otherwise let L be the common
image coordinate line from §3, corresponding to one factor of K.

If that factor has maximal order, choose its involution: its coordinate
vector is fixed by both induced actions, so the preceding lifting
observation again fixes its involution in K. If it has smaller order,
choose any maximal-order factor. Its coordinate vector can change modulo
two only by that shorter coordinate. All such changes disappear on its
involution, which is therefore fixed by both actions.

In every case, the involution of one of A²,B²,C² commutes with a and b,
hence with P=⟨a,b⟩. It is also the unique involution of A,B or C,
respectively. This contradicts the center-free conclusion of §2, and
proves the theorem. ∎

## 6. Hypertope consequence and trust boundary

The theorem proves Hou–Feng–Leemans
[Conjecture 3.3](https://arxiv.org/pdf/1901.09034) for every source
hypertope whose derived group P=G′ has abelian Frattini subgroup.
Indeed its distinguished square-rotation groups form a cyclic TPP triple,
and |G:G′|=8; the reduction is proved in phase3_order_bound.md, §3.
Neither a group-order bound nor a nilpotency-class bound is imposed.

This theorem is independent of the marked isobicyclic classification.
It does not imply that every finite 2-group has abelian Frattini subgroup.
The unrestricted cyclic-TPP inequality and the full source conjecture
remain unresolved here. No external peer review or verified publication
priority is claimed. Formal verification, if added separately, must state
its exact scope rather than treating the binary lemma as a formal proof
of the complete group-theoretic theorem.
