# Uniform counting of independent commuting involutions

This is a forward consequence of the torsor-quotient normal form. It treats
every rank r at once, rather than only the pair case of the 2013 paper.
The ingredients are classical finite-set decomposition, Burnside averaging
and Möbius inversion. No publication-priority claim is made for this formula.

Let V=F2^r with its distinguished basis, and let D=S_r act by permuting that
basis. We count sets of r commuting involutions that are **independent**:
the group they generate has order 2^r. Equivalence means conjugation by S_N
and permutation of the r marked generators. For the alternating version all
generators must be even, while equivalence still uses S_N. The exceptional
additional automorphisms in degree six are not part of this equivalence.

For a subspace J of dimension d, put

    mu(J)=(-1)^d 2^(d(d-1)/2).

This is the Möbius function from zero in the subspace lattice: its sum over
J<=L is one for L=0 and zero otherwise. It also may be defined recursively
by that identity; the displayed formula follows from the Gaussian-binomial
recurrence.

For delta in D, let O run through its orbits on the subspaces K<=V, and set

    k_O = intersection_(K in O) K,
    w_O = sum_(K in O) |V:K|,
    e_O = sum_(K in O, codim K=1) ell_K in V^*,

where ell_K has kernel K. Then the ordinary generating functions in the
permutation degree N are exactly

    C_r(u) = (1/r!) sum_(delta in D) sum_(J<=V) mu(J)
                       product_(O: J<=k_O) (1-u^(w_O))^(-1),

    C_r^even(u) = (1/(r! 2^r)) sum_(delta in D) sum_(J<=V) mu(J)
                   sum_(v in V)
                   product_(O: J<=k_O)
                     (1-(-1)^(e_O(v)) u^(w_O))^(-1).

**Proof.** Every finite V-set is uniquely a multiset of the transitive sets
V/K. A multiplicity vector is fixed by delta exactly when it is constant
on each orbit O. If that common multiplicity is m, its contribution to size
is m w_O and to sign is m e_O. Requiring the action kernel to contain J
allows exactly those orbits with J<=k_O. Their independent multiplicities
give the displayed geometric-series products.

For any fixed multiplicity vector with kernel L, summing mu(J) over J<=L
is exactly the indicator that L=0. This proves that Möbius inversion selects
faithful actions. Averaging over delta is Burnside's lemma, which forgets
the order of the independent marked generators. Finally,

    2^(-r) sum_(v in V) (-1)^(ell(v))

is one for ell=0 and zero otherwise. Applying it to the total sign character
imposes that every generator is even. This proves both formulas. ∎

Every rank therefore has a rational generating function obtained from a
finite list of subspaces and coordinate permutations. This is a finite
linear-algebra computation in dimension r; it never enumerates S_N.
The change in computational size is substantive when N grows.

The [standard-library implementation](elementary_action_counts.py) computes
ranks two through four through degree 24. It independently compares its
Burnside–Möbius calculation with direct multiplicity-orbit enumeration for
rank two through degree 16 and rank three through degree 12. It also
reproduces the two rank-two rational functions in
[commuting_pairs_compression.md](commuting_pairs_compression.md).
The [saved exact results](elementary_action_counts.json) pass all checks.

Some resulting counts, under precisely the equivalence above:

| Degree N | Independent triples in S_N | Independent even triples | Independent quadruples in S_N | Independent even quadruples |
|---|---:|---:|---:|---:|
| 6 | 14 | 0 | 0 | 0 |
| 8 | 80 | 17 | 160 | 19 |
| 10 | 294 | 34 | 1,619 | 68 |
| 12 | 888 | 165 | 10,602 | 1,153 |
| 16 | 5,677 | 951 | 256,421 | 23,679 |
| 24 | 111,359 | 16,296 | 55,985,711 | 4,170,680 |

The two independent algorithms check the small-degree implementation, while
the proof establishes the all-degree formula. The rank-four values have the
generic formula check but have not been independently enumerated as actual
permutation tuples. Counts of arbitrary distinct dependent involutions, or
of elementary abelian subgroups with all basis choices forgotten, are
different enumeration problems and are not silently identified with these.
