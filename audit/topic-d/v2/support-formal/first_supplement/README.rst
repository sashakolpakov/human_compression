Exact-support counting in finite group actions
==============================================

This supplement proves the finite-poset Möbius indicator, its finite-set sum,
and the actual Burnside orbit count for the invariant subset of greatest
support. It also proves the stabilizer-fiber summand and its sum over an
arbitrary finite set of base representatives. Individual sublevel subsets
need not be invariant.

The complete statement ``UD.ExactSupportOrbits`` is covered. For
``UD.AdmissibleExtensions``, the actual fiber action and numerical summands
are covered; this first supplement does not identify the global quotient
with the disjoint union over a complete orbit transversal. That packaging
and every source-specific instance remain separate. See ``scope.json``.

Reproduction
------------

Supply Lean 4.32.2 and the package checkout/cache directory with the exact
revisions in ``dependency_manifest.json``::

  python3 -B -O check.py --out /fresh/output \
    --lean /path/to/lean --packages /path/to/.lake/packages

The runner checks pinned revisions, compiles this source and any absent
pinned dependency into fresh output, and reports each declaration's axioms.
Existing pinned package objects are trusted; this is not a full mathlib
rebuild. No compiled objects are distributed with this packet.

The fresh author replay passed twelve declarations with standard axioms
only, four rejected Lean mutations, and six finite validations/countermodels.
The finite computations do not replace the quantified Lean proof.
``author_replay/report.json`` and exact compiler logs record the run.

Attribution and scope
---------------------

The incidence inverse identity and Burnside theorem are classical results
provided by mathlib. This work verifies their composition with the actual
support subset and stabilizer-fiber actions used in the common Topic D
argument. It makes no priority claim, new source credit, conjecture credit,
or compression measurement. Independent review remains pending.
