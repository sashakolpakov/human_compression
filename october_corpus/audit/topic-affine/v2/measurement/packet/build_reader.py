#!/usr/bin/env python3
"""Render the complete affine comparison from the frozen numerical result."""
import argparse,json,os,subprocess,tempfile
from pathlib import Path
cache=Path(tempfile.gettempdir())/'human-compression-affine-plot-cache'
cache.mkdir(exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR',str(cache/'matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME',str(cache))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from compute import HERE,read,need

def tex_number(value):
    return f'{value:,}'.replace(',',r'\,')

def build(out):
    r=read(HERE/'results.json');p=r['primary'];d=p['document_costs']
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'affine-complete-costs-v1'})
    fig,ax=plt.subplots(figsize=(9,3.2))
    colors={'source':'#656d78','common':'#335f9e','application':'#2a9b9a','program':'#c87528'}
    ax.barh(2,d['L012'],color=colors['source'])
    for y in [1,0]:
        ax.barh(y,d['U_Affine'],color=colors['common'])
        ax.barh(y,d['AF1'],left=d['U_Affine'],color=colors['application'])
    ax.barh(0,d['CODE'],left=p['written_denominator'],color=colors['program'])
    totals=[p['comparisons']['including_printed_program']['denominator'],p['written_denominator'],d['L012']]
    for y,value in enumerate(totals):ax.text(value+650,y,f'{value:,}',va='center')
    ax.set_yticks([2,1,0],['Complete source','Our written papers','Our papers and programs'])
    ax.set_xlim(0,max(totals)*1.18)
    ax.set_xlabel('Calibrated NFC characters without whitespace')
    ax.grid(axis='x',alpha=.22);ax.set_axisbelow(True)
    for side in ['top','right','left']:ax.spines[side].set_visible(False)
    ax.legend(handles=[Patch(color=colors[k],label=label) for k,label in
        [('source','Source'),('common','Common theory'),('application','Application'),('program','Whole program appendix')]],
        loc='upper center',bbox_to_anchor=(.45,-.3),ncol=4,frameon=False)
    fig.tight_layout()
    for extension in ['pdf','svg','png']:
        metadata={'CreationDate':None,'ModDate':None} if extension=='pdf' else {'Date':None} if extension=='svg' else None
        fig.savefig(out/('costs.'+extension),bbox_inches='tight',dpi=150,metadata=metadata)
    plt.close(fig)
    source,common,application,code=(tex_number(d[k]) for k in ['L012','U_Affine','AF1','CODE'])
    written=tex_number(p['written_denominator']);printed=tex_number(p['comparisons']['including_printed_program']['denominator'])
    raw=tex_number(p['raw_program_cost']);rawden=tex_number(p['comparisons']['including_raw_program_alternative']['denominator'])
    text=r'''\documentclass[a4paper,11pt]{article}
\usepackage[margin=22mm]{geometry}
\usepackage{fontspec,amsmath,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}
\setlength{\emergencystretch}{2em}
\begin{document}
\begin{center}{\Large Affine constructions: complete manuscript costs}\\[4pt]
Human Compression project\end{center}
The source is Hou, Feng and Leemans, \emph{Regular 3-polytopes of order
$2^n p$}, arXiv:2001.02945v2, dated 14 July 2024. We compare its complete
seventeen pages with our complete seven-page common paper and nine-page
application. The exact admitted principal contract has thirty-three rows;
this measurement changes none of its mathematical conclusions.

\paragraph{The combined written comparison.}
Using calibrated NFC characters without whitespace, the costs are
\begin{center}\begin{tabular}{lr}\toprule
Complete document & Characters\\\midrule
Source L012 & @SOURCE@\\
Common theory $U_{\mathrm{Affine}}$ & @COMMON@\\
Application AF1 & @APPLICATION@\\
Whole program appendix & @CODE@\\\bottomrule
\end{tabular}\end{center}
The combined written ratio is
\[
 R_{\mathrm{written}}=\frac{@SOURCE@}{@COMMON@+@APPLICATION@}
 =\frac{@SOURCE@}{@WRITTEN@}=@R_WRITTEN@.
\]
Thus the complete written replacement is longer than the source by this
measure. The common paper is charged in full in this topic, including
arguments also available in another topic. It is not discounted because
they were previously proved or counted elsewhere.

\paragraph{The result after acquiring the common material.}
Once the whole common paper and all six complete required programs are
available, the source/application ratio is
\[
 R_{\mathrm{conditional}}=\frac{@SOURCE@}{@APPLICATION@}=@R_CONDITIONAL@.
\]
This is a shorter local application. It does not make the common paper
free in the combined comparison. Titles, context, references, complete
proofs and all local hypotheses remain in every measured document.

\begin{center}\includegraphics[width=\linewidth]{costs.pdf}\end{center}
\newpage
\paragraph{The complete program boundary.}
The eight-page appendix prints six whole mathematical programs, including
their embedded diagnostics. It is required material in the accepted
scientific edition. Adding it once gives
\[
 R_{\mathrm{programs}}=\frac{@SOURCE@}{@WRITTEN@+@CODE@}
 =\frac{@SOURCE@}{@PRINTED@}=@R_PROGRAMS@.
\]
The six complete raw files cost @RAW@ characters. Substituting this
representation for the printed appendix gives
\[
 R_{\mathrm{raw}}=\frac{@SOURCE@}{@RAWDEN@}=@R_RAW@.
\]
The two program representations are alternatives. They are never both
added to the denominator, and no diagnostic fragment is pruned.

Three auxiliary scripts are inventoried separately: the replay driver,
the checks for changed input files and the finite hypothesis diagnostics.
They cost @AUXILIARY@ characters in the same NFC coordinate. The original
scientific metadata lists two different pairs; the inventory records
their union of all three files without changing the scientific edition.
The three supporting Lean files cost @FORMAL@ characters and are separately
recorded as formal validation. These costs are not silently added to a
mathematical manuscript or to the program appendix.

\paragraph{What is included and what remains unknown.}
The numerator is the whole source manuscript for the admitted principal
contract. It does not assert recovery of every auxiliary assertion.
General Problem 1.1, the separate full Table 1 census and the ancillary
uniqueness claim for the two order-384 seeds remain outside that contract.
The source sign correction and all retained external theorems keep their
existing attribution and qualifications. This measurement adds no credit for another source or a solved question.

The independent input review counted all forty-one physical PDF pages.
Only page numbers and repeated running headers are removed. It checked
114 glyph substitutions against the actual encoded bytes and embedded
fonts, and inspected every proposed furniture exclusion. Printed hyphens,
formula ordering and extraction spacing are preserved. The same complete
costs are supplied for three extraction policies, NFC and NFKC, and five
length units: thirty coordinates in all. The CSV tables contain ninety
combined fractions and thirty conditional fractions.

The source's 163 inline graphic marks have an unknown graphic and layout
cost. Its original program files are unavailable. Expanded external
proofs, the SmallGroups catalogue and the construction of exact group
algorithms also have unknown acquisition costs. None is assigned zero.
Consequently these are declared text and program comparisons, not a
measure of all visible mathematical information or research effort.

Nine existing Lean declarations verify specified quotient, period and
sign statements. They do not formalize the entire source contract.
Paired proof dependencies and exclusive passage costs are still pending.
The numerical packet awaits independent arithmetic and reader review;
its input boundary has already been independently accepted.
\end{document}
'''
    values={'SOURCE':source,'COMMON':common,'APPLICATION':application,'CODE':code,'WRITTEN':written,
            'PRINTED':printed,'RAW':raw,'RAWDEN':rawden,
            'R_WRITTEN':f"{p['comparisons']['written_papers']['factor']:.6f}",
            'R_CONDITIONAL':f"{p['per_result'][0]['factor']:.6f}",
            'R_PROGRAMS':f"{p['comparisons']['including_printed_program']['factor']:.6f}",
            'R_RAW':f"{p['comparisons']['including_raw_program_alternative']['factor']:.6f}",
            'AUXILIARY':tex_number(p['separate_auxiliary_cost']),'FORMAL':tex_number(p['separate_formal_cost'])}
    for key,value in values.items():text=text.replace('@'+key+'@',value)
    need('@' not in text,'all table placeholders resolved')
    (out/'measurement.tex').write_text(text)
    for _ in range(2):
        command=['/opt/homebrew/bin/xelatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','measurement.tex']
        result=subprocess.run(command,cwd=out,capture_output=True,text=True)
        need(result.returncode==0,result.stdout+result.stderr)
    log=(out/'measurement.log').read_text()
    diagnostics=[line for line in log.splitlines() if any(token in line for token in ['Overfull','Missing character','LaTeX Warning'])]
    need(not diagnostics,'render diagnostics: '+repr(diagnostics))
    from pypdf import PdfReader
    pages=PdfReader(out/'measurement.pdf').pages
    need(len(pages)==2,'two-page reader')
    report=dict(status='PASS_READER_RENDER',pages=len(pages),diagnostics=diagnostics,
                primary_input=r['primary'],mathematical_replay=False,real_browser_claim=False)
    (out/'render_report.json').write_text(json.dumps(report,indent=2)+'\n')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(),'fresh render directory')
    args.out.mkdir(parents=True);build(args.out)
    print('PASS: two-page reader and complete-cost figure rendered without diagnostics.')

if __name__=='__main__':main()
