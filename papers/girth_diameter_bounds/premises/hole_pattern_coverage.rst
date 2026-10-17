Coverage by twenty-seven distinguished hole patterns
===================================================

Status: proved finite labeling cover, pending independent adoption.
This note does not assert that any of the27 formulas is unsatisfiable.

Let an actual six-layer section have the hypotheses of proof.rst and
mass21. The fixed geodesic gives missing cell11. If m=6, choose two more
missing cells from the other eight; if m=5 choose three. There are exactly
28 and56 such literal hole sets. A cell ij is written as the integer10i+j
below; this is a display convention only, not a CNF variable identifier.

Allowed relabelings, without layer reversal
------------------------------------------

Let r exchange parent labels2,3 on the A side and fix1; let c do the same
on the B side. They generate the four-element group {1,r,c,rc}. For a
choice (rho,gamma) in this group, relabel

  Ai -> A(rho(i)),  Bj -> B(gamma(j)),
  Cij -> C(rho(i),gamma(j)),
  Uij -> U(rho(i),gamma(j)),  Vij -> V(rho(i),gamma(j)).

Keep u,v and, when present, X fixed. Keep EVERY vertex's original BFS
layer index unchanged. This is just a bijection of names, with inverse
the same group element. It maps fixed edges and missing cells exactly,
fixes A1,B1,U11,V11 and all six geodesic anchors, and preserves every
actual adjacency, degree and girth condition. The predecessor condition
is preserved because layer indices and edges are unchanged. The
asymmetric local-zero degree bound and the last-layer condition are
preserved separately. Consequently the graph-to-CNF theorem applies to
the relabeled representative whenever it applies to the original hole
set. Auxiliary gate values may simply be freshly evaluated in the
representative's deterministic builder; no claimed equality of its
literal variable numbers is needed.

In particular, no transposition of the A/B sides, interchange of u,v,
or reversal of layers is used. Such a reversal would require a separate
argument for the asymmetric boundary/predecessor constraints.

Orbit counts
------------

On the eight cells other than11, r has two fixed cells and three
two-cycles; c has the same cycle structure. The product rc has four
two-cycles and no fixed cell. The numbers of fixed two-subsets are
28,4,4,4 for the four group elements, respectively. The fixed
three-subset numbers are56,6,6,0: for a single swap one chooses one
of the two fixed cells and one of its three two-cycles.

Burnside's counting lemma therefore gives (28+4+4+4)/4=10 orbits
for m6 and (56+6+6+0)/4=17 for m5. This is ordinary finite group
counting, with no novelty claim. Independently of the count formula,
the explicit disjoint partitions below certify the entire cover.

Concrete representatives and orbit partitions
---------------------------------------------

Each row gives its representative before the bar and its complete orbit
after it. Every set includes11. The listed partitions contain28 and56
distinct sets, respectively; each set has exactly the required cardinality.
The representative is the lexicographically least set in its row.

::

  m6_01: 11 12 13  |  11 12 13
  m6_02: 11 12 21  |  11 12 21; 11 12 31; 11 13 21; 11 13 31
  m6_03: 11 12 22  |  11 12 22; 11 12 32; 11 13 23; 11 13 33
  m6_04: 11 12 23  |  11 12 23; 11 12 33; 11 13 22; 11 13 32
  m6_05: 11 21 22  |  11 21 22; 11 21 23; 11 31 32; 11 31 33
  m6_06: 11 21 31  |  11 21 31
  m6_07: 11 21 32  |  11 21 32; 11 21 33; 11 22 31; 11 23 31
  m6_08: 11 22 23  |  11 22 23; 11 32 33
  m6_09: 11 22 32  |  11 22 32; 11 23 33
  m6_10: 11 22 33  |  11 22 33; 11 23 32
  m5_01: 11 12 13 21  |  11 12 13 21; 11 12 13 31
  m5_02: 11 12 13 22  |  11 12 13 22; 11 12 13 23; 11 12 13 32; 11 12 13 33
  m5_03: 11 12 21 22  |  11 12 21 22; 11 12 31 32; 11 13 21 23; 11 13 31 33
  m5_04: 11 12 21 23  |  11 12 21 23; 11 12 31 33; 11 13 21 22; 11 13 31 32
  m5_05: 11 12 21 31  |  11 12 21 31; 11 13 21 31
  m5_06: 11 12 21 32  |  11 12 21 32; 11 12 22 31; 11 13 21 33; 11 13 23 31
  m5_07: 11 12 21 33  |  11 12 21 33; 11 12 23 31; 11 13 21 32; 11 13 22 31
  m5_08: 11 12 22 23  |  11 12 22 23; 11 12 32 33; 11 13 22 23; 11 13 32 33
  m5_09: 11 12 22 32  |  11 12 22 32; 11 13 23 33
  m5_10: 11 12 22 33  |  11 12 22 33; 11 12 23 32; 11 13 22 33; 11 13 23 32
  m5_11: 11 12 23 33  |  11 12 23 33; 11 13 22 32
  m5_12: 11 21 22 23  |  11 21 22 23; 11 31 32 33
  m5_13: 11 21 22 31  |  11 21 22 31; 11 21 23 31; 11 21 31 32; 11 21 31 33
  m5_14: 11 21 22 32  |  11 21 22 32; 11 21 23 33; 11 22 31 32; 11 23 31 33
  m5_15: 11 21 22 33  |  11 21 22 33; 11 21 23 32; 11 22 31 33; 11 23 31 32
  m5_16: 11 21 32 33  |  11 21 32 33; 11 22 23 31
  m5_17: 11 22 23 32  |  11 22 23 32; 11 22 23 33; 11 22 32 33; 11 23 32 33

The machine-readable companion hole_pattern_partition.json is24913 bytes,
SHA256 087e49bcddb1411a049fe9e4ae7a78ab070723ea3248802b143249f9f7c88678.
It records all four labeled images, including repetitions from stabilizers,
as well as each distinct orbit. A tiny integer-only construction checked
disjointness and full equality with all84 literal subsets; no graph,
formula, solver or group-model computation was run. The complete
reproducible verification of that finite table is:

::

  from itertools import combinations, product
  import json
  from pathlib import Path
  data = json.loads(Path("hole_pattern_partition.json").read_text())
  cells = (12,13,21,22,23,31,32,33)
  def image(x, r, c):
      i,j = divmod(x,10)
      if r and i != 1: i = 5-i
      if c and j != 1: j = 5-j
      return 10*i+j
  assert data["fixed_cell"] == 11
  assert data["transpose_or_layer_reversal_used"] is False
  assert [g["occupied_cells"] for g in data["groups"]] == [6,5]
  for g,k,wanted in zip(data["groups"],(2,3),(10,17)):
      all_sets = {tuple((11,*x)) for x in combinations(cells,k)}
      seen = set()
      assert len(g["partition"]) == wanted
      for row in g["partition"]:
          rep = tuple(row["representative"])
          images = {str(r)+str(c): [11,*sorted(image(x,r,c)
                    for x in rep[1:])] for r,c in product((0,1),repeat=2)}
          orbit = set(map(tuple,images.values()))
          assert row["images"] == images
          assert row["orbit"] == [list(x) for x in sorted(orbit)]
          assert rep == min(orbit) and orbit <= all_sets
          assert not seen.intersection(orbit)
          seen.update(orbit)
      assert seen == all_sets
      assert g["literal_patterns"] == len(all_sets)
      assert g["representatives"] == wanted
  assert data["total_patterns"] == 84
  assert data["total_representatives"] == 27

Application and limits
----------------------

The rectangle case11,12,21,22 is exactly m5_03; its orbit has four
literal distinguished patterns. A checked refutation for that
representative therefore applies to those four patterns, through the
unchanged-layer relabeling above. Each other representative remains a
separate obligation unless and until its own exclusion is acquired.

Conditionally, acquired refutations of all27 representative formulas
would exclude equality21 with m5 or m6. Together with the separately
accepted m8 and both m7 cases, and the elementary union-size exclusion
for m<=4, this would close equality21. That conditional composition
also needs its exact gates; this cover does not manufacture them.
There is no blanket execution request, automatic succession, global
order94 exclusion, source registration, or new enumeration-prefix
credit in this document.

The underlying reviewed sources are cnf.py76319949, proof.rst4eb762ff,
and method_distinct_review.rst b9d8789e, acquired by
method_acceptance.json96bcf7f6. Their exact full pins remain in the
method record; this note only adds the finite labeling cover.
