# Phase177: source intake, bounded reconstruction, and two local corrections

This packet is private author evidence awaiting independent review and public
admission. It does not alter frozen phase172.

## Accepted author claims

* L059 has a complete written faithful-marking classification over a fixed
  connected ordered bipartite graph, invariant-column derivations, and a new
  exhaustive bounded census of 69 markings over five explicitly constructed
  graphs. A separate validator checks every coset incidence, subgroup and
  invariant, duplicate freedom, and complete subgroup-class coverage.
* The historical L059 census, including the printed totals 1,082 and 1,643,
  has not been recovered. Its full principal contract remains incomplete.
  The smaller census earns no substitution credit for the historical lists.
* The F010 manuscript gives written deductions of all three gadget theorems,
  the finite-pair theorem, and both principal examples. Its general claims
  are candidates for independent mathematical review, not Lean-certified
  theorem admissions. The finite-pair theorem was already proved in2025
  by Díaz Ramos, Molinier and Viruel.
* The completed hexagon in F010 Example5.1 has correlation/automorphism pair
  (D12,S3), not the printed (D12,C3). GAP computes both full finite groups;
  Lean proves an explicit type-preserving involution and the impossibility
  of a nontrivial involution in C3. This corrects the example's kernel while
  preserving its intended obstruction to naive completion.
* Lean separately proves the C4×C2² marked-factor counterexample to L059's
  assertion following Proposition13. The file proves factor cardinalities,
  trivial intersection, universal opposite-factor coset incidence, and
  impossibility of the marked swap. It does not formalize the graph census.

## Replay

Run phase177_check.py with --out pointing to an unused directory. The runner
refuses an occupied output directory. GAP and Lean executable paths and the
pinned package directory are configurable. The default environment is
Lean4.32.2, Mathlib905b95818eb32af7874a58b427f50c1711a5e96c, GAP4.15.1 and GRAPE4.9.3.

The accepted replay starts with fresh local copies and fresh local Lean
objects; it uses pinned prebuilt Mathlib dependencies. The build report
hashes all10 inputs, all seven logs and the complete GAP witness file.
The two Lean files print eight axiom reports, all using only the standard
axioms propext, Classical.choice and Quot.sound. No sorry, custom
axiom or native_decide occurs in the accepted sources.

Run phase177_negative_controls.py with --build pointing to the accepted
replay and --out to another unused directory for four rejection controls:
an incorrect tip reflection, the loss of the order-four factor obstruction,
a duplicate valid census row, and reuse of an occupied output directory.
Rejected mutant Lean files are not certificates.

## Trust and attribution

The bounded census trusts GAP's complete conjugacy classes of subgroups and
GRAPE's complete graph automorphism calculation. The validator recomputes
its columns by alternative finite tests, including all-element orders,
all conjugates and direct coset incidence. It is not an independently
verified implementation of either exhaustive backend.

The source graph/coset realization is classical Tits-style action theory.
The F010 gadgets and finite-pair theorem belong to the named source authors;
their graph encoding follows the Frucht–König tradition. The retained U/D
interfaces organize these arguments, and the new application pays its
recognition, equivalence and local correction arguments explicitly.

No compression ratio, new open-conjecture resolution, full L059 reduction,
or fully Lean-checked F010 replacement is claimed by this packet.
