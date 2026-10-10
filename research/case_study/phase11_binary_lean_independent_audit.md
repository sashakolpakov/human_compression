# Independent statement audit: BinaryFrattiniActions.lean

10 October 2026. **PASS** for the actual finite theorem statements and their
use in the written abelian-Frattini argument. I read the entire Lean source
and its saved successful check report, and compared the cases with both
independent Python enumerations. This audit did not independently invoke
Lean; the successful kernel execution is the separately hash-bound report.

The vector type is exactly three Booleans. Addition is coordinatewise xor,
and `lin` specifies the images of the three coordinate vectors. Its extra
addition-preservation theorem confirms this concrete linear representation.
No abstract finite-group or Frattini objects occur in this source.

`compatible` fixes the first column of S and the second column of T at the
corresponding coordinate vectors. It requires both maps to square to the
identity and to commute. Its existential d,f equations are exactly

    Tx+x=Sd+d,  Sy+y=Td+d,
    z=x+y+Td+f+STf.

Thus it includes the additional square compatibility missing from the
tempting, false weaker action lemma. The scope is neither weakened nor
made vacuous by an impossible hypothesis. In the column encoding used by
the author checker, witnesses for the four displayed pairs are:

| Columns of S | Columns of T | d | f |
|---|---|---:|---:|
| (1,2,4) | (1,2,4) | 7 | 0 |
| (1,2,6) | (3,2,6) | 5 | 1 |
| (1,3,5) | (1,2,5) | 6 | 0 |
| (1,6,4) | (5,2,4) | 3 | 0 |

Here integers encode the three Boolean coordinates with weights 1,2,4.
The witnesses were read from the freshly rerun exact checker and agree
with the independently implemented row-matrix enumeration.

`binary_action_classification` proves that a compatible pair belongs to
the four explicit cases. `classified_has_coordinate_support` proves that
each listed case has a common fixed coordinate w, and every vector changes
under either map only by zero or w. Their combination is the coordinate
support corollary used by the maximal-exponent lift. It correctly includes
the identity case, whose image is zero rather than a nonzero line.

The final source also includes `classified_is_compatible` and combines
both implications in `binary_action_classification_iff`. Thus the formal
statement is an exact four-case classification, including realization of
every listed case. I read these additions after the initial forward-only
version; the accompanying binding is to the final six-theorem source and
its successful check report. The finite-checker witnesses above provide
an additional independent nonvacuity check.

The source uses `decide +kernel`, with no `native_decide` or `sorry`.
Its saved report has exit code zero and records only `propext`,
`Classical.choice` and `Quot.sound` for all six theorems. I verified that
the report's source hash equals the actual source hash.

The certificate does not formalize minimum-counterexample induction,
the direct-product identification of the Frattini subgroup, conjugation
identities in arbitrary groups, unequal-exponent lifting, or the odd-prime
and nilpotent extensions. Those are separately reviewed written arguments.
No complete formal group-theoretic theorem, external review, or priority
determination is asserted by this audit.
