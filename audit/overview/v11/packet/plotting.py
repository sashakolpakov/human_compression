"""Current cost charts omit all numeric bars for held rows."""
from pathlib import Path
COLORS={'source':'#344354','common':'#286e99','applications':'#81bdb0','application':'#81bdb0'}
def specs(data):return {k:dict(kind=k,rows=data[k],whole=k=='whole_topics')for k in ['whole_topics','conditional_1','conditional_2']}
def geometry(spec):
 rows=spec['rows'];whole=spec['whole'];W=777.6;H=604.8 if whole else 655.2
 maxcost=max(max(r['values']['source'],sum(v for k,v in r['values'].items()if k!='source'))for r in rows if not r['held']);sx=W*.77/(maxcost*1.08);sy=H*.84/len(rows);res={}
 for i,r in enumerate(rows):
  if r['held']:continue
  v=r['values'];x=W*.19;y=H*.08+(i+.5-.15-.115)*sy;res['bar-'+r['id']+'-source']=[x,y,v['source']*sx,.23*sy]
  y=H*.08+(i+.5+.15-.115)*sy;start=0
  for key in (['common','applications']if whole else ['application']):res['bar-'+r['id']+'-'+key]=[x+start*sx,y,v[key]*sx,.23*sy];start+=v[key]
 return res,H

def draw(spec,out):
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.patches import Patch
 from matplotlib.ticker import FuncFormatter
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'listing-symmetry-correction','pdf.fonttype':42})
 rows=spec['rows'];whole=spec['whole'];fig,ax=plt.subplots(figsize=(10.8,8.4 if whole else 9.1));fig.subplots_adjust(left=.19,right=.96,bottom=.08,top=.92)
 mx=max(max(r['values']['source'],sum(v for k,v in r['values'].items()if k!='source'))for r in rows if not r['held']);ax.set_xlim(0,mx*1.08);ax.set_ylim(len(rows)-.5,-.5)
 for i,r in enumerate(rows):
  if r['held']:
   ax.text(mx*.02,i,'awaiting matched code boundary',va='center',color='#934131',fontsize=10);continue
  v=r['values'];rect=ax.barh(i-.15,v['source'],height=.23,color=COLORS['source']);rect[0].set_gid('bar-'+r['id']+'-source');start=0
  for k in (['common','applications']if whole else ['application']):
   rect=ax.barh(i+.15,v[k],left=start,height=.23,color=COLORS[k],edgecolor='white',linewidth=.35);rect[0].set_gid('bar-'+r['id']+'-'+k);start+=v[k]
 labels=[r['id']if whole else r['id']+' / '+r['topic']for r in rows];ax.set_yticks(range(len(rows)),labels);ax.tick_params(axis='y',length=0,pad=7,labelsize=9)
 ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True);ax.xaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{int(x):,}'));ax.set_xlabel('Characters without whitespace (each row retains its published extraction convention)')
 for s in ['top','right','left']:ax.spines[s].set_visible(False)
 handles=[Patch(color=COLORS['source'],label='Complete original(s)')]
 if whole:handles.append(Patch(color=COLORS['common'],label='Whole common theory'))
 handles.append(Patch(color=COLORS['applications'],label='Complete application(s)'))
 fig.legend(handles=handles,ncol=len(handles),loc='upper center',frameon=False)
 fig.text(.575,.943,'Whole topics: full common theory and all applications charged' if whole else 'Conditional: whole common theory and required premises already acquired',ha='center',fontsize=9)
 fig.savefig(out/(spec['kind']+'.svg'),metadata={'Date':None});fig.savefig(out/(spec['kind']+'.pdf'),metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
