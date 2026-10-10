# Formal and computational scope

The three declarations in `phase250_formal/PeriodSignObstruction.lean`
prove, in every group, the conjugacy of the actual two source period
words, the power collapse caused by equal signs under the stated
commutation hypothesis, and their direct composition for the literal
source words. They quantify over all natural period parameters. Fresh
compilation reports only standard Lean axioms. They do not formally
prove the full affine recognition theorem, all positive constructions,
Burnside's theorem, Lucchini's theorem or the catalogue classification.

The exact affine checker proves a fixed integral lattice identity and
checks the finite overlap profile used in the written all-period proof.
GAP rewrites the actual index-48 abstract presentation kernel and proves
it is free abelian of rank three; an abelianization alone would not
suffice. The retained {6,6} kernel uses the same distinction. Their
Reidemeister–Schreier/Tietze algorithms are trusted executable inputs.

The nonexistence base exhausts all 20,169 groups of order 384 in
SmallGroups 1.5.4, then all required involution pairs up to the stated
conjugation reductions. It finds no generating triple with adjacent
orders 6 and 16 and commuting endpoints. A positive seed passes the same
search. Completeness of the catalogue is retained; it is neither proved
here nor certified in Lean. Lucchini's original cyclic-core bound then
supplies the written descent for every larger exponent.

Controls check that raw unnormalized Schreier differences can lose a
lattice direction, that collapsing the affine translation part is
rejected, that the literal source sign gives the wrong order, and that
omitting the commutation hypothesis invalidates the sign theorem. The
legacy Python checker is staged, run with assertions enabled, and its
altered lattice assertion is rejected. These controls test relevant
failure modes; they do not turn bounded examples into universal proofs.
