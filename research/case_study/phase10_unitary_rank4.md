# An explicit rank-four string C-group for PSU₄(5)

10 October 2026. Exact finite certificate, with software dependencies
specified below. This result concerns one field. It gives no uniform
rank-four construction for all odd unitary groups, and its historical
priority has not been established.

**Result.** The four permutations in
[phase10_unitary_rank4_witness.g](phase10_unitary_rank4_witness.g)
generate a string C-group isomorphic to $\operatorname{PSU}_4(5)$, of
Schläfli type $\{4,26,10\}$. Combining this finite existence certificate
with the internally reviewed
[phase-nine upper bound](phase9_linear_unitary.md) gives maximum rank
four for this particular group.

## Exact checks

The standalone [GAP checker](phase10_unitary_rank4_check.g) reads only
the constructed tuple. It verifies that its four entries are
involutions, every distant pair commutes, and adjacent product orders
are 4, 26 and 10. It generates each of the 16 subgroups indexed by
subsets of the four generators, and checks all 256 ordered pairs:
\[
 \langle\rho_i:i\in I\rangle\cap\langle\rho_i:i\in J\rangle
       =\langle\rho_i:i\in I\cap J\rangle.
\]
Thus it verifies the full intersection property directly. It does not
assume a rank-reduction or parabolic-intersection shortcut.

The generated group has degree 756 and order
\[
 14\,742\,000\,000
 =\frac{5^6(5^2-1)(5^3+1)(5^4-1)}{\gcd(4,6)}.
\]
GAP also verifies that the generated permutation group is simple, and
its finite-simple-group identification routine returns series 2A with
parameters $[3,5]$, namely $\operatorname{PSU}_4(5)$.

For reference, the nontrivial proper subgroup orders are:

| Generator indices (numbered 0–3) | Order |
|---|---:|
| 0; 1; 2; 3 individually | 2 |
| 01 | 8 |
| 02; 03; 13 | 4 |
| 12 | 52 |
| 23 | 20 |
| 012 | 15,600 |
| 013 | 16 |
| 023 | 40 |
| 123 | 9,360,000 |

The empty subgroup has order one. These orders are diagnostics; the
checker tests subgroup equality for the intersection property, not
only the corresponding orders.

## Reproduction and trust boundary

With GAP 4.15.1, run from the directory containing the two original
files:

    gap -q phase10_unitary_rank4_check.g

The saved [log](phase10_unitary_rank4_check.log) reports PASS. The group
operations use exact permutations and GAP's subgroup algorithms. Group
identification uses GAP's simplicity test followed by
IsomorphismTypeInfoFiniteSimpleGroup. The latter retains standard
finite-simple-group classification and order-identification knowledge;
it is not a newly proved recognition theorem. We inspected the installed
GAP definitions and documentation for this boundary. The public
[GAP reference manual](https://docs.gap-system.org/doc/ref/chap39.html)
documents the identification function.

This certificate is a computational proof of the finite statement
relative to those software dependencies. It is not a Lean formalization
of all subgroup computations. The inherited rank upper bound is a
separate written theorem with partial formal certificates.

## Discovery and source attribution

The ambient search used the primary
[ATLAS U₄(5) degree-756 representation](https://brauer.maths.qmul.ac.uk/Atlas/clas/U45/),
then selected new involutions inside centralizers of commuting outer
generators. With deterministic random seed 94127, the bounded probe
found this tuple on its 322nd attempted sample. Discovery is not the
proof: the standalone checker rebuilds the generated group and all
subset intersections from the saved tuple without reading the ATLAS
generator files or replaying the random search.

The original ATLAS generators remain private source assets. The
exportable witness is the actual constructed tuple; no article or
downloaded source text is bundled. The metadata records source URLs
and hashes for provenance.

The order-15,600 and order-9,360,000 parabolics suggest useful candidates
for a future uniform construction, but this note assigns no unverified
isomorphism type to them. In particular 15,600 alone does not establish
SL₂(25), and 9,360,000 is twice the order of PSp₄(5).

Targeted searches for PSU₄(5), U₄(5) and rank-four regular polytopes did
not locate a prior primary-source example. This bounded search does
not prove novelty. The general odd-PSU₄ rank-four existence problem
remains undecided by this package.
