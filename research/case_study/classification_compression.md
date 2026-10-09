# Classification by normalizer torsors: exact reductions and reproduced censuses

9 October 2026. These are proof drafts and reproducible computational rederivations. The equivalence used is conjugacy by the stated group, or isomorphism induced by its automorphism group, with an exchange of types allowed where stated. No claim is made that an arbitrary isomorphism of the underlying unmarked graph must normalize the specified group action.

There is a useful classification theorem here, rather than merely a common vocabulary. It replaces a search through coset incidence graphs by small normalizer orbits of subgroup inclusions. The same implementation reproduces **all eight rank-two geometries in the J2 census** and **all 29 rank-two RWPRI geometries of Sz(8)**. An explicit additive torsor also rederives a complete infinite counting family in the PSL(2,q) paper, extends it to composite odd field degrees, and reveals a distinction between ordered and unordered conjugacy counts in two published tables.

The remaining cost is explicit: the finite censuses import complete subgroup-class data from GAP's [Table of Marks library](https://gap-packages.github.io/tomlib/doc/chap1.html), whose rows index subgroup conjugacy classes. The infinite PSL2 family imports Dickson's list of possible proper subgroup types. The method does not independently reprove those subgroup classifications. In particular, the J2 rank-three and rank-four classifications have **not** been reproduced.

## 1. The normalizer-torsor classification theorem

Let G be a finite group. Let H be a maximal proper subgroup, and let T be a maximal proper subgroup of H. For every proper subgroup K of G containing T as a maximal subgroup, discard K if K is contained in H. Every remaining pair defines a firm, connected, flag-transitive, residually weakly primitive rank-two coset geometry. Conversely, every such geometry can be obtained this way after choosing which maximal parabolic is called H.

Indeed, maximality of T in H and exclusion of K<=H give `H intersect K=T`. Maximality of H gives `<H,K>=G`. Strictness of the two local inclusions gives firmness. Rank-two coset geometries are automatically flag-transitive: an incident pair has a common representative. Generation gives connectedness. Primitivity of a transitive coset action is equivalent to maximality of its point stabilizer, so the three maximality conditions are exactly the rank-two RWPRI requirements.

Additional local two-transitivity requires only

    |T \ H / T| = |T \ K / T| = 2.

Now fix a particular embedded inclusion `T<K`. Put

    U = N_G(T),
    A = N_G(H) intersect U,
    B = N_G(K) intersect U.

The conjugates `K^u`, for `u in U`, are parametrized by the coset torsor `B\U`; their orbits under the stabilizer of the anchored pair `(H,T)` are the double cosets

    B \ U / A.

Discard parameters giving `K^u<=H`. This gives all **ordered** conjugacy classes with the chosen anchored inclusion `(H,T)`. If both parabolics have interchangeable roles, the resulting classes must subsequently be quotiented by reversal. It is generally incorrect to count all remaining overgroups of T without that last step.

For completeness of the input construction, take one representative K of each G-conjugacy class of proper subgroups and one representative S of each K-conjugacy class of maximal subgroups satisfying the desired local condition. Whenever `S^c=T`, use the U-orbit of `K^c`. Every possible second parabolic occurs: a conjugate of K containing T determines such an inclusion S after pulling T back. Duplicate inclusions may be removed by the orbit operations.

This is also a torsor/partition statement. On the regular G-torsor, H and K specify translation-invariant equivalence relations. Their common refinement is the T-partition; their generated equivalence relation is the indiscrete partition because `<H,K>=G`. Relative positions of these partitions are the double-coset parameters above. Keeping only abstract subgroup names or their orders would lose that information.

### A small local stabilizer gives a strong reduction

If a transitive action of K with point stabilizer T is two-transitive of degree d, then `d−1` divides `|T|`. For `|T|=3`, this leaves only `d=2` or `d=4`. In the first case K has order six, so it is C6 or S3. In the second, the action is faithful and embeds K as the order-twelve subgroup A4 of S4. Therefore

    T=C3 and local two-transitivity imply K in {C6,S3,A4}.

This removes a whole subgroup-family case search in the A4 row of the PSL2 classification. The normalizer computation then determines the embeddings and counts.

### The rank-two intersection condition needs one small calculation

When the two local actions are two-transitive, fix `x in K\T`. The K-neighbors of the vertex H are the distinct cosets `K h`, with h running over a transversal for T in H. The neighbors of Hx are `K h x`. Let c be the size of the intersection of those two short lists.

Every length-two path with middle vertex of K-type is conjugate to this one. Thus the graph is a partial linear space exactly when `c=1`. The additional allowed case of a generalized digon occurs exactly when

    |H| |K| = |G| |T|.

The latter identity counts all possible edges of the complete bipartite graph. This supplies the (IP)2 test without constructing the incidence graph. The one-path shortcut is used only with the stated local two-transitivity hypothesis.

## 2. Two complete finite rank-two censuses from the same implementation

The program [classification_rank2_census.g](classification_rank2_census.g) implements the theorem, with switches for local two-transitivity and (IP)2. It imports representative subgroups from GAP TomLib and then recomputes the local inclusions, transporters, normalizers, intersections, generation tests, type reversal and automorphism fusion. The output is in [classification_rank2_census.log](classification_rank2_census.log). The exact inputs, versions, hashes and run time are recorded in [classification_compression_certificate.json](classification_compression_certificate.json).

| Published target | Imported subgroup classes | Local inclusion classes | Maximal-parabolic anchors | G-classes before (IP)2 | Final Aut(G)-classes |
|---|---:|---:|---:|---:|---:|
| J2, RWPRI + local two-transitivity + (IP)2 |146|417|21|9|8|
| Sz(8), RWPRI |22|55|8|75|29|

For J2 the second-parabolic candidate sets after anchoring have size at most two. Exactly one of the nine classes fails (IP)2: the parabolic orders are `(6048,2160)` with intersection order 216, and the tested two vertices have four common neighbors. The eight surviving order triples `(H,K,T)` are

    (1920,1152,384), (720,1080,180), (720,576,144), (720,600,120),
    (600,300,100), (60,48,12), (60,60,10), (60,20,10).

These reproduce the rank-two count in Leemans, [*The residually weakly primitive geometries of J2*](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v21n1p77/585), Note di Matematica 21 (2002), §3. That paper also gives 19 rank-three and three rank-four geometries; those results remain outside this reproduction.

For Sz(8), local primitivity is used without requiring local two-transitivity or (IP)2, exactly as in Leemans, [*The rank 2 geometries of the simple Suzuki groups Sz(q)*](https://emis.de/ft/11479), Beiträge zur Algebra und Geometrie 39 (1998). Its Corollary 8.1 gives 29 geometries; the 75 inner-conjugacy classes fuse to precisely that number. This is a complete rederivation of that finite corollary, not a reproof of the paper's all-q Theorem 7.1.

The generator representatives are exported in [classification_J2_representatives.json](classification_J2_representatives.json) and [classification_Sz8_representatives.json](classification_Sz8_representatives.json). These are representatives of orbits, without a claim of lexicographic canonicality. They permit independent checking of the listed objects. Completeness additionally uses the imported subgroup-class catalogue and the classification theorem above. Neither GAP output nor a file hash is represented as a Lean proof of that catalogue. A separate [witness checker](classification_verify_witnesses.py) reloads the exported permutation generators without loading TomLib or running the enumeration, and checks group orders, containment, generation, global/local primitivity, and the selected local conditions. All 37 witnesses pass; see [classification_witness_check.json](classification_witness_check.json). This second check establishes validity of the objects, not completeness or pairwise inequivalence.

## 3. An explicit additive torsor for the complete A4–A4 family

Let `q=3^e`, with `e>1` odd, let `G=PSL_2(F_q)`, and work projectively. Put

    U(t) = [[1,t],[0,1]],
    H = PSL_2(F_3) = A4,
    T = <U(1)> = C3,
    H_t = U(t) H U(−t).

Changing conjugation convention replaces t by −t and leaves all counts below unchanged.

**Theorem.** All A4 subgroups of G containing T are exactly H_t, with `t in F_q/F_3`. Two parameters give the same subgroup exactly when their difference belongs to F3. Moreover

    <H,H_t> = PSL_2(F_3(t)).

Consequently all connected, locally two-transitive A4–A4 coset geometries for G are classified by the full-degree parameter cosets `t+F_3`. Ordered conjugacy classes correspond to those cosets themselves; exchanging the two parabolics identifies t with −t. Automorphisms of G additionally identify t with its Frobenius conjugates.

**Proof of the normal form.** Every nonidentity element of T has the unique fixed point infinity on the projective line. The point stabilizer in G has odd order `q(q−1)/2`. If an A4 subgroup K contains T, its normal Klein-four subgroup therefore acts freely on the orbit of infinity. That orbit has four points, is K-invariant, and its other three points are a T-orbit, hence are `t,t+1,t−1`. Thus K stabilizes

    {infinity,t,t+1,t−1} = U(t) P^1(F_3).

The full projective stabilizer of the standard four-point set is PGL2(3), of order 24. Its intersection with G is PSL2(3), of order 12: a nonsquare of F3 remains a nonsquare in an odd-degree extension. Hence K=H_t. Equality of the four-point sets is exactly equality of the parameter cosets modulo F3.

**Proof of generation.** The assertion is immediate for t in F3. Otherwise let `F=F_3(t)`. Both groups lie in PSL2(F). Suppose their generated group is proper there. Dickson's subgroup list leaves, for an odd power of three, only a Borel subgroup, a dihedral subgroup, an A4 subgroup, or a subgroup of subfield type. The first two cannot contain H. The A4 case would force `t in F3`. The S4 and A5 exceptional types are absent in this characteristic and odd extension degree; even-degree PGL subfield subgroups are absent as well.

For the remaining case let a conjugate subfield subgroup preserve a projective subline Omega. Since it contains T, its fixed point infinity belongs to Omega. Since it contains H, the Klein-four orbit `{infinity,0,1,−1}` belongs to Omega. A subfield subline containing infinity,0,1 is the standard subfield line: compose its defining projectivity with the unique subfield projectivity matching those three points. Finally H_t's Klein-four orbit forces t into that proper subfield, contradicting `F=F_3(t)`. Thus the generated group is all PSL2(F).

The only locally two-transitive coset action of A4 on a proper subgroup is its degree-four action with stabilizer C3. All C3 subgroups are conjugate in G: after moving their fixed point to infinity, their nonzero translation parameters differ by a square up to sign, and −1 is nonsquare. Finally, translating an anchored pair `(H_s,H_t)` by −s gives `(H,H_(t−s))`. Therefore this normal form covers all the asserted connected A4–A4 geometries, not just a set of examples.

**Proof of equivalence.** The normalizer of T in G consists precisely of the translations U(b): an affine multiplier preserving T is ±1, and −1 is nonsquare in Fq. The stabilizer of H and T consists of translations by F3. Hence the normalizer torsor is the additive space `F_q/F_3`, with no further fusion of ordered anchored pairs. Reversing a pair acts by t↦−t. The full automorphism group is PΓL2(q); its stabilizer of H and T induces exactly

    t+F3  |->  ±t^(3^j)+F3.

This proves the claimed equivalences. The subgroup-type classification and the automorphism-group theorem are the explicit imported group-theoretic inputs. ∎

The subgroup list is stated in the 2013 source, §4.1, Lemma 4.1 (items 8–12), and in Leemans–Moerenhout–O'Reilly-Regueiro, [*Projective linear groups as automorphism groups of chiral polytopes*](https://arxiv.org/pdf/1606.08017), §2.2, Proposition 2.3 (preprint p. 5). The semilinear description of Aut(PSL2(q)) is explicitly stated in the opening paragraph of Gorenstein, [*Finite Groups the Centralizers of whose involutions have Normal 2-Complements*](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/finite-groups-the-centralizers-of-whose-involutions-have-normal-2complements/6FBC01E6154FF052A081196345F335E9), Canadian Journal of Mathematics 21 (1969), p. 335. These inputs are used with q=3^e>3 and e odd.

For prime e this is an RWPRI family because H is maximal in G. For composite e it is still connected and locally two-transitive, but **not RWPRI**: neither A4 parabolic is maximal in G. This distinction is essential.

## 4. A closed count, including the nonfree Frobenius correction

Write

    M(e) = sum_(d|e) mu(e/d) 3^d.

This is the number of full-degree elements of F_(3^e). Translation by F3 preserves degree, so the number of full-degree parameter cosets is M(e)/3.

If 3 does not divide e, put S(e)=0. If `e=3^s m` with `s>=1` and `3` not dividing m, put

    S(e) = sum_(k|m) mu(m/k) 3^(3^(s−1) k).

Then the complete counts are

    ordered G-conjugacy classes:                 M(e)/3,
    unordered G-conjugacy classes:               M(e)/6,
    classes under Aut(G), allowing type swap:    (M(e)+4S(e))/(6e).

**Proof.** Apply Burnside to sign and Frobenius on full-degree additive cosets. No negative Frobenius operation fixes a nonzero coset: Frobenius has odd order, so iterating such an equality would give `[t]=−[t]`, hence `[t]=0`.

A nonidentity positive Frobenius power sigma^j can fix a full-degree coset only if `sigma^j(t)−t=±1`; a zero difference would put t in a proper subfield. Applying it three times gives `sigma^(3j)(t)=t`. Full degree forces its order to be three. Thus the only possible nonidentity contributors are j=e/3 and 2e/3, when 3 divides e.

Put g=e/3. On a subfield F_(3^d), the equation `x^(3^g)−x=1` has no solution if d divides g. Otherwise its automorphism has order three, its trace of 1 is zero, and it has `3^(d/3)` solutions. Möbius inversion over subfields gives precisely S(e) full-degree solutions for each right-hand side ±1. Dividing their total by the three representatives of each additive coset gives `2S(e)/3` fixed cosets for each of the two contributing Frobenius elements. Therefore Burnside gives

    (M(e)/3 + 2*(2S(e)/3))/(2e) = (M(e)+4S(e))/(6e).

The field-orbit calculation [classification_field_orbits.g](classification_field_orbits.g) independently enumerates the parameter cosets and their semilinear orbits; its [output](classification_field_orbits.log) agrees for e=3,5,7,9:

|e|Full-degree parameter cosets|Unordered conjugacy classes|Aut(G)-classes|
|---:|---:|---:|---:|
|3|8|4|2|
|5|80|40|8|
|7|728|364|52|
|9|6552|3276|366|

At e=3 one can see the entire exceptional term in a two-dimensional solved permutation action. Choose alpha satisfying `alpha^3=alpha+1`. On the quotient basis `[alpha],[alpha^2]`, Frobenius has matrix `[[1,−1],[0,1]]`. The nonzero vectors form one orbit of size two and one of size six under Frobenius and sign. For e=9 there are three orbits of size six and 363 of size eighteen. Thus dividing blindly by `2e` would give incorrect counts when three divides the field degree.

## 5. Relation to the published PSL2 tables

Primary sources checked: Buekenhout–De Saedeleer–Leemans, [*On the rank two geometries of the groups PSL(2,q): part II*](https://amc-journal.eu/index.php/amc/article/download/181/241), Ars Mathematica Contemporanea 6 (2013), 365–388, especially §2 and Tables 2 and 5; and its [publisher-hosted appendix](https://amc-journal.eu/index.php/amc/article/download/181/1862), proof of Proposition 26. Exact PDF hashes are in the source inventory and the certificate accompanying this note.

For odd prime e≠3, the formula above becomes `(3^(e−1)−1)/(2e)`; for e=3 it is two. These are exactly the **isomorphism counts** in Table 5. The whole nonempty A4 family is therefore rederived from the explicit additive torsor, and the closed formula extends it to composite e with the stated loss of RWPRI.

There is, however, a counting-convention discrepancy in the checked version. Its §2 defines conjugacy by the unordered set of the two parabolics, but Table 5 lists `3^(e−1)−1` conjugacy classes, which counts ordered parabolics. Under that printed unordered definition the value is half as large. For q=27 an independent exhaustive subgroup computation gives 8 ordered classes, **4 unordered classes**, and 2 Aut(G)-classes. See [classification_normalizer_check.g](classification_normalizer_check.g) and its [log](classification_normalizer_check.log).

The same issue occurs in Table 2 for some prime q. When H=A4 is maximal and T=C3 is semisimple, the overgroup torsor is

    N_G(T)/T = D_(2m),       m=(q±1)/6,

where the sign is chosen so that 3 divides q±1. The nonidentity elements parametrize ordered A4–A4 classes. Type reversal is inversion. There are m reflections and `floor(m/2)` nonidentity rotation classes under inversion, giving

    unordered G-conjugacy classes = m + floor(m/2),

rather than the ordered count `2m−1`. Independent normalizer computations give:

|q|Ordered G-classes|Unordered G-classes|Aut(G)-classes|
|---:|---:|---:|---:|
|13|3|3|2|
|37|11|9|6|
|43|13|10|7|

The published isomorphism counts agree. The exact check is [classification_a4_torsor_check.g](classification_a4_torsor_check.g), with [output](classification_a4_torsor_check.log). This is a version-specific correction to the conjugacy column under the paper's stated convention, not a claim that the geometries or the principal isomorphism classification are wrong. A bounded exact-title search found no erratum; publication priority of this observation is not established.

## 6. What extends to higher-rank classifications, and what does not

For a tuple of subgroups `(G_i)`, put `G_J=intersection_(j in J) G_j`, with `G_empty=G`. All checks below can be performed in the common regular torsor, without constructing separate incidence graphs.

* Flag transitivity is the simultaneous-coset-intersection condition `intersection_(j in J)(G_i G_j)=G_i G_J`, for every i outside J. It follows by inductively extending a base flag: the left side parametrizes faces incident with it and the right side parametrizes those reached by its stabilizer.
* Once flag transitivity is established, residual connectedness is `G_J=<G_(J union {i}):i notin J>` whenever the residue has rank at least two.
* Residual weak primitivity says that, for every proper J, at least one `G_(J union {i})` is maximal proper in G_J. Panel firmness and local two-transitivity are the corresponding index and double-coset conditions at the bottom of this diagram.
* Every rank-two residue can then be tested for (IP)2 as above when the local two-transitivity assumption is present.

These are complete finite subgroup-diagram certificates. They support recursion through geometries of maximal subgroups and extension by overgroups of the local parabolics. Residual weak primitivity supplies a maximal chain from G to the Borel subgroup, so rank is bounded by the subgroup-chain length.

That recursion is **already part of the authors' algorithmic work**: the 2002 J2 paper §2 explicitly describes computing geometries of maximal subgroups and testing extensions. A torsor formulation makes the common mechanism and relative-position data precise; it does not erase the search for compatible higher-rank diagrams. Pairwise compatibility alone is insufficient: simultaneous coset intersections and all residues must still be checked. No reproduction of the 19 rank-three or three rank-four J2 objects, nor of the corresponding M12/J1 higher-rank censuses, is claimed here.

The demonstrated compression is consequently specific: two complete finite rank-two censuses, an infinite PSL2 counting family with a composite-degree extension, and a reusable classification/certificate theorem. It is not evidence that dozens of complete sporadic-group classifications follow from three short lemmas without substantial subgroup data and a completeness computation.
