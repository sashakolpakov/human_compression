# Coprime affine covers for all four atomic 2-primary families

10 October 2026. Author theorem package; independent review and public admission remain separate. This package preserves the frozen Γ2 construction. It supplies a smaller common marked quotient, a general parabolic pullback theorem, and two exact finite affine certificates. Its uniform conclusions follow from the source presentations and the written proof, not from parameter sampling. Historical priority and comprehensive current-literature status have not been established.

## 1. Exact scope and principal result

Retain Cunningham–Pellicer, *Tight chiral polytopes*, arXiv:2009.04566v1, Table 2, Proposition 4.2 and Theorems 4.8–4.10. Put q=2^β, t=q/4, β≥5, and e_i=ε_i t with ε_i independently ±1. Their rotation groups P have generators a,b,c, the relations

```text
a^p=b^q=c^r=(ab)^2=(bc)^2=(abc)^2=1,
```

and the following additional relations. The labels L2,L31,L32,R2,R31,R32 will always mean the literal left side times the inverse of the literal right side.

| Label | Relation |
|---|---|
| L2 | b a² = a² b^(1+e1) |
| L31 | b^(-1) a = a^(-1+t) b^(-3+e1) |
| L32 | b a^(-1) = a^(1+t) b^(3+e1) |
| R2 | c² b = b^(1+e2) c² |
| R31 | c^(-1) b = b^(3+e2) c^(1+t) |
| R32 | c b^(-1) = b^(-3+e2) c^(-1+t) |

The families and relation sets are

| Family | (p,r) | Additional relations |
|---|---|---|
| Γ2 | (8,8) | L2,R2 |
| Γ3 | (q/2,q/2) | L31,L32,R31,R32 |
| Γ4 | (8,q/2) | L2,R31,R32 |
| dual Γ4 | (q/2,8) | marked dual of the Γ4 presentation |

The retained source theorem identifies these exact presentations with tight chiral polytopes, of rotation order pqr and exact type {p,q,r}. It supplies their existence, tightness, intersection property, atomic/local classification inputs and normal chirality subgroup X=<x>, where x=b^(q/2) is an involution. Thus x is central. These substantial inputs are not re-proved or counted as new classification. Standard marked group/polytope correspondence, rank-three and rank-four recursive string-C recognition, and the universal property of the smallest regular maniplex cover are retained geometric background.

Let G be the **full reflection group** of the smallest regular maniplex cover of P. All maps and cover comparisons preserve the four marks and hence ranks. Full group orders, not rotation subgroup orders, are used below.

**Theorem A.** For every parameter in all four rows above, and for each ℓ∈{3,5}, there is a finite regular polytopal marked cover H_ℓ→G with

```text
|G|=4pqr,   ker(H_ℓ→G) ≅ C_ℓ^34,
|H_ℓ|=4pqr·ℓ^34,   type(H_ℓ)={ℓp,q,ℓr}.
```

Each end projection has kernel C_ℓ^9, and the medial projection is injective. Each H_ℓ has a quotient Q_ℓ that is a globally minimal regular polytopal cover of the original chiral polytope, with degree ℓ^d_ℓ over G for some 1≤d_ℓ≤34. In particular Q_3 and Q_5 are distinct. The two finite admissible universal kernels supplied by H_3,H_5 have product equal to the relation kernel of G; hence all finite admissible kernels have that same join.

The explicit groups are H_3,H_5. No particular minimal descendant or exponent d_ℓ is selected. There is no classification of every minimal cover, and no assertion that the large constructed covers are minimal. This result does not settle the arbitrary-polytope multiple-minimal-cover question. Together with the separately reviewed odd-prime Γ1 theorem, it establishes the proposed multiplicity assertion for the five specified source families, conditional on the stated retained construction and geometric inputs. That combination is a scope statement, not a historical-priority assertion or an additional source-compression count.

## 2. Coprime parabolic pullback with an exact obstruction

Let π:G→D be an epimorphism of finite groups with specified marked involutions r_i↦s_i, and N=ker π. For a set of marks I write G_I=<r_i:i∈I>, and similarly D_I. Let V be a finite-dimensional right F_ℓD-module, where ℓ is prime and ℓ does not divide |N|. Write affine multiplication as

```text
(v,g)(u,h)=(v^h+u,gh),
```

using π for the action of G. Choose shifts v_i and put

```text
Hbar=<(v_i,s_i)> ≤ V⋊D,    H=<(v_i,r_i)> ≤ V⋊G.
```

The marked projections onto D and G are surjective by generation. Denote the respective parabolics by Hbar_I,H_I.

**Theorem B (parabolic pullback).** For every I, H_I is the full fiber product of Hbar_I and G_I over D_I. In particular H is the full fiber product of Hbar and G, and the kernels over their original base groups identify. If Hbar has the intersection property, then, for K=I∩J,

```text
H_I ∩ H_J = {(0,n):n∈N∩G_I∩G_J} H_K.               (1)
```

Consequently H has the intersection property if and only if

```text
N∩G_I∩G_J ≤ G_(I∩J)       for every I,J.             (2)
```

If G is a rank-four involutory string group and its two ends A=G012,B=G123 are string C-groups, it suffices that Hbar is a string C-group and

```text
N∩(A∩B) ≤ C=G12.                                    (3)
```

There is no requirement N≤C.

**Proof.** Take n∈N∩G_I. Since the order of n is prime to ℓ, there is m∈<n> with m^ℓ=n. Lift m to some (v,m)∈H_I. The element m acts trivially on V, so

```text
(v,m)^ℓ=(ℓv,m^ℓ)=(0,n).
```

Thus H_I contains the entire standard subgroup N∩G_I, without any assumption that N is cyclic or that N lies in G_I. The image of H_I in V⋊D is exactly Hbar_I. For any element of Hbar_I and any matching base element of G_I, choose an actual lift in H_I and adjust its base coordinate by a standard element of N∩G_I. This proves the full fiber-product assertion. Taking I to be all marks proves the global assertion and identifies the two covering kernels. The proof is about the generated subgroups, not only their ambient preimages.

Suppose now that Hbar has IP. An element h∈H_I∩H_J maps into Hbar_I∩Hbar_J=Hbar_K. Choose h_K∈H_K with the same image. Then hh_K^(-1) lies in the standard N and also in both H_I,H_J. Its base element therefore belongs to N∩G_I∩G_J. This proves one inclusion in (1); the other follows from the standard-subgroup inclusions already proved and H_K≤H_I,H_J. Equality H_I∩H_J=H_K is equivalent to N∩G_I∩G_J≤G_K, by taking base coordinates, proving (2).

For the rank-four statement, inside either source end G_I∩G_J=G_(I∩J) already holds. Equation (1) consequently transports every intersection inside each end, so both lifted ends are string C-groups. Condition (3) and (1) give H012∩H123=H12. The lift relations are involutory and string whenever both their base and affine images have those relations: H embeds in the fiber product, so a word trivial in both coordinates is trivial. Recursive recognition completes the proof. ∎

A useful exact reformulation of (3) is available when A∩B=C⊔Cκ. If πκ∉πC, then no element of Cκ belongs to N; hence N∩(A∩B)=N∩C. This detects the original defect while allowing substantial kernels inside both ends.

## 3. Uniform mirror-relator calculation

The universal mirror substitution on rotation words is

```text
α(a)=a^(-1),    α(b)=a²b=a b^(-1)a^(-1),    α(c)=c.      (4)
```

It preserves the rotation power and square relations. For example α(ab)=ab, α(bc)=a(bc)a^(-1), and α(abc)=abc; the middle equality follows from (bc)^2=(abc)^2=1, while the last follows directly. The order of α(b) equals that of b by its conjugate-inverse expression. The substitution is involutory on the universal rotation group.

**Lemma 3.** Every additional literal relator w used by the applicable source row satisfies α(w)=x in P.

**Proof for the left relators.** Put e=e1. Since e² is divisible by q, the relation b a²=a² b^(1+e) gives

```text
b^(-1)a^(-2)=a^(-2)b^(-1+e).
```

The mirror of L2, written as the literal word b a² b^(-1-e)a^(-2), is therefore

```text
a b^(-1)a^(-2)b^(1+e)a = a^(-1)b^(2e)a = x.           (5)
```

Here b^(2e)=x and x is central. In the Γ3 local presentation, write

```text
L31=b^(-1)a b^(3-e)a^(1-t),
L32=b a^(-1)b^(-3-e)a^(-1-t).
```

Since a^(2t)=1, the two source relations give the following literal evaluations:

```text
α(L31)=a b a^(-1)b^(-3+e)a^(-2+t)
       =a^(t+2)b^(2e)a^(t-2)=x,
α(L32)=a b^(-1)a b^(3+e)a^t
       =a^t b^(2e)a^t=x.                             (6)
```

These calculations use both Γ3 local relations and no asymptotic congruence. They apply at β=5 and for either sign.

**Proof for the right relators.** This step fixes the local mirror convention explicitly. Put u=c^(-1),v=b^(-1). The Γ2 right relation becomes its L2 counterpart in u,v; the two Γ3 right relations become L32,L31, respectively, up to conjugation and inversion. More precisely, for R2,R31,R32 take respectively

```text
A0=c²b,  c^(-1)b,  c b^(-1).
```

The corresponding left literal relator in u,v equals A0^(-1) R_i^(-1) A0. Thus these are equivalent defining relations. The local mirror λ(u)=u^(-1), λ(v)=u²v sends each such left word to v^(q/2)=x by (5) or (6). Consequently it sends each corresponding right word to x as well: the conjugating word is immaterial because x is central and x^(-1)=x.

The intrinsic mirror on the right end is β(b)=b^(-1), β(c)=b²c. In u,v it is

```text
β(u)=u v²,   β(v)=v^(-1),
β(-)=(uv)^(-1) λ(-) (uv) on these generators,
```

where (uv)^2=1. Hence β(R_i)=x. Finally the rotation square relations give

```text
a^(-1)α(b)a=b^(-1),
a^(-1)α(c)a=b c^(-1)b^(-1)=b²c.
```

For the second identity, combine (ab)^2=(bc)^2=(abc)^2=1; it is also the standard change of base mirror between adjacent ends. Therefore β=a^(-1)α(-)a on the right end, and α(R_i)=a x a^(-1)=x. This proves all right cases and the lemma. ∎

No finite β/sign check is substituted for (5)–(6) or the right-end argument.

## 4. Exact presentation and end interface of the smallest cover

In P×P put

```text
Arot=(a,a^(-1)), Brot=(b,a²b), Crot=(c,c), κ=(1,x),
R=<Arot,Brot,Crot>.
```

Modulo <x>, Lemma 3 makes α a well-defined involutory automorphism of P/<x>. Therefore R lies in the corresponding twisted fiber product of P with itself, which has order 2|P|. Every source additional relator evaluates to κ≠1 in R, by Lemma 3; the first projection is onto P. It follows that R is that whole fiber product, of order 2pqr, and its first projection has kernel <κ>. It is the mirror mix, hence the rotation group of the smallest regular maniplex cover. The coordinate switch μ preserves R and realizes the mirror.

An exact presentation for R is obtained from the source rotation powers and squares by replacing all its additional equations w=1 with

```text
all w have the same value w0,
w0²=1,    [w0,a]=[w0,b]=[w0,c]=1.                    (7)
```

Indeed the group in (7), modulo its central subgroup <w0> of order at most two, is exactly the source P. Its order is at most 2pqr, and its evident map onto the actual mix R attains that order. This proves the presentation, rather than assuming that a central extension chosen from samples is the desired mirror mix.

Take G=R⋊<μ>, with marks

```text
r0=μ, r1=r0 Arot, r2=r1 Brot, r3=r2 Crot.              (8)
```

It has order 4pqr. Substituting a=r0r1,b=r1r2,c=r2r3 in (7), and retaining the four involution relations and three nonadjacent commutations, presents G exactly. The even-word subgroup is generated by a,b,c and is a quotient of (7), so the presented full group has order at most 4pqr; the actual group (8) attains it. This establishes a marked presentation, including the reflection convention.

The two rotation ends F=<Arot,Brot> and V=<Brot,Crot> both contain κ because each has at least one source additional relator. Each is the full preimage of the corresponding source end under R→P, so

```text
|F|=2pq, |V|=2qr, F∩V=<Brot,κ>, |F∩V|=2q.           (9)
```

The final equality uses the retained source IP. Their adjacent cyclic subgroups have trivial intersection by projection to P and the exact generator orders, so they have the rank-three intersection property. The mirror (4) preserves F, and the intrinsic right-end mirror from Lemma 3 preserves V. These are the regular rank-three end groups. Passing to full reflections gives

```text
A=G012, B=G123, C=G12,
|A|=4pq, |B|=4qr, |C|=2q,
I=A∩B=C⊔Cκ, |I|=4q.                               (10)
```

For the full intersection, remove a common reflection r1 from an odd-word element and use (9). Also κ∉C: in the rotation subgroup equality κ=Brot^j would give b^j=1 in P, then Brot^j=1 by its exact order q. Thus G is nonpolytopal. The involution κ is central in R; no claim that it is central in the full G is needed or made.

## 5. One explicit common marked quotient

Define D to be the subgroup of Sym(16) generated by the following four permutations. Each row gives the images of 1,...,16 in order; permutations act on the right, so multiplication means first the left factor, then the right factor.

```text
s0: 1 2 3 7 5 6 4 12 13 10 11 8 9 16 15 14
s1: 1 4 3 2 9 7 6 8 5 15 13 12 11 16 10 14
s2: 2 1 6 8 10 3 12 4 14 5 15 7 16 9 11 13
s3: 3 5 1 9 2 11 13 8 4 15 6 12 7 14 10 16
```

These literal arrays, also given in the bound JSON model, are a finite witness. Their discovery used GAP; no GAP presentation-solving correctness or hidden catalogue identification is needed in the proof. The standalone Python checker generates their whole group, checks every permutation/string relation, and obtains

```text
|D|=256, |D012|=|D123|=64, |D12|=8,
|D012∩D123|=16, type(D)={4,4,4}.                     (11)
```

Put a0=s0s1,b0=s1s2,c0=s2s3. In D the following six literal reduced words have one common value κ0:

```text
b0 a0² (a0² b0)^(-1),
c0² b0 (b0 c0²)^(-1),
b0^(-1)a0 (a0^(-1)b0^(-3))^(-1),
b0 a0^(-1) (a0 b0³)^(-1),
c0^(-1)b0 (b0³ c0)^(-1),
c0 b0^(-1) (b0^(-3)c0^(-1))^(-1).                   (12)
```

The checker verifies κ0²=1≠κ0, centrality of κ0, membership in both ends and κ0∉D12. These finite word identities are part of the charged certificate, not an inference from equal group orders.

**Lemma 5 (uniform quotient).** Every G in Γ2,Γ3,Γ4 has a marked epimorphism π:G→D carrying κ to κ0. Its kernel N satisfies

```text
|N|=pqr/64,
|N∩A|=pq/16, |N∩B|=qr/16,
N∩I=N∩C, |N∩C|=q/4.                               (13)
```

**Proof.** Both t and e_i are divisible by four, already at β=5, and a0,b0,c0 have order four. All source extra relators in the exact presentation (7) therefore reduce literally to the applicable words in (12). The source powers hold since p,q,r are divisible by four, and the rotation squares and involutory string relations were checked. All central-equality relations in (7) hold because the values in (12) are the same central involution κ0. Hence (7)–(8) define the marked homomorphism. It is onto because its images generate D. The word w0 identifies the image of κ as κ0, not just an unspecified nonidentity element.

Equation (11) and the exact parabolic orders in (10) give the first three kernel orders and |N∩C|. Since I=C⊔Cκ and κ0∉πC, the last observation of Theorem B proves N∩I=N∩C. This also gives |πI|=16. In particular N is a 2-group, but it need not lie in C. No description of N as a cyclic group or an unproved normal closure of a few powers is used. ∎

For the dual Γ4, reverse the four marked reflections in the original Γ4 presentation, construction and map. This transports the proved theorem to its exact marked dual. It exchanges the two ends and p,r and preserves all asserted kernel orders and coprime degrees. It neither assumes equal signs nor identifies distinct source parameter choices by an unproved self-duality.

## 6. Exact affine kernel and intersection test

The common finite construction below is applied separately over F3 and F5. It is not a claim about all odd characteristics. Let ℓ be either of these two primes and use the right affine convention from §2. Put

```text
E=F_ℓ[{<s0>g:g∈D}] ⊕ F_ℓ[{<s3>g:g∈D}].            (14)
```

There are 128 basis vectors in each summand. Denote them e and f, respectively. D acts by right multiplication on right cosets. Choose

```text
v0=v3=0,
v1=f_(<s3>)-f_(<s3>s1),
v2=-e_(<s0>)+e_(<s0>s2),
h_i=(v_i,s_i), T=<h0,h1,h2,h3>.                     (15)
```

All h_i are involutions because v_i^s_i=-v_i. The shift v2 is s0-fixed and v1 is s3-fixed, using the nonadjacent commutations in D; the remaining outer pair has zero shifts. Thus all three string commutations hold before any quotient. The program also checks these literal vector equations.

Let c be the translation given by (h1h2)^4. Its base element is trivial. Define

```text
M=span_F_ℓ{c^g:g∈D}, L=ker(T→D), Hbar_ℓ=T/M.          (16)
```

Then M≤L. The quotient embeds in (E/M)⋊D. The sole killed word is the indicated medial relation and its conjugates; no arbitrary complement is selected.

Here is the complete mathematical justification of the finite linear algorithm. For a marked subset I, choose by breadth-first word traversal one lift (t_I(g),g) of each g∈D_I. On each generator edge g→gs_i, take the vector difference between the extended chosen lift and the chosen lift at gs_i. Let L_I be the span of all these differences and their D_I-translates. Then

```text
ker(T_I→D_I)=L_I,   fiber over g = t_I(g)+L_I.          (17)
```

Every initial difference is the translation obtained as the left quotient of two actual lifts with the same base, and its translates are conjugates inside T_I. Hence L_I is contained in the kernel. Conversely insert chosen representatives and their inverses between consecutive letters of any word with trivial base image. This Schreier rewriting expresses it as a product of conjugates of these differences. That proves the opposite inclusion. The program saturates the span under the actual parabolic generators until its dimension stops increasing, and then explicitly verifies invariance; finiteness of E guarantees termination.

Modulo M, the kernel of the image of T_I is (L_I+M)/M. For I,J and K=I∩J, an intersection fiber over g∈D_I∩D_J is nonempty if and only if

```text
t_I(g)-t_J(g) ∈ L_I+L_J+M.                           (18)
```

Its translation dimension is

```text
dim(L_I+M)+dim(L_J+M)-dim(L_I+L_J+M)-dim M.            (19)
```

These are the usual exact conditions for two affine cosets of vector subspaces to intersect. The common marked subgroup T_K already lies in the intersection. Therefore exact IP for the pair follows when (18) fails at every g outside D_K and (19) equals dim(L_K+M)-dim M. All outside elements must be tested. This criterion allows enlarged local kernels and does not replace affine fiber compatibility by a dimension comparison alone.

## 7. Two finite certificates and complete IP

The standalone program evaluates (14)–(19) independently over F3 and F5. It enumerates only the 256-element base, then performs exact finite-field row operations. It does not enumerate the enormous affine group. For **each** field the results are

```text
dim L=65, dim M=31, dim ker(Hbar_ℓ→D)=34.
```

The complete recursive intersection data are

| I,J,K | |D_I|,|D_J|,|D_K| | |D_I∩D_J| | Quotient kernel dimensions | Intersection kernel dimension | Excluded base elements |
|---|---|---:|---|---:|---:|
| 012,123,12 | 64,64,8 | 16 | 9,9,0 | 0 | 8 |
| 01,12,1 | 8,8,2 | 2 | 1,0,0 | 0 | 0 |
| 12,23,2 | 8,8,2 | 2 | 0,1,0 | 0 | 0 |

For every one of the eight excluded elements in the first row, the certificate prints a nonzero remainder of the difference in (18) modulo the complete sum space. These are all unwanted projected elements. The equal dimensions in the table then give equality of the full intersection fibers, including kernels. The local rows prove both rank-three ends have IP. Rank-two groups on two distinct involutions are dihedral and have the required rank-two IP; nontriviality and distinctness follow from their base images. The top row and recursive recognition prove that Hbar_ℓ is a rank-four string C-group.

The checker evaluates adjacent product powers literally, including every smaller positive exponent up to the attained order. It finds

```text
type(Hbar_3)={12,4,12}, type(Hbar_5)={20,4,20},
|Hbar_ℓ|=256·ℓ^34,
```

with end kernels ℓ^9 and trivial medial kernel. The certificate includes the entire row bases of L and M, every required raw parabolic kernel basis, the literal vector c, all eight separating remainders in each field, and all model/relator checks. No floating-point calculation, p-quotient truncation or unproved catalogue identifier is involved. The two fields are two separately checked finite constructions; no interpolation in ℓ is used.

## 8. Transport to every source parameter

For each source G use the marked quotient π from Lemma 5 and let V=E/M act through π. Define H_ℓ in V⋊G by the same four shift vectors (15). Since N is a 2-group, the coprimality hypothesis of Theorem B holds for ℓ=3 and 5. Theorem B proves that H_ℓ and **every** generated parabolic are their full fiber products. It identifies ker(H_ℓ→G) with the computed C_ℓ^34 and identifies all local covering kernels as well. Thus the end kernels have order ℓ^9 and the medial covering kernel is trivial, uniformly in β and both signs.

The original source ends A,B are string C-groups by §4. Lemma 5 proves N∩(A∩B)≤C. The rank-four clause of Theorem B consequently proves H_ℓ has full IP. In particular both local rank-three IP tests are transported, not only the top-end equality. This proves the regular polytopal covering assertion and the order formula.

In a fiber product, a marked word has order equal to the least common multiple of its orders in the two factors. For the three adjacent products these factors have orders (p,q,r) and (4ℓ,4,4ℓ). Since p,q,r are powers of two divisible by four, the lcm values are (ℓp,q,ℓr). This gives the exact type. Duality transports the whole construction to dual Γ4 as specified in §5.

## 9. Finite minimal descendants and join-density

Fix either ℓ and let K_ℓ=ker(H_ℓ→G). Among the normal subgroups J≤K_ℓ such that H_ℓ/J is polytopal, choose one maximal by inclusion. The collection is nonempty (J=1) and finite. Put Q_ℓ=H_ℓ/J. Its degree over G is ℓ^d_ℓ with 0≤d_ℓ≤34. Since G is nonpolytopal by (10), d_ℓ is positive.

This quotient is globally minimal over the original chiral P. Every regular cover of P maps to its smallest regular maniplex G. A further marked regular polytopal quotient of Q_ℓ covering P therefore corresponds, by the uniquely determined marked map to G, to a larger H_ℓ-normal subgroup inside K_ℓ. Maximality excludes such a proper quotient. An infinite quotient cannot arise from the finite group Q_ℓ. This proves global minimality, not just minimality inside a separately chosen interval disconnected from the marked base.

The degrees of Q_3 and Q_5 over the same G are respectively positive powers of three and five. They cannot be equal, so the groups and their rank-preserving marked polytopes are different. This proves the multiplicity statement without presuming any even-degree cover for Γ3 or Γ4 and without classifying these new minimal descendants.

For the join assertion, let F be the universal rank-four involutory string group, with only involutions and nonadjacent commutations imposed, and K0=ker(F→G). The marked relation kernels J_3=ker(F→H_3) and J_5=ker(F→H_5) are normal, lie in K0 and are finite admissible kernels. Their indices in K0 are 3^34 and 5^34. The quotient K0/(J_3J_5) is a quotient of both K0/J_3 and K0/J_5; its order divides these coprime integers, hence is one. Thus J_3J_5=K0. Every finite admissible regular-cover kernel over P lies in K0 by the universal property of G. The join of all of them is therefore exactly K0. No claim that arbitrary mixes preserve IP is used.

## 10. Dependencies, certificates, attribution and limits

The primary source package is bound by exact PDF and extracted-text hashes in the ledger. The bounded primary reading for this theorem covers Table 2, Proposition 4.2 and the complete statements and construction proofs of Theorems 4.8–4.10; the earlier exact-source audits give broader context. Cunningham's later *Chiral polytopes whose smallest regular cover is a polytope*, §4, supplies the multiplicity question and the earlier finite odd-prime example, rather than any premise asserting the present conclusion. The frozen odd-prime Γ1 theorem and its reviews are needed only for the last sentence combining all five families; no Γ1 theorem is re-proved or used in constructing the four 2-primary cases.

The mirror mix, recursive recognition, affine semidirect products, Schreier rewriting, finite-field elimination and finite quotient descent are standard ingredients. The repository's earlier Γ2 construction supplied the two-edge-module shift pattern and the medial orbit relation. The general pullback criterion, the present fixed 256-element witness and its uniform source transport are the new derivations recorded here. That wording identifies their role in this investigation and does not establish historical priority. The earlier finite example and trivial-extension/mix strategies retain their original attribution.

All executable proof cost is explicit: `phase109_cover_families_generalization_check.py`, its 16-point model and the generated two-field certificate. The checker is standalone standard-library Python and uses explicit exceptions rather than removable assertions. It validates both fields, every required affine fiber and all six reduced source words before producing output. The control program tests corrupted certificates and model bindings, and occupied output paths, under optimized Python. The discovery GAP presentation and mutable probes are excluded from the theorem package; the model is independently defined by its literal permutations and wholly checked by the bound program. No sample source-family enumeration is required for the uniform proof.

This package adds no Lean component, new compression factor, source-classification replacement or unrestricted-cover classification. It does not claim that every nonpolytopal smallest regular cover has multiple minimal covers, nor that the literature has not already proved a related result. Independent review, root admission and any public-status update remain separate gates.
