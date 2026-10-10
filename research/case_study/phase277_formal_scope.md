# Formal and computational verification

The three declarations in `formal/IntervalMinimalCoverLifting.lean` prove
the order argument in Theorem 2 and its consequence that different local
kernels force different global kernels. Larger kernels mean smaller covers.
The extension hypothesis, descent hypothesis and restriction of admissible
kernels are explicit. The file does not formalize Monson–Schulte's finite
construction, the intersection property of a standard parabolic, the
rank-four surface theorem, or the correspondence with polytopes. Those
remain written mathematical inputs. All three declarations compile without
any axioms.

The finite program checks the complete order-64 example in the separate
obstruction note and its order-128 cover. It does not decide the conjecture
for actual polytopes. Its base marking cannot be a polytope monodromy group,
because two subgroups generated on disjoint color sets intersect
nontrivially.

Run `python3 -O phase277_check.py --out /fresh/output/directory` to replay
both parts. Lean 4.32.2 and the recorded mathlib revision are required;
`--lean` and `--packages` allow their locations to be supplied. Optional
`--verify-primary` checks the separately acquired source PDFs. The written
mathematics does not follow merely from a successful replay.
