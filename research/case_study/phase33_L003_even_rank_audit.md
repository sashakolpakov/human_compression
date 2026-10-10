# Independent review of the varying even-parameter construction

Date: 2026-10-10. Verdict: **PASS for the finite regular hypertope construction at every even source parameter.**

I read the complete written construction and literal standard-library checker,
then freshly executed the checker with a separate output path. I also reread
the primary source's equation (2.3), section-eight presentation, Table 8 and
Problem 9.2 in the saved primary PDF text. The [primary source](https://ria.ua.pt/bitstream/10773/23862/1/2018DFW.pdf)
specifies the ordered parameters used in the note. This review makes no new
claim about later literature or priority.

The doubled right-action convention is consistent: each new mark is an
involution, and the nine integral relations are checked on both copies. The
parameter word has nonidentity underlying permutation of order two, while
its square is a pure translation with a coordinate equal to minus one.
Consequently its order modulo any positive integer \(m\) is exactly \(2m\).
The two kernel translations belong to the growing maximal parabolic, commute,
and have the displayed determinant-minus-one coordinate minor. Any linear
relation modulo \(m\) therefore has both coefficients zero modulo \(m\).
This proves a subgroup of order \(m^2\) in the projection kernel, including
composite or even moduli; at \(m=1\) the statement is the trivial subgroup.

The underlying variable parabolic has order 48. The kernel lower bound hence
gives order at least \(48m^2\), without presuming a full description of the
ambient translation lattice. Its local rotations \((y^{-1}z,y^{-1})\) satisfy
the toroidal presentation and parameter relation with \(s=2m\). The retained
triangular-lattice toroidal order formula gives the matching upper bound.
Thus the marked local quotient is exactly the required toroidal group. The
three fixed parabolics are independently closed over the integers; comparing
all equal underlying permutations rules out hidden translations and proves
injectivity into every coordinate modulus. Their attained orders and the
three explicit local adapters identify the other ordered residues.

I checked the base closure, all subset intersections, and the meaning of each
typed-Helly orbit count in the code. The representatives enumerate the
appropriate parabolic cosets, membership in subgroup products is exactly
incidence with the remaining base objects, and the counted stabilizer orbit
has the stated index. Equality gives flag transitivity by induction. Thus
subgroup IP is not being substituted for the geometric flag condition.

The one-exceptional quotient lemma applies precisely: the three fixed maximal
parabolics inject into the base, while the growing one need not. The separately
kernel-checked generic transport result supplies both actual IP and typed
Helly. Their usual marked-coset consequences are also justified in the written
proof: every flag completes, panel stabilizers have order two, and generators
connect the chamber graph of every residue. This gives a thin residually
connected geometry whose full type-preserving automorphism group is the
constructed finite group. Distinct \(m\) have distinct growing-residue orders.

The fresh checker output is byte-identical to the author's report. It verifies
11,664 integral relator/state equalities; the exact finite integer parabolic
orders 36, 48 and 108; the determinant-minus-one local minor; the base group
of order 1,296; all 256 marked meets; and all 16 required typed-Helly counts.
This is a fresh execution of the author's implementation, not a separately
implemented census. The uniform conclusion depends on the written order
sandwich and quotient theorem, not extrapolation from sampled moduli.

The conclusion concerns finite regular examples for every even \(s\ge2\)
with the exact ordered residues. It does not identify their full group orders,
the universal groups, or the odd-parameter family. In particular it is
compatible with the previously proved infinite universal group at \(s=6\).
Those distinctions, the retained toroidal lattice input, and the partial scope
of the Lean module are all explicit. No correction to the reviewed argument
was requested. The companion JSON binds the final authored bytes and fresh
run separately.
