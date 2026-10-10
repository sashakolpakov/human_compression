# Root review of the integral tensor construction

Date: 2026-10-10. PASS after complete proof/code read and fresh execution.

The literal tensor convention, global sign of x, nine rotational words,
reflection involution and two parameter tensors agree. The checker uses
exact integer matrices and complete finite local closures. A fresh run
reproduces the saved report byte-for-byte; it is not a new implementation.

Conjugation on the three matrix-factor algebras proves the tensor scalar
lemma over every nonzero commutative ring. It also distinguishes the
factor-permutation part. The Fibonacci off-diagonal entry proves that
N has no scalar power before s modulo F_s, and its s-th power is an
invertible scalar. Thus the eight-dimensional parameter word has exact
order s for all s>=3, including composite moduli.

The three fixed local groups inject for every s>=4 by the integer entry
difference bound and separate modulus-three check. The variable local
contains C_s^2 semidirect S3; z is outside it since S is nonsymmetric
modulo F_s>2 whereas every scalar times an N-power is symmetric. This
gives the full torus lower bound12s^2, matching the retained presentation
upper bound and proving a marked isomorphism. The s3 collapse is explicit.

I also authored and freshly compiled FibonacciModulus.lean: it proves the
power formula over arbitrary semirings and both uniform scalar-power
assertions over ZMod(F_s). Its source was independently read by another
agent. Tensor cancellation, invertibility, exact group order and geometry
are not Lean conclusions. No global IP/Helly or all-parameter hypertope
claim is supplied by this package; bibliographic priority remains unverified.
