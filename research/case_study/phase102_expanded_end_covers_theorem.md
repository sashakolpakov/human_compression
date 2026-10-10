# An odd-degree cover with enlarged ends for the atomic Γ2 family

10 October 2026. Author theorem package; independent mathematical review and root admission remain separate. No frozen predecessor is changed. The finite construction below is an exact affine calculation over F3, with a standalone program and a complete generated certificate. The passage to every source parameter is a written pullback proof, not interpolation from examples. Historical novelty and comprehensive current-source status have not been established.

## 1. Statement and retained source interface

Take the Γ2 row of Cunningham–Pellicer, *Tight chiral polytopes*, arXiv:2009.04566v1, Table 2/Theorem 4.8. Put q=2^β, with β≥5, and let ε1,ε2 independently be ±1. Its rotation group P has the exact presentation

```text
a^8=b^q=c^8=(ab)^2=(bc)^2=(abc)^2=1,
b a^2=a^2 b^(1+ε1 q/4),   c^2 b=b^(1+ε2 q/4)c^2.
```

The source construction, tightness, unique tight normal forms, marked orders, intersection property, chirality and existence are retained inputs. In particular |P|=64q. This package does not reprove the atomic classification.

Write G for the **full reflection group** of its smallest regular maniplex cover, with marked involutions r0,r1,r2,r3. The reviewed phase58/66 proofs give the following exact interface:

* |G|=256q. Its two end groups A=G012 and B=G123 are regular rank-three string C-groups, each of order 32q. Their common marked medial group C=G12 has order 2q, whereas A∩B has order 4q. Thus G is not polytopal.
* N=<(r1r2)^4> is normal in G, has order q/4, and is contained in C. The marked quotient G/N is the same group of order 1024 for every β and both signs.
* The frozen 128-point model `phase66_coprime_cover_permutation_model.json`, SHA-256 `0247990a79729513799e8fe85d49dec74fade6b32a9aff8746a3fa4c0e8a2338`, represents that marked quotient, denoted below by Gbar. Its two ends have order 128 and its medial group has order eight.
* There is a regular polytopal marked double cover S→G with both ends injective. It is globally minimal over the original chiral polytope: every regular cover of that polytope maps to its smallest regular maniplex, and a degree-two cover of nonpolytopal G has no proper intervening polytopal quotient.

These are substantial retained predecessors, separately reviewed in phase73/74. In particular the uniform marked quotient is a presentation theorem: after b^4=1 is added to the exact mirror-mix presentation, all β/sign dependence disappears. The original source parameters are not inferred from a fixed sample. The standard marked group/polytope correspondence, recursive string C-group recognition, and the smallest-regular-maniplex universal property are retained geometric background.

**Theorem.** For every parameter above there is a finite regular polytopal marked cover H→G with the following properties:

1. Its kernel is elementary abelian of order 3^130, and its full group order is 256q·3^130.
2. Its type is {24,q,24}. Each maximal end projection has kernel of order 3^17; the medial projection is injective.
3. H has a finite quotient Q that is a globally minimal regular polytopal cover of the original chiral polytope and has degree 3^d over G for some 1≤d≤130. Consequently Q is different from S.
4. The two admissible universal relation kernels supplied by H and S have product equal to the relation kernel of G. Hence the join of all finite admissible universal kernels equals that kernel for this Γ2 family.

The explicit cover is H. The proof of part 3 is finite descent; no particular minimal descendant Q or value of d is selected by the certificate. It does prove existence of a second minimal cover for every stated parameter. It does not classify all minimal covers or address the other 2-primary source families.

The earlier exact classification of covers with both ends injective is consistent with this result. H enlarges both ends, and any odd-degree minimal descendant must enlarge at least one end if that classification is used. The proof here needs only the earlier double cover, not the later classification.

## 2. Exact affine kernel and intersection lemmas

Let D be a finite marked group acting on a finite-dimensional vector space E over Fp on the right. Use pairs with multiplication

```text
(v,g)(u,h)=(v^h+u,gh).
```

Thus the pair denotes the group element g followed by the translation v. Choose marked lifts h_i=(v_i,r_i), and let T be their generated subgroup. Its projection onto D is assumed surjective.

For a set of marks I, let D_I be the base subgroup and T_I the corresponding generated lift subgroup. Choose one word in those marks representing each g∈D_I, giving a chosen lift (t_I(g),g). Whenever appending a generator gives another word above g, the difference between the resulting vector and t_I(g) is an actual translation in T_I. Let L_I be the span of all these differences and all their images under the action of D_I.

**Kernel lemma.** The kernel of T_I→D_I is exactly L_I. The vectors occurring above a fixed g∈D_I are exactly t_I(g)+L_I.

**Proof.** The quotient of two actual lifts with the same base element is their vector difference, so every initial difference is in the kernel. Conjugation of a translation by a lifted generator is the prescribed linear action; thus the invariant span L_I lies in the kernel. Conversely the usual word rewriting along the chosen representatives expresses a word with trivial base image as a product of conjugates of these differences. This is elementary Schreier rewriting: insert the chosen representative and its inverse after each prefix. Hence every kernel translation lies in L_I. The fiber assertion follows by multiplication by kernel translations. ∎

This is a completeness argument. Computing an unclosed span of a few relations would not be enough. The program saturates every span under its actual parabolic generators and verifies invariance.

Now let M be a D-invariant subspace of L=L_all, and pass to the quotient by M. Write Lbar_I=(L_I+M)/M. For two mark sets I,J and K=I∩J, the common fiber over g∈D_I∩D_J is nonempty exactly when

```text
t_I(g)-t_J(g) ∈ L_I+L_J+M.                       (1)
```

If it is nonempty its translation dimension is

```text
dim(L_I+M)+dim(L_J+M)-dim(L_I+L_J+M)-dim(M).       (2)
```

Indeed this is the intersection of two affine cosets of the vector subspaces Lbar_I,Lbar_J. The common marked subgroup T_K/M∩T_K is already included in that intersection. Therefore the exact parabolic intersection property for this pair follows if (1) fails at every g outside D_K, and (2) equals dim(L_K+M)-dim(M). Conversely those conditions are necessary. This is the expanded-end version of the kernel-intersection mechanism: local kernels are allowed, and are measured explicitly rather than assumed trivial.

## 3. A fixed permutation module and four lifts

From now on p=3 and D=Gbar is the bound group of order 1024. Put

```text
E=F3[{<r0>g:g∈D}] ⊕ F3[{<r3>g:g∈D}].            (3)
```

Each summand has 512 basis vectors. Label its basis vectors e_(<r0>g) and f_(<r3>g), respectively. D acts on these right cosets by right multiplication. This gives a well-defined permutation action on E, with dimension 1024. It is not an action inferred only from abstract generator relations.

Use the four shift vectors

```text
v0=0,
v1=f_(<r3>)-f_(<r3>r1),
v2=-e_(<r0>)+e_(<r0>r2),
v3=0.                                             (4)
```

Let T≤E⋊D be generated by (v_i,r_i). Each is an involution: its shift is negated by its marked involution. For the nonadjacent pairs, v2 is r0-fixed, v1 is r3-fixed, and the remaining outer pair has both shifts zero. The base marks commute for those pairs. Thus all three string commutations hold before any quotient. The program also checks these literal vector equations.

Let c be the translation obtained by evaluating the word (h1h2)^4. Its base element is 1 because r1r2 has order four in D. Let

```text
M=span_F3{c^g:g∈D}.                              (5)
```

The vector c belongs to L=ker(T→D); since L is D-invariant, M≤L. No arbitrary choice of a subspace or complement is involved. Put

```text
Hbar=T/M ≤ (E/M)⋊D.                              (6)
```

This quotient preserves the marked epimorphism to D and all involution/string relations.

The exact finite calculation yields:

| Quantity | Value |
|---|---:|
| dim L | 257 |
| dim M | 127 |
| dim ker(Hbar→D) | 130 |
| type of Hbar | {24,4,24} |

All values follow from the standalone program, whose row operations take place exactly in F3. The certificate includes the full row bases of L and M, the literal vector c, the raw local-kernel bases, and all nonzero remainders needed to exclude the unwanted projected intersections. In its deterministic zero-based edge enumeration, c has the following nonzero coordinates:

```text
(0,2),(1,1),(2,1),(5,2),(7,2),(13,1),(17,1),(29,2),
(512,2),(514,1),(515,1),(519,2),(520,2),(528,1),(531,1),(547,2).
```

Here 2 denotes −1 in F3. This coordinate list is an illustration of the word evaluation, not a substitute for its coset definition (3)–(5).

## 4. Complete recursive intersection checks

Apply the kernel lemma to the eight required parabolics, and then (1)–(2) after quotienting by M. The exact results are:

| I, J, K | Base orders D_I, D_J, D_K | Base intersection order | Quotient kernel dimensions Lbar_I, Lbar_J, Lbar_K | Intersection kernel dimension | Excluded base elements outside D_K |
|---|---|---:|---|---:|---:|
| 012, 123, 12 | 128, 128, 8 | 16 | 17, 17, 0 | 0 | 8 |
| 01, 12, 1 | 16, 8, 2 | 2 | 1, 0, 0 | 0 | 0 |
| 12, 23, 2 | 8, 16, 2 | 2 | 0, 1, 0 | 0 | 0 |

For each of the eight forbidden base elements in the first row the certificate gives the nonzero remainder of t_012(g)-t_123(g) modulo L_012+L_123+M. These are all such elements, not selected tests. The equalities of dimensions prove equality of the full intersection fibers, not just the separation of the original base defect.

The second and third rows prove that both rank-three ends have their required cyclic intersections. Each rank-two group on two nontrivial involutions is dihedral with the usual rank-two intersection property; distinctness and nondegeneracy are inherited from their base images. The first row gives the required end intersection. Along with the checked string commutations, recursive recognition now proves that Hbar is a string C-group. Thus it is a finite regular polytope group.

The adjacent product orders are checked by literal word evaluation modulo M, for every lower positive exponent up to the attained orders: they are exactly 24,4,24. The two end kernel orders are 3^17 and the medial kernel is trivial. Its full order is 1024·3^130. This is an exact finite construction, despite that large cardinality: the program enumerates only the base group and computes the complete translation kernels by the proved Schreier-span lemma.

## 5. Pullback to every source parameter

Let the full source G act on V=E/M through G/N≅D. Take the same four shifts (4), interpreted in V, and let

```text
H=<(v_i,r_i):0≤i≤3> ≤ V⋊G.                       (7)
```

Its projection onto G is onto. The natural ambient map V⋊G→V⋊D has kernel the standard N={(0,n):n∈N}; this is a normal subgroup, since N is normal in G and acts trivially on V.

**Standard-kernel inclusion.** H contains the entire standard N. To prove this, take n∈N and an arbitrary lift (v,n)∈H. Since N acts trivially on V and V has exponent three,

```text
(v,n)^3=(0,n^3).
```

The cube map on the cyclic 2-group N is bijective. Taking a lift above a suitable cube root of each n proves (0,n)∈H. The same proof works for any generated parabolic H_I for which N≤G_I, because its projection onto G_I is onto.

Consequently H is the full preimage of Hbar. Its kernel over G is exactly the same elementary abelian group L/M of dimension 130, and its order is |G|·3^130. In particular the full-preimage assertion is proved from generation; it is not inferred only from the order of an image.

Since N≤C≤A,B, each of H012,H123,H12 is the full preimage of its corresponding subgroup in Hbar. Their intersection is therefore the full preimage of Hbar12, namely H12. Moreover H12→G12 is injective because the corresponding medial kernel in Hbar is trivial.

It remains to check the two local rank-three intersections; top-end equality alone would not suffice. The old end A is polytopal, so

```text
N∩G01 ≤ G12∩G01=<r1>.
```

But N consists of rotations in <r1r2>, whereas <r1> is a reflection subgroup, so this intersection is trivial. The analogous argument gives N∩G23=1. Therefore H01→Hbar01 and H23→Hbar23 are injective: their kernels lie in the standard N and project into these trivial base intersections. Both maps are onto by the marking.

An element of H01∩H12 maps in Hbar into <h1>, by the already proved rank-three intersection there. Injectivity on H01 identifies it with that same marked element, so H01∩H12=<h1>. Similarly H12∩H23=<h2>. Recursive recognition proves that both ends and the whole H are polytopal.

The first and last adjacent product orders stay 24, because the corresponding pair subgroups map isomorphically to Hbar01 and Hbar23. The middle order is q because H12≅G12. Thus H has type {24,q,24}. The end projection kernels to A and B have dimension 17, as in Hbar, whereas the medial projection remains injective. This proves parts 1 and 2 for every β and sign pair, using only the one exact fixed-group certificate and the uniform source quotient.

## 6. A different minimal descendant and global join-density

Let K=ker(H→G), so |K|=3^130. Among normal subgroups J≤K for which H/J is polytopal, choose an inclusion-maximal one. The set is finite and nonempty, since J=1 is allowed. Put Q=H/J. Its degree over G is 3^d for some 0≤d≤130; d cannot be zero because G is not polytopal.

This Q is globally minimal as a regular cover of the original chiral polytope. Indeed any further regular polytopal quotient covering that original polytope must map to its smallest regular maniplex G. It is also a quotient of H, and therefore corresponds to a normal subgroup J′ with J≤J′≤K. Maximality forces J′=J. Finiteness ensures this argument accounts for every quotient of Q, with no unresolved infinite descent.

The known minimal cover S has degree two over G. If Q had a marked epimorphism to S over G, its kernel over G would map onto the order-two kernel of S→G. The order two would then divide 3^d, impossible. Thus Q is a different minimal regular cover. In fact their group orders already differ in their odd prime divisors, so there is no accidental identification caused solely by a permutation of the types. No claim is made to have selected or enumerated all possible Q.

For the join assertion, take the universal group F on the four involutions and the nonadjacent string commutations. Let K0 be the relation kernel of F→G, and let J_H,J_S be the relation kernels of its marked maps to H and S. Both are finite-index admissible normal subgroups contained in K0. The index

```text
[K0:J_H J_S]
```

divides [K0:J_H]=3^130 and [K0:J_S]=2. Hence it equals one and J_H J_S=K0. Every finite admissible universal kernel covering the original polytope lies in K0 by the smallest-regular-maniplex property; the join of all of them is therefore exactly K0. This proof does not need the mix H⋄S to be polytopal and makes no inference interchanging kernel joins with intersections.

## 7. Certificate scope, attribution and unresolved questions

The standalone `phase102_expanded_end_covers_check.py` uses the standard library only. It rebuilds D from the bound permutations, both right-coset actions, the four shifts, all involution/string relations, every necessary parabolic Schreier kernel and invariant closure, the orbit span of the literal medial relation, all three recursive intersection tests, and the exact adjacent orders. It uses integer arithmetic modulo three, with no numerical rank tolerance, GAP simplifier, residual-p assumption or enumeration of the enormous affine group.

Its coefficient bases and all eight separating remainders appear in the generated certificate. They are required finite proof data, not optional illustrative samples. The accompanying code, certificate, report and controls are charged inputs to this theorem. Neither this manuscript nor the certificate adds a manuscript to a compression count or establishes a length ratio.

The construction was prompted by the root's suggestion to release all local relations in the right-angled Coxeter group and examine its finite homology quotients. The edge module (3) is also the edge-chain module for the amalgam V4(02) *_(<r0>) V4(03) *_(<r3>) V4(13). That interpretation explains the construction but is not needed for the affine proof above. A surface-group interpretation after the medial relation was considered during discovery and is not a retained premise or proved claim here. The exploratory F2/F5 calculations and arbitrary complement probes are excluded; only F3 and the literal relation (5) are used in the theorem.

The complete relevant §4 passage of Cunningham's July 2023 author version, published in JCTA204 (2024),105839, was reread from the frozen primary extraction. It gives one finite two-minimal-cover example and proposes analogous multiplicity for the five tight families of Example 3.5. The construction, prime-degree minimality mechanism and broader multiple-minimal-cover question have that earlier attribution. The present exact Γ2 affine construction and uniform pullback are repository derivations; priority has not been established. The older bounded source/status checks in phase44/55/72 remain limited searches, not proof of current openness.

The result concerns the full valid Γ2 family of type {8,2^β,8}, with all four signs and β≥5. It supplies an additional finite cover and proves existence of a second minimal descendant. It does not classify the minimal descendants, settle multiplicity for Γ3 or Γ4 and its dual, or prove the general conjecture for arbitrary polytopes. Independent review remains required before admission of this author package.

Replay to a fresh output directory, preserving the distributed certificate:

```text
python3 -O research/leemans/phase102_expanded_end_covers_check.py --expected-certificate research/leemans/phase102_expanded_end_covers_certificate.json --output-dir /private/tmp/NEW-phase102-replay
python3 -O research/leemans/phase102_expanded_end_covers_controls.py --output-dir /private/tmp/NEW-phase102-controls --successful-replay-dir /private/tmp/NEW-phase102-replay
```

The checker rejects a changed model or a mismatching expected certificate before creating its output directory. Existing files, directories and dangling symlinks are refused. Explicit exceptions keep all checks enabled under optimized Python. The author controls additionally mutate a shift, the medial word, a subspace basis, a kernel dimension and a separating remainder; all are rejected. They check integrity of the exact regeneration interface, not a substitute for independent mathematical review.
