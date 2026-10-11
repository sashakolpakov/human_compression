#!/usr/bin/env python3
from pathlib import Path
import argparse,json,os,subprocess,hashlib
from compute import need

def plot(r,out):
 os.environ['MPLCONFIGDIR']=str(out/'.mpl');os.environ['XDG_CACHE_HOME']=str(out/'.cache');import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.fonttype':'none','svg.hashsalt':'diagonal-whole-topic-v1'})
 fig,ax0=plt.subplots(1,1,figsize=(8.0,3.2),layout='constrained');axes=[ax0];colors={'source':'#626c76','common':'#426b9a','application':'#70a59a','program':'#bd874e'};data=[]
 maximum=max(x['written_denominator']+x['document_costs']['program'] for x in r['primary'].values())
 for ax,(topic,row) in zip(axes,r['primary'].items()):
  d=row['document_costs'];patches=[('source',0,d['source'],0),('common-written',1,d['common'],0),('application-written',1,d['application'],d['common']),('common-printed',2,d['common'],0),('application-printed',2,d['application'],d['common']),('program',2,d['program'],row['written_denominator'])]
  for name,x,cost,bottom in patches:
   role=name.split('-')[0];gid='bar-'+topic+'-'+name;ax.bar(x,cost,bottom=bottom,color=colors[role],width=.58)[0].set_gid(gid);data.append(dict(id=gid,topic=topic,cost=cost,bottom=bottom,role=role))
  for x,y in [(0,d['source']),(1,row['written_denominator']),(2,row['written_denominator']+d['program'])]:ax.text(x,y+maximum*.025,f'{y:,}',ha='center',fontsize=8)
  ax.set_xticks([0,1,2],['Original','Our written\npapers','Our papers\n+ printed code']);ax.set_ylim(0,maximum*1.20);ax.set_title('Diagonal twistings (N007)');ax.spines[['right','top']].set_visible(False);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
 axes[0].set_ylabel('NFC characters without whitespace')
 from matplotlib.patches import Patch
 fig.legend([Patch(color=colors[x]) for x in ['source','common','application','program']],['Original','Whole common theory','Complete application','Whole program appendix'],loc='outside lower center',ncol=4,frameon=False,fontsize=8)
 fig.savefig(out/'whole_costs.svg',metadata={'Date':None});fig.savefig(out/'whole_costs.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
 (out/'plot_data.json').write_text(json.dumps(dict(primary_only=True,bars=data,actual_rectangles=6,shared_y_limit=maximum*1.20),indent=2)+'\n')


def reader(r,out):
 row=r['primary']['Diagonal'];d=row['document_costs'];fmt=lambda x:f"{float(x['decimal']):.3f}";f=row['comparisons'];u=[]
 for label,unit in [('Whitespace tokens','whitespace_tokens'),('Alphanumeric runs','alphanumeric_units'),('Nonspace characters','characters_without_whitespace'),('Collapsed-space characters','characters_with_collapsed_whitespace'),('Collapsed-space UTF-8 bytes','utf8_bytes_with_collapsed_whitespace')]:
  x=next(x for x in r['rows'] if (x['variant'],x['normalization'],x['unit'])==('calibrated_selected','NFC',unit));u.append(label+' & '+' & '.join(fmt(x['comparisons'][k]) for k in ['written','conditional_application','including_printed_programs'])+r' \\')
 text=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=24mm]{geometry}\usepackage{fontspec,unicode-math,booktabs,graphicx,hyperref}\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}\hypersetup{hidelinks}
\title{A complete-manuscript comparison for diagonal twistings}\author{Human Compression Project}\date{11 October 2026}
\begin{document}\maketitle
The original is Piedade and Tranchida's \emph{Coset geometries acting on their elements: The $j$-diagonals twisting}, arXiv:2608.23223v1 (N007, twelve pages). The replacement comprises the entire common paper \emph{Orbit intersections and regular semidirect geometries} and the entire application \emph{Diagonal twistings and finite tree diagrams}, five pages each. Both use the published, independently reviewed quotient repair. One original is compared, not the thirty-two detailed scientific clauses. N006 is background and receives no whole-original credit here.

\paragraph{The whole topic and the conditional application.}
Let $L$ be the whole source, $U$ the whole common paper, $A$ the complete application and $P$ the complete validation program. The primary coordinate is calibrated selected NFC characters excluding whitespace:
\begin{center}\begin{tabular}{lrr}\toprule
Complete document & Pages & Characters\\\midrule
Original N007 & 12 & @SOURCE@\\
Common theory & 5 & @COMMON@\\
Application & 5 & @APP@\\
Full validation appendix & 2 & @CODE@\\\bottomrule
\end{tabular}\end{center}
All front matter, references, author information, source diagrams' extracted text and the version stamp remain. Only exact repeated furniture and physical page numbers are removed. The common paper is fully charged to this topic regardless of overlaps with any other topic.
\[
 R_{\rm written}=\frac{c(L)}{c(U)+c(A)}=@WRITTEN@,\qquad
 r\mid(U,P)=\frac{c(L)}{c(A)}=@CONDITIONAL@.
\]
The conditional comparison assumes that \emph{the full common paper and the whole declared program have already been acquired}. It is not a whole-topic saving. In the primary coordinate the written replacement is only slightly shorter; including the full validation software makes it longer:
\begin{center}\begin{tabular}{lr}\toprule
Complete denominator & Source/denominator\\\midrule
Written papers & @WRITTEN@\\
Written papers plus full printed program & @PRINTED@\\
Written papers plus full raw program & @RAW@\\\bottomrule
\end{tabular}\end{center}
The raw validation program costs 2,856 nonspace characters. Printed and raw programs are alternatives, never added together. Zero uniform mathematical claims rely on these finite samples. The two operational drivers (6,059 and 2,541) and Lean source (2,587) are separate inventories. Eight scoped declarations do not provide a complete formalization. A factor below one means a longer replacement in that coordinate.
\newpage
\begin{center}\includegraphics[width=\textwidth]{whole_costs.pdf}\end{center}
The stacks charge every common and application page, then the entire printed validation program where shown. One application cannot establish a repeated sawtooth pattern or a minimum proof complexity.

\paragraph{Unit and representation sensitivity.}
The following uses calibrated selected text under NFC:
\begin{center}\begin{tabular}{lrrr}\toprule
Unit & Whole written & Conditional & With printed program\\\midrule
@UNIT_ROWS@
\bottomrule\end{tabular}\end{center}
The exact data retain all five units under NFC and NFKC in three variants: raw untrimmed, raw selected and calibrated selected. They give thirty coordinates and 120 fractions. Raw untrimmed counts preserve page furniture on both sides. The written replacement is longer in whitespace tokens, collapsed-space characters and UTF-8 bytes. These are representation-sensitive lengths; a near-unit primary factor is not evidence of a unit-independent reduction or of deep mathematical compression.

\paragraph{Scope, attribution and costs not measured.}
The accepted contract recovers both diagonal constructions and their full parabolics, exact doubled labels including infinity, invariant quotients under the stated hypertope hypothesis, finite trees with at most one exceptional edge label, and the named classical polytope comparisons. Arbitrary finite diagrams remain an open question in this source contract. The corrected argument uses intersections of maximal-parabolic images in quotient geometries; it does not assert that every quotient is a hypertope. Classical Coxeter embeddings, the polytope correspondence and the named constructions retain their stated outside hypotheses and attributions.

The distinct input audit accepted every complete page, 120 PDF and forty raw-file cells. Seven visible delimiter components whose font encoding produces whitespace were retained, while generated line breaks remained whitespace. The duplicated Form callback affects metadata only: the version stamp stays once in returned text. Seventeen classes checked against actual outlines supply 237 substitutions. Directional diagram strokes are separate visible components, not a full encoding of the graphs.

Full graphics, retained external proofs, unavailable historical software and a complete formalization have unknown cost, not zero. This packet changes no scientific or conjecture credit and leaves every earlier numerical report immutable. Its arithmetic, actual plotted bars and reader require distinct review before these factors are admitted.
\end{document}
'''
 values={'SOURCE':f"{d['source']:,}",'COMMON':f"{d['common']:,}",'APP':f"{d['application']:,}",'CODE':f"{d['program']:,}",'WRITTEN':fmt(f['written']),'CONDITIONAL':fmt(f['conditional_application']),'PRINTED':fmt(f['including_printed_programs']),'RAW':fmt(f['including_raw_programs']),'UNIT_ROWS':'\n'.join(u)}
 for k,v in values.items():text=text.replace('@'+k+'@',v)
 need('@' not in text,'reader fields resolved');(out/'measurement.tex').write_text(text)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--results',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();need(not a.out.exists(),'fresh render');a.out.mkdir(parents=True);r=json.loads(a.results.read_text());plot(r,a.out);reader(r,a.out)
 for i in range(2):
  x=subprocess.run([a.xelatex,'-no-shell-escape','-halt-on-error','-interaction=nonstopmode','measurement.tex'],cwd=a.out,capture_output=True,text=True,timeout=180);(a.out/f'render{i}.log').write_text(x.stdout+x.stderr);need(x.returncode==0,'clean render')
 text=(a.out/'measurement.log').read_text();bad=[x for x in text.splitlines() if any(w in x for w in ['Overfull','Missing character:','LaTeX Warning:'])];need(not bad,'no render diagnostics '+repr(bad))
 from pypdf import PdfReader
 pages=[p.extract_text() or '' for p in PdfReader(a.out/'measurement.pdf').pages];need(len(pages)==2,'two reader pages');report=dict(status='PASS',reader_pages=2,page_text_sha256=[hashlib.sha256(x.encode()).hexdigest() for x in pages],diagnostics=[]);(a.out/'render_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
