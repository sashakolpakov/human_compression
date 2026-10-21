Ternary modules on the 105 flags of PG(2,4)
==========================================

This is an author-frozen bounded supplement awaiting distinct review. Read
``modules.pdf`` / ``modules.tex`` first, then ``source_map.json``, ``scope.json``
and ``formal_scope.json``. It covers L050 Theorem 1(a), Proposition 1,
Corollary 1 and Remarks 1--2, including both complete source tables. It is
not a whole-source admission or a compression measurement.

The common method is the same finite-field construction, full generated
matrix algebra, complete factor-Hom equations, and support-incidence
refinement used for the earlier 120/176 modules. ``reuse.json`` binds the
exact copied function bodies and the whole unchanged sparse enumerator.
The 45-dimensional factor uses a short rank-one algebra certificate;
there is no MeatAxe simplicity assertion in the final verification.

The other two 20-dimensional codes are proved to have distances 30 and 28
and exactly 672 and 720 minimum words. Each requires only the complete
583569-message search justified by the previously reviewed transitive
information-set theorem, followed by an invariant-orbit exhaustion proof.
The old complete 3^20 and 3^19 enumerations are retained, not rerun.
Their mathematical method and outputs remain dependencies in final assembly.

Replay
------

From an exact export-only copy, with NumPy, GAP and a C compiler::

  /Users/sasha/.venvs/global/bin/python -B -O check.py \
    --out /private/tmp/lcd105-new-replay --render

The output directory must not already exist. ``--study-root`` optionally
checks the original external source and prior acceptance bindings; it is
not needed to execute the self-contained finite certificate. ``--gap``,
``--cc`` and ``--pdflatex`` override tool paths. GAP errors are rejected even
when GAP exits with status zero. The full programs are supplied; no private
discovery output, source PDF, network resource or automorphism backend is
needed for this replay. GAP's standard exact group algorithms and named
PSL/dihedral groups remain trusted computational inputs.

The fresh result has ten controls: five weakened finite instances, one
false restricted minimum count, and four direct small ternary arithmetic
oracles. These controls are diagnostics, not mathematical premises.

Source qualifications
---------------------

The printed page-242 flag adjacency gives valency 8 under a conjunctive
reading or 40 under the all-disjunctive reading. Our explicit graph has
parameters (105,72,51,45). Identifying it with the source graph retains the
uniqueness theorem for its complement, exactly as attributed to Coolsaet,
source reference [6], Theorem 3. That primary is not newly acquired or
independently reproved here; parameter identity alone is not the claimed
identification argument.

The global minimal-dimension wording of Corollary 1 is false literally:
the full group has a nontrivial one-dimensional ternary character from
its index-two quotient. The valid local replacement and the source's
separate uniqueness claim inside this permutation module are proved.
No classification of all faithful irreducible modules or of all
20-dimensional submodules is claimed. Historical optimal-code-table
comparisons remain historical source assertions.

All automorphisms here are coordinate permutations. There is no new Lean
source; the three prior generic distance deductions keep their explicit
hypotheses, and the graph/module/computation instances remain unformalized.
The author also wrote the 120/176 supplements; their separate root reviews
are retained and do not replace distinct review of this new packet.

No public files, old scientific packets or old completed enumerations are
modified. No source, question, priority or numerical credit is introduced.
