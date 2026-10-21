"""Plot declared complete written costs; emit every program sensitivity in CSV.
No primary text. Graphs describe one acquisition and three completed applications,
not a repeated sawtooth or a historical discovery chronology.
"""
import argparse,csv,json,os
os.environ.setdefault("MPLCONFIGDIR","/private/tmp/topic-e-matplotlib")
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--result',type=Path,required=True);ap.add_argument('--out-dir',type=Path,required=True);a=ap.parse_args()
 r=json.loads(a.result.read_text());a.out_dir.mkdir(parents=True,exist_ok=True)
 primary=r['chronology']['NFC']['characters_without_whitespace'];x=list(range(4));labels=['Shared theory','L083 / A1','L079 / A2','L021 / A3']
 colors=['#203a60','#969da4','#167259']
 fig,axes=plt.subplots(1,2,figsize=(11.5,4.9),gridspec_kw={'width_ratios':[1.12,1]})
 series=[('Historical papers','source',colors[0]),('Previous complete proof','old_written',colors[1]),('Current complete proof','new_written',colors[2])]
 for label,key,color in series:
  axes[0].plot(x,primary[key+'_cumulative'],marker='o',linewidth=2.1,color=color,label=label)
 for j,(label,key,color) in enumerate(series):
  axes[1].bar([v+(j-1)*.25 for v in x],primary[key+'_marginal'],width=.23,color=color,label=label)
 for ax,title in zip(axes,['Cumulative manuscript cost','Cost acquired at each stage']):
  ax.set_title(title,loc='left',fontsize=12,pad=12);ax.set_xticks(x,labels,fontsize=9);ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_:f'{int(v):,}'));ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True);ax.spines[['top','right']].set_visible(False)
 axes[0].set_ylabel('NFC characters without whitespace',fontsize=10)
 for label,key,color in series:
  value=primary[key+'_cumulative'][-1]
  axes[0].annotate(f'{value:,}',xy=(3,value),xytext=(-6,8 if key!='new_written' else -16),textcoords='offset points',ha='right',color=color,fontsize=10)
 axes[0].set_ylim(0,max(primary['source_cumulative'])*1.135)
 axes[1].set_ylim(0,max(max(primary[k+'_marginal']) for _,k,_ in series)*1.115)
 handles,legend=axes[0].get_legend_handles_labels();fig.legend(handles,legend,loc='lower center',ncol=3,frameon=False,bbox_to_anchor=(.5,.07),fontsize=10)
 fig.suptitle('Three papers: common theory followed by complete applications',fontsize=13,y=.98)
 fig.text(.5,.025,'Written manuscripts in full; umbrella paid once. Required programs and diagnostic sensitivity are tabulated separately.',ha='center',fontsize=9)
 fig.subplots_adjust(left=.08,right=.98,top=.84,bottom=.23,wspace=.26)
 for ext in ['svg','pdf']:
  kw={'metadata':{'Date':None}} if ext=='svg' else {'metadata':{'CreationDate':None,'ModDate':None}}
  fig.savefig(a.out_dir/('costs.'+ext),**kw)
 fig.savefig(a.out_dir/'costs.png',dpi=150)
 plt.close(fig)
 with (a.out_dir/'costs.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['normalization','metric','series','stage','marginal','cumulative'])
  for form,metrics in r['chronology'].items():
   for metric,ch in metrics.items():
    for prefix in ['source','old_written','old_with_code','new_written','new_with_required','new_including_validation']:
     for i,stage in enumerate(ch['stage_order']):w.writerow([form,metric,prefix,stage,ch[prefix+'_marginal'][i],ch[prefix+'_cumulative'][i]])
 with (a.out_dir/'comparisons.csv').open('w',newline='') as f:
  w=csv.writer(f);fields=[k for k,v in r['comparisons']['NFC']['characters_without_whitespace'].items() if not isinstance(v,dict)];w.writerow(['normalization','metric']+fields)
  for form,metrics in r['comparisons'].items():
   for metric,c in metrics.items():w.writerow([form,metric]+[c[k] for k in fields])

 with (a.out_dir/'conditional.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['normalization','metric','source','source_full_manuscript','complete_local_application','factor','condition'])
  for form,metrics in r['comparisons'].items():
   for metric,c in metrics.items():
    for key,row in c['conditional_application_factors'].items():
     w.writerow([form,metric,key,row['source_full_manuscript'],row['complete_local_application'],row['factor'],c['conditional_application_basis']])
if __name__=='__main__':main()
