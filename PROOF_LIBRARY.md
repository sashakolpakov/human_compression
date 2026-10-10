# Reuse and honest compression measurement

The method adapts Alexander Kolpakov's
[GKM project](https://github.com/sashakolpakov/gkm): retain verified reusable
components, try their interfaces on new tasks, and refactor when new tasks
reveal shared structure. For mathematics a component is a proved theorem,
and an application includes proofs of every hypothesis. The original
working derivations supply material to rework; they are not the new
programme's product or comparator.

The mathematical output is U plus coherent application manuscripts.
U contains full general proofs. A module cites them and provides complete
application proofs and source-specific arguments in ordinary academic
language. The intended saving comes from shared mathematics, not
abbreviated proof sketches or omitted exceptional cases.

For a source bundle S_A, the conditional module factor is

    R_A = sum of comparable source lengths in S_A / length(A), conditional on U.

For several modules, the total factor is

    R_total = sum of lengths of distinct sources / (length(U) + sum length(modules)).

Source overlap is counted once. Specify source editions, target statements,
retained background and representation before comparing. Required proof
appendices, source-specific lemmas and certificate interfaces must be
included; separately report complete reproducibility artifacts and execution
requirements. Report page and normalized text counts under a common format,
with sensitivity to the counting convention. A nominal 20-page file is
not evidence of a saving if its necessary proof is hidden elsewhere.

The source-side observable is the length of the published derivations
under those explicit boundaries. It is not an estimate of their authors'
intelligence, historical effort, or minimum possible proof complexity.
Their use of earlier theorems also belongs in the dependency accounting.
Bibliographic repetition alone is not a theorem-reduction result.

At each meaningful revision retain the task contract and record:

- The complete U-plus-application cost for that contract.
- Gross new proof, interface, application and certificate material.
- Removed material, identifying which portion was repeated reasoning.
- Signed net change and the cost of genuinely new applications.
- Which earlier results still follow, and their exact proof/Lean status.

A shared body counts once; each hypothesis check and binding counts where
used. Mere relocation preserves cost. Removing a lemma and breaking one
derivation demonstrates that derivation's dependence, not necessity for
all possible proofs. A prospective application tests actual reuse beyond
the examples that motivated the theorem. Both large savings and expansion
are reported. The sawtooth shape is an empirical outcome to look for,
not a success label attached in advance.

The [GKM transfer protocol](https://github.com/sashakolpakov/gkm/blob/main/transduction/TRANSFER_VALUE.md)
provides the acquisition-plus-application discipline. Its program-level
complexity units and experimental outcomes are not imported as mathematical
proof measurements. Categorical language also needs its own mathematics:
a group pushout requires a specified diagram and a proved universal
property. Shared text or a dependency graph alone is not a pushout theorem.

An independent [earlier method and intake audit](research/case_study/phase121_gkm_proof_library_note.md)
records the precise GKM readings and the pre-reorganization state. It is
historical: the latest working compilation has thirteen source contracts,
and the present deliverable is U plus modules. Its stale registry cache
was corrected by regenerating the living map.
