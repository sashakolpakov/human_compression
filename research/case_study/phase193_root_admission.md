# Root admission of the finite normal-pair representation contract

Date: 2026-10-10. This admits F010's complete written principal-theorem
contract, with three explicit local source qualifications. It does not
admit the unrelated L059 census contained in the same historical author
checkpoint.

The source is Antonio Díaz Ramos, Rémi Molinier and Antonio Viruel,
*Every finite group is represented by a finite incidence geometry*,
arXiv:2511.02410v2, 16 December 2025. The thirteen-page primary PDF has
SHA256 `a8ff604a96a57ab8baf20aaa808a90308c01237ab0607a1062207fcb49f736e7`.
The finite normal-pair theorem, three explicit constructions and symmetric
family belong to these authors. F010 is an independently authored followup
in the fixed inventory, not an original L-series paper or a new conjecture
solution by this project.

## Accepted proof and source contract

The manuscript states one restriction-and-extension lemma: intrinsically
recognize the original vertices, prove pointwise rigidity of the extension,
extend every original correlation, and identify the type-preserving
kernels. All four obligations are paid in each of the three constructions.
The lemma is fully proved locally. Its connection to U.Action is a
conceptual reuse, not an unproved hypothesis imported from the source.

In the ordered-pair encoding, original vertices have degree at least four.
Each ordered pair has an intrinsically recognized outgoing degree-two
vertex and a chain whose length records the group-element label. Thus
every graph automorphism preserves every directed label and is a right
translation. The inverse in the translation parameter gives a homomorphism
under usual permutation composition. Normality of H makes the coset
colour action well-defined, with kernel exactly H.

For chamber completion, every new vertex belongs to a single edge chamber.
Triangle-freeness handles flags on original vertices. The degrees r−1
and d(v)(r−1) distinguish the two sets of vertices, and the old endpoint
pair and colour uniquely determine each new vertex. The case r=2 adds
nothing and is included. For cleaning, the two larger, unequal new colour
classes identify the old vertices. Common new neighbours recover old
edges. Each attached component has a recognizable old boundary and a
rigid root; the proof uses induced-gadget degrees at the branching points,
including the isolated-vertex case M=1. These facts establish the exact
pair isomorphisms without assuming away extra automorphisms.

Consequently Theorems 3.1, 4.1, 4.2 and A are recovered with their conclusions
unchanged. The main construction is connected, of rank [G:H]+3 when G is
nontrivial. The trivial case is a single vertex of rank one. The theorem
requires H normal in G and does not prescribe a fixed small rank. The
cleaning operation by itself preserves connected components; it does not
connect an arbitrary disconnected input.

The recursive symmetric-group family is also proved for every n≥2,
including its exact colour counts and faithful natural top action. Even
coset representatives make all local permutations induce the same colour
permutation. To exclude additional correlations, the proof identifies the
top class, the pair vertices, and the connected interiors of attached
copies from their distinct fixed boundaries. This completes the required
induction rather than relying on a finite list of examples.

Three qualifications are retained: the chamber-degree formula in the
source proof has an offset; the completed hexagon has type-preserving
group S3 rather than C3; and minimum degree two in the recursive family
starts at n=3, not at the four-vertex n=2 path. The hexagon still demonstrates
that naive completion can enlarge the correlation group. It does not
prove the informal claim that every hypothesis is universally optimal.

## Primary reading and independent review

Root read the entire extracted thirteen-page primary text, the full
replacement proof, source contract, independent review, complete finite
programs and local Lean file. Root visually checked primary pages 5, 9, 10,
covering the directed-label encoding, cleaning construction and completed
hexagon. The independent phase188 reviewer read every primary page and
visually inspected pages 5, 7, 9, 10, 11, 12, including both recursive examples.
Its review of all universal proof blocks found no unresolved mathematical
obligation in the declared principal contract.

Root verified every frozen author export and retained-input binding in
the private checkpoint, then every independent-review binding. Publication
copies only the F010 application files and phase188 review. The historical
phase177 manifest also describes L059 artifacts and primary PDFs which
are not included by this export. Its review-pending status is historical;
the later phase188 acceptance and this admission supply the current state.

## Fresh public execution and formal boundary

The original phase188 runner verifies the whole private author checkpoint.
The new `phase193_public_check.py` adapts its input binding to the selected
F010 sources and records GAP/GRAPE versions. Its mathematical programs,
Lean source and four changes tested for rejection are unchanged. No
private primary PDF or L059 data is required by the public command.

The fresh run checked all 25 properly coloured graphs on at most three
labelled vertices up to colour renaming. Cleaning and completion preserve
both groups under their actual restriction maps in those cases. It also
checked all seven normal pairs in C2,C3,S3, including equality with the
prescribed right-regular actions, and completion of the four C2/C3 pairs.
The S3 completions are not part of this bounded run. The separately proved
general theorem supplies their conclusion. The independent recursive
models for n=2,3,4,5 have 4, 12, 46, 225 vertices and the expected full Sn/An
top actions. These finite examples do not prove the universal statements.

The exact initial and completed hexagon groups are respectively (S3,C3)
and (D12,S3), with D12 of order twelve. Lean proves an explicit
adjacency- and colour-preserving involution in the completed graph, and
the absence of a nontrivial involution in C3. All four named reports use
only `propext`, `Classical.choice` and `Quot.sound`. The full geometry
automorphism-group identification and universal construction are not
formalized by this local certificate.

Four altered cases are rejected: deleting an asymmetric cleaning edge,
collapsing ordered-pair labels while retaining the rigidity test, imposing
the wrong completed-hexagon kernel, and changing the tip reflection.
The GAP controls require the expected error and absence of the success
marker, because a batch error can return process code zero. The positive
graph, hexagon and Lean logs match the independent review byte for byte.
The wrong-tip log has a different scratch path; its compiler rejection
is recorded directly in the fresh report.

Observed positive-run times are 4.166s for the bounded constructions,
0.660s for the hexagons and9.296s for Lean; these are not complexity bounds.
The environment is GAP 4.15.1, GRAPE 4.9.3 and Lean 4.32.2 with all pinned
dependency revisions and tracked-file cleanliness checked. GAP/GRAPE's
exact algorithms and cached compiled Lean dependencies remain trusted.

## Attribution, cost and coverage

The theorem, three constructions and explicit smaller family are borrowed
from the source; its Frucht–König antecedents remain attributed. The
restriction-and-extension criterion is elementary, not claimed as new.
The manuscript makes its applications explicit, supplies the component
recognition in the recursive proof, and preserves the local corrections.
No correction priority or new open-conjecture resolution is asserted.

The written application costs 21,870 raw UTF-8 bytes. The actual public
application, two finite sources, local Lean source and portable driver
cost 42,343 bytes; charging the full 61,576-byte umbrella gives 103,919.
This replaces the frozen review's private driver in its 40,820-byte
inventory. The old driver remains review support. The source's thirteen
pages and these raw byte counts are different units: no matched ratio,
fixed-coverage decrease or new sawtooth step is claimed.

The additive overlay raises encoded sources 56→57, known-result component
coverage 41→42, and principal-source contracts 18→19. It changes one
selected-section reading to a full-text reading, leaving 161 indexed and
102 retrieved works unchanged. The fixed A–D editions still cover 16
principal contracts. The new local Lean component brings the total to 72,
of which 71 have no native-evaluation axioms; the historical transfer
component retains its four explicitly recorded native axioms. No question
catalogue entry is added and no frozen registry is rewritten.
