#!/usr/bin/env python3
"""Readable complete-document comparison; no proof-complexity inference."""
import argparse,json,os,hashlib,subprocess
from pathlib import Path
from compute import need,read,write,UNITS

def plot(r,out):
    os.environ['MPLCONFIGDIR']=str(out/'.matplotlib');os.environ['XDG_CACHE_HOME']=str(out/'.cache')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.fonttype':'none','svg.hashsalt':'chamber-full-documents'})
    p=r['primary'];d=p['documents'];fig,axs=plt.subplots(1,2,figsize=(10,3.5),layout='constrained')
    left,right=axs;colors={'source':'#626c76','common':'#426b9a','application':'#70a59a','program':'#bd874e'}
    left.bar(0,p['source_sum'],color=colors['source'])[0].set_gid('bar-total-source')
    left.bar(1,d['U_H'],color=colors['common'],label='Whole common paper')[0].set_gid('bar-total-common')
    left.bar(1,d['H1']+d['H2'],bottom=d['U_H'],color=colors['application'],label='Both applications')[0].set_gid('bar-total-applications')
    left.set_xticks([0,1],['Sources','Our written papers']);left.set_ylabel('NFC characters without whitespace')
    ymax=max(p['source_sum'],p['written_denominator']);left.set_ylim(0,ymax*1.20)
    for x,y in [(0,p['source_sum']),(1,p['written_denominator'])]:left.text(x,y+ymax*.025,f'{y:,}',ha='center')
    left.legend(loc='upper center',bbox_to_anchor=(.5,-.12),frameon=False,ncol=1,fontsize=8);left.set_title('Complete written documents')
    keys=['U_H','L008','H1','N016','H2','CODE'];c=[colors[k] for k in ['common','source','application','source','application','program']]
    bars=right.bar(range(len(keys)),[d[k] for k in keys],color=c)
    for bar,k in zip(bars,keys):
        bar.set_gid('bar-component-'+k);right.text(bar.get_x()+bar.get_width()/2,d[k]+max(d.values())*.025,f'{d[k]:,}',ha='center',fontsize=8)
    right.set_xticks(range(6),['Common','L008','H1','N016','H2','Code']);right.set_ylim(0,max(d.values())*1.22);right.set_title('Each complete component')
    for ax in axs:ax.spines[['right','top']].set_visible(False);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
    fig.savefig(out/'complete_costs.pdf',metadata={'CreationDate':None,'ModDate':None});fig.savefig(out/'complete_costs.svg',metadata={'Date':None});plt.close(fig)

def reader(r,out):
    p=r['primary'];d=p['documents'];rc=p['raw_costs'];fmt=lambda x:f"{float(x['decimal']):.3f}"
    rows=[];labels=['Whitespace words','Alphanumeric units','Nonspace characters','Characters, collapsed spaces','UTF-8 bytes, collapsed spaces']
    for label,unit in zip(labels,UNITS):
        row=next(x for x in r['coordinates'] if (x['variant'],x['normalization'],x['unit'])==('calibrated_selected','NFC',unit))
        rows.append(label+' & '+' & '.join(fmt(x) for x in [row['combined']['written'],row['conditional']['L008']['comparison'],row['conditional']['N016']['comparison']])+r' \\')
    text=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=0.8in]{geometry}
\usepackage{fontspec,unicode-math,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\title{Chamber orbits and regular covers:\\complete manuscript costs}
\author{Human Compression project}\date{}
\begin{document}\maketitle
The sources are Zhang and Leemans, \emph{Testing chirality on hypertopes}
(L008, arXiv 2511.14562v1, November 2025), and Cunningham,
\emph{Chiral polytopes whose smallest regular cover is a polytope} (N016, the eight-page
25 July 2023 author edition). N016's publisher PDF was not available.
We compare two complete source manuscripts with the complete common
paper and both applications. The 27 detailed records describe these two
principal contracts; they are not 27 manuscripts.

\paragraph{Whole topic and individual applications.}
The primary unit is calibrated NFC characters without whitespace. Exact
running headers and page numbers are removed; titles, abstracts, references,
source code and extractable tables remain included.
\begin{center}\begin{tabular}{lrr}\toprule
Complete document & Pages & Characters\\\midrule
Source L008 & 10 & @L008@\\
Source N016 & 8 & @N016@\\
Common theory $U_H$ & 6 & @U_H@\\
Chirality application H1 & 3 & @H1@\\
Regular-cover application H2 & 6 & @H2@\\
Whole two-program appendix & 3 & @CODE@\\\bottomrule
\end{tabular}\end{center}
The whole-topic written comparison is
\[
 R_{\mathrm{written}}=\frac{@L008@+@N016@}{@U_H@+@H1@+@H2@}
 =\frac{@SOURCE@}{@WRITTEN@}=@RW@.
\]
The complete written replacement is slightly longer in this unit. Once the
\emph{whole common paper and both complete programs} have been acquired,
the conditional comparisons are
\[
 r_1\mid(U_H,P_H)=\frac{@L008@}{@H1@}=@R1@,\qquad
 r_2\mid(U_H,P_H)=\frac{@N016@}{@H2@}=@R2@.
\]
Both applications are shorter than their matched sources in this unit, but
these conditional factors do not pay for the common acquisition again.
Every topic pays for its own whole common theory even when proofs overlap.

\paragraph{Complete programs and the limits of the comparison.}
The GAP program is a premise for the six finite groups and their maps;
the Python program validates separately proved action formulas. Both files
are charged in full. Including their printed appendix gives
$@SOURCE@/(@WRITTEN@+@CODE@)=@RP@$. The raw files instead cost @RAWCODE@
(@REQUIRED@ required; @DIAGNOSTIC@ diagnostic), giving
$@SOURCE@/@WITHRAW@=@RR@$. These representations are alternatives,
never added together. Three operational drivers cost @DRIVERS@ separately;
three Lean files cost @LEAN@ separately and contain fourteen scoped
component declarations, seven new and seven reused. This is not a complete
Lean verification of either application.
\newpage
\begin{center}\includegraphics[width=\textwidth]{complete_costs.pdf}\end{center}
The left panel pays for the whole common paper and both applications.
The right panel shows each complete document separately, including code.
These text lengths do not establish minimum proof complexity or a recurring
sawtooth pattern.

\paragraph{Sensitivity to the measurement convention.}
For calibrated selected text with NFC normalization:
\begin{center}\begin{tabular}{lrrr}\toprule
Unit & Whole written & L008/H1 & N016/H2\\\midrule
@ROWS@
\bottomrule\end{tabular}\end{center}
All five units are retained under NFC and NFKC for raw untrimmed, raw
selected and calibrated selected text. The thirty coordinates provide
150 exact fractions: ninety whole-topic and sixty conditional. Small
factors near one should be read with this unit sensitivity, not as a claim
that every reasonable encoding gives the same conclusion.

\paragraph{What the source comparison covers.}
L008's principal finite chirality criterion is recovered. For infinite groups,
its numerical cardinality condition is replaced by the exact two-coset
condition. The printed source software and other ancillary claims are
outside the replacement contract, although their text remains in the
complete-source numerator. N016's proved conclusions are recovered for
its fixed author edition, including all five specified atomic families and
the six-group example. The correction excluding \emph{nonidentity} powers
and the retained Cunningham--Pellicer family classification remain explicit.

Standard geometric correspondences, the Schulte--Weiss section theorem,
the square-tessellation identification and that classification are retained
at their points of use. Their complete proof costs remain unknown, as do
unavailable historical software, graphics and formula layout. The later
unrestricted-cover answer and finite-rank extensions are separate results,
not unpriced premises here; all-rank finite minimal-cover multiplicity
remains unresolved. This measurement adds no source or question credit.

\paragraph{Input and review boundary.}
The independently accepted input audit covers all 36 pages, 180 PDF and
80 raw-file measurements, 34 actual font dictionaries and 893 used glyph
classes. It preserves 36 visible delimiter pieces and two bitmap bullets
among 217 occurrence repairs. Raw alternatives remain available. Extraction
uses pypdf 6.13.0 and fontTools 4.63.0; it does not measure complete visual
information. This numerical edition still requires distinct independent
arithmetic and reader review before publication.
\end{document}
'''
    values={**d,'SOURCE':p['source_sum'],'WRITTEN':p['written_denominator'],'RW':fmt(p['combined']['written']),'R1':fmt(p['conditional']['L008']['comparison']),'R2':fmt(p['conditional']['N016']['comparison']),'RP':fmt(p['combined']['including_printed_programs']),'RR':fmt(p['combined']['including_raw_programs']),'RAWCODE':rc['complete_mathematical_programs'],'REQUIRED':p['program_costs_by_role']['required'],'DIAGNOSTIC':p['program_costs_by_role']['diagnostic'],'WITHRAW':p['written_denominator']+rc['complete_mathematical_programs'],'DRIVERS':rc['complete_operational_drivers'],'LEAN':rc['complete_formal_files'],'ROWS':'\n'.join(rows)}
    for k,v in values.items():text=text.replace('@'+k+'@',str(v))
    need('@' not in text,'All reader values supplied');(out/'measurement.tex').write_text(text)

def main():
    p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=p.parse_args();need(not a.out.exists(),'Fresh render output');a.out.mkdir(parents=True);r=read(a.results);plot(r,a.out);reader(r,a.out)
    for i in range(2):
        x=subprocess.run([a.xelatex,'-no-shell-escape','-interaction=nonstopmode','-halt-on-error','measurement.tex'],cwd=a.out,capture_output=True,text=True,timeout=180);(a.out/f'render{i}.log').write_text(x.stdout+x.stderr);need(x.returncode==0,'Reader render')
    log=(a.out/'measurement.log').read_text();bad=[s for s in log.splitlines() if any(w in s for w in ['Overfull','Missing character:','LaTeX Warning:'])];need(not bad,'Render diagnostics '+repr(bad))
    from pypdf import PdfReader
    pages=[p.extract_text() or '' for p in PdfReader(a.out/'measurement.pdf').pages];need(len(pages)==2,'Exactly two reader pages')
    report={'status':'PASS_TWO_PAGE_RENDER','pages':len(pages),'page_text_sha256':[hashlib.sha256(x.encode()).hexdigest() for x in pages],'diagnostics':[],'visual_review_separate':True};write(a.out/'render_report.json',report);print(json.dumps(report))
if __name__=='__main__':main()
