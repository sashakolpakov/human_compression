Current consolidated comparison: 36 originals
============================================

The `six-page report <packet/summary.pdf>`_ gives all fourteen topic costs
and all thirty-six individual comparisons. The `complete-topic graph
<packet/whole_topics.svg>`_ displays every common and application paper.
The `first seventeen <packet/conditional_1.svg>`_ and `remaining nineteen
<packet/conditional_2.svg>`_ application comparisons assume full prior
acquisition. Exact `topic <packet/topics.csv>`_ and `application
<packet/applications.csv>`_ tables accompany the TeX and JSON.

The joint Operations topic replaces the previous two-original Diagonal
record. It includes N005, N006 and N007, the complete 21-page common paper,
all three applications and both N006 companions. Its written factor is
1.266700; including all 23 mathematical/validation files and both decoding
drivers gives 0.357176. Conditional factors are 2.459966, 1.455365 and 1.860057
after acquiring all common theory, programs and required data. All thirteen
other topic records remain unchanged.

Distinct review checked all 77 exact fractions, 50 CSV rows and 142 actual
bars in each vector format. All six pages were read and viewed after a fresh
build. Frozen author files retain their submission wording; `root admission
<admission.json>`_ supplies the current accepted status. The separate
`scientific admission <../../topic-operations/v1/admission.json>`_ earns N005
one additional original. Numerical consolidation itself earns no theorem,
conjecture or formalization credit.

There are 36 admitted and measured principal-result recoveries, out of 106
accessible originals in the fixed 161-title programme. The remaining 70
accessible originals await complete recovery and 55 await retrieval. Every
accessible original remains in the programme. Each topic pays its whole
common theory independently, including overlaps with other topics. Unknown
external proof, historical software, graphics and full formalization costs
remain unknown; the different source representations are not pooled.

A near-unit factor shows little saving by our present proofs. It does not
establish historical originality or minimum proof complexity. D still has
source cost 47,894, application cost 29,855 and common theory cost 15,632,
giving 1.053 overall. Further reuse must be demonstrated before it improves
that measured comparison.

Run ``python -B -O packet/check.py --public-root PUBLIC --out FRESH.json`` for
the author replay, and ``python -B -O independent_review/check.py --public-root
PUBLIC --packet packet --out FRESH.json`` for the distinct arithmetic and
vector-geometry check. Python needs pypdf and Matplotlib. The complete fresh
reader build is ``python -B -O packet/build.py --out FRESH --render``; it also
needs XeLaTeX and STIX fonts. These commands do not rerun the underlying GAP,
Lean or source extraction.
