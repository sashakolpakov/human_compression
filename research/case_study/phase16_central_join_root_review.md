# Root review of the central join and counting theorem

10 October 2026. PASS. The root contributed to the derivation and reviewed
the complete final note. The separately bound survey-agent audit is the
independent internal review; this note does not count as an additional
independent source of the construction.

The base group need not be abelian: each cocycle coordinate factors
through two group characters into F2. Expanding those characters gives
the cocycle identity without commuting base elements. Edges outside the
core produce individual central commutators, so the marked generators
generate the whole construction. The claimed parabolic formula is an
equality of coordinate sets, not an incorrect direct-product assertion.
It both generates every allowed coordinate and excludes every absent one.
Taking intersections then proves the full marked IP.

The derived subgroup is H' times the central edge space. Its commutators
with outside generators vanish because H' has zero vertex characters.
Consequently the third lower central subgroup is exactly the embedded
gamma3(H), with its original support. This supplies automatic attachment
for every core satisfying the stated finite conditions. The earlier
reconstruction theorem gives uniqueness, so the classification is a
bijection of ordered marked groups and canonical cores with positions.
No acceptance test for global IP or order remains necessary for these cores.

The counting patterns correctly distinguish gaps one and two, where
the neighborhoods overlap or touch, from gaps at least three, where
they are separate. End gaps need only distinguish zero from positive.
Additional gap length changes positions but not the ordered core or
its marking relations. Canonical support makes different patterns,
length vectors and core classes disjoint in the count.

Each pattern contributes m z^b/(1-z)^r with a finite, effectively
computable core multiplicity m. The bounds b<=6k-1 and r<=k+1 give
eventual polynomiality, and the r=0 terms disappear by d>=6k-1.
The already proved binomial lower bound forces degree exactly k.
This is a sufficient stabilization bound, not a claim of the first
stable rank. No coefficient computation for the full core library
or unmarked-group classification is asserted.

The frozen necessary-core proof and its diagnostics remain unchanged.
The join is a stronger, separate result. Its universal justification is
the written argument and independent audit; finite diagnostics have their
own explicit scopes. Current publication priority is unverified, and
no full Lean formalization or literal numerical compression ratio follows.
