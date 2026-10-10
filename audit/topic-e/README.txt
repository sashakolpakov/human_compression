Topic E: full manuscripts and shared theory

Read measurement.pdf (editable source measurement.tex) and costs.svg.
protocol.json fixes every PDF, page, included interval, furniture removal,
metric and normalization. author_measurement.json records the author count;
independent_measurement.json recounts the full pages without the author's
span-selection code. independent_review.json supplies the third review.
admission.json records the subsequent root decision and exact scope;
the author report retains its historical pre-review status.
The admitted mathematical contracts are inherited from the intake archive.

Primary publications are not distributed. With their exact pinned copies
in PRIVATE_STUDY/sources, reproduce from the repository root:

python audit/topic-e/measure.py --sources-root PRIVATE_STUDY --artifacts-root research/case_study --out /tmp/topic-e-author.json
python audit/topic-e/independent_measure.py --sources-root PRIVATE_STUDY --artifacts-root research/case_study --out /tmp/topic-e-independent.json

Both commands require pypdf 6.13.0 and fresh output paths. The compatibility
symlink topic_E_full_manuscript_protocol.json points to protocol.json so
that the byte-preserved author runner's default argument works.

Plot the frozen data with matplotlib:

python audit/topic-e/plot_costs.py

Compile the measurement note from this directory with XeLaTeX twice:

xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error measurement.tex

No Markdown input or primary-text export is involved. The complete required
GAP program and the three-page counted appendix are the exact files bound
by protocol.json, under research/case_study. Classical inputs remain
retained, and historical program cost is unknown. L021 is excluded from
this two-application measurement. The earlier selected-proof comparison
remains recorded as a separate sensitivity, not the full-source ratio.
