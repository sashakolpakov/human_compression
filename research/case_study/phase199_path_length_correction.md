# Chambers and the path-length wording in L092

This is an additional source qualification discovered during independent phase199 review of frozen phase186. It does not modify that author package. The primary is L092, printed p.566, Lemma3(4), Corollary1 and Theorem1, visually checked in the original PDF. The source says “paths of length four.” Its incidence construction instead gives configurations with **four vertices and three edges**:

\[
 P-M-x-L,\qquad P\ne x,\quad M\ne L.
\]

Here P,x are points and M,L are lines of the original partial linear space. The corresponding chamber is (P,L,(x,M)). Partial linearity implies P is not on L. Conversely every chamber yields precisely this path. Thus the correct unconditional equivalence is between chamber transitivity and transitivity on these oriented three-edge paths starting at a point. The author manuscript B2 already specifies this configuration correctly. The source's conventional four-edge reading is a stronger, false statement; no assertion about the author's intended convention is needed.

Take the affine plane AG(2,3) and G=ASL(2,3). It is thick and connected, and G is flag-transitive on it. Construction3 gives a firm residually connected geometry, as proved directly by B.AffinePlane. That proof also establishes that G acts regularly on its chambers. Its group order and chamber count are

\[
 |G|=3^2|SL(2,3)|=216.
\]

There are 9·4·2·3=216 oriented three-edge paths beginning at a point. Each extends to exactly two four-edge paths, by choosing a point on the final line other than the middle point. Both choices are distinct from the first point because the first point does not lie on the final line. Hence there are 432 genuine four-edge paths. A group of order216 cannot be transitive on them. This supplies a counterexample to the conventional four-edge conclusion under all of Theorem1's relevant hypotheses.

The source's own divisibility formula in Corollary1, v t(s−1)(t−1), equals the three-edge count. It supports the precise chamber-equivalent formulation, but does not prove historical intent about terminology.

The independently written `phase199_path_length.py` constructs all9 points,12 lines,36 flag objects and all216 chambers from the literal source incidence. It verifies every flag extends, panel sizes2/3, connectedness of the whole geometry and all57 singleton residues, and the rank-two intersection property. It enumerates the216 actual affine determinant-one permutations, checks original flag transitivity and regularity on chambers, and counts432 four-edge paths with an orbit of size216. The check imports no phase186 implementation.

This is a correction of wording when interpreted by the usual edge-count convention, not a new open-conjecture solution or a new general geometric theorem. The uniform proof of B.Necessity and the source's linear/dual/(4,3,4) classification are unaffected. The new finite counterexample is checked in Python and written mathematics, not Lean.
