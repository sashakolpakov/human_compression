# Independent review of the thirteenth-source integration

10 October 2026. **PASS for the complete declared principal contract, with the additive phase116 ledger correction and the explicitly retained background.** The original phase110 ledger alone fails this review. Its manuscript and mathematical programs require no correction. This verdict follows a fresh reading of the new mathematics and primary source, a complete author replay, an independently written exhaustive census, and a separate semantic audit of the corrected source bindings.

The unchanged continuous manuscript is `phase110_commuting_pairs_integration_manuscript.md`, 351348 bytes, SHA256 `31bf7977cf4712c10fa552374fcec41b676f74f6a1f3266be4756555347e7f3b`. The original author manifest is SHA256 `ed62d34e741342ee2da07485a76bea4e3b172fb373a2cb5ad1319fad3cd54c9c`. The required additive correction is bound by `phase116_commuting_pairs_manifest.json`, SHA256 `4975931d45b53a8a388904dec6413b3b4c295dcb9d8e321f98a59e00531cc412`. Its corrected ledger is SHA256 `59a2fc1872f45efdb8d465f81d94f5936754ab69d8ef8cc912d0f05ccd5bdf73`.

The reviewer authored neither the phase110 candidate nor the phase116 correction. The reviewer discovered the ledger defect; root authored the additive repair, which was then independently checked here. Frozen author inputs and the public repository were not changed by this review.

## Exact intake and attribution

The new source is L066, Ann Kiefer and Dimitri Leemans, *On pairs of commuting involutions in Sym(n) and Alt(n)*. The contract is its complete nine-page author PDF, SHA256 `788654bc5d015b72ad65819a848d78645a2e69fe940f44908b5d6452410fd134`. Publication metadata identifies Communications in Algebra 41(12) (2013), 4408–4418; the publisher's full text was not compared. Every line of the primary extraction was read, and all nine primary PDF pages were individually viewed, including the bibliography. The existing privately rendered pages were reused and hash-checked; the reviewer does not claim a new primary rasterization. Primary PDF, full text and images are excluded from exports.

The four principal targets are complete Theorems 1.1 and 1.2, including their exceptional six-point clauses; Theorem 3.6, exactly two regular S6 polyhedra up to isomorphism and duality; and Theorem 4.4 in its regular-polyhedron context. The full inventory also includes every one of the thirteen numbered source items, fourteen rows of Table 1, all five displayed exceptional endpoint representatives, and the even/odd degree observation. These yield sixteen new contract rows, not sixteen new theorems.

The original formulas and classifications remain credited to the source authors. Remark 3.7's attribution of the earlier computer classification to Leemans and Vauthier is preserved, but that classification is not used as an input. Finite orbit decomposition, core kernels, wreath-product centralizers, sign characters and orbit–stabilizer arguments are standard mathematics. The repository's work is the explicit shared assembly, complete adapters and fresh finite certificates. This review makes no historical-priority claim for either the ideas or results.

## The shared finite-action theorem

All of the added K(e), its proof and its actual application interfaces were read. Its transitive-orbit classification is the usual stabilizer classification: a point with stabilizer H identifies its orbit with G/H, and conjugate stabilizers are precisely the equivariantly isomorphic transitive actions. The action kernel is the intersection of their cores, so this is a valid extension of K(c), including nonfaithful actions.

The centralizer formula is correct for the permutation image even when the original action is nonfaithful. An equivariant permutation may only exchange isomorphic orbits; within one orbit its value at H lies in N_G(H)/H. The possible opposite-group convention is explicitly resolved by inversion, and the independent choices and exchanges give the stated wreath product.

The normalizer formula requires and has faithfulness. More explicitly, if a normalizing permutation t induces the automorphism alpha by `t rho(g) t^-1 = rho(alpha(g))`, the stabilizer of t(x) is alpha(G_x). Consequently its multiplicity vector is invariant under H -> alpha(H). Conversely, pair an orbit with stabilizer H to one with stabilizer alpha(H), and define `t(gx) = alpha(g)y`. This is well-defined and invertible. It proves surjectivity onto the displayed multiplicity stabilizer, not merely an inclusion. Replacing alpha by its inverse in a twist convention gives the same stabilizer. No splitting of the normalizer sequence is claimed or needed.

For an elementary abelian 2-group, an element outside H acts on G/H by [G:H]/2 transpositions. Only index-two stabilizers contribute a nontrivial sign; their unique nonzero characters sum as stated. This proves the evenness criterion rather than testing it on a few matrices.

The invariant-fiber orbit bijection is also correct without a surjective projection or faithful object action. Move an extension's base configuration to an orbit representative, then use precisely that representative's stabilizer. In the J1 application the rigorous extension object is a pair `(S,b)`, where S is an old marker set and b is the additional involution. Projection to S is equivariant. The subsequent map to the unlabelled set S union {b} can have multiple preimages, which is why the existing global deduplication remains necessary. The application does not assume that an unlabelled extended set has a uniquely designated old subset. The old subgroup-table completeness and geometric recognition are separately retained. In L066 the objects are an unordered endpoint pair together with a middle involution. These are two actual uses of the finite-action interface; K(e) does not make every earlier branch automatic.

## All-degree formulas

The complete Section 25 was checked against the primary statements and proofs. The multiplicities f,x,y,z,t respectively belong to stabilizers V, <a>, <c>, <ac>, and 1. Faithfulness is exactly t>0 or at least two of x,y,z positive. End reversal exchanges x and y. The two sign coordinates are x+z and y+z, so both endpoints are even precisely when x,y,z have the same parity.

The coordinate change in CPI3 is a genuine bijection. Commutation preserves the support of a. On regular four-point orbits, both a and c have two transpositions; on the two-point <ac> orbits both have one; and on <c> orbits only a has one. Thus k=y+z+2t and l=z+2t. The inverse y=k-l, z=l-2t and f=N-2(x+k) has exactly the listed nonnegative ranges. For k>=1 the only nonfaithful possibilities are c=1 and c=a, so exactly two choices are removed for each k.

Pairing consecutive even and odd values of l gives lambda(k). Reversal fixes an ordered class exactly when x=y, which is equivalent to equal endpoint cycle counts. For fixed k this forces x=k-l and gives the lower bound l>=max(0,2k-n). The omitted initial sum is the displayed psi(k,n); its two cases follow from the parity of 2k-n. Subtracting c=a gives D(k,n). The usual involution-orbit count `(all + fixed)/2` therefore produces the source's entire symmetric formula.

For even endpoints, k is even and x+l is even. The even-l and odd-l sums give exactly gamma(k) and delta(k), with the two removed choices both even. Counting fixed classes with even k gives the stated alternating formula. The ambient equivalence is explicitly handled: these are S_N-conjugacy orbits of pairs in S_N or A_N. The nonexceptional theorem that every relevant ambient automorphism is induced by S_N conjugation remains a named input. No false identification with conjugacy inside A_N is used. The n=2 boundary, namely groups of degree four and five, is included in that retained theorem.

Adding or removing one common fixed point gives the even/odd degree bijection. Every nontrivial V-orbit has even size, so odd degree guarantees such a point. The exceptional ambient automorphisms at degree six are separately treated and not transferred to degree seven.

Both rational expressions in CPI10 were also checked as formal generating series. Writing y=x+d gives weights 2,1,1,2,1; subtracting the t=0 actions with at most one nonzero coordinate gives `(1+v)/(1-v)^2`. For even endpoints the shared odd shift contributes v^3, and the remaining weights are 4,2,2,2,1. The nonfaithful subtraction is `(1+v^2)/((1-v)(1-v^2))`. These derivations prove the identities uniformly; numerical coefficient agreement is only supplementary.

The centralizer propositions are derived directly from K(e) for C2. A flip on any two-point orbit is odd and centralizes the involution, so the alternating centralizer has index two and the displayed order. This also proves the nonsplitting of each single-involution class, without using it as an unsupported assertion about simultaneous pair conjugacy.

## Exceptional census and independent computation

All three added mathematical programs, the builder, verifier, runner, controls and new ledger entries were read completely. Fresh optimized author structure, mathematics and controls pass. The author's census uses every commuting endpoint pair and then every stabilizer orbit of middles; this is complete by K(e). The exact action sorts endpoints and acts on the middle, which identifies precisely automorphism equivalence with endpoint reversal, the required duality. Generation and all 64 ordered subset meets are tested for every generating orbit. Neither the source list nor a published polytope classification filters that search.

The independent program here uses a different enumeration order. It first visits every raw unordered-endpoint/middle combination and tests generation, with no automorphism or stabilizer reduction. For every generating raw triple it checks every one of the 64 subgroup meets. Only after these tests does it quotient the complete surviving list by the full automorphism action with endpoint reversal. Its exact results are:

| Group | Raw combinations | Generating raw triples | Actual IP meets | Automorphism/duality classes | Class sizes |
|---|---:|---:|---:|---:|---|
| S6 | 37125 | 2160 | 138240 | 2 | 1440, 720 |
| A6 | 4050 | 0 | 0 | 0 | none |

The S6 classes have unordered adjacent orders {5,6} and {6,6}. Every generating raw triple has IP. The full endpoint census independently recovers 495 S6 pairs, nine S6-conjugacy classes and five full-automorphism classes, with orbit sizes 45,90,90,90,180. For A6 it recovers 90 pairs, two S6-conjugacy classes and one full-automorphism class. Both ambient automorphism groups have order 1440. The five primary representatives are then checked as a complete irredundant orbit list; only the second and fourth representatives have a generating middle, with sixteen raw middles each. Thus the primary representative list is an output comparison, not a completeness premise.

This independently establishes the exceptional statements and polyhedron classifications within the retained exact GAP algorithms and the string-C-group/regular-polytope correspondence. Both implementations use GAP's group, subgroup, intersection, automorphism and orbit algorithms; the independent program is not an independent implementation of GAP itself. It does not use a small-group or polytope classification database.

A separate independently written arithmetic checker enumerates 643914 ordered faithful multiplicity vectors through half-degree 40. It computes all ordered classes, reversal-fixed classes, even ordered classes and even fixed classes separately, checking the coordinate inverse and all fourteen source table rows. The author's separate program checks floor/rational agreement through half-degree 500 and 58450 coordinate instances. Neither bounded computation replaces the all-parameter proof above.

## Source boundaries and the corrected ledger

Source Lemma 3.3's conclusion is valid. Its printed inference from conjugacy of single second involutions to conjugacy fixing the first is not sufficient; the multiplicity classification provides the required proof. Remark 3.4 is accepted only as the endpoint-reversal statement. Equal-cycle endpoints alone do not specify a completed polyhedron or imply its self-duality: a suitable automorphism must also preserve the chosen middle. Theorem 4.4 is accepted in its section's regular-polyhedron context. Nothing here excludes arbitrary nonregular polyhedra with automorphism group A6.

Independent review found a genuine binding defect before admission. The original builder searched for a next heading starting one character inside the current `###` heading, causing its residual `##` prefix to match itself. Twelve new source spans contained only one hash. The other four ended before the body of the intended final subsection. In particular, the bindings for the two principal counting theorems omitted their exceptional-degree proof. The fresh original verifier returned PASS despite these defective but internally hash-consistent spans. That historical PASS is not treated as evidence of semantic coverage.

The additive phase116 correction was read completely and freshly replayed, including its controls. It preserves the manuscript, all 120 earlier contract rows and every new source statement. It changes the sixteen new intervals and adds explicit correction provenance. The independent checker here does not import the correction's helper functions or section map: it globally matches numbered headings and uses a separately transcribed source-to-section map. Every corrected interval includes the whole intended final subsection. All sixteen now pass, and the original ledger is rejected.

Seven independent semantic controls reject the original ledger, a one-character span, a truncated final subsection, a wrong but complete subsection, an altered retained contract, a demoted principal theorem, and a divergent printed executable. In the three mutated-span cases the internal SHA256 is recomputed, so rejection is semantic rather than merely a stale hash. A fresh-output refusal preserves an occupied directory and sentinel. The root correction's separate fresh controls reject the original and two altered ledgers and preserve six occupied targets, including dangling symlinks. The original author's four refusal and seven bound-input mutation controls also pass, but those checks did not discover the original semantic defect.

## Continuity, portability and limits

Every one of the 120 predecessor source-adapter proof spans is byte-identical, and every retained row's mathematical content is unchanged. Twenty-three complete old proof sections and all eight old executable appendices are byte-identical. The newly read interfaces include K(c), K(d), the geometric recognition convention, the J1 extension application, the added K(e), all of Section 25, Corollary CP and the changed cost/source-boundary text. Acceptance of the other unchanged mathematics is explicitly inherited from phase87 and its predecessor review chain; this task did not reread every earlier source or rerun every old mathematical program.

The continuous candidate contains 27 numbered sections, eleven full executable appendices and 136 contract rows. The complete 351348-byte text remains necessary for this verdict, including all code and earlier adapters. This is a reviewed thirteen-source principal contract under named retained inputs, not a dependency-free derivation of every sentence in thirteen papers. It adds no open-conjecture result and no new Lean theorem. Earlier scoped Lean results retain their existing meanings. No thirteen-source length factor has been measured, and the twelve-source ratio cannot be transferred.

The independent checker also passes from an isolated 40-file nonprimary snapshot containing exactly the original author exports, three retained public predecessor bindings, the seven correction exports and these three review programs. Default replay needs no private primary capture. `--primary-check` additionally verifies the three privately bound primary assets; the reading record states separately what was actually read. The independent raw-census output is identical between the full and portable replays. No PDF, full-text source or primary raster is distributed.

Use fresh output paths from a directory containing the distributed files:

```text
python3 -B -O phase114_commuting_pairs_review_check.py --output-dir NEW-review
python3 -B -O phase114_commuting_pairs_review_controls.py --output-dir NEW-controls
python3 -B -O phase116_commuting_pairs_correction.py --output NEW-ledger-check.json
```

The review manifest binds this audit, its structured verdict and reading record, all review programs, fresh author and correction replay records, fresh independent full and portable reports and logs, and semantic controls. Public admission is root's subsequent action. The original defective ledger remains a clearly identified historical artifact; the phase116 corrected ledger is required for any admission claim.
