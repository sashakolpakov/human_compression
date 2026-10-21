# A rank-four regular polytope for PSU₄(7)

Original phase-fourteen finite construction, 10 October 2026. This note gives one exact witness in the previously untreated congruence class. It does not assert uniform existence for every \(q\equiv3\pmod4\) or a determination of publication priority. The frozen phase-thirteen files are unchanged.

Let \(E=\mathbb F_7[t]/(t^2-t+3)\), with conjugation \(\bar x=x^7\), and put

\[
i=4+6t,\qquad a=6+2t,\qquad b=2,\qquad c=-2.
\]

Then \(i^2=-1\), \(\bar i=-i\), \(\bar a=-a\), \(a^2=3\) and \(a^2+bc=-1\). Define

\[
r_0=\operatorname{diag}(1,1,-1,-1),\qquad
r_1=\begin{pmatrix}1&0&0&0\\0&0&0&1\\0&0&-1&0\\0&1&0&0\end{pmatrix},
\]
\[
r_2=\begin{pmatrix}0&i&0&0\\i&0&0&0\\0&0&a&b\\0&0&c&-a\end{pmatrix},\qquad
r_3=\begin{pmatrix}0&0&1&0\\0&0&0&1\\-1&0&0&0\\0&-1&0&0\end{pmatrix}.
\]

All four matrices have determinant one and preserve the Hermitian form with matrix \(I_4\). Their squares are respectively \(I,I,-I,-I\). The distant pairs commute projectively, with lift signs \(r_0r_2=r_2r_0\), \(r_0r_3=-r_3r_0\), \(r_1r_3=-r_3r_1\).

**Exact finite result.** Their projective images form a string C-group for \(\operatorname{PSU}_4(7)\), of type \(\{4,24,4\}\).

The standalone [GAP checker](phase14_unitary_q7_check.g) verifies the field polynomial and coordinates, all natural matrix identities, and the action on all 2,752 totally isotropic two-dimensional subspaces. It then computes the generated permutation-group order

\[
1,165,572,172,800
=\frac{7^6(7^2-1)(7^3+1)(7^4-1)}{\gcd(4,8)},
\]

the three adjacent product orders, all sixteen distinguished subgroup closures, and all 256 exact subgroup intersections. The two maximal parabolics have orders 56,448 and 138,297,600 and intersect in the middle dihedral subgroup of order 48. The whole intersection property is checked, not just this last equality.

The group identification uses an order sandwich. The tuple lies in SU₄(7). Its action on the complete isotropic-plane set factors through the scalar center of order four, so its image is a subgroup of an image of PSU₄(7). The computed image already has the full order of PSU₄(7); hence the induced map from PSU₄(7) onto the ambient action image is an isomorphism and the tuple generates that image. This does not assume faithfulness in advance or use a simple-group recognition routine, ATLAS generators, or a subgroup database. Retained inputs are the standard special-unitary order formula, the size of its scalar center, the number of maximal totally isotropic planes and exact GAP core group algorithms.

Run from a disposable directory containing the checker with GAP 4.15.1:

```text
gap -q -T phase14_unitary_q7_check.g
```

It writes [phase14_unitary_q7_check.json](phase14_unitary_q7_check.json); the accompanying log records the actual run. The field polynomial and low-to-high coordinates make the chosen matrices independent of an undocumented primitive-element convention, although this checker verifies those coordinates inside GAP's field implementation rather than introducing a second field backend.

There is a useful template behind the example. For any odd \(q\equiv3\pmod4\), take \(i^2=-1\), \(\bar i=-i\), any \(\bar a=-a\), and \(b\ne0\) with \(b\bar b=1+a^2\), setting \(c=-\bar b\). The displayed matrices still lie in SU₄(q) and satisfy the same projective string relations. Full generation and the intersection property do **not** follow from those identities alone. For example, the exploratory q=7 marking \(a=b=Z(49)^4\) generates a proper subgroup of order 56,448. Further uniform assertions require separate proofs and will be recorded separately.

This is an exact finite mathematical certificate, subject to the retained computational and group-order inputs. Internal reviews and subsequent independent reruns, if performed, are recorded separately; none is silently claimed here.
