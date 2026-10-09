# Intertwiner separation: formal scope

`IntertwinerSeparation.lean` proves two statements in an arbitrary unital ring:

1. If `a*c=c*x` and `b*c=c*y`, then
   `(a*b-b*a)*c=c*(x*y-y*x)`.
2. If additionally `a*b=b*a` and the right additive commutator has a
   right inverse, then `c=0`.

Both theorems compile with no axioms reported by Lean. The recorded report
uses Lean 4.32.2 and the same pinned mathlib revision as the other modules.

In the written four-dimensional argument, the ring is the ring of
two-by-two matrices. The matrix `c` is a proposed off-diagonal block
intertwining the two endpoint representations. Projective commutator signs
are absorbed into `x` and `y`. The explicit normal forms supply a commuting
pair on one summand and an invertible additive commutator on the other.
The formal theorem then forces that off-diagonal block to vanish.

The module does not classify endpoint representations, prove that all
normal forms were covered, calculate their determinants, or formalize the
resulting maximum-rank theorem. Those remain written mathematics and exact
symbolic checks, with separately recorded internal reviews.
