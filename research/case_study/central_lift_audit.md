# Independent audit of the central lift

Audited 2026-10-09 against Kong–Feng–Hou–Leemans–Qu, *Chiral polytopes of order 2p^m*, arXiv:2508.20654v1, https://arxiv.org/html/2508.20654 . This is an internal mathematical review, not external peer review or a novelty certification.

## General elementary lift lemma

Let `p` be odd and let `(G;a,b)` be a chiral polyhedron group with `|a|=p²`, `|b|=2p`, `(ab)²=1`, and `<a> ∩ <b>=1`. Suppose there is a homomorphism `φ:G→C_p`, in additive notation, with `φ(a)=1`, `φ(b)=−1`. Let `x` generate `C_(p²)` and put

`H = <A=(a,x), B=(b,x^−1)> ≤ G × C_(p²)`.

Then `H` is a chiral polyhedron group of type `{p²,2p²}` and order `p|G|`.

Proof:

1. The projection `π:H→G` is onto. Every `(g,x^j)` in `H` satisfies `φ(g)=j mod p`, since this is true for A and B and is preserved under products and inverses. Thus `ker π` lies in `<(1,x^p)>`.
2. `B^(2p)=(1,x^(−2p))` generates `<(1,x^p)>`, since p is odd. Hence `K=ker π=<B^(2p)>` has order p and `|H|=p|G|`.
3. Direct-product orders give `|A|=p²`, `|B|=2p²`; also `(AB)²=1`.
4. If `z∈<A>∩<B>`, then `π(z)=1` because the corresponding intersection in G is trivial. Projection is injective on `<A>` because `|A|=|a|=p²`. Hence z=1. This checks the rank-three intersection condition without assuming any blanket preservation property of a mix.
5. Suppose an automorphism α of H simultaneously inverts A and B. It maps `K=<B^(2p)>` to itself. It therefore induces an automorphism of `H/K≅G` simultaneously inverting a and b, contrary to chirality of `(G;a,b)`. The standard rank-three chirality criterion (source Section 2.2) proves that H is chiral.

The argument does **not** assert that K is characteristic under every automorphism. Invariance under the particular hypothetical inversion automorphism is all that is required.

## Application to the omitted even exponents

Take an odd prime p and an even m with `6 ≤ m ≤ p+1`. Put `r=m−2`, so `4 ≤ r ≤ p−1` and r is even. Section 3 and Section 6 Case 1 of the source, with `e=1`, provide the chiral base group G of order `2p^(r+1)=2p^(m−1)` and type `{p²,2p}`. Its generators are `a=βs_1` and `b=s_1^−1 σ`.

The presentation reduces to an elementary abelian subgroup `<s_1,…,s_r>≅C_p^r`, with `s_(i+1)=[s_i,β]`, `β^p=s_r`, and an involutory automorphism σ that fixes s_1 and inverts β. The assignment

`φ(s_1)=1, φ(β)=φ(σ)=0`

defines an epimorphism to C_p: all higher s_i are commutators and map to zero; the power relation β^p=s_r maps to `0=0`; conjugation by σ respects the assignments. Equivalently, every relator in the specialized source presentation maps to zero. It follows that `φ(a)=1`, `φ(b)=−1`.

The lift lemma now gives a chiral polyhedron of order `2p^m` and type `{p²,2p²}`. Its type product is `2p^4 < 2p^m`, so it is non-tight. Combining this with source Theorem 1.4 covers **every m≥5 for every odd prime p**. For p=3 the original theorem already covers every m≥5; the omitted interval is empty. For p=5 the smallest new parameter is m=6 (order 31,250; type `{25,50}`).

## Scope and remaining checks

The reasoning is sound conditional on the cited established base construction. The source explicitly restricts its own even-exponent central extension to `e≥2` (Section 6, Claim 4), while this lift supplies the e=1 gap by increasing the second generator's order from 2p to 2p². This proves an extension of an existence theorem. The accepted manuscript adds a conjectural remark in Section 7, with an apparent tight/non-tight typo documented in the main proof.

Targeted searches found no subsequent paper already asserting the completed existence statement. The author's publication list still lists the paper as forthcoming, but the primary accepted manuscript has now been retrieved from https://amc-journal.eu/index.php/amc/article/download/3716/2232 . Accepted 19 January 2026, its Section 7 on page 20 explicitly leaves this range open. That resolves the version-check concern; independent novelty confirmation remains outstanding.

## Independent normal-form computations

The accompanying `verify_lift_normalforms.py` builds the groups using an elementary abelian module with unipotent action `T=I+N`, an explicit matrix involution `S` satisfying `STS=T^−1`, and the carry relation `β^p=s_r`. It does not use GAP or assume consistency of a supplied finite presentation. Breadth-first enumeration from the two distinguished generators gave:

| p | m | Group order | Generator orders | Product order | Cyclic intersection order | Kernel order |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 6 | 31,250 | 25, 50 | 2 | 1 | 5 |
| 7 | 6 | 235,298 | 49, 98 | 2 | 1 | 7 |

Commands: `python3 research/leemans/verify_lift_normalforms.py` and `python3 research/leemans/verify_lift_normalforms.py --p 7 --r 4`. Both also verify the fiber equation and `K=<B^(2p)>` exactly. These computations support the construction, while the proof above establishes the infinite parameter family. They do not enumerate automorphisms; chirality is certified by the invariant-kernel argument.
