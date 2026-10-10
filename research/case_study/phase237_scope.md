# Matrix centralizers: precise formal scope

This packet adds six Lean declarations about actual two-by-two matrices
over an arbitrary field. It strengthens the formal coverage of the common
projective-line proof, whose earlier phase230 certificate verified only
the abstract normalizer obstruction.

For matrices A and B, `projectivelyCommutes A B` means that AB is a
nonzero scalar multiple of BA. Invertibility is required separately by
the determinant hypotheses. The two main conclusions are:

1. If M is invertible and commutes projectively with diag(l,1) and
   [[0,d],[1,0]], where l and d are nonzero and l²≠1, then M is a
   nonzero scalar multiple of I or diag(−1,1).
2. If the field has characteristic different from two and M is invertible
   and commutes projectively with [[1,1],[0,1]] and [[−1,d],[0,1]],
   then M is a nonzero scalar multiple of I.

Two entrywise lemmas prove the necessary forms of M. Two further lemmas
identify diag(l,1)−(l+1)I/2 with (1−l)diag(−1,1)/2 and show its determinant
is nonzero when l≠1 in characteristic different from two.

These are the actual normal-form matrix calculations used in phase230's
written centralizer proof. They do not assume the desired centralizer
description, subgroup membership, or normality as hypotheses. However,
conjugacy to these normal forms over an algebraic closure, invariance
under basis change, the passage to PGL, and descent to the original field
remain written application arguments. No complete formal proof of the
centralizer descent lemma or either classification is claimed.

The compiler reports only propext, Classical.choice and Quot.sound.
The runner requires Lean's pinned mathlib revision and compiles two
deliberately weakened variants, both of which must fail. The mathematical
reasons for failure are explicit: when l=−1, an off-diagonal reflection
can commute projectively with both matrices; in characteristic two the
nontrivial translation commutes with itself and with the identity
reflection (d=0). Thus those broadened conclusions would be false.
The source and cached dependency objects remain the formal trust boundary.

The calculations are elementary matrix algebra already present in the
written proof; this packet claims additional formal verification, not a
new classification or historical priority. The source classifications
remain attributed to Leemans and Schulte.

Run with a new output directory:

```sh
python3 -B -O phase237_check.py --out NEW --lean LEAN --packages PACKAGES
```
