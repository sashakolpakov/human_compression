# Independent review of the small quotient and powerful eighth powers

10 October 2026. Root independently read the complete
[power-layer argument](phase12_power_layers.md) and both focused checkers.
The written proof passes internal review with its recorded dependencies.
The accompanying JSON binds the final files and fresh executions. This
is a necessary-condition theorem for a minimum counterexample, not a
proof of the unrestricted cyclic TPP inequality.

The weak-embedding induction is valid without assuming that iterated
square subgroups equal fourth-power subgroups. N⁴ is normal, and both
hypotheses descend to its quotient. With N⁴=1, a central order-two
subgroup inside N exists by the normal-subgroup center property. The
smaller quotient makes N′ central; exponent four then makes N² central
elementary abelian. Triviality of the G-action on N/N² implies triviality
on N², and hence each square of G centralizes N. This proves the stated
commutator containment and powerfulness.

The dimension-at-most-two action argument allows dependent marked
vectors, including zero ones. Nontrivial commuting involutions in
GL₂(F₂) coincide, and the square equations would put all three marked
vectors on the same line. This contradicts spanning. Applying weak
embedding with N=Φ(P)=P² then excludes both low dimension and the
trivial action in dimension three.

With a coordinate support line fixed, the complete square identities
determine the two action matrices and d modulo that line. They give
the displayed order-32 presentation. The collection upper bound is
proved in the text, separately from the NQ class-three quotient check:
the presentation commutator relations make a² central and permit at
most 32 normal forms. Its surjection onto the known order-32 quotient
therefore proves equality. A finite nilpotent quotient alone would
not have proved that upper bound.

The first equality triple squares into Φ²(P) because the preceding
Frattini rank is exactly three. Minimality proves generation, with no
global product-map injectivity assumption. The retained small-factor
theorem ensures the three fourth-power cyclic factors are nontrivial;
its marked-isobicyclic classification input remains charged. If this
next Frattini rank were at most two, the small linear action and weak
embedding would make it powerful. Actual powerful factorization plus
equality would then force rank three, a contradiction.

Squaring again gives T=Φ³(P)=P⁸, with a cyclic equality triple which
may now have trivial factors. An invariant flag bounds the exponent
of every 2-subgroup of GL₃(F₂) by four. Thus P⁴ centralizes T/Φ(T),
and weak embedding with ambient P⁴ makes T powerful. The indices
multiply to 4·8·8=256. Powerful power-subgroup generation identifies
every deeper Frattini iterate with the corresponding ordinary power
subgroup. Ordered coordinates there are genuinely bijective: initial
surjectivity comes from the retained factorization theorem, equality
gives injectivity, and restriction plus factorization handles powers.

The explicit two-matrix example correctly refutes the suggested
weaker fixed-coordinate shortcut. Its common fixed line is the sum
of all three coordinates, so the existence of a fixed vector alone
does not supply a central element in a marked cyclic factor. This
failure is documented rather than silently used to close the problem.

Root freshly ran both finite checkers. Their outputs match the frozen
reports byte for byte. The Python diagnostic checks all stated low
dimensional square identities and the failed-shortcut example. GAP/NQ
checks the concrete order-32 quotient without a group catalogue.
These complement the uniform written proof; they do not exhaust
counterexamples, remove the retained small-factor classification,
or constitute an additional Lean module. No priority or infinity
marker is assigned.
