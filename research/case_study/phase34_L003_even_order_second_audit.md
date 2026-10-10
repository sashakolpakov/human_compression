# Independent written and code review of the exact even-family orders

Date: 2026-10-10. Reviewer: recent_conjectures, an internal collaborating agent.

**PASS.** I read the entire frozen theorem and checker. For the stated right-action convention, the Schreier element s(q)r_j s(qr_j) inverse has translation vector v-w: the inverse permutation cancels the common forward permutation, so no extra coordinate permutation is missing. The product of these elements along a closed marked word telescopes to that word. Since all marks are involutions, the 5184 listed vectors therefore generate the complete integer translation kernel.

The six selected vectors are actual Schreier generators. The checker verifies their determinant-one coordinate minor and, for every Schreier vector, verifies the resulting integer expansion on every one of the1296 coordinates. Thus this is an integral basis and a split coordinate projection onto Z^6, not merely a rational rank computation. Literal re-evaluation of the six selected words corroborates the subtraction orientation. Exact elimination correctly records pivot factors and row-swap signs.

The integral inverse of the selected coordinate matrix gives L intersect mZ^1296 = mL for every positive m. Hence the actual coordinate-modulus quotient has kernel C_m^6 over its order1296 permutation image, proving |G_m|=1296m^6. The source universal group need not be this image, and no splitting of the extension is needed or claimed.

This is a complete written/code review without a fresh execution by this reviewer. The parent independently reran the checker. I authored the retained even-family construction, so this review is independent of the new lattice/order derivation but not of every retained input. It is not external peer review or a novelty determination.
