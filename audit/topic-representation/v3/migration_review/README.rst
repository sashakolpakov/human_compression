Independent review of the shared finite-pair relocation
======================================================

The frozen successor 0e391127 is accepted without requested correction.
This review reuses the full scientific/source/certificate/formal acceptance
b855471d and examines the complete new migration. Reviewer authorship of the
older F010 edition is disclosed; its distinct historical acceptance remains
separate from this relocation review.

The entire encoder and existence proof now belongs to the common paper.
Both F010 theorem statements remain exact, with direct references to their
fully proved common versions. L126 finite-existence uses now cite that common
proof, with finite-group and normal-inner-subgroup hypotheses explicit.
There is no longer a sibling F010 application proof premise in L126.
The required graph certificate/data and all classical qualifications remain.

All29 current scientific pages were viewed. Four fresh builds passed exact
page-text checks; the unchanged16-page code appendix retains its earlier
visual acceptance. No unchanged GAP or Lean calculation was repeated.
No source credit or numerical comparison follows from this review.

Portable replay::

  python3 -B -O check.py --author /path/to/topic_Representation_L126_recovery_v2 --out /fresh/path

Add --render for fresh four-paper TeX builds. The author packet supplies its
exact predecessor TeX and metadata; no primary PDF or proof-bank access is
needed for the bounded migration replay.
