# A universal complement group and an obstruction to odd-kernel covers

10 October 2026. Author manuscript; independent admission is recorded separately.

For every member of the specified Γ2 family, a finite regular polytopal cover
of its smallest regular maniplex cannot have an odd-order kernel and injective
maps on both maximal standard parabolics. The kernel need not be abelian.
The proof reduces the question to one noncommutative group presentation on
128 cosets. Thirty-five of its defining cells already force the relevant
defect to have order at most two. This exact implication is checked in Lean.

The family and its existence are borrowed. The universal-complement
organization, exact cell certificate and this application are repository
derivations; historical novelty is not established. This is a scoped cover
obstruction, not a proof of unrestricted minimal-cover uniqueness or a
certified resolution of a currently open source conjecture.

## 1. Interface and conventions

Let G be a finite 2-group with marked generating involutions r0,r1,r2,r3.
Assume the string relations [ri,rj]=1 for |i−j|>1. Write

```text
A = <r0,r1,r2>,  B = <r1,r2,r3>,  C = <r1,r2>,  I = A ∩ B.
```

Assume A and B, with these markings, are rank-three string C-groups, and
there is an element z such that

```text
I = C ⊔ Cz,     z centralizes C.                         (1)
```

In particular, [I:C]=2 and z∉C. We use right conjugation x^g=g⁻¹xg;
successive actions satisfy (x^g)^h=x^(gh). A marked cover is a surjective
homomorphism taking each distinguished generator to the corresponding ri.
Its ends are the subgroups on marks 012 and 123. Injectivity on the ends
is an essential hypothesis throughout.

For a right action of G by automorphisms of a group K, represent an element
of the split extension by (k,g), standing for gk. Multiplication is

```text
(k,g)(l,h) = (k^h l, gh).                               (2)
```

No multiplication in K is commuted in the arguments below.

## 2. Local complements, without an abelian hypothesis

**Proposition 1.** Under (1), the following are equivalent.

1. G has a finite regular polytopal marked cover with odd kernel and
   injective restrictions on both ends.
2. There are a finite odd-order group K, a right G-action by automorphisms
   on K, and w∈K satisfying

```text
w^r1 = w^r2 = w,
u = (w^r3)^−1 w,       u^r0 = u,
w^z ≠ w.                                               (3)
```

**Proof, construction.** In K⋊G take the standard A and the conjugate B^w.
Since w centralizes C, their common distinguished generators are r1,r2.
The fourth distinguished generator is

```text
s3 = w^−1 r3 w = r3 u.
```

It is an involution because it is conjugate to r3. It commutes with r1,
since w commutes with r1 and r3 commutes with r1. As r0 commutes with r3,
conjugating r3u by r0 shows that [r0,s3]=1 exactly when u^r0=u. Thus all
required string relations hold. Both ends project isomorphically onto
their respective base ends.

Projection onto G gives an exact intersection formula:

```text
A ∩ B^w = {i∈I : i^w=i}.                               (4)
```

Indeed, if i=j^w for i∈A and j∈B, projection forces i=j; the converse
is immediate. Every c∈C commutes with w. For i=cz in the other coset of C,
i commutes with w if and only if z does. Equation (4) is therefore C
exactly when w^z≠w; otherwise it is I. The standard rank-four string-C
recognition lemma says that two rank-three string C-group ends with this
intersection C give the full intersection property. Its hypotheses have
all been verified. Consequently H=<A,B^w> is a string C-group. Its
projection is onto G, and its kernel is a subgroup of K, hence finite and
odd. This supplies the stated regular polytopal cover.

**Proof, necessity.** Let π:H→G be such a cover and let K=ker π. Since K
is odd and G is a 2-group, a Sylow 2-subgroup S of H has order |G|.
Its intersection with K is trivial, so π identifies S with G and
H=K⋊S. This splitting uses only Sylow theory, without any solvability
assumption on K.

The lifted facet is a Sylow 2-subgroup of π⁻¹(A). Sylow conjugacy takes it
to the standard A. A conjugator can be chosen in K: if A^x is the desired
complement and x=ak with a∈A and k∈K, then A^x=A^k. After a global
K-conjugation, the first three distinguished generators are exactly
r0,r1,r2, since π is injective on this complement. Applying the same
argument in π⁻¹(B) gives the other lifted end as B^w for some w∈K.
Its marked lifts of r1,r2 coincide with the standard ones, so w
centralizes both and hence C. The cover's outer string commutation gives
u^r0=u, and its intersection property, using (4), forces w^z≠w. ∎

The recognition lemma and Sylow conjugacy are classical inputs. This
explicit normalization explains why the subsequent nonlinear certificate
addresses every finite odd kernel under the end-injectivity hypothesis,
rather than a chosen representation or a family of module constructions.

## 3. One universal group replaces all possible kernel groups

Let X=C\G be the set of right cosets, with its right G-action. Define
U=U(G,C;r0,r3) by one generator t_x for each x∈X, and one relation for
each translate g∈G of the indicated cell:

```text
(t_(Cr3r0g))^−1 t_(Cr0g) (t_(Cg))^−1 t_(Cr3g) = 1.      (5)
```

Repeated cells may be omitted. The right action t_x↦t_(xg) preserves
the whole relation set, so induces an action of G by automorphisms of U.
Set δ=t_C^−1 t_(Cz).

**Proposition 2.** Condition (3), and hence the cover in Proposition 1,
exists if and only if δ has nontrivial image in some finite odd-order
quotient of U. In particular, if δ^(2^a)=1 in U for some a≥0, no such
cover exists.

**Proof.** Given (3), assign t_(Cg)↦w^g. This is well-defined because w
is fixed by C. The base relation (5) maps to

```text
(w^(r3r0))^−1 w^r0 w^−1 w^r3 = u^r0 u^−1 = 1.
```

All translated relations follow by applying the corresponding
automorphism. Thus the assignment extends to a homomorphism U→K. Its
image is a finite odd-order quotient and the image of δ is w^−1w^z≠1.

Conversely, let L◁U have finite odd index and δ∉L. It need not be stable
under G. Replace L by L0=∩_(g∈G) L^g. This is a normal G-invariant
subgroup contained in L. The diagonal map embeds U/L0 into the finite
product of the U/L^g, so U/L0 is finite and odd. The defect still survives.
Put K=U/L0 and let w be the image of t_C. The induced G-action fixes w
under C, relation (5) gives u^r0=u, and the surviving δ gives w^z≠w.
Proposition 1 now applies.

Finally, a finite odd-order group has no nonidentity element of 2-power
order, by the element-order divisibility in Lagrange's theorem. It kills
δ whenever δ^(2^a)=1 in U. ∎

This is a nonlinear version of the integral module criterion. On
abelianizing U, relation (5) becomes the signed cell relation generated
by e_C(1−r3)(1−r0). The earlier 55-term identity establishes that the
abelianized defect is killed by two. A relation δ²=1 in U itself is
stronger and applies without commuting any kernel elements.

## 4. The retained family and uniform transport

The source is Cunningham–Pellicer, *Tight chiral polytopes*,
[arXiv:2009.04566v1](https://arxiv.org/pdf/2009.04566v1), Table 2 row Γ2
and Theorem 4.8. Put β≥5, q=2^β, h=q/4 and ε1,ε2∈{−1,1}. Its rotation
presentation is

```text
a^8=b^q=c^8=1,       (ab)^2=(bc)^2=(abc)^2=1,
b a² = a² b^(1+ε1 h),       c² b = b^(1+ε2 h)c².          (6)
```

The source supplies existence, the exact presentation, marked orders,
tight normal form, order 64q and the intersection property. These are
retained mathematical inputs, not new constructions claimed here.

The reviewed phase58 and phase66 manuscripts prove the following further
facts for every parameter and sign pair. Their proofs and independent
reviews are exact dependencies of this manuscript.

* In the mirror rotation mix R≤P×P take
  Arot=(a,a⁻¹), Brot=(b,a²b), Crot=(c,c), and let μ swap the coordinates.
  R has order 128q. The full group G=R⋊<μ> has order 256q, and
  r0=μ, r1=r0 Arot, r2=r1 Brot, r3=r2 Crot.
* Both maximal standard parabolics are rank-three string C-groups.
  For C=<r1,r2> and z=[Crot²,Brot], their intersection is C⊔Cz and z
  centralizes C. Thus the interface (1) holds.
* N=<Brot⁴> is normal in G, has order q/4 and lies in C.
  The marked quotient G/N has order 1024 and is independent of β and
  the signs. The exact presentation becomes parameter-independent upon
  adjoining b⁴=1. This is a presentation argument, not an inference
  from a finite sample.
* Consequently the action of G on C\G is the same 128-point action
  for every member of the family. The reviewed JSON model records its
  four literal permutations. Its SHA-256 is
  `0247990a79729513799e8fe85d49dec74fade6b32a9aff8746a3fa4c0e8a2338`.

The normal-subgroup reduction does not require N to act trivially on all
of a possible kernel K. It acts trivially on the orbit of a C-fixed w:
for n∈N and g∈G,

```text
w^(gn) = w^((gng^−1)g) = w^g,
```

because gng⁻¹∈N≤C. This is exactly the orbit used by the universal
assignment in Proposition 2. Equivalently, the coset sets C\G and
(C/N)\(G/N) identify by the same marked words. Therefore U, its
distinguished generator and δ identify with one fixed presentation for
the entire family.

The model is transitive on {1,…,128}, has generated permutation group
of order 1024, and the point-1 stabilizer is exactly <r1,r2>, of order 8.
The coset C is labelled 1 and Cz is labelled 40. The base cell
(C,Cr3,Cr0,Cr3r0) is labelled (1,2,39,77); its orbit consists of 1024
distinct ordered quadruples. These assertions are replayed by exact
permutation arithmetic, separately from the family transport proof.

## 5. The exact original-cell identity

Enumerate the 1024 quadruples lexicographically, with row numbers
0,…,1023. A quadruple (a,b,c,d) supplies the original relation

```text
t_d^−1 t_c t_a^−1 t_b = 1.                              (7)
```

**Lemma 3.** Relations (7) force (t_1⁻¹t_40)²=1 in every group.

**Proof and certificate.** The complete free-word trace uses only
elementary substitutions. If a defining word has the form A x B with
x occurring once, its equation gives x=A⁻¹B⁻¹. If it has the form
A x⁻¹ B, it gives x=BA. Replace that generator in the other equations
and in the distinguished word, then freely cancel adjacent inverses.
Deleting the solved relation and freely trivial relations preserves the
presentation. All words, original row identifiers and substitutions
are explicitly recorded in `phase83_word_elimination.json`.

There are 111 such eliminations, leaving 17 generators and 512 nonempty
relations. The distinguished word becomes t_6⁻¹t_7. Original row 239,
whose cell is (30,112,76,33), becomes

```text
t_32⁻¹ t_16 t_6⁻¹ t_7 t_6⁻¹ t_7 t_16⁻¹ t_32 = 1.       (8)
```

Conjugating (8) by t_16⁻¹t_32 gives (t_6⁻¹t_7)²=1. Only 34 of the
eliminations are needed for (8) and the distinguished-word substitution;
together with row 239 they use the following 35 original row identifiers:

```text
69,26,29,2,134,14,163,58,6,22,12,0,197,77,57,135,389,
10,37,13,53,127,11,227,129,40,56,27,529,536,559,342,
248,439,239.
```

The generated `formal/OddKernelWord.lean` contains all 35 literal
quadruples, the 34 solved equations, both generic solve rules and the
final conjugation. The theorem `MathCompression.OddKernelWord.defect_square`
assumes just these displayed group equations for an arbitrary group K
and an arbitrary function t:ℕ→K, and proves the asserted square identity.
Each occurrence of an original cell in that proof is checked by kernel
evaluation of membership in the literal 35-cell list. There is no
assumption that K is abelian, finite, solvable or a matrix group.

The replay verifies that every one of those 35 literal cells belongs to
the actual 1024-cell orbit, and regenerates both the full trace and Lean
source byte-for-byte. Lean checks the group implication itself;
the orbit computation is a separate exact finite certificate. Thus
neither the GAP presentation simplifier nor a truncated p-quotient
calculation is a premise of Lemma 3. ∎

The second Lean theorem,
`MathCompression.OddKernelWord.defect_trivial_of_odd_card`, adds
`Finite K` and `Odd (Nat.card K)` and proves t_1=t_40. It uses the
order-divides-cardinality theorem. The first theorem reports only
`propext` and `Quot.sound`; the second also reports `Classical.choice`.
There are no proof placeholders or native-evaluation axioms. The
pinned toolchain is Lean 4.32.2 with the existing dependency manifest;
previously compiled dependency objects remain a stated trust input.

## 6. Uniform consequence

**Theorem 4.** For every β≥5 and both signs independently in (6), the
smallest regular maniplex G has no finite regular polytopal marked cover
whose kernel has odd order and whose maps on both maximal standard
parabolics are injective.

**Proof.** If such a cover existed, Proposition 1 would supply a finite
odd group K and w satisfying (3). The retained presentation reduction
identifies its orbit presentation with the fixed one in Section 5.
Proposition 2 maps its distinguished defect to w⁻¹w^z. Lemma 3 makes
that image square to one. Odd order forces w⁻¹w^z=1, contradicting (3).
All arguments apply to arbitrary finite odd K. ∎

This strictly removes the abelian-kernel hypothesis from the earlier
phase66 obstruction. It does not remove end injectivity, classify even
or mixed kernels, settle unrestricted minimal-cover uniqueness, or
address every source family. No new source is admitted to a measured
compression assembly by this separate theorem. The number of original
cells is a proof-certificate size, not a manuscript-compression ratio.

## 7. Attribution and reproduction

**[B] Borrowed:** Cunningham–Pellicer's Γ2 polytopes and presentation;
classical Sylow theory, group presentations, Lagrange's theorem, semidirect
products and string C-group recognition; the exact phase58/66 quotient
and intersection proofs with their independent phase73/74 reviews.

**[I] Repository derivations, priority not established:** the nonabelian
local-complement formulation, universal finite-odd-quotient criterion,
explicit cell elimination and their uniform Γ2 application. Independent
agent work checked the complement normalization and orbit-only transport;
its reviewed report records that contribution separately.

**[R] Shared consequence:** the same 128-point presentation and 35-cell
proof supply every β and sign pair. Abelianization recovers the kind of
module relation used in the earlier obstruction, while the group proof
allows nonabelian kernels.

**[V] Exact finite work:** the full marked permutation action, cell
orbit, 111-step trace and 35 selected cells. **[L] Lean scope:** precisely
the two word/cardinality theorems in Section 5. The geometric interface,
Sylow normalization and all-parameter source transport are written
proofs, not claimed as formalized. No [M] measurement or [O] open-conjecture
resolution is asserted.

From the study directory, with the pinned packages and compiler available:

```sh
python3 -O phase83_nonabelian_cover_check.py \
  --packages /path/to/pinned/packages \
  --lean /path/to/lean-4.32.2 \
  --output-dir /tmp/human-compression-odd-kernel-new
```

The output directory must be new. The runner validates package revisions,
tracked-file cleanliness, the exact reviewed model, all selected orbit
memberships, byte-identical regeneration, compilation and axiom reports.
An independently implemented trace checker replays the elementary
relations without importing the author generator; its report belongs
to the separate independent review. Discovery probes suggesting a
free-product normal form are excluded from this proof package.
