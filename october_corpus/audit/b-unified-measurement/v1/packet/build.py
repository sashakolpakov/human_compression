#!/usr/bin/env python3
"""Exact unified-B tables and two-page reader from accepted inputs only."""
from pathlib import Path
from decimal import Decimal
import argparse,csv,os,shutil,subprocess,unicodedata
from accounting import H,load,save,sha,need,compute,ORIGINALS

def tables(out,r):
 with (out/'costs.csv').open('w',newline='') as f:
  names=['variant','normalization','unit','source_sum','common_theory','all_applications','written_denominator','printed_program_cost','raw_program_cost','operational_driver_cost','partial_formal_cost']+[f'source_{k}' for k in ORIGINALS]+[f'application_{k}' for k in ORIGINALS];w=csv.DictWriter(f,fieldnames=names);w.writeheader()
  for z in r['rows']:
   row={k:z[k] for k in names[:11]};row.update({f'source_{k}':v for k,v in z['source_costs'].items()});row.update({f'application_{k}':v for k,v in z['applications'].items()});w.writerow(row)
 with (out/'fractions.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['variant','normalization','unit','comparison','numerator','denominator','reduced_numerator','reduced_denominator','decimal']);w.writeheader()
  for z in r['rows']:
   pairs=[('whole_'+k,v) for k,v in z['whole'].items()]+[('conditional_'+k,v) for k,v in z['conditional'].items()]+[('article_only_whole_'+k,v) for k,v in z['article_only_sensitivity']['whole'].items()]+[('article_only_L040_conditional',z['article_only_sensitivity']['L040_conditional'])]
   for name,v in pairs:w.writerow(dict(variant=z['variant'],normalization=z['normalization'],unit=z['unit'],comparison=name,**v))
 with (out/'raw_files.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['category','path','role','bytes','sha256','normalization','unit','cost']);w.writeheader();c=load(H/'inputs/author_counts.json');p=load(H/'protocol.json')
  for category,rows in c['raw_files'].items():
   for name,z in rows.items():
    for n in p['normalizations']:
     for unit in p['units']:w.writerow(dict(category=category,path=name,role=z['role'],bytes=z['bytes'],sha256=z['sha256'],normalization=n,unit=unit,cost=z['metrics'][n][unit]))

def plot(out,r):
 os.environ.setdefault('MPLCONFIGDIR',str(out/'plot-cache'));os.environ.setdefault('XDG_CACHE_HOME',str(out/'cache'))
 import matplotlib
 matplotlib.use('Agg');import matplotlib.pyplot as plt
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.hashsalt':'unified-B-five-originals'})
 p=r['primary'];fig,(a,b)=plt.subplots(2,1,figsize=(7.1,5.8),gridspec_kw={'height_ratios':[1,2.6]});fig.subplots_adjust(left=.28,right=.88,bottom=.10,top=.97,hspace=.60)
 vals=[p['source_sum'],p['written_denominator'],p['denominators']['including_printed_programs'],p['denominators']['including_raw_programs']];labels=['Five original texts','Whole written edition','With printed programs','With raw programs']
 a.barh(range(4),vals,color=['#738799','#397c86','#b68145','#b68145']);a.set_yticks(range(4),labels);a.invert_yaxis();a.set_xlim(0,max(vals)*1.2);a.set_xlabel('Complete-topic costs; program forms are alternatives')
 for y,x in enumerate(vals):a.text(x+1600,y,f'{x:,}',va='center')
 v=[p['common_theory']];names=['Whole common theory'];colors=['#645b89']
 for k in ORIGINALS:v.extend([p['source_costs'][k],p['applications'][k]]);names.extend([k+' original',k+' application']);colors.extend(['#738799','#397c86'])
 b.barh(range(len(v)),v,color=colors);b.set_yticks(range(len(v)),names);b.invert_yaxis();b.set_xlim(0,max(v)*1.2);b.set_xlabel('Complete paper costs, including context and references')
 for y,x in enumerate(v):b.text(x+700,y,f'{x:,}',va='center')
 for ax in [a,b]:ax.spines[['top','right']].set_visible(False);ax.grid(axis='x',color='#dddddd',linewidth=.5);ax.set_axisbelow(True)
 fig.savefig(out/'costs.svg',metadata={'Date':None});fig.savefig(out/'costs.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)

def reader(out,r):
 p=r['primary'];fmt=lambda n:f'{n:,}';d=lambda s:f'{Decimal(s):.6f}';names={'N001':'Inductively minimal geometries','N003':'Maximal symmetric markings','N008':'Frattini coordinate geometries','L030':'Disjoint-subset geometries','L040':'High-rank symmetric markings'}
 pairrows='\n'.join(k+': '+names[k]+' & '+fmt(p['source_costs'][k])+' & '+fmt(p['applications'][k])+' & '+d(p['conditional'][k]['decimal'])+r'\\' for k in ORIGINALS)
 sens=[]
 for v,name in [('raw_untrimmed','Complete raw text (primary)'),('raw_selected','Selected literal text'),('calibrated_selected','Selected calibrated text')]:
  z=next(z for z in r['rows'] if z['variant']==v and z['normalization']=='NFC' and z['unit']=='characters_without_whitespace');sens.append(name+' & '+fmt(z['source_sum'])+' & '+fmt(z['written_denominator'])+' & '+d(z['whole']['written']['decimal'])+r'\\')
 article=p['article_only_sensitivity'];sens.append('L040 article-only, otherwise primary & '+fmt(article['source_sum'])+' & '+fmt(p['written_denominator'])+' & '+d(article['whole']['written']['decimal'])+r'\\')
 tex=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}
\usepackage{fontspec,unicode-math,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}\hypersetup{hidelinks}
\setlength{\emergencystretch}{2em}
\title{Coset geometries and symmetric group markings: unified proof costs}
\author{Human Compression project}\date{Numerical candidate awaiting independent review}
\begin{document}\maketitle
The complete written comparison for the five fixed original texts is
\[
 \frac{\sum_i c(L_i)}{c(U_B)+\sum_i c(B_i)}
 =\frac{@SOURCE@}{@COMMON@+@APPS@}
 =\frac{@SOURCE@}{@WRITTEN@}=\mathbf{@FACTOR@}.
\]
The numerator keeps the accepted source representations: N001's complete literal authored-browser rendering and the four complete PDFs. N001's original PDF remains unavailable; no complete-PDF factor for all five originals is claimed. The L040 identification cover remains in the primary input.

The entire sixteen-page common paper is charged once. It replaces the two earlier common papers through reviewed mathematical arguments, and all five complete applications remain. The fifty-page current input bundle includes references and the seven-page complete program appendix.

\begin{center}\begin{tabular}{lrrr}\toprule
Matched original & Original & Application & Conditional\\\midrule
@PAIRS@
\bottomrule\end{tabular}\end{center}
Every conditional factor presupposes acquisition of the \emph{whole current common theory and all four complete declared programs}. Each local paper, including context and references, is then charged in full. The common cost is @COMMON@ characters.

\begin{center}\begin{tabular}{lrr}\toprule
Complete-topic boundary & Denominator & Factor\\\midrule
Written common and all five applications &@WRITTEN@&@FACTOR@\\
Also the entire printed program appendix &@PRINTDEN@&@PRINTFACTOR@\\
Also the four whole raw programs (alternative) &@RAWDEN@&@RAWFACTOR@\\\bottomrule
\end{tabular}\end{center}
The appendix costs @PRINT@ characters; the raw files cost @RAW@. These are alternative representations, never additive charges. One program supplies bounded primitive-group inputs, two validate written general arguments, and one supplies the separate degree-eight example and branching-presentation check. No program is pruned because its role is auxiliary.

Two current operational drivers (@DRIVERS@ characters) and two Lean files (@LEAN@ characters) are separately inventoried. The fourteen reused declarations remain partial formal evidence. Full external proof, graphical and historical software costs remain unknown, not zero. No source, question or formal credit changes.
\newpage
\section*{Whole theory and complete applications}
\begin{center}\includegraphics[width=\linewidth]{costs.pdf}\end{center}
The lower bars compare full paper costs. Their conditional ratios require the common theory and complete programs already to have been acquired. The current written denominator pays the common paper once; it does not omit it or add both prior common papers.

\begin{center}\begin{tabular}{lrrr}\toprule
NFC nonspace sensitivity & Original total & Written total & Factor\\\midrule
@SENSITIVITIES@
\bottomrule\end{tabular}\end{center}
The primary counts raw, untrimmed NFC nonspace characters. All thirty settings---three extraction conventions, two normalizations and five units---are retained. The separate direct L040 article-only input changes only that source cost; all replacement costs and the other four conditionals stay unchanged. Complete JSON and CSV records give 240 main exact fractions and 120 cover-sensitivity fractions.

The earlier numerical edition is preserved. These results reuse the independently accepted inputs; no source extraction, font calibration, GAP or Lean is rerun here. The numerical author also authored those inputs, which received distinct root acceptance. This numerical candidate still requires its own independent review.
\end{document}
'''
 values={'SOURCE':fmt(p['source_sum']),'COMMON':fmt(p['common_theory']),'APPS':fmt(p['all_applications']),'WRITTEN':fmt(p['written_denominator']),'FACTOR':d(p['whole']['written']['decimal']),'PRINTDEN':fmt(p['denominators']['including_printed_programs']),'PRINTFACTOR':d(p['whole']['including_printed_programs']['decimal']),'RAWDEN':fmt(p['denominators']['including_raw_programs']),'RAWFACTOR':d(p['whole']['including_raw_programs']['decimal']),'PRINT':fmt(p['printed_program_cost']),'RAW':fmt(p['raw_program_cost']),'DRIVERS':fmt(p['operational_driver_cost']),'LEAN':fmt(p['partial_formal_cost']),'PAIRS':pairrows,'SENSITIVITIES':'\n'.join(sens)}
 for k,v in values.items():tex=tex.replace('@'+k+'@',v)
 need('@' not in tex,'all exact reader values');(out/'reader.tex').write_text(tex)

def render(out,engine):
 from pypdf import PdfReader
 for n in [1,2]:
  r=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=out,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/f'xelatex{n}.stdout').write_text(r.stdout);need(r.returncode==0,'reader compile')
 log=(out/'reader.log').read_text();diagnostics=[line for line in log.splitlines() if any(s in line for s in ['Missing character:','Overfull','Underfull','LaTeX Warning:','Package fontspec Warning:'])];need(not diagnostics,'clean complete reader '+str(diagnostics));pages=[p.extract_text() or '' for p in PdfReader(out/'reader.pdf').pages];need(len(pages)==2,'two complete reader pages');need(not any(unicodedata.category(c)=='Co' or c=='\ufffd' or (unicodedata.category(c)=='Cc' and c not in '\n\r\t') for c in '\n'.join(pages)),'no unclassified reader glyphs');return dict(pages=2,diagnostics=diagnostics,page_text_sha256=[sha(p.encode()) for p in pages])

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='xelatex');ap.add_argument('--prepare',action='store_true',help=argparse.SUPPRESS);a=ap.parse_args();need(not a.out.exists(),'fresh output');need(not a.prepare or not (H/'manifest.json').exists(),'frozen packet cannot regenerate itself');a.out.mkdir(parents=True)
 r,tests=compute();save(a.out/'results.json',r);tables(a.out,r);plot(a.out,r);reader(a.out,r);visual=render(a.out,a.xelatex) if a.render else None;names=['results.json','costs.csv','fractions.csv','raw_files.csv','costs.svg','costs.pdf','reader.tex']+(['reader.pdf'] if a.render else [])
 if a.prepare:
  for name in names:shutil.copy2(a.out/name,H/name)
 else:
  for name in names:
   if name in ['costs.pdf','reader.pdf']:continue
   need((a.out/name).read_bytes()==(H/name).read_bytes(),'exact generated table/chart/reader '+name)
  if a.render:
   from pypdf import PdfReader
   need([p.extract_text() or '' for p in PdfReader(a.out/'reader.pdf').pages]==[p.extract_text() or '' for p in PdfReader(H/'reader.pdf').pages],'exact full reader page text')
 report=dict(status='PASS',coordinates=30,main_exact_fractions=240,cover_sensitivity_fractions=120,all_exact_fractions=360,controls_rejected=tests,source_font_GAP_or_Lean_repeated=False,render=visual);save(a.out/'report.json',report);print(__import__('json').dumps(report))
