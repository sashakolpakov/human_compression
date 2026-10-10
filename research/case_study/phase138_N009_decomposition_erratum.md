# Mandatory correction: the diagonal factors in N009 Lemma 5.1(ii)

This additive correction preserves the already frozen manuscripts. It applies to the quoted decomposition in §7.4 of `phase117_two_group_application.md` (SHA-256 `d8b037be2e356416056eb3772be5e020ee7e598cd621ad6e79f0dab79a84c56f`) and the corresponding quoted background statement in the older source-bank manuscript. It is incorporated directly in the new Module A version 2. The affected displayed factors came from the primary source itself; they are not a new classification result.

The exact source is Gomi–Loyola–De Las Peñas, *String C-groups of order 1024*, Contributions to Discrete Mathematics 13(1) (2018), 1–22, DOI 10.55016/ojs/cdm.v13i1.62475. The private primary PDF is `sources/phase17_gomi_loyola2018.pdf`, SHA-256 `0618a57cb5ff35c13587877818a2e77bce442cf2c561f204b6d5e5e095fa2fda`. The displayed error is on physical and printed page 17, Lemma 5.1(ii). That entire page was visually checked in this phase; its text extraction agrees with the display.

With the source markers renamed a,b,c and right conjugation x^y=y⁻¹xy, the printed diagonal factors are

\[
 \langle b,b^a\rangle\quad\hbox{and}\quad\langle b^c,b^{ac}\rangle.
\]

These cannot be the asserted dihedral factors of order 2s for general s. Indeed

\[
 b b^a=baba=(ba)^2.
\]

Smoothness gives |ab|=4, so b and b^a are distinct commuting involutions and their subgroup has order four, independently of s. In particular the claimed factor order is false for s>2 (also for s=1). This elementary obstruction requires no computational inference.

The corrected diagonal decomposition, with D_(2s) denoting a dihedral group of order 2s and D_2=C_2, is

\[
 G=\bigl(\langle b,b^{ac}\rangle\times
             \langle b^a,b^c\rangle\bigr)\rtimes\langle a,c\rangle
   \cong(D_{2s}\times D_{2s})\rtimes(C_2\times C_2).
 \tag{E1}
\]

Here s is any positive integer in the finite diagonal family. The correct square-family decomposition in Lemma 5.1(i) is unchanged.

*Proof of (E1).* Work in the affine convention already used in Module A §7.4:

\[
 a(x,y)=(1-x,y),\qquad b(x,y)=(y,x),\qquad c(x,y)=(x,-y),
\]

and quotient W=Z²⋊D_8 by

\[
 L_s=\langle(s,s),(s,-s)\rangle.
\]

This is the complete diagonal quotient of [4,4] obtained by adding (abc)^(2s)=1: (abc)² is translation by (1,1), and its signed-permutation orbit generates exactly L_s after taking the s-th power. The normal form of W is proved in Module A §3. Thus the model identifies the full presentation, rather than just a group of the same order.

Put A=⟨b,b^(ac)⟩ and B=⟨b^a,b^c⟩. Their reflecting axes are respectively x−y=0,1 and x+y=1,0. The products b b^(ac) and b^a b^c are translations by (−1,1) and (1,1), respectively. Each has exact order s modulo L_s. In each factor its reflection remains nonidentity because its linear part is nonidentity, so both factors have exact order 2s; for s=1 each is C_2.

Every A-reflection axis is perpendicular to every B-reflection axis, so the four displayed cross-generators commute in W. Alternatively, their affine formulas give the same products in either order. The linear parts occurring in A are 1 and the coordinate swap S, whereas those in B are 1 and −S. Hence an element of A∩B must be a translation. The two translation subgroups lie along the independent lattice directions (−1,1) and (1,1). If k(−1,1)−l(1,1) lies in L_s, then s divides both k and l; thus A∩B=1 in the quotient.

Conjugation by either a or c interchanges the two factors. The linear parts of a and c lie outside the linear-part subgroup {1,S,−S,−1} of AB. The only remaining possible nonidentity element of AB∩⟨a,c⟩ is ac. Every affine element of AB with linear part −1 has translation coordinates of equal parity: b b^a has translation (1,1), and the available translations in AB change that vector by integer combinations of the two diagonals. The lattice L_s preserves this parity equality. In contrast ac has translation (1,0). Therefore ac is outside AB too. Since b∈A, the subgroups A,B,⟨a,c⟩ contain all original generators. They give the internal semidirect product (E1), including the stated complement action. This proves the correction for every s≥1.

## Scope and impact

The finite smooth-quotient classification, its two families, orders 8s² and 16s², complete presentations and word orders remain the retained prior interface. Only the named factor pairing in the diagonal structural display is corrected. In the new edition these structural decompositions are independently supplied by the shared affine argument, with the positive-integer boundary just checked. Attribution of the original classification to the source's cited McMullen–Schulte input is retained; this note does not imply that the error occurs in that earlier input.

The center formulas of source Lemma 5.2 are proved in Module A using the actual affine translations and signed-permutation action. That proof does not use the incorrect pairing. Likewise the universal-kernel census, complete presentation checks, marked facet identifications and every order-1024 classification count do not read either decomposition as an assumption. Their four exact programs and all recorded finite outputs are unchanged. There is therefore no reason to repeat the unchanged exhaustive computations for this correction.

The source-contract ledger must no longer quote the false factor pairing as a retained true statement. Its Lemma 5.1 row is replaced additively by the corrected factors (E1), explicitly preserving the original finite classification and positive parameter range. The correction changes neither the admitted principal classification target nor the numerical count, but it is mandatory for the accuracy of the quoted structural background in older expositions. Independent review of this correction is still required. No priority, open-conjecture, Lean or compression claim is made.
