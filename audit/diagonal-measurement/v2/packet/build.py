#!/usr/bin/env python3
"""Generate exact tables, vector costs and a concise numerical reader."""
from pathlib import Path
import argparse,csv,json,os,subprocess,tempfile,shutil,unicodedata
from decimal import Decimal
from accounting import H,compute,save,load,need,sha,validate_results

def csv_outputs(out,r):
 fields=['variant','normalization','unit','source_N007','source_N006','common','application_N007','application_N006','written','whole_programs','required_decoders','software_inclusive','old_single_printed_validation','operational_drivers_separate','partial_formal_separate']
 with (out/'costs.csv').open('w',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
  for z in r['rows']:
   writer.writerow(dict(variant=z['variant'],normalization=z['normalization'],unit=z['unit'],source_N007=z['original_costs']['N007'],source_N006=z['original_costs']['N006'],common=z['common_theory'],application_N007=z['application_costs']['N007'],application_N006=z['application_costs']['N006'],written=z['written_denominator'],whole_programs=z['whole_program_cost'],required_decoders=z['required_decoder_cost'],software_inclusive=z['program_inclusive_denominator'],old_single_printed_validation=z['old_single_printed_validation_cost'],operational_drivers_separate=z['operational_driver_cost'],partial_formal_separate=z['partial_formal_cost']))
 with (out/'fractions.csv').open('w',newline='') as f:
  fields=['variant','normalization','unit','comparison','numerator','denominator','reduced_numerator','reduced_denominator','decimal'];writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
  for z in r['rows']:
   for name,value in [(f'whole_{k}',v) for k,v in z['whole'].items()]+[(f'conditional_{k}',v) for k,v in z['conditional'].items()]:writer.writerow(dict(variant=z['variant'],normalization=z['normalization'],unit=z['unit'],comparison=name,**value))
 with (out/'raw_files.csv').open('w',newline='') as f:
  fields=['category','path','role','bytes','sha256','normalization','unit','cost'];writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();c=load(H/'inputs/author_counts.json');p=load(H/'protocol.json')
  for cat,rows in c['raw_files'].items():
   for name,row in rows.items():
    for norm in p['normalizations']:
     for unit in p['units']:writer.writerow(dict(category=cat,path=name,role=row['role'],bytes=row['bytes'],sha256=row['sha256'],normalization=norm,unit=unit,cost=row['metrics'][norm][unit]))

def plot(out,r):
 os.environ.setdefault('MPLCONFIGDIR',str(out/'plot-cache'));os.environ.setdefault('XDG_CACHE_HOME',str(out/'cache'))
 import matplotlib
 matplotlib.use('Agg');import matplotlib.pyplot as plt
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.hashsalt':'Diagonal-two-originals-v2'})
 p=r['primary'];fig,(a,b)=plt.subplots(2,1,figsize=(7.0,4.8),gridspec_kw={'height_ratios':[1,1]});fig.subplots_adjust(left=.27,right=.87,top=.96,bottom=.11,hspace=.75)
 labels=['Both originals','Whole written proof','With complete software'];vals=[p['source_sum'],p['written_denominator'],p['program_inclusive_denominator']]
 a.barh(range(3),vals,color=['#738799','#397c86','#b68145']);a.invert_yaxis();a.set_yticks(range(3),labels);a.set_xlim(0,max(vals)*1.15);a.set_xlabel('Complete nonspace character costs')
 for y,x in enumerate(vals):a.text(x+5000,y,f'{x:,}',va='center',fontsize=9)
 names=['N007 original','N007 application','N006 original','N006 complete application'];v=[p['original_costs']['N007'],p['application_costs']['N007'],p['original_costs']['N006'],p['application_costs']['N006']]
 b.barh(range(4),v,color=['#738799','#397c86','#738799','#397c86']);b.invert_yaxis();b.set_yticks(range(4),names);b.set_xlim(0,max(v)*1.18);b.set_xlabel('Full local papers; common theory and software already acquired')
 for y,x in enumerate(v):b.text(x+700,y,f'{x:,}',va='center',fontsize=9)
 for ax in [a,b]:
  ax.spines[['top','right']].set_visible(False);ax.grid(axis='x',color='#dddddd',linewidth=.5);ax.set_axisbelow(True)
 fig.savefig(out/'costs.svg',metadata={'Date':None});fig.savefig(out/'costs.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)

def reader(out,r):
 p=r['primary'];f=lambda x:f'{x:,}';d=lambda x:f'{Decimal(x):.6f}'
 tex=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}
\usepackage{fontspec,unicode-math,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}\hypersetup{hidelinks}
\setlength{\emergencystretch}{2em}
\title{Orbit and semidirect constructions: two complete originals}
\author{Human Compression project}\date{Numerical candidate awaiting independent review}
\begin{document}\maketitle
The complete written comparison is
\[
 \frac{c(\mathrm{N007})+c(\mathrm{N006})}{c(U)+c(A_{\mathrm{N007}})+c(A_{\mathrm{N006}})}
 =\frac{@SOURCE@}{@WRITTEN@}=\mathbf{@FACTOR@}.
\]
The whole eight-page common paper is charged once. The N007 application has five pages; the N006 application includes all three companion papers, of eight, five and four pages. Titles and references remain included. The prior N007-only edition is preserved separately.

\begin{center}\begin{tabular}{lrrr}\toprule
Matched original & Original & Complete application & Conditional factor\\\midrule
N007: diagonal twistings & @N007@ & @A1@ & @C1@\\
N006: wreath and semidirect products & @N006@ & @A2@ & @C2@\\\bottomrule
\end{tabular}\end{center}
The conditional figures assume that the \emph{whole common theory and all declared software and required data have already been acquired}, including both decoding drivers. They do not omit any local companion paper. Common theory costs @COMMON@ characters.

\begin{center}\includegraphics[width=\linewidth]{costs.pdf}\end{center}
\noindent Primary unit: calibrated, selected NFC nonspace characters. Source graphical substitutions are declared encoded-event proxies, not exact Unicode geometry. Raw and text-only sensitivities appear on the next page.
\newpage
\section*{Complete software and the measurement limits}
All nineteen whole GAP and witness files cost @PROGRAMS@ characters; both complete required decoding drivers add @DECODERS@. Including this entire @SOFTWARE@-character software bundle gives
\[
 \frac{@SOURCE@}{@WRITTEN@+@SOFTWARE@}
 =\frac{@SOURCE@}{@INCLUSIVE@}=\mathbf{@SOFTFACTOR@}.
\]
Sixteen files provide finite proof inputs or complete saved witnesses, and three are validation files. Large saved permutations receive no discount. The four other operational drivers (@DRIVERS@ characters) and three Lean files (@LEAN@ characters, seventeen partial declarations) are reported separately.

There is no complete printed appendix for the eighteen new files. The earlier two-page appendix (@OLDPRINT@ characters) is an alternative for its single N007 validation file only. It cannot stand for all nineteen files, and it is never charged in addition to that same raw file.

\begin{center}\begin{tabular}{lrrrr}\toprule
NFC nonspace convention & Original total & Written total & Written factor & With software\\\midrule
@SENSITIVITIES@
\bottomrule\end{tabular}\end{center}
All thirty ordinary coordinates (three extraction conventions, two normalizations and five units) are preserved. The ten additional text-only coordinates replace only identified graphical-proxy events by separators. That sensitivity does not measure the entire nontextual geometry. All forty settings and 160 exact fractions appear in the JSON and CSV records.

\begin{center}\begin{tabular}{lr}\toprule
Separate external storage inventory & Bytes\\\midrule
Four required representation files &21,960,689\\
Sixteen listed installed data/algorithm files &2,516,249\\\bottomrule
\end{tabular}\end{center}
These byte totals are separate from character costs. Binary/decoded and compressed/decompressed versions are alternative representations, not extra charges. The complete GAP runtime is trusted infrastructure and is not represented by the listed files. Retained classification proofs, historical software, full graphics and full formalization remain unknown, not zero.

This packet reuses the independently accepted input boundary and does not rerun source extraction, GAP or Lean. It covers the thirty-two N007 and twenty-seven corrected N006 clauses in the bound scientific edition. Later Fischer exception certificates lie outside this comparison. No source, question, priority or formal credit changes.
\end{document}
'''
 sens=[]
 for key,label in [('raw_untrimmed','Literal full extraction'),('raw_selected','Literal selected extraction'),('calibrated_selected','Calibrated selected (primary)'),('text_only_sensitivity','Identified proxies removed')]:
  z=next(z for z in r['rows'] if z['variant']==key and z['normalization']=='NFC' and z['unit']=='characters_without_whitespace');sens.append(label+' & '+f(z['source_sum'])+' & '+f(z['written_denominator'])+' & '+d(z['whole']['written']['decimal'])+' & '+d(z['whole']['including_whole_raw_software']['decimal'])+r'\\')
 values={'SOURCE':f(p['source_sum']),'WRITTEN':f(p['written_denominator']),'FACTOR':d(p['whole']['written']['decimal']),'N007':f(p['original_costs']['N007']),'N006':f(p['original_costs']['N006']),'A1':f(p['application_costs']['N007']),'A2':f(p['application_costs']['N006']),'C1':d(p['conditional']['N007']['decimal']),'C2':d(p['conditional']['N006']['decimal']),'COMMON':f(p['common_theory']),'PROGRAMS':f(p['whole_program_cost']),'DECODERS':f(p['required_decoder_cost']),'SOFTWARE':f(p['whole_software_cost']),'INCLUSIVE':f(p['program_inclusive_denominator']),'SOFTFACTOR':d(p['whole']['including_whole_raw_software']['decimal']),'DRIVERS':f(p['operational_driver_cost']),'LEAN':f(p['partial_formal_cost']),'OLDPRINT':f(p['old_single_printed_validation_cost']),'SENSITIVITIES':'\n'.join(sens)}
 for k,v in values.items():tex=tex.replace('@'+k+'@',v)
 need('@' not in tex,'all bound reader values');(out/'reader.tex').write_text(tex)

def render(out,engine):
 from pypdf import PdfReader
 for i in [1,2]:
  p=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=out,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/f'xelatex{i}.stdout').write_text(p.stdout);need(p.returncode==0,'complete reader compile')
 log=(out/'reader.log').read_text();warnings=[line for line in log.splitlines() if any(x in line for x in ['Missing character:','Overfull','Underfull','LaTeX Warning:','Package fontspec Warning:'])];need(not warnings,'clean reader diagnostics '+str(warnings));pages=[p.extract_text() or '' for p in PdfReader(out/'reader.pdf').pages];need(len(pages)==2,'exact two-page reader');need(not any(unicodedata.category(c)=='Co' or c=='\ufffd' or (unicodedata.category(c)=='Cc' and c not in '\n\r\t') for c in '\n'.join(pages)),'clean reader glyphs')
 return dict(pages=2,diagnostics=warnings,page_text_sha256=[sha(x.encode()) for x in pages])

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='xelatex');ap.add_argument('--prepare',action='store_true',help=argparse.SUPPRESS);a=ap.parse_args();need(not a.out.exists(),'fresh output');need(not a.prepare or not (H/'manifest.json').exists(),'frozen candidate cannot be rewritten');a.out.mkdir(parents=True)
 r,tests=compute();save(a.out/'results.json',r);csv_outputs(a.out,r);plot(a.out,r);reader(a.out,r);visual=render(a.out,a.xelatex) if a.render else None
 names=['results.json','costs.csv','fractions.csv','raw_files.csv','costs.svg','costs.pdf','reader.tex']+(['reader.pdf'] if a.render else [])
 if a.prepare:
  for name in names:shutil.copy2(a.out/name,H/name)
 else:
  for name in names:
   if name in ['costs.pdf','reader.pdf']:continue
   need((a.out/name).read_bytes()==(H/name).read_bytes(),'exact regenerated artifact '+name)
  if a.render:
   from pypdf import PdfReader
   need([p.extract_text() or '' for p in PdfReader(a.out/'reader.pdf').pages]==[p.extract_text() or '' for p in PdfReader(H/'reader.pdf').pages],'exact full reader page text')
 report=dict(status='PASS',ordinary_coordinates=30,text_only_coordinates=10,exact_fractions=160,controls_rejected=tests,source_extraction_or_GAP_Lean_repeated=False,render=visual);save(a.out/'report.json',report);print(json.dumps(report))
