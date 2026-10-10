# Independent review of Forest coordinates and primitive coset geometries

10 October 2026. **PASS for the exact four-source declared mathematical
contract, with the manuscript's explicit source corrections and retained
inputs.** No additional correction is required by this review. This is an
independent mathematical and source-scope review, not merely a comparison of
file hashes. The author manuscript is
`a18d09ae365f7a05df828652de249046be4460e434cf787a98d568ca53191b86`;
the author manifest is
`9b2f173d8430582d8072d02532b4206c1e15c1dac1bdb8edc7f542bff7e89164`.

I read the entire manuscript, the statements and full proofs of all six used
U-v2 results and their necessary surrounding definitions, the full available
mathematical texts of the four source versions, all30 source contracts and
their22 proof-node mappings, and the integrity, checkpoint and rendering code.
The frozen author files were not modified.

## Mathematical judgment

The four final source corollaries follow from the proved U interfaces and
the complete application arguments in B. The central reuse is substantive:
unit-weight trees, the contraction/sign construction and weighted stars share
the same forest subgroup computation and flag-completion proof. The Frattini
branch uses a different proved U interface and supplies its actual geometric
hypotheses. The manuscript does not pretend that these classification and
generation obligations follow from forest terminology alone.

**Forest coordinates and flags.** The component-partition argument computes
the actual intersection of the symmetric subgroups. Unique paths are essential
to identify the common refinement with the common-edge forest. Nonempty vertex
blocks make distinct edge sets give distinct groups. The proof of flag
completion separately uses laminarity: prescribed pairwise intersection
cardinalities force the same nesting and disjointness relations; subtraction
of maximal selected children yields equal-sized atoms and one common
permutation. This establishes the coset intersection condition for every
partial flag. The residue decomposition correctly retains kernels contributed
by isolated weighted vertices.

**Sign marking and property tests.** The even-word decomposition proves the
whole sign kernel, including the empty-support case. Intersecting its profiles
gives full marked independence. The two-block overgroup proof handles unequal
blocks, singleton blocks and the balanced exception separately. A balanced
edge is unique under positive weights. These statements give the primitive,
quasi-primitive and residual tests, with the rank-one boundary included.
The diagram-recognition construction is a tree: a longer shortest cycle
would violate the induced-cycle condition, while a triangle would violate
unique maximal-clique membership. The retained B97 uniqueness then applies
to the constructed geometry; it is not used to assume the four targeted
property conclusions.

**Symmetric-group recognition and counts.** W1 and W2 are separate retained
inputs. The two-point-block obstruction correctly obtains the strict module
generator bound and, in the equality case, forces the full symmetric block
action before using its even-weight module. Chosen crossing edges are
distinct and acyclic, so they form a spanning tree. Every intransitive
omission group has exactly the two corresponding component orbits. Taking
the cut intersections identifies the generators themselves, including the
unique possible alternating omission. For relative independence, a pendant
point stabilizer forces B to fix a point, which excludes an interchange of
balanced halves. The common omission intersection is therefore trivial.

The enumeration distinguishes three genuine conventions. Actual ordinary
sets recover their trees. Actual twisted sets recover a unique transposition
and a canonical distinguished-edge tree; replacing a three-cycle by its
inverse switches only its attachment across that edge. After identifying
those inverses, contraction leaves a tree on n−1 labelled blocks. Thus the
three displayed counts count their stated objects, not conjugacy orbits.

**Maximum-rank geometry recognition.** The sign construction's cut cosets
have a common representative by the weighted forest theorem, and the retained
odd transposition adjusts parity without changing them. The RWPRI proof
checks both the product-component projection and the final alternating
component, including A3. In the converse for arbitrary maximum-rank coset
geometries, the possible unordered balanced-cut enlargement is not silently
discarded: every panel containing it also contains another cut stabilizer,
which forbids swapping the halves. All panels therefore agree with the
marking, and (G2) supplies all remaining parabolics. The degree n≥7 condition
is used and retained. The action-isomorphism convention explicitly retains
innerness of symmetric-group automorphisms in this range.

**Relative generation and Frattini coordinates.** B.Flags proves flag
transitivity from residual weak primitivity in finite rank. Firmness then
supplies every required distinct intersection and panel choice. These are
the exact hypotheses of U.Relative; no extra finite-group assumption is
needed for that generation formula. The normal-quotient numerical bounds
are separately restricted to finite groups.

U.FrattiniLadder is applied with a finite maximal chain and the entire family
of distinct intersections, not with an arbitrary maximal chain alone. Its
upward argument uses normality and distinctness to exclude equality at each
step. Relative finite generation supplies the maximal overgroups through
Zorn's lemma, so the argument remains valid for an infinite group. The
Prüfer-group counterexample correctly disproves the unrestricted infinite
converse for generator transport. It does not contradict the geometrical
Frattini containment theorem, which has stronger structural hypotheses.

For a finite p-group, the elementary abelian Frattini quotient makes B normal.
Relative independence then makes the panel images a basis of P/B, identifying
every parabolic and every coordinate assignment. This proves the direct-sum
geometry, RPRI, chamber-regular translation action and the count of indexed
subgroup families. It does not identify that translation group with the full
type-preserving automorphism group for p>2, or identify indexed families with
automorphism orbits. The residue Frattini test is correctly a necessary test;
it does not use a false general inclusion between subgroup and ambient
Frattini subgroups.

**Kneser parameters and full graph automorphisms.** The weighted star has
positive central weight n−2k. Its panel size is exactly binomial(n−k,k), so
the sole thin case is k=1,n=3 and all other admitted parameters are thick.
The two-step replacement argument proves both lower bounds and constructions
for the exact parity distances. The common-neighbor formula and explicit
six-cycle establish the gonality, including k=1; the odd closed-walk argument
establishes odd girth. Diagram order is panel size minus one.

For typed automorphisms, common-neighbor maxima recover Johnson adjacency.
The maximal-clique proof distinguishes larger stars from smaller tops under
N>2k; induction recovers the unique ground-set permutation. Distinct
disjointness neighborhoods force the same permutation on all types.

The uncolored graph argument is complete. The indicator filtration exhausts
the entire real function space, and its successive scalar actions account for
all eigenvalues, without assuming that every quotient has positive dimension.
The strict inequality N>rk isolates the least eigenspace as the type-constant
sum-zero vectors. Equality in the independent-set bound then identifies
exactly the type classes. This closes the potential gap between typed and
uncolored automorphisms. In particular the63-vertex construction has full
graph group S7×S3, of order30240. It is not merely asserted from its evident
permutation subgroup.

## Exact source coverage

| Source version | Contracts reviewed | Result and boundary |
|---|---:|---|
| N001, Buekenhout–Cara1998, complete browser-rendered authored text | A1–A4 | All four clauses of Theorem1 follow from the unit-tree model and retained B97. “Middle” characterizes failure of PRI; QPRI itself also holds in the primitive cases. Original PDF unavailable. |
| N003, Cameron–Cara2002, complete12-page author manuscript | B1–B8 | Extremal markings, three counts, strong/relative independence and all maximum-rank geometries are recovered for n≥7. Numerical invariants are used in finite-group scope. Small-degree exceptional remarks and general open directions are excluded explicitly. |
| N008, Archer–Cara–Krempa2005, complete9-page published version | C1–C11 | Full geometric Frattini and finite-p-group conclusions, subsidiary facts and residue/kernel tests are recovered. The unrestricted infinite generator converse is corrected, with its counterexample. Gaschütz and Archer's quoted earlier theorems remain attributed background, not newly rederived targets. |
| L030, Garcia-Colin–Leemans institutional revised10-page manuscript | D1–D7 | Main construction, actions, diagram and displayed corollaries are recovered with corrected panel order, thin boundary and the specified graph's full group. This does not assert that no other locally Desargues graph has full group S7. |

For L030 I additionally viewed the actual primary-page rasters2,6,7,8. They
confirm that the accessed source prints the incorrect binomial order,
unconditional thickness and the stated graph group. I do not infer identity
with a publisher PDF or the earlier arXiv numbering. For N001 I read the
entire available authored browser text, including its diagram-recognition
input and proof discussion; damaged diagrams and unavailable original PDF
remain limitations. N003 and N008 were read in full extracted text. This
review does not claim a fresh visual inspection of every source PDF page.

The retained inputs are meaningful: B97 supplies classification and uniqueness
of inductively minimal geometries; W2 retains its classification-dependent
omission result; W1 gives the extremal-size bound and implication toward
generation. The general source coset criterion, Cayley, inner automorphisms,
the elementary abelian Frattini quotient and Zorn are also retained. Their
original proofs are not charged as newly supplied here. None is the same
conclusion as the four final application corollaries being recovered.

## Fresh execution and independent finite checks

The exact portable checker passed in an isolated tree containing only its
26 bound exported/shared files, under optimized Python. No primary source
or unlisted project proof was available there. It checked21 author files,
four shared inputs,22 proof nodes,30 source rows and the stated accounting.
A separate private run checked all30 primary anchors and every declared
visual-asset hash. These are documentary checks, not substitutes for the
mathematical reading above.

The new independent standard-library checker imports no author code or
reports. Its bounded diagnostics passed:

- 15 Kneser bipartite doubles, with all29,086 ordered parity-distance pairs,
  common-neighbor counts, diameters, four-cycle criteria and panel sizes.
- Three positively weighted trees, with144 exact subgroup intersections and
  all579 partial flags compared with actual permutation images.
- The63-vertex graph, with exact rational row reduction giving eigenspace
  dimensions20:1, −10:2, −8:6, 4:12, 2:14, −1:28. Two independent type-
  difference vectors span the least eigenspace. Every vertex link has the
  literal20-vertex, degree3 bipartite Kneser model.

The graph computation is not a full automorphism enumeration; the full group
is proved by the reviewed intrinsic reconstruction argument. Nor do the
finite checks extrapolate to arbitrary parameters. Existing-output refusal
preserved the original report, and separate mutations of the application
proof, shared proof, intake, checkpoint and checker itself were all rejected.
All isolated input bytes were restored and checked unchanged.

## Presentation, cost and admission limits

The authored PDF has16 ordinary A4 pages at11pt with one-inch margins. I
viewed authored pages1,7,12,16, which are legible and have ordinary continuous
mathematical exposition; I do not claim a new all16-page visual review or
fresh rendering. The author's all-page review and rendering artifacts remain
separately bound. The renderer's math, table and code AST comparisons were
read; the documentary replay verifies their frozen artifacts.

B has64,827 UTF-8 bytes and9,337 raw NFC whitespace tokens. The complete
retained U-v2 body has56,096 bytes, so the conservative full U+B total is
120,923 bytes. The6,399-byte subtotal of selected U statement/proof spans is
diagnostic only: it does not replace the charged U body and its context.
The arbitrary-parameter proofs require no external computational certificate.
The new finite reviewer checks are corroboration and review cost, not omitted
proof dependencies. No common source/replacement factor is measured here;
the damaged N001 transcription is not treated as a faithful source-PDF count.

This admits the exact four-source **corrected, declared main-result contract**
as corollaries of U+B. It does not certify every literal statement in all
editions, rederive the retained classifications, supply a full Lean proof,
solve an open conjecture or establish historical priority. It is an internal
independent review, not external peer review.
