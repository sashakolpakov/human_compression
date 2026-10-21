Diagonal transfer: full inner self-duality and outer seeds
========================================================

This addendum preserves the frozen inner_self_duality_transfer.rst
(SHA256 ad1e5e1ca10733014eb5cce76fe0c5ea907b3686c6bc065516a8bbba5732e553).
It adds two distinct conclusions. Their parity hypotheses must not
be interchanged. All arguments are read-only consequences of retained
proofs, character-table bytes and acquired order-four counts.

1. There is no outer order-four element of A = Aut(O'Nan)
-------------------------------------------------------

The ordinary ON.2 table in the already bound ctbllib ctospora.tbl has
45 classes. Its retained socle fusion occupies classes 1 through 25.
The independently acquired inversion output identifies the two
involution classes as 2 (inner) and 26 (outer).

In MOT("ON.2"), the square-power map sends the twenty outer classes,
in order 26 through 45, to

    1,3,4,4,5,6,6,9,12,13,13,16,15,20,21,19,23,23,24,24.

None is class 2. In fact the complete square-map preimage of class 2
is exactly classes 4 and 5, both in the socle. The table reader
CTblLib.MOT stores argument four as ComputedPowerMaps; its list has
unbound first entry and the displayed second entry is the square
map. Thus no interpretation of an element order from a class name
is being used.

An outer element of order four would square to a nonidentity inner
involution, necessarily class 2. The displayed map rules this out.
This is an application of the retained named character-table premise,
not a new construction or computation of the group.

Suppose a generating INNER marking (a,b,c) were reversed by an outer
automorphism x in A. Uniqueness of a reverser implies x^2=1:
its square fixes a,b,c and hence all of G. Since a^x=c and a,c are
distinct commuting involutions,

    (ax)^2 = ac

is a nonidentity involution. The element ax would be outer of exact
order four, a contradiction. Therefore every reversing automorphism
of an inner generating G-marking is inner.

Consequences for L026
--------------------

The 114 inner-reverser classes counted by the base note are now
ALL self-dual ordered A-classes of rank-three G-markings. Type by
type their numbers are exactly n_inner(4,q). The total duality-class
count is therefore

    Q = (C + 114)/2,

where C is the still unknown total of ordered A-classes. The source
claim Q=6536 is consequently equivalent to C=12958, not proved by
this identity.

The complete acquired portion with minimum adjacent order at most
five has 680 ordered classes and no self-dual ones: the type (5,5)
inner-reverser count is n_inner(4,5)=0, and the other types in the
portion have unequal adjacent orders. It therefore gives exactly
340 classes up to isomorphism and duality. The eight ordered (6,6)
G-markings are likewise all non-self-dual, since n_inner(4,6)=0, and
give exactly four duality classes. These are disjoint exact portions;
they do not establish the full rank-three or any higher-rank census.

2. Apply the same construction to OUTER inversion seeds
------------------------------------------------------

Let (x,a,b) be an acquired generating string for A whose three
involutions lie in A\G, with |xa|=4, |ab|=q, and [x,b]=1.
Put c=a^x and K=<a,b,c>. As in the base proof, a,c are distinct
commuting involutions, |bc|=q, and K is normalized by x. Since K
contains a,b, it is normal in A=<x,a,b>, and A/K has order at most
two.

Here A'=G: the quotient A/G is abelian, so A' is contained in G,
while perfectness of G gives G=G' contained in A'. Thus G is
contained in K. The outer involution a belongs to K, forcing K=A.
This is the extra generation argument needed in the outer case;
simplicity of A is neither asserted nor used.

The new marking (a,b,c) still has all entries in A\G. Its even-word
subgroup <ab,bc> is normal of index at most two in A and lies in G,
so it is exactly G. Its rotations therefore generate G and have
orders (q,q). Their simultaneous inverter b is outer. The already
accepted outer string/inversion theorem supplies full IP.

Conversely take an outer generating marking of type (q,q) that
has a reversing conjugator x in A\G. Its square centralizes the
generating marking and hence G, so it is the identity. The same
identity (ax)^2=ac gives |ax|=4; x fixes b. The recovered (x,a,b)
contains the original a,b,c and therefore generates A, and all
three entries are outer. This inverts the construction. The
reverser is unique because conjugation of A on G is faithful.

Consequently there is an exact A-equivariant bijection between
the acquired outer (4,q) classes and the subset of outer (q,q)
classes whose associated all-outer marking has an outer reversing
conjugator. No quotient by reversal is taken in this statement.
The explicit rotation words are again

    (R,S,B) = (s, s^-1 r^2, y s),    reversing conjugator x = r y,

now with the seed inverter y outer. Generation, parity and exact
orders follow algebraically; no seed word is reevaluated.

The accepted complete outer order-four row gives the exact subset:

    q             4  5  6  7  8 10 11 12 14 15 16 19 20 28 31
    outer subset  0  2  1 11  0 10 12  5 11  4  0 34 20 21 25

Its sum is 156. In particular the previously unresolved L046 outer
positive types (7,7),(10,10),(12,12),(14,14) are proved, with at
least 11,10,5,11 full-A ordered map classes, respectively. Additional
outer-inverter classes may lack this particular reversing conjugator,
so these are not asserted as the exact total outer inversion counts.

There is no conflict with Section 1: in Section 1 a was INNER and
x OUTER, making ax outer of order four. Here a and x are BOTH OUTER,
and ax is INNER of order four. These outer marking groups are A,
not G, and do not contribute to the L026 O'Nan G-marking total.

Attribution and limits
----------------------

The parent independently supplied the no-outer-four test and the
outer-generation extension. The existing amalgam and string/IP
arguments retain their earlier attribution. This application
introduces no group calculation or novelty claim. The full inner
and outer inversion spectra and the L026 ordered total remain
incomplete; no whole-original, higher-rank, conjecture or Lean
credit is inferred. Frozen earlier files remain unchanged.

Exact additional bindings
-------------------------

Paths below are absolute. The two table files and actual02/stdout
were checked against their pre-existing acquired dependency pins.
The square-map and class-index inspection is literal metadata
reading; no GAP invocation or table regeneration was performed.

* Frozen base proof and its fourteen inputs
  /Users/sasha/medusa/research/leemans/geometry/onan_regular_maps/operations/inner_self_duality_transfer.rst
  10044 bytes; SHA256 ad1e5e1ca10733014eb5cce76fe0c5ea907b3686c6bc065516a8bbba5732e553.

* Acquired ordinary ON.2 table
  /opt/homebrew/Cellar/gap/4.15.1/lib/gap/pkg/ctbllib/data/ctospora.tbl
  193334 bytes; SHA256 39854ca05e13eecbb1d2c60872d8de4d77b0a1d26c3da5b64767fdd442289a09.

* MOT record semantics
  /opt/homebrew/Cellar/gap/4.15.1/lib/gap/pkg/ctbllib/gap4/ctadmin.gi
  194666 bytes; SHA256 d6f1b0100147f8ff5c3c5b911e46b8cbbf396ce4b7cdf43d5566fdd17360089d.

* Acquired socle and involution class indices
  /Users/sasha/medusa/research/leemans/geometry/onan_regular_maps/inversion_bounds_work/actual02/stdout
  13740 bytes; SHA256 1cab22e8cc6c3bd3b67004771b3c211a3802d5de024f2f506e1665d7d6429af8.

* Accepted character/inversion input gate
  /Users/sasha/medusa/research/leemans/geometry/onan_regular_maps/inversion_bounds_root_review/manifest.json
  393 bytes; SHA256 ece7a05af8b029d7d8870c343191602112d291b8cf27dc2ebde8c746f78b998c.

* Exact independently acquired inner and outer p4 values
  /Users/sasha/medusa/research/leemans/geometry/onan_regular_maps/four_row_distinct/row.json
  1803 bytes; SHA256 e90ccb4f0184c2c3365a79838e51600cff885fbe710f4ce665a04d47e34214aa.

* Complete order-four acceptance
  /Users/sasha/medusa/research/leemans/geometry/onan_regular_maps/four_row_distinct_review/manifest.json
  382 bytes; SHA256 ac13ebf40ce91ee5b906f265d6208781117b56d00bb01b1356b05bb49ca0c740.

* Exact eight inner (6,6) classes
  /Users/sasha/medusa/research/leemans/geometry/onan_regular_maps/six_six_application_distinct01/result.json
  5251 bytes; SHA256 92c4cabb5995308513ef933586c18c0897e493ce2bded5f9d24c3d7c728ff051.

* Complete (6,6) source acceptance
  /Users/sasha/medusa/research/leemans/geometry/onan_regular_maps/six_six_application_distinct_review/manifest.json
  848 bytes; SHA256 b907a13200b8c3123eb34e88cb7177222cdbd730cbb137016f5b9e6a1164fa84.
