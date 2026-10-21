#!/usr/bin/env python3
"""Generate whole-cost tables/figures and reader from exact accepted inputs."""
from pathlib import Path
import argparse,csv,json,os,subprocess,shutil,unicodedata
from decimal import Decimal
from accounting import H,compute,load,save,need,sha

def csv_outputs(out,r):
 keys=['variant','normalization','unit','source_N005','source_N006','source_N007','common','application_N005','application_N006','application_N007','written','whole_programs','required_decoders','software_inclusive','operational_drivers_separate','partial_formal_separate']
 with (out/'costs.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
  for z in r['rows']:w.writerow(dict(variant=z['variant'],normalization=z['normalization'],unit=z['unit'],**{'source_'+k:v for k,v in z['original_costs'].items()},common=z['common_theory'],**{'application_'+k:v for k,v in z['application_costs'].items()},written=z['written_denominator'],whole_programs=z['whole_program_cost'],required_decoders=z['required_decoder_cost'],software_inclusive=z['program_inclusive_denominator'],operational_drivers_separate=z['operational_driver_cost'],partial_formal_separate=z['partial_formal_cost']))
 with (out/'fractions.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['variant','normalization','unit','comparison','numerator','denominator','reduced_numerator','reduced_denominator','decimal']);w.writeheader()
  for z in r['rows']:
   for name,v in [(f'whole_{k}',v) for k,v in z['whole'].items()]+[(f'conditional_{k}',v) for k,v in z['conditional'].items()]:w.writerow(dict(variant=z['variant'],normalization=z['normalization'],unit=z['unit'],comparison=name,**v))
 with (out/'raw_files.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['category','id','role','bytes','sha256','normalization','unit','cost']);w.writeheader();c=load(H/'inputs/author_counts.json');p=load(H/'protocol.json')
  for cat,rs in c['raw_files'].items():
   for k,row in rs.items():
    for norm in p['normalizations']:
     for unit in p['units']:w.writerow(dict(category=cat,id=k,role=row['role'],bytes=row['bytes'],sha256=row['sha256'],normalization=norm,unit=unit,cost=row['metrics'][norm][unit]))
 with (out/'acquisition.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['variant','normalization','unit','stage','current_increment','current_cumulative','matched_source_increment','matched_source_cumulative']);w.writeheader()
  for z in r['rows']:
   for s in z['acquisition']:w.writerow(dict(variant=z['variant'],normalization=z['normalization'],unit=z['unit'],**{k:v for k,v in s.items() if k!='scope'}))
 with (out/'partial_printed_alternatives.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['variant','normalization','unit','appendix','printed_cost','replaced_raw_cost','whole_files','complete_program_factor']);w.writeheader()
  for z in r['rows']:
   for k,v in z['partial_printed_costs'].items():w.writerow(dict(variant=z['variant'],normalization=z['normalization'],unit=z['unit'],appendix=k,printed_cost=v['printed_cost'],replaced_raw_cost=v['replaced_raw_cost'],whole_files=len(v['whole_file_ids']),complete_program_factor='not_defined'))

def plot(out,r):
 os.environ.setdefault('MPLCONFIGDIR',str(out/'plot-cache'));os.environ.setdefault('XDG_CACHE_HOME',str(out/'cache'))
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.ticker import FuncFormatter
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'Operations-three-originals-v1'})
 p=r['primary'];vals=[p['source_sum'],p['written_denominator'],p['program_inclusive_denominator']]
 fig,ax=plt.subplots(figsize=(7.0,2.25));fig.subplots_adjust(left=.36,right=.94,bottom=.25,top=.95)
 ax.barh(range(3),vals,color=['#78879a','#327c82','#b47b37']);ax.set_yticks(range(3),['All three originals','Whole written edition','Including complete software']);ax.invert_yaxis();ax.set_xlim(0,max(vals)*1.18);ax.set_xlabel('NFC nonspace characters')
 for y,v in enumerate(vals):ax.text(v+7000,y,f'{v:,}',va='center',fontsize=10)
 ax.spines[['top','right']].set_visible(False);ax.grid(axis='x',color='#dddddd');ax.set_axisbelow(True);ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{int(v/1000)}k'))
 for fmt in ['svg','pdf']:fig.savefig(out/('costs.'+fmt),metadata={'Date':None} if fmt=='svg' else {'CreationDate':None,'ModDate':None})
 plt.close(fig)
 fig,ax=plt.subplots(figsize=(7,3.4));fig.subplots_adjust(left=.13,right=.96,bottom=.22,top=.95)
 x=[0,1,2,3,4];own=[0]+[z['current_cumulative'] for z in p['acquisition']];src=[0]+[z['matched_source_cumulative'] for z in p['acquisition']]
 ax.plot(x,src,marker='o',color='#78879a',label='Complete matched originals');ax.plot(x,own,marker='s',color='#327c82',label='Whole theory then full applications')
 ax.set_xticks(x,['Start','Whole U','N005\napplication','N006\n8+5+4 pages','N007\napplication']);ax.set_ylim(0,max(src+own)*1.15);ax.set_xlim(0,4.1);ax.set_ylabel('Cumulative NFC nonspace characters');ax.legend(loc='upper left',fontsize=9);ax.grid(color='#dddddd');ax.spines[['top','right']].set_visible(False);ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{int(v/1000)}k'))
 for fmt in ['svg','pdf']:fig.savefig(out/('acquisition.'+fmt),metadata={'Date':None} if fmt=='svg' else {'CreationDate':None,'ModDate':None})
 plt.close(fig)
 save(out/'plot_data.json',dict(primary_policy=load(H/'protocol.json')['primary'],cost_bars=vals,acquisition_order=['Start','U','N005','N006','N007'],current_cumulative=own,matched_original_cumulative=src,axes_start_at_zero=True,claim_of_sawtooth=False,zero_matched_original_before_first_application_is_not_historical_theory_cost=True))

def reader(out,r):
 p=r['primary'];f=lambda x:f'{x:,}';d=lambda x:f'{Decimal(x):.6f}';c=load(H/'inputs/author_counts.json')
 tex=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}
\usepackage{fontspec,unicode-math,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}\hypersetup{hidelinks}
\setlength{\emergencystretch}{2em}
\title{Group operations: three complete originals}
\author{Human Compression project}\date{Numerical candidate awaiting independent review}
\begin{document}\maketitle
The three Piedade--Tranchida originals N005, N006 and N007 are compared with the whole common theory and every complete application and companion. The written comparison is
\[
\frac{c(N005)+c(N006)+c(N007)}{c(U)+c(A_{005})+c(A_{006})+c(A_{007})}
=\frac{@SOURCE@}{@WRITTEN@}=\mathbf{@FACTOR@}.
\]
The whole declared programme consists of 23 mathematical or validation files and both complete required decoding drivers. Including it gives
\[
\frac{@SOURCE@}{@WRITTEN@+@SOFTWARE@}
=\frac{@SOURCE@}{@INCLUSIVE@}=\mathbf{@SOFTFACTOR@}.
\]
These are separate comparisons. The source historical software and complete retained external proofs remain unpriced. Thus neither fraction is a fully priced comparison of all external mathematical work.

\begin{center}\includegraphics[width=\linewidth]{costs.pdf}\end{center}

\begin{center}\begin{tabular}{lrrr}\toprule
Complete matched papers & Original & Application & Conditional factor\\\midrule
N005: group operations & @N005@ & @A0@ & @C0@\\
N006: wreath and semidirect products & @N006@ & @A2@ & @C2@\\
N007: diagonal twistings & @N007@ & @A1@ & @C1@\\\bottomrule
\end{tabular}\end{center}
These conditional figures are $c(N_i)/c(A_i)$ \emph{after acquiring the whole common theory, all 23 files and both decoding drivers}, together with the required external data. Every local proof, companion and reference remains charged. There is no overlap discount between separate topics.

Primary unit: selected calibrated NFC nonspace characters. The encoded graphic-event substitutions are proxies for components, not complete geometry or literal Unicode extraction.
\newpage
\section*{The complete paper sequence}
The common paper has 21 pages and costs @COMMON@ characters. N005 has 18 pages; N006 comprises all three papers of 8, 5 and 4 pages; N007 has 5 pages. These six scientific documents total 61 pages. The three originals total 94 pages. References and front matter remain included on both sides.

\begin{center}\begin{tabular}{lrrrr}\toprule
Stage & New written cost & Written total & New original & Original total\\\midrule
@ACQUISITION@\bottomrule
\end{tabular}\end{center}
\begin{center}\includegraphics[width=\linewidth]{acquisition.pdf}\end{center}
The ordering displays whole documents, not theorem-node costs or an empirical learning curve. The initial source entry is zero because no matched original has yet been accumulated; it does not assign zero cost to historical common theory. The whole software bundle is shown separately on page~1 and is prepaid for the conditional comparisons.

\begin{center}\begin{tabular}{lrr}\toprule
Whole files & Nonspace characters & Raw bytes\\\midrule
23 mathematical/validation files & @PROGRAMS@ & @PROGRAMBYTES@\\
2 required decoding drivers & @DECODERS@ & @DECODERBYTES@\\
5 operational drivers (separate) & @DRIVERS@ & @DRIVERBYTES@\\
3 Lean files (separate) & @LEAN@ & @LEANBYTES@\\\bottomrule
\end{tabular}\end{center}
Seventeen mathematical files supply finite premises or saved witnesses; six are validation. Large saved permutations receive no discount. The 17 Lean declarations are scoped partial evidence, with no new N005 formalization.
\newpage
\section*{Sensitivity and retained costs}
\begin{center}\begin{tabular}{lrrrr}\toprule
NFC nonspace convention & Originals & Written & Written factor & With software\\\midrule
@SENSITIVITIES@\bottomrule
\end{tabular}\end{center}
The raw rows preserve extraction without glyph substitutions. The text-only sensitivity removes only identified graphical proxies. The input audit reconciles actual PDF font dictionaries, encodings and occurrences, including 20 visible N005 strokes extracted as carriage returns. Full drawing structure, placement and curvature remain unmeasured.

\begin{center}\begin{tabular}{lrrrr}\toprule
Calibrated selected unit & \multicolumn{2}{c}{Written factor} & \multicolumn{2}{c}{With software}\\
& NFC & NFKC & NFC & NFKC\\\midrule
@METRICS@\bottomrule
\end{tabular}\end{center}
The JSON/CSV contain all 30 ordinary settings and 10 text-only settings, with 200 exact fractions. Printed hyphens remain counted. Only exact running furniture is removed. The audit covers 11 PDFs and 161 pages, including two partial printed alternatives; this is not a 161-page replacement.

There is \emph{no complete printed programme factor}. The 4-page N005 appendix (@NEWPRINT@ characters) replaces only three named raw files; the 2-page N007 appendix (@OLDPRINT@) replaces only its one validation file. The remaining whole files and decoders cannot be omitted. Both printed alternatives are inventoried, never added to the same raw files.

Four required Atlas representation files occupy 21,960,689 bytes; sixteen listed installed catalogue/algorithm files occupy 2,516,249 bytes. These storage figures are separate from text costs. Binary/decoded and compressed/decompressed forms are alternatives. Named-group identification, maximal-subgroup classification, Coxeter and Artin theory, normal forms, Bass--Serre theory and affine-reflection inputs remain retained. Full external proofs, graphics, historical software and complete formalization have unknown cost, not zero cost.

All $81+27+32$ source dispositions and their corrections/exclusions are preserved. The unrestricted nonfirm HNN claim is not recovered, and unresolved general questions are not answered by these numbers. The later separate Fischer exception certificates are outside this comparison. This packet changes no source, question or formal credit and does not rerun source extraction, GAP or Lean.
\end{document}
'''
 sens=[]
 for key,label in [('raw_untrimmed','Literal full extraction'),('raw_selected','Literal selected extraction'),('calibrated_selected','Calibrated selected'),('text_only_sensitivity','Graphic proxies removed')]:
  z=next(z for z in r['rows'] if z['variant']==key and z['normalization']=='NFC' and z['unit']=='characters_without_whitespace');sens.append(label+' & '+f(z['source_sum'])+' & '+f(z['written_denominator'])+' & '+d(z['whole']['written']['decimal'])+' & '+d(z['whole']['including_whole_raw_software']['decimal'])+r'\\')
 metrics=[]
 for unit,label in [('whitespace_tokens','Whitespace tokens'),('alphanumeric_units','Alphanumeric units'),('characters_without_whitespace','Nonspace characters'),('characters_with_collapsed_whitespace','Collapsed-space characters'),('utf8_bytes_with_collapsed_whitespace','Collapsed-space UTF-8 bytes')]:
  pair={n:next(z for z in r['rows'] if z['variant']=='calibrated_selected' and z['normalization']==n and z['unit']==unit) for n in ['NFC','NFKC']};metrics.append(label+' & '+' & '.join(d(pair[n]['whole'][k]['decimal']) for k in ['written','including_whole_raw_software'] for n in ['NFC','NFKC'])+r'\\')
 acq='\n'.join(s['stage']+' & '+' & '.join(f(s[k]) for k in ['current_increment','current_cumulative','matched_source_increment','matched_source_cumulative'])+r'\\' for s in p['acquisition'])
 vals=dict(SOURCE=f(p['source_sum']),WRITTEN=f(p['written_denominator']),SOFTWARE=f(p['whole_software_cost']),INCLUSIVE=f(p['program_inclusive_denominator']),FACTOR=d(p['whole']['written']['decimal']),SOFTFACTOR=d(p['whole']['including_whole_raw_software']['decimal']),COMMON=f(p['common_theory']),PROGRAMS=f(p['whole_program_cost']),DECODERS=f(p['required_decoder_cost']),DRIVERS=f(p['operational_driver_cost']),LEAN=f(p['partial_formal_cost']),ACQUISITION=acq,SENSITIVITIES='\n'.join(sens),METRICS='\n'.join(metrics),NEWPRINT=f(p['document_costs']['CODEnew']),OLDPRINT=f(p['document_costs']['CODEold']))
 for k,name in [('N005','A0'),('N006','A2'),('N007','A1')]:vals[k]=f(p['original_costs'][k]);vals[name]=f(p['application_costs'][k]);vals['C'+name[-1]]=d(p['conditional'][k]['decimal'])
 for k,cat in [('PROGRAMBYTES','programs'),('DECODERBYTES','required_drivers'),('DRIVERBYTES','drivers'),('LEANBYTES','formal')]:vals[k]=f(sum(x['bytes'] for x in c['raw_files'][cat].values()))
 for k,v in vals.items():tex=tex.replace('@'+k+'@',v)
 need('@' not in tex,'all exact reader values');(out/'reader.tex').write_text(tex)

def render(out,engine):
 from pypdf import PdfReader
 for i in [1,2]:
  r=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=out,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/f'xelatex{i}.stdout').write_text(r.stdout);need(r.returncode==0,'fresh reader compile')
 log=(out/'reader.log').read_text();warnings=[x for x in log.splitlines() if any(t in x for t in ['Missing character:','Overfull','Underfull','LaTeX Warning:','Package fontspec Warning:'])];need(not warnings,'clean reader diagnostics '+str(warnings));pages=[p.extract_text() or '' for p in PdfReader(out/'reader.pdf').pages];need(len(pages)==3,'complete three-page reader');need(not any(unicodedata.category(x)=='Co' or x=='\ufffd' or (unicodedata.category(x)=='Cc' and x not in '\r\n\t') for x in '\n'.join(pages)),'readable reader glyphs')
 return dict(pages=3,diagnostics=warnings,page_text_sha256=[sha(x.encode()) for x in pages])

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');ap.add_argument('--prepare',action='store_true',help=argparse.SUPPRESS);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output');need(not a.prepare or not (H/'manifest.json').exists(),'frozen packet immutable');a.out.mkdir(parents=True)
 r,tests=compute();save(a.out/'results.json',r);csv_outputs(a.out,r);plot(a.out,r);reader(a.out,r);visual=render(a.out,a.xelatex) if a.render else None
 names=['results.json','costs.csv','fractions.csv','raw_files.csv','acquisition.csv','partial_printed_alternatives.csv','costs.svg','costs.pdf','acquisition.svg','acquisition.pdf','plot_data.json','reader.tex']+(['reader.pdf'] if a.render else [])
 if a.prepare:
  for n in names:shutil.copyfile(a.out/n,H/n)
 else:
  for n in names:
   if n.endswith('.pdf'):continue
   need((a.out/n).read_bytes()==(H/n).read_bytes(),'exact regenerated output '+n)
  if a.render:
   from pypdf import PdfReader
   need([p.extract_text() or '' for p in PdfReader(a.out/'reader.pdf').pages]==[p.extract_text() or '' for p in PdfReader(H/'reader.pdf').pages],'fresh complete page text')
 report=dict(status='PASS',ordinary_coordinates=30,text_only_coordinates=10,exact_fractions=200,acquisition_cells=640,controls_rejected=tests,render=visual,source_extraction_or_GAP_Lean_repeated=False);save(a.out/'report.json',report);print(json.dumps(report))
