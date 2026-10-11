#!/usr/bin/env python3
"""Plot exactly the frozen Topic A extraction coordinate; unknown costs stay unknown."""
from pathlib import Path
import csv, hashlib, json, os, tempfile
HERE=Path(__file__).resolve().parent
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir())/'hc-topic-a-matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def main():
    manifest=json.loads((HERE/'numerical_manifest.json').read_text())
    source=next(r for r in manifest['exports'] if r['path']=='results.json')
    data=(HERE/'measurement.json').read_bytes()
    if hashlib.sha256(data).hexdigest()!=source['sha256']:
        raise ValueError('Frozen numerical result binding')
    d=json.loads(data)
    c={k:v['metrics']['NFC']['calibrated_selected']['characters_without_whitespace']
       for k,v in d['documents'].items()}
    sources=['L032','L034','F016','F013','L035','N009']
    apps=['A1','A2','A3','A4','A5','A6']
    # At stage zero no manuscript has been acquired in this declared sequence.
    # This is not an estimate of the cost of historical libraries or programs.
    source_cumulative=[0];written=[c['U_A']];with_program=[c['U_A']+c['code']]
    for s,a in zip(sources,apps):
        source_cumulative.append(source_cumulative[-1]+c[s])
        written.append(written[-1]+c[a])
        with_program.append(with_program[-1]+c[a])
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,
       'axes.spines.top':False,'axes.spines.right':False,'svg.hashsalt':'topic-a-six-final'})
    fig,(top,bottom)=plt.subplots(2,1,figsize=(11.7,8.4),gridspec_kw={'height_ratios':[1,1.15]})
    orange,blue,pale='#ae5329','#175d75','#7baebd'
    width=.29
    top.bar([i-.16 for i in range(1,7)],[c[s] for s in sources],width,
            color=orange,label='Full source manuscript')
    top.bar([i+.16 for i in range(7)],[c['U_A']]+[c[a] for a in apps],width,
            color=blue,label='Our written paper')
    top.bar([.16],[c['code']],width,bottom=[c['U_A']],color=pale,
            label='Complete required program')
    for i,s,a in zip(range(1,7),sources,apps):
        top.text(i-.16,c[s]+2100,f'{c[s]:,}',ha='center',fontsize=8)
        top.text(i+.16,c[a]+2100,f'{c[a]:,}',ha='center',fontsize=8)
    top.text(.16,c['U_A']/2,f"U: {c['U_A']:,}",ha='center',va='center',color='white',fontsize=9)
    top.text(.16,c['U_A']+c['code']/2,f"Code: {c['code']:,}",ha='center',va='center',fontsize=9)
    top.set_xticks(range(7),['Acquisition']+[f'{s} / {a}' for s,a in zip(sources,apps)])
    top.set_xlim(-.5,6.55);top.set_ylim(0,112000)
    top.set_title('The full common theory and program are acquired once',loc='left',pad=12)
    top.legend(loc='upper right',frameon=False,fontsize=10)
    bottom.plot(range(7),source_cumulative,color=orange,marker='o',label='Full source manuscripts')
    bottom.plot(range(7),written,color=blue,marker='s',linestyle='--',label='Written papers')
    bottom.plot(range(7),with_program,color=blue,marker='s',label='Including the required program')
    bottom.set_xticks(range(7),['Acquisition']+[f'After {a}' for a in apps])
    bottom.set_xlim(-.12,6.62);bottom.set_ylim(0,217000)
    bottom.set_title('Cumulative costs in the stated application sequence',loc='left',pad=12)
    for values,color,offset in [(source_cumulative,orange,7),(with_program,blue,-8),(written,blue,0)]:
        bottom.annotate(f'{values[-1]:,}',(6,values[-1]),xytext=(8,offset),
                        textcoords='offset points',color=color,fontsize=10)
    bottom.legend(loc='upper left',frameon=False,fontsize=9)
    for ax in [top,bottom]:
        ax.set_ylabel('NFC characters other than whitespace')
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{int(x):,}'))
        ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
    fig.suptitle('Topic A: six applications of one common theory',fontsize=17,y=.98)
    fig.text(.5,.02,'Fixed accounting sequence, not discovery chronology. No repeated sawtooth is established.\n'
             'Image labels, graphical structure, retained proofs and historical programs remain unpriced.',
             ha='center',fontsize=10)
    fig.tight_layout(rect=(0,.07,1,.95),h_pad=2.5)
    fig.savefig(HERE/'costs.svg',metadata={'Creator':'Human Compression audit','Date':None})
    fig.savefig(HERE/'costs.pdf',metadata={'Creator':'Human Compression audit','CreationDate':None,'ModDate':None})
    with (HERE/'costs.csv').open('w',newline='') as out:
        writer=csv.writer(out);writer.writerow(['stage','source_cumulative','written_cumulative','including_complete_program_cumulative'])
        writer.writerows(zip(['acquisition']+apps,source_cumulative,written,with_program))
    with (HERE/'sensitivity.csv').open('w',newline='') as out:
        writer=csv.writer(out);writer.writerow(['normalization','variant','metric','full_sources','full_written_papers','complete_printed_program_appendix','written_factor','including_program_factor'])
        for form,variants in d['factors'].items():
            for variant,metrics in variants.items():
                for metric,row in metrics.items():
                    cc=row['costs'];writer.writerow([form,variant,metric,cc['full_sources'],cc['full_written_papers'],cc['complete_printed_program_appendix'],row['written_topic']['reduced_fraction'],row['program_inclusive_topic']['reduced_fraction']])

if __name__=='__main__':main()
