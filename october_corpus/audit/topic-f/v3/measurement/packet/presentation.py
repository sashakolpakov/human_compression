"""Complete manuscript costs and coarse source/application acquisition graph."""
import os,json
from calculate import UNITS,APP,SOURCES
COLORS={'L014':'#687d8d','L007':'#94a5b2','U':'#426b9a','A1':'#499383','A2':'#8bb8a4','CODE':'#b98249','programs':'#d1a573'}

def graph(r):
 c=r['primary']['costs'];raw=r['primary']['raw_costs']
 return dict(scope='Coarse whole-document acquisition graph, not a theorem dependency DAG or a minimal proof claim.',unit='raw untrimmed NFC characters without whitespace',nodes=[dict(id=k,title=t,role=role,pages=n,cost=c[k])for k,t,role,n in [('L014','String C-groups of order 4p^m','original',12),('L007','Chiral 3-polytopes of order 2p^m','original',22),('U','Odd kernels, cyclotomic modules and cyclic carries','whole_common',7),('A1','Regular polyhedra with an odd kernel of index four','whole_application',5),('A2','Chiral polyhedra of order twice an odd prime power','whole_application',6)]]+[dict(id='programs',title='All nine complete validation programs',role='validation_not_uniform_proof_premise',printed_pages=9,printed_cost=c['CODE'],raw_alternative_cost=raw['programs'],literal_bytes=25501),dict(id='retained',title='Retained classical and classification inputs',role='retained_input',cost=None)],edges=[dict(source='U',target=k,kind='proof_input')for k in APP]+[dict(source='retained',target=k,kind='retained_input')for k in ['U']+APP]+[dict(source=k,target=a,kind='source_correspondence')for k,a in zip(SOURCES,APP)]+[dict(source='programs',target=k,kind='validation_association')for k in APP],accounting='The whole U and both applications remain charged. Conditional comparisons require the whole common theory and actual retained mathematical premises. All9 optional validation programs are inventoried separately, not acquired as a condition of the written comparison. Outside proof and graphical costs remain unknown. No node-count ratio.')

def figures(r,out):
 os.environ['MPLCONFIGDIR']=str(out/'.matplotlib');os.environ['XDG_CACHE_HOME']=str(out/'.cache')
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.patches import FancyBboxPatch,FancyArrowPatch,Patch
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'svg.hashsalt':'expanded-F-symmetric-whole-documents'})
 c=r['primary']['costs'];raw=r['primary']['raw_costs'];fig,axs=plt.subplots(1,3,figsize=(11.4,4.5));fig.subplots_adjust(left=.075,right=.98,top=.86,bottom=.30,wspace=.42)
 groups=[('written',axs[0],[('Originals',[(k,c[k])for k in SOURCES]),('Papers',[(k,c[k])for k in ['U']+APP])],80000),('validation',axs[1],[('Printed',[('CODE',c['CODE'])]),('Raw',[('programs',raw['programs'])])],30000),('conditional',axs[2],[('L014',[('L014',c['L014'])]),('A1',[('A1',c['A1'])]),('L007',[('L007',c['L007'])]),('A2',[('A2',c['A2'])])],50000)]
 specs=[]
 for panel,ax,bars,limit in groups:
  for i,(label,parts)in enumerate(bars):
   base=0
   for key,val in parts:
    gid=f'cost-{panel}-{i}-{key}';b=ax.bar(i,val,bottom=base,color=COLORS[key])[0];b.set_gid(gid);specs.append(dict(id=gid,panel=panel,value=val,bottom=base,x=i));base+=val
   ax.text(i,base+limit*.025,f'{base:,}',ha='center',fontsize=10 if panel=='conditional' else 12)
  ax.set_xticks(range(len(bars)),[x[0]for x in bars]);ax.set_ylim(0,limit);ax.tick_params(axis='x',labelsize=11);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
 axs[0].set_title('Whole written topic');axs[0].set_ylabel('NFC nonspace characters');axs[1].set_title('Optional checks: costs only');axs[2].set_title('Conditional applications')
 labels={'L014':'Original L014','L007':'Original L007','U':'Whole common','A1':'Whole regular application','A2':'Whole chiral application','CODE':'Printed programs','programs':'Raw programs (alternative)'}
 fig.legend(handles=[Patch(facecolor=COLORS[k],label=v)for k,v in labels.items()],loc='lower center',bbox_to_anchor=(.5,.047),ncol=4,fontsize=10,frameon=False)
 fig.text(.5,.012,'Conditional figures require the whole common paper and retained premises; optional checks are separate.',ha='center',fontsize=10)
 fig.savefig(out/'costs.svg',metadata={'Date':None});fig.savefig(out/'costs.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
 (out/'plot_data.json').write_text(json.dumps(dict(bars=specs,bar_count=len(specs),program_representations_alternative=True),indent=2)+'\n')
 g=graph(r);(out/'document_graph.json').write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n')
 fig,ax=plt.subplots(figsize=(11.4,5.0));ax.set_xlim(0,12);ax.set_ylim(-.6,6.8);ax.axis('off')
 xy={'retained':(6,3.0),'L014':(2,5.8),'U':(6,5.8),'L007':(10,5.8),'A1':(2,3.0),'A2':(10,3.0),'programs':(6,.7)}
 labels={'retained':'Retained outside proofs\nFull costs unknown','L014':f"Original L014\n12 pages · {c['L014']:,}",'L007':f"Original L007\n22 pages · {c['L007']:,}",'U':f"Whole common paper\n7 pages · {c['U']:,}",'A1':f"Regular application A1\n5 pages · {c['A1']:,}",'A2':f"Chiral application A2\n6 pages · {c['A2']:,}",'programs':f"Nine whole validation programs\n{c['CODE']:,} printed / {raw['programs']:,} raw"}
 boxes={}
 for key,(x,y)in xy.items():
  boxes[key]=FancyBboxPatch((x-1.8,y-.62),3.6,1.24,boxstyle='round,pad=.025',facecolor='#edf5f1'if key in APP else'#f2f4f6',edgecolor='#77848c',lw=.8,zorder=2);boxes[key].set_gid('node-'+key);ax.add_patch(boxes[key]);ax.text(x,y,labels[key],ha='center',va='center',fontsize=12,zorder=3)
 for e in g['edges']:
  s,t=e['source'],e['target'];style={'source_correspondence':'--','validation_association':':'} .get(e['kind'],'-')
  rad=0
  a=FancyArrowPatch(xy[s],xy[t],patchA=boxes[s],patchB=boxes[t],connectionstyle=f'arc3,rad={rad}',arrowstyle='-|>',mutation_scale=12,lw=1.2,linestyle=style,color='#667984',shrinkA=4,shrinkB=4,zorder=1);a.set_gid('edge-'+s+'-'+t);ax.add_patch(a)
 ax.text(6,-.45,'Solid: proof input → use.   Dashed: source correspondence.   Dotted: validation, not a proof premise.',ha='center',fontsize=10)
 fig.tight_layout(pad=.3);fig.savefig(out/'document_graph.svg',metadata={'Date':None});fig.savefig(out/'document_graph.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)

def reader(r):
 from pathlib import Path
 p=r['primary'];c=p['costs'];raw=p['raw_costs'];t=p['totals'];f=p['comparisons']
 tex=(Path(__file__).resolve().parent/'reader_template.tex').read_text()
 vals={'S1':c['L014'],'S2':c['L007'],'S':t['source'],'U':c['U'],'A1':c['A1'],'A2':c['A2'],'W':t['written'],'CODE':c['CODE'],'RAW':raw['programs'],'MID':c['U']+c['A1'],'DRIVERS':raw['operational_drivers'],'FORMAL':raw['formal_files']}
 for k,n in [('RW','written'),('C1','conditional_L014'),('C2','conditional_L007')]:vals[k]=f"{float(f[n]['decimal']):.6f}"
 names=['Whitespace tokens','Alphanumeric units','Nonspace characters','Collapsed-space characters','Collapsed-space UTF-8 bytes'];lines=[]
 for unit,label in zip(UNITS,names):
  x=next(x for x in r['coordinates']if(x['variant'],x['normalization'],x['unit'])==('raw_untrimmed','NFC',unit));lines.append(label+' & '+' & '.join(f"{float(y['decimal']):.3f}"for y in x['comparisons'].values())+r' \\')
 vals['METRICS']='\n'.join(lines);lines=[]
 for x in r['coordinates']:
  if x['unit']!=UNITS[2]:continue
  label={'raw_untrimmed':'Untrimmed','raw_selected':'Selected','calibrated_selected':'Calibrated'}[x['variant']];lines.append(label+' & '+x['normalization']+' & '+' & '.join(f"{float(y['decimal']):.3f}"for y in x['comparisons'].values())+r' \\')
 vals['VARIANTS']='\n'.join(lines)
 for k,v in vals.items():tex=tex.replace('@'+k+'@',str(v))
 return tex
