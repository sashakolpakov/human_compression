#!/usr/bin/env python3
"""Readable Topic D complete-paper arithmetic and program sensitivity."""
from pathlib import Path
import argparse,json,hashlib,re,subprocess,os,tempfile
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'topic-d-results-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pypdf import PdfReader
HERE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--results',type=Path,default=HERE/'results.json');ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args()
 if a.out.exists() or a.out.is_symlink():raise ValueError('fresh reader output')
 a.out.mkdir(parents=True);r=json.loads(a.results.read_text());p=r['primary'];f=p['comparisons'];fmt=lambda n:f'{n:,}'
 if p['written_denominator']!=p['common_theory']+p['all_applications']:raise ValueError('complete written denominator')
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'human-compression-topic-d-v2'})
 fig,ax=plt.subplots(figsize=(8.1,2.7),layout='constrained')
 own=[p['common_theory']]+[q['application_cost'] for q in p['per_result']]+[p['printed_program_cost']]
 bars=ax.bar([i+.16 for i in range(5)],own,width=.31,color=['#245d88']*4+['#6a6f74'],label='Whole common paper and applications')
 src=ax.bar([i+.84 for i in range(3)],[q['source_cost'] for q in p['per_result']],width=.31,color='#a3632c',label='Whole source manuscripts')
 for group in [bars,src]:
  for b in group:ax.text(b.get_x()+b.get_width()/2,b.get_height()+350,fmt(round(b.get_height())),ha='center',fontsize=8)
 ax.set_xticks(range(5),['Common U_D','L066 / D1','L074 / D2','L104 / D3','Full program\nappendix']);ax.set_ylim(0,34000);ax.set_ylabel('NFC characters, no whitespace');ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True);ax.legend(loc='upper left',frameon=False,fontsize=8,ncol=1)
 for ext in ['svg','pdf','png']:fig.savefig(a.out/('costs.'+ext),dpi=150,facecolor='white')
 plt.close(fig)
 pairs='\n'.join(f"{q['source']} / {q['application']} & {fmt(q['source_cost'])} & {fmt(q['application_cost'])} & {q['factor']:.3f}"+r'\\' for q in p['per_result'])
 labels={'whitespace_tokens':'Whitespace tokens','alphanumeric_units':'Alphanumeric runs','characters_without_whitespace':'Nonspace characters','characters_with_collapsed_whitespace':'Collapsed characters','utf8_bytes_with_collapsed_whitespace':'Collapsed UTF-8 bytes'}
 sensitive=[]
 for u,label in labels.items():
  cells=[c for c in r['coordinates'] if c['unit']==u];sel={c['normalization']:c for c in cells if c['variant']=='calibrated_selected'};values=[c['comparisons']['written_papers']['factor'] for c in cells]
  sensitive.append(f"{label} & {sel['NFC']['comparisons']['written_papers']['factor']:.3f} & {sel['NFKC']['comparisons']['written_papers']['factor']:.3f} & {min(values):.3f}--{max(values):.3f} & {sel['NFC']['comparisons']['including_printed_program']['factor']:.3f}"+r'\\')
 tex=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=22mm]{geometry}
\usepackage{fontspec,amsmath,booktabs,graphicx,hyperref,array}
\setmainfont{STIXGeneral}
\setlength{\emergencystretch}{2em}
\begin{document}
\begin{center}{\Large Topic D: written papers and complete programs}\\[4pt]
Human Compression project\end{center}
The three accepted applications recover the declared principal results on
commuting involutions (L066/D1), Suzuki regular polyhedra (L074/D2), and
Hall--Janko geometries (L104/D3). The common paper supplies orbit data,
stabilizer fibers, support counting and panel recognition. The exact
37-row source contract, corrections, retained inputs and exclusions remain
unchanged. This is a comparison of complete extracted manuscript text for
those main results, not equivalence of every printed assertion.

\paragraph{Written papers.}
The three whole source manuscripts cost @SOURCE@ NFC characters without
whitespace. Our whole common paper costs @COMMON@ and the three whole
applications cost @APPS@. Charging the common paper once within Topic D gives
\[
 R_D=\frac{\sum_i c(L_i)}{c(U_D)+\sum_i c(D_i)}
     =\frac{@SOURCEMATH@}{@COMMONMATH@+@APPSMATH@}
     =\frac{@SOURCEMATH@}{@WRITTENMATH@}=\mathbf{@WRITTENFACTOR@}.
\]
The common paper is paid in full even where another topic uses the same idea.

\begin{center}\includegraphics[width=\linewidth]{costs.pdf}\end{center}
\noindent All bars use complete documents after exact running-furniture removal
and occurrence-specific visible-glyph calibration. Unique front matter and
references remain. The grey program bar is a separate comparison below.
These document costs are not a time series or evidence of a sawtooth pattern.

\paragraph{After acquiring the common work.}
After acquiring \emph{the whole common paper and the complete program boundary},
the conditional comparison is $c(L_i)/c(D_i)$. That boundary includes all five
required programs and all three complete diagnostics. Both common theory and
all eight programs are acquired in full before these local comparisons.
\begin{center}\begin{tabular}{lrrr}\toprule
Source / application & Whole source & Whole application & Conditional factor\\\midrule
@PAIRS@
\bottomrule\end{tabular}\end{center}
These conditional factors do not include the acquisition cost a second time.
The combined written comparison above pays the whole common paper explicitly;
the next comparison also pays every printed program.

\newpage
\paragraph{Including the required program.}
The complete 12-page appendix contains all eight mathematical files: five
required programs and three full diagnostics. It costs @PRINTED@ in the primary
unit, so the separate known-text comparison is
\[
 R_{D,\mathrm{program}}=\frac{@SOURCEMATH@}{@WRITTENMATH@+@PRINTEDMATH@}
 =\frac{@SOURCEMATH@}{@INCLUSIVEMATH@}=\mathbf{@INCLUSIVEFACTOR@}.
\]
Here the replacement is longer than the available historical manuscript text.
Historical software and external algorithm construction have unknown cost;
they are not assumed to be free. The comparison states exactly which measured
texts are in its numerator and denominator.

\begin{center}\begin{tabular}{p{.67\linewidth}rr}\toprule
Representation & Denominator & Factor\\\midrule
Written papers & @WRITTEN@ & @WRITTENFACTOR@\\
Written papers plus whole printed appendix & @INCLUSIVE@ & @INCLUSIVEFACTOR@\\
Written papers plus all eight whole raw programs & @RAWALL@ & @RAWFACTOR@\\\bottomrule
\end{tabular}\end{center}
The whole raw programs cost @RAW@, of which @REQUIREDRAW@ belongs to the five
required files and @DIAGNOSTICRAW@ to the three diagnostics. This is an
\emph{alternative} to the printed appendix, never an additional charge.
Raw metrics are summed file by file, without pruning branches or diagnostic
parts. The two complete execution drivers cost @DRIVERS@ separately and are
reported separately from the denominators above. Their @DRIVERBYTES@ actual file bytes
are also retained in the machine-readable inventory. One driver retains an
unused historical M22 branch; no M22 result is included.

\paragraph{Sensitivity to the ruler.}
The full tables retain three variants (raw untrimmed, raw selected and
calibrated selected), NFC and NFKC, and five units: 30 coordinates and
180 exact combined/conditional fractions. The middle columns below use
calibrated selected text; the range covers all six variants/normalizations.
\begin{center}\small\begin{tabular}{p{.29\linewidth}rrrr}\toprule
Unit & Written NFC & Written NFKC & Written range & With code NFC\\\midrule
@SENSITIVITY@
\bottomrule\end{tabular}\end{center}
No one of these units measures intrinsic mathematical difficulty. All use the
same complete-document and program boundary.

\paragraph{Extent and limits.}
The three source PDFs have 9, 12 and 5 physical pages (26 total). Our common
paper has 6 pages, the applications have 5, 6 and 2 (19 scientific pages total),
and the program appendix has 12. All 57 input pages are retained. Vector edges,
formula placement and other unextracted graphical information have unknown
cost. This is an extracted-text coordinate, not a claim to count every visible
mark or all prior research effort. External classical proofs, subgroup catalogue
construction, GAP internals and formal verification costs are separate.

The L104 printed diagrams, full Aut/Cor groups, doubling relation and supplement
annotations are not all recovered; their source text is nevertheless part of
the complete manuscript numerator. The L066 reversal/regularity qualifications
and the retained Suzuki classification remain explicit. The corrected extraction
uses original PDF bytes for fourteen L066 brackets previously confused with
brace pieces. This is an extracted-character/encoding collision, not a
ToUnicode-table collision: that font has no such stream. Only calibrated UTF-8
lengths changed by $-28$; the primary character counts did not change.
Input acceptance and numerical admission are recorded separately. No new
source, conjecture or formal theorem credit follows from this measurement.
\end{document}
'''
 def mathnum(n):return f'{n:,}'.replace(',',r'\,')
 subs={'SOURCE':fmt(p['source_sum']),'COMMON':fmt(p['common_theory']),'APPS':fmt(p['all_applications']),'WRITTEN':fmt(p['written_denominator']),'PRINTED':fmt(p['printed_program_cost']),'INCLUSIVE':fmt(f['including_printed_program']['denominator']),'RAWALL':fmt(f['including_raw_program_alternative']['denominator']),'RAW':fmt(p['raw_program_cost']),'REQUIREDRAW':fmt(p['raw_program_role_costs']['required']),'DIAGNOSTICRAW':fmt(p['raw_program_role_costs']['diagnostic']),'DRIVERS':fmt(p['separate_driver_cost']),'DRIVERBYTES':fmt(r['raw_file_bytes']['drivers']),'WRITTENFACTOR':f"{f['written_papers']['factor']:.3f}",'INCLUSIVEFACTOR':f"{f['including_printed_program']['factor']:.3f}",'RAWFACTOR':f"{f['including_raw_program_alternative']['factor']:.3f}",'PAIRS':pairs,'SENSITIVITY':'\n'.join(sensitive)}
 for name,value in [('SOURCE',p['source_sum']),('COMMON',p['common_theory']),('APPS',p['all_applications']),('WRITTEN',p['written_denominator']),('PRINTED',p['printed_program_cost']),('INCLUSIVE',f['including_printed_program']['denominator'])]:subs[name+'MATH']=mathnum(value)
 for k,v in subs.items():tex=tex.replace('@'+k+'@',v)
 if re.search('@[A-Z]+@',tex):raise ValueError('unsubstituted reader token')
 (a.out/'measurement.tex').write_text(tex)
 for i in range(2):
  proc=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','measurement.tex'],cwd=a.out,capture_output=True,text=True)
  (a.out/f'xelatex-{i+1}.txt').write_text(proc.stdout+proc.stderr)
  if proc.returncode:raise ValueError('reader TeX failed')
 log=(a.out/'measurement.log').read_text();bad=[l for l in log.splitlines() if re.search('Overfull|Underfull|Missing character|Warning|^!',l)]
 if bad:raise ValueError(bad)
 report=dict(status='PASS_READER_RENDER_PENDING_VISUAL_INSPECTION',results_sha256=sha(a.results),tex_sha256=sha(a.out/'measurement.tex'),pdf_sha256=sha(a.out/'measurement.pdf'),pages=len(PdfReader(a.out/'measurement.pdf').pages),per_page_text_sha256=[hashlib.sha256((p.extract_text() or '').encode()).hexdigest() for p in PdfReader(a.out/'measurement.pdf').pages],diagnostics=[],xelatex=a.xelatex,plot_units='primary calibrated NFC characters without whitespace',no_time_series_claim=True,svg_sha256=sha(a.out/'costs.svg'))
 (a.out/'render_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
