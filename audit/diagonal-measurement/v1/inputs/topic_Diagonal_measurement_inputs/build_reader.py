#!/usr/bin/env python3
from pathlib import Path
import json,argparse,subprocess,re
import pypdf
from font_tools import need,sha
H=Path(__file__).resolve().parent

def build(out,xelatex):
 c=json.loads((H/'author_counts.json').read_text());p=json.loads((H/'policy.json').read_text())
 n=lambda k:f"{c['documents'][k]['metrics']['calibrated_selected']['NFC']['characters_without_whitespace']:,}"
 raw=lambda category:list(c['raw_files'][category].values())
 rn=lambda r:f"{r['metrics']['NFC']['characters_without_whitespace']:,}"
 tex=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}\usepackage{fontspec}\setmainfont{STIXGeneral}\usepackage{unicode-math}\setmathfont{STIX Two Math}\usepackage{booktabs,array,hyperref}\hypersetup{hidelinks}\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\title{Complete length inputs for diagonal twistings}\author{Human Compression Project}\date{Input edition; no compression factor}
\begin{document}\maketitle
This packet measures one original manuscript, Piedade and Tranchida's \emph{Coset geometries acting on their elements: The $j$-diagonals twisting}, arXiv:2608.23223v1. The source has twelve physical pages. The replacement is the complete published common paper and its complete application, including the reviewed quotient repair. The thirty-two scientific clauses are not thirty-two manuscripts.

The scientific boundary is unchanged: both constructions, exact parabolics and doubled labels (including infinite labels), quotient variants under the stated hypertope hypothesis, the finite tree family, and the named classical comparisons. The question about arbitrary finite diagrams remains outside this result. N006 is background, with no whole-original credit here. Classical Coxeter and polytope inputs retain their explicit qualifications.

\begin{center}\begin{tabular}{lrr}\toprule
Complete document & Pages & NFC nonspace characters\\\midrule
N007 source & 12 & @SOURCE@\\
Common theory & 5 & @COMMON@\\
Application & 5 & @APP@\\
Complete validation appendix & 2 & @CODE@\\\bottomrule
\end{tabular}\end{center}
These are calibrated counts after removing only exact repeated headers, footers and physical page numbers. The source's title, authors, abstract, version stamp, acknowledgments, references, author addresses, and all extracted diagram text remain. All replacement front matter and references remain. The full common paper is charged to this topic; no other topic pays it on this topic's behalf.

The inventory also measures the entire raw validation program (@RAWCODE@ nonspace characters), two operational drivers (@DRIVER1@ and @DRIVER2@), and the Lean source (@LEAN@). The validation program is printed in full; zero uniform theorems depend on its finite samples. Its printed and raw forms are alternatives, never added together. Drivers are separate. Eight Lean declarations verify specific identities, not the entire geometric argument.

The fixed grid contains 120 PDF cells: four documents, three extraction variants, two normalizations and five units. Four whole raw files supply forty further cells. There is no compression factor in this input packet; a distinct input review must precede numerical comparisons.
\newpage
\section*{What the PDF extraction preserves}
Raw extraction is compared byte for byte with a separate, uninstrumented pypdf extraction. Instrumentation records metadata only. In the source, a left angle bracket is encoded by a byte decoded as a newline. The extractor therefore distinguishes the actual font event from line breaks inserted by pypdf. One visible left angle, one visible right angle and five visible vertical extensions survive calibration; none is treated as empty whitespace.

The rotated arXiv stamp is returned once, although its Form produces an extra visitor callback. Only this exact duplicate metadata callback is suppressed; the returned text and every measured variant retain the stamp once. The stamp's Unicode font is the sole exception to the actual Type1 body-glyph audit. All source body glyphs are matched to their PDF dictionary, effective encoding, byte and embedded outline. Identically named fonts are not merged.

The source audit contains 22 Type1 dictionaries and 569 used encoded glyph classes. Seventeen exceptional classes account for 237 literal substitutions. Actual outlines for all thirty-four classes requiring special scrutiny were viewed. They include delimiter components, a wide tilde, a display intersection, a script letter and the mapsto bar-and-stub component. Each visible component remains separate; no missing mathematical expression is guessed.

Four XYDASH classes encode diagonal stroke pieces in diagrams. Their substitutes record the direction of each visible stroke, not its precise angle, length or assembly into a graph. The drawing itself therefore has no complete text price. Mathematical meaning, full graphics, historical software, retained outside proofs and a complete formalization are not assigned zero cost: their unmeasured costs remain null.

\section*{Variants, checks and limits}
Every document has raw untrimmed, raw furniture-selected and calibrated furniture-selected variants. Each is counted under NFC and NFKC by whitespace tokens, alphanumeric runs, nonspace characters, characters after whitespace collapse and UTF-8 bytes after that collapse. These are representation-sensitive lengths, not a universal measure of mathematical difficulty. The designated primary input is calibrated selected NFC nonspace characters; the other twenty-nine coordinates remain available.

All twenty-four scientific and program pages were visually inspected. The checker reconstructs all cells and actual-font evidence from the pinned PDFs, verifies the complete program's presence, and rejects thirty boundary, glyph, scope and code corruptions. In particular it tests both directions of the delimiter problem: discarding a real bracket and inventing a bracket from a generated newline. It does not rerun GAP or Lean and does not readjudicate the independently accepted scientific result.

The portable replay requires the exact public scientific files and the separately supplied source PDF. No primary text, embedded font or source image is redistributed in this input packet. Source hashes, public routes, literal furniture boundaries, glyph-event identities and whole-file roles are explicit machine-readable inputs.
\end{document}
'''
 replacements={'SOURCE':n('N007'),'COMMON':n('U'),'APP':n('A1'),'CODE':n('CODE'),'RAWCODE':rn(raw('programs')[0]),'DRIVER1':rn(raw('drivers')[0]),'DRIVER2':rn(raw('drivers')[1]),'LEAN':rn(raw('formal')[0])}
 for k,v in replacements.items():tex=tex.replace('@'+k+'@',v)
 need(not re.search('@[A-Z]+@',tex),'reader placeholders resolved');out.mkdir(parents=True,exist_ok=False);(out/'input_reader.tex').write_text(tex)
 for i in range(2):
  r=subprocess.run([xelatex,'-interaction=nonstopmode','-halt-on-error','input_reader.tex'],cwd=out,text=True,capture_output=True);(out/f'pass{i}.log').write_text(r.stdout+r.stderr);need(r.returncode==0,'reader render')
 log=(out/'input_reader.log').read_text();need(not any(x in log for x in ['Overfull','Missing character','LaTeX Warning:','Package fontspec Warning']),'clean reader typography')
 pdf=out/'input_reader.pdf';pages=[x.extract_text() or '' for x in pypdf.PdfReader(pdf).pages];need(len(pages)==2,'two reader pages');need(all('\ufffd' not in x for x in pages),'reader glyphs')
 report=dict(status='PASS',pages=2,tex_sha256=sha(tex.encode()),pdf_sha256=sha(pdf.read_bytes()),page_text_sha256=[sha(x.encode()) for x in pages],diagnostics=[],actual_visual_review_separate=True)
 (out/'render_report.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();build(a.out,a.xelatex)
