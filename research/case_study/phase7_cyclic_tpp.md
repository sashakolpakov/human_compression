# Cyclic triple products: a metacyclic theorem and the order-512 certificate

10 October 2026. This continues the [structural reduction](phase3_order_bound.md)
and [smallest-counterexample analysis](phase3_cyclic_tpp_exploration.md).
The full hypertope order conjecture remains unresolved.

## 1. A uniform theorem

**Theorem.** Let P be a finite metacyclic p-group, and let A,B,C be cyclic
subgroups with the triple product property (TPP): abc=1, with a∈A,b∈B,c∈C,
implies a=b=c=1. Then

    |A||B||C| ≤ |P|.

Here metacyclic means that P has a cyclic normal subgroup N with cyclic
quotient P/N. The theorem has no nilpotency-class or order cutoff. It also
holds for finite nilpotent groups all of whose Sylow subgroups are metacyclic,
by applying it to each Sylow factor. It does not assert the corresponding
inequality for three arbitrary, possibly noncyclic subgroups.

**Proof.** Choose a counterexample of least order among metacyclic p-groups.
Subgroups and quotients of a metacyclic group are metacyclic: intersect the
cyclic normal subgroup with a subgroup, or take its image in a quotient.
The two induction steps below therefore stay inside the class.

First A∩Z(P)=1, and likewise for B,C. Otherwise a nontrivial central subgroup
D≤A gives a smaller TPP triple in P/D. A relation abc∈D is absorbed into
the A-factor; B,C intersect D trivially. The product/ambient-order ratio is
unchanged, contradicting minimality.

Second every pair generates P. If H=⟨A,B⟩<P, induction on the triple
A,B,C∩H gives |A||B||C∩H|≤|H|. The distinct C/(C∩H) cosets inject into
P/H as a set of cosets, so |C:C∩H|≤|P:H|. Multiplication contradicts the
assumed violation. The argument is symmetric in A,B,C; TPP is invariant
under permuting its three subgroup factors.

Consequently P is noncyclic and P/Φ(P)≅C_p², with the three generators
occupying three different one-dimensional subspaces. Let N be cyclic normal
with P/N cyclic. Every intersection A∩N,B∩N,C∩N is normal in P, because
every subgroup of N is characteristic in N. A nontrivial normal subgroup of
a finite p-group meets its center nontrivially. Thus all three intersections
are trivial.

At least one of A,B maps onto P/N, since their images generate a cyclic
p-group. Relabel it A. Then

    P = N ⋊ A,  N=⟨x⟩≅C_(p^m), A=⟨y⟩≅C_(p^n),
    yxy⁻¹=x^r.

Both m,n are positive. Conjugation embeds A in Aut(N): its kernel centralizes
both N and A, hence is contained in A∩Z(P)=1. The p-part of |Aut(C_(p^m))|
is p^(m−1), so n≤m−1. Also r≡1 mod p, since r has p-power order.

The Frattini subgroup is ⟨x^p,y^p⟩: the commutator x^(r−1) already belongs
to ⟨x^p⟩. Since A and B generate, a generator g=x^s y^t of B has p∤s.
Put |y^t|=p^k. Because B∩N=1, g also has order p^k. In particular k≤n<m.
Its power in the split extension gives the integer congruence

    0 ≡ s(1+R+⋯+R^(p^k−1)) mod p^m,   R=r^t.       (1)

For odd p, R≡1 mod p and the geometric sum in (1) has p-adic valuation
exactly k. For p=2 the same assertion holds when R≡1 mod4. These facts also
hold when k=0 or R=1; an elementary proof is given below. For odd p, (1)
therefore contradicts p∤s and k<m, proving the theorem.

For p=2 choose B or C with even y-exponent t. Such a choice is forced:
their distinct Frattini images are the two lines different from A=(0,1),
namely (1,0) and (1,1). Since r is odd and t is even, R≡1 mod8. The same
valuation argument again contradicts (1). This completes the proof. ∎

The nilpotent extension follows because a cyclic subgroup of a finite
nilpotent group is the direct product of its Sylow intersections. Each
Sylow triple inherits TPP, and the inequalities multiply.

### The elementary valuation input

For odd p and R≡1 mod p, or p=2 and R≡1 mod4, put

    S_k(R)=1+R+⋯+R^(p^k−1).

Then S_0=1 and

    S_(k+1)(R)=S_k(R)·(1+R^(p^k)+⋯+R^((p−1)p^k)).

The second factor has valuation one. For odd p, writing U=R^(p^k)=1+ph
gives Σ_(j=0)^(p−1)U^j≡p mod p² by the binomial theorem and
p | Σj. For p=2, 1+U≡2 mod4. Induction gives v_p(S_k)=k.
No classification of metacyclic groups is retained in the proof.

### Hypertope consequence and exact limitation

For a regular rank-three hypertope in the source conjecture, the earlier
proof identifies P=G′=Φ(G), |G:P|=8, and the TPP triple
⟨(ab)²⟩,⟨(bc)²⟩,⟨(ac)²⟩. Therefore the conjectured bound
|G|≥ord(ab)ord(bc)ord(ac) holds whenever G′ is metacyclic. This covers
arbitrarily high nilpotency class; it neither proves that every G′ is
metacyclic nor eliminates the remaining higher-class cases.

The target is [Hou–Feng–Leemans, Conjecture3.3](https://dipot.ulb.ac.be/dspace/bitstream/2013/287227/5/Hy2g.pdf).
The source defines the all-parameter order conjecture; it does not state the
metacyclic TPP theorem proved here. Searches on 10 October 2026 for the exact
title and for cyclic/metacyclic TPP found no direct earlier statement of this
theorem. This is a bounded search, not verified publication priority.
Relevant comparisons are the standard
[subgroup-TPP algorithms](https://arxiv.org/abs/1104.5097),
the [abelian prime-index bound](https://arxiv.org/abs/2512.16730), and the
[class-two subgroup bounds](https://arxiv.org/abs/2602.15796).
Those broader-subgroup statements have different hypotheses. No infinity
marker or claim of a complete solution is attached to this extension.

## 2. Exact finite extension to order512

[phase7_cyclic_tpp_search.g](phase7_cyclic_tpp_search.g) exhausts the 2,043
rank-two groups of order512, entries2–2044 of GAP SmallGroups1.5.4.
The transcript includes the library's range description, and the script
checks order512 and Frattini index4 for every entry. Catalogue completeness
and that range description are retained finite inputs.

The earlier minimal-counterexample reduction leaves only cyclic subgroups
disjoint from the center, whose generators lie in the three nonzero Frattini
classes. The script first uses the already proved class-two and
abelian-index-two exclusions. It enumerates every remaining element outside
Φ(P), tests whether its unique involution is central, deduplicates cyclic
subgroups by their odd-power generators, and takes the maximum available
order in each of the three classes. A zero maximum means no eligible cyclic
subgroup in that class. No group has product of the three maxima exceeding
512. Thus the final TPP-test branch is never needed.

Together with the frozen smaller-order certificate, this proves the cyclic
TPP inequality for **every 2-group of order at most512**. A hypothetical
counterexample with more generators would reduce to a smaller two-generator
one, so it cannot evade this argument. As |G′|=|G|/8, the hypertope order
conjecture is consequently verified through **|G|=2^12**.

The script does not use the new metacyclic theorem for pruning. That theorem
and this finite extension are separate pieces of evidence. The general
cyclic-TPP inequality for arbitrary 2-groups, and the full hypertope order
conjecture, remain open in this work.

## 3. Verification scope

The [arithmetic checker](phase7_cyclic_tpp_arithmetic.py) enumerates faithful
split cyclic extensions and tests the precise forbidden normal-coordinate
condition used above. It independently checks geometric sums modulo the
normal subgroup order, not a restatement of an asymptotic conclusion.
These finite arithmetic checks support the proof's delicate power formula;
the written induction supplies the all-parameter result. No Lean proof of
the metacyclic theorem or the SmallGroups catalogue is claimed.

The [certificate](phase7_cyclic_tpp_certificate.json) records executed bytes,
counts, dependencies, scope and review status. Historical phase3 artifacts
are unchanged.
