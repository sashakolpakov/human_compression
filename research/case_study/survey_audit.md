# Leemans survey audit and a rigorous PSL(4,q) obstruction

Audit date: 2026-10-09. This is research work in progress. No open conjecture is claimed solved here. “No resolution found” records a literature search, not a proof that no resolution exists.

## Which survey conjectures survive the audit?

The source is Dimitri Leemans, *String C-group representations of almost simple groups: a survey*, arXiv:1910.08843v2 (2020); published in Contemporary Mathematics 764 (2021), 157–178. [Full text](https://arxiv.org/html/1910.08843v2).

| Survey item | Statement, paraphrased | Audited status |
|---|---|---|
| Conjecture 1 | For fixed defect i and n ≥ 2i+3, the count of rank n−i string C-groups for S_n stabilizes. | **Solved**, 2024. |
| Conjecture 2 | For every odd prime power q, PSL(4,q) has maximum string C-group rank 4. | **No resolution found**; retain as a candidate. |
| Conjecture 3 | A_11 alone among finite simple groups has a noninterval string C-group rank spectrum. | **No resolution found**; recent literature still calls A_11 the only known example. |

Other potentially substantial survey targets: maximum ranks for almost simple groups with socle PSL(3,q) or PSL(4,q) (Problems 5, 7), characteristic-two orthogonal/symplectic groups (Problem 9), and small Ree C-groups without the string restriction (Problem 15). The enumeration questions concern symmetric/alternating groups, PSL(2,q) extensions, Ree/Suzuki groups, and sporadic groups. Problem 10 asks the rank-three count for O’Nan; its published resolution must not be missed.

Significance judgment: Conjectures 2 and 3 concern possible dimensions of regular polytopes with prescribed simple symmetry groups. Conjecture 3 is the broader structural question; Conjecture 2 is a sharply formulated infinite-family test case. These are significant within abstract regular polytopes and finite-group generation, not claims of universal prominence across mathematics.

## Sources that change the old survey picture

1. **Cameron–Fernandes–Leemans**, *The number of string C-groups of high rank*, Advances in Mathematics 453 (2024), 109832, [DOI](https://doi.org/10.1016/j.aim.2024.109832), [arXiv PDF](https://arxiv.org/pdf/2212.12723). Theorem 1.1 proves that for each κ ≥ 1 there is c_κ with |Σ^κ(n)| = c_κ whenever n ≥ 2κ+3. Here Σ identifies isomorphism and duality. Thus survey Conjecture 1 is not an open target. The paper explicitly identifies its purpose as proving that conjecture.

2. **Leemans–Mulpas**, *The string C-group representations of the Suzuki, Rudvalis and O’Nan sporadic groups*, Art of Discrete and Applied Mathematics 5(3) (2022), #3.09, [DOI](https://doi.org/10.26493/2590-9770.1405.4ce). The author's [current publication list](https://leemans.dimitri.web.ulb.be/papersbyyear.html) records the published three-group title. Jessica Mulpas's 2024 dissertation summary states that all string C-group representations of these three groups were computed, along with rank-three representations for Co_2 and Fi_22: [BMS thesis announcement](https://bms.ulb.ac.be/data/uploads/bmsncm/bmsne149.pdf), page 7. Crucial trap: [arXiv:2005.05372](https://arxiv.org/abs/2005.05372) still has a 2020 first version treating only Suzuki and Rudvalis. Do not use that older abstract to infer O’Nan remains open. The precise O’Nan numerical count was not retrieved in this audit.

3. **Fernandes et al.**, *String C-group representations of transitive groups: a case study with degree 11*, [accepted manuscript](https://oro.open.ac.uk/100498/1/100498.pdf). This recent primary paper calls A_11 the unique known group with a noninterval rank spectrum, and gives a theoretical classification related to its missing ranks 4 and 5. This supports continuing to investigate Conjecture 3; it does not prove the conjecture's present open status absolutely.

4. **Brooksbank**, *On the ranks of string C-group representations for symplectic and orthogonal groups*, [arXiv:1912.05512](https://arxiv.org/abs/1912.05512), [PDF](https://arxiv.org/pdf/1912.05512). Theorem 1.1 gives rk(PSp(4,q)) = {3,4,5} for q ≠ 3 and the empty set for q = 3. Its Figure 2 lists only {3,4} ⊆ rk(PSL(4,q)) for odd q. This resolves a low-dimensional instance of the orthogonal/symplectic rank question. Do not treat a displayed high-dimensional construction range as a proof of a global maximum without checking the underlying theorem.

5. **Leemans–Vandenschrick**, *On simple groups that admit a string C-group representation*, Art Discrete Appl. Math. 9 (2026), #1.07, [accepted PDF](https://dipot.ulb.ac.be/dspace/bitstream/2013/397490/3/simpleGroups6.pdf). Theorem 1.1 completes the existence/nonexistence classification at arbitrary rank. This classifies whether a simple group admits any representation, not its full rank spectrum; it therefore does not dispose of Conjecture 3.

The author's publication list was checked through its 2026 entries, with targeted searches for PSL(4,q), maximal rank, and subsequent string C-group papers. No later resolution of survey Conjecture 2 was found.

## Concrete proof attempt for PSL(4,q)

The following obstruction is proved here explicitly. It is a useful reduction and may well be standard; no novelty claim is made. It prevents a natural but unsuccessful attempt to extend the known rank-four construction.

**Proposition.** Let q ≥ 5 be odd. In the rank-four string C-group constructions of Brooksbank–Leemans whose first three generators generate the natural subgroup Ω_4^−(q) ≅ PSL_2(q²), no nonidentity element of PGL_4(q) can be adjoined as a fifth generator at the right endpoint while retaining the first four generators and the string commuting relations.

This is stronger than saying the intersection property fails: the required commuting relations already make the new generator trivial.

The source for the construction and subgroup identity is Brooksbank–Leemans, *Polytopes of large rank for PSL(4,F_q)*, Journal of Algebra 452 (2016), 390–400, Theorem 5.1(ii). [Publisher DOI](https://doi.org/10.1016/j.jalgebra.2015.11.051), [author-uploaded full text](https://www.researchgate.net/publication/293026803_Polytopes_of_large_rank_for_PSL4Fq), [institutional record](https://digitalcommons.bucknell.edu/fac_journ/1204/).

### Step 1: a general projective-centralizer lemma

Let H ≤ GL(V) be perfect, meaning H = [H,H], and suppose C_GL(V)(H) consists only of scalars. Then its projective image has trivial centralizer in PGL(V).

Indeed, if [X] centralizes the image of H, there are scalars χ(h) satisfying

    X h X^(-1) = χ(h) h,  h ∈ H.

Multiplication gives χ(hk) = χ(h)χ(k), so χ is a homomorphism from H to the abelian scalar group. Perfection makes χ trivial. Thus X centralizes H linearly and is scalar; [X] is the identity.

Consequently, in any rank-r string group with r ≥ 5, the subgroup generated by ρ_0, ρ_1, ρ_2 cannot be the projective image of such an H: the nontrivial generator ρ_4 would centralize it. This necessary condition is independent of the intersection property.

### Step 2: a self-contained scalar-centralizer computation

Put F = F_q and K = F_(q²), and realize the natural four-dimensional F-module for Ω_4^−(q) as the Hermitian 2×2 matrices

    V = { [[x,z],[z^q,y]] : x,y ∈ F, z ∈ K }.

The group SL_2(K) acts by M ↦ A M A^(qT). The image H has kernel {±I}, preserves det(M), and is the Ω_4^−(q) subgroup used in the construction.

This image is perfect: SL_2(K) is generated by upper and lower elementary unipotents, and each such unipotent is a commutator. For a ∈ K* with a² ≠ 1,

    [diag(a,a^(-1)), U(s)] = U((a²−1)s),

using [D,U]=DUD^(-1)U^(-1); the analogous identity handles lower unipotents. As s varies, these cover both elementary root groups. Images of perfect groups remain perfect.

Extend scalars to an algebraic closure of F, where the coordinates x, y, z, w=z^q become four independent linear coordinates. Choose a generator a of K*. The operator induced by diag(a,a^(-1)) has respective eigenvalues

    a^(q+1), a^(-q-1), a^(1-q), a^(q-1).

These four eigenvalues are distinct for q ≥ 5. This follows by checking the six exponent differences modulo q²−1: the possible absolute differences are 2, 2q, 2(q−1), and 2(q+1), all nonzero and less than q²−1 when q ≥ 5.

Thus any linear operator T commuting with H is diagonal in the coordinate eigenbasis e_x,e_y,e_z,e_w. The image of U(1) sends

    e_y ↦ e_x + e_y + e_z + e_w.

Commuting T with U(1) then equates all four diagonal entries of T. Hence T is scalar over the algebraic closure, and a commuting F-linear T is a scalar from F.

Step 1 now gives C_PGL_4(q)(H) = 1.

### Step 3: apply the string relation

An appended fifth generator ρ_4 must commute with ρ_0, ρ_1, and ρ_2 because their index distances from 4 exceed 1. It therefore centralizes H projectively. The preceding calculation forces ρ_4 = 1, contradicting its required order 2. This proves the proposition.

### What remains unresolved

This does **not** establish that every rank-five string C-group for PSL(4,q) would contain that particular Ω_4^−(q) endpoint triple. Other rank-three endpoint subgroups can have nontrivial projective centralizers. A full proof must rule out all such alternative configurations, and also must rule out higher ranks rather than assume rank reduction always succeeds. The published rank-reduction theorem has hypotheses; it is not an unconditional equivalence between existence at ranks 5 and above.

A viable next exhaustive search should enumerate compatible endpoint triples inside involution centralizers, prune triples with trivial projective centralizer, and then test generation and the intersection property. Computing more extensions of the existing Ω_4^−(q) construction would be wasted effort: the proposition excludes them uniformly for all q ≥ 5.

## Independent audit of the separate central-lift result

I independently reviewed `central_lift_audit.md` against the **accepted manuscript** of Kong–Feng–Hou–Leemans–Qu, *Chiral 3-polytopes of order 2p^m*, received 2025-08-28 and accepted 2026-01-19, DOI [10.26493/1855-3974.3716.b64](https://doi.org/10.26493/1855-3974.3716.b64), using the retrieved text `sources/chiral_accepted.txt`.

The general lift is sound: if a,b generate a chiral polyhedron group G with orders p²,2p and a character φ(a)=1, φ(b)=−1 in C_p, the subgroup generated by (a,x),(b,x^−1) in G×C_(p²) has kernel of order p over G. The subgroup generated by the first generator injects under projection, which proves the required cyclic intersection remains trivial. A hypothetical simultaneous-inversion automorphism preserves the kernel because that kernel is generated by the (2p)-th power of the second generator. It would descend to the forbidden simultaneous inversion on G. This does not require the kernel to be globally characteristic.

For each even target exponent 6 ≤ m ≤ p+1, set the source's base exponent to m−1, take e=1 and r=m−2. Then 4 ≤ r ≤ p−1 is even. The accepted source's Section 3 presentation really does specialize to s_1,...,s_r of order p, higher s_i trivial, β^p=s_r, and the usual commutator chain. Sending s_1 to 1 and β to 0 defines a map to C_p: every power relation maps to zero, every commutator maps to zero, and the last relation has binomial coefficients divisible by p. The involution σ fixes s_1 and inverts β, so extending it by φ(σ)=0 also respects every relation. Thus φ(a)=1 and φ(b)=−1 for the accepted paper's a=βs_1 and b=s_1^−1σ. This checks the key hypothesis of the lift without extrapolating the original even-exponent construction.

The resulting examples have order 2p^m and type {p²,2p²}. Since m ≥ 6, the type product 2p⁴ is strictly smaller than the group order; these are non-tight. Together with the accepted paper's Theorems 1.1–1.4, this yields the exact **existence criterion for non-tight chiral polyhedra of order 2p^m: m ≥ 5, for every odd prime p**. This is a specialist extension of a recent existence theorem, not a solution of the survey's simple-group rank conjectures, not a classification of all groups or all polytopes of these orders, and not yet externally peer reviewed.

There is a wording trap in the accepted paper's concluding Section 7: it literally conjectures that *tight* examples exist in the omitted range, while its Theorem 1.4 concerns non-tight examples and its introduction already cites tight examples covering the relevant orders. The surrounding context strongly suggests a missing “non-”, but that is an inference. Therefore describe the result as filling the explicitly omitted non-tight existence range, and mention the wording issue if calling it a conjecture solution.

No further mathematical gap was found in this independent audit. This audit does not certify novelty against all preprints or unpublished work.
