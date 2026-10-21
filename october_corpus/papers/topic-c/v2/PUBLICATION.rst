Chamber operations and binary translations
==========================================

This edition contains one complete common paper and four applications.
The `independent review <../../../audit/topic-c/v2/independent_review/review.pdf>`_
accepts their fixed principal-result contracts, including corrections and
exclusions. The `admission <../../../audit/topic-c/v2/admission.json>`_ binds
that review and the actual computations. Earlier author-stage status labels
are preserved in the frozen files and superseded by this admission.

Read the `common theory <umbrella.pdf>`_ (10 pages), followed by:

* `Six Janko geometries <janko-geometries.pdf>`_ (4 pages): Hartley and
  Leemans, 2005; all six constructions, failed operations and the full census.
* `Halving generalized cubes <halving-generalized-cubes.pdf>`_ (6 pages):
  Montero and Ivic Weiss, the 2020 arXiv edition; parity, local sphericity
  and actual toroidal identifications, with two auxiliary claims excluded.
* `Petrials and faithful actions <petrials-and-faithful-actions.pdf>`_
  (4 pages): Bonheure, Buekenhout and Leemans, 2001; the natural action
  kernel, thinness obstruction and recovery, with source qualifications.
* `Equal adjacent parameters <equal-adjacent-parameters.pdf>`_ (3 pages):
  Li and Zhang, the 2025 arXiv edition; the marked construction, matrices,
  universal presentation and separately stated small-parameter case.

The shared graph argument presents even binary translations by edge
differences. Covariance then gives an explicit inverse for the semidirect
presentation. Both the generalized-cube and equal-parameter applications
use graph generation. The latter replaces a finite-order comparison by
mutually inverse homomorphisms. The source displacement argument and
standard augmentation and semidirect-product theory remain attributed.
The complete geometric operation arguments are included at this topic's
own cost. No historical priority claim is made for these standard ideas.

The forty rows in `scope.json <scope.json>`_ comprise 32 recovered clauses,
five corrected or qualified assertions, two excluded auxiliary claims and
one retained background/adapter row. They are not forty new theorem credits.
The higher-rank question associated with F014 stays in its separate question
ledger. The existing total of admitted principal contracts does not change.

The `full program appendix <required-programs.pdf>`_ (4 pages) prints both
required GAP programs. The independent fresh execution tested all 100,016
rank-four and 21,352 rank-five extensions, giving six and zero classes,
respectively. The complete subgroup catalogue and exact group algorithms
remain retained inputs. The appendix is a separate required proof artifact;
it cannot be omitted from the program-inclusive comparison. The operational
runner and formal/audit infrastructure are inventoried separately.

The three files under formal/ have been freshly compiled by the independent
reviewer and by root. Nine new declarations prove the generic explicit
inverse; seven declarations are reused displacement and intersection
components. All reported axioms are standard. The augmentation basis,
specific cyclic maps, geometric adapters and Janko census remain outside
Lean. Read `formal/scope.json <formal/scope.json>`_ before interpreting the
formal coverage. The existing 100-module default library and the legacy-plus-B
runner do not include this separate checker::

  python3 -B -O papers/topic-c/v2/formal/check.py --out FRESH_FORMAL_DIRECTORY \
    --lean PATH_TO_LEAN --packages PATH_TO_PINNED_PACKAGES

To reproduce all six PDFs, including the program appendix::

  python3 -B -O papers/topic-c/v2/check.py --out FRESH_RENDER_DIRECTORY --render

The standard catalogue builder also builds the five scientific papers. The
appendix uses its separately bound program inputs and the command above.
For a bounded independent replay from the public checkout::

  python3 -B -O audit/topic-c/v2/independent_review/check.py \
    --author-root papers/topic-c/v2 --out FRESH_REVIEW_DIRECTORY

This last command checks bindings and finite controls; add --full to request
a new formal, render and full Janko run. See `README.rst <README.rst>`_ for
the separate census command and exact dependency requirements.

The original L108 PDF is unavailable. The Ens notation input retains only
an earlier selected web reading, with no stored primary artifact; its
classification is not used. These limits remain explicit. Lengths and paired
dependency costs have not yet been measured for this edition. The complete
common theory and both required programs must be charged once within Topic C,
with conditional factors separately reported after acquisition.
