Normal kernels and recognition of presentations

The written note is papers/formal/normal-kernel-recognition.tex (and .pdf).
It supplies one recognition argument and two exact presentation applications.
It is a supporting paper for the future complete Topic A volume, not a new
complete-source count or an independently measured replacement of F016.

The canonical Lean files are NormalKernelRecognition.lean and
NormalKernelProduct.lean in research/case_study/formal. From the repo root:

python3 -B -O audit/normal-kernels/check.py --source-dir research/case_study/formal --out /fresh/absolute/directory

The checker rebuilds both modules in dependency order. Use --lean and
--packages to supply the pinned compiler and an existing package cache.
It checks fourteen declaration reports and a finite counterexample showing
why kernel containment alone cannot prove the asserted product equivalence.
The dependency manifest fixes Lean 4.32.2 and the library revisions.
Existing compiled library objects remain part of the trust boundary.

The generic product map is multiplication of the actual local subgroups;
its equivalence preserves each original subgroup inclusion. The note's
source presentations, local normality and exact quotient identifications,
and the geometric correspondence retain written proofs. They are not
instantiated end to end by these two Lean files.

Recognition and product reviews are independent of their respective authors.
The author and review manifests preserve their original historical statuses;
admission.json records the accepted public edition and the exact source
bindings. No historical priority, new source or question credit, or new
compression factor is claimed for this supplement.
