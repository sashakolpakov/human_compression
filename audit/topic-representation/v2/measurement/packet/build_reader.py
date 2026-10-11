#!/usr/bin/env python3
"""Readable full-document Representation costs; no source text is exported."""
import argparse, hashlib, json, os, re, subprocess
from pathlib import Path
from compute import UNITS, read, need, write

def plot(r,out):
    os.environ['MPLCONFIGDIR']=str(out/'.matplotlib');os.environ['XDG_CACHE_HOME']=str(out/'.cache')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.hashsalt':'representation-complete-documents-v1'})
    c=r['primary']['document_costs'];fig,(ax,bx)=plt.subplots(1,2,figsize=(9.4,3.15),layout='constrained')
    colors={'source':'#686868','common':'#426b9a','app':'#70a59a','validation':'#bd874e'}
    ax.bar(0,c['F010'],color=colors['source'],label='Source')
    for x in [1,2]:
        ax.bar(x,c['U_R'],color=colors['common'],label='Common theory' if x==1 else None)
        ax.bar(x,c['R1'],bottom=c['U_R'],color=colors['app'],label='Application' if x==1 else None)
    ax.bar(2,c['CODE'],bottom=c['U_R']+c['R1'],color=colors['validation'],label='Validation appendix')
    totals=[c['F010'],c['U_R']+c['R1'],c['U_R']+c['R1']+c['CODE']]
    top=max(totals);ax.set_ylim(0,top*1.20)
    for x,v in enumerate(totals):ax.text(x,v+top*.018,f'{v:,}',ha='center',fontsize=9)
    ax.set_xticks([0,1,2],['Source','Written papers','With validation']);ax.tick_params(axis='x',labelsize=8)
    ax.set_ylabel('NFC characters without whitespace');ax.set_title('Whole document totals')
    ax.legend(ncol=2,loc='upper center',bbox_to_anchor=(.5,-.12),frameon=False,fontsize=7)
    keys=['U_R','R1','CODE'];bars=bx.bar(range(3),[c[k] for k in keys],color=[colors['common'],colors['app'],colors['validation']])
    top=max(c[k] for k in keys);bx.set_ylim(0,top*1.20)
    for b,k in zip(bars,keys):bx.text(b.get_x()+b.get_width()/2,c[k]+top*.02,f'{c[k]:,}',ha='center')
    bx.set_xticks(range(3),['Common theory','Application','Validation appendix']);bx.tick_params(axis='x',labelsize=8);bx.set_title('Complete replacement components')
    for a in [ax,bx]:a.spines[['top','right']].set_visible(False);a.grid(axis='y',alpha=.2);a.set_axisbelow(True)
    fig.savefig(out/'complete_costs.svg',metadata={'Date':None});fig.savefig(out/'complete_costs.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
    return dict(axes_start_at_zero=True,total_bars=totals,component_bars=[c[k] for k in keys],source_cost=c['F010'],common_cost=c['U_R'],application_cost=c['R1'],printed_validation=c['CODE'],raw_code_not_added=True,sawtooth_claim=False)

def reader(r,out):
    p=r['primary'];c=p['document_costs'];raw=p['raw_costs'];factor=lambda name:f"{float(p['comparisons'][name]['decimal']):.6f}"
    rows=[]
    for u,label in zip(UNITS,['Whitespace words','Alphanumeric units','Nonspace characters','Characters, spaces collapsed','UTF-8 bytes, spaces collapsed']):
        x=next(x for x in r['coordinates'] if (x['variant'],x['normalization'],x['unit'])==('calibrated_selected','NFC',u))
        rows.append(label+' & '+' & '.join(f"{float(x['comparisons'][k]['decimal']):.3f}" for k in ['written_papers','conditional_application','including_printed_validation'])+r' \\')
    text=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=27mm]{geometry}
\usepackage{fontspec,unicode-math,booktabs,graphicx,array}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\begin{document}
\begin{center}\Large Recognizable extensions:\\complete manuscript costs\end{center}

The source is Antonio Díaz Ramos, Rémi Molinier and Antonio Viruel,
\emph{Every finite group is represented by a finite incidence geometry},
arXiv:2511.02410v2 (16 December 2025), thirteen pages. The accepted
principal contract contains six source blocks and thirteen current proof
contexts. It preserves the stated corrections and exclusions; it does
not claim recovery of every historical auxiliary assertion.

\textbf{Written papers.}
The primary ruler is calibrated NFC characters without whitespace.
Titles, abstracts, body, references, author information and extractable
figure labels remain counted. Only exact running furniture is removed.
\begin{center}\begin{tabular}{lrr}\toprule
Complete document & Pages & Characters\\\midrule
Source F010 & 13 & @F010@\\
Common theory $U_R$ & 5 & @U_R@\\
Application R1 & 5 & @R1@\\
Complete validation appendix & 4 & @CODE@\\\bottomrule
\end{tabular}\end{center}
The combined comparison pays for the whole common paper and application:
\[
 R_{\rm written}=\frac{@F010@}{@U_R@+@R1@}
 =\frac{@F010@}{@WRITTEN@}=@WR@.
\]
After acquiring the whole common paper and both complete validation
programs, the conditional source/application comparison is
\[
 r_1\mid(U_R,P_R)=\frac{@F010@}{@R1@}=@CR@.
\]
The conditional factor does not discard the acquisition cost. Other
topics pay their own common theory in full, even where it overlaps.

\textbf{Including the validation programs.}
Neither program is a premise of the uniform written proof. Both remain
complete in the separate comparison. With the printed appendix,
\[
 R_{\rm printed}=\frac{@F010@}{@WRITTEN@+@CODE@}
 =\frac{@F010@}{@PRINTEDTOTAL@}=@PR@.
\]
The two whole raw files instead cost @RAW@ characters, giving
$@F010@/@RAWTOTAL@=@RR@$. These representations are alternatives,
never simultaneous charges. Two complete historical drivers cost
@DRIVERS@ characters separately. Two full Lean files cost @LEAN@
characters separately and contain eight generic and four reused local
declarations; they do not formalize the complete application.

\newpage
\begin{center}\includegraphics[width=\textwidth]{complete_costs.pdf}\end{center}
Both axes start at zero and every bar charges its complete documents.
The written difference in this ruler is only @DIFFERENCE@ characters;
the replacement including validation is longer than the source. A
single application supplies no evidence of a recurring sawtooth pattern.

\textbf{Sensitivity.}
For calibrated selected text in NFC:
\begin{center}\begin{tabular}{lrrr}\toprule
Unit & Written & Conditional & With appendix\\\midrule
@ROWS@
\bottomrule\end{tabular}\end{center}
The UTF-8 written factor is below one: the small written saving is not
stable across these units. The full JSON and CSV retain all five units
under NFC and NFKC, each for untrimmed raw, selected raw and calibrated
selected text: thirty coordinates and 120 exact fractions. Printed
hyphens, code continuation marks and actual whitespace are preserved.

\textbf{Scope and retained costs.}
The current proofs correct the chamber degrees to $r-1$ and
$d(v)(r-1)$, the completed hexagon pair to $(D_{12},S_3)$, and the
symmetric-family minimum-degree statement to $n\geq3$. There is no
universal rank-two representation or blanket
$(S_n,A_n)=(\operatorname{Aut}(A_n),\operatorname{Inn}(A_n))$ claim.
The original Theorem A already answers Question 2.4; no new question
answer is claimed here.

The accepted independent input audit checked all 27 pages, 120 PDF
metric cells, sixty separate raw-file cells and 566 glyph classes in
26 actual font dictionaries. Its 134 visible-glyph repairs include
three byte-9 right braces; actual whitespace is otherwise preserved.
The four mapsto strokes remain separate from adjacent arrows. The ruler
uses pypdf 6.13.0 and FontTools 4.63.0. Source vector figures, edges,
colors and formula placement are not fully represented by extracted
text. Their cost, external proofs, historical software and operational
engineering remain unknown, not zero. These factors describe the
declared text representation, not total research effort or minimum
proof complexity. Independent numerical review is required before
publication.
\end{document}
'''
    vals={**c,'WRITTEN':p['written_denominator'],'WR':factor('written_papers'),'CR':factor('conditional_application'),
          'PR':factor('including_printed_validation'),'RR':factor('including_raw_validation_alternative'),
          'RAW':raw['complete_validation_programs'],'RAWTOTAL':p['written_denominator']+raw['complete_validation_programs'],
          'PRINTEDTOTAL':p['written_denominator']+c['CODE'],'DRIVERS':raw['complete_operational_drivers'],
          'LEAN':raw['complete_formal_files'],'DIFFERENCE':c['F010']-p['written_denominator'],'ROWS':'\n'.join(rows)}
    for k,v in vals.items():text=text.replace('@'+k+'@',str(v))
    need('@' not in text,'all reader substitutions');(out/'measurement.tex').write_text(text)

def main():
    p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=p.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh reader directory');a.out.mkdir(parents=True)
    r=read(a.results);plots=plot(r,a.out);reader(r,a.out)
    for i in [1,2]:
        run=subprocess.run([a.xelatex,'-no-shell-escape','-interaction=nonstopmode','-halt-on-error','measurement.tex'],cwd=a.out,capture_output=True,text=True,timeout=180)
        (a.out/f'render{i}.log').write_text(run.stdout+run.stderr);need(run.returncode==0,'XeLaTeX failed')
    log=(a.out/'measurement.log').read_text();bad=[s for s in log.splitlines() if re.search(r'Overfull|Underfull|Missing character|LaTeX Warning|Package .* Warning|^!',s)];need(not bad,'render diagnostics '+repr(bad))
    from pypdf import PdfReader
    pages=[p.extract_text() or '' for p in PdfReader(a.out/'measurement.pdf').pages]
    need(len(pages)==2,'two readable pages')
    for t in pages:need('\ufffd' not in t and not any(0xE000<=ord(c)<=0xF8FF for c in t),'no unrendered reader glyph')
    report=dict(status='PASS_AUTHOR_READER_RENDER',pages=len(pages),plot=plots,
                page_text_sha256=[hashlib.sha256(t.encode()).hexdigest() for t in pages],
                source_sha256=hashlib.sha256((a.out/'measurement.tex').read_bytes()).hexdigest(),
                pdf_sha256=hashlib.sha256((a.out/'measurement.pdf').read_bytes()).hexdigest(),
                diagnostics=[],visual_review='Separate, not implied by compilation')
    write(a.out/'render_report.json',report);print(json.dumps(report))

if __name__=='__main__':main()
