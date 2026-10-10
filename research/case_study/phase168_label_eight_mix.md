# Equal labels eight times an admissible odd label

This additive consequence uses the class-four construction
E8.Construction and the previously reviewed marked parity-fiber theorem.
It extends the finite-existence range of the equal-label question. It
does not identify the universal source presentation.

**Corollary.** In every rank \(d\geq3\), there is a finite regular
polytope with constant adjacent label \(8n\), satisfying
\[
 \bigl((s_{i+1}s_{i+2})^k(s_is_{i+1})^k\bigr)^2=1
 \qquad(0\leq i<d-2,\ k\in\mathbb Z),
\]
whenever
\[
 n\in\{3\}\cup\{2^e+1:e\geq2\}\cup\{2^e-1:e\geq3\}.
\]
The separate construction E8.Construction gives label eight itself.

**Proof.** Let \(E=P_d\) be the finite group constructed in the
label-eight manuscript. Its distinguished involutions \(e_i\) generate
a string C-group of order \(2^{5d-7}\); every adjacent product has order
eight. Its parity homomorphism
\(\varepsilon:E\to\mathbb F_2\) sends each \(e_i\) to one, and
the displayed power words vanish for every integer exponent.

For \(n=3\), take \(G=S_{d+1}\) with its adjacent transpositions
\(g_i\) and the sign homomorphism \(\delta:G\to\mathbb F_2\).
The interval-block proof in the retained label-three construction gives
full IP; the outer commutation and period-three calculation give the
additional power relations.

For the other values, put \(q=2^e\) and \(n=q+1\) or \(q-1\)
in the stated range. Use the construction in §2 of
`phase124_even_label_mix.md`: choose an even \(D\geq d\), form the
constant-coefficient quadratic space on \(\mathbb F_q^D\), and
retain the first \(d\) coordinate symmetries. The adjacent coefficient
\(\alpha\ne0\) is selected from an eigenvalue of exact order n.
The retained Brooksbank–Ferrara–Leemans theorem gives full IP for these
markers and exact adjacent order n, including the stated restriction
\(q\geq8\) for \(q-1\). The whole-ambient singular-vector identity
of `phase124_equal_label_char2_bridge.md` gives every additional power
relation on this actual ambient space.

Its polar determinant is \(\alpha^D\ne0\). The classical Dickson
homomorphism on the nondegenerate even-dimensional orthogonal group,
\(g\mapsto\operatorname{rank}(g-I)\bmod2\), therefore restricts to
a homomorphism \(\delta:G\to\mathbb F_2\) taking every symmetry
\(g_i\) to one. This use retains the cited Dickson theorem; it does
not infer parity from a quotient of an odd-dimensional space.

The finite group E is a two-group, G has odd adjacent orders, both
markings have full IP and string commutation, and their genuine parity
characters have the same nonzero marker value. Thus all hypotheses of
the marked parity-fiber theorem are satisfied. It gives full IP for
\[
 H=\langle s_i=(e_i,g_i):0\leq i<d\rangle\leq E\times G.
\]
The markers are nonidentity involutions and satisfy the string relations.
The order of \(s_is_{i+1}\) is exactly
\(\operatorname{lcm}(8,n)=8n\), because the two coordinate orders are
eight and the odd number n. Every displayed power word is the identity
in both coordinates. The retained string-C-group/polytope correspondence
now gives the required finite regular polytope. ∎

This is an application of already proved interfaces with their hypotheses
discharged explicitly. The new two-primary input is E8.Construction.
The odd-label constructions, their intersection theorem and the Dickson
character remain credited to the retained work described above. The
generic group-theoretic parity-mix theorem is also verified in Lean,
but the concrete E and G constructions and the complete geometric
corollary are not yet formalized. Historical novelty and current
openness of these particular specializations have not been established.

For example the added all-rank labels include 8, 24, 40, 56, 72, 120
and 136. No new principal-source replacement, source-length factor or
infinite compression ratio is assigned to these question results.
