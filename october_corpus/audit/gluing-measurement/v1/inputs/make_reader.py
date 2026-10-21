"""Generate the complete input reader; no factors are evaluated."""
from pathlib import Path
import json
H=Path(__file__).resolve().parent

def make():
 c=json.loads((H/'author_counts.json').read_text());p=json.loads((H/'policy.json').read_text())
 names={'L010':'Original L010','U1':'Common paper: supported orbits','U2':'Common paper: synchronized trees','A1':'Complete application','CODE':'Three complete diagnostic programs'}
 rows=[]
 for k,v in c['documents'].items():
  n=lambda var:f"{v['metrics'][var]['NFC']['characters_without_whitespace']:,}"
  rows.append(f"{names[k]} & {v['pages']} & {n('raw_untrimmed')} & {n('calibrated_selected')} \\\\")
 raw=[]
 for cat,rs in c['raw_files'].items():
  for k,v in rs.items():
   label={'programs':'Diagnostic','drivers':'Driver','formal':'Lean'}[cat]+' '+Path(k).name.replace('_',r'\_')
   if cat=='drivers':label+=' ('+{'topic_B_core_theory':'orbits','topic_B_parallel_trees':'trees','topic_B_L010_recovery':'application'}[k.split('/')[0]]+')'
   raw.append(f"{label} & {v['bytes']:,} & {v['metrics']['NFC']['characters_without_whitespace']:,} \\\\")
 s=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}
\usepackage{fontspec,booktabs,tabularx,hyperref}
\setmainfont{STIXGeneral}\setmonofont{Menlo}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\begin{document}
\begin{center}{\Large Gluing: supported orbits and synchronized trees}\\[4pt]
Complete inputs for a future length comparison\end{center}

This packet fixes one original manuscript and the complete proof material used to recover its principal constructions and counterexamples. It does not calculate a compression factor. The original is Leemans and Mulpas, \emph{Two gluing methods for string C-group representations of the symmetric groups}, arXiv:2504.17535v1, 24 April 2025; the register labels it L010 (2026). All fifteen original pages are included, with references, addresses and the identification banner.

Both whole common papers are charged independently to this topic. The earlier sixteen-page common paper for Topic B is not used or imported. The full application remains included. There is no discount for overlap with another topic. The source map has twenty-three records concerning one manuscript, not twenty-three manuscripts.

\begin{center}\small
\begin{tabular}{lrrr}\toprule
Complete document & Pages & Raw & Selected\\\midrule
__PDF_ROWS__
\bottomrule\end{tabular}\end{center}

The displayed counts are NFC characters without whitespace. ``Raw'' retains the complete PDF extraction, including page furniture. ``Selected'' removes only precisely recorded running headers or isolated page numbers, then applies six observed glyph-class substitutions. No proof, introduction, connective passage or reference is omitted. The two selected character counts happen to agree before and after calibration; this does not make their Unicode or byte counts identical.

The packet records all five units---whitespace tokens, alphanumeric units, characters without whitespace, characters with collapsed whitespace, and UTF-8 bytes with collapsed whitespace---under NFC and NFKC, for raw untrimmed, raw selected and calibrated selected text. These give 150 PDF cells. The designated future primary coordinate is calibrated selected NFC characters without whitespace; the other coordinates remain explicit sensitivities.

The scientific papers have distinct mathematical acceptance. The measurement author also authored those papers; this input audit is not an independent mathematical review. The established scope includes the source's two gluing operations, exact ranges and exceptions, both small impure-leaf examples, and the already historical counterexamples. The closing numerical sequence and unused preliminary results are not claimed as new recoveries. The endpoint sesquiextension result and the classical end-parabolic criterion remain attributed external inputs. No new question answer is credited here.

\newpage
{\large Programs, glyphs and limits}

All three diagnostic programs are printed without pruning. They test finite models and failed weakenings; none supplies a premise of the uniform written proofs. The complete declared program bundle will nevertheless be paid in the program-inclusive comparison and prepaid together with both common papers for a conditional application comparison. Its four-page printed appendix and the three whole raw files are alternatives, never added together.

\begin{center}\small
\begin{tabular}{lrr}\toprule
Whole raw file & Bytes & NFC nonspace\\\midrule
__RAW_ROWS__
\bottomrule\end{tabular}\end{center}

These eight files contribute eighty raw measurement cells. The three operational drivers and the two Lean files are separately inventoried. The latter verify ten scoped declarations, not the complete gluing theorems or their source applications. No end-to-end formalization is claimed.

The actual source dictionaries contain 559 used glyph classes in 27 font dictionaries. The printed appendix adds three classes in two dictionaries; the replacement Unicode text is left unchanged. Twenty-one exceptional actual outlines were inspected. Six classes produce 175 substitutions: five script letters and one short arrow stile. Composite mathematical symbols are not reconstructed from conjectured meaning. A left-curved program-wrap glyph retains its literal comma decoding. The unembedded standard Times banner is accepted only for literal ASCII; no embedded outline is claimed for it.

Every original page and all replacement and program pages have been visually inspected. Text labels in the many source diagrams are measured where extracted, but incidence, position, lines, colour and shaded regions are not converted into character costs. Full graphical complexity remains unknown. Historical software, the complete retained external proofs and the cost of full formalization also remain unknown. All are recorded as null, not zero.

The replay checks complete byte bindings, every physical page, exact furniture cuts, original glyph events and the full printed program content. Primary PDFs, extracted text, fonts and page images remain private. Reproduction requires the bound primary and scientific PDFs and raw files supplied separately. A distinct input reviewer must accept this boundary before any numerical factor is evaluated.
\end{document}
'''
 return s.replace('__PDF_ROWS__','\n'.join(rows)).replace('__RAW_ROWS__','\n'.join(raw))
if __name__=='__main__':(H/'input_reader.tex').write_text(make())
