#!/usr/bin/env python3
"""Build the two-page enlarged Mixes input reader. No factors."""
from pathlib import Path
import json
H=Path(__file__).resolve().parent

def make():
 r=json.loads((H/'author_counts.json').read_text());old=r['retained_accepted_inputs'];rows=[]
 for k,title,legacy in [('F005','F005: complete source',True),('L016','L016: complete source',False),('U','Earlier common theory',True),('U1','Cover common theory',False),('A1','F005 local application',True),('A2','F005 exceptional application',True),('A3','L016 application',False),('REQ','Both required certificates',False),('VAL','New optional validations',False),('CODE1','Old mixed appendix (inventory)',True),('CODE2','Old optional appendix (inventory)',True)]:
  d=(old if legacy else r)['documents'][k];vals=[d['metrics'][v]['NFC']['characters_without_whitespace']for v in ['raw_untrimmed','raw_selected','calibrated_selected']]
  rows.append(title+' & '+str(d['pages'])+' & '+' & '.join(f'{v:,}'for v in vals)+r' \\')
 raw=[]
 for block,prefix in [(old,'F005'),(r,'L016')]:
  for category,role in [('programs',''),('drivers','Driver'),('formal','Partial Lean')]:
   for name,d in block['raw_files'][category].items():
    nm=Path(name).name
    rl=role or ('Required certificate'if nm in ['check_coprime.g','base_certificate.g']else 'Optional validation')
    if nm=='check.py'and 'exception' in name:rl='Additive driver'
    raw.append(prefix+r': \texttt{'+nm.replace('_',r'\_')+'} & '+rl+' & '+f"{d['metrics']['NFC']['characters_without_whitespace']:,}"+r' \\')
 return TEMPLATE.replace('@PDF_ROWS@','\n'.join(rows)).replace('@RAW_ROWS@','\n'.join(raw))
TEMPLATE=r'''\documentclass[a4paper,11pt]{article}
\usepackage[margin=22mm]{geometry}
\usepackage{fontspec,booktabs,array,hyperref}
\setmainfont{STIXGeneral}\setmonofont{Menlo}[Scale=0.79]
\hypersetup{hidelinks}\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\begin{document}
\begin{center}{\Large Complete inputs for the enlarged Mixes topic}\\[4pt]
Human Compression project\quad---\quad F005 and L016\end{center}
This input packet adds Leemans--Toledo's \emph{Faithful and thin non-polytopal
maniplexes}, arXiv:2305.01372v2 (10 May 2023), to the existing Mixes topic.
All 12 original pages are included. The entire earlier common paper (5 pages),
new cover common paper (4 pages), and all three application papers (8, 4 and
6 pages) are charged. There is no overlap deduction or free prior theory.

\textbf{Primary rule, fixed before counting:} NFC characters without whitespace
in literal, untrimmed PDF extraction on both sides. The raw column retains
headers, footers and the source banner. No factor is evaluated in this packet.

\begin{center}\small
\begin{tabular}{@{}p{72mm}rrrr@{}}\toprule
Complete document & Pages & Raw & Selected & Calibrated\\\midrule
@PDF_ROWS@
\bottomrule\end{tabular}\end{center}

The scientific comparison has two complete sources, two complete common
papers and three complete application papers. The last four table rows are
program representations or historical inventories, not four additive charges.
The new two-page required appendix contains both whole certificates. It is an
alternative to the two required raw files, never an additional cost. Any later
conditional application comparison must declare both whole common papers and
both required certificates already acquired.

\textbf{Optional verification is symmetric.} The four optional validation
programs may enter a comparison only when corresponding source-side optional
verification is also included; otherwise optional verification is excluded on
both sides. Historical software is unavailable, so its cost is unknown, not
zero. Neither source prints an executable listing; its written algorithms and
formulas stay in the full text. The earlier mixed appendices and earlier optional-inclusive numerical
results remain unchanged historical inventories. They are not relabelled as
current required-only compression factors.

\textbf{Input reuse and scientific scope.} All 180 PDF cells and 70 raw-file
cells from the accepted F005 input audit are retained exactly, without
reextracting those documents. The new extraction adds 150 PDF cells over
27 pages and 60 raw-file cells. The 35 F005 and 19 L016 dispositions describe
two originals, not 54 sources. L016's literal thin-base Lemma 3.5 is disproved
and repaired under the stated faithful-base hypothesis. Its principal family
and rank-three results are recovered; the small-example census, atlas claims
and further-cover questions remain visibly outside the contract. All three
final F005 problems remain unanswered. Distinct scientific reviews and root
adoptions are bound; distinct measurement-input acceptance is still required.

\newpage
\begin{center}{\large Whole files and representation limits}\end{center}
\begin{center}\small
\begin{tabular}{@{}p{92mm}p{42mm}r@{}}\toprule
Complete raw file & Role & NFC nonspace\\\midrule
@RAW_ROWS@
\bottomrule\end{tabular}\end{center}

The two required GAP files identify the finite coprime-mix example and the
order-96 marked presentation. The four optional programs check written
coordinate constructions. Five operational files and two Lean files remain
separate inventories. The Lean scope is six generic declarations (four new,
two reused), not a formalization of the complete source or applications.
Complete-file inclusion in both new appendices is checked without line pruning.
A comparison including required programs must disclose the unknown source-side
software cost; it cannot claim a complete measured software comparison.

\textbf{Units and extraction.} Every PDF has five units under NFC and NFKC in
three variants: literal untrimmed, literal selected, and calibrated selected.
The five units are whitespace tokens, alphanumeric units, nonspace characters,
characters with collapsed whitespace, and UTF-8 bytes with collapsed whitespace.
Selected L016 extraction removes only its isolated first-page footer and later
running headers; replacement selection removes isolated page footers. The source
banner stays. Raw files use all five units and both normalizations.

The source has 23 actual Type1 dictionaries and 566 encoded glyph classes.
Fifteen replacement Type0 dictionaries retain literal extraction. Actual embedded
outlines were inspected for 19 exceptional classes. Twelve observed aliases occur
331 times: script letters, brace components and four arrow-tee components. Only
the calibrated sensitivity changes those representations; no guessed composite
arrow is inserted. UTF-8 differences do not measure semantic proof complexity.
The pinned extractor uses \texttt{pypdf 6.13.0} and \texttt{fontTools 4.63.0},
checks ordinary returned text, and separates actual glyph events from generated
line breaks. No Form callback duplication was found.

\textbf{Visual and external limits.} All 27 new source, proof and appendix pages
were viewed; the earlier 45-page record is reused with its accepted bindings.
The four source figures on pages 7, 8, 9 and 11 retain their extractable labels
and captions. Edge strokes, colors, circles and layout have no established full
cost. Historical software, retained external proofs, runtime and complete formal
verification likewise remain unknown. No source text, font bytes or page images
are exported. The portable replay checks the inputs, 47 rejection controls and
fresh reader/appendix renders; it does not rerun the scientific GAP or Lean work.
The measurement author also authored L016, so input acceptance must be distinct.
\end{document}
'''
if __name__=='__main__':(H/'input_reader.tex').write_text(make())
