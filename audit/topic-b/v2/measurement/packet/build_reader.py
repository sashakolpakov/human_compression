#!/usr/bin/env python3
"""Render the fixed Topic B comparison without assigning a missing source cost."""
import argparse,hashlib,json,re,subprocess,os,tempfile
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'hc-b-matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pypdf import PdfReader

HERE=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def need(ok,message):
    if not ok:raise ValueError(message)
def number(x):return 'unknown' if x is None else f'{x:,}'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args()
    need(not a.out.exists(),'fresh output directory');a.out.mkdir(parents=True)
    data=json.loads((HERE/'results.json').read_text());p=data['primary']
    need(p['overall_factor'] is None and p['unknown_source']=='N001' and
         data['all_four_applications_charged'],'unknown source and complete boundary')
    pairs=p['per_result'];need([r['source'] for r in pairs]==['N001','N003','N008','L030'],'all source pairs')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'human-compression-topic-b-v2'})
    fig,ax=plt.subplots(figsize=(8.3,3.0),layout='constrained')
    our=[p['common_theory']]+[r['application_cost'] for r in pairs]
    bars=ax.bar([i+.17 for i in range(5)],our,width=.32,color='#174e82',label='Common theory and applications')
    known=[(i+1,r['source_cost']) for i,r in enumerate(pairs) if r['source_cost'] is not None]
    old=ax.bar([i-.17 for i,_ in known],[v for _,v in known],width=.32,color='#984f24',label='Source manuscripts')
    for collection in (bars,old):
        for bar in collection:
            ax.annotate(f'{int(bar.get_height()):,}',(bar.get_x()+bar.get_width()/2,bar.get_height()),
                        xytext=(0,4),textcoords='offset points',ha='center',va='bottom',fontsize=8)
    ax.text(.83,.022,'unknown',transform=ax.get_xaxis_transform(),ha='center',va='bottom',fontsize=8,color='#555555')
    ax.set_xticks(range(5),['Common theory\nU','N001 / B1\n1998','N003 / B2\n2002','N008 / B3\n2005','L030 / B4\n2021'])
    ax.set_ylabel('Characters without whitespace (NFC)')
    ax.set_ylim(0,max(our+[v for _,v in known])*1.25)
    ax.spines[['top','right']].set_visible(False);ax.set_axisbelow(True);ax.grid(axis='y',alpha=.2)
    ax.legend(frameon=False,ncol=2,loc='upper left',fontsize=8)
    for suffix in ['svg','pdf','png']:fig.savefig(a.out/('costs.'+suffix),dpi=150,facecolor='white',metadata={'Creator':'Human Compression'} if suffix!='png' else {})
    plt.close(fig)
    table=[]
    for r in pairs:
        factor='unknown' if r['factor'] is None else f"{r['factor']:.3f}"
        table.append(f"{r['source']} / {r['application']} & {number(r['source_cost'])} & {number(r['application_cost'])} & {factor}\\\\")
    tex=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=22mm]{geometry}
\usepackage{amsmath,booktabs,graphicx,hyperref}
\usepackage{fontspec}
\setmainfont{STIXGeneral}
\setlength{\emergencystretch}{2em}
\title{Topic B: common theory and application costs}
\author{Human Compression project}
\date{}
\begin{document}
\maketitle
The common paper and four applications recover thirty declared clauses
from manuscripts by Buekenhout--Cara (1998), Cameron--Cara (2002),
Archer--Cara--Krempa (2005), and Garcia-Colin--Leemans (the fixed revised
manuscript associated with the 2021 publication). Their retained inputs,
source corrections and exclusions are unchanged by this measurement.

\section*{One complete topic and four conditional comparisons}
The common theory costs \textbf{@U@} characters. The four applications
cost \textbf{@APPS@}, giving the complete written denominator
\textbf{@DEN@}. These figures use NFC characters without whitespace in
complete extracted PDF text, after the exact corrections and furniture
exclusions described on the next page.

The three available source PDFs cost @KNOWN@ characters. The original PDF
for N001 is unavailable. If its unknown cost
is $x$, the overall comparison is
\[
 R_B=\frac{x+@MKNOWN@}{@MDEN@}.
\]
There is no numerical value for $R_B$ in this audit. B1 remains in the
denominator; N001 is neither dropped nor assigned zero length.

\begin{center}
\begin{tabular}{lrrr}
\toprule
Matched result & Source & Application & Conditional factor\\
\midrule
@TABLE@
\bottomrule
\end{tabular}
\end{center}
Each conditional factor assumes that the \emph{whole} common theory has
already been acquired. Its cost is charged once in the complete-topic
comparison above. Separate topics each pay their complete common theory,
even where their arguments overlap. No finite mathematical program is
required by this edition's uniform written proofs.

\begin{center}
\includegraphics[width=\textwidth]{costs.pdf}
\end{center}
The blank source entry for N001 means unknown; it has no assigned bar
height. The first stage is the common theory, followed by the four
applications. The graph records actual document lengths and makes no
claim of a general pattern of decreasing proof complexity.

\newpage
\section*{What is counted}
Every page is extracted with pypdf 6.13.0, in its original order.
Titles, abstracts, mathematical statements and proofs, references,
addresses, footnotes and unique publication information remain included.
Only the individually recorded running headers and printed page numbers
are removed. Printed hyphens remain; words are not joined across lines.
The five new scientific PDFs comprise 22 pages. The three available
source PDFs comprise 31 pages. Page counts are not used as the headline
length unit. The two-page scope reader supplies audit context and no
mathematical premise; it is identified separately.

The parser represents four pieces of large parentheses on N003 page 8 by
private-use characters. Each is replaced by its visually identified
Unicode hook, preserving four separate pieces. Four open diagram vertices
on L030 page 5 are extracted as the letter i in a circle font; each becomes
a circle character. Every occurrence is bound to its actual font,
page offset and surrounding text. No other substitutions are made.

These rules were checked symmetrically across all eight available source
and replacement PDFs. An independent program re-extracted all 53 pages and
matched all 240 length cells and 48 normalized text hashes. It used independent counting code and rejected changes to the retained text boundary,
page bindings, furniture and glyphs. The same PDF parser remains a shared
dependency of the two counts.

\section*{Units and sensitivity}
The full numerical ledger retains both NFC and NFKC normalization and
three text variants: the complete raw extraction, that extraction after
removing running furniture, and the selected text after glyph correction.
For each it records five units: whitespace-separated tokens, maximal runs
of letters and numbers, characters without whitespace, characters after
collapsing whitespace, and UTF-8 bytes after the same collapse. An underscore
separates such runs. Collapsing whitespace replaces each
internal run by one space and removes leading and trailing whitespace.
The ledger contains ninety exact known conditional fractions, together
with explicit unknown entries for N001 and the complete topic. The
headline coordinate above is fixed in advance of choosing a favorable
factor; all other coordinates remain available in \texttt{results.json}.

\section*{Limits and attribution}
These are lengths of the stated complete documents, not minimum proof
complexities or counts of every visible mark. L030 page 5 has vector graphs
whose edges and layout are not measured. Some graph labels extract despite
being obscured by the drawing. N008's bibliography underline strokes
extract as minus glyphs; they remain counted. N003's original PDF contains
repeated font dictionary keys; the source bytes and parser are fixed, and
its page and font extraction are bound rather than silently repaired.

The foundational Buekenhout--Cara--Dehon classification and the two
separate Whiston results remain substantial retained inputs. Cayley's
formula, the stated symmetric-group automorphism fact, the finite
$p$-group Frattini theorem, Zorn's lemma and elementary linear algebra
also remain explicit. Their expanded proof costs are unknown. Lean
compilation and finite hypothesis counterexamples are verification
infrastructure; they do not supply an omitted mathematical enumeration.
No complete source application is claimed to be formalized in Lean.

This audit preserves the existing source and question credits. The
mathematical admission and corrected source map specify the thirty
clauses being compared; this reader does not expand that scope.
\end{document}
'''
    for key,value in {'U':number(p['common_theory']),'APPS':number(p['all_applications']),
                      'DEN':number(p['complete_denominator']),'KNOWN':number(p['known_source_sum']),
                      'MKNOWN':number(p['known_source_sum']).replace(',', '{,}'),
                      'MDEN':number(p['complete_denominator']).replace(',', '{,}'),
                      'TABLE':'\n'.join(table)}.items():tex=tex.replace('@'+key+'@',value)
    (a.out/'measurement.tex').write_text(tex)
    for turn in (1,2):
        run=subprocess.run([a.xelatex,'-no-shell-escape','-interaction=nonstopmode','-halt-on-error','measurement.tex'],cwd=a.out,text=True,capture_output=True,timeout=180)
        (a.out/f'build-{turn}.log').write_text(run.stdout+run.stderr);need(run.returncode==0,'XeLaTeX failed')
    log=(a.out/'measurement.log').read_text();diagnostics=[s for s in log.splitlines() if re.search(r'Warning:|Overfull|Missing character:|Missing glyph',s)]
    need(not diagnostics,'unclean TeX diagnostics: '+repr(diagnostics))
    pages=[p.extract_text() for p in PdfReader(a.out/'measurement.pdf').pages]
    need(len(pages)==2,'reader must occupy two pages')
    expected=[number(p[k]) for k in ['common_theory','all_applications','complete_denominator','known_source_sum']]
    expected += [f"{r['factor']:.3f}" for r in pairs if r['factor'] is not None]
    need(all(t in ''.join(pages) for t in expected),'printed counts and factors')
    report=dict(status='PASS_RENDERED_CANDIDATE',results_sha256=sha(HERE/'results.json'),
        pages=len(pages),checked_primary_values=expected,diagnostics=diagnostics,
        text_hashes=[hashlib.sha256(p.encode()).hexdigest() for p in pages],
        artifacts=[dict(path=name,bytes=(a.out/name).stat().st_size,sha256=sha(a.out/name))
                   for name in ['measurement.tex','measurement.pdf','costs.svg','costs.pdf','costs.png']],
        actual_visual_review=False)
    (a.out/'render_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],pages=2,diagnostics=[])))
if __name__=='__main__':main()
