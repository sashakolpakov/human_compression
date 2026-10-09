# Cyclic TPP beyond class two: exact reductions and a small-order certificate

9 October 2026. This is a continuation of [the hypertope order-bound proof](phase3_order_bound.md), kept separate because the general cyclic-TPP inequality remains unproved here.

## 1. The auxiliary target and its scope

The target is the following statement: if A,B,C are cyclic subgroups of a finite 2-group P and `abc=1` with a∈A,b∈B,c∈C only when a=b=c=1, then `|A||B||C|≤|P|`.

A proof for all finite 2-groups would prove Hou–Feng–Leemans Conjecture 3.3 through the Frattini reduction already given. A counterexample to this broader statement would not automatically produce a hypertope: an appropriate involutory ambient marking and typed Helly property would still be required.

Targeted primary-literature searches found the standard subgroup-TPP paper [Hedtke–Murthy (2012)](https://arxiv.org/abs/1104.5097), the [2025 abelian-index result](https://arxiv.org/abs/2512.16730), and the [2026 class-two preprint](https://arxiv.org/abs/2602.15796), but no theorem or counterexample specifically settling this cyclic-subgroup statement. This is a limited search result, not a claim that no such theorem exists. General-subgroup counterexamples do not answer the cyclic question.

## 2. Exact structure of a smallest counterexample

The induction in the class-two theorem has two steps that do not use its class assumption. Therefore a smallest counterexample P would have

    A∩Z(P)=B∩Z(P)=C∩Z(P)=1,
    <A,B>=<A,C>=<B,C>=P.

P is two-generated and noncyclic. Burnside's basis theorem gives `P/Φ(P)=C2²`, and generators of A,B,C have the three distinct nonzero images in that quotient. Conversely, choosing one cyclic subgroup in each nonzero Frattini class automatically makes each pair generate P.

For a cyclic subgroup of a finite 2-group, avoiding the center is equivalent to its unique involution not being central. It is also equivalent to having trivial normal core: any nontrivial normal subgroup of a finite p-group intersects its center, while a nontrivial central subgroup is normal.

There is a useful elementary size bound. If A avoids the center and u is its involution, choose g with u^g≠u. Then A∩A^g=1. A maximal subgroup M containing A is normal in P, so it also contains A^g. Thus

    |A|²=|AA^g|≤|M|=|P|/2.                          (5)

The same argument works for cyclic subgroups of a finite p-group, with |P|/p on the right. It is a special elementary instance of the cyclic-core bound, without importing a general permutation-group theorem. On its own it does not bound the product of three orders by |P|.

The class-two theorem and the abelian-index-two lemma exclude those two uniform classes of P entirely.

There is a further exact reduction. A smallest counterexample has ratio **exactly two**. Indeed let M be the maximal subgroup whose image in P/Φ(P) is the line containing A. Then B∩M=B² and C∩M=C². The triple `(A,B²,C²)` still has TPP inside M, and its order-product ratio is half the original ratio. If the original ratio were at least four, it would give a counterexample in the smaller group M. Since all orders are powers of two, a violating ratio is at least two, so it must equal two.

Write the three cyclic orders as α≥β≥γ. Then `|P|=αβγ/2`, and (5) yields `4α≤βγ`. In particular γ≥4. If γ=4, necessarily α=β and `|P|=2α²`. The largest cyclic subgroup A then has a disjoint conjugate A^g, and their product fills a maximal subgroup M of order α². This reduces the smallest-order-factor-four case to an extremal product of two cyclic subgroups. It does not by itself settle that case.

## 3. Exact search through order 256

[phase3_cyclic_tpp_search.g](phase3_cyclic_tpp_search.g) and its [completed GAP transcript](phase3_cyclic_tpp_search.log) implement precisely these reductions. The retained finite input is GAP 4.15.1, SmallGroups 1.5.4.

For each order 8 through 256, the script obtains every nonabelian group whose abelianization has exactly two cyclic factors. It analytically excludes class≤2 and groups with an abelian subgroup of index two, then enumerates every cyclic subgroup avoiding the center whose generator is outside Φ(P). Generator deduplication uses the odd powers of a generator. The subgroups are sorted into the three nonzero Frattini classes.

For a possible violation it is necessary that the product of the largest available cyclic orders in these three classes exceed |P|. No remaining group passes even this necessary size test.

| Order | Nonabelian two-generator groups checked | Groups surviving the center-free three-class size test |
|---:|---:|---:|
| 8 | 2 | 0 |
| 16 | 6 | 0 |
| 32 | 17 | 0 |
| 64 | 50 | 0 |
| 128 | 159 | 0 |
| 256 | 536 | 0 |

Consequently the actual TPP test is never reached. This is informative: within this range, the group-order obstruction occurs before the special cyclic triples can be chosen. The script nevertheless includes an exact test and independent pair-generation verification if a future larger range produces a candidate.

Combining this finite certificate with the smallest-counterexample induction proves the cyclic-TPP inequality for **every finite 2-group of order at most 256**, not just the two-generator groups. A larger-generator counterexample in this range would reduce to a smaller two-generator one, which the certificate excludes.

**Hypertope consequence.** Since `|G′|=|G|/8`, Conjecture 3.3 holds for every hypertope group of order at most `2^11`. The source reported checks through `2^10`; the present certificate extends that range by a structural reduction to a much smaller two-generator problem. It is still a finite consequence, separate from the uniform class and subgroup theorems.

No inference beyond order 256 in the auxiliary problem is made. In particular, the observed stronger condition—center-free cyclic choices in the three Frattini classes already have order product≤|P|—is a possible structural route, not a proved general lemma.

The [certificate manifest](phase3_cyclic_tpp_certificate.json) records the proof, scripts and completed transcripts with SHA256 hashes and reproduction commands. The proof reductions and search coverage received internal agent review, not external peer review.

## 4. A tempting stronger shortcut is false

One might try to show `|A||B|·exp(P/Z(P))≤|P|` for two cyclic center-free generators and then inject C into P/Z(P). [phase3_corefree_bound_probe.g](phase3_corefree_bound_probe.g) and [its transcript](phase3_corefree_bound_probe.log) reject this shortcut at `SmallGroup(32,6)`:

    nilpotency class = 3,
    largest center-free cyclic orders in the three Frattini classes = [2,4,4],
    exp(P/Z(P)) = 4.

Thus the proposed pair inequality would read 64≤32. The product of the three actual class maxima is only 32, so this is neither a counterexample to the cyclic-TPP target nor to the stronger three-class observation above. It pinpoints why replacing the third cyclic subgroup's actual Frattini position by the exponent of the central quotient loses essential information.

The general higher-class cyclic-TPP problem remains unresolved in this work. No finite census or experimental order pattern is presented as a proof for all orders.
