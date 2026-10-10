# Independent audit of the four-family coprime-cover theorem

10 October 2026. **PASS, with no required mathematical or executable correction.** This is an independent proof and finite-arithmetic review of the frozen phase109 package. It is not a historical-priority determination, a current-literature clearance, a new source-compression admission, or a complete Lean formalization.

The reviewed author manifest is `phase109_cover_families_generalization_manifest.json`, SHA256 `33ba4410188b8d6c3b4a0c205d94940155682084294bd858db0637ec3e07c136`; its complete 26,481-byte theorem has SHA256 `ecc09bbf395aa45a5830ba385eb7588e825f7c7b6a074ac5a2345e0d89876a9e`. The associated JSON and review manifest bind the exact programs, model, certificate, ledger, execution evidence and retained inputs. All ten theorem sections, complete author checker and controls, all eight ledger obligations, and every proof interface were read. No mutable probe or discovery presentation is a premise.

## What passes

For each of the four specified two-primary rows Γ2, Γ3, Γ4 and dual Γ4, every β≥5 and every independent sign pair, the theorem constructs regular polytopal covers of the full smallest regular maniplex group G. With source type {p,q,r}, q=2^β, their degrees are respectively 3^34 and 5^34, their types are {3p,q,3r} and {5p,q,5r}, and their end covering kernels have dimensions nine over the corresponding field. The medial covering kernel is trivial.

Each construction has a globally minimal regular polytopal descendant over the original chiral polytope. Its degree over G is a positive power of the chosen prime, with exponent at most 34. These two descendants are distinct. The argument does not select a particular maximal admissible normal subgroup, determine either exponent, prove that either large constructed cover is minimal, or classify every minimal cover. The two explicitly constructed universal relation kernels have product equal to the relation kernel of G, so the join of all finite admissible kernels is that kernel.

Combining this result with the already reviewed, separately bound Γ1 theorem proves the multiplicity assertion for the five specified source families. That combination retains Γ1's odd-prime, α≥2 and equal nonzero-parameter conditions. It does not prove the unrestricted multiplicity statement for arbitrary chiral polytopes, and it does not certify that the family assertion is currently open in the literature.

## Retained source contract and attribution

The source read is the bound Cunningham–Pellicer author version of *Tight chiral polytopes*, arXiv:2009.04566v1. Its Table 2 and Theorems 4.8–4.10 supply the exact presentations, existence, tight order pqr, exact generator orders, intersection property and atomic/local construction results. Proposition 4.2 supplies the normal chirality subgroup. Since q is a power of two, its prime-order conclusion is precisely X=<b^(q/2)> of order two. A normal subgroup of order two is central. The new proof uses this retained centrality; it does not independently reprove the source classification or conceal it inside a finite computation.

The preparation record binds the exact source editions and the prior complete relevant statement/construction reading, including visual inspection of PDF pages 23 and 26–30. This review additionally read the full extracted Proposition 4.2 proof and freshly inspected its entire PDF page 20. The proposition's assumptions hold by the retained atomic chiral source theorems and their chiral local sections. All local signs, exponents and left-side-times-inverse-right-side relator conventions match the primary Table 2. The β=5 case is included; no argument discards a term merely because it vanishes at larger β.

The frozen Cunningham smallest-cover source, Example 3.5 and §4, was reread. It supplies the proposed family multiplicity assertion and an earlier explicit {6,9,6} example with two distinct degree-three minimal covers. That earlier example and its mix/trivial-extension method remain attributed to Cunningham. This audit identifies the five-family scope through the explicitly retained author-version presentations and earlier reviewed Γ1 interface; it does not claim a fresh publisher-edition equivalence audit or an exhaustive search for subsequent results.

Other retained inputs are the regular group/polytope correspondence, the mirror-mix description and universal property of the smallest regular maniplex, recursive string-C recognition, elementary Schreier rewriting, finite linear algebra, and finite normal-subgroup descent. The repository's earlier Γ2 construction supplied the two-edge permutation-module and medial-relation pattern. The present common quotient, transport and two-field derivation are proved here in the repository sense; their historical novelty has not been established. The full phase102/58/66/90 results are contextual, not unproved premises for these four new-family constructions.

## Mathematical proof review

### General pullback and the defect intersection

Section 2 correctly proves generation of the full pullback, not merely containment in an ambient pullback. For n in N∩G_I, choose an ℓ-th root m in the cyclic subgroup <n>. A marked lift (v,m) exists in H_I because that parabolic projects onto G_I. Since m lies in the action kernel, its ℓ-th power is (0,n). Thus the whole standard copy of N∩G_I is present for every I. This uses finiteness and ℓ coprime to |N|; it does not require N cyclic or N contained in a medial subgroup.

For an intersection, equality of the affine projections allows an element of H_(I∩J) to be removed, leaving precisely the standard subgroup N∩G_I∩G_J. Hence

`H_I ∩ H_J = (N ∩ G_I ∩ G_J) H_(I∩J)`

with the standard embedding understood. The resulting criterion is exact in both directions. Inside either retained polytopal source end, all required base intersections already have IP. At the top the required condition is instead N∩(A∩B)≤C. It cannot be replaced by a kernel-dimension calculation. When A∩B=C disjoint-union Cκ, the checked condition πκ∉πC removes the whole unwanted coset and proves N∩(A∩B)=N∩C. Merely showing πκ≠1 would not suffice.

### All-parameter mirror calculation

The mirror α(a)=a^-1, α(b)=a²b=a b^-1 a^-1, α(c)=c is the correct involutory substitution for these rotation marks. It preserves the rotation power and square relations; α(bc)=a(bc)a^-1 follows from the two right-hand square relations. The source x=b^(q/2) is central and nontrivial.

For L2, e² is divisible by q for every β≥5. The displayed inverse conjugation identity follows from the invertibility of 1+e modulo q. Substitution yields a^-1 b^(2e) a=x, including negative e.

For Γ3, the first displayed mirror evaluation substitutes the *L32* relation into b a^-1; the second substitutes *L31* into b^-1 a. The remaining expressions are respectively a^(t+2)b^(2e)a^(t-2) and a^t b^(2e)a^t. Centrality of b^(2e)=x and a^(2t)=1 give x in both cases. These are literal uniform deductions, not sample computations.

The right-end convention has also been checked. With u=c^-1 and v=b^-1, the corresponding left literal words are exactly A0^-1 R_i^-1 A0 for A0=c²b, c^-1b and c b^-1, respectively. This follows by direct free cancellation with the stated LHS/RHS convention. The local substitution λ and the intrinsic right mirror β differ by conjugation by uv; the rotation square relations give β=a^-1α(-)a on b,c. Centrality and order two of x remove the conjugation and inversion. Therefore all applicable right relators also map to x. There is no unexamined sign pair or dependence on a Γ2-only calculation.

### Exact smallest-cover presentation and common quotient

The mirror mix lies in a twisted fiber product over P/<x>, which has order 2pqr. Each additional source relator maps to κ=(1,x), while the first projection is onto P. This proves equality and the exact rotation order; it does not assume a sampled presentation is the mix.

The central-relator presentation has order at most 2pqr because quotienting by its central involution gives exactly P. Its realized map onto the mix attains that bound. The full reflection presentation similarly has order at most 4pqr and attains it in the actual semidirect product. The reflection marking and rotation subgroup are therefore exact.

Both rotation ends contain κ by their local defining relators and are the full preimages of the corresponding source ends. Their cyclic intersections are trivial by the source IP and exact generator orders. Their appropriate mirrors extend them to regular rank-three ends. Removing a common reflection from the odd cosets then gives A∩B=C disjoint-union Cκ, of order 4q. Here κ is central in the rotation mix; centrality in the full group is not assumed.

The literal 16-point model defines a group D of order 256 and type {4,4,4}. All six reduced source relators are the same nonidentity central involution κ0, lying in both ends but outside the medial subgroup. Since t and both e_i are divisible by four and every p,q,r is divisible by four, this model satisfies the *proved exact* full marked presentation for every allowed source parameter. Thus the map G→D is proved surjective uniformly. No assertion that this kernel equals an independently guessed power-normal-closure is needed. Its order and local orders follow by division, and the defect condition supplies the top intersection. Rank reversal transports the entire proof to dual Γ4, without assuming Γ4 is self-dual.

### Affine completeness and all intersections

The right-action affine convention `(v,g)(u,h)=(v^h+u,gh)` is consistent throughout the proof and both programs. The two permutation modules use right cosets <s0>g and <s3>g. The four shifts satisfy involutions and all nonadjacent commutations before quotienting. The killed vector is the actual word (h1 h2)^4, and its whole D-orbit span lies in the generated translation kernel.

The author uses equal-projection differences followed by invariant closure. This is correct: an actual Schreier loop translation is the difference acted on by the inverse base endpoint, and invariant saturation produces the same submodule. The independent program instead computes the actual loop translations directly, spans all Schreier generators for every parabolic, and checks invariance separately. This is a distinct route to completeness of the computed kernel, not a repetition of the author's saturation stopping test.

For a common projected element g, affine fibers meet exactly when the transversal difference lies in L_I+L_J+M. The translation dimension is the dimension of `(L_I+M) ∩ (L_J+M)` modulo M. Equality of this dimension with the common marked kernel proves equality of compatible fibers because that marked subgroup is already included. Every projected element outside the common marked base must be excluded separately. Both the author's complete recursive tests and the independent all-subset tests do this. In particular the eight top forbidden elements are all checked in each field; none is inferred from dimensions alone.

### Transport, minimality and kernel join

The quotient kernel N is a 2-group, so both ℓ=3 and ℓ=5 satisfy the coprime hypothesis. The general theorem proves all generated parabolics are their full pullbacks. This establishes the exact degree ℓ^34, local degrees ℓ^9 and medial degree one, rather than just upper bounds. The source ends have IP and the quotient detects the entire defective coset, so IP transports globally. Adjacent orders are the least common multiples of the orders in the two pullback factors, giving exactly {ℓp,q,ℓr}.

Choose a maximal **H_ℓ-normal** subgroup of the finite covering kernel among those whose quotient remains polytopal. The resulting quotient has no further regular polytopal quotient covering the original P, because every such marked cover factors through its smallest regular maniplex G. Degree one would give the known nonpolytopal G, so the descendant degree is positive. Distinct positive powers of three and five give different orders over the same G, hence different marked polytopes. This proves global minimality of the descendants without asserting the constructed H_ℓ are minimal.

Finally the two universal normal kernels have coprime finite indices in K0=ker(F→G). The quotient by their product is a quotient of both prime-power groups, so it is trivial. All admissible marked regular-cover kernels lie in K0 by the smallest-cover universal property. This proves the claimed join statement. The unrestricted conjecture and a classification of every minimal cover remain outside the result.

## Independent arithmetic and execution evidence

The new `phase112_cover_families_review_check.py` imports no author program. It uses dense integer coefficient tuples with highest-coordinate pivots, lexicographically numbered base permutations and cosets, reverse-generator Schreier transversals, and actual inverse-endpoint Schreier loops. The author's program instead uses sparse dictionaries, least-coordinate pivots, BFS numbering and invariant saturation. All arithmetic is exact over each of F3 and F5 separately.

For each field the new program enumerates only D, independently verifies the six reduced source words and the marked defect, builds all 16 parabolics and tests all 136 unordered subset pairs. It also translates the published coordinates and proves equality of every published kernel/orbit basis space and the quotient classes of all eight published separating remainders. The exact base order, type, end orders and offending intersection are checked. It does not enumerate the huge affine covers.

The fresh final independent replay passes **272** pairs in **1.384399042 seconds**. In both fields, the raw kernel dimension is 65, the killed dimension is 31, the covering dimension is 34, the two end dimensions are nine, and the medial dimension is zero. Exact finite-cover types are {12,4,12} and {20,4,20}. A separate isolated replay using only the nine author public exports plus the independent checker passes in **1.507367208 seconds**, with no private inputs present.

The fresh optimized original author replay passes in **0.095255583 seconds**, reproducing the frozen certificate byte-for-byte (SHA256 `a90f111a307d39a28952d742a402fec1de6b04fc05e2e785787793df30d7ef15`). The author's eight mutation controls and three occupied-output controls were freshly rerun and passed. The independent wrapper additionally rejects changes to the manifest, theorem, author program, model and certificate before producing output; it preserves existing directories, regular files and dangling symlinks. These five independent binding controls and three no-clobber controls all pass. Runtime measurements are evidence for those particular replays, not a performance claim.

## Public reproduction and exact boundary

With the nine exact phase109 exports and the independent checker in one directory, run:

```sh
python3 -O phase112_cover_families_review_check.py --output-dir /path/to/NEW-output
```

The default verifies those nine public bindings and performs the full independent finite calculation. An optional `--private-source-root /path/to/private/study` additionally checks the bound primary, five-family-combination and context-only originals. That optional check is separate and is not required for public arithmetic. Primary PDFs, extracted copyrighted fulltexts and source-page rasters are not included in this review's export allowlist. Public readers can reproduce the all-pair calculation without those files.

The direct finite calculation does not formalize the uniform mirror proof, source classifications, geometric correspondence or minimality argument; those were assessed in the written mathematical review above. Existing Lean results about finite odd quotients or maximal admissible kernels are separate generic interfaces and do not turn this complete theorem into a Lean-certified polytope construction. This package adds no Lean component and no compression ratio.

All frozen author and retained input hashes were verified before and after the fresh calculation. The original phase109 package and public repository were not edited. The complete exact review export allowlist, original bindings and evidence bindings are in the associated manifest. Root admission and publication are separate from this independent PASS.
