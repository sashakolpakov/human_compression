# Root review of exact even-family quotient orders

Date: 2026-10-10. PASS after complete final proof/code review and fresh run.

The breadth-first lifts are actual generator words. The5184 Schreier words
generate the entire translation kernel by telescoping, not merely a sampled
sublattice. Equal underlying permutations justify the voltage subtraction.
Six selected Schreier vectors form a basis: the determinant-one coordinate
minor gives independence and integral coefficient recovery, and every full
1296-coordinate Schreier vector is checked against those coefficients.

The same integral inverse proves L intersect mZ^1296 = mL for every positive
m. Coordinate reduction can kill no nonidentity permutation, so its whole
kernel is exactly mL. This gives the exact extension by C_m^6 and the order
1296m^6. No splitting or faithfulness on the source universal group follows.
Direct basis-word reevaluation and the conjugation matrices agree with the
stated action convention. The fresh report is byte-identical to the author
report; it is a fresh execution, not an independent implementation.

The separate SplitLatticeReduction Lean module formalizes the generic
additive-left-inverse divisibility argument and the literal six-coordinate
inverse. It does not formalize the full Schreier census or the geometry.
The earlier family theorem supplies the exact residues and hypertope
properties; these were not recomputed by this order supplement.
