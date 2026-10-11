#!/usr/bin/env python3
"""Readable whole-document costs; plotting conventions follow prior project readers."""
import argparse,json,os,subprocess
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/L037_matplotlib')
import matplotlib
matplotlib.use('Agg');matplotlib.rcParams['svg.hashsalt']='L037-fixed'
import matplotlib.pyplot as plt
from compute import accepted_inputs,derive,need

def render_assets(result,out):
 out.mkdir(parents=True,exist_ok=True);c=result['primary'];d=c['document_costs']
 bars=[('Original L037',d['L037'],0,0,0),('Written papers',0,d['U'],d['A1'],0),('With printed program',0,d['U'],d['A1'],c['printed_program_cost']),('With raw program',0,d['U'],d['A1'],c['raw_program_cost'])]
 fig,ax=plt.subplots(figsize=(9,3.4));colors=['#666666','#244d80','#71a3be','#d9a45b'];labels=['Source','Whole common theory','Full application','Complete program']
 for i,b in enumerate(bars):
  left=0
  for j,value in enumerate(b[1:]):
   if value:
    ax.barh(i,value,left=left,color=colors[j],height=.62)
    ax.text(left+value/2,i,f'{value:,}',ha='center',va='center',fontsize=9,color='white' if j<2 else 'black');left+=value
  ax.text(left+210,i,f'{left:,}',va='center',fontsize=9)
 ax.set_yticks(range(4),[b[0] for b in bars]);ax.invert_yaxis();ax.set_xlim(0,22500);ax.set_xlabel('Complete raw PDF text: NFC characters without whitespace\nRaw-program row substitutes the entire raw GAP file for the printed appendix')
 from matplotlib.patches import Patch
 ax.legend(handles=[Patch(facecolor=c,label=l) for c,l in zip(colors,labels)],loc='lower left',bbox_to_anchor=(0,1.01),ncol=4,fontsize=8,frameon=False)
 ax.spines[['top','right']].set_visible(False);ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True);fig.tight_layout()
 for ext in ['svg','pdf','png']:fig.savefig(out/('costs.'+ext),dpi=170,metadata={'Date':None} if ext=='svg' else {'CreationDate':None,'ModDate':None} if ext=='pdf' else None)
 plt.close(fig)
 (out/'plot_data.json').write_text(json.dumps({'primary':[c[k] for k in ['variant','normalization','unit']],'zero_origin':True,'rendered_rectangles':[{'x':float(p.get_x()),'y':float(p.get_y()),'width':float(p.get_width()),'height':float(p.get_height())} for p in ax.patches],'bar_order':[b[0] for b in bars],'components':labels,'bars':[{'label':b[0],'components':dict(zip(labels,b[1:])),'total':sum(b[1:])} for b in bars],'counts_are_full_documents':True,'alternative_programs_not_added_together':True},indent=2)+'\n')
 def nice(n):return f'{n:,}'
 def mathfrac(f):return r'\frac{'+str(f['numerator'])+'}{'+str(f['denominator'])+'}='+f"{f['factor']:.6f}"
 q=c['comparisons'];cond=c['conditional_application']
 tables=[]
 unit_names={'whitespace_tokens':'Whitespace tokens','alphanumeric_units':'Alphanumeric runs','characters_without_whitespace':'Non-space characters','characters_with_collapsed_whitespace':'Collapsed characters','utf8_bytes_with_collapsed_whitespace':'Collapsed UTF-8 bytes'}
 for var,label in [('raw_untrimmed','Complete raw extraction'),('raw_selected','Exact furniture removed'),('calibrated_selected','Furniture removed and eight bracket events calibrated')]:
  rs=[]
  for row in result['coordinates']:
   if row['variant']==var:
    vals=[row['comparisons'][k]['factor'] for k in ['written_papers','including_printed_program','including_raw_program_alternative']]+[row['conditional_application']['factor']]
    rs.append(unit_names[row['unit']]+' & '+row['normalization']+' & '+' & '.join(f'{x:.6f}' for x in vals)+r' \\')
  tables.append(r'\subsection*{'+label+r'}\begin{tabular}{@{}llrrrr@{}}\toprule Unit & Form & Written & Printed & Raw & Conditional\\\midrule '+'\n'.join(rs)+r'\bottomrule\end{tabular}')
 tex=r'''\documentclass[a4paper,11pt]{article}
\usepackage[margin=24mm]{geometry}
\usepackage{fontspec,unicode-math,booktabs,graphicx,amsmath,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\hypersetup{hidelinks}
\setlength{\emergencystretch}{2em}\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\title{Rank contraction: complete written costs}
\author{Human Compression project}
\date{Private numerical candidate; distinct review pending}
\begin{document}\maketitle\raggedright
The original is Brooksbank--Leemans, \emph{Rank reduction of string C-group
representations}, arXiv:1812.01055v2, 3 May 2019. The accepted scope contains
22 source clauses and 20 proof contexts. This comparison measures the complete
source manuscript and the complete common paper and application, with no
free overlap with earlier Topic B theory. It makes no new mathematical or
source-credit claim.

\section*{Written papers}
The primary unit is the number of non-whitespace characters in the complete
raw PDF extraction, normalized to NFC. Titles, author blocks, running furniture,
references and the application’s references-only final page are included.
\begin{center}\begin{tabular}{@{}lrr@{}}\toprule Complete document & Pages & Characters\\\midrule
Original L037 & 6 & SOURCE\\
Whole common theory $U$ & 3 & COMMON\\
Application $A$ & 5 & APP\\
Written replacement $U+A$ & 8 & WRITTEN\\
Complete printed program & 1 & PRINTED\\\bottomrule\end{tabular}\end{center}
The combined written comparison is
\[\frac{c(L037)}{c(U)+c(A)}=WRITTENFRAC.\]
A value below one means that the replacement is longer in this coordinate.
Here the complete written replacement has 1,962 more characters than the source.
\begin{center}\includegraphics[width=\linewidth]{costs.pdf}\end{center}
\newpage
\section*{Including the complete program}
The GAP file \texttt{check\_examples.g} is required for the displayed matrix and
three literal $A_{11}$ examples and includes doubled-edge validation. The uniform
rank-contraction theorem and its infinite families do not depend on its output.
The complete printed appendix costs PRINTED characters; the whole raw program
costs RAW characters. These are alternatives:
\[
\frac{c(L037)}{c(U)+c(A)+c(\mathrm{printed\ program})}=PRINTEDFRAC,
\]
\[
\frac{c(L037)}{c(U)+c(A)+c(\mathrm{raw\ program})}=RAWFRAC.
\]
Neither row combines the printed and raw versions. No line or diagnostic part
is pruned from the whole file.

\section*{After acquiring the theory and program}
Only after acquiring \emph{all} of $U$ and the complete declared program is the
conditional application comparison
\[\frac{c(L037)}{c(A)}=CONDFRAC.\]
The prior acquisition costs are $6,937+2,925=9,862$ characters using the printed
program, or $6,937+2,501=9,438$ using the raw alternative. This conditional ratio
does not assert that the complete replacement is shorter.

\section*{Separate costs and limits}
The complete operational driver has 6,950 raw bytes and 6,114 primary
non-whitespace characters. The complete Lean file has 1,727 raw bytes and 1,280
primary characters. Its four declarations are scoped group-algebra facts;
they do not formalize the full contraction theorem, its classical seeds or the
source. These files are separately inventoried and are not silently included in
the program rows. The mathematical GAP file has 2,680 raw bytes.

The end criterion and stated highest-rank classical constructions, orthogonal
identifications and the prior $A_{11}$ exhaustion remain retained inputs. Their
full proof costs, historical software and full formalization costs are unknown,
not zero. Conjecture 5.1 remains an open research target; no answer or question
credit is claimed.

The source’s three diagrams contain 264 XYCIRC glyph events. Every variant
retains their literal extracted \texttt{/c16} through \texttt{/c23} strings.
Those strings are not a complete measurement of the drawn graphs. Formula and
graph layout costs also remain unknown; no full-visible-text or intrinsic
mathematical-complexity claim is made.

The numerical author separately reviewed the accepted inputs but is the author
of these new calculations, not their independent numerical reviewer. Publication
requires a distinct review. No GAP or Lean computation was repeated for these
numbers.
\newpage
\section*{Metric and extraction sensitivity}
All 30 coordinates use the same whole-document boundary. The five units are
computed under NFC and NFKC. ``Printed'' and ``Raw'' include the corresponding
whole program representation; ``Conditional'' assumes the full prior acquisition
specified above. The JSON and CSV files retain all 120 exact fractions; the table
rounds only the display.

{\small SENSITIVITY}

Exact furniture removal deletes only isolated page numbers and repeated running
headers. It keeps the source’s arXiv banner. The calibrated sensitivity replaces
eight font- and occurrence-bound square-bracket components by their visible
Unicode counterparts, retaining one component per event. Here that changes text
hashes but none of the five metric counts. Printed hyphens remain literal.
\end{document}
'''
 replacements={'SOURCE':nice(d['L037']),'COMMON':nice(d['U']),'APP':nice(d['A1']),'WRITTENFRAC':mathfrac(q['written_papers']),'PRINTEDFRAC':mathfrac(q['including_printed_program']),'RAWFRAC':mathfrac(q['including_raw_program_alternative']),'CONDFRAC':mathfrac(cond),'WRITTEN':nice(c['written_cost']),'PRINTED':nice(c['printed_program_cost']),'RAW':nice(c['raw_program_cost']),'SENSITIVITY':'\n'.join(tables)}
 for token in sorted(replacements,key=len,reverse=True):tex=tex.replace(token,replacements[token])
 (out/'reader.tex').write_text(tex)
 return tex

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=p.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output required');r=derive(*accepted_inputs());render_assets(r,a.out)
 if a.render:
  for i in range(2):
   q=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=a.out,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(a.out/f'render{i}.log').write_bytes(q.stdout);need(q.returncode==0,'XeLaTeX render')
 print('PASS reader and whole-document bars')
if __name__=='__main__':main()
