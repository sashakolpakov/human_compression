# Four infinite families of PGL maniplexes

The conjecture at the end of Section 5 of Leemans and Toledo's
*Maniplexes with automorphism group PSL(2,q)* asks for four infinite
families of regular rank-four maniplexes. In every family one end group
is PGL₂(q); the other is S₄, A₅, PSL₂(q), or PGL₂(q).

The [complete proof](research/case_study/phase257_four_families.md)
([six-page PDF](research/case_study/phase257_four_families.pdf)) constructs
all four, for every prime in the following progressions:

| Other end group | Primes p |
|---|---|
| S₄ | p > 5 and p ≡ 3 or 5 modulo 8 |
| A₅ | p ≡ 9 or 11 modulo 20 |
| PSL₂(p) | p ≡ 5 modulo 12 |
| PGL₂(p) | p > 3 and p ≡ 3 modulo 4 |

Dirichlet's theorem supplies infinitely many primes in each row, and
increasing group orders distinguish the resulting maniplexes. This is
one complete affirmative answer to the question in the May 15, 2023
author edition. It does not classify every PGL maniplex or claim an
example for every prime power.

## The common argument and its attribution

The determinant modulo squares distinguishes PSL₂(p) from PGL₂(p).
For two families, one constant quadruple of integral matrices generates
both end groups: each contains the full lower unipotent group and a
projectivity moving its fixed point, hence contains PSL₂(p). The
four determinants then decide which ends are PGL₂(p).

For the S₄ and A₅ families, start with a standard local map and adjoin
the unique nonidentity projectivity centralizing its first dihedral
pair. The [common centralizer theorem](PROJECTIVE_LINE_POLYTOPES.md)
supplies this element. The proof shows that it generates the full
ambient group with the local map, then separately proves that the
opposite end is also full. The exact maximal-subgroup classification
and the small Coxeter presentations are explicit retained inputs.

The original paper already uses this centralizer-extension strategy,
and the constant matrices are an explicit normalization of its PSL
construction. Those ideas retain their attribution. The additions are
the determinant conditions and the complete arguments for the four
PGL configurations. The [source ledger](research/case_study/phase257_source_ledger.json)
and [contract](research/case_study/phase257_contract.json) identify the
question, borrowed inputs, proof sections and excluded claims.

## Verification and publication scope

The [independent agent review](research/case_study/phase261_review.md) accepts
the complete written proof. External peer review is not claimed. The author checked 16 actual marked groups;
a separate implementation checked 17, together with all 48 relevant
S₄ cases, both exact finite Coxeter orders, and excluded-parameter
examples. A fresh public replay reproduces these checks. The examples
test the constructions; they do not establish the infinite quantifiers.

[Eleven Lean declarations](research/case_study/formal/FourProjectiveMarks.lean)
verify the actual matrix relations, determinants, nonscalarity,
pairwise nonproportionality, and the unipotent power, period and
exhaustion statements. They use standard axioms only. The
[formal scope](research/case_study/phase257_formal_scope.md) lists the
remaining written arguments, including subgroup classification and
Dirichlet. This is not a complete Lean proof of the conjecture.

The [bounded priority search](research/case_study/phase261_priority_search.md)
found no later solution through its twelve recorded queries. It does
not establish first publication or exhaustive knowledge of the
literature. The journal edition was not collated against the bound
author edition.

This adds one entry to the [question catalogue](CONJECTURE_RESULTS.md),
separate from recovering the paper's already proved principal results.
It adds no principal-source credit and no source-length compression
factor. The [publication record](provenance/phase128_review.md) binds
the preserved proof packets and fresh public checks.
