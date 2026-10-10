# A last lower-central quotient can lose the intersection property

10 October 2026. This is one explicit finite counterexample to a proposed
induction shortcut. It is not a counterexample to the common-quotient
existence claim.

There is a rank-three string C-group H of order 256, class four and type
{8,8} for which H/γ₄(H) fails the intersection property. Its lower-central
orders are

    256, 32, 8, 2, 1.

In contrast, H/γ₃(H) has order 32 and is the marked path-cocycle group.
Thus passing through successive lower-central quotients need not preserve
the class of string C-groups, even when the eventual class-two quotient
has the required marking.

## Explicit construction and the failed intersection

Let F be free on a,b,c. Write

    x=[a,b],  y=[b,c],  t=[x,c],

with [u,v]=u⁻¹v⁻¹uv. Impose

    a²=b²=c²=1,  [a,c]=1,
    x⁴=y⁴=t²=1,  x² y² [x,y]=1,

and take the class-at-most-four nilpotent quotient. The
[GAP/NQ construction](phase15_quotient_ip_check.g) produces H and exports
three explicit permutations of degree 256 in
[the witness file](phase15_quotient_ip_witness.json). The permutation group
itself is sufficient for every counterexample claim below; completeness
of the nilpotent-quotient construction is not needed once those
permutations are supplied.

Put A=<a,b>, B=<b,c>, z₁=x² and z₂=y². Exact computations give

    |A|=|B|=16,       A∩B=<b>,
    z₁≠z₂,           |z₁|=|z₂|=2,
    N=γ₄(H)=<z₁z₂>,  |N|=2,
    N∩A=N∩B=1.

The original marking satisfies all 64 subset-pair intersection checks.
For the quotient map π:H→H/N, however,

    π(A)∩π(B)=<π(b),π(z₁)>,   of order 4,
    π(z₁)=π(z₂)≠1.

The required common marked subgroup is only <π(b)>, of order 2.
This is the exact extra intersection; the ordered subset-mask pairs
(3,6) and (6,3) are the only failures among the 64 quotient comparisons.

The obstruction is a diagonal central subgroup: N lies in AB and
identifies two distinct parabolic involutions, while meeting each
parabolic trivially. Merely knowing that N is the last lower-central
term and is central elementary abelian does not rule this out.

## Independent exact verification

The original standard-library-only
[Python verifier](phase15_quotient_ip_verify.py) reads the three
permutations, closes the generated group, constructs its full
multiplication table, and computes all lower-central subgroups from
actual commutators. It checks the eight displayed relations, every
original subset intersection, the central diagonal and its parabolic
intersections, the exact enlarged quotient intersection, and all 64
intersections in the class-two quotient. It uses neither GAP/NQ nor a
group catalogue. Its [saved report](phase15_quotient_ip_verify.json)
passes.

Reproduce the independent verification with Python 3:

```sh
python3 phase15_quotient_ip_verify.py
```

The optional generator can be rerun with GAP and NQ:

```sh
gap -q phase15_quotient_ip_check.g
```

The [certificate](phase15_quotient_ip_certificate.json) binds the exact
construction, generated permutation data, independent verifier and
captured outputs. This is one witnessed boundary result, not a census,
an assertion about higher nilpotency classes, or a priority claim.
