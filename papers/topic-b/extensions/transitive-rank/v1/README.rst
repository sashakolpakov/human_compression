L047: transitive string C-groups
================================

This is an author-frozen candidate for the complete corrected principal contract
of Cameron, Fernandes, Leemans and Mixer, ``String C-groups as transitive
subgroups of S_n``, arXiv:1410.5863v1 (21 October 2014), twelve physical pages.
It awaits distinct complete scientific review. No public file, source count,
question count or numerical factor changes here.

Read ``transitive_string_groups.pdf`` (three full pages) and
``string_rank_theory.pdf`` (ten full pages), then ``source_map.json``. The
58 dispositions include all numbered results and all rows of the three source
tables. All four branches of Theorem 1.2, the sharp imprimitive bound and equality
classification, the complete primitive exception list and the three alternating
parabolic corollaries are proved. Twenty-three finer Table 3 maximum-rank reports
remain attributed ancillary reports, not premises or new reproofs. Source
Conjecture 1.1 was resolved by the accessible L044; it is not claimed as a new
solution or still-open question.

The complete accepted sixteen-page common paper ``Forest coordinates and
relative generation`` is retained under ``retained/common``. It supplies normal
quotients/modules, the extremal tree theorem and the weak primitive independent
length bound. No prior application is needed. The new sharp theorem closes by
strong induction on permutation degree; the old universal imprimitive length
bound is not a logical premise. Quotient block images are never assumed to
inherit IP. The normalized two-block image does inherit it.

The root-authored ten-action finite-neighbor lemma is copied unchanged with its
distinct acceptance and root adoption. Its entire proof body also appears in the
new common manuscript, with literal extraction equality recorded in
``finite_migration.json``. Thus it is not an uncharged external proof. The original
two-page PDF is retained as an archive. The new author's earlier independent
review of the old common paper is disclosed in ``dependencies.json``; it is not an
independent acceptance of this new manuscript.

Exact corrections and conventions
--------------------------------

The order-36 row of source Table 1 has actual type [3,2,3], not the printed
[2,3,3]. The latter would be a quotient of a group of order 48 and cannot have
order 36. For the odd-block wreath family, reversing its noncentral component
changes the ordered type. Both ordered classes up to global duality are kept;
uniqueness is asserted for the unordered marked set, not for a falsely identified
ordered polytope. In source Section 4 the symbol d indexes generators 0..d:
our parent rank R=d+1 and parabolic rank r=d remain separate. The standing
string-C-group hypothesis of source Proposition 2.2 is preserved explicitly.

Computation and formal limits
-----------------------------

``program-appendix.pdf`` prints all six required new/dependency files in full
(seven pages): four new complete searches and the unchanged finite-neighbor
``search.g`` and ``run.g``. The whole old seven-page program appendix and all four
old files remain visible, with their original required/validation/auxiliary
roles. No small model is used in place of an exhaustive range. The written
proof explains every pruning condition and why these finite ranges suffice.

The new searches cover both maximal independent S5/S6 involutory strings,
all 78 imprimitive catalogue actions in degrees 6/8/9, all primitive catalogue
entries through degree 25 and the eleven exact residual/parent marking searches.
Literal positive tuples receive a separate Python integer-permutation order,
transitivity, string and full subset-IP check. The outer S6 endpoint test uses
the actual derived tail centralizer, including the transitive A5 tail.
The root finite lemma has 59 normalized markings, 154 transitive completions,
all redundant, and positive lower-rank controls.

Retained external premises include Whiston, original Maroti with its lower
A_m^ell containment, Conder's nondegenerate rank-at-least-nine lower-order bound,
and the standard regular-polytope correspondence. GAP 4.15.1 and its exact
algorithms/catalogue completeness are trusted; ``external_software.json`` binds
the actual catalogue files and indices. Complete external proof/software and
graphics costs are unknown, not zero. No compression factor is calculated.

There are zero new Lean declarations. The fourteen partial declarations in the
two inherited common modules are copied unchanged, with their accepted scope.
They do not formalize this rank theorem, the searches or the classification.
Their old accepted replay is reused; no fresh formal replay is claimed.

Additive precision edition
--------------------------

This successor preserves the original author freeze 681c011d. Its only proof
change states the standard Maroti subset normalization explicitly: after
complementing subsets, 1 <= k <= m/2. All 58 source dispositions, programs,
finite results, scope and retained packets are unchanged. ``precision_delta.json``
and ``mathematical_delta.diff`` describe the exact change; ``check_precision.py``
checks it against the bound predecessor. The original ``author_replay.json`` and
``visual_review.json`` remain historical records of v1. Fresh changed-document
evidence is in ``precision_replay.json`` and ``precision_visual_review.json``.
No new program execution is needed for this prose-only change; the full v1
export-only replay is separately retained once it completes.

Replay
------

From any export-only copy in the pinned installed environment::

  /Users/sasha/.venvs/global/bin/python -B -O check.py \
    --out /fresh/path --programs --render \
    --gap /opt/homebrew/bin/gap --xelatex /opt/homebrew/bin/xelatex

Without ``--programs``, the checker verifies and parses the bound author output,
including the independent integer-permutation checks. With ``--programs`` it
reruns all four new searches and the complete two-file root finite lemma.
``--render`` rebuilds all three new documents twice and compares every page's
extracted text. ``--study-root /Users/sasha/medusa/research/leemans`` additionally
checks the exact private primary edition and every source span. No primary PDF,
primary full text, page raster, font or Markdown is exported.

``string_separators.tex`` and ``primitive_screen.g`` are superseded private
working files, deliberately absent from the manifest. They are not extra common
papers or execution inputs. Only manifest exports belong to the frozen packet.

Check the exact additive delta separately with ``python3 -B -O check_precision.py``.
