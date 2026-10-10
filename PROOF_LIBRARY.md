# Reuse and honest compression measurement

The method adapts Alexander Kolpakov's
[GKM project](https://github.com/sashakolpakov/gkm): retain verified reusable
components, try their interfaces on new tasks, and refactor when new tasks
reveal shared structure. For mathematics a component is a proved theorem,
and an application includes proofs of every hypothesis. The original
working derivations supply material to rework; they are not the new
programme's product or comparator.

The mathematical output is a family of papers for each coherent topic.
Topic A has shared theory U_A and application papers A₁, …, Aₖ, matched to
historical papers LA₁, …, LAₖ. Each application provides complete hypothesis
checks and source-specific proofs in ordinary academic language. The intended
saving comes from shared mathematics, not abbreviated proof sketches or
omitted exceptional cases.

The [topic-complexity protocol](TOPIC_COMPLEXITY.md) distinguishes:

- An independent topic comparison: Σ c(LAᵢ) / (c(U_A) + Σ c(Aᵢ)).
  Topic B pays its full U_B too, even when U_A and U_B overlap.
- Conditional paper comparisons: c(LAᵢ) / c(Aᵢ), with the acquisition cost
  c(U_A) displayed separately and charged once within that topic.
- A separate chronological GKM account: charge each new application for
  its complete proof-dependency closure absent from the already paid library,
  including all new interfaces and hypothesis checks. This account records
  the actual library snapshots and does not reduce the independent topic costs.

The dependency graphs of the original papers and the replacement must both
represent genuine earlier reuse. A globally deduplicated storage inventory
is a different quantity from the independent topic comparison.

Specify source editions, target statements, retained background and
representation before comparing. Required proof
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

At each meaningful revision retain the exact task and target results and record:

- The full topic umbrella and the complete matched application costs.
- Gross new proof, interface, application and certificate material.
- Removed material, identifying which portion was repeated reasoning.
- Signed net change and the cost of genuinely new applications.
- Which earlier results still follow, and their exact proof/Lean status.

A shared body counts once within a topic; an overlapping umbrella remains
fully charged in each other independent topic. Each hypothesis check and
binding counts where used. Mere relocation preserves cost. Removing a lemma and breaking one
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
records the earlier GKM readings and the pre-reorganization state. It is
historical; its mixed compilation supplies reusable proofs. It is neither one
of the new topic papers nor one of the historical papers being compared.
