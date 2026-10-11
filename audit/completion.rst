Completion of the closed corpus
===============================

The intake contains 161 indexed manuscripts, of which 102 were retrieved,
61 encoded and 48 had some results rederived. Within those sets, 27 have
admitted principal-result contracts. These counts are nested, not additive.
A contract records the particular conclusions recovered, including any
corrections and exclusions; it does not assert recovery of every sentence
of a source paper.

The independent `completion audit <completion.json>`_ examines those 27
contracts at commit ``d87957689d6455f2eca8568c4a667bd32ce0047e``. It resolves
later admissions before interpreting older registry fields and binds 187
proof, program and provenance artifacts to their Git contents. It is an
audit of scope and remaining work, not a new proof review of all 27 results.
The original registry and admission records remain unchanged.

At that baseline, five contracts had complete canonical TeX applications
with their common theory: L032, L009, L083, L079 and L021. The other 22
had accepted proofs in earlier combined manuscripts or individual proof
packages. They need complete topic editions. This distinction concerns
publication and measurement; it does not withdraw their mathematical
admissions. Topic E alone had a complete current comparison of both the
written manuscripts and the paired proof graphs.

Work by topic
-------------

The following division covers every admitted contract exactly once. Topic
boundaries remain subject to the actual mathematics: grouping papers by
subject does not itself prove a compression theorem.

.. list-table:: Complete source contracts to be preserved
   :header-rows: 1
   :widths: 34 26 40

   * - Topic
     - Sources
     - Remaining work
   * - E: Projective centralizers, polytopes and maniplexes
     - L083, L079, L021
     - Current common proof, applications and measurement are complete
       within the stated scope. Full source formalization remains separate.
   * - A: Supported kernels and two-group polytopes
     - L032, L034, L035, F013, F016, N009
     - Complete six applications and their common theory; preserve the
       classification, census, geometric conclusions and required programs.
   * - Affine lattices and mixed-prime polyhedra
     - L012
     - Prepare the complete accepted proof in TeX and include its actual
       Topic A, equal-label and cubic-lattice dependencies.
   * - C: Halving, parity and Petrial operations
     - L088, N013, L108, F014
     - Assemble common operation theorems and four full applications,
       including the toroidal geometry and finite census.
   * - B: Forest coordinates and primitive coset geometries
     - N001, N003, N008, L030
     - Separate the common forest and flag arguments from four complete
       applications, retaining the graph reconstruction proofs.
   * - D: Marked actions and geometry enumeration
     - L066, L074, L104
     - Complete the common enumeration arguments and all three
       applications, with their algorithms and exact census scope.
   * - G and incidence residues: Flag relations and Steiner geometry
     - L009, L092
     - Preserve the current G papers; assemble all accepted residue proofs,
       corrections and exceptional-group data for the second application.
   * - F: Odd kernels and cyclotomic polyhedra
     - L014
     - Prepare the complete existing proof in TeX, including the exact
       presentation and cyclotomic calculations.
   * - Recognizable incidence extensions
     - F010
     - Assemble the full construction and reconstruction criterion,
       including its gadgets, connectedness and arbitrary-rank arguments.
   * - Chamber orbits and regular covers
     - L008, N016
     - Prepare complete applications with the marked-inversion argument
       and every required family and finite example.

Measurement and formal proofs
-----------------------------

Each topic will report the sum of its historical manuscript costs divided
by the cost of its entire common theory and all complete applications.
It will also report each source/application ratio after that common theory
is available. Independent topics each pay their whole common theory, even
where they overlap. Required programs are separately inventoried and
included in the corresponding sensitivity calculation.

N001 and L108 were read through complete authored text renderings, but
their original PDFs are missing from the measurement corpus. Those PDF
costs remain unknown. An alternative transcription comparison would need
its own explicit, calibrated protocol; neither source can be assigned
zero length.

All 27 contracts currently have partial formal coverage. The available
Lean files prove specified supporting statements; no complete source
contract is asserted here to have an end-to-end Lean proof. Each new
edition must map declarations to its written lemmas and retain the exact
unformalized hypotheses and geometric steps. The formal library can grow
without changing a source contract's completion status automatically.

Answers to source questions, unfinished carry-over investigations and
qualified components stay outside this principal-result numerator. F015,
L028 and the remaining minimal-cover cases retain their separate review
or research obligations. Intake remains closed.
