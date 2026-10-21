Topic A: lengths of the manuscripts
===================================

The six applications, common paper and final attribution correction have
passed independent review. These private numerical results bind their
final editions and await root review before admission.

Primary coordinate: NFC characters other than whitespace, after only
reviewed page-furniture exclusions and font-aware glyph calibration.

Six complete sources: 195,379 characters.
Full umbrella: 49,059; six complete applications: 78,251.
Full printed four-program appendix: 53,035.

Written papers: 195,379/127,310 = 1.534671.
Including the required program: 195,379/180,345 = 1.083362.

The second denominator includes the entire printed appendix exactly once.
The same raw program files are not added again. Their complete raw-text
costs and the alternative denominator are reported as a sensitivity.

Conditional applications
------------------------

Each following factor is c(source manuscript)/c(application), after
acquiring the whole umbrella and the whole complete program appendix.
Those common costs remain included in the topic comparison above.

L032 -> A1: 16,558/8,212 = 2.016318
L034 -> A2: 21,433/5,784 = 3.705567
F016 -> A3: 43,983/15,419 = 2.852520
F013 -> A4: 25,562/6,224 = 4.107005
L035 -> A5: 51,019/14,498 = 3.519037
N009 -> A6: 36,824/28,114 = 1.309810

Calibrated metric sensitivity
-----------------------------

Each row uses the named unit throughout. The five units are reported
separately under each normalization.

Form  Metric                                  Written    With full code
====  ======================================  =========  ==============
NFC   whitespace_tokens                        1.770375        1.556223
NFC   alphanumeric_units                       1.896848        1.444332
NFC   characters_without_whitespace            1.534671        1.083362
NFC   characters_with_collapsed_whitespace     1.577151        1.154279
NFC   utf8_bytes_with_collapsed_whitespace     1.488189        1.122995
NFKC  whitespace_tokens                        1.772414        1.558015
NFKC  alphanumeric_units                       1.896848        1.444332
NFKC  characters_without_whitespace            1.535608        1.084214
NFKC  characters_with_collapsed_whitespace     1.578266        1.155246
NFKC  utf8_bytes_with_collapsed_whitespace     1.638395        1.206272
====  ======================================  =========  ==============

Scope and sensitivity
---------------------

All source pages, including titles, abstracts and references, belong to
the numerator under the reviewed main-result contracts and their explicit
corrections/retained inputs. No all-assertions equivalence is claimed.
This is an extracted-text comparison, not complete visible-text cost:
L035 pages 9, 10, 12 and 22 contain image-only scientific labels and diagrams;
its page 22 embedded image is clipped. N009 page 1 also has an image-only
journal banner. Their missing visible text and graphical construction
costs remain unknown, not zero. No private raster transcription is counted.

Every one of the five metrics is supplied under NFC and NFKC, with
untrimmed, raw selected and calibrated selected text. Glyph corrections
can change byte and alphanumeric counts. Per-document costs are summed;
no artificial inter-document separator is added.

Physical extents are separately recorded: 93 source pages; 17 umbrella pages,
33 application pages and 21 pages of complete programs. They are not substituted
for the text factors. Retained outside proofs, historical external code
and library/diagram complexity remain separately unpriced. Formal proof
coverage and verification costs are not collapsed into these ratios.

Reproduction
------------

Install the pinned pypdf version 6.13.0. Supply the primary files privately
under a sources-root containing the sources/ paths in input_spec.json;
public-root must contain the declared papers/topic-a/v2 artifacts. Run::

  python3 -B -O recount.py --sources-root /private/study \
    --public-root /path/to/repository --out /fresh/output

No original PDF text, primary image or private label transcription is
written to the result packet. No new source or question credit is assigned.
