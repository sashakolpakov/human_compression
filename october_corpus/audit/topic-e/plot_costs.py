"""Plot the fixed two-application audit; no inferred or missing costs become zero."""
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

HERE = Path(__file__).resolve().parent


def main():
    data = json.loads((HERE/'author_measurement.json').read_text())
    c = {k:v['NFC']['characters_without_whitespace'] for k,v in data['costs'].items()}
    m = data['comparisons']['NFC']['characters_without_whitespace']
    plt.rcParams.update({'font.size':10, 'axes.spines.top':False,
                         'axes.spines.right':False, 'svg.hashsalt':'topic-e-intake-audit'})
    fig, (left,right) = plt.subplots(1,2,figsize=(11.6,4.8))
    orange, blue, pale = '#b35c28','#17667b','#70a5b4'
    x = [0,1,2]; width = .34
    # At acquisition there is no historical manuscript in this sequence;
    # this is not a zero estimate of background or historical program cost.
    left.bar([.83,1.83],[c['L083'],c['L079']],width,label='Full source paper',color=orange)
    left.bar([.17,1.17,2.17],[c['U_E'],c['A1'],c['A2']],width,
             label='Our written proof',color=blue)
    left.bar([.17],[c['Code']],width,bottom=[c['U_E']],
             label='Required shared program',color=pale)
    for xpos,value in [(.17,c['U_E']+c['Code']),(.83,c['L083']),
                       (1.17,c['A1']),(1.83,c['L079']),(2.17,c['A2'])]:
        left.text(xpos,value+550,f'{value:,}',ha='center',fontsize=8)
    left.set_xticks(x,['Acquisition','L083 / A1','L079 / A2'])
    left.set_ylim(0,28500);left.set_title('Acquisition and application costs')
    left.set_ylabel('NFC characters, whitespace removed')
    left.legend(loc='upper right',fontsize=8,frameon=False)
    right.plot(x,[0]+m['source_cumulative'],color=orange,marker='o',label='Full source manuscripts')
    right.plot(x,[c['U_E']]+m['replacement_written_cumulative'],color=blue,
               linestyle='--',marker='s',label='Our complete manuscripts')
    right.plot(x,[c['U_E']+c['Code']]+m['replacement_with_code_cumulative'],
               color=blue,marker='s',label='Our manuscripts + required program')
    right.set_xticks(x,['Acquisition','After A1','After A2'])
    right.set_ylim(0,49000);right.set_title('Cumulative costs in the fixed sequence')
    for value,label,offset in [(41793,'41,793',850),(36968,'36,968',450),(32214,'32,214',-1800)]:
        right.annotate(label,(2,value),xytext=(5,offset/200),textcoords='offset points',fontsize=9)
    right.set_xlim(-.08,2.35)
    right.legend(loc='upper left',fontsize=8,frameon=False)
    for ax in (left,right):
        ax.yaxis.set_major_formatter(FuncFormatter(lambda value,pos:f'{int(value):,}'))
        ax.grid(axis='y',alpha=.17);ax.set_axisbelow(True)
    fig.suptitle('Topic E: two applications, full source manuscripts',fontsize=14)
    fig.text(.5,.025,'Historical program cost is unknown. Classical inputs are retained. L021 is excluded.\n'
             'This shows one acquisition and two applications; no repeated sawtooth is established.',
             ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.12,1,.92))
    for ext in ('svg','pdf'):
        fig.savefig(HERE/f'costs.{ext}',metadata={'Creator':'Human Compression audit'})
    with (HERE/'costs.csv').open('w',newline='') as stream:
        writer=csv.writer(stream)
        writer.writerow(['stage','full_source_cumulative','our_written_cumulative',
                         'our_written_and_required_program_cumulative'])
        for row in zip(['acquisition','A1','A2'],[0]+m['source_cumulative'],
                       [c['U_E']]+m['replacement_written_cumulative'],
                       [c['U_E']+c['Code']]+m['replacement_with_code_cumulative']):
            writer.writerow(row)


if __name__=='__main__':
    main()
