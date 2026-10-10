# The universal complement group is a free product

10 October 2026. Author derivation; independent review is a separate admission gate. This manuscript preserves the frozen phase83/86 theorem and provides a stronger structural description of its one fixed group. It makes no historical-priority claim and does not admit a new source manuscript to a measured compression assembly.

The universal complement group for the Γ2 family is

\[
U\cong F_{15}*(C_2\times C_2).
\]

The marked obstruction is exactly one nontrivial involution of the displayed Klein-four factor. The isomorphism is supplied in both directions, checked directly against all 1024 original relations, and does not use a GAP presentation simplifier as a proof input. The fixed group of order 1024 acts faithfully on this free product by explicit automorphisms. A canonical finite quotient also yields, uniformly in the source family, a regular polytopal cover of degree four and a degree-two quotient. A coset-complex argument identifies the degree-four group as the universal completion with these exact local ends, so these are the only two polytopal marked covers with injective ends. No assertion of historical novelty or of uniqueness among covers with different local ends is made.

## 1. Exact presentation and retained inputs

Let \(\bar G\) be the marked permutation group on 128 points in the frozen `phase66_coprime_cover_permutation_model.json`, SHA-256
`0247990a79729513799e8fe85d49dec74fade6b32a9aff8746a3fa4c0e8a2338`.
Its four permutations represent \(r_0,r_1,r_2,r_3\), acting on the right. It is transitive of order 1024; the stabilizer of 1 is exactly \(\bar C=\langle r_1,r_2\rangle\), of order eight. The marked word \(z=[(r_2r_3)^2,r_1r_2]\) sends 1 to 40. The orbit of \((1,2,39,77)\) consists of 1024 distinct quadruples.

Define \(U\) on generators \(t_1,\ldots,t_{128}\), with the relation

\[
t_d^{-1}t_c t_a^{-1}t_b=1
\tag{1}
\]

for each quadruple \((a,b,c,d)\) in that orbit. Its marked defect is \(\delta=t_1^{-1}t_{40}\). Rows are indexed from zero in lexicographic order of the quadruples. The action \(t_i^g=t_{i^g}\) preserves the relations.

The source is Cunningham–Pellicer, *Tight chiral polytopes*, arXiv:2009.04566v1, Table 2 row Γ2 and Theorem 4.8. Its presentation, existence, tight order, normal form, marked orders and intersection property remain borrowed inputs. The parameters are \(\beta\ge5\), \(q=2^\beta\), and the two independent signs. The reviewed phase58/66 proofs identify its smallest regular maniplex \(G\), of full group order \(256q\), and prove

\[
N=\langle(r_1r_2)^4\rangle\trianglelefteq G,
\qquad N\le C=\langle r_1,r_2\rangle,
\qquad G/N\cong\bar G.
\]

This is a uniform marked-presentation identification, not an extrapolation from finitely many parameters. The phase83 theorem with its required conjugation erratum, independently reviewed in phase86, proves the universal complement criterion and explains why its group is exactly (1) for every parameter. These remain explicit dependencies.

Classical facts retained here are the elementary elimination rule for group presentations, free groups and free products with their reduced-word normal form, semidirect products, Schreier generation of a finite-index kernel, and recursive string C-group recognition. No classification of finite groups, GAP Tietze routine, truncated p-quotient, or numerical matrix rank is used to prove the structural result.

## 2. A reversible reduction to seventeen generators

The complete original-relation trace is `phase83_word_elimination.json`, SHA-256
`d6cdcab4ea0bfd9a9a75255d5a1da0a1a589306c803d330b0a7a7b659ab86c17`.
The new checker independently replays its 111 eliminations, without importing the trace generator or earlier checker.

Each step chooses a relator in which a generator \(v\) occurs exactly once. A relation \(A v B=1\) solves \(v=A^{-1}B^{-1}\); a relation \(A v^{-1}B=1\) solves \(v=BA\). Neither \(A\) nor \(B\) contains \(v\). Substituting this expression into every other relation, deleting the solved relation, and eliminating \(v\) is reversible: a solution on the remaining generators extends uniquely to a solution of the old presentation. Freely trivial relations may be deleted. Thus these operations prove an isomorphism, not only the implication used by phase83.

The surviving generator indices are

```text
1,2,3,4,5,6,7,8,9,10,12,14,16,19,21,25,32.
```

There are 512 freely nonempty remaining relators. The exact expansion \(R_i\) of every original \(t_i\) in these seventeen generators is produced by applying the solved substitutions in order. All 128 expansions are listed in `original_generator_survivor_expansions` in the certificate. The old generators and these expansions correspond under the reversible elimination isomorphism.

## 3. Explicit free-basis change and the three surviving laws

Retain the following fifteen free generators in the indicated order:

\[
(f_1,\ldots,f_{15})
=(t_1,t_2,t_4,t_5,t_6,t_8,t_9,t_{10},t_{12},t_{14},
t_{16},t_{19},t_{21},t_{25},t_{32}).
\]

Set

\[
X=t_6^{-1}t_7,
\qquad Y=t_1^{-1}t_3t_{12}^{-1}t_6.
\tag{2}
\]

This is an invertible change of basis in a free group of rank seventeen. The inverse substitutions are

\[
t_7=t_6X=f_5X,
\qquad t_3=t_1Yt_6^{-1}t_{12}=f_1Yf_5^{-1}f_9,
\tag{3}
\]

and all other survivors are the displayed \(f_i\). Both composites are freely the identity on all seventeen generators. The checker verifies these 34 literal free-word identities before imposing any relation on \(X,Y\).

Three of the 512 remaining relations become, after the substitution (3),

| Original row | Exact transformed relation |
|---|---|
| 30 | \(f_7^{-1}f_1Y^2f_1^{-1}f_7=1\) |
| 67 | \(f_9^{-1}f_5X^2f_5^{-1}f_9=1\) |
| 176 | \(Y^{-1}X^{-1}YX=1\) |

Hence they imply \(X^2=Y^2=1\) and \([Y,X]=1\). Their original quadruples, final seventeen-generator words, transformed words and conjugating prefixes are all recorded explicitly in the certificate. There is no right-conjugation ambiguity in the displayed products.

Conversely, **every one** of the 512 transformed relations reduces to the identity using only

\[
X^2=Y^2=[X,Y]=1.
\tag{4}
\]

This is checked by exact free-product normal forms. Free letters \(f_i^{\pm1}\) cancel only with adjacent inverses. A contiguous Klein-four syllable is one of \(X,Y,XY\), encoded by its two bits; adjacent such syllables multiply by bitwise addition modulo two, with the zero syllable deleted. These are the reduced-word rules for \(F_{15}*(C_2\times C_2)\). They give a unique normal form by the classical free-product normal-form theorem. They do not commute a free generator past \(X\), \(Y\), or another free generator.

It follows in both directions that the normal closure of the 512 transformed relations equals the normal closure of (4). In particular, no untested relation on the fifteen \(f_i\) has been dropped.

**Theorem 1.** The group (1), with its specified marking, is isomorphic to \(T=F_{15}*(C_2\times C_2)\), and \(\delta\) maps exactly to \(X\).

**Proof.** The forward map \(\Phi:U\to T\) sends \(t_i\) to the normal form of the expansion \(R_i\) after (3). All 128 images appear in `original_generator_target_normal_forms`; the longest has length ten in the certificate encoding. Independently of the seventeen-generator comparison above, the checker substitutes these images in **all 1024 original relations (1)** and reduces each to the identity. Thus \(\Phi\) is a well-defined homomorphism from the original presentation.

The reverse map \(\Psi:T\to U\) sends \(f_j\) to its displayed original survivor, \(X\) to \(t_6^{-1}t_7\), and \(Y\) to \(t_1^{-1}t_3t_{12}^{-1}t_6\). The three original-row consequences above prove the required relations of \(T\), so this map is also well-defined. The free-basis identities show both composites are the identity on the seventeen surviving generators. The reversible elimination equalities \(t_i=R_i\) then show that \(\Psi\Phi\) fixes every one of the 128 original generators. The other composite fixes all seventeen generators of \(T\). This proves the isomorphism.

The original defect expansion is \(t_6^{-1}t_7\); (2) identifies it with \(X\). Its reduced normal form is nonempty, so it has order exactly two, not merely order dividing two. ∎

The result also gives \(U_{\rm ab}\cong\mathbb Z^{15}\oplus C_2^2\). Every homomorphism from \(U\) to a group with no nonidentity involution kills its Klein-four factor and factors through the quotient \(F_{15}\). In particular every finite odd quotient kills the marked defect. This recovers the phase83 obstruction structurally. It does not replace that smaller 35-cell Lean proof with a claim that the entire normal-form theorem is already formalized.

## 4. The marked action on the free product

The induced action is fully explicit. For each marked permutation \(r\),

\[
\begin{aligned}
f_j^r&=\Phi(t_{s_j^r}),\\
X^r&=\Phi(t_{6^r})^{-1}\Phi(t_{7^r}),\\
Y^r&=\Phi(t_{1^r})^{-1}\Phi(t_{3^r})
          \Phi(t_{12^r})^{-1}\Phi(t_{6^r}),
\end{aligned}
\tag{5}
\]

where \(s_j\) is the original index of \(f_j\). The certificate lists all seventeen images for each of the four marks. It checks the defining Klein-four relations, each mark's involutivity, the three nonadjacent commutations, and agreement with \(t_i^r=t_{i^r}\) on all 128 original generators.

With \(a=f_2^{-1}f_1\), the action on the finite factor takes the particularly simple form

| Mark | Image of \(X\) | Image of \(Y\) |
|---|---|---|
| \(r_0\) | \(XY\) | \(Y\) |
| \(r_1\) | \(X\) | \(Y\) |
| \(r_2\) | \(X\) | \(Y\) |
| \(r_3\) | \(aXYa^{-1}\) | \(aYa^{-1}\) |

This table alone does not specify the automorphisms; the fifteen free-generator images in (5) remain part of the action. The checker compares the full seventeen-image tuples for all 1024 group elements and finds them distinct. It also checks all 4096 right-generator edges against composition on all seventeen generators. Hence the action of \(\bar G\) on \(T\) is faithful. For a full source-family group \(G\), the action on \(U\) has kernel exactly \(N\).

The smallest \(\bar G\)-invariant normal subgroup containing \(\delta\) is precisely the normal closure of the Klein-four factor. Indeed it contains \(X\) and \(X^{r_0}=XY\), hence \(Y\). Conversely the table shows the normal closure of \(X,Y\) is preserved by every mark. Its quotient is \(F_{15}\). This records which part of the universal group carries the obstruction; it is not an assertion that an arbitrary quotient of its free factor is automatically compatible with the whole marked action.

## 5. A controlled finite even quotient

There is a characteristic quotient

\[
V=U/[U,U]U^2\cong\mathbb F_2^{17}.
\]

Its basis is the images of \(f_1,\ldots,f_{15},X,Y\). The four induced action matrices are listed by their seventeen binary columns in the certificate. They are obtained by taking exponent parity in the exact words (5), so they retain the right-action convention. Put \(w=\overline{t_1}=f_1\). Then

\[
w^{r_1}=w^{r_2}=w,\qquad
u=w^{r_3}+w=f_1+f_2,\qquad
u^{r_0}=u,\qquad w^z+w=X\ne0.
\tag{6}
\]

The construction half of the local-complement criterion uses no odd-order hypothesis: in any finite kernel group satisfying these conditions, the standard first end and the conjugate second end have the string relations, injective end projections and intersection exactly the medial subgroup. Applying that proof with the finite even module \(V\), form

\[
\bar H=\langle(0,r_0),(0,r_1),(0,r_2),(u,r_3)\rangle
\le V\rtimes\bar G.
\]

Here \(\bar H\) is first used only as an exact affine group over \(\bar G\). No separate claim that the quotient's two local geometries are the source geometries is needed. The source-family polytopality argument is given below for the full \(G\).

**Exact finite calculation.** The checker constructs a chosen affine lift of each of the 1024 base permutations by breadth-first multiplication. For each of the 4096 edges it compares the resulting lift with the chosen lift at its endpoint. The quotient of these two lifts is a kernel translation. The binary span of all these translations is exactly

\[
W=\langle X,Y\rangle\cong C_2^2.
\tag{7}
\]

That span is explicitly checked invariant under the four matrices. The usual Schreier kernel generators are conjugates of these differences; invariance ensures they span the same space. Thus this computes the entire kernel of \(\bar H\to\bar G\), not merely a subgroup of the kernel or a lower bound. In particular \(|\bar H|=4096\). This calculation uses exact binary arithmetic, with no floating-point rank decisions.

On \(W\), both \(r_0\) and \(r_3\) send \(X\) to \(X+Y\) and fix \(Y\); \(r_1,r_2\) act trivially. Thus \(\langle Y\rangle\) is the unique invariant line. Modulo that line, the calculation gives a kernel of dimension one and a group of order 2048. These numbers are separately checked rather than inferred from a list of sampled parameter values.

**Theorem 2.** For every source parameter and sign pair, (6) constructs a regular polytopal marked cover \(H\to G\) with injective ends, full group order \(1024q\), and kernel \(W\cong C_2^2\). Its quotient by \(\langle Y\rangle\) is a polytopal double cover of \(G\), of full order \(512q\). This quotient is the unique minimal cover over \(G\) within the quotient interval under this particular \(H\).

**Proof of uniform generation and order.** Let \(G\) act on \(V\) through the proved quotient \(G/N\cong\bar G\), and take the same four affine lifts in \(V\rtimes G\). Their generated subgroup \(H\) contains the **standard** \(N\): its marks \(r_1,r_2\) are standard, and \(N=\langle(r_1r_2)^4\rangle\). Since \(N\) acts trivially on \(V\), it is the normal kernel of

\[
V\rtimes G\longrightarrow V\rtimes\bar G.
\]

The image of \(H\) is the computed \(\bar H\). As \(H\) contains the entire kernel \(N\), it is the full preimage of \(\bar H\). Consequently its kernel over \(G\) is exactly the same \(W\), and its order is \(4|G|=1024q\). In particular, the degree is not inferred from the image alone while ignoring a possible missing part of a pullback.

**Proof of polytopality and the quotient.** The first end of \(H\) is standard \(A\); its second is \(B^w\). Both map isomorphically onto the known regular source ends. Equation (6), the retained equality \(A\cap B=C\sqcup Cz\), and the local-complement proof show that the two lifted ends meet exactly in \(C\) and satisfy all string relations. Recursive recognition gives a regular polytope. Exact generator and adjacent product orders are inherited through these end isomorphisms.

The line \(\langle Y\rangle\) is stable under the whole action, so the same construction makes sense in \((V/\langle Y\rangle)\rtimes G\). The image of the marked defect is still \(X\ne0\). The local-complement proof therefore proves that the quotient \(H/\langle Y\rangle\) is polytopal and still injective on both ends. The kernel has order two, so there is no proper intermediate cover between it and the nonpolytopal \(G\); it is minimal.

The three order-two subgroups of \(W\) are its three lines, and the displayed action fixes only \(\langle Y\rangle\). Thus the only normal kernels contained in \(W\) are \(0\), \(\langle Y\rangle\), and \(W\). The last gives the nonpolytopal \(G\). This proves the interval assertion. ∎

This interval assertion alone is not a classification of every cover with injective ends. The next section supplies the missing universal property. The degree-four cover is itself nonminimal, since it covers the degree-two polytope. The earlier phase58 package already constructs a uniform polytopal double cover and contains a finite degree-four classification in one parameter case. Historical novelty is not established here.

## 6. The universal completion and all covers with injective ends

The following bridge was suggested in the collaborating phase90 investigation, now frozen as `phase90_universal_complement_bridge.md` (SHA-256 `685ad72ffa0c9964693d54a52e3ee79d6b7d754c1b4c520d2b0eabe7087c50c3`). We give the specialized proof here in full. It requires the classical Bass–Serre tree of an amalgam; it does not infer a kernel from abstract free-product cancellation or from Grushko uniqueness. The general bridge's independent admission is separate from this authored specialization.

For the full source-family group \(G\), put \(A=G_{012}\), \(B=G_{123}\), and \(C=G_{12}\). In particular \(C\) is the specified common subgroup, not the larger actual intersection \(A\cap B\) in \(G\). Form

\[
F=A*_C B,\qquad
W=F/\langle\!\langle [r_0,r_3]\rangle\!\rangle_F.
\tag{8}
\]

Both map onto \(G\). The copies of \(A\) and \(B\) remain embedded in \(W\), since their composites into \(G\) are the original injective inclusions. Its four marked involutions satisfy all string commutations: two are already local, and the remaining outer commutator is the added relation.

**Completion lemma.** Let \(\mathcal X\) have vertices \(A\backslash G\) and \(B\backslash G\), one oriented edge \(Cg\) from \(Bg\) to \(Ag\), and a square for every \(G\)-translate of the outer commuting square. Then

\[
\pi_1(\mathcal X)\cong\ker(W\longrightarrow G).
\tag{9}
\]

**Proof.** The Bass–Serre tree of \(F=A*_C B\) has vertices \(A\backslash F\) and \(B\backslash F\), and edges \(C\backslash F\), with the same orientation. Let \(K=\ker(F\to G)\). The vertex stabilizers intersect \(K\) trivially because each conjugate of \(A\) or \(B\) maps injectively into \(G\). Thus \(K\) acts freely on the tree. Its quotient is exactly the indicated bipartite coset graph: for example the quotient of \(A\backslash F\) by the right \(K\)-action is \(A\backslash G\). Fix a base vertex \(v\) in the tree and concatenate paths from left to right. If a lifted based loop ends at \(v k\), identify its fundamental-group class with \(k^{-1}\). Right deck transformations make the raw endpoint assignment antihomomorphic; this inversion makes the identification with \(K\) a homomorphism.

The alternating \(r_0,r_3\) path associated to their commutator projects to the indicated square. Attaching all its \(G\)-translates kills the normal closure in \(K\) of all \(F\)-conjugates of that commutator. That is exactly \(\langle\!\langle[r_0,r_3]\rangle\!\rangle_F\), which is contained in \(K\). Reversing a square orientation replaces the relator by its inverse; changing its basepoint conjugates it, neither of which changes this normal closure. Repeated attaching loops can be omitted without changing the fundamental group. The resulting fundamental group is therefore the kernel in (9). ∎

For an original quadruple \((a,b,c,d)\), its edges satisfy

\[
A_a=A_c,\quad B_a=B_b,\quad A_b=A_d,\quad B_c=B_d.
\]

With each edge oriented from the \(B\)-vertex to the \(A\)-vertex, the word \(t_d^{-1}t_c t_a^{-1}t_b\) is consequently a closed boundary path. The checker verifies these incidences for all 1024 cells. This fixes the orientation linking (1) to the topological presentation. The common normal subgroup \(N\le C\) identifies the full source-family coset graph and cells with the fixed model, exactly as in the prior transport argument.

The graph has eight \(A\)-vertices and eight \(B\)-vertices. Crucially, the fifteen original edges whose labels are the fifteen \(f_i\) **form a spanning tree**. This is not inferred from the free rank. Their exact endpoints, in the certificate's sorted coset-block indexing, are:

| Edge | \(A\)-vertex | \(B\)-vertex |
|---|---:|---:|
| 1 | 0 | 8 |
| 2 | 1 | 8 |
| 4 | 3 | 9 |
| 5 | 0 | 10 |
| 6 | 0 | 11 |
| 8 | 0 | 12 |
| 9 | 4 | 8 |
| 10 | 1 | 9 |
| 12 | 2 | 11 |
| 14 | 3 | 13 |
| 16 | 0 | 14 |
| 19 | 0 | 15 |
| 21 | 5 | 9 |
| 25 | 6 | 9 |
| 32 | 7 | 14 |

The program constructs both coset partitions from the actual permutation subgroups, checks every edge above, checks that no successive edge creates a cycle, and checks connectivity on all sixteen vertices. The usual maximal-tree presentation of a connected cell complex imposes \(t_s=1\) on those tree edges and keeps all square boundaries. Hence

\[
\pi_1(\mathcal X)
\cong U/\langle\!\langle f_1,\ldots,f_{15}\rangle\!\rangle
\cong C_2\times C_2.
\tag{10}
\]

The last isomorphism is the exact one proved in Theorem 1. This proves the **abstract** kernel and its order. Tree contraction is not asserted to be \(G\)-equivariant, and simply killing the free generators is not used to deduce a kernel action.

To identify the action and the marked extension, apply the universal property of (8) to the affine cover \(H\) of Theorem 2. Its two end groups are marked copies of \(A,B\) agreeing on \(C\), and its outer string relation holds. There is therefore a marked surjection \(W\to H\) commuting with the maps to \(G\). By (9)–(10), \(|W|=4|G|\). Theorem 2 proves \(|H|=4|G|\) independently, with the full-preimage generation argument. The surjection is an isomorphism. This transfers the **actual** action on the kernel from the affine group to \(W\), and shows that \(W\) itself is polytopal. In particular the unique invariant kernel line is the line corresponding to \(\langle Y\rangle\) in that affine identification.

**Theorem 3.** For every Γ2 parameter, there are exactly two regular polytopal marked covers of \(G\) whose restrictions to both maximal standard parabolics are injective: the degree-four completion \(W\cong H\) and its degree-two quotient. In particular they are both finite, even if finiteness was not assumed initially. The degree-two quotient is the unique minimal cover within the entire class with injective ends.

**Proof.** In any such cover \(P'\to G\), each marked end maps isomorphically onto \(A\) or \(B\), and the two copies agree on \(C\). The outer marked involutions commute. Thus the two end maps extend to a surjective marked homomorphism \(W\to P'\), since the marks generate \(P'\). Its kernel lies in \(\ker(W\to G)\). This proves that every cover in the stated class is a quotient of the finite group \(W\); no independent finiteness assumption is needed.

The kernel is the abelian Klein-four group with action computed in Theorem 2. Its only subgroups normal in \(W\) are zero, its unique invariant line, and itself. They give respectively the degree-four cover, the polytopal degree-two quotient, and the nonpolytopal base \(G\). There are no other marked quotient kernels in this class. ∎

The degree-two quotient is consequently marked-isomorphic over \(G\) to the phase58 double cover, which already has injective ends. This identification uses the just-proved uniqueness, not merely matching orders. The theorem does **not** classify covers whose ends map noninjectively; it does not prove unrestricted uniqueness of minimal covers of the original chiral polytope. Any different minimal regular cover must change at least one local end. Historical novelty and current-source openness remain unverified.

## 7. Certificate, reproduction and attribution

The certificate gives all 128 forward normal forms, all 128 survivor expansions, all seventeen inverse images, the three reverse-relation witnesses, all four full automorphisms, and all four binary action matrices. Its normal-form alphabet is specified explicitly: signed `1..15` are the free letters, `16=X`, `17=Y`, and `18=XY`. The latter three symbols are involutions, and adjacent Klein-four syllables combine by their two-bit sum. In the raw free-basis witness words, `-16` and `-17` still denote formal inverses before imposing (4).

The standalone Python program rechecks the original coset model and complete elimination trace, both free-basis composites, all 512 remaining relations, all 1024 original relations, every transported original generator, all 1024 automorphisms and all 4096 action edges, the two coset partitions, all square incidences, the literal spanning tree, and the exact affine kernels. It imports no GAP, author algebra module, symbolic group package or numerical library. Its use of explicit conditions rather than Python assertions preserves all checks under `python3 -O`.

From the study directory:

```sh
python3 -O phase92_complement_normal_form.py \
  --expected-certificate phase92_complement_normal_form_certificate.json \
  --output-dir /tmp/complement-normal-form-new
```

The output path must not already exist, including as a dangling symlink. The two frozen original inputs are hash-checked and rechecked after computation. A supplied expected certificate must agree byte-for-byte with exact regeneration before output is created. The outer manifest binds the written proof, original dependencies, program and certificate. The code is a finite proof certificate interpreted through the elementary presentation and normal-form arguments above; no new Lean formalization of the complete isomorphism or cover theorem is claimed.

**[B] Borrowed:** the source Γ2 family and source theorem dependencies; classical group-presentation, free-product, Bass–Serre, Schreier and recognition facts; the exact phase58/66 transport; and the phase83/86 universal criterion, original trace and marked model. **[I] Repository derivations, historical novelty unestablished:** explicit bidirectional free-product maps, complete original-relator verification, marked action, controlled canonical even quotient, and the exact application of the phase90 coset-complex idea using the literal spanning tree. The latter conceptual bridge was supplied by the collaborating operations/compression agent; its specialized proof and compatibility checks are included here. **[R] Shared structure:** one presentation and its two involutions handle every β and sign pair. **[V] Exact certificate:** the enumerated relations, substitutions, automorphisms, tree and binary kernels. There is no new **[L]** whole-theorem formalization, **[M]** manuscript-compression measurement or **[O]** cleared open-conjecture resolution.
