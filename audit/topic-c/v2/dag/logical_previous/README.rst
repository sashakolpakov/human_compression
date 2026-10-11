Topic C: paired mathematical dependencies
========================================

This author packet compares the accepted Topic C proofs with the four fixed
source editions. It preserves the forty rows of ``papers/topic-c/v2/scope.json``
verbatim and binds every one of its thirty-eight statement/context locators and
seven complete proof regions. The scientific files are byte-identical to commit
``87757bf``. No source intake or new mathematical admission occurs here.

``logical_graph.json`` has arrows from prerequisite to use. The five logical
edge kinds are proof use, definition use, hypothesis use, proof assembly and
retained input use. Attribution, validation, formal scope and comparison are
separate kinds and never contribute to a mathematical predecessor closure.
Historical arrows record the printed argument, including its explicitly flagged
invalid intermediate assertions. They do not certify those assertions.

``coverage.json`` gives every historical and current output and its complete
logical predecessor closure. N14 and N15 are excluded auxiliary assertions and
have no proved current output. Corrected/qualified claims retain that status.
The exact marked agreement between the two polygon constructions is additionally
recorded as a comparison proved by the current text; it does not add a source row.

The graph contains no weights, exclusive text partition or compression factor.
Overlapping theorem/branch locators are evidence, not disjoint cost spans. All
costs are null. The original L108 PDF remains unavailable. Its browser-rendered
body supplies documentary locators, never a substitute manuscript length.
Historical required code and external proofs also have unknown costs.

Replay, using only Python's standard library::

  python3 -B -O check.py \
    --sources-root /path/to/research/leemans \
    --public-root /path/to/math_compression \
    --out /fresh/path/report.json

The private source root must contain the exact four primary artifacts and their
existing documentary text files named in the graph. This packet does not export
those texts or copyrighted PDFs. Public proof, program and formal files are
resolved below the public root. No Lean or GAP rerun is necessary for this graph
check; their accepted roles and exact bytes are bound.

To regenerate the graph and coverage from the declared construction::

  python3 build.py --study-root /path/to/research/leemans \
    --public-root /path/to/math_compression --out /fresh/output/directory

The public clone must retain commit ``87757bf`` for this edition check.
The checker verifies hashes, codepoint/line locators, all forty source records,
logical acyclicity, actual closures, required program routes and twelve controls.
It does not prove the mathematical correctness or necessity of an authored edge.
Independent semantic review remains required.

The two full J1 GAP programs are mathematical premises. Their driver is only
operational evidence. The three Lean modules are scoped formal evidence for
sixteen listed declarations; geometry, augmentation bases, the cyclic application,
and the source correspondence remain written proofs. Another topic's possession
of a theorem never removes it from this topic's own dependency closure.
