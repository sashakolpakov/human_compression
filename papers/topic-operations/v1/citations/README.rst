Citation editions for the unified operations common paper
========================================================

These are exact applications of the two patches in the frozen input contract
c84db79a. The old scientific and public files remain unchanged. N006's general
paper remains eight pages and N007 remains five. The complete new common paper
is the independently accepted 21-page edition ff13bbee; its proof review is
78d1ba74. No mathematical result, source credit or numerical factor is added.

All 18 complete theorem/proof environments are byte-identical to their prior
versions. Only the specified interface prose and bibliography entries differ.
The three old N007 reference numbers remain unchanged; its common reference is
appended as [4]. Finite-type and faithful-initial-input conditions are explicit.
The two sporadic companion papers need no changes and remain wholly required.

Both PDFs were freshly built twice from their complete inputs. All 13 pages
were visually inspected. The exact patches yield three underfull-line notices:
two in the N006 opening/bibliography and one in the N007 bibliography. The lines
remain legible without overlap or clipping; all notices are recorded, rather
than described as an empty diagnostic run. There are no undefined references,
missing glyphs or overfull boxes. The original preambles are unchanged.

Replay with pypdf 6.13.0 and XeLaTeX::

  python3 -B -O check.py --study-root /path/to/research/leemans \
    --public-root /path/to/math_compression --out /fresh/output --render \
    --xelatex /path/to/xelatex

The checker reconstructs the exact patch result, verifies complete unchanged
statement/proof environments, tests a deliberate proof edit, and optionally
rebuilds both documents with exact per-page extracted-text comparison. It does
not rerun GAP or Lean. Measurement must use these changed PDF bytes after the
additive editions are independently accepted; no length-neutrality is assumed.
