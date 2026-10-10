# A finite upper certificate for the equal-label presentation at eleven

This note concerns Conjecture 3.7 on page 11 of Mingchao Li and Wei-Juan
Zhang, *Regular 3-polytopes of type \(\{n,n\}\)*,
[arXiv:2505.09505v1](https://arxiv.org/abs/2505.09505v1), 14 May 2025.
The object under consideration is the literal presentation printed there.
In particular, all ten additional power relations are imposed on each
consecutive triple when \(n=11\).

Our main result here is an upper bound for that presented group, established
by finite certificates whose validity does not depend on the coset
enumerator used to find them. The separate matrix component, phase212,
supplies the matching image and an intersection witness. Section 5 explains
precisely how the two components give a counterexample to the existence
statement, rather than merely a counterexample to an assertion about one
chosen representation. The matrix component is an external input to this
note; its computations are not performed by the phase214 driver.

## 1. The presentation and the finite bound

For \(2\leq d\leq5\), let \(U_d\) have generators
\(r_0,\ldots,r_{d-1}\) and relations
\[
 r_i^2=1,\qquad
 (r_i r_j)^2=1\quad (|i-j|>1),\qquad
 (r_i r_{i+1})^{11}=1,
\tag{1}
\]
together with
\[
 \bigl((r_{i+1}r_{i+2})^k(r_i r_{i+1})^k\bigr)^2=1,
 \qquad 0\leq i\leq d-3,\quad 1\leq k\leq10.
\tag{2}
\]
There are no relations of type (2) for \(d=2\). Put
\(H_d=\langle r_0,\ldots,r_{d-2}\rangle\leq U_d\).
These are definitions of universal presented groups; no intersection
property or finiteness is assumed.

**Theorem 1.** The following index and order bounds hold.

| \(d\) | Certified bound for \([U_d:H_d]\) | Consequent bound for \(|U_d|\) |
|---:|---:|---:|
| 2 | — | 22 |
| 3 | 1,024 | 22,528 |
| 4 | 95,325 | 2,147,481,600 |
| 5 | 1,047,552 | 2,249,598,645,043,200 |

The three nontrivial index bounds are proved by the certificate procedure in
Sections 2–4. To deduce the order bounds, first observe that \(U_2\) is the
dihedral group of order 22. For example, writing \(a=r_0r_1\), every word
reduces to \(a^j\) or \(a^jr_0\), with \(0\leq j<11\); the usual action on
an eleven-gon shows that these 22 possibilities are distinct. Next, the
first \(d-1\) generators of \(U_d\) satisfy all the defining relations of
\(U_{d-1}\). Hence there is a surjection \(U_{d-1}\to H_d\), whether or not
that map is injective. Inductively,
\[
 |U_d|=[U_d:H_d]|H_d|
 \leq [U_d:H_d]|U_{d-1}|.
\]
The displayed finite index bounds therefore establish finiteness as well
as the stated order bounds. This argument does not retain the proof or
the order formula of the source's rank-three construction.

## 2. What an upper certificate must prove

A transitive permutation representation satisfying (1) and (2), with
\(H_d\) fixing a point, is insufficient to prove an index upper bound.
The stabilizer of that point might strictly contain \(H_d\). The one-point
representation, in which every generator acts trivially, illustrates the
problem: it satisfies every displayed relation for every group.

Our certificate consists of a proposed table \(T\) with \(N\) rows and
\(d\) columns. Its rows are names, not assumed distinct cosets. A separate
partial table \(P\) records only transitions already justified in the
actual group. The supplied entries of \(T\) guide the choice of names and
are checked for agreement when a transition is derived. They are never
accepted merely because they occur in \(T\).

**Lemma 2 (tree and relation certificate).** Let
\[
 G=\langle s_0,\ldots,s_{d-1}\mid s_i^2=1,\ R\rangle,
 \qquad H=\langle s_0,\ldots,s_{d-2}\rangle.
\]
Suppose a finite partial table is constructed by the following operations.

1. Begin with the name 1 for \(H\), and install
   \(P(1,i)=1\) for \(i<d-1\).
2. From a previously named coset, introduce a fresh name \(v\) by
   \(P(u,i)=v\). This defines its representative to be
   \(w_v=w_us_i\). Install the reverse transition \(P(v,i)=u\).
3. Read any relator from \(R\), starting at any named coset. If all its
   transitions except one are known, install the remaining transition
   forced by the relator, together with its reverse.

If every name is introduced in this way and all \(Nd\) transitions are
eventually known, then \([G:H]\leq N\).

*Proof.* Assign \(w_1=1\), and assign the word \(w_v\) on each use of
operation 2. We maintain the invariant
\[
 P(u,i)=v\quad\Longrightarrow\quad Hw_us_i=Hw_v.
\tag{3}
\]
The initial loops are valid because their labels belong to \(H\).
Operation 2 makes (3) true by definition, and its reverse is valid because
\(s_i^2=1\).

For operation 3, write the relator as \(p s_i q=1\), where the known
forward path labelled \(p\) reaches \(a\), and the known backward path
labelled \(q^{-1}\) reaches \(b\), from the same initial name \(u\).
By the induction hypothesis,
\(Hw_a=Hw_up\) and \(Hw_b=Hw_uq^{-1}\). The relation gives
\(p s_i=q^{-1}\), and therefore \(Hw_as_i=Hw_b\), as required.
Its reverse is again justified by involutivity. Names need not represent
distinct cosets at any stage of this reasoning.

When the table is complete, the set \(\{Hw_u:1\leq u\leq N\}\) contains
\(H\) and is closed under right multiplication by every generator.
All inverses are generators, so the set contains every right coset.
It has at most \(N\) members. This proves the lemma. ∎

The proof explains the distinction between an oracle table and an upper
certificate. A table which satisfies all relators can still fail to admit
the required deductions. Such a failure is reported as inconclusive; the
checker does not infer any negative mathematical statement from it.

## 3. The implementation of the deduction rule

The full checker is `phase214_table_deduction.cpp`. It is a short program
using only the C++ standard library. Its input consists of \(N,d\), followed
by the proposed generator transitions. The certificate format has one
column for each involution. Reverse edges use the already stated square
relations in (1).

The checker first installs the \(d-1\) facet loops. It then traverses the
proposed table breadth first. A supplied edge is used at this stage only
when its target has not previously been introduced. It therefore forms a
spanning tree of definitions of the kind in Lemma 2. An edge to an old
name is not admitted as a definition. Disconnected tables are rejected.

Next the program constructs the pair relators in (1) and every word in
(2) directly from the integers \(d\) and 11. For each relator and each
row, it scans as far as possible from the beginning along known edges,
and from the end along known reverse edges. If precisely one transition
remains, its endpoints are forced and the transition is installed. A
disagreement with the oracle table causes rejection. If a completely
known relator scan would identify different names, the checker also
rejects: it performs no unproved coincidence or merger of rows.

Full scans are repeated until all transitions have been derived or a scan
adds none. Only the first outcome is success. Thus a successful run is
exactly a finite instance of Lemma 2. In particular, neither termination
of a general coset-enumeration algorithm nor completeness of these simple
deduction rules is needed. The method is allowed to fail on other tables.

The input bounds and all consistency tests are explicit. The Python
driver does not use `assert`, and its checks remain active under `-O`.
Its digest checks bind the intended data and program before replay. Those
digests provide provenance; the mathematical upper-bound argument is the
deduction invariant, not the digests.

## 4. Certificate data and replay

The certificates were found by ACE as distributed with GAP 4.15.1.
`phase214_export_tables.g` records the literal presentation used for their
discovery. ACE is not needed to replay or verify the upper bounds.

The immutable compressed tables are listed in `phase214_tables.json`,
together with both compressed and uncompressed SHA256 values. The
successful deduction counts were as follows; counts include both
directions of a non-loop transition.

| Rank | Entries after tree definitions | Entries after successive full scans |
|---:|---:|---|
| 3 | 2,048 | 3,072 |
| 4 | 190,651 | 291,176; 381,292; 381,300 |
| 5 | 2,095,106 | 3,429,744; 3,443,404; 3,492,487; 3,788,936; 5,237,760 |

The final entry in each row is exactly \(dN\). Lemma 2 supplies the three
index bounds of Theorem 1, and the induction in Section 1 supplies the
order bounds.

From the directory containing these files, replay with

```sh
python3 -B -O phase214_check.py --out /tmp/phase214-fresh-replay
```

The output directory must not already exist. The dependencies are Python
3 and a C++17 compiler. The driver decompresses the tables into that fresh
directory, compiles the checker there, runs all three certificates, and
writes `report.json`. No files in the frozen package are modified.

Two negative controls are included. First, the one-point table with every
generator trivial is a valid permutation representation of all the
relations, with the facet fixing the unique point. The checker rejects it
as an upper certificate: the final generator transition cannot be derived
from the admitted tree and relator steps. Second, changing a defining facet
loop in the rank-three table causes an immediate contradiction with that
known loop. These controls test different boundaries: a valid action is
not an upper proof, and the initial subgroup constraint cannot be changed.

## 5. The quotient obstruction supplied by the matrix component

This section states the exact external inputs needed to turn Theorem 1
into the conjecture obstruction. It is included to make the logical
division between the two independently reviewed components explicit.

Let \(S=\operatorname{Sp}_4(32)\). The matrix component supplies a marking
\(s_0,\ldots,s_4\) of \(S\) with the following properties:

* the five involutions generate \(S\), satisfy (1) and (2), and have
  \(|s_is_{i+1}|=11\);
* \(S\) is nonabelian simple, of order
  \(32^4(32^2-1)(32^4-1)=1,124,799,322,521,600\);
* in \(C_2\times S\), with marked generators \((\epsilon,s_i)\), there is
  an element belonging to both four-generator endpoint subgroups whose
  \(S\)-coordinate does not belong to \(\langle s_1,s_2,s_3\rangle\).

The last item is a signed intersection witness. It is stronger than merely
showing that the unsigned natural matrix representation fails the
intersection property. Phase212 supplies its own explicit matrix and
membership certificates; they are not replaced here by an unverified
order estimate for an orthogonal intersection.

**Proposition 3.** Given these three matrix inputs, \(U_5\) is the marked
group \(C_2\times S\). No quotient of \(U_5\) with an adjacent product of
order 11 is a string C-group under the induced marking.

*Proof.* Sending \(r_i\) to \((\epsilon,s_i)\) respects every relation:
the \(S\)-coordinates do so by hypothesis, and every defining relator has
even length. Let \(L\) be the image in \(C_2\times S\). It projects onto
both factors. The kernel of its projection to \(S\) is either all of
\(C_2\) or trivial. In the latter case \(L\cong S\), and the other
projection gives a nontrivial homomorphism \(S\to C_2\), impossible for a
nonabelian simple group. Thus \(L=C_2\times S\).

This quotient has order 2,249,598,645,043,200, exactly the upper bound of
Theorem 1. The map \(U_5\to C_2\times S\) is consequently an isomorphism.

Now let \(N\) be the kernel of any quotient of \(C_2\times S\). The
intersection \(N\cap(1\times S)\) is normal in the simple group
\(1\times S\). If it is all of that factor, the quotient has order at
most two, and no adjacent marked product can have order 11. Otherwise
the intersection is trivial. For \(n\in N\) and \(s\in1\times S\), the
commutator \([n,s]\) belongs to both normal subgroups. It is therefore
trivial. Hence \(N\) centralizes \(1\times S\); because \(S\) has trivial
centre, \(N\leq C_2\times1\). In particular, the \(S\)-coordinate of
an element is determined by its image in every quotient still having
an adjacent product of order 11.

Take the signed intersection witness from the third input. Its image
still lies in both endpoint parabolics. If that image belonged to the
middle parabolic, its \(S\)-coordinate would belong to
\(\langle s_1,s_2,s_3\rangle\), contrary to the defining property of the
witness. The intersection property thus fails in every admissible
quotient. ∎

Every subgroup generated by a subset of the distinguished generators of
a string C-group inherits the intersection property. Consequently the
same obstruction excludes every rank \(d\geq5\) with constant label 11
and the printed consecutive-triple relations: the first five generators
would otherwise give the forbidden rank-five quotient. This conclusion
addresses the existence quantifier in Conjecture 3.7. It does not assert
that all quotients of a group with a defective marking must remain
defective; Proposition 3 proves that additional assertion for this group.

## 6. Attribution, edition, and formal scope

The conjecture and its presentation are due to Li and Zhang. The
characteristic-two symmetry construction used in the separate matrix
component comes from the earlier orthogonal-polytope framework; its
retained inputs are recorded there. The new work in this component is the
specific universal upper-bound certificate and its deduction replay,
together with the application of that bound in Proposition 3. The
one-hole deduction principle is the standard mathematical mechanism
behind coset enumeration, stated and proved here so that the supplied
certificate can be checked without trusting the discovery software.

No claim of a new general coset-enumeration principle is made. No source
theorem is silently reassigned to the present project. The source's
rank-three order formula is consistent with the rank-three certificate,
but is not needed as a retained proof input.

The primary target is specifically the arXiv v1 statement. A later article
appears in *Journal of Algebra* 695 (1 June 2026), 1–13,
[doi:10.1016/j.jalgebra.2026.01.041](https://doi.org/10.1016/j.jalgebra.2026.01.041).
Its publisher preview revises the introductory existence discussion and
credits prior work of Cunningham and Mixer. We have not verified the full
published text of its conjecture section. The present package therefore
does not claim that the printed v1 conjecture is unchanged in that edition,
that it remains open in the current literature, or that this obstruction
has publication priority.

The finite deduction program is not formalized in Lean. Its soundness is
proved in Lemma 2, its actual deductions are executable, and its code and
inputs are independently reviewable. The separate phase212 Lean component
formalizes parts of the general quotient-obstruction argument; its exact
coverage must be read from its own declaration list. This phase214 package
alone certifies Theorem 1. The full conjecture conclusion additionally
requires the matrix inputs and their independent review.
