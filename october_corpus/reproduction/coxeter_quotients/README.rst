An order bound from a universal presentation
==========================================

The supplied quartet satisfies the Coxeter relations of type {5,3,5} and
the additional equation (abc)^5=1. Reversing its generators gives a quotient
of the group in Hartley and Leemans, Theorem 3.2. That group has order
600,415,200. Hence the supplied matrices cannot generate a group isomorphic
to G2(11), whose order is 376,611,192,619,200.

Run with Python's standard library::

    python3 -E -B verify.py --controls
    python3 -E -B verify.py

The checker verifies every matrix equation over F11. It uses the published
finite presentation bound as an attributed theorem input. The identification
of the tuple with original F004, job20, position200 is inherited from the
reviewed source register. Its matrix tuple is fixed by its recorded digest.
The order argument itself needs no identification of the generated subgroup
or embedding into a particular ambient matrix group.

This is an application of an existing theorem. It adds no answer to an open
conjecture, complete manuscript, compression measurement or Lean proof.

Reference: M. I. Hartley and D. Leemans, ``Quotients of a Universal Locally
Projective Polytope of type {5,3,5}'', arXiv:math/0307075v1 (2003),
presentation on printed page3 and Theorem3.2 on printed page5:
https://arxiv.org/pdf/math/0307075v1.
