# Independent review of the odd unitary diagonal rank-three construction

Date: 2026-10-10. Internal review, not external peer review; priority remains unverified. Exact reviewed files and the independently executed finite base are bound in the companion JSON.

**Verdict: the full written proof passes review.** It proves the proposed rank-three representation of the diagonal index-two extension U₂(q), uniformly for odd q≥5 and using a separate finite certificate for q=3. The resulting exact rank set {3,4} additionally retains the earlier upper bound and rank-four constructions. It does not assert a rank-three representation of the simple socle PSU₄(3).

## Scalar normalization and rank-one generation

The block swap is an anti-isometry. The chosen scalar has norm −1, so its product with that swap is unitary and is a projective involution. Its determinant supplies exponent two in the norm-one determinant group, while the reflection supplies exponent (q+1)/2. Modulo fourth powers these generate exactly the diagonal subgroup of order two, in both congruence classes of q. This fixes the missing diagonal class without treating an anti-isometry as an ordinary unitary matrix.

The reflection vector has norm −2. I checked the displayed invariant isotropic plane, root parameter, Jordan-three calculation and nonzero pairing with its reflected plane. Choosing a primitive field element forces its square to generate the full field; the order comparison works already at q=5.

The two projected unipotents generate the full rank-one special linear group. I reopened [Leemans–Moerenhout–O'Reilly-Regueiro, Proposition 2.3](https://arxiv.org/html/1606.08017), which supplies both projective rank-one maximal-subgroup lists. Distinct fixed points and characteristic-p orders exclude the solvable alternatives. The difference of the two projective trace invariants generates the whole field, including against conjugates of PGL subfield groups. The exceptional trace fields in characteristics three and five are too small; larger characteristics are excluded by element order. Perfection removes the central-cover ambiguity. No dimension-four maximal-subgroup classification is used.

## The parabolic kernel and root extraction

The pointwise stabilizer of a maximal isotropic plane in the full unitary group is exactly the indicated abelian radical. If its intersection with the generated stabilizer were trivial, the preimage of SL₂(E) would be an isomorphic copy of that group. It lies in SU₄ because the determinant of a lift restricting to g is det(g)/overline(det(g)); this is the necessary adapter when the whole stabilizer is not special unitary.

The prime-to-characteristic torus admits an invariant complement. Its two dual weights are distinct from the two weights on the isotropic plane, and the complement is itself isotropic. I checked all four off-block cocycle equations and their elimination order. Each successive additive function has a linearized-polynomial expansion. None of its possible torus weights equals 2p^j modulo q²−1 for 0≤j<2e, including the boundary cases q=5 and q=9. Thus the lifted root groups and the Weyl element preserve the complement, contradicting the actual Jordan block of size three.

The radical irreducibility argument uses only additive subgroup operations, not an assumed F_q-vector-space structure. The trace pairing first produces a nonzero diagonal coordinate. Positive and negative root parameters isolate norm terms and then all off-diagonal terms; norm surjectivity supplies every base-field diagonal entry. Consequently a nonzero kernel is the entire radical, and its elements remove the off-block parts of all rank-one lifts.

The nonzero pairing h(m,Bm) puts the reflected isotropic plane adjacent to the original one. A radical element sends its second generator to the chosen opposite isotropic vector, using a free mixed entry and a trace-zero diagonal entry. This produces both opposite rank-one root groups. Their Weyl element, and its conjugate under the Levi factor, give the opposite parabolic radical. The final generation step explicitly retains elementary unitary Gaussian elimination. The conclusion is SU₄ containment, after which the determinant calculation identifies the full projective group exactly.

## Intersection property and the exceptional field

Both projective endpoints are nontrivial, distinct and commuting. The unequal reflection multiplicities rule out anticommutation with the swap, while the displayed vector rules out commutation; therefore the first adjacent product has order greater than two. The second has projective order 2p, also in characteristic three.

I checked the full same-marking intersection argument, including its mixed rotation/reflection alternative. In that alternative the two commuting dihedral factors have cyclic rotation subgroups normal in the whole group. This contradicts almost-simplicity, just as a common nonidentity rotation does. Thus the proof does not replace a theorem asserting existence of some marking with a claim about the present marking.

I independently executed [phase20_unitary_q3_independent_check.py](phase20_unitary_q3_independent_check.py). It starts from the literal matrices over F₃[T]/(T²−T−1), implements its own field arithmetic and row reduction, checks unitary membership and determinants, and builds the orbit of 112 isotropic planes. SymPy's Schreier–Sims calculation gives image order 6,531,840. The classical unitary order and containment give the projective order sandwich; no faithfulness assumption is needed. The seven proper marked subgroups are enumerated directly. All 49 proper/proper meets and the 15 tautological meets involving the full group satisfy IP, giving all 64 marked meets. The type is {8,6}.

This check imports no GAP, ATLAS data, author code or group-recognition oracle. Its large order computation retains SymPy's permutation-group implementation, and the order sandwich retains the classical unitary order formula. The executed report is [phase20_unitary_q3_independent_check.json](phase20_unitary_q3_independent_check.json). I inspected the author's symbolic and six-field GAP checker, but do not claim a fresh execution of either in this review. Larger finite samples are corroboration only; the written proof supplies the uniform statement. There is no new Lean certificate in this package.
