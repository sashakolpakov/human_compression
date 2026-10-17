Existence of inner inversion for type (6,28)
==========================================

Proposed source application, pending distinct mathematical review. It uses
only accepted finite records and subgroup/counting premises. No generation
test, new group calculation, or explicit choice of a generating representative
is made. Put G=O'Nan, g=460815505920 and A=Aut(G), with |A|=2g.

Claim
-----
There are at least two A-orbits of generating ordered pairs (R,S) of G with
orders (6,28), involutory product, and an inner simultaneous inverter.
In particular the existing source assertion of this inner positive type is
true. This is not an exact count and does not complete either spectrum.

Acquired candidate orbits: no generation inference
-------------------------------------------------
The accepted complete even-pair partition and its three inner order-six
families identify all A-classes of ordered inner involution pairs (a,b)
with |ab|=6. Their full pair stabilizers H=C_A(a,b) have orders 4,16,16.
For each fixed pair, the accepted third-involution reader partitions the
entire set of inner c != a commuting with a into H-orbits. It computes
|bc| for EVERY orbit before the later q=6 generation selector. Thus these
already acquired order fields can also be used for q=28. Only orbit weights
and exact product orders are used below, never the untested generation fields.

Select rows with product_order=28 and weight=H_order. The three independent
result files give respectively 44,10,10 such rows. The complete indices are:

class2_pair1 (H=4):
  45,48,78,84,99,112,113,119,155,159,163,166,176,204,212,225,251,261,
  274,276,280,313,315,318,320,324,332,333,335,336,338,346,355,365,
  388,389,395,410,412,416,419,438,439,450.
class3_pair1 (H=16):
  27,33,34,36,47,55,78,85,104,107.
class3_pair2 (H=16):
  39,57,72,75,85,87,96,118,121,123.

An H-orbit of size |H| has trivial third-point stabilizer, hence
C_A(a,b,c)=1. The complete pair-class normalization makes these 64 different
A-orbits of ordered triples. Consequently their A-saturation T has exactly
64|A|=128g triples. All satisfy a,b,c in G, |a|=|b|=|c|=2, a != c,
ac=ca, |ab|=6 and |bc|=28. No generation has yet been deduced.

From triple freeness to uniqueness of the inner inverter
------------------------------------------------------
For a triple in T put R=ab and S=bc. The involution b simultaneously
inverts R,S. We prove C_G(R,S)=1 without assuming <R,S>=G.

The accepted order-28 class premise gives |C_G(S)|=28. Since <S> has that
order, C_G(S)=<S>. Therefore C_G(R,S) is a subgroup of the cyclic group C28.
If it has even order it contains z=S^14. Then z commutes with R,S and b:
the last assertion follows because b inverts S and hence fixes its unique
involution. It follows that z commutes with a=Rb and c=bS, contradicting
C_A(a,b,c)=1. Thus C_G(R,S) has odd order, either 1 or 7.

Let U=<S^4>, of order 7. The accepted transvection-normalizer lemma gives
N_G(U)=N_M(U) of order 8232 for a projective maximal M=L3(7):2 containing S.
Its conjugation action on U realizes all six automorphisms. Indeed in the
accepted coordinates U=<I+E13>, the determinant-one diagonal matrices
diag(lambda,lambda^-1,1), lambda in F7*, give all nonzero scalings of E13
(or their inverses, depending on the conjugation convention). Quotienting
by the scalar center does not change this action. Hence

    |C_G(U)| = |N_G(U)| / |Aut(U)| = 8232/6 = 1372 = 4*7^3.

If C_G(R,S) had order 7, it would contain U, so R would belong to C_G(U).
That is impossible because |R|=6 and 3 does not divide 1372. This proves
C_G(R,S)=1. Notice that the argument distinguished the triple stabilizer
from the rotation-pair centralizer; their equality was not assumed.

If two inner involutions b,b' invert the same ordered pair R,S, then their
quotient belongs to C_G(R,S). Thus b=b'. The map

    (a,b,c) -> (R,S)=(ab,bc)

is injective on T. It remains injective even on its nongenerating part.
This is the key point allowing a raw ordered-pair count to bound triples.

Exhaustive proper overgroups and the count
-----------------------------------------
The accepted complete cyclic-28 ancestor list has exactly three possible
maximal G-conjugacy classes: roster rows 2 and 3, each L3(7):2 of order
m=3753792 and class length g/m=122760, and row 7, the involution
centralizers. There are no other maximal overgroup classes for S.

If a triple in T has <R,S> proper, the pair lies in one such maximal.
It cannot lie in an involution centralizer C_G(t). Since t commutes with S,
the equality C_G(S)=<S> forces t=S^14. Then t commutes with R,S,b and
hence with a,b,c, contradicting triple freeness as above.

Thus every nongenerating pair arising from T lies in a conjugate of one of
the two projective maximal classes. The accepted raw character evaluations
give, in EACH such maximal M,

    x_M(6,28) = 234612000 = (125/2)*3753792.

Here x_M counts ALL ordered pairs (R,S) in M with |R|=6, |S|=28 and
|RS|=2. It is not a generating-pair count, a triple count, a count divided
by duality, or a source-supplied numerical answer. The bound counts all
pairs in each of the 122760 actual conjugates of each maximal class.
Possible multiple containments only make it an upper bound. By injectivity
of T -> (R,S), the number of nongenerating triples in T is at most

    2*(g/m)*x_M(6,28) = 125g.

Since |T|=128g, at least 3g triples in T generate G. Generation is invariant
under A, and every orbit in T has size |A|=2g. The number of generating
A-orbits is therefore an integer at least 3/2, hence at least two. Their
inverter is the inner involution b, proving the claim.

Exact retained interfaces
-------------------------
Paths below are relative to geometry/onan_regular_maps unless prefixed S/,
where S is the retained research/leemans study root. The small file hashes
were joined read-only; no imported numerical or group calculation was rerun.

* Full pair classes/stabilizers: even_pair_application_distinct_review/manifest.json,
  d07305ec869d6c6ba4c15e1b4796a65903a2487bad0ae5a343b71dba9f07613a.
* Complete third-orbit acquisition: six_six_acquisition_distinct_review/manifest.json,
  1a22e3a4a3a2a72bf83a18864c29b7328b64834938fef9b20d8a67171a678092.
  Its result.json, 549cfa7364d7b2a65919ef392035d218bb1e3c599ca04321fc49bbd38d19ac1f,
  binds all fresh result paths, execution receipts and complete journals.
* First fresh family: six_six_acquisition/remaining_first_pair/literal01/result.json,
  166232 bytes, b57d58988f0b0b175b554d5747b75cde7d87f029db7be8321774b2c1093f3942.
  The accepted prefix-plus-remainder admission in that gate is retained.
* Second fresh family: six_six_work/class3_pair1/independent_result01/result.json,
  49191 bytes, 9bfe3953b93ff6b3917435c9f5d1ea852880c87934c21960688895eded203559.
* Third fresh family: six_six_work/class3_pair2/independent_result01/result.json,
  48133 bytes, 3f17ba3db5a21805ec111b89e51e92bc963c4e53b9a4d3c5b2da0c6a51d922b6.
* Order-28 theorem and raw-count acquisition: order28_column_distinct_review/manifest.json,
  020c7d9d14f5a15d91637e384da1958136abbb626dccb3266745afa32ad6254a;
  author manifest order28_column_v1/manifest.json,
  f3efaa09f856a8a063ad15a5f2e1d078c71c8a75bc2fa4035988d7461102a198.
  The proof column.tex, 68c863bc8eee885851eaedc9a7284551c6e731ddd8db02a4c0b7a2852fbd3f02,
  provides C_G(S)=C28, the exhaustive three maximal classes and N_G(U)=8232.
* Raw numerical interface: S/corpus106_L046_maximal_bounds_v1/bounds.json,
  307719 bytes, cb84d983d930ff4d10a0da98281fe16d9dc0356be5a2b2b1ef60f19b9a8b0b4f.
  Its (p,q)=(6,28) contributions for L3(7).2 and ONM2 both give
  order 3753792, count 234612000, index 122760. The accepted order-28
  calculate.py reconstructs these values from the acquired character vectors.
* Complete roster: S/algebra/subgroup_atlas/data_intake/parsed/on/table.json,
  743912 bytes, 3354969358133e7747f934eb0500addcc096be53cff754add51ff8461b51164e.
  The accepted order-28 proof joins its native source pages and checks the
  complete ancestors of cyclic row 466, including only maximal rows 2,3,7.
* Historical comparison and existing positive union:
  source_synthesis_work/spectrum_union_after_derived_power/result.json,
  c1bfd6071a73ac21d29fe5f8e48be79be44c137567d0a8d30225ac2e7be27232.
  Inner (6,28) is among its unresolved asserted types. The fixed source's
  inner-positive list and conventions are retained through that union.

Scope
-----
The candidate generation fields for q=28 remain untested. This proof does
not identify which saved representatives generate G and does not adopt or
execute the held 77-candidate request. It gives existence by a counting
comparison. All 136 exact numerical table entries remain unchanged. The
held one-witness (6,10) request, outer (6,12) refutation, remaining source
types and whole-original status stay separate. The character table/model,
complete subgroup roster and accepted orbit certificates are explicit
borrowed premises, not independently reconstructed in this note.
