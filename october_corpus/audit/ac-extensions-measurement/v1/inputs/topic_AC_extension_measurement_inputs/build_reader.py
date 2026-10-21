#!/usr/bin/env python3
from pathlib import Path
import json,argparse,subprocess,re
import pypdf
from font_tools import need,sha
H=Path(__file__).resolve().parent

def build(out,xelatex):
 c=json.loads((H/'author_counts.json').read_text())
 labels={'L128':'L128: diagram symmetries','L068':'L068: Livingstone graph','A7':'A: seventh application','A_CODE_NEW':'A: complete new program','U_C_INC':'C: complete incidence note','C5':'C: fifth application','C_CODE_NEW':'C: complete additional program'}
 rows='\n'.join(labels[k]+' & '+str(r['pages'])+' & '+f"{r['metrics']['raw_untrimmed']['NFC']['characters_without_whitespace']:,}"+' & '+f"{r['metrics']['calibrated_selected']['NFC']['characters_without_whitespace']:,}"+r'\\' for k,r in c['documents'].items())
 raw=lambda cat:[f"{v['metrics']['NFC']['characters_without_whitespace']:,}" for v in c['raw_files'][cat].values()]
 tex=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}\usepackage{fontspec}\setmainfont{STIXGeneral}\usepackage{unicode-math}\setmathfont{STIX Two Math}\usepackage{booktabs,array,hyperref}\hypersetup{hidelinks}\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\title{Complete length inputs for additions to Topics A and C}\author{Human Compression Project}\date{Input edition; no compression factor}
\begin{document}\maketitle
This packet adds two original manuscripts to existing topics: Leemans--Spiga--Tranchida, \emph{Hypertopes with prescribed diagram symmetries}, arXiv:2610.09711v1 (L128, nine pages); and Hartley--Hubard--Leemans, \emph{Regular 4-polytopes from the Livingstone graph of Janko's first group}, Journal of Algebraic Combinatorics 35 (2012), 193--214 (L068, twenty-two pages). The accepted maps contain fourteen and seventeen clauses, respectively; these are not thirty-one manuscripts.

Topic A retains its whole common paper, all six previous applications and the complete earlier program bundle, then adds the seventh application and its whole finite search. Topic C retains its whole common paper and all four previous applications. The complete two-page incidence note is added to its common theory, followed by the complete fifth application. There is no new topic and no discount across topics.

\begin{center}\small\begin{tabular}{lrrr}\toprule
Complete document & Pages & Raw untrimmed & Calibrated selected\\\midrule
@ROWS@
\bottomrule\end{tabular}\end{center}
The displayed unit is NFC nonspace characters. Topic A retains its calibrated-selected primary coordinate. Topic C retains its accepted primary representation: the complete literal rendering of L108 and raw untrimmed PDF extraction for every other document, including these additions. Selected and calibrated variants remain separate sensitivities; this packet does not silently change the representation of the older sources.

The new whole raw programs have @A_RAW@ and @C_RAW@ nonspace characters. Topic C's existing construction program (@SHARED@) is byte-identical in both locations and is paid once. The earlier exhaustive J1 census remains paid in full, although this new application does not need it. Printed software cost is the old complete appendix plus the new complete appendix; raw whole files are an alternative, never an additional duplicate charge.

Three operational drivers (@D1@, @D2@, @D3@) and two Lean files (@F1@, @F2@) are separately inventoried. Their nine declarations verify specific common interfaces; they do not formalize either complete source theorem. The seven PDFs supply 210 cells across thirty coordinates, and eight raw files supply eighty cells. There is no compression factor before distinct input acceptance.
\newpage
\section*{Exact source and proof boundaries}
The L128 application preserves the graph construction, diagram realization, correlation quotient and finite rank-three minimum. The final proper-quotient assertion requires preservation of the same diagram; that qualification remains visible. Frucht's theorem, the small-group classification and GAP's exact algorithms remain retained inputs. The full new finite search is required for the unrestricted minimum, not for the uniform construction.

The L068 application recovers the second printed construction and an explicitly corrected first construction, with their complete face counts and stabilizer lattices. It retains the literal counterexample, the missing compatibility condition, and the qualification of Proposition 3.3. Named J1 data, the Livingstone graph identification and classical subgroup facts remain explicit. The new whole finite program checks the entire source-object incidence construction; the existing construction and exhaustive census programs remain in the full Topic C bundle. No new scientific or conjecture credit is assigned.

\section*{Literal extraction and visible glyphs}
Every physical page is included. Selected variants remove only exact repeated running headers, isolated footers and page numbers. Titles, authors, dates, DOI, version stamp, acknowledgments, references, publisher information, L128 margin reference labels and extracted diagram text remain. Untrimmed variants remove nothing.

Raw text is compared with an independent uninstrumented pypdf extraction. Metadata instrumentation distinguishes generated line breaks from actual glyph events. The L128 arXiv Form produces a duplicate visitor callback, but the returned stamp occurs once and remains in every variant. Seven visible delimiter components decoded as form feeds are retained as visible components. They are not discarded as whitespace.

The audit matches actual font dictionaries, effective encodings, bytes and outlines: 36 dictionaries and 805 used classes, with 27 exceptional classes and 286 replacements. All 56 classes requiring special scrutiny were viewed. L068's single envelope glyph is decoded as seven literal characters; calibration replaces that entire one-glyph span by one envelope, never seven envelopes. Script letters and separate arrow-bar pieces are retained as their observed outlines, without guessing a missing formula. An omitted CFF charset uses its specified ISOAdobe default; the PDF's explicit MacRoman encoding and differences are applied before matching actual events.

The new program appendix has visible line-wrap hooks; its measured text keeps them literally. The literal comma used by extraction for a hook remains a representation limitation. L068's full-page subgroup-lattice image is not a text reconstruction. Full graphics, historical software, retained outside proofs and a complete formalization have unknown costs, not zero costs.

\section*{Replay and review}
All forty-eight source, replacement and program pages were visually inspected. The portable checker reconstructs all 290 cells, matches full program inclusion and actual-font evidence, and rejects 36 boundary, glyph, code and topic-closure corruptions. The grid uses raw untrimmed, raw selected and calibrated selected text, NFC and NFKC, and five units: tokens, alphanumeric runs, nonspace characters, collapsed characters and collapsed UTF-8 bytes. These are representation-sensitive lengths, not a universal measure of mathematical difficulty.

Scientific acceptance is retained; GAP and Lean are not rerun. Replay needs the exact public files and two supplied primary PDFs. Primary text, font bytes and source images are not redistributed.
\end{document}
'''
 repl={'ROWS':rows,'A_RAW':raw('new_programs')[0],'C_RAW':raw('new_programs')[1],'SHARED':raw('shared_existing')[0],'D1':raw('drivers')[0],'D2':raw('drivers')[1],'D3':raw('drivers')[2],'F1':raw('formal')[0],'F2':raw('formal')[1]}
 for k,v in repl.items():tex=tex.replace('@'+k+'@',v)
 need(not re.search('@[A-Z_]+@',tex),'reader substitutions');out.mkdir(parents=True,exist_ok=False);(out/'input_reader.tex').write_text(tex)
 for i in range(2):
  r=subprocess.run([xelatex,'-interaction=nonstopmode','-halt-on-error','input_reader.tex'],cwd=out,text=True,capture_output=True);(out/f'pass{i}.log').write_text(r.stdout+r.stderr);need(r.returncode==0,'reader render')
 log=(out/'input_reader.log').read_text();need(not any(x in log for x in ['Overfull','Missing character','LaTeX Warning:','Package fontspec Warning']),'clean reader typography')
 pdf=out/'input_reader.pdf';pages=[x.extract_text() or '' for x in pypdf.PdfReader(pdf).pages];need(len(pages)==2,'two reader pages')
 report=dict(status='PASS',pages=2,tex_sha256=sha(tex.encode()),pdf_sha256=sha(pdf.read_bytes()),page_text_sha256=[sha(x.encode()) for x in pages],diagnostics=[],actual_visual_review_separate=True)
 (out/'render_report.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();build(a.out,a.xelatex)
