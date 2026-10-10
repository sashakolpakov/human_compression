# Common-fiber monodromy obstruction: formal scope

This module is an algebraic companion to the written graph-cover theorem in `phase28_voltage_shadow_theory.md`. It uses arbitrary groups and an arbitrary indexed family of subgroups; finiteness, commutativity and normality are not assumed.

For subgroups S_i and shifts g_i, `CommonFiber g S` is the explicit set of points x satisfying g_i⁻¹x∈S_i for every i. Given a chosen common point z, the module checks:

1. `common_fiber_rebased`: x belongs to the common fiber exactly when z⁻¹x belongs to the subgroup intersection ⋂S_i.
2. `common_fiber_eq_coset`: the corresponding equality of sets, expressing the common fiber as z(⋂S_i).
3. `same_monodromy_class_equivalence`: the relation x⁻¹y∈H is an equivalence relation for every subgroup H, without assuming H is normal.
4. `common_fiber_one_class_iff`: assuming H≤⋂S_i, every two points of the nonempty common fiber are related exactly when H=⋂S_i.
5. `monodromy_defect_witness`: any k∈(⋂S_i)\H gives two explicit common points z,z·k in different classes.

The graph-cover application sets H equal to the common-shadow monodromy subgroup and S_i equal to the individual-shadow monodromy subgroups, all based at one vertex. The written walk-lifting argument identifies connected components on that fiber with the relation x⁻¹y∈H. That identification is an explicit external mathematical step, not a Lean graph theorem hidden behind the name `SameMonodromyClass`.

Not formalized here: graph covers or voltage assignments; their path-lifting and monodromy correspondence; typed coset Helly; the incidence construction; chamber extension or connected truncations; the full geometric recognition theorem; or the number of components as an index/cardinality. The module checks the nonempty-fiber subgroup obstruction after those data have been supplied.

The pinned Lean 4.32.2 compile passed. Four theorems use only `propext`, `Classical.choice`, and `Quot.sound`; the equivalence-relation theorem uses only `propext`. The standard classical axiom enters through the subgroup-intersection library interface. There is no `sorry`, `native_decide`, numerical lookup or additional axiom. The saved report contains all five printed axiom lists and binds the exact source hash.

Reproduce in the private workspace with:

    python3 research/leemans/formal/verify_lean.py Phase29CosetMonodromy.lean

The existing runner reads its pinned, already-built dependency checkout. No public or previously frozen formal files were changed. The `.olean` file is a generated build product and is excluded from the original-file manifest.
