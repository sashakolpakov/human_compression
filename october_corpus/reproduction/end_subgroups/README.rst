Finite end-subgroup certificates
================================

This package checks eleven supplied intersection-property exclusions for
job20 of the acquired G2(11) rank4 calculation. It uses Python's standard
library. Run from any directory with CPython3 on POSIX Darwin or Linux::

    python3 -E -B -S verify.py --controls
    python3 -E -B -S verify.py --all

For a single certificate use, for example, ``--case 248``. The fixed input
paths are relative to ``verify.py``. The checker writes one bounded JSON
result to stdout and creates no files. ``VALIDATION.json`` records the
publisher's actual private and installed replays; it is not a consumed
input. The package Source, manifest, imports and certificates must retain
the exact tested bytes when installed.

What is checked
---------------

Every case checks all four distinct nonidentity involutions and the three
string commutations over F11. For RIGHT cases248,399,910,1082,1273,2200,3379
the two supplied words use only labels1,2,3. For LEFT cases1812,2015 they
use only labels0,1,2. The checker evaluates the words and stated cofactors,
compares the complete supplied matrices and verifies nonidentity and the
19th or37th power equation. The two primes must occur in that same end.

RIGHT cases490,3417 instead supply an order37 word, a nonzero fixed vector
and one of labels1,2,3. The checker verifies the whole row equation vY=v
and a nonzero2by2 minor between v and its image under that generator.
It runs no word search, eigenspace solver, subgroup closure or model
recognition. All matrix products, row images and scalar allowances share
one bank across the chosen cases.

Why these are exclusions
------------------------

``proof.tex`` explains the attributed complete maximal-subgroup cover and
its two consequences. An end containing elements of orders19 and37 is
the entire named inner G2(11). An order37 element in its natural Cayley
module has a unique rational invariant line, and every proper subgroup
containing it preserves that line. One end generator moving it therefore
also proves the end is the entire group. The omitted mark is nonidentity,
so its singleton subgroup has nontrivial intersection with that full end,
although their label sets are disjoint. This contradicts the intersection
property. This is not a consecutive-intersection-excess test.

The ambient named group, faithful natural module, all four memberships in
one common frame, complete maximal cover and Original row identification
are explicit attributed imports in ``IMPORTS.json``. Bare matrix orders
do not recognize G2(11). ``PROVENANCE.json`` identifies the historical
tuples, strict supplier carriers, proofs, accepted records and scope by
whole-byte SHA256 anchors, with private machine paths removed. Numerical
field, matrix, word and line kernels are retained from the earlier strict
consumers; ``SOURCE_REUSE.json`` records their literal reuse.

These finite replays reproduce eleven registered marking-property
exclusions. They supply no new Original execution, whole-job completion,
equivalence-class, automorphism, duality, census, manuscript or Lean credit.
The26 original-free controls use generic GL7(F11) examples; they do not
pretend to be G2 fixtures.

Resource profile
----------------

Use the unchanged outer128MiB/100s profile for each invocation. The code
enforces a90s/112MiB cooperative bank, with Darwin RSS measured in bytes
and Linux RSS in KiB converted to bytes. The shared limits are400000
complete7by7 products,200000 row images,200000 scalar units,8MiB cumulative
input reads and96 paths. An initial131072-byte reservation covers known
worker/guard startup Source loads. Whole input reads require canonical
single-link regular files, exact EOF and unchanged same-FD/path identities;
all consumed Sources and data are reopened before success. At most one
128KiB result is emitted. All eleven certificates fit one explicit finite
bank; there is no discovery or unbounded cache.

Attribution
-----------

The maximal-cover argument and line corollary are borrowed from the
retained common note ``g2_11_generation_by_prime_witnesses.tex`` (SHA256
f1b6c8a69780c7b8ac88f239627a7ce6889c24203f72ddc35c86fe93e661e76b),
independently reviewed under SHA256
8de6c659c024cd16d90bde4f8a8d548735b201b5a5892c747f63d9a8e08ae053.
That note attributes the classification to Kleidman, its complete list to
Nguyen and Wilson, and the natural-module geometry to Wilson. This
portable wrapper and proof presentation make no novelty claim.
