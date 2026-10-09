# Exhaustive high-rank search for PSL(4,3) and PSL(4,5)

Status: exact computational verification in GAP 4.15.1. These results establish the two finite cases, not the conjectural uniform upper bound for all odd q.

## Results

The groups PSL(4,3) and PSL(4,5) have no string C-group representations of rank at least five. Combined with the known rank-four construction, their maximum rank is four.

| q | Ordered commuting-triple representatives | Fourth-generator orbits | Rank-five candidates | IP-valid rank-five prefixes | Rank-six extensions tested | IP-valid rank-six prefixes |
|---|-----------------------------------------|-------------------------|----------------------|-----------------------------|----------------------------|---------------------------|
| 3 | 112 | 2,186 | 5,224 | 200 | 8 | 0 |
| 5 | 14 | 1,354 | 5,892 | 184 | 0 | 0 |

Every rank-five prefix generates a proper subgroup of PSL(4,q), including the prefixes that fail the intersection property. The recursive search terminates after the displayed rank-six tests. It uses no rank cutoff and no sampling.

## Why the enumeration is complete

Let (rho0,...,rho_(r-1)) be a string C-group generating the target simple group, with r>=5. Distinct adjacent generators cannot commute: a commuting adjacent pair would divide the string into two mutually commuting nontrivial factors, giving a direct-product decomposition incompatible with simplicity. All nonadjacent pairs commute by the string condition.

1. Choose rho2 from each conjugacy class of involutions of G.
2. Choose rho0 from each involution class of C_G(rho2), excluding rho2.
3. Choose rho4 from each involution class of C_G(rho0,rho2), excluding <rho0,rho2>. The intersection property makes (rho0,rho2,rho4) independent, so this exclusion is necessary. These steps give representatives of every possible ordered commuting triple up to conjugation by G.
4. Enumerate every involution in C_G(rho4) that fails to commute with rho0 and rho2, modulo conjugation by C_G(rho0,rho2,rho4). This covers all possibilities for rho1.
5. Enumerate every involution in C_G(rho0,rho1) that fails to commute with rho2 and rho4. These are all possibilities for rho3. At this point all required commutations hold.
6. Test the full intersection property recursively: the left and right maximal string subgroups must themselves be string C-groups, and their intersection must be the middle subgroup. This is the standard recursive criterion for string C-groups.
7. For each valid prefix, enumerate its extensions in the centralizer of all generators except the last. An extension must fail to commute with the last generator and lie outside the existing prefix subgroup. Retain only extensions passing the full intersection property, and recurse.

Every prefix of a string C-group is a string C-group, so rejecting an invalid prefix loses no possible representation. Each extension strictly enlarges the generated finite subgroup, making the recursion finite without a conjectural rank bound. For these two targets there are no valid prefixes of rank six, so ranks above six are automatically excluded as well.

## Reproduction

The all-rank verifier is [psl4_higher_search.g](psl4_higher_search.g):

    gap -q -b -T research/leemans/psl4_higher_search.g
    gap -q -b -T -c 'PSL4Q:=5; Read("research/leemans/psl4_higher_search.g");'

Logs are [q=3](psl4_higher_search_q3.log) and [q=5](psl4_higher_search_q5.log). The separate initial rank-five enumeration is in [psl4_search.g](psl4_search.g); its logs agree with the all-rank search's initial candidate counts.

GAP reported total CPU runtimes of approximately 15 seconds and 46 seconds for the all-rank searches. This is evidence for a promising centralizer method, but finite cases alone do not resolve the conjecture for general q.

## Critical coverage audit

The search was reviewed against its executable code after completion:

* GAP's `OnPoints` acts on permutation-group elements by exponentiation, hence conjugation. The acting triple centralizer preserves both the fixed triple and all filters on rho1. Taking one representative of each resulting orbit therefore preserves coverage.
* The six nonadjacent commutations in a length-five string are all enforced: (0,2), (0,3), (0,4), (1,3), (1,4), (2,4). Every one of the four adjacent pairs is required to fail to commute, as necessary for a simple target.
* There is no conjugacy quotient on rho3 or later extensions, so those stages may duplicate cases but cannot omit an orbit through a stabilizer mistake.
* The recursive test rejects only conditions necessary for the intersection property. Thus the nonexistence conclusion needs only necessity of these tests, even independently of the standard theorem that makes the test sufficient as well.
* An extension centralizes exactly the required earlier prefix: all generators except the last. Requiring it outside the preceding subgroup is necessary for every string C-group, by independence of its distinguished generators.
* The first five generators of every possible higher-rank representation appear in the initial search, and every actual C-group prefix survives the necessary tests. This is why a rank-five search alone would have been insufficient, while the completed recursive searches exclude all higher ranks.

The computation does not classify rank-three or rank-four representations or prove their existence; the statement that the maximum is four additionally uses the established rank-four existence theorem. Nor does it establish that these finite-case conclusions are new: q=3 already appears in earlier enumeration work. No claim of a uniform result for odd q follows from these two cases.
