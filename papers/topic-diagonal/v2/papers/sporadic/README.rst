Sporadic finite certificates for N006
====================================

This private packet verifies the nine cases explicitly treated in the proof of Theorem 5.3 in
Piedade–Tranchida, arXiv:2605.04646v2. It is the finite application component,
not a replacement for the paper's full twisting and wreath theory.

Replay
------

From a copied packet, run::

  python3 -B -O check.py --out /fresh/absolute/output --atlas-root /directory/of/atlas/files

The two required external files are ONd2G1-p245520B0.g1 and .g2. Their exact
URLs, sizes and SHA256 hashes are in scope.json. They are literal permutation
data; the driver rejects mismatched bytes before GAP reads either file.
The original external files are not exported. The new compact O'Nan witness
contains only explicit word instructions in those two standard generators.
The other eight new/literal-source witnesses are fully supplied.

Use --part eight, --part on, or --part outer-orders for an explicitly partial
run. The JSON report distinguishes the nine-case existence check from the
separate source-route obstruction. A zero GAP exit code is insufficient:
the driver also rejects GAP errors and requires the exact completion marker.
Negative controls include a genuine rank-three C-group that fails flag
transitivity, so intersection tests alone cannot satisfy the checker.

Mathematical and data boundaries
-------------------------------

All four complete finite programs and all nine witness files are proof inputs.
The program on_outer_orders.g concerns the source's O'Nan proof route rather
than the positive existence certificate. Search programs and unsuccessful
search traces are construction history, not replay premises. The Atlas
max-subgroup SLP whose computed output did not match the anticipated label is
unused. No conclusion here relies on that label.

The named sporadic groups, their outer-automorphism orders and the Atlas data
remain retained inputs. Exact group order, faithful socle action, generation,
all subgroup-intersection equalities, and all rank-three flag-product
conditions are verified in the actual permutation models. Naming a group
from its order alone is not accepted. No Lean certificate is claimed for
these GAP calculations. External catalogue/classification proof costs are
not measured or treated as zero.

The source's two possible exceptions Fi22 and Fi24' remain exceptions. The
O'Nan outer-duality route is impossible, because it would give an outer
order-four element. That correction is separate from the theorem's positive
existence conclusion, which is addressed by the direct saved marking. No
new conjecture or priority claim is made.

Literal theorem boundary
------------------------

The literal universal statement also includes HN, whose outer automorphism
group has order two. The source proof omits that case. This nine-case packet
does not discharge HN and must not be called the complete literal theorem.
The original exceptions Fi22 and Fi24' are a different boundary. The exact
external-data bytes and versions, including the 3,720,665-byte required ON
representation pair, are in retained_inputs.json; the 1,948-byte witness
instructions alone are not the full data/software cost.
