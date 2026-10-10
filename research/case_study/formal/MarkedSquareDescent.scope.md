# Marked square descent: formal scope

10 October 2026. [MarkedSquareDescent.lean](MarkedSquareDescent.lean)
compiles with the pinned Lean 4.32.2 and mathlib setup. Its
[saved report](MarkedSquareDescent.check.json) binds the source bytes,
compiler version, successful exit and printed theorem axioms.

The module imports the earlier [binary Frattini certificate](BinaryFrattiniActions.lean).
Vectors are actual triples of Boolean coordinates; the matrix functions
are the specified binary-linear maps. Kernel-checked finite decisions
prove both directions of the unique commuting marked-action classification.
They do not assume that arbitrary nonlinear functions are linear.

The abstract transport theorem then proves that an equivariant map
preserving the three marked coordinates takes a common fixed marked
coordinate to a common fixed marked coordinate. This theorem itself has
no axioms. Combining it with the earlier complete binary Frattini lemma
gives `no_frattini_to_unfixed_marked_map`: such a marked equivariant
map cannot connect a compatible Frattini action to an action with no
common fixed marked coordinate.

The finite decisions use `decide +kernel`, not a trusted native decision
axiom. The printed dependencies are only Lean's standard propositional
extensionality, choice and quotient soundness; there is no `sorryAx`.

The application to the [uniform cyclic-TPP proof](../phase14_cyclic_tpp.md)
requires separate written arguments. This module does **not** formalize:

- The minimum-counterexample reductions for cyclic TPP triples.
- Powerful-group generation, factorization or the top-power map.
- The reduction of an arbitrary finite 2-group image to the commuting
  involutions used in the finite classification.
- The quotient groups and well-definedness of their squaring maps.
- The hypertope, coset Helly and derived-group interpretation.

Thus the certificate checks a complete finite-linear classification and
the final abstract obstruction. It is a component certificate, not a
full Lean formalization of the nilpotent-group theorem or the hypertope
conjecture. Publication priority and external review are separate.
