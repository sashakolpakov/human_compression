# Independent review of the subline residue calculation

Phase183; reviewer distinct from the phase182 manuscript and Python-checker
author. This review accepts the stated correction and its proof. It does
not admit the entire source manuscript, an open-conjecture solution, or an
end-to-end Lean certificate.

## 1. Reviewed statement and source contract

The reviewed manuscript is `phase182_inversive_residues.md`, SHA256
`db84a028b3ffda1b639db96d61ae0187d510f8e2c4598d75b482d0d6afab965d`.
Its exact scope is literal Construction2 applied to the classical subline
design S(3,q+1,q^e+1), where q≥3 is a prime power and e≥2. In this scope:

1. The result is a firm rank-four geometry, with panel sizes
   2, q, (q^e−1)/(q−1)−1, q−1 in the stated type order.
2. It is residually connected if and only if e=2.
3. When e=2, its full type-preserving automorphism group is PΓL₂(q²),
   and it is flag-transitive if and only if q=4.

The primary source was read before the author checker: D. Leemans,
*A Generalization of a Construction due to Van Nypelseer*, Beiträge zur
Algebra und Geometrie 46 (2005), 561–574; Construction2 on printed p.564,
the definitions on pp.561–562, and Lemma5 on p.571. The source PDF is
`sources/older_L092_gwdg.pdf`, SHA256
`f76a72aeec658ace5d821519a686c3041e455d3a1c5c4276988bd711ba830403`.
The construction is the source's construction, with its acknowledgements
to Van Nypelseer and Meixner; the underlying subline designs are classical.
These are retained inputs, not new constructions of this project.
[Primary source](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.46/no.2/b46h2lee.pdf).

The literal residual-connectivity assertion in Lemma5 is false: q=3,e=2
is a counterexample. The proof there invokes Theorem6, whose conclusion
concerns a conjunction including flag transitivity and a construction
applied to a rank-three geometry. It does not establish failure of residual
connectivity in the case at hand. The correction does not refute the
subline branch of Theorem11: its conjunction still selects q=4,e=2.
Other branches of that theorem, the full source contract, and the unital
conjecture are outside this review. No historical priority is claimed for
the correction.

## 2. Independent reconstruction and exact comparison

`phase183_inversive_review.g` does not read the author checker, its block
list, its incidence lists, or a saved answer. It builds GF(9) using GAP's
native field arithmetic. It finds the sublines as harmonic four-subsets
of the ten projective points, using determinant cross-ratio −1. In
characteristic three all six cross-ratio transforms of −1 coincide, so
the test is independent of the ordering of a four-subset. Normalizing an
ordered triple to ∞,0,1 shows that these are precisely the F₃ sublines.
The program additionally verifies that every triple is in exactly one
of the resulting thirty blocks.

The marked objects are stored as (B,T), where T is a two-subset of B.
The author instead stores (T,B\T). Each of the six literal incidence
rules is tested directly. Flags are enumerated over all Cartesian
products for all sixteen type subsets; equality with all chamber
projections checks that every flag extends. Connectivity is checked by
merging component labels over every residue edge. These choices differ
from the author's custom field arithmetic, projectivity-orbit block
construction, recursive flag enumeration, and breadth-first connectivity
algorithm.

`phase183_review.py` transports the native field through an explicit
root of X²+1 and reindexes every object. It compares the hash of the
complete block, object and adjacency data with the author's freshly
computed certificate. This checks the full incidence structure, rather
than only a list of matching counts. The common certificate digest is
`148353e0ce5d781cc2b0e17ac74104c0bff9537bd80c15b357a8a7ca8734351c`.
It hashes the canonical JSON bytes without a final newline; the saved
`native_certificate.json` has a final newline and consequently a separate
file hash in the export manifest.

The fresh replay under `python3 -O` gave:

| Quantity | Result |
|---|---:|
| Objects by source types 1,2,3,4 | 10,180,30,10 |
| Flags of sizes 0,1,2,3,4 | 1,230,1650,3600,2160 |
| Connected residues of rank at least two | 1881 of 1881 |
| Rank-two partial-linear-or-digon checks | 1650 of 1650 |
| Panels with two completions | 2160 |
| Panels with three completions | 1440 |
| Full design automorphism order | 1440 |
| Chambers | 2160 |

All typed flag counts and all residue sizes are preserved in
`phase183_review_replay/review.json`. The native GAP calculation took
about 1.91 seconds, and the fresh author calculation about 0.06 seconds
on this machine. Timings are observations, not complexity bounds.

Two altered incidence relations are rejected with a nonextendable typed
flag: allowing equality between original and copied points, and allowing
a marked object to be incident with its own underlying block. Both
changes are made to uniquely identified source lines, and neither
altered program reaches the final acceptance marker. They check the two
disjointness restrictions most likely to be lost in a transcription.
This is a pair of targeted controls, not a claim of complete mutation
coverage.

Replay, from the directory containing the reviewed files:

```sh
python3 -O phase183_review.py --gap /opt/homebrew/bin/gap \
  --output-dir /private/tmp/phase183_fresh_review
```

The output directory must not already exist. GAP and Python are trusted
execution dependencies. The runner rejects errors, GAP warnings, missing
acceptance markers, failed incidence comparison, surviving mutations,
and any change in a reviewed input during execution. The final export
manifest binds the programs, the observed outputs and the source PDFs.

## 3. Review of the uniform proof

All six rank-two residues were recomputed from the six incidence rules.
Here the labels are the author's 0,1,2,3, one less than the source labels.
Write r=(q^e−1)/(q−1).

| Fixed types | Recomputed residue |
|---|---|
| 0,1 | K_(r−1,q−1) |
| 1,2 | K_(2,q−1) |
| 1,3 | K_(2,r−1) |
| 2,3 | Vertex-edge incidence of K_(q+1) |
| 0,3 | Affine points other than z, and affine lines avoiding z |
| 0,2 | Affine points outside L, and affine lines meeting L once |

The derived design at an original point is AG(e,q), not an unspecified
linear space: after moving the point to ∞, the derived blocks are exactly
aF_q+b. The fifth graph is connected because two points whose joining
line contains z can be joined through a point off that line. In the last
graph, each outside point w determines the affine plane spanned by L and
w. Every permitted line through w stays in that plane, so no path changes
the plane. Within a plane the graph is connected: joining lines suffice
unless they are parallel to L, in which case a point outside the two
parallel lines gives a two-line path. Such a point exists for q≥3.
The number of components is therefore

    (q^(e−1)−1)/(q−1),

each with q(q−1) point vertices and q² line vertices. This is one precisely
when e=2. The exclusion q=2 is necessary for that within-plane argument;
the manuscript explicitly excludes it.

The four singleton residues and the empty-flag residue were checked
separately. At an original point, the affine point-line nonincidence
subgraph is connected because a parallel class has at least three lines,
one avoiding any two prescribed points. At a marked object the residue
is complete tripartite. At a block the original points in the block and
copied points outside it form a connected complete bipartite subgraph.
At a copied point the original points and marked objects contain the
subdivision of the complete graph on all other points. The whole geometry
contains the original-copy complete bipartite graph minus its matching.
In every case the remaining vertices attach by a stated incidence.
Thus the proof checks all residue types; it does not infer residual
connectivity from a sample of rank-two residues.

The panel counts are correct. The argument that every pair extends uses
the six described residue graphs, which have no isolated vertices;
triples extend by the panel calculation and singletons belong to pairs.
This proves the geometry axiom without assuming it in the connectivity
argument. Every panel size is at least two in the stated parameter range.

## 4. Full automorphisms and flag transitivity

The reconstruction of the full type-preserving geometry group is valid.
The original-copy inequality relation forces the two point permutations
to agree. Original-point incidence recovers every block. The original
and copied neighbors recover the pair T and its tail E, hence each marked
object. Conversely a design automorphism preserves all six relations.
Consequently Aut(Γ)=Aut(S); this is not merely a lower bound furnished by
a convenient subgroup.

For q=3 the independent program tests every one of the 7! permutations
fixing 0,1,∞ and finds exactly two that preserve the block family. The
known sharp triple transitivity of PGL₂(9), which follows from elementary
fractional-linear normalization, then gives the full design group order
10·9·8·2=1440. Together with the reviewed reconstruction this is also
the full geometry group order. Its failure to be divisible by 2160
excludes flag transitivity. Thus the finite full-group calculation is
independent of Kantor's classification input.

For the uniform e=2 statement the manuscript retains Kantor's
classification of highly transitive design groups. I checked Theorem3
and its proof on printed p.73 of W. M. Kantor, *Homogeneous designs and
geometric lattices*, J. Combin. Theory A38 (1985), 66–74. The proof gives
the required PΓL upper bound. The abbreviated Theorem10 in L092 does not
state that upper bound, so consulting the earlier primary source matters.
The projective group ensures that the full design group satisfies the
transitivity hypothesis. For e=2 the degree q²+1 excludes the affine
binary and Mathieu alternatives. All semilinear projectivities preserve
the subline family, giving equality. This input is credited and retained,
not reconstructed by the current proof.
[Kantor primary PDF](https://pages.uoregon.edu/kantor/PAPERS/homogeneousdes.pdf).

The retained PDF is now available at
`sources/phase183_kantor_homogeneousdes.pdf`, SHA256
`36532c56e2af68c0b043c3b21818dbc71fe5ce250e9f380315e122842de308a2`.
It was downloaded after the phase182 author's recorded unsuccessful
local acquisition, so that historical sentence in the frozen author
manuscript is not evidence of a current source gap.

The chamber count |PGL₂(q²)|q and full group order 2f|PGL₂(q²)|, for
q=p^f, are correct. The divisibility implication q|2f leaves only q=4.
For q=4 the base flag normalization and its stabilizer action are valid:
Frobenius squares cyclically permute the four nonidentity elements of
F₁₆*/F₄*, and multiplication by F₄* permutes the three eligible copied
points inside each selected class. This proves the required transitivity
on all twelve completions of a fixed base flag. No unstated computational
transitivity assumption remains in that sufficiency argument.

## 5. Attribution, formal status and admission decision

The construction, classical subline designs, elementary projective
normalization and Kantor group classification remain attributed inputs.
The phase182 contribution is the complete residue calculation and the
resulting correction. The phase183 contribution is independent proof
review and an independently authored finite reconstruction, including
the full small-case group census and exact incidence comparison.

Accepted: the three stated propositions and the finite counterexample
at q=3,e=2. The sole requested mathematical-scope clarification, that
the retained automorphism input is being used for e=2, is present in
the hash-bound manuscript. No remaining mathematical defect was found
within this scope.

Not supplied: a Lean formalization of these propositions, a proof of
all L092 main results, a replacement of the source's other families, a
matched-source compression ratio, or an open-conjecture solution. The
new whole-source principal count is zero. Extending the residue argument
to other derived designs is further work, not part of this acceptance.
