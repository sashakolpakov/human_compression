#!/usr/bin/env python3
from pathlib import Path
import argparse,json,os,subprocess,hashlib
from compute import need

def plot(r,out):
 os.environ['MPLCONFIGDIR']=str(out/'.mpl');os.environ['XDG_CACHE_HOME']=str(out/'.cache');import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.fonttype':'none','svg.hashsalt':'additional-two-whole-topics-v1'})
 fig,axes=plt.subplots(1,2,figsize=(9.8,3.4),layout='constrained');colors={'source':'#626c76','common':'#426b9a','application':'#70a59a','program':'#bd874e'};data=[]
 maximum=max(x['written_denominator']+x['document_costs']['program'] for x in r['primary'].values())
 for ax,(topic,row) in zip(axes,r['primary'].items()):
  d=row['document_costs'];patches=[('source',0,d['source'],0),('common-written',1,d['common'],0),('application-written',1,d['application'],d['common']),('common-printed',2,d['common'],0),('application-printed',2,d['application'],d['common']),('program',2,d['program'],row['written_denominator'])]
  for name,x,cost,bottom in patches:
   role=name.split('-')[0];gid='bar-'+topic+'-'+name;ax.bar(x,cost,bottom=bottom,color=colors[role],width=.58)[0].set_gid(gid);data.append(dict(id=gid,topic=topic,cost=cost,bottom=bottom,role=role))
  for x,y in [(0,d['source']),(1,row['written_denominator']),(2,row['written_denominator']+d['program'])]:ax.text(x,y+maximum*.025,f'{y:,}',ha='center',fontsize=8)
  ax.set_xticks([0,1,2],['Original','Our written\npapers','Our papers\n+ printed code']);ax.set_ylim(0,maximum*1.20);ax.set_title('Matching extensions' if topic=='Matching' else 'Chiral enumeration');ax.spines[['right','top']].set_visible(False);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
 axes[0].set_ylabel('NFC characters without whitespace')
 from matplotlib.patches import Patch
 fig.legend([Patch(color=colors[x]) for x in ['source','common','application','program']],['Original','Whole common theory','Complete application','Whole program appendix'],loc='outside lower center',ncol=4,frameon=False,fontsize=8)
 fig.savefig(out/'whole_costs.svg',metadata={'Date':None});fig.savefig(out/'whole_costs.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
 (out/'plot_data.json').write_text(json.dumps(dict(primary_only=True,bars=data,actual_rectangles=12,shared_y_limit=maximum*1.20),indent=2)+'\n')

def reader(r,out):
 p=r['primary'];fmt=lambda x:f"{float(x['decimal']):.3f}"
 drows=[]
 for topic,row in p.items():
  d=row['document_costs'];drows.append(('Matching (F015)' if topic=='Matching' else 'Chiral enumeration (L028)')+' & '+' & '.join(f'{d[x]:,}' for x in ['source','common','application','program'])+r' \\')
 frows=[]
 for topic,row in p.items():frows.append(('Matching' if topic=='Matching' else 'Chiral enumeration')+' & '+' & '.join(fmt(row['comparisons'][x]) for x in ['written','conditional_application','including_printed_programs','including_raw_programs'])+r' \\')
 urows=[]
 for label,unit in [('Whitespace tokens','whitespace_tokens'),('Alphanumeric runs','alphanumeric_units'),('Nonspace characters','characters_without_whitespace'),('Collapsed-space characters','characters_with_collapsed_whitespace'),('Collapsed-space UTF-8 bytes','utf8_bytes_with_collapsed_whitespace')]:
  vals=[]
  for topic in p:
   x=next(x for x in r['rows'] if (x['topic'],x['variant'],x['normalization'],x['unit'])==(topic,'calibrated_selected','NFC',unit));vals.extend([fmt(x['comparisons']['written']),fmt(x['comparisons']['conditional_application'])])
  urows.append(label+' & '+' & '.join(vals)+r' \\')
 text=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=24mm]{geometry}\usepackage{fontspec,unicode-math,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}\hypersetup{hidelinks}
\title{Two additional complete-manuscript comparisons}
\author{Human Compression Project}\date{11 October 2026}
\begin{document}\maketitle
These are two separate topics, each with a complete common paper and one complete application. The originals are Piedade's \emph{Infinite Families of Hypertopes from Centrally Symmetric Polytopes} (F015, final EJC edition, 21 pages), and Buekenhout--Leemans--Tranchida's \emph{A new algorithm to classify chiral polytopes with a given automorphism group} (L028, revised ULB author edition, 14 pages). The 64 detailed records describe these two accepted principal contracts; they are not 64 manuscripts. The earlier ten-topic, 27-original report is unchanged.

\paragraph{Whole topics and conditional applications.}
The primary unit is calibrated NFC characters excluding whitespace. Every authored page is included: front matter, references, source software and extractable diagram and table text remain. Only exact repeated page furniture is removed.
\begin{center}\begin{tabular}{lrrrr}\toprule
Topic & Original & Common & Application & Printed code\\\midrule
@DOCUMENT_ROWS@
\bottomrule\end{tabular}\end{center}
For each topic, let $L$ be the complete original, $U$ the whole common paper, $A$ the complete application, and $P$ the entire accompanying program bundle. We report
\[
 R_{\rm written}=\frac{c(L)}{c(U)+c(A)},\qquad
 r\mid(U,P)=\frac{c(L)}{c(A)}.
\]
The second comparison assumes that \emph{all of $U$ and all of $P$ have already been acquired}. It is not a whole-topic saving. Shared material is fully charged independently in each topic.
\begin{center}\begin{tabular}{lrrrr}\toprule
Topic & Whole written & Conditional & With printed code & With raw code\\\midrule
@FACTOR_ROWS@
\bottomrule\end{tabular}\end{center}
Matching is shorter as a complete written replacement in this unit, but slightly longer when its full code is included. Chiral enumeration is longer as a complete topic in this coordinate. Both individual applications are shorter once the full common acquisition has been paid. A factor below one means that the replacement costs more in the stated coordinate.

The complete raw program costs are 4,408 for Matching and 11,090 for chiral enumeration. Printed and raw software are alternative representations; they are never added together. Matching's exceptional-orbit GAP census is a finite proof premise. All three chiral programs are retained in full: reference enumeration, formula evaluation and independent involution-count validation. They do not replace the uniform written proof. Three operational drivers and two Lean files are inventoried separately; the fourteen Lean declarations do not establish end-to-end formalization.
\newpage
\begin{center}\includegraphics[width=\textwidth]{whole_costs.pdf}\end{center}
The bars charge the full common paper and application, followed by the complete program appendix where shown. There is only one application in each new topic; this does not establish a recurring sawtooth pattern or a minimum proof complexity.

\paragraph{Unit sensitivity.}
For calibrated selected text with NFC normalization:
\begin{center}\begin{tabular}{lrrrr}\toprule
 & \multicolumn{2}{c}{Matching} & \multicolumn{2}{c}{Chiral enumeration}\\
Unit & Whole & Conditional & Whole & Conditional\\\midrule
@UNIT_ROWS@
\bottomrule\end{tabular}\end{center}
The exact data retain all five units under NFC and NFKC for raw untrimmed, raw selected and calibrated selected text: 30 coordinates per topic and 240 fractions. Raw untrimmed counts keep page furniture on both sides. These alternatives matter: chiral enumeration is slightly shorter in whitespace tokens, but longer in nonspace characters and UTF-8 bytes. No unit-independent compression conclusion is asserted.

\paragraph{Scope, attribution and unknown costs.}
F015's intended finite families, defining presentations, orders and halved geometries are recovered with the accepted corrections. The printed 120-cell presentations omit twenty unordered-pair orbits and define infinite groups; the repaired finite presentations are kept distinct. The original extension/lattice theorem and stated toroid-coordinate descriptions remain attributed inputs. Incidental catalogue comparisons are excluded from the recovered principal contract, while their text remains in the whole-source numerator.

L028's complete connected chiral enumeration covers every finite input group and all ranks. Oriented and unrooted classes are distinguished; duality is not quotiented. The geometric reconstruction and almost-simple involution estimate remain attributed inputs. Source timings remain empirical observations. Corrected table entries and the regular-output qualification do not create an additional source or an open-question solution.

Full retained external proofs, unprovided historical software, graphic layout and complete formalization remain unknown, not zero. The source PDFs contain vector mathematical content; this text comparison does not price its complete visual information. The independently accepted input audit covers 68 pages, 240 PDF and 90 raw-file cells, 78 actual Type1 dictionaries and 1,358 glyph classes. Its 660 repairs preserve visible components. A code-wrap hook without an asserted exact Unicode equivalent retains its literal extracted comma, an explicit UTF-8 representation limitation. No source mathematics is rewritten by calibration.

This numerical packet requires distinct arithmetic, plot and reader review. It adds no mathematical or conjecture credit and does not alter the existing scientific contracts or earlier measurements.
\end{document}
'''
 for key,value in [('DOCUMENT_ROWS','\n'.join(drows)),('FACTOR_ROWS','\n'.join(frows)),('UNIT_ROWS','\n'.join(urows))]:text=text.replace('@'+key+'@',value)
 need('@' not in text,'all reader fields');(out/'measurement.tex').write_text(text)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--results',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();need(not a.out.exists(),'fresh render');a.out.mkdir(parents=True);r=json.loads(a.results.read_text());plot(r,a.out);reader(r,a.out)
 for i in range(2):
  x=subprocess.run([a.xelatex,'-no-shell-escape','-halt-on-error','-interaction=nonstopmode','measurement.tex'],cwd=a.out,capture_output=True,text=True,timeout=180);(a.out/f'render{i}.log').write_text(x.stdout+x.stderr);need(x.returncode==0,'clean render')
 text=(a.out/'measurement.log').read_text();bad=[x for x in text.splitlines() if any(w in x for w in ['Overfull','Missing character:','LaTeX Warning:'])];need(not bad,'no render diagnostics '+repr(bad))
 from pypdf import PdfReader
 pages=[p.extract_text() or '' for p in PdfReader(a.out/'measurement.pdf').pages];need(len(pages)==2,'two reader pages');report=dict(status='PASS',reader_pages=2,page_text_sha256=[hashlib.sha256(x.encode()).hexdigest() for x in pages],diagnostics=[]);(a.out/'render_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
