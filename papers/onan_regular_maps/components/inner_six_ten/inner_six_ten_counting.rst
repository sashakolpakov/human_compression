Existence of inner inversion for type (6,10)
==========================================

Proposed source application, pending distinct mathematical review.
Put G = O'Nan, g = 460815505920 and A = Aut(G), with |A:G| = 2.
There are at least twelve A-orbits of generating ordered pairs (R,S)
with |R| = 6, |S| = 10, |RS| = 2 and an inner simultaneous inverter.

This is an existence/lower-bound proof, not an exact split, an explicit
generating representative, or a new calculation in G. It uses the
accepted complete third-involution records and the acquired subgroup
and character premises below. The held one-witness reader and the
77-candidate request are neither executed nor changed.

A free triple has odd common rotation centralizer
------------------------------------------------

Let a,b,c be involutions in A with a and c distinct and commuting.
Set R = ab and S = bc. Then b inverts R and S, and RS = ac has order
two. Suppose C_A(a,b,c) = 1. Define C = C_A(R,S). Conjugation by b
is an automorphism alpha of C with alpha squared equal to the identity.
Its fixed subgroup is

    C_C(b) = C_A(R,S,b) = C_A(a,b,c) = 1,

since a = Rb and c = bS. This does not identify the rotation-pair
centralizer with the triple centralizer.

Here is the elementary fixed-point-free involution argument in full.
The map f(x) = x^-1 alpha(x) on the finite group C is injective:
f(x) = f(y) implies y x^-1 = alpha(y x^-1), hence y = x. Therefore
it is surjective. Also alpha(f(x)) = f(x)^-1. Thus alpha inverts
every element of C. Inversion is an automorphism only for an abelian
group, as follows by comparing alpha(xy) = x^-1 y^-1 with
(xy)^-1 = y^-1 x^-1. Any element of order two would be fixed by
alpha, so C has odd order. The argument also covers C = 1; if C
is nontrivial, its fixed-point-free automorphism cannot be the identity.

The quotient map A -> A/G = C2 is trivial on the odd group C, so C
is contained in G. In particular

    |C| divides gcd(|C_G(R)|, |C_G(S)|).

The accepted centralizer theorem gives C_G(R) = C3^2 x D8 of order
72 when |R| = 6. The accepted order-ten theorem gives the sole
class 10A and C_G(S) = C20 of order 20. Hence |C| divides four
and is odd, proving C_A(R,S) = 1.

If b and b' simultaneously invert the same R,S, their quotient
centralizes R,S, so b = b'. Consequently (a,b,c) -> (ab,bc) is
injective on all the selected free triples, including nongenerating
ones. The fixed-point-free argument is classical elementary group
theory; no historical novelty is claimed.

Thirteen acquired free triple orbits
-----------------------------------

The accepted complete inner order-six pair partition has full
stabilizers H = C_A(a,b) of orders 4,16,16. Its independent third-point
acquisitions partition all 1750 inner c != a commuting with a.
Every row's exact |bc| and H-orbit size were checked before the
later generation selector, which selected q = 6 only.

Select rows with product_order = 10 and weight = H_order:

    family          |H|   complete selected row indices
    class2_pair1      4   3,5,17,40,49,199,226,287,343,398,407
    class3_pair1     16   90,91
    class3_pair2     16   none

These are eleven plus two plus zero different full A-orbits of
ordered triples. Indeed the accepted first-pair normalization
separates its full A-classes, and each H-orbit of size |H| has
trivial triple stabilizer. Their A-saturation T therefore has

    |T| = 13|A| = 26g.

All three involutions lie in G, so the resulting inverter b is inner.
No untested generation field is used. By the preceding argument the
map from T to ordered rotation pairs is injective.

Exclude the two centralizer maximal families
-------------------------------------------

The accepted complete character evaluations for all thirteen maximal
classes show nonzero raw (6,10) pair counts only in roster rows 6,7,11:

    row / table             |M|       x_M(6,10)    [G:M]   x_M/|M|
    6 / J1                175560        8602440    2624832       49
    7 / 4_2.L3(4).2_1     161280        1249920    2857239     31/4
    11 / ONM5              25920          64800   17778376      5/2

Here x_M counts ALL ordered pairs inside M with exact orders 6,10
and involutory product. It is not a generating-pair count or a
triple count. All other ten maximal class counts are zero.

Every row 7 subgroup is C_G(t) for an inner involution t, by the
accepted involution-centralizer premise. Any pair contained there
has t in C_A(R,S), contradicting the established C_A(R,S) = 1.

For row 6, the acquired outer involution a0 has full centralizer
of order 351120. The accepted outer-three argument proves

    C_A(a0) = <a0> x C_G(a0),    |C_G(a0)| = 175560.

The complete subgroup roster has exactly one G-conjugacy class of
subgroups of order 175560: row 6, labelled J1, and it is maximal.
This joins the actual centralizer to that row without identifying
groups merely from a label or character fingerprint. Every row 6
conjugate consequently centralizes an outer involution conjugate
to a0. Such an involution would also belong to C_A(R,S), again
impossible. We need only this nontrivial centralizer; no equality
C_A(J1) = <a0> is asserted or needed.

It follows that a nongenerating pair arising from T must be
contained in a row 11 maximal subgroup. The existence of a
maximal overgroup for every proper generated subgroup and the
complete thirteen-class/count list are explicit borrowed inputs.

The bound and its source scope
------------------------------

There are g/25920 = 17778376 actual row 11 subgroups. Counting all
their raw pairs, with possible multiple containments permitted,
gives the upper bound

    # nongenerating triples in T
        <= (g/25920) * 64800 = (5/2)g.

Injectivity of triples into pairs was proved before this comparison.
Thus at least 26g - (5/2)g = (47/2)g selected triples generate G.
Generation is invariant under A and each selected orbit has size
2g. The number of generating A-orbits is therefore an integer at
least 47/4, hence at least twelve. The equivariant injective map
to pairs gives twelve distinct ordered-pair A-orbits with inner
inverter, proving the claimed positive source type.

The current accepted union lists inner (6,10) as unresolved; it
does not supply a desired count to this proof. All 136 numerical
cells and the exact total 953 for (6,10) stay unchanged. No explicit
member of the thirteen candidate orbits is identified as generating.
No claim about the remaining spectra or whole original follows.

Exact retained interfaces
-------------------------

All paths below are relative to the retained study root
/Users/sasha/medusa/research/leemans. O denotes geometry/onan_regular_maps.
The pins bind imported accepted facts; this review reads their proofs
and existing metadata, not a new group/character computation.

* Full A pair classes and H orders
  O/even_pair_application_distinct_review/manifest.json
  398 bytes; SHA256 d07305ec869d6c6ba4c15e1b4796a65903a2487bad0ae5a343b71dba9f07613a.

* Full third-domain independent acquisition
  O/six_six_acquisition_distinct_review/manifest.json
  1604 bytes; SHA256 1a22e3a4a3a2a72bf83a18864c29b7328b64834938fef9b20d8a67171a678092.

* Acquisition fresh-result/receipt/journal join
  O/six_six_acquisition_distinct_review/result.json
  9501 bytes; SHA256 549cfa7364d7b2a65919ef392035d218bb1e3c599ca04321fc49bbd38d19ac1f.

* First family, 11 selected rows
  O/six_six_acquisition/remaining_first_pair/literal01/result.json
  166232 bytes; SHA256 b57d58988f0b0b175b554d5747b75cde7d87f029db7be8321774b2c1093f3942.

* Second family, 2 selected rows
  O/six_six_work/class3_pair1/independent_result01/result.json
  49191 bytes; SHA256 9bfe3953b93ff6b3917435c9f5d1ea852880c87934c21960688895eded203559.

* Third family, 0 selected rows
  O/six_six_work/class3_pair2/independent_result01/result.json
  48133 bytes; SHA256 3f17ba3db5a21805ec111b89e51e92bc963c4e53b9a4d3c5b2da0c6a51d922b6.

* Order-six centralizer theorem and inner involution centralizer premise
  O/centralizer_union/centralizers.tex
  9286 bytes; SHA256 6697ee4a26b1e5d2653051966c200eedb325a03fc4976f8bdbf72152add734d6.

* Centralizer theorem accepted adoption
  O/centralizer_union_root_adoption/manifest.json
  382 bytes; SHA256 162e3ef7a6db2ea96d7204c1c5170529ee74dfafec33b37f65d83ab8ba29c050.

* Order-ten centralizer and exhaustive three nonzero maximal classes
  O/order10_overlaps_v1/column.tex
  8552 bytes; SHA256 8c0ade4129174715e1f235a00a64316b4c94ea3c32b9735c31eac92401d41a57.

* Order-ten accepted distinct review
  O/order10_overlaps_distinct_review/manifest.json
  600 bytes; SHA256 bee9393cc2cddc03847fd95ef1230fd9735a9202bd6aaf48852b6c518b4cbc16.

* Actual outer involution centralizer order and index-two direct product
  O/outer_three_v1/outer.tex
  9050 bytes; SHA256 e645d1bf3952d263e0d5018aeb8afb302bf22cf700421e7603b6a6e674704388.

* Outer centralizer application accepted review
  O/outer_three_distinct_review/manifest.json
  373 bytes; SHA256 a1b79a0be8f8bb06046a65a4378b6f392447983fd4c2fa89dcc24be8153e6668.

* Underlying acquired full-automorphism character data
  O/inversion_bounds_root_review/manifest.json
  393 bytes; SHA256 ece7a05af8b029d7d8870c343191602112d291b8cf27dc2ebde8c746f78b998c.

* Complete roster: row1 maximal list, unique order175560 row6, rows7/11
  algebra/subgroup_atlas/data_intake/parsed/on/table.json
  743912 bytes; SHA256 3354969358133e7747f934eb0500addcc096be53cff754add51ff8461b51164e.

* Raw thirteen maximal contributions at (p,q)=(6,10)
  corpus106_L046_maximal_bounds_v1/bounds.json
  307719 bytes; SHA256 cb84d983d930ff4d10a0da98281fe16d9dc0356be5a2b2b1ef60f19b9a8b0b4f.

* Accepted maximal character/count interface
  corpus106_L046_maximal_bounds_independent_review/manifest.json
  1487 bytes; SHA256 76572289d9f351b7d73eb01ffd029b1ae0870a3d66fd1dc62a8de4dc726408d9.

* Historical comparison: accepted88/88 and unresolved inner6,10
  O/source_synthesis_work/counting_spectrum.json
  7427 bytes; SHA256 d6c09ad9d01e5e1e1298de836106d3e8bb05433cb5c9a5b8cdc5319031f7f47f.

Attribution: the parent and finite_recoveries independently challenged the
fixed-point-free argument and counting transfer before final review. The
new contribution is this application of the elementary centralizer lemma
to accepted candidate orbits. The character tables, complete roster,
centralizer theorems, model and orbit acquisitions remain named imports.
No files in a frozen prior packet, execution guard, or public/CURRENT
record are changed.
