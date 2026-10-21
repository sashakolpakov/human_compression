"""Generate a human-readable input specification; no factors are computed."""
from pathlib import Path
import json
O=Path(__file__).resolve().parent;c=json.loads((O/'author_counts.json').read_text());p=json.loads((O/'policy.json').read_text())
def comma(x):return f'{x:,}'
def val(key):return comma(c['documents'][key]['metrics']['calibrated_selected']['NFC']['characters_without_whitespace'])
labels={'N007':'N007 original','N006':'N006 original','U':'Whole enlarged common theory','A1':'N007 application','A2':'N006 general application','A2nine':'N006 nine-case companion','A2HN':'N006 Harada--Norton companion','CODEold':'Old N007 validation appendix (alternative)'}
rows='\n'.join(f"{labels[k]} & {v['pages']} & {val(k)}\\\\" for k,v in c['documents'].items())
rawrows='\n'.join(f"{label} & {len(c['raw_files'][cat])} & {comma(sum(x['bytes'] for x in c['raw_files'][cat].values()))} & {comma(sum(x['metrics']['NFC']['characters_without_whitespace'] for x in c['raw_files'][cat].values()))}\\\\" for cat,label in [('programs','GAP and witness files'),('required_drivers','Required decoding drivers'),('drivers','Operational drivers'),('formal','Unique Lean files')])
sensitivity='\n'.join(f"{key} & {comma(c['documents'][key]['metrics']['raw_untrimmed']['NFC']['characters_without_whitespace'])} & {comma(c['documents'][key]['metrics']['raw_selected']['NFC']['characters_without_whitespace'])} & {val(key)} & {comma(c['text_only_sensitivity'][key]['metrics']['NFC']['characters_without_whitespace'])}\\\\" for key in ['N007','N006'])
tex=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}\usepackage{fontspec}\setmainfont{STIXGeneral}\usepackage{unicode-math}\setmathfont{STIX Two Math}\usepackage{booktabs,array,hyperref}\hypersetup{hidelinks}\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\title{Length inputs for orbit and semidirect constructions}\author{Human Compression Project}\date{Proposed input edition; no compression factor}
\begin{document}\maketitle
This packet covers two original manuscripts by Claudio Alexandre Piedade and Philippe Tranchida: \emph{Coset geometries acting on their elements: The $j$-diagonals twisting} (N007, arXiv:2608.23223v1) and \emph{The geometry of wreath and semi-direct products} (N006, arXiv:2605.04646v2). The complete published replacement edition is pinned to commit \texttt{faf0a46}. The thirty-two N007 and twenty-seven N006 source rows are scientific scope records, not additional manuscripts.

\begin{center}\begin{tabular}{lrr}\toprule
Complete document & Pages & NFC nonspace characters\\\midrule
'''+rows+r'''
\bottomrule\end{tabular}\end{center}
The written boundary includes the whole enlarged common theory once, the unchanged five-page N007 application, and all seventeen pages of the N006 application and its two necessary companions. It does not charge the old common paper again. All title, abstract, author, body, table, reference and address text remains on both sides. Only the exact recorded running furniture and isolated page numbers are removed. No source page is dropped.

The displayed coordinate is calibrated selected NFC nonspace characters. New diagram-stroke proxies remain a proposal for distinct review; raw alternatives and an additional text-only sensitivity are shown below. These are input lengths, not an admitted comparison. No factor is computed here.

The scientific scope retains every correction and exclusion of the accepted edition. In particular the ten affirmative sporadic cases include Harada--Norton, while the source's two Fischer exceptions are outside this edition's recovery contract. Later exception certificates are not silently added. Classical Coxeter and polytope correspondences, named group identifications and maximal-subgroup classifications keep their stated retained-input status.
\newpage
\section*{Complete programs and required data}
\begin{center}\begin{tabular}{lrrr}\toprule
Complete raw boundary & Files & Bytes & NFC nonspace\\\midrule
'''+rawrows+r'''
\bottomrule\end{tabular}\end{center}
All eighteen new GAP or witness files and the old N007 validation file are included in full. Sixteen contain finite proof checks or complete witness data; three are validation. Both complete finite-certificate decoding drivers belong to the required software boundary. Compact words do not eliminate the programs and representation data that give them meaning. Four other drivers are operational and are measured separately. Three unique Lean files contain seventeen scoped declarations, including eight unchanged reused declarations; none formalizes the complete source geometry or sporadic computation.

The primary complete software representation is raw, because this scientific edition has no printed appendix for all eighteen new files. The old two-page appendix is a printed alternative for its one N007 validation file only, never an addition to that same raw file. No required routine, witness file or diagnostic is pruned. JSON records every file and all five units under both normalizations.

The required external representation inputs are four complete files totaling \textbf{21,960,689 bytes}: the O'Nan pair contributes 3,720,665 bytes and the Harada--Norton binary pair 18,240,024. Sixteen separately listed installed catalogue, index and algorithm files contribute \textbf{2,516,249 bytes}, once per identical file within this topic. These data remain external and hash-bound. Their byte sizes are visible costs; they are not converted into invented mathematical proof lengths. The binary and decoded Harada--Norton inputs are alternatives, as are compressed catalogue files and their decompressed versions.

The Janko $J_3$ Atlas pair and the O'Nan matrix pair are recorded construction provenance, not inputs to these fixed replays. The complete saved $J_3$ permutation witness is already charged. Classification proofs, full graphic constructions, historical source software and full formalization costs remain null, not zero. GAP, its algorithms and its catalogues remain explicit trust inputs; no measurement run re-executes the mathematics.

Any later written comparison must divide the two full originals by the whole common theory plus all applications. A source/application comparison is conditional on already acquiring the entire common theory and all required finite software and data, including both decoding drivers. A comparison including complete programs is separate. Neither short saved words nor a prior topic supplies a silent discount.
\newpage
\section*{Actual PDF glyphs and proposed graphic proxies}
Both source bodies are aligned to actual PDF font dictionaries, effective encodings, encoded bytes and rendered glyph outlines. Font names alone are not cache keys. N007 has twenty-two audited Type1 dictionaries and 569 used classes; N006 has twenty-three dictionaries and 698 classes. All thirty-four exceptional N007 and fifty exceptional N006 outline classes were inspected. All sixty-six PDF pages were visually read.

N007 retains the prior accepted 237 event substitutions. These include seven visible components decoded as whitespace; generated line breaks are distinguished from actual delimiter ink. Its rotated version stamp is returned once; one duplicate Form visitor callback is excluded from metadata only. N006 has no such duplicate callback or skipped Unicode font. Its version stamp uses an audited standard Type1 font. Every raw string agrees with uninstrumented pypdf extraction.

N006 has 356 proposed substitutions: 68 mathematical symbols and 288 graphical primitives. Thirty drawn circles each use eight separately encoded curved fragments, giving 240 events. Forty-four line strokes and four underbrace tips supply the remainder. N007 has 152 line-stroke events among its 237 substitutions. The proposed Unicode corner and line proxies preserve one counted component per event and record a direction. They are \textbf{not literal Unicode extraction}, exact arc-angle transcriptions or prices for connectivity, layout or the full graphic. The full geometry cost remains null. Distinct input review must decide compatibility with the existing primary convention before a factor can be admitted.

\begin{center}\begin{tabular}{lrrrr}\toprule
Source & Raw full & Raw selected & Proposed & Text-only\\\midrule
'''+sensitivity+r'''
\bottomrule\end{tabular}\end{center}
The extra text-only sensitivity replaces only identified graphical-proxy events by separators. Ordinary formula symbols and diagram labels remain. It does not assert that arbitrary unextracted graphics cost nothing, or that every graphical element is represented by these events. Both unchanged raw alternatives remain available. No theorem, missing label or intended formula is guessed.

The ordinary grid contains 240 PDF cells: eight documents, three extraction variants, two normalizations and five units. Twenty-eight full raw files give another 280 cells; the extra text-only sensitivity has eighty cells. The units are whitespace tokens, alphanumeric runs, nonspace characters, characters after whitespace collapse and UTF-8 bytes after that collapse. NFC and NFKC are both retained. These representation-sensitive lengths are not a universal difficulty metric.

The portable checker binds every PDF and scientific scope, recounts the cells, checks complete old-appendix inclusion and rejects boundary, glyph-event, program and attribution corruptions. It preserves the old N007 counts exactly. No primary PDF, extracted body text, font stream or raster is exported. The input author previously authored the two sporadic companions; input acceptance requires a distinct reviewer.
\end{document}
'''
(O/'input_reader.tex').write_text(tex)
