#!/usr/bin/env python3
"""Build a readable B/C comparison and the complete common/application plots."""
import argparse
import json
import os
from pathlib import Path
import subprocess


def main():
    p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if a.out.exists(): raise ValueError('Fresh output required')
    a.out.mkdir(parents=True)
    os.environ['MPLCONFIGDIR']=str(a.out/'.matplotlib')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'svg.fonttype':'none','svg.hashsalt':'BC-whole-rendered-text',
                        'font.family':'DejaVu Sans','font.size':9})
    result=json.loads(a.results.read_text())
    preamble=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=0.85in]{geometry}
\usepackage{fontspec,unicode-math,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\title{Complete comparisons using the available authored texts}
\author{Human Compression project}\date{}
\begin{document}\maketitle
Two missing PDFs need not prevent comparison of the available manuscripts.
For Buekenhout and Cara's \emph{Some properties of inductively minimal
geometries} (1998, N001), and Bonheure, Buekenhout and Leemans's
\emph{On the Petrials of thin rank 3 geometries} (2001, L108), the complete
authored renderings are available. Both contain all seven printed pages,
including references and final author matter. The saved and newly retrieved
bodies agree. An independent review checked the complete boundaries and
all twenty counts. It removed one website trailer after N001's final address.

The primary comparison counts NFC characters without whitespace in every
complete authored document. Running headers and page numbers remain
included on both sides. N001 and L108 use their literal authored renderings;
all other originals and all replacement papers use untrimmed PDF text.
This is a comparison of the available text representations. Missing figure
information and unverified formula glyphs are not reconstructed.
The previous PDF-only comparisons remain unchanged historical records.

The declared principal-result contracts and their qualifications are exactly
those of the accepted B and C editions. No additional result or conjecture
is proved by measuring them. Each topic pays for its own entire common
theory once. Individual factors assume that theory has been acquired;
Topic C also assumes both complete required programs have been acquired.
There is no discount between topics. Expanded external proofs and complete
graphic costs remain unknown. These lengths are not minimum proof lengths.
'''
    sections=[]
    for topic,title in [('B','Forest coordinates and primitive geometries'),
                        ('C','Chamber operations and binary translations')]:
        r=result['primary'][topic]
        fig,ax=plt.subplots(figsize=(9.5,2.55),layout='constrained')
        labels=['Common'];values=[r['common_theory']];colors=['#426b9a']
        for item in r['individual']:
            labels.extend([item['source'],item['application']]);values.extend([item['source_cost'],item['application_cost']]);colors.extend(['#626c76','#70a59a'])
        for i,(bar,v) in enumerate(zip(ax.bar(range(len(values)),values,color=colors),values)):
            bar.set_gid(f'bar-{topic}-{i}');ax.text(bar.get_x()+bar.get_width()/2,v+max(values)*.02,f'{v:,}',ha='center',fontsize=8)
        ax.set_xticks(range(len(values)),labels);ax.set_ylim(0,max(values)*1.22)
        ax.set_ylabel('Nonspace characters');ax.set_title(title)
        ax.spines[['right','top']].set_visible(False);ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
        fig.savefig(a.out/f'{topic}-costs.svg',metadata={'Date':None})
        fig.savefig(a.out/f'{topic}-costs.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
        s='\n\\newpage\n\\section*{Topic '+topic+': '+title+'}\n'
        s+=r'\begin{center}\begin{tabular}{lrrr}\toprule Source/application & Source cost & Application cost & Conditional factor\\\midrule'+'\n'
        for item in r['individual']:
            s+=f"{item['source']}/{item['application']} & {item['source_cost']} & {item['application_cost']} & {float(item['comparison']['decimal']):.3f}"+r'\\'+'\n'
        s+=r'\bottomrule\end{tabular}\end{center}'+'\n'
        s+=f"The entire common paper costs {r['common_theory']:,} characters; the four applications cost {r['applications']:,}. Thus\n"
        s+=r'\[R_'+topic+r'=\frac{'+str(r['source_sum'])+'}{'+str(r['common_theory'])+'+'+str(r['applications'])+r'}=\frac{'+str(r['source_sum'])+'}{'+str(r['written_denominator'])+'}='+f"{float(r['whole']['written']['decimal']):.6f}."+r'\]'+'\n'
        if topic=='B':
            s+='These proofs require no finite mathematical program. All four sources remain in the numerator and all four applications remain in the denominator.\n'
        else:
            s+=f"The complete printed program appendix costs {r['printed_program_cost']:,}, giving {float(r['whole']['including_printed_programs']['decimal']):.6f}. Both whole raw programs cost {r['raw_program_alternative']:,} instead, giving {float(r['whole']['including_raw_programs']['decimal']):.6f}. These program representations are alternatives, never two simultaneous charges.\n"
        s+=r'\begin{center}\includegraphics[width=\textwidth]{'+topic+r'-costs.pdf}\end{center}'+'\n'
        s+='The graph shows acquisition of the complete common paper, followed by each matched original and application in the established application order. It does not by itself establish a recurring sawtooth pattern.\n'
        s+=r'\paragraph{Unit sensitivity.} All documents remain untrimmed in this table.\begin{center}\begin{tabular}{lr}\toprule Unit & Whole written factor\\\midrule'+'\n'
        names=['Whitespace words','Alphanumeric units','Nonspace characters','Characters, collapsed spaces','UTF-8 bytes, collapsed spaces']
        rows=[x for x in result['rows'] if x['topic']==topic and x['PDF_variant']=='raw_untrimmed' and x['normalization']=='NFC']
        for name,row in zip(names,rows):s+=f"{name} & {float(row['whole']['written']['decimal']):.3f}"+r'\\'+'\n'
        s+=r'\bottomrule\end{tabular}\end{center}'+'\n'
        s+='The machine-readable results retain both normalizations and all five units. Comparisons with selected or calibrated PDF text are labelled separately as mixed-boundary sensitivities; they are not the primary factors above. Literal rendered-source counts remain fixed in those variants.\n'
        sections.append(s)
    (a.out/'measurement.tex').write_text(preamble+''.join(sections)+'\n\\end{document}\n')
    for i in range(2):
        run=subprocess.run(['/opt/homebrew/bin/xelatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','measurement.tex'],cwd=a.out,capture_output=True,text=True)
        (a.out/f'render{i}.log').write_text(run.stdout+run.stderr)
        if run.returncode:raise ValueError('Reader failed to render')
    log=(a.out/'measurement.log').read_text()
    if any(x in log for x in ['Overfull','Missing character:','LaTeX Warning:']):raise ValueError('Reader diagnostics')
    from pypdf import PdfReader
    if len(PdfReader(a.out/'measurement.pdf').pages)!=3:raise ValueError('Three complete reader pages required')
    print('PASS: three-page reader and both full common/application plots')


if __name__=='__main__':main()
