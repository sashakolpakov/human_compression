# Scope of FibonacciModulus.lean

The literal two-by-two matrix N=[[0,1],[1,1]] satisfies its Fibonacci
power formula over every semiring. For every s>=3, its s-th power over
ZMod(F_s) is the scalar F_(s-1), and no positive smaller power is scalar.
The proof handles the equality F1=F2 explicitly and works for composite
Fibonacci moduli. It uses induction and divisibility, not finite samples.

A fresh pinned Lean4.32.2 compilation passed. The principal printed
axioms are propext, Classical.choice and Quot.sound; no native-evaluation
axiom or unproved placeholder is used. A second agent read every source
proof and confirmed the exact scope; no second-agent compilation is claimed.

The module does not prove scalar invertibility, tensor cancellation,
exact order in GL/PGL, eight-dimensional relations, local subgroup orders,
intersection property, incidence or hypertope existence. Those are separate
written adapters and finite certificates, with global geometry still pending
in the tensor package. The source need not be trusted as an all-purpose
certificate for claims beyond its explicit theorem statements.
