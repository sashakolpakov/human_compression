# A uniform class-four construction for label eight

Frozen author manuscript, 10 October 2026, pending independent review. The finite collector has passed the complete critical-pair check described below. This manuscript supplies the uniform argument turning that finite check into a construction in every rank. No universal-presentation identification is claimed.

## 1. The constructed groups

**Theorem E8.Construction.** For every integer \(d\geq3\), there is a finite group \(P_d\) with an ordered generating family of nonidentity involutions \(r_0,\ldots,r_{d-1}\) such that:

- distant generators commute, and every adjacent product has order eight;
- the full marked intersection property holds;
- for every consecutive triple and every integer \(k\),
\[
                  \bigl((r_{i+1}r_{i+2})^k(r_ir_{i+1})^k\bigr)^2=1;
\]
- \(|P_d|=2^{5d-7}\), and \(P_d\) has nilpotency class exactly four;
- there is a homomorphism \(P_d\to\mathbb F_2\) taking every distinguished generator to (1).

More precisely, if \(a_\ell(S)\) is the number of intervals of length \(\ell\) contained in a support \(S\subseteq\{0,\ldots,d-1\}\), then
\[
                  |(P_d)_S|=2^{a_1(S)+2a_2(S)+a_3(S)+a_4(S)}.
\]
The proof gives a binary normal form for every element and an exact support criterion for membership in every parabolic. It does not assume the desired intersection property.

Via the classical correspondence between string C-groups and regular abstract polytopes, these groups give finite examples of equal label eight in every rank, satisfying the displayed additional power relations. This correspondence remains a retained input. The theorem constructs images of the source presentation, rather than identifying that presentation's universal group.

## 2. A positive presentation

Use the following ordered letters, each ordered by increasing subscript within its row:
\[
\begin{array}{c|c|c}
\text{letters}&\text{index range}&\text{support}\\\hline
r_i&0\leq i<d&[i,i]\\
x_i&0\leq i<d-1&[i,i+1]\\
y_i&0\leq i<d-2&[i,i+2]\\
z_i&0\leq i<d-3&[i,i+3]\\
w_i&0\leq i<d-1&[i,i+1].
\end{array}
\]
All \(r\)'s precede all \(x\)'s, followed by \(y\)'s, \(z\)'s and \(w\)'s. There are \(5d-7\) letters. An empty row, such as the \(z\)-row at \(d=3\), contributes no letters.

Every letter squares to the empty word, except that \(x_i x_i\) rewrites to \(w_i\). For two distinct letters \(b>a\), rewrite
\[
                                ba\longrightarrow ab\,c(b,a),
\]
where the only nonempty correction words are the following. A row is used only when all the displayed input letters exist.
\[
\begin{array}{c|c|c}
b&a&c(b,a)\\\hline
r_{i+1}&r_i&x_iw_i\\
x_i&r_i& w_i\\
x_i&r_{i+1}&w_i\\
x_i&r_{i+2}&y_i\\
x_i&r_{i-1}&y_{i-1}w_{i-1}w_i\\
x_{i+1}&x_i&w_iw_{i+1}\\
x_{i+2}&x_i&z_i\\
y_i&r_{i-1}&z_{i-1}\\
y_i&r_{i+1}&w_iw_{i+1}\\
y_i&r_{i+3}&z_i.
\end{array}                                                    \tag{1}
\]
Every omitted correction is empty. In particular the \(z\)'s and \(w\)'s commute with all letters. Every letter in a correction lies strictly after \(b\). Every power correction lies strictly after the letter being squared. Most importantly, every output letter has support contained in the union of the input supports. Both assertions follow immediately from the displayed ranges and table, and are checked for all rules in the finite certificate.

We initially interpret these as relations of a monoid of positive words, not as an already consistent polycyclic group presentation. Termination and confluence will prove consistency, after which the existence of inverses follows from the power relations.

## 3. Termination — E8.Termination

Here is a termination argument for any finite alphabet with rules of the same triangular form. It does not rely on finite experimental ranks.

Define a strict order on words recursively in the size of the alphabet. On the empty alphabet there is only the empty word. For a nonempty alphabet with smallest letter \(a\), write a word uniquely as
\[
                       u_0a u_1a\cdots a u_s,
\]
where every \(u_j\) is a word on the higher letters. First compare the number \(s\) of occurrences of \(a\). At equal \(s\), compare the tuple \((u_0,\ldots,u_s)\) lexicographically using the recursively defined order on higher-letter words. Smaller counts and smaller tuples mean smaller words.

This is a well-founded order. In a descending chain the nonnegative count \(s\) can decrease only finitely often; once it is fixed, a lexicographic product of \(s+1\) well-founded orders is well-founded. The same induction shows that deleting a nonempty suffix makes a word strictly smaller: either it removes a smallest letter, or the smallest-letter count remains fixed and the last higher-letter block is replaced by a proper prefix.

A rewrite involving only higher letters occurs inside one block and decreases that block by induction. A smallest-letter square deletes two occurrences of the smallest letter, so it decreases the first comparison coordinate. Finally, a swap \(ba\to ab\,c(b,a)\) moves a smallest letter \(a\) left across the final letter \(b\) of its preceding block. That preceding block becomes a proper prefix; only subsequent blocks can grow. The correction contains only higher letters, so the smallest-letter count remains unchanged. Hence this rewrite also strictly decreases the word.

Every rewrite therefore decreases a well-founded order. In particular every collection path terminates, including the deterministic leftmost procedure used by the certificate.

## 4. A finite certificate for all ranks — E8.Locality and E8.Confluence

Every left side of a rule has length two, and there is exactly one rule for each nonincreasing pair of letters. Two reductions in disjoint positions commute. Thus the only overlapping ambiguities are the two reductions of a three-letter word
\[
                              abc,\qquad a\geq b\geq c.        \tag{2}
\]
Equality is allowed; this includes ambiguities involving powers.

The certificate instantiates the presentation at rank fourteen. It checks all 2,016 rules for triangularity and preservation of the union of supports. It then enumerates all
\[
                             {65\choose3}=43,680
\]
triples of the form (2) on its 63 letters. For each triple it reduces the left pair first and the right pair first, and collects both results to irreducible words. The two results agree in every case. No group order, nilpotent quotient routine, or assumed consistency flag is used.

We now show why rank fourteen suffices for every rank, including every intermediate word in either reduction path. Fix an arbitrary initial triple in rank \(d\), and let \(S\) be the union of its three interval supports. Its cardinality is at most twelve, and it has at most three consecutive components. Translate each component, preserving all its internal distances, and place one unused index between consecutive translated components. The resulting support \(S'\) lies in an interval of length at most
\[
                       |S|+(\#\text{components of }S)-1\leq14.
\]
Pad the surrounding ambient index set to rank fourteen if necessary.

A basis letter has support contained in \(S\) exactly when its interval lies within a single component of \(S\). Translation on that component gives a bijection between all such letters and all rank-fourteen letters whose support lies in \(S'\). It preserves letter type, support length, and the order of anchors. Consequently it preserves the total basis order. Valid boundary conditions are preserved as well: an image support is contained in \(S'\subseteq\{0,\ldots,13\}\), and its inverse image is contained in the original rank-\(d\) support. No nonexistent boundary letter is introduced.

This bijection preserves every rule on those letters. For input supports with connected union, the inputs lie in one component of \(S\), so a common translation preserves all anchor differences in (1). For input supports with disconnected union, the correction word in (1) is empty. Their images also have disconnected union: an internal gap inside one component is unchanged, and different components still have the deliberately retained unused separator. Thus no new nontrivial correction is created by compression. Power rules plainly preserve the letter type. The same argument in reverse proves exact agreement of the two restricted rule systems.

Every intermediate letter in a reduction of the initial triple remains supported in \(S\), because each rule preserves the union of supports. The preceding bijection therefore applies to the entire reduction, not merely its initial three letters. Its image is exactly the rank-fourteen reduction under the same choice of positions. The rank-fourteen critical-pair certificate consequently proves joinability of every overlapping ambiguity in every rank.

Together with the commuting disjoint reductions, this proves local confluence. Termination upgrades local confluence to confluence: apply well-founded induction to a word with two reduction paths. Join their first steps by local confluence, then apply the induction hypothesis to the resulting proper descendants to join the remaining paths. This is the usual terminating-rewriting diamond argument; its hypotheses have now been proved for the actual presentation.

## 5. The group and its normal forms — E8.NormalForm

The irreducible words are precisely the strictly increasing words in the ordered basis. Thus every basis letter occurs with exponent zero or one. Confluence says that each congruence class of positive words has exactly one such representative: a defining relation preserves the terminal word, and equal terminal words are connected by the defining reductions. There are exactly \(2^{5d-7}\) normal forms.

Let \(P_d\) be the quotient monoid. Every generator is a unit. The \(r,y,z,w\) letters square to one, and \(x_i^2=w_i\), \(w_i^2=1\), imply \(x_i^4=1\). Hence \(P_d\) is a group of the asserted order. The commutator convention used here is
\[
                            [a,b]=a^{-1}b^{-1}ab.
\]
The swap rule becomes \([b,a]=c(b,a)\). From its first row and \(x_i^2=w_i\), we obtain
\[
 [r_{i+1},r_i]=x_iw_i=x_i^{-1},\qquad
 [r_i,r_{i+1}]=x_i.
\]
The table also gives
\[
 y_i=[x_i,r_{i+2}],\qquad z_i=[y_i,r_{i+3}],\qquad w_i=x_i^2.       \tag{3}
\]
Every auxiliary generator is consequently generated by the \(r\)'s on exactly its stated support. The \(r_i\) therefore generate the whole group.

Each \(r_i\) is a nonidentity involution, because its one-letter normal form is distinct from the empty word. Since
\[
                    (r_ir_{i+1})^2=x_i,\qquad x_i^2=w_i\ne1,
\]
and \(w_i^2=1\), the adjacent product has exact order eight. Nonadjacent distinguished generators commute by the omitted rows of (1).

## 6. All parabolics and all intersections — E8.IP

For a support \(S\), let \(K_S\) be the set of normal forms using only basis letters whose entire supports are contained in \(S\). This is a subgroup. Concatenating two such words and collecting cannot create a letter outside \(S\), by support preservation. The inverse of any permitted basis letter also uses only its support: the involutory letters are their own inverses and \(x_i^{-1}=x_iw_i\). Reversing a product and collecting therefore keeps it in \(K_S\).

Every \(r_i\) with \(i\in S\) belongs to \(K_S\), so \((P_d)_S\leq K_S\). Conversely, (3) expresses every permitted auxiliary letter by distinguished generators on its own support. Hence every such letter belongs to \((P_d)_S\), and
\[
                              (P_d)_S=K_S.                       \tag{4}
\]
A normal form belongs to both \(K_S\) and \(K_T\) exactly when every letter in it has support contained in both \(S\) and \(T\). By uniqueness of normal form this is equivalent to membership in \(K_{S\cap T}\). Equation (4) proves full IP.

There is one \(r\)-coordinate for each contained singleton, two coordinates \(x,w\) for each contained interval of length two, one \(y\)-coordinate for each contained interval of length three, and one \(z\)-coordinate for each contained interval of length four. Counting the binary choices proves the stated parabolic order formula, including the empty support.

## 7. The additional power relations — E8.Relators

All rules supported on three consecutive indices agree, after translation, with the rank-three presentation. Their normal forms embed in every higher-rank presentation by the support argument. It is therefore enough to collect the source words at rank three.

Put \(A=r_0r_1\) and \(B=r_1r_2\). The certificate obtains the following normal forms for \(B^kA^k\):
\[
\begin{array}{c|l}
k& B^kA^k\\\hline
0&1\\
1&r_0r_2x_0x_1y_0w_1\\
2&x_0x_1w_0w_1\\
3&r_0r_2w_0w_1\\
4&w_0w_1\\
5&r_0r_2x_0x_1y_0w_0\\
6&x_0x_1\\
7&r_0r_2.
\end{array}
\]
Squaring each entry and applying (1) gives the empty normal form; all eight reductions are checked explicitly. Since \(A\) and \(B\) both have order eight, their powers depend only on \(k\bmod8\), including negative integers. The required relation follows for every integer and, by translation, every consecutive triple in every rank.

## 8. Nilpotency and parity — E8.Class and E8.Parity

Let
\[
 N_2=\langle x,y,z,w\rangle,\quad
 N_3=\langle y,z,w\rangle,\quad
 N_4=\langle z,w\rangle.
\]
The table shows that these subgroups are normal, that \([P_d,P_d]\leq N_2\), \([N_2,P_d]\leq N_3\), \([N_3,P_d]\leq N_4\), and that \(N_4\) is central. To check these inclusions it suffices to conjugate the displayed subgroup generators by the generating \(r_i\)'s; every resulting correction is in the indicated next subgroup. Thus the group has class at most four. It has class exactly four because
\[
                      [[[r_0,r_1],r_2],r_1]=w_0w_1\ne1.
\]
The last inequality follows from its nonempty binary normal form.

During collection, each \(r_i\)-count is preserved modulo two: swaps merely reorder the distinguished letters, correction words contain no \(r\)'s, and a distinguished square removes two copies. The vector of \(r\)-coordinates of a normal form therefore defines a homomorphism \(P_d\to\mathbb F_2^d\). Composing with the sum of coordinates gives the asserted genuine parity homomorphism, taking each \(r_i\) to (1).

This parity interface is exactly the one needed to apply the already proved marked parity-mix theorem with an orientable odd-label string C-group. If that factor has odd label \(n\) and satisfies the additional power relations, the mixed adjacent order is \(\operatorname{lcm}(8,n)=8n\), the power words vanish in both coordinates, and the full mixed IP follows from the parity-mix theorem. A final source-specific corollary must bind the odd factor's construction and genuine character separately; those existence inputs are not supplied by the collector.

## 9. Why class four is necessary — E8.Class3Obstruction

Suppose \(a,b,c\) are involutions, both \(ab\) and \(bc\) have order eight, the source relation at \(k=2\) holds, and the generated group has nilpotency class at most three. Put \(A=(ab)^2=[a,b]\) and \(B=(bc)^2=[b,c]\). Both lie in the commutator subgroup. Since \([\gamma_2,\gamma_2]\leq\gamma_4=1\), they commute. The source relation says \((BA)^2=1\), so
\[
                         (ab)^4=A^2=B^2=(bc)^4.
\]
This is a nonidentity element of both adjacent dihedral subgroups. It is not \(b\): if \((ab)^4=b\), then \(b\) and \(a=(ab)b\) both lie in the cyclic group \(\langle ab\rangle\), so they commute, contradicting the order eight of \(ab\). Hence the common element lies outside \(\langle b\rangle\), violating the required intersection property.

Thus no nilpotent example of class at most three can meet the rank-three label-eight requirements. The construction above attains class four and is optimal in that precise sense. This lower bound does not identify the universal group or exclude nonnilpotent constructions.


## 10. Exact verification and provenance

The standard-library checker is `phase161_label_eight_collector.py`. Its default run needs only that file and a fresh output path:

```sh
python3 -B -O phase161_label_eight_collector.py --report NEW_REPORT.json
python3 -B -O phase161_label_eight_controls.py --output-dir NEW_CONTROLS
```

The first command rebuilds the actual rule table, verifies its structural properties, checks every one of the 43,680 critical pairs, checks 49 auxiliary-generator identities, verifies the rank-three normal forms printed in §7 and their squares, and records the nonzero class-four witness. The critical-pair normal-form digest is `c5f150119dbd84877056d3f6d97672f76463a7d9f54f325b81847d949bb1dd38`; the complete §7 row digest, including the inner and squared normal forms, is `6ed5cd8b3395789ea4e0f2b04ad0c1c1c2022b33fd6332dc629666faa38f2606`. Both are output bindings rather than substitutes for replay. The run takes about 0.22 seconds in the author environment.

The ten controls remove one of three necessary commutator corrections, collapse an edge square, introduce an unsupported power correction, introduce a nontriangular power correction, and test four occupied output paths including live and dangling symlinks. The four algebraically plausible mutations are rejected by actual failed critical pairs; the two structural mutations are rejected by the corresponding structural check. The original source is hash-bound and left unchanged. Existing outputs are preserved.

The commutator table was suggested by exact nilpotent-quotient computations on the source relators in ranks three through seven. A copy of the discovery table is retained as provenance, not as a consistency proof. Those exploratory quotient calculations are not rerun by this certificate. The new uniform argument consists of the positive presentation, the termination and support-compression proofs, the complete finite ambiguity certificate and its confluence consequence, and the normal-form support theorem. The general rewriting diamond argument and the elementary commutator fact used in §9 are classical. Historical novelty of this specific construction has not been investigated.

The underlying question is the equal-label presentation in Li–Zhang, *Regular 3-polytopes of type {n,n}*, arXiv:2505.09505v1, Conjecture 3.7, as transcribed and audited in the existing question track. The construction supplies the label-eight finite-existence case in every rank. It does not settle that conjecture for every label, prove the universal group's intersection property, or identify the maximal class-four quotient of the source presentation. Finite presentations with additional relations may have smaller images, and no converse presentation is asserted here.

The parity-mix application in §8 uses an existing theorem, with its actual hypothesis checks; it is not a claim that this collector formalizes the odd-label factor or the group-to-polytope correspondence. The present all-rank theorem is a written proof with an executable finite certificate. It is not yet a Lean theorem. Any later Lean certificate for the finite ambiguity lemma alone must retain the separate boundary around the uniform termination/locality argument.

The checkpoint follows the GKM discipline of preserving already established interfaces, recording the acquisition of new proof and certificate bodies, and charging later attachments separately. It makes no source-paper replacement claim, compression-ratio claim, measured payback claim, or optimal-description-length claim.
